# Literature and private-letter update, 16 November 2026

Checked 16 November 2026 by opening each source linked below. A figure that was not in the opened source is left out. This note is not a GPTZero result, and it is not a method for passing a detector. Evidence and hypothesis are labelled as such.

This note was checked against commit `de9576eda951a229968267e7e306bfe0a6f12ac8` (13 November 2026, “Record Stage 16 GPTZero scans and a 13 November literature update (#11)”). `SKILL.md`, `README.md`, `docs/literature-update-2026-11-13.md`, `docs/detector-literature-and-proxy.md`, and `skills/anti-ai-detection-writing-skill/references/detector-research.md` were opened. This note adds only items that those documents did not already record. The same change applies the rules in section (c) to the skill.

The scans in section (b) are from today’s GPTZero 5.0b work on a private ~700-word professional recommendation letter (not published). They are one letter, not a general pass method.

Section (d) records Stages 22–25 from the same date. Those scans do not change the rules in section (c). Section (d) quotes the supplied scan results. It does not add figures from a newly opened paper.

Section (e) records Stages 26–31. Stages 26–29 were scanned on 16 November 2026. Stages 30–31 were scanned on 17 November 2026. Section (e) quotes the supplied scan results. The arXiv ids in that section are the stated sources of two ideas. Section (e) does not extract figures from those papers, and it does not change the rules in section (c).

## What the 11 and 13 November notes already cover

Do not re-add these as new literature:

- GPTZero’s own 2026 report ([Adam et al., arXiv:2602.13042](https://arxiv.org/abs/2602.13042)): a supervised Human / AI / Mixed classifier, with finer AI classes including Polished and AI Paraphrased; training against paraphrasing prompts, translation chains, DIPPER, TempParaphraser, humanisers, and word substitution; document-plus-sentence losses; Table 1 is version 4.1b, not 5.0b.
- [DIPPER](https://arxiv.org/abs/2303.13408) (Krishna et al., NeurIPS 2023) and [recursive paraphrasing](https://arxiv.org/abs/2303.11156) (Sadasivan et al.).
- [Liang et al.](https://arxiv.org/abs/2304.02819) (Patterns 2023) on bias against non-native English writers, plus Ghostbuster’s non-native test and Weber-Wulff et al. on translation and light obfuscation.
- Adversarial Paraphrasing, RAID, RADAR, RAFT, Stumbling Blocks, DetectGPT, Fast-DetectGPT, Binoculars, DAMAGE, Beemo, Saha and Feizi (“Almost AI, Almost Human”), EditLens, “Attacking Only Half the Data”, “Humanized but Still True?”, HIP, “Amplifying, Not Learning”, “The Perplexity Trap”, and Jabarian and Imas.
- Vendor release-note claims, fetched 13 November 2026, for models 5.0b, 4.2b, 4.1b, and 3.14b.
- The standing skill rules: never trade accuracy or readability for a score; never drop or invent a fact; do not run a whole-text AI polish over fact-dense text; a paragraph or sentence highlight is not a rewrite instruction; a result on an older GPTZero or an open detector does not transfer to Model 5.0b unless that case was measured.

The gaps this update fills are back-translation as a measured attack (ESPERANTO is not in those notes), later work on fluency versus detection and on professional-editing / proficiency confounds, official GPTZero pages on “Possible AI Paraphrasing” and document-versus-sentence scores, and today’s letter scans.

---

## (a) New papers and official pages

### Back-translation

[Ayoobi et al., “ESPERANTO”](https://arxiv.org/abs/2409.14285) (arXiv:2409.14285, 22 September 2024). Back-translation through ten intermediate languages with Google Translate (Portuguese, Spanish, French, Italian, Chinese, Dutch, Danish, Japanese, German, Korean), then a WER-max combiner. Semantic preservation is checked with P-SP and USEE, with thresholds taken from human paraphrases on PAR3 (0.76 and 0.69). Table 1 shows that, on the original-to-single-language back-translations, typologically closer languages stay nearer the source: German News P-SP is 0.983 and Portuguese is 0.988, while Chinese is 0.970 and Japanese is 0.967. The combined texts in Table 2 still sit above those thresholds (News P-SP 0.951; review sets R-G / R-L 0.881 and 0.872). Nine detectors were tested, including GPTZero, Pangram, and ZeroGPT. GPTZero and ZeroGPT were limited to 200 randomly sampled texts per dataset; where a 1% false-positive rate could not be fixed, the actual FPR is given in superscripts. The authors say GPTZero and ZeroGPT “indicate a lack of robustness against back-translation techniques.” The example they highlight is GPTZero on the R-L review set: TPR 0.65 before, 0.09 after. That drop is not uniform. The GPTZero row of Table 3 also stays high after the attack on several other sets (for example 0.97, 0.96, and 1 with a 0.05 FPR). The GPTZero build is the August 2024 product cited as [47], not Model 5.0b. The attack is a multi-language Google Translate pipeline plus a combiner, not a single-pivot translation written by an LLM. **Evidence** that back-translation can lower an older GPTZero’s TPR on some short-review data, and that Chinese and Japanese single-language back-translations diverge more from the source than German ones. **Does not transfer** as a 5.0b document AI-percent, and it is not a fact-preservation audit.

### Fluency, quality, and detection

[Zheng et al., “TH-Bench”](https://arxiv.org/abs/2503.08708) (arXiv:2503.08708, 2025). A benchmark of six evading attacks (Dipper, Recursion in the sense of Sadasivan et al., Prompt, RAFT, HMGC, and TOBLEND) against 13 machine-generated-text detectors, six datasets, 19 domains, and 11 generators. GPTZero is not one of the detectors. The abstract’s finding is that no single attack excels on all three of evading effectiveness, text quality, and computational overhead, and that there is a trade-off among those three. **Evidence** of a quality-versus-evasion trade-off on open detectors. **Not** a GPTZero 5.0b result and **not** permission to degrade a letter’s English.

[Zheng, “StyleShield”](https://arxiv.org/abs/2605.00924) (arXiv:2605.00924, 2026). A continuous style-transfer attack on a multi-domain **Chinese** benchmark, with a parameter γ that traces an evasion–preservation frontier. GPTZero is not named. Table 1, on the training detector: an LLM rewrite baseline (Qwen-2.5-7B-Instruct prompted to humanise) evades only 0.3% of samples at threshold 0.5, with semantic similarity 0.964; back-translation (Chinese→English→Chinese via NLLB-200) evades 82.6% but drops semantic similarity to 0.852, and its perplexity (14.6) falls below the human reference (16.5), which the authors read as “unnatural regularity.” StyleShield at γ=7.0 reaches 94.6% evasion with similarity 0.928. The paper also describes RateAudit, a diagnostic that can shift document-level detection rates to pre-specified values. **Evidence** that, on those Chinese detectors, a fluent LLM rewrite can remain detectable, and that back-translation can evade more only with a semantic (and, on their PPL reading, regularity) cost. **Hypothesis**, not a 5.0b finding, if applied to an English professional recommendation letter.

### Watermark-free robustness under paraphrase

[Shportko and Verbitsky, “Paraphrasing Attack Resilience of Various AI-Generated Text Detection Methods”](https://arxiv.org/abs/2605.14240) (arXiv:2605.14240, 2026). Fine-tuned RoBERTa, Binoculars (Falcon-7B / Falcon-7B-Instruct), and five surface text features, plus Random Forest ensembles. The paraphrase attack is 201 AI texts passed through the commercial bypasser GPTinf, plus 201 human texts. GPTZero is not evaluated; the paper only records GPTinf’s marketing claim that it bypasses GPTZero and other tools. Table 1: Binoculars F1 falls from 0.7497 to 0.5533 (degradation 0.1964), the largest drop; RoBERTa goes from 0.7586 to 0.6594; the full ensemble from 0.8061 to 0.6716. The authors call this a performance-versus-resilience dichotomy: Binoculars-inclusive ensembles are strongest before the attack and lose the most after it. They also report that Binoculars’ information gain increases as the context window grows and plateaus somewhere after 256–512 tokens. **Evidence** that a watermark-free likelihood-ratio detector can degrade under a commercial paraphraser, and that short windows carry less of that information gain. **Not** a GPTZero 5.0b document score.

### Non-native writing, professional editing, and population limits

[Park, Jeong, and Kim, “Style as a Confound”](https://arxiv.org/abs/2608.26710) (arXiv:2608.26710, 2026). 135,389 paired non-native academic manuscripts and their professionally edited versions (2018–2025), content and authorship held fixed. Thirteen **publicly available** detectors; the limitations section says proprietary commercial detectors are not covered, and GPTZero is not in the list. Table 3, pre-ChatGPT human texts (so any AI flag is a false positive): false-positive rates run from Binoculars 0.0% to Log-rank 100.0%, with RoBERTa at 93.1% and RADAR at 88.3%. Token-statistics detectors are near ceiling; some zero-shot likelihood-ratio detectors stay near zero. The same Table 3, on that pre-ChatGPT set (2018–2022), raises Fast-DetectGPT by 6.4 percentage points and lowers MAGE by 9.1 points. Score shifts correlate with edit intensity, and the authors treat professional editing style as a confound rather than a clean separation of origin from style. **Evidence** that polished academic English, including edits of non-native manuscripts, can move open-detector scores in either direction. **Not** a GPTZero 5.0b measurement, and not a reason to treat a high 5.0b score as proof of AI authorship or a low score as proof of human authorship.

[Li and Wan, “Who Writes What”](https://arxiv.org/abs/2502.12611) (arXiv:2502.12611, submitted 18 February 2025; the opened abstract page is v2). ICNALE learner essays plus parallel LLM texts; ten open detectors, no GPTZero. Accuracy is reported at a 5% false-positive-rate threshold. Table 6: CEFR proficiency is significant (p<0.05) for every detector; language environment (EFL, ESL, or native) is significant for most; sex is significant for none; academic field is detector-dependent. Table 7 gives LSMeans accuracies by CEFR band; the direction is not uniform across detectors (for example chatgpt-roberta is higher at A2_0, 0.7480, than at B2_0, 0.7045, while detectgpt moves the other way, 0.7944 to 0.8289). The limitations section confines the claim to open-source detectors and a corpus of Asian English learners. **Evidence** that proficiency and language environment affect open-detector accuracy. **Not** a 5.0b result, and not a simple “lower proficiency is always flagged” rule.

[Garland, “AI Detectors Fail Diverse Student Populations”](https://arxiv.org/abs/2603.20254) (arXiv:2603.20254, v1, 11 March 2026). A theoretical note: if the assessor does not know the individual student’s writing distribution, the null is composite, and any text-only one-shot detector with useful power has a false-accusation rate bounded by the overlap between student writing and model output. The paper argues that this limit is independent of detector engineering, and that detection scores should not be the sole evidence in misconduct proceedings. **Evidence** only of that formal bound and policy claim. It does not measure GPTZero 5.0b.

### Official GPTZero pages opened 16 November 2026

These are vendor claims, not measurements of the private letter.

[“How does GPTZero detect AI paraphrasing and AI bypassers?”](https://support.gptzero.me/articles/5593633457-how-does-gptzero-detect-ai-paraphrasing-and-ai-bypassers). Advanced Scan can classify a document as AI paraphrased. The high-confidence wording is: “We are highly confident this text was originally AI, but rewritten by AI or a human.” A badge reads “Possible AI Paraphrasing,” still marked beta. At lower confidence the wording changes to “moderately confident” or “uncertain.” The AI score can be split into chance AI Generated and chance AI Paraphrased. The page claims a false-positive rate below 0.1% on paraphrased text from “certain popular AI tools,” and says coverage of bypassers is still improving. It also says detection is not infallible and points to GPTZero Authorship for a writing-process record. **Evidence** of what the current Advanced Scan paraphrasing label means. The page does not name Model 5.0b. **Not** a measured false-positive rate on this letter.

[“How do I interpret results from GPTZero's Advanced Sentence Scanning?”](https://support.gptzero.me/articles/7549392421-how-do-i-interpret-results-from-gptzero-s-advanced-sentence-scanning). The percentage is confidence in the classification of the **entire** text. “100% AI” means the model is confident the whole document was written by AI; it does not mean that 100% of the sentences were written by AI. Yellow and green highlights show which sentences most pushed the document toward AI or human. Unhighlighted sentences can still affect the result. “Editing the whole document can move the score more than editing only the highlighted sentences, because the model reads the document as a whole.” Confidence bands are given as vendor error-rate claims: highly confident, less than 2%; moderately confident, around 10%; uncertain, 14% or higher. The page says that if the model is not confident something is AI, it generally errs toward human, and that a detection result should not be the only basis for academic punishment. **Evidence** that a paragraph-level scan and a document-level scan are different quantities, which matches today’s c4 / c7 split. **Vendor claim**, not a causal editing rule.

[“What is the difference between the free and paid for plans?”](https://support.gptzero.me/articles/1272562776-what-is-the-difference-between-the-free-and-paid-for-plans). The free plan includes Basic AI Scan (overall score) “plus one free Advanced Scan.” Premium includes Advanced Scan with sentence highlighting. **Evidence** that Basic and Advanced are different product modes, and that a fresh free account’s first Advanced scan is a complimentary Advanced scan. **Hypothesis**, until a paired Basic-versus-Advanced rescan of the same bytes is run, whether that mode difference moved today’s c7 score.

[GPTZero model release notes](https://gptzero.me/news/ai-detection-model-api-updates), fetched again 16 November 2026. The 13 November note already recorded 5.0b (improved performance on polished and AI-paraphrased sub-classes; lower false-positive rates; larger architecture), 4.2b, 4.1b, and 3.14b. Additional vendor claims not in that short table: **4.11b** (7 October 2026, `2026-10-07-base`) improved recall on AI-paraphrased, mixed, and polished sub-classes and “improved document chunking and aggregation”; **3.15b** (18 December 2025) “improved robustness to AI paraphrasers.” Older notes still on the same page: 16 October 2023, an updated model “including documents written by ESL students, resulting in fewer false positives”; 19 July 2023, the model was “tuned … to improve its performance on ESL writing”; 9 January 2024, a claim that an AI score of 90% means a 90% chance the text is entirely AI-written (a calibration statement for that 2024 build, not demonstrated here for 5.0b).

[“How AI Content Detectors Work To Check For AI”](https://gptzero.me/news/how-ai-detectors-work) (14 October 2026). Restates that an AI probability score is not the percentage of the document written by AI, but an estimate of the probability of a classification; that GPTZero “deliberately tackles” paraphrased and mixed text; and that no detector should be a basis for automatic punishment. The article names GPTZero 4o as “our most recent model,” which is consistent with its October 2026 date and is earlier than the 5.0b release on 4 November 2026.

**Implication for the skill, taken together.** ESPERANTO and the support pages make back-translation and “Possible AI Paraphrasing” first-class topics, which the 13 November update did not treat as such. Adam et al., already in the repo, says later GPTZero training includes translation chains; 5.0b’s vendor notes say polished and AI-paraphrased performance was improved again. That combination is a reason to treat a full-document round trip as something 5.0b is described as trained to notice, not as a default rewrite. TH-Bench and StyleShield, plus today’s c7 / c7a / c7b / c8 scores, support the existing rule that readability is not a score lever. Park et al. and Li and Wan support the existing rule that a score is not authorship, especially for academic or non-native-like English, without transferring their open-detector rates onto 5.0b.

---

## (b) Today’s experimental results on a private ~700-word professional recommendation letter (not published)

All scores below are free-plan GPTZero **Model 5.0b**. Earlier full-letter and most paragraph scans used **Basic**. The document versions c7, c7a, c7b, and c8 were each logged once on the **same fresh account**, **Model 5.0b**, **Advanced**. The official free-plan page says a free account includes one complimentary Advanced Scan. Four Advanced results on one account exceed that description, so the Advanced label is the session record, not a check that the plan allowed four Advanced scans. Basic and Advanced were not paired on the same bytes, so any comparison between the earlier Basic scans and these Advanced document scores is a recorded caveat, not a measured cause of the score change. Among these four, the log records the same mode, model, and account. Word counts are `wc` counts of the files on disk. Fact checks used a fixed 82-item inventory. This is one letter and one account, a single scan of each version, not a general method.

### Full-letter AI-written and steered drafts

Every AI-written full letter scored **100% AI**: t0, c1, c2, and c3 (c3 is 645 words).

### Single-paragraph style variants

Style variants of one paragraph all scored **100% AI**: dictated, dry British, length variance, and clause folding (v1, v2, v5, v6). v3 was not scanned (HTTP 429 / “Not scanned”).

### Round-trip paragraph that scored 0%

A round trip English→Chinese→English, done by the LLM itself, with only factual drift and genuine grammar errors repaired and odd phrasing left in, scored **0% AI** on one paragraph (v4, 120 words). This **replicated on a rescan**. That is evidence for this one paragraph, not for the letter as a whole.

### Full-letter round trip (c4)

A full-letter round trip (c4, 698 words) scored **100% AI** and was labelled **“Possible AI Paraphrasing.”** Passing a paragraph and passing the assembled document are different outcomes. That split is consistent with the vendor’s statement that the model reads the document as a whole, and with Adam et al.’s already-recorded claim that later GPTZero training includes translation chains. It is **not** a reproduction of ESPERANTO (different pipeline, different GPTZero, different metric).

### Paragraph-level scans of the c4-family text

Passing, as given: the relationship paragraph scored 0%; project paragraph A scored 0%; the credentials paragraph scored 0% on one version and 4% on a second; the plans paragraph scored 26% AI (human-leaning). Other versions of the credentials paragraph, and a German round trip of the relationship paragraph, scored 100%. Results-heavy project paragraph B failed in eight versions (Chinese, German, and Japanese round trips, a split, and short sentences), all **94–100% AI**.

**Observation, with a mechanism still a hypothesis.** German round trips in this set kept English word order and stayed fluent, and they scored 100%. Chinese round trips restructured sentences, and some of those paragraphs scored low. ESPERANTO Table 1 is compatible with that contrast as a source-similarity fact (German stays closer to the English source than Chinese or Japanese), but ESPERANTO did not measure Model 5.0b, and Japanese was not a reliable pass on results-heavy project paragraph B here. Do not treat pivot-language choice as a working method.

### Assembled letter c7 and later polishes

The passing paragraphs were assembled, and the facts from results-heavy project paragraph B were folded in after the passing project paragraph A rather than kept as a standalone 100% paragraph. The four document versions below were each logged once on the same fresh account, Model 5.0b, Advanced, with the plan-limit caveat above. This is one letter and one account, a single scan each, not a general method.

- **c7** (assembled round-trip paragraphs; 702 words; 82 facts still present): **15% AI**, with the label quoted as **“highly confident” that the text is entirely human**.
- **c7a** (c7 plus the five most awkward phrases fixed; 689 words): **13% AI**, **“highly confident human”**.
- **c7b** (c7a plus eight further outright-error fixes, leaving remaining stylistic quirks; 676 words): **43% AI**, **“uncertain, likely human”**.
- **c8** (full natural polish of c7 into natural academic English; 672 words; **25** targeted replacements; 82 facts still present): **100% AI**.

The translation-like phrasing that remained in c7 is part of the measured text. Whether those quirks caused the 15% is a **hypothesis**. They also sit in tension with the skill’s readability rule and with a polished academic voice for a professional recommendation letter.

**Evidence**, on this letter: the same facts in fluent English (c8) scored 100% AI. Five local repairs (c7a) stayed at 13%, which is not a step up from 15%. Eight further error fixes (c7b) rose to 43%. That sequence is not a smooth ladder and not a bypass. Full natural polish (c8) returned to 100%. The shape is consistent with TH-Bench’s quality-versus-evasion trade-off and with StyleShield’s finding that a fluent LLM rewrite can remain detectable. Those papers did not measure 5.0b.

The user chose the natural c8 for actual use, because quality beats the score. c7 remains a scored backup.

---

## (c) Skill rule changes applied with this note

These rules are applied in `skills/anti-ai-detection-writing-skill/SKILL.md` and `references/detector-research.md`. Each one is tied to the 16 November scans and/or to a source opened for this note. None of them authorises dropping a fact, inventing a fact, or trading away a requested academic voice in order to hit a number.

1. **Document scores and paragraph scores are different quantities.** After any paragraph-level experiment, rescan the exact assembled body before reporting a letter or article score. A 0% paragraph does not establish a low document score (c4: 0% paragraph, 100% letter with “Possible AI Paraphrasing”). This is also what GPTZero’s Advanced Scan page says: the percentage is confidence about the entire text, and the model reads the document as a whole. **[evidence]**

2. **Do not run a fluency or “natural academic English” polish over a low-scoring candidate without treating it as a new text.** Rescan the exact polished bytes. On this letter, 25 fluency edits took c7 from 15% to c8 at 100%. The same-account Advanced intermediates were 13% after five awkward-phrase fixes (c7a) and 43% after those plus eight further outright-error fixes (c7b). This tightens the existing Stage 16 rule (“do not run a whole-text AI polish”) to cover post-hoc naturalisation of an already-scored draft. **[evidence]**

3. **When readability and a lower score pull in opposite directions, report both and do not optimise the score.** Keep c7 (or any later low-scoring but awkward draft) as a scored backup. Offer a natural candidate, its own score, and the trade-off. The skill already says never to trade readability for a score; today’s c7 / c7a / c7b / c8 set is the measured illustration, and TH-Bench’s abstract is supporting literature on open detectors. The user chose the natural c8 for actual use, because quality beats the score. **[evidence for this letter; literature as supporting, not 5.0b]**

4. **Round-trip or back-translation is an experiment, not a default rewrite.** If it is tried at all: use it only when the user has asked for detector iteration; repair only factual drift and genuine grammar errors; keep every protected name, number, date, hedge, and highlighted note; fact-check before scanning; and say plainly that odd phrasing may be part of any lower score. ESPERANTO measured an older GPTZero, a different pipeline, and TPR rather than a 5.0b AI-percent. Full-letter c4 was caught as possible AI paraphrasing. **[evidence that it can move a paragraph; evidence that it need not move a 5.0b document; literature does not make it a method]**

5. **Do not assume a pivot language.** In this letter, German round trips stayed fluent, kept English word order, and scored 100% at paragraph level; some Chinese round trips restructured the sentence and scored low. ESPERANTO Table 1 shows German back-translations staying closer to the source than Chinese or Japanese ones, which is compatible but not a 5.0b mechanism proof. Japanese did not salvage results-heavy project paragraph B here. **[evidence of the contrast on this letter; mechanism is a hypothesis]**

6. **Folding facts from a failing paragraph into a neighbouring passing paragraph is one measured assembly, not a recipe.** It is how c7 was built. It still requires a full-document rescan, a fact check, and a readability review. **[evidence for this letter only]**

7. **Log scan mode, model version, and the paraphrase label separately from the AI percent.** Record whether the scan was Basic or Advanced, and whether a free account’s complimentary Advanced Scan was used. Do not treat a Basic 100% and an Advanced 15% as a pure wording effect until the same bytes are scanned in both modes. Record “Possible AI Paraphrasing” (and any Generated-versus-Paraphrased split) as its own field. **[evidence of a mode caveat; vendor pages for what the fields mean]**

8. **A detector score is still not authorship, inbox delivery, or permission to send.** Park et al. and Li and Wan show that open detectors can respond to proficiency and to professional academic editing; Garland argues a score should not be sole evidence. GPTZero’s own Advanced Scan and “How AI detectors work” pages say the same about punishment and about the score not being a share of AI sentences. This restates the skill’s existing limit with newer sources. It does not transfer those papers’ false-positive rates onto 5.0b. **[literature and vendor claims; not a 5.0b FPR]**

9. **Do not add DIPPER, a commercial humaniser, synonym lists, or invisible characters as score levers.** Those remain covered by the 13 November note and by the fact that 5.0b’s vendor notes target paraphrased and polished text. “Humanized but Still True?” already warns that humanisers alter numbers and names. **[already covered; restated so a back-translation update does not reopen them]**

### Proposed experiments, not findings

The c7a and c7b scores above are now recorded (same fresh account, Model 5.0b, Advanced, one scan each). Still not done:

- Pairwise Basic versus Advanced rescans of the exact c7 and c8 bytes, if credits allow, to test the mode caveat.
- A second independent rescan of c7, c7a, or c7b on the same mode before treating a single Advanced scan as stable.

None of those is a result until the scan exists.

---

## (d) Stages 22–25, 16 November 2026 (negative)

All scans below are free-plan GPTZero Model 5.0b Basic scans. No email address, account name, referee, applicant, or letter wording is recorded. Mixed and human percentages were not in the supplied record. These are small samples, single scans, and one detector version. They are not a method for passing a detector. They do not change the rules in section (c): the request stays last, round-trip translation stays an experiment only, and when readability and a lower score conflict, keep natural fact-complete English. The labelled evidence note is in [evidence limits](../skills/anti-ai-detection-writing-skill/references/evidence.md). The per-text rows that were logged are in the [results report](reports/gptzero-results.md).

**[evidence]** Thirty natural fact-complete recommendation-letter variants (Stages 22–23) and six interpretive-versus-plain-record scans of three fully synthetic recommendation paragraphs (Stage 24) all scored 100% AI. Off-the-shelf humanizers moved 1 of 7 emails (Stage 25). That is not a new editing method.

### Stage 22

21 scans of recommendation-letter paragraphs. The texts are not published. No author, subject, referee, applicant, or letter wording is recorded. The arms were recommender voice, uneven sentence length, plain verbs and fewer nominalizations (Reinhart et al., PNAS 2025), a pstack `unslop` rewrite, and a pstack `technical-writing` rewrite, plus controls and two full letters. All 21 scored 100% AI. No per-text row was logged.

### Stage 23

9 scans of recommendation-letter paragraphs, with the same privacy limit. The arms were feature-matching to paragraphs that scored 0% and author-style conditioning on the author's public writing (idea from [arXiv:2505.14608](https://arxiv.org/abs/2505.14608)). All 9 scored 100% AI. Across Stages 22–23, 30 natural fact-complete variants scored 100% AI. No per-text row was logged. The arXiv id is the stated source of the conditioning idea. This note does not extract figures from that paper.

### Stage 24

Three fully synthetic recommendation paragraphs, interpretive framing versus plain-record framing: six scans, all 100% AI. One scan was labelled Possible AI Paraphrasing. The supplied record does not say which paragraph or which framing carried that label. No letter wording is published. The plain-record framing left all three paragraphs at 100% AI.

### Stage 25

Eight open Hugging Face detectors, on 122 edited texts already scored by GPTZero 5.0b, do not track GPTZero. The best was HC3-roberta, Spearman 0.20, AUC 0.61. The other seven coefficients were not in the supplied record.

Smaug-Humanizer and jialinyyzz/humanizer rewrites: e04 scored 47 and 48. The supplied record does not say which model produced which of those two scores. The same-session rescan of the unchanged e04 text was 100. e01 and e07 stayed at 100. The supplied record does not give a separate score per model for e01 or for e07. Step 2 best-of-24 Smaug-Humanizer rewrites of e02, e03, e05, e06, e08, and e09 all scored 100% AI. e05, e06, e08, and e09 were labelled Possible AI Paraphrasing. A fact check for these rewrites was not in the supplied record. The supplied scores cover e01, e02, e03, e04, e05, e06, e07, e08, and e09. The recorded conclusion is that the humanizer route moved 1 of 7 emails; the supplied record does not define that denominator further. AuthorMist was unusable and was not scanned. No LoRA pilot was run. Modal cost was about $0.37.

---

## (e) Stages 26–31, 16–17 November 2026

All scans below are free-plan GPTZero Model 5.0b, scores read in Basic view. % is AI probability. No email address, account name, writer name, or message body is recorded. Mixed and human percentages were not in the supplied record. These are small samples and one detector version. They are not a method for passing a detector. They do not change the rules in section (c): the request stays last, round-trip translation stays an experiment only, and when readability and a lower score conflict, keep natural fact-complete English. The hedged human-draft note in the skill is an addition beside those rules. It does not lower the score of text that starts AI-written. The labelled evidence note is in [evidence limits](../skills/anti-ai-detection-writing-skill/references/evidence.md). The per-text rows that were logged are in the [results report](reports/gptzero-results.md).

**[evidence]** Stages 26–27 closed two humanizer routes. Stages 28–31 preserved a human classification only when the starting draft was already human-written. That is not a way to lower the score of AI-written text.

### Stage 26

16 Nov 2026. Small open instruct models and HF rephrasers, prompted as humanizers, on 8 synthetic calibration emails, 8 samples each, run on Modal (about $0.83). Fact-check pass counts were best for Qwen3-4B-Instruct-2507, then Llama-3.2-3B. The supplied record does not give the pass counts. DIPPER-XXL produced translationese and broke numbers. Gemma-3-4B, Phi-4-mini, Qwen2.5-3B, a 1.5B ARI model, and gohumanize mostly copied input or broke facts. Those models were not given a Stage 26 GPTZero score.

Scans: Qwen3-4B e05, e08, e03 = 100/100/100. Llama-3.2-3B e01, e02, e09 = 100/100/100. e01 and e02 were labelled Possible AI Paraphrasing. 0/6 moved. Together with Stage 25, off-the-shelf HF models moved only e04. Route closed. The scan line's "Qwen3-4B" is the supplied abbreviation of Qwen3-4B-Instruct-2507.

### Stage 27

16 Nov 2026. A base-model humanizer adapter from [arXiv:2605.19516](https://arxiv.org/abs/2605.19516) (Qwen3-4B-Base). 144 outputs. Only 2 of 48 first-pass outputs kept every fact, and 0/48 kept every fact on passes 2 and 3. Six scans (2 fact-passing pass-1 outputs, the e05 control, and 3 multi-pass outputs) were all 100% AI and were labelled Possible AI Paraphrasing, the control included. Route closed. No per-text row was logged: separate file ids for those six scans were not in the supplied record. The arXiv id is the stated source of the adapter. This note does not extract figures from that paper.

### Stage 28

16 Nov. The idea is from [arXiv:2608.11256](https://arxiv.org/abs/2608.11256) (human draft + light LLM edit). Two genuine human emails, Enron AESLC test rows 50 = a and 57 = b. LLM edits were measured by similarity = 1 − Levenshtein/max_len, where Levenshtein is the character edit distance and max_len is the length of the longer text. There is no similarity script in this repo. a0 orig 0%, a1 (0.898) 0%, a2 (0.701) 6%; b0 0%, b1 (0.904) 0%, b2 (0.723) 0%. The arXiv id is the stated source of the idea. This note does not extract figures from that paper. No message body is published.

### Stage 29

16 Nov. Heavier rewrites. New draft c is row 65. c0 0%, c4 (0.654) 0%, c5 (0.380) 0%; b4 (0.535) 14%; b5 (0.400) 0%; a5 (0.516) 100% AI. Similarity alone does not predict the flip.

### Stage 30

17 Nov. A register hypothesis (keep the draft's casual voice) was tested. a3 (0.715) 3%; a4 casual (0.502) 100%; a5 rescan 100% (repeats). New draft d is row 79. d0 0%, d4 keep-register (0.591) 0%, d5 formal (0.500) 24%. The register hypothesis was not supported (a4 casual also flipped).

### Stage 31

17 Nov. Three new drafts: rows 101 (f), 119 (g, an assessment/judgement-style note), and 170 (h). f0 0, f1 (0.740) 0; g0 2, g1 (0.751) 21; h0 0, h1 (0.764) 0; b3 (0.655) 0.

### Tally

LLM edits of human drafts at ≥0.70 similarity: 8/8 still classed human (a1, a2, a3, b1, b2, f1, g1, h1), 7 at 0–6% but g1 rose to 21% (+19, beyond the ~2-point rescan band) on the most opinion/assessment-style draft. 0.50–0.70: text-dependent (b3, b4, c4, d4 human; a4/a5 100%; d5 24%); below 0.50: b5, c5 0%.

When a human draft exists, polish it lightly and keep similarity to the draft at roughly ≥0.75 (a conservative margin, not a tested cutoff). Check facts against the draft. Caveats: small sample (8 drafts, short business emails), one upward drift (g1), not tested on long documents, and it does not help text that starts AI-written. The supplied record names AESLC test rows 50 (a), 57 (b), 65 (c), 79 (d), 101 (f), 119 (g), and 170 (h), and states the sample as 8 drafts. It does not name an eighth row.
