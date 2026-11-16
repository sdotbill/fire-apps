/* Dave dashboard service worker.
   App-shell cache for the dashboard's own static assets ONLY.
   It never caches the dashboard HTML, and it never touches any API
   path (/chat, /owner/*, /account/*, or the worker origin) — those
   always go straight to the network, untouched. */
"use strict";

var CACHE = "dave-dashboard-shell-v1";
var SHELL = [
  "/dashboard/manifest.webmanifest",
  "/assets/dave-eye-living.webp",
  "/assets/dave-eye-192.png",
  "/assets/dave-eye-512.png",
  "/assets/dave-eye-maskable-512.png"
];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) { return c.addAll(SHELL); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        return k === CACHE ? null : caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;
  var url;
  try { url = new URL(req.url); } catch (err) { return; }
  if (url.origin !== self.location.origin) return;      // worker/API origins: hands off
  if (SHELL.indexOf(url.pathname) === -1) return;        // only the shell assets
  e.respondWith(
    caches.match(req).then(function (hit) {
      return hit || fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
        return res;
      });
    })
  );
});
