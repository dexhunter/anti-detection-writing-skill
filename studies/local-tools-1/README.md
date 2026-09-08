# Local tools and released-model research

September 7, 2026. This work adds an exercised local detector CLI and tests a released paraphraser. Local detector output is a separate measurement from GPTZero or Pangram. No commercial scan or publication occurred in this study.

## A working scorer, with a weak proxy for these cases

The [local detector CLI](../../skills/anti-detection-writing/references/local-detector.md) loads a fixed Desklib model from a verified local snapshot. It checks exact file hashes, scores complete inputs serially, rejects more than 768 tokens rather than truncating, and records raw logits, sigmoid probabilities, runtime and failures. Model weights are downloaded separately and are not included in this repository.

Before reading local scores, we selected eight existing, quality-passing development texts: three technical versions, three business versions and the last article pair. Every text was AI-origin. They are reused development examples, not unseen evaluation data or a representative accuracy benchmark. The [selection plan](detector/plan.json), [exact inputs](detector/manifest.json) and [full results](detector/results.json) are retained.

| Text | Tokens including special tokens | Desklib AI probability (0–1) | Prior Pangram AI text |
| --- | ---: | ---: | --- |
| Library baseline | 402 | 0.014980 | 100% |
| Library revised | 411 | 0.012341 | 100% |
| Technical baseline | 150 | 0.066911 | 100% |
| Technical preserved original | 153 | 0.186104 | 100% |
| Technical core expansion | 147 | 0.051038 | 100% |
| Business baseline | 150 | 0.057683 | 100% |
| Business preserved original | 151 | 0.062286 | 100% |
| Business core expansion | 147 | 0.087645 | Unmeasured |

Values are rounded only in this table. The JSON preserves native precision. The commercial column refers to the earlier [writing-methods study and follow-up](../writing-methods-1/README.md) and [reader-dialogue study](../reader-dialogue-1/README.md), not new scans. Pangram text proportions and Desklib sigmoid probabilities have different meanings; they are not interchangeable percentages. At the Desklib model card's 0.5 threshold, all eight texts fall in its non-AI class, disagreeing with the seven available Pangram classifications. No human controls were included, so this cannot estimate general accuracy or false-positive rates.

A separate reviewer reproduced the publisher's inference algorithm without importing the CLI backend. On the library baseline, the reference and CLI produced the exact same logit, −4.18595552444458, with matching token IDs and attention masks. The publisher's AI-labelled example returned 0.997424, confirming variable output and the documented orientation; its authorship was not independently verified. [Parity record](detector/model-card-parity.json).

The scorer works on these complete texts, but this model has not demonstrated useful ranking for our commercial endpoint. We retain it for diagnostics. Small decreases in its probability are not evidence that a revision will improve on GPTZero or Pangram.

The [measured scorer snapshot](detector/scorer-at-measurement.py) preserves the batch's exact script hash for inspection. It is an archive, not a separately packaged installation. The final CLI additionally reports tokenizer and Hub library versions; a [final-version smoke test](detector/final-smoke-results.json) reproduced the same baseline logit. There were eight diagnostic forward calls, two independent reference calls, and one final smoke call, all local.

## AuthorMist: both complete outputs failed quality review

We then exercised the pinned [Originality-focused AuthorMist weights](https://huggingface.co/authormist/authormist-originality/tree/2866bc928850ef4910d24ef5a9179740fab72e22) on the two existing technical and business originals. The [plan](authormist/plan.json) fixed one completion per source before generation, with no repairs, seed retries, reranking or detector feedback. It used the card's plain-completion prompt, explicitly recorded its sampling settings, and loaded the model on Apple MPS in bfloat16. Complete prompts fit the model context and both outputs ended on an EOS token. This is a card-use feasibility test, not a base-versus-trained-model comparison or reproduction of the paper's eight-candidate selection.

| Case | Source words | Output words | Independent result | Candidate detector score |
| --- | ---: | ---: | --- | --- |
| HTTP caching explanation | 123 | 242 | Failed; source preferred | Unmeasured |
| Migration update | 129 | 281 | Failed; source preferred | Unmeasured |

The technical output omitted `If-None-Match`, changed `Cache-Control: max-age=60` into invalid header syntax, dropped an operational qualification and confused permitted fresh reuse with unchanged origin data. The business output changed whether staff could be supplied into whether people could be managed, and changed deciding whether to schedule rollout into deciding when to roll out. Both added repeated drafts and unrelated editing commentary. These were substantive failures beyond changes to protected date formatting.

The separate reviewer saw exact source contracts and masked text pairs without model labels or detector results. Both source texts passed; both generated outputs failed factual fidelity and readability. All four text hashes were verified. The [full review](authormist/reviews/quality.json), [unmodified outputs](authormist/outputs/wm4-dev-technical-01.txt), [generation record](authormist/run.json) and [final outcome](authormist/outcome.json) retain the complete result. Fields marked pending in the generation record describe that earlier stage; the outcome records the final rejection. Neither candidate was sent to any detector.

This two-case result does not establish that every AuthorMist configuration fails, nor that the training caused these defects. It does show that the released card workflow did not produce usable revisions here. No trained paraphraser was adopted into the skill.

## What the literature changed

The released [StealthRL implementation](https://github.com/suraj-ranganath/StealthRL/tree/6a981cd3a92a57e7558699b5b5694cb4eeba5e04) offers a trained paraphraser, but its [revised paper](https://arxiv.org/html/2602.08934v2) reports poor judged quality and similarity alongside detector reductions. Its single-output code path can also store zero as an unmeasured detector score. That supports retaining null scores and rejecting factual failures, rather than adopting its reported reduction as a writing benefit.

[AuthorMist](https://arxiv.org/html/2503.08716v1) releases a smaller learned paraphraser. Its reported evaluation includes candidate selection, so a single-completion test is a narrower feasibility check. The released card's MIT label must be read alongside the [base model's research license](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/main/LICENSE). Our test is private research; the weights are not distributed with this skill.

[Adversarial Paraphrasing](https://github.com/chengez/Adversarial-Paraphrasing/tree/d8515ab705e10b08a1a04214767114522c454bd7) implements detector feedback during token generation. Its default generator and repeated classifier calls make it a larger porting task. Silent detector truncation in that code is particularly relevant: an apparent improvement on a prefix is not a measured improvement on the full answer. We did not reproduce its search algorithm.

The resulting tool preserves full input coverage and native, separately labelled measurements. No detector-oriented default writing rule is promoted from these papers or from the local diagnostic.
