# DptOIE — artefatos oficiais utilizados (sem alteração de código)

- Sistema: DptOIE (Oliveira, Claro & Souza, 2023)
- Repositório oficial: FORMAS/DptOIE, commit `1a5ef708b1ed` (clone raso em `.external/DptOIE`)
- Razão deste registro: o repositório inclui `DptOIE.jar` e `pt-models/pt-pos-tagger.model`,
  mas o modelo do parser de dependências (`pt-dep-parser.gz`) é distribuído pelos
  autores na pasta "Models" (Google Drive) apontada no README oficial.
- Alteração: **nenhuma linha de código do DptOIE foi modificada.** Foram apenas
  copiados, do canal oficial de distribuição dos autores:
  - `pt-models/pt-dep-parser.gz` (sha256 `341e6b5bfc2288b8e7991ee746b2517b02dfb2ef7e540b3666f2b969bd4db30d`)
  - `DptOIE.jar` do Drive, salvo como `DptOIE-drive.jar` (sha256 `9c260049ad0ff03bcd795c5837ea71f62308bdf5fa088eada75cf2b3206a6dde`)
  - jar do repositório git, para referência (sha256 `5ff8246cc170537ce7ccb7e1640872564b1534f2ab6c0dbb00ea264468b36d52`)
- Execução: `java -jar DptOIE-drive.jar -sentencesIN <arquivo> -SC true -CC true -appositive 1`,
  em lote (uma invocação para as 262 sentenças, na ordem do corpus), pois a carga
  do parser domina o custo por processo.
- Efeito esperado: extrações produzidas pelo algoritmo oficial, sem qualquer
  modificação de regras linguísticas.
- Licença: repositório sem arquivo LICENSE explícito; uso restrito a avaliação
  acadêmica comparativa, com citação aos autores.
