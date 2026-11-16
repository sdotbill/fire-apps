/* The Laboratory — physics core.
   Pure functions, no DOM. The practice page loads this file, and the
   headless verifier runs the identical code in Node, so what is tested
   is exactly what the page computes. Nothing here is a canned curve:
   every trajectory and readout is integrated / evaluated live. */
(function (global) {
  'use strict';

  /* ================= The bounce frame (Watch Floor) =================
     Dimensionless form. A = scale factor, normalized so that with zero
     torsion the bounce sits at A = 1. Radiation content:
         rho(A) = RHO_A * A^-4
     Bounce-frame Friedmann equation (the cap enters as rho^2 / RHO_A):
         H^2  ~  rho * (1 - rho / RHO_A)  -  torsion repulsion
     In units of H_A = sqrt(8 pi G RHO_A / 3), with tau = t * H_A:
         (1/A dA/dtau)^2 = A^-4 - A^-8 - beta * A^-6
     The A^-8 term is the Aldred cap: it grows faster than the A^-4
     content term as A shrinks, cancels it exactly at rho = RHO_A, and
     H passes through zero — collapse halts and reverses. The beta term
     is the Riemann–Cartan torsion contribution (spin density): a
     repulsion ~ A^-6 that makes the bounce happen earlier, at a lower
     peak density. beta = 0 is the pure cap bounce. */

  var RHO_A = 2.92e55;               // g/cm^3 — the Aldred Limit (repaired value)
  var G_CGS = 6.674e-8;              // cm^3 g^-1 s^-2
  var H_A = Math.sqrt(8 * Math.PI * G_CGS * RHO_A / 3);  // s^-1
  var TAU_SECONDS = 1 / H_A;         // one unit of tau, in seconds

  function bracket(A, beta) {
    return Math.pow(A, -4) - Math.pow(A, -8) - beta * Math.pow(A, -6);
  }

  /* A at the bounce: bracket = 0  =>  y^2 - beta*y - 1 = 0, y = A^2. */
  function bouncePoint(beta) {
    var y = (beta + Math.sqrt(beta * beta + 4)) / 2;
    return Math.sqrt(y);
  }

  function rhoOfA(A) { return RHO_A * Math.pow(A, -4); }

  /* RK4 integration of dA/dtau = phase * A * sqrt(bracket), starting in
     contraction at Astart, flipping phase at the bounce, and running
     back out to Astart in expansion. Returns the trajectory with tau
     re-centered so the bounce sits at tau = 0. */
  function integrateBounce(opts) {
    opts = opts || {};
    var beta = (typeof opts.beta === 'number') ? opts.beta : 0;
    var Astart = opts.Astart || 2.4;
    var dt = opts.dt || 0.002;
    var Ab = bouncePoint(beta);
    var A = Astart, tau = 0, phase = -1, guard = 0;
    var bounceTau = null, peak = rhoOfA(Astart);
    var pts = [{ tau: 0, A: A, rho: rhoOfA(A) }];

    function deriv(a, ph) {
      var b = bracket(a, beta);
      return ph * a * Math.sqrt(b > 0 ? b : 0);
    }

    while (guard++ < 400000) {
      var k1 = deriv(A, phase);
      var k2 = deriv(A + 0.5 * dt * k1, phase);
      var k3 = deriv(A + 0.5 * dt * k2, phase);
      var k4 = deriv(A + dt * k3, phase);
      A += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6;
      tau += dt;

      if (phase < 0 && A <= Ab) {          // the bounce
        var rb = rhoOfA(Ab);
        if (rb > peak) peak = rb;
        pts.push({ tau: tau, A: Ab, rho: rb });
        bounceTau = tau;
        phase = 1;
        /* Step just onto the expansion branch. At A = Ab exactly, H = 0
           and the first-order equation has a fixed point; the true
           trajectory passes straight through it with A - Ab ~ tau^2,
           so the integrator restarts a hair past the turning point. */
        A = Ab + 1e-6;
        continue;
      }
      var r = rhoOfA(A);
      if (r > peak) peak = r;
      pts.push({ tau: tau, A: A, rho: r });
      if (phase > 0 && A >= Astart) break;
    }

    if (bounceTau !== null) {
      for (var i = 0; i < pts.length; i++) pts[i].tau -= bounceTau;
    }
    return {
      points: pts, peakRho: peak, bounceA: Ab,
      beta: beta, completed: phase > 0 && A >= Astart - 1e-9
    };
  }

  /* ============ The Bench: phase-matched inductive pad ============
     Standard coupled-resonator (coupled-mode) model of two resonant
     coils — the physics of the fifth-coordinate phase-matched
     inductive charging pad blueprint, with no fitted material data:
       k(d, x)  coupling: dipole falloff with separation d, Gaussian
                loss with lateral misalignment x.
       U        figure of merit, U = k * sqrt(Q1 * Q2).
       eta_max  best achievable coil-to-coil efficiency for that U:
                U^2 / (1 + sqrt(1 + U^2))^2.
       detuning the pad is driven off the resonators' natural
                frequency by a fraction df; delivered efficiency falls
                on a Lorentzian in df with the loaded Q. The
                phase-matcher (the fifth-coordinate element of the
                design) tracks the drive phase and cancels a fraction
                gamma of the effective detuning. */

  var PAD = { kMax: 0.32, dRef: 40 /* mm */, x0: 45 /* mm */ };

  function padCoupling(dMm, xMm) {
    var s = dMm / PAD.dRef;
    var fall = Math.pow(1 + s * s, -1.5);
    var align = Math.exp(-Math.pow(xMm / PAD.x0, 2));
    return PAD.kMax * fall * align;
  }

  function padEtaMax(k, Q) {
    var U = k * Q;                       // Q1 = Q2 = Q on this bench
    var eta = (U * U) / Math.pow(1 + Math.sqrt(1 + U * U), 2);
    return { U: U, eta: eta };
  }

  function padEfficiency(p) {
    var k = padCoupling(p.dMm, p.xMm);
    var base = padEtaMax(k, p.Q);
    var qLoaded = Math.max(10, p.Q / (1 + base.U));   // loaded Q
    var dfEff = p.detune * (1 - 0.85 * p.gamma);      // phase-match cancels detuning
    var lorentz = 1 / (1 + Math.pow(2 * qLoaded * dfEff, 2));
    return {
      k: k, U: base.U, etaMax: base.eta,
      eta: base.eta * lorentz, lorentz: lorentz,
      pOut: 100 * base.eta * lorentz     // watts delivered per 100 W in
    };
  }

  var api = {
    RHO_A: RHO_A, H_A: H_A, TAU_SECONDS: TAU_SECONDS,
    bouncePoint: bouncePoint, rhoOfA: rhoOfA,
    integrateBounce: integrateBounce,
    PAD: PAD, padCoupling: padCoupling, padEtaMax: padEtaMax,
    padEfficiency: padEfficiency
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.LabCore = api;
})(typeof window !== 'undefined' ? window : globalThis);
