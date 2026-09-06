---
name: discussion-answer-polish
description: Improve source-grounded GitHub Discussion answers with claim tracking and a separate correctness review. Use when editing or preparing technical replies, or measuring before/after detector results when requested. Do not promise detector evasion or human authorship.
---

# Discussion answer polish

Answer the reader's question accurately and concisely. Separate writing quality, detector measurements, and permission to publish. Detector testing is optional and only runs when requested; a score is never evidence of correctness or human authorship.

## Establish the facts

1. Read the current question, comments, replies, and repository participation rules. For an edit, save the owned answer first. Respect explicit objections to AI-assisted participation and any disclosure requirements.
2. Inspect the relevant official documentation or implementation. Record its URL and version or commit where possible. Distinguish reading source, running a local test, and verifying a deployment. Do not claim any test you did not run.
3. Inventory the substantive claims, commands, code, conditions, uncertainty, and reported symptoms. For each claim record whether it is preserved, corrected, or removed, and why. Identify the action or decision the asker needs help with.

## Write and review

- Rebuild the answer around the question rather than retaining the original sentence order. Lead with the fix or explanation and include the detail needed to apply it.
- Prefer concrete nouns and verbs. Remove generic reassurance, repeated summaries, rhetorical contrasts, and irrelevant background. Use lists only where they make steps or comparisons easier to follow.
- Preserve operational qualifications and exact code unless evidence supports a correction. Record deliberate scope cuts; do not call an answer fully claim-preserving when useful details were removed.
- Use an authentic writing sample for tone only when supplied. Never invent personal experience, tests, certainty, identity, quotations, typos, or invisible characters to make text appear human-written.
- A short, exact asker quotation can identify the concern being answered. Include it only when it helps the reader. Verify context and attribution; do not pad or rotate quotations to hunt for a detector score.
- When a separate reviewer is requested or available, give them the question, sources, baseline, final text, and claim inventory without detector scores. Request a verdict on correctness, relevance, professional tone, and necessary qualifications, tied to the final file's SHA-256. Resolve factual objections even if an incorrect version has a lower score. If no separate reviewer is available, say so; a self-check is not independent review.

## Measure only when requested

Read [measurement instructions](references/measurement.md) before live scanning and [evidence limits](references/evidence.md) before interpreting results. Use the user's requested service, mode, and supported browser tools. This skill supplies no browser controls and does not authorize subscriptions, paid scans, public posting, or new account access.

For a comparison, select cases and candidates before seeing scores. Record fresh baseline and candidate scans using the same service, mode, and displayed model. Retain failures and unchanged results. Compare a fixed body with a relevant quotation separately from prose rewriting; track content and length changes. Distinguish first-pass trials from adaptive iterations.

Confirm the effective editor text, completed scan, fresh-result indicator, model, all classification confidences, timestamp, and warnings. Save exact inputs and private visible evidence. A stale displayed number is not a result for changed text. Never omit code or pad a short answer to satisfy a detector.

The optional checker in `scripts/validate_receipt.py` checks strict plain-text receipt consistency. Its [receipt format](references/receipt-format.md) rejects unrecorded editor changes; it does not support rendered-Markdown transformations or authenticate the service. A valid receipt can record 100% AI. Apply a numeric threshold only when the user explicitly requests one.

## Publish and report

Honor existing user authorization; do not invent authorization or ask again for an already authorized action. Refresh the discussion before posting and reassess if context changed. Match the final body to the reviewed version and, when required, its scan and requested threshold. Update the owned answer when editing, then independently read back its author, exact body, and URL. Do not post a duplicate or claim an answer was accepted without checking.

Report the actual quality findings, scores and warnings when measured, and edit or keep decisions. Missing required review or measurement leaves a candidate unpublished. A detector threshold applies only if requested. A successful local receipt check never authorizes publication.
