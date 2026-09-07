"""Validate saved native detector evidence, not service authenticity or authorship."""

import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def artifact(root, item):
    require(isinstance(item, dict), "Artifact must be an object")
    name = item.get("path")
    require(isinstance(name, str) and name, "Missing artifact path")
    relative = Path(name)
    require(not relative.is_absolute() and ".." not in relative.parts,
            "Artifact path must remain inside receipt directory")
    target = (root / relative).resolve()
    require(target.is_relative_to(root.resolve()), "Artifact symlink escapes receipt")
    raw = target.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == item.get("sha256"),
            f"Artifact hash mismatch: {name}")
    return raw


def unique(pattern, text, label):
    matches = re.findall(pattern, text, re.M)
    require(len(matches) == 1, f"Missing or ambiguous {label}")
    return matches[0]


def percent(value):
    require(type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 100,
            "Invalid percentage")
    return value


def snapshot_text(value):
    """Decode the snapshot's single-line string representation."""
    if value.startswith('"'):
        return json.loads(value)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    require(value not in ("|", ">"), "Unsupported multiline snapshot representation")
    return value


def display_text(text):
    # Accessibility snapshots fold whitespace. This additional cross-check never
    # replaces the byte-exact submitted/editor/rendered checks above.
    return re.sub(r"[ \t\r\n]+", " ", text).strip(" ")


def validate_scan(receipt_path, expected_answer):
    """Return native measurements only after exact representations and UI agree.

    The coordinator must independently validate reservation time, reviewer identity,
    case/skill hashes and paired model equality. Saved files are operator evidence;
    a party able to forge files can forge these observations.
    """
    receipt_path, expected_answer = Path(receipt_path), Path(expected_answer)
    root = receipt_path.parent
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    require(isinstance(receipt, dict) and type(receipt.get("schema_version")) is int
            and receipt["schema_version"] == 1,
            "Unsupported receipt schema")
    require(receipt.get("status") == "complete", "Scan is incomplete")
    stamp = datetime.fromisoformat(receipt["observed_at"].replace("Z", "+00:00"))
    require(stamp.utcoffset() is not None, "Observation time needs timezone")
    require(stamp <= datetime.now(stamp.tzinfo), "Observation time is in the future")
    fields = ("answer", "submitted", "editor_before", "editor_after", "visible_result",
              "screenshot")
    data = {key: artifact(root, receipt[key]) for key in fields}
    require(data["answer"] == expected_answer.read_bytes(), "Answer differs from reviewed output")
    require(bool(data["answer"].strip()), "Empty answer")
    image = data["screenshot"]
    require(image.startswith(b"\x89PNG\r\n\x1a\n") or image.startswith(b"\xff\xd8\xff"),
            "Evidence screenshot is not PNG or JPEG")
    ui = data["visible_result"].decode("utf-8")
    answer = data["answer"].decode("utf-8")
    submitted = data["submitted"].decode("utf-8")
    before = data["editor_before"].decode("utf-8")
    after = data["editor_after"].decode("utf-8")
    model = receipt.get("model")
    require(isinstance(model, str) and re.fullmatch(r"[A-Za-z0-9._-]+", model),
            "Invalid model version")
    detector = receipt.get("detector")
    result = {"detector": detector, "mode": receipt.get("mode"), "model": model,
              "observed_at": receipt["observed_at"], "ai": None, "mixed": None,
              "human": None, "ai_assisted": None,
              "input_sha256": hashlib.sha256(data["answer"]).hexdigest()}

    if detector == "gptzero":
        require(receipt.get("mode") == "Basic Scan", "Expected GPTZero Basic Scan")
        transform = receipt.get("entry_transform")
        if transform == "gptzero_code_block_v1":
            expected_submission = answer[:-1] if answer.endswith("\n") else answer
            require(submitted == expected_submission, "Unexpected source-to-submission change")
            require(before == submitted + "\n\n\n", "Unexpected Code Block editor wrapper")
        else:
            require(transform == "verbatim_v1", "Unsupported GPTZero representation")
            require(answer == submitted == before, "Verbatim input changed")
        require(after == before, "Post-scan editor differs")
        if transform == "gptzero_code_block_v1":
            visible_body = snapshot_text(unique(r'^  - code: (.+)$', ui, "visible editor body"))
        else:
            visible_body = snapshot_text(unique(r'^  - paragraph: (.+)$',
                                                 ui.split('- heading "Basic Scan"')[0],
                                                 "visible editor body"))
        require(visible_body == display_text(submitted), "Visible editor belongs to different text")
        unique(r'^\s*- heading "(Basic Scan)" \[level=1\]\s*$', ui, "Basic heading")
        unique(r'^\s*- generic: (Text up-to-date)\s*$', ui, "fresh result")
        require(not re.search(r'^\s*- (?:generic|button|paragraph|text).*'
                              r'(?:Text changed|Scan to update|Scanning)', ui, re.M),
                "GPTZero result is stale or processing")
        require(unique(r'^\s*- generic: Model (\S+)\s*$', ui, "model") == model,
                "GPTZero model mismatch")
        for label in ("AI", "Mixed", "Human"):
            value = unique(r'^\s*- button "' + label + r' (\d+(?:\.\d+)?)%":?\s*$',
                           ui, label + " confidence")
            result[label.lower()] = percent(float(value))
        require(abs(sum(result[k] for k in ("ai", "mixed", "human")) - 100) <= 1,
                "GPTZero confidences do not sum to approximately 100")
        short = bool(re.search(r'^\s*- paragraph: This text is under 100 words', ui, re.M))
        result.update(unit="document_confidence_percent", label=None,
                      short_text_warning=short)
    elif detector == "pangram":
        require(receipt.get("mode") == "Free text detection", "Unexpected Pangram mode")
        require(receipt.get("entry_transform") == "pangram_textarea_v1",
                "Unsupported Pangram representation")
        require(answer == submitted == before, "Pangram textarea changed input")
        # The post-scan textarea is cleared by this UI; record the rendered result
        # as editor_after, without pretending it is the submitted model input.
        rendered = artifact(root, receipt["rendered"]).decode("utf-8")
        expected = "\n".join(line.strip(" \t\r") for line in submitted.split("\n")
                             if line.strip(" \t\r"))
        require(rendered == expected and after == rendered, "Pangram result rendering changed")
        details = artifact(root, receipt["details_ui"]).decode("utf-8")
        require(not re.search(r'^\s*- (?:generic|button|text|paragraph).*'
                              r'(?:Processing|Checking|Scan to update|Text changed)',
                              ui + "\n" + details, re.M), "Pangram is processing or stale")
        for snapshot in (ui, details):
            dialog = unique(r'(?ms)^- dialog "Text Query"[^\n]*:\n(.*)\Z',
                            snapshot, "Pangram result dialog")
            candidates = [snapshot_text(v) for v in re.findall(r'^  - generic: (.+)$',
                                                               dialog.split('  - tablist:')[0], re.M)]
            require(candidates.count(display_text(rendered)) == 1,
                    "Pangram visible document belongs to different text")
        overview = unique(r'(?ms)^  - tabpanel "Overview":\n(.*?)(?=^  - tabpanel|^  - region|\Z)',
                          ui, "Pangram Overview")
        require(unique(r'Detection model: Pangram ([A-Za-z0-9._-]+)', overview, "model") == model,
                "Pangram model mismatch")
        result["label"] = unique(
            r'^    - generic: (AI Generated|AI Assisted|Human Written|Human|Mixed)\s*$',
            overview, "document label")
        native = re.findall(r'^    - generic: "?(\d+(?:\.\d+)?)"?\n'
                            r'    - generic: "%"\n'
                            r'    - generic: of this text is (AI|AI Assisted|human|Human)\s*$',
                            overview, re.M)
        require(bool(native), "Missing native Pangram proportions")
        mapping = {"AI": "ai", "AI Assisted": "ai_assisted", "human": "human", "Human": "human"}
        seen = set()
        for raw, label in native:
            key = mapping[label]
            require(key not in seen, "Duplicate Pangram proportion")
            result[key] = percent(float(raw))
            seen.add(key)
        require(sum(result[key] for key in seen) <= 100.01, "Impossible Pangram proportions")
        confidence = re.findall(r'generic "Confidence level":\n\s+- text: (low|medium|high)\s*$',
                                details, re.M)
        require(bool(confidence), "Missing Pangram segment confidence")
        short = "Confidence limited — short text" in overview
        result.update(unit="displayed_text_proportion_percent", mixed=None,
                      segment_confidence_labels=confidence, short_text_warning=short)
    else:
        raise ValueError("Unsupported detector adapter")

    warnings = receipt.get("warnings", [])
    require(isinstance(warnings, list) and all(isinstance(x, str) and x for x in warnings),
            "Warnings must be nonempty strings")
    require(all(w in ui for w in warnings), "A warning is absent from visible evidence")
    require(type(receipt.get("short_text_warning")) is bool
            and receipt["short_text_warning"] == result["short_text_warning"],
            "Short-text warning metadata mismatch")
    result["warnings"] = warnings
    result["artifact_sha256"] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    if "metrics" in receipt:
        expected_metrics = {key: result[key] for key in ("ai", "mixed", "human", "ai_assisted")}
        require(isinstance(receipt["metrics"], dict), "Metrics must be an object")
        for value in receipt["metrics"].values():
            if value is not None:
                percent(value)
        require(receipt["metrics"] == expected_metrics, "Declared metrics disagree with native UI")
    return result
