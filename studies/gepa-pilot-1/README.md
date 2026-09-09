# GEPA pilot: two rejected policies, no detector reduction

September 9, 2026. **The baseline and both revised outputs scored 100% AI / 0% mixed / 0% human in GPTZero Basic Scan, Model 4.9b.** The optimizer retained the incumbent. Neither writing policy was adopted, and two preselected confirmation cases remained sealed.

| Output on the reused HTTP case | Prose words | Separate quality review | GPTZero AI confidence |
| --- | ---: | --- | ---: |
| Incumbent | 122 | Pass | 100% |
| Proposal 1: regroup claims into sentences | 124 | Facts and clarity pass; incumbent slightly preferred | 100% |
| Proposal 2: organize the explanation around the requested outcome | 131 | Facts and clarity pass; incumbent slightly preferred | 100% |

All three observations are prose-only, with no short-text warnings. No standalone code occurs in these answers; header names and values remain in the measured explanation. The [results](results.json) retain all three confidences, timestamps, exact inputs, independent reviews and private evidence hashes. The three scans consumed **377 free word credits**, matching the observed allowance decrease from 1,160 to 783. No credits or subscription were purchased.

## What GEPA controlled

The pilot ran the actual [upstream GEPA optimizer at commit 0632cdb](https://github.com/gepa-ai/gepa/tree/0632cdb5dcc052e690eab439e1b4a7e3e9cfe407). Its custom adapter supplied reviewed outputs, utility values and development traces. A custom proposer called a separate reflection agent; fresh agents wrote each retained output and independently reviewed the exact answers. Chrome operations and receipt validation were performed by the coordinator. The default GEPA reflection model was not used.

The [GEPA paper](https://arxiv.org/abs/2507.19457) motivates reflection on execution feedback and prompt search. It supplies no GPTZero writing benchmark. This small adaptation used one reused HTTP case for both training and validation, a two-proposal limit, Pareto candidate selection, strict improvement acceptance and no merging. With one case, it does not test a meaningful multi-case Pareto tradeoff or generalization.

Only the incumbent skill's Write and review section could change. The [frozen writer packet](method/writer-skill.txt), [incumbent policy](method/incumbent-policy.txt), both proposed policies and their reflections are archived. The incumbent release was `357f15b262b75b58c7197872f45571e9431d67b3`. Neither proposal contains a target answer or a detector-driven vocabulary ban. Both overlap with earlier reader-focused editing methods; they are specific variants, not claims of entirely new techniques.

## Strict search and additional measurement were separate

The frozen [GEPA protocol](method/protocol.json) required factual correctness and no readability preference loss. Its utility was one minus AI confidence divided by 100 for an eligible output, or −1 for a quality rejection without a scan. The seed scored 100% AI, giving utility 0. Reviewers slightly preferred the incumbent in both anonymous pairs, although every required claim and all protected strings passed. GEPA therefore assigned each candidate −1 and rejected both. Those negative utilities are not detector scores.

Proposal 2 received the seed trace and the first candidate's quality rejection as development feedback. The two parent reevaluations reused the exact seed output and receipt, consuming no extra scan credits. The [completed engine record](engine/run-metadata.json) contains one scan, three unique evaluations and zero accepted proposals.

A separate [diagnostic protocol](method/diagnostic-protocol.json) was declared while the final evaluation response was handed to GEPA; the candidate scans began after the engine completed. This adaptive diagnostic allowed the already-recorded slight preference losses for measurement, while requiring the existing factual and clarity passes. It measured both unchanged candidates, with no extra writer call, repair or candidate selection. Both stayed at 100% AI against the same saved seed observation. The shared seed is one observation, not two independent baseline scans. These later results do not overwrite GEPA's utilities or acceptance decisions.

## Preparation and evidence limits

The first baseline writer encountered archived target scores in the ordinary phrase reference and stopped without an output or scan. The coordinator then froze the same editing-only reference view for both arms and dispatched a fresh baseline writer. The discarded dispatch and filtering are retained in the [packet amendment](method/protocol.json). The repository fix moves those archived outcomes into the evidence reference.

Candidate 1's coordinator instruction used different wording and expanded trace requirements. Candidate 2 used the recovered baseline instruction with only skill and output paths changed. Exact sanitized operators are archived. Proposal 1 also received a coordinator-requested activation repair before its writer was dispatched; the original proposal remains available. These differences limit a causal attribution to the skill policy alone. Agent separation was operational on a shared filesystem. Exact backend model and sampling details, tokens and model costs were not exposed.

Reviewers used the supplied claim inventory and RFC evidence; this was not an exercised client/server test. Literal entry used GPTZero's Code Block editor style to preserve text, independently of code exclusion: one terminal source LF was removed for submission, and the editor added three LF characters. The [submitted and editor representations](measurements) retain those exact bytes. Each completed Basic view showed Text up-to-date, and the native validator matched the reviewed prose, before/after editor content and visible result. The free interface initially displayed Advanced results and an upgrade prompt; the coordinator selected the completed Basic view without an upgrade or second submission.

These are saved maintainer UI observations, not authenticated service exports. Account UI, detector document URLs, screenshots and confirmation content stay private; hashes and allowlisted measurements are public. The [export manifest](export-manifest.json) distinguishes exact copies from sanitized metadata. This reused-case pilot establishes neither a score benefit nor that further optimization is impossible.

## Archived runner

[runner.py](runner.py) is the exact executed callback adapter. It expects a pinned upstream checkout and a configuration path, and writes request files for a coordinator to answer. It does not call writers, control Chrome or authenticate receipts itself. The coordinator must validate native receipts, enforce scope and review requirements, and reserve costs before scanning.

Its deadline is checked while waiting for absent responses, so a coordinator must also enforce the deadline before dispatch. The source guard checks HEAD and unstaged tracked changes but misses staged-only or untracked changes. Persisted evaluations can survive an interruption ahead of GEPA's checkpoint, so the optimizer counter alone is not a complete restart spend ledger. These limitations are retained with the executed snapshot rather than silently patched after measurement.
