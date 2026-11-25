# Aldred Limit v5 (second revision) — Round 3 Adversarial Peer Review

**Reviewer:** Round 3 adversarial reviewer (child of the build coordinator).
**Date:** 19 November 2026. **Manuscript:** `aldred-limit-v5.tex` (826 lines).
**Role:** attack, not praise. Review only — no file in the build was edited, except
that running the verification scripts regenerated the two figure PNGs and the
results JSONs (the scripts' own behaviour).

## Verdict

**MAJOR REVISION — the manuscript does NOT survive as a submission-ready paper.**

The verified core is still real: the dust bound in W/B, the W/B ultra-relativistic
landmarks, the measured-bench vacuum count (Table 3), and the 77-gate script all
recompute correctly under my own independent recomputation. The Round 2 revision
genuinely fixed most of Round 2: Eq. (1), the W adoption, the sign problem in the
abstract and kill conditions, the UR turnaround proof, the grid claim, the axis
section, the rotating-core cut, the floor-rule concession, the single bench, the
Popławski 2011 correction, the correction-paper disclosure, the bibliography, and
the closed-model threshold definition all hold (see §0.4).

But this revision introduces — or leaves — three errors in the paper's own
displayed mathematics, each of which a referee who does the arithmetic will catch
on sight:

1. **Eq. (7) is wrong by a factor of 64** (§5, L337; repeated Appendix A, L699).
   It prints ε_b/ε_Pl = 81/(4096β²); the correct value, proved by direct SI solution
   and printed three lines later in the same paragraph, is 81/(64β²). The paper
   contradicts itself inside one paragraph.
2. **Table 4 (sever bench) cannot be reproduced from its own stated definition.**
   The caption says "84.6219 dex … plus the repair log₂3"; applying that per row
   gives values 1.585 bits higher on every row than printed. The printed table is
   log₂(ρ_A/anchor-ρ_L) with the repair baked only into the ratio-on-B base — a
   construction the manuscript never states. The verification script encodes the
   same opaque construction, so its gates pass circularly.
3. **Table 2's D row prints an x_SEC that does not exist for D.** For the Dirac
   term ε̃ = −p̃ (Popławski 2012, Eq. 10), ε_eff + 3p_eff = 2x + 2αx^{3/2} > 0
   always — there is no SEC onset for D, and the §5 turnaround proof fails for D.
   The manuscript dropped the p̃ = −ε̃ fact that v4 documented explicitly, and
   with it the warning that the UR formula does not apply to D.

Add to those the surviving κ-notation collision in §2 (Round 2 B1's "re-check every
κ" was not done) and a Figure 1a whose two top annotations overlap each other and
the title into illegibility, and the paper is not submittable. None of this requires
new physics; all of it requires correcting displayed equations and tables against
the paper's own numbers. That is major revision, not a rewrite — but it is major,
and Round 4 must re-verify the three corrected tables/equations from scratch, not
from the script's expected values.

**Counts: 6 BLOCKING findings, 13 NON-BLOCKING findings, plus the audit.**
Blocking = must be fixed before any submission. Non-blocking = real defects a
referee could raise.

---

## 0. What I ran myself (not trusted from Round 2 or the revision report)

| Check | Result |
|---|---|
| `scripts/v5_verify.py` (re-run by me) | **77/77 PASS, exit 0** — confirmed |
| `scripts/correction_paper_compute_standalone.py` (re-run by me) | **75/75 PASS, exit 0** — confirmed |
| Independent recomputation (Decimal, 50-digit, typed from CODATA values, not from `v5_verify.py`) | Table 1 (all 7 rows, ρ/n/d), Ḣ(W/B), p_F, spacing, Planck gap, Table 2 W/B landmarks, Table 3 (all 4 rows), 36%/14% density ratios, Beck, torsion scale, ρ_KT — **all agree** (see §0.1). **Table 4 disagrees with its stated definition by exactly 1.585 bits on every row** (see B4). **Eq. (7) disagrees with Table 2 by a factor of 64** (see B1). |
| Popławski 2010 ar5iv full text (read directly) | Eq. (8): ε_eff = ε − κs²/4, p_eff = p − κs²/4, κ = 8πG/c⁴; Eq. (9): s² = ½s_ij s^ij > 0; Eq. (13): s² = (1/8)(ħcn)². The Hehl/W form and the ⅛ average are confirmed against the primary. See §0.2. |
| Popławski 2012 PRD 85, 107502 ar5iv full text (read directly) | Eq. (10): ε̃ = −p̃ = −αn², α = (9/16)κ; ⟨s²⟩ = (3/4)n²; "Dirac spinors coupled to torsion enhance the energy condition"; cusp-like bounce. Confirms the D-row physics that v5 omits. See §0.3. |
| Kerlick 1975 abstract (APS) | PRD 12, 3004–3006; "repulsive between Dirac particles whose spins are aligned and attractive when spins are opposed"; "spin-spin interaction enhances rather than opposes singularity formation". §4's paraphrase is accurate. |
| Bibliography pass (7 entries Round 2 did not verify) | Cartan 1922 ✓, Hehl 1976 ✓, Popławski 2010 ✓, Popławski 2012 (GRG) ✓, Popławski 2016 ✓ (details, but bibitem lacks a title), Popławski 2019 ✓, CODATA 2018 ✓. See §3. |
| Figures (viewed as images) | Fig. 1a: dashed branch and threshold marker present, **but the two top annotations overlap each other and the title** (see B6). Fig. 1b: curves and markers correct; y-range compresses the maxima (see N7). |
| LaTeX compile | NOT checked — no toolchain on this VM (`which pdflatex latexmk xelatex tectonic` all empty). Structural check done instead (§4). |

### 0.1 Independent recomputation results (selection; full table in §2)

Constants (CODATA 2018, typed independently): G = 6.67430×10⁻¹¹,
ħ = 1.054571817×10⁻³⁴, c = 299792458, m_n = 1.67492749804×10⁻²⁷,
m_e = 9.1093837015×10⁻³¹, α = 7.2973525693×10⁻³.

| Quantity | My value | Manuscript | Verdict |
|---|---|---|---|
| W ρ_A (β=1/4) | 3.887111×10⁵⁵ g cm⁻³ | 3.8871×10⁵⁵ | ✓ |
| B ρ_A (β=1) | 9.717777×10⁵⁴ | 9.7178×10⁵⁴ | ✓ |
| D ρ_A (β=9/2) | 2.159506×10⁵⁴ | 2.1595×10⁵⁴ | ✓ |
| All Table 1 n_A, d_A (7 rows) | agree to printed precision | — | ✓ |
| Ḣ(B) / Ḣ(W) | 8.150467×10⁴⁸ / 3.260187×10⁴⁹ s⁻² | 8.1505×10⁴⁸ / 3.2602×10⁴⁹ | ✓ |
| p_F/m_nc: W / B | 1.8533×10¹³ / 1.1675×10¹³ | 1.85×10¹³ / 1.17×10¹³ | ✓ |
| UR balance ε_b/ε_Pl, B / W / D (direct SI solve) | 1.265625 / 20.25 / 0.0625 | 1.265625 / 20.25 / 0.0625 (§5 text, Table 2) | ✓ — **but Eq. (7) prints 81/(4096β²) = 0.01978 / 0.316 / 0.000977** (B1) |
| Table 3 N*: W / B / rB / rW | 281.7754 / 279.7754 / 281.3603 / 283.3603 | 281.775 / 279.775 / 281.360 / 283.360 | ✓ |
| 282-cell density / measured: rB / W | 0.6419 (35.8% low) / 0.8558 (14.4% low) | 0.642 (36%) / 0.856 (14%) | ✓ |
| Table 4 N* **from the caption's definition** (84.6219 dex + log₂3 per row) | W 284.693 / B 282.693 / rB 284.278 / rW 286.278 | W 283.108 / B 281.108 / rB 282.693 / rW 284.693 | ✗ **−1.585 bits on every row** (B4) |
| Beck Λ / ratio / bits | 1.362852×10⁻⁵² m⁻² / 1.2437 / 0.3146 | 1.3628×10⁻⁵² / ~24% / 0.32 | ✓ |
| T_A: W / B | 2.693491×10¹⁶ / 1.346746×10¹⁶ m⁻¹ | 2.6935×10¹⁶ / 1.3467×10¹⁶ | ✓ |
| r_dS: B / W | 1.2861×10⁻¹⁶ / 6.4305×10⁻¹⁷ m | 1.286×10⁻¹⁶ / 6.429×10⁻¹⁷ | ⚠ W last digit (N6) |
| ρ_KT (W) | 1.675395×10⁷⁴ eV⁴ | 1.675×10⁷⁴ | ✓ |
| Planck gap ρ_Pl/ρ_A(B) | 5.3045×10³⁸ | 5.30×10³⁸ | ✓ |
| Spacing B / 0.84 fm ratio | 5.5651×10⁻²⁹ m / 1.509×10¹³ | 5.57×10⁻²⁹ / 1.5×10¹³ | ✓ |
| TOV gap from printed 11.46 / 11.71 km | 2.18% | §3/§9 "2%", App. B "2.4%" | ⚠ App. B wrong (N5) |

### 0.2 Hehl / Popławski 2010 — verification against the primary source

Source read: ar5iv of Popławski, Phys. Lett. B **694**, 181–185 (2010)
(arXiv:1007.0587).

- Eq. (1): Einstein equations with κ = 8πG/c⁴ — confirmed (Popławski's κ).
- Eq. (3): Cartan equations S = −½κs — confirmed.
- Eq. (8): G^ij = κ(ε − ¼κs²)u^i u^j − κ(p − ¼κs²)(g^ij − u^i u^j) —
  i.e. ε_eff = ε − κs²/4, p_eff = p − κs²/4, confirmed, citing HHK.
- Eq. (9): s² = ½s_ij s^ij > 0 — confirmed.
- Eq. (13): s² = (1/8)(ħcn)² for unpolarised fermions — confirmed.
- Conversion to the manuscript's form: (κ_H/4)·s² with κ_H = 8πG/c⁴ gives a
  spin energy density πGħ²n²/(4c²); dividing by c² gives the mass-density
  correction πGħ²n²/(4c⁴) = (κ²/4)⟨S²⟩ in the manuscript's notation
  (κ² = 8πG/c⁴, ⟨S²⟩ = ħ²n²/8). **The arithmetic is right; the notation is
  not** — see B5. The manuscript's κ and Hehl/Popławski's κ are different
  objects with the same letter.
- The ⅛ average is also given in Popławski 2012 (see §0.3): s² = ½s_ik s^ik
  = (1/8)n² for the spin fluid (natural units).

### 0.3 Popławski 2012 (PRD) — verification against the primary source

Source read: ar5iv of Popławski, Phys. Rev. D **85**, 107502 (2012)
(arXiv:1111.4595).

- Eq. (9): T_ik + U_ik = (GR part) + (3/4)κ s^l s_l g_ik, "found by Kerlick"
  — confirmed.
- Eq. (10): **ε̃ = −p̃ = −αn², α = (9/16)κ**, with ⟨s²⟩ = (3/4)n² —
  confirmed. The Dirac correction's pressure is the **negative** of its
  energy density: p̃ = +αn² while ε̃ = −αn². This is the opposite sign
  structure from the spin fluid (ε̃ = p̃ = −¼κs²).
- Text: "In contrast to spin fluids, Dirac spinors coupled to torsion
  enhance the energy condition for the formation of singularities" —
  confirmed; §4's paraphrase is accurate.
- Text: "the minimal coupling … despite enhancing the energy condition,
  also averts the big-bang singularity" with a "cusp-like bounce at a
  finite minimum scale factor" — confirmed; §4's account is accurate.
- Consequence for this paper (see B3): with p̃ = −ε̃, the UR-branch
  combinations for D are ε_eff + p_eff = 4ε/3 > 0 and
  ε_eff + 3p_eff = 2ε + 2ε_spin > 0 at the D zero — no smooth turnaround,
  no SEC onset. v4 documented this; v5 dropped it.

### 0.4 Round 2 fixes — verified as holding (spot-check, not trusted)

Fixed and holding: B1 Eq. (1) (now ρ_eff = ρ − κ²⟨S²⟩, no /c² — **but** see B5
for the surviving prose collision); B2 adoption reverted to v4's stated-choice
language with the s_P = 2S_B mechanism labelled an unrun conjecture; B3 sign
problem in the abstract and as §9 kill condition #2; B4 UR Ḣ proof present in
§5 and Appendix A (for W/B — see B3 for D); B5 grid claim now matches the
results file (root ~10⁻⁸, SEC ~10⁻⁷, max ~10⁻⁵); B7 abstract narrowed to
Tables 1–4 with §7 excluded; B8 kill line 30°/15° stated in §7 and §9,
catalogue numbers cut, Iye gone, Shamir reported accurately (2.8σ HST /
7.38σ SDSS — verified, §3); B9 rotating-core numbers cut; B10 floor-rule
one-sidedness stated ("283, 300, or any larger integer would also pass"),
abstract gives the full pattern, both rules tabulated on both benches;
B11 single measured bench (5.845×10⁻³⁰ g cm⁻³ = 2.5193×10⁻⁴⁷ GeV⁴),
36%/14% density statements present, N* uncertainty ±0.026 stated;
B12 Popławski 2011 quoted correctly as an energy scale with the leptons
qualifier; B13 "drafted, not adopted" quotation gone; B14 correction-paper
disclosure complete (Draft status line, corrected source undeposited,
standalone script ≠ deposited script); B15 bibliography filled, Kerlick now
PRD 12, 3004–3006 (1975) with its conclusion confronted in §4; B16 sign
numbers labelled reported-not-established and the D dismissal rewritten on
Kerlick vs Popławski 2012 (cusp as expected shape, not a disqualifier);
B17 closed-model threshold defined in §3 (ρ_A/4 dust) and §5 (u = 1/4,
y = 1/8) and marked in Fig. 1a. Non-blocking N1–N18: N1, N2, N3, N4, N5, N6,
N7, N8, N9, N10, N11, N12, N13, N14, N15 (in part — see §3), N16, N17, N18
all addressed in the rewrite as claimed, except N18 (LaTeX still uncompiled)
and the residual items listed under Non-blocking findings below.

---

## BLOCKING FINDINGS

### B1. Eq. (7) is wrong by a factor of 64, and the paper contradicts itself inside one paragraph — §5, L337–343; Appendix A, L699

Eq. (7) (L337) reads ε_b/ε_Pl = 81/(4096β²). Three lines later (L340–343) the
same paragraph states the balance is 1.265625 ε_Pl on B, 20.25 ε_Pl on W and
0.0625 ε_Pl on D. Those three numbers are 81/(64β²), not 81/(4096β²):
81/4096 = 0.01978 on B, 0.316 on W, 0.000977 on D — a factor of 64 smaller on
every row. Table 2 (L428–431) prints the 81/(64β²) values, so Eq. (7)
contradicts Table 2 as well as its own paragraph.

I derived it independently from the stated inputs, in SI units (see §0.1):
ε(n) = (3/4)ħc(3π²)^{1/3}n^{4/3}, ε_spin = βπGħ²n²/c²; setting them equal
gives ε_b/ε_Pl = 20.25 (W), 1.265625 (B), 0.0625 (D) — exactly 81/(64β²).
The coefficient check also confirms it: with x = ε/ε_Pl, the spin term is
αx^{3/2} with α = 8β/9 (verified numerically: the coefficient is 0.88888… =
8/9 for β = 1), so the root is x₀ = 1/α² = 81/(64β²). The 4096 (= 64²) in
Eq. (7) looks like a squaring error on the 64.

Appendix A (L699) repeats the wrong formula verbatim ("ε_b/ε_Pl =
81/(4096β²), Eq. (7)").

**Why this survived a 77/77 script pass:** no gate in `v5_verify.py` tests
Eq. (7)'s 81/(4096β²) form. The script gates the landmarks 81/(64β²)
(`UR-*-x0`) and the Fermi balance (1.265625 / 20.25) — both correct — but
never the equation as printed. The script verifies the tables, not the
displayed equations.

**Exact change required:** replace 4096 with 64 in Eq. (7) (L337) and in
Appendix A (L699); add a script gate that evaluates the printed Eq. (7)
form itself against the Table 2 x₀ values. Round 4 must re-derive Eq. (7)
from ε(n) = ε_spin(n) independently, not from the script's expected values.

### B2. §5's scaled-variable definitions are wrong: ε₀ is not "the zero", and y is used for two different normalisations — §5, L354–365; Fig. 1a caption, L376–380

L354: "Let x = ε/ε₀ where ε₀ is the zero of the effective density, and let
y = ε_eff/ε₀." If ε₀ were the zero, the zero would sit at x = 1. Table 2
gives the zero at x₀ = 81/(64β²) (20.25 on W, 1.265625 on B) — so x is in
units of ε_Pl, not of the zero, and ε₀ here can only mean ε_Pl. The
sentence as written is false, and it contradicts Table 2's caption
("landmarks, in units of the Planck energy density ε_Pl").

L363–365 then claims: "In scaled variables the curve is the same for every
β: y = u(1−√u) with u = x/x₀, maximum (4/9, 4/27), root (1, 0)." With y
defined two sentences earlier as ε_eff/ε₀ (= ε_eff/ε_Pl), this is false by
a factor of x₀: y = x − αx^{3/2} gives, at u = 4/9, y = x₀·(4/27), not
4/27. The curve y = u(1−√u) is the curve of the **differently normalised**
quantity Y = ε_eff/(x₀ε_Pl) — i.e. ε_eff divided by the balance (zero)
density. v4 had this right ("in the scaled variables u = x/x₀,
y = ε_eff/(x₀ε_P) every curve is y = u(1−√u)"); v5 dropped the x₀ factor
from the definition while keeping the scaled formula, and mislabelled ε₀
as "the zero" in the same move. Figure 1a plots the scaled curve
(maximum 4/27, root (1, 0)) and its caption repeats the scaled formula, so
the figure and the §5 definitions disagree about what y is.

**Exact change required:** rewrite L354–365 as: x = ε/ε_Pl, y = ε_eff/ε_Pl,
y = x − αx^{3/2}; then define the scaled variable Y = ε_eff/(x₀ε_Pl) =
u(1−√u), u = x/x₀, and use a distinct symbol (Y, not y) for it in the text,
the figure caption, and the figure axis label. The figure's y-axis label
currently reads "y = epsilon_eff / epsilon_0", which inherits the same
confusion — relabel it with the scaled definition.

### B3. Table 2's D row prints an x_SEC that does not exist for D, and §4/§5 omit the p̃ = −ε̃ fact that makes it so — §4, L302–316; §5, L340–343, L354–372; Table 2, L430

Table 2 prints for D (β = 9/2): x_SEC = 0.015625, x_max = 0.027777…,
y_max = 0.009259…, x₀ = 0.0625. The x₀, x_max and y_max entries are correct
as landmarks of the **effective-density curve** ε_eff(x) = x − αx^{3/2}
(α = 4 for D). But x_SEC is not a landmark of D at all. The SEC combination
is computed with the pressure, and for the Dirac term the pressure
correction has the opposite sign from the energy correction:
Popławski 2012, Eq. (10), ε̃ = −p̃ = −αn² (verified against the primary,
§0.3). So for D, p_eff = ε/3 + ε_spin (not ε/3 − ε_spin), and

ε_eff + 3p_eff = (x − αx^{3/2}) + 3(x/3 + αx^{3/2}) = 2x + 2αx^{3/2} > 0

for every x > 0: the combination never vanishes, so there is no SEC onset
for D. The printed 0.015625 is the value the **stiff-fluid** formula
81/(256β²) would give — it is not a property of the D row. Likewise the §5
turnaround proof ("p_eff = −2ε/3, ε_eff + p_eff = −2ε/3 < 0, so Ḣ > 0")
fails for D: at the D zero, ε_eff + p_eff = 0 + (ε/3 + ε) = 4ε/3 > 0, so
Ḣ < 0 in the smooth sense. Popławski's D bounce is a cusp reached through
the non-monotonic a(T) relation (his Eqs. 15–17), not through the §5
three-line proof.

v4 documented both halves of this explicitly: "the ultra-relativistic
formula of Section 5, which assumes p̃ = ε̃, does not apply to it" and
"at the zero of ρ_eff one has H = 0 but ρ_eff + 3p_eff/c² = +3αn²/c² > 0,
so ä < 0: the scale factor cannot turn round smoothly there". v5 dropped
both sentences. §4 now says only that D is not adopted because "the sign
is open, and which spin tensor the field equations take is open" — true,
but it omits the established, published fact (p̃ = −ε̃) that already
removes the smooth bounce for D on either sign reading of the spatial
average. The §5 text ("on D it is 0.0625 ε_Pl, but D is an algebraic zero
only, as Section 4 explains") points at an explanation Section 4 does not
contain.

**Exact change required:** (i) in Table 2, delete the D x_SEC entry (mark it
n/a or "no onset") and add a table note that the SEC column is the
stiff-fluid (W/B) combination only; (ii) in §4, state Popławski 2012 Eq. (10),
ε̃ = −p̃, and its consequence (ε_eff + 3p_eff > 0 at the D zero, no smooth
turnaround); (iii) in §5, restrict the turnaround proof and the x_SEC
landmark to W and B explicitly, and state that D's 0.0625 ε_Pl is an
algebraic zero of ε_eff whose bounce, if any, is the cusp mechanism of
Popławski 2012, not the §5 proof. The script's `UR-D-x0` gate (which gates
only x₀) does not cover this — add a gate asserting the D SEC combination
has no zero, or remove the D row from the landmark table.

### B4. Table 4 does not follow from its stated definition: every printed N* is 1.585 bits below the value the caption defines — §8, L525–530; Table 4 caption, L571–573; Table 4, L579–582

§8 defines the sever bench as "a gap of 84.6219 dex built on the thumbnail
1×10⁻⁴⁷ GeV⁴" and states "the repair that the correction paper makes is to
multiply ρ_A by exactly 3, adding log₂3 = 1.585 bits". Table 4's caption
repeats it: "84.6219 dex … plus the repair log₂3 = 1.585 bits." Applying
that definition per row — N* = log₂(3ρ_A,row / ρ_L,thumb), with
ρ_L,thumb = 1×10⁻⁴⁷ GeV⁴ = 2.3201×10⁻³⁰ g cm⁻³ — gives:

| Row | From the caption's definition | Printed | Difference |
|---|---|---|---|
| W | 284.693 | 283.108 | −1.585 |
| B | 282.693 | 281.108 | −1.585 |
| Ratio on B | 284.278 | 282.693 | −1.585 |
| Ratio on W | 286.278 | 284.693 | −1.585 |

(My independent computation, §0.1; floors under the caption's definition
would be 285 / 283 / 284 / 286, not 284 / 282 / 283 / 285. The tolerance
verdicts do not flip — all four still Fail — but every number in the table
moves.)

What the printed table actually is: log₂(ρ_A,row / ρ_L,anchor) with
ρ_L,anchor = 2.321×10⁻³⁰ g cm⁻³ (the thumbnail-implied density), i.e. the
84.6219-dex gap **without** any per-row repair. The single number 282.693
is the correction paper's "sever, repaired" requirement — but in the
correction paper that number belongs to one density only: the repaired
density 2.916×10⁵⁵ g cm⁻³, which is numerically the ratio-on-B density
(B × 3 = ratio-on-B, since 1/(1/3) = 3). The printed table is that single
number offset by log₂ of the density ratio from the ratio-on-B row. The
manuscript never states that construction, never states that 282.693 is
anchored to the ratio-on-B row, and never mentions the B×3 = ratio-on-B
coincidence that makes the two readings differ by exactly log₂3. A referee
who recomputes Table 4 from the caption — the only definition the paper
gives — gets a different table.

**Why this survived a 77/77 script pass:** the script encodes the same
opaque construction (`nstar_sever = 84.6219/log10(2) + log(3)/LOG2`,
then `nstar_W_sev = nstar_sever + log(4/3)/LOG2`) and gates Table 4's
printed values against it. The gates verify the table against itself, not
against the thumbnail density. No gate computes Table 4 from
ρ_L,thumb = 1×10⁻⁴⁷ GeV⁴.

**Exact change required:** either (a) restate the definition so it
generates the printed table — e.g. "the sever bench's repaired requirement
is 282.693 for the repaired (ratio-on-B) density; other rows are offset by
log₂(ρ_A,row/ρ_A,ratio-on-B)" — and fix the caption accordingly, with a
script gate deriving each Table 4 entry from the correction paper's single
repaired number; or (b) recompute Table 4 per the caption as written
(values above) and correct the floors. Either way, add a script gate that
derives Table 4 from ρ_L,thumb directly, so the definition and the table
cannot drift apart again. Note for Round 4: the same B×3 = ratio-on-B
coincidence means the "repair" language is a standing trap in this section
— any future edit must say which density the repair is applied to.

### B5. The κ-notation collision Round 2 B1 ordered fixed still survives in §2 — §2, L106–108, L151

Round 2 B1 required: "rewrite the §2 prefactor sentences to use κ²/4 vs κ²
throughout; re-check every later κ in §§2–6 for the same collision." Eq. (1)
is fixed (ρ_eff = ρ − κ²⟨S²⟩, κ² = 8πG/c⁴, L93–97) and L110–113 correctly
use κ²/4 against κ². But L106–108 still write, of Hehl/Popławski, "with the
same coupling κ = 8πG/c⁴" — in the manuscript's own notation κ = √(8πG)/c²,
not 8πG/c⁴; the quantity 8πG/c⁴ is the manuscript's κ², and Hehl's κ. And
L151 still says Hehl et al. give the density and pressure "with the κ/4
prefactor" — "κ/4" is correct in Hehl's notation and wrong in the
manuscript's (the manuscript's form is κ²/4). A reader has to know, sentence
by sentence, which κ is meant. The arithmetic underneath is right (§0.2),
so this is a notation defect, not a numerical one — but it is exactly the
defect Round 2 B1 was written to kill, and a referee doing the dimensional
check that caught the old Eq. (1) will trip on it again.

**Exact change required:** pick one convention for the whole paper and use
it in every sentence: either rename the Hehl/Popławski coupling κ_H
("Hehl writes ε_eff = ε − κ_H s²/4 with κ_H = 8πG/c⁴ = κ² in this paper's
notation") or rewrite L106–108 and L151 in κ²/4 form. Grep every κ in the
.tex after the fix and confirm no bare κ denotes 8πG/c⁴ anywhere.

### B6. Figure 1a's top annotations overlap each other and the title — figures/fig1a_ur_branch_v5.png

Round 2 B6 is fixed in substance: the dashed negative continuation past
the root is now plotted, and the closed-model threshold marker (green
triangle at (1/4, 1/8)) is present. But the regeneration introduced a new
defect: the two top annotations — "closed-model threshold (1/4, 1/8)" and
"maximum (4/9, 4/27)" — are placed so that their texts overlap each other
and run into the figure title ("Ultra-relativistic branch, every beta:
y = u(1 − sqrt(u))"). In the rendered PNG the top-centre text is
illegible where the two labels collide. (The "bounce root (1, 0)"
annotation is placed cleanly.) Note the script regenerates this figure on
every run, so fixing the PNG alone is not enough — the annotation
coordinates in `scripts/v5_verify.py` §9 must be fixed (move the
closed-model annotation down-left and the maximum annotation up-right, or
use a legend instead of in-plot text), and the regenerated figure
re-checked visually.

**Exact change required:** fix the annotation placement in the figure
script, regenerate, and view the PNG before calling the figure done.
Round 4 must view both figures as images, not just confirm the files exist.

---

## NON-BLOCKING FINDINGS

### N1. Popławski 2016 bibliography entry has no title — Bibliography, L759–760

`\bibitem{Poplawski16}` reads "N. J. Popławski, Astrophys. J. 832, 96
(2016)." — author, journal, volume, page, year, but no title, where every
other entry gives one. The paper is "Universe in a Black Hole in
Einstein–Cartan Gravity" (verified, §3). Add the title.

### N2. First-page-only citations are inconsistent — Bibliography, L747–749, L790–792

Cartan 1922 is cited as "174, 593" (full range 593–595, verified §3) and
Popławski 2012b as "44, 1007" (full range 1007–1014, verified §3), while
Popławski 2010, Hehl 1976 and others give full ranges. Add the end pages
for consistency.

### N3. D's β = 9/2 is cited to Kerlick as well as Popławski — §2, L125–126

"D is β = 9/2 \cite{Kerlick75,Poplawski12}". The value comes from
Popławski 2012, Eq. (10) (ε̃ = −p̃ = −(9/16)κn², averaged with
⟨s²⟩ = (3/4)n² — verified §0.3). Kerlick 1975 gives the un-averaged
(3/4)κ s^l s_l form (Popławski 2012, Eq. (9), "found by Kerlick"), not the
averaged β = 9/2. Cite Popławski 2012 Eq. (10) alone for the β value; keep
Kerlick for the (3/4)κ form where it is actually used.

### N4. The UR and covariant sign numbers are still uncited in the build — §4, L280–290; Appendix B, L737

§4's −3/8 / −3/16 (spatial) and +8/3 / +1/8 (covariant) numbers are now
honestly labelled "reported house calculations, not established results",
which satisfies Round 2 B16's soften option. Residual gap: the deposited
evidence in the build covers only the non-relativistic −3/8 — the
EXCHANGE-CALCULATION file proves −3/8 by three methods, but the UR −3/16
and both covariant values (+8/3, +1/8) rest on v4's Ref. [18] (the Zenodo
repair paper), which is not in this build's bibliography or sources, and
the exchange file does not derive them. Before submission, cite Ref. [18]
properly (or deposit the exchange file) so the paper's most consequential
numbers have a pointer a referee can follow. Note also that v4's claim
that the covariant ratio "is the 1/3 above" does not follow from +8/3 →
+1/8 (ratio 3/64); v5 wisely drops that sentence — do not reintroduce it.

### N5. TOV radius gap: "2%" vs "2.4%" vs computed 2.18% — §3, L267–268; §9; Appendix B, L735

§3 says "its unexplained 2% radius gap", §9's open problems say "the 2%
radius gap", but Appendix B says "2.4% gap vs an independent 11.71 km run".
From the printed numbers, (11.71 − 11.46)/11.46 = 2.18%, so "2%" is the
correct rounding and "2.4%" is wrong. Reconcile all three places to 2.2%.

### N6. de Sitter radius on W: last-digit rounding — §6

§6 prints r_dS = 6.429×10⁻¹⁷ m on W; my 50-digit recomputation gives
6.4305×10⁻¹⁷ m, which rounds to 6.431×10⁻¹⁷ at four significant figures
(B is correct: 1.286×10⁻¹⁶). The script gates it at 10⁻³ relative
tolerance, which hides a last-digit slip. Fix the printed value (or the
script's expected value) so table, text and script agree to the printed
precision.

### N7. Figure 1b's y-range buries the maxima — figures/fig1b_dust_v5.png

The curves and markers are correct (B max (0.5, 0.25), zero (1, 0); W max
(2, 1), zero (4, 0); caption accurate). But the y-axis runs to −16 because
the B curve is plotted to z = 4.5, so both maxima sit in a thin strip at
the top and are barely visible. Restrict the plotted range (e.g. z ≤ 4.2
with a broken axis, or y ≥ −2 with the tail noted) so the landmarks the
caption points at can actually be seen.

### N8. Four labels are never \ref'd — whole manuscript

`\label{fig:dust}`, `\label{tab:count-meas}`, `\label{tab:count-sever}` and
`\label{tab:verify}` have no corresponding `\ref` in the text (the text
refers to "Tables 3–4" and "Appendix B" by bare number/name). Not an error
— LaTeX will not warn — but cross-references should be used consistently,
and an unreferenced figure (Fig. 1b) is easy to lose in a revision. Add
`\ref{fig:dust}` where Fig. 1b is introduced and `\ref`s for Tables 3–4.

### N9. ρ_KT formula printed without ħ and c — §2, L152–154

"the incoherent coupling α = πG/4 gives ρ_KT = m_n²/α = 1.675×10⁷⁴ eV⁴".
The number checks out (script gate RHO-KT; my recomputation 1.675395×10⁷⁴),
but m_n²/α as written is a natural-units schematic — in SI it needs the
ħ, c factors that convert a mass-squared over G into eV⁴. State the units
("in ħ = c = 1 units") or give the SI form.

### N10. Appendix B gate-count label overcounts Table 2 — Appendix B, L725–727

"Table 2 landmarks — Script, 13 gates". The script's UR-prefixed gates do
number 13, but two of them (`UR-HDOT-RATIO`, `UR-HDOT-SIGN`) are the
relativistic-turnaround gates, not Table 2 landmarks (the landmark gates
are 11: UR-W 5 + UR-B 5 + UR-D-x0 1). Relabel as "Table 2 landmarks (11) +
UR turnaround (2)".

### N11. Popławski 2010 erratum not noted — Bibliography, L755–758

Phys. Lett. B 694, 181–185 (2010) carries an erratum, Phys. Lett. B 701,
672 (2011) (arXiv journal reference). Optional: note it, or leave it —
the cited equations are unaffected.

### N12. Popławski 2016 s² citation chain not verified against the 2016 text — §2, L114–116

§2 says "Popławski gives s² = ⅛ħ²n_f² citing Nurgaliev and Ponomariev,
Gasperini, and Brechet and co-workers \cite{Poplawski16,…}". I verified
the ⅛ value itself in Popławski 2010 Eq. (13) and Popławski 2012
(s² = (1/8)n², §0.2–0.3), but I did not verify the 2016 paper's text for
that formula and that citation chain (Round 2 asserted it without showing
the text). Confirm it against ApJ 832, 96 before submission, or re-point
the sentence at Popławski 2010 Eq. (13), which I did verify.

### N13. Trautman Symposia Mathematica entry not independently verified — Bibliography, L765–769

The Nature (Phys. Sci.) 242, 7 (1973) half of the Trautman entry is
verified (corroborated by multiple citing papers; see §3), as is
Kopczyński 1972, Phys. Lett. A 39, 219 (1972). The Symposia Mathematica
12, 139–162 (1973) half was not independently checked against a primary
in this round. Verify it or drop it to the single Nature citation.

---

## 1. Reproducibility audit

### 1.1 Script runs (run by me, in the build directory)

- `python3 scripts/v5_verify.py` → **GATES: 77 PASS, 0 FAIL, of 77**, exit 0.
  Figures regenerated by the run.
- `python3 scripts/correction_paper_compute_standalone.py` → **GATES: 75 PASS,
  0 FAIL, of 75**, exit 0.

Both scripts run from their own files alone, as claimed. Two caveats on what
the passes do and do not establish:

1. **The 77/77 pass does not cover the displayed equations.** No gate tests
   Eq. (7) as printed (81/4096β²) — the script gates the correct landmarks
   81/(64β²) instead. That is how B1 survived a passing suite. Likewise no
   gate tests Table 2's D x_SEC as a D-physics statement (only `UR-D-x0`),
   and no gate derives Table 4 from the thumbnail density (see B4).
2. **The sever gates are circular.** `COUNT-SEVER` (282.693) and
   `COUNT-W-SEV` (283.108) gate the printed Table 4 values against the same
   opaque construction (dex/log₁₀2 + log₂3, then +log₂(4/3)) that produced
   them. A gate that recomputed Table 4 from ρ_L,thumb = 1×10⁻⁴⁷ GeV⁴ would
   have failed — correctly — on all four rows.

### 1.2 Traceability — every number in Tables 1–4

| Number | Traced to | Verdict |
|---|---|---|
| Table 1, all 7 rows: β, ρ_A, n_A, d_A | Script gates T1-*/T1n-* (14 gates); my independent recomputation agrees to printed precision on all 28 entries | ✓ traceable |
| §3 Ḣ(B), Ḣ(W) | Script HDOT-B/W/POS (3 gates); my recomputation agrees | ✓ |
| §3 p_F/m_nc (W/B), spacing, 0.84 fm ratio, Planck gap | Script PF-*, SPACING-*, RADIUS-RATIO, PLANCK-GAP; my recomputation agrees | ✓ |
| Table 2, W/B rows: x_SEC, x_max, y_max, x₀ | Script UR-W/B (10 gates) + grid G10K (8) + FERMI (2); my recomputation agrees; fractions verified by hand (§0.1) | ✓ |
| Table 2, D row: x_max, y_max, x₀ | ε_eff-curve landmarks; agree as algebra | ✓ as algebra, ✗ as physics for x_SEC (B3) |
| Table 2, D row: x_SEC = 0.015625 | **No valid trace**: the stiff-fluid formula does not apply to D (p̃ = −ε̃); no gate asserts it as D physics | ✗ not traceable (B3) |
| Table 3, all 4 rows: N*, \|282−N*\|, Tolerance, Floor | Script COUNT-*-PC, COUNT-DENS-*, COUNT-282-*; my recomputation agrees (281.775 / 279.775 / 281.360 / 283.360) | ✓ |
| Table 4, all 4 rows | Script COUNT-SEVER / COUNT-W-SEV gate the printed values against the same opaque construction; **not derivable from the caption's stated definition** (values are 1.585 bits low throughout) | ✗ not traceable as stated (B4) |
| §6 T_A (W/B), T = 2S doubling, r_dS (B/W) | Script TORS-*/RDS-*; my recomputation agrees except r_dS(W) last digit (N6) | ✓ (modulo N6) |
| §8 Beck Λ, bits, ratio | Script BECK-* (3 gates); my recomputation agrees (1.362852×10⁻⁵², 0.3146 bits, 1.2437) | ✓ |
| §8 N* uncertainty ±0.026 bits | Script COUNT-ERR; agrees (log 1.018/log 2 = 0.0257) | ✓ |
| §8 ρ_KT = 1.675×10⁷⁴ eV⁴ | Script RHO-KT; my recomputation 1.675395×10⁷⁴ | ✓ |
| §3 TOV M_max = 2.060 M_⊙, R = 11.46 km | **Not in any script**; carried from the November 18 run (Appendix B says so honestly) | ⚠ untraceable by design (disclosed) |
| §4 sign numbers −3/8, −3/16, +8/3, +1/8 | **Not in any script**; exchange file in sources/ proves NR −3/8 only; the rest rest on v4 Ref. [18], not in the build | ⚠ untraceable as deposited (N4) |
| §7 axis test numbers | **None printed** (pipeline not deposited — disclosed); the script's AXIS-SEP-METHOD gate uses November 18 coordinates no longer printed, as a method check only | ✓ correctly withheld |
| Appendix B "77 gates" / gate counts | Script results JSON: 77 gates, counts per prefix match Appendix B except the Table 2 label (N10) | ✓ (modulo N10) |

Numbers **not** traceable to a script gate or a deposited file: Table 2 D
x_SEC, all four Table 4 N* values (as defined in the caption), the TOV
numbers (disclosed as carried), and the §4 sign numbers other than the NR
−3/8 (disclosed as house calculations). Everything else in Tables 1–4
traces and recomputes.

### 1.3 Correction-paper check

The standalone correction script passes 75/75 from its own file, as claimed.
I verified its key arithmetic against the corrected source:
dex 84.6219 = 37.6219 + 47 (thumbnail exponent); measured ρ_L =
2.5192712936×10⁻⁴⁷ GeV⁴; overstatement 1.332153793 bits; sever repaired
N* = 282.6928295535 for the repaired density 2.916×10⁵⁵ g cm⁻³; Planck-central
N* = 281.3606757603. All consistent with the corrected source. **But** the
correction paper's sever number is a single-density number (repaired density
= ratio-on-B density), and v5's Table 4 extends it to four rows by an offset
the manuscript never states — that extension, not the correction paper, is
where B4 lives. The manuscript's disclosure of the correction paper's status
(Draft line still on the deposited file; corrected source undeposited;
standalone script ≠ deposited script) is complete and accurate.

### 1.4 Bibliography pass (entries Round 2 did not verify)

| Entry as printed | Verified? | Evidence |
|---|---|---|
| Cartan 1922, "Sur une généralisation de la notion de courbure de Riemann et les espaces à torsion", C. R. Acad. Sci. (Paris) 174, 593 (1922) | **Yes.** Title, journal, volume, year exact. Full page range is 593–595 (ms gives first page only — N2). | Hehl & Obukhov essay bibliography; nLab Cartan page (174 (1922) 593–595); 22 Feb 1922 note. |
| Hehl, von der Heyde, Kerlick & Nester 1976, "General relativity with spin and torsion: Foundations and prospects", Rev. Mod. Phys. 48, 393–416 (1976) | **Yes, exact.** Authors, title, journal, volume, pages, year all correct. | RMP 48, 393 (1976), DOI 10.1103/RevModPhys.48.393; corroborated in multiple citing works. |
| Popławski 2010, "Cosmology with torsion: An alternative to cosmic inflation", Phys. Lett. B 694, 181–185 (2010) | **Yes, exact.** Title, journal, volume, pages, year correct. (Erratum: Phys. Lett. B 701, 672 (2011) — N11.) | arXiv:1007.0587 journal ref. Phys. Lett. B 694:181–185, 2010; DOI 10.1016/j.physletb.2010.09.056. |
| Popławski 2012 (GRG), "Big bounce from spin and torsion", Gen. Relativ. Gravit. 44, 1007 (2012) | **Yes.** Title, journal, volume, first page, year correct. Full range 1007–1014 (ms gives first page only — N2). | GRG Vol. 44, No. 4 (2012) pp. 1007–1014; abstract ("energy density of matter at the bounce is a few orders of magnitude larger than the Planck energy density…") matches the §5 quotation verbatim. |
| Popławski 2016, Astrophys. J. 832, 96 (2016) | **Yes on details, incomplete as printed** (no title — N1). The paper is "Universe in a Black Hole in Einstein–Cartan Gravity", ApJ 832:96 (8pp), 2016 Dec 1, DOI 10.3847/0004-637X/832/2/96. | IOPscience ApJ 832:96; received Aug 2016, published Nov 2016. |
| Popławski 2019, "Universe in a rotating black hole and preferred axis", arXiv:1910.10819 (2019) | **Yes.** Title, arXiv ID, year (v1, Oct 2019) correct. Note: physics.pop-ph preprint, revised as v2 May 2025; the manuscript does not claim journal publication. Abstract ("If the parent black hole is rotating, then its axis of rotation becomes a preferred axis") supports §7's use. | arXiv:1910.10819 [physics.pop-ph], submitted 23 Oct 2019. |
| CODATA 2018, Tiesinga, Mohr, Newell & Taylor, "CODATA recommended values of the fundamental physical constants: 2018", Rev. Mod. Phys. 93, 025010 (2021) | **Yes, exact.** Authors, title, journal, volume, article number, year correct. | NIST publication page; RMP 93, 025010 (2021), DOI 10.1103/RevModPhys.93.025010. |

No invented page ranges found in the seven entries. The only bibliography
defects in this pass are the missing Popławski 2016 title (N1) and the
first-page-only style for Cartan and Popławski 2012b (N2). (Spot-check beyond
the assigned seven: Kopczyński 1972, Phys. Lett. A 39, 219, and Trautman,
Nature (Phys. Sci.) 242, 7 (1973), are corroborated by multiple citing
papers — see N13 for the unverified Symposia Mathematica half. The Shamir
2.8σ/7.38σ sentence in §7 is verified against the PASA 2020 abstract.)

### 1.5 LaTeX — compilation untested; structural check

- No toolchain on this VM: `which pdflatex latexmk xelatex tectonic` all
  return nothing. **Compilation remains untested** (carried from Rounds 1–2).
- Structural check (by script over the .tex): environments balanced —
  document 1/1, abstract 1/1, table 5/5, figure 2/2, equation 9/9,
  thebibliography 1/1; dollar signs even (618); all 20 `\cite` keys resolve
  to `\bibitem`s with no orphans in either direction; both
  `\includegraphics` files exist
  (`figures/fig1a_ur_branch_v5.png`, `figures/fig1b_dust_v5.png`).
- Labels defined: tab:bound, fig:ur, fig:dust, tab:ur, tab:count-meas,
  tab:count-sever, tab:verify. `\ref`s used: tab:bound (×2), fig:ur, tab:ur.
  Four labels are never referenced (N8). No undefined references were found
  among the `\ref`s actually used.

---

## 2. What Round 4 must do (checklist)

1. Fix Eq. (7) (4096 → 64) in §5 and Appendix A; gate the printed equation
   in the script (B1).
2. Rewrite the §5 variable definitions (x = ε/ε_Pl; scaled Y =
   ε_eff/(x₀ε_Pl)); relabel Fig. 1a's axis (B2).
3. Fix Table 2's D row (delete/mark n/a the D x_SEC; state ε̃ = −p̃ in §4;
   restrict the §5 turnaround proof to W/B) (B3).
4. Restate Table 4's construction so it generates the printed numbers, or
   recompute Table 4 per its caption; gate Table 4 from the thumbnail
   density directly (B4).
5. Fix the §2 κ notation (one convention, every κ checked) (B5).
6. Fix Fig. 1a's annotation placement in the script and re-view the PNG
   (B6).
7. Apply N1–N13, compile the LaTeX on a machine with a toolchain, and
   re-verify Tables 2 and 4 and Eq. (7) **from the corrected text**, not
   from the script's expected values — the script's expected values were
   part of how B1 and B4 survived.

## 3. Final word to the coordinator

The revision answered Round 2 honestly and thoroughly on almost every
front — the adoption, the sign problem, the axis section, the count
section, the bibliography, and the threshold definition are all in
materially better shape than the Round 1 draft. What stops this manuscript
is narrower and more embarrassing than what stopped the last one: a
displayed equation that is wrong by 64× against its own table, a table
that cannot be reproduced from its own caption, and a table row that
applies a stiff-fluid formula to a Dirac term whose pressure has the
opposite sign. All three are checkable from the paper's own numbers, in
minutes, with no new physics — which is exactly why a referee will check
them first. Fix those three, the κ notation, and the figure labels, and
the paper's verified core — a careful multi-normalisation computation of a
known bound, with its domain and its failures stated honestly — is ready
for a referee to attack on its merits rather than its arithmetic.
