# Optional detector measurement

Use the service and browser requested by the user through supported browser controls. Do not substitute a different session for an explicit browser request. Let the user complete sign-in if needed. Preserve the user's scan mode and spending constraints. Before an open-ended experiment, record the editing hypothesis, selected cases and candidates, and a finite comparison batch within the user's existing scope and budget. Choose its size for the task; honor any count already specified without imposing a universal attempt count or another approval step.

1. Save the baseline, source evidence, claim inventory, and candidate. Select multiple cases before seeing scores and record selection reasons. Keep the original and candidate names unambiguous.
2. Review technical correctness before interpreting detector results. A score cannot resolve a factual objection. Keep the separate reviewer unaware of scores when assessing quality.
3. Freeze the measurement scope before scanning. By default, use `prose_only`: keep the full reviewed message separately, identify independent code blocks and standalone command lines, and save the exact remaining prose as the detector input. Preserve every explanatory sentence, qualification and inline identifier. For an explicit `full_text` request, use the entire message. Paste the complete declared input, read it back and compare with its file. Preserve original Markdown, submitted representation and editor text separately if they differ.
4. Do not accept broad normalization that can hide changed words or code. An observed editor once merged adjacent `api` and `ui` spans into `apiui`; that input was invalid. If rendering changes content, repair entry and repeat verification before scanning. Keep invalid attempts in an audit log.
5. Run the selected scan. A newly created document URL is not evidence of completion. Let processing finish before navigating to another result view, then confirm the requested mode, model and visibly current result. On GPTZero, `Text changed` or `Scan to update` means the displayed score may belong to an earlier input; wait for a completed `Text up-to-date` result.
6. Record the detector's native labels and metrics; for GPTZero, retain AI, mixed, and human confidences separately. Include the timestamp, displayed length, any short-text warning, and exact input hashes. Save a private visible-result snapshot. If the UI or model differs between paired scans, report the mismatch rather than treating it as comparable evidence.
7. Any change to the declared detector input requires a new scan. Under `prose_only`, a change confined to excluded code requires renewed full-message correctness review and a new full-message/prose association; it does not change an existing receipt for identical prose bytes. Under `full_text`, code changes also require a new scan. Apply the user's threshold to the declared input and report the scope. Never call a lower AI confidence proof of human authorship.

For prose-only measurements, retain the full-message hash, prose hash and exact excluded code ranges with the independent review. Do not infer exclusions by deleting everything in backticks: technical names and inline commands can be necessary parts of a sentence. The reviewer checks that each exclusion is independent code, all explanatory text remains, and the complete answer is correct. Code correctness is a separate result, not a detector confidence. Too-short prose remains a warning or unavailable scan; do not pad it with code or filler.

Use the same declared scope and extraction rule on both sides of a comparison. A change from whole-message to prose-only measurement needs a fresh comparable baseline; it is not a demonstrated rewriting improvement. Preserve historical receipts and their original scope. The receipt's `answer` artifact is the exact declared detector input, with the separately reviewed full-message association retained alongside it; its content cannot be silently replaced.

The supplied strict receipt checker accepts only verbatim plain-text entry, apart from CRLF/LF line endings. Prefer an editor mode that preserves literal source text. If Markdown renders differently, the checker rejects the mismatch: do not rewrite a receipt to hide it. Either use a verified entry method preserving the intended source or explicitly report that this checker cannot validate that representation. Historical studies used separately recorded formatting checks and are not in the new strict receipt format.

For a quotation comparison, write and review the plain answer first, choose one short useful excerpt before scores, then hold the body fixed. Record the added words and retain unchanged outcomes. Prose edits and quotations are different interventions. Do not rotate excerpts or add unrelated material to lower a score.

## Pangram comparisons

Confirm the model on each completed result. Our September 6 web results displayed **Pangram 4.0**; a marketing page or an API default is insufficient evidence of the version used. Record the document label, displayed proportions of AI-generated, AI-assisted and human text, and any separately shown confidence labels. These proportions are not GPTZero document confidences. An AI-assisted classification still detects AI involvement; it does not mean human-written. Leave undisplayed fields unavailable rather than inventing observed zeroes.

Preserve short-text warnings and each service's word count. Save the quoted scan cost separately from the actual allowance change: our web UI sometimes estimated three credits but deducted two. In that run, result rendering removed blank lines and line-edge indentation. The textarea had matched the frozen input exactly; retain both representations and audit the precise differences and protected code. Do not infer internal model preprocessing from the display. Keep cross-detector observations separate from new-skill or unseen-case validation, and retain any existing service-specific publication requirement.

## Plateau and transfer

### Keep diagnostic comparisons small

For one specific failed answer, a single-case comparison can answer whether a proposed edit helps that text. Label it as an exposed development diagnostic, not unseen validation or evidence about the whole skill. Start with one final draft per distinct editing hypothesis and a separate quality review. Add model or editor stages only when the hypothesis needs them; record reused contexts and cached intermediates rather than describing them as fresh generation.

Check applicability and quality before spending scan allowance. Keep no-ops and rejected drafts in the record without scanning them. Reserve the complete comparison using the service's displayed word counts; a new document, an estimated quote and an actual deduction are different events. Reusing one freshly measured control across a small exploratory batch reduces calls, but does not create independent paired trials. Use fresh paired generation and untouched cases when the intended claim requires confirmation. The strict autoresearch controller's own generation and reservation requirements still apply to runs using that controller.

Do not rank candidates for GPTZero using a cheap local detector until useful ranking agreement has been demonstrated on comparable development pairs. The current local proxy disagreed with commercial classifications, so its low scores are not a validated shortcut. Preserve the target service's exact-text check when the user requires it for posting.

If a completed batch produces no quality-passing reduction, record that outcome before starting another. Further detector-directed revisions need a distinct, written hypothesis explaining what changes and what the comparison can establish. Restating the same editing prompt or chasing highlighted words is not a distinct hypothesis. If no justified next hypothesis remains, stop detector-directed iteration and report the plateau; retain useful edits subject to the user's publication conditions.

Before claiming that an approach works beyond its development cases, freeze the skill version and editing procedure and evaluate preselected fresh cases in the relevant writing format. Keep adaptive retries separate from transfer results and scope the claim to the tested service, mode, displayed model, cases, and intervention. A literature-derived instruction is an untested variant until its own results are measured; do not relabel an ongoing comparison as a test of it.

When an isolated decrease drives the next experiment, a bounded repeat of the exact fixed inputs can check an unresolved measurement assumption before another rewrite. Freeze the repeated inputs, order and complete pair budget before scanning, and retain earlier and new observations separately. Matching scores do not distinguish deterministic scoring from caching, establish a success rate, or validate a new skill. Repeating an edit without its original does not repeat the original-to-edit comparison.

## Retesting a skill revision

Use this workflow when the user asks to improve the skill through repeated tests; ordinary polishing does not require a comparative experiment.

1. Identify the previous failure: an incorrect claim, missing content, weak readability, a detector tie, or incomplete measurement. Check whether the changed instruction applies to the case. A voice-matching update cannot be evaluated without a suitable supplied sample.
2. Freeze the original, complete skill files, source context and one explicit workflow variation before scores. Reusing failed cases is a development retest, not unseen validation. Record writer context as part of the intervention.
3. If testing a writer that sees only a fact inventory, have the preparer reconcile that inventory against the original first. Account for useful explanations as well as commands, and record intentional cuts. Give the independent reviewer the original; hiding it from the writer must not hide omissions from the review.
4. Retain first-pass failures. Repair factual defects within the recorded batch limit, then review the exact replacement before scanning. Attribute a missing input fact to preparation rather than claiming the writer invented a mistake. Keep post-score exploration separate.
5. Compare original, current edit and workflow variation under the same measurement conditions. Record correctness, reader preference, content/length changes and detector outcomes separately. A passing rewrite can still be less readable than the original; a detector tie is not evidence that the edit had no editorial value.

Promote only the supported lesson. An inventory-check correction can improve factual coverage without a detector benefit. A development-case reduction needs fresh-case confirmation before a transfer claim; an inactive instruction or an unchanged batch does not justify a new score-reduction claim.

## Sharing evidence

Before sharing study artifacts, export only an allowlist of public fields. Remove session/document URLs, account details, credentials, quota UI, local paths, and unnecessary copies of other people's questions. Attribute necessary short excerpts. State whether the scores are observed UI records or authenticated service exports; do not imply one is the other.
