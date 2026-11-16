/* Unit tests for gate-core.js — the general classroom gate checker.
   Run: node test-gate.js   (exit 0 = all pass) */
'use strict';
const G = require('./gate-core.js');

let pass = 0, fail = 0;
function check(name, cond) {
  if (cond) { pass++; }
  else { fail++; console.log('FAIL: ' + name); }
}
const num = (answer, said, tol) =>
  G.checkAnswer({ kind: 'number', answer, tol }, said);

/* --- number parsing --- */
check('parse plain sci', G.parseNumber('1.227e13') === 1.227e13);
check('parse times-ten form', Math.abs(G.parseNumber('1.227 × 10^13') - 1.227e13) < 1e2);
check('parse x10 form', Math.abs(G.parseNumber('1.227 x 10^13') - 1.227e13) < 1e2);
check('parse superscript form', Math.abs(G.parseNumber('1.227×10¹³') - 1.227e13) < 1e2);
check('parse comma integer', G.parseNumber('12,270,000,000,000') === 12270000000000);
check('parse decimal in prose', G.parseNumber('it is 0.0778 per unit') === 0.0778);
check('parse none', G.parseNumber('no number here') === null);

/* --- number gate --- */
check('exact value passes', num(1.227e13, '1.227e13').pass);
check('value with words and unit passes', num(1.227e13, 'T max is 1.227e13 K').pass);
check('student rounding passes (3 sig figs)', num(1.227e13, '1.23e13').pass);
check('longhand passes', num(1.227e13, '12270000000000').pass);
check('wrong value holds', !num(1.227e13, '5.0e12').pass);
check('wrong order of magnitude holds', !num(0.0778, '0.778').pass);
check('no number holds', !num(51.0, 'fifty one').pass);
check('zero key needs exact zero', num(0, '0').pass && !num(0, '0.5').pass);
check('integer with tolerance', num(833, '830').pass && !num(833, '700').pass);

/* --- exact gate --- */
const doi = { kind: 'exact', answer: '10.5281/zenodo.24147708' };
check('doi exact passes', G.checkAnswer(doi, '10.5281/zenodo.24147708').pass);
check('doi in a sentence passes',
  G.checkAnswer(doi, 'the DOI is 10.5281/zenodo.24147708 I think').pass);
check('wrong doi holds', !G.checkAnswer(doi, '10.5281/zenodo.99999999').pass);
const nm = { kind: 'exact', answer: 'proof by induction', accept: ['induction'] };
check('accept list passes', G.checkAnswer(nm, 'Induction').pass);
check('wrong concept holds', !G.checkAnswer(nm, 'direct proof').pass);

/* --- title gate (unit titles) --- */
const tt = { kind: 'title', answer: 'Integers, rationals, and why fractions behave' };
check('unit title passes', G.checkAnswer(tt, 'integers rationals and why fractions behave').pass);
check('unit title near-verbatim passes', G.checkAnswer(tt, 'Integers, rationals, and fractions').pass);
check('different unit holds', !G.checkAnswer(tt, 'Counting and the natural numbers').pass);
check('syllabus dump fails precision', !G.checkAnswer(tt,
  'counting integers rationals fractions irrational numbers proof induction sets functions').pass);

/* --- keyword gate (conceptual answers) --- */
const kw = { kind: 'keywords',
  keywords: [['largest'], ['natural number'], ['contradiction'], ['n + 1', 'one more']],
  need: 3 };
check('worked-answer concepts pass', G.checkAnswer(kw,
  'Suppose there is a largest natural number N; then N + 1 is bigger, contradiction').pass);
check('thin answer holds', !G.checkAnswer(kw, 'because numbers go on forever').pass);
check('empty holds', !G.checkAnswer(kw, '').pass);

/* --- grade bookkeeping --- */
const store = {};
const fakeStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v); }
};
check('recordStep writes', G.recordStep(fakeStorage, {
  date: '2026-11-16T07:45:00Z', classId: 'c1', classTitle: 'C1',
  step: 0, status: 'skip', attempts: 2
}));
G.recordStep(fakeStorage, {
  date: '2026-11-16T07:46:00Z', classId: 'c1', classTitle: 'C1',
  step: 0, status: 'pass', attempts: 3
});
G.recordStep(fakeStorage, {
  date: '2026-11-16T07:47:00Z', classId: 'c1', classTitle: 'C1',
  step: 1, status: 'skip', attempts: 0
});
G.recordStep(fakeStorage, {
  date: '2026-11-16T07:47:00Z', classId: 'other', classTitle: 'Other',
  step: 0, status: 'pass', attempts: 1
});
const states = G.loadStepStates(fakeStorage, 'c1');
check('pass outranks earlier skip', states[0] === 'pass');
check('skip recorded as skip', states[1] === 'skip');
check('states are per-class', G.loadStepStates(fakeStorage, 'other')[0] === 'pass');
const g = G.gradeFor(states, 4);
check('grade counts', g.passed === 1 && g.skipped === 1 && g.percent === 25);
check('recordGrade writes', G.recordGrade(fakeStorage, {
  date: '2026-11-16T07:48:00Z', classId: 'c1', classTitle: 'C1',
  states, total: 4, attempts: 5, complete: false
}));
const log = JSON.parse(store['dave_lab_log']);
const grade = log.find(e => e.kind === 'class-grade');
check('grade entry shape', grade && grade.passed === 1 && grade.skipped === 1 &&
  grade.percent === 25 && grade.minutes === 0 && grade.complete === false);

console.log(`gate-core: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
