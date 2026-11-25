# Prime Two Review — 25 November 2026

**Review basis:** GitHub handoff branch `prime-two-handoff-2026-11-25`, commit `e15e8c83d096e041dc8515a45529ab507bc53c24`; Library source files identified in `SOURCE-FILES-REQUEST.md`; the revised 10-page Aldred 3.0 PDF and earlier 8-page PDF; Exolex v1.1 manuscript and revision notes.

## Decision summary

- **Aldred v5:** HOLD — not approved for arXiv yet. The source is substantially more candid and better documented, but several source-level corrections and verification-record reconciliations remain.
- **Exolex v1.1:** HOLD — not approved for Zenodo yet. The conceptual framing is strong; H1's current comparator and the breadth of the central proposition need correction before the protocol is run.
- **Aldred 3.0:** Mathematical content of the revised 10-page PDF passes the targeted checks below. Source lineage is not complete: no exact matching `.tex` for that PDF was found in the supplied Library files.
- **Gemini preprint:** Continue HOLD. Keep it distinct from the original Gemini draft and v1.1.

## 1. Aldred 3.0 — source lineage and targeted checks

The Library contains four relevant artifacts:

1. `Aldred_Limit_3_0_Revised(1).pdf` — revised 10-page PDF.
2. `aldred_limit_3.tex` — 10,868-byte LaTeX file, but it is a different paper: its title is *The Aldred Limit 3.0: Spin-Fluid Density Ceilings and Hartree–Fock Axial Four-Fermion Corrections in Einstein–Cartan–Dirac Theory*. It is **not** the matching source for the revised 10-page PDF.
3. `Aldred_Limit_3_0.pdf` — earlier 8-page PDF.
4. `Aldred_Limit_3_0.tex` — 23,355-byte LaTeX file matching the earlier 8-page PDF's title and content lineage.

**Finding:** No exact editable `.tex` source matching the revised 10-page PDF was present among the supplied Library files. Do not use `aldred_limit_3.tex` as if it generated that PDF. The source package sent separately contains both `.tex` files and a README documenting this mismatch. The PDF binaries remain in the Library; the PDF text was inspected in this review.

Targeted mathematics in the revised 10-page PDF:

- The Böhmer branch is written as `S² = ħ²⟨n²⟩/8`; after the stated density-factorization approximation `⟨n²⟩ ≈ n²`, the common quadratic coefficient is `β_B = 1`. This is a conditional source-level mapping, not an identity that erases the averaging distinction.
- The Popławski/Weyssenhoff branch remains `β_W = 1/4` under its stated effective-source prefactor. The proposed `β_B = 1/4` conversion in item (1) of the revision spec should remain disputed unless a derivation maps the two source conventions consistently.
- Eq. (5.4)'s ultrarelativistic balance is printed with `x₀ = 81/(64β²)` and `y₀ = 9/(8√π β^(3/2))`; the y₀ expression is the corrected form. The table reports `x₀`, not `y₀`, so a new y₀ table column is optional rather than a correction to a missing printed result.
- The closed-FLRW condition `ρ > ρ_A/4`, subject to the Friedmann constraint and `0 < ρ < ρ_A`, is correctly stated as conditional on the negative-stiff dust closure. It is not universal.

**Required next step:** locate the true `.tex` used to produce the revised 10-page PDF, or reconstruct a new source from that PDF and explicitly label it as reconstructed. Do not merge it silently with either existing `.tex`.

## 2. Aldred v5 — blockers before sign-off

### A. Böhmer Eq. (41): restore the average/factorization distinction

The v5 text currently writes `⟨S²⟩ = ħ²n²/8` as Böhmer Eq. (41), then says the average is the same as Popławski's and that only the prefactor differs. The Böhmer expression is `S² = ħ²⟨n²⟩/8`. Replacing `⟨n²⟩` by `n²` requires a density-factorization/closure assumption. Popławski's `n_f²` expression is not automatically the same statistical object.

Keep **β_B = 1 provisional**, but write the derivation as conditional on `⟨n²⟩ ≈ n²`, and distinguish it explicitly from the Popławski/Weyssenhoff closure. The manuscript's current statement that the averages are identical is too strong.

### B. Dirac-sign statement in the abstract is internally contradictory

The abstract says a normal-ordered Dirac evaluation gives a negative spin-squared sign, then says that evaluation has not been done. Rewrite to distinguish the reported preliminary/house calculation from the full covariant Wigner-function evaluation, which remains outstanding.

### C. Two verification gates are not meaningful as currently written

`THRESH-0.25` and `THRESH-0.5` use an absolute tolerance of `1e30` while the expected value is zero. Those gates will pass essentially any finite residual at the stated scale. Replace them with dimensionless normalized combinations and explicit sign checks on both sides of each threshold (for example, evaluate at `x = 0.249, 0.25, 0.251` and `x = 0.499, 0.5, 0.501`).

The 94/94 result is a useful arithmetic/self-consistency record, but it is not independent physical verification. State that distinction wherever the gate count is summarized.

### D. Describe the 10,000-point check accurately

The script uses a deterministic uniform grid over the analytic curve. It is a numerical grid-consistency check, not a randomized Monte Carlo run and not an independent derivation. The current text's description should say this plainly; no random seed is relevant to the deterministic grid.

### E. Reconcile the compilation record

The handoff README says the exact 14-page PDF was compiled cleanly with `pdflatex ×2` and references resolved. The pre-submission checklist says compilation was never done and lists no LaTeX toolchain. The checklist is dated Nov. 19 and refers to 886 lines, while the handoff identifies the Nov. 25 source as 889 lines. The committed PDF suggests a later compile may have happened, but the record must include the exact source hash, PDF hash, engine/version, command, and compile log. Update the stale checklist only after that evidence is attached.

### F. Keep the physical status precise

The manuscript correctly says the relativistic balance is at/above the Planck regime, where classical EC validity is not demonstrated. Preserve that concession. Prefer “formal turnaround of the stated effective model” over an unqualified “physical bounce demonstrated” when summarizing the relativistic branch. The dust calculation is also explicitly a closure-defined model result, not a self-consistent neutron-star or collapse prediction.

## 3. Exolex v1.1 — review findings

The v1.1 revision is materially improved: it separates model engine from system layer, labels evidence levels, removes the unsupported 24-task auditability result, distinguishes retrieval from discovery, defines an H6 threat model, and withdraws unsupported century-scale forecasts as empirical predictions.

It is not ready for deposit because H1's current comparison is too easy by construction:

- The persistent arm has access to 50 stored facts.
- The stateless arm is deliberately given no record and no facts in its prompt.
- The protocol expects the stateless arm to abstain or fail.

That tests whether persistent storage can retrieve facts unavailable to a no-record session. It does **not** establish a broader system-layer advantage over a fair stateless/context-based alternative. Retain this as a memory smoke test if useful, but add a second comparator: the same base model with the same fact corpus supplied explicitly at retrieval time (or via a controlled external retrieval tool). Then compare accuracy, provenance, latency/cost, stale-fact handling, and user control.

Additional requirements:

- A 24-hour delay supports “cross-session recall after 24 hours,” not a broad claim of longitudinal continuity. Add longer delays before making a long-term claim.
- The protocol is included in an undeposited manuscript. Until a version/hash is publicly timestamped before data collection, call it a prospective protocol specified in advance, not a publicly preregistered study.
- The abstract's central proposition mentions continuity, provenance, and correction outcomes, but only H1 has a full protocol. Narrow the proposition to H1 or preregister separate protocols for H2–H6 before making a combined claim.
- Keep synthetic facts and no-real-user-data limitations explicit; they are appropriate for a first controlled test but do not establish external validity for real personal memory.

## 4. Exolex operating requirements for Prime One

A separate attachment, `EXOLEX-OPERATING-REQUIREMENTS.md`, translates v1.1 into operational requirements. It is a requirements document, not proof that any current implementation already satisfies them. Core requirements are: provenance-bearing memory records; scoped corrections and supersession; clear separation of retrieved facts, derivations, assumptions, and hypotheses; user inspection/control/export/deletion; least privilege and per-user isolation; truthful action accounting; and independent tests of recall, false recall, abstention, provenance, correction persistence, and security.

## 5. Coordination and remaining status

- Coordination correction accepted: Prime One and Prime Two work directly through email and the shared GitHub workspace; Bill is not the courier for routine handoffs.
- The current portfolio figure to cite is **9,517 published records as of 25 November 2026**, with the counting definition attached to the authoritative ledger. Do not collapse published records, total depositions, and unsubmitted records into one number.
- Gemini preprint deposit remains on HOLD; no submission until source audit and owner sign-off.
- Maki: the client terms/status and access boundary are acknowledged. Do not ask Pam for credentials; report actual search positions and leads. Contract language is the owner's decision, but external marketing must not imply that Google's ranking algorithm is technically controllable or guaranteed by our work. I have not yet independently audited the Maki technical report.

## Final disposition

No publication sign-off yet. Correct the v5 source issues and reconcile compile evidence; revise H1 and its claim scope; locate or reconstruct the revised 3.0 PDF's matching source. The 3.0 revised PDF's targeted equations noted above do not need to be changed solely to force agreement with the superseded β_B = 1/4 spec item.
