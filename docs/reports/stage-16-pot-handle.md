# Stage 16: pot-handle complaint on GPTZero 5.0b

This is a results record of one free-plan GPTZero session on 13 November 2026, Model 5.0b. Each text was scanned once. It is not a method for passing GPTZero. Human and mixed percentages, per-scan mode, account, and clock time were not logged. Where a figure was not logged, the table says “not logged”. The complaint is a synthetic UK consumer email: a pot handle broke, with an order number, a purchase date, a price, a payment method, refund-request dates, a Consumer Rights Act rejection, and photos available. No personal name, email address, or phone number is recorded here. The earlier human-scoring control is the Wood to Water v5 email from the [Stages 1–15 record](gptzero-results.md). Its source text stays withheld.

The Stages 1–15 CSV is not extended. These scans are not part of its 114 rows.

## Scope

**Not a general GPTZero bypass.** Every whole-text rewrite of this complaint scored 100% AI. The lowest fact-complete text in the session was 7% AI, on one email, at 177 words. A one-sentence change at the start of that text moved it to 16% and, with different wording, to 19%. Nothing here shows that the skill reliably defeats GPTZero, or that the same placement will score below 100% on another email.

Two comparability notes apply. The v5 control was already an Advanced scan in the earlier record, and this session does not log a mode on each new row. One advanced-labelled scan of about 178 words used about 178 credits. That credit note is not tied to a named row.

## What was scanned

The fresh panel is the human draft and 11 rewrites. The ladder applies one edit at a time to v5. The combination rows are not single-edit arms. The 7% text is listed once: it is the fact-complete relative-clause version, and it is the best fact-complete score in the session.

| Group | Edit | Words | AI % | Notes |
| --- | --- | ---: | ---: | --- |
| Fresh | Original human draft of the pot complaint | about 120 | 100 | One scan |
| Fresh | Eleven rewrites: plain, passive, mixed, timeline, legal, casual, signed and unsigned, and one built from a previous human-scoring email | about 120 | 100 | Each scanned once; every one was 100% |
| Control | Rescan of Wood to Water v5, previously 3% AI | not logged | 3 | Stable against the earlier Advanced scan |
| Ladder | Remove the greeting and the sign-off | not logged | 8 | One edit on v5 |
| Ladder | Change a date and add brand and product words inside an existing phrase | not logged | 3 | One edit on v5; the new date and the added words were not logged as a separate quotation |
| Ladder | Add the bracketed parenthetical “(bought on 18 October 2026, £42.75 paid with Shop Pay)” | not logged | 100 | One edit on v5 |
| Ladder | Insert a refund-history sentence in the middle | not logged | 5 | One edit on v5 |
| Ladder | Append a standalone sentence about photos | not logged | 57 | One edit on v5 |
| Combination | Remove or rewrite the closing escalation sentence | not logged | 100 | Confounded with other edits; remove and rewrite were not logged as separate scores |
| Combination | Same facts without the photos fact | not logged | 13 | |
| Combination | Photos fact as a mid-sentence relative clause: “Detachment of the handle, of which photos can be supplied along with the full email thread, took place…” | 177 | 7 | Best fact-complete text in the session |
| Combination | The same photos fact as a clause on the first sentence | not logged | 100 | |
| Combination | The same photos fact as a standalone final sentence | not logged | 100 | Distinct from the ladder’s 57% appended sentence |
| Wording | Change only the end of the first sentence of the 7% text, from “so this is a follow-up on that” to “so this report is being made to Shop” | 178 | 16 | No other edit |
| Wording | An alternative wording of that same ending | not logged | 19 | No other edit was described |

## Confirmed findings

Each point is tied to the rows above. This is one synthetic complaint plus one earlier control. These are not a general method for passing GPTZero.

1. A fresh draft and 11 whole-text rewrites, in the styles named in the table, all scored 100% AI. One of those rewrites was built from a previous human-scoring email. The unchanged v5 control rescanned at 3% AI. On this task, starting over did not keep the control’s score.

2. The bracketed parenthetical that added the purchase date, the price, and the payment method scored 100% AI. That was one edit on v5.

3. Putting the photos fact in the middle of an existing sentence, as a relative clause, scored 7% AI at 177 words. The same fact as a clause on the first sentence scored 100% AI. The same fact as its own final sentence scored 100% AI. A single appended photos sentence on v5, in the ladder, scored 57% AI. Leaving the photos fact out scored 13% AI. Placement and position both moved the score on this email. The rows do not say which feature the model used.

4. Three other single edits on v5 stayed low: greeting and sign-off removed, 8%; a date change plus brand and product words inside an existing phrase, 3%; a refund-history sentence inserted in the middle, 5%. Each is one edit. None of them is a recipe, and none of them is the fact-complete email by itself.

5. Removing or rewriting the closing escalation sentence scored 100% AI. Other edits were in the same text, so this row does not isolate that sentence.

6. The best fact-complete text scored 7% AI at 177 words. Changing only the end of its first sentence moved that text to 16% AI at 178 words, and an alternative wording of the same ending scored 19% AI. A small change at the start was enough to move the score. The 7% result is one wording of one email.

## Open hypotheses

These are not findings.

- A new fact is safer inside an existing sentence than as a bracket or a new final sentence. The 100%, 7%, 100%, and 57% photos rows are consistent with that on this email, and the first-sentence clause at 100% says “inside an existing sentence” is not enough by itself. The mechanism is not identified. This is the placement hypothesis carried into the skill, labelled there as our scans plus a mechanism hypothesis.

- Plain first person, and less legal boilerplate, may be easier to read. This session does not show that either one lowers a GPTZero score. The 7% text uses a formal relative clause. The legal-style rewrite in the fresh panel scored 100% AI, as did every other fresh style.

- Why v5 stays near 3% AI, and why the first-sentence ending moved 7% to 16% and 19%, is not established.

## Account and credits

GPTZero treated a Gmail plus-address and a Gmail dot-address as the same account, and it treated a plus-address on another domain the same way. The notice was “You already have an account”. A new free account needs an address that is actually a different account. No address is recorded in this note.

An advanced-labelled scan of about 178 words used about 178 credits. Credits were not logged for the other rows.

## What this changes in the skill

The skill text labels each new rule. The labels match the split above.

- **[evidence + our scans]** When a known human-scoring version exists, start from it and change as little as possible. Do not run a whole-text polish or rewrite over fact-dense text.
- **[our scans; mechanism hypothesis]** Add a new fact inside an existing sentence. Do not add it as a bracketed parenthetical or as a standalone appended sentence. Change one thing per scan.
- **[evidence]** Do not invent a detail or delete a fact to chase a score. Run `scripts/check_facts.py` on the fact-complete source and the candidate before a scan.
- **[hypothesis]** Prefer plain first person and keep legal boilerplate minimal where the facts allow. This is not a detector result.
- **[evidence]** Each scan session includes a known-human control and a known-AI control, and logs model version, scan mode, word count, and credits.
- Synonym swaps, “AI word” lists, and invisible characters are not detector levers. The readability list stays. The [literature update](../literature-update-2026-11-13.md) is the source for that downgrade. This session did not test a synonym swap.

## Proposed experiments

Not run. They are listed in the skill as experiments, not as findings.

1. Rescan noise: scan the best text twice, plus the known-human control, on the same model and mode, before treating a small gap as a real move.
2. Brackets versus a fact summary: the same facts with brackets and without them.
3. Whether a synonym swap moves Model 5.0b.

## Sources

- This session’s scan notes, 13 November 2026, GPTZero Model 5.0b, free plan, one scan per text.
- [GPTZero experiment results, Stages 1–15](gptzero-results.md), for the v5 control and the rule that its source text stays withheld.
