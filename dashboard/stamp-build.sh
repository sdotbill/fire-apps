#!/bin/sh
# Stamp the dashboard build (parity convergence, Nov 16 2026).
# Run BEFORE committing any dashboard change: rewrites the
# x-dash-build meta in index.html to "<git-short-hash>-<UTC build time>"
# where the hash is the current HEAD — i.e. the stamp names the repo
# revision this copy was minted from. Commit the stamped file together
# with the change it belongs to. Verify after deploy with
# ~/workspace/your_files/dave-4-public-app-2026-11-08/verify-dashboard-stamp.py
set -e
cd "$(dirname "$0")"
STAMP="$(git rev-parse --short HEAD)-$(date -u +%Y%m%dT%H%M)"
sed -i "s/name=\"x-dash-build\" content=\"[^\"]*\"/name=\"x-dash-build\" content=\"$STAMP\"/" index.html
grep -o 'name="x-dash-build" content="[^"]*"' index.html
echo "stamped: $STAMP"
