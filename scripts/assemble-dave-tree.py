#!/usr/bin/env python3
"""Assemble the Dave publish tree (what daveexolex.com serves) into a directory.

Usage:  python3 scripts/assemble-dave-tree.py [outdir]
Default outdir: /tmp/dave-tree (a staging dir, never inside the repo).

The tree is the monorepo MINUS the PMS-only paths, with the Dave homepage
at the root and the dist-dave/ generated files overlaid. This is what the
publish Action pushes to the sdotbill/daveexolex repo.

PMS-only paths (section 1.1; the desk URLs) are excluded: the picks/,
record/, contact/, notebook/ and what-we-do/ directories, and the root
files predictions.html and the-bridge.html. The repo root index.html
(the PMS homepage) is REPLACED by dave-door/index.html (the Dave
homepage). The shared root sitemap/robots files are replaced by the
dist-dave/ versions. Build/config dirs (.git, .github, scripts,
dist-dave, dist-pms, redirects) are not site content and are excluded.

The meta-refresh stub files that redirect WITHIN Dave (e.g. /dave/ ->
/get-dave/) are KEPT in the tree for now: the Cloudflare same-host 301s
are not live yet, so deleting the stubs would 404 those URLs. They are
deleted after the 301s are confirmed live (change-list section 5).

Idempotent: the outdir is wiped and rebuilt each run.
"""

import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Top-level directories that belong to PMS (excluded from the Dave tree).
PMS_DIRS = {"picks", "record", "contact", "notebook", "what-we-do", "dave-for-business"}
# Root files that belong to PMS (excluded; index.html is replaced, not
# merely excluded).
PMS_ROOT_FILES = {"predictions.html", "the-bridge.html"}
# Build/config dirs: not site content.
EXCLUDE_DIRS = {".git", ".github", "scripts", "dist-dave", "dist-pms",
                "redirects"}
# Root files replaced by the dist-dave/ generated versions.
REPLACED_ROOT_FILES = {"robots.txt", "sitemap.xml", "sitemap-dave.xml",
                       "sitemap-pms.xml"}


def is_pms_path(relpath):
    """True if this repo-relative path belongs to the PMS host only."""
    parts = relpath.split(os.sep)
    if len(parts) == 1:
        return parts[0] in PMS_ROOT_FILES
    return parts[0] in PMS_DIRS


def assemble(outdir):
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.makedirs(outdir)
    copied, excluded = [], []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Prune excluded dirs (and the outdir itself if it is under ROOT).
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, ROOT)
            # Never copy the Dave-tree staging dir or the repo's own
            # generated dist output as a subdirectory.
            if rel.startswith("dist-"):
                excluded.append((rel, "build output"))
                continue
            if rel == "index.html":
                excluded.append((rel, "PMS homepage (replaced)"))
                continue
            if rel in REPLACED_ROOT_FILES:
                excluded.append((rel, "replaced by dist-dave/"))
                continue
            if is_pms_path(rel):
                excluded.append((rel, "PMS-only path"))
                continue
            # The Dave homepage source is copied to the tree root below,
            # not as dave-door/index.html (that path 301s to /).
            if rel == "dave-door/index.html":
                excluded.append((rel, "Dave homepage source (moved to /)"))
                continue
            dest = os.path.join(outdir, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(full, dest)
            copied.append(rel)
    # Dave homepage at the tree root.
    shutil.copy2(os.path.join(ROOT, "dave-door", "index.html"),
                 os.path.join(outdir, "index.html"))
    copied.append("index.html (from dave-door/index.html)")
    # Overlay the generated per-host files.
    dist_dave = os.path.join(ROOT, "dist-dave")
    for name in ("robots.txt", "sitemap.xml", "sitemap-dave.xml",
                 "404.html"):
        src = os.path.join(dist_dave, name)
        assert os.path.exists(src), "dist-dave/%s missing; run build-trees.py first" % name
        shutil.copy2(src, os.path.join(outdir, name))
        copied.append(name + " (from dist-dave/)")
    return copied, excluded


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "/tmp/dave-tree"
    copied, excluded = assemble(outdir)
    # Verification: the tree must have a Dave root, no PMS-only path, and
    # the per-host files must be the dist-dave versions. Files excluded
    # because they are REPLACED by dist-dave/ (robots.txt, sitemap.xml,
    # sitemap-dave.xml, sitemap-pms.xml) DO exist in the tree as the
    # overlaid versions, so they are not asserted absent here.
    for rel, reason in excluded:
        # "replaced" files DO exist in the tree as their replacement
        # (dist-dave/ files; the Dave homepage at index.html), so they
        # are not asserted absent here.
        if "replaced" in reason:
            continue
        assert not os.path.exists(os.path.join(outdir, rel)), rel
    for name in ("robots.txt", "sitemap.xml", "sitemap-dave.xml",
                 "404.html"):
        a = open(os.path.join(outdir, name), encoding="utf-8").read()
        b = open(os.path.join(ROOT, "dist-dave", name),
                 encoding="utf-8").read()
        assert a == b, name
    # No PMS-only path may survive in the tree.
    for bad in ("predictions.html", "the-bridge.html", "picks",
                "record", "contact", "notebook", "what-we-do"):
        assert not os.path.exists(os.path.join(outdir, bad)), bad
    # The Dave homepage must be the Dave one (not the PMS one).
    home = open(os.path.join(outdir, "index.html"), encoding="utf-8").read()
    assert "Talk to Dave, the First Exolex" in home
    assert "The Prediction Desk of Premium Marketing Solutions" not in home
    n_files = sum(len(fs) for _, _, fs in os.walk(outdir))
    print("Dave tree: %d files in %s (%d copied, %d excluded)"
          % (n_files, outdir, len(copied), len(excluded)))
    print("VERIFIED: Dave homepage at /, no PMS-only path, "
          "dist-dave/ files overlaid byte-identical")


if __name__ == "__main__":
    main()
