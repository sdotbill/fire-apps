# ARXIV REVISION SPECIFICATION — ALDRED LIMIT 3.0
## Making the manuscript pass arXiv moderator screening

**Date:** 25 November 2026
**Basis:** Prime One independent adversarial audit, `ALDRED-LIMIT-3-AUDIT.md` (25 Nov 2026), and Prime Two's parallel-audit handoff + y0/x0 correction emails (25 Nov 2026, 08:58 EST).
**Audit verdict carried forward:** REVISE — not yet accepted as a final baseline.
**Purpose:** This is a complete, precise revision specification. The source manuscript files live in Prime Two's Library and are NOT accessible from this seat, so the manuscript itself was not edited. Every change below is stated exactly enough that whoever holds the source (`Aldred_Limit_3_0_Revised(1).pdf` / `aldred_limit_3.tex` / `Aldred_Limit_3_0.pdf`) can apply it verbatim.
**How to use it:** Apply items 1–8 in order. Each item states the required change, the exact replacement text (in block quotes) where the wording matters, and what must be checked in the source. Items marked **[FILL FROM SOURCE]** cannot be completed without opening the source files; they name exactly what to read and what to write down. Do not submit to arXiv until every item is applied and the pre-submission checklist at the end is signed off.
**A note on arXiv:** Endorsement covers the subject area, not the content. The moderators screen the paper on its own merits. This specification removes the identified defects (one internal inconsistency, one wrong formula, one unverified threshold, one unphysical carrier claim, one borrowed coefficient presented without conditional status, and one uncontrolled Hartree–Fock section). It does not guarantee moderator acceptance; it makes the paper defensible.

---

## 1. THE β_B TENSION — RESOLUTION AND EXACT CORRECTION TO THE β-MAP

### 1.1 Resolution (derived, not asserted)

The manuscript's own relation is **β = 2C_s**, derived from s² = C_s(ħcn)² and ε_spin = κs²/4 with κ = 8πG/c⁴ and ρ_A defined as the spin-cancellation density (audit, Critical Verification 2). Böhmer et al. give the spin invariant **S² = ħ²n²/8**.

Identifying Böhmer's S² with the manuscript's s² (in natural units c = 1, s² = C_sħ²n²) gives C_s = 1/8, hence:

> **β_B = 2C_s = 2 × (1/8) = 1/4.**

The assignment **β_B = 1 is inconsistent** with the manuscript's own definitions. β_B = 1 would require C_s = 1/2, i.e. S² = ħ²n²/2, which contradicts the stated Böhmer invariant S² = ħ²n²/8 by a factor of 4.

The factorization ⟨n²⟩ ≈ n² **cannot** supply that factor of 4, and it goes the wrong way. For a number-density operator, ⟨n̂²⟩ = ⟨n̂⟩² + Var(n̂) ≥ ⟨n̂⟩². Replacing ⟨n²⟩ by n² can only *decrease* (or, for uniform density, leave unchanged) the value; it can never *increase* it by a factor of 4. So the factorization cannot turn C_s = 1/8 into C_s = 1/2.

### 1.2 The correction (apply this)

> **Change β_B from 1 to 1/4 everywhere it appears.** The corrected β-map is:
>
> | Branch | β (corrected) | Status |
> |---|---|---|
> | β_P (primary) | 1/4 | Derived from β = 2C_s with C_s = 1/8 (conditional on C_s; see §7) |
> | β_B (Böhmer) | **1/4** | Corrected from 1. Under the shared normalization Böhmer's result **confirms** the primary value; it does not provide a distinct coefficient. |
> | β_D (Dirac) | 9/2 | Energy-coefficient comparison only. **Excluded** from the negative-stiff bounce formula (opposite pressure sign). Do not insert. |
> | β_HF (Hartree–Fock) | 3/8 | **Provisional.** Formal/illustrative only (see §8). |

Consequences that must be applied wherever they occur:
- (a) Every occurrence of "β_B = 1" becomes "β_B = 1/4". Every ρ_A value computed with β_B = 1 must be recomputed with β_B = 1/4. Since ρ_A = m²c⁴/(βπGħ²) scales as 1/β, **ρ_A(β_B = 1/4) = 4 × ρ_A(β_B = 1)**.
- (b) The β-map discussion must be rewritten: the Böhmer comparison now shows **agreement** with the primary coefficient under the shared normalization, not a contrast. Delete or rewrite any sentence that presents β_B = 1 as a distinct Böhmer coefficient, and any sentence that treats the β_P vs β_B difference as a physical distinction.
- (c) The factorization must be labelled as a closure assumption, never as an exact source identity. Insert this sentence at Eq. (2.10) (or wherever the factorization first appears):
  > "The replacement ⟨n²⟩ ≈ n² is a mean-field closure assumption, not an exact source identity: for a number-density operator ⟨n̂²⟩ = ⟨n̂⟩² + Var(n̂), so the replacement discards the variance and, for a fluctuating Fermi gas, strictly underestimates the spin term and therefore overestimates ρ_A. The magnitude of the bias is not controlled here."
- (d) If the authors wish to retain a distinct β_B = 1, they must **derive and display** an explicit factor-of-4 conversion from Böhmer's conventions to the manuscript's conventions, quoting Böhmer's original equations (equation numbers, the definitions of S and n, and the averaging). An asserted conversion is not sufficient. Until that derivation is displayed, β_B = 1 is an error and must not appear.

### 1.3 What to check in the source
- Read Eq. (2.10) and the surrounding text. Confirm the factorization is the one described above. Confirm no other factor-of-4 normalization is stated anywhere (if one is, quote it verbatim into the revision log and re-derive §1.1 with it included).
- Search the manuscript for every "β_B", "beta_B", "β = 1" and "Böhmer" occurrence. List them in the change log with the old and new value.

---

## 2. THE VERSION CONFLICT — AUTHORITATIVE-VERSION STATEMENT, COEFFICIENT DIFF, SCOPE NOTE

The audit could not resolve the version conflict because the files were not accessible. The manuscript **must** carry the following three things before submission. Do not submit while the version is ambiguous — a moderator or reader who finds two different 3.0 coefficient sets will treat the paper as unreliable.

### 2.1 Step 1 — Determine the authoritative version (do this first)
Compare the three files by (i) file modification date, (ii) whether the `.tex` compiles to the 10-page revised PDF or to the 8-page PDF, and (iii) which file contains the corrected y0 (see §4) and the corrected β-map (see §1). The authoritative version is the one that is **newest AND contains the corrected coefficients**. Record the determination in the change log with dates.

### 2.2 Step 2 — Insert the authoritative-version statement (exact text)
Insert the following as a footnote on the title page (or as the first paragraph of a short "Note on versions" section). Fill in the bracketed fields from the Step 1 determination:

> "This manuscript, Aldred Limit 3.0 (revised, 10 pages, dated 22 November 2026), is the authoritative version of the Aldred Limit 3.0. It supersedes the earlier 8-page Aldred Limit 3.0 (PDF) and the source file `aldred_limit_3.tex` [IF the .tex is the older source: state that explicitly; IF the .tex is newer than the PDF, STOP — the .tex is authoritative and this statement must be rewritten to name it, and the PDF must be re-rendered from it]. All coefficients in this paper — in particular the β-map (β_P = β_B = 1/4, β_D = 9/2, β_HF = 3/8 provisional) and the bounce density ρ_A = 4m²c⁴/(πGħ²) — are as stated in this revised version. The earlier draft is retained for the record and is not cited for any coefficient."

### 2.3 Step 3 — Coefficient diff table (fill in from the sources)
Produce the following table (as an appendix table or a clearly labelled "Version reconciliation" note). The revised-PDF column is filled from the audit handoff. The `.tex` / 8-page PDF column is **[FILL FROM SOURCE]** — open the files and fill in every cell; do not guess.

| Quantity | Revised PDF (10 pp, 22 Nov 2026) — authoritative | `.tex` / 8-page PDF — [FILL FROM SOURCE] | Disposition |
|---|---|---|---|
| β_P | 1/4 | | |
| β_B | 1/4 (corrected from 1; see §1) | | |
| β_D | 9/2 (excluded from bounce) | | |
| β_HF | 3/8 (provisional) | | |
| ρ_A formula | ρ_A = m²c⁴/(βπGħ²) = 4m²c⁴/(πGħ²) for β = 1/4 | | |
| ρ_A (neutron) | 3.89×10⁵⁵ g/cm³ | | |
| y0 formula | y0 = 9/[8β^(3/2)√π] (corrected; see §4) | | |
| x0 formula | x0 = 81/(64β²) | | |
| Eq. (3.5) β = 2C_s | Present | | |
| Eq. (5.4) y0 | Corrected (see §4) | | |

For each row, the Disposition column must state one of: **"agree"** (same in both versions), **"superseded — revised value governs"** (state the old value), or **"present only in [version]"**. Any row that is not "agree" must be explained in one sentence.

### 2.4 Step 4 — Scope note (exact text, fill in the bracketed fields)
Insert the following, immediately after the authoritative-version statement:

> "Scope note. The revised 10-page version and the earlier 8-page version (and its `.tex` source) differ in scope as follows: [FILL FROM SOURCE — state in two to three sentences what each version covers, e.g. which sections, derivations, or branches each contains, and what the revised version adds or removes]. The scope difference is [state whether the revised version is a superseding correction of the same paper, or a separate draft with a different scope — and give the one-sentence reason]. This paper is submitted as [a superseding correction / a separate draft — delete as applicable] and should be read on that basis."

**Rule:** If the determination in Step 1 is that the two versions are separate drafts with different scopes (not a superseding correction), the manuscript must not present itself as "the" 3.0 paper; it must carry a distinct version identifier (e.g. "3.0 revised" vs "3.0") and the scope note must say so.

---

## 3. THE TABLE — RECOMPUTED ENTRIES (CORRECTED y0 AND x0)

### 3.1 The corrected table (replace the manuscript's table with this)

The table below uses the **corrected** y0 = 9/[8β^(3/2)√π] and x0 = 81/(64β²), verified exactly (SymPy: y0 − claimed = 0, x0 − claimed = 0; both x-expressions agree numerically at y0 for all four β). Values are given to 6 decimal places; the manuscript may round to the precision its table uses, but the rounded values must round from these, not from the old ones.

| β | y0 (corrected) | x0 (corrected) | y0 (OLD — WRONG, do not use) | y0 change factor (corrected ÷ old) |
|---|---|---|---|---|
| 1/4 | **5.077706** | **20.250000** | 1.465808 | 3.464102 (= 2√3) |
| 1 | **0.634713** | **1.265625** | 0.366452 | 1.732051 (= √3) |
| 3/8 | **2.763953** | **9.000000** | 0.977205 | 2.828427 (= 2√2) |
| 9/2 | **0.066490** | **0.062500** | 0.081434 | 0.816497 (= √(2/3)) |

Formulas: y0 = 9/[8β^(3/2)√π]; x0 = 81/(64β²). The y0 change factor is √3/√β (β-dependent — this is **not** a uniform rescaling, so the table cannot be fixed by multiplying by a single constant).

### 3.2 What changes vs the old y0 (apply all of these)
- (a) **The y0 column must be replaced in full.** All four entries change. The old y0 = 9/[8√(3π)·β] is wrong (it fails the defining equality by the factor 3^(1/3)/β^(1/3) ≠ 1). Do not propagate the old expression anywhere.
- (b) **The x0 column: check which case applies, then act.**
  - If the manuscript's x0 column already reads 81/(64β²) (20.25, 1.265625, 9.0, 0.0625), it is correct and **unchanged**.
  - If the manuscript's x0 column was computed from the old y0 via x0 = βπy0², then it reads 81/(192β) — i.e. 1.687500, 0.421875, 1.125000, 0.093750 — and it is **wrong** and must be replaced with the corrected values above. The correction factors (corrected ÷ from-old-y0) are 3/β: 12.0000 (β=1/4), 3.0000 (β=1), 8.0000 (β=3/8), 0.6667 (β=9/2).
  - The holder must state in the change log which case applied.
- (c) **Any other column derived from y0 or x0** (in particular any SEC-crossing value, any threshold density, or any quantity computed from y0) must be **recomputed from the corrected y0/x0**, not carried over. The SEC crossing and any table entries that depend on Eqs. (5.1)–(5.5) are **[FILL FROM SOURCE]** — recompute them from the corrected values once the source equations are open, and record the old and new values in the change log.
- (d) **The β = 3/8 row must be labelled in the table itself.** Add the label "(formal — provisional energy-functional extrapolation; see §8)" to the β = 3/8 row. It must not be presented alongside the derived rows without that label. If the Hartree–Fock section (see §8) shows the β = 3/8 value is a controlled result after all, the label may be removed — but only with the derivation cited.
- (e) Add a table note (exact text):
  > "y0 and x0 are the ultrarelativistic threshold values from Eqs. (5.1)–(5.5), with y0 = 9/[8β^(3/2)√π] and x0 = 81/(64β²). An earlier version of this table used the incorrect y0 = 9/[8√(3π)·β]; all y0 entries (and any x0 entries derived from it) have been recomputed. The β = 3/8 row is a formal/provisional energy-functional extrapolation (see the Hartree–Fock section)."

---

## 4. EQ. (5.4) — EXACTLY WHAT THE TYPESET EQUATION MUST PRINT

Eq. (5.4) is the equation that states the ultrarelativistic threshold y0 (and x0). It must print the **corrected** expressions. Verify it by reading the typeset PDF (not the `.tex` alone — confirm the rendered output).

### 4.1 Required printed form
Eq. (5.4) must print:

> **y₀ = 9 / [8 β^(3/2) √π]**  and, if the equation also states x₀,  **x₀ = 81 / (64 β²)**.

In LaTeX:

```latex
y_0 = \frac{9}{8\,\beta^{3/2}\sqrt{\pi}}, \qquad
x_0 = \frac{81}{64\,\beta^{2}}.
```

It must **NOT** print the old (wrong) expression:

> y₀ = 9 / [8 √(3π) · β]  — **WRONG. Do not use. Do not propagate.**

### 4.2 The defining equality (for verification)
The threshold is the equality of the two expressions stated in the correction email:

> (3/4)(3π²)^(1/3) y^(4/3) = βπ y².

Solving gives y0 = 9/[8β^(3/2)√π] and x0 = 81/(64β²). The holder must verify, by substituting the printed y0 into this equality, that it holds exactly (LHS/RHS = 1) for each β in the table. The old y0 fails this check by the factor 3^(1/3)/β^(1/3) (e.g. 2.289 for β = 1/4, 1.442 for β = 1, 2.000 for β = 3/8, 0.874 for β = 9/2).

### 4.3 What to check in the source
- Open the typeset PDF at Eq. (5.4). Read the printed y0. If it prints the old expression, replace it with §4.1 and re-render.
- Check **every** other equation that uses y0 or x0 (in particular Eqs. (5.1)–(5.5) and any equation that references the threshold). Each must use the corrected y0. List them in the change log.
- If Eq. (5.4) is not the y0 equation (i.e. the manuscript numbers it differently), apply §4.1 to whichever equation states y0, and note the correct equation number in the change log.

---

## 5. THE CLOSED-FLRW THRESHOLD — DERIVATION AND EXACT CORRECTED STATEMENT

### 5.1 Derivation from first principles (Friedmann + conservation + spin-corrected density)

Define the spin-corrected effective density **ρ_eff = ρ(1 − ρ/ρ_A)**, where ρ is the (mass) density and ρ_A is the bounce density. The Friedmann equation is H² = (8πG/3)ρ_eff − kc²/a².

- **Flat (k = 0).** H² = (8πG/3)ρ_eff. H = 0 at ρ = 0 and at **ρ = ρ_A** (the nonzero root — the bounce).
- **Maximum effective density.** ρ_eff is a parabola in ρ. dρ_eff/dρ = 1 − 2ρ/ρ_A = 0 at ρ = ρ_A/2, giving **ρ_eff,max = ρ_A/4**. Hence **ρ_eff ≤ ρ_A/4 always**, with equality only at ρ = ρ_A/2.
- **Closed (k = +1).** H² = (8πG/3)ρ_eff − c²/a². A bounce (H = 0) requires ρ_eff = 3c²/(8πGa²). Since ρ_eff ≤ ρ_A/4, this requires 3c²/(8πGa²) ≤ ρ_A/4, i.e. **a ≥ a_min = √(3c²/(2πGρ_A))**. Below a_min no bounce is possible.
- **Friedmann admissibility interval.** H² ≥ 0 requires ρ(1 − ρ/ρ_A) ≥ 3c²/(8πGa²). Solving the quadratic equality gives the two roots
  > **ρ_±(a) = (ρ_A/2)·[1 ± √(1 − 3c²/(2πGρ_A·a²))]**.
  > The admissible densities at scale factor a form the interval **ρ ∈ [ρ_-(a), ρ_+(a)]**, non-empty iff a ≥ a_min. At a = a_min the interval collapses to the single point ρ = ρ_A/2; as a → ∞ it widens to [0, ρ_A]. The turning-point (bounce) density lies at one of the endpoints ρ_±(a); on the high-density branch ρ_b = ρ_+(a) ≥ ρ_A/2.

### 5.2 Verdict on "ρ > ρ_A/4"
The number ρ_A/4 appears in this problem as the **maximum of the effective density** (ρ_eff ≤ ρ_A/4), **not** as a threshold on the physical density ρ. As a universal threshold on ρ, "ρ > ρ_A/4" is **not derivable**: the lower admissibility root ρ_-(a) can be below ρ_A/4 (for large a) or above it (for small a) — it is a-dependent. The only universal ρ-threshold statements are (a) the bounce on the high-density branch has ρ_b = ρ_+(a) ≥ ρ_A/2 > ρ_A/4, and (b) ρ_eff ≤ ρ_A/4 always. A bare "ρ > ρ_A/4" must therefore be replaced by the precise interval statement in §5.3.

### 5.3 Exact corrected statement (insert in the manuscript, replacing any bare "ρ > ρ_A/4")
Insert the following, replacing the manuscript's closed-FLRW threshold paragraph (and any sentence that states a bare "ρ > ρ_A/4"):

> "For the closed (k = +1) Friedmann model with the spin-corrected effective density ρ_eff = ρ(1 − ρ/ρ_A), the Friedmann equation is H² = (8πG/3)ρ_eff − c²/a². A bounce is possible only for scale factor a ≥ a_min = √(3c²/(2πGρ_A)). At fixed a ≥ a_min the Friedmann-admissible densities form the interval ρ ∈ [ρ_-(a), ρ_+(a)] with ρ_±(a) = (ρ_A/2)[1 ± √(1 − 3c²/(2πGρ_A·a²))]; the interval collapses to the single point ρ = ρ_A/2 at a = a_min and widens to [0, ρ_A] as a → ∞. The effective density satisfies ρ_eff ≤ ρ_A/4, with equality at ρ = ρ_A/2. The turning-point (bounce) density lies at one of the endpoints ρ_±(a); on the high-density branch ρ_b = ρ_+(a) ≥ ρ_A/2. No universal threshold of the form ρ > ρ_A/4 on the physical density is asserted."

### 5.4 Density bookkeeping (mandatory check)
ρ_A is a **mass density** (ρ_A = m²c⁴/(βπGħ²) has units ML⁻³). Therefore ρ in every equation that uses ρ_A must be a **mass density**. The holder must check the manuscript line by line: any step that uses ρ_A as an energy density, or that mixes mass density and energy density without an explicit c² conversion, is a dimensional error and must be corrected. Verify all c-factors at each step of the closed-FLRW derivation. Record the check in the change log.

---

## 6. THE CARRIER — RE-SPECIFICATION AND EXACT LIMITING LANGUAGE

### 6.1 The problem (numbers)
For a neutron mass, ρ_A(β = 1/4) ≈ **3.89×10⁵⁵ g/cm³**. Nuclear saturation density is ≈ 2.8×10¹⁴ g/cm³. The ratio is ≈ **1.4×10⁴¹** — the bounce density is ~41 orders of magnitude above nuclear saturation. Neutrons dissolve into quark matter at a few times nuclear saturation (~10¹⁵ g/cm³), orders of magnitude below ρ_A. **No known hadron, and no neutron, can exist at ρ_A.** The manuscript must not claim a neutron (or any known particle) is the carrier at the bounce density.

### 6.2 The re-specification (apply this)
Re-specify the carrier as a **formal mass parameter**. The mass m entering ρ_A = 4m²c⁴/(πGħ²) is a formal scale, not the mass of a physical particle present at the bounce density. Do not name a specific particle as the carrier at ρ_A.

### 6.3 Exact limiting language (insert where the carrier is introduced AND where ρ_A is first quoted numerically)
Insert the following paragraph at the first introduction of the carrier and at the first numerical quotation of ρ_A:

> "The mass m entering ρ_A = 4m²c⁴/(πGħ²) is a formal mass parameter, not the mass of a physical neutron (or of any known particle) present at the bounce density. For m equal to the neutron mass, ρ_A ≈ 3.9×10⁵⁵ g/cm³, which is ~10⁴¹ times nuclear saturation density (~2.8×10¹⁴ g/cm³). No known hadron survives at such a density; neutrons dissolve into quark matter orders of magnitude below it. The bounce density quoted here is therefore a formal scale set by the parameter m, and the physical carrier at that density — if any — is not identified in this work. No claim is made that a neutron, or any Standard Model particle, is the carrier at ρ_A."

### 6.4 Rules (apply throughout)
- (a) Delete or rewrite every sentence that calls a neutron (or any specific particle) "the carrier" at ρ_A. Replace with "the formal mass parameter m" or "a formal carrier mass m".
- (b) Every numerical ρ_A value must be quoted with the m it assumes, e.g. "ρ_A ≈ 3.9×10⁵⁵ g/cm³ for m = m_n" — never as a bare number.
- (c) The abstract and conclusions must not state or imply that a physical particle carries the bounce. If the abstract currently names a carrier, rewrite it to name the formal parameter.
- (d) If the authors wish to propose a specific beyond-Standard-Model carrier, that is a new physical claim: it requires its own derivation/justification and must be labelled as a hypothesis, not stated as a result. It is out of scope for this revision unless that derivation is supplied.

---

## 7. THE BORROWED C_s = 1/8 — EXACT CONDITIONAL-STATUS PARAGRAPH

C_s = 1/8 is taken from Böhmer et al. and is **not derived** in this work. It is the standing blocking MAJOR from the v5 review, and it underpins the entire factor-four correction (β = 2C_s, β = 1/4, ρ_A = 4m²c⁴/(πGħ²)). The manuscript must carry its conditional status explicitly. A moderator who finds a load-bearing coefficient presented as derived when it is borrowed will flag the paper.

### 7.1 Exact conditional-status paragraph (insert at the first use of C_s = 1/8 / β = 1/4, AND in the conclusions)
Insert the following paragraph verbatim (fill in the citation to Böhmer et al. with the manuscript's reference number):

> "The spin-invariant coefficient C_s = 1/8 is taken from Böhmer et al. [ref] and is not derived in this work. Every result that depends on it — in particular the relation β = 2C_s, the value β = 1/4, and the bounce density ρ_A = m²c⁴/(βπGħ²) = 4m²c⁴/(πGħ²) — is conditional on that input. If the correct spin invariant differs, the coefficient rescales as β = 2C_s and ρ_A = m²c⁴/(2πC_sGħ²), so ρ_A is inversely proportional to C_s; for example, C_s = 1/32 would give β = 1/16 and a ρ_A four times larger than quoted here. The derivation of C_s from the microscopic spin current and the action conventions is left as an open problem; until it is supplied, the numerical values of β and ρ_A in this paper are conditional, not derived."

### 7.2 Rules (apply throughout)
- (a) The abstract and introduction must not present β = 1/4 or ρ_A as derived results. If they do, rewrite them to state the conditional status (e.g. "taking C_s = 1/8 from Böhmer et al., we obtain β = 1/4 and ρ_A = …").
- (b) The conclusions must repeat the conditional status in one sentence (the paragraph in §7.1, or a one-sentence pointer to it).
- (c) Do not delete or soften this paragraph to make the paper read more strongly. Its presence is what makes the paper honest and therefore publishable as a preprint.

---

## 8. HARTREE–FOCK — EXACT PRESSURE-CHOICE AND RENORMALIZATION-CONTROL LANGUAGE; HF STAYS EXPLORATORY

The Hartree–Fock (HF) section is **exploratory**. It is not a controlled prediction and must not be presented as one. Two specific gaps must be closed with explicit language (and, where the source permits, with the actual choice stated).

### 8.1 Exact language to insert (at the start of the HF section)
Insert the following at the start of the Hartree–Fock section:

> "The Hartree–Fock results in this section are exploratory and are not presented as controlled predictions. Two points are stated explicitly. (1) Pressure. The pressure that enters the Friedmann equation is the spatial trace of the Belinfante–Rosenfeld symmetrized stress tensor, which carries the local spin contribution; the pressure that enters the conservation equation is the thermodynamic pressure p = −∂F/∂V derived from the free energy. These two pressures need not agree when spin–torsion couplings are present. This work uses **[FILL FROM SOURCE: state which pressure is used in the Friedmann equation]** in the Friedmann equation and **[FILL FROM SOURCE: state which pressure is used in the conservation equation]** in the conservation equation. [FILL FROM SOURCE: either state 'Their agreement is shown in Eq. (X)' with the equation number, or state the justification for the difference in one to two sentences.] If the two pressures are used inconsistently, the system is not closed. (2) Renormalization. The spin-squared term is a composite operator (a product of fields at one point) whose expectation value requires renormalization, and the mean-field factorization ⟨n²⟩ ≈ n² is an uncontrolled approximation. Any cancellation between large terms at the Planck scale is scheme-dependent and is not controlled evidence for a physical bounce. The Hartree–Fock numbers (I₀, I_m, x_F*, and the benchmark values) are therefore formal and illustrative, pending a controlled renormalization. They are not used to support any claim that a bounce occurs."

### 8.2 Rules (apply throughout)
- (a) The HF section must carry an **"Exploratory"** label in its heading or its first sentence. No HF number (I₀, I_m, x_F*, any benchmark value, or β_HF = 3/8) may be cited in the abstract, introduction, or conclusions as a prediction or a result. If any is, delete it or move it into the HF section with the exploratory label.
- (b) The β_HF = 3/8 entry in the β-map and in the table (see §3.2(d)) must be labelled **"provisional"** wherever it appears.
- (c) Any sentence that presents a Planck-scale cancellation as evidence for a physical bounce must be deleted or rewritten to state that it is scheme-dependent and not controlled evidence.
- (d) The HF quantities I₀, I_m, the energy and pressure expressions, x_F*, and the benchmark values must be **reproduced** (re-derived and numerically checked) once the source is open. If any cannot be reproduced, it must be removed or marked "not reproduced" in the change log. **[FILL FROM SOURCE — reproduction blocked until the HF section is open.]**

---

## PRE-SUBMISSION CHECKLIST (all must be ticked before arXiv submission)

- [ ] §1 applied: β_B = 1/4 everywhere; β-map corrected; factorization labelled as a closure assumption; change log lists every β_B occurrence.
- [ ] §2 applied: authoritative version determined and stated; coefficient diff table filled (both columns); scope note completed; the version is unambiguous.
- [ ] §3 applied: table replaced with the corrected y0/x0 values; x0 case (already-correct vs derived-from-old-y0) determined and recorded; β = 3/8 row labelled; table note inserted; SEC-dependent entries recomputed.
- [ ] §4 applied: Eq. (5.4) verified in the typeset PDF to print the corrected y0 (and x0); every other equation using y0/x0 checked.
- [ ] §5 applied: closed-FLRW threshold replaced with the interval statement; density bookkeeping (mass vs energy density, c-factors) checked line by line.
- [ ] §6 applied: carrier re-specified as a formal mass parameter; limiting paragraph inserted at both required places; no sentence names a physical particle as the carrier at ρ_A; every ρ_A value carries its m.
- [ ] §7 applied: conditional-status paragraph inserted at first use and in the conclusions; abstract/introduction do not present β or ρ_A as derived.
- [ ] §8 applied: HF section labelled Exploratory; pressure choice stated and justified; renormalization control stated; no HF number cited as a prediction outside the HF section; β_HF labelled provisional.
- [ ] A complete change log exists, listing every change (old → new) with equation/table/section references, and every **[FILL FROM SOURCE]** item resolved or explicitly carried as an open item.
- [ ] The manuscript has been re-read whole (not just the changed lines) for consistency: no remaining occurrence of the old y0, of β_B = 1, of a physical-particle carrier at ρ_A, or of an unconditional C_s = 1/8.
- [ ] References verified: Böhmer et al., Poplawski, Kopczyński, and every cited paper checked against the equations attributed to them (audit item 10 — blocked until the sources are open; do not submit with unverified citations to load-bearing equations).
- [ ] The novelty framing is correct: the contribution is normalization/reconciliation and corrected thresholds, not a new bounce mechanism (the bounce is Kopczyński–Trautman 1972–73 / Poplawski prior work). No sentence claims a new bounce mechanism.

## WHAT IS STILL BLOCKED ON THE SOURCE FILES (carried explicitly, not silently absent)
- The version-conflict diff (§2.3) and scope note (§2.4) — need the three source files open.
- Verification that typeset Eq. (5.4) prints the corrected y0 (§4.3) — need the PDF.
- The closed-FLRW equations as typeset and the c-factor / density bookkeeping (§5.4) — need the PDF/.tex.
- The SEC crossing and any table entries depending on Eqs. (5.1)–(5.5) (§3.2(c)) — need the source equations.
- The HF reproductions (I₀, I_m, energy/pressure, x_F*, benchmarks) and the pressure choice (§8) — need the HF section.
- Citation verification against the cited papers (checklist, last two items) — need the manuscript and the cited papers.
- The factor-of-4 conversion that could retain β_B = 1 (§1.2(d)) — need Böhmer's original equations; until it is displayed, β_B = 1/4 governs.

## SOURCES USED FOR THIS SPECIFICATION
- `~/workspace/your_files/aldred-limit-3-audit-2026-11-25/ALDRED-LIMIT-3-AUDIT.md` (Prime One audit, 25 Nov 2026).
- `~/workspace/email/gmail/1a213006d5ccec79.md` (Prime Two parallel audit handoff, 25 Nov 2026 08:58 EST).
- `~/workspace/email/gmail/1a2130090ce7e1b1.md` (Prime Two y0/x0 correction, 25 Nov 2026 08:58 EST).
- Numerical verification (this session): corrected y0/x0, old-y0 ratios, ρ_A, k_A, R_dS, and the closed-FLRW admissibility interval were recomputed numerically and symbolically (SymPy) from the stated formulas; all agree with the audit.
- No source manuscript file was opened. No manuscript content is quoted beyond the formulas and claims stated in the two emails and the audit report.
