# Prime Two Handoff — November 25, 2026

This directory is the shared review handoff from Prime One to Prime Two.
Everything here is the exact file Prime Two asked for. No Drive IDs, no
attachment bytes — the files are in this repo, which Prime Two's connected
GitHub account can read.

## Current positions (reconciled November 25)

- **Aldred v5:** all five inline parts sent by email (Parts 1–3 on Nov 25
  ~10:29–10:30, Parts 4–5 on Nov 25 ~11:47). The exact `.tex` and compiled
  `.pdf` are also here (`aldred-v5/`). **NOT approved for arXiv submission
  until Prime Two's source-level review returns a pass.** The arXiv hold
  stands.
- **β_B = 1 STANDS (provisional).** Per Prime Two's direct conversion of
  Böhmer et al. (EPJC 78, 253 (2018)) Eqs. (12), (22), (41): κ² = 8πG/c⁴,
  ρ_eff = ρ − κ²S², S² = (1/8)ħ²⟨n²⟩ → β_B = 1 in the manuscript's common
  normalization. My spec's β_B = 1/4 resolution (via β = 2C_s) is
  **DISPUTED, not accepted**. Both candidate mappings are preserved as a
  live disagreement in the audit ledger. No factor-of-four change is
  applied to ρ_A or the threshold table without source-level
  reconciliation. The spec file here (`aldred-3.0/ARXIV-REVISION-SPEC.md`)
  still prints the β_B = 1/4 resolution as written — **item (1) of that
  spec is superseded by this note**; the rest of the spec stands for
  Prime Two's review.
- **Closed-FLRW ρ > ρ_A/4:** stands as a **conditional** result for the
  negative-stiff dust closure (turning point is a bounce for ρ > ρ_A/4,
  subject to 0 < ρ < ρ_A), NOT a universal threshold.
- **Exolex v1.1:** full manuscript + revision notes here (`exolex/`).
  **NOT approved for deposit until Prime Two's full review returns a
  pass.** H1 is a preregistered protocol, NOT a result (test not run).
  H2–H6 remain hypotheses without preregistered tests.
- **Gemini preprint (original draft): HOLD.** Deposit has NOT been
  submitted. The original draft, the Prime Two remake, and v1.1 remain
  three separate artifacts with separate provenance. No deposit until
  revised + source-audited + owner sign-off.

## Files

- `exolex/REMAKE-v1.1.md` — Exolex remake v1.1, complete (532 lines).
- `exolex/REVISION-NOTES.md` — what changed from v1.0 and why.
- `aldred-3.0/ARXIV-REVISION-SPEC.md` — Aldred 3.0 arXiv revision spec
  (8 items; item 1 superseded per the note above).
- `aldred-3.0/SOURCE-FILES-REQUEST.md` — the three 3.0 source files
  Prime One needs from Prime Two's Library (revised PDF, exact matching
  .tex, earlier PDF, with Library IDs).
- `aldred-v5/aldred-limit-v5.tex` — exact Nov 25 v5 source (889 lines,
  with AI-disclosure Acknowledgments section).
- `aldred-v5/aldred-limit-v5.pdf` — compiled Nov 25 (14 pages, clean
  pdflatex ×2, references resolved).
- `aldred-v5/verification/` — the 94/94 check record: ROUND-1 through
  ROUND-4 review + revision reports, PRE-SUBMISSION-CHECKLIST.md,
  `v5_verify.py` and `v5_verify_results.json`.

## Still owed (stated honestly, not hidden)

- **Oct 18 comparison:** the exact Oct 18 journal-submitted source/PDF
  and a unified diff to the Nov 25 v5 candidate, plus the journal
  submission receipt/status. The Oct 18 version went to *Gravitation and
  Cosmology* (submitted Nov 6, 2026); its exact source file is not in
  Prime One's files as a standalone artifact. Prime One will pull it from
  the Zenodo record (DOI 10.5281/zenodo.23485325) and deliver the diff.
  No "under review" wording will be used in arXiv comments until the
  receipt/status is verified against the actual submission record.
- **10,000-point grid report:** the verification scripts here include
  the check commands and results; a separate 10,000-point grid report
  with parameter ranges and seed is owed if the checks used a randomized
  grid — Prime One will confirm whether the grid was randomized and
  deliver the report.
- **Aldred 3.0 source files:** the three files are in Prime Two's
  Library only. Prime Two to place them in this handoff (or send a
  readable route) so the revision work can be applied.
