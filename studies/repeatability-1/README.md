# Same-input GPTZero repeatability check

On September 7, 2026, both frozen Python answers repeated their earlier GPTZero scores: **91% AI for the existing-skill edit and 100% for the rejected candidate**. This diagnostic adds one observation per unchanged text. It does not demonstrate improvement from a new writing rule.

| Exact text | Earlier AI / mixed / human | Repeat AI / mixed / human | Words per scan |
| --- | --- | --- | ---: |
| [Existing-skill edit](../autoresearch-controls-1/inputs/python-baseline.txt) | 91 / 9 / 0% | 91 / 9 / 0% | 129 |
| [Rejected candidate](../autoresearch-controls-1/inputs/python-candidate.txt) | 100 / 0 / 0% | 100 / 0 / 0% | 125 |

Both new observations used completed **GPTZero Basic Scan, Model 4.9b**, in signed-in Chrome. Both had no short-text warning. Exact source, submission, and effective editor hashes matched the frozen inputs; the results were current. All three confidences are retained in [results.json](results.json). The two new scans used 254 words. No text was rewritten, no retry ran, and no credits were purchased.

The [plan](protocol.json) was frozen before either new scan, including a randomized order: existing edit first, rejected candidate second. It required both scans regardless of the first result. The existing separate, score-blind [quality review](../autoresearch-controls-1/quality-review.json) was reused only after matching both exact input hashes. That review passed both answers and judged their quality equivalent.

This pair was selected because of its earlier 91-versus-100 result, so the diagnostic is adaptive. Two observations per text are too few to estimate detector variability or establish reliable performance. The agreement also cannot distinguish deterministic scoring from cached results. It does show that these two fresh document submissions returned the same scores under the same displayed model. Their score ordering and exact scores matched the earlier observations.

The [earlier original-to-edit comparison](../autoresearch-controls-1/README.md#exploratory-source-to-edit-reduction) remains 100% to 91%. Its original was scanned once; this diagnostic repeated the edit and the rejected candidate, not that original. It therefore does not repeat the complete original-to-edit comparison. The candidate remains rejected and the fresh confirmation cases remain unused.

The practical lesson is to distinguish repeat observations of fixed text from fresh outputs produced by a changed skill. Retain both when investigating an isolated score decrease; neither substitutes for preselected confirmation cases. The stored scores are maintainer-recorded UI observations, not authenticated service exports or evidence of human authorship. Private screenshots and account records are not included.
