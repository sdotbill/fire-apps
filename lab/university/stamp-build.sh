#!/bin/sh
# Stamp the University build (Nov 16 2026 — the dashboard's
# x-dash-build pattern, carried over after Bill's phone was served
# a stale classroom from a warm tab across a deploy).
# Run BEFORE committing any University change: rewrites the
# x-uni-build meta, the window.UNI_BUILD value, and the ?v= on the
# four classroom script tags in index.html to
# "<git-short-hash>-<UTC build time>" where the hash is the current
# HEAD — i.e. the stamp names the repo revision this copy was
# minted from. Commit the stamped file together with the change
# it belongs to. The page's self-check compares the running stamp
# against the served stamp and reloads once when they differ, and
# every data fetch (gate-data.json, catalogue.json,
# trainer-data.json) carries the stamp as ?v=.
set -e
cd "$(dirname "$0")"
STAMP="$(git rev-parse --short HEAD)-$(date -u +%Y%m%dT%H%M)"
sed -i "s/name=\"x-uni-build\" content=\"[^\"]*\"/name=\"x-uni-build\" content=\"$STAMP\"/" index.html
sed -i "s/window\.UNI_BUILD = \"[^\"]*\"/window.UNI_BUILD = \"$STAMP\"/" index.html
for f in uni-core trainer-core gate-core gate-ui lessons30-ui; do
  sed -i "s|src=\"$f\.js?v=[^\"]*\"|src=\"$f.js?v=$STAMP\"|" index.html
done
grep -o 'name="x-uni-build" content="[^"]*"' index.html
grep -o 'src="gate-ui.js?v=[^"]*"' index.html
echo "stamped: $STAMP"
