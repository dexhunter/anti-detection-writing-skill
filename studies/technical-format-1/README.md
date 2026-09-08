# Technical formats: a small diagnostic with no score reduction

September 8, 2026. Two additional formats left the technical example at **100% AI confidence**. A separate reviewer passed all three answers for correctness and readability, with every pair tied. The full comparison used **three GPTZero Basic Scan / Model 4.9b scans and 394 word credits**. No further iterations were run within this diagnostic.

| Exact text | Displayed words | AI / Mixed / Human confidence |
| --- | ---: | --- |
| [Freshly scanned existing baseline](measurements/baseline/answer.txt) | 133 | 100% / 0% / 0% |
| [Reference card](measurements/reference-card/answer.txt) | 127 | 100% / 0% / 0% |
| [Mini-FAQ](measurements/mini-faq/answer.txt) | 134 | 100% / 0% / 0% |

The [source contract](sources/case.json) asks how ETag validation saves an unchanged JSON body and whether it eliminates requests. Both formats preserve all seven claims, protected identifiers and necessary conditions. The [frozen methods](frozen/methods.json) change organization: one makes a lookup reference, and the other groups the answer under the reader's two questions. No mistakes, padding, invented examples or scope cuts were introduced.

One writer produced one final per format. A separate reviewer assessed anonymous exact texts before scanning; the [full review](quality-review.json) and [mapping](review-mapping.json) are retained. The [configuration](frozen/config.json) initially requested fresh contexts. A [prospective amendment](frozen/context-amendment.json), recorded before generation when a new agent could not start, disclosed reuse of existing writer and reviewer contexts. They reported no previous exposure to this ETag case or its scores, but their contexts included unrelated work. Fresh-context isolation is not claimed. The [original operator](frozen/operator.txt) and [skill entry](frozen/skill-entry.txt) are preserved; the latter predates the latest readability instruction.

The complete package was reserved before its first scan, within a 480-word and three-call ceiling. No local model run, repair loop or scan retry was used. This limits spend for a specific diagnostic; it is not a monetary or runtime cost comparison. LLM token usage and monetary cost are unavailable.

The [results](results.json) retain all three completed observations, timestamps, exact text hashes, and submitted and effective editor representations. Literal Markdown was entered through Code Block mode. Submission removed one final line feed; the captured editor added exactly three line feeds, with identical text before and after each scan. Each result was current, displayed Basic Scan / Model 4.9b, and had no warning. Account information, private document URLs and native screenshots are omitted from this public export. These are operator-recorded UI observations, not authenticated service exports. The [manifest](export-manifest.json) covers every exported file except itself.

This is one previously exposed synthetic development case with a shared control. It supplies no unseen-case validation, skill-wide success rate, or explanation of the detector's internal decision. The result does not establish that a reduction is impossible. Neither format was adopted as a method for reducing detector scores.
