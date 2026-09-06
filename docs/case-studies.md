# Showcase: measured score reductions

These five examples passed separate technical review and recorded a lower GPTZero AI confidence after editing during development on September 5–6, 2026. They are the five reductions from ten fixed-body quotation comparisons. See [when the skill may not help](when-it-may-not-help.md) for the other outcomes and the complete comparison totals.

**What changed:** each reviewed plain answer received one short, relevant quotation from the asker. The complete answer body stayed identical. These examples show observed whole-document score reductions when context was added; they do not establish a score benefit from rewriting alone or from the current packaged skill.

## Before and after

All pairs used GPTZero **Basic Scan, Model 4.9b**. Click a score to inspect the exact effective-editor input. The before column is the reviewed plain answer, and the after columns describe that same answer with the quotation added.

| Case and topic | Before AI | After AI | After mixed | After human |
| --- | ---: | ---: | ---: | ---: |
| [Qwen Code #1942](https://github.com/QwenLM/qwen-code/discussions/1942) — Command permission rules | [100%](../studies/inputs/quote-transfer-2/qwen-1942/plain.txt) | [1%](../studies/inputs/quote-transfer-2/qwen-1942/quoted.txt) | 99% | 0% |
| [Google ADK #2194](https://github.com/google/adk-python/discussions/2194) — Collecting required inputs across turns | [100%](../studies/inputs/quote-transfer-1/adk-2194/plain.txt) | [40%](../studies/inputs/quote-transfer-1/adk-2194/quoted.txt) | 60% | 0% |
| [Datasets #7351](https://github.com/huggingface/datasets/discussions/7351) — Storing an ID-to-label mapping | [100%](../studies/inputs/quote-transfer-2/datasets-7351/plain.txt) | [67%](../studies/inputs/quote-transfer-2/datasets-7351/quoted.txt) | 33% | 0% |
| [Open WebUI #19736](https://github.com/open-webui/open-webui/discussions/19736) — Nested knowledge directories | [100%](../studies/inputs/quote-transfer-1/open-webui-19736/plain.txt) | [93%](../studies/inputs/quote-transfer-1/open-webui-19736/quoted.txt) | 7% | 0% |
| [Open WebUI #20233](https://github.com/open-webui/open-webui/discussions/20233) — Per-chat parameter precedence | [100%](../studies/inputs/quote-transfer-2/open-webui-20233/plain.txt) | [93%](../studies/inputs/quote-transfer-2/open-webui-20233/quoted.txt) | 7% | 0% |

Every before result was 100% AI, 0% mixed, and 0% human. None of these ten before/after scans displayed a short-text warning. These are document classification confidences: 1% AI with 99% mixed does not mean 99% human or identify the percentage of words written by AI.

## Qwen Code: 100% → 1% AI

The reply explained how to allow selected commands in normal approval mode. The added quotation identified the asker's whitelist question. The existing configuration example, deny/ask/allow priority, narrow-pattern advice, and sandbox limitation remained intact. Both versions passed technical review; adding the quotation was judged equivalent in prose quality to the plain answer.

Read the [before](../studies/inputs/quote-transfer-2/qwen-1942/plain.txt) and [after](../studies/inputs/quote-transfer-2/qwen-1942/quoted.txt). The recorded change is **100/0/0 → 1/99/0** for AI/mixed/human confidence.

## Google ADK: 100% → 40% AI

The reply explained collecting required tool arguments in session state. The added quotation identified the asker's proposed state object. The Python example, validation requirement, state reassignment, and handling of valid zero values were preserved. Both versions passed technical review; adding the quotation was judged equivalent in prose quality.

Read the [before](../studies/inputs/quote-transfer-1/adk-2194/plain.txt) and [after](../studies/inputs/quote-transfer-1/adk-2194/quoted.txt). The recorded change is **100/0/0 → 40/60/0** for AI/mixed/human confidence.

## What the other three examples preserve

- **Datasets #7351, 100% → 67%:** the ClassLabel example, shared class ordering across splits, and persistence advice remain intact.
- **Open WebUI #19736, 100% → 93%:** the directory structure, version qualification, and distinction between directories and separate knowledge bases remain intact.
- **Open WebUI #20233, 100% → 93%:** the parameter precedence, temperature example, and distinction between request settings and server configuration remain intact.

The separate reviewers were LLM agents and did not receive detector scores. All five quotation variants passed technical review and were judged equivalent in prose quality to their plain counterparts. The quotations were selected for relevance before scanning and were not rotated or lengthened afterward.

These are maintainer-observed, completed UI results, not authenticated service exports or independent remeasurements. The [44-scan dataset](../studies/results.json) retains every primary result and exact input hash; [methodology](methodology.md) explains the study design and provenance. A selected showcase is not a success-rate estimate. Anti-Detection Writing Skill consolidates the earlier discussion-focused development workflow; the packaged version has not been prospectively validated for detector performance.
