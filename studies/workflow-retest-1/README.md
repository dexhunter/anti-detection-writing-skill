# Retesting the updated skill on four failed cases

**All 12 completed scans returned 100% AI / 0% mixed / 0% human.** Direct editing and reconstruction from a fact inventory each produced **0 reductions in 4 comparisons**. This batch does not establish a score-reduction workflow.

The September 6, 2026 test reused the four failed questions from [requested-alternatives-1](../requested-alternatives-1/README.md). The two longer cases had also failed quality review in the separate [HIP model pilot](../hip-feasibility-1/README.md). This retest used the updated writing skill with fresh writer agents; it did not use HIP. These are synthetic development cases, not an unseen dataset or new public answers.

## Compared workflows

The [plan](plan.json) selected all four cases and randomized the scan order before results. The complete [frozen skill](frozen-skill/SKILL.txt) and [file hashes](frozen-skill-files.json) identify the tested version.

1. **Original:** rescan the exact original as a current-service control.
2. **Direct edit:** a fresh writer sees the original, question and source inventory, and follows the updated skill to produce one requested alternative.
3. **Rebuild from facts:** a separate fresh writer sees the question, source inventory and protected code/URLs, without the original prose, and writes one answer. This tests whether removing the old wording from the writer's context helps.

No authentic writing sample was available, so the conditional voice-matching instruction was inactive. No invented sample, padding, added quotation or post-score rewrite was used. Different writer instances and workflow context prevent isolating the effect of one instruction.

## Complete results

GPTZero **Basic Scan, displayed Model 4.9b**, September 6, **19:56–20:05 UTC**. All results displayed **Text up-to-date** and matched the frozen final inputs. Scores below are AI confidence; all mixed/human confidences were zero. Word counts are from the UI.

| Case | Original | Direct edit | Rebuild | Words: original / direct / rebuild | Short warning |
| --- | ---: | ---: | ---: | --- | --- |
| Git tracking | 100% | 100% | 100% | 78 / 90 / 97 | All three |
| Docker port publishing | 100% | 100% | 100% | 85 / 99 / 96 | All three |
| Kubernetes probes | 100% | 100% | 100% | 164 / 181 / 210 | None |
| PostgreSQL snapshots | 100% | 100% | 100% | 180 / 178 / 206 | None |

The [complete records](results.json) link all 12 original/candidate texts and exact submitted/effective representations. There are eight paired alternative comparisons sharing four controls, not eight independent controls.

## Quality review and one repair

A separate reviewer saw randomized A/B candidates, originals and source inventories without workflow labels or scores. [Seven of eight first passes passed](reviews/first-pass.json). The Git reconstruction omitted why the ignore rule prevents ordinary re-addition. Its commands and operational instructions were correct, but useful original content was missing from both the prepared inventory and the resulting answer.

The [first attempt](revisions/git-rebuild-first-pass.md) is retained. One [recorded repair](revisions/git-rebuild-repair.json) restored the explanation before any scan; the [exact corrected version passed review](reviews/git-repair.json). Thus all eight final alternatives passed, while the initial coverage failure remains visible. The manifest's label map connects masked reviews to workflows.

The reviewer preferred the originals for Git and Docker, and the direct edits for Kubernetes and PostgreSQL. The facts-only reconstructions were longer without a demonstrated readability advantage. These are LLM judgments, not human preference measurements. Added explicit details and length differences are recorded separately from correctness.

## What the workflow should retain

Before a writer works from facts alone, a preparer must reconcile that inventory with the original and record intentional cuts. Otherwise, the writer cannot recover a missing claim. Keep the original available to the independent reviewer. Classify a packet omission separately from a false claim or a detector tie.

Retest a frozen version, check that the changed instruction actually applies, and retain one explicit workflow comparison at a time. Review and repair factual defects before scanning; preserve every earlier attempt and review. A lower score would justify a fresh-case confirmation before a broader transfer claim. This batch supports the inventory-check correction, not adopting facts-only rewriting as a detector improvement.

The follow-up inventory-check instruction was added after these results and is not part of the frozen intervention tested here.

## Measurement limits

Literal Markdown was entered in Code Block mode. One final source newline was removed where present; the editor then appended exactly three line feeds. Exact representations and hashes are retained; the strict verbatim receipt checker does not accept that wrapper difference and was not used. Saved UI observations are not authenticated service exports.

An initial PostgreSQL direct-edit scan did not complete after immediate navigation; it was retried once on the same document. The first attempt remains unmeasured. Final observations account for the visible 1,664-word allowance change. Later processing and navigation delays caused no additional scan submissions. Raw screenshots, document identifiers, account UI and private audit logs remain private.

These 12 observations are separate from the historical 19-question/44-scan dataset, the six-question comparison and the earlier eight-scan requested-alternative pilot. No earlier records or showcase examples were replaced.
