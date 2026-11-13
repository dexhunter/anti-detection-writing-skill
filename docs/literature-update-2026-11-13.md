# Literature update, 13 November 2026

Checked 13 November 2026 by opening each source linked below. A figure that was not in the opened source is left out. This note is not a GPTZero result, and it is not a method for passing a detector. The same-day email scans are the [Stage 16 report](reports/stage-16-pot-handle.md). The earlier literature note and the offline proxy stay in [detector literature and an offline proxy](detector-literature-and-proxy.md).

This repository's 11 November 2026 note already records [Adam et al.](https://arxiv.org/html/2602.13042v1): GPTZero is a supervised classifier with Human, AI, and Mixed classes, and that paper's Table 1 is version 4.1b. A result about DetectGPT, Binoculars, or an older GPTZero build does not transfer to a 120-word email on 5.0b unless the paper measured that case. None of the papers opened for this update did.

## Polishing and editing

[Saha and Feizi, “Almost AI, Almost Human”](https://arxiv.org/html/2502.15666) (arXiv:2502.15666). Extremely minor edits with Llama-2-7B raised the share of human-written samples flagged as AI to 32.31% for ZeroGPT, 42.56% for Pangram, and 64.71% for GPTZero. The human texts come from MixSet, six domains, 50 samples each, written before widespread LLM use. One domain is the Enron email set. The 64.71% figure is the polished sample as a whole, not an Enron-only rate, and it is not a Model 5.0b document confidence.

[Beemo](https://arxiv.org/abs/2411.04032) (Artemova et al., arXiv:2411.04032, NAACL 2025). The benchmark has 6.5k human, machine, and expert-edited texts, plus 13.1k machine-generated and LLM-edited texts. The abstract's finding, from 33 detector configurations, is that expert editing evades machine-text detection, while LLM-edited text is unlikely to be recognised as human-written.

[EditLens](https://arxiv.org/abs/2510.03154) (Thai, Emi, Masrour, and Iyyer, arXiv:2510.03154). Thai, Emi, and Masrour are affiliated with Pangram Labs in the paper. EditLens is a regression model for how much AI editing a text has had, trained with similarity metrics as intermediate supervision. The abstract reports binary F1 94.7% and ternary F1 90.4% for human, AI, and mixed writing. On the APT-Eval polish set the paper reports a 0.606 correlation with edit magnitude, against 0.491 for Pangram used as a binary baseline. It is a measure of editing, not a GPTZero score and not a rewrite instruction.

## Synonyms, invisible characters, and humanisers

[“Attacking Only Half the Data”](https://arxiv.org/html/2610.18151v1) (arXiv:2610.18151, October 2026). Synonym substitution, a median of 21% of words, hurts probability-based detectors: Binoculars drops 0.181 AUROC, and its true-positive rate at a 1% false-positive rate falls from 0.74 to 0.30. The paper says the same attack barely affects trained classifiers, because they use word choice and style rather than token probabilities. Zero-width characters and homoglyphs can be stripped. After the attack, and before that cleanup, a log-likelihood detector flagged 98% of attacked human texts at a threshold set to 1% of clean human text. The confidence interval runs to 1.00, and the abstract says attacked human text was misclassified at rates up to 100%. Sanitization removes the Unicode attacks. The detectors named in that section are log-likelihood, log-rank, Binoculars, Lastde, Fast-DetectGPT, and a RoBERTa classifier. GPTZero is not one of them.

[“Humanized but Still True?”](https://arxiv.org/html/2611.00359v1) (arXiv:2611.00359, November 2026). In the October 2026 cycle of a public humaniser leaderboard, 10 of 11 commercial tools altered at least one number or name in 20% or more of the documents that contained one. The document rates for numbers and names alone were 11–58%; only hix-bypass fell to 11%. The paper found no reliable trade-off between keeping those units and evading the detectors it ran. Those detectors were two perplexity methods, a GPT-2-era classifier, RADAR, and a decision model. GPTZero 5.0b was not among them.

## Base models, formal prose, and legal prose

[HIP / “Base Models Look Human To AI Detectors”](https://arxiv.org/html/2605.19516v1) (Xu et al., arXiv:2605.19516). Already cited in this repository. For Llama-3-8B continuations of human-written prefixes, GPTZero's human probability was 96.7% on the base model and 30.3% on the instruct model. Pangram was 98.8% and 17.1% on the same split. The score is on the continuation, not on the prefix. The paper does not identify Model 5.0b. The local 0.6B adapter pilot in this repository failed factual review and was not adopted.

[“Amplifying, Not Learning”](https://arxiv.org/html/2605.21653) (arXiv:2605.21653). A fine-tuned ELECTRA detector rated the median formal-native human essay, from Ghostbuster, n=600, at 99.5% AI, and cleared a genuine high-temperature AI set at 10.5% AI. The paper also says chatgpt-detector-roberta flagged 56% of formal essays at a 1% false-alarm rate. These are open fine-tuned detectors, not GPTZero 5.0b.

[“The Perplexity Trap”](https://arxiv.org/html/2607.13044) (arXiv:2607.13044). On granted EPO patent claims, three open detectors each exceeded a 60% false-positive rate: Binoculars 78.3%, Fast-DetectGPT 61.3%, DetectGPT 80.5%. The paper names GPTZero as a detector that needs a larger GPU than the consumer card under test. It does not report a GPTZero score on those claims. The over-flag is about the open detectors that were run, on claim text written to be clear and concise.

## Vendor release notes

[GPTZero's model release notes](https://gptzero.me/news/ai-detection-model-api-updates), fetched 13 November 2026. These are vendor claims, not measurements of our emails.

| Model | Released | Vendor claim used here |
| --- | --- | --- |
| 5.0b (`2026-11-04-base`) | 4 November 2026 | Improved performance on polished and AI-paraphrased sub-classes; lower false-positive rates; a larger detection architecture |
| 4.2b (`2026-02-14-base`) | 16 February 2026 | Decreased reliance on special characters |
| 4.1b (`2026-01-20-base`) | 20 January 2026 | Improved robustness to named entities; also classic texts, Q&A, reviews, legal, and government documents |
| 3.14b (`2025-11-28-base`) | 28 November 2025 | Increased robustness against word swapping |

## Older results

[DAMAGE](https://ar5iv.labs.arxiv.org/html/2501.03437) (Masrour, Emi, and Spero, arXiv:2501.03437, GenAIDetect 2025). On academic text, at a fixed 5% false-positive rate, GPTZero's true-positive rate fell from 99.73% (±0.19) on AI text to 60.04% (±1.80) on humanised AI text. At the models' own thresholds the same table's appendix lists GPTZero at 95.60% and 34.53%. That is a true-positive rate on an academic benchmark, not a document AI-percent on a short email, and the GPTZero build is the one available to that paper.

[Jabarian and Imas, “Artificial Writing and Automated Detection”](https://www.nber.org/system/files/working_papers/w34223/w34223.pdf) (NBER Working Paper 34223, 2025). Pangram's AUROC on shorter passages in their sample never falls below 0.9979, and the paper says Pangram still does well on stubs under 50 words. GPTZero's AUROC approaches 0.96 on shorter passages. The introduction says GPTZero and OriginalityAI are not suitable for those stubs and are susceptible to humanisers. The [Becker Friedman Institute summary](https://bfi.uchicago.edu/wp-content/uploads/2025/10/Artificial-Writing-and-Automated-Detection.pdf) of the same working paper says GPTZero's false-negative rate after StealthGPT was around 50% and above across most genres and models. A quoted AUROC band of 0.78–1 for texts under 50 words was not in the working paper or that summary, so it is not repeated. These are older models than 5.0b.

## What transfers to a short email on GPTZero 5.0b

**Carries over as a reason to refuse an edit, not as a score.**

- A whole-text polish or LLM rewrite is a bad default for fact-dense mail. Saha and Feizi show an earlier GPTZero flagging lightly polished human text. Beemo's abstract says LLM-edited text is unlikely to be read as human. The vendor says 5.0b targets polished and AI-paraphrased text; that sentence is a vendor claim. Stage 16 is the check that matters for this skill: the human draft and 11 rewrites of one pot complaint, including one built from a human-scoring email, all scored 100% AI, while the untouched control stayed at 3%.
- Do not send a candidate that changed a number, a date, a price, an order ID, or a capitalised name. The November 2026 humaniser audit found that evasion and fact-keeping were unrelated, and 10 of 11 commercial tools crossed a 20% document rate for altered numbers or names. That audit did not run 5.0b. The skill's fact check is the local guard, and it does not predict a score.
- Do not use synonym lists or invisible characters as a detector lever. The October 2026 attack paper found synonym swaps effective against probability detectors and weak against trained classifiers, and it found that cleanup strips invisible characters. GPTZero's notes claim robustness to word swapping since 3.14b and less reliance on special characters since 4.2b. Those notes are vendor claims. Stage 16 did not test a synonym swap. That test is still a proposed experiment.
- Formal and legal register can be over-flagged by the open detectors in the essay paper and the patent paper. Neither paper scored GPTZero 5.0b. In Stage 16 the legal-style rewrite scored 100% AI, and so did every other fresh style, so the batch does not isolate register. Preferring plain first person and shorter legal boilerplate stays a readability hypothesis.

**Does not transfer.**

- DAMAGE's drop from 99.73% to 60.04% is a true-positive rate at a 5% false-positive rate on academic text, on an older GPTZero. It is not a 5.0b AI-percent, and it is not permission to humanise a complaint.
- The StealthGPT result of about 50% missed is the BFI summary of Jabarian and Imas, on the GPTZero they tested in 2025. It is not Model 5.0b, and the summary does not audit whether the humaniser kept every fact.
- HIP's 96.7% versus 30.3% is a continuation score for Llama-3-8B under human prefixes, on whatever GPTZero the authors called in May 2026. It is not a rewrite of a 120-word complaint on 5.0b. Stage 16's rewrite built from a human-scoring email still scored 100% AI.
- EditLens measures edit amount. It does not say which sentence to change, and it was not run on these emails.
- The stub result in Jabarian and Imas is about passages under 50 words. The Stage 16 texts are about 120 to 178 words. A short-text paper does not describe those scans.
- None of these sources is a repeatable way to make GPTZero 5.0b call a fact-complete retailer email human-written.
