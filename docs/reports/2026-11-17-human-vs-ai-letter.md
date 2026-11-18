# Human-written vs AI-drafted recommendation letter: what differed (17 Nov 2026)

Public-safe summary. It contains no letter text, names or private details. The letters are described only generically.

## Setup

- **Texts.** A ~370-word recommendation letter from a professor, for a visa endorsement application. It was written in two ways:
  - **Human version.** A professional human writer wrote it from the same brief. A second pass then made small fixes: one opening sentence was reworded, one overclaim was corrected, two sentences were cut, and a stock two-sentence close was kept from the AI draft. The adopted text keeps a char-similarity of 0.90 to the writer's raw edit. The writer's raw edit shares only ~4% of its 4-grams with the AI draft, so it is new wording, not an edit of the AI draft.
  - **AI-drafted versions.** One LLM-drafted baseline (~430 words) plus 9 whole-letter rewrites of it. The rewrites changed vocabulary density, sentence length, active voice, paragraph order, first-hand framing and added numbers, and two of them added genuine quoted wording.
- **Detector.** GPTZero 5.0b on the free plan, one scan per text, read in the Basic view.
- **Scores.** The human version scored **1% AI / 99% mixed**, labelled "AI Polished" (human-written and polished with AI). The baseline and all 9 rewrites scored **100% AI**.
- **Secondary contrast.** A second letter, hand-edited at sentence level with no human writer, scored 53%. Scanned in three chunks, it gave 32%, 100% and 7%.
- **Caveats.** There is only one human version (n=1). It does not say exactly the same things as the AI drafts: the writer cut the biography recital, an independence disclaimer and some figures, and added concrete examples of leadership and future plans. Every causal claim below is therefore a hypothesis.

## Measured differences (regex heuristics, approximate)

| Feature | Human version | AI baseline | AI rewrites (range) |
|---|---|---|---|
| Words | 365 | 428 | 431–495 |
| Sentences | 23 | 20 | 19–37 |
| Mean sentence length (words) | 15.9 | 21.4 | 12.6–25.4 |
| SD sentence length | **4.3** | 9.1 | 4.8–16.0 |
| Longest sentence | 23 | 39 | 23–74 |
| Type-token ratio | **0.608** | 0.514 | 0.481–0.530 |
| MATTR (50-word window) | **0.878** | 0.812 | 0.788–0.833 |
| Share of words with 7+ letters | **0.334** | 0.192 | 0.142–0.201 |
| Nominalisations per 100 words | **6.0** | 2.3 | 1.8–2.7 |
| Passives | **0** | 5 | 1–5 |
| Sentences containing I/my/me | 9 | 13 | 12–19 |
| Sentences with the candidate as subject | 8 | 2 | 1–6 |
| Stock evaluative phrases (checklist hits) | **7** | 2 | 0–2 |
| Negations (not/never/no) | 0 | 3 | 3 (in the rewrites checked) |
| Approximators (about, mainly, more than...) | 1 | 5 | 3–5 (in the rewrites checked) |
| Sentences opening with a connective or temporal/conditional lead | 2 | 5 | 4–7 |
| Biography/credential sentences | 1 clause (title only; CV enclosed) | 5 | credentials kept in all 9 (moved or compressed in some; not counted per version) |

How the content was organised (hand-coded):
- **AI drafts.** A credentials recital, then relationship plus disclaimer, then a lay definition of the project, an external result with caveats, a short judgement and the close. The register is a tutorial for a non-expert. Things are described rather than named, step-by-step explanations appear, and in one place a rhetorical question frames the research.
- **Human version.** Title in one clause, then the relationship, a one-sentence definition, and paragraphs that each run claim → dated concrete action by the candidate → brief judgement. Benchmarks and tools are named, not explained. It ends with future work and UK benefit. Its judgements use conventional professional phrasing.
- **Most-flagged sentences in the AI versions.** These were the credentials/awards sentences (in 4 separate runs), a lay step-list, and definition/maintainer sentences.

## Evidence vs speculation

**Evidence:**
- The human-chosen wording scored 1% on GPTZero 5.0b, while ten AI-drafted variants of the same letter scored 100%.
- On summary stylometrics, the human letter is *more* lexically diverse, more Latinate, more nominal and more uniform in sentence length than every AI version. It also contains more "AI-sounding" evaluative phrases.
- AI rewrites that targeted any single surface feature never left 100%.

**Speculation (untested, n=1):**
- **Most likely cause.** A human chose the words. This fits earlier tests, where light AI edits of human drafts stayed human. It also fits published work showing that AI *generation* leaves a stylometric footprint while AI *editing* barely does. The direction of the summary statistics shows the detector is not keying on lexical diversity, sentence-length variance or stock-phrase counts. Model-specific word choice is the more plausible signal.
- **Possible contributors, none isolated.**
  - Dropping the credentials recital, which held the most-flagged sentences.
  - Dropping the lay-explainer register.
  - Fewer stacked hedges.
  - A cheap isolating test would be the AI baseline with only the credentials paragraph removed.
- **Unlikely causes on this evidence:**
  - "Burstiness" (sentence-length variety): the human version was more uniform, not more varied.
  - Plain vocabulary: the human version used longer, more varied words.
  - Removing stock phrases: the human version had more of them.
- **The "AI Polished" label.** It may come from the small AI-made fixes and the kept AI close, but this was not shown, because the free plan gives no sentence highlights.

## Lessons

These lessons are for future formal letters and professional writing. They keep the standing rules: preserve every fact, uncertainty and qualification, and never copy outside text word for word as a technique.

1. **Have a human choose the words of the whole document. Let AI check facts and fix small errors only.**
   - Evidence: 1% vs 100% across ten AI variants. The writer's text was ~96% new 4-grams, and the adopted version stayed within a light-edit budget (0.90 similarity to the writer's raw edit). This matches earlier email tests.
   - This is the strongest lesson, but it rests on n=1 for full letters.

2. **Don't optimise surface statistics as a humanizing target.** Plainer words, lower type-token ratio, short sentences, varied lengths, and fewer nominalisations or stock phrases are all surface targets.
   - Evidence: the human letter scored "worse" than the AI drafts on every one of these and still passed. The AI rewrites that pushed them stayed at 100%.

3. **Don't recite the writer's CV in the body.** Give the title in one clause and point to an enclosed CV, so the facts are kept but moved, not deleted.
   - Evidence: credential sentences were the top-flagged sentences in four runs, and the human version had none.
   - Untested in isolation, so treat it as a likely contributor, not a proven cause.

4. **Write at the reader's real level. Name the benchmark, tool or venue instead of describing it for a layperson.** Keep definitions to one short sentence. Avoid step-by-step "it does X, then Y, then keeps the best" explanations and rhetorical questions.
   - Evidence: the AI drafts used a tutorial register and a lay step-list was flagged. The second letter's 100% chunk was the one explaining an event to an outsider.
   - Counter-evidence: a chunk with a one-line definition scored 7%, so this is a tendency, not a rule.

5. **Build each paragraph as claim, then a dated, concrete action by the subject, then a short judgement.** Tie each judgement to the action just given.
   - Evidence: the human letter's structure.
   - Caveat: actor-first sentences on their own did not move the AI drafts, which stayed at 100% even with 4–6 actor-first sentences. Use this as a structure, not as a trick.

6. **Don't spend effort scrubbing conventional professional phrasing.** Phrases like "demonstrates leadership" or "gives me confidence" are normal in human formal letters.
   - Evidence: 7 checklist hits at 1% vs 0–2 hits at 100%.
   - Better use of effort: make sure each such phrase is backed by a stated example.

7. **Keep every needed qualification, but state each one once and plainly. Don't add hedges, disclaimers or approximations nobody asked for.**
   - Evidence: the AI drafts carried 3 negations and 3–5 approximators against 0 and 1 in the human version. Part of that gap is because the writer cut facts, which we must not do.
   - Scope or independence statements can go where the format expects them, such as a capacity line or a note to the signer, provided the signed letter still states them if they are needed.

8. **After a human draft, keep later edits small and fact-driven.** Fix overclaims and overlaps, keep the writer's sentence shapes, and don't run a whole-text "polish".
   - Evidence: the adopted text stayed at 0.90 similarity and scored 1%. Its residual "AI Polished" label may reflect the small AI-made fixes (not shown). Earlier tests found the "AI Polished" label grows as more sentences are polished.

9. **Judge by the whole-document score. Use chunk scans only to find which part is pulling the score up, then route that part back to a human.**
   - Evidence: the second letter scored 53% overall, with chunks at 32%, 100% and 7%. AI rewrites of its 100% chunk scored 100% again and pushed the whole letter back to 100%.
