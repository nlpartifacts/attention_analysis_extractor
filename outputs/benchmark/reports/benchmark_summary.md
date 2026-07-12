# Comparative benchmark: summary

Corpus: BIA, 262 sentences, 427 gold triples (sha256 `ddd882e93b3d...`).
Gemma 4: `gemma4:latest` digest `c6eb396dbd5992bbe3f5cdb947e8bbc0ee413d7c17e2beaae69f5d569cf982eb`, quantization Q4_K_M, Ollama 0.20.0.

## Metrics (all protocols)

| System | Protocol | TP | FP | FN | P | R | F1 | 95% CI (F1) |
|---|---|---|---|---|---|---|---|---|
| dptoie | strict | 53 | 2022 | 374 | 2.55 | 12.41 | 4.24 | [3.08, 5.49] |
| dptoie | tolerant | 92 | 1983 | 335 | 4.43 | 21.55 | 7.35 | [5.84, 9.00] |
| dptoie | bia_legacy | 180 | 2201 | 247 | 7.56 | 42.15 | 12.82 | [10.78, 15.04] |
| dptoie | carb_style | 197 | 1878 | 230 | 9.49 | 46.14 | 15.75 | [13.42, 18.26] |
| multi2oie | strict | 5 | 667 | 422 | 0.74 | 1.17 | 0.91 | [0.18, 1.78] |
| multi2oie | tolerant | 85 | 587 | 342 | 12.65 | 19.91 | 15.47 | [12.61, 18.47] |
| multi2oie | bia_legacy | 189 | 483 | 238 | 28.12 | 44.26 | 34.39 | [31.13, 37.85] |
| multi2oie | carb_style | 271 | 401 | 156 | 40.33 | 63.47 | 49.32 | [46.63, 52.10] |
| ollama_gemma4 | strict | 130 | 607 | 297 | 17.64 | 30.45 | 22.34 | [19.09, 25.68] |
| ollama_gemma4 | tolerant | 168 | 569 | 259 | 22.80 | 39.34 | 28.87 | [25.59, 32.31] |
| ollama_gemma4 | bia_legacy | 252 | 485 | 175 | 34.19 | 59.02 | 43.30 | [40.13, 46.59] |
| ollama_gemma4 | carb_style | 279 | 458 | 148 | 37.86 | 65.34 | 47.94 | [44.85, 51.11] |
| pt_oie | strict | 87 | 433 | 340 | 16.73 | 20.37 | 18.37 | [15.03, 21.79] |
| pt_oie | tolerant | 138 | 382 | 289 | 26.54 | 32.32 | 29.14 | [25.59, 32.71] |
| pt_oie | bia_legacy | 265 | 273 | 162 | 49.26 | 62.06 | 54.92 | [51.00, 58.75] |
| pt_oie | carb_style | 292 | 228 | 135 | 56.15 | 68.38 | 61.67 | [58.21, 65.04] |
| ud_baseline | strict | 88 | 492 | 339 | 15.17 | 20.61 | 17.48 | [14.26, 20.79] |
| ud_baseline | tolerant | 155 | 425 | 272 | 26.72 | 36.30 | 30.78 | [27.29, 34.29] |
| ud_baseline | bia_legacy | 272 | 333 | 155 | 44.96 | 63.70 | 52.71 | [49.03, 56.34] |
| ud_baseline | carb_style | 298 | 282 | 129 | 51.38 | 69.79 | 59.19 | [55.99, 62.31] |

## Paired F1 differences (sentence-level bootstrap)

| A | B | Protocol | ΔF1 (point) | mean ΔF1 | 95% CI | P(Δ>0) |
|---|---|---|---|---|---|---|
| pt_oie | ud_baseline | strict | 0.90 | 0.89 | [0.37, 1.33] | 0.9987 |
| pt_oie | ud_baseline | tolerant | -1.64 | -1.65 | [-3.25, -0.26] | 0.0078 |
| pt_oie | ud_baseline | bia_legacy | 2.21 | 2.21 | [0.61, 3.81] | 0.9964 |
| pt_oie | ud_baseline | carb_style | 2.48 | 2.49 | [1.42, 3.60] | 1.0000 |
| pt_oie | dptoie | strict | 14.14 | 14.12 | [10.89, 17.52] | 1.0000 |
| pt_oie | dptoie | tolerant | 21.79 | 21.78 | [18.18, 25.43] | 1.0000 |
| pt_oie | dptoie | bia_legacy | 42.10 | 42.09 | [38.11, 46.02] | 1.0000 |
| pt_oie | dptoie | carb_style | 45.92 | 45.92 | [42.02, 49.78] | 1.0000 |
| pt_oie | multi2oie | strict | 17.46 | 17.44 | [14.06, 20.95] | 1.0000 |
| pt_oie | multi2oie | tolerant | 13.68 | 13.66 | [9.16, 18.10] | 1.0000 |
| pt_oie | multi2oie | bia_legacy | 20.53 | 20.50 | [16.08, 25.03] | 1.0000 |
| pt_oie | multi2oie | carb_style | 12.35 | 12.35 | [8.77, 15.94] | 1.0000 |
| pt_oie | ollama_gemma4 | strict | -3.96 | -4.00 | [-8.83, 0.67] | 0.0490 |
| pt_oie | ollama_gemma4 | tolerant | 0.28 | 0.23 | [-4.59, 4.88] | 0.5398 |
| pt_oie | ollama_gemma4 | bia_legacy | 11.62 | 11.58 | [7.11, 15.94] | 1.0000 |
| pt_oie | ollama_gemma4 | carb_style | 13.73 | 13.70 | [9.72, 17.65] | 1.0000 |
| dptoie | ollama_gemma4 | strict | -18.10 | -18.12 | [-21.66, -14.60] | 0.0000 |
| dptoie | ollama_gemma4 | tolerant | -21.51 | -21.55 | [-25.24, -17.93] | 0.0000 |
| dptoie | ollama_gemma4 | bia_legacy | -30.48 | -30.51 | [-34.17, -26.89] | 0.0000 |
| dptoie | ollama_gemma4 | carb_style | -32.19 | -32.22 | [-35.92, -28.40] | 0.0000 |
| multi2oie | ollama_gemma4 | strict | -21.43 | -21.44 | [-24.77, -18.18] | 0.0000 |
| multi2oie | ollama_gemma4 | tolerant | -13.40 | -13.43 | [-17.43, -9.48] | 0.0000 |
| multi2oie | ollama_gemma4 | bia_legacy | -8.90 | -8.92 | [-13.04, -4.81] | 0.0000 |
| multi2oie | ollama_gemma4 | carb_style | 1.38 | 1.35 | [-2.18, 4.85] | 0.7726 |

## Unavailable systems (no metrics, since unavailability is not zero)

- **portnoie**: official code exists (FORMAS/dptoie-neural) with a trained model, but its official environment (Python$<$3.10, allennlp 2.7.0, unpinned git dependencies) is not deterministically reconstructible; building an approximate substitute is not allowed

## Runtime

| System | Sentences | Errors | Triples | Median s/sent | p95 s/sent |
|---|---|---|---|---|---|
| dptoie | 262 | 1 | 2381 | 0.254 | 0.254 |
| multi2oie | 262 | 0 | 672 | 0.103 | 0.103 |
| ollama_gemma4 | 262 | 1 | 737 | 4.707 | 10.258 |
| pt_oie | 262 | 0 | 538 | 0.159 | 0.277 |
| ud_baseline | 262 | 0 | 605 | 0.179 | 0.340 |
