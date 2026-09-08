# Experimental release checks

The September 6 checks below are historical. They assess packaging and saved evidence consistency; they are not new detector trials. The current release has additional scripts, references and studies.

## September 8 update

The expanded offline suite passed 94 tests under Python 3.13.5: 48 controller tests, 20 original receipt/study checks, 12 native-receipt checks and 14 local-detector tests. A separate code review found no release blocker. The optional [local detector](../skills/anti-detection-writing/references/local-detector.md) requires Python 3.11–3.13 and four pinned ML dependencies; it is not part of the standard-library-only receipt/controller path. Its saved CPU inference evidence was checked against the current script and model-manifest hashes, without downloading or rerunning the model. MPS inference and a clean dependency installation were not exercised in this release review.

An independent evidence review checked 218 exported or explicitly paired hashes, 105 study JSON files and 171 live documentation links before the latest report was added. It found no private-data or evidence-integrity blocker. Newly added experiment records are checked separately; the historical dataset checker covers the original 44 observations only.

A separate final audit verified all 195 model-assisted export hashes and all 22 technical-format export hashes, including source correspondence and all 27 native scan receipts. It confirmed the corrected development decision, unscanned failed confirmation, and three unchanged technical-format results. The audit found no remaining publication blocker in either export; it did not rerun the detector service.

Final packaging checks passed the skill-creator validator with PyYAML supplied in an isolated `uv` environment, Ruff across the repository, and `skills` 1.5.23 discovery of exactly one skill. The 94-test suite passed again after the exports were added, and all 202 local file links in current documentation resolved. No additional live model execution was needed for these packaging checks. Whitespace checks passed for current code and documentation; archived study text deliberately preserves its measured blank lines and raw-output whitespace.

## Historical September 6 checks

The latest focused research update inspected five additional papers and five GitHub skills. Its [HIP model pilot](../studies/hip-feasibility-1/README.md) generated two outputs locally; both failed separate factual review and neither was scanned. A separate writer followed the conditional style-sample instruction on one synthetic incident update, preserving the times, pending-job count, uncertainty and retry prerequisite without importing sample facts. The parent reviewer confirmed those invariants against the exact reply. This is one behavior check, with no detector or human-preference result. The 20 offline tests, Ruff and packaged/installed skill validators passed; the original 44-scan record remains unchanged.

| Check | Observed result |
| --- | --- |
| Public dataset integrity | 44 exact input hashes verified; 19 questions; all cohort counts recomputed |
| Fixed-body comparisons | All ten quoted inputs retain their plain answer body exactly |
| Offline Python tests | 20 passed, including corrupted text, stale UI, mismatched scores, unsafe artifact paths, omitted failures, optional thresholds, and command-line exit codes |
| Skill structure | Skill-creator validator passed |
| CLI discovery | `skills` 1.5.23 discovered exactly `anti-detection-writing` after the publication rename |
| Isolated project installation | Copy installation for Codex succeeded; all six packaged skill files present |
| Local documentation links | No missing file targets |
| Public export hygiene | No detected personal filesystem paths, detector document URLs, or token/private-key patterns; documentation independently reviewed for private data |
| Lint | Ruff 0.9.10 passed |

Those historical Python tests ran with Python 3.13.5. The receipt and study-checking code used only the standard library and targeted Python 3.10+. This statement does not cover the later optional ML detector. Other Python versions and agent products were not exercised in those checks.

A separate writer agent followed the packaged skill on one synthetic email-retry fixture. The supplied facts were that sending occurs before saving the sent record, a crash can occur between them, and the provider has no idempotency support. The baseline invented production experience and promised that saving after sending makes duplicates impossible. The revised reply removed that experience, explained the crash gap, and avoided the guarantee. A separate evaluator requested one clarification: a crash during saving does not necessarily mean the write failed. The final wording therefore made the retry risk conditional on the record not having been saved. The writer correctly reported no scan or publication because the fixture provided neither browser access nor publication authorization. This is a single LLM packaging smoke check, not evidence of general writing quality or detector performance.

The larger historical study received a separate LLM audit of its raw saved evidence. That audit confirmed the primary counts and the distinction between legacy editor capture and later submitted-text records. It did not rerun GPTZero or supply independent human ratings. Raw private audit files are not included in this public package.

The subsequent [six-question comparison](../studies/unseen-transfer-1/README.md) adds 18 exact prepared Markdown files, whose hashes and protected spans were checked separately. All twelve candidate answers passed blind technical review; clarity preference was revised 2, current 1, equivalent 3. The skill structure validator and lint passed after the two instruction additions. Its 12 planned detector observations were subsequently completed on September 6, 2026, all at 100% AI / 0% mixed / 0% human in Basic Scan / Model 4.9b. The cohort retains 24 exact submitted/effective text files and one supplemental unchanged repeat; its six paired outcomes are ties. This is completion of the older frozen comparison, not validation of later literature-informed instructions. The earlier 44 scan records are unchanged.

Before publication as `anti-detection-writing-skill`, the packaged skill was renamed to `anti-detection-writing` and its wording broadened to replies, emails, articles, and documentation. The 20 tests, evidence checker, skill validator, and Ruff passed again. An isolated project copy installation with `skills` 1.5.23 for Codex discovered one skill and matched all six packaged files byte-for-byte. A separate publication reviewer checked the repository and its two prior commits for private material, reconciled the saved evidence, and found no publication blockers.

A fresh writer followed the renamed skill to edit a synthetic workshop email. It preserved the room change and reason, both session times, the entrance instructions, the no-action condition for existing bookings, and the Thursday step-free-access deadline. The coordinator checked the result against those supplied facts. No detector scan ran. This is one behavior check for a general writing format, not a readability benchmark or evidence of lower detector scores. Historical study inputs, scores, and frozen skill versions remain unchanged.

The later [requested-alternative pilot](../studies/requested-alternatives-1/README.md) retained four current-skill keep decisions and eight distinct original/alternative text records. All eight texts passed masked quality review; all eight Basic 4.9b observations scored 100% AI / 0% mixed / 0% human. A separate measurement audit reconciled exact text, UI freshness, warnings and order. A variant behavior check on the ordinary workshop email made one justified clarification without triggering a detector experiment. This supports a narrow requested-alternative exception, not improved detector performance. Complete inputs and limitations are recorded with that pilot.

The subsequent showcase update selects only the five primary paired reductions and documents other outcomes in [when the skill may not help](when-it-may-not-help.md). A separate reviewer checked all five pairs, score triplets, quality verdicts, warnings, full denominators, and retained evidence. All 20 tests, the study checker, skill validator, Ruff, and local file-link checks passed. No new detector scans ran and no historical study files changed.
