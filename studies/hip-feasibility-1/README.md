# Released HIP model: local feasibility pilot

September 6, 2026. **Two generated alternatives, two independent quality failures, zero detector scans.** No detector score is available for either output. These are rejected research outputs, not advice to use or showcase successes.

After a prompt-based comparison plateaued, we tested the released [HIP 0.6B base-model adapter](https://huggingface.co/YixuanEvenXu/Qwen3-0.6B-Base-HIP-adapter/tree/98a907f41440e10aafedd10364b41c32bb5fbf6a). Its [paper](https://arxiv.org/html/2605.19516v1) uses a trained paraphraser and iterative inference; copying a prompt into the writing skill does not implement it. The authors describe the adapter as a research artifact for detector robustness. It was not adopted as the skill's rewriting engine.

The cases are the two longer answers from [requested-alternatives-1](../requested-alternatives-1/README.md), selected before generation. They are reused development cases, not an unseen dataset. Each received one generation, with no corrections, resampling or detector feedback. The complete Markdown answer, including code and links, entered the model. Both inputs fit without truncation and both outputs ended normally.

| Case | Source/output words | Independent review | Detector |
| --- | ---: | --- | --- |
| [Kubernetes input](inputs/kubernetes-probe-roles.md), [output](outputs/kubernetes-probe-roles.md) | 164 / 207 | Fail: loses the deadlock-specific liveness role and consecutive-failure qualification; confuses health conditions with the failure threshold. | Not measured |
| [PostgreSQL input](inputs/postgresql-snapshot-scope.md), [output](outputs/postgresql-snapshot-scope.md) | 180 / 231 | Fail: reverses first-statement snapshot timing, loses the own-write exception, and adds invalid `ISOLATION_LEVEL` wording. | Not measured |

Word counts use whitespace splitting, not a detector UI. The independent LLM reviewer compared exact output hashes with the questions, claims and official documentation without detector scores. This is a factual review, not a human preference study. Exact commands can survive while surrounding prose becomes wrong; a code-presence check alone would miss these failures.

## Configuration and retained evidence

The [plan](plan.json) froze cases, settings and rejection rules before inference. The [run record](run.json) identifies the executed runner and input/output hashes; [results](results.json) records the subsequent quality decisions. Questions and source ledgers are under `sources/`. Each output also has its full `.raw.txt` generation, `.prompt.txt` input and `.json` metadata.

- Base: `Qwen/Qwen3-0.6B-Base`, revision `da87bfb608c14b7cf20ba1ce41287e8de496c0cd`.
- Adapter: `YixuanEvenXu/Qwen3-0.6B-Base-HIP-adapter`, revision `98a907f41440e10aafedd10364b41c32bb5fbf6a`.
- One pass; temperature 1.0, top-p 0.95, top-k 0, fixed per-case seeds; 1,024-token input limit checked without truncation and 1,024-token output cap.
- Local Apple MPS, BF16; Transformers 4.57.6, PEFT 0.18.1 and PyTorch 2.8.0. Standard model loading, remote code disabled, safetensors weights. No training or paid inference.

The [executed runner](run_pilot.py) and [dependency versions](requirements-lock.txt) are included for inspection. Weights and the local environment are not distributed. To reproduce locally, copy the runner, plan and inputs into a separate directory, create an isolated environment with `uv`, install the locked dependencies, and create an empty `outputs/` directory. The runner refuses to overwrite an existing run record. Hardware and sampling can affect output despite fixed seeds.

This pilot differs from the upstream example in round count, technical Markdown inputs, hardware, explicit top-k setting and token limits; it is not a reproduction of the paper's aggregate results. Both model cards identify Apache-2.0 licensing. No upstream skill prose or model weights were copied into the installed skill.

## What this changes

The small released model did not preserve enough technical meaning in these two cases. This supports rejecting these outputs before scanning and checking temporal conditions even when code and links survive. It does not establish the performance of larger HIP models, other genres, further rounds or current GPTZero. No score-reduction claim follows, and no historical scan totals change.
