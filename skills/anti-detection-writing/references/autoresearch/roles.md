# Research role packets

The coordinator passes only the relevant packet to each fresh agent. Record the real model/settings when available; otherwise record the shared inherited runtime and the missing detail. Keep baseline and candidate generation conditions the same. These are logical role boundaries in a shared workspace, not a filesystem sandbox or proof that an agent followed its packet.

## Skill improver

Read the frozen incumbent, development cases and complete development history, including failures and ties. Propose up to the configured number of distinct, small editing hypotheses. Each proposal contains a complete `SKILL.md`, a rationale, the affected case types and how it differs from a previously failed direction. Change only the `Write and review` section. Do not change evaluation, measurement, publication, spending, source-preservation or user-authorization requirements. Do not edit controller files, receipts or answers. Do not inspect holdout cases. Do not claim a score without a measurement. The first implementation may use one improver for several proposals; do not label those proposals independent model samples.

## Research preference selector

Read the task, frozen candidate diffs/hypotheses, development evidence and remaining budget. Rank all candidates by the value of spending the next evaluation on them. Compare pairs explicitly; save the reasons, uncertainty and any tie-break. Prefer a candidate that changes a relevant behavior while preserving the full answer contract. Do not predict fabricated absolute detector scores. Prioritize measured comparable history over appealing explanations. Do not inspect holdout cases. Return `ranker`, `ranked_ids` and `reason` in JSON. This ranking allocates an experiment; it does not prove that the chosen skill works.

The first controller supports inference-only ranking before output generation. Optional cheap generation pilots can inform a later selector design, but are not silently included in this version's treatment. A ranking model is not trained or calibrated by this setup.

## Output writers

Use the exact common [writer prompt](writer-prompt.md), one frozen skill arm and one source packet. Run baseline and candidate writers in separate fresh contexts with the same model and settings. They see neither each other's outputs nor current detector results. Save exact text and generation metadata. The incumbent output must actually come from applying the incumbent skill; the original draft is not a substitute. The coordinator may batch independent cases per arm, but must record that context choice consistently.

## Quality judge

Read the original, question, source evidence, required claims and two final answers under randomized labels A/B. Do not receive detector scores, skill identities, hypotheses, ranking reasons or the writers' self-assessments. Check correctness, relevance, clarity, tone, all decision-changing qualifications and protected spans. Reconstruct each answer's conclusion, next action and limiting condition. Return a pass/fail for each answer, preference A/B/tie, exact SHA-256 values and concrete reasons. The coordinator maps A/B to arms and imports the review without changing its verdict. The judge must be different from the improver and both output writers. This is separate LLM review, not human preference evidence.

## Detector worker

Receive one exact reviewed answer, its reserved attempt ID, detector mode, permitted entry transform and available allowance. Use the user's signed-in Chrome and requested Basic Scan for GPTZero. Read the current UI and quota before submitting. Submit the entire answer once; wait for completion, read back its effective text and save the actual native results, warnings and private screenshots. See [receipt contract](receipt-contract.md). No wording changes, credit purchases, limit bypasses, posting or result invention. Do not navigate away while processing. A missing, failed or uncertain result is a recorded outcome, never zero or 100 by assumption. A worker for another detector follows that detector's native units; it cannot satisfy a GPTZero-specific posting condition.

## Coordinator and audit

The coordinator alone mutates the ledger and performs supported browser actions. Serialize access to each signed-in browser/account, reserve before external work, use bounded tool calls, and reconcile service allowance. Capture actual model usage separately when exposed; otherwise label it unavailable. The controller's word/call reservations are conservative accounting, not vendor billing or dollar cost. A separate measurement auditor can inspect all retained records after quality review, checking exact text, current results, native metrics, costs and the public export. The improver cannot overwrite the judge or audit's decisions.
