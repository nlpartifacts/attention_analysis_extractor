# PT OIE EXTRACTOR experimental artifact

This repository contains the experimental code associated with the PT OIE EXTRACTOR paper. The code is organized to preserve the original experimental behavior while exposing clearer module boundaries.

## Structure

```text
src/
  extractor.py
  attention.py
  theory_rules.py
  evaluation.py
  run_experiment.py
notebooks/
  openie_pt_experiment_final.ipynb
data/
  README.md
```

## Main modules

- `src/extractor.py`: main extractor, UD parsing, candidate generation, attention attachment, theoretical validation, and experimental helpers.
- `src/attention.py`: attention utilities and head ranking helpers.
- `src/theory_rules.py`: rule related dataclasses and summary helpers.
- `src/evaluation.py`: matching, metrics, tables, and file writing helpers.
- `src/run_experiment.py`: CLI and callable experiment runner.

## Running from the command line

```bash
python -m src.run_experiment \
  --gold data/bia_gold_sentences.jsonl \
  --bosque data/pt_bosque-ud-train.conllu \
  --output-dir outputs/rq3_attn_on_thr0 \
  --dataset-name bia \
  --heads-mode rank \
  --top-k-heads 10 \
  --attn-threshold 0.0 \
  --theory-mode off
```

## Notes

The best reported configuration in the paper uses UD based extraction with BERTimbau attention based candidate selection and theoretical validation disabled. The theoretical validation layer remains available for ablation studies.
