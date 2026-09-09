# Paired editing examples: preferred prose, unchanged detector scores

September 9, 2026. **Both prose-only comparisons stayed at 100% AI / 0% mixed / 0% human.** A separate masked LLM reviewer slightly preferred both candidate answers, and all required claims passed. The controller closed the round as `development_no_improvement`; no writing rule was promoted and no article or reply was updated.

| Reused development case | Control → candidate prose words | Control → candidate AI confidence | Quality preference |
| --- | ---: | ---: | --- |
| HTTP conditional GET explanation | 123 → 119 | 100% → 100% | Candidate, slight |
| Complete X launch article | 574 → 558 | 100% → 100% | Candidate, slight |

All four completed observations used **GPTZero Basic Scan, Model 4.9b**, with no short-text warning. They consumed **1,374 free word credits**, matching the combined quotes and observed allowance decrease. The [results](results.json) retain all three confidences, timestamps, exact inputs, full-message associations and private evidence hashes. Two preselected confirmation cases stayed unreleased to output writers and unscanned because development did not improve.

## What changed

The [candidate policy](method/candidate.txt) adds three fixed synthetic editing demonstrations to the [incumbent](method/incumbent.txt): two useful revisions and one accurate revision that makes the instruction less direct. Each pairs evidence, original, revision and an illustrative editorial judgment. The writer reads all three, records at most two reading problems, and produces one complete revision. There was no target-draft selection, post-review repair, trained paraphraser or local detector.

Earlier local experiments had already used a worked Python source/edit pair and an example-to-target edit map. This round tests the specific three-example mix and explicit judgments; it is not the first use of editing demonstrations. The initial literature review did not identify that overlap, which the final independent audit caught. The frozen proposal and its result were retained.

[AdParaphrase](https://aclanthology.org/2025.findings-naacl.78.pdf), section 4.2 and Appendix E, motivates comparing positive and non-improving revision demonstrations. Its Japanese advertisements, human preference data and larger example sets differ substantially from these three English teaching examples. It reports no detector experiment. Our examples are explicitly synthetic; their judgments are not human annotations or measured detector outcomes.

The coordinator assessed one proposal for feasibility before generation. Separate fresh agents wrote the two arms using the same [operator](method/operator.txt) and [source packets](sources/development.json), with both cases in each agent's context. The [masked review](reviews/masked-verdict.json) passed all seven HTTP claims and eighteen article claims in both arms. The reviewer preferred the candidate's earlier request-cost clarification and the article's more explicit dating and independent-review wording. Added examples, judgments, diagnosis and prompt length remain a bundled intervention.

## Prose and code were separate

Both full messages were reviewed, then explicit complete-line exclusions produced the measured prose. The HTTP case has no independent code: its header names and values remain part of the explanation. Each article excludes only the unchanged installation command and its terminating newline. Titles, step labels, prompts, URLs, qualifications, historical evidence and the full screenshot caption remain in the scan. The article has 580/564 words including its command and 574/558 measured prose words.

The article's example measurement prompt was updated under the user's prose-only requirement in **both** arms. Its historical September 5–6 study counts and September 6 screenshot results remain historical facts. Those screenshots do not score this article. This round uses fresh controls; earlier whole-message observations were not relabelled as prose results. It does not isolate the effect of removing code.

Full messages, derived prose and exclusion maps are under [outputs](outputs). The [saved submitted/editor representations](measurements) retain exact bytes. Literal entry used GPTZero's Code Block editor style to preserve the prose: exactly one terminal source LF was removed for submission, and the editor added three LF characters. This entry style is separate from the source-code exclusions; the submitted article contains no installation command.

The free workflow initially displayed Advanced results and an upgrade prompt. After processing completed, the operator dismissed the prompt and selected the completed Basic result view. Each saved result showed `Text up-to-date`; no upgrade was accepted or second scan submitted. Native validation checked the complete editor text and visible result text. Private screenshots show result panels and visible excerpts, not every line of the long articles.

These are saved operator UI observations, not authenticated service exports. Exact backend model/settings details and monetary costs are unavailable. Agent separation on a shared filesystem is operational, not an isolation guarantee. The [export manifest](export-manifest.json) identifies exact copies and sanitized metadata; account UI, document identifiers and unreleased confirmation content stay private. Frozen `.txt` policies are archival experiment inputs, not additional installable skills.
