#!/usr/bin/env python3
"""Run pinned GEPA with manual, receipt-backed evaluation and reflection jobs.

Usage: uv run --no-project python runner.py --config /absolute/config.json

Config: {"seed_candidate": {"writing_policy": "..."}, "case": {...},
         "run_dir": "/absolute/private/run", "upstream_repo": "/tmp/..."}
Optional limits default to max_proposals=2, max_unique_evaluations=3,
max_development_words=510, deadline_seconds=3600. No detector/model transport.

Each jobs/<id>/request.json is immutable; the coordinator atomically writes
response.json there. Every response needs request_sha256 from the request.
Evaluation responses need status=ok, output (full message), prose, quality_pass,
feedback, and, when quality passes: ai_confidence, mixed_confidence,
human_confidence, scan_words, receipt_path. Quality failures need no detector
values and receive utility -1; unavailable measurements terminate the run.
Exact prose with an existing identical receipt/confidences may set
reused_receipt=true and scan_words=0, after a renewed full-message review.
Proposal responses need status=ok, candidate={writing_policy: ...}, reflection.
status=unavailable plus reason terminates either kind without a fabricated score.

The coordinator must honor remaining_word_budget BEFORE scanning. This runner
never scans and rejects over-budget receipts, but cannot undo external spending.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

UPSTREAM_SHA = "0632cdb5dcc052e690eab439e1b4a7e3e9cfe407"


class ManualStop(BaseException):
    """Escape GEPA's internal proposer Exception retry without synthetic scoring."""


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def text_digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    os.replace(temporary, path)


def finite_confidence(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ManualStop("Confidence must be numeric")
    if not math.isfinite(value) or not 0 <= value <= 100:
        raise ManualStop("Confidence outside 0..100")
    return float(value)


class Coordinator:
    propose_new_texts = None

    def __init__(self, config, evaluation_batch):
        self.config = config
        self.batch_type = evaluation_batch
        self.root = Path(config["run_dir"])
        self.root.mkdir(parents=True, exist_ok=True)
        frozen = self.root / "runner-config.json"
        if frozen.exists() and read_json(frozen) != config:
            raise ManualStop("Run configuration changed; start a separate run")
        if not frozen.exists():
            write_json(frozen, config)
        self.max_words = config.get("max_development_words", 510)
        self.max_evaluations = config.get("max_unique_evaluations", 3)
        self.max_proposals = config.get("max_proposals", 2)
        self.iteration = 0
        clock_path = self.root / "clock.json"
        if not clock_path.exists():
            write_json(clock_path, {"started_at_unix": config.get("started_at_unix", time.time())})
        self.deadline = read_json(clock_path)["started_at_unix"] + config.get("deadline_seconds", 3600)

    def event(self, kind, **values):
        with (self.root / "events.jsonl").open("a") as stream:
            stream.write(canonical({"time_unix": time.time(), "kind": kind, **values}) + "\n")

    def accounting(self):
        records = [read_json(p) for p in (self.root / "evaluations").glob("*.json")]
        return {"unique_evaluations": len(records),
                "scans": sum(int(r["quality_pass"] and not r.get("reused_receipt", False)) for r in records),
                "scan_words": sum(r["scan_words"] for r in records)}

    def job(self, kind, identity, payload):
        job_id = kind + "-" + digest(identity)
        directory = self.root / "jobs" / job_id
        request_path = directory / "request.json"
        response_path = directory / "response.json"
        request = {"kind": kind, "job_id": job_id, **payload}
        request["request_sha256"] = digest(request)
        if request_path.exists():
            previous = read_json(request_path)
            # Resume uses its original immutable budget and request identity.
            request = previous
        else:
            write_json(request_path, request)
        self.event("job_requested", job_id=job_id)
        print("MANUAL_JOB " + str(request_path), flush=True)
        last_heartbeat = 0.0
        while not response_path.exists():
            now = time.time()
            if now >= self.deadline:
                raise ManualStop("Overall manual-run deadline reached")
            if (self.root / "STOP").exists():
                raise ManualStop("Coordinator STOP file observed")
            if now - last_heartbeat >= 30:
                print("WAITING " + job_id, flush=True)
                last_heartbeat = now
            time.sleep(1)
        response = read_json(response_path)
        if response.get("request_sha256") != request["request_sha256"]:
            raise ManualStop("Response does not match exact frozen request")
        if response.get("status") != "ok":
            raise ManualStop(response.get("reason", "Manual response unavailable"))
        self.event("job_received", job_id=job_id, response_sha256=digest(response))
        return response, request

    def evaluate(self, batch, candidate, capture_traces=False):
        outputs, scores, traces = [], [], []
        newly_scanned = 0
        for case in batch:
            identity = {"candidate": candidate, "case": case}
            record_path = self.root / "evaluations" / (digest(identity) + ".json")
            if record_path.exists():
                record = read_json(record_path)
                if record["identity"] != identity:
                    raise ManualStop("Evaluation cache identity mismatch")
                self.event("evaluation_cache_hit", key=record_path.stem, capture_traces=capture_traces)
            else:
                used = self.accounting()
                if used["unique_evaluations"] >= self.max_evaluations:
                    raise ManualStop("Unique evaluation limit reached")
                remaining = self.max_words - used["scan_words"]
                if remaining <= 0:
                    raise ManualStop("Development word budget exhausted")
                response, request = self.job("evaluation", identity, {
                    **identity,
                    "candidate_sha256": digest(candidate), "case_sha256": digest(case),
                    "measurement_scope": "prose_only", "remaining_word_budget": remaining,
                    "full_message_and_code_review_required": True,
                    "fresh_basic_scan_required_if_quality_passes": True,
                    "confirmation_data_forbidden": True,
                })
                output, prose = response.get("output"), response.get("prose")
                if not isinstance(output, str) or not output.strip() or not isinstance(prose, str) or not prose.strip():
                    raise ManualStop("Evaluation needs exact nonempty full message and prose")
                quality = response.get("quality_pass")
                if type(quality) is not bool or not response.get("feedback"):
                    raise ManualStop("Evaluation needs explicit quality verdict and feedback")
                if quality:
                    confidences = {k: finite_confidence(response.get(k)) for k in
                                   ("ai_confidence", "mixed_confidence", "human_confidence")}
                    if abs(sum(confidences.values()) - 100) > 1:
                        raise ManualStop("Detector confidence sum inconsistent")
                    words = response.get("scan_words")
                    reused = response.get("reused_receipt", False)
                    if type(reused) is not bool or type(words) is not int:
                        raise ManualStop("Invalid receipt-reuse flag or scan word count")
                    receipt = response.get("receipt_path")
                    if not isinstance(receipt, str) or not Path(receipt).is_file():
                        raise ManualStop("Completed scan receipt file required")
                    if reused:
                        prior_records = [read_json(p) for p in (self.root / "evaluations").glob("*.json")]
                        matches = [r for r in prior_records if r["quality_pass"]
                                   and r["prose"] == prose and r["receipt_path"] == receipt
                                   and r["confidences"] == confidences]
                        if words != 0 or not matches:
                            raise ManualStop("Receipt reuse needs exact prior prose, receipt, confidences and zero words")
                        self.event("prose_receipt_reused", prose_sha256=text_digest(prose),
                                   full_message_sha256=text_digest(output))
                    elif words <= 0 or words > remaining:
                        raise ManualStop("Invalid or over-budget scan word count")
                    score = 1 - confidences["ai_confidence"] / 100
                    newly_scanned += int(not reused)
                else:
                    if any(response.get(k) is not None for k in
                           ("ai_confidence", "mixed_confidence", "human_confidence")):
                        raise ManualStop("Quality failures must not consume a detector scan")
                    confidences, words, receipt, score, reused = {}, 0, None, -1.0, False
                record = {"identity": identity, "request_sha256": request["request_sha256"],
                          "response_sha256": digest(response), "output": output, "prose": prose,
                          "full_message_sha256": text_digest(output), "prose_sha256": text_digest(prose),
                          "quality_pass": quality, "feedback": response["feedback"],
                          "confidences": confidences, "scan_words": words,
                          "receipt_path": receipt, "reused_receipt": reused, "score": score}
                write_json(record_path, record)
            outputs.append({"full_message": record["output"], "prose": record["prose"],
                            "prose_sha256": record["prose_sha256"]})
            scores.append(record["score"])
            traces.append(record)
        return self.batch_type(outputs=outputs, scores=scores,
                               trajectories=traces if capture_traces else None,
                               num_metric_calls=newly_scanned)

    def make_reflective_dataset(self, candidate, eval_batch, components_to_update):
        return {component: [{"Inputs": row["identity"]["case"],
                             "Generated Outputs": row["output"], "Measured Prose": row["prose"],
                             "Feedback": row["feedback"], "Quality Passed": row["quality_pass"],
                             "Detector Observations": row["confidences"], "Utility": row["score"]}
                            for row in eval_batch.trajectories]
                for component in components_to_update}

    def propose(self, candidate, reflective_dataset, components_to_update, *, metadata=None):
        if not 1 <= self.iteration <= self.max_proposals:
            raise ManualStop("Proposal ordinal outside configured bound")
        identity = {"iteration": self.iteration, "candidate": candidate,
                    "reflective_dataset": reflective_dataset, "components_to_update": components_to_update}
        response, _ = self.job("proposal", identity, {
            **identity, "candidate_sha256": digest(candidate),
            "instruction": "Reflect on the actual supplied development trace and propose a reusable writing policy. Preserve the frozen wrapper and factual constraints. Do not inspect confirmation cases.",
        })
        proposed = response.get("candidate")
        if not isinstance(proposed, dict) or set(proposed) != {"writing_policy"}:
            raise ManualStop("Proposal must change only writing_policy")
        if not isinstance(proposed["writing_policy"], str) or not proposed["writing_policy"].strip():
            raise ManualStop("Proposed writing policy is empty")
        if not response.get("reflection"):
            raise ManualStop("Proposal needs recorded reflection on supplied feedback")
        self.event("proposal_returned", iteration=self.iteration, candidate_sha256=digest(proposed),
                   noop=proposed == candidate)
        return proposed

    def on_iteration_start(self, event):
        self.iteration = event["iteration"]
        self.event("iteration_started", iteration=self.iteration)

    def on_iteration_end(self, event):
        self.event("iteration_ended", iteration=event["iteration"],
                   accepted=event["proposal_accepted"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config = read_json(args.config)
    if set(config["seed_candidate"]) != {"writing_policy"}:
        raise SystemExit("seed_candidate must contain only writing_policy")
    upstream = Path(config.get("upstream_repo", "/tmp/gepa-research-20260909"))
    actual = subprocess.check_output(["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True).strip()
    if actual != UPSTREAM_SHA:
        raise SystemExit("Upstream GEPA commit differs from reviewed pin")
    subprocess.run(["git", "-C", str(upstream), "diff", "--exit-code", "--quiet"], check=True)
    sys.path.insert(0, str(upstream / "src"))
    from gepa import EvaluationBatch, optimize
    from gepa.utils.stop_condition import MaxCandidateProposalsStopper

    coordinator = Coordinator(config, EvaluationBatch)
    # Same object intentionally: this tiny search set is NOT an unseen test set.
    development = [config["case"]]
    try:
        result = optimize(
            seed_candidate=config["seed_candidate"], trainset=development,
            adapter=coordinator, custom_candidate_proposer=coordinator.propose,
            reflection_minibatch_size=1, candidate_selection_strategy="pareto",
            acceptance_criterion="strict_improvement", use_merge=False,
            max_metric_calls=config.get("max_metric_calls", 3),
            stop_callbacks=[MaxCandidateProposalsStopper(coordinator.max_proposals)],
            run_dir=str(coordinator.root / "gepa"), callbacks=[coordinator],
            cache_evaluation=True, write_agent_state=False, skip_perfect_score=False,
            seed=0, raise_on_exception=True, display_progress_bar=False,
        )
        summary = {"status": "completed", "upstream_sha": UPSTREAM_SHA,
                   "scope": "single-development-case; no confirmation evaluation",
                   "best_candidate": result.best_candidate, "best_index": result.best_idx,
                   "gepa_result": result.to_dict(), "accounting": coordinator.accounting()}
        write_json(coordinator.root / "result.json", summary)
        print(canonical({"status": "completed", "best_index": result.best_idx,
                         "accounting": summary["accounting"]}), flush=True)
        return 0
    except (ManualStop, Exception, KeyboardInterrupt) as error:
        write_json(coordinator.root / "result.json", {
            "status": "blocked", "reason": str(error), "upstream_sha": UPSTREAM_SHA,
            "accounting": coordinator.accounting(),
            "note": "No fabricated score. Cached artifacts survive; GEPA checkpoint may precede interrupted iteration."})
        print("STOPPED " + str(error), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
