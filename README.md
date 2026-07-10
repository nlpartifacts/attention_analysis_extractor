# PT-OIE-EXTRACTOR: UD + Attention for Brazilian Portuguese OpenIE

This repository contains the experimental artifact for **PT-OIE-EXTRACTOR**, a training-free hybrid Open Information Extraction system for Brazilian Portuguese. The pipeline:

1. generates candidate triples from Universal Dependencies patterns;
2. scores eligible candidates with preselected BERTimbau attention heads; and
3. optionally applies structural and syntactic-semantic validation rules.

The repository supports individual experiments and the complete 26-configuration ablation study reported in the paper.

## Repository structure

```text
attention_analysis_extractor/
├── README.md
├── notebooks/
│   ├── openie_pt_experiment_final.ipynb
│   ├── bia_gold_sentences.jsonl
│   └── pt_bosque-ud-train.conllu
└── src/
    ├── __init__.py
    ├── extractor.py
    ├── attention.py
    ├── theory_rules.py
    ├── evaluation.py
    ├── run_experiment.py
    └── run_all_ablations.py
```

`run_all_ablations.py` also detects the two input files under `data/` if the repository is later reorganized to keep corpora outside `notebooks/`.

## Data

- `bia_gold_sentences.jsonl`: BIA evaluation corpus, containing 262 Brazilian Portuguese sentences and 427 reference triples.
- `pt_bosque-ud-train.conllu`: Portuguese UD Bosque file used to rank attention heads for subject and object evidence.

The BIA file is used for evaluation. The Bosque file is used for attention-head selection and is not an additional OpenIE test set.

## Environment

The experiments reported in the paper used:

- Ubuntu 24.04 LTS;
- Python 3.12;
- Stanza 1.10.1;
- Transformers 4.46.3;
- PyTorch 2.5.1;
- pandas 2.2.3;
- conllu 6.0.0; and
- `neuralmind/bert-base-portuguese-cased`.

Create an isolated environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Install the Python dependencies:

```bash
pip install \
  stanza==1.10.1 \
  transformers==4.46.3 \
  torch==2.5.1 \
  pandas==2.2.3 \
  conllu==6.0.0 \
  numpy \
  tqdm \
  openpyxl
```

For GPU execution, install the PyTorch build appropriate for the local CUDA environment before installing the remaining packages.

Download the Portuguese Stanza model once:

```bash
python -c "import stanza; stanza.download('pt')"
```

The first attention-enabled execution also downloads the BERTimbau checkpoint from Hugging Face unless it is already cached.

## Run one experiment

From the repository root:

```bash
python -m src.run_experiment \
  --gold notebooks/bia_gold_sentences.jsonl \
  --bosque notebooks/pt_bosque-ud-train.conllu \
  --output-dir outputs/rq3_attn_on_thr0 \
  --dataset-name bia \
  --heads-mode rank \
  --top-k-heads 10 \
  --attn-threshold 0.0 \
  --theory-mode off
```

This command executes the attention-enabled configuration with threshold `0.00` and linguistic validation disabled.

## Run the complete ablation study

Place `run_all_ablations.py` under `src/`, then execute:

```bash
python -m src.run_all_ablations \
  --gold notebooks/bia_gold_sentences.jsonl \
  --bosque notebooks/pt_bosque-ud-train.conllu \
  --output-dir outputs/ablation_experiments
```

When `--gold` and `--bosque` are omitted, the script searches for the files in this order:

1. `data/`;
2. `notebooks/`; and
3. the repository root.

List the 26 configurations without executing them:

```bash
python -m src.run_all_ablations --list
```

Run only selected groups using shell-style patterns:

```bash
python -m src.run_all_ablations \
  --only 'rq3_*' \
  --only 'rq8_*'
```

Ignore cached metrics and recompute the selected configurations:

```bash
python -m src.run_all_ablations --force
```

Stop after the first failed configuration:

```bash
python -m src.run_all_ablations --fail-fast
```

## Ablation design

| Group | Purpose | Configurations |
|---|---|---:|
| RQ1 | Pure UD baseline, without attention or validation | 1 |
| RQ2 | Copular extraction: `full`, `restricted`, and `off` | 3 |
| RQ3 | Attention enabled with thresholds `0.00` and `0.15` | 2 |
| RQ4 | All structural and semantic/discourse rules enabled | 1 |
| RQ5 | Structural rules only versus semantic/discourse rules only | 2 |
| RQ6 | Leave-one-out ablation of S1–S5 | 5 |
| RQ6b | Leave-one-out ablation of E1–E9, including E4 subflags | 11 |
| RQ8 | Attention plus validation, excluding E4 | 1 |
| **Total** |  | **26** |

The labels in the script are identical to those used in the notebook and paper, including `rq6b` and `rq8`.

## Output files

Each configuration is stored in an isolated directory:

```text
outputs/ablation_experiments/
├── ablation_manifest.json
├── ablation_results.csv
├── ablation_results.json
├── ablation_results.xlsx
├── abl_rq1_baseline_ud_puro/
│   └── bia_abl_rq1_baseline_ud_puro_*.{json,csv,jsonl}
├── abl_rq3_attn_on_thr0/
│   └── bia_abl_rq3_attn_on_thr0_*.{json,csv,jsonl}
└── ...
```

The consolidated files contain TP, FP, FN, precision, recall, F1, the difference from the RQ1 baseline, execution status, cache source, metrics path, and the complete serialized configuration.

`ablation_manifest.json` records the input paths, model, seed, and configuration of every selected run before execution.

## Cache behavior

For each configuration, the script looks for:

```text
<output-dir>/abl_<label>/bia_abl_<label>_metrics.json
```

When the file exists, the metrics are loaded from disk and the extraction pipeline is not executed again. Use `--force` after changing the code, model, corpus, parser, matching protocol, or configuration.

## Reproducibility checks

Before reporting results:

1. confirm that all 26 rows have status `ok` or `cached`;
2. verify that the same corpus and Bosque files were used for every run;
3. preserve `ablation_manifest.json` with the result tables;
4. report the matching protocol together with P, R, and F1; and
5. do not compare scores produced by different matching implementations as if they were directly equivalent.

The paper reports the strongest configuration as UD extraction with attention enabled at threshold `0.00` and linguistic validation disabled. The exact reproduction target depends on using the same repository revision, model checkpoint, parser resources, corpus, and matching implementation.

## Notebook

`notebooks/openie_pt_experiment_final.ipynb` contains the original interactive analysis, including derived tables, error analysis, protocol comparisons, and attention diagnostics. The command-line ablation script reproduces the systematic RQ1–RQ8 execution and consolidation; the notebook remains the reference for exploratory and post-hoc analyses.

## Citation

When using this artifact, cite the associated PT-OIE-EXTRACTOR paper and the original resources used by the experiment, including BERTimbau, Universal Dependencies Bosque, and the BIA corpus.
