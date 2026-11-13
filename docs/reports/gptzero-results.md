# GPTZero experiment results

This is a results record of logged GPTZero Model 5.0b (free plan) scans from the calibration batch, the Wood to Water tests, and Stages 1–15. It is not a method for passing GPTZero. Figures are taken from the scan logs and are shown without rounding. Where a log field is missing, the table says “not logged”. Times are in Europe/London. The last scan in the log is 13 Nov 2026, about 03:56 Europe/London.

Companion data: [data/gptzero-scans.csv](data/gptzero-scans.csv) (114 scans; accounts redacted; no source-text bodies, no document URLs, no credentials).

## Scope

**Not a general GPTZero bypass.** No repeatable method has been shown to work across three or more different emails. Several low AI scores still depend on invented details, on a single email, or on a scan mode that may not match earlier batches.

Two comparability notes apply throughout. The Stage 14 and Stage 15 panels were labelled Advanced even though the logged free account had 0 advanced scans left, so those scores may not be exactly comparable with earlier Basic batches. The 14% blender text (b3; 13% on rescan) still contains an invented address and invented model numbers, which a real email cannot use.

All listed customer-service emails except the Wood to Water chaser are synthetic test scenarios. Wood to Water scores are included, but the source texts are withheld because they contain a real retailer contact name and order number.

## Progress

| Measure | Value | Note |
| --- | --- | --- |
| GPTZero scans in the logs | 114 | Stage 11 had no scans (0 of 160 samples were fact-complete) |
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

Kettle 13% is Stage 8 f1 and its Stage 9 Basic rescan (Sue Hall, dates folded in). Stage 12 e01-add later scored 22% on the same scenario. Jacket has no fact-complete result below 100%; the unedited raw scored 18%, and the Stage 14 address tests scored 29% and 38%, but those texts are not fact-complete. Blender 13% in the middle column is b3-rescan, which still has the invented address and both NC-350W model numbers; b4, with the address replaced but the model numbers kept, scored 49%. The first fact-complete blender with no invented details, b5, scored 100%, and Stage 15 c1 and c2 also scored 100%. Lamp never moved off 100%, and its raw text already scored 100% and included leaked template advice. Wood to Water v5 scored 3% on an Advanced scan; the original and v1–v4, all 100%, were scanned before the free Basic option disappeared, so the modes are not the same. Wrong colour 30% is the Stage 2 stitched candidate e10-halo; the later fact-conditioned edit e10-r2 scored 100%.

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

## Open hypotheses

These are recorded as hypotheses, not as findings.

- GPTZero treats stock LLM-style persona names, such as Helen, as an AI signal. This is how [PR #9](https://github.com/dexhunter/anti-detection-writing-skill/pull/9) states it, after the kettle name tests.
- Removing the base model's idiosyncratic or rambling content removes the human signal. This was noted after the Stage 10 deletion flips, and it is not treated as established cause.
- A fact-neutral block of the same shape can stand in for an invented address without flipping the score. Stage 14 b1 (39%) and b4 (49%) are consistent with that on the blender email when invented model numbers remain; b5 (100%) and Stage 15 c1 and c2 (100%) are not, once those model numbers are also removed.
- Why any particular reduction happened, including Wood to Water v5 at 3%, is not established by these records.

## Every recorded scan

114 scans. Scan level is normalised to basic, advanced, or unknown. Unknown includes logs with no scan-level field, Stage 1 s1-01 (logged as advanced, with the page later showing basic), Stage 10 (no scanType in the URL; the panel showed Advanced Scan and 0 advanced left), calibration scans (the log notes 0 advanced scans left and sentence highlighting, but has no scan-level column), and Wood to Water original plus v1–v4 (scanned before the free Basic option disappeared).

Exact timestamps are in the CSV and are not repeated in the table below. The account column is “not logged” on every row. The Stage 15 note's “free account A” is only a redacted label in this report; it is not a value in the CSV. Mixed % is 0 wherever it was logged, and is “not logged” for the ten Wood to Water texts that scored 100% AI; v5 mixed was 0.

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

## Sources

- `/workspace/iterations/log.md`
- `/workspace/baseexp/stage1` through `stage15` scan-log.csv, README, and edit-log files (Stage 11 has no scan log)
- `/workspace/calib/scan-log.csv`
- `/workspace/gptzero-w2w/receipt-5.0b-redacted.json` (scores only; texts withheld)
- [PR #9](https://github.com/dexhunter/anti-detection-writing-skill/pull/9)
