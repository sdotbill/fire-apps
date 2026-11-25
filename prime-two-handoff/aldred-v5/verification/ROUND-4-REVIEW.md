# Aldred Limit v5 (third revision) — Round 4 Adversarial Peer Review

**Reviewer:** Round 4 adversarial reviewer (child of the build coordinator).
**Date:** 19 November 2026. **Manuscript:** `aldred-limit-v5.tex` (880 lines).
**Role:** attack, not praise. Final polish round and pre-submission check.
Review only — no file in the build was edited, except that running the
verification scripts regenerated the two figure PNGs and the results JSONs
(the scripts' own behaviour).

## Verdict

**FINAL MINOR REVISION — the manuscript survives on its science and its
arithmetic. It is not yet submittable as it stands, for two trivial
reasons only: the title-page date line is stale ("second revision" for a
third revision), and the LaTeX has still never been compiled.**

There are **0 BLOCKING findings** in the science, the tables, or the
displayed equations. All six Round 3 blocking findings (B1–B6) are fixed
in the corrected text, and I re-verified each one from the corrected text
with my own independent recomputation — not from the script's expected
values. The three items Round 3 ordered re-derived from scratch
(Eq. (7), Table 2 D row, Table 4) all reproduce exactly. The two citation
re-pointings check out against the primaries (the GRG quote is verbatim
from Popławski 2012b; the cusp-bounce sentence is verbatim from the PRD
paper's abstract). The κ notation is clean under grep. The figures are
legible, correctly labelled, and match their captions.

What remains is **7 NON-BLOCKING findings** (one stale date line, one
0.0005-bit seam between two routes to the sever bench, two labelling
nits in Appendix B, one ungated-but-verified column, two one-clause
clarifications) plus the standing open problems, which the paper already
states honestly. None of them requires new physics, new computation, or
another review round on the science. Fix the date line, compile the
LaTeX on a machine with a toolchain, and submit — no re-review is needed
unless compilation surfaces errors.

**Counts: 0 BLOCKING findings, 7 NON-BLOCKING findings, plus the audit.**

---

## 0. What I ran myself (not trusted from Round 3 or the revision report)

| Check | Result |
|---|---|
| `scripts/v5_verify.py` (re-run by me) | **85/85 PASS, exit 0** — confirmed |
| `scripts/correction_paper_compute_standalone.py` (re-run by me) | **75/75 PASS, exit 0** — confirmed |
| Independent recomputation (Decimal, 50-digit, CODATA values typed by me, not imported from `v5_verify.py`) | Table 1 all 7 rows (ρ/n/d), Eq. (7) by direct SI solve, Table 2 all rows, Tables 3–4 all 8 N* values from the thumbnail anchor, Ḣ(W/B), p_F, spacing, Planck gap, torsion scale, r_dS, TOV gap, Beck, 282-cell ratios — **all agree with the printed text** (see §0.1). |
| GRG paper full text (arXiv:1105.6127, read via search) | The §5 Planck-density concession quote is **verbatim** from Popławski 2012b (GRG 44, 1007–1014): "We found that the energy density of matter at the bounce is a few orders of magnitude larger than the Planck energy density. The scenario of a big bounce within the classical ECSK theory may therefore be inadequate because the Planck regime is expected to be described by a quantum theory of gravity." Cite is now `Poplawski12b` ✓. |
| PRD paper abstract/full text (arXiv:1111.4595, read via search) | The §4 cusp sentence is **verbatim** from Popławski 2012 (PRD 85, 107502): "replacing it with a cusp-like bounce at a finite minimum scale factor" and "despite enhancing the energy condition, also averts the big-bang singularity". Cite is now `Poplawski12` ✓. |
| Popławski 2016 text (arXiv:1410.3881, read via search) | s² = (ħcn_f)²/8 for unpolarised fermions, citing [9, 10, 33], and ε_eff = ε − κs²/4, p_eff = p − κs²/4 — confirmed in the 2016 text itself. Round 3 N12 is closed. |
| Aldred 2026 Zenodo 24113586 title | Confirmed in the v4 reference list (`sources/Aldred_Limit_v4_13_j0l7.txt`, ref [18]): "The Spin Coefficient of the Einstein–Cartan Bound: Displaying the Coefficient 1/8 and Computing Its Relativistic Form for a Free Dirac Gas", doi:10.5281/zenodo.24113586 — matches the new `\bibitem{Aldred26}` exactly. The preprint's *contents* were not fetched in this round (see §3, residual gap). |
| Exchange calculation (`sources/EXCHANGE-CALCULATION-2026-11-17.md`) | −(3/8)ħ²n² by three independent methods (Wick/momentum, Wick/position, pair-distribution), all agreeing exactly. Confirmed as stated in §4. |
| Figures (viewed as images) | Fig. 1a: all three annotations legible, no overlap; dashed branch and threshold marker present; axis labels use the scaled Y. Fig. 1b: both maxima and both zeros visible and correctly placed; B curve cut at y = −2 as captioned. See §1.2. |
| LaTeX compile | NOT checked — no toolchain on this VM (`which pdflatex latexmk xelatex tectonic lualatex` all empty). Structural check done instead (§1.3). |
| κ grep (whole .tex) | Every κ is κ², κ_H, or the sentence explaining the convention. No bare κ denotes 8πG/c⁴. See §0.2. |

### 0.1 Independent recomputation results (selection)

Constants typed independently: G = 6.67430×10⁻¹¹, ħ = 1.054571817×10⁻³⁴,
c = 299792458, m_n = 1.67492749804×10⁻²⁷. GeV⁴→g/cm³ conversion done
from scratch via (ħc)³: 1 GeV⁴ = 2.320115×10¹⁷ g/cm³, so the thumbnail
1×10⁻⁴⁷ GeV⁴ = 2.320115×10⁻³⁰ g/cm³ (ms: 2.3201×10⁻³⁰ ✓) and the
measured 5.845×10⁻³⁰ g/cm³ = 2.519271×10⁻⁴⁷ GeV⁴ (ms: 2.5193×10⁻⁴⁷ ✓).

| Quantity | My value | Manuscript | Verdict |
|---|---|---|---|
| Eq. (7), direct SI solve ε(n) = ε_spin(n): W / B / D | 20.25 / 1.265625 / 0.0625 | Eq. (7) 81/(64β²); text 20.25 / 1.265625 / 0.0625 | ✓ — the 4096 is gone in §5 and Appendix A |
| Table 1, all 7 rows ρ_A / n_A / d_A | agree to printed precision on all 21 entries (e.g. W 3.887111×10⁵⁵, B 9.717777×10⁵⁴, D 2.159506×10⁵⁴) | as printed | ✓ |
| Table 2 W: x_SEC / x_max / y_max / x₀ | 5.0625 / 9 / 3 / 20.25 | as printed | ✓ |
| Table 2 B: x_SEC / x_max / y_max / x₀ | 0.31640625 / 0.5625 / 0.1875 / 1.265625 | as printed | ✓ |
| Table 2 D: x_max / y_max / x₀ (algebra) | 0.027777… / 0.009259… / 0.0625 | as printed | ✓ |
| Table 2 D: x_SEC | n/a — no onset (see §0.3) | **n/a** | ✓ fixed |
| Table 3 N*: W / B / rB / rW (measured bench) | 281.775383 / 279.775383 / 281.360346 / 283.360346 | 281.775 / 279.775 / 281.360 / 283.360 | ✓ |
| Table 4 N*: W / B / rB / rW (thumbnail anchor, direct) | 283.108390 / 281.108390 / 282.693352 / 284.693352 | 283.108 / 281.108 / 282.693 / 284.693 | ✓ — from the stated definition, not the old opaque construction |
| Table 4 floors | 284 / 282 / 283 / 285 | as printed | ✓ |
| 282.693 = ratio-on-B; B×3 = ratio-on-B | log₂(rB/thumb) = 282.693352; 3×ρ_A(B) = 2.915333×10⁵⁵ = ρ_A(rB) exactly | §8 as stated | ✓ |
| 84.6219 dex + log₂3 | 282.692830 (vs direct 282.693352; Δ 0.0005 bits — see R4-N2) | 282.693 | ✓ at printed precision |
| D SEC combination at the D zero | ε_eff + 3p_eff = 2ε + 2ε_spin = 4×0.0625 = **0.25** ε_Pl, never 0; ε_eff + p_eff = 4ε/3 = 0.0833 > 0 | §4 as stated; script gate D-SEC-AT-ZERO = 0.25 | ✓ |
| Ḣ(B) / Ḣ(W) | 8.150467×10⁴⁸ / 3.260187×10⁴⁹ s⁻² | 8.1505×10⁴⁸ / 3.2602×10⁴⁹ | ✓ |
| p_F/m_nc: W / B | 1.8533×10¹³ / 1.1675×10¹³ | 1.85×10¹³ / 1.17×10¹³ | ✓ |
| T_A: W / B | 2.693491×10¹⁶ / 1.346746×10¹⁶ m⁻¹ | 2.6935×10¹⁶ / 1.3467×10¹⁶ | ✓ |
| r_dS: B / W | 1.286101×10⁻¹⁶ / 6.430505×10⁻¹⁷ m | 1.286×10⁻¹⁶ / **6.431×10⁻¹⁷** | ✓ — last digit fixed |
| TOV gap (11.71−11.46)/11.46 | 2.1815% | **2.2%** in §3, §9, Appendix B (3 places) | ✓ reconciled |
| 282-cell density / measured: rB / W | 0.6419 (35.8% low) / 0.8558 (14.4% low) | 0.642 (36%) / 0.856 (14%) | ✓ |
| Beck Λ / bits / ratio | 1.362852×10⁻⁵² m⁻² / 0.3211 bits / 1.2493 on the paper's own bench (script: 1.2437) | 1.3628×10⁻⁵² / 0.32 / "about 24%" | ✓ (see R4-N5) |
| ρ_Pl; gap vs B | 5.154849×10⁹³ g/cm³; 5.3046×10³⁸ | 5.1548×10⁹³; 5.30×10³⁸ | ✓ |
| Grid (from results JSON): root / SEC / max rel. err. | 3.7×10⁻⁹ / 6.0×10⁻⁸ / 1.25×10⁻⁵ | §5 "10⁻⁷–10⁻⁸ / 10⁻⁵" | ✓ |
| Fermi gates | rel. tolerance 1×10⁻¹² in script | §5 "better than one part in 10¹² (the gate tolerance)" | ✓ |

### 0.2 κ notation — grep of the whole .tex

Every κ occurrence: L93 κ² = 8πG/c⁴ (definition); L94–96 the sources'
κ renamed κ_H with the explicit sentence "no bare κ in this paper ever
denotes 8πG/c⁴"; L99, L113, L115–116, L154 κ²/4 vs κ²; L108–110 κ_H;
L323 α = (9/16)κ_H. No other κ exists. Round 3 B5 is fixed, including
the two surviving prose collisions (old L106–108, L151) — both now read
in κ²/κ_H form.

### 0.3 Table 2 D row — the physics, checked by hand

With Popławski 2012 Eq. (10), ε̃ = −p̃ = −αn²: p_eff = ε/3 + ε_spin
(UR gas), ε_eff = ε − ε_spin, so ε_eff + 3p_eff = 2ε + 2ε_spin > 0 for
every ε > 0 — no zero, no SEC onset. At the D zero (ε = ε_spin =
0.0625 ε_Pl) the combination is 0.25 ε_Pl and ε_eff + p_eff = 4ε/3 >
0, so no smooth turnaround. The manuscript now states all of this in
§4, marks D x_SEC "n/a" with the stiff-fluid-only table note, restricts
the §5 turnaround proof and the x_SEC landmark to W and B explicitly,
and calls D's 0.0625 ε_Pl an algebraic zero whose bounce, if any, is
the Popławski cusp mechanism. The D x_max/y_max/x₀ entries are correct
as landmarks of the curve y = x − 4x^{3/2} (α = 8β/9 = 4 for D).
Round 3 B3 is fixed in full.

---

## 1. Round 3 blocking findings — disposition (verified from the corrected text)

- **B1 (Eq. (7) wrong by 64×).** FIXED and independently confirmed.
  §5 Eq. (7) and Appendix A both read 81/(64β²). My direct SI solve of
  ε(n) = ε_spin(n) gives 20.25 / 1.265625 / 0.0625 (W/B/D) — exactly
  81/(64β²), and the 4096 form would give 0.316 / 0.0198 / 0.00098.
  The three new EQ7 gates evaluate the printed form itself. No "4096"
  remains in the .tex.
- **B2 (§5 scaled-variable definitions).** FIXED. §5 now defines
  x = ε/ε_Pl, y = ε_eff/ε_Pl, y = x − αx^{3/2}; the scaled curve is
  Y = u(1−√u), u = x/x₀, Y = y/x₀ = ε_eff/(x₀ε_Pl), with the distinct
  symbol Y in text, caption, and figure axis labels
  ("u = epsilon/epsilon_b", "Y = epsilon_eff/epsilon_b"). No ε₀
  remains. The landmarks check: maximum (4/9, 4/27) since
  (4/9)(1−2/3) = 4/27; threshold (1/4, 1/8) since (1/4)(1−1/2) = 1/8.
- **B3 (Table 2 D x_SEC).** FIXED — see §0.3 above.
- **B4 (Table 4 irreproducible).** FIXED by option (a), and verified
  from the definition, not the script. §8 and the Table 4 caption now
  state N* = log₂(ρ_A,row/ρ_L,thumb) with ρ_L,thumb = 1×10⁻⁴⁷ GeV⁴ =
  2.3201×10⁻³⁰ g/cm³ and no per-row repair; the repair (×3) produces
  the ratio-on-B density, so 282.693 sits in the ratio-on-B row and the
  other rows are offsets by log₂ of the density ratio. My direct
  computation from the thumbnail anchor gives 283.108390 /
  281.108390 / 282.693352 / 284.693352 — the printed table to the
  printed precision, with floors 284/282/283/285. The old
  COUNT-SEVER/COUNT-W-SEV gates are gone; COUNT-SEV-W/B/RB/RW derive
  from the thumbnail directly, plus COUNT-THUMB and COUNT-SEV-XCHECK.
- **B5 (κ collision).** FIXED — see §0.2.
- **B6 (Fig. 1a annotations).** FIXED and viewed. See §1.2.

## Round 3 non-blocking findings — disposition (spot-checked)

N1 Popławski 2016 title + DOI added ✓. N2 full page ranges (Cartan
593–595, Popławski 2012b 1007–1014) ✓. N3 D β = 9/2 cites Popławski
2012 alone ✓ (L129; Kerlick kept only where the (3/4)κ form is
discussed). N4 sign numbers cite Aldred 2026, Zenodo 24113586, title
verified against the v4 reference list (§0); normalisation of the
covariant values flagged undocumented; the "ratio is the 1/3 above"
sentence not reintroduced ✓. N5 TOV gap 2.2% in all three places ✓
(§0.1). N6 r_dS(W) = 6.431×10⁻¹⁷ ✓ (§0.1). N7 Fig. 1b ylim (−2, 1.2),
caption notes the cut ✓ (viewed). N8 all seven labels referenced ✓
(structural check: zero unreferenced labels, zero undefined refs).
N9 ρ_KT "in ħ = c = 1 units" ✓. N10 Appendix B Table 2 row reads
"11 gates (UR turnaround: 2 further gates)" ✓. N11 Popławski 2010
erratum noted ✓. N12 Popławski 2016 s² chain confirmed in the 2016
text itself (§0) and Popławski 2010 cited alongside ✓. N13 Trautman
Symposia Mathematica entry kept; the reviser cites Trautman's own
publication list — I did not re-verify that list independently, and it
is a standard, low-risk entry; no change required.

## Round 2 fixes — spot-check that they still hold

Eq. (1) has no /c² (ρ_eff = ρ − κ²⟨S²⟩) ✓; W adoption is stated-choice
language with the s_P = 2S_B mechanism labelled an unrun conjecture ✓;
sign problem in the abstract and as §9 kill condition #2 ✓; UR Ḣ proof
in §5 and Appendix A (W/B) ✓; grid claim matches the results JSON ✓
(§0.1); abstract narrowed to Tables 1–4 with §7 excluded ✓; kill line
30°/15° in §7 and §9 ✓; catalogue numbers cut, Shamir reported as
2.8σ HST / 7.38σ SDSS ✓; rotating-core numbers cut ✓; floor-rule
one-sidedness stated ✓; single measured bench, 36%/14% statements,
±0.026-bit uncertainty ✓; Popławski 2011 as energy scale with leptons
qualifier ✓; correction-paper disclosure complete (Draft status line,
corrected source undeposited, standalone script ≠ deposited script) ✓;
bibliography complete, Kerlick PRD 12, 3004–3006 (1975) with its
conclusion confronted ✓; closed-model threshold defined in §3 (ρ_A/4
dust) and §5 (u = 1/4, Y = 1/8) and marked in Fig. 1a ✓.

---

## 2. NON-BLOCKING FINDINGS (Round 4)

### R4-N1. Title-page date line is stale: "second revision" for a third revision — L10

`\date{19 November 2026\\ Revision 5, second revision --- research draft,
not peer reviewed}`. The Round 3 revision report calls this build the
third revision (880 lines, up from 826), and Round 3's review called the
previous manuscript the second revision. The date line is one revision
behind. **Fix:** "third revision". One word; the only factual error I
found on the title page.

### R4-N2. Two routes to the sever bench differ by 0.0005 bits — §8, Table 4 caption

The manuscript presents the sever bench two ways that are not quite the
same number: the "84.6219-dex gap the earlier papers printed" and the
thumbnail anchor ρ_L,thumb = 1×10⁻⁴⁷ GeV⁴. The dex route gives
84.6219/log₁₀2 + log₂3 = 282.692830 for the ratio-on-B row; the direct
thumbnail route gives log₂(ρ_A(rB)/ρ_L,thumb) = 282.693352 — a 0.0005-bit
difference, because the exact dex gap from the thumbnail anchor is
84.62206, not 84.6219 (the correction paper documents 84.6219 as a
hard-coded literal in the earlier record, and its anchor-implied density
2.321487×10⁻³⁰ vs the thumbnail's 2.320115×10⁻³⁰). Both round to the
printed 282.693, and Table 4 is computed from the thumbnail anchor, so
nothing printed is wrong. **Fix (optional, one clause):** note in §8 or
the caption that 84.6219 dex is the earlier papers' rounded literal and
the table is computed from the thumbnail anchor directly. A referee
recomputing via the dex will land 0.0005 bits away and should not have
to wonder why.

### R4-N3. Appendix B "Tables 3–4 count — Script, 13 gates" undercounts the COUNT gates — Appendix B

The COUNT-prefixed gates in `v5_verify_results.json` total 17, not 13.
The 13 counts only the table-entry gates (4 measured-bench N*, 4
sever-bench N*, 2 density ratios, 3 tolerance verdicts); the 4
supporting gates (COUNT-RHOL-GEV4, COUNT-THUMB, COUNT-SEV-XCHECK,
COUNT-ERR) are not accounted for in that row. The 85-gate total is
correct and every gate passes; this is a labelling ambiguity, not a
miscount. **Fix:** relabel as "13 table-entry gates (+ 4 supporting
gates)" or add the supporting gates to the row.

### R4-N4. Table 1 d_A column is not separately gated — Appendix B, Table 1

The 14 Table 1 gates cover ρ_A and n_A only (7 rows × 2); d_A =
n_A^{−1/3} is determined by n_A and is not itself a gate. I verified
all seven d_A values independently (§0.1) and they are correct.
**Fix (optional):** add 7 d_A gates, or note in Appendix B that d_A is
derived from the gated n_A. Either closes the gap; neither is needed
for the numbers to be right.

### R4-N5. Beck "about 24%" depends on which reference Λ is used — §8

Beck's Λ = 1.362852×10⁻⁵² m⁻². Against the script's reference Λ the
ratio is 1.2437 (24.4%, 0.3146 bits); against Λ derived from the paper's
own measured bench (ρ_Λ = 5.845×10⁻³⁰ g/cm³) it is 1.2493 (24.9%,
0.3211 bits). The manuscript says "about 24% … 0.32 bits", which
matches the script's reference; the bench-derived figure rounds to
25%. The difference is 0.5% and immaterial to the point (Beck lands
closer than the 282 count either way). **Fix (optional):** "about 25%"
or name the reference Λ in the sentence.

### R4-N6. §4's SEC formula is the ultra-relativistic form, unstated — §4

"For D the strong-energy-condition combination is then ε_eff + 3p_eff
= 2ε + 2ε_spin > 0" uses the ultra-relativistic gas pressure p = ε/3
(p_eff = ε/3 + ε_spin for D). In the non-relativistic limit the
combination is ε + 2ε_spin, which is equally > 0, so the conclusion
(no onset, no smooth turnaround) is unaffected in either limit — but
§4 does not say which limit the printed formula is in. **Fix
(optional, one clause):** "in the ultra-relativistic limit" before the
formula, or a footnote that the non-relativistic form is likewise
positive.

### R4-N7. Zenodo 24113586 contents not re-verified in this round — §4, Appendix B

The −3/16 (UR spatial) and +8/3 / +1/8 (covariant) numbers rest on
Aldred 2026, Zenodo 24113586. I confirmed the citation exists in the
v4 reference list with the exact title and DOI the manuscript prints,
and the manuscript honestly labels the numbers reported-not-established
with the covariant normalisation undocumented — which is the correct
posture for submission. I did not fetch or read the Zenodo preprint
itself in this round, so its contents remain unverified by a Round 4
read. A referee may ask for it; the paper's labelling already concedes
the point. No manuscript change required; recorded here so the gap is
not silently inherited.

---

## 3. Reproducibility audit (final)

### 3.1 Script runs (run by me, in the build directory)

- `python3 scripts/v5_verify.py` → **GATES: 85 PASS, 0 FAIL, of 85**,
  exit 0. Figures regenerated by the run.
- `python3 scripts/correction_paper_compute_standalone.py` → **GATES:
  75 PASS, 0 FAIL, of 75**, exit 0.

Gate-coverage note: the three Round 3 coverage holes are now closed in
the script itself — EQ7-W/B/D gate the printed Eq. (7) form,
D-SEC-AT-ZERO gates the D SEC combination (+0.25, never 0), and
COUNT-SEV-W/B/RB/RW derive Table 4 from the thumbnail anchor directly
with COUNT-THUMB and COUNT-SEV-XCHECK as cross-checks. The one
remaining coverage gap is R4-N4 (d_A ungated). The script's gate
tolerances are loose in places (e.g. TORS/RDS at rel 10⁻³–10⁻⁴, which
would have hidden the old r_dS(W) last-digit slip) — but the printed
values were verified against my own 50-digit recomputation, so no
printed number depends on a loose gate.

### 3.2 LaTeX — compilation UNTESTED; structural check

- No toolchain on this VM: `which pdflatex latexmk xelatex tectonic
  lualatex` all return nothing. **Compilation remains untested** (carried
  from Rounds 1–3). This is the one substantive pre-submission item:
  the file must be compiled on a machine with a toolchain before it is
  submitted. Risk looks low — standard packages only
  (amsmath, amssymb, booktabs, graphicx, hyperref, geometry), no exotic
  commands — but "looks low" is not a compile.
- Structural check (by script over the .tex): environments balanced —
  document 1/1, abstract 1/1, table 5/5, figure 2/2, equation 9/9,
  thebibliography 1/1; dollar signs even (696); all 21 `\cite` keys
  resolve to `\bibitem`s with no orphans in either direction; all 7
  `\label`s are `\ref`'d and every `\ref` resolves; both
  `\includegraphics` files exist
  (`figures/fig1a_ur_branch_v5.png`, 151481 bytes;
  `figures/fig1b_dust_v5.png`, 120128 bytes).
- No leftover Round 3 strings: "4096", "epsilon_0", "6.429", "2.4%",
  "0.015625", "77 gates" all absent; "85 gates" in the conclusion and
  Appendix B; "2.2%" in all three TOV places.

### 3.3 Figures (viewed as images, not just confirmed to exist)

- **Fig. 1a** (`fig1a_ur_branch_v5.png`): curve Y = u(1−√u) correct;
  maximum blue dot at (4/9, 4/27) with a legible top-right label;
  closed-model threshold green triangle at (1/4, 1/8) with a long arrow
  from a legible bottom-left label — no overlap with each other or the
  title (Round 3 B6 fixed); bounce root red square at (1, 0) with a
  legible label; dashed formal negative branch past the root, reaching
  Y ≈ −0.42 at u = 1.6 as the formula gives; axis labels use the scaled
  definitions (u = ε/ε_b, Y = ε_eff/ε_b), consistent with §5's Y.
- **Fig. 1b** (`fig1b_dust_v5.png`): B curve y = z(1−z), maximum
  (0.5, 0.25), zero (1, 0); W curve y = z(1−z/4), maximum (2, 1), zero
  (4, 0); legend correct; y-range (−2, 1.2) leaves both maxima clearly
  visible; B curve cut at y = −2 exactly as the caption states
  (Round 3 N7 fixed).

### 3.4 Correction-paper check

The standalone correction script passes 75/75 from its own file, as
claimed. Its key numbers cross-check against the manuscript: sever
repaired N* = 282.6928295535 (dex route) vs the manuscript's direct
282.693352 (thumbnail route) — the 0.0005-bit seam of R4-N2, invisible
at printed precision. The manuscript's disclosure of the correction
paper's status (Draft line still on the deposited file; corrected
source undeposited; standalone script ≠ deposited script) is complete
and accurate.

### 3.5 What Round 4 did NOT verify

- The contents of Zenodo 24113586 (see R4-N7); the TOV solver and its
  2.060 M_⊙ / 11.46 km numbers (carried from the November 18 run, solver
  not deposited — disclosed in the paper); the axis-test pipeline and
  any catalogue numbers (none printed — disclosed); the LaTeX compile
  (no toolchain — see §3.2). None of these is a manuscript error; all
  are disclosed limitations, and all are listed in the pre-submission
  checklist.

## 4. Final word to the coordinator

Round 3 ended with a displayed equation wrong by 64× against its own
table, a table irreproducible from its own caption, and a table row
applying a stiff-fluid formula to a Dirac term of opposite pressure
sign. All three are gone, verified from the corrected text by
independent recomputation — not by trusting the script that let two of
them survive. The κ notation, the two citation re-pointings, the
r_dS(W) last digit, and the TOV 2.2% gap are all fixed and checked
against primaries or my own arithmetic. The figures are legible and
correct. The remaining defects are a stale word on the title page, a
0.0005-bit seam, and labelling nits. Fix the date line, compile the
file, submit it. The paper's verified core — a careful
multi-normalisation computation of a known bound, with its domain, its
sign problem, and its failures stated honestly — is ready for a referee
to attack on its merits rather than its arithmetic.
