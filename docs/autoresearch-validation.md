# Autoresearch setup validation

September 6, 2026. This validates the workflow implementation and its first agent-driven pilot. It does not demonstrate lower detector scores from a new skill.

## First real agent round

One improver produced three small instruction proposals from the same frozen incumbent. A separate inference-only selector ranked them and selected the condition-and-outcome comparison proposal. Two fresh writers, using the same common operator and inherited runtime settings, generated incumbent and candidate answers for two existing synthetic development cases. The precise model identifier was not exposed and was recorded as unavailable rather than guessed.

A separate judge received randomized A/B labels and no detector scores, skill identities or ranking. All four answers passed factual and editorial review with all 17 claims preserved. The judge narrowly preferred the candidate for the GitHub Actions case and the incumbent for the Python TaskGroup case. Under the predeclared rule requiring no quality regression, the candidate was rejected before scanning.

The ledger finished as `development_rejected`, with **zero detector calls, zero detector words charged**, no pending jobs and a fixed completion timestamp. The otherwise eligible case was retained as `not_scanned_candidate_rejected`; no detector score was invented. Two confirmation cases were prepared privately but never supplied to the improver, selector or output writers. They were neither generated nor scanned. The first pilot therefore exercised proposal, ranking, generation, masked review, rejection and resumption; it did not exercise a fresh live detector submission through the new controller.

## Detector adapter compatibility

Eight genuine saved observations from the earlier targeted-edit comparison were replayed through the new receipt adapters: four GPTZero Basic 4.9b and four Pangram 4.0 results. All matched the saved native metrics and exact declared input transformations. These were archived compatibility checks with their original timestamps, not new scans or evidence for the pilot candidate. Twenty adversarial probes rejected contradictory or invalid receipts, including a different answer's snapshot, stale/processing evidence, altered text, missing scores and unsupported transformations.

The separate review initially found missing snapshot-to-answer binding and missing Pangram processing rejection; both were fixed and the archived replays and probes passed again. The evidence remains operator-recorded UI material, not independently authenticated service output.

## Controller checks

The test suite exercises frozen source/configuration/output metadata; role and generation-context separation; native receipt import; full synthetic development/confirmation runs; wrong hashes and models; no-op and quality rejection; pair affordability; reserved confirmation calls and words; failed and uncertain attempts remaining charged; concurrent reservations; interrupted-commit recovery; stable positive and negative completion after expiry; and rejection before spending when any fully reviewed case fails the quality rule. Synthetic detector fixtures in these tests are explicitly labeled and are never included in measured study results.

Independent review found and resolved three controller behaviors: a completed outcome changing to expired, first-arm reservation when the full pair was unaffordable, and pending scan jobs surviving rejection of the whole candidate. All 72 repository tests passed after those fixes, along with lint and skill validation. The earlier 44-scan historical checker retains its original scope; it does not validate new experiments.

The implementation is an on-demand loop driven by an active agent. It does not prove OS isolation, authenticate agent identities, run agents or Chrome unattended, implement a vendor API, train a preference model, or show that RPM ranking improves writing-detector performance. The installed changes add the research workflow; the tested candidate rewriting rule was not promoted. No public answer, new showcase success or repository push was produced by this pilot.

## September 7: complete reservations and failure recovery

A synthetic probe found that the first-arm affordability check could underestimate the other arm's UI cost. With two five-whitespace-word outputs costing six service words each and eleven development words available, the first reservation succeeded and the second failed. The first attempt still appeared as a detector job. This was a controller reproduction with synthetic text, not a live detector observation.

The new `reserve-pair` command commits both actual UI word reservations in one transaction or commits neither. The older single-arm command remains available for resuming partial reservations, but it does not release a scan job until both costs are reserved. Research calls, research words and live vendor allowance remain separate limits; an unspent word reserve alone does not retain confirmation call capacity.

Separate review also found that reserved jobs could remain dispatchable after a primary scan failure or a later quality rejection in the same split. Those jobs now permit outcome recording only. A primary failure blocks new work, retains every charge and incomplete case, and becomes a stable completed rejection once all existing reservations are settled. Reconciliation can finish after the deadline without replacing that failure with an expiry status. Existing partial reservations also remain visible for reconciliation after a quality rejection.

The 80-test suite includes eight added regression tests for UI-cost mismatch, atomic rollback, exact-budget pair dispatch, concurrent pair reservation, primary-failure blocking, deadline reconciliation and partial-reservation recovery. Existing rejection coverage also checks that already reserved jobs become reconciliation-only. These checks validate the controller's local behavior; they do not establish detector-score improvement, service authenticity or protection against an operator submitting text outside the ledger.
