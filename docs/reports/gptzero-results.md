# GPTZero experiment results

This is a results record of logged GPTZero Model 5.0b (free plan) scans from the calibration batch, the Wood to Water tests, Stages 1–15, and Stages 22–25. It is not a method for passing GPTZero. Figures are taken from the scan logs and are shown without rounding. Where a log field is missing, the table says “not logged”. Times for the Stages 1–15 log are in Europe/London. The last scan in that log is 13 Nov 2026, about 03:56 Europe/London. Stage 16, later the same day, is a separate note: [stage-16-pot-handle.md](stage-16-pot-handle.md). Those scans are not in the CSV. Stages 22–25 were scanned on 16 Nov 2026. No clock time was logged for them.

Companion data: [data/gptzero-scans.csv](data/gptzero-scans.csv) (133 scans; accounts redacted; no source-text bodies, no document URLs, no credentials). The first 114 rows are the calibration batch, Wood to Water, and Stages 1–15. Nineteen further rows are the Stage 24 and Stage 25 scans that have a per-text score. Stages 22 and 23 are aggregates in the narrative below (21 scans and 9 scans, all 100% AI) and have no CSV rows. The record for those two stages is the count and the uniform result, not a per-text table.

## Scope

**Not a general GPTZero bypass.** No repeatable method has been shown to work across three or more different emails. Several low AI scores still depend on invented details, on a single email, or on a scan mode that may not match earlier batches.

Two comparability notes apply throughout. The Stage 14 and Stage 15 panels were labelled Advanced even though the logged free account had 0 advanced scans left, so those scores may not be exactly comparable with earlier Basic batches. The 14% blender text (b3; 13% on rescan) still contains an invented address and invented model numbers, which a real email cannot use.

Stages 22–25 used Basic view, file upload, one scan per file, on 16 Nov 2026, Model 5.0b, free plan. The account label in this report is free test account C. It is not an email address and it is not a CSV value. Mixed and human percentages, and clock times, were not logged. The Stage 24 engineer record arm is 84 words, so the under-100-words caveat applies to that one text. These are small samples, single scans, and one detector version.

All listed customer-service emails except the Wood to Water chaser are synthetic test scenarios. Wood to Water scores are included, but the source texts are withheld because they contain a real retailer contact name and order number.

## Progress

| Measure | Value | Note |
| --- | --- | --- |
| GPTZero scans in the CSV | 133 | 114 through Stage 15; 19 per-text rows for Stages 24–25. Stage 11 had no scans (0 of 160 samples were fact-complete). Stages 22–23 (30 scans, all 100% AI) are narrative aggregates and are not rows. Stage 16 is not in the CSV. |
| Best kettle fact-complete AI % | 13% | Stage 8 f1 and Stage 9 Basic rescan; one email |
| Best blender with no invented details | 100% | Stage 14 b5 and Stage 15 c1, c2; fact-complete |
| Wood to Water v5 AI % | 3% | Advanced scan; one email; modes differ from v1–v4 |

Starting scores below are the Calib synthetic baselines, or the Wood to Water original. “Best fact-complete” may still contain invented details. “Best with no invented details” keeps only texts with no invented address or model numbers. Lower is a lower logged AI %.

| Email | Starting AI % | Best fact-complete AI % | Best with no invented details |
| --- | ---: | ---: | ---: |
| Kettle | 100 | 13 | 13 |
| Jacket | 100 | 100 | 100 |
| Blender | 100 | 13 | 100 |
| Lamp | 100 | 100 | 100 |
| Wood to Water | 100 | 3 | 3 |
| Wrong colour | 100 | 30 | 30 |

**[evidence]** Freshly written or re-polished natural text, record-style framing, author-style conditioning and off-the-shelf humanizer models did not lower GPTZero 5.0b scores on fact-complete texts that already scored 100% (Stages 22–25). The only edits that have kept a score low are minimal single edits to a text that already scores human. These are small samples, single scans, and one detector version. The scan record is [Stages 22–25](#stages-22-25).

Kettle 13% is Stage 8 f1 and its Stage 9 Basic rescan (Sue Hall, dates folded in). Stage 12 e01-add later scored 22% on the same scenario. Jacket has no fact-complete result below 100%; the unedited raw scored 18%, and the Stage 14 address tests scored 29% and 38%, but those texts are not fact-complete. Stage 25 humanizer rewrites of that email scored 47 and 48. That step does not record a fact check, and the same-session baseline rescan was 100. Blender 13% in the middle column is b3-rescan, which still has the invented address and both NC-350W model numbers; b4, with the address replaced but the model numbers kept, scored 49%. The first fact-complete blender with no invented details, b5, scored 100%, and Stage 15 c1 and c2 also scored 100%. Lamp never moved off 100%, and its raw text already scored 100% and included leaked template advice. Wood to Water v5 scored 3% on an Advanced scan; the original and v1–v4, all 100%, were scanned before the free Basic option disappeared, so the modes are not the same. Wrong colour 30% is the Stage 2 stitched candidate e10-halo; the later fact-conditioned edit e10-r2 scored 100%.

## Confirmed findings

Each point is tied to named scans. Results seen on only one email are marked as such. These are not a general method for passing GPTZero.

1. A standalone date sentence flipped the kettle control from 4% AI (Stage 6 v00; also Stage 4 e01-del at 4% on Basic and on Advanced) to 100% AI (Stage 6 v01). Folding the same dates into an existing sentence stayed lower: Stage 7 d1 31%, d2 17%. Observed on the kettle email only.

2. The name Helen, or Helen Cartwright, scored 100% AI wherever it was added on the kettle email: Stage 6 v04; Stage 7 n1, n2, combo-n1 and combo-n2; Stage 8 f2 (Helen) and f3 (Helen Cartwright). On the same fact-complete body, Sue Hall scored 13% (Stage 8 f1, Advanced) and 13% again (Stage 9 rescan, Basic). The no-name version f0 scored 52%, but it was uploaded rather than pasted, so it is not like-for-like with the other Stage 8 scans. A stock persona name as an AI signal remains a hypothesis, not a finding. A real sender's name is not changed to chase a score.

3. The kettle recipe did not generalise. Stage 9 used the same folded-facts, plain-name recipe on three other emails: jacket (Kate Ward) 100%, lamp (Ann Price) 100%, blender (Ian Brooks) 100%.

4. Deletion-only edits flipped two of three human-scoring raw samples to 100% AI: jacket e04-raw 18% to e04-del 100% (Stage 10); blender e07-raw 1% to e07-del 100% (Stage 4; 85 words, under-100-words warning). The kettle was the exception: e01-raw 0% to e01-del 4%. The lamp raw, e05-raw, was already 100% and included 89 words of leaked template advice.

5. On the blender raw, deleting the invented address was the single Stage 13 edit that flipped the score from 2% (v00) to 100% (v02). The other single edits stayed lower: model numbers deleted 3%, contradiction fix 0%, sign-off changed to Ian Brooks 40% (flagged uncertain), countertop and date 5%, fault details 9%, refund line 10%. Adding those facts, on this email, did not itself cause the flip.

6. Address deletion is not a universal flip. On the jacket raw (18% AI), deleting the address block scored 29% (Stage 14 k1) and replacing it scored 38% (k2), both still on the human side of the earlier raw.

7. On the blender email, keeping a line in the original address slot mattered in the Stage 14 tests: b1, same slot filled with the existing order number, scored 39%; b2, address deleted and the order number moved to the greeting, scored 100%. b3, address kept plus the safe additions, scored 14%, and 13% on rescan. These Stage 14 scores carry the Advanced-label caveat above.

8. So far, the human-leaning blender scores depend on keeping invented details, and no fact-complete version with no invented details has passed. b3 and b3-rescan (14%, then 13%) still contain the invented address and both NC-350W model numbers. b4, which is b3 with the address replaced by the order number and the model numbers kept, scored 49% AI / 51% human. The scan log records no flags for b4; the parent confirmed that GPTZero called this result uncertain but likely human. b5, which is b4 with NC-350W also removed and is the first version with no invented details, scored 100% AI. Observed on this blender email, in the Stage 14 panel, only, until Stage 15 repeated the 100% result.

9. Raw unedited OLMo-2-7B base emails can score as human, but they are not fact-complete skill outputs. Stage 1 s1-01, s1-02 and s1-03 all scored 0% AI. Stage 4 e01-raw scored 0% and e07-raw scored 1%; e10-raw scored 100%. Stage 10 e04-raw scored 18%.

10. Stitching or editing facts back into base-model text often returned the score to 100% AI. Stage 2: 5 of 6 fact-passing stitched candidates scored 100%; e10-halo scored 30%. Stage 3 e01-r2 and e10-r2 scored 100%. Stage 5 c01, c05, c04 and c02 all scored 100%; c03 and c06 were not scanned. A later Advanced rescan of e01-del stayed at 4%, so scan mode does not explain the Stage 5 kettle flip.

11. Fact-conditioned generation with the facts in the prompt produced 0 fact-complete emails out of 160 Stage 11 samples. There were no GPTZero scans in that stage.

12. In the calibration batch, all 15 public-domain human controls scored 0% AI / 100% human, and all 20 synthetic baselines and rewrites scored 100% AI, including the five nominalised rewrites. The formal, passive style that scored 3% on Wood to Water v5 did not move any of those five calibration emails off 100%.

13. On the Wood to Water chaser, the original and 9 of 10 rewrites scored 100% AI. v5, the formal, passive, nominalised rewrite, scored 3% AI / 97% human. The receipt records that v5–v10 used Advanced AI Scan, that the original and v1–v4 were scanned before the free Basic option disappeared, and that mixed and human percentages were not separately recorded for the 100% texts. This is one email. The batch notes describe v5 as the least like the writer's own voice and say not to make it a rule without a fresh comparable confirmation case.

## Stage 15 negative result

Stage 15 tested whether the clean, fact-complete blender email (b5, 100% AI, no invented details) could be rescued if OLMo-2-7B base wrote the wording in the two slots that earlier edits had filled, so the agent side only deleted. Two independent-review PASS candidates were scanned on GPTZero 5.0b, file upload, panel labelled Advanced (0 advanced left), free account A, 13 Nov 2026, about 03:55–03:56 Europe/London:

| File | Words | Edit | AI % | Human % | Notes |
| --- | ---: | --- | ---: | ---: | --- |
| c1 | 123 | b5 with a base-model fill in the s2 slot (` 2026.`); rest of the text is b5 word-for-word | 100 | 0 | highly confident AI generated |
| c2 | 118 | seed 15006 sentences replace b5's first two sentences; no invented details | 100 | 0 | highly confident AI generated |

Both stayed at 100% AI, like b5. Letting the base model write the replacement text did not rescue the clean blender email. Together with Stages 13–14, the human-leaning blender scores so far need invented specifics (address, model number). Inventing facts is off-limits for the skill; those earlier human-leaning scores are not a usable method.

<a id="stages-22-25"></a>

## Stages 22–25 negative results

Scanned 16 Nov 2026. GPTZero Model 5.0b, free plan, Basic view, file upload, one scan per file, account labelled free test account C. No email address is recorded. Mixed % and human % were not logged. Clock times were not logged. File ids in the CSV for these stages are scan labels; disk filenames were not logged. These are small samples, single scans, and one detector version. They are not a method for passing GPTZero.

### Stage 22

21 scans. The texts are private, credential-dense recommendation-letter paragraphs (not published). No author, subject, or letter wording is recorded. The arms were applied to three paragraphs that already scored 100% AI: recommender voice; uneven sentence length; plain verbs and fewer nominalizations (after Reinhart et al., PNAS 2025); a rewrite with the pstack `unslop` skill; and a rewrite with the pstack `technical-writing` skill. The same session included controls and two full letters. All 21 scans scored 100% AI. Clear negative. Per-text file names and separate scores were not logged, so Stage 22 has no CSV rows.

### Stage 23

9 scans. The texts are private, credential-dense recommendation-letter paragraphs (not published). No author, subject, or letter wording is recorded. The arms feature-matched the 100% paragraphs to the same letter's 0%-scoring paragraphs (shorter sentences, person subjects, split facts) and conditioned on the author's public writing. That conditioning is an idea from arXiv 2505.14608. All 9 scans scored 100% AI. Per-text file names and separate scores were not logged, so Stage 23 has no CSV rows.

Across Stages 22–23, 30 natural, fact-complete variants scored 100% AI. Natural polishing does not move GPTZero on credential-dense paragraphs that already score 100%.

### Stage 24

Fully synthetic, fictional recommendation paragraphs: an engineer, a PhD student, and a food-bank coordinator. I is typical interpretive letter framing. R keeps the same facts and opinions as plain record sentences, with glosses removed.

| Persona | I AI % | R AI % | Note on R |
| --- | ---: | ---: | --- |
| Engineer | 100 | 100 | 84 words, under 100, less reliable |
| PhD student | 100 | 100 | Labelled Possible AI Paraphrasing |
| Food-bank coordinator | 100 | 100 | |

0 of 3 moved. `check_facts.py` marked two pairs `facts_preserved`. One pair differs only because the checker reads a sentence-initial "Since" followed by a capitalised name as a name. That pair was hand-checked. The record does not say which persona that pair was. These six scores are CSV rows.

### Stage 25

Off-the-shelf humanizer models, on the synthetic calibration emails e01–e09 from earlier stages. The email names in the scan table are the names already used for those ids in this report.

Eight open Hugging Face detectors, scored on 122 texts that GPTZero 5.0b had already scored, do not track GPTZero. The best was HC3-roberta, Spearman 0.20, AUC 0.61. tropa-mini was −0.01 / 0.50. desklib was −0.08 / 0.44. Binoculars (Qwen 1.5B) was −0.18 / 0.38. Some separate public-domain human text from raw AI text perfectly (AUC 1.00). That is a different task. Coefficients for the rest of the eight were not in the record, so they are not filled in.

The humanizers ran on Modal L4 GPUs via llama.cpp (Q8 GGUF): Smaug-Humanizer, jialinyyzz/humanizer, and authormist-originality. AuthorMist was unusable: 0 of 40 outputs were usable, so it has no scan row.

Step 1 scans: e01 Smaug 100; e04 jialin 47; e07 Smaug 100; e01 jialin 100; e04 Smaug 48; e01 baseline control 100. Step 1 does not record a fact check. Step 2: best-of-24 fact-checked Smaug rewrites of e02, e03, e05, e06, e08, and e09, all 100% AI. e05, e06, e08, and e09 were labelled Possible AI Paraphrasing. The same-session e04 baseline rescan was 100, so the e04 drop (47 and 48, from two different models) is real and specific to that one text. Overall, humanizers moved 1 of 7 emails. GPTZero has a paraphrase detector that flags humanizer output. In this batch that label was recorded on the Stage 24 PhD-student record arm and on the step-2 rewrites of e05, e06, e08, and e09.

Because the open detectors do not track GPTZero, training a rephraser (LoRA) against them is unlikely to transfer. No training pilot was run. Total GPU cost was about $0.37.

## Open hypotheses

These are recorded as hypotheses, not as findings.

- GPTZero treats stock LLM-style persona names, such as Helen, as an AI signal. This is how [PR #9](https://github.com/dexhunter/anti-detection-writing-skill/pull/9) states it, after the kettle name tests.
- Removing the base model's idiosyncratic or rambling content removes the human signal. This was noted after the Stage 10 deletion flips, and it is not treated as established cause.
- A fact-neutral block of the same shape can stand in for an invented address without flipping the score. Stage 14 b1 (39%) and b4 (49%) are consistent with that on the blender email when invented model numbers remain; b5 (100%) and Stage 15 c1 and c2 (100%) are not, once those model numbers are also removed.
- Why any particular reduction happened, including Wood to Water v5 at 3%, is not established by these records.

## Every recorded scan

133 scans, matching the CSV. Scan level is normalised to basic, advanced, or unknown. Unknown includes logs with no scan-level field, Stage 1 s1-01 (logged as advanced, with the page later showing basic), Stage 10 (no scanType in the URL; the panel showed Advanced Scan and 0 advanced left), calibration scans (the log notes 0 advanced scans left and sentence highlighting, but has no scan-level column), and Wood to Water original plus v1–v4 (scanned before the free Basic option disappeared). Stages 22 and 23 are not in this table.

Exact timestamps are in the CSV and are not repeated in the table below. The account column is “not logged” on every row. The Stage 15 note's “free account A”, and the Stages 22–25 label “free test account C”, are redacted labels in this report; they are not values in the CSV. Mixed % is 0 wherever it was logged, and is “not logged” for the ten Wood to Water texts that scored 100% AI and for every Stage 24 and Stage 25 row; v5 mixed was 0. Human % for those Stage 24 and Stage 25 rows is “not logged”.

| Stage | Email | File | Edit | AI % | Human % | Level |
| --- | --- | --- | --- | ---: | ---: | --- |
| Calib | Human control (h13) | `h13` | Verbatim public-domain paragraph (The Thirty-Nine Steps) | 0 | 100 | unknown |
| Calib | Human control (h01) | `h01` | Verbatim public-domain paragraph (Letters of Jane Austen) | 0 | 100 | unknown |
| Calib | Human control (h07) | `h07` | Verbatim public-domain paragraph (Letters of a Woman Homesteader) | 0 | 100 | unknown |
| Calib | Blender (e07) | `e07-baseline` | Plain AI draft (synthetic baseline) | 100 | 0 | unknown |
| Calib | Blender (e07) | `e07-natural` | Natural rewrite, skill style | 100 | 0 | unknown |
| Calib | Blender (e07) | `e07-nominalised` | Formal, passive, nominalised rewrite | 100 | 0 | unknown |
| Calib | Human control (h14) | `h14` | Verbatim public-domain paragraph (My Ántonia) | 0 | 100 | unknown |
| Calib | Human control (h12) | `h12` | Verbatim public-domain paragraph (The Diary of a Nobody) | 0 | 100 | unknown |
| Calib | Kettle (e01) | `e01-baseline` | Plain AI draft (synthetic baseline) | 100 | 0 | unknown |
| Calib | Kettle (e01) | `e01-natural` | Natural rewrite, skill style | 100 | 0 | unknown |
| Calib | Kettle (e01) | `e01-nominalised` | Formal, passive, nominalised rewrite | 100 | 0 | unknown |
| Calib | Human control (h15) | `h15` | Verbatim public-domain paragraph (Ethan Frome) | 0 | 100 | unknown |
| Calib | Human control (h10) | `h10` | Verbatim public-domain paragraph (Mark Twain's Letters) | 0 | 100 | unknown |
| Calib | Double charge (e03) | `e03-baseline` | Plain AI draft (synthetic baseline) | 100 | 0 | unknown |
| Calib | Double charge (e03) | `e03-natural` | Natural rewrite, skill style | 100 | 0 | unknown |
| Calib | Double charge (e03) | `e03-nominalised` | Formal, passive, nominalised rewrite | 100 | 0 | unknown |
| Calib | Human control (h08) | `h08` | Verbatim public-domain paragraph (Adams letters) | 0 | 100 | unknown |
| Calib | Human control (h09) | `h09` | Verbatim public-domain paragraph (Dickens letters) | 0 | 100 | unknown |
| Calib | Lamp (e05) | `e05-baseline` | Plain AI draft (synthetic baseline) | 100 | 0 | unknown |
| Calib | Lamp (e05) | `e05-natural` | Natural rewrite, skill style | 100 | 0 | unknown |
| Calib | Lamp (e05) | `e05-nominalised` | Formal, passive, nominalised rewrite | 100 | 0 | unknown |
| Calib | Human control (h02) | `h02` | Verbatim public-domain paragraph (Darwin letters) | 0 | 100 | unknown |
| Calib | Human control (h04) | `h04` | Verbatim public-domain paragraph (Vailima Letters) | 0 | 100 | unknown |
| Calib | Missing delivery (e08) | `e08-baseline` | Plain AI draft (synthetic baseline) | 100 | 0 | unknown |
| Calib | Missing delivery (e08) | `e08-natural` | Natural rewrite, skill style | 100 | 0 | unknown |
| Calib | Missing delivery (e08) | `e08-nominalised` | Formal, passive, nominalised rewrite | 100 | 0 | unknown |
| Calib | Human control (h03) | `h03` | Verbatim public-domain paragraph (Keats letters) | 0 | 100 | unknown |
| Calib | Human control (h05) | `h05` | Verbatim public-domain paragraph (Lincoln papers) | 0 | 100 | unknown |
| Calib | Human control (h06) | `h06` | Verbatim public-domain paragraph (Chesterfield letters) | 0 | 100 | unknown |
| Calib | Human control (h11) | `h11` | Verbatim public-domain paragraph (Lady Mary Wortley Montagu letters) | 0 | 100 | unknown |
| Calib | Boots not received (e02) | `e02-baseline` | Plain AI draft (synthetic baseline) | 100 | 0 | unknown |
| Calib | Jacket (e04) | `e04-baseline` | Plain AI draft (synthetic baseline) | 100 | 0 | unknown |
| Calib | Charge after cancellation (e06) | `e06-baseline` | Plain AI draft (synthetic baseline) | 100 | 0 | unknown |
| Calib | Pre-sale price (e09) | `e09-baseline` | Plain AI draft (synthetic baseline) | 100 | 0 | unknown |
| Calib | Wrong colour (e10) | `e10-baseline` | Plain AI draft (synthetic baseline) | 100 | 0 | unknown |
| Wood to Water | Wood to Water chaser | `original` | Real chaser as written | 100 | not logged | unknown |
| Wood to Water | Wood to Water chaser | `v1` | Casual-polite rewrite | 100 | not logged | unknown |
| Wood to Water | Wood to Water chaser | `v2` | Recap rewrite | 100 | not logged | unknown |
| Wood to Water | Wood to Water chaser | `v3` | Me again rewrite | 100 | not logged | unknown |
| Wood to Water | Wood to Water chaser | `v4` | Choppy fragments rewrite | 100 | not logged | unknown |
| Wood to Water | Wood to Water chaser | `v5` | Formal, passive, nominalised rewrite | 3 | 97 | advanced |
| Wood to Water | Wood to Water chaser | `v6` | One long run-on paragraph | 100 | not logged | advanced |
| Wood to Water | Wood to Water chaser | `v7` | Problem-first order | 100 | not logged | advanced |
| Wood to Water | Wood to Water chaser | `v8` | Annoyed-customer register | 100 | not logged | advanced |
| Wood to Water | Wood to Water chaser | `v9` | Labelled reference block between short paragraphs | 100 | not logged | advanced |
| Wood to Water | Wood to Water chaser | `v10` | Fragments mixed with a terse recap line | 100 | not logged | advanced |
| Stage 1 | Late courier (s1-01) | `s1-01` | Unedited raw OLMo-2-7B base email | 0 | 100 | unknown |
| Stage 1 | Zoom account (s1-02) | `s1-02` | Unedited raw OLMo-2-7B base email | 0 | 100 | advanced |
| Stage 1 | Helicopter (s1-03) | `s1-03` | Unedited raw OLMo-2-7B base email | 0 | 100 | advanced |
| Stage 2 | Kettle (e01) | `e01-halo` | Stitched HALO-lite candidate (fact-passing) | 100 | 0 | unknown |
| Stage 2 | Jacket (e04) | `e04-halo` | Stitched HALO-lite candidate (fact-passing) | 100 | 0 | unknown |
| Stage 2 | Lamp (e05) | `e05-halo` | Stitched HALO-lite candidate (fact-passing) | 100 | 0 | unknown |
| Stage 2 | Blender (e07) | `e07-halo` | Stitched HALO-lite candidate (fact-passing) | 100 | 0 | unknown |
| Stage 2 | Pre-sale price (e09) | `e09-halo` | Stitched HALO-lite candidate (fact-passing) | 100 | 0 | unknown |
| Stage 2 | Wrong colour (e10) | `e10-halo` | Stitched HALO-lite candidate (fact-passing) | 30 | 70 | unknown |
| Stage 2 | Kettle (e01) | `e01-baseline` | Control (synthetic baseline rescan) | 100 | 0 | unknown |
| Stage 2 | Lamp (e05) | `e05-baseline` | Control (synthetic baseline rescan) | 100 | 0 | unknown |
| Stage 3 | Kettle (e01) | `e01-r2` | Fact-conditioned best-of-N sample, deletion-first edits plus fact insertions | 100 | 0 | basic |
| Stage 3 | Wrong colour (e10) | `e10-r2` | Fact-conditioned best-of-N sample, deletion-first edits plus fact insertions | 100 | 0 | basic |
| Stage 4 | Kettle (e01) | `e01-raw` | Unedited fact-conditioned raw sample | 0 | 100 | advanced |
| Stage 4 | Wrong colour (e10) | `e10-raw` | Unedited fact-conditioned raw sample | 100 | 0 | basic |
| Stage 4 | Blender (e07) | `e07-raw` | Unedited fact-conditioned raw sample | 1 | 99 | basic |
| Stage 4 | Kettle (e01) | `e01-del` | Deletion-only (zero insertions) | 4 | 96 | basic |
| Stage 4 | Wrong colour (e10) | `e10-del` | Deletion-only (zero insertions); under-100-words note (99 words) | 100 | 0 | basic |
| Stage 4 | Blender (e07) | `e07-del` | Deletion-only (zero insertions); under-100-words note (85 words) | 100 | 0 | basic |
| Stage 4 | Kettle (e01) | `e01-del-adv` | Rescan of e01-del on Advanced (one accidental double space in the paste) | 4 | 96 | advanced |
| Stage 5 | Kettle (e01) | `c01` | Model-written fact sentences, then deletion-only agent edits | 100 | 0 | advanced |
| Stage 5 | Blender (e07) | `c05` | Model-written fact sentences, then deletion-only agent edits | 100 | 0 | advanced |
| Stage 5 | Lamp (e05) | `c04` | Model-written fact sentences, then deletion-only agent edits | 100 | 0 | advanced |
| Stage 5 | Double charge (e03) | `c02` | Model-written fact sentences, then deletion-only agent edits | 100 | 0 | advanced |
| Stage 6 | Kettle (e01) | `v00.txt` | None (control: unchanged e01-del) | 4 | 96 | advanced |
| Stage 6 | Kettle (e01) | `v01.txt` | Standalone order/delivery date sentence after the salutation | 100 | 0 | advanced |
| Stage 6 | Kettle (e01) | `v02.txt` | Fault qualifiers added after "1 November." | 21 | 79 | advanced |
| Stage 6 | Kettle (e01) | `v04.txt` | Sign-off name "Helen Cartwright" inserted | 100 | 0 | advanced |
| Stage 6 | Kettle (e01) | `v03.txt` | Refund to the original debit card, £34.99, inserted in the ask | 1 | 99 | advanced |
| Stage 7 | Kettle (e01) | `d1.txt` | Dates folded into the existing delivery sentence | 31 | 69 | advanced |
| Stage 7 | Kettle (e01) | `d2.txt` | Dates folded into the order-number sentence | 17 | 83 | advanced |
| Stage 7 | Kettle (e01) | `n1.txt` | Sign-off "Ms Helen Cartwright" | 100 | 0 | advanced |
| Stage 7 | Kettle (e01) | `n2.txt` | "My name is Helen Cartwright and …" in the opening; no sign-off name | 100 | 0 | advanced |
| Stage 7 | Kettle (e01) | `combo-n1.txt` | Folded dates, fault and refund facts, plus "Ms Helen Cartwright" | 100 | 0 | advanced |
| Stage 7 | Kettle (e01) | `combo-n2.txt` | Folded dates, fault and refund facts, plus the name in the body | 100 | 0 | advanced |
| Stage 8 | Kettle (e01) | `f0.txt` | No name anywhere (uploaded as .txt; other Stage 8 scans were pasted) | 52 | 48 | advanced |
| Stage 8 | Kettle (e01) | `f1.txt` | Sign-off "Sue Hall" on a fact-complete body with dates folded in | 13 | 87 | advanced |
| Stage 8 | Kettle (e01) | `f2.txt` | Sign-off "Helen" only | 100 | 0 | advanced |
| Stage 8 | Kettle (e01) | `f3.txt` | Sign-off "Helen Cartwright" | 100 | 0 | advanced |
| Stage 9 | Kettle (e01) | `stage8/f1.txt` | Re-scan of Stage 8 f1 (Sue Hall) | 13 | 87 | basic |
| Stage 9 | Jacket (e04) | `stage9/e04.txt` | Same f1-style recipe; sign-off Kate Ward | 100 | 0 | basic |
| Stage 9 | Lamp (e05) | `stage9/e05.txt` | Same f1-style recipe; sign-off Ann Price | 100 | 0 | basic |
| Stage 9 | Blender (e07) | `stage9/e07.txt` | Same f1-style recipe; sign-off Ian Brooks | 100 | 0 | basic |
| Stage 10 | Jacket (e04) | `e04-raw.txt` | Unedited raw cut_text | 18 | 82 | unknown |
| Stage 10 | Jacket (e04) | `e04-del.txt` | Deletion-only (no facts added) | 100 | 0 | unknown |
| Stage 10 | Lamp (e05) | `e05-raw.txt` | Unedited raw cut_text (includes 89 words of leaked template advice) | 100 | 0 | unknown |
| Stage 10 | Lamp (e05) | `e05-del.txt` | Deletion-only (no facts added); under-100-words warning | 100 | 0 | unknown |
| Stage 12 | Kettle (e01) | `e01-add.txt` | Additive-only from e01-raw; Sue Hall; inserted 14 words, deleted 0 | 22 | 78 | basic |
| Stage 12 | Jacket (e04) | `e04-add.txt` | Additive-first from e04-raw, but 59 words deleted (invented address, return window, C5 envelope); Kate Ward | 100 | 0 | basic |
| Stage 12 | Blender (e07) | `e07-add.txt` | From e07-raw: facts added, and 9 words deleted (both NC-350W numbers, invented address, "and was returned"); Ian Brooks | 100 | 0 | basic |
| Stage 13 | Blender (e07) | `v00.txt` | None (control: unchanged e07-raw) | 2 | 98 | basic |
| Stage 13 | Blender (e07) | `v01.txt` | Invented model numbers deleted | 3 | 97 | basic |
| Stage 13 | Blender (e07) | `v02.txt` | Invented address deleted | 100 | 0 | basic |
| Stage 13 | Blender (e07) | `v03.txt` | Contradiction fix: "was returned" / still-has wording | 0 | 100 | basic |
| Stage 13 | Blender (e07) | `v04.txt` | Sign-off Duncan Lidsey → Ian Brooks | 40 | 60 | basic |
| Stage 13 | Blender (e07) | `v05.txt` | Countertop and 25 October inserted; address kept | 5 | 95 | basic |
| Stage 13 | Blender (e07) | `v06.txt` | Fault details inserted (will not start; cause not known) | 9 | 91 | basic |
| Stage 13 | Blender (e07) | `v07.txt` | Refund to the original payment method inserted | 10 | 90 | basic |
| Stage 14 | Blender (e07) | `b1.txt` | On v00: address replaced in the same slot with ", for order number NB-52044" | 39 | 61 | advanced |
| Stage 14 | Blender (e07) | `b2.txt` | On v00: address deleted; order number appended to the greeting | 100 | 0 | advanced |
| Stage 14 | Blender (e07) | `b3.txt` | Address kept, plus the v03/v05/v06/v07 additions; invented address and NC-350W remain | 14 | 86 | advanced |
| Stage 14 | Jacket (e04) | `k1.txt` | On e04-raw: invented four-line address block deleted | 29 | 71 | advanced |
| Stage 14 | Jacket (e04) | `k2.txt` | On e04-raw: address block replaced with a fact-neutral order-reference of the same shape | 38 | 62 | advanced |
| Stage 14 | Blender (e07) | `b3-rescan` | Re-scan of b3 (control) | 13 | 87 | advanced |
| Stage 14 | Blender (e07) | `b4.txt` | b3 with the address replaced by ", for order number NB-52044"; NC-350W kept | 49 | 51 | advanced |
| Stage 14 | Blender (e07) | `b5.txt` | b4 with invented model number NC-350W also removed; first version with no invented details | 100 | 0 | advanced |
| Stage 15 | Blender (e07) | `c1.txt` | b5 with base-model fill in the s2 slot (" 2026."); rest of text is b5 word-for-word; 123 words | 100 | 0 | advanced |
| Stage 15 | Blender (e07) | `c2.txt` | s1 seed 15006 sentences replace b5's first two sentences; 118 words; no invented details | 100 | 0 | advanced |
| Stage 24 | Fictional recommendation (engineer) | `engineer-I` | Interpretive letter framing (I); fully synthetic | 100 | not logged | basic |
| Stage 24 | Fictional recommendation (engineer) | `engineer-R` | Plain record sentences; same facts and opinions; glosses removed; 84 words, under 100 | 100 | not logged | basic |
| Stage 24 | Fictional recommendation (PhD student) | `phd-student-I` | Interpretive letter framing (I); fully synthetic | 100 | not logged | basic |
| Stage 24 | Fictional recommendation (PhD student) | `phd-student-R` | Plain record sentences; same facts and opinions; glosses removed; Possible AI Paraphrasing | 100 | not logged | basic |
| Stage 24 | Fictional recommendation (food-bank coordinator) | `food-bank-I` | Interpretive letter framing (I); fully synthetic | 100 | not logged | basic |
| Stage 24 | Fictional recommendation (food-bank coordinator) | `food-bank-R` | Plain record sentences; same facts and opinions; glosses removed | 100 | not logged | basic |
| Stage 25 | Kettle (e01) | `e01-smaug` | Step 1 Smaug-Humanizer rewrite | 100 | not logged | basic |
| Stage 25 | Jacket (e04) | `e04-jialin` | Step 1 jialinyyzz/humanizer rewrite | 47 | not logged | basic |
| Stage 25 | Blender (e07) | `e07-smaug` | Step 1 Smaug-Humanizer rewrite | 100 | not logged | basic |
| Stage 25 | Kettle (e01) | `e01-jialin` | Step 1 jialinyyzz/humanizer rewrite | 100 | not logged | basic |
| Stage 25 | Jacket (e04) | `e04-smaug` | Step 1 Smaug-Humanizer rewrite | 48 | not logged | basic |
| Stage 25 | Kettle (e01) | `e01-baseline` | Step 1 baseline control | 100 | not logged | basic |
| Stage 25 | Boots not received (e02) | `e02-smaug` | Step 2 best-of-24 fact-checked Smaug-Humanizer rewrite | 100 | not logged | basic |
| Stage 25 | Double charge (e03) | `e03-smaug` | Step 2 best-of-24 fact-checked Smaug-Humanizer rewrite | 100 | not logged | basic |
| Stage 25 | Lamp (e05) | `e05-smaug` | Step 2 best-of-24 fact-checked Smaug-Humanizer rewrite; Possible AI Paraphrasing | 100 | not logged | basic |
| Stage 25 | Charge after cancellation (e06) | `e06-smaug` | Step 2 best-of-24 fact-checked Smaug-Humanizer rewrite; Possible AI Paraphrasing | 100 | not logged | basic |
| Stage 25 | Missing delivery (e08) | `e08-smaug` | Step 2 best-of-24 fact-checked Smaug-Humanizer rewrite; Possible AI Paraphrasing | 100 | not logged | basic |
| Stage 25 | Pre-sale price (e09) | `e09-smaug` | Step 2 best-of-24 fact-checked Smaug-Humanizer rewrite; Possible AI Paraphrasing | 100 | not logged | basic |
| Stage 25 | Jacket (e04) | `e04-baseline` | Same-session baseline rescan | 100 | not logged | basic |


## What is in the skill

[PR #9](https://github.com/dexhunter/anti-detection-writing-skill/pull/9), titled “Record a preliminary single-fact placement probe”, was merged on 12 Nov 2026, 16:29 Europe/London, as commit `4be38604419aadcdccb1f4d947bb255ecbed5c0b`. It covers the Stage 6–9 kettle tests. The skill also includes a preliminary Stage 10–15 note. Status below is as of this report (13 Nov 2026, Europe/London).

Already in the skill from PR #9:

- Fold dates and other facts into a sentence already in the draft, rather than adding a standalone “Please note…” or date recap.
- Check the recap and sign-off lines first when a requested scan flags a draft.
- Keep every fact, uncertainty and qualification, including the sender's own name. A real sender's name is never changed to lower a score.
- Avoid stock persona names such as Helen in test emails. A stock LLM-style persona name is recorded as a hypothesis, not a finding.
- A deletions-only control is a measurement arm, not the message to send.
- State plainly that date folding and avoiding a stock persona name are not a way to pass GPTZero, and that the 13% score holds for one email.

The preliminary Stage 10–15 note says these probes are not a way to pass GPTZero, and it keeps the rule against inventing a fact:

- Deleting text from a human-scoring raw draft can flip the score to 100% AI: jacket 18% to 100%, blender 1% to 100%; the kettle deletion-only control stayed at 4%.
- On the blender raw, deleting an invented address flipped 2% to 100%. Adding the countertop and date, the fault details, and the refund line stayed at 5–10% AI. Those three logged scores are 5%, 9%, and 10%. That address deletion did not flip the jacket raw (29% after deletion, 38% after a fact-neutral replacement).
- Human-leaning blender scores so far depended on invented details. A fact-complete blender with those details removed scored 100% AI, including two later versions where the base model wrote the replacement wording.

Not in the skill:

- Facts-in-the-prompt generation produced 0 of 160 fact-complete emails, and Stage 11 had no scans. In Stage 12 the only additive-only edit, the kettle, scored 22% AI. The jacket and blender edits in that stage also deleted words and scored 100% AI.
- The Stage 14 blender address-slot contrast is not stated as its own result. b1, with the order number kept in the address slot, scored 39%. b2, with the address deleted and the order number moved to the greeting, scored 100%.
- Wood to Water v5 (3% AI, Advanced, nominalised style) is a single development observation, without making it a rule. It is recorded in this report and in the [limitations guide](../when-it-may-not-help.md), not in the skill.
- Stages 22–25 (16 Nov 2026) stay a negative result. They are recorded here and as a labelled note in the [evidence limits](../../skills/anti-ai-detection-writing-skill/references/evidence.md). They are not a new editing method.

## Gaps in the logs

- Stage 11 has no scan-log.csv, because no fact-complete candidate was kept (0 of 160).
- Stage 5 c03 (jacket) and c06 (wrong colour) were not scanned.
- Account is not logged for the calibration batch, the Wood to Water receipt, or Stages 1–3.
- Scan level is not logged for Stage 2. Stage 3's level is taken from the CSV note column (basic scan), not from a scan_level field. Calibration has no scan-level column. Wood to Water original and v1–v4 have no per-text mode in the receipt.
- Timestamps are missing from the Stage 2, Stage 3 and Stage 5 scan logs. Stage 4, Stage 10 and Stage 15 times are approximate (`about` / history shows date only). Wood to Water is dated 11 Nov 2026 with no time of day. Stage 1's timestamp has no timezone suffix; it is shown here as Europe/London, matching the iterations log.
- For Wood to Water texts that scored 100% AI, the receipt says mixed and human percentages were not separately recorded, so human % is shown as not logged.
- The calibration README still says no GPTZero scan was run. The scan-log.csv in the same directory records 35 scans on 11 Nov 2026, and those are the figures used here.
- The Stage 14 edit-log describes b1, b2, b3, k1 and k2, and was not updated in the file for b4 and b5. Descriptions of b4 and b5 in this report come from the scan log, the later iterations-log note, the parent confirmation, and a direct comparison of the text files (b4 replaces the b3 address with the order-number phrase; b5 also removes both NC-350W mentions).
- Stage 1 s1-02 and s1-03 carried a Text changed - Scan to update footer. Calibration rows also note that footer after the scan. Those footers are recorded in the logs and are not treated as score changes.
- Stages 22 and 23 have no per-text CSV rows. The logged result is 21 scans and 9 scans, each at 100% AI. File names, word counts, mixed %, human %, and clock times for those scans were not in the record used here.
- Stages 24 and 25 have no logged mixed % or human %, and no clock time. The CSV `file` values are scan labels, not logged disk filenames. The only logged word count in Stage 24 is the engineer record arm (84). `check_facts.py` is stage-level for Stage 24: two pairs `facts_preserved`, and one pair differs only because a sentence-initial "Since" plus a capitalised name is read as a name (hand-checked). Which pair was not identified.
- Stage 25 names four of the eight open-detector correlations (HC3-roberta, tropa-mini, desklib, Binoculars). The other coefficients were not in the record. AuthorMist (authormist-originality) produced 0 of 40 usable outputs and was not scanned. Step 1 does not record a fact check. The recorded summary is that humanizers moved 1 of 7 emails. The per-text scores are the rows above, including the e04 scores of 47 and 48 and the same-session baseline rescan at 100.
- No email address is published. The Stages 22–25 account label is free test account C.

## Sources

- `/workspace/iterations/log.md`
- `/workspace/baseexp/stage1` through `stage15` scan-log.csv, README, and edit-log files (Stage 11 has no scan log)
- `/workspace/calib/scan-log.csv`
- `/workspace/gptzero-w2w/receipt-5.0b-redacted.json` (scores only; texts withheld)
- [PR #9](https://github.com/dexhunter/anti-detection-writing-skill/pull/9)
- Stages 22–25: the 16 Nov 2026 scan results recorded in this note (Model 5.0b, free plan, Basic view, file upload, one scan per file). A scan-log path was not supplied with those results.
