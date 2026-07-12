# Evidências para resposta aos revisores (ARR/EMNLP 2026)

Benchmark executado em 2026-07-12 sobre o BIA (262 sentenças, 427 triplas gold,
SHA-256 `ddd882e9...`). Métricas completas: `../metrics/`, ICs e diferenças
pareadas: `../bootstrap/`. Salvo indicação, F1 sob o protocolo `bia_legacy`
(o antigo "Official"), agora formalizado; os quatro protocolos estão reportados
lado a lado em `metrics_by_system_protocol.csv`.

Resumo dos resultados:

| Sistema | F1 legacy | IC95 | F1 strict | F1 tolerant | F1 CaRB-style |
|---|---|---|---|---|---|
| PT-OIE-EXTRACTOR (UD+atenção) | **54,92** | [51,00, 58,75] | 18,37 | 29,14 | **61,67** |
| UD puro (RQ1) | 52,71 | [49,03, 56,34] | 17,48 | 30,78 | 59,19 |
| Gemma 4 (Ollama, zero-shot) | 43,30 | [40,13, 46,59] | **22,34** | 28,87 | 47,94 |
| Multi²OIE (zero-shot oficial) | 34,39 | [31,13, 37,85] | 0,91 | 15,47 | 49,32 |
| DptOIE (oficial) | 12,82 | [10,78, 15,04] | 4,24 | 7,35 | 15,75 |
| PortNOIE | indisponível (não é zero) | — | — | — | — |

---

## Revisor 1

### R1.1 Cobertura parcial da atenção (62,1%)
- **Experimento:** reexecução de RQ1 vs RQ3 com bootstrap pareado por sentença
  (10.000 reamostragens, seed 42).
- **Resultado:** ΔF1(UD+atenção − UD puro) = **+2,21 pontos**, IC95 **[+0,61, +3,81]**,
  P(Δ>0) = **99,64%** (`bootstrap/paired_f1_differences.csv`).
- **Evidência:** `metrics/metrics_by_system_protocol.csv`, `bootstrap/`.
- **Conclusão permitida:** o ganho da atenção é positivo e estatisticamente
  robusto sob o protocolo legado, mesmo com cobertura de 62,1%.
- **Conclusão não permitida:** que a atenção ajudaria igualmente em padrões
  fora do seu escopo.
- **Trecho sugerido (Official Comment):**
  "We computed sentence-level paired bootstrap intervals (10,000 resamples).
  The attention-enabled configuration improves F1 over the pure-UD baseline by
  2.21 points, 95% CI [0.61, 3.81], with 99.6% of resamples favoring attention."

### R1.3 Corpus pequeno / incerteza
- **Resultado:** ICs bootstrap para P, R e F1 de todos os sistemas
  (`bootstrap/confidence_intervals.csv`); o IC do F1 do PT-OIE-EXTRACTOR é
  [51,00, 58,75].
- **Conclusão permitida:** efeitos de componente da ordem de vários pontos são
  detectáveis; diferenças pequenas permanecem não conclusivas (registrado em
  `limitations.md`).

### R1.4 Concordância entre anotadores
- Não recalculável retrospectivamente; mantida como limitação
  (`limitations.md` §2). Nenhum experimento novo é possível sem nova anotação.

### R1.5 Ausência de comparação entre sistemas
- **Experimento:** benchmark comparativo com DptOIE (implementação e modelos
  oficiais), Multi²OIE (código e checkpoint multilíngue oficiais, zero-shot) e
  Gemma 4 (LLM aberto local, zero-shot), todos nas mesmas 262 sentenças e sob
  os mesmos 4 protocolos.
- **Resultado:** ver tabela acima. Sob o protocolo legado e o CaRB-style, o
  PT-OIE-EXTRACTOR supera todos os sistemas comparados
  (Δ vs Gemma 4 = +11,62 [7,11, 15,94]; vs Multi²OIE = +20,53 [16,08, 25,03];
  vs DptOIE = +42,10 [38,11, 46,02]). Sob o protocolo strict, o Gemma 4 é o
  melhor sistema (22,34 vs 18,37) — reforçando a tese do artigo sobre
  sensibilidade ao protocolo.
- **Conclusão permitida:** na configuração avaliada e sob os protocolos
  reportados, o PT-OIE-EXTRACTOR é competitivo com sistemas simbólicos,
  neurais zero-shot e um LLM aberto no BIA.
- **Conclusão não permitida:** estado da arte em geral; DptOIE/Multi²OIE não
  foram ajustados ao guideline do BIA e o Multi²OIE é zero-shot n-ário
  (mapeado para binário), o que os penaliza em protocolos estritos.

## Revisor 2

### R2.1 Sem reivindicação de estado da arte
- A tabela LaTeX não destaca o PT-OIE-EXTRACTOR automaticamente; o melhor
  resultado por protocolo foi apurado numericamente. O texto sugerido evita
  "state of the art" e restringe as claims ao corpus e protocolos usados.

### R2.3 Baseline interno
- Reconfirmado com estatística: +2,21 F1 [0,61, 3,81] (ver R1.1).

### R2 Experimento pedido ("DptOIE, pelo menos um LLM aberto, PortNOIE e Multi²OIE se possível")
- Executados: DptOIE (oficial), Multi²OIE (oficial, zero-shot), Gemma 4
  (LLM aberto local). PortNOIE documentado como indisponível com evidência
  objetiva (`system_availability.json`) — sem substituto aproximado.

### R2.4 Sensibilidade ao protocolo (achado que transcende o sistema)
- **Resultado novo:** o ranking dos sistemas muda com o protocolo
  (Gemma 4 é 3º no legado e 1º no strict; Multi²OIE quase dobra o F1 do
  tolerant para o CaRB-style). A mesma predição do PT-OIE-EXTRACTOR varia de
  18,37 (strict) a 61,67 (CaRB-style).
- **Trecho sugerido:** "Under four matching protocols applied to identical
  predictions, system rankings change: the zero-shot LLM ranks first under
  strict matching but third under the legacy matcher. This confirms that
  protocol choice, not only architecture, drives reported Portuguese OpenIE
  scores."

## Revisor 3

### R3.1 Novidade do PT-OIE-EXTRACTOR
- **Confirmado pelo autor (2026-07-12):** o extrator não foi descrito em
  qualificação, tese ou qualquer submissão anterior; não há publicação prévia
  do sistema. Busca por "PT-OIE-EXTRACTOR" na literatura não retorna nenhuma
  ocorrência. As pastas de versões (v2–v16) contêm apenas experimentos
  internos de desenvolvimento.
- Único componente herdado de trabalho publicado: a seleção de cabeças de
  atenção deriva de Oliveira, Claro & Cavalcante (STIL 2025), já citado na
  submissão.
- **Trecho definitivo para o Official Comment:**
  "PT-OIE-EXTRACTOR is introduced for the first time in this submission.
  The attention-head selection derives from our prior analysis (Oliveira et
  al., 2025), which is cited; the extraction pipeline, the validation layer,
  and the ablation study are contributions of this submission. 'Earlier runs'
  refers only to internal development experiments, not to a previously
  published system."

### R3.2 BIA não foi criado neste trabalho
- Confirmado e citado (Queiroz et al., 2023); o benchmark usa o arquivo
  publicado sem modificação (SHA-256 no manifesto).

### R3.4 Avaliador "Official" formalizado
- **Ação executada:** renomeado para `bia_legacy`; normalização, matching,
  thresholds e política de atribuição documentados em `BENCHMARK.md` e
  `src/benchmark/evaluation.py`; comportamento preservado **bit a bito** —
  a reexecução reproduz exatamente TP=265/FP=273/FN=162 (F1=54,92) do artigo
  (`tests/test_reproduction.py`).
- 54,92 não é apresentado como comparável externamente; a tabela reporta os
  quatro protocolos.

### R3.5 Related Work (Multi²OIE, CrossOIE, MT4CrossOIE, BenchIE, BenchIE-FL)
- Multi²OIE agora é comparado empiricamente. Os demais são reconhecidos como
  necessários ao posicionamento (a adaptação do BenchIE ao português permanece
  trabalho futuro, como o próprio revisor delimita).

### R3.6 Reprodutibilidade
- Artefato com código, dados, dependências, seeds, hashes, digest do modelo
  e comandos: `BENCHMARK.md`, `manifest.json`,
  `reports/reproducibility_checklist.md`.

---

## Observações de integridade

- O prompt do Gemma 4 foi fixado antes de qualquer resultado e não foi alterado
  (SHA-256 no manifesto); zero-shot, sem exemplos do BIA.
- Falhas: DptOIE 1/262 (crash interno do sistema em uma sentença),
  Gemma 4 1/262 (JSON fora do schema mesmo após o único reparo permitido);
  contabilizadas como zero predição, sem imputação nem exclusão.
- Sistemas indisponíveis não receberam métricas.
- Nenhuma predição foi corrigida manualmente.
