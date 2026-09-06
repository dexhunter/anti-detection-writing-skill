# Anti-Detection Writing Skill

Polish AI-written text for smoother flow, clearer meaning, and a natural voice. Use it for replies, emails, articles, and documentation. When requested, test the edits with GPTZero and work toward lower AI-detection scores while preserving facts, qualifications, and the writer's intended meaning.

**The goals are better readability for people and lower detector scores.** The [showcase](docs/case-studies.md) contains measured reductions with exact before/after inputs. [When the skill may not help](docs/when-it-may-not-help.md) covers unchanged scores, rejected edits, and untested formats. Results are experimental; the skill does not guarantee a detector outcome.

## Install

Install from GitHub:

```sh
npx skills add dexhunter/anti-detection-writing-skill --skill anti-detection-writing
```

From a local checkout, use `npx skills add . --skill anti-detection-writing`.

The [skills CLI](https://github.com/vercel-labs/skills#source-formats) supports local paths and named skill selection. This installs into the current project by default; review its prompts before replacing an existing skill. Alternatively, copy `skills/anti-detection-writing/` into your agent's supported skill directory.

Example request:

> Use $anti-detection-writing to make this text smoother and easier to read. Preserve its facts and qualifications, remove formulaic wording, and match the intended audience. Get a separate review of the final text.

For a requested measurement, add:

> Also test the original and final text using GPTZero Basic Scan. Aim for lower AI confidence without sacrificing clarity or accuracy. Record all three confidences, the model, exact inputs, and warnings. Keep unchanged and worse results.

## What you get

- [`anti-detection-writing`](skills/anti-detection-writing/SKILL.md): identify the reader and purpose, preserve claims, improve flow and wording, review, and measure detector results when requested.
- A [showcase of measured reductions](docs/case-studies.md), a separate [limitations guide](docs/when-it-may-not-help.md), and [44 exact editor inputs](studies/results.json) with the full results.
- An optional local receipt checker for new scans. It checks saved evidence consistency, not human authorship or the authenticity of a detector service.

The editing workflow draws on [four other writing skills](docs/related-skills.md): put prerequisites and exceptions beside the claims they qualify, then reconcile the finished text against its original facts. The [unseen-question trial](studies/unseen-transfer-1/README.md) reports readability review separately; its detector measurements remain pending.

The skill has no account credentials, browser automation, paid-service dependency, or automatic posting permission. Basic editing needs the text and its intended audience; factual corrections need supporting sources. Live scanning additionally needs a browser tool supported by your agent and your own detector access. Independent review needs a separate reviewer; the development reviews used LLM agents.

## Showcase

Five reviewed examples recorded lower GPTZero AI confidence during development. In each pair, one relevant asker quotation was added to the unchanged answer body. Both scans used **Basic Scan, Model 4.9b**.

| Example | Before AI | After AI |
| --- | ---: | ---: |
| [Qwen Code #1942](https://github.com/QwenLM/qwen-code/discussions/1942) | 100% | 1% |
| [Google ADK #2194](https://github.com/google/adk-python/discussions/2194) | 100% | 40% |
| [Datasets #7351](https://github.com/huggingface/datasets/discussions/7351) | 100% | 67% |
| [Open WebUI #19736](https://github.com/open-webui/open-webui/discussions/19736) | 100% | 93% |
| [Open WebUI #20233](https://github.com/open-webui/open-webui/discussions/20233) | 100% | 93% |

See the [full showcase](docs/case-studies.md) for exact inputs, all three confidences, and what each example preserves. These are five reductions from ten quotation comparisons, not a general success-rate estimate. The 1% AI result was **99% mixed and 0% human**. All results are maintainer-observed UI measurements; they do not establish human authorship or the effect of rewriting alone.

## When the skill may not help

Plain rewriting did not reduce scores in the 15-question development sample, even where separate LLM review found clearer prose. Five of ten quotation comparisons also stayed unchanged. Short technical replies, unsupported factual changes, and formats without paired measurements need particular care. The [limitations guide](docs/when-it-may-not-help.md) provides concrete cases and next steps; the [methodology](docs/methodology.md) and complete dataset retain every result.

## Community

[Start here](https://github.com/dexhunter/anti-detection-writing-skill/discussions/1) for installation and your first example. The [reporting guide](https://github.com/dexhunter/anti-detection-writing-skill/discussions/2) explains how to share a useful writing or detector result.

[Ask a question](https://github.com/dexhunter/anti-detection-writing-skill/discussions/categories/q-a), [share a measured success](https://github.com/dexhunter/anti-detection-writing-skill/discussions/categories/showcase), or [report where the skill falls short](https://github.com/dexhunter/anti-detection-writing-skill/discussions/categories/results-and-limitations). [Ideas](https://github.com/dexhunter/anti-detection-writing-skill/discussions/categories/ideas) is the place for a concrete editing improvement or a proposed experiment.

Start with one short text and tell us the intended reader, your agent, and what changed. Detector access is optional for writing feedback. Read [CONTRIBUTING.md](CONTRIBUTING.md) for help choosing the right place and sharing useful evidence.

## Local checks

With Python 3.10+ available through [uv](https://docs.astral.sh/uv/):

```sh
uv run --no-project python scripts/check_studies.py
uv run --no-project python -m unittest discover -s tests -v
uvx ruff check .
```

No detector account or network call is needed by these checks. They do not rerun the historical scans. See the [completed release checks](docs/release-checks.md), including isolated installation and the limits of a single synthetic writing check.

## Scope and license

Use the workflow to serve the reader, correct unsupported claims, and preserve uncertainty. Do not invent experience, disguise authorship, add irrelevant material for a score, or disregard a community's participation rules. Publication requires the user's authorization and a final context check; a score cannot supply either.

Original skill instructions, code, and documentation are under the [MIT License](LICENSE). Brief third-party quotations and linked upstream material retain their original rights; see [NOTICE](NOTICE). GPTZero is an external service, with no affiliation or endorsement implied.
