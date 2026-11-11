# Detector literature and an offline proxy

Checked November 11, 2026. This note summarises published work on how AI-text detectors score a document, and on attacks those papers actually measured. It then describes an optional local proxy and a plan for training one later. Nothing here is a GPTZero result, a promise that a wording will score as human, or a reason to change a fact.

The short-email scans in the last section were reported with this task. Their texts and receipts are not in `studies/`. The archived comparison uses only files already in the repository.

## What current detectors are doing

Several families are easy to mix up because they all return a single "AI" number. They do not estimate the same thing.

### Perplexity, burstiness, and rank

Early detectors asked how surprising a text was to a language model. [GLTR](https://arxiv.org/abs/1906.04043) (Gehrmann, Strobelt, and Rush, 2019) visualises the rank of each token under a model such as GPT-2. Low, smooth surprise was the machine-like pattern. "Burstiness" was the variation of that surprise across sentences: human prose was described as more uneven.

GPTZero's own support page, fetched November 11, 2026, says that as of autumn 2023 it no longer uses perplexity or burstiness, because detection moved to a deep-learning architecture. The page points at the technical report below. It does not say whether sentence length or vocabulary still affects the score. Historical thresholds on that page are not current instructions. [Support page](https://support.gptzero.me/articles/9585228410-how-do-i-interpret-burstiness-or-perplexity)

### DetectGPT and Fast-DetectGPT

[DetectGPT](https://arxiv.org/abs/2301.11305) (Mitchell et al., ICML 2023) does not train a classifier. It uses the source model's log probabilities. Machine samples tend to sit in regions of negative curvature: small rewrites, produced by masking with T5, usually have lower log probability than the original. On fake news from 20B GPT-NeoX, the paper reports AUROC moving from 0.81 for the strongest zero-shot baseline to 0.95 for DetectGPT. The method needs many perturbation passes. It is a property of one source model, not a measurement of GPTZero.

[Fast-DetectGPT](https://arxiv.org/abs/2310.05130) (Bao et al., ICLR 2024) replaces those rewrites with one forward pass. At each token it compares the conditional log probability of the observed token with alternative tokens drawn from the same context. The paper calls the normalised gap conditional probability curvature. When the sampling model and the scoring model are the same, the numerator is the sum of two older baselines, likelihood and entropy. The paper reports about a 75% relative improvement over DetectGPT and about a 340-fold speed-up, in both a white-box setting (the source model) and a black-box setting (a surrogate). Its Figure 1, on 30-token prefixes from XSum, shows machine curvature near 3 and human curvature near 0. That is one dataset and one prefix length, not a result about a 100-word email or about GPTZero.

### Binoculars

[Binoculars](https://arxiv.org/abs/2401.12070) (Hans et al., 2024) also trains nothing. Two language models that share a tokenizer both score the text. Perplexity is how surprising the observed tokens are to one model. Cross-perplexity is how surprising the other model's next-token distribution is to the first, token by token. The score is the ratio of those two log quantities (their equation 4). The default pair is Falcon-7B-Instruct in the numerator and Falcon-7B with Falcon-7B-Instruct in the cross-perplexity. Machine text scores lower: the capybara example in their Table 1 is 0.73, under a global threshold of 0.901, while raw perplexity on that prompt-dependent passage was high. The paper reports detecting over 90% of ChatGPT samples at a 0.01% false-positive rate, without ChatGPT training data. The length plot in the paper is at 128, 256, and 512 tokens. A firm email of about 100 words is shorter than the left edge of that plot. The ratio does not transfer to a pair of models that do not share a tokenizer.

### Feature classifiers and finetuned encoders

[Ghostbuster](https://arxiv.org/abs/2305.15047) (Verma et al., NAACL 2024) runs the document through weaker language models, searches combinations of those probability features, and trains a linear classifier. It does not need the source model's logits. The paper reports 99.0 F1 across its essay, creative-writing, and news sets, 5.9 F1 above the best preexisting model in that comparison, and an average margin of 23.7 F1 over DetectGPT and GPTZero. It also tests non-native English writing. Those are the authors' datasets and the GPTZero version they could call in 2023, not Basic 4.9b or 5.0b.

[RADAR](https://arxiv.org/abs/2307.03838) (Hu, Chen, and Ho, NeurIPS 2023) trains a paraphraser and a detector against each other. The paraphraser tries to evade the detector; the detector trains on the paraphraser's output. The paper evaluates eight open models (Pythia, Dolly, Palmyra, Camel, GPT-J, LLaMA, Vicuna, and an earlier Dolly) on four datasets, and reports transfer from instruction-tuned models to others. A public Vicuna-7B checkpoint exists. It is not a small CPU proxy, and this repository does not run it.

Finetuned encoder classifiers are a separate family:

- The [OpenAI RoBERTa detector](https://huggingface.co/openai-community/roberta-base-openai-detector) is RoBERTa-base finetuned to separate GPT-2 1.5B output from WebText, as described in the [GPT-2 release report](https://arxiv.org/abs/1908.09203) (Solaiman et al., 2019). The model card says a detection rate around 95% on GPT-2 1.5B is not enough to stand alone, and it says not to use the model as a ChatGPT detector when the consequence is an accusation. Label 0 is "Fake" and label 1 is "Real".
- [HC3 RoBERTa](https://huggingface.co/Hello-SimpleAI/chatgpt-detector-roberta) (Guo et al., [HC3](https://arxiv.org/abs/2301.07597), 2023) is RoBERTa-base finetuned for one epoch on human and ChatGPT answers, including split sentences. Its card does not declare a license. Labels are "Human" and "ChatGPT".
- [Fakespot RoBERTa](https://huggingface.co/fakespot-ai/roberta-base-ai-text-detection-v1) is another RoBERTa-base finetune. Its card says a cleaning function improves results. The proxy scores the raw text and records that the cleaning step was not applied.
- [Desklib v1.01](https://huggingface.co/desklib/ai-text-detector-v1.01) and [Oculus v2](https://huggingface.co/danibor/oculus-v2.0-multilingual) are DeBERTa-v2 models with a masked-mean pool and one logit. Oculus's card describes distillation from GPTZero labels. That does not make the checkpoint GPTZero Basic 4.9b or 5.0b. The skill's pinned Desklib scorer is documented in [local-detector.md](../skills/anti-ai-detection-writing-skill/references/local-detector.md).

[Pangram's 2024 technical report](https://arxiv.org/abs/2402.14873) describes a trained transformer and lists email among its domains. The [Pangram 4 report](https://arxiv.org/abs/2607.27183) excludes short conversational replies under 50 words. Neither report is a measurement of our emails or of GPTZero.

### What GPTZero says about itself

[GPTZero: Robust Detection of LLM-Generated Texts](https://arxiv.org/abs/2602.13042) (Adam et al., February 13, 2026) describes a supervised detector, not a perplexity score. A document is classified as Human, AI, or Mixed. Under AI, the report names finer classes: Pure AI, Polished (human text edited by a model), and AI Paraphrased. A document is also a sequence of sentences, with a document loss plus a sentence loss. The Mixed class is how the product separates "half the words are AI" from "the model is unsure". Architecture and hyperparameters are proprietary. The report's Table 1 is version 4.1b. Our archived scans display Basic 4.9b. The short-email scans below display 5.0b. The paper does not say which of those changes touched the decision rule.

The robustness section says training includes paraphrasing prompts, translation chains, DIPPER and TempParaphraser outputs, black-box humaniser services, and white-box word substitution of the kind in Zhou et al. (2024). Before scoring, the pipeline strips extra whitespace, splits over-long documents into windows, and remaps probabilities. Deep Scan attributes the document score to sentences. The report distinguishes that attribution from the sentence-level class. A highlighted sentence is not, on the paper's own account, a rewrite instruction.

[Chakraborty et al.](https://arxiv.org/abs/2304.04736) (2023) argue that detection stays possible unless human and machine text are indistinguishable on their whole support, and that the number of samples required grows as machine text gets closer to human text. They evaluate RoBERTa detectors and GPTZero and say the length effect matches OpenAI's earlier empirical observations. The paper does not give a word count at which a current GPTZero scan becomes informative.

## Evasion results, and what they measured

These papers change the text and then measure a detector. "Bypass" in a table is the paper's own metric, usually a true-positive rate or AUROC on that paper's set. It is not a GPTZero document confidence, and it is not evidence that the same edit preserves every fact.

| Work | What was changed | Detectors in the paper | What the paper reports | Length |
| --- | --- | --- | --- | --- |
| [DIPPER](https://arxiv.org/abs/2303.13408) (Krishna et al., NeurIPS 2023) | An 11B paragraph paraphraser with lexical and order controls | Watermarks, DetectGPT, OpenAI's classifier, GPTZero, RankGen | At a 1% false-positive rate on 300-token Wikipedia continuations, GPTZero's detection accuracy was already low before paraphrasing (13.9% on GPT-2, 8.7% on OPT-13B, 7.1% on GPT-3.5) and fell to 1.2%, 1.0%, and 1.8% at the most diverse setting. DetectGPT on GPT-2 fell from 70.3% to 4.6%. Semantic similarity stayed high on their automatic metric. | About 300 tokens |
| [Recursive paraphrasing](https://arxiv.org/abs/2303.11156) (Sadasivan et al., TMLR) | Repeated neural paraphrases, including of DIPPER output | Watermarks, DetectGPT-style zero-shot, OpenAI's 2019 classifier, a retrieval detector | On passages of about 300 tokens, detection fell across those families. Their retrieval detector, built to survive paraphrases, fell from 100% accuracy to below 60%. In the human study, 77% of the recursive paraphrases were rated high quality. The paper also shows a watermark spoofing attack and a bound relating the best AUROC to the distance between human and machine text. | About 300 tokens |
| [SICO](https://arxiv.org/abs/2305.10847) (Lu et al., TMLR) | A prompt built from 40 human examples | Six detectors, including finetuned classifiers | GPT-3.5 with that prompt lowered AUC by about 0.5 on average. Human raters judged readability and task completion. | Task passages, not 100-word mail |
| [Red teaming](https://arxiv.org/abs/2305.19713) (Shi et al., TACL) | Synonym substitution, or a searched style prompt | The detectors in that study | Both strategies degraded every detector they tested. The auxiliary model can itself be behind a detector. | Not a short-email set |
| [Stumbling Blocks](https://arxiv.org/abs/2402.11638) (Wang et al., 2024) | Editing, paraphrasing, prompting, co-writing, at several budgets | A panel of then-current detectors | About a 35% average drop across detectors and attacks. No detector stayed robust to all of them. | Mixed |
| [Word and sentence substitution](https://arxiv.org/abs/2402.00412) (Peng et al., EMNLP 2023) | Automatic substitution in student essays | Detectors available for that paper | Straightforward substitution evaded the detectors while the essays stayed fluent on their checks. | Essays |
| [Adversarial word swap](https://arxiv.org/abs/2404.01907) (Zhou, He, and Sun, COLING 2024) | Small word substitutions, white-box or black-box, with a perplexity constraint | Detectors they attack | Some models were driven to a human classification in about 10 seconds. Adversarial training helped only partly. GPTZero's 2026 report cites this attack as training data, so a 2024 bypass is not a 2026 result. | Not reported as 100-word mail |
| [RAFT](https://arxiv.org/abs/2410.03658) (Wang et al., EMNLP 2024) | Grammar-preserving word substitution chosen with an embedding | The detectors in that study | Up to a 99% drop, and the substitutions transferred across source models. Human raters did not reliably distinguish them. | Mixed domains |
| [RAID](https://arxiv.org/abs/2405.07940) (Dugan et al., ACL 2024) | A benchmark, not one attack: 11 models, 8 domains, 11 attacks, 4 decoding strategies, over 6 million generations | 8 open and 4 closed detectors | Detectors that look strong on a friendly set fail under attacks, sampling changes, repetition penalties, and unseen generators. | Benchmark domains, not this email set |
| [Non-native English](https://arxiv.org/abs/2304.02819) (Liang et al., Patterns 2023) | TOEFL essays, plus simple prompts | Several widely used detectors, including GPTZero as it then was | Non-native essays were systematically called AI. Simple prompts both reduced that bias and bypassed detectors. | Essays |
| [Tool survey](https://arxiv.org/abs/2306.15666) (Weber-Wulff et al., International Journal for Educational Integrity, 2023) | Coursework, plus translation and light obfuscation | 12 public tools, Turnitin, PlagiarismCheck | The tools were not reliable. Errors leaned toward calling text human. Obfuscation made them worse. | Course documents |
| [Adversarial Paraphrasing](https://arxiv.org/abs/2506.07001) (Cheng et al., 2025) | Detector-guided token generation | Eight open detectors, not GPTZero | Aggregate detection rates on their set. The authors' quality rubric allows minor factual changes at rating 4, so a high rating is not exact claim preservation. Already discussed in the [detector research note](../skills/anti-ai-detection-writing-skill/references/detector-research.md). | Not this email set |

Two negative results belong next to that table. [MPU](https://arxiv.org/abs/2305.18149) (Tian et al., ICLR 2024) says mainstream detectors fail on short texts such as SMSes, tweets, and reviews, and treats some short machine text as too human-like to label cleanly. [Mitrović, Andreoletti, and Ayoub](https://arxiv.org/abs/2301.13852) (2023) get about 79% accuracy on short reviews, worse when the model rephrased a human review than when it wrote from a prompt. Their SHAP notes describe the ChatGPT reviews as polite, short on specifics, and lexically showy. That is a description of one review set, not a list of words to delete. [Mireshghallah et al.](https://arxiv.org/abs/2305.09859) (2023) report that a small surrogate can beat a larger one as a black-box detector: OPT-125M had AUC 0.81 on ChatGPT text where GPT-J-6B had 0.45. Small does not mean useless. It also does not mean the small model agrees with GPTZero.

The pattern across the evasion papers is that a detector evaluated on clean in-domain text looks stronger than the same detector after paraphrase, substitution, or a change of generator. GPTZero's 2026 report says it now trains on DIPPER, humanisers, and substitution attacks. A bypass measured before that training does not carry over. None of these papers measured a fact-preserving edit of an 85–120 word UK refund email on Model 5.0b.

## What the archived GPTZero scans can support

`scripts/proxy_detector.py corpus` walks `studies/` and keeps a GPTZero observation only when the AI, mixed, and human figures sit on an object marked GPTZero and a file in `studies/` matches a checksum. The checksum is the one stored on that object, or, when the score object has none, the parent record's `input_sha256`. A rendered hash on the same record is not used, because it can name a different text. Exact repeats collapse. Conflicting scores for the same bytes would be reported and excluded; there are none.

The run used for this note found **112** files with distinct checksums, all Basic Scan, Model **4.9b**. Five pairs differ only by trailing newlines, so correlations use **107** texts. **101** are 100% AI. **11** are below the ceiling: 0, 0, 1, 11, 40, 67, 91, 91, 93, 93, and 93. The two 91s are the same Python answer; the editor copy has two extra trailing newlines. Five texts are under 100 words, and all five are 100% AI. Fifty-two texts are 130 words or shorter, and only those two 91s and the 67 are below the ceiling inside that band. The two 0% texts are the business answers from the model-assisted study (148 and 150 words), not short emails.

Six score objects in `studies/pangram-transfer-1/results.json` have no hash of their own. The join uses the parent `input_sha256`. Two of those inputs were already present: the `qwen-1942` plain text at 100% AI and the quoted text at 1% AI. The other four are new to the correlation. They are the kubernetes-probe-roles and postgresql-snapshot-scope original and direct editor files, at 164, 181, 180, and 178 words. Each recorded score is Basic Scan, Model 4.9b, 100% AI, 0% mixed, and 0% human, and the recorded word count matches the file. The two originals are byte-identical to copies under `studies/requested-alternatives-1/inputs/`, so the join keeps one path. Pangram proportions are a different unit and are not mixed in.

The ten pairs frozen in [open-detector-proxy-1](../studies/open-detector-proxy-1/README.md) all resolve onto this set. Three of them fall by at least five GPTZero points: 100 to 93 (a quotation added), and 100 to 0 twice on the same business case. The other seven are exact ties at 100. That five-point bar is the one that study declared before its own local scores.

The September 7 Desklib diagnostic, recorded in [local-detector.md](../skills/anti-ai-detection-writing-skill/references/local-detector.md), scored eight AI-origin development texts between 0.0123 and 0.1861, all below the card's 0.5 line, including seven that Pangram had called 100% AI. That was already a class disagreement. The proxy run below asks the same question against the 112 GPTZero texts, with the model files kept outside the repository.

## The optional proxy

`skills/anti-ai-detection-writing-skill/scripts/proxy_detector.py` is not imported by the skill. Its torch and transformers pins live in the script header, the same way the Desklib scorer's pins do. `python3 -m unittest discover -s tests` does not download a model and does not import torch. The tests check the corpus, the published Binoculars ratio, the analytical curvature formula, and the pair summary.

The score command reads a local Hugging Face snapshot index. It does not download weights. Each metric is oriented so that a higher number means "more AI" before it is compared with GPTZero's AI percent. The raw direction is stored with the metric.

| Metric | Models | Raw direction | Why it is here |
| --- | --- | --- | --- |
| Log perplexity | DistilGPT-2, GPT-2, GPT-2 medium, SmolLM2-360M, Qwen2.5-0.5B | Higher means more surprising | The feature GPTZero says it stopped using in autumn 2023 |
| Conditional curvature | The same five, one forward pass, sampling model equal to scoring model | Higher means more machine-like in Bao et al. | Fast-DetectGPT's same-model formula |
| Sentence burstiness | Stdev of per-sentence mean log probability on the same forwards | Higher was the old "human" story | A negative control for the abandoned feature |
| Binoculars ratio | GPT-2 over DistilGPT-2, GPT-2 medium over GPT-2, SmolLM2-360M-Instruct over the base, Qwen2.5-0.5B-Instruct over the base | Lower means more machine-like in Hans et al. | Same-family pairs only, because the tokenizer must match |
| RoBERTa classifiers | OpenAI GPT-2 detector, HC3 ChatGPT detector, Fakespot | Higher means the card's AI label | The finetuned-encoder family, at base size |
| Mean-pool detectors | Desklib v1.01 (768-token limit) and Oculus v2 (512-token limit) | Higher means the AI logit | The local detectors this repo already tried |

Over-length inputs are left unscored rather than truncated. RoBERTa's limit is 512 tokens, so the long articles drop out of those three metrics. Two public-domain paragraphs already in the proxy study (Darwin and Carroll) are scored as human controls. They have no GPTZero label and are not part of the correlation.

Ranking agreement was declared before looking at the scores: Spearman correlation of the oriented score with GPTZero AI percent; the same correlation on the texts under 100; the fraction of those below-ceiling texts that fall under the median score of the 100% texts; and, on the ten archived pairs, how many of the three drops of at least five points the proxy also lowers, and how many of the seven exact ties it lowers anyway. Trailing-newline duplicates are counted once in the correlations.

Run the scores only when the snapshots are already on disk:

```sh
python3 skills/anti-ai-detection-writing-skill/scripts/proxy_detector.py corpus \
  --root . --output studies/detector-proxy-1/corpus.json
python3 skills/anti-ai-detection-writing-skill/scripts/proxy_detector.py score \
  --root . --model-index /path/to/model-index.json \
  --output studies/detector-proxy-1/scores.json
python3 skills/anti-ai-detection-writing-skill/scripts/proxy_detector.py report \
  --root . --scores studies/detector-proxy-1/scores.json \
  --output studies/detector-proxy-1/report.json
```

## Proxy evaluation

One CPU run, torch 2.8.0+cpu, float32, no truncation. The report is [studies/detector-proxy-1/report.json](../studies/detector-proxy-1/report.json). Correlations count a text once after stripping trailing newlines: 112 files, 107 texts. Six texts are longer than 512 tokens. They are left unscored for the three RoBERTa classifiers and for Oculus, and all six are 100% AI, so those four metrics have n=101 and still include all 10 unique below-ceiling texts. Every other metric scores all 107. The two public-domain controls are scored and kept out of the correlations.

The comparisons below were declared before the scores were read. Spearman uses the oriented score against GPTZero AI percent. "Below median" is the share of the 10 below-ceiling texts that fall under the median oriented score of the ceiling texts. "Drops caught" counts how many of the three archived reductions of at least five points the proxy also lowered. "Ties lowered" counts how many of the seven exact 100-to-100 pairs it lowered. A decrease of any size counts, including a few thousandths. The five-point bar and a zero margin give the same two counts, because the three reductions are 7, 100, and 100 points. Figures are rounded to three decimals from the report.

These are not a second GPTZero scan and not an accuracy claim about human writing. Most texts sit on the 100% ceiling, the texts share a handful of topics, and the two business drops are the same case written twice.

| Metric | n | Spearman | Spearman under 100 | Below median | Drops caught | Ties lowered |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `classifier__hc3_roberta` | 101 | 0.131 | −0.129 | 0.800 | 1/3 | 1/7 |
| `classifier__fakespot_roberta` | 101 | 0.111 | −0.191 | 0.600 | 2/3 | 4/7 |
| `binoculars__gpt2_distilgpt2` | 107 | 0.071 | 0.419 | 0.600 | 1/3 | 3/7 |
| `distilbert__distilgpt2__curvature` | 107 | 0.063 | −0.185 | 0.500 | 0/3 | 4/7 |
| `openai-community__gpt2__curvature` | 107 | 0.062 | 0.800 | 0.600 | 0/3 | 1/7 |
| `binoculars__gpt2medium_gpt2` | 107 | 0.053 | 0.394 | 0.500 | 0/3 | 4/7 |
| `Qwen__Qwen2.5-0.5B__log_perplexity` | 107 | 0.025 | 0.529 | 0.500 | 1/3 | 1/7 |
| `HuggingFaceTB__SmolLM2-360M__log_perplexity` | 107 | 0.021 | 0.554 | 0.500 | 2/3 | 2/7 |
| `classifier__openai_roberta` | 101 | −0.008 | 0.585 | 0.500 | 2/3 | 3/7 |
| `openai-community__gpt2__log_perplexity` | 107 | −0.012 | 0.554 | 0.500 | 0/3 | 1/7 |
| `openai-community__gpt2-medium__log_perplexity` | 107 | −0.017 | 0.554 | 0.500 | 0/3 | 1/7 |
| `desklib__ai_probability` | 107 | −0.034 | 0.234 | 0.500 | 1/3 | 5/7 |
| `Qwen__Qwen2.5-0.5B__curvature` | 107 | −0.035 | 0.135 | 0.200 | 1/3 | 2/7 |
| `openai-community__gpt2-medium__curvature` | 107 | −0.055 | 0.726 | 0.500 | 0/3 | 1/7 |
| `oculus__ai_probability` | 101 | −0.060 | 0.468 | 0.400 | 3/3 | 4/7 |
| `HuggingFaceTB__SmolLM2-360M__curvature` | 107 | −0.061 | 0.037 | 0.400 | 1/3 | 2/7 |
| `distilbert__distilgpt2__log_perplexity` | 107 | −0.071 | 0.652 | 0.300 | 1/3 | 1/7 |
| `binoculars__qwen2.5_0.5b` | 107 | −0.084 | −0.135 | 0.300 | 3/3 | 3/7 |
| `distilbert__distilgpt2__burstiness` | 107 | −0.107 | −0.683 | 0.300 | 2/3 | 5/7 |
| `Qwen__Qwen2.5-0.5B__burstiness` | 107 | −0.109 | −0.566 | 0.400 | 0/3 | 4/7 |
| `binoculars__smollm2_360m` | 107 | −0.113 | 0.172 | 0.300 | 2/3 | 4/7 |
| `openai-community__gpt2__burstiness` | 107 | −0.137 | −0.542 | 0.100 | 0/3 | 5/7 |
| `openai-community__gpt2-medium__burstiness` | 107 | −0.157 | −0.542 | 0.200 | 0/3 | 5/7 |
| `HuggingFaceTB__SmolLM2-360M__burstiness` | 107 | −0.192 | −0.775 | 0.200 | 0/3 | 4/7 |

The strongest overall Spearman is **0.131**, HC3 RoBERTa, on 101 texts. That is not a ranking to spend a scan on. HC3's probabilities sit near zero: the median on the 91 ceiling texts it scored is 0.0018, and 5 of those 91 reach 0.5. The drop it catches is the quotation pair, 0.00088 to 0.00050. On both business pairs, where GPTZero fell from 100 to 0, HC3's score went up. Fakespot, scored on the raw text because its card's cleaning step was not applied, is the next Spearman at 0.111 and lowers 4 of the 7 ties.

GPT-2 curvature has Spearman 0.800 on the 10 below-ceiling texts, and GPT-2 medium curvature has 0.726. Both catch **0 of 3** paired drops. On every archived reduction the curvature moved the wrong way: the candidate scored more machine-like after an edit that GPTZero scored as less AI. Overall Spearman is 0.062 and −0.055. The Darwin and Carroll controls score 0.450 and 1.587, both on the machine side of the ceiling-text median (−0.623). Cross-section among ten dependent documents is not a paired ranking, and it does not put those paragraphs on the human side of the AI texts.

Qwen2.5-0.5B Binoculars catches 3 of 3 drops and also lowers 3 of 7 ties. The three catches are raw moves of +0.003, +0.009, and +0.019. Labelled texts on that metric span 0.974 to 1.272. Overall Spearman is −0.084. Carroll scores 0.928, more machine-like than every labelled text, and Darwin scores 0.987. The Falcon-7B ratio in Hans et al. is not what this 0.5B pair is doing. Sentence burstiness is at or below zero on every model in the table. Log perplexity is not: Qwen2.5-0.5B is +0.025 and SmolLM2-360M is +0.021, and the other three log-perplexity rows are below zero. GPTZero's support page says it stopped using those features in autumn 2023.

Oculus catches 3 of 3 and lowers 4 of 7 ties, including pair 06, the technical edit whose GPTZero score stayed at 100 (0.173 to 0.023). On the ten pairs and both controls, these 22 probabilities are within 0.000002 of the full-precision values in [oculus/results.json](../studies/open-detector-proxy-1/oculus/results.json). On the wider set, 3 of 91 ceiling texts are at or above 0.5. Spearman is −0.060. Catching the drops by also moving the ties is the same failure that study already recorded.

Desklib, the skill's pinned local detector, has Spearman **−0.034**. The median probability on the 97 ceiling texts is 0.054. Four of those 97 are at or above 0.5, and so is one below-ceiling text (0.961 on a quotation GPTZero scored at 93%). The September 7 note that eight development texts all fell under 0.5 still describes those eight. This run does not pad to 768. [desklib-pad-parity.json](../studies/detector-proxy-1/desklib-pad-parity.json) compares the unpadded logit with the skill's padded scorer on three texts: a four-word sentence, the Carroll paragraph, and one business answer. The largest absolute difference in that file is 2.38×10⁻⁶, on the business answer. The archive does not make Desklib a GPTZero ranker.

The OpenAI GPT-2 detector's median on its 91 ceiling texts is 0.0002. Two of them exceed 0.5. `scores.json` records the head that was scored: label 0 is Fake, label 1 is Real, and the metric uses index 0. A GPT-2-versus-WebText detector calling later prose Real is the limit stated on its own card.

No metric both ranks the AI percents and catches the paired drops without also moving the ties. None of the five texts under 100 words leaves 100% AI, so this run cannot say how a proxy would order a short firm email. The Model 5.0b email report below is not in this correlation.

## Training a small mimic of GPTZero

Not done here. No cloud account was used and no instance was started. The prices below are a planning estimate.

### What the labels would have to be

A model that mimics GPTZero has to be trained on GPTZero labels, and the label has to name the displayed model. The 112 joined texts are Basic 4.9b. The emails in the redacted receipt below were scored on 5.0b. A 4.9b mimic is a different task. The labels also have to keep AI, mixed, and human apart: the archived 1% AI text was 99% mixed and 0% human, so an "AI percent only" target throws away the result that mattered.

The joined archive is a poor training set for the email problem. One hundred and one of the 112 files are 100% AI. The eleven that are not are two business answers at 0% (148 and 150 words), two copies of the Python baseline at 91 (the same paragraph; the Python candidate is 100% AI), five quotation texts (1, 40, 67, 93, and 93), and two unpaired `mattpocock/skills` answers with no baseline and no unquoted control: `mattpocock-285/final.txt` at 11% and `mattpocock-231/final.txt` at 93%. Five of those eleven files are quotation texts. None of the five texts under 100 words leaves the ceiling. Fitting a classifier to that set teaches it to say 100, with a few memorised exceptions.

Do not train on private retailer or customer mail, even when a score already exists. Use public-domain prose and synthetic emails written for the experiment, with no real order, name, or account detail.

A useful sequence is:

1. **Calibration, before any training.** About 50 public-domain paragraphs of 80–160 words, and about 50 synthetic firm emails that share one fact sheet and vary only the wording. Scan them once on the current model (5.0b at the time of this note). Hold out a slice before looking.
2. **Stop if the short emails do not move.** If that set is still all 100 except a single voice, more labels of the same kind will not create a ranking signal. The scan budget is the scarce resource, not the GPU.
3. **Only then collect a training set.** A 125M encoder can memorise a few dozen non-ceiling emails. A few thousand balanced documents is a reasonable band if, and only if, the calibration set shows that scores actually vary. Split by document, and never put an email and its rewrite on opposite sides of the split. Keep the ten archived pairs, and any email used to choose the wording, out of training.
4. **Predict the three confidences.** They sum to about 100 in the archive. Report mixed and human, not a binary "human" flag.

### What the compute would cost

A RoBERTa-base finetune on a few thousand texts of 128 tokens is a short job on a 16 GB GPU: on the order of minutes per epoch once the run is underway. The allowance below is four hours, which covers pulling an image, a failed run, and three small trials. It is an engineering allowance, not a measured training time. A larger decoder is unnecessary for this label set. The 7B RADAR checkpoint is the wrong tool and the wrong price.

Prices were read from [ec2.shop](https://ec2.shop) on November 11, 2026. That site republishes AWS on-demand and spot figures; it is not an AWS bill, and both on-demand and spot move. Sterling uses the ECB reference rate published by [Frankfurter](https://www.frankfurter.app) for the same day: 1 USD = 0.75149 GBP. Confirm the region and the tenancy on the AWS pricing page before launching anything. Spot can be reclaimed; the saving rates below are the ones ec2.shop showed that day.

| Instance | Region | What the price row listed | On-demand USD/h | Spot USD/h | 4 hours on-demand | 4 hours spot |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| g4dn.xlarge | us-east-1 | 4 vCPU, 16 GiB, one T4 16 GB | 0.526 | 0.2204 | £1.58 | £0.66 |
| g4dn.xlarge | eu-west-2 | 4 vCPU, 16 GiB, one T4 16 GB | 0.615 | 0.2057 | £1.85 | £0.62 |
| g5.xlarge | us-east-1 | 4 vCPU, 16 GiB, one A10G 24 GB | 1.006 | 0.5006 | £3.02 | £1.51 |
| g5.xlarge | eu-west-2 | 4 vCPU, 16 GiB, one A10G 24 GB | 1.277 | 0.5164 | £3.84 | £1.55 |

A CPU run is enough for this model size and avoids a GPU quota. On the same price list, us-east-1 `t3.xlarge` (4 vCPU, 16 GiB) was $0.1664/h on demand, about £1.00 for eight hours, and `c7i.2xlarge` (8 vCPU, 16 GiB) was $0.357/h, about £2.15 for eight hours. Eight hours is a guess at a careful CPU finetune plus setup, not a benchmark. Disk for a 125M checkpoint is small beside one instance-hour; the GB-month price should be checked before a volume is left attached, and it is not included above.

The practical budget for a first mimic, if calibration shows that scores vary, is one `g4dn.xlarge` for an afternoon: under £2 on demand in either region above, under £1 on spot. That does not include GPTZero word credits. Those credits are the binding cost, and this note does not invent a credit price.

### Free options

- **Colab.** The [FAQ](https://research.google.com/colaboratory/faq.html), fetched November 11, 2026, says Colab provides free GPU and TPU access, that the resources are not guaranteed, and that usage limits fluctuate. A RoBERTa finetune fits a free GPU session if the session stays up. It is a poor place to put private email.
- **Kaggle.** The notebooks documentation page did not return a GPU-quota figure when fetched the same day, so no weekly hour count is stated here. Check the current quota before relying on it.
- **A CPU you already have.** The proxy script in this repository already runs the small scoring models on CPU. A DistilBERT or RoBERTa finetune on a few thousand short texts can run on CPU as well. It still needs the GPTZero labels, which no free GPU substitutes for.
- **Hugging Face.** Free hosted inference can run a small classifier. It does not supply GPTZero labels.

## What to do with a short firm email

**Redacted receipt, not a method.** [gptzero-5.0b-receipt.json](../studies/detector-proxy-1/gptzero-5.0b-receipt.json) records free-plan GPTZero Model 5.0b scans from 11 November 2026. The texts are withheld. The original has no hash in the receipt. v1–v10 record the sha256 of the scanned file. The receipt says the scan modes differ. The original and v1–v4 were scanned before the free Basic option disappeared. v5–v10 used Advanced AI Scan, after the free advanced review was used, and that mode displays only the overall score. Only the displayed overall classification was recorded. For every 100% text, mixed and human were not recorded.

The original is 85 words, the real chaser as written, at 100% AI. v1–v4 are 103, 107, 105, and 91 words, with strategies casual-polite, recap, "me again", and choppy fragments, each at 100% AI. v5 is 124 words, formal, passive, and nominalised, recorded as 3% AI and 97% human. Mixed is not a field on that row. v6–v10 are 123, 119, 115, 116, and 119 words, each at 100% AI. That is one Advanced AI Scan of one nominalised wording, not a method, and not a reason to copy it. The skill does not use this receipt as a reason to scan again or to skip a scan. In the joined 4.9b set, all five texts under 100 words are 100% AI. Published short-text work (MPU; the length discussion in Chakraborty et al.) says short machine text is hard to separate, which fits a ceiling, not a recipe for beating it.

**What the writer should do.** Keep every fact, qualification, and uncertainty. Leave a draft unchanged when it already answers the question in ordinary words with one ask. If a measured alternative is explicitly requested, one predeclared comparison is the whole experiment: same facts, same ask, and the result reported whether it moves or not, including mixed and human. The offline proxy does not rank the archived 4.9b pairs well enough to choose which wording to scan. That comparison is the evaluation above and [detector-proxy-1](../studies/detector-proxy-1/README.md).
