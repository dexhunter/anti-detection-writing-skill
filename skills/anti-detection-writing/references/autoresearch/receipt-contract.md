# Native detector receipts

These receipts belong to the autoresearch adapter, not the earlier strict plain-text receipt checker. The adapter verifies consistency of saved evidence. It cannot authenticate a service, prove agent independence or establish authorship. Keep raw receipts private.

Each artifact is an object with `path` relative to the receipt directory and its exact UTF-8/binary `sha256`. Parent traversal and escaping symlinks are rejected. The coordinator imports the receipt and every referenced artifact into its reserved attempt. A bad import remains a charged, invalid outcome; do not edit the files to turn it into a successful measurement.

The receipt's `answer` is the frozen detector input: the derived prose for a `prose_only` run, or the complete message for `full_text`. The controller retains the full reviewed output, code-range mapping and measured-input hash separately, and validates the receipt against that measured input without relaxing this adapter's exact-byte checks. The worker must receive the declared scope and report it with the result. An optional receipt `scan_scope` must match the frozen run; when absent, the controller supplies the run's scope. A prose-only receipt is not a detector result for the complete message or its code.

```json
{
  "schema_version": 1,
  "detector": "gptzero",
  "mode": "Basic Scan",
  "model": "4.9b",
  "status": "complete",
  "observed_at": "2026-09-06T22:00:00Z",
  "entry_transform": "gptzero_code_block_v1",
  "short_text_warning": false,
  "warnings": [],
  "answer": {"path": "answer.txt", "sha256": "actual file hash"},
  "submitted": {"path": "submitted.txt", "sha256": "actual file hash"},
  "editor_before": {"path": "editor-before.txt", "sha256": "actual file hash"},
  "editor_after": {"path": "editor-after.txt", "sha256": "actual file hash"},
  "visible_result": {"path": "result-ui.txt", "sha256": "actual file hash"},
  "screenshot": {"path": "result.jpg", "sha256": "actual file hash"}
}
```

The example illustrates fields; its date and hash labels are not evidence. Use the version and time actually observed on the completed result. `observed_at` must follow the reservation. Optional `metrics` must contain `ai`, `mixed`, `human`, `ai_assisted`, with null for unavailable fields, and must agree with the UI. The parser derives the measurements from native visible controls even when this optional object is omitted.

## GPTZero Basic

`gptzero_code_block_v1` removes exactly one terminal source LF if present, then records the observed editor as submitted text plus exactly three LF characters. Read the editor both before and after completion. The snapshot must contain the matching literal code body, unique Basic Scan heading, unique current model, Text up-to-date and all three confidence buttons. Stale/processing indicators invalidate the receipt. The accessibility snapshot folds displayed whitespace; its body check is additional to, and does not replace, the exact editor-byte checks.

`verbatim_v1` accepts identical source, submission and editor bytes and a matching single-paragraph input snapshot. Other rendering modes require a separately implemented and tested adapter; do not silently normalize them.

Wait until scanning completes before navigating to the Basic result view. A created document URL or an old confidence value is not sufficient. Retain any short-text warning. A result of 100% is valid observed data, even though it provides no reduction in a tied pair.

## Pangram

Use `detector: "pangram"`, `mode: "Free text detection"`, the displayed version such as `model: "4.0"`, and `entry_transform: "pangram_textarea_v1"`. Add `rendered` and `details_ui` artifact objects. `visible_result` is the Overview snapshot. The submitted and pre-scan textarea must equal the answer exactly. The supported result display trims ASCII space/tab/CR from line edges, removes empty lines and joins the remainder with single LF characters. Store that rendered result in both `rendered` and `editor_after`; it is the displayed document, not the cleared textarea or a claim about model preprocessing.

Both snapshots must contain the matching document. Save native label, displayed AI/AI-assisted/human proportions and the Details segment-confidence labels. Undisplayed categories stay null. AI-assisted is not human. The adapter refuses contradictory processing evidence and retains short-text warnings. Current support covers the observed English UI; a changed UI must be checked before adapting the parser.

The worker separately retains input preview, result word count, quoted cost and actual account allowance. The controller's reservation is a budget ceiling and does not infer vendor billing from these word counts.
