#!/usr/bin/env python3
"""Exact byte crossover; enforces structure, never judges factual correctness."""

import argparse
import hashlib
import json
from pathlib import Path


class InvalidInput(ValueError):
    """The reviewed crossover cannot be executed as specified."""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidInput(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def claim_ids(value, label):
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        raise InvalidInput(f"{label} must be a nonempty list of claim IDs")
    if len(set(value)) != len(value):
        raise InvalidInput(f"{label} contains duplicate claim IDs")
    return set(value)


def check_offset(data, offset, label):
    if type(offset) is not int or not 0 < offset < len(data):
        raise InvalidInput(f"{label} must be an internal integer byte offset")
    try:
        data[:offset].decode("utf-8")
        data[offset:].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidInput(f"{label} splits a UTF-8 code point") from exc


def prepare(parent_a, parent_b, review_path, max_words=140):
    """Validate everything and return in-memory children and their manifest."""
    if type(max_words) is not int or max_words < 1:
        raise InvalidInput("max_words must be a positive integer")
    paths = {"A": Path(parent_a), "B": Path(parent_b)}
    parents = {key: path.read_bytes() for key, path in paths.items()}
    for key, data in parents.items():
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise InvalidInput(f"Parent {key} is not UTF-8") from exc
    review_bytes = Path(review_path).read_bytes()
    try:
        review = json.loads(review_bytes, object_pairs_hook=unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InvalidInput("Review must be valid UTF-8 JSON") from exc
    if not isinstance(review, dict):
        raise InvalidInput("Review must be an object")
    for key in parents:
        if review.get(f"parent_{key.lower()}_sha256") != digest(parents[key]):
            raise InvalidInput(f"Parent {key} hash does not match review")
    required = claim_ids(review.get("required_claim_ids"), "required_claim_ids")
    seams = review.get("approved_seams")
    if not isinstance(seams, list) or not seams:
        raise InvalidInput("No approved seams")
    seen = set()
    for index, seam in enumerate(seams):
        if not isinstance(seam, dict) or seam.get("source_review_pass") is not True:
            raise InvalidInput(f"Seam {index} lacks a passing source review")
        if not isinstance(seam.get("reason"), str) or not seam["reason"].strip():
            raise InvalidInput(f"Seam {index} lacks a review reason")
        a_offset, b_offset = seam.get("a_offset"), seam.get("b_offset")
        check_offset(parents["A"], a_offset, f"Seam {index} A offset")
        check_offset(parents["B"], b_offset, f"Seam {index} B offset")
        if (a_offset, b_offset) in seen:
            raise InvalidInput("Duplicate seam offsets")
        seen.add((a_offset, b_offset))
        prefix = claim_ids(seam.get("prefix_claim_ids"), f"Seam {index} prefix")
        suffix = claim_ids(seam.get("suffix_claim_ids"), f"Seam {index} suffix")
        if prefix & suffix or prefix | suffix != required:
            raise InvalidInput(f"Seam {index} does not partition required claims")
    index, seam = min(
        enumerate(seams),
        key=lambda item: (
            abs(2 * len(item[1]["prefix_claim_ids"]) - len(required)),
            item[1]["a_offset"],
            item[1]["b_offset"],
        ),
    )
    offsets = {"A": seam["a_offset"], "B": seam["b_offset"]}
    children = {}
    records = {}
    for child_id, (first, second) in {"A": ("A", "B"), "B": ("B", "A")}.items():
        prefix = parents[first][: offsets[first]]
        suffix = parents[second][offsets[second] :]
        child = prefix + suffix
        words = len(child.decode("utf-8").split())
        if not child.endswith(b"\n"):
            raise InvalidInput(f"Child {child_id} lacks a final LF")
        if words > max_words:
            raise InvalidInput(f"Child {child_id} exceeds the {max_words}-word limit")
        if child in parents.values():
            raise InvalidInput(f"Child {child_id} is a no-op identical to a parent")
        children[f"child-{child_id.lower()}.txt"] = child
        records[child_id] = {
            "file": f"child-{child_id.lower()}.txt",
            "sha256": digest(child),
            "bytes": len(child),
            "words": words,
            "final_lf": True,
            "spans": [
                {
                    "parent": first,
                    "source_start": 0,
                    "source_end": offsets[first],
                    "child_start": 0,
                    "child_end": len(prefix),
                },
                {
                    "parent": second,
                    "source_start": offsets[second],
                    "source_end": len(parents[second]),
                    "child_start": len(prefix),
                    "child_end": len(child),
                },
            ],
        }
    if len(set(children.values())) != 2:
        raise InvalidInput("Reciprocal children are identical")
    manifest = {
        "schema_version": 1,
        "role": "research diagnostic; not a factual validator or promoter",
        "assembly": "exact reciprocal byte concatenation; no inserted bytes",
        "range_convention": "zero-based UTF-8 bytes, start inclusive, end exclusive",
        "word_count": "Python str.split() over the complete UTF-8 input text",
        "max_words": max_words,
        "parents": {
            key: {"path": str(paths[key].resolve()), "sha256": digest(data), "bytes": len(data)}
            for key, data in parents.items()
        },
        "review": {"path": str(Path(review_path).resolve()), "sha256": digest(review_bytes)},
        "required_claim_ids": review["required_claim_ids"],
        "selected_seam_index": index,
        "selected_seam": seam,
        "selection_key": [
            abs(2 * len(seam["prefix_claim_ids"]) - len(required)),
            seam["a_offset"],
            seam["b_offset"],
        ],
        "children": records,
    }
    return children, manifest


def run(parent_a, parent_b, review_path, out, max_words=140):
    out = Path(out)
    if out.exists() or out.is_symlink():
        raise InvalidInput("Output path already exists; refusing overwrite")
    children, manifest = prepare(parent_a, parent_b, review_path, max_words)
    payloads = dict(children)
    payloads["manifest.json"] = (
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    # Exclusive directory creation also closes the exists()/mkdir() race.
    out.mkdir()
    created = []
    try:
        for filename, data in payloads.items():
            path = out / filename
            with path.open("xb") as handle:
                created.append(path)
                handle.write(data)
    except BaseException:
        for path in reversed(created):
            path.unlink()
        out.rmdir()
        raise
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-a", required=True, type=Path)
    parser.add_argument("--parent-b", required=True, type=Path)
    parser.add_argument("--review", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path, help="new output directory")
    parser.add_argument("--max-words", type=int, default=140)
    args = parser.parse_args()
    try:
        run(args.parent_a, args.parent_b, args.review, args.out, args.max_words)
    except (InvalidInput, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")
    print(f"Saved two exact hybrids and manifest to {args.out}")


if __name__ == "__main__":
    main()
