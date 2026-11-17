# GPTZero experiment results

This is a results record of logged GPTZero Model 5.0b (free plan) scans from the calibration batch, the Wood to Water tests, Stages 1–15, and Stages 22–31. It is not a method for passing GPTZero. Figures are taken from the scan logs and are shown without rounding. Where a log field is missing, the table says “not logged”. Times for the Stages 1–15 log are in Europe/London. The last scan in that log is 13 Nov 2026, about 03:56 Europe/London. Stage 16, later the same day, is a separate note: [stage-16-pot-handle.md](stage-16-pot-handle.md). Those scans are not in the CSV. Stages 22–29 were scanned on 16 Nov 2026, and Stages 30–31 on 17 Nov 2026. No clock time was logged for them.

Companion data: [data/gptzero-scans.csv](data/gptzero-scans.csv) (162 scans; accounts redacted; no source-text bodies, no document URLs, no credentials). The first 114 rows are the calibration batch, Wood to Water, and Stages 1–15. Seventeen further rows are the Stage 24 and Stage 25 scans that have a per-text score. Thirty-one further rows are the Stage 26, 28, 29, 30, and 31 scans that have a per-text score. Stages 22 and 23 are aggregates in the narrative below (21 scans and 9 scans, all 100% AI) and have no CSV rows. Stage 27’s six scans are also an aggregate (all 100% AI) and have no CSV rows. The record for those stages is the count and the uniform result, not a per-text table.

## Scope

**Not a general GPTZero bypass.** No repeatable method has been shown to work across three or more different emails. Several low AI scores still depend on invented details, on a single email, or on a scan mode that may not match earlier batches.

Two comparability notes apply throughout. The Stage 14 and Stage 15 panels were labelled Advanced even though the logged free account had 0 advanced scans left, so those scores may not be exactly comparable with earlier Basic batches. The 14% blender text (b3; 13% on rescan) still contains an invented address and invented model numbers, which a real email cannot use.

Stages 22–25 were Basic scans on the free plan, Model 5.0b, on 16 Nov 2026. Mixed and human percentages, and clock times, were not in the supplied record. No email address or account name is published. These are small samples, single scans, and one detector version.

Stages 26–31 were Basic scans on the free plan, Model 5.0b, with the score read in Basic view. Stages 26–29 were 16 Nov 2026. Stages 30–31 were 17 Nov 2026. Mixed and human percentages, and clock times, were not in the supplied record. No email address, account name, writer name, or message body is published. Stage 26 used the existing synthetic calibration emails. Stages 28–31 used public Enron corpus emails from the AESLC test split, named by test-row number. These are small samples and one detector version. They are not a method for passing GPTZero. Light edits in Stages 28–31 preserved a human classification only when the starting draft was already human-written. They do not lower the score of text that starts AI-written.

All listed customer-service emails except the Wood to Water chaser are synthetic test scenarios. Wood to Water scores are included, but the source texts are withheld because they contain a real retailer contact name and order number.

## Progress

| Measure | Value | Note |
| --- | --- | --- |
| GPTZero scans in the CSV | 162 | 114 through Stage 15; 17 per-text rows for Stages 24–25; 31 per-text rows for Stages 26 and 28–31. Stage 11 had no scans (0 of 160 samples were fact-complete). Stages 22–23 (30 scans, all 100% AI) and Stage 27 (6 scans, all 100% AI) are narrative aggregates and are not rows. Stage 16 is not in the CSV. |
| Human-draft edits at similarity ≥ 0.70 still classed human | 8/8 | Stages 28–31. Seven at 0–6% AI; g1 rose to 21% (+19). Does not lower the score of text that starts AI-written. |
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

**[evidence]** Stages 22–23: 30 natural fact-complete recommendation-letter variants scored 100% AI. Stage 24: six interpretive-versus-plain-record scans of three fully synthetic recommendation paragraphs, all 100% AI. Stage 25: off-the-shelf humanizers moved 1 of 7 emails. These are small samples, single scans, and one detector version. They do not change the skill rules: keep the request last, keep round-trip translation experiment-only, and when readability and a score conflict, keep natural fact-complete English. The scan record is [Stages 22–25](#stages-22-25).

**[evidence]** Stages 26–27: the off-the-shelf and adapter humanizer routes closed. Stage 26 moved 0/6. Stage 27’s six scans were all 100% AI. Stages 28–31 edited public human drafts. Light edits preserved a human classification only when the draft was already human-written. They do not lower the score of text that starts AI-written. The scan record is [Stages 26–31](#stages-26-31).

Kettle 13% is Stage 8 f1 and its Stage 9 Basic rescan (Sue Hall, dates folded in). Stage 12 e01-add later scored 22% on the same scenario. Jacket has no fact-complete result below 100%; the unedited raw scored 18%, and the Stage 14 address tests scored 29% and 38%, but those texts are not fact-complete. Stage 25 humanizer rewrites of that email scored 47 and 48. A fact check for those rewrites was not in the supplied record, and the same-session rescan of the unchanged email was 100. Blender 13% in the middle column is b3-rescan, which still has the invented address and both NC-350W model numbers; b4, with the address replaced but the model numbers kept, scored 49%. The first fact-complete blender with no invented details, b5, scored 100%, and Stage 15 c1 and c2 also scored 100%. Lamp never moved off 100%, and its raw text already scored 100% and included leaked template advice. Wood to Water v5 scored 3% on an Advanced scan; the original and v1–v4, all 100%, were scanned before the free Basic option disappeared, so the modes are not the same. Wrong colour 30% is the Stage 2 stitched candidate e10-halo; the later fact-conditioned edit e10-r2 scored 100%.

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

Scanned 16 Nov 2026. GPTZero Model 5.0b, free plan, Basic. No email address, account name, referee, applicant, or letter wording is recorded. Mixed % and human % were not in the supplied record. Clock times were not in the supplied record. File ids in the CSV for these stages are scan labels; disk filenames were not logged. These are small samples, single scans, and one detector version. They are not a method for passing GPTZero. They do not change the skill rules: keep the request last, keep round-trip translation experiment-only, and when readability and a score conflict, keep natural fact-complete English.

### Stage 22

21 scans of recommendation-letter paragraphs. The texts are not published. No author, subject, referee, applicant, or letter wording is recorded. The arms were recommender voice, uneven sentence length, plain verbs and fewer nominalizations (Reinhart et al., PNAS 2025), a rewrite with the pstack `unslop` skill, and a rewrite with the pstack `technical-writing` skill, plus controls and two full letters. All 21 scans scored 100% AI. Per-text file names and separate scores were not logged, so Stage 22 has no CSV rows.

### Stage 23

9 scans of recommendation-letter paragraphs, with the same privacy limit. The arms were feature-matching to paragraphs that scored 0% and author-style conditioning on the author's public writing. That conditioning is an idea from arXiv 2505.14608. All 9 scans scored 100% AI. Per-text file names and separate scores were not logged, so Stage 23 has no CSV rows.

Across Stages 22–23, 30 natural fact-complete variants scored 100% AI.

### Stage 24

Three fully synthetic recommendation paragraphs, interpretive framing versus plain-record framing. No letter wording is published.

| Paragraph | Interpretive AI % | Plain-record AI % |
| --- | ---: | ---: |
| 1 | 100 | 100 |
| 2 | 100 | 100 |
| 3 | 100 | 100 |

All six scans scored 100% AI, so the plain-record framing left every paragraph at 100% AI. One of the six scans was labelled Possible AI Paraphrasing. The supplied record does not say which paragraph or which framing carried that label. These six scores are CSV rows.

### Stage 25

Off-the-shelf humanizer models, on the synthetic calibration emails from earlier stages. The email names in the scan table are the names already used for those ids in this report.

Eight open Hugging Face detectors, scored on 122 edited texts that GPTZero 5.0b had already scored, do not track GPTZero. The best was HC3-roberta, Spearman 0.20, AUC 0.61. The other seven coefficients were not in the supplied record.

Smaug-Humanizer and jialinyyzz/humanizer rewrites: e04 scored 47 and 48. The supplied record does not say which model produced which of those two scores. The same-session rescan of the unchanged e04 text was 100. e01 and e07 stayed at 100. The supplied record does not give a separate score per model for e01 or for e07. Step 2 best-of-24 Smaug-Humanizer rewrites of e02, e03, e05, e06, e08, and e09 all scored 100% AI. e05, e06, e08, and e09 were labelled Possible AI Paraphrasing. A fact check for these rewrites was not in the supplied record. The supplied scores cover e01, e02, e03, e04, e05, e06, e07, e08, and e09. The recorded conclusion is that the humanizer route moved 1 of 7 emails; the supplied record does not define that denominator further. AuthorMist was unusable and has no scan row. No LoRA pilot was run. Modal cost was about $0.37.

<a id="stages-26-31"></a>

## Stages 26–31

Scanned 16–17 Nov 2026. GPTZero Model 5.0b, free plan, scores read in Basic view. % below is AI probability. No email address, account name, writer name, or message body is recorded. Mixed % and human % were not in the supplied record. Clock times were not in the supplied record. File ids in the CSV for these stages are scan labels; disk filenames were not logged. These are small samples and one detector version. They are not a method for passing GPTZero. Stages 26–27 do not change the skill rules. The only skill addition from Stages 28–31 is a hedged note: when a human-written draft already exists, polish it lightly and keep similarity to that draft at roughly 0.75 or higher. That note does not lower the score of text that starts AI-written. It does not replace the other rules: keep the request last, keep round-trip translation experiment-only, and when readability and a score conflict, keep natural fact-complete English.

Similarity, where a number is shown, is 1 − Levenshtein/max_len. Levenshtein is the character edit distance, and max_len is the length of the longer text. This repo’s `scripts/` directory holds the study checker only, and the skill scripts check facts, receipts, and detectors. A similarity helper does not fit those jobs, so the formula is recorded in prose. Unedited drafts have no similarity in the supplied record.

### Stage 26

16 Nov 2026. Small open instruct models and HF rephrasers, prompted as humanizers, on 8 synthetic calibration emails, 8 samples each, run on Modal (about $0.83). Fact-check pass counts were best for Qwen3-4B-Instruct-2507, then Llama-3.2-3B. The supplied record does not give the pass counts, only that order. DIPPER-XXL produced translationese and broke numbers. Gemma-3-4B, Phi-4-mini, Qwen2.5-3B, a 1.5B ARI model, and gohumanize mostly copied input or broke facts. Those six models have no GPTZero row in this stage.

The scan line abbreviates Qwen3-4B-Instruct-2507 as Qwen3-4B. Six scans, all 100% AI. 0/6 moved. e01 and e02 were labelled Possible AI Paraphrasing. A label for the other four scans was not in the supplied record.

| Model | Email | AI % | Label |
| --- | --- | ---: | --- |
| Qwen3-4B-Instruct-2507 | Lamp (e05) | 100 | not logged |
| Qwen3-4B-Instruct-2507 | Missing delivery (e08) | 100 | not logged |
| Qwen3-4B-Instruct-2507 | Double charge (e03) | 100 | not logged |
| Llama-3.2-3B | Kettle (e01) | 100 | Possible AI Paraphrasing |
| Llama-3.2-3B | Boots not received (e02) | 100 | Possible AI Paraphrasing |
| Llama-3.2-3B | Pre-sale price (e09) | 100 | not logged |

Together with Stage 25, off-the-shelf HF models moved only e04. Route closed. These six scores are CSV rows.

### Stage 27

16 Nov 2026. A base-model humanizer adapter from arXiv 2605.19516 (Qwen3-4B-Base). The arXiv id is the stated source of the adapter. This note does not extract figures from that paper.

144 outputs. Only 2 of 48 first-pass outputs kept every fact. 0/48 kept every fact on pass 2, and 0/48 on pass 3. Six scans (2 fact-passing pass-1 outputs, the e05 control, and 3 multi-pass outputs) were all 100% AI and were labelled Possible AI Paraphrasing, the control included. Route closed.

Separate file ids for those six scans were not in the supplied record. Which emails the two fact-passing outputs and the three multi-pass outputs were is not in the supplied record, beyond the e05 control. Stage 27 has no CSV rows.

### Stage 28

16 Nov. The idea is from arXiv 2608.11256 (human draft + light LLM edit). This note does not extract figures from that paper. Two genuine human emails from the public Enron corpus, AESLC test split: row 50 = a, row 57 = b. No message body is published.

| Id | Row | Similarity | AI % |
| --- | ---: | ---: | ---: |
| a0 | 50 | not logged | 0 |
| a1 | 50 | 0.898 | 0 |
| a2 | 50 | 0.701 | 6 |
| b0 | 57 | not logged | 0 |
| b1 | 57 | 0.904 | 0 |
| b2 | 57 | 0.723 | 0 |

a0 is the unedited draft. These six scores are CSV rows.

### Stage 29

16 Nov. Heavier rewrites. New draft c is AESLC test row 65. Similarity alone does not predict the flip.

| Id | Row | Similarity | AI % | Note |
| --- | ---: | ---: | ---: | --- |
| c0 | 65 | not logged | 0 | Unedited draft |
| c4 | 65 | 0.654 | 0 | |
| c5 | 65 | 0.380 | 0 | |
| b4 | 57 | 0.535 | 14 | |
| b5 | 57 | 0.400 | 0 | |
| a5 | 50 | 0.516 | 100 | 100% AI |

These six scores are CSV rows.

### Stage 30

17 Nov. A register hypothesis (keep the draft’s casual voice) was tested. It was not supported: a4 casual also flipped. New draft d is AESLC test row 79. The a5 row is a rescan of the Stage 29 text. The supplied record says the 100% result repeats. It does not give a second similarity.

| Id | Row | Similarity | AI % | Note |
| --- | ---: | ---: | ---: | --- |
| a3 | 50 | 0.715 | 3 | |
| a4 | 50 | 0.502 | 100 | Casual register kept |
| a5 | 50 | 0.516 | 100 | Rescan; repeats |
| d0 | 79 | not logged | 0 | Unedited draft |
| d4 | 79 | 0.591 | 0 | Keep-register |
| d5 | 79 | 0.500 | 24 | Formal register |

These six scores are CSV rows.

### Stage 31

17 Nov. Three new drafts: AESLC test row 101 (f), row 119 (g, an assessment/judgement-style note), and row 170 (h). b3 is a further edit of row 57.

| Id | Row | Similarity | AI % |
| --- | ---: | ---: | ---: |
| f0 | 101 | not logged | 0 |
| f1 | 101 | 0.740 | 0 |
| g0 | 119 | not logged | 2 |
| g1 | 119 | 0.751 | 21 |
| h0 | 170 | not logged | 0 |
| h1 | 170 | 0.764 | 0 |
| b3 | 57 | 0.655 | 0 |

f0, g0, and h0 are the unedited drafts. These seven scores are CSV rows.

### Tally

LLM edits of human drafts at ≥0.70 similarity: 8/8 still classed human (a1, a2, a3, b1, b2, f1, g1, h1), 7 at 0–6% but g1 rose to 21% (+19, beyond the ~2-point rescan band) on the most opinion/assessment-style draft. 0.50–0.70: text-dependent (b3, b4, c4, d4 human; a4/a5 100%; d5 24%); below 0.50: b5, c5 0%.

The suggested workflow, recorded as a hedged skill note and not as a bypass: when a human draft exists, polish it lightly and keep similarity to the draft at roughly ≥0.75 (a conservative margin, not a tested cutoff). Check facts against the draft. Caveats: small sample (8 drafts, short business emails), one upward drift (g1), not tested on long documents, and it does not help text that starts AI-written. It only preserved a human classification when the starting draft was already human-written.

The caveat states a sample of 8 drafts. The supplied record names AESLC test rows 50 (a), 57 (b), 65 (c), 79 (d), 101 (f), 119 (g), and 170 (h). It does not name an eighth row.

## Open hypotheses

These are recorded as hypotheses, not as findings.

- GPTZero treats stock LLM-style persona names, such as Helen, as an AI signal. This is how [PR #9](https://github.com/dexhunter/anti-detection-writing-skill/pull/9) states it, after the kettle name tests.
- Removing the base model's idiosyncratic or rambling content removes the human signal. This was noted after the Stage 10 deletion flips, and it is not treated as established cause.
- A fact-neutral block of the same shape can stand in for an invented address without flipping the score. Stage 14 b1 (39%) and b4 (49%) are consistent with that on the blender email when invented model numbers remain; b5 (100%) and Stage 15 c1 and c2 (100%) are not, once those model numbers are also removed.
- Why any particular reduction happened, including Wood to Water v5 at 3%, is not established by these records.

## Every recorded scan

162 scans, matching the CSV. Scan level is normalised to basic, advanced, or unknown. Unknown includes logs with no scan-level field, Stage 1 s1-01 (logged as advanced, with the page later showing basic), Stage 10 (no scanType in the URL; the panel showed Advanced Scan and 0 advanced left), calibration scans (the log notes 0 advanced scans left and sentence highlighting, but has no scan-level column), and Wood to Water original plus v1–v4 (scanned before the free Basic option disappeared). Stages 22, 23, and 27 are not in this table.

Exact timestamps are in the CSV and are not repeated in the table below. The account column is “not logged” on every row. The Stage 15 note's “free account A” is only a redacted label in this report; it is not a value in the CSV. No account name is published for Stages 22–31. Mixed % is 0 wherever it was logged, and is “not logged” for the ten Wood to Water texts that scored 100% AI and for every Stage 24, 25, 26, 28, 29, 30, and 31 row; v5 mixed was 0. Human % for those rows is “not logged”. One Stage 24 scan was labelled Possible AI Paraphrasing; the supplied record does not say which of the six. Stage 26 labels Possible AI Paraphrasing on e01 and e02 only. Stage 27’s six scans, which are not rows, were all labelled Possible AI Paraphrasing.

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
| Stage 24 | Synthetic recommendation 1 | `paragraph-1-interpretive` | Interpretive framing; fully synthetic | 100 | not logged | basic |
| Stage 24 | Synthetic recommendation 1 | `paragraph-1-record` | Plain-record framing; fully synthetic | 100 | not logged | basic |
| Stage 24 | Synthetic recommendation 2 | `paragraph-2-interpretive` | Interpretive framing; fully synthetic | 100 | not logged | basic |
| Stage 24 | Synthetic recommendation 2 | `paragraph-2-record` | Plain-record framing; fully synthetic | 100 | not logged | basic |
| Stage 24 | Synthetic recommendation 3 | `paragraph-3-interpretive` | Interpretive framing; fully synthetic | 100 | not logged | basic |
| Stage 24 | Synthetic recommendation 3 | `paragraph-3-record` | Plain-record framing; fully synthetic | 100 | not logged | basic |
| Stage 25 | Jacket (e04) | `e04-humanizer-47` | Smaug-Humanizer or jialinyyzz/humanizer rewrite; which model produced 47 was not in the supplied record | 47 | not logged | basic |
| Stage 25 | Jacket (e04) | `e04-humanizer-48` | Smaug-Humanizer or jialinyyzz/humanizer rewrite; which model produced 48 was not in the supplied record | 48 | not logged | basic |
| Stage 25 | Jacket (e04) | `e04-rescan` | Same-session rescan of the unchanged e04 text | 100 | not logged | basic |
| Stage 25 | Kettle (e01) | `e01-humanizer` | Humanizer rewrite stayed at 100% AI; no separate score per model in the supplied record | 100 | not logged | basic |
| Stage 25 | Blender (e07) | `e07-humanizer` | Humanizer rewrite stayed at 100% AI; no separate score per model in the supplied record | 100 | not logged | basic |
| Stage 25 | Boots not received (e02) | `e02-smaug` | Step 2 best-of-24 Smaug-Humanizer rewrite | 100 | not logged | basic |
| Stage 25 | Double charge (e03) | `e03-smaug` | Step 2 best-of-24 Smaug-Humanizer rewrite | 100 | not logged | basic |
| Stage 25 | Lamp (e05) | `e05-smaug` | Step 2 best-of-24 Smaug-Humanizer rewrite; Possible AI Paraphrasing | 100 | not logged | basic |
| Stage 25 | Charge after cancellation (e06) | `e06-smaug` | Step 2 best-of-24 Smaug-Humanizer rewrite; Possible AI Paraphrasing | 100 | not logged | basic |
| Stage 25 | Missing delivery (e08) | `e08-smaug` | Step 2 best-of-24 Smaug-Humanizer rewrite; Possible AI Paraphrasing | 100 | not logged | basic |
| Stage 25 | Pre-sale price (e09) | `e09-smaug` | Step 2 best-of-24 Smaug-Humanizer rewrite; Possible AI Paraphrasing | 100 | not logged | basic |
| Stage 26 | Lamp (e05) | `e05-qwen3-4b` | Qwen3-4B-Instruct-2507 prompted as a humanizer; scan line says Qwen3-4B | 100 | not logged | basic |
| Stage 26 | Missing delivery (e08) | `e08-qwen3-4b` | Qwen3-4B-Instruct-2507 prompted as a humanizer; scan line says Qwen3-4B | 100 | not logged | basic |
| Stage 26 | Double charge (e03) | `e03-qwen3-4b` | Qwen3-4B-Instruct-2507 prompted as a humanizer; scan line says Qwen3-4B | 100 | not logged | basic |
| Stage 26 | Kettle (e01) | `e01-llama-3.2-3b` | Llama-3.2-3B prompted as a humanizer; Possible AI Paraphrasing | 100 | not logged | basic |
| Stage 26 | Boots not received (e02) | `e02-llama-3.2-3b` | Llama-3.2-3B prompted as a humanizer; Possible AI Paraphrasing | 100 | not logged | basic |
| Stage 26 | Pre-sale price (e09) | `e09-llama-3.2-3b` | Llama-3.2-3B prompted as a humanizer | 100 | not logged | basic |
| Stage 28 | Enron AESLC test row 50 (a) | `a0` | Unedited human draft | 0 | not logged | basic |
| Stage 28 | Enron AESLC test row 50 (a) | `a1` | LLM edit; similarity 0.898 | 0 | not logged | basic |
| Stage 28 | Enron AESLC test row 50 (a) | `a2` | LLM edit; similarity 0.701 | 6 | not logged | basic |
| Stage 28 | Enron AESLC test row 57 (b) | `b0` | Unedited human draft | 0 | not logged | basic |
| Stage 28 | Enron AESLC test row 57 (b) | `b1` | LLM edit; similarity 0.904 | 0 | not logged | basic |
| Stage 28 | Enron AESLC test row 57 (b) | `b2` | LLM edit; similarity 0.723 | 0 | not logged | basic |
| Stage 29 | Enron AESLC test row 65 (c) | `c0` | Unedited human draft | 0 | not logged | basic |
| Stage 29 | Enron AESLC test row 65 (c) | `c4` | Heavier LLM edit; similarity 0.654 | 0 | not logged | basic |
| Stage 29 | Enron AESLC test row 65 (c) | `c5` | Heavier LLM edit; similarity 0.380 | 0 | not logged | basic |
| Stage 29 | Enron AESLC test row 57 (b) | `b4` | Heavier LLM edit; similarity 0.535 | 14 | not logged | basic |
| Stage 29 | Enron AESLC test row 57 (b) | `b5` | Heavier LLM edit; similarity 0.400 | 0 | not logged | basic |
| Stage 29 | Enron AESLC test row 50 (a) | `a5` | Heavier LLM edit; similarity 0.516 | 100 | not logged | basic |
| Stage 30 | Enron AESLC test row 50 (a) | `a3` | LLM edit; similarity 0.715 | 3 | not logged | basic |
| Stage 30 | Enron AESLC test row 50 (a) | `a4` | Casual register kept; similarity 0.502 | 100 | not logged | basic |
| Stage 30 | Enron AESLC test row 50 (a) | `a5-rescan` | Rescan of a5; 100% repeats. Stage 29 similarity 0.516 | 100 | not logged | basic |
| Stage 30 | Enron AESLC test row 79 (d) | `d0` | Unedited human draft | 0 | not logged | basic |
| Stage 30 | Enron AESLC test row 79 (d) | `d4` | Keep-register edit; similarity 0.591 | 0 | not logged | basic |
| Stage 30 | Enron AESLC test row 79 (d) | `d5` | Formal register; similarity 0.500 | 24 | not logged | basic |
| Stage 31 | Enron AESLC test row 101 (f) | `f0` | Unedited human draft | 0 | not logged | basic |
| Stage 31 | Enron AESLC test row 101 (f) | `f1` | LLM edit; similarity 0.740 | 0 | not logged | basic |
| Stage 31 | Enron AESLC test row 119 (g) | `g0` | Unedited human draft; assessment/judgement-style note | 2 | not logged | basic |
| Stage 31 | Enron AESLC test row 119 (g) | `g1` | LLM edit; similarity 0.751 | 21 | not logged | basic |
| Stage 31 | Enron AESLC test row 170 (h) | `h0` | Unedited human draft | 0 | not logged | basic |
| Stage 31 | Enron AESLC test row 170 (h) | `h1` | LLM edit; similarity 0.764 | 0 | not logged | basic |
| Stage 31 | Enron AESLC test row 57 (b) | `b3` | LLM edit; similarity 0.655 | 0 | not logged | basic |


## What is in the skill

[PR #9](https://github.com/dexhunter/anti-detection-writing-skill/pull/9), titled “Record a preliminary single-fact placement probe”, was merged on 12 Nov 2026, 16:29 Europe/London, as commit `4be38604419aadcdccb1f4d947bb255ecbed5c0b`. It covers the Stage 6–9 kettle tests. The skill also includes a preliminary Stage 10–15 note. Status for those stages below is as of 13 Nov 2026, Europe/London. The Stages 22–25 bullet is 16 Nov 2026. The Stages 26–31 bullet is 16–17 Nov 2026.

In the skill from Stages 28–31, as a hedged note only:

- When a human-written draft already exists, polish it lightly and keep similarity to that draft at roughly 0.75 or higher. Similarity is 1 − Levenshtein/max_len. Check facts against the draft.
- That note only preserved a human classification when the starting draft was already human-written. It does not lower the score of text that starts AI-written. The sample is 8 drafts, short business emails, with one upward drift (g1, to 21%, +19). It was not tested on long documents. Roughly 0.75 is a conservative margin, not a tested cutoff.
- The note does not replace the other writing rules.

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
- Stages 22–25 (16 Nov 2026) stay a negative result. They are recorded here and as a labelled note in the [evidence limits](../../skills/anti-ai-detection-writing-skill/references/evidence.md). They do not change the skill: the request stays last, round-trip translation stays an experiment only, and a readability conflict is still resolved by keeping natural fact-complete English. They are not a new editing method.
- Stages 26–27 (16 Nov 2026) stay a negative result. Off-the-shelf HF humanizers, together with Stage 25, moved only e04, and the adapter route’s six scans were all 100% AI. Those routes are closed. They are not a new editing method.
- The 0.50–0.70 band, the below-0.50 scores, and the register hypothesis are not rules. Stage 30 did not support keeping a casual voice as a score lever. Matching register stays the readability preference already in the skill.

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
- Stages 22 and 23 have no per-text CSV rows. The supplied result is 21 scans and 9 scans, each at 100% AI. File names, word counts, mixed %, human %, and clock times for those scans were not in the supplied record.
- Stages 24 and 25 have no logged mixed % or human %, and no clock time. The CSV `file` values are scan labels, not logged disk filenames. Stage 24 does not identify which of the six scans carried the Possible AI Paraphrasing label. Stage 25 does not say which humanizer produced the e04 score of 47 and which produced 48, and it does not give separate per-model scores for e01 or e07. A fact check for the humanizer rewrites was not in the supplied record. The other seven open-detector coefficients, besides HC3-roberta, were not in the supplied record. AuthorMist was unusable and was not scanned. The recorded conclusion is that humanizers moved 1 of 7 emails. The per-text scores that were supplied are the rows above, including the e04 scores of 47 and 48 and the same-session rescan of the unchanged e04 text at 100.
- No email address, account name, referee, applicant, or recommendation-letter wording is published for Stages 22–25.
- Stages 26, 28, 29, 30, and 31 have no logged mixed % or human %, and no clock time. The CSV `file` values are scan labels, not logged disk filenames. Stage 26 does not give numeric fact-check pass counts, only the order Qwen3-4B-Instruct-2507 then Llama-3.2-3B, and it does not give a GPTZero score for DIPPER-XXL, Gemma-3-4B, Phi-4-mini, Qwen2.5-3B, the 1.5B ARI model, or gohumanize. A paraphrase label was supplied for e01 and e02 only.
- Stage 27 has no per-text CSV rows. The supplied result is 6 scans, each at 100% AI, each labelled Possible AI Paraphrasing. The composition is 2 fact-passing pass-1 outputs, the e05 control, and 3 multi-pass outputs. File names for those six scans were not in the supplied record. Fact-check counts are 144 outputs, 2 of 48 first-pass outputs kept every fact, and 0/48 on pass 2 and on pass 3.
- Stages 28–31 do not publish the Enron email bodies or any writer or subject name. Draft letters in the supplied record are a (row 50), b (row 57), c (row 65), d (row 79), f (row 101), g (row 119), and h (row 170). The caveat says 8 drafts. An eighth row was not named. Unedited drafts have no similarity in the supplied record. The a5 rescan does not give a second similarity; the 0.516 figure is the Stage 29 measurement.
- No email address or account name is published for Stages 26–31.

## Sources

- `/workspace/iterations/log.md`
- `/workspace/baseexp/stage1` through `stage15` scan-log.csv, README, and edit-log files (Stage 11 has no scan log)
- `/workspace/calib/scan-log.csv`
- `/workspace/gptzero-w2w/receipt-5.0b-redacted.json` (scores only; texts withheld)
- [PR #9](https://github.com/dexhunter/anti-detection-writing-skill/pull/9)
- Stages 22–25: the 16 Nov 2026 scan results recorded in this note (Model 5.0b, free plan, Basic). A scan-log path was not supplied with those results.
- Stages 26–31: the 16–17 Nov 2026 scan results recorded in this note (Model 5.0b, free plan, Basic view). A scan-log path was not supplied with those results.
