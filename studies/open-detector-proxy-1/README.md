# Oculus and Greyscope as cheaper research feedback

September 10, 2026. **Greyscope is the more promising diagnostic on these examples, but neither model is a validated substitute for GPTZero.** Both run locally. This study measures agreement with archived outcomes; it does not demonstrate a new writing improvement.

We froze 10 historical comparisons, comprising 16 unique prose inputs, and added two verified historical human paragraphs before reading local scores. The comparisons span only three recurring topics. Two of the three GPTZero reductions reuse the same business case, with different final text. Shared controls and selected outcomes make these dependent development observations, not 10 independent tests or an unseen benchmark.

The [protocol](protocol.md) defined a local decrease of at least 0.01 on each model's native 0–1 scale as meaningful, before inference. All three historical reductions exceed its separate five-percentage-point GPTZero threshold. Those scales have different meanings.

| Diagnostic | Historical reductions recognized | Local decreases where GPTZero stayed unchanged |
| --- | ---: | ---: |
| Oculus v2 | 2 of 3 | 4 of 7 |
| Greyscope v2, MLX 4-bit | 3 of 3 | 2 of 7 |

Counting any decrease, however small, changes Oculus to 3 of 3 recognized reductions and Greyscope to 3 of 7 misleading decreases on ties. These are descriptive counts, not accuracy estimates. An always-unchanged rule would match seven of the ten pair labels. The small quotation decrease and one technical decrease lie close to the chosen 0.01 threshold; their repeatability was not tested.

## Every paired result

GPTZero columns are **historical Basic Scan, Model 4.9b document AI confidence**, in percent. Oculus is sigmoid AI probability; Greyscope is calibrated ordinal AI involvement. Local columns retain their native 0–1 units, rounded here only. Positive decreases in [analysis.json](analysis.json) mean the candidate scored lower.

| Pair and intervention | GPTZero before → after | Oculus before → after | Greyscope before → after |
| --- | ---: | ---: | ---: |
| 01 · Open WebUI, attributed quotation added | 100 → 93 | 0.073343 → 0.068618 | 0.686291 → 0.674114 |
| 02 · HTTP, split and rephrase | 100 → 100 | 0.173073 → 0.443864 | 0.475194 → 0.530702 |
| 03 · Business, split and rephrase | 100 → 100 | 0.148875 → 0.056563 | 0.391851 → 0.386736 |
| 04 · HTTP, minimal writing instructions | 100 → 100 | 0.173073 → 0.088619 | 0.475194 → 0.461640 |
| 05 · Business, minimal writing instructions | 100 → 100 | 0.148875 → 0.090536 | 0.391851 → 0.415582 |
| 06 · HTTP, trained-model output plus repair/editing | 100 → 100 | 0.173073 → 0.023258 | 0.475194 → 0.284564 |
| 07 · Business, trained-model output plus repair/editing | 100 → 0 | 0.148875 → 0.009457 | 0.391851 → 0.002059 |
| 08 · Same business case, fresh pipeline verification | 100 → 0 | 0.205154 → 0.018351 | 0.365295 → 0.003131 |
| 09 · HTTP, exact sentence crossover | 100 → 100 | 0.051175 → 0.056461 | 0.471663 → 0.497940 |
| 10 · HTTP, paired editing examples | 100 → 100 | 0.101562 → 0.133891 | 0.453454 → 0.495525 |

Pair 06 is the important counterexample for future autoresearch: a large Greyscope decrease accompanied no GPTZero improvement on the technical explanation. Optimizing a local score alone could send us back toward that known failure. Pairs 07 and 08 support testing Greyscope further, but they do not supply independent evidence of transfer to new business topics.

All 16 AI-origin archived bodies fell below Oculus's published 0.5 AI classification threshold. Greyscope labelled 14 as AI-edited and the two business reductions as human. The generation provenance remains AI-origin regardless of those labels; neither detector establishes authorship.

## Coverage, controls and inference checks

The [input manifest](inference-manifest.json) retains exact saved editor bytes, including terminal newlines. Nine other historical quotation pairs contained independent code and were excluded: removing code would invalidate comparison with their old whole-input scores. Selected older inputs retain their legacy full-input, all-prose scope. The four newer inputs have explicit prose-only records with empty code exclusions. No old whole-message result was relabelled as a new prose scan.

Both models completed all 18 inputs without truncation. Oculus used 143–349 tokens including special tokens, below its 512 limit. Greyscope used 235–409 tokens for the complete calibrated prompt, below its 2,048 limit. Its author preprocessing lowercased and normalized whitespace on every input; Unicode normalization left these texts unchanged. Raw, cleaned and prompted versions are retained separately. No think-block or AI-header removal occurred. These are faithful pipeline comparisons on the same source texts, not identical internal representations across models.

The two human controls are the first eligible 100–160-word complete paragraphs from Darwin's *Origin of Species* (1859) and Carroll's *Alice's Adventures in Wonderland* (1865). Exact source attribution, hashes and the selection rule are in [human-controls.json](review/human-controls.json). The Darwin passage discusses publication circumstances. These familiar historical texts may occur in training and are not representative of modern technical replies.

| Historical human control | Oculus | Greyscope |
| --- | ---: | ---: |
| Darwin, 157 words | 0.007780 | 0.008684 |
| Carroll, 141 words | 0.018013 | 0.001223 |

Both models classified both controls as human. No GPTZero scans were run for them, and two out-of-domain controls cannot estimate a human false-positive rate.

- [Oculus](https://huggingface.co/danibor/oculus-v2.0-multilingual/tree/e6b41a2159c78d480738317c3ea6a680073a7b32): revision `e6b41a2159c78d480738317c3ea6a680073a7b32`, 1.736 GB weights, PyTorch float32 on Apple MPS. Its card reports GPTZero-label distillation; that does not make it the GPTZero Basic 4.9b model. Strict loading and the publisher's masked-mean, linear-head inference were checked. A separate publisher-class CPU replay matched tokens and differed from the MPS batch by only 0.000000858 probability. [Parity record](oculus/publisher-parity.json).
- [Greyscope MLX 4-bit](https://huggingface.co/yaoandy107/greyscope-v2-qwen3.5-4b-mlx-4bit/tree/59b6ec7a24cae161c4cbc85e594c586541d8f710): weight revision `59b6ec7a24cae161c4cbc85e594c586541d8f710`, [author source](https://github.com/yaoandy107/greyscope/tree/e052f07b5e5bddacce41fe4d5fcc3250081385da) revision `e052f07b5e5bddacce41fe4d5fcc3250081385da`. The author preprocessing, prompt and CORN ordinal decoder were retained. A replay through the author's entrypoint matched the exact tokens, logits and native output. [Runtime validation](greyscope/runtime-validation.json).

Greyscope's 18 scoring forwards took 18.22 seconds; its recorded batch took 21.54 seconds including loading and a parity replay, but excluding early imports and hash verification. Peak MLX allocation was 3.06 GB. Oculus's recorded batch took 29.32 seconds including initialization. These are single local runs, not a controlled speed benchmark. There were 36 primary scoring forwards and two parity forwards in total. Downloads and setup add overhead; no paid compute or commercial scan credits were used.

## Research decision and reproducibility

Retain Greyscope for exploratory diagnostics and design a prospective comparison before using it to select rewrites automatically. Retain failures such as pair 06 in development evidence. Keep source fidelity and independent writing review ahead of detector feedback, and keep fresh GPTZero confirmation for claims about that endpoint. No default rewriting rule or automatic local-score selector was adopted here.

The archive includes exact [Oculus outputs](oculus/results.json), [Greyscope outputs](greyscope/results.json), measured wrapper sources, pinned file hashes and dependency versions. Weights and full source books are not redistributed. The wrappers are experiment snapshots; the installed detector CLI still supports its existing pinned Desklib model. Recreating inference requires separate model downloads and, for Greyscope, the pinned author repository and its locked Mac environment. Run new inference in a separate working directory; preserve this archive.

Recompute the comparison without models, accounts or network access:

```sh
uv run --no-project python studies/open-detector-proxy-1/analyze.py
uv run --no-project python studies/open-detector-proxy-1/check_export.py
uv run --no-project python -m unittest discover -s studies/open-detector-proxy-1 -p 'test_analyze.py'
uv run --no-project python -m unittest discover -s studies/open-detector-proxy-1/oculus -p 'test_runner.py'
```

The [export manifest](export-manifest.json) maps private source hashes to public artifact hashes where local paths were removed. Historical hashes inside archived records remain unchanged. The independent [review](review/final-review.md) covers archive correspondence, inference semantics, arithmetic and limitations; the reviewer had prior model-survey context, so this is not a fresh blind writing-quality review. The commercial records are maintainer-observed UI evidence, not authenticated service exports. The [archive review](review/archive-review.md) qualifies two unverified per-arm service word-count fields; the [metadata erratum](oculus/metadata-erratum.md) corrects a source-formatting claim without changing frozen records.

The publisher reference class in `oculus/publisher-parity.py` is adapted from the linked Oculus card under Apache-2.0; see [LICENSE-2.0.txt](oculus/LICENSE-2.0.txt). Historical control passages are public-domain works, attributed in their metadata. Linked upstream code and model weights retain their respective licenses.
