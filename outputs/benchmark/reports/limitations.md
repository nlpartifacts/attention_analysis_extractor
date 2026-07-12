# Limitations of the comparative benchmark

1. **Small corpus.** 262 sentences / 427 gold triples. Bootstrap confidence
   intervals quantify uncertainty, but small differences between systems
   remain statistically indistinguishable, and conclusions about them must be
   moderated.

2. **Inter-annotator agreement.** BIA was annotated by proposal and mutual
   consensus (Queiroz et al., 2023); there is no independent parallel
   annotation and Kappa cannot be reconstructed retrospectively. This
   limitation is inherited by every comparison in this benchmark.

3. **Matching protocols are not interchangeable.** `bia_legacy` is the
   project's historical scorer and its numbers are not externally comparable.
   The four protocols are reported side by side precisely because F1 on
   identical predictions varies by tens of points across protocols.

4. **Deduplication.** The standardized protocols deduplicate exact duplicates
   (lowercase, whitespace) identically for all systems, while `bia_legacy`
   does not, for historical fidelity. Systems that emit near-duplicate
   variants (for example, DptOIE span variants) are affected differently by
   protocols with and without deduplication.

5. **PortNOIE unavailable.** Official code exists (FORMAS/dptoie-neural,
   commit 770f29fe) with a trained model, but the official environment
   (Python below 3.10, allennlp 2.7.0, unpinned git dependencies
   sru@3.0.0-dev and flair@master) is not deterministically reconstructible.
   No substitute was built, and the comparison with PortNOIE remains open.

6. **Multi2OIE on a modern stack.** The official checkpoint (torch 1.4) was
   loaded with torch 2.5.1 and transformers 4.48.2 (0 missing or unexpected
   keys). Kernel-level numerical differences between torch versions could, in
   principle, marginally alter outputs relative to the authors' original
   environment.

7. **Multi2OIE is zero-shot and n-ary.** The model was trained on English
   (OpenIE4) and produces n-ary tuples; the mapping to the binary schema
   (arg2 as the concatenation of remaining arguments) is documented but
   penalizes the system under strict boundary protocols.

8. **Quantized Gemma 4.** `gemma4:latest` on Ollama is Q4_K_M (8.0B). Results
   may differ from full-precision weights. The exact digest is in the
   manifest. Decoding with temperature 0 and a fixed seed is deterministic
   only to the extent the Ollama runtime supports it.

9. **Single run per system.** Deterministic systems (UD, DptOIE) do not vary,
   and no repeated runs were performed for Gemma 4 to estimate residual
   runtime variance.

10. **Single parser.** PT-OIE-EXTRACTOR and the UD baseline depend on Stanza,
    and parser sensitivity was not evaluated (a limitation also recorded in
    the paper).

11. **Failures counted, not imputed.** Sentences with errors count as zero
    predictions (full FNs) in the failing system's aggregate metrics, with
    the failure rate reported separately. There was no sentence exclusion and
    no imputation.
