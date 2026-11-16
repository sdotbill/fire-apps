/* The Laboratory — the Room: shared logic core.
   Pure data + functions, no DOM, no three.js. The room page loads this
   file, and the headless verifier runs the identical code in Node, so
   what is tested is exactly what the page uses: the station registry,
   the guided-step definitions, the session timer, and the University
   hours log. The physics itself lives in ../lab-core.js, untouched. */
(function (global) {
  'use strict';

  /* ==================== Stations ====================
     Each station: an object in the room, its explanation card, and its
     guided walk. A step advances either by the visitor pressing Next
     ('button') or by an instrument state check ('action'). Checks are
     declarative — {control, op, value} or {all: [...]} — interpreted by
     the page against the live instrument state, whose keys are the raw
     control values: beta (0..1), df (slider −30..30, 0.1% steps),
     gamma (0..100), d (mm), playing (bool), nearBounce (bool),
     panelOpen (bool). */

  var STATIONS = [
    {
      id: 'watchfloor',
      name: 'The Watch Floor',
      title: 'The Watch Floor — the bounce, live',
      kind: 'instrument',
      what: 'A wall-sized screen running the bounce-frame cosmology ' +
        'integrator: a universe in collapse, with the Aldred Limit ' +
        'written into its equations.',
      does: 'It integrates the bounce-frame Friedmann equation live, in ' +
        'your browser — no canned curves. Density climbs toward the ' +
        'Limit (ρ_A = 2.92×10⁵⁵ g/cm³); there the density-squared term ' +
        'cancels gravity\u2019s pull exactly, H passes through zero, and ' +
        'the universe re-expands instead of crushing to a singularity. ' +
        'The torsion control adds Riemann–Cartan spin repulsion, which ' +
        'fires the bounce earlier, at a lower peak.',
      principle: 'Design with the limit inside the equations. On this ' +
        'theory spacetime itself has a rated maximum density, the way a ' +
        'pressure vessel has a rated maximum pressure — and a competent ' +
        'engineer never designs past the rating.',
      steps: [
        { text: 'Take control of the run: press Pause, and the universe ' +
                'holds still for you.',
          advance: 'action', check: { control: 'playing', op: '==', value: false } },
        { text: 'Drag Torsion (β) up to 0.60 and read the Peak line. ' +
                'Spin pushes back harder the denser things get, so the ' +
                'bounce fires early — the peak drops to about 55% of ' +
                'the Limit.',
          advance: 'action', check: { control: 'beta', op: '>=', value: 0.55 } },
        { text: 'Bring Torsion back to zero. Now the Aldred cap does all ' +
                'the work alone — the peak touches the Limit exactly, ' +
                'and never passes it.',
          advance: 'action', check: { control: 'beta', op: '<=', value: 0.05 } },
        { text: 'Press Run, then scrub the run to the centre — the ' +
                'bounce itself, the moment H passes through zero and ' +
                'collapse turns around.',
          advance: 'action', check: { control: 'nearBounce', op: '==', value: true } },
        { text: 'That is the whole experiment: one equation, two ' +
                'rescues — the cap, and spin. Close the instrument and ' +
                'look around; the Bench is across the room.',
          advance: 'button' }
      ]
    },
    {
      id: 'bench',
      name: 'The Bench',
      title: 'The Bench — the phase-matched charging pad',
      kind: 'instrument',
      what: 'A design bench for the fifth-coordinate phase-matched ' +
        'inductive charging pad: two resonant coils passing power ' +
        'across a gap, one in the pad and one in the vehicle.',
      does: 'Five controls — coil separation, lateral misalignment, ' +
        'coil quality Q, drive detuning, phase-match compensation — ' +
        'feed the standard coupled-mode model of two resonators. Every ' +
        'number on the bench is derived from those equations live; ' +
        'nothing is fitted, and nothing is looked up.',
      principle: 'Wireless power is a conversation, not a broadcast. ' +
        'The whole game is the figure of merit U = k·√(Q₁Q₂) — coupling ' +
        'times quality — and every real design feature exists to ' +
        'protect U.',
      steps: [
        { text: 'Set the pad up badly, the way a rushed installer ' +
                'would: Drive detuning to +3.0%, and Phase-match ' +
                'compensation all the way down to 0%.',
          advance: 'action',
          check: { all: [ { control: 'df', op: '>=', value: 28 },
                          { control: 'gamma', op: '<=', value: 2 } ] } },
        { text: 'Read the damage: Delivered η has fallen far below Best ' +
                'possible η. Detuned, the two coils fall out of step — ' +
                'energy sloshes across and sloshes back before the ' +
                'receiver can keep it.',
          advance: 'button' },
        { text: 'Now the rescue: raise Phase-match compensation to 70% ' +
                'or more. That control is the fifth-coordinate element ' +
                'of the design — a tracker that re-times the drive so ' +
                'the resonators stay in step.',
          advance: 'action', check: { control: 'gamma', op: '>=', value: 68 } },
        { text: 'Last lesson, and it is an honest one: drag Coil ' +
                'separation out to 120 mm. The phase-matcher cannot ' +
                'save you now — coupling dies with distance, and the ' +
                'efficiency falls off its cliff. That cliff is the real ' +
                'limit of the design.',
          advance: 'action', check: { control: 'd', op: '>=', value: 115 } },
        { text: 'Bench work done: set it up badly, read the damage, ' +
                'rescue what can be rescued — and learn what cannot.',
          advance: 'button' }
      ]
    },
    {
      id: 'university',
      name: 'The University Door',
      title: 'The University Door — Exolex University',
      kind: 'door',
      what: 'The door to Exolex University. The Lab is one of its ' +
        'classrooms: the lessons here are real classes, taught by ' +
        'doing the work at the instruments, not by watching someone ' +
        'else do it.',
      does: 'Your time in this room is logged honestly — the session ' +
        'clock runs only while you are here with the room in front of ' +
        'you — and written to your Lab log: the date, the minutes, the ' +
        'stations you worked, the guided steps you completed. Those ' +
        'receipts are the seed of your University record.',
      principle: 'Credit follows work that can be shown. Every session ' +
        'in this room writes its own receipt, and the ledger only ever ' +
        'grows by real time at real work.',
      steps: [
        { text: 'This door is a classroom door. Everything you do in ' +
                'the Lab counts as University work — the instruments ' +
                'are the lessons.',
          advance: 'button' },
        { text: 'Open the University panel and find “My hours” — your ' +
                'logged time in the room, totalled from your own ' +
                'session receipts.',
          advance: 'action', check: { control: 'panelOpen', op: '==', value: true } },
        { text: 'That is the ledger. Kept honestly, it is the record a ' +
                'certificate will one day be printed from — hours first, ' +
                'paper second.',
          advance: 'button' }
      ]
    }
  ];

  function stationById(id) {
    for (var i = 0; i < STATIONS.length; i++) {
      if (STATIONS[i].id === id) return STATIONS[i];
    }
    return null;
  }

  /* Evaluate a declarative step check against an instrument state. */
  function checkPasses(check, state) {
    if (!check) return false;
    if (check.all) {
      return check.all.every(function (c) { return checkPasses(c, state); });
    }
    var v = state ? state[check.control] : undefined;
    if (typeof v === 'undefined') return false;
    switch (check.op) {
      case '==': return v === check.value;
      case '!=': return v !== check.value;
      case '>=': return v >= check.value;
      case '<=': return v <= check.value;
      case '>':  return v >  check.value;
      case '<':  return v <  check.value;
      default:   return false;
    }
  }

  /* ==================== Session timer ====================
     Real elapsed time in the room only. The page pauses the timer
     whenever the tab is hidden, so a room left open in a background
     tab earns nothing. The clock is injected for testability. */
  function createSessionTimer(nowFn) {
    var now = nowFn || function () { return Date.now(); };
    var accumulated = 0;      // ms banked from finished running spans
    var spanStart = null;     // ms timestamp of the current span, or null
    return {
      start: function () {
        if (spanStart === null) spanStart = now();
      },
      pause: function () {
        if (spanStart !== null) {
          accumulated += now() - spanStart;
          spanStart = null;
        }
      },
      resume: function () { this.start(); },
      isRunning: function () { return spanStart !== null; },
      elapsedMs: function () {
        return accumulated + (spanStart !== null ? now() - spanStart : 0);
      },
      elapsedMinutes: function () { return this.elapsedMs() / 60000; }
    };
  }

  /* ==================== The hours log ====================
     localStorage key 'dave_lab_log': an array of session entries
       { date: ISO string (session end), minutes: number,
         stations: [station ids, in first-visit order],
         stepsCompleted: number }
     Storage is injected (localStorage in the page, a stub in tests). */
  var LOG_KEY = 'dave_lab_log';

  function loadLog(storage) {
    try {
      var raw = storage.getItem(LOG_KEY);
      if (!raw) return [];
      var parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  function makeEntry(opts) {
    var stations = [];
    (opts.stations || []).forEach(function (id) {
      if (stations.indexOf(id) === -1) stations.push(id);
    });
    return {
      date: opts.date,
      minutes: Math.round((opts.minutes || 0) * 10) / 10,
      stations: stations,
      stepsCompleted: opts.stepsCompleted || 0
    };
  }

  function appendEntry(storage, entry) {
    var log = loadLog(storage);
    log.push(entry);
    storage.setItem(LOG_KEY, JSON.stringify(log));
    return log;
  }

  function summarizeLog(log) {
    var totalMinutes = 0, totalSteps = 0, stations = [];
    (log || []).forEach(function (e) {
      totalMinutes += e.minutes || 0;
      totalSteps += e.stepsCompleted || 0;
      (e.stations || []).forEach(function (id) {
        if (stations.indexOf(id) === -1) stations.push(id);
      });
    });
    return {
      sessions: (log || []).length,
      totalMinutes: Math.round(totalMinutes * 10) / 10,
      totalSteps: totalSteps,
      stationsWorked: stations
    };
  }

  function formatMinutes(mins) {
    var m = Math.round(mins || 0);
    if (m < 60) return m + ' min';
    var h = Math.floor(m / 60), rem = m % 60;
    return h + ' h ' + (rem < 10 ? '0' : '') + rem + ' min';
  }

  var api = {
    STATIONS: STATIONS,
    stationById: stationById,
    checkPasses: checkPasses,
    createSessionTimer: createSessionTimer,
    LOG_KEY: LOG_KEY,
    loadLog: loadLog,
    makeEntry: makeEntry,
    appendEntry: appendEntry,
    summarizeLog: summarizeLog,
    formatMinutes: formatMinutes
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.RoomCore = api;
})(typeof window !== 'undefined' ? window : globalThis);
