# Prospective Greyscope selection diagnostic

September 10, 2026. Greyscope added no selection benefit on two new synthetic technical questions. The independent quality reviewer chose one clear winner per question, leaving no eligible alternative under the frozen rule. Both winners then received fresh GPTZero Basic 4.9b results of **100% AI / 0% mixed / 0% human** in a separately declared baseline diagnostic. A subsequent adaptive writing test produced one readable revision with the same result and one revision rejected on readability before scanning.

## What was tested

One fresh writer produced three sequential answers per question using the incumbent skill's writing instructions and a shared fact packet. The questions concern Python mutable default arguments and DNS negative caching; their claims were checked against Python documentation, RFC 2308 and AWS documentation. They are synthetic examples, not public Discussion answers or untouched confirmation cases from earlier studies.

A fresh LLM reviewer, without detector scores or writer-version labels, checked all six answers and all 36 required claims. Every answer passed factual and suitability review. The reviewer ranked Python A, B, C and DNS B, C, A, placing every answer in a separate preference group. Only members of the best group could replace the quality-only control. Both groups contained a single answer; the original selector therefore has two no-op cases and zero dispatched comparisons.

| Input | Quality rank within question | Greyscope AI involvement, 0–1 | Fresh GPTZero AI / mixed / human |
| --- | ---: | ---: | --- |
| Python A | 1 | 0.742589 | 100 / 0 / 0 |
| Python B | 2 | 0.898881 | Unmeasured |
| Python C | 3 | 0.856951 | Unmeasured |
| DNS A | 3 | 0.795294 | Unmeasured |
| DNS B | 1 | 0.624466 | 100 / 0 / 0 |
| DNS C | 2 | 0.646350 | Unmeasured |

All six pinned Greyscope forwards completed in 6.301 seconds, without truncation; complete calibrated prompts contained 231–255 tokens. The model's lowest score matched the quality winner on each question. Its native AI involvement is an ordinal estimate, not GPTZero document confidence. The four unscanned alternatives prevent any claim about their GPTZero ranking.

The [baseline addendum](baseline-addendum.md) was frozen after quality review and before local inference or commercial results. It selected Python A and DNS B from quality alone. Their two completed scans used 246 word credits; neither had a short-text warning. Every answer is entirely prose, with inline identifiers retained and empty independent-code exclusions. Exact input, submitted and editor bytes, completed Basic view, model and all three confidences were checked against private native receipts. The UI initially opens the completed Advanced view; the recorded result is its Basic view after completion. No additional result scan or paid upgrade was used to open that view.

## Separate adaptive writing test

After observing both baselines, the coordinator froze a [specific extension](adaptive-candidate-SKILL.md) of the existing component/dependency guidance: organize a state-related explanation around the concrete object or cached response being reused and keep its lifetime together. This reused earlier reader-focused ideas; it was not claimed as a novel method. A fresh writer received only the fact packet and writing instructions, with no earlier answers or scores, and returned one first-pass answer per question.

A further fresh LLM reviewer saw neutral X/Y labels and no scores or method identity. Both revisions preserved the six required claims and passed suitability checks. The reviewer preferred the Python original because the revision split the conditional fix from its empty-list rationale. It preferred the DNS revision because it followed the question's cause, lifetime and proposed TTL change before offering the diagnostic check.

| Adaptive case | Quality preference | GPTZero baseline → candidate, AI confidence | Disposition |
| --- | --- | --- | --- |
| Python | Original | 100% → unmeasured | Revision lost readability comparison |
| DNS | Revision | 100% → 100% | No measured reduction |

Only the DNS revision was scanned, using 119 additional word credits. Its result was again 100% AI / 0% mixed / 0% human, Basic 4.9b, without a short-text warning. The Python rejection remains in the two-case denominator. No complete-cohort mean is reported. Total spending was **three new scans and 365 word credits**, with no purchases.

The [adaptive protocol](adaptive-protocol.md) declared reuse of the same-session baseline receipts before generating either new answer. These are not new baseline scans, and this adaptive comparison is not untouched confirmation. The baseline was chosen among three drafts, whereas the candidate was a single new output; any result belongs to that complete workflow, not an isolated causal estimate of the extra instruction. The [exact outputs and review](adaptive-quality/packet.json), [review verdict](adaptive-quality/review.json) and [complete results](adaptive-results.json) retain both cases. The experimental instruction remains uninstalled and was not promoted.

## Interpretation and evidence

This convenience sample does not validate a local selector, establish general detection accuracy, or prove that a technical reduction is impossible. A quality preference is an independent LLM assessment, not a human-reader evaluation. The six initial answers are sequential alternatives from one writer, not six independent samples. Exact backend model and sampling settings were unavailable. No writing instruction or automatic detector selector is promoted from this result.

The [source packet](sources/cases.json), [exact answers](quality-inputs), [blinded review](quality/review.json), [local results](greyscope/results.json), [baseline observations](baselines.json), [frozen no-op decision](selection.json) and [export provenance](EXPORT.md) retain unsuccessful and unmeasured outcomes. The original private artifact hashes are distinguished from sanitized public metadata. Account captures, screenshots and private detector document URLs are excluded.

The selector's 26 synthetic offline tests cover quality eligibility, duplicate records, invalid scores, missing outcomes, exact-input hashes and the decimal 0.01 threshold. Run `uv run --no-project python -m unittest discover -s studies/prospective-proxy-1 -p test_selection_rule.py -v` from the repository root. These checks reproduce decisions from saved values; they do not authenticate or rerun commercial scans.

## Later phrase-list update

After the measured comparisons were complete, a user suggestion prompted a check of GPTZero's visible AI Patterns preview. It listed Empty commentary (5.7×), Overblown importance (5.3×) and Dressed-up verbs (4.3×); text-specific pattern findings required the Advanced feature. The skill's [phrase review list](../../skills/anti-detection-writing/references/phrase-review.md) now includes these as contextual editing checks, with our own examples and preserved qualifications. They are vendor-reported associations, not a diagnosis of these answers or measured edit effects.

A [limited phrase and context check](phrase-category-review.json) found no justified phrase-only edit in the eight saved replies. Illustrative literal matches were zero; the check is not an exhaustive semantic detector. No text or prior receipt was changed, and no further scan was made for this list update.
