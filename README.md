# Anti-AI Detection Writing Skill

Polish AI-written text for smoother flow, clearer meaning, and a natural voice. Use it for replies, emails, articles, and documentation. When requested, test the edits with GPTZero and work toward lower AI-detection scores while preserving facts, qualifications, and the writer's intended meaning.

**The goals are better readability for people and lower detector scores.** The [showcase](docs/case-studies.md) contains measured reductions with exact before/after inputs. [When the skill may not help](docs/when-it-may-not-help.md) covers unchanged scores, rejected edits, and untested formats. Results are experimental; the skill does not guarantee a detector outcome.

## Install

Install from GitHub:

```sh
npx skills add dexhunter/anti-detection-writing-skill --skill anti-ai-detection-writing-skill
```

From a local checkout, use `npx skills add . --skill anti-ai-detection-writing-skill`.

The [skills CLI](https://github.com/vercel-labs/skills#source-formats) supports local paths and named skill selection. This installs into the current project by default; review its prompts before replacing an existing skill. Alternatively, copy `skills/anti-ai-detection-writing-skill/` into your agent's supported skill directory.

Example request:

> Use $anti-ai-detection-writing-skill to make this text smoother and easier to read. Preserve its facts and qualifications, remove formulaic wording, and match the intended audience. Get a separate review of the final text.

For a requested measurement, add:

> Also test the original and final prose using GPTZero Basic Scan. Keep code separate and check its correctness independently. Aim for lower AI confidence without sacrificing clarity or accuracy. Record the full message, exact prose inputs, excluded code, all three confidences, the model, and warnings. Keep unchanged and worse results.

## What you get

- [`anti-ai-detection-writing-skill`](skills/anti-ai-detection-writing-skill/SKILL.md): identify the reader and purpose, preserve claims, improve flow and wording, review, and measure detector results when requested.
- A [showcase of measured reductions](docs/case-studies.md), a separate [limitations guide](docs/when-it-may-not-help.md), and [44 exact editor inputs](studies/results.json) with the full results.
- An optional local receipt checker for new scans. It checks saved evidence consistency, not human authorship or the authenticity of a detector service.
- An optional fact checker, `scripts/check_facts.py` inside the skill. It compares numbers, dates, prices, order IDs, and capitalised names before a scan. It does not judge a detector score.
- An optional [local detector diagnostic](skills/anti-ai-detection-writing-skill/references/local-detector.md) with pinned model verification and full-text checks. Its scores are not a validated substitute for GPTZero or Pangram. A separate [literature review and small-model proxy](docs/detector-literature-and-proxy.md) checks cheaper offline scores against the archived GPTZero results. The strongest Spearman correlation in that run is 0.131, so the scores are not a way to choose a scan.

The editing workflow draws on [other writing skills](docs/related-skills.md): put prerequisites and exceptions beside the claims they qualify, then reconcile the finished text against its original facts. The [unseen-question trial](studies/unseen-transfer-1/README.md) reports readability review separately. Its 12 completed measurements all scored 100% AI / 0% mixed / 0% human, giving six tied pairs; this completes the older frozen comparison, not a test of later literature-informed instructions.

The later [requested-alternative pilot](studies/requested-alternatives-1/README.md) adds four new source-grounded examples and eight exact scans. All four pairs stayed at 100% AI. The skill now permits an acceptable alternative when explicitly requested, while keeping clear passages intact during ordinary polishing; that change has not demonstrated a detector-score benefit.

A [targeted-edit comparison](studies/targeted-edit-1/README.md) tested two fresh synthetic examples on both GPTZero and Pangram. A separate LLM reviewer preferred both edits for clarity, but neither detector improved in either pair. The full record retains all eight scans and Pangram's short-text warnings.

For systematic skill improvement, the [bounded autoresearch workflow](docs/autoresearch.md) separates proposals, candidate selection, quality review and detector confirmation. Its resumable local controller preserves failures and reserves evaluation budget; an active agent supplies subagents and supported browser operations.

A later [twenty-method search](studies/model-assisted-1/README.md) found a repeated 100% → 0% AI-confidence reduction on one business example using a local trained model plus separate repair and editing. The technical example stayed at 100%, and both unseen candidates lost the readability comparison. The workflow was not promoted; this release adds the evidence and research guidance without claiming a general detector-performance improvement.

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

## Documentation / Reports index

Reports and guides in this repository. Results are experimental; none of these documents is a method for passing a detector.

### Reports

- [GPTZero experiment results](docs/reports/gptzero-results.md): every logged Model 5.0b scan from the 2026 calibration batch, Wood to Water tests, and Stages 1–15 (114 scans), with findings kept separate from hypotheses. Companion data: [docs/reports/data/gptzero-scans.csv](docs/reports/data/gptzero-scans.csv).
- [Stage 16 pot-handle scans](docs/reports/stage-16-pot-handle.md): one free-plan Model 5.0b session on 13 November 2026. Whole-text rewrites scored 100% AI. The lowest fact-complete text was 7% AI on one email. Not in the 114-row CSV, and not a way to pass GPTZero.
- [Literature update, 13 November 2026](docs/literature-update-2026-11-13.md): papers and GPTZero release notes opened that day, and what does and does not transfer to Model 5.0b on a short email. Vendor notes are labelled as vendor claims.
- [Hugging Face humanizer survey](docs/reports/huggingface-humanizer-survey.md): a desk survey of model cards. None of these models were run by us.
- [Showcase: measured score reductions](docs/case-studies.md): earlier maintainer-observed Basic Scan, Model 4.9b quotation comparisons.
- [When the skill may not help](docs/when-it-may-not-help.md): unchanged scores, rejected edits, and untested formats.
- [Methodology and provenance](docs/methodology.md): how historical results were recorded.
- [Detector literature and an offline proxy](docs/detector-literature-and-proxy.md): literature notes and a small-model proxy that did not predict GPTZero scores well (strongest Spearman 0.131 in that run).
- [Skill autoresearch](docs/autoresearch.md) and [autoresearch setup validation](docs/autoresearch-validation.md): the bounded improvement workflow and its checks.
- [Related writing skills](docs/related-skills.md): other writing skills this workflow draws on.
- [Experimental release checks](docs/release-checks.md): completed offline release checks.
- [Complete historical dataset](studies/results.json): 44 exact editor inputs with full results.

### Study reports

Each study has its own README and supporting files under `studies/`.

- [article-model-transfer-1](studies/article-model-transfer-1/README.md) — Full-article model transfer and adaptive recovery
- [autoresearch-controls-1](studies/autoresearch-controls-1/README.md) — Control-boundary instruction experiment
- [detector-proxy-1](studies/detector-proxy-1/README.md) — Small offline proxies against archived GPTZero scores
- [exact-crossover-1](studies/exact-crossover-1/README.md) — Exact crossover between complete drafts
- [gepa-pilot-1](studies/gepa-pilot-1/README.md) — GEPA pilot: two rejected policies, no detector reduction
- [hip-feasibility-1](studies/hip-feasibility-1/README.md) — Released HIP model: local feasibility pilot
- [local-tools-1](studies/local-tools-1/README.md) — Local tools and released-model research
- [model-assisted-1](studies/model-assisted-1/README.md) — Model-assisted rewriting: a development gain that failed confirmation
- [open-detector-proxy-1](studies/open-detector-proxy-1/README.md) — Oculus and Greyscope as cheaper research feedback
- [paired-editing-examples-1](studies/paired-editing-examples-1/README.md) — Paired editing examples: preferred prose, unchanged detector scores
- [pangram-transfer-1](studies/pangram-transfer-1/README.md) — Checking existing answers with Pangram 4
- [prospective-proxy-1](studies/prospective-proxy-1/README.md) — Prospective Greyscope selection diagnostic
- [reader-dialogue-1](studies/reader-dialogue-1/README.md) — Reader dialogue before drafting
- [reader-reconstruction-1](studies/reader-reconstruction-1/README.md) — Reader reconstruction: one negative development round
- [register-and-selection-1](studies/register-and-selection-1/README.md) — Two rejected methods and an adaptive diagnostic
- [repeatability-1](studies/repeatability-1/README.md) — Same-input GPTZero repeatability check
- [requested-alternatives-1](studies/requested-alternatives-1/README.md) — Requested alternatives: four-case pilot
- [targeted-edit-1](studies/targeted-edit-1/README.md) — Targeted editing comparison
- [technical-format-1](studies/technical-format-1/README.md) — Technical formats: a small diagnostic with no score reduction
- [unseen-transfer-1](studies/unseen-transfer-1/README.md) — Unseen-question comparison
- [windowed-article-1](studies/windowed-article-1/README.md) — Five-window article rewrite
- [workflow-retest-1](studies/workflow-retest-1/README.md) — Retesting the updated skill on four failed cases
- [writing-methods-1](studies/writing-methods-1/README.md) — Writing methods: quality screening and a preservation comparison

### Other repo documents

- [CONTRIBUTING.md](CONTRIBUTING.md) — how to share a writing or detector result
- [LICENSE](LICENSE) and [NOTICE](NOTICE) — MIT licence and third-party notices
- Skill instructions: [SKILL.md](skills/anti-ai-detection-writing-skill/SKILL.md), with references under [skills/anti-ai-detection-writing-skill/references/](skills/anti-ai-detection-writing-skill/references/)

## Community

[Start here](https://github.com/dexhunter/anti-detection-writing-skill/discussions/1) for installation and your first example. The [reporting guide](https://github.com/dexhunter/anti-detection-writing-skill/discussions/2) explains how to share a useful writing or detector result.

[Ask a question](https://github.com/dexhunter/anti-detection-writing-skill/discussions/categories/q-a), [share a measured success](https://github.com/dexhunter/anti-detection-writing-skill/discussions/categories/showcase), or [report where the skill falls short](https://github.com/dexhunter/anti-detection-writing-skill/discussions/categories/results-and-limitations). [Ideas](https://github.com/dexhunter/anti-detection-writing-skill/discussions/categories/ideas) is the place for a concrete editing improvement or a proposed experiment.

Start with one short text and tell us the intended reader, your agent, and what changed. Detector access is optional for writing feedback. Read [CONTRIBUTING.md](CONTRIBUTING.md) for help choosing the right place and sharing useful evidence.

## Local checks

Run the offline checks with [uv](https://docs.astral.sh/uv/) (exercised with Python 3.13.5):

```sh
uv run --no-project python scripts/check_studies.py
uv run --no-project python -m unittest discover -s tests -v
uvx ruff check .
```

No detector account or network call is needed by these checks. They do not rerun the historical scans. See the [completed release checks](docs/release-checks.md), including isolated installation and the limits of a single synthetic writing check.

## Scope and license

Use the workflow to serve the reader, correct unsupported claims, and preserve uncertainty. Do not invent experience, disguise authorship, add irrelevant material for a score, or disregard a community's participation rules. Publication requires the user's authorization and a final context check; a score cannot supply either.

Original skill instructions, code, and documentation are under the [MIT License](LICENSE). Brief third-party quotations and linked upstream material retain their original rights; see [NOTICE](NOTICE). GPTZero is an external service, with no affiliation or endorsement implied.
