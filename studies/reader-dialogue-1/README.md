# Reader dialogue before drafting

September 7, 2026. **No detector reduction was observed.** In one synthetic development case, Pangram 4.0 classified both the current-skill baseline and the revised dialogue candidate as **AI Generated**, with **100% of the text identified as AI**. Both results showed high segment confidence and no short-text warning. This trial supplies no detector-performance improvement to adopt in the skill.

## What was compared

The [fictional library case](frozen/common-case.json) asks for a complete, approximately 300–350-word explanation of a room-booking pilot and the proposed conditions for considering expansion. It contains 24 source facts and 20 required claims. A separate agent constructed the case without reading the writing skill, earlier experiments, detectors or holdouts.

The baseline writer used the [frozen skill entrypoint](frozen/skill/SKILL.md), original article, source brief, claim inventory and [common writing instructions](frozen/common-operator.txt). A separate candidate writer received the same inputs plus a short preparation dialogue: a reader asked one source-grounded question, saw the writer's analytical answer, and asked one response-dependent follow-up. The reader did not see the original article, drafts or detector results. Both writers used fresh contexts and inherited the same configured model and effort; the exact runtime model identifier was not exposed.

This procedure was motivated by the responsive question-and-answer preparation in [Shao et al.'s STORM paper](https://arxiv.org/html/2402.14207v2). STORM investigates a broader system for researching and writing long articles. This two-question, fixed-evidence adaptation neither reproduces that system nor inherits evidence of a commercial detector benefit. The [frozen method](frozen/method.md) records the adaptation and its limits.

## Review and revision before scanning

The first reader question asked why continuing unaccommodated requests should support considering more rooms only alongside staff coverage and booking reliability. The follow-up asked why timely cancellation counts toward the proposed reliability threshold without establishing actual room use. The [saved exchange](dialogue/question-1.json) links these questions and answers to the source facts.

A separate masked agent reviewer found both first-pass articles factually acceptable, preserving all 20 claims, but **modestly preferred the baseline's clarity**. The initial candidate was therefore not admitted for scanning. The protocol allowed one pre-score clarity repair: the writer explicitly paired each possible explanation with its observation, stated the three necessary expansion conditions and their time period, moved the cancellation explanation beside the threshold, and removed a repetitive clause.

A fresh masked agent reviewer assessed the exact revised pair without method labels, dialogue, detector scores or the earlier review. Both articles passed all 20 claims, with **a quality tie**. These were agent judgments, not a human-reader study. The record retains the [first review](reviews/quality-review.json), [repair decision](reviews/repair-decision.json), and [final review](reviews/final-quality-review.json). The first-pass labels were A = candidate and B = baseline; the final labels were A = baseline and B = repaired candidate.

The measured treatment is consequently **reader dialogue plus one review-informed clarity repair**. It includes extra model calls and context. The dialogue alone, the repair and their computational cost are not separately identified.

The protocol was frozen before writer dispatch, but its claim of freezing before case delivery is not supported by the saved timing: the source-case file already existed before the protocol timestamp. This record therefore does not establish that the coordinator had no access to the case when freezing the protocol. The original protocol wording is retained with this qualification; see the [provenance addendum](provenance-addendum.json).

## Completed measurements

Exactly two completed scans were run in Pangram's **Free text detection** mode, displaying model **4.0**, after final quality review. The baseline was scanned first. The original and first-pass candidate were not scanned. No wording changed after scanning began.

| Text | Whitespace words | UI quote words | UI result words | Pangram result |
| --- | ---: | ---: | ---: | --- |
| [Original](outputs/original.txt) | 328 | — | — | Unscanned |
| [Current-skill baseline](outputs/baseline/final.txt) | 341 | 347 | 347 | AI Generated; 100% AI text |
| [First dialogue draft](outputs/candidate/final.txt) | 327 | — | — | Unscanned; baseline preferred for clarity |
| [Repaired dialogue candidate](outputs/candidate/repaired.txt) | 334 | 342 | 343 | AI Generated; 100% AI text |

The table reports the final admitted pair's UI quotes. An earlier quote for the unscanned first draft was retained privately but was not a detector result. The candidate's quote/result word-count difference is retained without attributing a cause. Both completed results displayed high segment confidence and no short-text warning. Undisplayed human or AI-assisted proportions remain `null`; they are not inferred to be zero. Pangram's displayed AI-text proportion is not GPTZero's AI confidence and does not establish authorship.

The frozen success condition required acceptable quality and either a decrease of at least five percentage points in comparable fully-AI text proportion or a better native label, with neither metric worsening. The observed change was **zero percentage points with the same label**, so the condition failed. Native receipt-derived values and exact input hashes are recorded in [results.json](results.json). No GPTZero scan was run in this trial.

## What this adds to the evidence

The dialogue surfaced a useful distinction between cancellation and attendance. The first candidate still lost the clarity comparison, and its repaired version only tied the baseline. Neither an overall readability advantage nor a detector reduction was demonstrated. The method is retained as an unsuccessful development trial, with no new default detector-oriented instruction promoted to the skill.

This is one new synthetic case, with one selected candidate and one allowed repair. It does not establish transfer to other topics, real user writing, other generators or other detectors. Held-out cases were not opened. The longer article format and absence of a short-text warning do not isolate an effect of length or explain the previous short-case results. No post-score variants were generated in this round.

## Reproducibility record

[export-manifest.json](export-manifest.json) identifies exact copies, sanitized records and the original text extracted from the common case. The frozen skill entrypoint is an exact text snapshot of the writer input, not an independently installable package; its linked references were not given to the writers and are not copied here. Writer claim maps, both masked review packets and their mappings, the saved dialogue, and process/admission audits retain the unsuccessful first pass as well as the scanned revision. Statements such as “not scanned” in writer records describe their pre-scan creation stage; the measurement table and results record describe the completed trial.

Account UI, screenshots, private browser evidence and account allowances are omitted. The study exports exact answer bodies and review records; retained private receipts check text/result correspondence but do not independently authenticate the service. Internal agent identifiers and local workspace paths are removed from the public-facing export. No public discussion answer was posted during this trial.
