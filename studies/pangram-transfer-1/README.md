# Checking existing answers with Pangram 4

**One of three pairs changed classification: the PostgreSQL rewrite moved from entirely AI-generated to entirely AI-assisted.** The other two pairs stayed entirely AI-generated. None of the six texts was classified as human-written.

On September 6, 2026, we checked six saved texts in the free Pangram web interface. Every completed result explicitly displayed **Pangram 4.0**. The cases and order were frozen before seeing Pangram results. These are existing development cases; no new writing or skill revision was tested.

## Results

The Pangram columns describe the displayed classification and proportion of text. The GPTZero column gives historical document confidence from Basic Scan, Model 4.9b, earlier that day. These are different metrics and were not measured concurrently.

| Pair | Pangram before | Pangram after | Earlier GPTZero AI confidence |
| --- | --- | --- | --- |
| Kubernetes probes, direct rewrite | 100% AI-generated | 100% AI-generated | 100% → 100% |
| PostgreSQL snapshots, direct rewrite | 100% AI-generated | 100% AI-assisted | 100% → 100% |
| Qwen command permissions, existing quotation added | 100% AI-generated | 100% AI-generated | 100% → 1% |

The Qwen GPTZero result was 1% AI / 99% mixed / 0% human. Its quotation changed the context and length of an unchanged answer body; that historical effect did not carry over to this Pangram check. The two direct rewrites had passed separate LLM quality review and were preferred to their originals. These are not human reader ratings.

Pangram flagged the Kubernetes original and both Qwen texts as short, with limited confidence. Their result word counts were 194, 145 and 168 respectively. The other three results had no short-text warning. Texts were not padded or shortened for either service.

## Evidence and interpretation

The [complete records](results.json) link all six existing inputs, their hashes, rendered result text, prior GPTZero observations, displayed classifications and separate confidence labels. A missing category percentage is recorded as unavailable, not as an observed zero. A [separate audit](review.json) checked all six text records and twelve result screenshots.

Before every scan, the textarea matched the saved historical GPTZero effective input byte-for-byte. Pangram's result display removed blank lines and stripped line-edge spaces, tabs and carriage returns. We retained that display separately and verified the exact transformation, unchanged token sequence, SQL statement and parsed JSON values. This observation does not identify the model's internal preprocessing. Raw screenshots and account UI remain private.

All six scans completed once, using 12 free credits and no paid services. Some preview word counts differed from result counts, and preview credit estimates totaled 15 while the observed deduction was 12; the individual records retain both estimates and actual usage.

This small selected comparison shows why it is useful to check another detector. It supports one observed category change, not general detector avoidance: Pangram still detected AI involvement in every output. The strongest historical quotation result was deliberately selected, so these three pairs cannot estimate a general success rate. GPTZero publication requirements remain unchanged.
