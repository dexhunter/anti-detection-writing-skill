# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["torch==2.8.0", "transformers==4.57.6", "safetensors==0.8.0", "sentencepiece==0.2.1"]
# ///
"""Independent publisher-class replay on CPU; never imports the measured adapter."""
import hashlib
import json
from pathlib import Path
import time

import torch
from transformers import AutoTokenizer, AutoConfig, AutoModel, PreTrainedModel


class DesklibAIDetectionModel(PreTrainedModel):
    config_class = AutoConfig

    def __init__(self, config):
        super().__init__(config)
        self.model = AutoModel.from_config(config)
        self.classifier = torch.nn.Linear(config.hidden_size, 1)
        self.init_weights()

    def forward(self, input_ids=None, attention_mask=None, **kwargs):
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden = outputs[0]
        mask_expanded = attention_mask.unsqueeze(-1).expand(last_hidden.size()).float()
        sum_embeddings = torch.sum(last_hidden * mask_expanded, dim=1)
        sum_mask = torch.clamp(mask_expanded.sum(dim=1), min=1e-9)
        pooled = (sum_embeddings / sum_mask).to(self.classifier.weight.dtype)
        return {"logits": self.classifier(pooled)}


root = Path(__file__).resolve().parent
started = time.monotonic()
reference = json.loads((root / "results.json").read_bytes())["records"][0]
raw = (root.parent / reference["path"]).read_bytes()
assert hashlib.sha256(raw).hexdigest() == reference["input_sha256"]
tokenizer = AutoTokenizer.from_pretrained(root / "model", local_files_only=True)
ids = tokenizer(raw.decode("utf-8"), truncation=False)["input_ids"]
assert len(ids) <= 512
ids_sha = hashlib.sha256(json.dumps(ids, separators=(",", ":")).encode()).hexdigest()
assert ids_sha == reference["token_ids_sha256"]
model, loading = DesklibAIDetectionModel.from_pretrained(
    root / "model", local_files_only=True, output_loading_info=True)
assert not loading["missing_keys"] and not loading["unexpected_keys"]
assert not loading["mismatched_keys"] and not loading["error_msgs"]
model.eval()
inputs = tokenizer(raw.decode("utf-8"), return_tensors="pt", truncation=False,
                   max_length=512, padding="max_length")
with torch.no_grad():
    logit = model(**inputs)["logits"].squeeze(-1)
    probability = torch.sigmoid(logit).item()
delta = abs(probability - reference["ai_probability"])
report = {"status": "pass" if delta <= 0.0001 else "fail", "input_sha256": reference["input_sha256"],
          "token_ids_sha256": ids_sha, "full_token_count": len(ids), "publisher_device": "cpu",
          "batch_device": "mps", "dtype": "float32", "reference_logit": logit.item(),
          "reference_probability": probability, "batch_logit": reference["raw_logit"],
          "batch_probability": reference["ai_probability"], "absolute_probability_difference": delta,
          "tolerance_frozen_before_reference_run": 0.0001, "loading_info": loading,
          "source": "Pinned Oculus README publisher class, local path substituted and input length checked before full padding",
          "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          "elapsed_seconds": time.monotonic() - started}
with (root / "publisher-parity.json").open("x") as stream:
    json.dump(report, stream, indent=2)
    stream.write("\n")
print(json.dumps(report))
assert report["status"] == "pass"
