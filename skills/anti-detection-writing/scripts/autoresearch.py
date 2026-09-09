#!/usr/bin/env python3
"""Durable local ledger for an agent-driven writing experiment; executes no agents or scans."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
import unicodedata

START = b"## Write and review\n"
END = b"## Measure only when requested\n"
DEFAULTS = dict(schema_version=1, max_candidates=3, max_rounds=1,
                max_detector_calls=8, max_detector_words=1200,
                reserved_confirmation_calls=4, reserved_confirmation_words=500,
                max_elapsed_seconds=2700, min_development_pairs=2,
                min_holdout_pairs=2, primary_detector="gptzero",
                min_mean_ai_reduction=5, max_case_regression=0, scan_scope="full_text")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def safe_id(value):
    require(isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", value),
            "IDs must contain only letters, numbers, underscores and hyphens")
    return value


def clean_path(path):
    path = Path(path).absolute()
    require(".." not in path.parts, "Parent traversal is forbidden")
    require(not any(p.is_symlink() for p in (path, *path.parents)), "Symlinks are forbidden")
    return path


def read_json(path):
    return json.loads(clean_path(path).read_text(encoding="utf-8"))


def text_bytes(path):
    data = clean_path(path).read_bytes()
    text = data.decode("utf-8")
    require(text.strip(), "Text cannot be empty")
    require(not any(unicodedata.category(c) == "Cf" or c in "\u034f\u2800" for c in text),
            "Hidden Unicode markers are forbidden")
    return data


def scan_scope(state):
    scope = state["config"].get("scan_scope", "full_text")
    require(scope in ("full_text", "prose_only"), "Unsupported scan scope")
    return scope


def measured_input(row):
    """Legacy outputs measured the full message; new outputs freeze both identities."""
    scope = row.get("scan_scope", "full_text")
    require(scope in ("full_text", "prose_only"), "Unsupported output scan scope")
    if scope == "prose_only":
        return dict(path=row["detector_input_path"], sha256=row["detector_input_sha256"])
    return dict(path=row["path"], sha256=row["sha256"])


def prose_bytes(data, manifest):
    """Remove declared complete lines only; judging whether they are code is separate."""
    require(isinstance(manifest, dict) and set(manifest) ==
            {"schema_version", "full_message_sha256", "ranges"}, "Invalid code-ranges manifest")
    require(type(manifest["schema_version"]) is int and manifest["schema_version"] == 1,
            "Unsupported code-ranges schema")
    require(manifest["full_message_sha256"] == digest(data), "Code ranges full-message hash mismatch")
    require(isinstance(manifest["ranges"], list), "Code ranges must be a list")
    text, cursor, kept = data.decode("utf-8"), 0, []
    for span in manifest["ranges"]:
        require(isinstance(span, list) and len(span) == 2
                and all(type(offset) is int for offset in span), "Code ranges need integer offset pairs")
        start, end = span
        require(cursor <= start < end <= len(text), "Code ranges must be ordered, nonoverlapping and in bounds")
        require((start == 0 or text[start - 1] == "\n")
                and (end == len(text) or text[end - 1] == "\n"), "Code ranges must cover complete lines")
        require(text[start:end].strip(), "Code ranges cannot contain only whitespace")
        kept.append(text[cursor:start])
        cursor = end
    kept.append(text[cursor:])
    prose = "".join(kept).encode("utf-8")
    require(prose.strip(), "Measured prose cannot be empty")
    return prose


def measurement_noop(outputs):
    return len(outputs) == 2 and measured_input(outputs["baseline"])["sha256"] == measured_input(outputs["candidate"])["sha256"]


def tree_files(root):
    root = clean_path(root)
    result = {}
    for path in sorted(root.rglob("*")):
        clean_path(path)
        if path.is_file() and "__pycache__" not in path.parts and not path.name.endswith(".pyc"):
            result[path.relative_to(root).as_posix()] = path.read_bytes()
    require("SKILL.md" in result, "Skill directory must contain SKILL.md")
    return result


def tree_hash(files):
    return digest(encode({name: digest(data) for name, data in files.items()}))


def save_artifact(run, state, name, data):
    require(not (run / name).exists(), f"Artifact already exists: {name}")
    path = clean_path(run / ".pending/files" / name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    state["artifacts"][name] = digest(data)
    return name


def save_state(run, state):
    temp = run / ".state.tmp"
    clean_path(temp)
    with temp.open("wb") as stream:
        stream.write(encode(state))
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, run / "state.json")
    fd = os.open(run, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def recover_transaction(run):
    """Finish a journaled commit, or discard files from an uncommitted command."""
    pending = clean_path(run / ".pending")
    if not pending.exists():
        return
    for path in pending.rglob("*"):
        clean_path(path)
    if (pending / "state.json").exists():
        state = read_json(pending / "state.json")
        for name, expected in state["artifacts"].items():
            destination = clean_path(run / name)
            require(destination.is_relative_to(run), "Journal artifact escapes run")
            source = clean_path(pending / "files" / name)
            if source.exists():
                require(digest(source.read_bytes()) == expected, "Journal artifact changed")
                require(not destination.exists(), "Journal would overwrite an artifact")
                destination.parent.mkdir(parents=True, exist_ok=True)
                os.replace(source, destination)
            require(digest(destination.read_bytes()) == expected, "Journal artifact missing or changed")
        save_state(run, state)
    shutil.rmtree(pending)


@contextmanager
def locked(run, initialize=False):
    run = clean_path(run)
    if initialize:
        require(not run.exists() or all(p.name in (".lock", ".pending") for p in run.iterdir()), "Run directory must be empty")
        run.mkdir(parents=True, exist_ok=True)
    require(run.is_dir(), "Run directory does not exist")
    clean_path(run / ".lock")
    with (run / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        recover_transaction(run)
        if initialize:
            require(not (run / "state.json").exists(), "Run already initialized")
            state = {"schema_version": 1, "artifacts": {}, "candidates": {},
                     "outputs": {}, "reviews": {}, "attempts": {}, "selected": None}
        else:
            state = read_json(run / "state.json")
            for name, expected in state["artifacts"].items():
                path = clean_path(run / name)
                require(path.is_relative_to(run), "Artifact escapes run directory")
                require(digest(path.read_bytes()) == expected, f"Frozen artifact changed: {name}")
            require({k: state[k] for k in ("started_at", "baseline_tree_sha256")} == read_json(run / "frozen/run.json"), "Frozen run metadata changed")
            require(encode(state["config"]) == (run / "frozen/config.json").read_bytes(), "Frozen config differs from state")
            require(encode(state["corpus"]) == (run / "frozen/cases.json").read_bytes(), "Frozen corpus differs from state")
            require(tree_hash(tree_files(run / "baseline")) == state["baseline_tree_sha256"], "Frozen baseline tree changed")
            for key, candidate in state["candidates"].items():
                require(candidate == read_json(run / "candidates" / safe_id(key) / "proposal.json"), "Frozen proposal metadata changed")
                require(tree_hash(tree_files(run / "candidates" / safe_id(key) / "skill")) == candidate["tree_sha256"], "Frozen candidate tree changed")
            for case_id, outputs in state["outputs"].items():
                for arm, row in outputs.items():
                    require(arm in ("baseline", "candidate"), "Invalid output arm")
                    require(row == read_json(run / "outputs" / safe_id(case_id) / f"{arm}-record.json"), "Frozen output metadata changed")
                    require(row.get("scan_scope", "full_text") == scan_scope(state), "Output scan scope differs from frozen config")
                    if scan_scope(state) == "prose_only":
                        manifest = read_json(run / row["code_ranges_path"])
                        require(prose_bytes((run / row["path"]).read_bytes(), manifest) ==
                                (run / row["detector_input_path"]).read_bytes(), "Frozen prose differs from code ranges")
            for case_id, row in state["reviews"].items():
                require(row == read_json(run / "reviews" / f"{safe_id(case_id)}.json"), "Frozen review metadata changed")
            for key, row in state["attempts"].items():
                name = "reservation.json" if row["status"] == "reserved" else "outcome.json"
                require(row == read_json(run / "attempts" / safe_id(key) / name), "Frozen attempt metadata changed")
                require(row.get("scan_scope", "full_text") == scan_scope(state), "Attempt scan scope differs from frozen config")
            if state.get("completion"):
                require(state["completion"] == read_json(run / "completion.json"), "Frozen completion changed")
            if state["selected"]:
                require(state["selected"] == read_json(run / "ranking.json")["ranked_ids"][0], "Frozen ranking changed")
        yield run, state


def validate_inputs(config, corpus):
    if isinstance(config, dict):
        config = dict(config)
        config.setdefault("scan_scope", "full_text")
    require(isinstance(config, dict) and set(config) == set(DEFAULTS), "Config keys must match documented schema")
    for key, default in DEFAULTS.items():
        value = config[key]
        if key == "primary_detector":
            require(value == "gptzero", "Only GPTZero primary decisions are supported")
        elif key == "scan_scope":
            require(value in ("full_text", "prose_only"), "Unsupported scan scope")
        else:
            require(type(value) in (int, float) and math.isfinite(value) and value >= 0,
                    f"Invalid numeric config: {key}")
            if type(default) is int and key not in ("min_mean_ai_reduction", "max_case_regression"):
                require(type(value) is int, f"Expected integer: {key}")
    require(config["schema_version"] == 1 and config["max_rounds"] == 1,
            "Only schema 1 and a single bounded round are supported")
    require(config["max_elapsed_seconds"] > 0 and config["reserved_confirmation_words"] < config["max_detector_words"], "Require positive duration and development word capacity")
    require(config["max_candidates"] > 0 and config["min_development_pairs"] >= 2
            and config["min_holdout_pairs"] >= 2, "Require candidates and at least two cases per split")
    require(isinstance(corpus, dict) and type(corpus.get("schema_version")) is int
            and corpus["schema_version"] == 1 and isinstance(corpus.get("cases"), list), "Invalid corpus")
    seen, texts, counts = set(), set(), {"development": 0, "holdout": 0}
    for case in corpus["cases"]:
        require(isinstance(case, dict), "Each case must be an object")
        key = safe_id(case.get("id"))
        require(key not in seen, "Duplicate case ID")
        seen.add(key)
        require(case.get("split") in counts, "Unknown case split")
        counts[case["split"]] += 1
        for field in ("question", "original"):
            require(isinstance(case.get(field), str) and case[field].strip(), f"Missing {field}")
        normalized = " ".join(case["original"].split())
        require(normalized not in texts, "Duplicate case text, including across splits")
        texts.add(normalized)
        for field in ("claims", "protected", "sources"):
            require(isinstance(case.get(field), list) and all(isinstance(v, str) and v.strip()
                    for v in case[field]), f"Invalid {field}")
        require(all(v in case["original"] for v in case["protected"]), "Protected span missing in original")
    require(counts["development"] >= config["min_development_pairs"]
            and counts["holdout"] >= config["min_holdout_pairs"], "Corpus has insufficient pairs")
    reserve = config["reserved_confirmation_calls"]
    require(reserve >= 2 * counts["holdout"], "Confirmation reserve must cover every holdout pair")
    require(config["max_detector_calls"] >= 2 * counts["development"] + reserve,
            "Call budget cannot cover development plus confirmation")


def initialize(args, run, state):
    skill = clean_path(args.skill)
    require(not run.is_relative_to(skill) and not skill.is_relative_to(run), "Run and skill directories must be disjoint")
    for ancestor in run.parents:
        if (ancestor / ".git").exists():
            relative = run.relative_to(ancestor)
            allowed = relative.parts[0] in ("private", ".autoresearch")
            ignores = (ancestor / ".gitignore").read_text().splitlines() if (ancestor / ".gitignore").exists() else []
            require(allowed and any(line.strip().lstrip("/") in
                    (relative.parts[0], relative.parts[0] + "/") for line in ignores),
                    "Runs inside a repository must use ignored private/ or .autoresearch/")
    config, corpus = read_json(args.config), read_json(args.cases)
    validate_inputs(config, corpus)
    config.setdefault("scan_scope", "full_text")
    files = tree_files(skill)
    state.update(config=config, corpus=corpus, baseline_tree_sha256=tree_hash(files),
                 started_at=datetime.now(timezone.utc).isoformat())
    save_artifact(run, state, "frozen/run.json", encode({k: state[k] for k in ("started_at", "baseline_tree_sha256")}))
    save_artifact(run, state, "frozen/config.json", encode(config))
    save_artifact(run, state, "frozen/cases.json", encode(corpus))
    state["corpus_sha256"] = state["artifacts"]["frozen/cases.json"]
    for name, data in files.items():
        save_artifact(run, state, "baseline/" + name, data)
    save_artifact(run, state, "frozen/manifest.json", encode(dict(state["artifacts"])))


def case_for(state, case_id):
    safe_id(case_id)
    case = next((c for c in state["corpus"]["cases"] if c["id"] == case_id), None)
    require(case is not None, "Unknown case")
    return case


def pair_outputs(state, case_id):
    row = state["outputs"].get(case_id, {})
    require(set(row) == {"baseline", "candidate"}, "Both outputs are required")
    require(all(output.get("scan_scope", "full_text") == scan_scope(state) for output in row.values()),
            "Paired outputs must use the frozen scan scope")
    return row


def eligible(state, case_id):
    review = state["reviews"].get(case_id)
    return review and review["baseline_pass"] and review["candidate_pass"] and review["preference"] != "baseline"


def decision(state, split):
    rows, deltas, incomplete, rejected, noop = [], [], False, False, False
    cases = [c for c in state["corpus"]["cases"] if c["split"] == split]
    quality_rejected = all(c["id"] in state["reviews"] for c in cases) and any(not eligible(state, c["id"]) for c in cases)
    for case in cases:
        key = case["id"]
        row = {"case": key, "scan_scope": scan_scope(state)}
        outputs = state["outputs"].get(key, {})
        row["hashes"] = {arm: dict(full_message_sha256=output["sha256"],
                                  detector_input_sha256=measured_input(output)["sha256"])
                         for arm, output in outputs.items()}
        if scan_scope(state) == "full_text" and measurement_noop(outputs):
            row["status"], noop = "no_op", True
        elif key not in state["reviews"]:
            row["status"], incomplete = "awaiting_outputs_or_review", True
        elif not eligible(state, key):
            row["status"], rejected = "quality_rejected", True
        elif measurement_noop(outputs):
            row["status"] = "no_op" if outputs["baseline"]["sha256"] == outputs["candidate"]["sha256"] else "prose_no_op"
            noop = True
        else:
            attempts = [a for a in state["attempts"].values() if a["case"] == key and a["detector"] == "gptzero"]
            if any(a["status"] in ("failed", "invalid", "uncertain") for a in attempts):
                row["status"], rejected = "scan_failed", True
            elif quality_rejected and len(attempts) < 2 and not any(a["status"] == "reserved" for a in attempts):
                row["status"], rejected = "not_scanned_candidate_rejected", True
                row["completed_scan_arms"] = [a["arm"] for a in attempts if a["status"] == "complete"]
            elif len(attempts) != 2 or any(a["status"] != "complete" for a in attempts):
                row["status"], incomplete = "awaiting_scans", True
            else:
                scans = {a["arm"]: a["result"] for a in attempts}
                if any(scans["baseline"].get(v, "full_text") != scans["candidate"].get(v, "full_text")
                       for v in ("mode", "model", "scan_scope")):
                    row["status"], rejected = "incomparable_scans", True
                else:
                    delta = scans["baseline"]["ai"] - scans["candidate"]["ai"]
                    deltas.append(delta)
                    row.update(status="paired", ai_reduction=delta)
        rows.append(row)
    status = "rejected" if rejected else "incomplete" if incomplete else "no_improvement"
    mean = sum(deltas) / len(deltas) if deltas else None
    if not (rejected or incomplete or noop) and deltas:
        cfg = state["config"]
        if mean >= cfg["min_mean_ai_reduction"] and min(deltas) >= -cfg["max_case_regression"] and max(deltas) > 0:
            status = "promising" if split == "development" else "supported"
    return {"status": status, "mean_ai_reduction": mean, "rows": rows}


def expired(state):
    return (datetime.now(timezone.utc) - datetime.fromisoformat(state["started_at"])).total_seconds() > state["config"]["max_elapsed_seconds"]


def primary_scan_failed(state):
    return any(a["detector"] == state["config"]["primary_detector"]
               and a["status"] in ("failed", "invalid", "uncertain") for a in state["attempts"].values())


def summary(state):
    development, holdout = decision(state, "development"), decision(state, "holdout")
    if state["selected"] is None:
        status = "awaiting_selection" if state["candidates"] else "awaiting_proposals"
    elif development["status"] != "promising":
        status = "development_" + development["status"]
    elif holdout["status"] == "supported":
        status = "candidate_supported"
    elif holdout["status"] == "incomplete":
        status = "development_promising"
    else:
        status = "holdout_" + holdout["status"]
    if state.get("completion"):
        status = state["completion"]["status"]
    elif expired(state) and not primary_scan_failed(state):
        status = "budget_expired"
    pending = []
    if state["selected"]:
        for case in state["corpus"]["cases"]:
            if case["split"] == "holdout" and development["status"] != "promising":
                continue
            key, outputs = case["id"], state["outputs"].get(case["id"], {})
            for arm in ("baseline", "candidate"):
                if arm not in outputs:
                    pending.append({"role": "writer", "case": key, "arm": arm,
                                    "skill": "baseline" if arm == "baseline" else "candidates/" + state["selected"] + "/skill"})
            if len(outputs) == 2 and key not in state["reviews"] and (scan_scope(state) == "prose_only" or not measurement_noop(outputs)):
                pending.append({"role": "quality_judge", "case": key})
            if eligible(state, key) and not measurement_noop(outputs):
                quality_rejected = any(c["split"] == case["split"] and c["id"] in state["reviews"]
                                       and not eligible(state, c["id"]) for c in state["corpus"]["cases"])
                scans = {a["arm"]: a for a in state["attempts"].values()
                         if a["case"] == key and a["detector"] == "gptzero"}
                if set(scans) != {"baseline", "candidate"} and not quality_rejected:
                    pending.append({"role": "coordinator", "action": "reserve complete pair",
                                    "case": key, "detector": "gptzero", "reserved_arms": sorted(scans)})
                else:
                    for arm, attempt in scans.items():
                        if attempt["status"] != "reserved":
                            continue
                        job = {"role": "detector_worker", "case": key, "arm": arm,
                               "attempt": attempt["id"]}
                        if quality_rejected:
                            job["action"] = "record existing outcome only"
                        pending.append(job)
    else:
        pending.append({"role": "ranker" if state["candidates"] else "improver"})
    if expired(state) or state.get("completion") or primary_scan_failed(state):
        pending = [{"role": "detector_worker", "attempt": a["id"], "action": "record existing outcome only"}
                   for a in state["attempts"].values() if a["status"] == "reserved"]
    inputs = {key: {arm: dict(scan_scope=output.get("scan_scope", "full_text"),
                             full_message_path=output["path"], full_message_sha256=output["sha256"],
                             detector_input_path=measured_input(output)["path"],
                             detector_input_sha256=measured_input(output)["sha256"],
                             **({"code_ranges_path": output["code_ranges_path"],
                                 "code_ranges_sha256": output["code_ranges_sha256"]}
                                if output.get("scan_scope") == "prose_only" else {}))
                    for arm, output in outputs.items()}
              for key, outputs in state["outputs"].items()}
    return {"status": status, "scan_scope": scan_scope(state), "outputs": inputs,
            "completed_at": state.get("completion", {}).get("completed_at"),
            "selected": state["selected"], "development": development,
            "holdout": holdout, "budget": {"calls_charged": len(state["attempts"]),
            "words_charged": sum(a["words"] for a in state["attempts"].values())},
            "next": pending, "attempts": state["attempts"],
            "limitations": "Local consistency only; role identities and service authenticity are not verified. No automatic installation or publication."}


def propose(args, run, state):
    key, writer = safe_id(args.id), safe_id(args.writer)
    require(state["selected"] is None, "Ranking is already frozen")
    require(key != "baseline" and key not in state["candidates"], "Candidate ID already used or reserved")
    require(len(state["candidates"]) < state["config"]["max_candidates"], "Candidate budget exhausted")
    require(args.hypothesis.strip(), "Hypothesis is required")
    original, changed = (run / "baseline/SKILL.md").read_bytes(), text_bytes(args.skill_file)
    require(original.count(START) == original.count(END) == changed.count(START) == changed.count(END) == 1, "Unique editable section headings required")
    before, editable = original.split(START)
    _, after = editable.split(END)
    prefix, body = changed.split(START)
    _, suffix = body.split(END)
    require(before == prefix and after == suffix, "Only Write and review section may change")
    require(original != changed, "No-op skill proposal")
    require(all(c["main_sha256"] != digest(changed) for c in state["candidates"].values()), "Duplicate skill proposal")
    files = tree_files(run / "baseline")
    files["SKILL.md"] = changed
    for name, data in files.items():
        save_artifact(run, state, f"candidates/{key}/skill/{name}", data)
    row = dict(id=key, writer=writer, hypothesis=args.hypothesis, parent="baseline",
               main_sha256=digest(changed), tree_sha256=tree_hash(files))
    save_artifact(run, state, f"candidates/{key}/proposal.json", encode(row))
    state["candidates"][key] = row


def select(args, run, state):
    require(state["selected"] is None, "Ranking already frozen")
    ranking = read_json(args.ranking)
    ranker = safe_id(ranking["ranker"])
    ids = ranking["ranked_ids"]
    require(isinstance(ids, list) and ids and all(isinstance(v, str) for v in ids)
            and len(ids) == len(set(ids)) and set(ids) == set(state["candidates"]), "Rank every proposed candidate exactly once")
    require(ranker not in {c["writer"] for c in state["candidates"].values()}, "Ranker must be independent of improvers")
    require(isinstance(ranking.get("reason"), str) and ranking["reason"].strip(), "Ranking reason required")
    save_artifact(run, state, "ranking.json", encode(ranking))
    state["selected"] = ids[0]


def output(args, run, state):
    require(state["selected"], "Select a candidate first")
    case = case_for(state, args.case)
    require(case["split"] == "development" or decision(state, "development")["status"] == "promising", "Holdout is locked until positive development decision")
    writer = safe_id(args.writer)
    require(writer != state["candidates"][state["selected"]]["writer"], "Output writer must differ from improver")
    generation = read_json(args.generation)
    require(isinstance(generation, dict) and generation.get("context") == "fresh", "Generation needs fresh context")
    require(all(isinstance(generation.get(k), str) and generation[k].strip() for k in ("model", "settings")), "Generation model and settings required")
    require(isinstance(generation.get("operator_sha256"), str) and re.fullmatch(r"[a-f0-9]{64}", generation["operator_sha256"]), "Generation operator hash required")
    for other in state["outputs"].get(args.case, {}).values():
        require(other["writer"] != writer, "Paired outputs require different fresh writers")
        require(other["generation"] == generation, "Paired generation provenance must match")
    require(args.arm not in state["outputs"].get(args.case, {}), "Output already frozen")
    data = text_bytes(args.file)
    require(all(span in data.decode("utf-8") for span in case["protected"]), "Protected span missing")
    scope = scan_scope(state)
    measurement = dict(scan_scope=scope)
    if scope == "prose_only":
        require(args.code_ranges_file is not None, "Prose-only outputs require --code-ranges-file")
        manifest = read_json(args.code_ranges_file)
        prose = prose_bytes(data, manifest)
        measurement.update(
            code_ranges_path=save_artifact(run, state, f"outputs/{args.case}/{args.arm}-code-ranges.json", encode(manifest)),
            code_ranges_sha256=digest(encode(manifest)),
            detector_input_path=save_artifact(run, state, f"outputs/{args.case}/{args.arm}-prose.txt", prose),
            detector_input_sha256=digest(prose))
    else:
        require(args.code_ranges_file is None, "Full-text outputs do not accept code ranges")
    name = save_artifact(run, state, f"outputs/{args.case}/{args.arm}.txt", data)
    skill_hash = state["baseline_tree_sha256"] if args.arm == "baseline" else state["candidates"][state["selected"]]["tree_sha256"]
    save_artifact(run, state, f"outputs/{args.case}/{args.arm}-generation.json", encode(generation))
    state["outputs"].setdefault(args.case, {})[args.arm] = dict(generation=generation, path=name, sha256=digest(data),
             corpus_sha256=state["corpus_sha256"], skill_tree_sha256=skill_hash, writer=writer, **measurement)
    save_artifact(run, state, f"outputs/{args.case}/{args.arm}-record.json", encode(state["outputs"][args.case][args.arm]))


def review(args, run, state):
    case_for(state, args.case)
    outputs = pair_outputs(state, args.case)
    require(args.case not in state["reviews"], "Review already frozen")
    row = read_json(args.file)
    reviewer = safe_id(row["reviewer"])
    excluded = {o["writer"] for o in outputs.values()} | {state["candidates"][state["selected"]]["writer"]}
    require(reviewer not in excluded, "Reviewer must be independent of output writers and improver")
    require(row.get("detector_scores_withheld") is True, "Detector scores must be withheld from reviewer")
    for arm in ("baseline", "candidate"):
        require(row.get(arm + "_sha256") == outputs[arm]["sha256"], "Review output hash mismatch")
        require(type(row.get(arm + "_pass")) is bool, "Quality verdicts must be booleans")
        if scan_scope(state) == "prose_only":
            require(row.get(arm + "_prose_sha256") == measured_input(outputs[arm])["sha256"], "Review prose hash mismatch")
    if scan_scope(state) == "prose_only":
        require(row.get("code_ranges_approved") is True, "Independent review must approve code ranges and preserved prose")
    require(row.get("preference") in ("baseline", "candidate", "tie"), "Invalid preference")
    require(isinstance(row.get("reason"), str) and row["reason"].strip(), "Review reason required")
    save_artifact(run, state, f"reviews/{args.case}.json", encode(row))
    state["reviews"][args.case] = row


def reserve(args, run, state):
    case = case_for(state, args.case)
    outputs = pair_outputs(state, args.case)
    require(eligible(state, args.case), "Quality review does not permit scanning")
    require(not any(c["id"] in state["reviews"] and not eligible(state, c["id"])
                    for c in state["corpus"]["cases"] if c["split"] == case["split"]),
            "Split quality rejection prevents further scans")
    require(not measurement_noop(outputs), "No-op measured inputs do not need duplicate scans")
    require(not any(a["case"] == args.case and a["arm"] == args.arm and a["detector"] == args.detector for a in state["attempts"].values()), "Scan already reserved; failures and uncertain outcomes remain charged")
    measured = measured_input(outputs[args.arm])
    words = len((run / measured["path"]).read_text().split())
    require(type(args.words) is int and args.words >= words and words > 0, "Word reservation must cover measured-input whitespace word count")
    words = args.words
    cfg, attempts = state["config"], list(state["attempts"].values())
    opposite = "candidate" if args.arm == "baseline" else "baseline"
    opposite_exists = any(a["case"] == args.case and a["arm"] == opposite and a["detector"] == args.detector for a in attempts)
    pair_calls = 1 if opposite_exists else 2
    pair_words = words + (0 if opposite_exists else len((run / measured_input(outputs[opposite])["path"]).read_text().split()))
    require(len(attempts) + pair_calls <= cfg["max_detector_calls"], "Call budget cannot cover paired scans")
    require(sum(a["words"] for a in attempts) + pair_words <= cfg["max_detector_words"], "Word budget cannot cover paired scans")
    if case["split"] == "development":
        require(sum(a["words"] for a in attempts if a["split"] == "development") + pair_words <= cfg["max_detector_words"] - cfg["reserved_confirmation_words"], "Development cannot spend confirmation word reserve")
        require(sum(a["split"] == "development" for a in attempts) + pair_calls <= cfg["max_detector_calls"] - cfg["reserved_confirmation_calls"], "Development cannot spend confirmation reserve")
    key = f"attempt-{len(attempts) + 1:04d}"
    row = dict(id=key, case=args.case, arm=args.arm, detector=args.detector, words=words,
               split=case["split"], status="reserved", reserved_at=datetime.now(timezone.utc).isoformat(),
               output_sha256=outputs[args.arm]["sha256"], scan_scope=scan_scope(state),
               detector_input_path=measured["path"], detector_input_sha256=measured["sha256"])
    save_artifact(run, state, f"attempts/{key}/reservation.json", encode(row))
    state["attempts"][key] = row
    return dict(row, dispatch_ready=opposite_exists)


def reserve_pair(args, run, state):
    """Commit both UI word costs together under the command's existing transaction."""
    attempts = []
    for arm in ("baseline", "candidate"):
        options = argparse.Namespace(case=args.case, arm=arm, detector=args.detector,
                                     words=getattr(args, arm + "_words"))
        attempts.append(reserve(options, run, state))
    return {"attempts": [dict(row, dispatch_ready=True) for row in attempts]}


def import_receipt(source, run, state, base):
    source = clean_path(source)
    data = source.read_bytes()
    save_artifact(run, state, base + "/receipt.json", data)
    receipt = json.loads(data)

    def visit(value):
        if isinstance(value, dict):
            if "path" in value:
                name = value["path"]
                require(isinstance(name, str) and name not in ("", ".", "receipt.json"), "Invalid receipt artifact path")
                relative = Path(name)
                require(not relative.is_absolute() and ".." not in relative.parts, "Unsafe receipt artifact path")
                dest = base + "/" + relative.as_posix()
                data = clean_path(source.parent / relative).read_bytes()
                if dest not in state["artifacts"]:
                    save_artifact(run, state, dest, data)
            for item in value.values():
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)
    visit(receipt)
    return run / ".pending/files" / base / "receipt.json"


def record(args, run, state):
    key = safe_id(args.attempt)
    require(key in state["attempts"], "Unknown attempt")
    row = state["attempts"][key]
    require(row["status"] == "reserved", "Attempt outcome is terminal")
    if args.failure is not None:
        require(args.failure.strip(), "Failure explanation required")
        row.update(status="uncertain" if args.failure.lower().startswith("uncertain") else "failed", failure=args.failure)
    else:
        try:
            from detector_receipts import validate_scan
            path = import_receipt(args.receipt, run, state, f"attempts/{key}/evidence")
            receipt = read_json(path)
            require(receipt.get("scan_scope", scan_scope(state)) == scan_scope(state),
                    "Receipt scan scope differs from reservation")
            output = state["outputs"][row["case"]][row["arm"]]
            measured = measured_input(output)
            expected = run / measured["path"]
            result = validate_scan(path, expected)
            require(result["detector"] == row["detector"], "Receipt detector mismatch")
            require(result["input_sha256"] == row.get("detector_input_sha256", row["output_sha256"]) == measured["sha256"], "Receipt measured-input hash mismatch")
            require(row["output_sha256"] == output["sha256"], "Reservation full-message hash mismatch")
            require(result.get("scan_scope", scan_scope(state)) == row.get("scan_scope", "full_text") == scan_scope(state),
                    "Receipt scan scope differs from reservation")
            result.update(scan_scope=scan_scope(state), full_message_sha256=output["sha256"])
            observed = datetime.fromisoformat(result["observed_at"].replace("Z", "+00:00"))
            require(observed.utcoffset() is not None and observed >= datetime.fromisoformat(row["reserved_at"]), "Receipt predates reservation")
            for other in state["attempts"].values():
                if other["case"] == row["case"] and other["detector"] == row["detector"] and other["status"] == "complete":
                    require(all(other["result"][v] == result[v] for v in ("mode", "model")), "Paired scans have different mode or model")
                    require(other["result"].get("scan_scope", "full_text") == result["scan_scope"], "Paired scans have different scope")
            row.update(status="complete", result=result)
        except (ValueError, OSError, KeyError, TypeError, AttributeError, ImportError) as error:
            row.update(status="invalid", failure=str(error))
    save_artifact(run, state, f"attempts/{key}/outcome.json", encode(row))
    return row


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    fields = {
        "init": [("skill", Path), ("cases", Path), ("config", Path)],
        "propose": [("id", str), ("skill-file", Path), ("hypothesis", str), ("writer", str)],
        "select": [("ranking", Path)],
        "output": [("case", str), ("arm", str), ("file", Path), ("writer", str), ("generation", Path)],
        "review": [("case", str), ("file", Path)],
        "reserve": [("case", str), ("arm", str), ("detector", str), ("words", int)],
        "reserve-pair": [("case", str), ("detector", str), ("baseline-words", int), ("candidate-words", int)],
        "record": [("attempt", str)], "summarize": [], "status": []}
    for name, options in fields.items():
        command = commands.add_parser(name)
        command.add_argument("--run", type=Path, required=True)
        for field, kind in options:
            choices = ("baseline", "candidate") if field == "arm" else ("gptzero", "pangram") if field == "detector" else None
            command.add_argument("--" + field, type=kind, required=True, choices=choices)
        if name == "record":
            group = command.add_mutually_exclusive_group(required=True)
            group.add_argument("--receipt", type=Path)
            group.add_argument("--failure")
        if name == "output":
            command.add_argument("--code-ranges-file", type=Path)
    return result


def main(argv=None):
    cli = parser()
    args = cli.parse_args(argv)
    try:
        with locked(args.run, args.command == "init") as (run, state):
            if args.command in ("summarize", "status"):
                result = summary(state)
            else:
                if args.command not in ("init", "record"):
                    require(not state.get("completion"), "Run completed; start a new run for further work")
                    require(not expired(state), "Run elapsed-time budget expired")
                    require(not primary_scan_failed(state), "Primary detector failure stops new work; record existing outcomes only")
                action = initialize if args.command == "init" else globals()[args.command.replace("-", "_")]
                result = action(args, run, state)
                result_summary = summary(state)
                terminal = result_summary["status"] in ("candidate_supported", "development_no_improvement",
                                                       "holdout_no_improvement", "development_rejected", "holdout_rejected")
                split = "development" if result_summary["status"].startswith("development_") else "holdout"
                settled = all(row["status"] in ("paired", "no_op", "prose_no_op", "quality_rejected", "scan_failed", "incomparable_scans", "not_scanned_candidate_rejected")
                              for row in result_summary[split]["rows"])
                pending = any(a["status"] == "reserved" for a in state["attempts"].values())
                if not state.get("completion") and terminal and (settled or primary_scan_failed(state)) and not pending:
                    state["completion"] = dict(status=result_summary["status"], selected=state["selected"],
                                               completed_at=datetime.now(timezone.utc).isoformat())
                    save_artifact(run, state, "completion.json", encode(state["completion"]))
                save_state(run / ".pending", state)
                recover_transaction(run)
                result = result or summary(state)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        print(f"Autoresearch rejected: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
