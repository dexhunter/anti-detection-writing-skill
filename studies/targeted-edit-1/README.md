# Targeted editing comparison

On September 6, 2026, two new synthetic technical answers were edited by diagnosing specific clarity problems and changing the affected passages. A separate reviewer modestly preferred both revisions. Neither detector improved on either pair.

| Case | GPTZero AI confidence, original → revision | Pangram original → revision | Separate quality review |
| --- | --- | --- | --- |
| GitHub Actions concurrency | 100% → 100% | 100% AI-generated → 100% AI-generated | Revision modestly preferred |
| Python TaskGroup | 100% → 100% | 100% AI-generated → 100% AI-generated | Revision modestly preferred |

All four GPTZero results were **100% AI / 0% mixed / 0% human**, using completed Basic Scan results displaying Model 4.9b. All four Pangram results displayed **Pangram 4.0**, AI Generated, 100% of text AI, and medium confidence with a short-text warning. Pangram's text percentages are not GPTZero's document confidences. Undisplayed Pangram categories are recorded as null, not measured zero.

## What was tested

The [design](design.json) was saved before fixture creation and scores. A separate source agent constructed two correct originals with specific clarity problems from official documentation. A fresh writer received the [frozen skill](frozen-skill/SKILL.txt), questions, originals and source evidence. The added instruction was to diagnose reader-facing problems first, then revise affected passages while preserving clear prose. Diagnoses were saved before revisions. There was one revision per original, no repairs and no edits after scores.

The GitHub revision moved the repository/group condition and compatible cancellation setting beside their governing claims, and named the queued runs explicitly. The Python revision moved the version prerequisite and cancellation exception beside the relevant behavior, and named when the exception group is raised. Length changed from 147 to 144 words and from 134 to 137 words respectively; no padding was added.

The [separate review](quality-review.json) checked the exact original and revised hashes against live official sources before scans, without reading detector material or the writer's reports. All 17 claims, protected identifiers and necessary qualifications survived. Both originals also passed technically. Preference is a separate LLM judgment, not human preference or measured usefulness.

The four inputs were frozen and scanned on each service in the same saved order: GitHub original, Python revision, Python original, GitHub revision. Eight scans completed without retries. Pangram used 8 existing free credits; GPTZero used 562 words. No credits were purchased.

## Exact inputs and evidence

[Results](results.json) include every observation, native metrics, model/mode, warnings, input hashes and recorded representations. The `inputs` folder preserves source Markdown, including backticks. Pangram received those exact bytes; its result display trimmed line edges and removed blank lines, with the exact transformation checked against all four saved rendered texts. This describes the display, not internal detector preprocessing. GPTZero's literal Code Block input removed one source-terminal newline; its effective editor text added exactly three newline characters. All four completed results matched that effective text and showed Text up-to-date. These separately documented wrappers are not represented as strict receipts from the packaged receipt validator.

Pangram preview/result word counts were 155/155, 145/148, 142/145 and 152/152 in scan order. Its four short-text warnings remain part of the outcome; the answers were not extended to remove them. GPTZero displayed no short-text warning for these inputs.

Raw DOM records, screenshots and account document URLs remain private. The public records are maintainer-recorded UI observations; hashes establish file integrity, not independently authenticated scores. The frozen entrypoint uses `SKILL.txt` to avoid creating a second installable skill. Its complete file manifest is [saved here](frozen-skill-files.json).

## What this changes

This is a two-case development comparison using deliberately constructed editing fixtures. It is not a naturally occurring discussion sample or an unseen validation dataset. With no current-skill-only editing arm, it cannot show that the added diagnosis instruction outperforms the existing skill or identify which instruction caused the quality preference. Detector repeatability and human preference were not measured.

The result supports a modest clarity preference in these two examples, with **zero detector improvements**. The production rewriting instructions were not changed on this evidence. The failed score-reduction result was added to the skill's evidence notes, and no example from this batch enters the success showcase.
