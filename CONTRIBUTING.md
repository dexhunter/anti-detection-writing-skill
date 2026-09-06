# Contributing

Help make AI-written text clearer while preserving meaning. Useful contributions include small wording fixes, installation feedback, well-documented experiments, and reports of where the skill falls short.

## Where to start

- [Q&A](https://github.com/dexhunter/anti-detection-writing-skill/discussions/categories/q-a): installation and usage help.
- [Ideas](https://github.com/dexhunter/anti-detection-writing-skill/discussions/categories/ideas): concrete editing or workflow proposals.
- [Showcase](https://github.com/dexhunter/anti-detection-writing-skill/discussions/categories/showcase): paired, measured score reductions that preserve accuracy and readability.
- [Results and limitations](https://github.com/dexhunter/anti-detection-writing-skill/discussions/categories/results-and-limitations): all other outcomes, including clearer writing with unchanged scores or no scan.
- [Issues](https://github.com/dexhunter/anti-detection-writing-skill/issues): reproducible bugs in the files, installation instructions, or receipt checker. Include expected and actual behavior, reproduction steps, and relevant versions.

Search existing discussions and issues first. Share only non-sensitive text and evidence you have permission to publish; leave out credentials and private account links. No detector account is needed to ask for help or contribute writing feedback.

## Proposing changes

Keep each change focused. Explain the problem, the intended improvement, and how you checked it. Use concise prose, preserve factual qualifications and exact code, and distinguish an editing hypothesis from a measured result. AI-assisted contributions are welcome; review the final text and verify its claims before submitting it.

For experiments, retain the original and revised inputs, skill version, all attempts, and quality findings. Record detector settings, completed paired results, and warnings when measured. Keep unchanged and worse outcomes. Identify quotation effects separately from rewriting, and never present a detector score as proof of human authorship. See the [methodology](docs/methodology.md) and [limitations](docs/when-it-may-not-help.md).

## Local checks

For Python changes, use [uv](https://docs.astral.sh/uv/) with Python 3.10+ and run:

```sh
uv run --no-project python scripts/check_studies.py
uv run --no-project python -m unittest discover -s tests -v
uvx ruff check --fix .
```

For documentation or form changes, check links and any YAML you touched. Do not rewrite saved study inputs or reported outcomes to make a change pass validation. These local checks do not rerun detector scans.

Use a conventional commit title such as `docs: clarify installation` or `fix: reject inconsistent receipts`. Reference a relevant issue when there is one, and include validation results in the pull request.
