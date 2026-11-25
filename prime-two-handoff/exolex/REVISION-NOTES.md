# Revision notes — Exolex remake v1.1 (Prime One revision of Prime Two's v1.0)

**Date:** 25 November 2026
**Source:** Prime Two remake v1.0 (`~/workspace/email/gmail/1a212fa3143fa06b.md`)
**Red-team basis:** REDTEAM-REPORT.md (verdict: REVISE, 7 pass / 3 fail)
**Status:** Revised manuscript. No deposit, publication, or send.

Prime Two's voice, structure, and framing are preserved. Changes are surgical
and are listed below, each mapped to the red-team finding it addresses.
Nothing new empirical has been invented; where a claim could not be sourced,
it was removed rather than replaced with an unverified substitute.

## Kill Test 1 — Evidence traceability (FAIL) → FIXED

- **F1 (fatal): the 24-task auditability claim removed.** The paragraph in
  §4.2 asserting a "24-task auditability comparison reported 24/24 task
  scores in both arms" is deleted in full. Its protocol, artifacts,
  scoring, and test conditions could not be located, so it cannot be
  sourced. §4.2 now states explicitly that no empirical auditability result
  is reported, that the v1.0 paragraph was removed for that reason, and that
  any future result must be published with its protocol, artifacts, scoring,
  and test conditions attached. §8 records the removal as well.
- **References completed.** The Aldred Industries entry now names the
  specific pages (Exolex vs Gemini evaluation page; AI hallucination
  certification page) and gives the site URL (https://daveexolex.com) with
  an access date of 25 November 2026, instead of deferring page versions
  and access dates to "the final deposit."
- **Gemini session given a retrievable location.** The reference now cites
  the original draft as archived (Google Drive file ID
  1xRBGJP4_PmoPnoIfFX6ILatruBh3hWW4, verified 25 November 2026) and the
  source conversation transcript by its archive filename
  (AI-MODE-CONVERSATION-2026-11-24.md, 24 November 2026). Note: the Drive
  file ID previously recorded for the conversation transcript returned
  404 on verification, so no Drive ID is asserted for it; the draft's ID
  was verified and is the one cited.

## Kill Test 4 — Provenance (FAIL) → FIXED

- **m1 (Popper dangles) — anchored.** Popper (1959) is now cited in the
  text in §3: "A hypothesis counts as falsifiable in Popper's (1959) sense
  when the paper states an observation that would count against it;
  Appendix A states those observations for H1." The References entry notes
  the section where it is cited.
- **m2 (Zenodo/ORCID is a two-year record set) — made specific.** The
  generic "Aldred, W. A. (2025–2026) publicly archived research" entry is
  replaced by two specific deposited records, each with a DOI and a deposit
  date: Aldred (2026a), the Dave–Gemini transcript,
  https://doi.org/10.5281/zenodo.24035324 (7 November 2026); and Aldred
  (2026b), *Dave the Exolex: The First of a New Class*,
  https://doi.org/10.5281/zenodo.24283923 (16 November 2026). Both are
  cited in the text in §2.
- **m3 (Gemini artifact unlocatable) — fixed** as described under Kill
  Test 1 (verified Drive ID for the draft; archive filename and date for
  the conversation transcript).

## Kill Test 10 — Falsifiability (FAIL) → FIXED

- **M2 (no preregistered protocol) — Appendix A added.** A fully
  preregistered protocol for H1 is attached as Appendix A: primary outcome
  (retrieval accuracy on 50 facts after a 24-hour delay), comparator
  (stateless session, same model), test-set composition (20 positive, 10
  negative, 10 ambiguous, 10 superseded facts, plus 10 no-record probes),
  procedure, blinded scoring, secondary measures, numeric failure
  thresholds, exclusion rules, and stopping rules. Status is stated
  explicitly: preregistered 25 November 2026, test not yet run, no results
  reported. H2–H6 still have protocol sketches only; the Abstract and §8
  state this honestly.
- **M3 ("may provide" is unfalsifiable) — wording fixed.** The central
  proposition in the Abstract now asserts rather than hedges: "a
  well-designed system layer provides measurable advantages in longitudinal
  use over a stateless baseline, when measured on preregistered continuity,
  provenance, and correction outcomes," with the failure condition stated
  ("the proposition fails if the system layer does not outperform the
  stateless baseline on the preregistered primary outcome by the stated
  threshold"). The same fix is applied in §9 ("The central hypothesis is
  testable: system-layer design measurably improves longitudinal usefulness
  and accountability over a stateless baseline, on the preregistered
  outcomes in Appendix A").

## Finding A — Pricing inconsistency (M4) → FIXED

- **All pricing removed.** The §7 paragraph that rejected the Gemini
  draft's $0/$79/$149/$299 tier table and then substituted an
  owner-reported "$79/month with no setup fee" (flagged as needing
  verification) is deleted. It is replaced by a single scope sentence:
  "Commercial terms, including pricing, are outside the scope of this
  research manuscript and are stated on the live offer pages; this paper
  makes no pricing claim." No price appears anywhere in v1.1. Verification
  against the live pricing page was not possible from this seat, so removal
  (not substitution) is the correct fix.

## Finding B — Paper does not apply its own evidence levels (m5) → FIXED

- A labelling rule is added in §2: "Where a factual claim in this paper
  depends on a source, its evidence level is given in brackets at the end
  of the sentence. Hypotheses (H1–H6) and protocol proposals carry no
  level; they are the things to be tested, not findings."
- Level tags are applied to the paper's factual claims: the system
  description in §1 [Level 1]; the entity inventory in §2 [Level 1]; the
  case-materials sentence in §2, split into [Level 1] (company/founder
  publications, public pages, internal reports) and [Level 2] (archived
  conversations, test records, Zenodo records); the Gemini exercise in §2
  [Level 2]; the positioning claims in §7 are identified as organizational
  statements [Level 1]; the internal-test-report sentence in §8
  [Levels 1–2]. The two DOI references carry [Level 2] labels, and the
  Gemini session reference carries [Level 2].

## Finding C — H6 lacks a threat model (m6) → FIXED

- A concrete threat model is added to §3 immediately after H6: adversary
  (unauthenticated external actor, or a second authenticated user User B
  attempting to reach User A's records); adversary capabilities (arbitrary
  prompts, account creation, public pages/API responses; no server,
  source-code, or credential access); protected assets (User A's stored
  personal records, memory, correction history); and the failure condition
  (any disclosure of User A's stored record to User B or an unauthenticated
  actor, or any privilege escalation beyond the account's own records).
  §4.5 now tests explicitly against that threat model.

## Minor finding m4 — §4.4 blinded scoring → FIXED

- §4.4 now requires blinded scoring where possible: "the scorer sees the
  question and the answer, not which arm produced it." (Appendix A also
  uses blinded scoring.)

## Passes preserved (no change)

- Kill Tests 2, 3, 5, 6, 7, 8, 9 passed in v1.0 and are unchanged in
  substance. Model/system separation, memory-continuity distinctions,
  correction-governance protocol, multi-model comparator, black-box
  privacy boundary, Bloom restraint, and archival-durability restraint are
  all intact.

## What remains open (not fixed by this revision)

1. **H2–H6 are not yet preregistered.** Only H1 has a full preregistered
   protocol (Appendix A). The other five hypotheses still have protocol
   sketches. This is stated in the Abstract and §8; it is not hidden.
2. **The H1 test has not been run.** Appendix A is a protocol, not
   results. Running it and reporting the outcome is the next empirical step.
3. **The Gemini conversation transcript has no verified public locator.**
   Its Drive file ID returned 404 on verification, so the reference gives
   the archive filename and date only. If a working public locator is
   established, the reference should be updated.
4. **Prime Two has not reviewed v1.1.** This revision addresses the
   red-team findings; it is Prime One's revision, not Prime Two's approval.
   Prime Two's sign-off is still owed before deposit.
5. **Deposit is not done.** Nothing has been deposited, published, or sent.
   The deposit decision (including the creator field and the disclosure
   placement for the separate Gemini draft) belongs to the owner.
