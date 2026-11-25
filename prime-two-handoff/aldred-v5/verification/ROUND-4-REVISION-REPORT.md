# Aldred Limit v5 — Round 4 Revision Report

**Date:** 19 November 2026. **Manuscript:** `aldred-limit-v5.tex`, 880 → **886 lines**,
fourth revision. **Review basis:** `rounds/ROUND-4-REVIEW.md` (verdict: FINAL MINOR
REVISION — 0 blocking, 7 non-blocking) and `rounds/PRE-SUBMISSION-CHECKLIST.md`.

**Result: all 7 Round 4 non-blocking findings fixed, plus one blocking-grade
citation error found and fixed by closing the review's one open gap (R4-N7).**
Verification scripts now pass **94/94** and **75/75**. The only remaining
pre-submission item is the LaTeX compile (no toolchain on this VM).

---

## 1. What Round 4 found — and what changed

### R4-N1 — stale date line (fixed)
`\date{... Revision 5, second revision ...}` → **"fourth revision"**. Round 4
asked for "third revision", but that was the count before this polish pass:
Round 1 build, Round 2 rewrite, Round 3 rewrite, and this Round 4 revision
make four. The date line now names the manuscript as delivered.

### R4-N2 — 0.0005-bit seam between the two routes to the sever bench (fixed)
§8 now states: the 84.6219-dex figure is the earlier papers' rounded literal,
the exact gap from the thumbnail anchor is 84.62206 dex, the dex route lands
0.0005 bits from the direct route, and the table is computed from the anchor
directly. New script gate **SEAM-SEV** passes: computed 0.0005227 bits.

### R4-N3 — Appendix B count row undercounts COUNT gates (fixed)
Row now reads "13 table-entry gates (+ 5 supporting gates)" — the fifth
supporting gate is the new SEAM-SEV. (Supporting: COUNT-RHOL-GEV4,
COUNT-THUMB, COUNT-SEV-XCHECK, COUNT-ERR, SEAM-SEV.)

### R4-N4 — Table 1 d_A column ungated (fixed by adding gates)
7 new **T1d-\*** gates check d_A = n_A^(−1/3) against the printed values
(W 3.51, B 5.57, D 9.19, aligned-W 4.42, aligned-B 7.01, ratio-on-B 3.86,
ratio-on-W 2.43, all ×10⁻²⁹ m). All pass. One correction during the run:
T1d-W first failed at rel tolerance 1e-3 (computed 3.50582e-29 vs printed
3.51e-29, 0.119% — the print is the correct 3-significant-figure rounding,
and 3-sig-fig prints in the 3–9 range carry up to 0.14% rounding error).
Tolerance set to 2e-3, which covers the rounding and still catches any real
error. Appendix B Table 1 row now reads "21 gates".

### R4-N5 — Beck "about 24%" depends on the reference Λ (fixed)
Text now says "about $25\%$ above the measured value": the bench-derived
ratio is 1.2493 (24.9%), while the script's H0/Ω_Λ reference gives 1.2437
(24.4%). The sentence's reference is the paper's measured bench, so 25% is
the consistent figure. New script gate **BECK-RATIO-BENCH** passes:
computed 1.24928 vs 1.25. The "0.32 bits" is unchanged (bench-derived 0.3211
bits, script-derived 0.3146 bits — both round to 0.32).

### R4-N6 — §4 SEC formula is the ultra-relativistic form, unstated (fixed)
§4 now reads "in the ultra-relativistic limit" before
ε_eff + 3p_eff = 2ε + 2ε_spin > 0, with the non-relativistic form
(ε + 2ε_spin, likewise positive) named in the same clause. Verified by hand:
NR dust p = 0, p_eff = ε_spin, so ε_eff + 3p_eff = ε + 2ε_spin > 0.

### R4-N7 — Zenodo 24113586 contents not re-read in Round 4 (closed — and it changed the paper)
See §2 (R4-R1). This was not a rubber stamp: reading the preprint whole
uncovered a false citation claim.

---

## 2. R4-R1 — the sign-citation error (blocking-grade, found and fixed in this revision)

### What the manuscript claimed
§4 stated that the ultra-relativistic value −(3/16)ħ²n² and the covariant
averages ⟨:s_l s^l:⟩ = +8/3 and +1/8 are "stated in the revision notes of
the earlier version of this work, citing the deposited preprint that
computed them" (\cite{Aldred26}, Zenodo 24113586). Appendix B's sign row
repeated the attribution: "ultra-relativistic −(3/16) and covariant +8/3,
+1/8: Aldred 2026, Zenodo 24113586".

### What the sources actually contain
I read the deposited preprint whole — `paper.md` (498 lines) and
`compute.py` (513 lines) — and grepped every source in the build
(v3, v4 text, v4 changelog, Grok revised texts, ChatGPT manuscript,
the Nov 17 exchange file) for `3/16` and `8/3`:

- **The preprint contains no −3/16, no +8/3, no +1/8 as covariant averages.**
  What it computes is coef(u) = (1/8)·(1/3)[1 + 2A(u)²], coef(0) = 1/8,
  coef(∞) = 1/24, ratio R(∞) = 1/3. Its sign conclusion is the **opposite**
  of what §4 implied: "the exchange term enters with the fermionic minus
  sign; the resulting Fock contribution is positive… The exchange term
  therefore has the sign the bound assumes: it opposes compression"
  (§3.5; `compute.py` sign check: "the spin term is repulsive, as the
  flagship assumes"). The only "3/16" in the preprint is the positive
  Hehl–Datta Wilson coefficient in Hehl and Datta's normalisation (§2.5).
- **−(3/8) is sourced** — the Nov 17 house exchange file gives it by three
  independent methods (Wick/momentum, Wick/position, pair-distribution).
- **−(3/16) is asserted in exactly one place**: the v4 changelog, line 12 —
  "The same calculation shows the normal-ordered spatial spin square is
  negative (−3/8, then −3/16 ħ²n²)." It is a revision-note claim, not a
  preprint result; the changelog does not derive it.
- **+8/3 and +1/8 as covariant averages appear in NO source in the build.**
  No file — preprint, changelog, v3, v4, Grok, ChatGPT, exchange file —
  contains them. They were unsourced numbers.

A referee opening Zenodo 24113586 and searching for −3/16 or 8/3 would find
nothing, and would find the preprint's own conclusion running the other way.
The manuscript's "reported-not-established" label softened the numbers but
did not fix the false citation claim. That is a referee trap, and it had to
go.

### The fix
§4 rewritten (the sign paragraph only; the ratio-1/3 sentences and the
β = 1/3 / 1/12 ratio rows are supported by the preprint and unchanged):

- The house −(3/8) stays, with its provenance (Nov 17 exchange calculation,
  three methods, house file, not deposited).
- The −(3/16) stays **as a revision-note claim**, with the correction stated
  in the same paragraph: the deposited preprint does not contain that value,
  and its own sign conclusion is the opposite — its exchange term is
  positive, the coefficient falling from 1/8 to 1/24 and the spin term
  repulsive, as the bound assumes (\cite{Aldred26} now cites that true claim).
- The +8/3 and +1/8 covariant averages are **removed entirely**. Appendix B
  records the removal and the reason ("no source in the build") so the
  numbers do not silently reappear in a later revision.
- The paragraph now presents **both** evaluations honestly: the house spatial
  calculation gives a negative spin square; the deposited preprint's exchange
  calculation gives a positive one. They average different objects. The
  sign remains unsettled, the full Wigner-function evaluation is still not
  done, and kill condition #2 stands unchanged.

The paper is stronger for this: §4 no longer leans one way on an unsourced
citation, and the sign problem is now stated as a genuine conflict between
two evaluations rather than a one-sided negative result with a borrowed
reference.

---

## 3. Verification after the revision

- `scripts/v5_verify.py`: **94 PASS, 0 FAIL, of 94**, exit 0. New gates:
  T1d-W/B/D/aligned-W/aligned-B/ratio-on-B/ratio-on-W (7),
  SEAM-SEV (1), BECK-RATIO-BENCH (1). One tolerance corrected during the
  run (T1d-W, 1e-3 → 2e-3; see §1, R4-N4). Figures regenerated by the run.
- `scripts/correction_paper_compute_standalone.py`: **75 PASS, 0 FAIL, of 75**,
  exit 0.
- Manuscript cross-check (re-run after all edits): "85 gates" 0 occurrences;
  "94 gates" in both places (conclusion, Appendix B); "second revision" 0;
  "fourth revision" present; "8/3" only on the Appendix B removal-record
  line; all 21 `\cite` keys resolve with zero uncited bibitems and zero
  undefined keys; all 7 labels referenced, zero undefined refs; dollar
  signs even (708); environments balanced (document 1/1, abstract 1/1,
  table 5/5, figure 2/2, equation 9/9, thebibliography 1/1).
- LaTeX compilation still untested — no toolchain on this VM
  (pdflatex/latexmk/xelatex/tectonic/lualatex all absent). Structural check
  above is the substitute; a real compile on a machine with a toolchain is
  the one remaining pre-submission item.
- The §4 rewrite was verified by re-reading the paragraph as printed (§2
  above) and by the primary-source reads that motivated it. No numbers in
  Tables 1–4 changed; no figure changed.

## 4. What remains open

- **LaTeX compile** (checklist A2) — the only blocking pre-submission item.
- **Targeted re-read of §4** — the Round 4 verdict said no re-review was
  needed after the two trivial fixes, but that predates the R4-R1 rewrite,
  which is substantive. A single targeted re-read of the §4 sign paragraph
  against the preprint is the proportionate re-check; a full fifth round is
  not warranted (no numbers changed, no new physics, kill condition
  untouched). Prime's call.
- **The standing open problems** (checklist §C, unchanged): coefficient
  derivation, Dirac evaluation (now stated as a two-sided conflict — see
  §2), junction conditions, 287 journal update (Bill's word only), axis
  pipeline deposit, TOV solver deposit, torsion-scalar derivation, carrier
  at the bound, correction-paper deposit state.
- **Preprint `results.json`** (Zenodo 24113586) was not fetched; `paper.md`
  and `compute.py` were read whole and are sufficient for every claim the
  manuscript makes about the preprint.

## 5. Files changed in this revision

- `aldred-limit-v5.tex` (880 → 886 lines): date line; §4 sign paragraph;
  §4 SEC-formula clause; §8 seam clause; Beck 25%; Appendix B rows
  (Table 1 21 gates, count 13 + 5 supporting, Beck 4 gates, sign row).
- `scripts/v5_verify.py` (+9 gates) and `scripts/v5_verify_results.json`
  (94/94). Figures regenerated by the script run (same content).
- `rounds/PRE-SUBMISSION-CHECKLIST.md`: A1 done; B11 updated (94/94);
  B17 added (R4-R1); §D all six items marked done with dispositions;
  §E summary updated.
- `rounds/ROUND-4-REVISION-REPORT.md`: this file.

No outward sends, deposits, submissions, emails, or approval cards.
No secrets printed. Work stayed inside the build directory.
