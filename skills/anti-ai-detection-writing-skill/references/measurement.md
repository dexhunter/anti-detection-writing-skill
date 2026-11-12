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

## Restore one fact at a time

Use this when the user has asked for a diagnostic scan of a short email that keeps every fact and scores as AI. A deletions-only control, plus variants that each add one fact back, locates a candidate trigger sentence. The deletions-only text is a measurement arm. The email you return still contains every fact, uncertainty, and qualification.

1. Freeze the fact-complete draft and the deletions-only control before looking at scores.
2. Each variant restores exactly one fact to the control, in one sentence or one signature line, and changes nothing else.
3. Scan the control and each variant once, on the same service, mode, and displayed model. Record the AI result and any flag the UI shows. Do not repeat a text to chase a different number.
4. Compare each variant with the control. A large jump marks that added sentence or line as the first candidate trigger. A smaller move stays in the record. The mark locates the sentence. It does not explain the model.
5. In the email you return, work that fact into a sentence that is already there. Do not leave it as a standalone "Please note..." sentence or a reminder sentence that only lists facts. Do not drop the fact. A real sender's name is one of those facts: never replace it with a different name to lower a score.

Check a bolted-on recap or date sentence, and the sign-off or signature block, before rewriting the rest of a flagged draft.

For a synthetic probe, do not use a stock LLM persona name such as Helen Cartwright. On the only email below, that name alone scored 100% AI and can confound every other change in the experiment.

**Preliminary.** The scans below are the November 12, 2026 batch in [evidence limits](evidence.md): one synthetic kettle complaint, free-plan GPTZero Model 5.0b, Advanced scans, one scan per text, no repeats. The first five texts run 118–139 words. Later rows do not have a separate word count. The tables are repeated here so the procedure and that run stay together.

| Variant | Added to the deletions-only control | AI | Flag recorded |
| --- | --- | ---: | --- |
| Control | None | 4% | None recorded |
| Date sentence, directly after the salutation | Please note the order date was 28 October 2026 and the delivery date was 31 October 2026. | 100% | Possible AI Paraphrasing |
| Bare name, after Yours sincerely | Helen Cartwright. | 100% | Possible AI Paraphrasing |
| Fault sentence | The handle came loose during ordinary use the first time the kettle was boiled. | 21% | None recorded |
| Refund sentence | Under the Act I have the right to a full refund to the original debit card, so £34.99, within 14 days. | 1% | None recorded |

On this email, the date sentence and the bare name are the two arms at 100%. The fault sentence (21%) and the refund sentence (1%) were also added as their own sentences, so an added sentence is not itself the observation. Earlier context, outside this Advanced batch: the raw base-model text passed as human; versions with all facts restored scored 100% AI; this deletions-only control also scored 4% on a Basic scan, so the scan level does not account for the 4%.

**Stage 7, same preliminary limits.** The first four rows each change only the 4% control. The last two restore dates, fault, and refund together, each with one name form. A paraphrasing flag is the Possible AI Paraphrasing label. A bare flag means a flag was reported and the UI string was not quoted again.

| Variant | Change | AI | Flag recorded |
| --- | --- | ---: | --- |
| Dates folded into the existing first sentence | on 31 October 2026, which I ordered on 28 October 2026 | 31% | None recorded |
| Dates folded into the existing order-number sentence | via your website on 28 October 2026, and it was delivered on 31 October 2026 | 17% | None recorded |
| Sign-off | Ms Helen Cartwright | 100% | Paraphrasing flag |
| First sentence, no sign-off name | My name is Helen Cartwright and ... | 100% | Flag |
| All facts: dates folded, fault and refund folded, sign-off name | Ms Helen Cartwright | 100% | Flag |
| All facts: dates folded, fault and refund folded, body name, no sign-off name | My name is Helen Cartwright and ... | 100% | Flag |

The date fold inside those two all-facts rows was not quoted separately from "dates folded."

**Stage 8.** All facts are present, the dates sit in the order-number sentence, and the fault and refund facts are folded in. Only the sign-off changes.

| Sign-off | AI | Flag recorded |
| --- | ---: | --- |
| No name | 52% | uncertain |
| Sue Hall | 13% | highly confident ... entirely human |
| Helen | 100% | Flag |
| Helen Cartwright | 100% | Flag |

**Observed in this test.** Folding the dates into an existing sentence did not reproduce the standalone date sentence's 100% result. Helen, as a first name or a full name in the sign-off, and as a full name in the first sentence, scored 100% AI. Sue Hall, on the fact-complete draft, scored 13% AI. First name alone in the body was not scanned. A displayed label is not a finding about authorship.

**Hypothesis, not a result.** GPTZero may treat stock LLM-style persona names as an AI signal. A formal-letter interaction is a separate hypothesis. The body-only full name also scored 100%, and Sue Hall in the sign-off scored 13%, so these rows do not isolate the sign-off or the letter genre. Do not send the control, and do not change a real sender's name to chase the Sue Hall result.

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
