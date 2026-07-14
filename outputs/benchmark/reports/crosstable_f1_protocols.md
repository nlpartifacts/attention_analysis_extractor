# Full cross-table: F1 of all systems under the four matching protocols

Same 262 BIA sentences and 427 gold triples for every system. Bold marks the
best system per protocol. Scores are not comparable across protocols.
Data source: `../metrics/metrics_by_system_protocol.csv`.

| System | Strict | Tolerant | BIA legacy | CaRB style |
|---|---:|---:|---:|---:|
| PT-OIE-EXTRACTOR (UD + attention) | 18.37 | 29.14 | **54.92** | **61.67** |
| Pure UD baseline (RQ1) | 17.48 | **30.78** | 52.71 | 59.19 |
| Gemma 4 (zero-shot LLM, 8B) | **22.34** | 28.87 | 43.30 | 47.94 |
| Multi2OIE (official, zero-shot) | 0.91 | 15.47 | 34.39 | 49.32 |
| DptOIE (official) | 4.24 | 7.35 | 12.82 | 15.75 |

PortNOIE is not scored: its official execution environment is not
reconstructible, and unavailability is not zero
(see `../../system_availability.json`).

## Greedy vs. optimal assignment under the BIA legacy matcher

The legacy matcher scans greedily in gold order. Replacing the greedy scan
with maximum bipartite matching under identical boolean criteria changes the
counts as follows (no ranking changes). The greedy scan is conservative, and
its only measurable distortion works against PT-OIE-EXTRACTOR, not in its
favor. Data source: `../metrics/greedy_vs_optimal_bia_legacy.csv`.

| System | Greedy F1 | Optimal F1 | Delta TP | Delta F1 |
|---|---:|---:|---:|---:|
| PT-OIE-EXTRACTOR | 54.92 | 56.37 | +7 | +1.45 |
| Pure UD baseline | 52.71 | 53.68 | +5 | +0.97 |
| Gemma 4 | 43.30 | 43.47 | +1 | +0.17 |
| Multi2OIE | 34.39 | 34.39 | 0 | 0.00 |
| DptOIE | 12.82 | 12.96 | +2 | +0.14 |
