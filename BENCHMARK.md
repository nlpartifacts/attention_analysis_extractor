# Comparative OpenIE benchmark for Brazilian Portuguese (BIA corpus)

A scientifically controlled benchmark comparing Open Information Extraction
systems on **exactly the same 262 sentences and 427 gold triples** of the BIA
corpus (`data/bia_gold_sentences.jsonl`; SHA-256 recorded in the manifest).

## Systems

| System | Source | Execution |
|---|---|---|
| `pt_oie` | This repository, using the paper's best configuration (`rq3_attn_on_thr0`: UD + attention, ranked heads top-10, tau=0.0, validation off, seed 13) | local, GPU |
| `ud_baseline` | This repository, using the RQ1 configuration (pure UD, no attention, no validation) | local |
| `dptoie` | Official: FORMAS/DptOIE plus the authors' officially distributed models (see `patches/dptoie_artifacts.md`) | Java, batch |
| `multi2oie` | Official: youngbin-ro/Multi2OIE plus the official multilingual checkpoint, zero-shot (see `patches/multi2oie_artifacts.md`) | CPU, batch |
| `portnoie` | **Unavailable**: official code exists (FORMAS/dptoie-neural) but its execution environment is not reconstructible, and no substitute was built (see `outputs/benchmark/system_availability.json`) | not run |
| `ollama_gemma4` | `gemma4:latest` via the native Ollama API, zero-shot, fixed prompt (`configs/gemma4_prompt_pt.txt`), temperature 0, seed 42, verified model digest | local, GPU |

Unavailable systems receive **no** scores, since unavailability is not zero.

## Reproduction

```bash
# 0. Environment: Python 3.12 (see requirements.txt) + pytest
#    Ollama at http://localhost:11434 with gemma4:latest
#    Java 8+ for DptOIE

# 1. Validate the corpus (262 sentences / 427 triples / SHA-256)
python -m scripts.validate_corpus

# 2. Fetch the official external systems (network; idempotent)
python -m scripts.fetch_external_systems
# DptOIE: copy pt-dep-parser.gz and DptOIE.jar from the official "Models"
#   folder (authors' Drive) into .external/DptOIE/, see
#   patches/dptoie_artifacts.md (hashes)
# Multi2OIE: download the official multilingual checkpoint to
#   .external/Multi2OIE/multilingual_model.bin, see patches/multi2oie_artifacts.md

# 3. Record the gemma4:latest digest (required before the full run)
python -m scripts.inspect_ollama --model gemma4:latest \
  --output outputs/benchmark/models/gemma4_latest_manifest.json

# 4. Unit tests
python -m pytest tests/ -q

# 5. Smoke test (format and technical errors only; 5 sentences)
python -m scripts.smoke_test_benchmark --systems pt_oie ud_baseline ollama_gemma4 --limit 5

# 6. Full benchmark (extraction writes raw/, normalized/, errors/)
python -m scripts.run_benchmark \
  --config configs/benchmark.yaml \
  --systems pt_oie ud_baseline dptoie multi2oie portnoie ollama_gemma4 \
  --output-dir outputs/benchmark \
  --seed 42

# 7. Evaluation (re-runnable from the saved predictions, no re-extraction)
python -m scripts.evaluate_benchmark \
  --predictions-dir outputs/benchmark/normalized \
  --gold data/bia_gold_sentences.jsonl \
  --output-dir outputs/benchmark \
  --bootstrap-samples 10000 \
  --seed 42

# 8. Reports (summary, LaTeX table)
python -m scripts.generate_reviewer_report
```

Useful `run_benchmark` options: `--systems`, `--limit`, `--resume`, `--force`,
`--fail-fast`, `--timeout`, `--dry-run`.

## Evaluation protocols

All systems are evaluated under the same four protocols, and only gold triples
with `valid=true` count. Under the standardized protocols (strict, tolerant,
carb_style), exact deduplication (lowercase plus whitespace collapse) is
applied to every system's predictions before matching. `bia_legacy` applies
**no** deduplication, preserving the exact historical behavior of the paper's
evaluator, which was verified by bit-exact reproduction of the published
counts (RQ3: TP=265, FP=273, FN=162, F1=54.92; RQ1: F1=52.71).

1. **strict**: exact equality of all three slots after lowercasing and
   whitespace collapse, with deterministic one-to-one assignment.
2. **tolerant**: per-slot token F1 (tokenization: lowercase, punctuation
   removed, accents preserved); a pair is eligible when the **minimum** slot
   F1 is at least 0.70, with one-to-one assignment by mean slot F1.
3. **carb_style**: weighted score 0.35*F1(arg1) + 0.30*F1(rel) + 0.35*F1(arg2)
   of at least 0.60, with one-to-one assignment by score.
4. **bia_legacy**: the project's legacy scorer (called *Official* in the
   submitted paper), preserved **unchanged** via
   `src.extractor.evaluate_dataset_legacy`. Normalization: lowercasing,
   contraction expansion, punctuation removal, removal of leading determiners
   from arguments. Argument matching: equality, suffix, prefix (at least one
   token), or word-subset; relation matching: equality or partial prefix
   (skipping a leading light verb in the gold). Greedy scan in gold order,
   one-to-one by construction. Scores obtained under this protocol are not
   externally comparable.

Under the standardized protocols (1 to 3), assignment sorts candidate pairs by
(-score, gold index, prediction index), which is deterministic with stable
tie-breaking.

## Statistics

- **Sentence-level paired bootstrap** (resampling unit = sentence),
  10,000 resamples, seed 42, 95% percentile intervals.
- F1 differences between systems use the **same** resamples (pairing), with
  mean delta F1, median, 95% CI, and P(delta > 0).
- No significance claim is made from point estimates alone.

## Scientific controls

- Corpus and gold untouched; same sentences, same order, for every system.
- The Gemma 4 prompt was fixed before any result was observed (SHA-256 in the
  manifest), zero-shot, no BIA examples, temperature 0, seed 42, at most one
  repair per sentence, restricted to format conversion of the original answer.
- The `gemma4:latest` digest is resolved before execution and enforced
  (`fail_on_digest_change: true`), so results from different digests never mix.
- Per-sentence failures are recorded (`errors/`) and counted, never silently
  converted into empty lists; an empty list only counts when explicitly
  returned by the system.
- External systems: official implementations and artifacts only, with commits
  and hashes recorded, and no rules or weights modified (see `patches/`).
- Full raw outputs preserved under `outputs/benchmark/raw/`.

### Technical adjustments recorded during the smoke test

Two **format and capacity** adjustments were made after the 5-sentence smoke
test, before the full run, without touching the prompt and without consulting
the gold:

1. The `gemma4` template in Ollama 0.20 returns the JSON wrapped in a markdown
   fence even when `format` (JSON Schema) is set; the parser strips the fence
   syntactically (inner content untouched, raw response preserved).
2. `num_predict` was raised from 384 to 1024, because long BIA sentences
   truncated the response (`done_reason=length`), invalidating the JSON.

## Outputs

See the full tree under `outputs/benchmark/`: manifest (`manifest.json` with
corpus SHA-256, commits, model digest, seeds, versions, environment),
availability (`system_availability.json`), predictions (`raw/`, `normalized/`,
`errors/`), per-protocol matching (`matches/`), metrics (`metrics/`),
bootstrap (`bootstrap/`), runtime (`runtime/`), and reports (`reports/`,
including `benchmark_results.tex`).
