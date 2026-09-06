# Evidence-first Writing

An experimental agent skill for writing concise, source-grounded technical answers and checking that editing preserves their meaning. Optional GPTZero measurements are recorded separately from writing quality.

**Ready to try as an editing workflow; not a validated detector bypass.** The development trials found no detector-score reductions from plain rewriting in 15 questions. Adding a relevant asker quotation to a fixed answer reduced the displayed AI confidence in 5 of 10 comparisons. All failures are included.

## What you get

- [`discussion-answer-polish`](skills/discussion-answer-polish/SKILL.md): inspect the question and sources, track claims, rewrite, review, and verify any authorized publication.
- [Case studies](docs/case-studies.md) covering successful, unchanged, and rejected outcomes; [methodology](docs/methodology.md) and [44 exact editor inputs](studies/results.json) for the complete cohorts and new answers.
- An optional local receipt checker for new scans. It checks saved evidence consistency, not human authorship or the authenticity of a detector service.

The latest revision adds explicit prerequisite/exception placement and a final claim reconciliation, informed by [four other writing skills](docs/related-skills.md). In a [six-question comparison](studies/unseen-transfer-1/README.md), one separate LLM reviewer preferred the revision twice, the original once, and judged three equivalent; all twelve answers passed technical review. GPTZero measurement is pending available scan allowance. The historical results below do not establish the additions' detector effect.

The skill has no account credentials, browser automation, paid-service dependency, or automatic posting permission. Basic editing needs access to the question and relevant sources. Live scanning additionally needs a browser tool supported by your agent and your own detector access. Independent review needs a separate reviewer; the development reviews used LLM agents.

## Install

From a checkout of this repository:

```sh
npx skills add . --skill discussion-answer-polish
```

The [skills CLI](https://github.com/vercel-labs/skills#source-formats) supports local paths and named skill selection. This installs into the current project by default; review its prompts before replacing an existing skill. Alternatively, copy `skills/discussion-answer-polish/` into your agent's supported skill directory.

Example request:

> Use $discussion-answer-polish to improve this technical reply. Verify the source claims, preserve the qualifications, and get a separate correctness review. Do not post it yet.

For a requested measurement, add:

> Compare the original and final text using GPTZero Basic Scan. Record all three confidences, the model, exact inputs, and warnings. Keep unchanged results.

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

Use the workflow to answer the actual question, correct unsupported claims, and preserve uncertainty. Do not invent experience, disguise authorship, add irrelevant material for a score, or disregard a community's participation rules. Publication requires the user's authorization and a final context check; a score cannot supply either.

Original skill instructions, code, and documentation are under the [MIT License](LICENSE). Brief third-party quotations and linked upstream material retain their original rights; see [NOTICE](NOTICE). GPTZero is an external service, with no affiliation or endorsement implied.
