# Small offline proxies against archived GPTZero scores

November 11, 2026. **No metric here is a validated substitute for GPTZero, and none is accurate enough to choose which short email to scan.** The run asks whether free small models, scored on CPU, rank the archived Basic 4.9b results. It does not demonstrate a writing improvement.

The join, the scores, and the summary are [corpus.json](corpus.json), [scores.json](scores.json), and [report.json](report.json). The literature note and the training-cost estimate are in [detector literature and proxy](../../docs/detector-literature-and-proxy.md). A maintainer report of Model 5.0b email scans is in that note. It has no text and no receipt here, mixed was not reported, and it is not mixed into the numbers below.

## What was scored

`proxy_detector.py corpus` keeps a GPTZero observation only when the AI, mixed, and human figures sit on an object marked GPTZero and a file in `studies/` hashes to a checksum stored with that object. This run found 108 files, all Basic Scan, Model 4.9b, with no conflicting scores for the same bytes. Five pairs of files differ only by trailing newlines and share an AI percent. Correlations count each stripped text once: **103 texts**. Ninety-seven files are 100% AI. Eleven files are below the ceiling; after the newline collapse, **10 texts**. Five texts are under 100 words, and all five are 100% AI.

The ten pairs are the ones frozen in [open-detector-proxy-1](../open-detector-proxy-1/README.md). Three fall by at least five GPTZero points: 100 to 93, and 100 to 0 twice on the same business case. The other seven are exact ties at 100. "Drops caught" means the proxy's oriented score decreased by any amount. A move of a few thousandths counts. The five-point bar and a zero margin give the same counts, because every archived reduction is at least 7 points.

Six texts exceed 512 tokens and are unscored for the three RoBERTa classifiers and for Oculus. All six are 100% AI. Desklib's 768-token limit covers every joined text. Nothing was truncated. Torch was 2.8.0+cpu, float32, four threads.

Six `prior_gptzero` objects in `studies/pangram-transfer-1/results.json` have no hash of their own. Two parent inputs are already in the 108. Four others are not: the kubernetes-probe-roles and postgresql-snapshot-scope original and direct editor files, 164 to 181 words, each Basic 4.9b at 100% AI. The literature note lists them. They are outside this correlation.

## Agreement with the archived scores

Spearman is the oriented score against GPTZero AI percent. "Below median" is the share of the 10 below-ceiling texts that fall under the median oriented score of the ceiling texts. Rounded to three decimals from `report.json`.

| Metric | n | Spearman | Spearman under 100 | Below median | Drops caught | Ties lowered |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `classifier__hc3_roberta` | 97 | 0.155 | −0.129 | 0.800 | 1/3 | 1/7 |
| `classifier__fakespot_roberta` | 97 | 0.102 | −0.191 | 0.600 | 2/3 | 4/7 |
| `binoculars__gpt2_distilgpt2` | 103 | 0.077 | 0.419 | 0.600 | 1/3 | 3/7 |
| `openai-community__gpt2__curvature` | 103 | 0.070 | 0.800 | 0.600 | 0/3 | 1/7 |
| `binoculars__gpt2medium_gpt2` | 103 | 0.067 | 0.394 | 0.600 | 0/3 | 4/7 |
| `distilbert__distilgpt2__curvature` | 103 | 0.063 | −0.185 | 0.500 | 0/3 | 4/7 |
| `Qwen__Qwen2.5-0.5B__log_perplexity` | 103 | 0.023 | 0.529 | 0.500 | 1/3 | 1/7 |
| `HuggingFaceTB__SmolLM2-360M__log_perplexity` | 103 | 0.015 | 0.554 | 0.500 | 2/3 | 2/7 |
| `classifier__openai_roberta` | 97 | 0.003 | 0.585 | 0.500 | 2/3 | 3/7 |
| `openai-community__gpt2__log_perplexity` | 103 | −0.016 | 0.554 | 0.500 | 0/3 | 1/7 |
| `openai-community__gpt2-medium__log_perplexity` | 103 | −0.018 | 0.554 | 0.500 | 0/3 | 1/7 |
| `Qwen__Qwen2.5-0.5B__curvature` | 103 | −0.028 | 0.135 | 0.200 | 1/3 | 2/7 |
| `desklib__ai_probability` | 103 | −0.035 | 0.234 | 0.500 | 1/3 | 5/7 |
| `openai-community__gpt2-medium__curvature` | 103 | −0.046 | 0.726 | 0.500 | 0/3 | 1/7 |
| `HuggingFaceTB__SmolLM2-360M__curvature` | 103 | −0.053 | 0.037 | 0.400 | 1/3 | 2/7 |
| `oculus__ai_probability` | 97 | −0.076 | 0.468 | 0.400 | 3/3 | 4/7 |
| `binoculars__qwen2.5_0.5b` | 103 | −0.077 | −0.135 | 0.300 | 3/3 | 3/7 |
| `distilbert__distilgpt2__log_perplexity` | 103 | −0.091 | 0.652 | 0.200 | 1/3 | 1/7 |
| `distilbert__distilgpt2__burstiness` | 103 | −0.092 | −0.683 | 0.300 | 2/3 | 5/7 |
| `Qwen__Qwen2.5-0.5B__burstiness` | 103 | −0.100 | −0.566 | 0.400 | 0/3 | 4/7 |
| `binoculars__smollm2_360m` | 103 | −0.104 | 0.172 | 0.300 | 2/3 | 4/7 |
| `openai-community__gpt2__burstiness` | 103 | −0.125 | −0.542 | 0.300 | 0/3 | 5/7 |
| `openai-community__gpt2-medium__burstiness` | 103 | −0.146 | −0.542 | 0.200 | 0/3 | 5/7 |
| `HuggingFaceTB__SmolLM2-360M__burstiness` | 103 | −0.186 | −0.775 | 0.200 | 0/3 | 4/7 |

The strongest overall Spearman is 0.155. GPT-2 curvature's 0.800, and GPT-2 medium's 0.726, are confined to the 10 below-ceiling texts, and both catch none of the three paired drops: curvature rose on the edits GPTZero scored as less AI. Qwen Binoculars and Oculus catch 3 of 3 drops. Qwen's three catches are raw moves of +0.003, +0.009, and +0.019 on a score whose labelled texts span 0.974 to 1.272. Oculus also lowers 4 of 7 ties, including the technical pair whose GPTZero score stayed at 100. Desklib's Spearman is −0.035, and its median probability on the 93 ceiling texts is 0.054.

The Darwin and Carroll controls have no GPTZero label. GPT-2 curvature scores them at 0.450 and 1.587, both more machine-like than the ceiling median of −0.616. Qwen Binoculars scores Carroll at 0.928, more machine-like than every labelled text. Desklib scores the same paragraphs at 0.016 and 0.026, which is the human side of its own 0.5 line and also where most of the 100% AI texts sit.

Oculus on the ten pairs and both controls, 22 probabilities, is within 0.000002 of the full-precision values in [oculus/results.json](../open-detector-proxy-1/oculus/results.json). Desklib was scored without padding to 768. [desklib-pad-parity.json](desklib-pad-parity.json) compares that logit with the skill's padded scorer on a four-word sentence, the Carroll paragraph, and one business answer. The largest absolute difference is 2.38×10⁻⁶. Fakespot was scored on raw text; its card's cleaning step was not applied. For the OpenAI detector, `scores.json` records label 0 as Fake, label 1 as Real, and `ai_index` 0.

## Snapshots

Weights are not in this repository. Revisions are the snapshots that produced `scores.json`.

| Model | Revision | License recorded with the snapshot |
| --- | --- | --- |
| `distilbert/distilgpt2` | `2290a62682d06624634c1f46a6ad5be0f47f38aa` | apache-2.0 |
| `openai-community/gpt2` | `607a30d783dfa663caf39e06633721c8d4cfcd7e` | mit |
| `openai-community/gpt2-medium` | `6dcaa7a952f72f9298047fd5137cd6e4f05f41da` | mit |
| `HuggingFaceTB/SmolLM2-360M` | `f8027fd0eaeea54caa13c31d31b9fdc459c38b49` | apache-2.0 |
| `HuggingFaceTB/SmolLM2-360M-Instruct` | `a10cc1512eabd3dde888204e902eca88bddb4951` | apache-2.0 |
| `Qwen/Qwen2.5-0.5B` | `060db6499f32faf8b98477b0a26969ef7d8b9987` | apache-2.0 |
| `Qwen/Qwen2.5-0.5B-Instruct` | `7ae557604adf67be50417f59c2c2f167def9a775` | apache-2.0 |
| `openai-community/roberta-base-openai-detector` | `6cba99c003b711c7fe94f8a3aa2be35a792cb6fa` | mit |
| `Hello-SimpleAI/chatgpt-detector-roberta` | `d2b342c61775d5dd0221808a79983ed3b86ffd86` | none on the card |
| `fakespot-ai/roberta-base-ai-text-detection-v1` | `f9cdb14d1f8b105f597d80fa7b56f20c6ea0e9db` | apache-2.0 |
| `desklib/ai-text-detector-v1.01` | `5fdea974cd4287c61674951ec78803aa274e2fb7` | mit |
| `danibor/oculus-v2.0-multilingual` | `e6b41a2159c78d480738317c3ea6a680073a7b32` | apache-2.0 |

## Recompute

The report command does not load a model. It rebuilds the summary from `scores.json` and the current `studies/` tree.

```sh
python3 skills/anti-ai-detection-writing-skill/scripts/proxy_detector.py report \
  --root . \
  --scores studies/detector-proxy-1/scores.json \
  --output studies/detector-proxy-1/report.json
```

`python3 -m unittest tests.test_proxy_detector` checks that this committed report still matches a fresh summary, and it does not import torch. A new score run needs the snapshots above and the optional script dependencies. It is not part of the default test suite.
