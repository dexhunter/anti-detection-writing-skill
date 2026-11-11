# Phrase review

Use this list to find wording that may deserve an edit. Prioritize generic openings and claims that leave the actual action unexplained. An ordinary word used precisely can stay. Do not treat the list as a detector, an exhaustive catalogue or a requirement to eliminate every match.

## Source and scope

The initial ten entries are short excerpts from [GPTZero's October 7, 2024 article](https://gptzero.me/news/most-common-ai-vocabulary/), checked September 9, 2026. Its reported frequency differences describe associations in its data, not the probability that a particular passage has a given author. The linked [vocabulary FAQ](https://gptzero.me/ai-vocabulary) says changing flagged wording may or may not change the detector score. These dated lists do not establish the features or weights used by Basic Scan Model 4.9b. The editing suggestions here are our own contextual guidance.

## Initial GPTZero list

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

## GPTZero pattern categories

Checked September 10, 2026 in the signed-in [GPTZero app](https://app.gptzero.me/), under Basic Scan → AI Patterns. The preview lists the three categories and multipliers below; it directs users to Advanced Scan for text-specific findings. A visible preview label is not evidence that the current answer contains that pattern. The preview does not supply its dataset, denominator or calculation method, so keep these as vendor-reported associations, not probabilities, detector weights or expected score reductions. The examples and editing advice are ours, not excerpts from a GPTZero pattern definition.

| Category | Reported multiplier | Review for | Useful edit |
| --- | ---: | --- | --- |
| Empty commentary | 5.7× | Setup or evaluation that adds no fact: “It is worth noting that the cache may expire.” | State the useful fact directly: “The cache may expire.” Retain warnings, conditions and uncertainty. |
| Overblown importance | 5.3× | Unsupported claims of significance: “This is a groundbreaking improvement to the workflow.” | Name the supported change: “The workflow now records failed scans.” Do not invent impact, a comparison or a measured result. |
| Dressed-up verbs | 4.3× | An elaborate verb where a plain one has the same meaning: “Utilize the existing list.” | “Use the existing list.” Review “leverage” and “facilitate” in context; preserve distinctions such as enabling an action versus performing it, and literal technical meanings. |

Check the whole sentence, not just a keyword. “Under the stated caching assumptions” supplies a real qualification; it is not empty commentary. “Critical” can denote an actual severity, and “leverage” can have a precise domain meaning. Preserve these uses when supported. Do not manufacture a pattern match to explain an unchanged score.

## Additional words and constructions

Checked September 9, 2026. **Corpus observation** identifies usage differences in a particular research dataset. **Editorial heuristic** identifies a possible reading problem without a measured frequency or detector benefit here. Neither is a reason to rewrite an otherwise useful sentence.

| Review candidates | Evidence | Useful editing question |
| --- | --- | --- |
| delve; intricate; underscore; intricacies; realm; groundbreaking; garnered | [Juzek and Ward, COLING 2025](https://aclanthology.org/2025.coling-main.426.pdf), abstract and Appendix A: corpus observations | Can the sentence name the actual activity, relationship or achievement? Preserve a literal character name, security domain or other precise use. |
| comprehensive; crucial; additionally; notably | [Kobak et al., 2025](https://arxiv.org/html/2406.07016v5), §2.2: corpus observations | Does the adjective have a supported scope or necessity claim? Does the transition help the reader follow the argument? Keep it when it does. |
| “dive in”; “it's important to note that” | [GPTZero's November 2025 writing guide](https://gptzero.me/news/avoid-ai-detection-as-a-writer/), Tip 3: editorial heuristic | Can the reader start with the point itself? Keep the substantive warning or exception that follows. |
| “a myriad of” | Same GPTZero guide: editorial heuristic | Would a plain description of the relevant items be clearer? Do not invent a count. |
| tapestry; robust | [Humanizer at `9862685`](https://github.com/blader/humanizer/blob/9862685f575c65a8247f90369951df1b3416e3d6/SKILL.md), §12: editorial heuristic | Is the metaphor or praise doing useful work? Keep literal objects and technical properties; explain a robustness claim only as far as the evidence permits. |
| “at its core”; not just X but Y | Same Humanizer, §§1 and 3: editorial heuristic | Does the emphasis add a claim, or does the contrast correct a real misunderstanding? Keep distinctions the reader needs. |
| “experts argue”; “industry reports” | Same Humanizer, §17: editorial heuristic | Can the statement identify its real source and what that source found? Do not invent authority or erase an existing attribution. |
| “I hope this helps”; “Great question” | Same Humanizer, §22: editorial heuristic | Is conversational wrapping left in a standalone article or technical answer? Preserve greetings or closings that suit an actual correspondence. |
| “could potentially” | Same Humanizer, §9: editorial heuristic | Are two qualifiers doing one job? Simplify redundancy only while preserving the source's uncertainty. |

The academic studies concern abstracts, not our technical replies. The COLING paper's vocabulary-preference experiment did not find a significant overall preference difference; neither paper establishes a GPTZero reduction from these edits. Kobak et al. explicitly limit their method to corpus-level inference. Ordinary prepositions also occur in that study's marker set; importing the entire set as prohibited wording would damage useful prose.

A [BEA 2025 study](https://aclanthology.org/2025.bea-1.71.pdf) separately tested classifiers built from historical GPTZero vocabulary lists on student and generated essays. Its results depended on the generator; it did not run GPTZero's detector on vocabulary-removal rewrites. Use that as a reason to retain model, date and domain scope, not as a score claim for this checklist.

## Apply it to a draft

Review case-insensitive whole words and phrases in the explanatory prose, including obvious grammatical variants when context warrants. Do not flag arbitrary substrings inside identifiers or expand a source observation into a ban on an entire word family. Treat exact quotations, titles, code and standalone commands as protected; inline technical terms remain part of the prose and require contextual judgment.

For each useful edit, identify the reading problem first: vague action, unnecessary setup, repetition or mismatched register. Revise the sentence enough to solve that problem. Do not replace one conspicuous word with an obscure synonym, invent a mechanism, or delete a qualification to clear the list. Compare the result with the claim inventory and retain a clear original when the proposed edit adds nothing.

If a vocabulary-only hypothesis finds no applicable matches, record a no-op. Do not label an unrelated structural rewrite as a vocabulary intervention. A requested detector comparison still follows [measurement.md](measurement.md): fix exact inputs, check meaning independently, and compare completed scans. A zero-match result is not a detector pass and does not justify rescanning unchanged text.
