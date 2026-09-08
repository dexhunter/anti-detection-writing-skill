# Local development detector

Use `scripts/local_detector.py` for requested detector research on explicitly supplied development texts. It runs the open `desklib/ai-text-detector-v1.01` model at the revision recorded in [local-detector-model.json](local-detector-model.json). Model files must already exist locally and match every pinned hash. The scorer downloads no model, executes no remote model code, and calls no hosted inference service.

The output is a **local proxy**: a raw logit and its sigmoid in the range 0–1, with higher values indicating the model's AI class. It is uncalibrated for our writing cases. It is neither a GPTZero/Pangram result nor evidence of human authorship. Keep commercial tests, factual review and any posting conditions separate. This script does not modify or promote the skill.

## Run

Download and verify the fixed public model once, outside the skill repository. This downloads approximately 1.75 GB; the weights are not bundled with the skill. The scorer needs the snapshot directory printed by the first command.

```sh
hf download desklib/ai-text-detector-v1.01 --revision 5fdea974cd4287c61674951ec78803aa274e2fb7
hf cache verify desklib/ai-text-detector-v1.01 --revision 5fdea974cd4287c61674951ec78803aa274e2fb7 --fail-on-missing-files --fail-on-extra-files
```

Create a JSON manifest whose paths are relative to that manifest, with the SHA-256 of each exact UTF-8 file:

```json
{
  "schema_version": 1,
  "records": [
    {"id": "baseline", "path": "baseline.txt", "sha256": "REPLACE_WITH_EXACT_SHA256"},
    {"id": "candidate", "path": "candidate.txt", "sha256": "REPLACE_WITH_EXACT_SHA256"}
  ]
}
```

```sh
uv run scripts/local_detector.py --model-dir /path/to/verified-snapshot --manifest /path/to/inputs.json --output /path/to/new-results.json
```

The script declares pinned Python dependencies; `uv` may install those dependencies on first use. Model inference itself uses local files only. The default is CPU float32. Use `--device mps` explicitly to test an available Apple accelerator; report that device, and do not assume cross-device numerical identity. Each forward pass contains one document. An existing output is never overwritten.

The implementation follows the [pinned model card](https://huggingface.co/desklib/ai-text-detector-v1.01/blob/5fdea974cd4287c61674951ec78803aa274e2fb7/README.md): attention-mask-weighted mean pooling, one linear output, and sigmoid. It retains fixed padding to 768 tokens. Unlike the card's example, it **rejects texts longer than 768 tokens including special tokens**, instead of truncating them. Do not shorten an answer merely to obtain a measurable score or present partial-text results as a complete article measurement.

The report preserves every supplied record, input and token hashes, full token count, model file hashes, device/dtype, library versions and native scores. A failed record has null scores and a specific error. Exit codes are 0 for all records completed, 1 for a report containing failures, and 2 for invalid setup such as a malformed manifest or changed model files. Setup failures produce no report.

## Use the result

Start with fixed, previously seen development cases to check whether the detector yields useful variation in the intended domain. Give candidates the same source contract and keep independent quality review separate from scores. Preserve all generated candidates and all local outcomes, including ties, failures and worse scores. Never scan hidden confirmation files by recursively reading a study directory.

The September 7 diagnostic on eight preselected, quality-passing AI-origin development texts returned AI probabilities from 0.0123 to 0.1861; all were below the model card's 0.5 classification threshold. Seven had prior Pangram results of 100% AI text; the eighth had not been scanned there. These are different native units, but the class decisions disagree on those seven texts. There were no human controls, so this does not estimate general accuracy or false-positive rates.

This adapter is therefore a diagnostic tool, not a validated way to rank revisions for GPTZero or Pangram. A low number alone is insufficient reason to spend commercial scan allowance on a candidate. Establish useful ranking on separate comparable cases before using it for selection; keep every development result and reserve untouched confirmation. Any future GPTZero/Pangram improvement claim still needs exact, fresh paired measurements in the relevant service and native units.

An independent reproduction of the publisher's inference algorithm matched the library baseline's raw logit and tokenization exactly. Its supplied AI-labelled example scored 0.997424. Those checks support implementation correspondence, not general accuracy or the authorship of the publisher's example.
