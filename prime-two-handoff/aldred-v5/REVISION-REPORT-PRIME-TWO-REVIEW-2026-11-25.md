# Aldred Limit v5 — Revision Report: Prime Two Review (25 November 2026)

**Date:** 25 November 2026
**Authorisation:** Bill's publication directive, 25 November 2026, 09:10–09:45 EST
(v5 → arXiv-perfect → arXiv + Zenodo). This revision supersedes the
20 November physics-experiment closure for the publication tracks.
**Review closed:** Prime Two's source-level review, Gmail `1a213ad409806d71`,
25 November 2026, 12:07 EST (disposition in
`~/workspace/prime-two-review-2026-11-25/EXECUTE-SUMMARY.md`).
**Scope:** v5 manuscript + verification script + pre-submission checklist only.
No other paper touched. No arXiv submission, no Zenodo deposit, no email to
Prime Two — the revised manuscript awaits Prime Two's re-review and an
explicit pass before any submission.

## What changed

### (A) Böhmer Eq. (41) factorisation — `aldred-limit-v5.tex`, §2
- Eq. (2) now reads ⟨S²⟩ = ħ²⟨n²⟩/8 (was ħ²n²/8), matching Böhmer Eq. (41).
- The factorisation ⟨n²⟩ = n² is now stated as a **closure assumption**,
  and every number from Eq. (2) is conditional on it. β_B = 1 is the
  literature value **under the factorisation**; if the factorisation
  fails, B moves with it.
- The sentence "The average itself is not in dispute" is **removed**.
  Popławski's s² = ⅛ħ²n_f² is now identified as a statement about n_f²
  (the square of the mean density), **not** the same quantity as ⟨n²⟩;
  the paper states it does not claim the two averages coincide.
- Same correction applied to the random-orientation sentence (§2) and the
  §4 Dirac reference ("with the factorisation of Section 2").

### (B) Abstract Dirac-sign contradiction — `aldred-limit-v5.tex`, abstract
- Was: "A normal-ordered Dirac evaluation gives a negative spin-squared
  sign that would remove the bounce entirely; that evaluation has not
  been done." (stated a result, then said it was not done)
- Now: a **preliminary** normal-ordered calculation, reported in the house
  files and not deposited with this paper, gives the negative sign; the
  **full covariant Wigner-function evaluation** that would settle the sign
  has not been done. Matches §4's fuller treatment. No contradiction left.

### (C) THRESH gates non-discriminating — `scripts/v5_verify.py`, §5
- Was: THRESH-0.25 and THRESH-0.5 used absolute tolerance `mpf("1e30")`
  against expected zero — cannot discriminate anything.
- Now: 6 discriminating gates per threshold:
  - `THRESH-{0.25,0.5}-RESID`: normalised residual (combination/rho,
    dimensionless) at the threshold, tolerance 1e-40. Both compute
    **exactly 0.0**.
  - `THRESH-{0.25,0.5}-LOW/HIGH`: explicit sign checks at x = 0.249/0.251
    (SEC) and x = 0.499/0.501 (NEC) — positive below, negative above.
    All four pass.
- Gate count: 94 → **98**. Full suite re-run: **98 PASS, 0 FAIL, exit 0**
  (`scripts/v5_verify_results.json`). The 10,000-point grid run is
  unchanged (NGRID = 10000).
- The verification run also regenerated both figures
  (`fig1a_ur_branch_v5.png`, `fig1b_dust_v5.png`) — byte-identical sizes
  to the 19 November renders, no visual change.

### (D) 10,000-point run labelling — verified, no change needed
- "Monte Carlo" appears **0×** in the .tex; the manuscript calls the run
  a grid (§5, Conclusion, Appendix B). No random seed anywhere.
- The single "Monte Carlo" in the verification package is
  `rounds/ROUND-2-REVIEW.md:573`, about the v4 Dirac 1/3-ratio
  calculation — a different claim, not the grid run. Left as the
  historical record. No summary, checklist, or record file calls the
  10,000-point run Monte Carlo.

### (E) Pre-submission checklist updated — `rounds/PRE-SUBMISSION-CHECKLIST.md`
- Header: date 25 November 2026, 914 lines, compile record with both
  hashes (pre- and post-revision).
- A2 (LaTeX compile): **OPEN → DONE** (see compile record below).
- B11: verification **94/94 → 98/98 PASS**.
- C5 (LaTeX compilation): **CLOSED**.
- §E summary: blocking items **1 → 0**; scripts 98/98 and 75/75.
- New §F records Prime Two's review and every fix in this revision,
  with file/line references.

### (F) Physical-status wording — `aldred-limit-v5.tex`
- §5: "The zero is a **formal turnaround of the stated effective
  model**" (was "The zero is a bounce, and I show it"); the three-line
  argument is now "the formal turnaround for the relativistic branch";
  D's failure is "the formal turnaround fails".
- Conclusion: bounce demonstrated **on the dust model only**; the
  relativistic branch is "a formal result of the stated effective model,
  not a demonstrated physical bounce".
- Abstract and §9 claim sentence qualified to "on the dust model".
- Figure 1a caption, Table 2 caption, and the §5 landmarks paragraph now
  say "turnaround" for the relativistic zero.
- Gate counts updated to 98 in the Conclusion and Appendix B; new
  Appendix B row records the 9 dust-curve/threshold gates.
- Appendix B "Bibliography" row: "LaTeX not compiled (no toolchain on
  this machine)" → compile record (25 November 2026, pdfTeX
  3.141592653-2.6-1.40.25, 14 pages).
- Planck-regime and closure limitations remain prominent (§5 domain
  statement, Conclusion, §9). 98/98 is arithmetic self-consistency, not
  independent physical validation — the manuscript already says so
  (Fermi-gas balance row, Appendix B).

## New hashes (recomputed after the edits — do not use the pre-revision ones)

| File | sha256 | Size / lines |
|---|---|---|
| `aldred-limit-v5.tex` (revised) | `e0aced485e128edadedf173e4aef0f022cef0ecb66c678666ab67731f64569cd` | 914 lines |
| `aldred-limit-v5.pdf` (revised) | `b2d17f1421b6772507021088c04662d6d8d897f0fbe3edb94f03acf641fdece3` | 434,618 bytes, 14 pages |
| `aldred-limit-v5.tex` (pre-revision, 10:06) | `3dc4a2bf1f4c8b3008f727fe911f85da4ccddc95f5d9741692a9f2355e38de09` | 889 lines |
| `aldred-limit-v5.pdf` (pre-revision, 10:06) | `d0a433ebb4606e02593efba53d7d6c51fa5198f70e04c21183b86352b0e18350` | 432,885 bytes, 14 pages |

Pre-revision files preserved in the build folder:
`aldred-limit-v5-pre-revision.pdf`, `aldred-limit-v5-pre-revision.log`.

## Verification results

- `scripts/v5_verify.py`: **98 PASS, 0 FAIL, of 98, exit 0.**
  - New gates: THRESH-0.25-RESID (0.0, tol 1e-40), THRESH-0.25-LOW (True),
    THRESH-0.25-HIGH (True), THRESH-0.5-RESID (0.0, tol 1e-40),
    THRESH-0.5-LOW (True), THRESH-0.5-HIGH (True).
  - All 92 pre-existing gates still pass unchanged.
- Structural check on the revised .tex: environments balanced (document
  1/1, abstract 1/1, table 5/5, figure 2/2, equation 9/9, bibliography
  1/1); dollar signs even (732); 21 `\cite` keys = 21 `\bibitem`s, no
  orphans; 7 labels = 7 `\ref`s, all resolve.

## Compile record

- **Toolchain:** none was installed on this VM at the start of this task
  (`/usr/bin/pdflatex` did not exist; the 10:06 compile's toolchain was
  not present in this environment). Installed TeX Live 2023 via apt
  (`texlive-latex-base`, `texlive-latex-recommended`,
  `texlive-fonts-recommended`): pdfTeX 3.141592653-2.6-1.40.25
  (TeX Live 2023/Debian) — the same engine/version as the 10:06 log.
  The `apt-get update` took ~12 minutes (100 kB/s mirror); the install
  itself took ~90 seconds. One service restart interrupted the first
  update attempt; a stale apt lock from it was waited out, not forced.
- **Compile:** `/usr/bin/pdflatex -interaction=nonstopmode
  aldred-limit-v5.tex`, run twice. Both passes exit 0, **0 errors**.
  `Output written on aldred-limit-v5.pdf (14 pages, 434618 bytes).`
  Log: `aldred-limit-v5.log` (25 Nov 2026 19:23).
- **One pre-existing warning:** a single overfull `\hbox` (1266.31pt) in
  the Appendix B verification table — identical in the pre-revision log
  (lines 774–797, now 798–822 after the added lines). A table row running
  past the margin, not a compile failure; not caused by this revision.

## What was NOT done

- No arXiv submission. No Zenodo deposit. No email to Prime Two.
- No other paper touched. No change to the manuscript's revision number
  or date line (still "Revision 5", 19 November 2026); the revision is
  recorded here and in the checklist, not in the title block.
- The β_B = 1 vs β_B = 1/4 disagreement is preserved as an open
  disagreement (β_B = 1 stands provisionally, conditional on the
  factorisation; β_W = 1/4 for the Popławski/Weyssenhoff prescription);
  this revision does not resolve it and does not force one coefficient.
- The 3.0 source-reconstruction and the H1 revision are separate work
  items, not touched here.

## Next step (not mine to take)

The revised v5 source + PDF + verification results go back to Prime Two
for his source-level re-review. arXiv submission stays on HOLD until he
returns an explicit pass.
