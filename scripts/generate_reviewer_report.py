"""Gera os relatórios finais a partir das métricas salvas:

- reports/benchmark_summary.md
- reports/benchmark_results.tex
- reports/reviewer_response_evidence.md
- reports/limitations.md
- reports/reproducibility_checklist.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.benchmark.reporting import latex_table  # noqa: E402
from src.benchmark.schemas import read_jsonl  # noqa: E402

DISPLAY = {
    "pt_oie": "PT-OIE-EXTRACTOR (UD+attention)",
    "ud_baseline": "UD baseline (RQ1)",
    "ollama_gemma4": "Gemma 4 (Ollama, zero-shot)",
    "dptoie": "DptOIE",
    "multi2oie": "Multi\\textsuperscript{2}OIE",
    "portnoie": "PortNOIE",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def load_csv(path: Path) -> list[dict]:
    import csv

    if not path.exists():
        return []
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--benchmark-dir", default="outputs/benchmark")
    args = p.parse_args(argv)

    bdir = Path(args.benchmark_dir)
    reports = bdir / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    metrics = load_json(bdir / "metrics/metrics_by_system_protocol.json") or []
    ci = load_csv(bdir / "bootstrap/confidence_intervals.csv")
    diffs = load_csv(bdir / "bootstrap/paired_f1_differences.csv")
    runtime = load_csv(bdir / "runtime/runtime_metrics.csv")
    availability = load_json(bdir / "system_availability.json") or []
    manifest = load_json(bdir / "manifest.json") or {}
    gemma_manifest = load_json(bdir / "models/gemma4_latest_manifest.json") or {}

    by_sys: dict[str, dict] = {}
    for m in metrics:
        d = by_sys.setdefault(m["system"], {})
        d[f"{m['protocol']}_f1"] = float(m["f1"])
        d[f"{m['protocol']}_p"] = float(m["precision"])
        d[f"{m['protocol']}_r"] = float(m["recall"])
        if m["protocol"] == "bia_legacy":
            d["f1_ci_low"] = float(m["f1_ci_low"])
            d["f1_ci_high"] = float(m["f1_ci_high"])
    for r in runtime:
        if r["system"] in by_sys:
            by_sys[r["system"]]["median_seconds"] = float(r["median_seconds"])
            by_sys[r["system"]]["failure_rate"] = float(r["failure_rate"])

    rows = []
    for name, d in by_sys.items():
        rows.append({
            "display_name": DISPLAY.get(name, name),
            "bia_legacy_p": d.get("bia_legacy_p"),
            "bia_legacy_r": d.get("bia_legacy_r"),
            "bia_legacy_f1": d.get("bia_legacy_f1"),
            "f1_ci_low": d.get("f1_ci_low"),
            "f1_ci_high": d.get("f1_ci_high"),
            "strict_f1": d.get("strict_f1"),
            "tolerant_f1": d.get("tolerant_f1"),
            "carb_f1": d.get("carb_style_f1"),
            "median_seconds": d.get("median_seconds", 0.0),
            "failure_rate": d.get("failure_rate", 0.0),
            "supervised": "yes" if name in ("multi2oie", "portnoie") else "no",
        })
    rows.sort(key=lambda r: -(r["bia_legacy_f1"] or 0))
    unavailable = [a for a in availability if a["status"] == "unavailable"]
    EN_REASONS = {
        "portnoie": (
            "official code exists (FORMAS/dptoie-neural) with a trained model, but "
            "its official environment (Python$<$3.10, allennlp 2.7.0, unpinned git "
            "dependencies) is not deterministically reconstructible; building an "
            "approximate substitute is not allowed"
        ),
    }
    for u in unavailable:
        u = dict(u)
    unavailable = [
        {**u, "reason": EN_REASONS.get(u["system"], u["reason"])} for u in unavailable
    ]

    tex = latex_table(rows, unavailable, gemma_digest=gemma_manifest.get("digest"))
    (reports / "benchmark_results.tex").write_text(tex, encoding="utf-8")

    # ---- summary -------------------------------------------------------------
    lines = ["# Benchmark comparativo — resumo", ""]
    lines.append(f"Corpus: BIA — {manifest.get('corpus', {}).get('n_sentences', '?')} sentenças, "
                 f"{manifest.get('corpus', {}).get('n_gold_triples', '?')} triplas gold "
                 f"(sha256 `{str(manifest.get('corpus', {}).get('sha256'))[:12]}...`).")
    if gemma_manifest:
        lines.append(f"Gemma 4: `{gemma_manifest.get('name')}` digest `{gemma_manifest.get('digest')}`, "
                     f"quantização {((gemma_manifest.get('details') or {}).get('quantization_level'))}, "
                     f"Ollama {gemma_manifest.get('ollama_version')}.")
    lines += ["", "## Métricas (todos os protocolos)", "",
              "| Sistema | Protocolo | TP | FP | FN | P | R | F1 | IC95 F1 |",
              "|---|---|---|---|---|---|---|---|---|"]
    for m in metrics:
        lines.append(
            f"| {m['system']} | {m['protocol']} | {m['tp']} | {m['fp']} | {m['fn']} | "
            f"{100*float(m['precision']):.2f} | {100*float(m['recall']):.2f} | "
            f"{100*float(m['f1']):.2f} | [{100*float(m['f1_ci_low']):.2f}, "
            f"{100*float(m['f1_ci_high']):.2f}] |"
        )
    lines += ["", "## Diferenças pareadas de F1 (bootstrap por sentença)", "",
              "| A | B | Protocolo | ΔF1 (pontual) | ΔF1 médio | IC95 | P(Δ>0) |",
              "|---|---|---|---|---|---|---|"]
    for d in diffs:
        lines.append(
            f"| {d['system_a']} | {d['system_b']} | {d['protocol']} | "
            f"{100*float(d['delta_point']):.2f} | {100*float(d['delta_mean']):.2f} | "
            f"[{100*float(d['ci_low']):.2f}, {100*float(d['ci_high']):.2f}] | "
            f"{float(d['prop_delta_gt_0']):.4f} |"
        )
    if unavailable:
        lines += ["", "## Sistemas indisponíveis (sem métricas — indisponibilidade não é zero)", ""]
        for u in unavailable:
            lines.append(f"- **{u['system']}**: {u['reason']}")
    if runtime:
        lines += ["", "## Execução", "",
                  "| Sistema | Sentenças | Erros | Triplas | Mediana s/sent | p95 s/sent |",
                  "|---|---|---|---|---|---|"]
        for r in runtime:
            lines.append(f"| {r['system']} | {r['n_sentences']} | {r['n_sentences_error']} | "
                         f"{r['n_triples']} | {float(r['median_seconds']):.3f} | "
                         f"{float(r['p95_seconds']):.3f} |")
    (reports / "benchmark_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"relatórios gerados em {reports}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
