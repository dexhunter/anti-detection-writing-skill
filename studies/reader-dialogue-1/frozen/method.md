# One proposed experiment: reader questions before drafting

September 7, 2026. **Proposed and untested.** Add a bounded dialogue with a separate reader agent before the candidate writer produces its first complete passage. Test one initial question and one responsive follow-up, then draft once. The possible writing benefit is a better explanation of a distinction the reader needs to understand. Any GPTZero or Pangram effect remains unknown.

This proposal followed the previous [writing-methods-1](../../writing-methods-1/README.md) development trial. This exported copy removes local workspace and agent-operation details; the proposed operator is unchanged.

## Why this is distinct

The prior trials changed factual representation, answer order, expansion order, or sentence transitions. This procedure changes the writer's interaction: a separate agent asks a question, sees the answer, and chooses its next question from that answer before any final prose exists. Both arms retain the same original, evidence and claim inventory; no alternate fact table is introduced. There is no short answer core to expand, no prescribed action sequence, and no diagnosed sentence span to edit. The extra interaction and added context are part of the treatment, so this is a workflow comparison, not an equal-cost test isolating adaptivity.

## Primary evidence inspected

- [Shao et al., STORM, NAACL 2024, §§3.2, 5.2 and 6](https://arxiv.org/html/2402.14207v2): each question depends on earlier questions and grounded answers. Removing conversation in favor of generating all questions together reduced outline performance despite equal question counts. The full system also received better organization ratings from Wikipedia editors. These findings support investigating responsive questions during preparation. They concern retrieved evidence, multiple perspectives, outlines and long articles; they do not validate this two-round, fixed-evidence adaptation. The paper identifies unsupported connections between facts as a failure mode and supplies no commercial AI-detector result.
- [Authors' `knowledge_curation.py`, inspected on `main` September 7](https://github.com/stanford-oval/storm/blob/main/knowledge_storm/storm_wiki/modules/knowledge_curation.py): `ConvSimulator.forward` calls the questioner with accumulated `dlg_history`, obtains an answer, appends the turn, and repeats up to `max_turn`. This confirms an implemented feedback loop. I inspected the code but did not run or reproduce STORM; this dynamic link is not a pinned experimental dependency.

The local hypothesis is narrower: asking a source-grounded follow-up may expose a missing explanatory connection before composition. Whether the final explanation improves requires separate review.

## Exact operator

Freeze these instructions before showing any new cases or detector outcomes. Use the same model and observable settings for the incumbent and candidate writers. Give both the frozen installed skill, original passage, exact reader purpose, complete claim inventory, source evidence, protected strings and the same 300–350-word requirement. Original cases must already support that length; an insufficient packet is an admission failure, not permission to add material. Candidate instructions authorize a complete revision after the dialogue while preserving the factual contract.

**Reader agent, first turn.** Supply only the reader purpose, question, evidence, inventory and protected strings. Withhold the original, other candidate text and all scores.

> Before an explanatory passage is written, identify one question the specified reader would need answered to understand the supplied material. Target a meaningful relationship or distinction involving at least two supplied facts. Use only premises supported by this packet; do not invent a reader's experience, error, background or opinion. Return one question, the relevant claim IDs, and a brief note explaining why the answer matters to this reader. Maximum 80 words. Do not propose wording, an outline, a scenario, a metaphor or a draft. If the packet contains no suitable question, return `NO_SUPPORTED_CHALLENGE` with the reason.

**Candidate writer, answer turn.** Supply the initial reader question alongside the common packet.

> Answer this preparation question using only the supplied evidence. Return claim IDs plus concise analytical notes, at most 100 words. Preserve uncertainty and conditional scope; mark unsupported parts unresolved instead of guessing. These are preparation notes, not an opening paragraph or an incomplete draft. Do not write the final passage yet.

**Same reader agent, follow-up turn.** Supply the actual answer, retaining the reader's prior context.

> Read the answer. Ask at most one follow-up about a specific distinction or implication it leaves unclear for the stated reader. Name the part of the answer that prompted the question and the relevant claim IDs. Maximum 80 words. Do not repeat your first question or invent an objection. If it is fully resolved and no relevant supported follow-up remains, return `RESOLVED`. Do not supply prose or an outline.

If a follow-up exists, the same writer answers using the previous answer-turn instruction. Stop after this answer; no further dialogue or alternative questions.

**Same candidate writer, composition turn.** Supply the complete saved exchange and common packet.

> Now write one complete 300–350-word explanatory passage for the specified reader. Use what the dialogue clarified to decide what needs explanation and emphasis, while preserving every required claim and protected span from the common packet. The exchange is preparation, not a passage template: choose the organization freely. Do not reproduce it as a Q&A, quote the simulated reader, mention the review process, or force rhetorical questions. Do not turn the preparation answers into a core and append the remaining facts. Use only supplied evidence, with no invented context, personal voice, anecdotes, unsupported connections, errors or filler. Save the final passage separately from a claim-to-passage map. Return one final version without detector feedback.

## Boundaries and interpretation

Retain questions, answers, final text, claim map and input hashes. A `NO_SUPPORTED_CHALLENGE` result ends this method for that case as unexercised; do not keep generating questions until a useful one appears. An unresolved question cannot enlarge the evidence or justify a new claim. Do not hide a failed first attempt through regeneration.

Use independent reviewers with method labels, dialogue and detector results hidden for factual assessment and prose preference. Give them the original, full evidence and exact final outputs so they can catch omissions from the inventory itself. After that judgment, a separate process audit can check whether the candidate addresses the question and follow-up accurately. It is not independent evidence of reader preference.

Record actual lengths and material content differences even within the common band. Fail incorrect actors, changed causal claims, weakened conditions, artificial disputes and bloated caveats before scanning. Preserve no-ops and quality ties as such. Freeze detector admission, complete-pair budget, success and stopping rules separately; longer input does not guarantee the service will remove a warning. Development ties stop this hypothesis. An isolated detector decrease cannot establish the dialogue as its cause or justify a general skill update.
