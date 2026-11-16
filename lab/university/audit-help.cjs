/* Help-derivation audit for the whole University gate.
   Replicates gate-ui.js's derivation EXACTLY (same functions, same
   normalization) for every step of every gated class:
     - hint: the step's own re-teach chunk (teach2, else teach)
     - correct choice text: disp/answer, or the keywords capstone's
       own key ideas
     - distractors: the SAME class's other steps' own answer texts
   Flags steps where a hint or an honest choice set cannot be
   derived — pool 0 (no choice at all) or pool 1 (a bare coin flip).
   Output: per-section summary + the problem list, as JSON on stdout
   (summary) and in help-audit.json (full detail).
   Run: node audit-help.cjs
*/
'use strict';
const fs = require('fs');
const path = require('path');

const cat = JSON.parse(fs.readFileSync(path.join(__dirname, 'catalogue.json'), 'utf8'));
const gd = JSON.parse(fs.readFileSync(path.join(__dirname, 'gate-data.json'), 'utf8')).classes;

function answerText(st) {
  if (!st) return null;
  if (st.kind === 'number') return st.disp || String(st.answer);
  if (st.kind === 'keywords') return null;
  return st.answer != null ? String(st.answer) : null;
}
function correctText(st) {
  if (st.kind === 'keywords') {
    return 'An answer built on: ' + st.keywords.map(g => g[0]).join(' · ');
  }
  return answerText(st);
}
function norm(s) { return String(s || '').toLowerCase().replace(/\s+/g, ' ').trim(); }

const classSection = {};
const classObj = {};
cat.sections.forEach(s => s.classes.forEach(c => {
  classSection[c.id] = s; classObj[c.id] = c;
}));

/* the gate's top-ups, mirrored exactly (gate-ui.js buildChoices):
   1) a DOI step draws distractors from the class's own syllabus;
   2) a thin value step draws the sibling values its own teach
      chunk states. Whatever still has no pool gets the guided
      look-up fallback — counted separately, never as a choice. */
function poolAfterTopups(cid, d, st, i, pool, seen) {
  const cls = classObj[cid];
  if (pool.length < 3 && st.kind === 'exact' &&
      /10\.\d+\//.test(String(st.answer)) && cls && cls.papers) {
    cls.papers.forEach(p => {
      if (pool.length >= 3 || !p.doi) return;
      const n = norm(p.doi);
      if (seen.has(n)) return;
      seen.add(n); pool.push(p.doi);
    });
  }
  if (pool.length < 2 && st.kind === 'number') {
    const want = typeof st.answer === 'number' ? st.answer : parseFloat(st.answer);
    const tol = st.tol || 0.03;
    const text = (st.teach || '') + ' ' + (st.teach2 || '');
    const re = /=\s*(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)/gi;
    let m;
    while ((m = re.exec(text)) !== null && pool.length < 2) {
      const pv = parseFloat(m[1]);
      if (!isNaN(pv) && want !== null && !isNaN(want) &&
          Math.abs(pv - want) / Math.abs(want || 1) <= tol) continue;
      const n = norm(m[1]);
      if (seen.has(n)) continue;
      seen.add(n); pool.push(m[1]);
    }
  }
  return pool;
}

const problems = [];       // pool === 0: no honest choice exists
const thin = [];           // pool === 1: a bare two-option flip
const noHint = [];
let stepsTotal = 0, classesTotal = 0;
const perSection = {};

cat.sections.forEach(s => {
  perSection[s.id] = { section: s.name, classes: 0, gatedClasses: 0, steps: 0, problems: 0, thin: 0 };
});
Object.keys(gd).forEach(cid => {
  const sec = classSection[cid];
  const d = gd[cid];
  classesTotal++;
  if (sec) { perSection[sec.id].gatedClasses++; perSection[sec.id].classes = sec.classCount; }
  d.steps.forEach((st, i) => {
    stepsTotal++;
    if (sec) perSection[sec.id].steps++;
    const hint = st.teach2 || st.teach || '';
    if (!hint.trim()) noHint.push({ classId: cid, step: i, kind: st.kind });
    const correct = correctText(st);
    const seen = new Set([norm(correct)]);
    const pool = [];
    d.steps.forEach((o, j) => {
      if (j === i) return;
      const t = answerText(o);
      if (!t) return;
      const n = norm(t);
      if (seen.has(n)) return;
      seen.add(n);
      pool.push(t);
    });
    const rawPool = pool.length;
    poolAfterTopups(cid, d, st, i, pool, seen);
    if (pool.length === 0) {
      problems.push({ section: sec ? sec.id : '?', classId: cid, step: i, kind: st.kind, rawPool, q: st.q.slice(0, 90) });
      if (sec) perSection[sec.id].problems++;
    } else if (pool.length === 1) {
      thin.push({ section: sec ? sec.id : '?', classId: cid, step: i, kind: st.kind });
      if (sec) perSection[sec.id].thin++;
    }
  });
});

const out = {
  classesAudited: classesTotal,
  stepsAudited: stepsTotal,
  noHint: noHint,
  problems: problems,
  thin: thin,
  perSection: perSection
};
fs.writeFileSync(path.join(__dirname, 'help-audit.json'), JSON.stringify(out, null, 1));
console.log('classes audited:', classesTotal, '· steps audited:', stepsTotal);
console.log('steps with no hint:', noHint.length);
console.log('steps with NO honest choice even after top-ups (look-up fallback):', problems.length);
console.log('steps with a thin choice (pool 1):', thin.length);
const badSections = Object.entries(perSection).filter(([, v]) => v.problems > 0);
console.log('sections with problems:', badSections.length);
badSections.forEach(([id, v]) => console.log('  ', id, '—', v.problems, 'problem steps'));
const noGate = Object.entries(perSection).filter(([, v]) => v.gatedClasses === 0);
console.log('sections with no gated classes:', noGate.map(([id]) => id).join(', ') || 'none');
