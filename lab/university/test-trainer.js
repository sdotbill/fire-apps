/* Unit tests for trainer-core.js — the pronunciation gate.
   Run: node test-trainer.js   (exit 0 = all pass) */
'use strict';
const T = require('./trainer-core.js');

let pass = 0, fail = 0;
function check(name, cond) {
  if (cond) { pass++; }
  else { fail++; console.log('FAIL: ' + name); }
}
function grade(target, heard) { return T.gradeAttempt(target, heard); }

/* --- normalization --- */
check('normalize folds accents', T.normalizeSpeech('¡Buenos días!') === 'buenos dias');
check('normalize strips punctuation', T.normalizeSpeech("S'il vous plaît") === 's il vous plait');
check('normalize keeps Cyrillic', T.normalizeSpeech('Спасибо!') === 'спасибо');
check('normalize keeps hanzi', T.normalizeSpeech('你好。') === '你好');
check('normalize collapses spaces', T.normalizeSpeech('  me   llamo  ') === 'me llamo');

/* --- the gate: passes --- */
check('exact pass', grade('Hola', 'hola').pass);
check('accent-free heard passes', grade('Buenos días', 'buenos dias').pass);
check('case/punct ignored', grade('Me llamo Bill', '¡Me llamo Bill!').pass);
check('the flagship line passes', grade('Buenas noches, mi amor', 'buenas noches mi amor').pass);
check('full sentence passes', grade('Mi prometida se llama Jillian', 'mi prometida se llama jillian').pass);
check('one word off in a long sentence still passes (word-match)',
  grade('Mi prometida se llama Jillian', 'mi prometida se llama jilian').pass);
check('recognizer filler around a correct phrase passes',
  grade('Te quiero', 'eh te quiero').pass);
check('near-miss spelling passes at phrase level', grade('Mucho gusto', 'mucho gustó').pass);
check('native-script exact passes', grade('ありがとうございます', 'ありがとうございます').pass);
check('hanzi exact passes', grade('谢谢', '谢谢').pass);

/* --- the gate: misses must HOLD (no advance) --- */
check('wrong word holds', !grade('Hola', 'adios').pass);
check('short word missing letter holds', !grade('Hola', 'ola').pass);
check('empty heard holds', !grade('Hola', '').pass);
check('silence/null holds', !grade('Hola', null).pass);
check('different sentence holds', !grade('Soy de Michigan', 'soy empresario').pass);
check('half the sentence holds', !grade('Mi prometida se llama Jillian', 'mi prometida').pass);
check('gibberish holds', !grade('Buenas noches, mi amor', 'banana pancake seven').pass);
check('wrong language holds', !grade('Gracias', 'thank you very much').pass);

/* --- mastery log entries --- */
const store = {};
const fakeStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v); }
};
check('recordMastery writes', T.recordMastery(fakeStorage, {
  date: '2026-11-16T07:30:00Z', classId: 'espanol-i-speak-from-zero',
  classTitle: 'Español I', phrase: 'Hola', selfChecked: false
}));
const log = JSON.parse(store['dave_lab_log']);
check('entry shape: minutes stay 0 (hours untouched)', log[0].minutes === 0);
check('entry shape: kind + phrase carried',
  log[0].kind === 'phrase-mastery' && log[0].phrase === 'Hola');
const mastered = T.loadMastered(fakeStorage, 'espanol-i-speak-from-zero');
check('loadMastered reads it back', mastered['Hola'] === true);
check('loadMastered is per-class',
  Object.keys(T.loadMastered(fakeStorage, 'deutsch-i-speak-from-zero')).length === 0);

console.log(`trainer-core: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
