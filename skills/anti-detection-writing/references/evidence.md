# Evidence limits

Development observations on September 5–6, 2026 used GPTZero Basic Scan, displayed Model 4.9b. Across three complete, preselected five-question cohorts, plain rewriting reduced AI confidence in **0 of 15** cases. Separate LLM reviews rated eight revisions improved and seven equivalent, all passing technical review. Corrections and scope cuts were allowed, so this was a complete editing workflow comparison, not an isolated test of style.

Two of those cohorts also compared each fixed revised body with one relevant asker quotation selected before scanning. **5 of 10** quoted inputs reduced AI confidence; five remained at 100%. The reduced values were 93, 40, 1, 67, and 93% AI. All human confidences were zero. In particular, 1% AI was paired with **99% mixed, not 99% human**.

These small convenience samples establish neither a reliable bypass nor a general success probability. Adding a quotation changes content and length. The records do not establish why a classifier changes its output. A document confidence is not a measured fraction of words written by AI.

Additional exploratory rewrites failed, including six structural variants, one observation-led version, and two formatting controls. A quotation pilot scored 94% while its reserved transfer check remained at 100%. These are outside the two later five-question cohorts (ten quotation comparisons total). An adaptive candidate at 43% was rejected for incorrect advice; its corrected replacement scored 60% and passed review. Four later new answers scored 100, 93, 100, and 11%; they had no baseline or unquoted control.

The public repository contains 44 exact effective-editor inputs for the complete cohorts and the new answers. These are maintainer-recorded UI observations, not authenticated service exports. The raw account/browser records stay private. File hashes establish artifact integrity, not score authenticity. The reviews were separate LLM agents, not independent human raters. Acceptance, usefulness, repeatability, and human authorship were not measured. Five scans displayed a short-text warning.

The packaged instructions consolidate lessons from evolving development snapshots. They have not been prospectively validated as a fixed intervention. Treat future detector experiments as bounded hypothesis tests; retain all attempts, measure quality separately, and stop if improving a score requires degrading the answer.

## Later requested-alternative pilot

A subsequent four-case pilot on September 6 used newly authored Git, Docker, Kubernetes and PostgreSQL documentation questions. Under the frozen current instruction, the editor kept all four already-clear originals unchanged. A separately frozen exception permitting an explicitly requested measured alternative, combined with a scenario/action/consequence framing prompt, produced four different replies. This combined procedure is not an isolated test of the exception sentence.

All eight original/alternative texts passed a separate masked LLM quality review with no material loss of clarity or necessary qualifications. The reviewer slightly preferred three originals and one alternative. All eight fresh GPTZero Basic Scan / Model 4.9b results were **100% AI / 0% mixed / 0% human**, giving **0 reductions in 4 pairs**. Both Git and Docker versions carried short-text warnings; both longer pairs had no such warning. Original/current byte-identical texts shared one observation rather than being counted as independent scans.

The cases were new to the earlier local datasets, but the exception was proposed after observing the current arm's keep behavior. Baseline authoring was not isolated from prior skill context. These are synthetic convenience cases with one output per condition, an added framing prompt, and no ordinary-editing control. The exception supports trying an acceptable alternative when requested; this pilot establishes no detector-score improvement. Keep its eight observations separate from the historical 19-question/44-scan dataset and six-question comparison.

## Targeted edits across two detectors

A September 6 comparison added a diagnose-then-targeted-edit instruction to the frozen skill on two new synthetic answers about GitHub Actions concurrency and Python TaskGroup. Both originals were deliberately constructed with clarity problems. A separate score-blind LLM reviewer modestly preferred both revisions and verified all 17 claims and necessary qualifications. All four GPTZero Basic 4.9b scans remained 100% AI / 0% mixed / 0% human; all four Pangram 4.0 scans displayed 100% AI-generated text with medium confidence and short-text warnings. No repairs, retries or post-score edits were made.

This supports a limited clarity preference, with no detector improvement in either pair. It does not isolate the added instruction from the existing skill, measure human preference, or validate naturally occurring discussions. Do not promote targeted editing as a score-reduction technique from this result. Preserve readable prose for the reader's benefit; a stronger detector claim requires a new, comparable test. The public `studies/targeted-edit-1` record retains all eight observations separately from earlier cohorts.

## Autoresearch control-boundary comparison

On September 7, a separate selector chose one of three proposed rules for explaining interacting controls. Against the frozen installed incumbent, the new rule produced GPTZero Basic 4.9b AI-confidence changes of 100% → 100% and 91% → 100%. Separate blinded review passed all four answers and judged each pair equivalent. The candidate was rejected; confirmation cases stayed untouched.

A subsequent, explicitly adaptive check scanned the unchanged original for the incumbent's 91% Python edit. That original scored 100%, establishing a 9-point source-to-edit decrease for this exact pair. The edit had 9% mixed and 0% human confidence. A separate score-blind review preferred the edit and verified all nine claims. The original was scanned after the edit; neither was repeated. This observation does not validate the rejected rule or establish transfer. The [complete case study](https://github.com/dexhunter/anti-detection-writing-skill/tree/main/studies/autoresearch-controls-1) retains all five observations, frozen writing snapshots and the adaptive selection limitation. Use this as development evidence, not a new universal writing rule.

A later [same-input diagnostic](https://github.com/dexhunter/anti-detection-writing-skill/tree/main/studies/repeatability-1) repeated the existing Python edit at 91% AI / 9% mixed / 0% human and the rejected candidate at 100% AI / 0% mixed / 0% human. Both new Basic 4.9b results matched their earlier scores without short-text warnings. This was one additional observation per fixed text, selected after seeing the earlier difference, not a new skill or transfer test. The original was not repeated, so the complete source-to-edit comparison was not replicated. These observations also cannot distinguish deterministic scoring from caching. Keep the candidate rejected and the writing rules unchanged on this evidence.

## Reader reconstruction without an attributable repair

On September 9, a bounded trial tested frozen comprehension questions, a separate source-blind reader model, and one repair pass allowed only for misunderstandings attributable to the prose. The HTTP caching answer and complete skill tutorial passed separate final quality review, with both pairs judged equivalent. Neither repair stage admitted an edit. The technical outputs were byte-identical and unscanned. Two independent incumbent article drafts, 538 and 540 words including title and caption, both returned 100% AI / 0% mixed / 0% human in fresh GPTZero Basic 4.9b scans without short-text warnings.

This was no improvement: two scans consumed 1,078 word credits, confirmation was not unlocked, and the writing proposal was not promoted. Preserve first drafts and repair ledgers for a method with several stages; when the proposed stage makes no change, variation between separately composed outputs does not establish a benefit from that stage. This small trial does not show that reader feedback never helps. The [complete study](https://github.com/dexhunter/anti-detection-writing-skill/tree/main/studies/reader-reconstruction-1) retains the exact texts, selected policy and measurement summaries separately from earlier cohorts.

## Register analysis and independent draft selection

Later on September 9, selecting between two independent drafts failed because both candidate articles turned an ongoing validation limitation into a historical-only claim. A second method used a professional reference to plan one justified register change per case before fresh rewriting. All facts passed, but the control article was preferred for readability. Both formal rounds closed without scans.

An additional adaptive diagnostic repaired the crowded article paragraph and, before its new review or scores, changed its scan gate from relative non-inferiority to absolute suitability. All final texts passed, although the article control remained preferred. Four fresh GPTZero Basic 4.9b scans then returned 100% AI / 0% mixed / 0% human throughout, without short-text warnings: zero reductions across the technical and full-article pairs, using 1,305 free word credits. The [complete study](https://github.com/dexhunter/anti-detection-writing-skill/tree/main/studies/register-and-selection-1) preserves both failed rounds, both diagnostic protocols, the pre-repair article and exact measured inputs. No method was promoted or confirmation unlocked. The resulting time-scope and paragraph-density checks are fidelity/readability guidance, not demonstrated detector improvements.

## Full-article model transfer and artifact recovery

Two later local AuthorMist runs failed on the complete 541-word article. The custom decoder reached its time cap with corrupt output; native generation saved a more coherent partial output but stopped on an invalid-probability exception without EOS. An attention-kernel check did not reproduce a numerical discrepancy large enough to support the suspected runtime explanation. Neither failed run produced a detector measurement.

A separately declared recovery kept the exact complete first draft from the native output, repaired facts and grammar, then made one bounded fluency pass. The final 529-word article and 538-word control both passed all 18 claims and seven protected literals, but the independent LLM reviewer preferred the control. The recovery therefore remained unscanned and unpublished. Its factual editor had disclosed exposure to historical score summaries; the final reviewer received neither method identities nor new scores. The [full record](https://github.com/dexhunter/anti-detection-writing-skill/tree/main/studies/article-model-transfer-1) retains both model failures, the extraction, edits, review and provenance limits. It establishes no score reduction or general model failure rate.

## Sequential sections with prior-text context

A further [article experiment](https://github.com/dexhunter/anti-detection-writing-skill/tree/main/studies/windowed-article-1) used five fresh writers in sequence, each receiving its source section and the immutable revised prefix. The 526-word assembled article and fixed 538-word control passed all 18 claims and seven literals. The reviewer slightly preferred the control for clearer dates and measurement instructions, so the candidate remained unscanned under the declared gate.

The source notes contained the September 5–6 study range, but the relevant section packet omitted those notes and its claim said only "dated development sample." The control included the range. This preparation asymmetry limits the comparison; the result cannot isolate the effect of sequential writing. It supports checking evidence parity in writer packets, not a detector-performance claim. No further repair or method promotion followed.

## Paired editing demonstrations with prose-only measurement

The [September 9 demonstration trial](https://github.com/dexhunter/anti-detection-writing-skill/tree/main/studies/paired-editing-examples-1) added three fixed synthetic original/revision/judgment examples and a short diagnosis step. Separate fresh writers produced controls and candidates for the reused HTTP and X article cases. Masked review passed every claim and slightly preferred both candidates. All four fresh Basic 4.9b scans stayed at 100% AI / 0% mixed / 0% human, with no warnings; total usage was 1,374 word credits.

This round declared `prose_only`. Full messages and code were independently reviewed. The article's unchanged installation command was excluded while its title, prompts, qualifications and caption remained; the HTTP explanation had no independent code to exclude. Both arms received the updated prose-only measurement instruction. Earlier whole-message scores remain historical. Two preselected confirmation cases stayed unscanned, and the illustrative-example policy was not promoted. Neither the quality preference nor this scope change establishes a detector benefit.

## Phrase-list applicability checked September 9, 2026

These checks cover the vendor-derived entries and later additions in the [phrase review list](phrase-review.md).

On September 9, 2026, a separate reviewer checked all four frozen prose inputs in the [paired-example study](https://github.com/dexhunter/anti-detection-writing-skill/tree/main/studies/paired-editing-examples-1/outputs): HTTP baseline and candidate, and article baseline and candidate. Case-insensitive checks with word boundaries and normalized apostrophes found zero matches for the ten entries or the variants explicitly named in the source article. The input hashes matched the saved study.

That is an offline applicability check of the initial list. All four existing Basic 4.9b observations remain 100% AI / 0% mixed / 0% human. No text changed and no new detector scans ran for that check. The initial list offers no specific edit for those cases; its benefit for detector scores is unmeasured.

A separate follow-up on the same date checked all 23 additional entries against those four unchanged inputs, including ordinary inflections, normalized apostrophes, flexible whitespace and the contrast construction. It also found zero matches. Manual review of broader negations and contrasts retained the HTTP conditions and the article's necessary distinctions about measurement scope, quotations, confidence labels and validation. This expansion supplied no justified edit for those cases either; no new scan or detector benefit is claimed.

## GEPA prompt optimization checked September 9, 2026

A [bounded pilot](https://github.com/dexhunter/anti-detection-writing-skill/tree/main/studies/gepa-pilot-1) ran the pinned upstream GEPA optimizer with separate reflection, writing, quality-review and Chrome callbacks. It proposed two reusable changes to the writing section on one exposed HTTP case. Both outputs preserved all seven claims, but separate masked reviewers slightly preferred the incumbent. GEPA rejected both under the frozen no-preference-loss rule and kept its seed; the rejection utilities were not detector scores.

After that run closed, a separately declared diagnostic scanned both unchanged, factually acceptable outputs while retaining their preference losses. The shared seed and both candidates all scored 100% AI / 0% mixed / 0% human in GPTZero Basic 4.9b, without short-text warnings. These three prose-only scans used 377 free word credits; the baseline receipt was reused for comparison, not counted as another scan. Both proposals, the adaptive change of scan criteria, a discarded exposed writer, and a dispatch-wording difference are retained. No policy was promoted and two confirmation cases stayed sealed. This trial demonstrates no detector-score improvement or general impossibility.
