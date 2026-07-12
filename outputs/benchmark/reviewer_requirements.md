# Matriz de requisitos dos revisores — benchmark comparativo

Fontes lidas antes da implementação:

- Artigo: *Deconstructing UD+Attention for Open Information Extraction on Brazilian Portuguese* (submissão EMNLP 2026, short paper, PDF fornecido).
- Pareceres consolidados dos três revisores e propostas de resposta: `../../revisao_arr/proposta_respostas_revisores_emnlp_arr.pdf` (lido integralmente).
- PDF comentado por Rerisson: `../../comentarios_rerisson/EMNLP_2026___...COMENTADO RERISSON.pdf`.
- Código do artefato: `src/extractor.py`, `src/run_experiment.py`, `src/run_all_ablations.py`, `README.md`, `notebooks/openie_pt_experiment_final.ipynb`.
- Corpus: `data/bia_gold_sentences.jsonl` (262 sentenças, 427 triplas gold, todas `valid=true`), `data/pt_bosque-ud-train.conllu`.

| Reviewer concern | Evidence in the paper | Required action | Experiment | Output |
|---|---|---|---|---|
| Ausência de comparação com sistemas externos (R1 §5, R2 §1, R3 §3) | Sem baseline externo; apenas ablação interna (Tabela 3) | Executar DptOIE, Multi²OIE e PortNOIE sobre o BIA com os mesmos protocolos, ou documentar indisponibilidade objetiva | Benchmark comparativo neste repositório (`scripts/run_benchmark.py`) | `outputs/benchmark/metrics/`, `outputs/benchmark/system_availability.json` |
| Ausência de comparação com LLMs abertos (R2, "pelo menos um LLM aberto instruído") | Nenhum LLM avaliado no mesmo corpus | Executar Gemma 4 (Ollama, local, zero-shot, prompt fixo) sobre as mesmas 262 sentenças | Sistema `ollama_gemma4` | `outputs/benchmark/raw/ollama_gemma4.jsonl`, métricas |
| Separar efeito do backbone UD (R2 §3, R3 §3) | RQ1 vs RQ3 = +2,21 F1 (Tabela 3) | Reexecutar RQ1 (UD puro) como baseline interno do benchmark e medir delta pareado com IC | Sistema `ud_baseline` vs `pt_oie` + bootstrap pareado | `outputs/benchmark/bootstrap/paired_f1_differences.csv` |
| Cobertura parcial do módulo de atenção (R1 §1) | 62,1% dos triples cobertos (§5.1) | Reconhecer; reportar análise por padrão UD (padrões com/sem atenção) para RQ1 vs RQ3 | Análise por padrão em `metrics_by_pattern.csv` | `outputs/benchmark/metrics/metrics_by_pattern.csv` |
| Corpus pequeno / incerteza estatística (R1 §3, R3) | 262 sentenças, 427 triplas (Limitations) | Bootstrap pareado por sentença, 10.000 reamostragens, IC 95% para P/R/F1 e para deltas | `scripts/evaluate_benchmark.py --bootstrap-samples 10000` | `outputs/benchmark/bootstrap/confidence_intervals.csv` |
| Ausência de intervalos de confiança (R1, R3: "necessário e viável") | Nenhum IC reportado | Idem acima; não declarar significância só pelo valor pontual | Bootstrap | `outputs/benchmark/bootstrap/` |
| Ausência de concordância entre anotadores (R1 §4) | Corpus por proposta e consenso, sem Kappa (Limitations) | Não recalculável retrospectivamente; registrar como limitação explícita | — (documental) | `outputs/benchmark/reports/limitations.md` |
| Sensibilidade ao protocolo de matching (R2 §4) | F1 de 18,03% a 61,14% (Tabela 4) | Avaliar todos os sistemas sob os 4 protocolos (strict, tolerant, bia_legacy, carb_style) | Avaliação multiprotocolo | `outputs/benchmark/metrics/metrics_by_system_protocol.csv` |
| Falta de formalização do avaliador "Official" (R3 §4) | "project scoring script... retained for continuity" (§3.3) | Renomear para `bia_legacy`, preservar comportamento bit a bit, documentar normalização/matching/thresholds | Documentação + reuso de `evaluate_dataset_legacy` | `BENCHMARK.md` §Protocolos, `src/benchmark/evaluation.py` |
| Comparação com DptOIE (R2, R3) | Citado mas não executado (Limitations) | Obter implementação oficial (Java), executar sobre BIA ou registrar `unavailable` com evidência | Sistema `dptoie` | `outputs/benchmark/system_availability.json` |
| Comparação com PortNOIE (R2, R3) | Citado mas não executado | Procurar artefato oficial executável; não construir substituto; registrar busca | Sistema `portnoie` | `outputs/benchmark/system_availability.json` |
| Comparação com Multi²OIE (R3 §5, Related Work) | Omitido do Related Work | Obter implementação/checkpoint oficiais (zero-shot ou multilíngue), executar ou registrar indisponibilidade | Sistema `multi2oie` | `outputs/benchmark/system_availability.json` |
| Posicionamento diante de BenchIE / BenchIE-FL (R3 §5) | Omitidos do Related Work | Reconhecer no relatório aos revisores; adaptação do BenchIE fica para nova versão (o próprio revisor a exclui da discussão) | — (documental) | `outputs/benchmark/reports/reviewer_response_evidence.md` |
| Documentar novidade e componentes herdados (R3 §1) | "retained for continuity with earlier runs" sugere trabalho anterior | Declarar sem ambiguidade o que é novo nesta submissão; registrar proveniência dos componentes no manifesto | — (documental) | `outputs/benchmark/reports/reviewer_response_evidence.md`, `manifest.json` |
| Sem reivindicação de estado da arte (R2 §1) | Artigo não reivindica SOTA | Tabela comparativa sem destaque automático do PT-OIE-EXTRACTOR; destacar melhor resultado só após cálculo objetivo | Tabela LaTeX | `outputs/benchmark/reports/benchmark_results.tex` |

Notas de escopo, registradas antes da execução:

1. Os revisores classificam a execução de DptOIE/PortNOIE/Multi²OIE/LLMs como material **para a próxima versão**, não para o período de discussão; este benchmark antecipa esse trabalho.
2. Nenhuma conclusão do artigo será alterada antes da obtenção dos resultados.
3. O corpus BIA e as triplas gold não serão modificados; o BIA não será usado como conjunto de desenvolvimento (prompt do Gemma 4 fixado antes de qualquer resultado, sem exemplos do BIA).
