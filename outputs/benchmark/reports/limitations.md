# Limitações do benchmark comparativo

1. **Corpus pequeno.** 262 sentenças / 427 triplas gold. Os ICs bootstrap
   quantificam a incerteza, mas diferenças pequenas entre sistemas permanecem
   estatisticamente indistinguíveis; conclusões sobre elas devem ser moderadas.

2. **Concordância entre anotadores.** O BIA foi anotado por proposta e consenso
   mútuo (Queiroz et al., 2023); não há anotação paralela independente e o
   Kappa não pode ser reconstruído retrospectivamente. Limitação herdada por
   todas as comparações deste benchmark.

3. **Protocolos de matching não são intercambiáveis.** O `bia_legacy` é o
   avaliador histórico do projeto e seus números não são comparáveis
   externamente. Os quatro protocolos são reportados lado a lado justamente
   porque o F1 do mesmo conjunto de predições varia dezenas de pontos entre
   protocolos.

4. **Deduplicação.** Os protocolos padronizados deduplicam predições exatas
   (minúsculas/espaços) de forma idêntica para todos os sistemas; o
   `bia_legacy` não deduplica (fidelidade histórica). Sistemas que emitem
   variantes quase duplicadas (ex.: DptOIE, com variantes de spans) são
   afetados de modo diferente por protocolos com e sem dedup.

5. **PortNOIE indisponível.** Código oficial existe (FORMAS/dptoie-neural,
   commit 770f29fe) com modelo treinado, mas o ambiente oficial
   (Python <3.10, allennlp==2.7.0, sru@3.0.0-dev e flair@master não pinados)
   não é reconstituível deterministicamente. Não foi construído substituto.
   A comparação com PortNOIE permanece em aberto.

6. **Multi²OIE em stack moderno.** O checkpoint oficial (torch 1.4) foi
   carregado com torch 2.5.1/transformers 4.48.2 (0 chaves faltantes/
   inesperadas). Diferenças numéricas de kernels entre versões de torch podem,
   em princípio, alterar marginalmente as saídas em relação ao ambiente
   original dos autores.

7. **Multi²OIE é zero-shot n-ário.** O modelo foi treinado em inglês
   (OpenIE4) e produz tuplas n-árias; o mapeamento para o esquema binário
   (arg2 = concatenação dos argumentos restantes) é documentado, mas penaliza
   o sistema em protocolos estritos de fronteira.

8. **Gemma 4 quantizado.** `gemma4:latest` no Ollama é Q4_K_M (8,0B). Resultados
   podem diferir dos pesos plenos. O digest exato está no manifesto. Decodificação
   com temperatura 0/seed fixa é determinística apenas na medida em que o
   runtime do Ollama o suporta.

9. **Uma única execução por sistema.** Sistemas determinísticos (UD, DptOIE)
   não variam; para o Gemma 4 não foram feitas execuções repetidas para
   estimar variância residual de runtime.

10. **Parser único.** PT-OIE-EXTRACTOR e UD baseline dependem do Stanza; a
    sensibilidade a parser não foi avaliada (limitação também registrada no
    artigo).

11. **Falhas contabilizadas, não imputadas.** Sentenças com erro contam como
    zero predição (FNs integrais) nas métricas agregadas do sistema que falhou,
    com a taxa de falha reportada separadamente — não houve exclusão de
    sentenças nem imputação.
