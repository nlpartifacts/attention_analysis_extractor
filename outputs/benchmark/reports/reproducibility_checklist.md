# Checklist de reprodutibilidade

- [x] Corpus BIA validado antes da execução: 262 sentenças, 427 triplas gold,
      SHA-256 `ddd882e93b3d7f9f5778f1a740e0f3854a193e00327082acc3d658bd6550b19e`
      (`corpus_validation.json`).
- [x] Mesmas sentenças, na mesma ordem, para todos os sistemas.
- [x] Digest de `gemma4:latest` registrado ANTES da execução completa
      (`models/gemma4_latest_manifest.json` e `manifest.json`):
      `c6eb396dbd5992bbe3f5cdb947e8bbc0ee413d7c17e2beaae69f5d569cf982eb`,
      Ollama 0.20.0, Q4_K_M, 8,0B parâmetros. `fail_on_digest_change: true`.
- [x] Prompt do Gemma 4 fixo, SHA-256 registrado no manifesto; zero-shot,
      sem exemplos do BIA; inalterado após o smoke test.
- [x] Seeds fixas: benchmark/bootstrap/Gemma = 42; extrator (artigo) = 13.
- [x] Commits dos sistemas externos registrados (DptOIE `1a5ef708`,
      Multi2OIE `4a73a3c3`, dptoie-neural/PortNOIE `770f29fe`) + SHA-256 dos
      artefatos binários (`patches/*.md`).
- [x] Versões de SO, Python, PyTorch, Transformers, Stanza, CUDA, CPU, GPU e RAM
      em `environment.json`/`manifest.json`.
- [x] Saídas brutas integralmente preservadas (`raw/`), erros por sentença
      (`errors/`), predições normalizadas (`normalized/`).
- [x] Avaliação reexecutável a partir das predições salvas
      (`scripts/evaluate_benchmark.py`), sem nova extração; determinismo coberto
      por testes (`tests/test_determinism.py`).
- [x] Protocolo legado (`bia_legacy`) preservado sem alteração e verificado por
      reprodução bit-exata dos números do artigo
      (RQ3: TP=265/FP=273/FN=162, F1=54,92; RQ1: F1=52,71) —
      `tests/test_reproduction.py`.
- [x] Bootstrap pareado por sentença, 10.000 reamostragens, seed 42, IC
      percentil 95%; diferenças entre sistemas sobre as mesmas reamostragens.
- [x] Indisponibilidade registrada com evidência objetiva, sem atribuir zero
      (`system_availability.json`).
- [x] 52 testes unitários (`python -m pytest tests/ -q`).
- [x] Comandos completos de reprodução em `BENCHMARK.md`.
