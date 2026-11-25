# Aldred Limit v5 — Round 2 Adversarial Peer Review

**Reviewer:** Round 2 adversarial reviewer (child of the build coordinator).
**Date:** 19 November 2026. **Manuscript:** `aldred-limit-v5.tex` (755 lines).
**Role:** attack, not praise. Review only — no file in the build was edited.

## Verdict

**The manuscript SURVIVES Round 2 as a draft. It does NOT survive as a submission-ready paper. Major revision required — not a from-scratch rewrite.**

The core bound computation is sound: every number in Tables 1–2 that the verification
script covers recomputes correctly from CODATA 2018, Böhmer et al. Eq. (22) and Eq. (41)
check out against the primary source, and the four new citations exist with correct
details. No fatal mathematical error was found in the dust or ultra-relativistic algebra.

But the manuscript as written contains a wrong equation (Eq. 1), an unjustified
adoption at its centre, a vacuum-count section whose headline claim cannot fail the way
it is framed, and a whole observational section built on numbers no one can reproduce —
plus a bibliography that still carries placeholders and one citation that appears to be
wrong. A referee who checks any of these will stop reading. That is what Round 2 is for.

**Counts: 17 BLOCKING findings, 18 NON-BLOCKING findings, plus Notes.**
Blocking = must be fixed before Round 3. Non-blocking = fix at the reviewer's
discretion, but each is a real defect a referee could raise.

**The three most serious findings:**

1. **B1 — Eq. (1) is wrong, and §2 uses two different meanings of κ.**
   Eq. (1) writes ρ_eff = ρ − κ²⟨S²⟩/c² with κ² = 8πG/c⁴. Substituting Eq. (2),
   ⟨S²⟩ = ħ²n²/8, the correction is πGħ²n²/c⁶ — off by 1/c² from the paper's own
   Eq. (4) (βπGħ²n²/c⁴) and dimensionally not a mass density. Böhmer's Eq. (22) has
   no /c². The paper's founding equation contradicts its own Eq. (4).
2. **B2 — The adoption of W (β = 1/4) is unjustified as written, and the
   s_P = 2S_B explanation is presented as supported when its support collapses.**
   v5 regresses from v4, which honestly said the factor of four is "unresolved" and
   "we do not claim" the factor-two enters Böhmer. v5 re-adopts v3's proposal with
   three arguments, of which one is tautological and the other two rest on papers
   the build admits were not read. The paper's central number (3.8871×10⁵⁵ vs
   9.7178×10⁵⁴) therefore rests on a choice dressed as a result.
3. **B10/B11 — §9's vacuum-count "consistency" cannot fail and is reported
   selectively.** The floor rule as stated is one-sided (any integer ≥ N* passes, so
   283 or 300 would "pass" too); the manuscript never concedes this. The abstract
   reports only the one passing combination (W / measured / tolerance) and omits that
   the count fails on the literature normalisation B and on the earlier papers' own
   density (ratio-on-B) under the tolerance rule — and that the "consistency" therefore
   rests entirely on the unconfirmed W adoption from B2.

---

## 0. What I ran myself (not trusted from Round 1)

| Check | Result |
|---|---|
| `scripts/v5_verify.py` (re-run by me) | **73/73 PASS, exit 0** — confirmed |
| `scripts/correction_paper_compute_standalone.py` (re-run by me) | **75/75 PASS, exit 0** — confirmed |
| Independent recomputation (Decimal, 50-digit, typed from CODATA values, not from `v5_verify.py`) | W ρ_A = 3.8871107123489…×10⁵⁵ g cm⁻³ ✓; B ρ_A = 9.71777678087…×10⁵⁴ ✓; UR B x₀ = 81/64 = 1.265625 exactly ✓; UR W x₀ = 20.25 exactly ✓; Beck Λ = 1.362852328…×10⁻⁵² m⁻² ✓; Ḣ(B) = 8.150467250×10⁴⁸ s⁻² ✓. See §0.1 for the full table, including two discrepancies (0.002–0.003 bits) in §9. |
| Böhmer et al. 2018 vs PMC5866282 (read directly) | Eq. (19) S² ≡ ½S_μνS^μν ≥ 0 ✓; Eq. (22) ρ_eff = ρ − κ²S² ✓; Eq. (23) p_eff = p − c²κ²S² ✓; Eq. (41) S² = ⅛ħ²n² ✓. The manuscript's use of Eq. (22)/(41) as the B normalisation is correct. See §0.2. |
| Four new citations (web search) | All four exist with the details as printed — Beck, Ellis, Padilla–Saltas, Popławski 2011. See §0.3. One use is wrong (B12: Popławski "eight times"). |
| Figures (viewed as images) | Fig. 1a lacks the dashed continuation and the closed-model marker its caption claims; Fig. 1b's two "curves" coincide exactly. See B6. |
| LaTeX compile | NOT checked — no toolchain on this VM (Round 1 limitation, carried forward). |

### 0.1 Independent recomputation results

Constants (CODATA 2018, typed independently): G = 6.67430×10⁻¹¹,
ħ = 1.054571817×10⁻³⁴, c = 299792458, m_n = 1.67492749804×10⁻²⁷,
m_e = 9.1093837015×10⁻³¹, α = 7.2973525693×10⁻³.

| Quantity | My value | Manuscript | Verdict |
|---|---|---|---|
| W dust ρ_A (β=1/4) | 3.8871107123489×10⁵⁵ g cm⁻³ | 3.8871×10⁵⁵ | ✓ |
| W n_A | 2.3207635655260×10⁸⁵ m⁻³ | 2.3208×10⁸⁵ | ✓ |
| B dust ρ_A (β=1) | 9.7177767808722×10⁵⁴ g cm⁻³ | 9.7178×10⁵⁴ | ✓ |
| Ratio-on-B ρ_A (β=1/3) | 2.9153330342616×10⁵⁵ g cm⁻³ | 2.9153×10⁵⁵ | ✓ |
| UR B x₀ = 81/(64·1²) | 1.265625 | 1.265625 | ✓ exact |
| UR W x₀ = 81/(64·(1/4)²) | 20.25 | 20.25 | ✓ exact |
| UR B x_max = 9/16, y_max = 3/16 | 0.5625, 0.1875 | 0.5625, 0.1875 | ✓ exact |
| Planck gap ρ_Pl/ρ_A(B) | 5.3045054606999×10³⁸ | 5.30×10³⁸ | ✓ |
| Ḣ at bounce (B) | 8.15046725016×10⁴⁸ s⁻² | 8.1505×10⁴⁸ | ✓ |
| Beck Λ = G²m_e⁶/(ħ⁴α⁶) | 1.3628523282991×10⁻⁵² m⁻² | 1.3628×10⁻⁵² | ✓ |
| Beck/observed ratio | 1.2437 (24.4% high), 0.315 bits | 25%, 0.32 bits | ✓ |
| Count N* W, measured (GeV⁴ bench) | 281.7777 | 281.778 | ✓ |
| Count N* W, measured (5.845×10⁻³⁰ g cm⁻³ bench) | **281.7754** | 281.778 | ⚠ 0.0023-bit bench inconsistency — see B11 |
| Count N* ratio-on-B, measured (GeV⁴ bench) | 281.3627 | Table: 281.361; text: 281.361 then 281.363 | ⚠ table/text/script disagree — see B11 |
| Count N* ratio-on-B (5.845×10⁻³⁰ bench) | 281.3603 | — | (third value for the "same" bench — see B11) |
| 282-cell density / measured, ratio-on-B | 0.6429 → **35.7% low** | "36% low" appears only in the unsent journal letter, not in §9 | Miles's 36% confirmed; §9 omits it — see B11 |
| 282-cell density / measured, W | 0.8572 → 14.3% low | not stated | — |
| Planck Λ uncertainty (H₀ ±0.54, Ω_Λ ±0.0056) | ≈1.8% → **0.026 bits** on N* | not stated anywhere | Miles's "~2%" confirmed; immaterial vs 0.64-bit margin — see N13 |

Two further checks I did by hand: (a) the 10,000-point grid's x_max relative error is
1.25×10⁻⁵ on both W and B (computed from `v5_verify_results.json`: 9.0001125 vs 9;
0.56250703125 vs 0.5625) — **not** "a part in 10⁷" (see B5). Root error is 3.7×10⁻⁹
relative; SEC error ≈6×10⁻⁸ relative. (b) The UR-branch turnaround: at the UR zero,
ε_eff = 0 and p_eff = ε/3 − ε_spin = −2ε/3 (since ε_spin = ε at the zero), so
ε_eff + p_eff = −2ε/3 < 0 and Ḣ = −(4πG/c²)(ε_eff + p_eff) > 0 — the turnaround
**does** hold, but the manuscript never shows this (see B4).

### 0.2 Böhmer et al. 2018 — verification against the primary source

Source read: PMC5866282, "Does space-time torsion determine the minimum mass of
gravitating particles?", Böhmer, Burikham, Harko & Lake, Eur. Phys. J. C **78**, 253
(2018), doi:10.1140/epjc/s10052-018-5719-y, arXiv:1709.07749.

- Eq. (19): S² ≡ ½ S_μν S^μν ≥ 0 — confirmed (PMC L354).
- Eq. (22): ρ_eff = ρ − κ²S² — confirmed (PMC L374). **No /c².** The manuscript's
  Eq. (1) inserts one (see B1).
- Eq. (23): p_eff = p − c²κ²S² — confirmed (PMC L379).
- Eq. (41): S² = ⅛ ħ²n² — confirmed (PMC L528), in the "Fermion model" subsection,
  introduced as "It was shown in [17] that…" — i.e. Böhmer Eq. (41) is itself a
  **cited** result (from Gasperini and others), not Böhmer's own derivation.
- Eq. (18): T^λ_μν = κ²u^λS_μν — confirmed (PMC L344).
- The manuscript's statement (§2, L127) that "the Böhmer form as printed is the B
  normalisation" is **correct**: κ²S² with S² = ħ²n²/8 gives πGħ²n²/c⁴, i.e. β = 1.
- The ⅛ average is independently attested: Popławski (ApJ 832, 96, 2016) gives
  s² = ⅛ħ²n_f² citing Nurgaliev & Ponomariev (1983), Gasperini (1986) and
  Brechet et al. (2008). The **average** is not in dispute; the **prefactor** is.
- Note: Böhmer's introduction (Eq. 1, citing Kopczyński/Trautman) quotes yet another
  form for the maximum density, ρ_max ≃ 10⁵⁵ g cm⁻³ — the literature itself carries
  more than one coefficient, which reinforces B2.

### 0.3 Citation verification — the four new citations

| Citation as printed in v5 | Verified? | Evidence |
|---|---|---|
| Beck 2009, Physica A **388**, 3384–3390, "Axiomatic approach to the cosmological constant" | **Yes, exact.** | arXiv:0810.0752; journal ref. Physica A 388:3384–3390, 2009; DOI 10.1016/j.physa.2009.05.023. Formula Λ = G²m_e⁶/(ħ⁴α_el⁶) confirmed from the abstract. My recomputation: 1.36285×10⁻⁵² m⁻², 24.4% above the Planck-2018 observed value, 0.315 bits — manuscript's "25% / 0.32 bits" is fair. |
| Ellis et al. 2011, CQG **28**, 225007, "On the trace-free Einstein equations…" | **Yes, exact.** | arXiv:1008.1196; CQG 28 (2011) 225007; DOI 10.1088/0264-9381/28/22/225007. Note: Miles's brief said "Padilla–Saltas 2014" — the correct journal year is **2015** (arXiv 1409.3573); the manuscript has it right and Miles had it wrong. |
| Padilla & Saltas 2015, EPJC **75**, 561, "A note on classical and quantum unimodular gravity" | **Yes, exact.** | DOI 10.1140/epjc/s10052-015-3767-0; arXiv:1409.3573. Caveat on **use**, not details: the paper's own conclusion is that unimodular gravity says nothing new about the cosmological-constant problem (see N9). |
| Popławski 2011, Ann. Phys. (Berlin) **523**, 291, "Cosmological constant from quarks and torsion" | **Yes — details exact, use wrong.** | arXiv:1005.0893; Ann. Phys. 523:291–295, 2011; DOI 10.1002/andp.201000162. Abstract: the torsion-induced constant's "**energy scale** is only about 8 times larger than the observed value." The manuscript (§9, L569) writes "a cosmological constant of the order of eight times the observed value" — that converts an energy **scale** into a value of Λ. See B12. The arXiv abstract also adds "Adding leptons to this picture could lower this scale to the observed value" — a qualifier the manuscript omits. |

Also verified in passing: Gasperini 1986 = Phys. Rev. Lett. **56**, 2873–2876 (1986),
"Spin-dominated inflation in the Einstein–Cartan theory"; Nurgaliev & Ponomariev 1983
= Phys. Lett. B **130**, 378 (1983) (cited as such by Popławski 2016 and by
Garcia de Andrade, astro-ph/0007204); Magueijo–Zlosnik–Kibble 2013 = Phys. Rev. D
**87**, 063504 (2013), "Cosmology with a spin"; Shamir 2020 = Publ. Astron. Soc.
Aust. **37**, e053 (2020), doi:10.1017/pasa.2020.46, arXiv:2011.03723; Popławski 2012
= Gen. Relativ. Gravit. **44**, 1007–1014 (2012), "Big bounce from spin and torsion";
Popławski 2010 = Phys. Lett. B **694**, 181–185 (2010); Böhmer 2018 = EPJC **78**,
253 (2018) (see §0.2). Kerlick: see B15 — the citation as printed was **not** verified
and appears wrong.

---

## BLOCKING FINDINGS

### B1. Eq. (1) is wrong, and §2 uses κ in two incompatible senses — §2, Eq. (1), L89–90

Eq. (1) reads ρ_eff = ρ − κ²⟨S²⟩/c² with κ² = 8πG/c⁴. Substituting Eq. (2),
⟨S²⟩_W = ħ²n²/8, the spin correction is (8πG/c⁴)(ħ²n²/8)/c² = **πGħ²n²/c⁶**.
The paper's own Eq. (4) gives the correction as βπGħ²n²/c⁴. The two differ by
1/c² = 1.11×10⁻¹⁷. πGħ²n²/c⁶ has units kg·s²·m⁻⁵ — it is not a mass density under
any reading (mass density: πGħ²n²/c⁴; energy density would need ×c², not ÷c²).
Böhmer's Eq. (22), verified against PMC5866282 (§0.2), is ρ_eff = ρ − κ²S² with
**no /c²**. The manuscript mis-transcribes the very equation it cites as verified.

Compounding it, §2's prose (L121–135) says the difference "sits entirely in the
prefactor — κ/4 in one writing, κ in the other". But Eq. (1) defines κ² = 8πG/c⁴,
so κ = √(8πG)/c², while the prose uses κ to mean the coupling 8πG/c⁴ itself
(Hehl's convention). The W form is (κ²/4)⟨s²⟩ and the B form is κ²⟨S²⟩ in the
manuscript's own notation — not "κ/4" vs "κ".

**Exact change required:** rewrite Eq. (1) as ρ_eff = ρ − κ²⟨S²⟩ (no /c²), with
κ² = 8πG/c⁴ defined once; rewrite the §2 prefactor sentences to use κ²/4 vs κ²
throughout; re-check every later κ in §§2–6 for the same collision. This is a
one-line fix to the paper's founding equation — a referee who does the dimensional
check will not read further until it is fixed.

### B2. The adoption of W is unjustified as written; the s_P = 2S_B explanation is a choice dressed as a result — §2, L118–160

The manuscript adopts W (β = 1/4) and justifies the adoption solely with the
"proposed explanation" that the Popławski spin tensor is twice Böhmer's,
s_P = 2S_B (L140), supported by "three arguments" (L142). On inspection:

- **Argument 3 is tautological.** "The two writings agree on every observable
  except the prefactor… and only ρ_A moves, by exactly four." That is true of any
  two writings that differ only by a prefactor. It is evidence for nothing about
  which prefactor is right.
- **Arguments 1 and 2 rest on papers not read in this build** — the manuscript
  itself admits it (L147–152): "the Gasperini and Nurgaliev–Ponomariev papers have
  not been read against their primaries in this build." Argument 1 invokes
  "Gasperini's 2πGσ²/c⁴" without ever defining σ or showing that Gasperini's σ²
  is the same object as ⟨s²⟩; the identity 2πG/c⁴ = κ/4 is arithmetic, not evidence.
  Argument 2 ("the Nurgaliev–Ponomariev form carries the same κ/4 prefactor") is
  asserted for a paper whose full details the bibliography does not even give.
- **The "accompanying note" behind the explanation is not in the build.**
  v3 (sources, L43) is explicit: the three arguments are "reported from an
  accompanying note", the "calibration scripts were not re-run", and argument (iii)
  — the aligned-spin ceiling — is "not decisive" by v3's own admission
  (with quantum counting s(s+1) = 3/4 the ceiling rises to 3/16). v5 drops that
  caveat and presents the three arguments as support without qualification.
- **This is a regression from v4.** v4 (sources, §2) states the honest position:
  "A factor of two between the two papers' normalisations of the spin tensor would
  produce exactly four in the square, but we have not found where such a factor
  enters Böhmer et al.'s derivation, and we do not claim that it does. The factor
  is unresolved." v5 reverts to v3's proposal while keeping v4's "not independently
  confirmed" fig leaf — but then **adopts** W on the strength of it.
- **v5 also drops v4's actual reasons for adopting W**, which were (1) W is the
  coefficient of the original spin-fluid derivation, written out with the averaging
  stated in two peer-reviewed papers, and (2) adopting W keeps this paper consistent
  with the author's own vacuum-energy programme (incoherent coupling α = πG/4).
  Those are reasons of sourcing and consistency, openly labelled "not a derivation".
  v5 gives the reader none of them.

**Exact change required:** either (a) derive s_P = 2S_B from the two papers'
definitions (with the calibration scripts re-run and Gasperini/Nurgaliev read
against their primaries), or (b) revert §2 to v4's language — the factor is
**unresolved**, the s_P proposal is a conjecture, W is adopted as a **stated choice**
on the sourcing/consistency grounds v4 gave, and B remains the literature value
carried beside it. Under (b), delete or demote the "three arguments" paragraph:
argument 3 deleted as vacuous; arguments 1–2 deleted until the primaries are read.
The abstract's "I adopt the classical spin-fluid value" must then read as a choice,
not as the outcome of an explanation.

### B3. The sign problem is absent from the abstract and misclassified in §10 — Abstract L14–41; §4 L272–310; §10 L581–631

§4 states the problem well: the normal-ordered spatial spin square is negative
(−3/8 ħ²n² non-relativistic, −3/16 ħ²n² ultra-relativistic) while the covariant
average is positive, the full Dirac (Wigner-function) evaluation "has not been done",
and "if the negative sign carries to the full evaluation, the spin term changes sign,
the effective density has no zero, and there is no bounce at all" (L289–293). That is
the single most consequential sentence in the paper: it kills the bounce, not a
coefficient. Yet:

- The **abstract never mentions it**. A reader of the abstract alone learns the
  bounce is at/above Planck density and the count is not derived — but not that the
  bounce may not exist at all. The Planck-domain caveat is about the theory's
  *validity*; the sign problem is about the bounce's *existence*. The latter is
  more fundamental and is the one omitted.
- §10 lists it as a **revision condition** ("If the full Dirac evaluation returns a
  negative spin-squared sign, the bounce is removed and the paper becomes a paper
  about why there is no bounce"). That is a **kill** of the claim as stated, not a
  revision. §10's kill conditions instead list only a hypothetical EC solution that
  compresses through ρ_A — which is not the live threat. The live threat is the sign.

**Exact change required:** add one sentence to the abstract: "A normal-ordered Dirac
evaluation gives a negative spin-squared sign that would remove the bounce entirely;
that evaluation has not been done." In §10, move the negative-sign case from the
revision conditions into the kill conditions, in those words. (The numbers themselves
are a separate problem — see B16.)

### B4. The ultra-relativistic "bounce" is never shown to be a bounce — §5, L311–405

§3 proves the bounce for **dust**: Ḣ = −4πGρ(1 − 2ρ/ρ_A), so at ρ = ρ_A, H = 0 and
Ḣ = +4πGρ_A > 0. §5 then computes the **relativistic** zero (1.27 ε_Pl on B,
20.25 ε_Pl on W) and calls it "the flat-Friedmann bounce" (Table 2 caption, L386–389;
§5 text, L322–326) — but never computes Ḣ for the relativistic branch. A zero of
ε_eff gives H = 0; a turnaround additionally needs Ḣ > 0, which for a relativistic
gas with non-zero p_eff is a different calculation from the dust one and is not done
anywhere in the paper (not in §5, not in Appendix A). The headline numbers are
therefore asserted to be bounces, not shown to be.

I checked it myself (§0.1): at the UR zero, ε_spin = ε, so
p_eff = ε/3 − ε_spin = −2ε/3, ε_eff + p_eff = −2ε/3 < 0, hence
Ḣ = −(4πG/c²)(ε_eff + p_eff) > 0 — the turnaround does hold. The claim is true;
the proof is absent.

**Exact change required:** add the three-line Ḣ computation for the UR branch to §5
(or Appendix A): p_eff at the zero, ε_eff + p_eff = −2ε/3, Ḣ > 0. Until then the
paper's headline result (the 1.27/20.25 ε_Pl bounce) is an unproved assertion in the
paper's own terms.

### B5. The grid-precision claim is false against the paper's own results file — §5, L371–375

§5: "The grid check is new in this revision… (maximum, root, and SEC onset each
recovered to a part in 10⁷)". The paper's own `v5_verify_results.json` gives, for
the maximum: W 9.0001125 vs 9 (relative error 1.25×10⁻⁵), B 0.56250703125 vs 0.5625
(relative error 1.25×10⁻⁵). That is **125 times worse** than a part in 10⁷. (Root:
3.7×10⁻⁹ relative — better than claimed; SEC: ≈6×10⁻⁸ — as claimed.) The word
"each" makes the sentence false, and the failure is structural: a grid maximum is
limited by the grid step, so it cannot reach 10⁻⁷ on a 10,000-point grid.

**Exact change required:** replace "each recovered to a part in 10⁷" with the actual
figures: "root and SEC onset recovered to ~10⁻⁷–10⁻⁸, maximum to ~10⁻⁵ (grid-step
limited)". Same correction in Appendix B Table 4, which prints "~10⁻⁷" for the grid
row (L688).

### B6. Figure 1a's caption describes a figure that does not exist; Figure 1b shows one curve as two — §5, L350–360; figures/

Caption to Fig. 1a: "The dashed continuation past the root is the formal negative
branch and is not physical. The closed-Friedmann turning-point criterion is a
distinct geometric condition, not a root of this curve" (implying it is marked in
the figure). The regenerated `fig1a_ur_branch_v5.png` (viewed by me) contains
**neither**: the curve stops at the root (the regeneration code sets y = NaN for
u > 1), there is no dashed continuation, and there is no closed-model marker of any
kind. The caption also says the closed-model criterion "is marked separately in the
figure" (§5, L346) — it is not marked anywhere.

Fig. 1b: the regeneration code plots x(1−x) twice with different labels (W and B).
In scaled variables the two curves are identical, so the figure shows **one visible
curve** (orange over blue) with a legend claiming two. A reader sees one curve
labelled two ways.

**Exact change required:** either regenerate Fig. 1a with the dashed continuation and
a marked closed-model criterion (and define that criterion — see B17), or delete
both claims from the caption and §5 text. For Fig. 1b, either plot the curves in
unscaled variables (where W and B actually differ) or delete the duplicate and say
in the caption that the scaled dust curve is prescription-independent.

### B7. The abstract overclaims verification — Abstract, L38–40

"Every number in this paper is recomputed from CODATA 2018 constants by a script
that runs from the deposited files alone." That is false, and the paper's own
Appendix B contradicts it: axis-fit pipeline outputs "not reproduced; pipeline not
deposited"; rotating-core numbers "carried from November 18 rerun; ansatz-level";
TOV solver "not deposited; 2% radius gap open"; Kretschmann scalar "not computed";
torsion-scalar derivation "still to be shown"; sign numbers (§4) appear in no script
at all; spin-flip numbers are absent. "Every number" cannot survive Appendix B.

**Exact change required:** narrow the abstract to what is true, e.g. "Every number
in Tables 1–3 is recomputed from CODATA 2018 constants by a script that runs from
the deposited files alone; the numbers in §8 are carried from the November 18 rerun
and are not covered by that script." Do not let the abstract promise what Appendix B
retracts.

### B8. The axis test: kill condition unstated in v5, an anachronistic citation, a misrepresented source, and unreproduced numbers — §8, L443–484; §10, L581–631

Four defects in one section:

- **(a) The kill condition is not actually specified.** §10 says a galaxy-spin axis
  "coincides with the CMB Cold Spot within the stated angular and precision cuts".
  But v5 never states the angular cut anywhere. The November 18 source
  (sources/aldred-limit_2_p3ep.txt, Table II) specifies the kill line as
  "separation above 30° with a cone below 15°" — v5 kept the 15° precision cut
  (§8: "twice as wide as the 15° precision the kill line requires") and **dropped
  the 30° angular cut**. §8's "44.6° … past the kill distance" is meaningless in v5
  because the kill distance is never given. A referee cannot apply a kill condition
  the paper does not state.
- **(b) The Iye citation is anachronistic.** §8: "Iye's result is 1.29σ
  \cite{Iye91}". Iye91 is Iye & Sugai, ApJ **374**, 112 (1991). The 1.29σ figure
  concerns the **cleaned SDSS sample of 72,888 galaxies** — SDSS did not exist in
  1991. The 1991 paper cannot be the source of a result on that sample. Either the
  1.29σ comes from a later Iye work that must be cited, or it comes from the house
  pipeline's own reading, in which case it is unreproduced (see (d)).
- **(c) "None of them claims a detection" is false.** §8: "Earlier surveys found the
  same pattern of marginal signals and none of them claims a detection
  \cite{Longo11,Land08,Shamir12,Shamir20}". Shamir 2020 (verified, §0.3) reports
  dipole-axis fits at "~2.8σ and ~7.38σ in HST and SDSS, respectively" — that
  **is** a claimed detection-level signal, whatever one thinks of it. The sentence
  misrepresents the cited source. (Longo 2011 likewise claims evidence for a
  preferred handedness; Land 2008 and Shamir 2012 were not re-verified here and must
  be checked in Round 3 before the sentence is re-asserted in any form.)
- **(d) The numbers are unreproduced and the "University standard" is undefined.**
  §8 admits the axis-fit pipeline "is not in the deposited files, and its outputs
  have not been independently reproduced". What v5's script verifies (AXIS-SEP) is
  only spherical trigonometry **from the fitted axis coordinates** (44.7° from rounded
  inputs vs 44.6° printed) — it does not verify the fit, the 72,888-galaxy cleaning,
  the bootstrap cone, or any catalogue number. Ganalyzer (34.9°/23.5°), HSC
  (75.2°/22.9°), the 1.6σ dipole and the 1.29σ figure are all carried from the
  October pipeline, which is not in the workspace (Round 1 and the Nov 18 changelog
  both say so). The sentence "the University standard for this paper stands at 76
  of 87 checks, below the 90% pass line" (L478–479) introduces undefined internal
  bookkeeping ("University standard", "87 checks") that appears nowhere else in the
  paper and cannot be checked by a reader.

**Exact change required:** (a) state the full kill line in §8 **and** §10 — angular
cut 30°, precision cut 15° — with the source of each number; (b) fix the Iye
citation (cite the actual paper the 1.29σ comes from, or delete the figure);
(c) delete or rewrite the "none claims a detection" sentence to state what Shamir
2020 actually reports (2.8σ/7.38σ dipole fits) and the paper's assessment of it;
(d) either deposit the axis-fit pipeline and reproduce its outputs, or cut the
catalogue numbers (see the scope ruling in §4 below) — and delete the "76 of 87"
sentence or define the standard and list the 87 checks.

### B9. Rotating-core numbers are unverified, ungated, and underived in v5 — §8, L443–466

§8 prints a_max = 0.9866 at l = 0.5, 1 − a_max ≈ 0.470 (l/M)⁵, a 1.4×10⁻⁶⁷
deviation from Kerr for a 10 M_⊙ core, a_max = 0.9 at 3.0×10¹⁴ g, a_max = 0.5 at
1.6×10¹⁴ g, and an alternative-profile a_max = 0.1610 with a 4.6×10¹⁵ g threshold.
**None** of these numbers appears in `v5_verify.py` (no gates), no metric and no
density profile is given in v5 from which they could be derived, and Appendix B
admits they are "carried from [the] November 18 rerun; ansatz-level". The Nov 18
source itself warns that its own earlier figures for the old profile "do not
reproduce" and "are superseded", and that "the profile choice matters at this level".
§10's kill condition ("a black hole spinning above the torsional cap kills the
rotating extension") therefore rests on numbers the paper cannot verify. The
Kretschmann scalar for the rotating model "has not been computed" (§8).

**Exact change required:** either deposit the rotating-core calculation (metric,
profile, derivation) and gate its numbers in the verification script, or cut all
the numbers from §8 and reduce the rotating core to a short ansatz paragraph with
no quantitative claims (see scope ruling, §4). The kill condition in §10 must go
with the numbers if they are cut.

### B10. The floor rule cannot confirm 282, and the abstract reports only the passing combination — §9, L486–580; Abstract; Conclusion L633–647

§9 is honest about the tolerance rule and the floor rule being different, and about
the margin being thinner than the earlier fixes. It then fails to draw the
consequence that matters:

- **The floor rule is one-sided and cannot confirm a specific integer.** Under the
  floor rule, "the smallest integer at or above N*" passes. For the ratio-on-B
  reading (N* = 281.36), 282 passes — but so would 283, 300, or any larger integer.
  A rule under which the count cannot fail for any N ≥ N* carries no evidence that
  **282** is the right number rather than 283. The manuscript never concedes this.
  It presents the floor rule as a legitimate alternative reading ("the reading under
  which a count of cells must at least reach the requirement") without noting that
  it destroys the test's falsifiability for the fixed count 282. This is Miles's
  central objection ("under 'at least the target,' 283 or 300 would pass too, so the
  test can't fail"), and §9 does not answer it — it restates the rule and moves on.
- **The abstract reports only the passing combination.** Abstract: "on the adopted
  normalisation the 282-cell count is inside tolerance on the measured bench and
  misses on the sever bench". It omits that the count **fails on the literature
  normalisation B** (|282 − 279.778| = 2.222) and **fails on the earlier papers' own
  density** (ratio-on-B, |282 − 281.361| = 0.639, missing tolerance by 0.139 bits)
  under the tolerance rule. The only tolerance-rule pass in the whole table is
  W/measured — i.e. it passes only on the adopted normalisation, whose adoption is
  itself unconfirmed (B2). The "consistency" claimed in §9 ("a bound computed from
  the neutron mass… lands within a quarter of a bit of the measured vacuum density")
  and in the Conclusion ("the vacuum count is consistent with the bound on the
  adopted normalisation and the measured bench") is therefore conditional on W in a
  way the abstract hides.
- **The two rules are applied asymmetrically in Table 3.** The table gives a Tol
  verdict column for the measured bench only; the sever bench gets no rule verdict
  at all, and no floor-rule verdict is tabulated anywhere — the reader must compute
  them. (Note also: on the sever bench under the floor rule, the admissible integer
  for W is ⌈283.108⌉ = **284**, not 283; §9's "where the admissible integer is 283"
  is the tolerance-rule answer, stated without saying which rule.)

**Exact change required:** (i) in §9, state explicitly that the floor rule is
one-sided — it can only show 282 is *at least* enough, it cannot confirm 282
against 283 or any larger integer — and therefore the floor-rule "pass" on
ratio-on-B is not evidence for 282; (ii) in the abstract, state the full pattern:
the count passes tolerance **only** on W/measured, and fails on B and on ratio-on-B
under the tolerance rule; (iii) label the §9/Conclusion "consistency" claim as
conditional on the unconfirmed W adoption; (iv) tabulate both rules on both benches.

### B11. §9 is not self-contained: undefined terms, multiple "measured benches", internal inconsistency on N* — §9, L486–580

A referee who has not read the house history cannot follow §9, and the section
disagrees with itself and its own script:

- **Undefined house terms.** "Bench" (measured/sever), "pair", "cells", "dex" are
  used without definition on first use. What is a "sever bench"? What is a "dex of
  84.6219" — a dex of *what*? Where does the +log₂(3) in the sever-bench N*
  (N* = 84.6219/log₁₀2 + log₂3) come from? What is "the pair" — §9 says "the pair
  of cells the earlier work builds is N = 282", which reads as if a pair were 282
  things. None of this is defined in v5; all of it lives in the correction paper.
  §9 must be readable without it.
- **"The measured bench" is not one bench.** The correction paper itself documents
  three values for the ratio-on-B N* on measured prints: 281.3606757603 (5.845×10⁻³⁰
  g cm⁻³), 281.3520626300 (5.88×10⁻³⁰), 281.364963 (audit table) — a spread of
  0.013 bits. v5's script gates 281.363 (GeV⁴ bench, 2.5152×10⁻⁴⁷ GeV⁴). v5 §9
  presents "the measured bench" as singular. Pick **one** bench definition, print
  it, and use it in table, text, and script alike.
- **Table 3, text, and script disagree on N* (ratio-on-B, measured).** Table 3
  prints 281.361 (|282 − N*| = 0.639); §9's text uses **both** 281.361 (L537) and
  281.363 (L539) in adjacent sentences; the script gates 281.363 (computed
  281.362679). My independent recomputation gives 281.3627 (GeV⁴ bench) and 281.3603
  (5.845×10⁻³⁰ bench) — the table's 281.361 matches neither cleanly. The discrepancy
  (0.002 bits) is immaterial against the 0.139-bit miss, but a table that disagrees
  with its own verification script on the paper's central count number is not
  submission-ready.
- **The printed ρ_Λ values disagree with each other.** §9 prints
  ρ_Λ = 2.5152×10⁻⁴⁷ GeV⁴ (5.845×10⁻³⁰ g cm⁻³). Converted, 2.5152×10⁻⁴⁷ GeV⁴ =
  5.8356×10⁻³⁰ g cm⁻³, not 5.845×10⁻³⁰ — a 0.16% (0.0023-bit) inconsistency between
  the two forms of the same number, and the script's `RHO_L_GCC = 5.845e-30` is dead
  code (the gates use the GeV⁴ form). Reconcile them.
- **The most intelligible statement of the miss is missing from §9.** Miles's "36%
  low" (verified by me: 282 cells give 0.643× the measured density on ratio-on-B,
  i.e. 35.7% low) appears **nowhere in §9** — only in the unsent journal letter.
  Round 1's report claims §9 says "36% low against the measured density"; it does
  not. §9 reports the miss only in bits, which is the least intelligible unit for
  the size of the failure. A reader should be told in plain density terms that the
  282-cell count undershoots the measured density by ~36% on the earlier papers'
  own density.

**Exact change required:** define bench/pair/cells/dex and the sever-bench derivation
in §9 itself; fix one measured-bench definition and make Table 3, §9 text, and the
script agree to the printed precision; reconcile the two ρ_Λ forms; add the 36%
density statement to §9.

### B12. Popławski 2011 is misstated: "energy scale" became "cosmological constant" — §9, L566–572

§9: Popławski's "mechanism generates a cosmological constant of the order of eight
times the observed value". Popławski's abstract (verified, §0.3) says the
torsion-induced constant's "**energy scale** is only about 8 times larger than the
observed value". An energy scale 8× larger is not Λ 8× larger (if the scale is
Λ^{1/4}, Λ is ~8⁴ ≈ 4096× larger). The manuscript converts a scale into a value.
This is in the very paragraph that claims the citation faults of earlier versions
are "fixed in this revision".

**Exact change required:** quote Popławski's words — "energy scale about eight times
the observed value" — do not convert it to "a cosmological constant eight times the
observed value", and add his qualifier that adding leptons "could lower this scale
to the observed value". The "undercuts any claim that torsion charges nothing" point
survives the correction; the magnitude as printed does not.

### B13. "Drafted, not adopted" is presented as a quotation from earlier papers; it appears in none of them — §9, L543–546

§9: "the pair is not derived — the earlier papers call it 'drafted, not adopted' in
their own words". I searched every source file in the build (v3, v4, Nov 18
manuscript, both revisions, the correction paper, the changelog). The phrase
"drafted, not adopted" appears **only** in two places: v5 itself, and the unsent
journal-287 draft letter written in this build. It is not in any earlier paper. The
sentiment is supported — the correction paper says "the paper does not say why the
pair builds 282 rather than 281 or 283" — but the quoted phrase is not the earlier
papers' "own words" as far as the build's evidence shows.

**Exact change required:** either produce the earlier-paper source of the quotation
(with page/line), or remove the quotation marks and the "in their own words"
attribution and state the point in the author's own words ("the pair is not derived;
no earlier paper derives it").

### B14. The correction paper is misdescribed: the deposited file still says "Draft" and its script cannot run from the deposit — §9, L505–512; Appendix B, L668–700

§9: "The correction is deposited as its own paper \cite{Correction24329543}". True
that a version is deposited (Zenodo DOI 10.5281/zenodo.24329543, 18 Nov 2026) — but
the build's own `correction-paper-corrected-source.md` states the deposited file
"carried the line 'Status: Draft — deposit-ready, pending verification before
deposit' at its head" and that the corrected source is "**not yet deposited — Bill's
word only**". So the public record **still** says "Draft". v5 does not disclose this.
Likewise, Appendix B says "Correction-paper script: Standalone version runs 75/75
from its own file" — but the standalone script is **not** the deposited script: the
deposited (original) script reads six primary files that were not deposited and
cannot run from the deposit (Round 1, confirmed by reading its code). A reader who
follows v5's citation finds a "Draft" paper whose script does not run.

**Exact change required:** in §9 and Appendix B, state plainly that the deposited
correction file still carries the "Draft" status line, that the corrected source is
undeposited, and that the 75/75 standalone script is not the deposited script. Do
not present the correction as a clean deposited record until the corrected version
is actually deposited (Bill's word only — v5 cannot fix this itself, but it must not
misdescribe it).

### B15. Bibliography: placeholders in a "submission-ready" draft, and one citation that appears wrong — Bibliography, L708–755

Five entries are author/year only, with "Full bibliographic details to be verified
against the primary source in Round 3" printed **in the bibliography itself**:
Gasperini 1986, Nurgaliev–Ponomariev 1983, Magueijo–Zlosnik–Kibble 2013, Shamir
2020 — plus Böhmer cited via PMC + equation numbers with no journal, volume, pages,
title, or DOI. A draft that prints "to be verified" in its own bibliography is not
submission-ready, and Round 2 has now done most of the verification (see §0.3):

- Gasperini 1986 → M. Gasperini, "Spin-dominated inflation in the Einstein–Cartan
  theory", Phys. Rev. Lett. **56**, 2873–2876 (1986). (Verified.)
- Nurgaliev–Ponomariev 1983 → I. S. Nurgaliev and V. N. Ponomariev, Phys. Lett. B
  **130**, 378 (1983). (Verified. Note the spelling: Ponomariev, as Popławski cites
  it; the Soviet Physics Journal translation renders it Ponomarev.)
- Magueijo–Zlosnik–Kibble 2013 → J. Magueijo, T. G. Zlosnik and T. W. B. Kibble,
  "Cosmology with a spin", Phys. Rev. D **87**, 063504 (2013). (Verified.)
- Shamir 2020 → L. Shamir, "Galaxy spin direction distribution in HST and SDSS show
  similar large-scale asymmetry", Publ. Astron. Soc. Aust. **37**, e053 (2020),
  doi:10.1017/pasa.2020.46, arXiv:2011.03723. (Verified.)
- Böhmer 2018 → C. G. Böhmer, P. Burikham, T. Harko and M. J. Lake, "Does space-time
  torsion determine the minimum mass of gravitating particles?", Eur. Phys. J. C
  **78**, 253 (2018), doi:10.1140/epjc/s10052-018-5719-y, arXiv:1709.07749.
  (Verified, §0.2.)

Separately, **Kerlick73 is wrong as printed**: "G. D. Kerlick, Phys. Rev. D **7**,
3014 (1973)". Two targeted searches found no such paper. Kerlick's actual papers
are ApJ **185**, 631 (1973) (neutron stars) and Phys. Rev. D **12**, 3004–3006
(1975), "Cosmology and particle pair production via gravitational spin-spin
interaction in the Einstein–Cartan–Sciama–Kibble theory of gravity" — which is the
paper v3's bibliography correctly lists (as PRD 12, 3004, "not read directly"). v5
regressed the citation. Worse, the 1975 paper's conclusion cuts **against** the D
row: Kerlick finds the Dirac spin–spin interaction "enhances rather than opposes
singularity formation" and "enhances the energy condition" — i.e. the Dirac field as
Kerlick computes it does not bounce. The manuscript cites Kerlick for β = 9/2
without confronting that conclusion.

**Exact change required:** fill all five entries with the details above (and remove
every "to be verified in Round 3" from the bibliography); replace Kerlick73 with
Kerlick, Phys. Rev. D **12**, 3004 (1975), with its correct title — and add a
sentence in §4 confronting its conclusion (Dirac spin–spin enhances singularity
formation), since it bears directly on the sign problem and on whether D is a bounce
candidate at all.

### B16. The sign-section numbers are undocumented, and the D "cusp" dismissal is backwards — §4, L272–310; §5, L311–330

- §4 asserts the normal-ordered spatial spin square is "−(3/8)ħ²n² in the
  non-relativistic limit and −(3/16)ħ²n² in the ultra-relativistic limit, by three
  independent methods", and the covariant average is "+8/3 and +1/8 in the same
  limits". No method is named, no derivation or citation is given, and the numbers
  appear in no script in the build. (v4's changelog says the 1/3 ratio limit was
  re-derived with explicit Dirac spinors and confirmed by Monte Carlo — but that is
  the **ratio**, not these sign values, and the re-derivation is not in this build.)
  The "+8/3" is stated without units and is 7× the magnitude of −3/8 with no
  explanation of the asymmetry. The deepest open calculation in the paper rests on
  numbers a referee cannot check.
- §4/§5 dismiss D with "on D the relativistic branch is a cusp bounce only, with no
  smooth bounce" — asserted, never explained, and §5's cross-reference ("as Section 4
  explains") points at an assertion, not an explanation. It is also backwards:
  Popławski's own Dirac-field bounce **is** cusp-like ("replacing it with a cusp-like
  bounce at a finite minimum scale factor", PRD 85, 107502 (2012)). A cusp is the
  expected Dirac shape, not a disqualification of D. If D is excluded, the reason
  must be stated (e.g. Kerlick's conclusion — see B15 — or the sign problem), not
  "cusp".

**Exact change required:** either give the derivation/citation for the −3/8, −3/16,
+8/3, +1/8 values (with units and the three methods named) or soften §4 to state
them as preliminary, undocumented results. And rewrite the D dismissal: state the
actual reason D is not adopted, or carry D as a live candidate; delete "cusp bounce
only, with no smooth bounce" as a disqualifier.

### B17. The "closed-Friedmann threshold" is invoked but never defined — §3 L224; §5 L346, L356; Fig. 1a caption

"The peak, the zero, and the closed-Friedmann threshold are three different things"
(§3); "the closed-Friedmann turning-point criterion is a geometric condition on the
scale factor, not a root of this curve, and it is marked separately in the figure"
(§5). No definition, no formula, no number, and no marker in the figure (see B6)
is given anywhere in the paper. A three-way distinction in which one term is never
defined is not a clarification — it is a promissory note repeated three times.

**Exact change required:** either define the closed-Friedmann turning-point criterion
(formula and value, for dust and for UR) and mark it in Fig. 1a, or delete all three
mentions and keep the distinction two-way (peak vs zero).

---

## NON-BLOCKING FINDINGS

### N1. The "full Fermi-gas check" is a forced agreement, not an independent verification — §5, L326–330; Abstract; Conclusion

§5 is honest about the mechanism ("because at the balance the Fermi momentum is
thirteen orders of magnitude above m_n c and the ultra-relativistic limit is exact
for practical purposes") — which is exactly why the check cannot fail: corrections
to the UR limit scale as (m_n c/p_F)² ~ 10⁻²⁶. The full Fermi-gas integration can
only confirm the same algebra the closed forms already encode, using a neutron gas
at p_F/m_n c ~ 10¹³ where the paper itself says neutrons do not survive (§3). The
Conclusion's "checked three ways: by exact algebra, by a 10,000-point grid, and by
a full Fermi-gas integration" overstates the independence: the grid checks the same
closed-form curve, and the Fermi integration checks the same UR limit asymptotically.

**Fix (discretionary):** reframe as two checks (closed-form algebra, numerically
evaluated two ways), and stop calling the Fermi integration an independent
verification of the balance. Do not present it as a physical check of a neutron gas
at the bound.

### N2. The "better than one part in 10¹²" Fermi claim exceeds what the paper's own gate proves — §5, L326

The script gates the Fermi balance at relative tolerance 10⁻⁹ (FERMI-B/W), and the
results file prints the value as "1.265625" (7 significant figures). Neither
establishes 10⁻¹². The claim is probably true (corrections ~10⁻²⁶), but the paper
does not demonstrate it.

**Fix:** either tighten the gate and print full precision, or soften to "better than
one part in 10⁹ (the gate tolerance)".

### N3. §6 torsion scale: verified arithmetic on an underived formula — §6, L407–427

The paper itself flags that "what is not yet shown is the derivation that connects
the Cartan tensor to this scalar twist, and a referee should ask for it". That is
honest. But §6 still presents T_A = 2.6935×10¹⁶ m⁻¹ (W) as a result, then doubles
it to 5.3870×10¹⁶ m⁻¹ "in the convention where the torsion is twice the spin
density" without saying which number is the paper's. A section whose formula is
admittedly underived and whose headline number is convention-ambiguous earns its
place only barely.

**Fix:** either derive T_A from the Cartan tensor, or demote §6 to an appendix
labelled "arithmetic identity, derivation outstanding", and state which convention
the paper uses.

### N4. §7 entropy ansatz: cut it — §7, L429–441

The ansatz is honestly labelled ("kept… as a calibration exercise and nothing more",
"no conclusion depends on it") — which is precisely why it should not be a section.
It also carries two inconsistent calibrations without reconciling them: matching the
maximum gives ρ_Aldred = ρ_A/2, while the least-squares fit gives 0.417 ρ_A with
4.4% RMS error. Which calibration is the paper's? Neither is used. The Four Round
Review advised excluding this material for a narrow submission; v5 kept it.

**Fix:** delete §7 (move the two calibration numbers to Appendix B as a one-line
note, or drop them). This is the scope ruling in §4 below.

### N5. Ḣ at the bounce is given for the B row only — §3, L205–210

"For the B row, Ḣ = 8.1505×10⁴⁸ s⁻² at the bounce." The W row value (4× larger,
3.2602×10⁴⁹ s⁻²) is not given, although the paper carries both normalisations "at
every step" (Abstract). Give both or neither.

### N6. "Nucleon charge radius (0.84 fm)" is the proton's radius, not the neutron's — §3, L228–232

0.84 fm is the proton charge radius (CODATA 2018: 0.8414 fm). The neutron's mean
square charge radius is negative (≈ −0.116 fm²); a neutron has no 0.84 fm charge
radius. The ratio 1.5×10¹³ is arithmetically right for 0.84 fm; the label is wrong.

**Fix:** "the proton charge radius (0.84 fm)" or "the nucleon size scale (~1 fm)".

### N7. The TOV "footnote in Appendix B" contains no TOV numbers — §3, L246–250; Appendix B

§3: "the Tolman–Oppenheimer–Volkoff calculation that remains is a footnote in
Appendix B". Appendix B's TOV row says only "Not deposited; 2% radius gap open" —
it does not give the November 18 numbers (M_max 2.060 M_⊙, R 11.46 km, 2.4% gap vs
an independent 11.71 km run). Either give the numbers in Appendix B or correct §3.

### N8. Beck comparison should name the reference value — §9, L555–560

Beck's own paper claims "perfect agreement with current WMAP data" (2009). The
manuscript's "25% above the observed value" is against the **Planck 2018** value.
Say so ("25% above the Planck 2018 value"), so the reader does not infer Beck was
wrong by his own lights.

### N9. Padilla–Saltas's conclusion cuts against the count's use of unimodular gravity — §9, L560–566

§9 cites Ellis et al. and Padilla & Saltas for priority on the unimodular setup.
Fair as priority. But Padilla & Saltas's paper argues that unimodular gravity "can
say anything more or less than GR about… the cosmological constant problem" — i.e.
it does **not** help with the vacuum problem. The manuscript uses the unimodular
framing as if it supported the count, without noting the cited paper's negative
conclusion.

**Fix:** one sentence noting that Padilla & Saltas argue unimodular gravity does not
by itself resolve the cosmological-constant problem, so the count's use of the setup
is a choice of framing, not a solution.

### N10. Small wording defects — §9, L537–549; §1; §5

- "Inside tolerance on the measured bench by 0.222 bits" (§9): 0.222 is the
  **distance from the target**, not the margin — the margin to the tolerance line is
  0.500 − 0.222 = 0.278 bits. Reword ("0.222 bits from the target, inside the
  ±0.5-bit tolerance").
- "A bound computed from the neutron mass and the spin of the electron's family"
  (§9, L549): "the spin of the electron's family" is meaningless. Delete or rewrite
  ("from the neutron mass and ħ/2 spin").
- §1's "This paper does six things…" enumeration and §10's seven-item work list are
  lists dressed as prose (see §3, Writing).

### N11. "The figure in the literature has been drawn wrong" — §5, L332

No literature figure is identified, no citation is given. Either cite the figure and
say what is wrong with it, or delete the sentence. An unsubstantiated swipe at the
literature is exactly what a hostile referee will demand substantiation for.

### N12. Writing: enumeration habit and performative-honesty tics — §§1, 5, 9, 10

The prose is mostly full, first-person, human-physicist prose, and the honesty is
real. Two habits weaken it:

- **Enumeration as structure.** §1 ("does six things… First… Sixth"), §2 ("Three
  arguments… First… Second… Third"), §9 ("Three pieces of prior work… First…
  Second… Third"), §10 (open problems "(1)…(7)"). A paper that repeatedly
  announces its own outline reads like a report, not an argument. The §1 six-point
  list should be cut or folded into flowing prose; a referee does not need a table
  of contents in the introduction.
- **Performative-honesty tics.** "I say so plainly" (Abstract), "I will not soften
  it" (§5, L395), "I am not dressing this up" (§9, L543), "the paper says so rather
  than hiding it" (Conclusion). Once is voice; four times is a tic, and it invites
  the reader to check whether the softening is in fact happening elsewhere (see
  B10, where it is).
- Title/abstract: "Pinning the Einstein–Cartan Spin-Density Bound" / "I pin down
  the spin-density bound" overstates a bound known only up to a factor of four.
  The abstract corrects itself in the next sentence; the title does not.

### N13. N* carries no error bar — §9, Table 3

Planck 2018 gives Λ with ≈1.8% uncertainty (H₀ ±0.54, Ω_Λ ±0.0056), i.e. ±0.026
bits on N* (my computation, §0.1). That does not change any verdict (0.026 ≪ 0.139
and ≪ 0.64), but N* is printed to three decimals with no uncertainty. State it:
N* = 281.778 ± 0.026 (W, measured).

### N14. The random-orientation assumption is never flagged as an assumption — §2

The paper adopts the unpolarised average ⟨S²⟩ = ħ²n²/8 without noting that spin
alignment at bounce conditions is assumed, not shown. The spin-flip section (which
addressed this) was dropped (see scope ruling, §4) — but dropping the section
should not drop the acknowledgement. One sentence in §2 or §4: "Random orientation
is assumed at the bound; the weak spin-flip rate that would establish equilibration
has not been computed."

### N15. Bibliography entries not re-verified in Round 2 — Bibliography

Verified in this round: Beck, Ellis, Padilla–Saltas, Popławski 2011, Popławski 2012,
Böhmer, Gasperini, Nurgaliev–Ponomariev, Magueijo–Zlosnik–Kibble, Shamir 2020,
Popławski 2010. **Not** re-verified against primaries here: Kopczyński 1972,
Trautman 1973, Cartan 1922, Hehl et al. 1976, Longo 2011, Land et al. 2008,
Shamir 2012, Iye & Sugai 1991, Planck 2018, CODATA 2018, Correction 2026. Round 3
must complete the bibliography pass for all of them (the manuscript already promises
this for five; extend it to all). Longo/Land/Shamir 2012 matter for B8(c).

### N16. Table 2's D row is labelled a bounce root while the text says D is not a bounce — §5, Table 2, L380–392

Table 2's caption: "x₀ the zero (flat-Friedmann bounce)" — for all rows including D
(β = 9/2). §5's text says D "is not a bounce". The script's own gate calls it
"UR x_0, D (algebraic zero only)". Fix the caption: "x₀ the zero (the flat-Friedmann
bounce on W and B; an algebraic zero only on D)".

### N17. The "4.2× more galaxies" assumes pure N^(−1/2) scaling — §8, L470–472

(30.6/15)² = 4.16 is arithmetic, but the inference assumes the cone shrinks as
N^(−1/2) with no systematics floor. The Nov 18 source itself notes the fitted axes
cluster at the Galactic poles (|b| ≈ 79°–85°), "a pattern that points to a selection
effect rather than a cosmological axis" — a systematics warning v5 drops. State the
assumption and restore the selection-effect warning.

### N18. LaTeX has never been compiled — whole manuscript

Carried from Round 1: no pdflatex/xelatex/tectonic on this VM; the manuscript has
NOT been compiled. A compile check (and a figure/caption consistency check) is owed
before any submission — Round 3, on a machine with a toolchain. (Note: B6's
caption/figure mismatch would very likely have been caught by a compiled visual
check.)

---

## NOTES (no action required; recorded for the record)

- **Miles's vacuum review — scorecard.** Verified against §9, point by point:
  - Kill log is the strongest thing — **agreed**; v5 keeps the kill/revision structure.
  - "Most math checks out (6.01e-85 shift, 4.16e83 boundary, rho_A formula, 8π/3
    identity)" — the ρ_A formula and the count arithmetic were re-verified by me;
    the 6.01e-85 shift / 4.16e83 boundary / 8π/3 identity were **not** re-checked in
    this round (they are correction-paper internals, outside v5's tables).
  - 282 misses as a prediction (36% low; Planck uncertainty ~2%) — **confirmed** by
    my recomputation (35.7% low on ratio-on-B; Planck Λ uncertainty ≈1.8%, 0.026 bits).
    But §9 never states the 36% (B11), and the abstract hides the failures (B10).
  - Closes only because the rule changed after the target moved — **partly answered**:
    §9 admits the earlier papers "did not state the rule before the target moved",
    but does not concede the floor rule's one-sidedness (B10).
  - Margin 0.64 bits thinner than earlier fixes (1.58, 1.33) — **answered in §9**,
    verbatim.
  - 282 isn't derived, "drafted, not adopted" — **sentiment supported, quotation
    not** (B13).
  - Journal paper still says 287 — **honestly reported** in §9/§10, but the
    correction is unsent (draft held, Bill's word only). Reporting is not fixing;
    that is correctly a Round 3 / Bill decision, not a v5 defect — except that the
    abstract does not mention it, which is fine.
  - Beck 2009 closer at 0.32 bits, uncited — **fixed**: cited, fairly (0.315 bits
    by my recomputation). See N8 for the WMAP caveat.
  - Unimodular setup published first (Ellis 2011, Padilla–Saltas) — **fixed**: both
    cited with correct details (2015, not 2014 as Miles wrote). See N9.
  - Popławski 2011 uncited, undercuts "torsion charges nothing" — **cited, but the
    magnitude is misstated** (B12).
  - Correction paper still says "Draft" — **not fixed, and not disclosed in v5**
    (B14).
  - Neither script ran — **partly fixed**: the standalone correction script now runs
    75/75 from its own file (re-run by me), but it is not the deposited script (B14).
  - Bounce wall NOT above Planck density (ρ_A ~10³⁸ below it) — **answered**: §3
    states the dust bound on B sits 5.30×10³⁸ below Planck; §5 states the relativistic
    reading is at/above Planck. The two readings are kept apart, which is exactly
    Miles's correction. (Note for accuracy: ρ_A(B) = 9.72×10⁵⁴ vs ρ_Pl = 5.15×10⁹³
    is a factor 5.30×10³⁸ — "about 1e38 below" is right in order of magnitude.)
- **v5 improvements over v4 worth recording.** The §9 honesty (both benches, both
  rules, margins stated), the four new citations, the recorded withdrawals (§4:
  1/24 and the MZK sign claim), the TOV demotion, and the explicit "located and
  argued, not derived" language are all real improvements. The regression is
  specific: v4's "unresolved" on the coefficient (B2) and v3's correct Kerlick
  citation (B15) were both lost in v5.
- **Popławski 2012 concedes the Planck problem himself.** "The energy density of
  matter at the bounce is a few orders of magnitude larger than the Planck energy
  density. The scenario of a big bounce within the classical ECSK theory may
  therefore be inadequate because the Planck regime is expected to be described by
  a quantum theory of gravity." (GRG 44, 1007 (2012).) §5 should cite this
  concession — it is the literature agreeing with the paper's own domain statement,
  and it strengthens §5 rather than weakening it.
- **What Round 2 did not do.** I did not re-derive the Dirac sign values (B16 —
  they are undocumented in the build), did not read Gasperini/Nurgaliev against
  their primaries (B2 — the papers were not read in this build either), did not
  compile the LaTeX (N18), and did not verify the rotating-core or axis-pipeline
  calculations (there is nothing in the build to verify them against — that is
  itself the finding, B8/B9).

---

## 4. Scope ruling (rotating core / axis test / entropy ansatz / spin-flip)

The ChatGPT Four Round Review advised excluding the rotating-core, axis-test,
entropy-ansatz and TOV material for a narrow technical-note submission. v5 kept
rotating-core and axis-test (short) and the entropy ansatz (as calibration), on the
ground that v5 is a full research draft and Bill wants the best version of "our
paper", including its kill conditions. My ruling, as the hostile reviewer:

| Material | Ruling | Reason |
|---|---|---|
| **Rotating core (§8, first half)** | **CUT the numbers; keep at most a 2–3 sentence ansatz note with no quantitative claims** (BLOCKING, B9) | The numbers are unverified, ungated, underived in v5, and the Nov 18 source itself says its earlier figures "do not reproduce". A kill condition (§10) cannot rest on them. If the calculation is ever deposited and gated, the numbers may return. |
| **Axis test (§8, second half)** | **CUT the catalogue numbers (Ganalyzer, HSC, dipole 1.6σ, Iye 1.29σ, and the SDSS fit numbers unless the pipeline is deposited and reproduced); keep one paragraph** stating the test was run, is inconclusive at the registered precision, and the pipeline is to be deposited — **or deposit the pipeline and keep them** (BLOCKING, B8) | An inconclusive result from an unreproduced pipeline is not a result a referee can use; printing four catalogue numbers that no one can reproduce invites exactly the attack this review is simulating. The kill line itself (30° / 15°) may stay, stated in full. |
| **Entropy ansatz (§7)** | **CUT** (NON-BLOCKING, N4) | Honestly labelled and harmless, but it adds nothing, carries two unreconciled calibrations, and is the kind of padding a referee cites when recommending rejection of a short paper. Deleting it costs nothing. |
| **TOV** | **Keep as is (footnote/appendix only)** | Correctly demoted. Fix N7's wording. |
| **Spin-flip section** | **STAYS OUT — do not restore** (ruling, see below) | It was in the Nov 18 manuscript on Bill's instruction with the weak rate **not computed**; v3 and v4 both dropped it; the College rounds deleted it. The Nov 18 changelog itself concedes the "about 10¹⁹" margin "is not a rate comparison" (it is bounce-time/Planck-time). Restoring an uncomputed-rate section into a paper whose standard is verified numbers would reintroduce exactly the defect Round 2 exists to catch. The only legitimate residue is one sentence acknowledging the random-orientation assumption (N14). Bill's Nov 18 instruction to keep it applied to the Nov 18 manuscript, a different, longer document; it does not oblige v5 to carry an unverified section. |

Net scope effect: v5 as revised would be §§1–6 (bound, dust, Dirac question, UR
branch, torsion scale) + §9 (vacuum count, rebuilt) + §10–11 (claim/kill/revision,
conclusion), with §7 deleted, §8 reduced to a short stated-kill-line paragraph (or
cut entirely if the pipeline is not deposited), and no spin-flip section. That is
closer to the Four Round Review's narrow technical note — which is where this paper's
actual strength lies (a careful, multi-normalisation computation of a known bound
with its domain stated honestly). The extra material as it stands weakens the paper:
every unverified number in §8 is a free attack surface that distracts from the
verified core.

---

## 5. Writing — does it read like a human physicist?

Mostly yes; the first-person voice, the recorded withdrawals, and the plain
admissions ("the paper does not pretend otherwise", "that is now the biggest
problem") read like a human physicist, not a summary. The failures are specific,
not general:

- **Passages that read like a summary / list dressed as prose:** §1's six-point
  enumeration (L45–66); §10's seven-item work list; §2's "three arguments";
  §9's "three pieces of prior work". See N12. The worst is §1: a referee does not
  need the paper to announce its own table of contents in prose.
- **AI-boilerplate / performative tics:** "I say so plainly", "I will not soften
  it", "I am not dressing this up" (N12). Also "The domain statement is the point
  of this section" (§5, L395) — throat-clearing.
- **Sentences that overstate:** Abstract "I pin down the spin-density bound"
  (N12); Abstract "Every number… is recomputed" (B7); §5 "each recovered to a part
  in 10⁷" (B5); §5 "reproduces… to better than one part in 10¹²" (N2); §9 "a
  cosmological constant of the order of eight times" (B12); §8 "none of them claims
  a detection" (B8).
- **Hedges that are dishonest by omission:** §9's floor-rule presentation (B10);
  the abstract's selective count reporting (B10); §2's "located and argued" applied
  to an explanation whose support is not in the build (B2).
- **Internal vocabulary in outward prose:** "bench", "sever bench", "pair",
  "cells", "dex", "kill condition", "University standard", "76 of 87 checks"
  (B8, B11). A referee outside the house cannot parse these. Every one needs a
  definition on first use or deletion.
- **Passages that are genuinely good and should be kept as the model:** §3's
  "The dust model is not self-consistent at the bound, and the paper does not
  pretend otherwise"; §4's sign paragraph; §10's one-paragraph claim statement.
  The fix is not a rewrite of the voice — it is deleting the lists, the tics, and
  the overstatements, and letting the existing voice carry the corrected content.

---

## 6. What Round 3 must do (checklist distilled from the blocking findings)

1. Fix Eq. (1) and the κ notation (B1). 2. Settle §2: derive s_P = 2S_B or revert
   to "unresolved" + stated-choice adoption (B2). 3. Abstract: add the sign problem
   (B3), narrow the verification claim (B7), report the full count pattern (B10).
4. Add the UR Ḣ derivation (B4). 5. Correct the grid claim (B5) and the figure
   captions / figures (B6). 6. Rebuild §8: full kill line, fixed Iye citation,
   corrected Shamir sentence, and either deposit the pipeline or cut the catalogue
   numbers; cut the rotating-core numbers or deposit them (B8, B9). 7. Rebuild §9:
   floor-rule one-sidedness, self-contained definitions, one bench, consistent N*,
   36% statement, Popławski correction, quotation fix, correction-paper disclosure
   (B10–B14). 8. Fill the bibliography and fix Kerlick (B15). 9. Document the sign
   numbers and fix the D dismissal (B16). 10. Define or delete the closed-Friedmann
   threshold (B17). 11. Apply the scope ruling (§4): cut §7, cut §8 numbers,
   spin-flip stays out. 12. Compile the LaTeX (N18) and complete the bibliography
   pass for the remaining entries (N15).

## 7. Final word to the coordinator

The manuscript's verified core — the bound in three normalisations, the three
landmarks kept apart, the UR branch algebra, the honest Planck-domain statement —
is real work and it survives hostile review. What does not survive is the frame
around it: a wrong founding equation, an adopted coefficient presented as explained
rather than chosen, a vacuum-count section that can pass without confirming anything,
and an observational section whose numbers cannot be reproduced and whose sources
are in one place misrepresented. None of these requires new physics to fix; all of
them require the author to say less, more precisely, and to cut what cannot be
shown. That is a major revision, not a rewrite — but it is major, and Round 3
should not be a light pass.
