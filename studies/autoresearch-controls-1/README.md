# Control-boundary instruction experiment

On September 7, 2026, the selected new instruction **did not improve detector performance**. The current skill produced one Python answer at 91% GPTZero AI confidence; the proposed rule produced 100% for that case. A separate follow-up scan found the original Python text at 100%, establishing a modest, exploratory **100% → 91% source-to-edit decrease using the existing skill**.

## Frozen skill comparison

| Development case | Current skill: AI / mixed / human | Proposed rule: AI / mixed / human | Separate quality preference |
| --- | --- | --- | --- |
| GitHub Actions concurrency | 100 / 0 / 0% | 100 / 0 / 0% | Tie; both pass |
| Python TaskGroup | 91 / 9 / 0% | 100 / 0 / 0% | Tie; both pass |

The selected rule asks the writer to explain the distinct effects of related controls and their interaction. One improver proposed three changes, and a separate inference-only selector ranked them before generating the candidate answers. Only one procedure/explanation bullet changed; the rest of the skill remained frozen. Two writers used fresh contexts, the same inherited model/settings, the same source packets and [common operator](writer-prompt.txt). The exact runtime model identifier was unavailable and was not guessed.

“Current skill” refers to the archived installed snapshot used in this experiment. Its exact entrypoint and full-tree digest are retained below; the published repository version may differ.

Both cases were reused synthetic development fixtures. An independent, score-blind LLM judge reviewed randomized A/B files, verified all 17 required claims and protected spans, and judged both pairs equivalent in quality. No wording changed after review. All four observations used completed **GPTZero Basic Scan, Model 4.9b**, in signed-in Chrome, with no short-text warnings. [Exact observations](results.json) and [review findings](quality-review.json) are retained.

The mean AI-confidence reduction was **−4.5 percentage points**: one tie and one 9-point regression. The controller correctly rejected the candidate. The two prepared confirmation cases were not disclosed to the improver or writers and were neither generated nor scanned. The candidate rule was not installed or promoted.

## Exploratory source-to-edit reduction

After seeing the current skill's Python edit score 91%, the coordinator froze a separate one-scan diagnostic: scan its unchanged original under the same service, mode and displayed model. This comparison was selected after the edit's score was known; it is **not an unseen validation case or a preselected success-rate estimate**. The original scan occurred after the edit scan.

| Python text | AI confidence | Mixed confidence | Human confidence | Words |
| --- | ---: | ---: | ---: | ---: |
| [Original](inputs/python-original.txt) | 100% | 0% | 0% | 134 |
| [Existing-skill edit](inputs/python-baseline.txt) | 91% | 9% | 0% | 129 |

Before the diagnostic scan, a separate score-blind review explicitly passed both texts, verified all nine claims and protected spans, and preferred the edit. The edit puts the Python prerequisite first, places the child-cancellation exception beside its triggering condition, and makes waiting before error reporting explicit. The cleanup paragraph is unchanged. These are useful editorial differences; the experiment does not establish which change caused the score difference.

The observed decrease is **9 percentage points**, with **0% human confidence**. It supports this exact source/edit observation, not a general reliability claim or improvement from the rejected candidate. Each text was scanned once; detector repeatability and human readability were not measured. The 91% edit observation is reused in this diagnostic and the main table, not counted as another scan.

## Records and cost

The complete batch contains **five distinct scans and 659 charged words**: four preselected observations using 525 words, followed by the adaptive 134-word source check. No credits were purchased. The closed research round remains unchanged; the separate diagnostic is recorded separately. The 500-word headroom stayed unspent, but five combined calls leave three of the overall eight-call ceiling, not the original four-call confirmation capacity.

Source Markdown, literal submissions and effective editor text are included. Entry removed at most one terminal source newline; the Code Block editor added exactly three newline characters. Before/after editor bytes, current Basic results, all three confidences, displayed model, timestamps and warnings were checked against private snapshots and screenshots. The first click timed out in Chrome; its completed result and quota deduction were reconciled without resubmitting. No uncertain result was replaced with an invented score.

The [protocol](protocol.json), [source contracts](sources.json), [incumbent entrypoint](frozen-skills/incumbent.txt) and [selected candidate entrypoint](frozen-skills/selected-candidate.txt) retain the experiment context. Entrypoints are archived as text so they do not register as additional installable skills. Raw account evidence remains private. These are maintainer-recorded UI observations; hashes verify artifact consistency, not service authenticity. No Pangram scan ran in this batch.

A [later same-input diagnostic](../repeatability-1/README.md) repeated the Python edit at 91 / 9 / 0% and the rejected candidate at 100 / 0 / 0%. Those two additional observations are recorded separately and do not change this five-scan batch, its adaptive original comparison, or its rejected-candidate decision.
