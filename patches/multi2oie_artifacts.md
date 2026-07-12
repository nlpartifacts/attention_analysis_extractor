# Multi2OIE — official artifacts used (no code changes)

- System: Multi2OIE (Ro, Lee & Kang, EMNLP 2020)
- Official repository: youngbin-ro/Multi2OIE, commit `4a73a3c37412` (shallow clone in `.external/Multi2OIE`)
- Checkpoint: the official multilingual model distributed by the authors on
  the Google Drive linked from the official README (`multilingual_model.bin`,
  980,501,266 bytes, dated 2021), stored at
  `.external/Multi2OIE/multilingual_model.bin`.
- Execution mode: multilingual zero-shot, as in the original paper (mBERT
  trained only on English OpenIE4 data and tested on Portuguese without
  adaptation). **No training or tuning with BIA.**
- Code modification: **none.** The benchmark adapter invokes
  `dataset.load_data(train=False)` and `extract.extract` from the repository
  itself.
- Compatibility note: the official requirements.txt pins torch 1.4.0 and
  transformers 2.10.0 (Python 3.7). Execution used torch 2.5.1 and
  transformers 4.48.2; `load_state_dict` reports **0 missing and 0 unexpected
  keys**, and the only transformers API used by the model
  (`BertModel(...)[0]`) is stable across these versions. The stack difference
  is recorded in the manifest.
- Mapping to the benchmark's binary schema: the official output is n-ary
  `[pred, arg0, arg1, ...]`; arg1 = arg0, rel = pred, arg2 = concatenation of
  the remaining arguments. The full raw line is preserved in `raw_output`.
- License: MIT (repository LICENSE file).
