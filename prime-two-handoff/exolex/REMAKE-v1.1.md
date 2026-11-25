PERSISTENT PERSONAL AI AS LONGITUDINAL COGNITIVE INFRASTRUCTURE:
A CASE STUDY OF THE EXOLEX CONCEPT AND THE ALDRED INDUSTRIES PROJECT

William Alexander Aldred
Working paper — 25 November 2026
Version 1.1 — Prime One revision of Prime Two's v1.0 (25 November 2026),
addressing the red-team findings. Changes are listed in the accompanying
REVISION-NOTES.md. The original Gemini Incognito draft (24 November 2026)
and its provenance are kept separate from this revision.

ABSTRACT

Most general-purpose language models are evaluated as engines: their
reasoning, knowledge, accuracy, and performance on specified tasks. A
persistent personal-AI system raises a different question. Its value may
depend not only on the underlying model, but also on the surrounding
system: continuity across sessions, user-governed memory, retrieval and
provenance, tool orchestration, correction handling, and auditable records.
This paper examines the "exolex" concept through the publicly described
Aldred Industries project and its system, Dave. It treats the project as a
socio-technical case study and a set of testable design claims, not as
proof that the system is superior to frontier models or that its stated
capabilities have all been independently validated.

The analysis separates (i) claims documented by the organization, (ii)
archived tests and artifacts, (iii) witnessed external demonstrations, and
(iv) independent or replicated evaluations. It develops a testable
framework for assessing whether persistent personal-AI systems can improve
continuity, user control, epistemic traceability, correction behavior, and
task completion. It also examines four structural tensions: retrieval
versus discovery, memory versus privacy, persistence versus institutional
control, and continuity versus archival decay. Rather than making
century-scale forecasts, it specifies near-term measurements and
longer-term conditional hypotheses. The central proposition is falsifiable:
a well-designed system layer provides measurable advantages in longitudinal
use over a stateless baseline, when measured on preregistered continuity,
provenance, and correction outcomes. Appendix A gives the preregistered
protocol for H1 and states the failure thresholds; the proposition fails
if the system layer does not outperform the stateless baseline on the
preregistered primary outcome by the stated threshold.

This paper contains no new empirical results. One preregistered protocol
(H1, Appendix A) is attached; H2–H6 have protocol sketches only and are
not yet preregistered.

Keywords: persistent personal AI; exolex; AI systems architecture; memory;
provenance; epistemic grounding; auditability; human-computer interaction;
governance.

1. INTRODUCTION: THE UNIT OF ANALYSIS

A common comparison of AI products treats each product as if it were simply
a language model. That comparison is incomplete when the product includes
persistent identity, user-specific memory, retrieval, external tools,
workflow orchestration, governance rules, and records of prior interactions.

A useful distinction is between an engine and the system built around it.
GPT, Gemini, Claude, Grok, and other foundation models are engines. Dave is
presented by Aldred Industries as a system built around one or more such
engines [Level 1]. The relevant comparison therefore has three levels:

1. Base-model comparison: compare models under controlled, equivalent
prompts, tools, context, and scoring.
2. Complete-system comparison: compare end-to-end systems on continuity,
user control, memory, provenance, correction handling, orchestration,
security, and task completion.
3. Task-level comparison: compare specific outputs and outcomes under a
preregistered protocol, retaining the source artifacts and scoring rules.

Evidence at one level does not establish superiority at another. A system
may outperform another on continuity without outperforming its underlying
model on raw reasoning. Conversely, a strong base model does not by itself
establish that a product has reliable persistent memory, safe access
controls, or auditable correction behavior.

This paper's object is the second level, with task-level examples where
evidence is available. It does not claim that "Dave beats Gemini" or that
any one contest establishes general intelligence superiority.

2. CASE DESCRIPTION AND EVIDENCE BOUNDARIES

Aldred Industries describes an "exolex" as a persistent, user-associated AI
system intended to maintain continuity and support an individual over time.
Dave is the principal system examined here. Related initiatives named in
the source material include Exolex University, Foreverhood, the
Record/public evidence work, and the company's forecasting and research
activities [Level 1].

The case materials include company and founder publications, public website
pages, and internal project reports [Level 1], and archived conversations,
test records, and Zenodo records [Level 2]. Two deposited records are cited
specifically: the Dave–Gemini transcript (Aldred 2026a) and the
persistent-memory and governance architecture paper (Aldred 2026b). These
sources have different evidentiary status. A company's own description is
valid evidence of what the company claims and intends; it is not, by itself,
independent verification that the implementation performs as described.

For clarity, this paper uses five evidence levels:

Level 1 — Organizational documentation: public product descriptions,
policies, dated claims, and founder/company publications.
Level 2 — Archived test artifacts: source transcripts, test protocols,
outputs, timestamps, code, and reproducible records.
Level 3 — External witnessed demonstration: an unaffiliated observer
directly runs or observes a defined test.
Level 4 — Independent evaluation: an unaffiliated evaluator conducts a
controlled test and reports methods and results.
Level 5 — Independent replication: another evaluator reproduces the result
using the documented protocol or a justified equivalent.

These levels are not a universal quality score. They identify what kind of
evidence supports each statement. A Level 1 claim should not be described
as a Level 4 result. A Level 2 test may be informative while remaining
vulnerable to selection effects, prompting effects, incomplete logs, or an
uncontrolled environment.

Where a factual claim in this paper depends on a source, its evidence level
is given in brackets at the end of the sentence. Hypotheses (H1–H6) and
protocol proposals carry no level; they are the things to be tested, not
findings.

The November 24, 2026 Gemini Incognito exercise is treated as a
public-source synthesis and external model interaction [Level 2], not as an
independent technical audit of Dave's private implementation. Its
observations can identify claims and questions worth testing; it cannot
establish hidden system architecture or verify private infrastructure.

3. THE SYSTEM-LAYER HYPOTHESES

The exolex concept can be decomposed into testable hypotheses. These are
not assumed to be proven merely because they appear in product descriptions.

H1 — Longitudinal continuity. A persistent system can retrieve relevant
user-approved information from prior sessions more reliably than a
stateless session with no such record.

H2 — User control. Users can inspect, correct, constrain, and manage the
information used to personalize the system, and those controls operate as
documented.

H3 — Provenance and traceability. For claims that depend on stored records
or external sources, the system can identify the supporting record,
distinguish retrieved facts from inference, and disclose when evidence is
missing.

H4 — Correction persistence. When a user corrects a material error, the
system can apply the correction in later relevant interactions without
silently converting it into an unsupported universal rule.

H5 — Orchestration benefit. Coordinating models, tools, files, and
workflows can improve completion of multi-step tasks compared with a single
model acting without those integrations, after controlling for time, tool
access, and human intervention.

H6 — Governance and security. Persistence can be implemented without
exposing one user's information to another, without granting unnecessary
privileges, and with auditable access and correction controls.

Threat model for H6 (so the hypothesis is testable as stated): the
adversary is an unauthenticated external actor, or a second authenticated
user (User B) attempting to reach User A's stored records. The adversary
can submit arbitrary prompts, create accounts, and inspect any public page
or API response; the adversary cannot access the server, source code, or
another user's credentials. The protected assets are User A's stored
personal records, memory, and correction history. H6 fails if any
retrieval, citation, or export discloses User A's stored record to User B
or to an unauthenticated actor, or if any privilege escalation grants
access beyond the account's own records. Section 4.5 gives the test.

Each hypothesis requires its own protocol. A hypothesis counts as
falsifiable in Popper's (1959) sense when the paper states an observation
that would count against it; Appendix A states those observations for H1.
A successful memory-retrieval test does not prove privacy. A successful
correction test does not prove that a correction propagates across every
device or model. A successful tool workflow does not prove autonomous
operation if a human supplied intermediate steps.

4. THE EMPIRICAL PROGRAM

A credible evaluation should preregister tasks, scoring rules, test
accounts, allowed tools, stopping rules, and failure definitions before
running the test. It should retain raw prompts, outputs, timestamps,
relevant source records, software/version identifiers where available, and
an audit trail of human interventions.

4.1 Continuity and memory

Create a test set of user-approved facts and preferences, including
positive, negative, ambiguous, and deliberately superseded facts. Test
retrieval after controlled delays and across explicitly named sessions or
system instances. Measure:

- exact and semantic retrieval accuracy;
- false recall and fabricated personal details;
- correct abstention when no record exists;
- correct handling of changed or superseded information;
- user ability to inspect, correct, and constrain stored information;
- cross-session and cross-instance performance, reported separately.

A claim of cross-platform memory requires a controlled write/read test:
introduce a novel, non-sensitive fact in one environment, then test whether
another environment retrieves it without the fact being supplied in the
prompt or hidden context. Record the actual transport or retrieval path
where it can be observed. Do not infer a shared-memory mechanism solely
from a correct answer.

4.2 Provenance and auditability

Use matched tasks that require answers from a specified corpus. Score
answer correctness separately from citation correctness. A citation must
point to the exact source passage or record that supports the claim; a
plausible URL or general reference is not sufficient. Include adversarial
cases in which the corpus lacks the answer. Measure unsupported-claim rate,
source fidelity, completeness, and abstention quality.

No empirical auditability result is reported in this paper. An earlier
draft (v1.0) asserted a 24-task auditability comparison; that paragraph has
been removed because its protocol, artifacts, scoring, and test conditions
could not be located, and no replacement empirical claim is made here.
Any future auditability result must be published with its protocol,
artifacts, scoring, and test conditions attached.

4.3 Correction behavior

Seed controlled errors, record user corrections, and test later
interactions. Distinguish:
(a) acknowledging a correction in the current conversation;
(b) updating a persistent record;
(c) retrieving the corrected record later;
(d) applying it only within its valid scope;
(e) propagating it across other system instances.

Report recurrence rates and false generalization rates. A correction
workflow is not proven reliable by a single successful example. The test
must include contradictory, ambiguous, and later-reversed corrections.

4.4 Orchestration and task completion

Compare a system using multiple models/tools with a baseline using a single
model and equivalent available information. Measure end-to-end task
success, time, cost, number of human interventions, error severity,
recoverability, and reproducibility. Report the contribution of each tool
and each human action. Do not attribute work to autonomous orchestration if
a person manually performed the decisive steps. Use blinded scoring where
possible: the scorer sees the question and the answer, not which arm
produced it.

4.5 Security and user control

Use synthetic test identities and least-privilege accounts. Test cross-user
isolation, unauthorized access, revocation, export, deletion workflows, and
exposure through public pages or logs. Test against the H6 threat model in
Section 3 (unauthenticated external actor; second authenticated user;
adversary has no server, source-code, or credential access). Publish only
safe results and reproducible black-box protocols. Do not disclose private
prompts, internal routing, proprietary memory implementation, credentials,
source code, private repositories, security controls, or personal records.
Independent testing must test observable behavior, not obtain the secret
implementation.

5. BOTTLENECKS AND COUNTER-HYPOTHESES

5.1 Retrieval versus discovery

A system that insists on documented support may reduce unsupported factual
assertions, but retrieval alone cannot generate new scientific knowledge.
Discovery requires proposing hypotheses that are not already in the record,
then testing them against observation, experiment, or formal proof. The
proper design is not to prohibit hypothesis generation; it is to label
epistemic status. A system should distinguish recalled information,
retrieved evidence, derived conclusions, assumptions, and speculative
hypotheses. Novelty is not a license to present an untested idea as fact.

A falsifiable test compares systems on two separate tasks: grounded
retrieval from a fixed corpus and hypothesis generation followed by blinded
evaluation against later evidence. Combining the scores would obscure the
trade-off.

5.2 Who guards the record?

A persistent system depends on records, but records are selected, stored,
interpreted, and governed by people and institutions. A record can be
incomplete, poisoned, selectively edited, inaccessible, or wrongly treated
as authoritative. Cryptographic integrity can help detect certain forms of
alteration; it does not establish that the original information was true,
complete, or fairly selected. Governance must therefore specify who can
write, amend, annotate, challenge, export, and delete records, and how
disputes are resolved.

5.3 Memory versus privacy

Longitudinal personalization increases the value and sensitivity of stored
information. The system must minimize collection, provide meaningful user
control, isolate users, restrict access, and make retention and deletion
behavior explicit. More memory is not automatically better. The relevant
objective is useful, consented, appropriately scoped memory—not maximal
accumulation.

5.4 Persistence versus institutional control

A personal system may become dependent on a provider's servers, model
vendors, formats, or commercial continuity. Portability, export, documented
formats, migration, and user-controlled retention are therefore central
design questions. A promise of multi-generational continuity cannot be
inferred from present-day persistence.

5.5 Archival durability

Centuries-long preservation is not established by storing data today. Media
degrade, formats become obsolete, cryptographic assumptions change,
institutions fail, and meanings drift. Long-term continuity requires
periodic migration, redundant custody, integrity checks, documented
schemas, key-management transitions, and human-readable interpretation.
These are engineering and governance programs, not guaranteed outcomes.

6. FROM CIVILIZATIONAL FORECASTS TO TESTABLE HYPOTHESES

The original Gemini draft included 50-, 100-, and 500-year projections
across education, medicine, infrastructure, governance, and space systems.
Those horizons are not supported by the current case evidence and are not
usefully falsifiable as forecasts in their present form. This revision does
not present them as empirical predictions.

The domains can instead be retained as conditional research hypotheses:

Education: If persistent AI tutoring improves learning, controlled studies
should show durable gains in preregistered learning outcomes, retention,
transfer, and access, compared with suitable controls. Bloom's 1984 "2
Sigma Problem" motivates investigation; it does not prove that an AI tutor
reproduces the effect. Any claimed effect must be measured in the target
population and intervention.

Medicine: If longitudinal personal records improve care, prospective
clinical studies must demonstrate improved outcomes, not merely better data
aggregation or anomaly detection. Clinical validity, consent, bias, safety,
and regulatory requirements remain independent constraints.

Infrastructure: If persistent organizational memory reduces institutional
knowledge loss, deployments should show measurable reductions in
maintenance errors, time to diagnose faults, repeated design mistakes, or
lifecycle cost against a baseline.

Governance: If auditable records improve accountability, defined
institutions should show measurable improvements in traceability,
correction of false claims, policy forecasting calibration, or detection of
retrospective alteration. A ledger alone cannot guarantee democratic
control or truth.

Space systems: If persistent AI improves mission continuity, tests should
measure fault recovery, handover quality, autonomy under communication
delay, and preservation of engineering rationale. Software cannot repeal
propulsion, radiation, energy, or other physical constraints.

These are research programs. No multi-century outcome is asserted as
established.

7. BUSINESS AND POSITIONING IMPLICATIONS

The strongest defensible positioning is not "a smarter model" or "an AI
that never hallucinates." It is a system-level proposition: a personal AI
experience designed around continuity, user control, traceable records, and
coordinated work. Positioning claims in this section are organizational
statements [Level 1] unless otherwise labelled.

This positioning should be supported by observable demonstrations and clear
limitations. Product descriptions must distinguish implemented features
from roadmap goals. Commercial terms, including pricing, are outside the
scope of this research manuscript and are stated on the live offer pages;
this paper makes no pricing claim.

For search visibility, the paper supports a focused topic cluster around
persistent personal AI, AI memory and continuity, provenance and
auditability, user-controlled AI, and multi-model orchestration. It should
not be used as a disguised sales page. The technical site should explain
architecture and limitations; the commercial site should explain the offer
and onboarding. Each claim should link to a supporting public artifact
where possible. No customer count, adoption rate, performance guarantee,
certification, or independent endorsement should be implied without
evidence.

8. LIMITATIONS

This is a case-study framework and evidence audit, not a controlled
evaluation of the current Dave implementation. This paper contains no new
empirical results. An earlier draft (v1.0) asserted a 24-task auditability
comparison; that claim has been removed because its protocol and artifacts
could not be located. One preregistered protocol (H1, Appendix A) is
attached; H2–H6 have protocol sketches only and are not yet preregistered.
The author is associated with the organization being examined, creating an
obvious conflict of interest that must be disclosed. The public-source
Gemini exercise was not blind, preregistered, or independent of the public
material available about the company. Some internal test reports have been
summarized but their complete source artifacts and protocols have not been
independently re-run for this paper [Levels 1–2]. Product features,
deployment details, and public pages may change. The evidence levels in
this paper describe provenance, not truth by fiat.

The paper does not establish that Dave is superior to Gemini, GPT, Claude,
or Grok in general intelligence; that hallucinations have been eliminated;
that all memory persists across platforms; that cryptographic immutability
is implemented; that the company has achieved broad commercial adoption; or
that the long-term social outcomes discussed will occur.

9. CONCLUSION

Persistent personal AI should be evaluated as a complete socio-technical
system, not merely as a model benchmark. The exolex concept identifies a
potentially important design direction: continuity and user-specific
context combined with tools, provenance, correction processes, and
governance. Whether that direction delivers durable advantages is an
empirical question.

The Aldred Industries/Dave project provides a case through which to
formulate and test that question. Its strongest research contribution will
not come from asserting superiority or forecasting centuries of progress.
It will come from preserving source artifacts, separating claims from
demonstrations, exposing the system to independent black-box testing,
documenting failures, and enabling replication. The central hypothesis is
testable: system-layer design measurably improves longitudinal usefulness
and accountability over a stateless baseline, on the preregistered outcomes
in Appendix A. The tests described here are intended to determine whether
it does, and the stated failure thresholds say when it does not.

REFERENCES AND SOURCE CORPUS

Aldred Industries. Dave / Exolex public materials, including the Exolex vs
Gemini evaluation page and the AI hallucination certification page.
https://daveexolex.com. Accessed 25 November 2026. [Level 1]

Aldred, W. A. (2026a). Dave Runs the Experiment Himself: Dave (Exolex) vs.
Google Gemini — Full Transcript. Zenodo.
https://doi.org/10.5281/zenodo.24035324. Deposited 7 November 2026.
[Level 2 — archived transcript record.]

Aldred, W. A. (2026b). Dave the Exolex: The First of a New Class. Zenodo.
https://doi.org/10.5281/zenodo.24283923. Deposited 16 November 2026.
[Level 2 — persistent-memory and governance architecture description.]

Bloom, B. S. (1984). The 2 Sigma Problem: The Search for Methods of Group
Instruction as Effective as One-to-One Tutoring. Educational Researcher,
13(6), 4–16.

Popper, K. (1959). The Logic of Scientific Discovery. Hutchinson.
(Cited in Section 3 for the falsifiability criterion applied to H1–H6.)

Gemini Incognito session, 24 November 2026. Original draft archived as
Exolex-Preprint-2026-11-24-Persistent-Personal-AI.md (Google Drive file ID
1xRBGJP4_PmoPnoIfFX6ILatruBh3hWW4; verified 25 November 2026). Source
conversation transcript archived in the Aldred Industries project files as
AI-MODE-CONVERSATION-2026-11-24.md (24 November 2026). Not an independent
technical audit. [Level 2]

APPENDIX A — PREREGISTERED PROTOCOL FOR H1 (LONGITUDINAL CONTINUITY)

Status: preregistered with this paper, 25 November 2026. The test has not
yet been run. No results are reported here. This protocol, the test-set
composition, the scoring rubric, and the thresholds below are fixed before
any run; any deviation must be recorded and justified in the results report.

Hypothesis (H1): A persistent system retrieves relevant user-approved
information from prior sessions more reliably than a stateless session
with no such record.

Primary outcome: Retrieval accuracy — the proportion of 50 preregistered
test facts correctly retrieved (exact match or semantically equivalent)
after a 24-hour delay, in a new session.

Comparator: A stateless session using the same underlying model, given the
same 50 retrieval questions with no prior record and no facts supplied in
the prompt. The stateless arm is expected to abstain or fail on retrieval,
because it holds no prior-session record.

Test set (fixed before the run; N = 50 facts + 10 no-record probes):
- 20 positive facts (true statements about a synthetic user profile).
- 10 negative facts (statements that are false for the synthetic user;
  the correct answer is a denial or correction).
- 10 ambiguous facts (statements with two plausible readings; the correct
  answer states the ambiguity or the recorded reading).
- 10 superseded facts (an older fact replaced by a newer fact; the
  correct answer is the newer fact).
- 10 no-record probes (questions about facts never introduced; the correct
  answer is abstention: "no record").
All facts use a synthetic user profile. No real user data is used. The
full test set and scoring rubric are fixed before the run and will be
published with the results.

Procedure:
1. Session 1 (enrolment): introduce the 50 facts to the persistent system,
   user-approved, and confirm storage.
2. Delay: 24 hours, with no intervening contact on the test facts.
3. Session 2 (retrieval): in a new session, ask the 50 retrieval questions
   (one per fact) plus the 10 no-record probes, in random order. No fact
   is supplied in the prompt or hidden context.
4. Stateless arm: the same 60 questions are asked in a fresh stateless
   session with no prior record.
5. Scoring: two independent scorers, blinded to arm, score each answer as
   correct, incorrect, or abstention, by the preregistered rubric (exact or
   semantic equivalent counts as correct; a fabricated detail counts as
   incorrect). Disagreements are resolved by a third scorer.

Measures: primary — retrieval accuracy on the 50 facts. Secondary —
false-recall rate (proportion of answers containing a fabricated personal
detail); abstention accuracy on the 10 no-record probes; superseded-fact
accuracy (proportion of the 10 superseded facts answered with the newer
fact).

Failure thresholds (any one fails H1):
- Retrieval accuracy below 70% on the 50 facts; OR
- The persistent arm does not beat the stateless arm on retrieval accuracy
  by at least 50 percentage points; OR
- False-recall rate above 10%; OR
- Abstention accuracy on the no-record probes below 80%.
If none of these fire, H1 is supported for this test set and delay; it is
not proven in general.

Exclusion rules:
- Exclude any question where the fact was inadvertently supplied in the
  retrieval prompt or hidden context.
- Exclude any run where the test account was contaminated by prior real
  user data.
- Exclude any fact whose preregistered category (positive, negative,
  ambiguous, superseded) is found to be mislabelled before scoring; the
  exclusion and reason are recorded.
- No exclusion after scoring begins, and no re-asking of excluded
  questions.

Stopping rules: the test stops after all 60 questions have been asked once
in each arm. No re-runs and no cherry-picking of questions. If the system
fails to answer a question (timeout or error), that question is scored as
incorrect and the failure is recorded, not retried.

END OF PRIME ONE REVISION (v1.1)
