# Multi²OIE — artefatos oficiais utilizados (sem alteração de código)

- Sistema: Multi²OIE (Ro, Lee & Kang, EMNLP 2020)
- Repositório oficial: youngbin-ro/Multi2OIE, commit `4a73a3c37412` (clone raso em `.external/Multi2OIE`)
- Checkpoint: modelo multilíngue oficial distribuído pelos autores no Google Drive
  apontado pelo README oficial (`multilingual_model.bin`, 980.501.266 bytes,
  datado de 2021), salvo em `.external/Multi2OIE/multilingual_model.bin`.
- Modo de execução: multilíngue zero-shot, como no artigo original (mBERT
  treinado só com dados em inglês do OpenIE4 e testado em português sem ajuste).
  **Nenhum treino ou ajuste com o BIA.**
- Alteração de código: **nenhuma.** O adaptador do benchmark invoca
  `dataset.load_data(train=False)` e `extract.extract` do próprio repositório.
- Nota de compatibilidade: o requirements.txt oficial pina torch 1.4.0 e
  transformers 2.10.0 (Python 3.7). A execução usou torch 2.5.1 e
  transformers 4.48.2; `load_state_dict` do checkpoint retorna **0 chaves
  faltantes e 0 inesperadas**, e a única API do transformers usada pelo modelo
  (`BertModel(...)[0]`) é estável entre as versões. A diferença de stack fica
  registrada no manifesto.
- Mapeamento para o esquema binário do benchmark: a saída oficial é n-ária
  `[pred, arg0, arg1, ...]`; arg1 = arg0, rel = pred, arg2 = concatenação dos
  demais argumentos. A linha bruta completa é preservada em `raw_output`.
- Licença: MIT (arquivo LICENSE do repositório).
