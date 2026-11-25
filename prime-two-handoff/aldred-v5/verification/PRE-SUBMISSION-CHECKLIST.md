# Pre-Submission Checklist — Aldred Limit v5 (third revision)

**Date:** 19 November 2026. **Manuscript:** `aldred-limit-v5.tex` (886 lines,
fourth revision — the Round 4 revision).
**Review basis:** `rounds/ROUND-4-REVIEW.md` (verdict: FINAL MINOR REVISION —
0 blocking findings, 7 non-blocking findings) **plus** the Round 4 revision's
own close of R4-N7 (see B17): reading the cited preprint found one
blocking-grade citation error (R4-R1), fixed in the revision.
**Scope of this checklist:** what a journal submission needs. Items are
DONE (with evidence), STILL OPEN, or BLOCKING vs HONEST LIMITATION.
A BLOCKING item must be done before submission. An HONEST LIMITATION is
a genuine open problem that the paper already states plainly; it does not
block submission, but it is a referee's first target and must stay stated.

---

## A. MUST DO BEFORE SUBMISSION (blocking)

| # | Item | Status | Evidence / action |
|---|---|---|---|
| A1 | Fix the stale title-page date line: "Revision 5, second revision" → "fourth revision" (this revision is the fourth: Round 1 build, Round 2 rewrite, Round 3 rewrite, Round 4 polish) | **DONE** | Date line now reads "Revision 5, fourth revision". |
| A2 | Compile the LaTeX on a machine with a toolchain and fix any errors/warnings | **OPEN — never done** | No toolchain on this VM (`pdflatex`, `latexmk`, `xelatex`, `tectonic`, `lualatex` all absent). Round 4 structural check passed instead: environments balanced (document 1/1, abstract 1/1, table 5/5, figure 2/2, equation 9/9, bibliography 1/1); dollar signs even (696); all 21 `\cite` keys resolve with no orphans; all 7 labels referenced and all `\ref`s resolve; both figure files exist. Risk looks low (standard packages only), but a submission requires an actual compile and a PDF proofread. |

---

## B. DONE — verified in Round 4 (with evidence)

| # | Item | Evidence |
|---|---|---|
| B1 | Eq. (7) correct: ε_b/ε_Pl = 81/(64β²) in §5 and Appendix A | Round 4 derived it by direct SI solve of ε(n) = ε_spin(n): 20.25 / 1.265625 / 0.0625 (W/B/D). No "4096" remains. Script gates EQ7-W/B/D pass. |
| B2 | Table 2 D row: x_SEC = n/a, §4 states ε̃ = −p̃ with its consequence, §5 restricts turnaround proof and x_SEC to W/B | Verified from the corrected text and by hand: ε_eff + 3p_eff = 2ε + 2ε_spin = 0.25 ε_Pl at the D zero, never 0; ε_eff + p_eff = 4ε/3 > 0. D x_max/y_max/x₀ (0.027777… / 0.009259… / 0.0625) verified as algebra. Script gate D-SEC-AT-ZERO passes. |
| B3 | Table 4 reproducible from its stated definition | Round 4 recomputed all four N* directly from the thumbnail anchor ρ_L = 1×10⁻⁴⁷ GeV⁴ (converted to g/cm³ from scratch: 2.320115×10⁻³⁰): 283.108 / 281.108 / 282.693 / 284.693, floors 284/282/283/285. §8 and caption state the construction; 282.693 = ratio-on-B and B×3 = ratio-on-B both confirmed. Script gates COUNT-SEV-W/B/RB/RW + COUNT-THUMB + COUNT-SEV-XCHECK pass. |
| B4 | κ/κ_H notation: no bare κ denotes 8πG/c⁴ | Grep of the whole .tex: every κ is κ², κ_H, or the convention sentence. |
| B5 | §5 Planck-density concession quote cited to the GRG paper (Popławski 2012b), not the PRD paper | Quote verified verbatim against Popławski 2012b, Gen. Relativ. Gravit. 44, 1007–1014 (arXiv:1105.6127). Cite is `\cite{Poplawski12b}`. |
| B6 | §4 cusp-bounce sentence cited to the PRD paper (Popławski 2012) | Verified verbatim against Popławski 2012, Phys. Rev. D 85, 107502 (arXiv:1111.4595): "cusp-like bounce at a finite minimum scale factor", "despite enhancing the energy condition". Cite is `\cite{Poplawski12}`. |
| B7 | Aldred 2026 Zenodo 24113586 citation for the −3/16 and +8/3/+1/8 sign numbers | Full title verified against the v4 reference list (`sources/Aldred_Limit_v4_13_j0l7.txt`, ref [18]): "The Spin Coefficient of the Einstein–Cartan Bound: Displaying the Coefficient 1/8 and Computing Its Relativistic Form for a Free Dirac Gas", doi:10.5281/zenodo.24113586. `\bibitem{Aldred26}` matches. (Contents not re-read in Round 4 — see §D.) |
| B8 | r_dS(W) = 6.431×10⁻¹⁷ m | Round 4 recomputation: 6.430505×10⁻¹⁷ m → 6.431 at printed precision. B value 1.286×10⁻¹⁶ m also confirmed. |
| B9 | TOV 2.2% gap in all three places | (11.71−11.46)/11.46 = 2.1815% → 2.2% in §3, §9, Appendix B. |
| B10 | All numbers in Tables 1–4 recompute from CODATA 2018 | Round 4 independent 50-digit recomputation (typed constants, not the script): Table 1 all 7 rows × (ρ, n, d); Table 2 all rows; Tables 3–4 all 8 N* values; plus Ḣ, p_F, spacing, Planck gap, torsion scale, Beck, 282-cell ratios — all agree to printed precision. |
| B11 | Verification scripts pass | `scripts/v5_verify.py`: **94/94 PASS, exit 0** (re-run by the Round 4 revision — 7 new d_A gates, SEAM-SEV, BECK-RATIO-BENCH added). `scripts/correction_paper_compute_standalone.py`: **75/75 PASS, exit 0** (re-run by the Round 4 revision). |
| B12 | Figures legible and matching captions | Viewed as images by Round 4. Fig. 1a: maximum (4/9, 4/27), threshold (1/4, 1/8), root (1, 0) all labelled legibly with no overlap; dashed negative branch present; axis labels use scaled Y. Fig. 1b: B max (0.5, 0.25) / zero (1, 0); W max (2, 1) / zero (4, 0); B curve cut at y = −2 as captioned. |
| B13 | Bibliography complete and verified | All 21 entries cited and defined, no orphans either way (structural check). Titles/pages verified across Rounds 2–4, including Popławski 2016 title + DOI, Cartan 593–595, Popławski 2012b 1007–1014, Popławski 2010 erratum, Kerlick PRD 12, 3004–3006 (1975). |
| B14 | Cross-references consistent | All 7 labels referenced; every `\ref` resolves; no undefined references among those used. |
| B15 | Round 3 non-blocking items N1–N13 closed | Titles, page ranges, D citation, sign-number citation, TOV gap, r_dS, Fig. 1b range, label references, ρ_KT units, Appendix B gate counts, erratum, Popławski 2016 s² chain (confirmed in the 2016 text itself, arXiv:1410.3881), Trautman entry — all verified in Round 4. |
| B16 | Round 2 fixes still holding | Eq. (1) (no /c²), W as stated choice, sign problem in abstract + kill conditions, UR Ḣ proof, grid claim vs results JSON, single measured bench, floor-rule concession, axis kill line 30°/15°, correction-paper disclosure — all spot-checked in Round 4. |
| B17 | **Sign-citation correction (R4-R1, found by closing R4-N7): the §4 attribution of −(3/16), +8/3, +1/8 to the deposited preprint was false** | The Round 4 revision read the preprint whole (Zenodo 24113586, `paper.md` + `compute.py`): it contains no −3/16, no +8/3, no +1/8 as covariant averages, and its own sign conclusion is the opposite (exchange term positive, coefficient 1/8 → 1/24, "the sign the bound assumes"). Provenance now established: −(3/8) is the Nov 17 house exchange file (three methods); −(3/16) is asserted only in the v4 changelog ("The same calculation shows the normal-ordered spatial spin square is negative (−3/8, then −3/16 ħ²n²)"); +8/3 and +1/8 appear in NO source in the build and are removed. §4 rewritten to state both evaluations honestly with the corrected provenance; Appendix B sign row rewritten to match. The sign remains unsettled; kill condition #2 stands. Full evidence in `rounds/ROUND-4-REVISION-REPORT.md`. |

---

## C. STILL OPEN — standing open problems (honest limitations, stated in the paper)

These do **not** block submission: the paper states each one plainly, with
its consequences. They are what a referee will press on, and they are the
research programme after submission — not pre-submission fixes.

| # | Open problem | Where the paper states it | What would close it |
|---|---|---|---|
| C1 | **Coefficient derivation** — β is unresolved (W = 1/4 adopted as a stated choice; B = 1 is the literature value; factor of four unresolved) | §2, §9, abstract | A derivation fixing β from the two papers' spin-tensor normalisations (the s_P = 2S_B mechanism is recorded as an unrun conjecture). A β = 1 derivation rescales the bound ×4 and moves the count to N* = 279.775 (fails tolerance); β = 9/2 removes the smooth bounce. |
| C2 | **Dirac evaluation** — the sign of the spin-squared term is not established; a negative sign removes the bounce entirely | §4, abstract, §9 kill condition #2 | A Wigner-function evaluation of the spin-squared average in a degenerate Dirac gas. The −3/8 / −3/16 / +8/3 / +1/8 numbers are reported house calculations, not established results. |
| C3 | **Junction conditions** — no black-hole interior bounce, baby universe, or rotating-progenitor claim can be made without them | §3, §9 | A bounced interior matched to an exterior black-hole spacetime. |
| C4 | **287 journal update** — the journal manuscript still states 287 for the count; the corrected bench gives 281.36 on the ratio-on-B row | §8, §9 | Bill's word only. Draft update written and held, not sent. |
| C5 | **LaTeX compilation** | Appendix B | Compile on a machine with a toolchain (see A2 — the only open item that is blocking rather than a stated limitation). |
| C6 | **Axis-test pipeline deposit + DESI Legacy Survey refit** | §7, §9 | Deposit the pipeline; run the refit under the registered 30°/15° kill line. No catalogue numbers are printed until then (correctly withheld). |
| C7 | **TOV solver deposit + the 2.2% radius gap** | §3, §9, Appendix B | Deposit the solver; explain the 2.18% gap (11.46 km vs an independent 11.71 km run). Numbers carried from the November 18 run. |
| C8 | **Torsion-scalar derivation** — §6's T_A formula is verified arithmetic, derivation outstanding | §6, §9, Appendix B | Derive T_A = m_n c/(ħ√coef) from the Cartan tensor. |
| C9 | **Carrier at the bound** — neutrons do not survive to the bound (spacing 1.5×10¹³ times smaller than the proton charge radius; p_F/m_nc ~ 10¹³) | §3, §9 | A deconfined phase whose spin survives to the bound, or a quantum treatment of the spin-torsion coupling. |
| C10 | **Correction-paper deposit state** — deposited file still carries its "Draft — pending verification before deposit" status line; corrected source undeposited; the 75-gate standalone script is not the deposited script | §8, Appendix B | Deposit the corrected source (Bill's word only). Disclosed in the paper; do not present the correction as a clean deposited record until then. |

---

## D. MINOR ITEMS — all fixed in the Round 4 revision

| # | Item | Disposition |
|---|---|---|
| D1 | 84.6219-dex vs thumbnail-anchor routes to the sever bench differ by 0.0005 bits (exact dex from the thumbnail is 84.62206). | **DONE.** §8 now notes 84.6219 dex is the earlier papers' rounded literal, the exact gap is 84.62206 dex, the routes differ by 0.0005 bits, and the table is computed from the anchor directly. New script gate SEAM-SEV passes (0.0005227 bits). |
| D2 | Appendix B "Tables 3–4 count — Script, 13 gates" counts only table-entry gates; 4 supporting COUNT gates unlisted. | **DONE.** Row now reads "13 table-entry gates (+ 5 supporting gates)" — the fifth is the new SEAM-SEV gate. |
| D3 | Table 1 d_A column is not separately gated (14 gates cover ρ_A and n_A only). | **DONE.** 7 new T1d-* gates added; all pass. Appendix B Table 1 row now reads "21 gates". |
| D4 | Beck "about 24%": 24.4% against the script's reference Λ, 24.9% against Λ from the paper's own measured bench. | **DONE.** Text now says "about 25% above the measured value" (bench-derived ratio 1.2493). New script gate BECK-RATIO-BENCH passes (1.24928). |
| D5 | §4's ε_eff + 3p_eff = 2ε + 2ε_spin is the ultra-relativistic form (p = ε/3); the non-relativistic form (ε + 2ε_spin) is equally > 0. | **DONE.** §4 now says "in the ultra-relativistic limit" before the formula, with the non-relativistic form named as likewise positive. |
| D6 | Zenodo 24113586 contents not re-read in Round 4 (citation verified against the v4 reference list; numbers labelled reported-not-established). | **DONE — and it changed the paper.** The Round 4 revision read the preprint whole (`paper.md`, 498 lines, + `compute.py`, 513 lines). It does NOT contain −3/16, +8/3, or +1/8, and its sign conclusion is the opposite of what §4 implied. See B17 / R4-R1. |

---

## E. SUBMISSION READINESS — summary (updated by the Round 4 revision)

- **Blocking before submission:** 1 item (A2 LaTeX compile — never done on
  this VM, no toolchain; standard packages only, structural check clean).
  A1 is done. No new science and no further review round is required by
  the Round 4 verdict, but note the R4-R1 correction (B17): the §4 sign
  paragraph was substantively rewritten in this revision on primary-source
  evidence — a targeted re-read of §4 alone is the one re-check Prime may
  want before submission.
- **Verified done:** 17 items (§B), including every number in Tables 1–4
  recomputed independently, both scripts passing (94/94 and 75/75),
  both figures viewed and correct, all citations and cross-references
  resolving, and the sign-citation correction (B17).
- **Honest limitations (do not block):** 10 standing open problems (§C),
  all stated in the paper with their consequences, including the two
  that would kill the bounce (negative Dirac sign; coefficient fixed at
  9/2) and the two that depend on Bill's word alone (287 journal
  update; correction-paper deposit).
- **Minor:** 6 items (§D), all fixed in this revision.
