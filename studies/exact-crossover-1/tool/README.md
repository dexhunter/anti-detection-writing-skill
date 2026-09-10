# Exact crossover diagnostic

This standard-library tool follows the frozen protocol in the parent directory. It consumes two UTF-8 parent files and a source-review JSON file, validates their hashes and claim partitions, selects one seam deterministically, and saves two reciprocal byte-exact children plus `manifest.json` in a **new** output directory.

```sh
uv run --no-project python crossover.py --parent-a /path/a.txt --parent-b /path/b.txt --review /path/review.json --out /path/new-output --max-words 140
uv run --no-project python -m unittest -v
uvx ruff check --fix .
```

The default ceiling is 140 whitespace-delimited words. Counting covers the complete files supplied to the tool: it does not identify or remove code. Offsets and manifest ranges count UTF-8 bytes, with exclusive ends. No byte, including a newline, is inserted at the seam. Children must end in LF, fit the ceiling, and differ from each other and both parents. Any malformed seam invalidates the review; if the selected seam fails an output invariant, the tool stops without trying another seam. Invalid inputs and no-ops create no output directory. Existing output paths are refused.

The independent reviewer supplies sentence boundaries, claim attribution, semantic compatibility, protected-span meaning and relevance. These are reviewer responsibilities, not mechanical guarantees. The CLI cannot verify those judgments, readability, code correspondence, detector performance or eligibility for publication. It is a research diagnostic, not a factual validator or promoter. Tests use synthetic files inside temporary directories under this tool directory and never read development or confirmation answers.
