# DptOIE — official artifacts used (no code changes)

- System: DptOIE (Oliveira, Claro & Souza, 2023)
- Official repository: FORMAS/DptOIE, commit `1a5ef708b1ed` (shallow clone in `.external/DptOIE`)
- Reason for this record: the repository ships `DptOIE.jar` and
  `pt-models/pt-pos-tagger.model`, but the dependency-parser model
  (`pt-dep-parser.gz`) is distributed by the authors in the "Models" folder
  (Google Drive) linked from the official README.
- Modification: **no line of DptOIE code was changed.** The following files
  were copied from the authors' official distribution channel:
  - `pt-models/pt-dep-parser.gz` (sha256 `341e6b5bfc2288b8e7991ee746b2517b02dfb2ef7e540b3666f2b969bd4db30d`)
  - `DptOIE.jar` from the Drive, saved as `DptOIE-drive.jar` (sha256 `9c260049ad0ff03bcd795c5837ea71f62308bdf5fa088eada75cf2b3206a6dde`)
  - the git repository's jar, kept for reference (sha256 `5ff8246cc170537ce7ccb7e1640872564b1534f2ab6c0dbb00ea264468b36d52`)
- Execution: `java -jar DptOIE-drive.jar -sentencesIN <file> -SC true -CC true -appositive 1`,
  in batch mode (one invocation for the 262 sentences, in corpus order),
  since dependency-parser loading dominates per-process cost. A bisection
  fallback isolates sentences that crash the Java process (1/262 in this run).
- Expected effect: extractions produced by the official algorithm, with no
  modification of its linguistic rules.
- License: repository has no explicit LICENSE file; usage restricted to
  academic comparative evaluation, with citation to the authors.
