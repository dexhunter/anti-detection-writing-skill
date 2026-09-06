# Anti-Detection Writing Skill

Polish AI-written text for smoother flow, clearer meaning, and a natural voice. Use it for replies, emails, articles, and documentation. When requested, test the edits with GPTZero and work toward lower AI-detection scores while preserving facts, qualifications, and the writer's intended meaning.

**The goals are better readability for people and lower detector scores.** Current evidence is experimental and comes from technical discussion answers: plain rewriting lowered scores in 0 of 15 questions; adding a relevant asker quotation to a fixed answer lowered them in 5 of 10 comparisons. All failures are included. The skill does not guarantee a detector result, and broader writing genres have not been benchmarked.

## What you get

- [`anti-detection-writing`](skills/anti-detection-writing/SKILL.md): identify the reader and purpose, preserve claims, improve flow and wording, review, and measure detector results when requested.
- [Case studies](docs/case-studies.md) covering successful, unchanged, and rejected outcomes; [methodology](docs/methodology.md) and [44 exact editor inputs](studies/results.json) for the complete cohorts and new answers.
- An optional local receipt checker for new scans. It checks saved evidence consistency, not human authorship or the authenticity of a detector service.

The discussion-focused development revision added explicit prerequisite/exception placement and a final claim reconciliation, informed by [four other writing skills](docs/related-skills.md). In a [six-question comparison](studies/unseen-transfer-1/README.md), one separate LLM reviewer preferred that revision twice, the original once, and judged three equivalent; all twelve answers passed technical review. GPTZero measurement is pending available scan allowance. This public release broadens the wording to other writing formats; the historical results do not establish its detector effect.

The skill has no account credentials, browser automation, paid-service dependency, or automatic posting permission. Basic editing needs the text and its intended audience; factual corrections need supporting sources. Live scanning additionally needs a browser tool supported by your agent and your own detector access. Independent review needs a separate reviewer; the development reviews used LLM agents.

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

## Observed results

These are small convenience samples from September 5–6, 2026, using GPTZero Basic Scan, displayed Model 4.9b. They document development of the workflow, rather than a prospective benchmark of the packaged skill.

| Cohort | Questions | Plain-rewrite reductions | Fixed-body quotation reductions | Scans |
| --- | ---: | ---: | ---: | ---: |
| Initial plain pilot | 5 | 0/5 | — | 10 |
| First quotation transfer | 5 | 0/5 | 2/5 | 15 |
| Second quotation transfer | 5 | 0/5 | 3/5 | 15 |
| New answers, no baseline | 4 | Not measured | Not measured | 4 |

Separate LLM reviews rated 8 of the 15 plain revisions improved and 7 equivalent, with all passing technical review. Four later new answers scored 100, 93, 100, and 11% AI. Two met that user's below-100 condition and were published; those unpaired scores are **not reductions**.

The largest change was **100% AI → 1% AI, 99% mixed, 0% human** after adding a relevant quotation. Those values describe the detector's document classification confidence, not the proportion written by a person. Adding a quotation changes content and length; these observations establish neither a general success rate nor the cause of the change. A 43% candidate with incorrect advice was rejected; its corrected replacement scored 60%.

The records are maintainer-observed UI results, not authenticated service exports. Hashes make the distributed input files checkable; they do not independently establish the scores. The work lacks independent human ratings, repeatability estimates, and measurements of answer acceptance. See the [complete limits and exploratory attempts](docs/methodology.md).

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
