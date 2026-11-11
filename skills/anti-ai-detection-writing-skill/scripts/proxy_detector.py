#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#   "torch==2.8.0",
#   "transformers==4.57.6",
#   "safetensors==0.8.0",
#   "sentencepiece==0.2.1",
# ]
# ///
"""Offline proxy scores for archived GPTZero observations.

The scores are local model outputs. They are not GPTZero results, not authorship
evidence, and not a reason to change a fact. Model files stay outside the repository.
Importing this module does not import torch; scoring functions import it themselves.
"""

import argparse
import gc
import hashlib
import json
import math
import re
import statistics
import sys
from pathlib import Path

SHA256 = re.compile(r"[a-f0-9]{64}")
SENTENCE = re.compile(r"[^.!?]+(?:[.!?]+|$)")
# Same five-point bar as studies/open-detector-proxy-1, fixed before scoring.
GPTZERO_REDUCTION_POINTS = 5
SHORT_WORDS = 130
WARNING_WORDS = 100

# Lower priority number wins. Effective editor text is what the UI scored.
KEY_PRIORITY = {
    "effective_sha256": 0, "effective": 0, "effective_editor": 1, "editor_after": 2,
    "source_input": 2, "detector_input": 3, "prose_sha256": 3, "answer": 4,
    "answer_sha256": 4, "input": 5, "input_sha256": 5, "source_sha256": 6,
    "submitted": 7, "submitted_sha256": 7, "full_message": 8, "full_message_sha256": 8,
}
PATH_KEYS = {"input", "source_input", "text_path", "source", "path"}
NESTED_SCORE_KEYS = ("scores", "confidences", "metrics", "confidence_percent")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def is_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def index_study_texts(root):
    """Map SHA-256 to repo-relative paths of study text files."""
    index = {}
    studies = root / "studies"
    for path in studies.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".txt", ".md"}:
            continue
        if "private" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        index.setdefault(digest(path.read_bytes()), []).append(rel)
    return index


def confidence_owner(obj):
    """Return (ai, mixed, human) when this object is the record that owns them."""
    if is_number(obj.get("ai_percent")) and "human_percent" in obj:
        return obj["ai_percent"], obj.get("mixed_percent"), obj["human_percent"]
    for key in NESTED_SCORE_KEYS:
        child = obj.get(key)
        if isinstance(child, dict) and is_number(child.get("ai")) and "human" in child:
            return child["ai"], child.get("mixed"), child["human"]
    if is_number(obj.get("ai")) and "human" in obj and ("detector" in obj or "service" in obj):
        return obj["ai"], obj.get("mixed"), obj["human"]
    return None


def looks_gptzero(obj):
    if not isinstance(obj, dict):
        return False
    for key in ("detector", "service"):
        value = obj.get(key)
        if isinstance(value, str) and value.lower() == "gptzero":
            return True
    return False


def nearest_string(obj, ancestors, key):
    for item in (obj, *ancestors):
        value = item.get(key) if isinstance(item, dict) else None
        if isinstance(value, str) and value.strip() and len(value) < 80:
            return value
    return None


def nearest_bool(obj, ancestors, key):
    for item in (obj, *ancestors):
        value = item.get(key) if isinstance(item, dict) else None
        if type(value) is bool:
            return value
    return None


def nearest_int(obj, ancestors, keys):
    for item in (obj, *ancestors):
        if not isinstance(item, dict):
            continue
        for key in keys:
            value = item.get(key)
            if type(value) is int:
                return value
    return None


def resolve_path(root, json_file, name):
    if not isinstance(name, str) or not name.strip():
        return None
    path = Path(name)
    if path.is_absolute() or ".." in path.parts:
        return None
    for base in (root, json_file.parent):
        candidate = base / path
        try:
            candidate.resolve().relative_to(root.resolve())
        except ValueError:
            continue
        if candidate.is_file():
            return candidate
    return None


def iter_bindings(obj, key, depth, out):
    if depth > 5:
        return
    priority = KEY_PRIORITY.get(key, 9)
    if isinstance(obj, dict):
        sha = obj.get("sha256")
        path = obj.get("path") if isinstance(obj.get("path"), str) else None
        if isinstance(sha, str) and SHA256.fullmatch(sha):
            out.append((priority, sha, path))
        for child_key, value in obj.items():
            if child_key == "sha256":
                continue
            if isinstance(value, str) and child_key.endswith("sha256") and SHA256.fullmatch(value):
                out.append((KEY_PRIORITY.get(child_key, 9), value, None))
            elif isinstance(value, str) and (child_key in PATH_KEYS or child_key.endswith("path")):
                out.append((KEY_PRIORITY.get(child_key, 9), None, value))
            elif isinstance(value, (dict, list)):
                iter_bindings(value, child_key, depth + 1, out)
    elif isinstance(obj, list):
        for value in obj:
            iter_bindings(value, key, depth + 1, out)


def choose_binding(obj, root, json_file, index):
    bindings = []
    iter_bindings(obj, "", 0, bindings)
    resolved = []
    for priority, sha, path in bindings:
        file_path = resolve_path(root, json_file, path) if path else None
        file_sha = digest(file_path.read_bytes()) if file_path else None
        if sha and file_sha and sha != file_sha:
            continue
        use_sha = sha or file_sha
        if use_sha not in index:
            continue
        if file_path is not None and file_sha == use_sha:
            chosen = file_path.relative_to(root).as_posix()
        else:
            chosen = min(index[use_sha])
        resolved.append((priority, use_sha, chosen))
    if not resolved:
        return None
    resolved.sort()
    return {"sha256": resolved[0][1], "path": resolved[0][2]}


def collect_hits(root, index):
    hits = []
    unbound = []
    studies = root / "studies"
    for json_file in sorted(studies.rglob("*.json")):
        if "private" in json_file.parts:
            continue
        try:
            payload = json.loads(json_file.read_text(encoding="utf-8"))
        except (UnicodeError, json.JSONDecodeError):
            continue
        rel = json_file.relative_to(root).as_posix()

        def walk(obj, ancestors, evidence, source):
            if isinstance(obj, dict):
                found = confidence_owner(obj)
                if found and any(looks_gptzero(item) for item in (obj, *ancestors)):
                    ai, mixed, human = found
                    numbers = [value for value in (ai, mixed, human) if value is not None]
                    if is_number(ai) and is_number(human) and all(is_number(value) for value in numbers):
                        binding = choose_binding(obj, root, source, index)
                        if binding is None:
                            unbound.append(evidence)
                        else:
                            hits.append({
                                "sha256": binding["sha256"], "path": binding["path"],
                                "ai": ai, "mixed": mixed, "human": human,
                                "model": nearest_string(obj, ancestors, "model"),
                                "mode": nearest_string(obj, ancestors, "mode"),
                                "short_text_warning": nearest_bool(obj, ancestors, "short_text_warning"),
                                "displayed_words": nearest_int(
                                    obj, ancestors, ("displayed_words", "words", "words_charged",
                                                     "words_displayed", "ui_words")),
                                "evidence": evidence,
                            })
                for value in obj.values():
                    if isinstance(value, (dict, list)):
                        walk(value, (obj, *ancestors), evidence, source)
            elif isinstance(obj, list):
                for value in obj:
                    if isinstance(value, (dict, list)):
                        walk(value, ancestors, evidence, source)

        walk(payload, (), rel, json_file)
    return hits, unbound


def load_gptzero_corpus(root):
    """Unique archived GPTZero texts, keyed by the exact file bytes we can hash."""
    root = Path(root).resolve()
    index = index_study_texts(root)
    hits, unbound = collect_hits(root, index)
    grouped = {}
    for hit in hits:
        grouped.setdefault(hit["sha256"], []).append(hit)
    records = []
    conflicts = []
    for sha, group in sorted(grouped.items()):
        outcomes = {(item["ai"], item["mixed"], item["human"]) for item in group}
        if len(outcomes) > 1:
            conflicts.append({"sha256": sha, "outcomes": sorted(outcomes),
                              "evidence": sorted({item["evidence"] for item in group})})
            continue
        ai, mixed, human = next(iter(outcomes))
        path = min(item["path"] for item in group)
        raw = (root / path).read_bytes()
        require(digest(raw) == sha, f"Index path does not match its hash: {path}")
        text = raw.decode("utf-8")
        models = sorted({item["model"] for item in group if item["model"]})
        records.append({
            "id": sha[:16], "sha256": sha,
            "stripped_sha256": digest(text.rstrip().encode("utf-8")),
            "path": path,
            "ai": ai, "mixed": mixed, "human": human,
            "model": models[0] if len(models) == 1 else None,
            "models": models,
            "modes": sorted({item["mode"] for item in group if item["mode"]}),
            "short_text_warning": next((item["short_text_warning"] for item in group
                                        if item["short_text_warning"] is not None), None),
            "displayed_words": next((item["displayed_words"] for item in group
                                     if item["displayed_words"] is not None), None),
            "whitespace_words": len(text.split()),
            "evidence": sorted({item["evidence"] for item in group}),
            "observations": len(group),
        })
    return {"schema_version": 1, "service": "GPTZero", "unit": "document_confidence_percent",
            "records": records, "conflicts": conflicts, "unbound_score_objects": len(unbound),
            "raw_hits": len(hits)}


def load_archived_pairs(root, records):
    """The ten predeclared comparisons in studies/open-detector-proxy-1."""
    root = Path(root)
    study = root / "studies/open-detector-proxy-1"
    corpus = json.loads((study / "corpus.json").read_text(encoding="utf-8"))
    targets = json.loads((study / "targets.json").read_text(encoding="utf-8"))
    by_sha = {record["sha256"]: record for record in records}
    id_sha = {}
    for item in corpus["inputs"]:
        path = study / item["path"]
        raw = path.read_bytes()
        require(digest(raw) == item["sha256"], f"Proxy input hash changed: {item['id']}")
        id_sha[item["id"]] = item["sha256"]
    pairs = []
    for pair in targets["pairs"]:
        baseline = by_sha.get(id_sha[pair["baseline"]])
        candidate = by_sha.get(id_sha[pair["candidate"]])
        require(baseline is not None and candidate is not None,
                f"Archived pair {pair['id']} is not in the labelled corpus")
        pairs.append({"id": pair["id"], "case": pair["case"], "intervention": pair["intervention"],
                      "baseline_sha256": baseline["sha256"], "candidate_sha256": candidate["sha256"],
                      "baseline_ai": baseline["ai"], "candidate_ai": candidate["ai"]})
    return pairs


def human_control_records(root):
    root = Path(root)
    directory = root / "studies/open-detector-proxy-1/review"
    meta = json.loads((directory / "human-controls.json").read_text(encoding="utf-8"))
    records = []
    texts = meta.get("controls") or meta.get("records") or meta.get("texts")
    if isinstance(texts, list):
        for item in texts:
            if not isinstance(item, dict):
                continue
            name = item.get("path") or item.get("file")
            path = resolve_path(root, directory / "human-controls.json", name) if name else None
            if path is None:
                continue
            raw = path.read_bytes()
            records.append({"id": "human-" + digest(raw)[:12], "sha256": digest(raw),
                            "path": path.relative_to(root).as_posix(), "ai": None,
                            "origin": "public_domain_human", "whitespace_words": len(raw.decode("utf-8").split())})
    if records:
        return records
    for path in sorted(directory.glob("human-control-*.txt")):
        raw = path.read_bytes()
        records.append({"id": "human-" + digest(raw)[:12], "sha256": digest(raw),
                        "path": path.relative_to(root).as_posix(), "ai": None,
                        "origin": "public_domain_human", "whitespace_words": len(raw.decode("utf-8").split())})
    return records


def ranks(values):
    order = sorted(range(len(values)), key=lambda index: values[index])
    ranked = [0.0] * len(values)
    start = 0
    while start < len(values):
        end = start
        while end + 1 < len(values) and values[order[end + 1]] == values[order[start]]:
            end += 1
        average = (start + end) / 2 + 1
        for cursor in range(start, end + 1):
            ranked[order[cursor]] = average
        start = end + 1
    return ranked


def pearson(xs, ys):
    count = len(xs)
    if count < 3:
        return None
    mean_x = sum(xs) / count
    mean_y = sum(ys) / count
    diff_x = [value - mean_x for value in xs]
    diff_y = [value - mean_y for value in ys]
    numerator = sum(left * right for left, right in zip(diff_x, diff_y))
    spread_x = math.sqrt(sum(value * value for value in diff_x))
    spread_y = math.sqrt(sum(value * value for value in diff_y))
    if spread_x == 0 or spread_y == 0:
        return None
    return numerator / (spread_x * spread_y)


def spearman(xs, ys):
    if len(xs) != len(ys) or len(xs) < 3:
        return None
    return pearson(ranks(xs), ranks(ys))


def movement(before, after, margin):
    delta = after - before
    if delta < 0 and delta <= -margin:
        return "lower"
    if delta > 0 and delta >= margin:
        return "higher"
    return "flat"


def binoculars_score(log_perplexity, log_cross_perplexity):
    """Ratio from Hans et al., equation 4. Lower scores were the machine side."""
    require(is_number(log_perplexity) and is_number(log_cross_perplexity), "Nonfinite Binoculars input")
    require(log_perplexity > 0 and log_cross_perplexity > 0, "Binoculars logs must be positive")
    return log_perplexity / log_cross_perplexity


def curvature_from_rows(rows):
    """Analytical same-model conditional curvature (Bao et al., equation 5).

    Each row is (observed_logprob, probabilities). Higher curvature was the
    machine side in that paper. Returns None when the variance is zero.
    """
    require(rows, "Curvature needs at least one token")
    total_logprob = 0.0
    total_mean = 0.0
    total_variance = 0.0
    for observed, probabilities in rows:
        require(is_number(observed), "Nonfinite observed log probability")
        require(probabilities and all(is_number(value) and value >= 0 for value in probabilities),
                "Invalid probability row")
        mass = sum(probabilities)
        require(abs(mass - 1) < 1e-5, "Probability row must sum to 1")
        mean = 0.0
        for probability in probabilities:
            if probability > 0:
                mean += probability * math.log(probability)
        variance = 0.0
        for probability in probabilities:
            if probability > 0:
                gap = math.log(probability) - mean
                variance += probability * gap * gap
        total_logprob += observed
        total_mean += mean
        total_variance += variance
    if total_variance <= 1e-12:
        return None
    return (total_logprob - total_mean) / math.sqrt(total_variance)


def mean_cross_entropy(observer_rows, performer_rows):
    """Mean token cross-entropy H(observer, performer), the Binoculars denominator."""
    require(len(observer_rows) == len(performer_rows) and observer_rows, "Cross-entropy rows differ")
    total = 0.0
    for observer, performer in zip(observer_rows, performer_rows):
        require(len(observer) == len(performer), "Cross-entropy vocabularies differ")
        step = 0.0
        for left, right in zip(observer, performer):
            require(left >= 0 and right > 0, "Cross-entropy needs a positive performer probability")
            if left > 0:
                step -= left * math.log(right)
        total += step
    return total / len(observer_rows)


def oriented(value, higher_is_ai):
    return value if higher_is_ai else -value


def summarize_metric(records, values_by_sha, pairs, higher_is_ai):
    paired = []
    seen_text = set()
    for record in records:
        value = values_by_sha.get(record["sha256"])
        if value is None or record.get("ai") is None:
            continue
        # Trailing editor newlines produced a second archived scan of the same words.
        key = record.get("stripped_sha256", record["sha256"])
        if key in seen_text:
            continue
        seen_text.add(key)
        paired.append((record, value))
    scores = [oriented(value, higher_is_ai) for _, value in paired]
    labels = [record["ai"] for record, _ in paired]
    below = [(score, label) for score, label in zip(scores, labels) if label < 100]
    ceiling = [score for score, label in zip(scores, labels) if label >= 100]
    short = [(score, label, record) for (record, _), score, label in zip(paired, scores, labels)
             if record["whitespace_words"] <= SHORT_WORDS]
    very_short = [item for item in short if item[2]["whitespace_words"] < WARNING_WORDS]

    def separation(rows_low, rows_high):
        if not rows_low or not rows_high:
            return None
        midpoint = statistics.median(rows_high)
        return sum(score < midpoint for score in rows_low) / len(rows_low)

    def pair_counts(margin):
        recognized = false_lower = considered_reductions = considered_ties = 0
        details = []
        for pair in pairs:
            before = values_by_sha.get(pair["baseline_sha256"])
            after = values_by_sha.get(pair["candidate_sha256"])
            if before is None or after is None:
                continue
            gptzero = movement(pair["baseline_ai"], pair["candidate_ai"], margin)
            proxy = movement(oriented(before, higher_is_ai), oriented(after, higher_is_ai), 0)
            if gptzero == "lower":
                considered_reductions += 1
                recognized += proxy == "lower"
            if pair["candidate_ai"] == pair["baseline_ai"]:
                considered_ties += 1
                false_lower += proxy == "lower"
            details.append({"id": pair["id"], "gptzero": gptzero, "proxy": proxy,
                            "gptzero_ai": [pair["baseline_ai"], pair["candidate_ai"]],
                            "proxy_raw": [before, after]})
        return {"gptzero_margin_points": margin, "reductions_recognized": recognized,
                "reductions": considered_reductions,
                "ties_with_a_proxy_decrease": false_lower, "exact_ties": considered_ties,
                "pairs": details}

    return {
        "n": len(paired),
        "higher_is_ai": higher_is_ai,
        "spearman_oriented_vs_ai_percent": spearman(scores, labels),
        "spearman_below_ceiling": spearman([score for score, _ in below], [label for _, label in below]),
        "n_below_ceiling": len(below),
        "n_at_ceiling": len(ceiling),
        "ceiling_median_separation": separation([score for score, _ in below], ceiling),
        "short_words_at_most": SHORT_WORDS,
        "n_short": len(short),
        "n_short_below_ceiling": sum(label < 100 for _, label, _ in short),
        "spearman_short": spearman([item[0] for item in short], [item[1] for item in short]),
        "n_under_100_words": len(very_short),
        "n_under_100_words_below_ceiling": sum(label < 100 for _, label, _ in very_short),
        "archived_pairs_at_5_points": pair_counts(GPTZERO_REDUCTION_POINTS),
        "archived_pairs_any_decrease": pair_counts(0),
    }


def summarize(records, metric_values, metric_directions, pairs):
    report = {}
    for name, higher_is_ai in metric_directions.items():
        report[name] = summarize_metric(records, metric_values.get(name, {}), pairs, higher_is_ai)
    return report


def read_text(root, record):
    return (Path(root) / record["path"]).read_text(encoding="utf-8")


def sentence_spans(text):
    spans = []
    cursor = 0
    for match in SENTENCE.finditer(text):
        spans.append((match.start(), match.end()))
        cursor = match.end()
    if cursor < len(text) and text[cursor:].strip():
        spans.append((cursor, len(text)))
    return spans


def burstiness(text, offsets, token_logprobs):
    """Stdev of per-sentence mean log probability. None when fewer than two sentences."""
    spans = sentence_spans(text)
    buckets = [[] for _ in spans]
    # token_logprobs[i] is the log probability of the token at offsets[i + 1].
    for index, logprob in enumerate(token_logprobs):
        target = index + 1
        if target >= len(offsets):
            break
        start, _end = offsets[target]
        for bucket, (left, right) in zip(buckets, spans):
            if left <= start < right:
                bucket.append(logprob)
                break
    means = [sum(bucket) / len(bucket) for bucket in buckets if bucket]
    if len(means) < 2:
        return None
    return statistics.pstdev(means)


def score_causal_text(model, tokenizer, text, torch):
    encoded = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True, truncation=False)
    ids = encoded["input_ids"]
    offsets = encoded["offset_mapping"]
    limit = getattr(model.config, "max_position_embeddings", None)
    if not isinstance(limit, int) or limit > 100000:
        limit = 1024
    if len(ids) < 2:
        return {"status": "too_short", "tokens": len(ids)}
    if len(ids) > limit:
        return {"status": "over_length", "tokens": len(ids), "limit": limit}
    input_ids = torch.tensor([ids])
    with torch.inference_mode():
        logits = model(input_ids=input_ids).logits[0, :-1]
        log_probs = torch.log_softmax(logits.float(), dim=-1)
    targets = ids[1:]
    observed = log_probs[range(len(targets)), targets]
    mean_logprob = float(observed.mean())
    probabilities = torch.softmax(logits.float(), dim=-1)
    mean = (probabilities * log_probs).sum(dim=-1)
    variance = (probabilities * (log_probs - mean.unsqueeze(-1)) ** 2).sum(dim=-1)
    total_variance = float(variance.sum())
    curvature = None if total_variance <= 1e-12 else float((observed.sum() - mean.sum()) / math.sqrt(total_variance))
    return {"status": "complete", "tokens": len(ids),
            "log_perplexity": -mean_logprob, "curvature": curvature,
            "burstiness": burstiness(text, offsets, [float(value) for value in observed])}


def score_classifier_text(model, tokenizer, text, torch, ai_index, max_tokens):
    encoded = tokenizer(text, add_special_tokens=True, truncation=False, return_tensors="pt")
    tokens = int(encoded["input_ids"].shape[1])
    if tokens > max_tokens:
        return {"status": "over_length", "tokens": tokens, "limit": max_tokens}
    with torch.inference_mode():
        logits = model(**encoded).logits[0].float()
        probabilities = torch.softmax(logits, dim=-1)
    return {"status": "complete", "tokens": tokens, "ai_probability": float(probabilities[ai_index])}


def ai_label_index(config):
    labels = {int(key): value for key, value in config.id2label.items()}
    ai_names = {"fake", "ai", "chatgpt"}
    matches = [index for index, name in labels.items() if str(name).lower() in ai_names]
    require(len(matches) == 1, f"Could not find one AI label in {labels}")
    return matches[0], {str(index): name for index, name in labels.items()}


class MeanPoolDetector:
    """Masked-mean pool plus one logit. Same calculation as the pinned Desklib scorer."""

    def __init__(self, model_dir, max_tokens):
        import torch
        from safetensors.torch import load_file
        from transformers import AutoConfig, AutoModel, AutoTokenizer

        config = AutoConfig.from_pretrained(model_dir, local_files_only=True, trust_remote_code=False)
        require(config.model_type == "deberta-v2", "Expected a DeBERTa-v2 detector")

        class Network(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.model = AutoModel.from_config(config, trust_remote_code=False)
                self.classifier = torch.nn.Linear(config.hidden_size, 1)

            def forward(self, input_ids, attention_mask):
                hidden = self.model(input_ids, attention_mask=attention_mask)[0]
                mask = attention_mask.unsqueeze(-1).expand(hidden.size()).float()
                pooled = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1e-9)
                return self.classifier(pooled.to(self.classifier.weight.dtype))

        self.torch = torch
        self.max_tokens = max_tokens
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True, trust_remote_code=False)
        self.network = Network()
        state = load_file(str(Path(model_dir) / "model.safetensors"), device="cpu")
        self.network.load_state_dict(state, strict=True)
        del state
        self.network.eval()

    def score(self, text):
        ids = self.tokenizer(text, add_special_tokens=True, padding=False, truncation=False)["input_ids"]
        if len(ids) > self.max_tokens:
            return {"status": "over_length", "tokens": len(ids), "limit": self.max_tokens}
        input_ids = self.torch.tensor([ids])
        mask = self.torch.ones_like(input_ids)
        with self.torch.inference_mode():
            logit = float(self.network(input_ids, mask).reshape(-1)[0])
        if logit >= 0:
            probability = 1.0 / (1.0 + math.exp(-logit))
        else:
            value = math.exp(logit)
            probability = value / (1.0 + value)
        return {"status": "complete", "tokens": len(ids), "raw_logit": logit, "ai_probability": probability}


def release(obj):
    del obj
    gc.collect()


def write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


GENERATIVE_MODELS = (
    "distilbert/distilgpt2", "openai-community/gpt2", "openai-community/gpt2-medium",
    "HuggingFaceTB/SmolLM2-360M", "Qwen/Qwen2.5-0.5B",
)
# Performer supplies the numerator perplexity. Observer is M1 in H(M1, M2).
BINOCULAR_PAIRS = (
    ("binoculars__gpt2_distilgpt2", "openai-community/gpt2", "distilbert/distilgpt2"),
    ("binoculars__gpt2medium_gpt2", "openai-community/gpt2-medium", "openai-community/gpt2"),
    ("binoculars__smollm2_360m", "HuggingFaceTB/SmolLM2-360M-Instruct", "HuggingFaceTB/SmolLM2-360M"),
    ("binoculars__qwen2.5_0.5b", "Qwen/Qwen2.5-0.5B-Instruct", "Qwen/Qwen2.5-0.5B"),
)
CLASSIFIERS = (
    ("classifier__openai_roberta", "openai-community/roberta-base-openai-detector", 512),
    ("classifier__hc3_roberta", "Hello-SimpleAI/chatgpt-detector-roberta", 512),
    ("classifier__fakespot_roberta", "fakespot-ai/roberta-base-ai-text-detection-v1", 512),
)
MEAN_POOLS = (
    ("desklib__ai_probability", "desklib/ai-text-detector-v1.01", 768),
    ("oculus__ai_probability", "danibor/oculus-v2.0-multilingual", 512),
)
CAUSAL_FEATURES = {"log_perplexity": False, "curvature": True, "burstiness": False}


def slug(model_id):
    return model_id.replace("/", "__")


def load_model_index(path):
    index_file = Path(path).resolve()
    payload = json.loads(index_file.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), "Model index must be an object")
    for model_id, meta in payload.items():
        require(isinstance(meta, dict) and isinstance(meta.get("path"), str), f"Missing path for {model_id}")
        raw = Path(meta["path"])
        found = None
        candidates = [raw] if raw.is_absolute() else []
        candidates += [base / raw for base in (Path.cwd(), index_file.parent, index_file.parent.parent)]
        for candidate in candidates:
            if candidate.is_dir():
                found = candidate.resolve()
                break
        require(found is not None, f"Model path not found for {model_id}: {meta['path']}")
        meta["path"] = str(found)
    return payload


def scoring_texts(root, corpus):
    rows = []
    for record in list(corpus["records"]) + list(corpus.get("human_controls") or []):
        rows.append((record["sha256"], read_text(root, record)))
    return rows


def ensure_metric(scores, name, higher_is_ai, model_id):
    metrics = scores.setdefault("metrics", {})
    metric = metrics.setdefault(name, {"higher_is_ai": higher_is_ai, "model_id": model_id,
                                       "by_sha": {}, "status_counts": {}})
    require(metric["higher_is_ai"] is higher_is_ai, f"Direction changed for {name}")
    return metric


def add_status(metric, status):
    counts = metric["status_counts"]
    counts[status] = counts.get(status, 0) + 1


def score_one_causal(model_id, model_dir, texts, scores):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(4)
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(model_dir, local_files_only=True, dtype=torch.float32)
    model.eval()
    features = {feature: ensure_metric(scores, f"{slug(model_id)}__{feature}", direction, model_id)
                for feature, direction in CAUSAL_FEATURES.items()}
    done = set(features["log_perplexity"]["by_sha"])
    for sha, text in texts:
        if sha in done:
            continue
        result = score_causal_text(model, tokenizer, text, torch)
        status = result["status"]
        for feature, metric in features.items():
            add_status(metric, status)
            if status == "complete":
                metric["by_sha"][sha] = result[feature]
        done.add(sha)
    release(model)
    return tokenizer


def score_one_binocular(name, performer_id, observer_id, paths, texts, scores, tokenizers):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(4)
    metric = ensure_metric(scores, name, False, performer_id + " | " + observer_id)
    performer = AutoModelForCausalLM.from_pretrained(paths[performer_id], local_files_only=True, dtype=torch.float32)
    observer = AutoModelForCausalLM.from_pretrained(paths[observer_id], local_files_only=True, dtype=torch.float32)
    performer.eval()
    observer.eval()
    performer_tok = tokenizers.get(performer_id) or AutoTokenizer.from_pretrained(
        paths[performer_id], local_files_only=True)
    observer_tok = tokenizers.get(observer_id) or AutoTokenizer.from_pretrained(
        paths[observer_id], local_files_only=True)
    done = set(metric["by_sha"])
    for sha, text in texts:
        if sha in done:
            continue
        performer_ids = performer_tok.encode(text, add_special_tokens=False)
        observer_ids = observer_tok.encode(text, add_special_tokens=False)
        if performer_ids != observer_ids or len(performer_ids) < 2:
            add_status(metric, "tokenization_mismatch" if performer_ids != observer_ids else "too_short")
            continue
        limit = min(getattr(performer.config, "max_position_embeddings", 1024),
                    getattr(observer.config, "max_position_embeddings", 1024))
        if len(performer_ids) > limit:
            add_status(metric, "over_length")
            continue
        input_ids = torch.tensor([performer_ids])
        with torch.inference_mode():
            performer_log = torch.log_softmax(performer(input_ids=input_ids).logits[0, :-1].float(), dim=-1)
            observer_log = torch.log_softmax(observer(input_ids=input_ids).logits[0, :-1].float(), dim=-1)
        targets = performer_ids[1:]
        log_perplexity = float(-performer_log[range(len(targets)), targets].mean())
        cross = float((-(observer_log.exp() * performer_log).sum(dim=-1)).mean())
        metric["by_sha"][sha] = binoculars_score(log_perplexity, cross)
        add_status(metric, "complete")
    release(performer)
    release(observer)


def score_one_classifier(name, model_id, model_dir, max_tokens, texts, scores):
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    torch.set_num_threads(4)
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_dir, local_files_only=True, dtype=torch.float32)
    model.eval()
    ai_index, labels = ai_label_index(model.config)
    metric = ensure_metric(scores, name, True, model_id)
    metric["labels"] = labels
    metric["ai_index"] = ai_index
    metric["preprocessing"] = "raw text; no publisher cleaning"
    done = set(metric["by_sha"])
    for sha, text in texts:
        if sha in done:
            continue
        result = score_classifier_text(model, tokenizer, text, torch, ai_index, max_tokens)
        add_status(metric, result["status"])
        if result["status"] == "complete":
            metric["by_sha"][sha] = result["ai_probability"]
    release(model)


def score_one_mean_pool(name, model_id, model_dir, max_tokens, texts, scores):
    metric = ensure_metric(scores, name, True, model_id)
    metric["padding"] = "none; masked mean ignores pad positions"
    metric["max_tokens"] = max_tokens
    detector = MeanPoolDetector(model_dir, max_tokens)
    done = set(metric["by_sha"])
    for sha, text in texts:
        if sha in done:
            continue
        result = detector.score(text)
        add_status(metric, result["status"])
        if result["status"] == "complete":
            metric["by_sha"][sha] = result["ai_probability"]
    release(detector)


def score_command(root, model_index, output, only):
    import torch
    corpus = load_gptzero_corpus(root)
    corpus["pairs"] = load_archived_pairs(root, corpus["records"])
    corpus["human_controls"] = human_control_records(root)
    texts = scoring_texts(root, corpus)
    index = load_model_index(model_index)
    scores = {"schema_version": 1, "torch": torch.__version__, "metrics": {}}
    if Path(output).exists():
        scores = json.loads(Path(output).read_text(encoding="utf-8"))
    paths = {}
    for model_id, meta in index.items():
        require(isinstance(meta, dict) and meta.get("path"), f"Missing path for {model_id}")
        paths[model_id] = meta["path"]
    tokenizers = {}
    for model_id in GENERATIVE_MODELS:
        if only and model_id not in only and slug(model_id) not in only:
            continue
        print(f"scoring {model_id}", flush=True)
        tokenizers[model_id] = score_one_causal(model_id, paths[model_id], texts, scores)
        write_json(output, scores)
    for name, performer_id, observer_id in BINOCULAR_PAIRS:
        if only and name not in only:
            continue
        print(f"scoring {name}", flush=True)
        score_one_binocular(name, performer_id, observer_id, paths, texts, scores, tokenizers)
        write_json(output, scores)
    for name, model_id, max_tokens in CLASSIFIERS:
        if only and name not in only and model_id not in only:
            continue
        print(f"scoring {name}", flush=True)
        score_one_classifier(name, model_id, paths[model_id], max_tokens, texts, scores)
        write_json(output, scores)
    for name, model_id, max_tokens in MEAN_POOLS:
        if only and name not in only and model_id not in only:
            continue
        print(f"scoring {name}", flush=True)
        score_one_mean_pool(name, model_id, paths[model_id], max_tokens, texts, scores)
        write_json(output, scores)
    print(json.dumps({"metrics": sorted(scores["metrics"]), "output": str(output)}))


def report_command(root, scores_path, output):
    corpus = load_gptzero_corpus(root)
    pairs = load_archived_pairs(root, corpus["records"])
    scores = json.loads(Path(scores_path).read_text(encoding="utf-8"))
    directions = {name: metric["higher_is_ai"] for name, metric in scores["metrics"].items()}
    values = {name: metric["by_sha"] for name, metric in scores["metrics"].items()}
    summary = summarize(corpus["records"], values, directions, pairs)
    labelled = [record for record in corpus["records"]]
    payload = {
        "schema_version": 1,
        "corpus": {"records": len(labelled), "conflicts": len(corpus["conflicts"]),
                   "below_ceiling": sum(record["ai"] < 100 for record in labelled),
                   "at_ceiling": sum(record["ai"] >= 100 for record in labelled),
                   "words_at_most_130": sum(record["whitespace_words"] <= SHORT_WORDS for record in labelled),
                   "words_under_100": sum(record["whitespace_words"] < WARNING_WORDS for record in labelled),
                   "under_100_words_below_ceiling": sum(
                       record["ai"] < 100 and record["whitespace_words"] < WARNING_WORDS for record in labelled),
                   "models": sorted({record["model"] for record in labelled})},
        "pairs": len(pairs),
        "metrics": summary,
        "status_counts": {name: metric.get("status_counts") for name, metric in scores["metrics"].items()},
    }
    write_json(output, payload)
    print(json.dumps({"metrics": len(summary), "output": str(output)}))


def corpus_command(root, output):
    payload = load_gptzero_corpus(root)
    payload["pairs"] = load_archived_pairs(root, payload["records"])
    payload["human_controls"] = human_control_records(root)
    write_json(output, payload)
    print(json.dumps({"records": len(payload["records"]), "conflicts": len(payload["conflicts"]),
                      "unbound_score_objects": payload["unbound_score_objects"],
                      "pairs": len(payload["pairs"]), "human_controls": len(payload["human_controls"])}))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("corpus", "score", "report"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-index", type=Path)
    parser.add_argument("--scores", type=Path)
    parser.add_argument("--only", default="", help="Comma-separated model ids or metric names to run")
    args = parser.parse_args(argv)
    only = [item for item in args.only.split(",") if item]
    try:
        if args.command == "corpus":
            corpus_command(args.root, args.output)
        elif args.command == "score":
            require(args.model_index is not None, "score needs --model-index")
            score_command(args.root, args.model_index, args.output, only)
        else:
            require(args.scores is not None, "report needs --scores")
            report_command(args.root, args.scores, args.output)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, ImportError, RuntimeError) as error:
        print(f"Proxy detector failed: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
