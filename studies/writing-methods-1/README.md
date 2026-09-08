# Writing methods: quality screening and a preservation comparison

September 7, 2026. **No detector reduction was observed, and no new writing method was promoted.** This is a limitations study, not a showcase success.

Four fresh writers used the same installed skill snapshot on two newly authored synthetic cases: an HTTP caching explanation and an invented project update. The baseline applied the current skill. Three alternatives used a nonprose fact map, expanded a short answer core, or checked sentence-topic continuity. Two independent LLM reviewers saw randomly labelled outputs and source contracts, with methods and detector results hidden. A separate selector applied the frozen quality and simplicity rules before any scans.

| Method | Quality outcome | Detector testing in the main round |
| --- | --- | --- |
| Current-skill baseline | Both pass | Both Pangram; technical GPTZero |
| Relation-map reconstruction | Technical passes; business adds an unsupported copying actor | Excluded before scanning |
| Core expansion | Both pass; readability ties with baseline | Unselected and unscanned |
| Topic continuity | Both pass; readability ties with baseline | Selected by simplicity tie-break |

The selected method returned both originals unchanged except for a terminal newline. The measured comparison therefore tests **preservation versus the current skill's rewrite**. It does not exercise sentence-topic edits or establish that they lower scores. All eight outputs, including the failed and unselected drafts, are retained in [outputs](outputs).

| Complete input pair | Current-skill rewrite | Preserved original |
| --- | --- | --- |
| Technical — GPTZero Basic 4.9b | AI 100%, mixed 0%, human 0% | AI 100%, mixed 0%, human 0% |
| Technical — Pangram 4.0 | AI Generated; 100% AI text | AI Generated; 100% AI text |
| Project update — Pangram 4.0 | AI Generated; 100% AI text | AI Generated; 100% AI text |

Pangram reported a short-text confidence warning and medium segment confidence for every scan. Its text proportions differ from GPTZero's document confidences. Four Pangram submissions used eight credits; two GPTZero submissions used 243 words. The full phases were reserved before their first submissions. Six native receipts passed exact-input, editor/rendering and visible-result checks locally. Raw browser evidence remains private because it includes account details; [results.json](results.json) retains native values, warnings, input hashes and private receipt hashes. Those records are operator evidence, not independent service authentication.

The primary advance criterion failed, so the two unused confirmation cases were neither released nor scanned. The core-expansion and relation-map methods have **no detector result in the main round**. Their nonselection or rejection there must not be described as detector failures.

The factual failure originated in preparation: a passive source statement did not name who copied the articles, but the relation table supplied a migration team. The coordinator missed that addition; the independent reviewer caught it. The resulting skill clarification preserves unspecified actors in both fact tables and final prose, using passive voice when necessary. It does not recommend passive voice to influence detectors.

The [frozen protocol](frozen/protocol.json), [writing snapshot](frozen/SKILL.md), [method instructions](methods), [source contracts](sources/development.json), [quality reviews](reviews) and [selection](reviews/selection.json) make the decision inspectable. The writing snapshot captures the installed skill, including pre-existing local changes; it is not a claim that published `main` had identical instructions. The snapshot's reference links were not followed by writers and are not an installable copy of the skill.

This small synthetic study has no human-authored control, no independent human quality panel and no confirmation measurement. The relation packet removed sentence templates but largely retained conceptual order. No general efficacy conclusion follows from these two cases.

## Separate core-expansion follow-up

After the round stopped, a separately frozen adaptive probe compared the already reviewed core-expansion technical draft with a fresh scan of the baseline. The candidate had been generated and reviewed before any scores; choosing to scan it afterward was adaptive. This probe allowed exactly two Pangram submissions and no confirmation cases.

Both Pangram 4.0 results were **AI Generated, 100% displayed AI text**, with short-text warnings and medium segment confidence. The pair used four credits and showed no reduction. Core expansion now has one measured technical pair, while its business draft remains unmeasured. It has no GPTZero result here. See the [exact texts, protocol and results](core-followup).

Across the main round and follow-up, eight native receipts were validated: six Pangram scans using 12 credits and two GPTZero scans using 243 words. Neither phase supports a detector-reduction method. Their results remain separate rather than replacing the original selection or denominator.
