# Requested alternatives: four-case pilot

All eight planned GPTZero observations returned **100% AI / 0% mixed / 0% human**. The four original/alternative pairs are ties. This round found no detector-score reduction, including in the longer answers without short-text warnings.

The cases are newly authored, source-grounded documentation questions about Git, Docker, Kubernetes and PostgreSQL. They were absent from the earlier local datasets. They are offline examples, not actual unanswered discussion threads, and were not posted publicly as answers. The [results](results.json) retain the questions, scenario assumptions, official sources, all three confidences, exact inputs, hashes, warnings and review outcomes.

## Why the instruction changed

The [frozen current skill](skills/current.txt) produced four byte-identical keeps: the neutral originals were already clear. Its instruction to leave clear passages intact is useful for ordinary polishing. For this user's explicit request to test another formulation, a separately frozen [variant](skills/variant.txt) permitted a reader-appropriate alternative while retaining the original as a control and preserving the facts and practical meaning.

The alternative writer also received a specific framing prompt: organize around what happens in the supplied scenario and the action or consequence the reader needs, rather than beginning with a general definition where applicable. That prompt is part of the intervention. The results cannot isolate the effect of the changed instruction sentence.

All four alternatives were written once and frozen before any scores. No added quotations, padding, invented experience or post-score edits were used. Commands and citation URLs stayed exact. Substantive claims and qualifications were retained; source-only optional facts were distinguished from facts actually present in the original. The changed instruction is retained as support for an explicitly requested comparison, with no claim that it reduces detector scores.

## Complete results

Measurements used **GPTZero Basic Scan, Model 4.9b**, on **September 6, 2026, 17:45–17:50 UTC**. Each result displayed **Text up-to-date** and was checked against its unchanged editor text. Values below are AI / mixed / human confidences. Words are the service's displayed counts.

| Case | Original | Alternative | Words, original / alternative | Short-text warning | Slight quality preference |
| --- | --- | --- | ---: | --- | --- |
| [Git: stop tracking while keeping the local file](inputs/git-tracked-ignore/alternative.md) | 100 / 0 / 0 | 100 / 0 / 0 | 78 / 83 | Both | Original |
| [Docker: publish only on the host loopback address](inputs/docker-expose-local/alternative.md) | 100 / 0 / 0 | 100 / 0 / 0 | 85 / 90 | Both | Original |
| [Kubernetes: divide probe responsibilities](inputs/kubernetes-probe-roles/alternative.md) | 100 / 0 / 0 | 100 / 0 / 0 | 164 / 158 | Neither | Original |
| [PostgreSQL: snapshot scope and transaction retries](inputs/postgresql-snapshot-scope/alternative.md) | 100 / 0 / 0 | 100 / 0 / 0 | 180 / 167 | Neither | Alternative |

**0 lower, 4 tied, 0 higher; 0 alternatives below 100% AI.** All eight texts passed the separate quality review. The reviewer saw randomized X/Y pairs with source context, without arm labels or detector scores. They found every alternative acceptable as a quality equivalent, with no material loss of correctness, clarity or necessary qualifications. Their slight preferences favored three originals and one alternative. Quality equivalence does not mean that every alternative was preferred or improved readability.

Original/current outputs are byte-identical and share one observation per case. There are eight distinct measured inputs, not twelve independent scans. This deduplication was recorded before the first scan. Original-first versus alternative-first order was balanced across two cases each and fixed with seed `2026090602` before scoring.

## Evidence and limitations

Each case retains six input files: original and alternative Markdown, exact submitted text, and exact effective editor text. Literal Markdown was entered in a Code Block. These source texts have no final newline; the editor appended exactly three line-feed characters. No words, code or citations changed in that representation. The strict verbatim receipt checker was not used because it does not accept that wrapper difference. File hashes establish consistency, not service authenticity.

A separate LLM audit checked all eight source/review/submitted/effective hash relationships, saved UI fields, warning states, observed order and quota correspondence. It visually inspected a short and a long result screenshot. Two navigation delays were resolved without an additional Scan click; the saved observations and quota change agree with eight inputs. These are maintainer-observed UI records, not authenticated service exports or independent remeasurements. Raw screenshots, account details and browser document identifiers remain private.

The source inventories were fixed before each neutral first-pass original was written. The original author had already read the skill, so this is not a skill-naive or context-isolated baseline. The variant was proposed after observing the current writer's four keep decisions. Although the cases were fresh to local detector testing, this is an adaptive instruction-development pilot, not an untouched holdout. There is one writer output per condition, a small synthetic convenience sample, an additional framing prompt, and no ordinary-editing control. Reviews came from separate LLM agents, not human raters. Official documentation was inspected; runtime behavior was not reproduced.

An additional ordinary-email behavior exercise applied the variant without a measurement request. It made one local clarification and preserved the supplied logistics without creating alternatives or invoking a detector. This supports the narrow ordinary-behavior check; it is not a detector result or a general quality benchmark.

Keep these observations separate from the historical **19 questions / 44 scans** and the [six-question comparison](../unseen-transfer-1/README.md). This pilot supports permission to try an acceptable alternative when explicitly requested, but does not validate a score-reduction method or a general answer structure. The slight preference for the original in three cases also argues against making action-first ordering compulsory.
