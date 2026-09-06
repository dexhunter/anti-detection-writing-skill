# Unseen-question comparison

**GPTZero measurements are pending.** The six questions below were selected before scores and were absent from the previous 19-question primary dataset. “Unseen” refers to this local trial history, not model pretraining. They are offline writing cases; several threads already have useful or accepted answers.

Two fresh writer agents received the same newly authored draft, primary-source evidence, protected spans, and material-claim requirements. One used the frozen current skill; the other used the revised skill. The revision adds dependency ordering for actions and conditions, plus a final inventory reconciliation. Both arms use plain prose without added asker quotations.

| Case | Question being tested |
| --- | --- |
| [Pydantic #13585](https://github.com/pydantic/pydantic/discussions/13585) | How constraints and validators interact in the six supplied annotations |
| [pytest #14190](https://github.com/pytest-dev/pytest/discussions/14190) | Whether global log settings prevent DEBUG capture through the fixture |
| [HTTPX #3630](https://github.com/encode/httpx/discussions/3630) | Whether request hooks sign after connection-pool waiting |
| [HTTPX #3164](https://github.com/encode/httpx/discussions/3164) | Which connection stages and DNS operations the connect timeout covers |
| [FastAPI #7077](https://github.com/fastapi/fastapi/discussions/7077) | Which response object must receive the cookie before a redirect |
| [FastAPI #16297](https://github.com/fastapi/fastapi/discussions/16297) | When background work needs separate workers and recovery mechanisms |

The [plan](plan.json) identifies the frozen versions and protocol. The [results record](results.json) links 18 exact Markdown files: six common drafts and twelve edited answers. Its detector fields remain null until observed. The [current](skills/current.txt) and [revised](skills/revised.txt) files are text snapshots for comparison, not installable copies; install the main skill package.

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

This is a small convenience sample with one writer output per arm, one reviewer, and no repeated generation. It cannot establish a general writing-quality advantage or a detector success rate. Twelve Basic Scans are planned on the frozen final texts using a comparable displayed model. No extra quotations, repeated score-seeking edits, quota bypasses, or substitute heuristic “GPTZero” scores are part of the design.
