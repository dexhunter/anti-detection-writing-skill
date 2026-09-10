# Source selection and freeze

Two synthetic cases were selected for a prospective local-selector diagnostic: Python mutable list defaults and DNS NXDOMAIN caching after name creation. Each has six required claims with sources, limitations, protected inline identifiers and a natural 110–130-word answer target. Neither requires a code block or standalone command. No answer draft was written.

The Python case deliberately preserves a caller-supplied list, even when empty, so a truthiness shortcut or unconditional copy would violate the API. The DNS case uses explicit example numbers to distinguish a negative TTL from a newly created positive record TTL. Its remaining lifetime is an upper bound; expiry starts from the original cached response, not record creation. The case excludes serving expired data and other DNS mechanisms that would require a longer answer.

Facts were checked online against the official Python tutorial, FAQ and built-in type documentation, RFC 2308 sections 3/5/6, and official AWS Route 53 documentation. The AWS troubleshooting article was returned with its relevant content and AWS OFFICIAL marker by web search; subsequent direct opens failed, which is retained in its provenance field. RFC and AWS corroborate the negative caching rule. Source notes are factual paraphrases and distinguish supplied synthetic conditions, arithmetic and inferences from directly documented rules. No program behavior was exercised.

Only tracked public study README/results metadata and public question/case lists were searched for the two topics. novelty-audit.json records the complete file list, repository head and no-match result. Private confirmation and sealed holdout files were not opened. This check establishes no match in the inspected public metadata, not global originality or absence from training data.

These sources are frozen before any prospective answer generation or detector score. Keep future candidates and scoring receipts outside sources/. Do not modify facts, required claims or questions in response to scores. Meaning, code independence, input scope and factual review take precedence over detector performance.
