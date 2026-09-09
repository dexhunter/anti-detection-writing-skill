# Full-article model transfer and adaptive recovery

Two local generations failed to produce an eligible full article. A later, separately declared recovery repaired the first draft retained from the native run. The independent judge passed that repaired article on facts and suitability but preferred the fixed control on readability. The recovery therefore failed its required preference gate and closed without detector scans. There was no publication, method promotion or confirmation unlock.

This September 9, 2026 development diagnostic used one 541-word source article and the pinned `authormist/authormist-originality` revision `2866bc928850ef4910d24ef5a9179740fab72e22`. It is outside the formal skill-method rounds. It is not a test of the unmodified packaged skill, a paper reproduction or evidence of detector improvement. Any later windowed experiment is separate and cannot change these outcomes.

| Step | Retained output | Outcome |
| --- | --- | --- |
| Custom paired-context decoder | 750 tokens, 425 words | Stopped at the time cap; the factual editor rejected bounded repair because it would require reconstruction. |
| Native generation | 853 tokens, 630 words | Native sampling raised an invalid-probability exception on call 854; no EOS token was emitted. |
| Adaptive extraction and factual repair | Fixed first draft: 479 words; Stage B: 519 words | Exact extraction plus 33 recorded local factual/grammar/format edits, including the final newline. |
| Separate flow pass and masked review | Stage C: 529 words; control: 538 words | Both passed quality review; the judge preferred the control, so the recovery failed its preference gate. |

## What changed

The [custom method](custom/method.json) supplied the complete source and claim contract in paired JSON/chat prompts. It used temperature 1 and CPU multinomial without top-k, top-p or repetition penalties. Intensity was zero, which disables the contrast and plausibility mask. The [native method](native/method.json) used a 790-token plain-source prompt and the pinned sampling configuration: temperature 0.7, top-k 20, top-p 0.8 and repetition penalty 1.05. Both used bfloat16 MPS SDPA and a 1,024-token output allowance. The native settings differ from the published example, and the source exceeds its preferred 100–500-word range. The prompt, sampling and runtime changes are bundled; no component effect is isolated.

The full native continuation is retained. A unique transition into a second draft follows its first caption. The [479-word first article](recovery/first-article-exact.txt) and [151-word removed tail](recovery/removed-tail-exact.txt) concatenate byte-for-byte to [the 630-word raw output](native/raw.txt). The recovery protocol was recorded before its edits and final review. It allowed local factual/grammar repair, then one separate movement/continuity pass, with all 18 claims, seven exact literals and complete title/body/caption preserved within 600 words. It prohibited blanket reconstruction, a second factual repair and post-review editing.

The [Stage B ledger](recovery/stage-b/edit-ledger.json) repairs material errors, including broken commands and URLs, a reversed rewriting-benefit negation and the missing zero-of-fifteen result. Its 33 entries replay exactly; all 22 paragraph positions remain, with 391 of 479 input words unchanged in order. The editor disclosed reading an installed skill evidence reference containing old aggregate detector results, including historical article-scan summaries. Current exact-candidate outcomes remained unseen, but this was not a context with zero historical score exposure.

The [Stage C ledger](recovery/stage-c/operation-ledger.json) records one intact prerequisite move, six local wording changes and three presentation changes. Its listed join describes the paragraph split within that same move. Both ledgers replay to the saved texts, and both claim maps have exact spans for all 18 claims and all seven literals. The [masked review](quality/review.md) passed [A](quality/A.txt), the candidate, and [B](quality/B.txt), the control, but preferred B for reader usefulness and readability. Factual passage did not satisfy the separate preference gate; [the recovery outcome](recovery/outcome.json) retains that failure.

## Runtime and evidence limits

| Run | Model load | Generation or probe work | Outer process |
| --- | ---: | ---: | ---: |
| Custom | 26.273 s | 300.270 s | 331.499 s |
| Native | 24.039 s | 135.309 s | 176.018 s |
| Synthetic probe | No model loaded | 1.176 s | 2.213 s |

These intervals overlap and should not be added. The custom run slightly exceeded its configured 300-second generation cap because the check occurs between iterations. Both outer processes exited 0 after saving their evidence; their generation and quality outcomes remain failures. Full Stage B, Stage C and judge runtimes and model usage/cost receipts are unavailable. Stage C has a 94.664596-second recorded timestamp interval, not a measured full task duration. The local generations incurred no cloud model charge; local compute cost was not measured. Unknown costs remain null.

The synthetic probe checked six key/value lengths using one seeded, one-query attention shape. No compared tensor was nonfinite and no absolute error exceeded 0.01; maximum MPS SDPA error was 0.000766069 and repeat calls matched. It used synthetic tensors, not model weights or real activations. It neither proves whole-model MPS correctness nor establishes an MPS/SDPA defect. The native exception does not identify which invalid condition occurred or its cause, and it does not explain the custom output failure. See [the probe summary](runtime-check/summary.json).

The original frozen native protocol includes EOS IDs but does not explicitly require EOS for eligibility. A stricter pre-run instruction is not retained. The exception and absence of EOS are verified; the later recovery protocol describes a separate artifact evaluation. Its preserved wording about an earlier EOS gate is not independent evidence that the earlier gate was predeclared.

No detector scans were performed for these trials or the recovery. All new outcomes are null. Historical confidence values within the article and its claim inventory are required source facts from earlier studies, not scores for this article. No detector benefit, authorship conclusion or generalization follows from this one development case.

## Files and provenance

[results.json](results.json) records the closed outcomes, timings and unavailable costs. [process-audit.json](process-audit.json) summarizes the independent source-process audit and its caveats. The original article, both full failed raw outputs, all exact prompts, fixed extraction, B/C texts, replay ledgers, claim maps and neutral review texts are retained in this directory.

[export-manifest.json](export-manifest.json) lists every export file except itself, its SHA-256, its copy/sanitization/summary status and private-source hashes. Exact-copy entries preserve source bytes. Sanitized records omit local paths, task identities and browser/account verification metadata; source article text and reviewed A/B bytes remain unchanged. The review retains the original packet hashes, while [the public packet manifest](quality/packet-manifest.json) records any export differences. No account UI, credentials, weights or sealed data is included.

This export was prepared by the source-process auditor and subsequently passed a separate export review of its original 44-file snapshot. The source-process audit and article review serve different purposes from that export check.
