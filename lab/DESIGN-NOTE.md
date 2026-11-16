# The Laboratory — design note (stage 1, 2026-11-15)

Bill's order, in his words: a digital laboratory on the dashboard — "a digital
one where we do real science, your simulations, everything's like you're doing
it but I want to be able to watch you do it… like a science bench… we can
digitally build the things that we have in our blueprints, build them together
and see how it works, and teach me how to be more an engineer." Built on
practice pages first, iterated until it's right; Prime is told when it's
getting there.

## The shape — three parts, always together

**1. The Watch Floor.** Live simulations with plotted output, running in front
of Bill — real computations in the page, never animations of pre-baked curves.
A run can be played, paused, scrubbed, and re-run with different parameters
while he watches. Stage 1 ships the bounce-frame cosmology integrator: RK4
integration of the bounce-frame Friedmann equation with the Aldred Limit
inside it (ρ_A = 2.92×10⁵⁵ g/cm³, the repaired value). Density rises, the
ρ²/ρ_A term cancels the pull exactly at the cap, H passes through zero, and
the universe re-expands. A torsion slider (β, the Riemann–Cartan spin
repulsion ~ A⁻⁶) makes the bounce fire earlier at a lower peak density — the
two rescues, side by side, from one equation.

**2. The Bench.** One blueprint design at a time: set its parameters, run it,
see how it behaves. Stage 1 bench: **the fifth-coordinate phase-matched
inductive charging pad.** Why this one first: its physics is the standard
coupled-resonator (coupled-mode) model — exact equations, parameters a hand
can feel (separation, misalignment, Q, detuning, phase-match), and no fitted
material data, so every number on the bench is derived, not looked up. (The
magnetocaloric module was the runner-up; it needs measured material curves
for gadolinium before it can be run honestly, so it waits for stage 2 with
its data attached.) The bench's teaching moment is built in: detune the pad
with the phase-matcher off and watch it bleed, then rescue it.

**3. The Teaching Rail.** Every station carries the same three notes, in
plain words, at full substance (Bill is on a PhD track — no dumbing down,
just no jargon without a translation): *What you're seeing* / *Why it
behaves that way* / *The engineering principle*. The rail is what turns a
simulation into a lesson and a blueprint into engineering judgment.

## Honesty rules for everything the Lab ever shows

- Everything computes live; no canned curves, no fake animations.
- The page and the verifier run the *same* code file (`lab-core.js`), so
  what is tested is what Bill sees.
- Model limits are printed on the station itself (radiation content,
  dimensionless time, identical coils, coupled-mode first pass).

## Verification, stage 1 (all headless, all passing)

- Integrator: β=0 peak = ρ_A exactly, density never exceeds the cap,
  monotone rise then fall through the bounce; β=0.3/0.6/1.0 peaks match the
  analytic A_b⁻⁴ prediction to <0.5% (74.2% / 55.4% / 38.2% of cap).
- Bench: default operating point η=87.8% (k=0.052, U=15.6); efficiency
  falls monotonically with distance (96.0% → 87.8% → 23.8%); phase-matching
  rescues a 1%-detuned pad from 77.8% to 87.7%.
- Page smoke test: the page's own script, driven headlessly, animates,
  re-integrates on the torsion slider (peak readout moves to the predicted
  1.62×10⁵⁵ g/cm³ at β=0.6), and the bench sliders move the model.
- One numerical note: at the bounce point H=0 exactly, the first-order
  equation has a fixed point; the integrator records the exact bounce point
  and restarts a hair (10⁻⁶) onto the expansion branch, matching the true
  A − A_b ~ τ² passage. Documented in the code.

## Stage 2 (next)

- More benches from the blueprint shelf (magnetocaloric cooling module with
  its material data attached; the torsion pendulum rig; a transit-law
  demonstrator), chosen by the same honesty test: derivable in the open, or
  shipped with its data.
- Heavy simulations driven by the owner lane: long integrations and
  parameter sweeps run Dave-side and stream results to the Watch Floor, so
  Bill watches real work arrive, not just browser-weight math.
- An experiment log: every run Bill makes is written down (parameters,
  result, the note he was reading) — the Lab's own record page.
- The dashboard hookup: the Lab becomes a tab in Bill's dashboard (Prime's
  crew owns dashboard/index.html; the Lab arrives as its own page, wired in
  when that crew has a window).
- Bill-driven sessions: he sets a design problem, the bench is configured
  for it, and the Teaching Rail walks the iteration — version, result,
  critique, next version — the loop he already works by.

## Files (stage 1, standalone — not committed, not wired into any menu)

- `lab/index.html` — the practice page (white/gold, self-contained).
- `lab/lab-core.js` — the shared physics core (page + verifier).
- Verifiers lived in /tmp for the run: `lab-verify.js` (physics),
  `lab-page-smoke.js` (page drive test). Rebuild them from the checks
  listed above if a future stage needs them.
