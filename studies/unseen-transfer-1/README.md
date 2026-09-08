# Unseen-question comparison

**All 12 planned GPTZero measurements are complete:** every frozen answer scored **100% AI / 0% mixed / 0% human**, giving six tied pairs. This completes the earlier frozen comparison; it does not test later literature-informed skill changes. The six questions below were selected before scores and were absent from the previous 19-question primary dataset. “Unseen” refers to this local trial history, not model pretraining. They are offline writing cases; several threads already have useful or accepted answers.

Two fresh writer agents received the same newly authored draft, primary-source evidence, protected spans, and material-claim requirements. One used the frozen current skill; the other used the revised skill. The revision adds dependency ordering for actions and conditions, plus a final inventory reconciliation. Both arms use plain prose without added asker quotations.

| Case | Question being tested |
| --- | --- |
| [Pydantic #13585](https://github.com/pydantic/pydantic/discussions/13585) | How constraints and validators interact in the six supplied annotations |
| [pytest #14190](https://github.com/pytest-dev/pytest/discussions/14190) | Whether global log settings prevent DEBUG capture through the fixture |
| [HTTPX #3630](https://github.com/encode/httpx/discussions/3630) | Whether request hooks sign after connection-pool waiting |
| [HTTPX #3164](https://github.com/encode/httpx/discussions/3164) | Which connection stages and DNS operations the connect timeout covers |
| [FastAPI #7077](https://github.com/fastapi/fastapi/discussions/7077) | Which response object must receive the cookie before a redirect |
| [FastAPI #16297](https://github.com/fastapi/fastapi/discussions/16297) | When background work needs separate workers and recovery mechanisms |

The [plan](plan.json) identifies the frozen versions and protocol; its pending measurement status is retained as historical preparation metadata. The [results record](results.json) gives the completed measurement status and links 18 unchanged Markdown files plus 24 exact submitted/effective-editor text files. The arm keys `current` and `revised` identify the frozen original and revised snapshots, not later package versions. The [current](skills/current.txt) and [revised](skills/revised.txt) files are text snapshots for comparison, not installable copies; install the main skill package.

Primary-source inspection preceded writing. A local Pydantic 2.13.4 / pydantic-core 2.46.4 reproduction matched the six reported outcomes, and five pytest 9.0.2 checks established the distinction between fixture capture and report handlers. HTTPX and FastAPI advice was source-inspected; the reported network failures, browser behavior, and ECS deployment were not reproduced.

All twelve first-pass answers retained the protected code, inline-code occurrences, and URL targets exactly. A separate LLM evaluator reviewed randomized X/Y pairs without the arm mapping or detector scores. **All twelve passed technical review**, with no material unrecorded cuts, unsupported additions, or required corrections. The revised skill was preferred in two cases, the current skill in one, and three were equivalent.

| Case | Blind clarity/actionability preference |
| --- | --- |
| Pydantic #13585 | Revised: clearer reproduction limits |
| pytest #14190 | Equivalent |
| HTTPX #3630 | Revised: clearer retry prerequisites and timeout scope |
| HTTPX #3164 | Equivalent |
| FastAPI #7077 | Equivalent |
| FastAPI #16297 | Current: answers the architectural choice sooner |

These are judgments from one separate LLM reviewer, not human ratings. The [per-case reviews](results.json) include hashes and reasons. One optional wording clarification was logged for the current HTTPX #3630 answer; it was non-blocking, and no first-pass text was changed after review. The original skill's win matters: ordering an entire explanation by its mechanism can delay the recommendation the reader requested. The result does not justify applying one paragraph shape everywhere.

The revised HTTPX signing answer records a source-supported correction: a pool timeout bounds each acquisition wait, not necessarily all waiting across internal reacquisition. The revised Pydantic answer also retains the evidence packet's operating-system/Python reproduction limit. Those changes are disclosed rather than calling the experiment an isolated test of surface style.

This is a small convenience sample with one writer output per arm, one reviewer, and no repeated generation. It cannot establish a general writing-quality advantage or a reliable detector success rate. The measurements below used the already-frozen final texts; no quotations or score-seeking edits were added.

## Completed detector comparison

The 12 planned observations used **GPTZero Basic Scan, Model 4.9b**, on **September 6, 2026, 16:26–16:38 UTC**. Each completed result displayed **Text up-to-date**, the captured editor text remained unchanged after scanning, and no short-text warning appeared. Scores below are **AI / mixed / human percentages**; word counts are the service's displayed counts.

| Case | Frozen original | Frozen revised | Displayed words, original / revised |
| --- | --- | --- | --- |
| [Pydantic #13585](https://github.com/pydantic/pydantic/discussions/13585) | 100 / 0 / 0 | 100 / 0 / 0 | 144 / 145 |
| [pytest #14190](https://github.com/pytest-dev/pytest/discussions/14190) | 100 / 0 / 0 | 100 / 0 / 0 | 140 / 135 |
| [HTTPX #3630](https://github.com/encode/httpx/discussions/3630) | 100 / 0 / 0 | 100 / 0 / 0 | 143 / 149 |
| [HTTPX #3164](https://github.com/encode/httpx/discussions/3164) | 100 / 0 / 0 | 100 / 0 / 0 | 144 / 146 |
| [FastAPI #7077](https://github.com/fastapi/fastapi/discussions/7077) | 100 / 0 / 0 | 100 / 0 / 0 | 133 / 126 |
| [FastAPI #16297](https://github.com/fastapi/fastapi/discussions/16297) | 100 / 0 / 0 | 100 / 0 / 0 | 150 / 149 |

There were **0 revised-lower, 6 tied, and 0 revised-higher** AI-confidence pairs. This is a comparison between two edited arms; the common drafts were not scanned. Keep these results separate from the original **19 questions / 44 scans**, including **0/15** plain-rewrite reductions and **5/10** quotation reductions. The separate blind quality preference remains revised 2, original 1, equivalent 3.

The submitted text preserves each frozen Markdown file except for removal of its single final LF character. The literal editor then added three trailing LF characters. The [results record](results.json) retains the original source/review hashes and separate submitted/effective file hashes. All source, submitted, and effective bytes were checked, along with the saved visible mode, model, freshness, confidences, and warning state. These are maintainer-recorded UI observations, not authenticated service exports or independent remeasurements. The strict receipt checker was not used; its verbatim newline-equality requirement does not match this capture representation.

One additional completed scan of the frozen original Pydantic answer occurred at **16:28 UTC**, before its paired revised-arm observation. It also showed **100% AI / 0% mixed / 0% human**. A read-only reopening of that repeat document at **16:43 UTC** recovered exact editor bytes matching the first observation; this later verification did not run another scan. The supplemental entry references the same public effective-input file and hash. Its sanitized supplemental record is retained in [results.json](results.json), outside the 12 planned observations; it does not replace the first result or add a seventh pair. Arm order was prerecorded before the first scan using a seeded assignment balanced across three original-first and three revised-first cases. The observed order matches that assignment. The seed, method, public case/arm order, and preparation-record hash are retained in [results.json](results.json); private source paths are excluded.

Completing this older comparison does not validate subsequent literature-informed instructions. It shows that these two frozen outputs for each of six selected questions received the same AI confidence despite differences in some quality judgments.
