# Model-assisted rewriting: a development gain that failed confirmation

September 8, 2026. **Retain the incumbent.** One model-and-editing workflow reduced GPTZero AI confidence on a reused business example from **100% to 0%**, and fresh execution repeated that result with different final wording. The technical example stayed at **100%**. Both previously sealed confirmation candidates preserved the facts but lost the independent reviewer's readability preference. **Confirmation received no detector scans, and no skill change was promoted.**

This is an adaptive development study with twenty attempted methods, not twenty independent trials. The complete [results](results.json) preserve every attempt disposition and all **24 completed GPTZero Basic Scan / Model 4.9b observations**, including controls and repeats. Scores below are native **AI / Mixed / Human confidence percentages**, not evidence of human authorship.

| Phase | Technical baseline → candidate | Business baseline → candidate | Completed scans |
| --- | --- | --- | ---: |
| Initial shared controls | 100 / 0 / 0 | 100 / 0 / 0 | 2 |
| Seven quality-passing method screens | Six methods tied in both cases; r20 technical stayed 100 / 0 / 0 | Six methods tied; r20 changed 100 / 0 / 0 → 0 / 0 / 100 | 14 |
| Midpoint and endpoint repeats | Exact control stayed 100 / 0 / 0 at both checks | Exact control stayed 100 / 0 / 0 at both checks | 4 |
| Fresh r20 verification | 100 / 0 / 0 → 100 / 0 / 0 | 100 / 0 / 0 → 0 / 0 / 100 | 4 |
| Retired confirmation cases | Visitor notice: baseline preferred | Game guide: baseline preferred | 0 |

All 24 completed scans had no recorded warnings. Seven methods passed the quality gate and were scanned: r01, r10, r12, r16, r18, r20 and r21. Six had no reduction; r20's mean development reduction was 50 percentage points, entirely from the business case. The other thirteen attempts comprise seven quality regressions, one fidelity failure, four no-ops and one declared-input execution deviation. An initial r04 proposal and r08 were rejected before authoring; these two proposal decisions are not extra attempts.

## What the measured workflow did

The selected r20 workflow used the released [AuthorMist Originality model](https://huggingface.co/authormist/authormist-originality/tree/2866bc928850ef4910d24ef5a9179740fab72e22), pinned at revision `2866bc928850ef4910d24ef5a9179740fab72e22`. Screening reused two known defective local pilot outputs. A fresh editor repaired factual and grammatical defects within a bounded pass; a different fresh editor then planned the answer around the reader's purpose and made bounded organization and fluency edits. Each editor processed both cases in one context. The exact [r20 instructions](frozen/methods/r20.txt), [incumbent](frozen/incumbent.txt), raw/repaired texts and operation ledgers are retained under [stages](stages).

Fresh verification executed two new local generation processes before new repair, organization and masked review. The fixed seed produced the same raw model bytes as screening; these were new processes, not independent random draws. Both final edited candidates and both newly written incumbent answers differed from the screening versions. The [fresh quality review](reviews/verification.json) passed all four answers and judged both pairs tied.

Generation used Apple MPS in bfloat16, seed 19, temperature 1, a 512-token output cap and CPU multinomial sampling without top-k, top-p or repetition penalty. The local runner's intensity was zero: contrastive decoding and its plausibility mask were disabled. Complete rendered prompts were checked without truncation against a 4,096-token context limit. This is the full model-and-editing workflow's observation, not a skill-only effect, an attribution to one stage, or a reproduction of CoPA or the AuthorMist paper. No model weights, generator implementation or supported rewriting backend is added to the skill by this study.

## Why confirmation stopped

The two synthetic cases were frozen before the first screening scan and released only after successful fresh verification. They are now retired and their complete contracts are public in [confirmation-retired.json](sources/confirmation-retired.json). The original custodian and later packet preparer were excluded from blind writing and judging. Generation settings and the two editor stages were frozen before confirmation, with no post-review repairs or retries.

| Retired case | Baseline / candidate words | Exact masked quality result | Detector metrics |
| --- | ---: | --- | --- |
| Fictional museum visitor notice | 144 / 162 | Both factually correct; baseline more direct and natural | Unmeasured |
| Fictional game quick-start guide | 142 / 146 | Both factually correct; baseline clearer, with shorter steps | Unmeasured |

The [confirmation review and decoded labels](reviews/confirmation.json) preserve all four exact-text judgments. All 24 required claims passed, but both candidate comparisons failed the no-readability-regression gate. The organization stage moved and grouped existing sentences without wording substitutions. In the game guide, reducing twelve numbered entries to five removes seven list labels; it does not remove seven words of rule content. All four answers were entered into prepared editors, but no scan action followed the failed quality review. Their detector values are **null**, and confirmation contributed zero observations.

## Retained failures and provenance

All [forty method-final answers](answers/screening) remain public, including unscanned quality failures and no-ops. Available screening reviews include their masked verdicts and decoded mappings. The final r19 translation changed an uncommitted rollout date into an unconfirmed date; that fidelity failure was retained without repair or scanning. The r15 join stage saw original prose contrary to its prepared input restriction; it remains an excluded execution deviation. No-op methods do not receive invented detector results.

One derived screening decision was wrong: event 141 prematurely hardcoded a no-gain result. The native r20 business receipt was already correct. Append-only correction **142** explicitly superseded that derived decision with the receipt's 0 / 0 / 100 result; the original incorrect event remains in the private history. This export derives all observation metrics from completed native receipts and records that correction separately. The source results snapshot covers event 175; event **176** closes the batch with failed confirmation and no promotion.

The [export manifest](export-manifest.json) identifies exact copies and sanitized metadata. All 24 observations link exact reviewed answer, submitted text and effective editor text. Submission removed exactly one terminal LF; the editor added exactly three LF, and the pre/post scan editor bytes were identical. These representations are preserved byte-for-byte. This batch used its frozen native receipt validation; the packaged strict plain-text receipt checker does not support this editor transformation. Three browser transport timeouts were reconciled without unresolved scans or duplicate submissions.

Full [development source contracts](sources/development.json), the [source notes](sources/development-notes.txt), retired confirmation contracts, exact frozen workflow entrypoints, selected raw/repair stages and relevant reviews are included. Frozen `.txt` entrypoints are archival snapshots, not separate installable skills; their reference links describe the original environment. Private account UI, screenshots, document identifiers, internal agent identifiers, execution paths, and the full event history are omitted. Other intermediate attempts and the separate four-output, quality-failed decoder pilot remain private. No failed method is omitted from the twenty-attempt denominator.

These are saved operator observations, not authenticated service exports or independent remeasurement. The source audits checked the screening receipts and fresh verification separately. Operational separation on a shared filesystem cannot prove undeclared reads impossible. All seventeen individual frozen incumbent files matched their recorded installed versions, although the original aggregate-hash serialization could not be reproduced; pre-existing untracked repository files were not hashed at the start. Large-writer backend settings, usage and monetary costs are unavailable. The study does not isolate the source of the business reduction, establish statistical significance, or demonstrate transfer to other detectors or writing formats.
