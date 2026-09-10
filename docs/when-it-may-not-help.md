# When the skill may not help

The [GEPA pilot](../studies/gepa-pilot-1/README.md) tested two prompt revisions on the reused HTTP explanation. Separate reviewers passed their facts and clarity but slightly preferred the incumbent, so the optimizer retained it. A declared follow-up diagnostic measured both revisions anyway: the shared baseline and both candidates stayed at 100% AI / 0% mixed / 0% human in Basic 4.9b. Changing the optimizer did not produce a reduction in this small trial; its three scans consumed 377 word credits, and neither writing policy was adopted.

The skill aims to improve readability and reduce detector scores. Those outcomes can differ. This page records cases that do not qualify for the [score-reduction showcase](case-studies.md), with practical guidance for deciding what to do next. Historical measurements used GPTZero Basic Scan, Model 4.9b; all primary results remain in the [dataset](../studies/results.json).

## Clearer prose can receive the same score

All 15 baseline-to-plain-rewrite comparisons stayed at 100% AI confidence. Separate LLM reviewers rated eight revisions improved and seven equivalent, with all passing technical review. These results support some readability improvements, but no detector benefit from plain rewriting in this sample.

If an edit improves clarity but the score stays unchanged, report both outcomes. Keep useful wording when the user's publication conditions allow it; do not present it as a detector success. Another experiment needs a specific new editing hypothesis, a bounded attempt count, and a fresh comparison that retains every attempt.

## Relevant quotations do not reliably reduce scores

Five of ten fixed-body quotation comparisons stayed at 100% AI:

| Case | Plain AI | With quotation AI |
| --- | ---: | ---: |
| [Poetry #9928](https://github.com/python-poetry/poetry/discussions/9928) | 100% | 100% |
| [Qwen Code #1298](https://github.com/QwenLM/qwen-code/discussions/1298) | 100% | 100% |
| [Datasets #7131](https://github.com/huggingface/datasets/discussions/7131) | 100% | 100% |
| [Poetry #10430](https://github.com/python-poetry/poetry/discussions/10430) | 100% | 100% |
| [Google ADK #1956](https://github.com/google/adk-python/discussions/1956) | 100% | 100% |

Include a quotation only when it identifies a concern the reply answers. Do not add one to an unrelated email or article to imitate the showcase, or rotate excerpts until a score changes. The observed comparisons changed both content and length and do not establish why GPTZero responded differently.

## Very short technical replies may yield uninformative measurements

In ADK #1956, the rewrite removed an unverified screenshot description and preserved uncertainty about historical deprecation. The [baseline](../studies/inputs/quote-transfer-2/adk-1956/baseline.txt), [plain revision](../studies/inputs/quote-transfer-2/adk-1956/plain.txt), and [quotation variant](../studies/inputs/quote-transfer-2/adk-1956/quoted.txt) still scored 100%. Their displayed lengths were 82, 78, and 84 words; all carried the under-100-word warning. Qwen #1251 also carried that warning at 90 and 99 words.

Keep warnings with the result. Do not pad concise prose to meet a detector minimum. Under prose-only measurement, keep code in the separately reviewed full message and retain every explanatory sentence and inline identifier in the scan.

## A lower score can accompany incorrect advice

An exploratory ADK #1742 revision scored 43% AI but failed technical review because it overpromised duplicate-email prevention. Sending can succeed before the sent record is saved. The corrected revision passed at 60% AI, 40% mixed, 0% human and was published. The incorrect version is a rejected attempt, regardless of its lower score.

Correct the facts first, then scan the corrected text if measurement is required. This adaptive sequence is outside the primary comparison counts; see [methodology](methodology.md#exploratory-work-outside-the-primary-counts).

## A low score without a baseline does not show improvement

Four later answers in `mattpocock/skills` scored 100%, 93%, 100%, and 11% AI. None had a baseline or an unquoted control. The 93% and 11% answers met that user's publication threshold, but cannot demonstrate a reduction. They remain in the complete dataset and are not showcase examples.

The [six-question unseen comparison](../studies/unseen-transfer-1/README.md) has twelve quality-reviewed candidates and twelve completed GPTZero Basic Scan / Model 4.9b observations, all 100% AI / 0% mixed / 0% human: six tied pairs. Its separate LLM review preferred the frozen revised skill twice, the frozen original once, and judged three equivalent. This completes the older fixed comparison; it does not validate later literature-informed instructions. One extra unchanged scan is retained separately from the planned pairs. Later small studies include business writing and a [synthetic article comparison](../studies/reader-dialogue-1/README.md), but do not provide representative validation across broader writing formats. Measure the relevant format before making a score claim.

## A published paraphraser can change the advice

The [local HIP feasibility pilot](../studies/hip-feasibility-1/README.md) used a released 0.6B model adapter on two existing long technical answers. Both outputs failed independent factual review before any GPTZero scan: one blurred the distinct Kubernetes health conditions, and the other reversed PostgreSQL snapshot timing and added invalid syntax. Commands and URLs surviving a rewrite did not establish that the surrounding explanation remained correct. These are two unmeasured quality failures, not detector successes or failures. The model was not adopted by the skill.

## Changing the drafting workflow can still leave scores unchanged

The [updated-skill retest](../studies/workflow-retest-1/README.md) compared four fresh original controls with direct edits and answers rebuilt without seeing the old prose. All 12 Basic 4.9b scans scored 100% AI: neither workflow reduced confidence in any of its four comparisons. One missing Git explanation was repaired before scanning, leaving all eight final alternatives technically acceptable. The reviewer preferred two originals and two direct edits. This supports checking the completeness of fact inventories, but supplies no evidence that reconstruction from facts reduces detection.

A subsequent [Pangram 4 comparison](../studies/pangram-transfer-1/README.md) scanned three saved pairs. The PostgreSQL rewrite changed from entirely AI-generated to entirely AI-assisted; Kubernetes stayed entirely AI-generated. A Qwen quotation pair that had reduced GPTZero AI confidence from 100% to 1% stayed entirely AI-generated on Pangram. None of the six outputs was classified as human-written, and three had short-text warnings. Pangram's displayed text proportions are not GPTZero document confidences. This is a selected cross-detector check, not a new-skill or unseen-case validation.

The later [targeted-edit comparison](../studies/targeted-edit-1/README.md) used two new synthetic answers with deliberately introduced clarity problems. Diagnosing those problems and editing the affected passages earned a modest preference from a separate score-blind LLM reviewer. Both pairs nevertheless stayed at 100% AI on GPTZero and entirely AI-generated on Pangram. All four Pangram scans had short-text warnings. No production rewriting instruction was changed from this result; targeted edits remain useful for clarity without demonstrated detector benefit here.

In the [reader-reconstruction trial](../studies/reader-reconstruction-1/README.md), a separate model answered frozen comprehension questions about an HTTP caching reply and a complete skill tutorial. Adjudication found no prose defect warranting a repair. The technical outputs were identical and unscanned; two independently composed article drafts both scored 100% AI / 0% mixed / 0% human in Basic 4.9b. Independent quality review passed both pairs and judged them equivalent. The trial used two scans and 1,078 word credits, with no confirmation or writing-policy promotion. Because neither repair stage edited anything, the article comparison measures variation between incumbent drafts and cannot establish a reader-repair benefit.

The later [register and draft-selection study](../studies/register-and-selection-1/README.md) rejected two methods before scanning: selecting between two drafts lost a current limitation, and reference-guided rewriting produced a less readable article. An additional diagnostic repaired the crowded paragraph and changed its scan gate before new review or measurement. Both complete pairs then passed suitability checks but remained 100% AI / 0% mixed / 0% human in all four Basic 4.9b scans. The reviewer preferred the technical candidate and the article control. The skill's new temporal-scope and paragraph-density checks address those quality findings; they have no demonstrated detector benefit.

## Complete primary comparison totals

The [model-assisted search](../studies/model-assisted-1/README.md) found a repeated 100% to 0% GPTZero reduction on one reused business case, while its technical case stayed at 100%. Both confirmation drafts lost the readability comparison and were not scanned; the workflow was not promoted. A subsequent [technical-format diagnostic](../studies/technical-format-1/README.md) tested a reference card and mini-FAQ against a fresh baseline scan. All three texts passed separate quality review and scored 100% AI / 0% mixed / 0% human. That bounded comparison used three scans and 394 word credits. Neither study establishes a reliable technical score-reduction method or that such a reduction is impossible.

A later [requested-alternative pilot](../studies/requested-alternatives-1/README.md) tested four new documentation questions after the current skill kept all four clear originals unchanged. A separate variant permitted a requested alternative, with a scenario/action/consequence framing prompt. All eight original/alternative scans scored 100% AI / 0% mixed / 0% human: four tied pairs. Short warnings affected both short pairs; the two longer pairs had none. A masked reviewer accepted every alternative as a quality equivalent, while slightly preferring three originals and one alternative. This instruction change enables a requested comparison; it has no demonstrated score benefit. The pilot has its own eight-observation record and does not change the historical counts below.

| Cohort | Questions | Plain-rewrite reductions | Fixed-body quotation reductions | Scans |
| --- | ---: | ---: | ---: | ---: |
| Initial plain pilot | 5 | 0/5 | — | 10 |
| First quotation transfer | 5 | 0/5 | 2/5 | 15 |
| Second quotation transfer | 5 | 0/5 | 3/5 | 15 |
| New answers, no baseline | 4 | Not measured | Not measured | 4 |

Further unsuccessful structural rewrites and formatting controls, and the separate quotation pilot, remain documented in [methodology](methodology.md#exploratory-work-outside-the-primary-counts). No study inputs or measurements were removed to produce the showcase. The current packaged skill consolidates evolving development versions; these results do not establish its future performance.

The [full-article model transfer](../studies/article-model-transfer-1/README.md) also failed to produce an eligible measured revision. Two local generations failed; a separately declared recovery produced a factually correct article that the independent reviewer found less readable than the control. That candidate was left unscanned. A readable partial output, successful evidence saving, or repaired claim inventory does not establish that the complete writing method succeeded.

In the [sequential-section experiment](../studies/windowed-article-1/README.md), both articles passed factual and suitability review, but the control was slightly preferred. The new article remained unscanned. One section writer had not received a study-date detail from the supporting notes, so the comparison partly reflects a preparation difference. More writing calls cannot compensate for evidence missing from their inputs.

The [paired-editing-example trial](../studies/paired-editing-examples-1/README.md) measured prose separately from code. Three fixed synthetic revision examples produced two quality-passing candidates that a masked LLM reviewer slightly preferred. Both the HTTP and full-article prose pairs nevertheless stayed at 100% AI / 0% mixed / 0% human in all four Basic 4.9b scans. Only the article's installation command was excluded; its title, explanations and caption remained. This is a new scoped comparison, not evidence that code removal or the demonstration method lowers confidence. No writing rule was promoted.

The [exact-crossover trial](../studies/exact-crossover-1/README.md) combined unchanged passages from two complete drafts after independent review of their boundaries. A separate reviewer slightly preferred the selected combination, but its fresh prose score and the selected parent's score both remained 100% AI / 0% mixed / 0% human in Basic 4.9b. The two scans used 227 free word credits. No confirmation case was opened and no writing rule was promoted.
