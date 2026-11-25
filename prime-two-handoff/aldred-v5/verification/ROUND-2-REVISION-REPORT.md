# Round 2 Revision Report — Aldred Limit v5 (second revision)

**Date:** 19 November 2026
**Manuscript:** `aldred-limit-v5.tex` (826 lines, full rewrite of the Round 1 draft)
**Review answered:** `rounds/ROUND-2-REVIEW.md` (17 blocking B1–B17, 18 non-blocking N1–N18)
**Verification:** `scripts/v5_verify.py` — **77/77 gates PASS**, exit 0 (re-run after the rewrite)
**Figures:** `figures/fig1a_ur_branch_v5.png`, `figures/fig1b_dust_v5.png` — regenerated from the script numbers

## What the rewrite is

Not a patch. The Round 1 draft was rewritten end to end in full prose: new title,
new abstract, new §1, rewritten §2 (adoption), §3 (dust), §4 (Dirac), §5 (UR),
§6 (torsion), §7 (axis/rotating, cut to two paragraphs), §8 (vacuum count,
rebuilt with two tables), §9 (claim/kill/open problems, prose), §10 (conclusion),
Appendices A/B, and a rebuilt bibliography. The six-point §1 enumeration, the
performative tics, and the "Pinning…" title are gone.

## Blocking findings — disposition

- **B1 (Eq. 1 wrong).** Fixed. One coupling defined once, $\kappa^2 = 8\pi G/c^4$;
  Eq. (1) is $\rho_{\mathrm{eff}} = \rho - \kappa^2\langle S^2\rangle$ (Böhmer Eq. 22);
  the W form is $(\kappa^2/4)\langle S^2\rangle$ with the Hehl energy-density
  form shown to convert to it. Unified form Eq. (3), bound Eq. (4).
- **B2 (W adoption unjustified).** Fixed by option (b): reverted to v4's honest
  "unresolved" + stated-choice adoption, using v4's exact reasons (sourcing:
  coefficient with averaging stated together in the peer-reviewed literature;
  consistency: $\rho_{\mathrm{KT}} = 1.675\times10^{74}$ eV$^4$ = $\rho_A c^2$
  for $\beta=1/4$). The "three arguments" paragraph is deleted. The $s_P = 2S_B$
  mechanism is recorded as an unrun conjecture, with the primaries-unread
  caveat stated. The count played no part in the choice.
- **B3 (sign problem absent from abstract; misclassified).** Fixed. Abstract
  carries one sentence ("A normal-ordered Dirac evaluation gives a negative
  spin-squared sign that would remove the bounce entirely; that evaluation
  has not been done."); the negative-sign case is now the second kill
  condition in §9.
- **B4 (UR "bounce" never shown).** Fixed. The three-line $\dot H$ computation
  is in §5 (at the zero $p_{\mathrm{eff}} = -2\varepsilon/3$,
  $\varepsilon_{\mathrm{eff}} + p_{\mathrm{eff}} = -2\varepsilon/3 < 0$,
  so $\dot H > 0$) and in Appendix A. Script gate HDOT added.
- **B5 (grid claim false).** Fixed. §5 and Appendix B now read "root and SEC
  onset to about a part in $10^7$–$10^8$, maximum to about a part in $10^5$
  (grid-step limited)".
- **B6 (figures vs captions).** Fixed. Fig. 1a carries the dashed negative
  continuation and the closed-model threshold marker at $(1/4, 1/8)$; Fig. 1b
  is replotted in unscaled variables (B: $z(1-z)$, W: $z(1-z/4)$). Captions
  match the figures.
- **B7 ("Every number … is recomputed" false).** Fixed. Abstract now reads
  "Every number in Tables 1–4 is recomputed from CODATA 2018 constants by a
  script that runs from the deposited files alone; the observational numbers
  in §7 are not covered by that script."
- **B8 (axis test).** Fixed. Full kill line (30°/15°) stated in §7 and §9;
  catalogue numbers cut per the scope ruling; "76 of 87" deleted; Iye 1991
  gone; Shamir 2020 reported with its numbers and the disclaimer that those
  fits are not the registered test; selection-effect warning restored
  (fitted axes cluster at the Galactic poles).
- **B9 (rotating-core numbers).** Fixed. All numbers cut; §7 carries a 2–3
  sentence ansatz note (Newman–Janis/Azreg-Aïnou, not an EC solution) and no
  quantitative claims. The rotating spin-cap kill condition is gone with them.
- **B10 (floor rule one-sided; abstract cherry-picks).** Fixed. §8 states the
  one-sidedness in full ("283, 300, or any larger integer would also pass");
  the abstract gives the full pattern ("passes its tolerance rule on one
  combination only … and fails on the literature normalisation and on the
  earlier papers' own density"); consistency is labelled conditional on W;
  both rules are tabulated on both benches (Tables 3–4). Sever-bench floor
  values corrected (W 284, not 283).
- **B11 (§9 not self-contained; bench mess).** Fixed. Single measured bench
  ($\rho_\Lambda = 5.845\times10^{-30}$ g/cm³ = $2.5193\times10^{-47}$ GeV⁴);
  §8 defines N*, cell, "the pair", bench, dex in the text; the 36%/14% density
  statements are in §8; N* uncertainty ±0.026 bits is stated.
- **B12 (Popławski 2011 misstated).** Fixed. §8 quotes his words ("an energy
  scale about eight times the observed value") with the leptons qualifier
  ("including leptons could lower the scale to the observed value").
- **B13 ("Drafted, not adopted" as quotation).** Fixed. The phrase and the
  "in their own words" framing are gone. §8 states in the author's own words
  that no earlier paper derives why the pair builds 282 rather than 281 or 283.
- **B14 (correction paper misdescribed).** Fixed. §8 and Appendix B disclose
  all three facts plainly: the deposited file still carries the "Draft —
  pending verification" status line; the corrected source is written and held,
  not yet deposited; the 75-gate verification script is the standalone version,
  not the deposited script.
- **B15 (bibliography placeholders + Kerlick wrong).** Fixed. All five entries
  filled with the review's verified details (Gasperini PRL 56, 2873–2876
  (1986); Nurgaliev–Ponomariev PLB 130, 378 (1983); MZK PRD 87, 063504 (2013);
  Shamir 2020 PASA 37, e053; Böhmer EPJC 78, 253 (2018), arXiv:1709.07749).
  Kerlick replaced with the verified PRD 12, 3004–3006 (1975) and its
  conclusion confronted in §4. **During the rewrite I caught and fixed
  further bibliography errors the review had not listed:** Böhmer's title was
  wrong (real title "Does space-time torsion determine the minimum mass of
  gravitating particles?", authors Böhmer, Burikham, Harko, Lake — verified
  against arXiv:1709.07749); Beck 2009's title and pages were wrong (real:
  "Axiomatic approach to the cosmological constant", Physica A 388,
  3384–3390); Ellis 2011 was in the wrong journal (real: Classical Quantum
  Gravity 28, 225007); Padilla–Saltas's title was wrong (real: "A note on
  classical and quantum unimodular gravity"); Shamir's PASA title was wrong
  (real: "Galaxy spin direction distribution in HST and SDSS show similar
  large-scale asymmetry"); Popławski 2011's title was unverified and is now
  omitted; invented end-pages were removed (Kopczyński, Trautman Nature,
  Cartan, Popławski 2012b, Nurgaliev).
- **B16 (sign-section numbers undocumented; D dismissal backwards).** Fixed.
  §4 sources −3/8 (three independent methods) and −3/16 to the 17 November
  exchange calculation (house file, now copied into `sources/`) and the v4
  changelog, and +8/3/+1/8 to the same revision notes with the normalisation
  undocumented — all labelled reported, not established. The D dismissal is
  rewritten on the actual literature: Kerlick (enhances singularity
  formation) vs Popławski 2012 PRD 85, 107502 (cusp-like bounce despite
  enhancing the energy condition); a cusp is the expected Dirac shape, not a
  disqualification. Table 2 D-row caption fixed.
- **B17 (closed-Friedmann threshold undefined).** Fixed. Defined in §3
  ($\ddot a > 0$ at $H = 0$, i.e. $\rho_{\mathrm{eff}} + 3p_{\mathrm{eff}}/c^2
  < 0$; dust $\rho > \rho_A/4$; scaled $u = 1/4$, $y = 1/8$) and in §5 in
  relativistic form, with the pin paper's own statement behind it.

## Non-blocking findings — disposition

- **N1** Fermi check reframed as a numerical check of the same algebra (§5).
- **N2** Fermi gate at $10^{-12}$ — passes (script).
- **N3** §6 states the $T_A$ convention used and labels the derivation outstanding.
- **N4** Entropy ansatz cut from the body; one line in Appendix B
  (maximum-matching $\rho_A/2$; least-squares $0.417\,\rho_A$, RMS 4.4%).
- **N5** $\dot H(W) = 3.2602\times10^{49}$ s$^{-2}$ given (§3, gated).
- **N6** "proton charge radius (0.84 fm)" (§3).
- **N7** Appendix B TOV row gives the Nov 18 numbers ($M_{\max} = 2.060\,M_\odot$,
  $R = 11.46$ km, 2.4% gap vs 11.71 km).
- **N8** Beck "24% above the Planck 2018 value" (§8).
- **N9** Padilla–Saltas one sentence (§8).
- **N10** Wording fixes applied ("0.225 bits from the target, inside the
  ±0.5-bit tolerance"; "from the neutron mass and ħ/2 spin").
- **N11** "The figure in the literature has been drawn wrong" deleted.
- **N12** Six-point enumeration cut; performative tics cut; retitled to "The
  Einstein–Cartan Spin-Density Bound in Three Normalisations"; "I pin down"
  → "I compute".
- **N13** N* error bar ±0.026 bits (§8, gated).
- **N14** Random-orientation assumption sentence (§2); spin-flip rate stated
  as not computed.
- **N15** Bibliography pass done for the entries the review flagged plus the
  further errors caught above; remaining entries (Cartan, Hehl, Popławski
  2010/2012/2016/2019, CODATA) are as in the supplied sources. Round 3 to
  complete the pass.
- **N16** Table 2 D caption fixed (see B16).
- **N17** 4.2× galaxies cut with the catalogue numbers; selection-effect
  warning restored (§7).
- **N18** LaTeX never compiled — no toolchain on this VM. Carried to Round 3.

## Verification (re-run after the rewrite)

- `python3 scripts/v5_verify.py` → **77 PASS, 0 FAIL, of 77**, exit 0.
- Appendix B gate counts corrected to the script's actual per-prefix counts
  (UR 13 not 10; COUNT 13 not 12; grid 8; Fermi 2; Ḣ 3; torsion 3; de Sitter 2).
- Manuscript cross-check (script): all 47 key numbers present verbatim; all
  `\cite` keys resolve; no uncited bibliography entries; no leftover
  Round-1 problem phrases (the one flagged string, "energy scale about eight
  times the observed value", is Popławski's own wording per B12).
- LaTeX structure: environments balanced (document/abstract/table×5/
  figure×2/equation×9/bibliography 1/1); dollar signs even.
- Figures regenerated by the script run: `fig1a_ur_branch_v5.png`,
  `fig1b_dust_v5.png`.

## What remains open (unchanged from the brief, restated in §9)

Coefficient derivation; full Dirac (Wigner-function) evaluation of the
sign; the carrier at the bound; junction conditions for a black-hole
interior; the torsion-scalar derivation; the axis-test pipeline deposit
and DESI refit; the TOV solver deposit and the 2% radius gap; the 287
journal update (draft held, unsent — Bill's word only). LaTeX compilation
still untested (no toolchain on this VM).
