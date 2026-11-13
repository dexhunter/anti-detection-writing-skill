# Hugging Face survey: existing humanizer and paraphraser models

**Desk survey of model cards.** None of the models below were run by us. Counts, licences, and detector claims are taken from the cited cards, papers, and pages, not from our own runs.

Survey date: 13 Nov 2026, Europe/London. Figures are taken from Hugging Face Hub (`hub_repo_details` / `hub_repo_search` / model and dataset cards) and from the cited papers or pages, as of that date. Download and like counts can change and sometimes differed slightly between Hub tools in the same session; the numbers below prefer `hub_repo_details` when both were available. This survey does not evaluate the models on our emails, and it does not endorse them as a way to pass GPTZero.

Most high-download Hub hits for the query “humanizer” are GGUF redistributions of the same two 12B checkpoints (`jialinyyzz/humanizer` and `abacusai/Smaug-Humanizer`). Those redistributions are omitted here unless they are the canonical weights. A separate cluster of commercial “AI humanizer” websites appears in Hub *datasets* and org pages; those are closed tools, not open weights, and are noted only at the end.

## 1. jialinyyzz/humanizer

- **Repo:** [jialinyyzz/humanizer](https://huggingface.co/jialinyyzz/humanizer) (dataset: [jialinyyzz/humanizer-data](https://huggingface.co/datasets/jialinyyzz/humanizer-data); GGUF pack: [jialinyyzz/humanizer-GGUF](https://huggingface.co/jialinyyzz/humanizer-GGUF); code: [github.com/sgaofen/humanizer-local-model](https://github.com/sgaofen/humanizer-local-model))
- **Base model and size:** fine-tune of `google/gemma-4-12B`. Hub reports about 11,960M parameters (12B class). English and Chinese.
- **Licence:** Apache-2.0 (model card). The training-data repo is tagged `license:other`.
- **Downloads / likes (13 Nov 2026):** 459.0K downloads, 2,260 likes (`hub_repo_details`). This was the most downloaded and most liked open humanizer checkpoint found in this search. The data repo: 873 downloads, 14 likes.
- **Claimed detector results:** the model card (and a copy of the same write-up seen on [npario/humanizer](https://huggingface.co/npario/humanizer)) reports an author-run Originality.ai check, not a GPTZero figure: “95% judged human by Originality.ai at its strictest setting (210 English drafts, bf16 weights, 2026-10-02): 11 of 210 rewrites were flagged as AI, against 26 for the previous release, and no AI detector was used anywhere in training.” A table on the same card also reports “Flagged as AI, same 60 drafts” for several GGUF files (Q8_0: 7/60; Q3-QAT: 4/60; IQ2_XS-QAT: 0/60; bf16: 4/60). The detector used for that 60-draft column is the Originality.ai evaluation described above; the card does not state a GPTZero result.
- **Independently backed?** Not in the sources checked here. The numbers are author-reported. The card points to a published method and held-out outputs on GitHub, which makes the evaluation inspectable, but this survey did not find a third-party replication on GPTZero or Originality.ai.

## 2. abacusai/Smaug-Humanizer

- **Repo:** [abacusai/Smaug-Humanizer](https://huggingface.co/abacusai/Smaug-Humanizer) (GGUF: [abacusai/Smaug-Humanizer-GGUF](https://huggingface.co/abacusai/Smaug-Humanizer-GGUF); blog: [Smaug Humanizer: An open-weight 12B humanizer](https://blog.abacus.ai/blog/2026/10/26/smaug-humanizer-an-open-weight-12b-humanizer/))
- **Base model and size:** fine-tune of `google/gemma-4-12B` (pretrained, not instruction-tuned). Card: 12B, bf16. Hub reports about 11,960M parameters. Training: SFT on 3,676 rewrite pairs, then 200 steps of GRPO. English.
- **Licence:** Apache-2.0.
- **Downloads / likes (13 Nov 2026):** 1.2K downloads, 29 likes (`hub_repo_details`). The GGUF mirror had higher downloads in search results (6.4K) than the full-weight repo.
- **Claimed detector results:** the card says held-out rewrites were scored with [Pangram](https://www.pangram.com) during development, and it shows three example screenshot pairs labelled “Input: Pangram 100% AI” and “Smaug Humanizer: Pangram 100% human.” The limitations section says, in the authors’ words, “Smaug Humanizer turns many texts that detectors score as AI into text they score as human, but not every time. Pangram still flags some rewrites, more often for long texts.” The card does not publish an aggregate pass rate, and it does not report GPTZero figures.
- **Independently backed?** Not in the sources checked here. The Pangram examples and the qualitative claim are author-reported. No independent GPTZero or Pangram replication was found in this survey.

## 3. gohumanize/gohumanize-open-humanizer

- **Repo:** [gohumanize/gohumanize-open-humanizer](https://huggingface.co/gohumanize/gohumanize-open-humanizer) (dataset: [gohumanize/gohumanize-open-humanizer-dataset](https://huggingface.co/datasets/gohumanize/gohumanize-open-humanizer-dataset), 2,883 pairs, CC-BY-4.0; code and write-up: [GoHumanize-ai/gohumanize-open-humanizer](https://github.com/GoHumanize-ai/gohumanize-open-humanizer); DOI [10.5281/zenodo.22843083](https://doi.org/10.5281/zenodo.22843083))
- **Base model and size:** `Qwen/Qwen3-4B`. Hub reports about 4,022.5M parameters. English. The dataset card describes 2,629 training pairs and 254 test pairs from public-domain books and US federal publications, with LLM-styled inputs paired to the original human passages.
- **Licence:** Apache-2.0 (model); CC-BY-4.0 (dataset).
- **Downloads / likes (13 Nov 2026):** model 6.4K downloads, 3 likes (`hub_repo_details`). Dataset: 566 downloads (likes not returned as a number in that details call).
- **Claimed detector results:** the model card states, explicitly, “Educational demo; no claims about AI detectors.”
- **Independently backed?** There is no detector-score claim on the card to back. The training data and pipeline are published.

## 4. kalpeshk2011/dipper-paraphraser-xxl

- **Repo:** [kalpeshk2011/dipper-paraphraser-xxl](https://huggingface.co/kalpeshk2011/dipper-paraphraser-xxl) (paper: [arXiv:2303.13408](https://arxiv.org/abs/2303.13408); code: [martiansideofthemoon/ai-detection-paraphrases](https://github.com/martiansideofthemoon/ai-detection-paraphrases))
- **Base model and size:** T5-XXL paraphraser, 11B parameters (Hub: 11,266.9M). The paper describes DIPPER as an 11B paraphrase model that can condition on surrounding context and control lexical diversity and content reordering.
- **Licence:** Apache-2.0.
- **Downloads / likes (13 Nov 2026):** 105.4K downloads, 56 likes (`hub_repo_details`). (A keyword search earlier in the same session showed 2.2K; the details figure is the one used here.)
- **Claimed detector results:** from the paper abstract and Table 1 (Wikipedia open-ended generation, 300 tokens, detection accuracy at a 1% false-positive rate), DIPPER paraphrasing reduced several 2023-era detectors. At the highest diversity setting (60L, 60O):
  - DetectGPT on GPT-2 XL text: 70.3% → 4.6%.
  - GPTZero on GPT-2 XL: 13.9% → 1.2%; on OPT-13B: 8.7% → 1.0%; on GPT-3.5 davinci-003: 7.1% → 1.8%.
  - Watermarking was more resilient (GPT-2 XL: 100.0% → 57.2% at the same setting).

  These figures are for 2023 detectors and 2023 models. They are not measurements of GPTZero Model 5.0b, and this survey did not re-run them.
- **Independently backed?** Yes, as a published paper (Krishna et al., 2023) with open models, code and data. That is independent of this skill’s scans. It is not a contemporary evaluation of GPTZero 5.0b, and it is not evidence that DIPPER would score well on our emails today.

## 5. contextboxai/vi-humanizer-gemma-4-e2b

- **Repo:** [contextboxai/vi-humanizer-gemma-4-e2b](https://huggingface.co/contextboxai/vi-humanizer-gemma-4-e2b)
- **Base model and size:** tagged `base_model:google/gemma-4-E2B-it`. Hub reports about 5,104.3M parameters. Languages: Vietnamese and English.
- **Licence:** Gemma (`license:gemma` on the Hub card).
- **Downloads / likes (13 Nov 2026):** 1.4K downloads, 5 likes (`hub_repo_details`).
- **Claimed detector results:** this survey did not obtain a usable isolated copy of the model card’s evaluation section (the card fetch was intermixed with another file). No GPTZero or other detector score is therefore reported here.
- **Independently backed?** No detector claim is reported here.

## 6. simonlesaumon/qwen-french-humanizer

- **Repo:** [simonlesaumon/qwen-french-humanizer](https://huggingface.co/simonlesaumon/qwen-french-humanizer)
- **Base model and size:** QLoRA fine-tune of `unsloth/Qwen2.5-14B-Instruct-bnb-4bit` (Qwen2.5-14B class). French. The card describes a manually curated dataset of about 1,200 ShareGPT conversation pairs, 3 epochs, effective batch size 16, learning rate 2e-4, trained on an NVIDIA A40.
- **Licence:** Apache-2.0.
- **Downloads / likes (13 Nov 2026):** 1.9K downloads, 3 likes (`hub_repo_details`). (A keyword search earlier in the same session showed 820 downloads; the details figure is the one used here.)
- **Claimed detector results:** the card’s project description says the aim is “to produce texts that are undetectable by classification algorithms (AI detectors), by introducing burstiness (rhythm variation) and a less probable vocabulary” (translated from the French card). It labels the work “Alpha / Research.” The card does not publish a GPTZero, Originality.ai, or other detector score table.
- **Independently backed?** No measured detector result is given on the card, so there is nothing to independently back. The stated goal is not a reported outcome.

## Related datasets and commercial-tool benchmarks

These are not open rewriter checkpoints, but they are the main Hub datasets returned for “humanizer” that mention detector scores.

- **[ai-humanizer-benchmark/ai-humanizer-benchmark](https://huggingface.co/datasets/ai-humanizer-benchmark/ai-humanizer-benchmark)** — 3.5K downloads, 3 likes, CC-BY-4.0 (13 Nov 2026). The dataset card describes a monthly benchmark of commercial humanizer *tools* against seven detectors, including GPTZero. It is a benchmark of closed products, not of the open models above.
- **[HumanizerBench/humanizerbench](https://huggingface.co/datasets/HumanizerBench/humanizerbench)** — 602 downloads, 3 likes, CC-BY-4.0. The card describes a monthly audit of commercial humanizers scored by six commercial detectors, with published inputs and outputs. A related website, [humanizerbench.com/detectors/gptzero](https://humanizerbench.com/detectors/gptzero/), ranks closed tools (Phrasly, WriteHuman, Rephrasy, and others) against GPTZero as of November 2026. Those rankings are about paid web tools, not about the open Hub weights listed above.
- **[gohumanize/gohumanize-open-humanizer-dataset](https://huggingface.co/datasets/gohumanize/gohumanize-open-humanizer-dataset)** and **[jialinyyzz/humanizer-data](https://huggingface.co/datasets/jialinyyzz/humanizer-data)** — training data for models 3 and 1.
- Several small “humanize-rl” datasets and low-download LoRA/SFT repos (for example under `jayshah5696/`) exist; none of the ones inspected in this pass had download or like counts comparable to the models above, and they were not included in the top list.

A Hub organisation page, [huggingface.co/ai-humanizer](https://huggingface.co/ai-humanizer), and a similarly named “best-ai-humanizer-2026-ranked” page make strong GPTZero claims about *commercial* humanizers (Rephrasy, Undetectable AI, Walter Writes, and others). Those claims were not used as evidence for any open-weight model in this survey. Their methods and affiliations were not independently verified here.

## Takeaway for this project

Open humanizer weights do already exist on Hugging Face, including two recent 12B Gemma-4 fine-tunes and a well-known 11B paraphraser from 2023. The only GPTZero numbers in this survey that come with a citable paper are DIPPER’s 2023 results, which predate GPTZero Model 5.0b. The current 12B “humanizer” cards report author-run Originality.ai or Pangram checks, or they explicitly make no detector claim. None of these sources replaces a scan of our own synthetic emails on GPTZero 5.0b.
