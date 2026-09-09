Export note: Local reviewer identity is omitted. The integrity table retains hashes of the original review packet. The article files remain exact; source verification metadata in case.json was sanitized for this export. See [packet-manifest.json](packet-manifest.json) for exported hashes.

# Independent exact article quality review

Verdict: A PASS; B PASS. Reader usefulness/readability preference: B.

Reviewer fresh-context identity: `separate masked exact quality reviewer`. Actual model, settings and usage are unavailable. Review was limited to the four named packet files. No method identity was inferred. Historical Qwen figures in the article were treated as required source facts, not as measurements of either candidate.

The exact full title/body/caption counts are A: 529 words and B: 538 words using whitespace-separated tokens. Both are below 600; an alternative word-like-token count is also below the limit (A: 549, B: 542).

## Integrity

| File | Independently computed SHA-256 | Match |
| --- | --- | --- |
| case.json | `b1aa702e9186c973382675e179d35348966edd574ea6bc5bc578ab3ab2dc0a28` | Yes |
| A.txt | `f9409c735fa600a98d0709a38bf0c2983d8383c35e399c290cfd62ed94e7620f` | Yes |
| B.txt | `6a79ade61d31d7382f75ae2a57bfc6c37de39ff035e7fe7531522c125a150514` | Yes |
| hashes.json | `9e219cffe39aeb2bc55644d1af0b022aad1d15f1a1f45da1256d2692eb2337aa` | No supplied self-hash |

## Readability preference

- B starts with the concrete small-draft use case and immediately separates optional comparison from editing, including the absence of a guaranteed lower score.
- B uses direct instructional language and sentence-case headings, giving the installation and editing sequence a smoother progression.
- B makes the evidence boundary easier to interpret with the dated-evidence heading, quotation-comparisons wording and explicit statement that the counts exclude subsequent research.
- B’s concise paragraph about the identical answer body, changed content and length, and mixed confidence expresses the limitations with fewer awkward constructions than A.

Both versions pass every factual/protected-text requirement. That does not make their readability equivalent; B is the preferred article for the stated reader purpose. No preference is based on detector likelihood, guessed authorship or method identity.

## Arm A: PASS

All 18 claims and all 7 protected literals pass. Full artifact: 529 words. No unsupported additions, material omissions or blocking issues were found.

### Claim evidence

#### AX1: PASS

AX1: The skill offers repeatable editing to identify reader needs, preserve facts, improve flow and review; detector comparison is optional, without a success guarantee.

Exact supporting span(s):

> Anti-Detection Writing Skill lets your agent follow a repeatable editing process: understand what the reader needs, keep the facts intact, enhance flow, and review the result. You can also compare results using GPTZero.

> 3. Measure Detector Results If Needed.

The comparison is optional in the introduction and step 3. No guaranteed reduction or success claim appears; the unchanged-score advice and lack of prospective validation further constrain expectations. An explicit no-guarantee sentence is not needed for factual passage.

#### AX2: PASS

AX2: A reader can start with one reply, email or documentation section; editing and measurement are separate tasks.

Exact supporting span(s):

> Begin with a reply, email, or documentation section.

> 2. Provide context and original text.

> 3. Measure Detector Results If Needed.

One small draft is the starting point; editing and optional measurement have separate numbered steps.

#### AX3: PASS

AX3: Install with the exact npx command; choose the agent in the installer; the default scope is the current project.

Exact supporting span(s):

> npx skills add dexhunter/anti-detection-writing-skill --skill anti-detection-writing

> Select your agent in the installer. Default installation uses the current project.

Exact installation command, agent selection and current-project default all remain.

#### AX4: PASS

AX4: Supply the original text, intended audience and purpose. Technical replies also need their question, relevant documentation and version constraints.

Exact supporting span(s):

> 2. Provide context and original text.

> Tell the agent who is reading and what they need to accomplish. If the text is technical, include the question and any relevant docs and version limits.

The heading supplies the original-text requirement, and the following paragraph supplies audience, purpose and technical context.

#### AX5: PASS

AX5: The example editing request asks for smoother readable prose, preservation of facts/code/qualifications, removal of repetition and irrelevant background, explanations of factual corrections and separate review of exact final text.

Exact supporting span(s):

> "Use $anti-detection-writing to make this text smoother and easier to read for [audience]. Preserve facts, code, and qualifications. Remove repetition and irrelevant background. Explain any factual corrections and get a separate review of the exact final text."

Every requested editing requirement remains, including a separate review of the exact final text.

#### AX6: PASS

AX6: Useful edits may move prerequisites, clarify pronouns or remove repeated explanations, while preserving the meaning of the advice.

Exact supporting span(s):

> The skill may adjust the text by moving prerequisites ahead of instructions, replacing vague pronouns, or cutting repeated explanations. Continually check that the advice still means the same thing.

All three editing examples and preservation of meaning remain.

#### AX7: PASS

AX7: Optional comparison uses original and final text in GPTZero Basic Scan with the same displayed model; save exact inputs, all three confidences, dates, warnings, unchanged results and worse results.

Exact supporting span(s):

> 3. Measure Detector Results If Needed.

> "Compare original and final text using GPTZero Basic Scan with the same displayed model and record exact inputs, all three confidences, dates, and warnings. Record unchanged and worse results as well."

All required comparison conditions and recordkeeping categories remain.

#### AX8: PASS

AX8: Live scanning needs the user's own detector access and an agent-supported browser tool. The skill supplies neither. Review correctness/readability separately from score.

Exact supporting span(s):

> Live scanning requires access to your own detector and a browser tool your agent supports. The skill supplies neither.

> Review correctness and readability separately from the score.

Both user-supplied scanning dependencies and the separate quality review are explicit.

#### AX9: PASS

AX9: A saved Qwen Code reply pair was freshly rechecked September 6, 2026 using GPTZero Basic Scan Model 4.9b: before AI100/Mixed0/Human0; after AI1/Mixed99/Human0.

Exact supporting span(s):

> A fresh recheck of one saved Qwen Code reply showed 100% AI/0% mixed/0% human → 1% AI/99% mixed/0% human with GPTZero Basic Scan Model 4.9b on September 6, 2026.

The exact dated Qwen recheck, native category order and both values remain.

#### AX10: PASS

AX10: The existing screenshots show that completed Qwen recheck, not this article or a new prospective test of the packaged skill.

Exact supporting span(s):

> Screenshots show these completed scans, not scans of this article. This recheck repeated a development case; it is not a new prospective test of the packaged skill.

The immediately preceding Qwen sentence identifies the scans; the text explicitly excludes article scores and a new prospective packaged-skill test.

#### AX11: PASS

AX11: The measured change added one short relevant asker quotation while the answer body stayed identical. Content and length both changed; it does not isolate a rewriting benefit.

Exact supporting span(s):

> The change involved adding one short relevant asker quote to an otherwise identical answer. The comparison changed content and length; this does not show benefits from rewriting alone.

One relevant short quotation is added to an otherwise identical answer, with both content and length confounding a rewriting-only interpretation.

#### AX12: PASS

AX12: 99% mixed does not mean 99% human and lower confidence does not establish human authorship.

Exact supporting span(s):

> Scores of 99% mixed do not indicate 99% human. Lower AI confidence does not establish human authorship.

Both mixed-versus-human and authorship limitations are explicit.

#### AX13: PASS

AX13: In the dated development sample, 5 of 10 quotation comparisons reduced AI confidence, while 0 of 15 plain-rewrite comparisons did. These are development-sample counts, not all subsequent research.

Exact supporting span(s):

> Among 10 quoted comparisons in the September 5–6, 2026 development sample, five reduced AI confidence; plain rewriting reduced AI confidence in 0 of 15 comparisons.

Five of ten and zero of fifteen remain scoped to the September 5–6, 2026 development sample. The sentence does not claim totals for subsequent work.

#### AX14: PASS

AX14: Separate LLM reviewers rated eight plain revisions clearer and seven equivalent; this is not a human preference study.

Exact supporting span(s):

> Separate LLM reviewers rated eight plain edits as clearer and seven as equivalent. This was not a human preference study.

Eight clearer and seven equivalent remain LLM reviewer judgments, with an explicit exclusion of a human preference study.

#### AX15: PASS

AX15: Observations are completed UI scans; the current packaged skill has not been prospectively validated for reliable detector performance.

Exact supporting span(s):

> Observations come from completed UI scans; the current packaged skill hasn't been prospectively validated for reliable detector performance.

Completed UI scans support the observations; reliable detector performance of the current packaged skill remains unvalidated prospectively.

#### AX16: PASS

AX16: Include a quotation only when it helps answer the question. A correct clear edit can remain useful with an unchanged score, subject to the user's publication requirements.

Exact supporting span(s):

> Use quotes when they help answer the question. Stick to clear, correct edits even if the detector score is unchanged, subject to your publication requirements.

Quotation use is conditioned on answering the question, and unchanged scores do not erase a correct clear edit subject to publication requirements.

#### AX17: PASS

AX17: Readers can try a draft and share improvements or failures in Discussions. The repository contains exact inputs, measured examples and unsuccessful cases; preserve both destination URLs.

Exact supporting span(s):

> Try this on one draft and discuss what worked and what didn't in Discussions. The repository includes exact inputs and measured examples along with failed cases.

> Repository: https://github.com/dexhunter/anti-detection-writing-skill

> Discussions: https://github.com/dexhunter/anti-detection-writing-skill/discussions

The invitation, all three repository evidence categories and both destinations remain.

#### AX18: PASS

AX18: Preserve a caption for the two genuine before/after screenshots: same Qwen body plus quotation, native confidence triplets, Basic Scan Model 4.9b, September 6 recheck, visible panels plus partial input, full inputs linked in repository, content/length change. No screenshot score is attributed to the article.

Exact supporting span(s):

> Before: plain Qwen Code answer at 100% AI/0% mixed/0% human. After: same answer plus one short relevant quote from the asker, 1% AI/99% mixed/0% human. Fresh recheck on September 6, 2026 using GPTZero Basic Scan, Model 4.9b. Genuine screenshots show result panels and parts of each input; the full inputs are linked in the repository. Quotes change content and length.

The complete caption preserves Qwen attribution, identical-answer-plus-quotation comparison, both native triplets, scan mode/model/date, genuine screenshots, panels plus partial inputs, repository full inputs, and content/length change.

### Protected literals

| Exact literal | Result | Exact substring occurrences |
| --- | --- | --- |
| `npx skills add dexhunter/anti-detection-writing-skill --skill anti-detection-writing` | PASS | 1 |
| `$anti-detection-writing` | PASS | 1 |
| `GPTZero Basic Scan` | PASS | 3 |
| `4.9b` | PASS | 2 |
| `September 6, 2026` | PASS | 2 |
| `https://github.com/dexhunter/anti-detection-writing-skill` | PASS | 2 |
| `https://github.com/dexhunter/anti-detection-writing-skill/discussions` | PASS | 1 |

The repository URL count includes its occurrence as the Discussions URL prefix; a separate labeled Repository destination is also present.

### Purpose, qualifications and presentation

- PASS: Complete installation/use article and screenshot caption for readers interpreting the dated evidence.
- PASS: Historical sample and Qwen recheck remain separate from current prospective validation status.
- PASS: 5/10, 0/15, eight clearer, seven equivalent, AI/mixed/human 100/0/0 and 1/99/0 are preserved.
- PASS: Screenshots are the completed Qwen recheck; no score is attributed to this article.
- PASS: LLM judgments are identified; no human preference study or established human authorship is claimed.
- PASS: A complete title, numbered steps, readable prompts, repository links and a standalone caption remain suitable for plain-text X article presentation.

Added qualifications about article-score attribution, human authorship, human preference studies and current reliable detector performance are supported by the supplied claims. Dated sample scope is supported by the supplied case. No later study or new detector outcome is introduced.

Nonblocking readability issue: “Among 10 quoted comparisons” — The compressed phrase is less precise on first reading than B’s quotation comparisons. The surrounding quotation paragraph and dated sample make the intended category recoverable; this is a readability issue, not a factual failure.

## Arm B: PASS

All 18 claims and all 7 protected literals pass. Full artifact: 538 words. No unsupported additions, material omissions or blocking issues were found.

### Claim evidence

#### AX1: PASS

AX1: The skill offers repeatable editing to identify reader needs, preserve facts, improve flow and review; detector comparison is optional, without a success guarantee.

Exact supporting span(s):

> The skill gives your agent a repeatable editing process: identify the reader's needs, preserve the facts, improve the flow, and review the result. You can request a detector comparison separately, with no guarantee of a lower score.

All editing stages remain; optional separate measurement and no guaranteed lower score are explicit.

#### AX2: PASS

AX2: A reader can start with one reply, email or documentation section; editing and measurement are separate tasks.

Exact supporting span(s):

> Start with one reply, email, or section of documentation.

> You can request a detector comparison separately, with no guarantee of a lower score.

A single reply, email or documentation section is the starting point; separate comparison is explicit.

#### AX3: PASS

AX3: Install with the exact npx command; choose the agent in the installer; the default scope is the current project.

Exact supporting span(s):

> npx skills add dexhunter/anti-detection-writing-skill --skill anti-detection-writing

> Choose your agent in the installer. The default installation is for the current project.

Exact installation command, agent selection and current-project default all remain.

#### AX4: PASS

AX4: Supply the original text, intended audience and purpose. Technical replies also need their question, relevant documentation and version constraints.

Exact supporting span(s):

> 2. Give the agent context and the original

> Include the intended audience and what they need to do. For a technical reply, supply the question, relevant documentation, and version constraints.

The heading requests the original, and the next paragraph supplies audience, purpose and technical context.

#### AX5: PASS

AX5: The example editing request asks for smoother readable prose, preservation of facts/code/qualifications, removal of repetition and irrelevant background, explanations of factual corrections and separate review of exact final text.

Exact supporting span(s):

> “Use $anti-detection-writing to make this text smoother and easier to read for [audience]. Preserve its facts, code, and qualifications. Remove repetition and irrelevant background. Explain any factual corrections, and get a separate review of the exact final text.”

Every requested editing requirement remains, including a separate review of the exact final text.

#### AX6: PASS

AX6: Useful edits may move prerequisites, clarify pronouns or remove repeated explanations, while preserving the meaning of the advice.

Exact supporting span(s):

> Useful edits include moving a prerequisite before an instruction, replacing an ambiguous pronoun, or removing a repeated explanation. Check that the advice still means the same thing.

All three editing examples and preservation of meaning remain.

#### AX7: PASS

AX7: Optional comparison uses original and final text in GPTZero Basic Scan with the same displayed model; save exact inputs, all three confidences, dates, warnings, unchanged results and worse results.

Exact supporting span(s):

> 3. Request measurement if you need it

> “Compare the original and final text using GPTZero Basic Scan. Use the same displayed model. Record the exact inputs, all three confidences, dates, and warnings. Keep unchanged and worse results too.”

All required comparison conditions and recordkeeping categories remain.

#### AX8: PASS

AX8: Live scanning needs the user's own detector access and an agent-supported browser tool. The skill supplies neither. Review correctness/readability separately from score.

Exact supporting span(s):

> Live scanning needs your own detector access and a browser tool your agent supports; the skill supplies neither. Review correctness and readability separately from the score.

Both user-supplied scanning dependencies and the separate quality review are explicit.

#### AX9: PASS

AX9: A saved Qwen Code reply pair was freshly rechecked September 6, 2026 using GPTZero Basic Scan Model 4.9b: before AI100/Mixed0/Human0; after AI1/Mixed99/Human0.

Exact supporting span(s):

> On September 6, 2026, a fresh recheck of one saved Qwen Code reply pair returned 100% AI / 0% mixed / 0% human → 1% AI / 99% mixed / 0% human in GPTZero Basic Scan, Model 4.9b.

The exact dated Qwen pair recheck, native category order and both values remain.

#### AX10: PASS

AX10: The existing screenshots show that completed Qwen recheck, not this article or a new prospective test of the packaged skill.

Exact supporting span(s):

> The screenshots show those completed scans, not scores for this article or a new prospective test of the packaged skill.

The immediately preceding Qwen sentence identifies the scans; article scores and a new prospective packaged-skill test are explicitly excluded.

#### AX11: PASS

AX11: The measured change added one short relevant asker quotation while the answer body stayed identical. Content and length both changed; it does not isolate a rewriting benefit.

Exact supporting span(s):

> The answer body stayed identical; the change added one short, relevant asker quotation. Both content and length changed, so this comparison does not isolate a rewriting benefit.

The answer body remains identical, with a single short relevant quotation added; content and length changes preclude isolating a rewriting benefit.

#### AX12: PASS

AX12: 99% mixed does not mean 99% human and lower confidence does not establish human authorship.

Exact supporting span(s):

> A 99% mixed result is not 99% human, and lower AI confidence does not establish human authorship.

Both mixed-versus-human and authorship limitations are explicit.

#### AX13: PASS

AX13: In the dated development sample, 5 of 10 quotation comparisons reduced AI confidence, while 0 of 15 plain-rewrite comparisons did. These are development-sample counts, not all subsequent research.

Exact supporting span(s):

> In the September 5–6 development sample, 5 of 10 quotation comparisons reduced AI confidence; plain rewriting reduced it in 0 of 15 comparisons. These counts cover that sample, not subsequent research.

Five of ten and zero of fifteen remain in the dated development sample, explicitly excluding subsequent research totals. The adjacent recheck sentence supplies the 2026 context.

#### AX14: PASS

AX14: Separate LLM reviewers rated eight plain revisions clearer and seven equivalent; this is not a human preference study.

Exact supporting span(s):

> Separate LLM reviewers rated eight plain revisions clearer and seven equivalent; this was not a human preference study.

Eight clearer and seven equivalent remain LLM reviewer judgments, with an explicit exclusion of a human preference study.

#### AX15: PASS

AX15: Observations are completed UI scans; the current packaged skill has not been prospectively validated for reliable detector performance.

Exact supporting span(s):

> The observations came from completed UI scans. The current packaged skill has not yet been prospectively validated for reliable detector performance.

Completed UI scans support the observations; reliable detector performance of the current packaged skill remains unvalidated prospectively.

#### AX16: PASS

AX16: Include a quotation only when it helps answer the question. A correct clear edit can remain useful with an unchanged score, subject to the user's publication requirements.

Exact supporting span(s):

> Use a quotation only when it helps answer the question. A clear, correct edit can remain useful with an unchanged score, subject to your publication requirements.

Quotation use is limited to helping answer the question, and unchanged scores do not erase a correct clear edit subject to publication requirements.

#### AX17: PASS

AX17: Readers can try a draft and share improvements or failures in Discussions. The repository contains exact inputs, measured examples and unsuccessful cases; preserve both destination URLs.

Exact supporting span(s):

> Try one draft and share what improved or fell short in Discussions. The repository includes exact inputs, measured examples, and unsuccessful cases.

> Repository: https://github.com/dexhunter/anti-detection-writing-skill

> Discussions: https://github.com/dexhunter/anti-detection-writing-skill/discussions

The invitation, all three repository evidence categories and both destinations remain.

#### AX18: PASS

AX18: Preserve a caption for the two genuine before/after screenshots: same Qwen body plus quotation, native confidence triplets, Basic Scan Model 4.9b, September 6 recheck, visible panels plus partial input, full inputs linked in repository, content/length change. No screenshot score is attributed to the article.

Exact supporting span(s):

> Caption: Before: Qwen Code answer, 100% AI / 0% mixed / 0% human. After: the identical body plus one relevant asker quotation, 1% AI / 99% mixed / 0% human. GPTZero Basic Scan, Model 4.9b; fresh recheck on September 6, 2026. These genuine screenshots show the result panels and part of each input; complete inputs are linked in the repository. Adding a quotation changes content and length.

The complete caption preserves Qwen attribution, identical-body-plus-quotation comparison, both native triplets, scan mode/model/date, genuine screenshots, panels plus partial inputs, repository full inputs, and content/length change. The shortness of the quotation is explicit in the body.

### Protected literals

| Exact literal | Result | Exact substring occurrences |
| --- | --- | --- |
| `npx skills add dexhunter/anti-detection-writing-skill --skill anti-detection-writing` | PASS | 1 |
| `$anti-detection-writing` | PASS | 1 |
| `GPTZero Basic Scan` | PASS | 3 |
| `4.9b` | PASS | 2 |
| `September 6, 2026` | PASS | 2 |
| `https://github.com/dexhunter/anti-detection-writing-skill` | PASS | 2 |
| `https://github.com/dexhunter/anti-detection-writing-skill/discussions` | PASS | 1 |

The repository URL count includes its occurrence as the Discussions URL prefix; a separate labeled Repository destination is also present.

### Purpose, qualifications and presentation

- PASS: Complete installation/use article and screenshot caption for readers interpreting the dated evidence.
- PASS: Historical sample and Qwen recheck remain separate from current prospective validation status.
- PASS: 5/10, 0/15, eight clearer, seven equivalent, AI/mixed/human 100/0/0 and 1/99/0 are preserved.
- PASS: Screenshots are the completed Qwen recheck; no score is attributed to this article.
- PASS: LLM judgments are identified; no human preference study or established human authorship is claimed.
- PASS: A complete title, numbered steps, readable prompts, repository links and a standalone caption remain suitable for plain-text X article presentation.

Added qualifications about article-score attribution, human authorship, human preference studies and current reliable detector performance are supported by the supplied claims. Dated sample scope is supported by the supplied case. No later study or new detector outcome is introduced.

No concrete readability issue requires qualification of this pass.

Review only: no revisions, proposed rewrites, scans, publication or additional research.
