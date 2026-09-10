# Exact crossover between complete drafts

September 10, 2026. **The selected parent and exact crossover hybrid both received 100% AI / 0% mixed / 0% human in GPTZero Basic Scan, Model 4.9b, with no warnings: zero reduction in one paired comparison.** Both passed the final claim and quality review; the independent reviewer slightly preferred the hybrid. No production writing policy changed and the method was not adopted.

Two fresh writers used the same frozen incumbent skill and complete HTTP source contract. A separate reviewer checked both parents and 36 possible boundary pairs: five were approved and 31 rejected. The archived review retains every disposition. The assembler selected byte offsets 211 in parent A and 205 in parent B using the frozen claim-balance rule and offset tie-break. It copied reciprocal prefixes and suffixes with **zero inserted bytes**.

| Candidate | Prose words | Separate selection | Basic AI / mixed / human |
| --- | ---: | --- | --- |
| Parent A | 122 | Retained, not selected | Unscanned |
| Parent B | 113 | Selected parent | 100 / 0 / 0 |
| Hybrid A: A prefix + B suffix | 114 | Selected hybrid | 100 / 0 / 0 |
| Hybrid B: B prefix + A suffix | 121 | Retained, not selected | Unscanned |

The two completed scans consumed 227 existing free word credits, matching the allowance change from 783 to 556. No credits or subscription were purchased. The two confirmation cases remained unopened and unscanned because development showed no reduction. Both parents, both assembled hybrids and every rejected boundary remain in the record; the unselected answers have no detector result.

The source, exact answers and traces are in `source/`, `parents/` and `hybrids/`. The boundary, selection and final quality reviews are in `reviews/`. The final review packet contains neutral labels X and Y; its identity mapping is stored separately in `method/final-review-mapping.json`. Judgments are independent LLM assessments, not human-reader findings. Reviewers inspected supplied RFC evidence; this study did not exercise HTTP client/server behavior. The selected texts contain no standalone code; all explanatory prose and inline identifiers belong to the declared prose-only measurement.

`observations/` retains exact answer, submitted, editor-before and editor-after text, alongside native-validator metrics and hashes of private receipt, UI-text and screenshot evidence. Each submission removed the answer's final LF; the editor added three LF characters. Before/after editor bytes matched for both scans. The validated receipt hashes match the archived metric records. These are operator-retained UI observations and consistency checks, not authenticated exports from the detector service. Raw receipts, browser UI and screenshots remain private. `results.json`, the reservation and measurement associations preserve the outcome, spend and exact reviewed-text correspondence.

The intervention is exact output crossover added to a shared two-parent pool. Its control already includes selection between two incumbent drafts. This does not test superiority to one incumbent call, execute GEPA, or reproduce LMX. The historical proposal in `method/proposal.md` allowed one predeclared seam newline. The later frozen `method/protocol.json` superseded that allowance, requiring no inserted newline or other byte; the executed assembler follows that stricter rule.

`tool/` preserves all three executed tool files byte-for-byte. Its historical README says the protocol is in the parent directory because that was the execution layout. In this public layout, the protocol is `method/protocol.json`; the CLI does not read it automatically. To reconstruct the hybrids from the study root, use:

```sh
uv run --no-project python tool/crossover.py --parent-a parents/a/answer.txt --parent-b parents/b/answer.txt --review reviews/boundary-review.json --out reconstructed-hybrids --max-words 140
uv run --no-project python -m unittest discover -s tool -v
```

The tool enforces hashes, byte boundaries, claim partitions, deterministic seam selection and output limits. Sentence boundaries, source-supported meaning, protected-span interpretation and readability require independent review. All 15 synthetic invariant tests and Ruff passed for the executed tool.

`export-manifest.json` records original and public hashes, source-relative names, public paths and exact versus sanitized copies. Sanitization changes local paths and internal reviewer routing labels only; candidate prose and code remain exact. Paths in sanitized metadata are relative to the study root or refer to the frozen repository commit. Historical SHA fields still identify the original source artifacts; use the export manifest to find a sanitized artifact's public hash. Reconstructing with the sanitized boundary review therefore produces the same child bytes but a different provenance manifest. The frozen incumbent file hashes are retained in `method/incumbent-manifest.json`; source files are available at the linked frozen commit in the sanitized operators.

This archive includes one reused development case, and the exact backend model and sampling details were unexposed. Role isolation used separate contexts on a shared filesystem and was operational rather than security-enforced. No confirmation case, confirmation manifest, browser/account UI, screenshot, detector document URL or credential is included. The generation record retains only previously recorded sealing hashes, not sealed contents. This pair establishes neither generalization nor that further improvement is impossible. Detector confidence does not establish human authorship, factual correctness or the cause of the unchanged result.
