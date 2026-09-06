# Experimental release checks

Checked September 6, 2026. These checks assess packaging and saved evidence consistency; they are not new detector trials.

| Check | Observed result |
| --- | --- |
| Public dataset integrity | 44 exact input hashes verified; 19 questions; all cohort counts recomputed |
| Fixed-body comparisons | All ten quoted inputs retain their plain answer body exactly |
| Offline Python tests | 20 passed, including corrupted text, stale UI, mismatched scores, unsafe artifact paths, omitted failures, optional thresholds, and command-line exit codes |
| Skill structure | Skill-creator validator passed |
| CLI discovery | `skills` 1.5.23 discovered exactly `discussion-answer-polish` |
| Isolated project installation | Copy installation for Codex succeeded; all six packaged skill files present |
| Local documentation links | No missing file targets |
| Public export hygiene | No detected personal filesystem paths, detector document URLs, or token/private-key patterns; documentation independently reviewed for private data |
| Lint | Ruff 0.9.10 passed |

Python tests ran with Python 3.13.5. The code uses only the standard library and targets Python 3.10+. Other Python versions and agent products were not exercised.

A separate writer agent followed the packaged skill on one synthetic email-retry fixture. The supplied facts were that sending occurs before saving the sent record, a crash can occur between them, and the provider has no idempotency support. The baseline invented production experience and promised that saving after sending makes duplicates impossible. The revised reply removed that experience, explained the crash gap, and avoided the guarantee. A separate evaluator requested one clarification: a crash during saving does not necessarily mean the write failed. The final wording therefore made the retry risk conditional on the record not having been saved. The writer correctly reported no scan or publication because the fixture provided neither browser access nor publication authorization. This is a single LLM packaging smoke check, not evidence of general writing quality or detector performance.

The larger historical study received a separate LLM audit of its raw saved evidence. That audit confirmed the primary counts and the distinction between legacy editor capture and later submitted-text records. It did not rerun GPTZero or supply independent human ratings. Raw private audit files are not included in this public package.
