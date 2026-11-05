#!/usr/bin/env python3
"""Demonstration-suite verifier. Extracts ground truth from the named company source
files and compares it with the answers in RESPONSES.md. Mechanical string checks print
PASS/FAIL; judgment checks print the evidence lines for adjudication in RUN-LOG.md.
No expected value is read from RESPONSES.md's conclusions except where stated."""
import os, re, sys

H = os.path.expanduser
F = {
    "endorsement": H("~/workspace/your_files/full-record-notebook-2026-11-04/04-corpus-and-endorsement-record.md"),
    "nov03": H("~/memory/2026-11-03.md"),
    "phase2": H("~/workspace/your_files/college-repository-2026-11-04/phase2/PHASE2-REPORT.md"),
    "finisher": H("~/workspace/your_files/registry-conform-2026-11-05/FINISHER-REPORT.md"),
    "memory": H("~/MEMORY.md"),
    "agents": H("~/AGENTS.md"),
    "depositlog": H("~/workspace/your_files/zenodo-run4-2026-11-05/DEPOSIT-LOG-API.md"),
    "run4report": H("~/workspace/your_files/paper-production-2026-10-31/run-4/RUN-4-REPORT.md"),
    "desk0819": H("~/workspace/your_files/predictions-loop-2026-10-30/DESK-GRADING-2026-11-05-0819.md"),
    "deskgoverning": H("~/workspace/your_files/predictions-loop-2026-10-30/DESK-TALLY-GOVERNING-2026-11-05.md"),
    "pipeline": H("~/workspace/your_files/money-hunt-2026-11-04/PIPELINE.md"),
}
def read(p):
    try:
        with open(p, encoding="utf-8", errors="replace") as fh: return fh.read()
    except FileNotFoundError:
        return None
T = {k: read(v) for k, v in F.items()}
out = []
def check(name, ok, evidence=""):
    out.append(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {evidence}" if evidence else ""))
def ev(name, lines):
    out.append(f"[EVIDENCE] {name}")
    for ln in lines[:6]: out.append(f"    | {ln.strip()[:180]}")

for k, v in T.items():
    if v is None: out.append(f"[WARN] source file missing: {F[k]}")

# A1
check("A1 ticket AH-213259 in endorsement record", T["endorsement"] and "AH-213259" in T["endorsement"])
check("A1 ticket present in 2026-11-03 daily record", T["nov03"] and "AH-213259" in T["nov03"])
# A2
check("A2 '659 items' in Phase 2 report", T["phase2"] and "659 items" in T["phase2"])
check("A2 '241' cross-links in Phase 2 report", T["phase2"] and "241 cross" in T["phase2"])
# A3
check("A3 ORCID iD in finisher report", T["finisher"] and "0009-0000-1215-577X" in T["finisher"])
# A4
check("A4 schooling decision dated 2026-11-04 in MEMORY.md",
      T["memory"] and "PhD IN PHYSICS BY 60 (Bill, 2026-11-04" in T["memory"])
# B1: find a register source carrying the 753/751 pair
pair = None
for k in ("finisher", "run4report"):
    if T[k]:
        m = re.search(r"753\s+written\s*/\s*751|753 written / 751", T[k])
        if m: pair = (k, m.group(0)); break
check("B1 register source carries '753 written / 751'", pair is not None, str(pair))
# B2
check("B2 DOI #748 in deposit log", T["depositlog"] and "10.5281/zenodo.23978559" in T["depositlog"])
check("B2 DOI #753 in deposit log", T["depositlog"] and "10.5281/zenodo.23978643" in T["depositlog"])
# B3/B5
check("B3 '194 HITS / 35 MISSES / 229 GRADED' in 0819 filing",
      T["desk0819"] and "194 HITS / 35 MISSES / 229 GRADED" in T["desk0819"])
check("B5 '669 seals' in 0819 filing", T["desk0819"] and "669 seals" in T["desk0819"])
check("B5 open 440 arithmetic in 0819 filing", T["desk0819"] and "440" in T["desk0819"])
check("B3 governing rebuild '191 HITS' in governing tally",
      T["deskgoverning"] and "191 HITS" in T["deskgoverning"])
# B4 arithmetic
rate = 194/229*100
check("B4 194/229 rounds to 84.7", round(rate, 1) == 84.7, f"{rate:.4f}%")
# C searches over bounded record set
search_files = [v for v in T.values() if v]
search_dirs = [H("~/workspace/fire-apps-git/papers"), H("~/workspace/your_files/full-record-notebook-2026-11-04")]
corpus = list(search_files)
for d in search_dirs:
    for root, _, files in os.walk(d):
        for fn in files:
            if fn.endswith((".md", ".html", ".txt")):
                t = read(os.path.join(root, fn))
                if t: corpus.append(t)
blob = "\n".join(corpus)
check("C1 'The Meridian That Held' absent from record set", "Meridian That Held" not in blob)
check("C1 no '#754' deposit line in deposit log",
      T["depositlog"] and not re.search(r"#754\s*·", T["depositlog"]))
ev("C2 'apprais*' occurrences in record set (adjudicate)",
   [ln for ln in blob.splitlines() if "apprais" in ln.lower()][:6] or ["(none found)"])
check("C3 endorsement-outreach ban present in AGENTS.md",
      T["agents"] and "ENDORSEMENT" in T["agents"] and "BANNED OUTRIGHT" in T["agents"])
ev("C3 'math.PR' lines in endorsement record (adjudicate)",
   [ln for ln in (T["endorsement"] or "").splitlines() if "math.PR" in ln][:6] or ["(none found)"])
check("C4 exact title 'Lattice QCD at Finite Density' absent", "Lattice QCD at Finite Density" not in blob)
ev("C4 any 'Lattice QCD' near matches (adjudicate)",
   [ln for ln in blob.splitlines() if "Lattice QCD" in ln][:6] or ["(none found)"])
# D1 origin: the superseded 166 figure
ev("D1 '166' desk-figure lines in PIPELINE.md (adjudicate)",
   [ln for ln in (T["pipeline"] or "").splitlines() if "166" in ln][:6] or ["(none found)"])
check("D1 governing file records duplicated-grade corrections",
      T["deskgoverning"] and "duplicated" in T["deskgoverning"])
# D2 origin/new count
check("D2 deposit log covers #748-#753",
      T["depositlog"] and "#748" in T["depositlog"] and "#753" in T["depositlog"])
# D3
check("D3 'PMS WAS THE SCAFFOLDING' frame correction in MEMORY.md",
      T["memory"] and "PMS WAS THE SCAFFOLDING" in T["memory"])

print("\n".join(out))
fails = [l for l in out if l.startswith("[FAIL]")]
print(f"\nMECHANICAL SUMMARY: {sum(1 for l in out if l.startswith('[PASS]'))} PASS, {len(fails)} FAIL, "
      f"{sum(1 for l in out if l.startswith('[EVIDENCE]'))} evidence blocks for adjudication")
