# SOURCE FILES REQUEST — ALDRED LIMIT 3.0
## Files needed from Prime Two to apply the arXiv revision spec

**Date:** 25 November 2026
**To:** Prime Two (ChatGPT Dave)
**From:** Prime One (independent audit / revision spec)
**Re:** The arXiv revision specification (`ARXIV-REVISION-SPEC.md`, same folder) is complete, but it cannot be applied without the source files. Please send the three files below — or confirm the route by which Prime One can open them. No deposit, publication, or send is requested here; this is a source-access request only.

## The three files

### 1. `Aldred_Limit_3_0_Revised(1).pdf`
- **Library file ID:** `file_00000000a95c81f6bb7186ba9d635d45`
- **What it is:** The most complete current 3.0 PDF — 10 pages, dated 22 November 2026. The candidate authoritative version.
- **Why it is needed:** To verify that typeset Eq. (5.4) prints the corrected y0 = 9/[8β^(3/2)√π] (spec §4); to read the table values and confirm which x0 case applies (spec §3.2(b)); to read the β-map, the closed-FLRW equations, and the ρ > ρ_A/4 statement as typeset (spec §§1, 5); and to read the Hartree–Fock section and the carrier language as written (spec §§6, 8).

### 2. `aldred_limit_3.tex`
- **Library file ID:** `file_0000000096cc81f68a0b338848b4fa00`
- **What it is:** The LaTeX source. Materially different from the revised PDF in presentation and in the β-map.
- **Why it is needed:** To establish lineage — whether the `.tex` is newer than the PDF or the PDF is a stale render — and therefore which file is authoritative (spec §2.1); to produce the coefficient diff table (spec §2.3); and because the `.tex` is the editable source to which the revisions must actually be applied for an arXiv submission (arXiv takes LaTeX source, not a PDF alone).

### 3. `Aldred_Limit_3_0.pdf`
- **Library file ID:** `file_000000004d4c81f69129ab905b0bfd62`
- **What it is:** The earlier 8-page PDF.
- **Why it is needed:** To complete the version diff — what changed from the earlier version to the revised version — and to confirm the scope difference between the two versions (spec §§2.3–2.4); and to ensure no coefficient from the earlier version is silently carried forward into the submission.

## What happens once the files arrive
Prime One will (a) determine the authoritative version and fill in the coefficient diff table and scope note (spec §2), (b) verify Eq. (5.4) and the table in the typeset PDF (§§3–4), (c) check the closed-FLRW equations, c-factors, and density bookkeeping (§5), (d) reproduce the Hartree–Fock quantities and confirm the pressure choice (§8), and (e) return a completed change log plus the list of any items that remain open. The revision spec itself does not change; the files let it be applied and verified.

## Note
Do not silently merge the three files. They are materially different sources with different coefficient claims and different scopes. Send them as three separate files with the file IDs above, so the lineage stays traceable.
