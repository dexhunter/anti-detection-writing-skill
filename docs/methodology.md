# Methodology and provenance

This is a retrospective record of developing an answer-editing workflow on September 5–6, 2026. The packaged skill is a portable consolidation of lessons, not the unchanged intervention used in every trial. No new detector scans were run for the initial repository export of that historical study.

This document describes the original 44-scan study. The [showcase](case-studies.md) selects only paired, quality-passing reductions; [when the skill may not help](when-it-may-not-help.md) covers unchanged, rejected, unpaired, and unmeasured outcomes. The subsequent [six-question comparison](../studies/unseen-transfer-1/README.md) keeps its inputs and outcomes separate. Its 12 planned Basic Scan / Model 4.9b observations were completed on September 6, 2026; all scored 100% AI / 0% mixed / 0% human, giving six tied pairs. Its exact submitted/effective inputs, trailing-newline transformations, and one supplemental repeat are documented with that cohort. This completes the older frozen comparison and does not validate later literature-informed instructions.

## Included observations

`studies/results.json` includes 19 questions and 44 valid scans. Each scan points to an exact UTF-8 effective-editor input and its SHA-256. The first three cohorts cover all 15 preselected questions and all their baseline/plain pairs. Two of those cohorts add ten fixed-body quotation comparisons. Four later new answers have only a final-text observation.

Every primary baseline and plain revision scored 100% AI. Separate LLM evaluators, withheld detector scores, assessed technical correctness and prose. Eight plain revisions were rated improved, seven equivalent, all technically acceptable. Necessary code, factual corrections, and scope cuts were part of the editing process. Consequently, the comparison does not isolate stylistic changes.

For each of the ten quotation comparisons, the revised body stayed fixed. A short, exact asker excerpt was selected for relevance before scanning. No excerpt was rotated after a score. Five comparisons decreased AI confidence and five did not. All quotation variants were rated equivalent in prose quality to their respective plain revisions. Content and length change together; these observations identify no mechanism.

The new-answer cohort selected #553, #231, and #287 before its initial scans; #285 was added afterward. It has neither owned-answer baselines nor unquoted controls. Two of four final texts met the particular user's below-100 AI condition and were published. This is not a before/after success count or a preselected four-case transfer benchmark. A metadata correction marked their added quotations explicitly; input bytes, scores, and hashes did not change.

## Exact artifacts and private evidence

The dataset is an allowlisted export of maintainer-recorded completed GPTZero Basic Scan UI observations, displayed Model 4.9b. It includes all three confidences, UTC times, displayed word counts, short-text warnings, source discussion links, review outcomes, and editor input hashes. The original Markdown hashes are included as provenance identifiers; those Markdown files are not distributed here. Public comment links show the last verified publication artifact, which can later change.

An independent LLM agent audited the underlying 44 records for original-body hashes, exact editor hashes, completed and visibly fresh mode/model/scores, and recorded transformations. Thirty-four later records also retain exact submitted-text sidecars privately. The initial ten use older editor-based provenance with documented backtick and whitespace rendering checks, including one observed opening-link-bracket change. These should not be represented as identical capture pipelines. The optional public receipt checker is stricter and is for new verbatim-entry measurements, not these historical records.

Raw browser snapshots, account quotas, detector document IDs, local paths, complete discussion dumps, and private review records are not distributed. The input hashes and the local checker detect inconsistent files; they cannot authenticate a remote detector response. There is no signed GPTZero export or independent replication. An LLM audit of saved evidence is not a human quality rating or independent remeasurement.

## Exploratory work outside the primary counts

Earlier adaptive work on ADK #1742 produced multiple unchanged prose rewrites. Version 8 scored 43% AI but failed technical review because it overpromised duplicate-email prevention. Version 9 corrected that wording, passed at 60%, and was published. Its source qualifications and optional detail also changed, so this is not a fixed-body quotation test or complete preservation of every earlier claim. No cloud deployment was exercised.

A later follow-up to the initial five-case pilot tested six alternate structures across three questions, one observation-led revision, and two formatting controls; all stayed at 100%. A fixed-body quotation pilot on Poetry #10095 scored 94%, while the reserved ADK #1513 check stayed at 100%. That follow-up recorded eleven valid scans and one invalid input-corruption attempt, which was repaired. Its adaptive design is distinct from the ten fresh quotation-transfer cases. These exploratory inputs are summarized here but are not included in the 44-file primary dataset or the primary showcase. Their exclusion from the primary denominator must not be read as an absence of further failures.

## Limits

- Small, selected technical-answer samples; no random sampling or externally held-out benchmark.
- Evolving skill versions and corrected source claims; no prospective evaluation of the packaged version.
- Separate LLM reviewers, with no independent human usefulness ratings or agreement study.
- Typically one scan per text, with no systematic repeatability estimates, confidence intervals, or current-service replication.
- Five displayed under-100-word warnings: both Qwen #1251 inputs and all three ADK #1956 inputs. No padding was added.
- Detector confidences classify the document; they do not measure the percentage of words generated by AI. All 44 recorded human confidences were zero.
- A quotation changes content and length; lower scores do not establish better prose, human authorship, or a reusable bypass.
- Published bodies were read back at the time. Acceptance as a best answer, GitHub badges, and downstream usefulness were not measured.

Future studies should prerecord cases and variants, keep the model/mode comparable, retain every attempt, separate adaptive work, and ask independent human reviewers to assess usefulness without scores. Any prospective fixed-skill claim needs a new study rather than relabeling these development records.
