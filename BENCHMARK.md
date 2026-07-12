# Benchmark comparativo de OpenIE para português brasileiro (corpus BIA)

Benchmark cientificamente controlado que compara sistemas de Open Information
Extraction sobre **exatamente as mesmas 262 sentenças e 427 triplas gold** do
corpus BIA (`data/bia_gold_sentences.jsonl`, SHA-256 registrado no manifesto).
Motivado pelos pareceres da submissão EMNLP 2026 do PT-OIE-EXTRACTOR
(ver `outputs/benchmark/reviewer_requirements.md`).

## Sistemas

| Sistema | Origem | Execução |
|---|---|---|
| `pt_oie` | Este repositório — melhor configuração do artigo (`rq3_attn_on_thr0`: UD + atenção, heads rank top-10, τ=0.0, validação off, seed 13) | local, GPU |
| `ud_baseline` | Este repositório — RQ1 (UD puro, sem atenção, sem validação) | local |
| `dptoie` | Oficial: FORMAS/DptOIE + modelos do Drive dos autores (ver `patches/dptoie_artifacts.md`) | Java, lote |
| `multi2oie` | Oficial: youngbin-ro/Multi2OIE + checkpoint multilíngue oficial, zero-shot (ver `patches/multi2oie_artifacts.md`) | CPU, lote |
| `portnoie` | **Indisponível** — código oficial existe (FORMAS/dptoie-neural) mas o ambiente de execução não é reconstituível; sem substituto (ver `outputs/benchmark/system_availability.json`) | — |
| `ollama_gemma4` | `gemma4:latest` via API nativa do Ollama, zero-shot, prompt fixo (`configs/gemma4_prompt_pt.txt`), temperatura 0, seed 42, digest verificado | local, GPU |

Sistemas indisponíveis **não** recebem métricas (indisponibilidade não é zero).

## Reprodução

```bash
# 0. Ambiente: Python 3.12 (ver requirements.txt) + pytest
#    Ollama em http://localhost:11434 com gemma4:latest
#    Java 8+ para o DptOIE

# 1. Validar corpus (262 sentenças / 427 triplas / SHA-256)
python -m scripts.validate_corpus

# 2. Obter sistemas externos oficiais (rede; idempotente)
python -m scripts.fetch_external_systems
# DptOIE: copiar pt-dep-parser.gz e DptOIE.jar da pasta "Models" (Drive oficial)
#   para .external/DptOIE/ — ver patches/dptoie_artifacts.md (hashes)
# Multi2OIE: baixar o checkpoint multilíngue oficial para
#   .external/Multi2OIE/multilingual_model.bin — ver patches/multi2oie_artifacts.md

# 3. Registrar o digest do gemma4:latest (obrigatório antes da execução)
python -m scripts.inspect_ollama --model gemma4:latest \
  --output outputs/benchmark/models/gemma4_latest_manifest.json

# 4. Testes unitários
python -m pytest tests/ -q

# 5. Smoke test (formato e erros técnicos; 5 sentenças)
python -m scripts.smoke_test_benchmark --systems pt_oie ud_baseline ollama_gemma4 --limit 5

# 6. Benchmark completo (a extração grava raw/, normalized/, errors/)
python -m scripts.run_benchmark \
  --config configs/benchmark.yaml \
  --systems pt_oie ud_baseline dptoie multi2oie portnoie ollama_gemma4 \
  --output-dir outputs/benchmark \
  --seed 42

# 7. Avaliação (reexecutável a partir das predições salvas, sem nova extração)
python -m scripts.evaluate_benchmark \
  --predictions-dir outputs/benchmark/normalized \
  --gold data/bia_gold_sentences.jsonl \
  --output-dir outputs/benchmark \
  --bootstrap-samples 10000 \
  --seed 42

# 8. Relatórios (resumo, tabela LaTeX)
python -m scripts.generate_reviewer_report
```

Opções úteis de `run_benchmark`: `--systems`, `--limit`, `--resume`, `--force`,
`--fail-fast`, `--timeout`, `--dry-run`.

## Protocolos de avaliação

Todos os sistemas são avaliados pelos mesmos quatro protocolos; apenas triplas
gold com `valid=true` contam. Nos protocolos padronizados (strict, tolerant,
carb_style), deduplicação exata (minúsculas + colapso de espaços) é aplicada
às predições de todos os sistemas antes do matching. O `bia_legacy` **não**
aplica deduplicação, para preservar exatamente o comportamento histórico do
avaliador do artigo — verificado por reprodução bit-exata dos números
publicados (RQ3: TP=265, FP=273, FN=162, F1=54,92; RQ1: F1=52,71).

1. **strict** — igualdade exata dos três slots após minúsculas e colapso de
   espaços; atribuição um-para-um determinística.
2. **tolerant** — F1 de tokens por slot (tokenização: minúsculas, pontuação
   removida, acentos preservados); par elegível quando o **menor** F1 de slot
   ≥ 0.70; atribuição um-para-um pelo F1 médio dos slots.
3. **carb_style** — score ponderado 0.35·F1(arg1) + 0.30·F1(rel) + 0.35·F1(arg2)
   ≥ 0.60; atribuição um-para-um pelo score.
4. **bia_legacy** — o avaliador legado do projeto (antes chamado *Official* no
   artigo), preservado **sem alteração** via `src.extractor.evaluate_dataset_legacy`.
   Normalização: minúsculas, expansão de contrações, remoção de pontuação,
   remoção de determinantes iniciais dos argumentos. Matching de argumentos:
   igualdade, sufixo, prefixo (≥1 token) ou subconjunto de palavras; relação:
   igualdade ou prefixo parcial (com salto de verbo leve inicial do gold).
   Varredura gulosa na ordem do gold, um-para-um por construção. Números
   obtidos sob este protocolo não são comparáveis externamente.

Nos protocolos padronizados (1–3) a atribuição ordena os pares por
(-score, índice gold, índice predição) — determinística, empates estáveis.

## Estatística

- Bootstrap **pareado por sentença** (unidade de reamostragem = sentença),
  10.000 reamostragens, seed 42, IC percentil 95%.
- As diferenças de F1 entre sistemas usam as **mesmas** reamostragens
  (pareamento), com ΔF1 médio, mediana, IC 95% e P(Δ>0).
- Nenhuma alegação de significância é feita apenas com o valor pontual.

## Regras científicas aplicadas

- Corpus e gold intocados; mesmo conjunto e ordem de sentenças para todos.
- Prompt do Gemma 4 fixado antes de qualquer resultado (SHA-256 no manifesto),
  zero-shot, sem exemplos do BIA, temperatura 0, seed 42, no máximo 1 reparo
  por sentença restrito à conversão de formato da resposta original.
- Digest de `gemma4:latest` resolvido antes da execução e verificado
  (`fail_on_digest_change: true`); resultados de digests diferentes não se misturam.
- Falhas por sentença são registradas (`errors/`) e contabilizadas — nunca
  convertidas em lista vazia; lista vazia só vale quando retornada explicitamente.
- Sistemas externos: somente implementação/artefatos oficiais, commits e hashes
  registrados; nenhuma regra ou peso alterado (ver `patches/`).
- Saída bruta integral preservada em `outputs/benchmark/raw/`.

### Ajustes técnicos registrados (smoke test)

Dois ajustes de **formato/capacidade** foram feitos após o smoke test de 5
sentenças, antes da execução completa, sem tocar no prompt e sem consultar o gold:

1. O template do `gemma4` no Ollama 0.20 devolve o JSON dentro de cerca
   markdown mesmo com `format` (JSON Schema); o parser remove a cerca
   sintaticamente (conteúdo interno intacto; resposta bruta preservada).
2. `num_predict` 384→1024: sentenças longas do BIA truncavam a resposta
   (`done_reason=length`), invalidando o JSON.

## Saídas

Ver árvore completa em `outputs/benchmark/`: manifesto (`manifest.json` com
corpus SHA-256, commits, digest, seeds, versões, ambiente), disponibilidade
(`system_availability.json`), predições (`raw/`, `normalized/`, `errors/`),
matching por protocolo (`matches/`), métricas (`metrics/`), bootstrap
(`bootstrap/`), execução (`runtime/`) e relatórios (`reports/`, incluindo
`benchmark_results.tex`).
