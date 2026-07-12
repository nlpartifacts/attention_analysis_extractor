# Reproducibility checklist

- [x] BIA corpus validated before execution: 262 sentences, 427 gold triples,
      SHA-256 `ddd882e93b3d7f9f5778f1a740e0f3854a193e00327082acc3d658bd6550b19e`
      (`corpus_validation.json`).
- [x] Same sentences, same order, for every system.
- [x] `gemma4:latest` digest recorded BEFORE the full run
      (`models/gemma4_latest_manifest.json` and `manifest.json`):
      `c6eb396dbd5992bbe3f5cdb947e8bbc0ee413d7c17e2beaae69f5d569cf982eb`,
      Ollama 0.20.0, Q4_K_M, 8.0B parameters, with `fail_on_digest_change: true`.
- [x] Fixed Gemma 4 prompt, SHA-256 in the manifest, zero-shot, no BIA
      examples, unchanged after the smoke test.
- [x] Fixed seeds: benchmark, bootstrap and Gemma use 42; the extractor uses
      13, as in the paper.
- [x] External system commits recorded (DptOIE `1a5ef708`,
      Multi2OIE `4a73a3c3`, dptoie-neural/PortNOIE `770f29fe`), plus SHA-256
      of binary artifacts (`patches/*.md`).
- [x] OS, Python, PyTorch, Transformers, Stanza, CUDA, CPU, GPU, and RAM
      versions in `environment.json` and `manifest.json`.
- [x] Raw outputs fully preserved (`raw/`), per-sentence errors (`errors/`),
      normalized predictions (`normalized/`).
- [x] Evaluation re-runnable from saved predictions
      (`scripts/evaluate_benchmark.py`) without re-extraction, with
      determinism covered by tests (`tests/test_determinism.py`).
- [x] Legacy protocol (`bia_legacy`) preserved unchanged and verified by
      bit-exact reproduction of the paper's counts
      (RQ3: TP=265/FP=273/FN=162, F1=54.92; RQ1: F1=52.71), see
      `tests/test_reproduction.py`.
- [x] Sentence-level paired bootstrap, 10,000 resamples, seed 42, 95%
      percentile CIs, with between-system differences on the same resamples.
- [x] Unavailability recorded with objective evidence, never scored as zero
      (`system_availability.json`).
- [x] 52 unit tests (`python -m pytest tests/ -q`).
- [x] Full reproduction commands in `BENCHMARK.md`.
