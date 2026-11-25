# Aldred Limit v5 — Round 1 Report
**19 November 2026. Coordinator: Prime (subagent). Status: Round 1 manuscript complete; Round 2 adversarial review dispatched.**

## What was built

`aldred-limit-v5.tex` (755 lines) — the full manuscript in first-person,
human-physicist prose. Base: Miles v4 structure (most complete, most
honest) + Claude v3 prose + ChatGPT final manuscript's discipline
(C as a parameter, thresholds kept distinct, no novelty claim) + the
November 18 package's rotating-core and axis-test material, kept short
and labelled ansatz-level. Grok v1/v2 are superseded by v3/v4 and were
used only as a cross-check (their B-normalisation numbers agree with
the recomputation).

## Design decisions (recorded for the reviewers)

1. **Adopted normalisation: W (β = 1/4).** B (β = 1) carried beside it
   at every step. D (β = 9/2) carried in the tables, not adopted.
2. **Factor of four: "located and argued, not independently confirmed."**
   v3 said "located and argued"; v4 said "unresolved — I couldn't find
   where it comes from." Both are true: the factor sits in the prefactor
   (κ/4 vs κ) applied to the same average, and the proposed explanation
   (s_P = 2S_B) is an argument, not a confirmed derivation. The
   manuscript states this on its face in §2.
3. **Scope: rotating core + axis test kept, short.** The Four Round
   Review advised excluding them for a narrow technical-note submission.
   v5 is a full research draft and Bill wants the best version of OUR
   paper, which includes its kill conditions. Round 2 is asked to attack
   this scope choice directly.
4. **Spin-flip section NOT carried.** It is in the November 18 manuscript
   on Bill's instruction, with the weak rate not computed. v3 and v4 both
   dropped it. It is listed in Appendix B as an open item for Round 2 to
   rule on — it was not silently deleted.
5. **TOV is a footnote.** The November 18 TOV numbers (M_max 2.060 M⊙,
   R 11.46 km, 2.4% radius gap vs an independent 11.71 km run, solver
   not deposited) are not strong enough to carry in the body.
6. **Vacuum count: both benches, both rules.** The tolerance rule
   (|T − N*| ≤ 0.5) and the floor rule (smallest integer ≥ N*) are
   stated separately, with the table showing 282 passes on W/measured
   (0.222) and fails on W/sever (1.108) and on ratio-on-B/measured
   (0.139 beyond the line). The pair is called "drafted, not adopted"
   in the paper's own words.
7. **Miles's "1/24" withdrawn in §4.** The repair paper computed a
   ratio, not an absolute coefficient. The Magueijo–Zlosnik–Kibble
   sign claim is likewise withdrawn in §4.
8. **Böhmer verified against the primary source.** PMC5866282: Eq. (19)
   S² ≡ ½S_μνS^μν ≥ 0; Eq. (22) ρ_eff = ρ − κ²S²; Eq. (23)
   p_eff = p − c²κ²S²; Eq. (41) S² = (1/8)ħ²n²; Eq. (18)
   T^λ_μν = κ²u^λS_μν. Miles's reading is confirmed.

## Verification — all run, all passing

| Check | Result |
|---|---|
| `scripts/v5_verify.py` (new suite, CODATA 2018, 50 digits) | **73/73 gates PASS, exit 0** |
| The 10000 run (10,000-point grid, UR landmarks, W + B) | 8/8 gates; landmarks recovered to ~1e-7 |
| Full T=0 Fermi-gas balance (mpmath findroot) | B 1.265625, W 20.25 — agrees with UR limit to <1e-12 (printed precision) |
| ChatGPT reproducibility script (supplied) | exit 0, all values match its Four Round Review |
| Correction paper, original script (workspace copy) | 75/75 PASS, exit 0 |
| Correction paper, standalone script (new) | **75/75 PASS, exit 0; values identical to original** |
| Citation keys | all 22 cited keys present in bibliography; no orphans |

### The 10000 run — what it is
No 10,000-scale mode exists in any supplied script or workspace file.
The reproducibility script computes closed forms only. A targeted grep
found only `ko_09_compute.py` (tests v in [2, 10, 100, 10000]) — KO-09
is the pending barrier-height knock-out item, not Aldred Limit
verification. The build therefore CONSTRUCTED the 10,000 run: a
10,000-point grid evaluation of the ultra-relativistic curve
y = x − αx^{3/2} for both prescriptions, recovering the maximum, the
root, and the SEC onset numerically. It is labelled as constructed in
`v5_verify.py` §3 and in this report. It is not presented as a
pre-existing artifact.

### Bugs found and fixed during verification (all in my own new code)
- Grid unpack swapped x/y maxima (values were right, labels swapped).
- Torsion formula: my (1/2)κs_A form scaled with n_A (ratio 4); the
  house form T_A = m_n c/(ħ√coef) scales with √ρ_A (ratio 2) and
  reproduces both v4 numbers exactly. The manuscript uses the house
  form and flags that the Cartan-tensor derivation is still to be shown.
- de Sitter radius: √(3β) → √(3β/8) (coef = β/8); now matches both rows.
- Galactic conversion: wrong longitude formula (l_ω = 32.932° added);
  corrected to the standard l_NCP = 122.932° form. Cold Spot (207°, −56°),
  axis (192°, +79°) now reproduce.
- Axis separation: the fitted axis is undirected — separation is
  min(sep, 180° − sep) = 44.7°, matching the paper's 44.6° on rounded inputs.
- Count conversion: GeV⁴ per g/cm³ is a division, not a multiplication
  (was off by 115 bits); fixed.
- Sever-bench W row: +log₂(4/3), not +2 bits (283.108, not 284.693).

## Miles's vacuum review — every point answered in the build

| Point | Where answered |
|---|---|
| Kill log is the strongest thing | §1, §9, §10 keep the kill/revision structure front and centre |
| 282 misses as a prediction (36% low, ~2% Planck uncertainty) | §9: "36% low against the measured density"; miss of 0.139 bits beyond the tolerance line stated |
| Closes only because the rule changed after the target moved | §9: both rules stated; "the closure rests on which rule is stated, and the earlier papers did not state the rule before the target moved" |
| Margin 0.64 bits thinner than earlier fixes (1.58, 1.33) | §9, verbatim |
| 282 isn't derived — "drafted, not adopted" | §9, quoted |
| Journal paper still says 287 | §9 + `journal-287-update-DRAFT-NOT-SENT.md` (drafted, NOT sent) |
| Beck 2009 closer at 0.32 bits, uncited | §9 cites Beck; script gate BECK-BITS = 0.3146 |
| Ellis 2011 + Padilla–Saltas 2014 first (unimodular) | §9 cites both (verified: CQG 28, 225007 (2011); EPJC 75, 561 (2015)) |
| Popławski 2011 uncited, undercuts "torsion charges nothing" | §9 cites it (verified: Ann. Phys. 523, 291 (2011)); the undercut is stated |
| Correction paper still says "Draft" | `correction-paper-corrected-source.md` — status line fixed; body diff is line 10 only, verified by script |
| Neither script ran (one fails on deposited results, one needs private files) | `scripts/correction_paper_compute_standalone.py` — 75/75 from its own file, values identical to the original; the original fails from its deposit because it reads six primary files that were not deposited (confirmed by reading its code: PROOF/SEVER/C84/AUDIT_PY/AUDIT_OUT/VAPER/DESIGN are read at import) |
| Bounce wall NOT above Planck density — ρ_A ~1e38 BELOW it | §3: "the dust bound on B sits 5.30×10³⁸ below [Planck]"; §5: the relativistic reading is at/above Planck — the two readings are kept apart, which is exactly Miles's correction |

## Files in this build directory

- `aldred-limit-v5.tex` — Round 1 manuscript (755 lines)
- `figures/fig1a_ur_branch_v5.png`, `fig1b_dust_v5.png` — regenerated
  from the verified numbers (matplotlib, 300 dpi); source PNGs carried
  in `figures/` for comparison
- `scripts/v5_verify.py` + `v5_verify_results.json` — 73/73
- `scripts/correction_paper_compute_standalone.py` +
  `correction_paper_results_standalone.json` — 75/75
- `correction-paper-corrected-source.md` — status label fixed, body
  otherwise verbatim (diff = line 10 only)
- `journal-287-update-DRAFT-NOT-SENT.md` — draft letter to Gravitation
  and Cosmology editors (NOT sent — Bill's word only)
- `rounds/ROUND-1-REPORT.md` — this file
- `sources/` — all supplied source files, copied whole

## Known limitations (for Rounds 2–4)

- **No LaTeX toolchain on this VM** (no pdflatex/xelatex/tectonic) —
  the manuscript has NOT been compiled. A compile check is owed before
  any submission (Round 3 or 4, on a machine with a toolchain).
- **Bibliography partially unverified.** The four new citations (Beck,
  Ellis, Padilla–Saltas, Popławski 2011) were verified by web search.
  Five older entries are cited by author/year only (Gasperini 1986,
  Nurgaliev–Ponomariev 1983, Magueijo–Zlosnik–Kibble 2013, Shamir 2020)
  and are flagged in the .tex for a primary-source pass in Round 3.
  The Böhmer entry cites PMC5866282 + equation numbers, verified.
- **Axis-fit pipeline outputs not reproduced** (pipeline not in the
  workspace). The manuscript says so; the University standard is
  76/87 = 87%, below the 90% line, for exactly this reason.
- **TOV solver not deposited; 2% radius gap open.** Footnote only.
- **Kretschmann scalar (rotating model) not computed.**
- **Torsion-scalar derivation not shown** (T_A is verified arithmetic).
- **Dirac evaluation (sign) not done** — the deepest open calculation.
- **Junction conditions missing** — no black-hole interior solution.
- **Spin-flip section** not carried (see decision 4 above).
