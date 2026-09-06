# When the skill may not help

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

Keep warnings with the result. Do not pad a concise answer or remove necessary code to change the detector's input length.

## A lower score can accompany incorrect advice

An exploratory ADK #1742 revision scored 43% AI but failed technical review because it overpromised duplicate-email prevention. Sending can succeed before the sent record is saved. The corrected revision passed at 60% AI, 40% mixed, 0% human and was published. The incorrect version is a rejected attempt, regardless of its lower score.

Correct the facts first, then scan the corrected text if measurement is required. This adaptive sequence is outside the primary comparison counts; see [methodology](methodology.md#exploratory-work-outside-the-primary-counts).

## A low score without a baseline does not show improvement

Four later answers in `mattpocock/skills` scored 100%, 93%, 100%, and 11% AI. None had a baseline or an unquoted control. The 93% and 11% answers met that user's publication threshold, but cannot demonstrate a reduction. They remain in the complete dataset and are not showcase examples.

The [six-question unseen comparison](../studies/unseen-transfer-1/README.md) has twelve quality-reviewed candidates but no completed detector scans. Its review preferred the revised skill twice, the original once, and judged three equivalent. That is a small LLM quality comparison, not a detector result. Emails, articles, and other broader writing formats also have no detector benchmark here. Use the skill for editing them, but measure before making a score claim.

## Complete primary comparison totals

| Cohort | Questions | Plain-rewrite reductions | Fixed-body quotation reductions | Scans |
| --- | ---: | ---: | ---: | ---: |
| Initial plain pilot | 5 | 0/5 | — | 10 |
| First quotation transfer | 5 | 0/5 | 2/5 | 15 |
| Second quotation transfer | 5 | 0/5 | 3/5 | 15 |
| New answers, no baseline | 4 | Not measured | Not measured | 4 |

Further unsuccessful structural rewrites and formatting controls, and the separate quotation pilot, remain documented in [methodology](methodology.md#exploratory-work-outside-the-primary-counts). No study inputs or measurements were removed to produce the showcase. The current packaged skill consolidates evolving development versions; these results do not establish its future performance.
