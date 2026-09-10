# Export provenance and replay

This packet retains all six exact neutral-label prose drafts, the exact blinded review and packet, the quality-only gate, and the original no-op selection snapshot. Both top quality groups contain one answer, so neither case offers an eligible replacement. The separately frozen baseline addendum does not alter that selector outcome. Its commercial results belong in the separate baseline summary.

The inference manifest already uses portable relative paths and is copied byte-for-byte. Six input hashes, review hashes, source packet hashes and quality-gate hashes remain unchanged. The writer mapping records the sequential generation identities; the reviewer saw only neutral labels.

The public protocol and baseline addendum omit live account allowance. Their public freeze files retain both original hashes and hashes of sanitized copies. Export provenance records the source hash and exported hash for every copied or transformed artifact. The original selection.json remains byte-for-byte: its local_results_sha256 refers to the original private Greyscope results artifact. The public Greyscope results identify that original hash explicitly and retain every native output, calibrated full-precision score, token count and preparation hash. Removed filesystem paths do not change scores.

The Greyscope runtime manifest is a hash inventory, not a bundled runnable model. Model files, runtime environments, command logs, account/browser captures and detector document URLs are excluded. Metadata describing the original runtime is evidence about that run, not an independently executed reproduction. Author entrypoint parity was recorded for one input; no claim is made that all six had separate parity forwards.

Run the 26 synthetic offline selector tests from this directory with `uv run --no-project python -m unittest discover -s . -p test_selection_rule.py -v`. They use temporary synthetic fixtures and do not load model weights or access the archived commercial service. The exact-source selector review retains earlier failing runs and their resolutions.

To replay the archived selection without writing files, import selection_rule, call freeze_quality on this directory and compare the returned gate with quality-gate.json, then call select_candidates with that gate and greyscope/results.json records. The per-case outcomes should match selection.json. Do not invoke a phase that overwrites the preserved original selection artifact.

Hashes establish byte integrity and association, not independent authenticity of detector outcomes. This small synthetic convenience sample has no independent human quality ratings and supports no automatic selector promotion or general accuracy claim.
