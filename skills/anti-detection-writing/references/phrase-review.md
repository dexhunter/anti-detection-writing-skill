# Phrase review

Use this list to find wording that may deserve an edit. Prioritize generic openings and claims that leave the actual action unexplained. An ordinary word used precisely can stay. Do not treat the list as a detector, an exhaustive catalogue or a requirement to eliminate every match.

## Source and scope

The ten entries below are short excerpts from [GPTZero's October 7, 2024 article](https://gptzero.me/news/most-common-ai-vocabulary/), checked September 9, 2026. Its reported frequency differences describe associations in its data, not the probability that a particular passage has a given author. The linked [vocabulary FAQ](https://gptzero.me/ai-vocabulary) says changing flagged wording may or may not change the detector score. This dated list does not establish the features or weights used by Basic Scan Model 4.9b. The editing suggestions here are our own contextual guidance.

## Review list

| Expression to review | Edit when useful; preserve when necessary |
| --- | --- |
| “Play a significant role in shaping” | Explain the supported contribution or relationship. Do not strengthen an association into causation. |
| “Showcasing” | Describe what the example demonstrates, if that is clearer. Keep it when presenting a showcase is the actual activity. |
| “Remarked” | Use neutral attribution when no nuance is needed. Preserve exact quotations and the intended reporting meaning. |
| “Aligns” | Explain the agreement or relationship if vague. Keep precise uses involving memory, geometry or layout. |
| “Aims to explore” | State the specific question or intended task. Preserve the distinction between a goal and a completed result. |
| “Today’s fast-paced world” | Remove a generic opening; retain a specific, supported time constraint if it matters. |
| “Notable works include” | List the works relevant to the reader. Do not invent a reputation claim to replace the adjective. |
| “Surpassing” | Prefer a concrete comparison with its threshold or quantity. Keep an already precise comparison. |
| “Tragically” | Keep it when it expresses the author's intended tone; remove it when it imposes unsupported emotion. |
| “Impacting” | Name the actual effect if it is known. Preserve a precise physical or domain-specific meaning. |

## Apply it to a draft

Review case-insensitive whole words and phrases in the explanatory prose, including obvious grammatical variants when context warrants. Do not flag arbitrary substrings inside identifiers or expand a source observation into a ban on an entire word family. Treat exact quotations, titles, code and standalone commands as protected; inline technical terms remain part of the prose and require contextual judgment.

For each useful edit, identify the reading problem first: vague action, unnecessary setup, repetition or mismatched register. Revise the sentence enough to solve that problem. Do not replace one conspicuous word with an obscure synonym, invent a mechanism, or delete a qualification to clear the list. Compare the result with the claim inventory and retain a clear original when the proposed edit adds nothing.

If a vocabulary-only hypothesis finds no applicable matches, record a no-op. Do not label an unrelated structural rewrite as a vocabulary intervention. A requested detector comparison still follows [measurement.md](measurement.md): fix exact inputs, check meaning independently, and compare completed scans. A zero-match result is not a detector pass and does not justify rescanning unchanged text.

## Applicability to the latest failed cases

On September 9, 2026, a separate reviewer checked all four frozen prose inputs in the [paired-example study](https://github.com/dexhunter/anti-detection-writing-skill/tree/main/studies/paired-editing-examples-1/outputs): HTTP baseline and candidate, and article baseline and candidate. Case-insensitive checks with word boundaries and normalized apostrophes found zero matches for the ten entries or the variants explicitly named in the source article. The input hashes matched the saved study.

That is an offline applicability check. All four existing Basic 4.9b observations remain 100% AI / 0% mixed / 0% human. No text changed and no new detector scans ran for this check. The list offers no specific edit for those cases; its benefit for detector scores is unmeasured.
