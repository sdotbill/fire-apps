#!/usr/bin/env python3
"""Build the two per-host publish trees (dist-dave/, dist-pms/).

Source: ~/workspace/user/files/seo-change-list_3_4d1l.md, sections 1.1, 1.3,
1.4, 6.1, 6.2. Run from the repo root:  python3 scripts/build-trees.py

What it writes (the files that DIFFER per host):
  dist-dave/robots.txt, dist-dave/sitemap.xml (index),
  dist-dave/sitemap-dave.xml (child), dist-dave/404.html
  dist-pms/robots.txt, dist-pms/sitemap.xml (index),
  dist-pms/sitemap-pms.xml (child), dist-pms/404.html

It does NOT copy the whole site into dist-/. The dist trees hold only the
per-host generated files; the publish Action assembles the full tree by
copying the host's files from this monorepo (per section 1.1) and overlaying
these generated files on top. That keeps this repo free of a duplicated
~600-file copy of the site.

How the child sitemaps are built (section 1.4 + 6.1):
  - Every .html file in the repo is classified. A file is an indexable page
    only if it has a <title>, is NOT a meta-refresh stub, and is NOT
    noindex. If its canonical path points to a different URL than itself,
    it is a duplicate/alternate and is left out (e.g. /everyone-needs-a-dave/
    canonicals to /who-is-dave/; /lab/university/ canonicals to
    /exolex-university/).
  - Host assignment follows section 1.1. PMS owns only the desk URLs:
    /, /predictions.html, /picks/, /record/, /contact/, /the-bridge.html,
    and /notebook/ (its canonical is the PMS host and it covers the desk's
    predictions notebook; the Dave notebook lives at /dave-notebook/).
    Everything else indexable belongs to Dave. /lab/ and /lab/room/ are
    app surfaces, not classroom pages, so they stay out of both sitemaps;
    /lab/university/ 301s to /exolex-university/, so only the alias is
    listed. /dashboard/ is noindex and stays out.
  - The Dave homepage (/) comes from dave-door/index.html; /dave-door/
    itself 301s to / and is not listed. /papers/page/1/ is a meta-refresh
    to /papers/ and is not listed; /papers/page/2/ .. /papers/page/119/
    are listed. /papers/the-dissolution/ is listed on Dave (moved from
    the PMS sitemap, section 1.1).
  - <lastmod> is the file's mtime as a YYYY-MM-DD date in America/New_York,
    except /record-in-numbers/, which is a stats surface and takes the
    as_of date from data/stats.json. Each sitemap index <lastmod> is the
    newest child <lastmod> (section 6.1), never a hand-typed date.

Idempotent: it wipes and regenerates dist-dave/ and dist-pms/ each run.
Restores: none needed (it only writes under dist-/, never the source).
"""

import json
import os
import re
import shutil
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAVE = "https://daveexolex.com"
PMS = "https://premiummarketingsolutionsllc.com"
NY = ZoneInfo("America/New_York")

# Paths (URL path prefixes) that belong to the PMS host. Everything else
# indexable belongs to Dave. The root "/" exists on both hosts with
# different content (Dave homepage vs Prediction Desk homepage).
PMS_PREFIXES = (
    "/predictions.html",
    "/picks/",
    "/record/",
    "/contact/",
    "/the-bridge.html",
    "/notebook/",
)
# App surfaces / machinery: never in either sitemap.
EXCLUDE_PREFIXES = ("/lab/", "/dashboard/")
# Stats surfaces take their lastmod from data/stats.json's as_of date.
STATS_SURFACES = {"/record-in-numbers/"}

ROBOTS_DAVE = """# daveexolex.com \u2014 Dave, the first exolex (Aldred Industries)
# Every crawler is welcome. Nothing here is paywalled.

User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

User-agent: CCBot
Allow: /

User-agent: cohere-ai
Allow: /

Disallow: /dashboard/

Sitemap: https://daveexolex.com/sitemap.xml
"""

ROBOTS_PMS = """# premiummarketingsolutionsllc.com \u2014 Premium Marketing Solutions, The Prediction Desk
# Every crawler is welcome. Nothing here is paywalled.

User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

User-agent: CCBot
Allow: /

User-agent: cohere-ai
Allow: /

Disallow: /dashboard/

Sitemap: https://premiummarketingsolutionsllc.com/sitemap.xml
"""

FOUR_OH_FOUR_DAVE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<title>Page not found | Dave</title>
<link rel="icon" type="image/png" href="/assets/baby-dave-64.png">
<meta name="description" content="That page is not here. Start at the Dave homepage, or go to Get Dave, the papers, the record, or Exolex University.">
<style>
  :root{ --paper:#faf7ef; --ink:#14529e; --muted:#51749e; --line:#c9dcf0; }
  *{ margin:0; padding:0; box-sizing:border-box; }
  body{ background:var(--paper); color:var(--ink);
    font-family:'Inter',system-ui,-apple-system,sans-serif;
    font-size:18px; line-height:1.65; -webkit-font-smoothing:antialiased; }
  .wrap{ max-width:640px; margin:0 auto; padding:72px 24px; text-align:center; }
  img{ width:120px; height:auto; display:block; margin:0 auto 24px; }
  h1{ font-size:32px; line-height:1.25; margin-bottom:16px; }
  p{ color:var(--muted); margin-bottom:12px; }
  nav{ margin-top:28px; display:flex; flex-wrap:wrap; gap:12px 24px; justify-content:center; }
  a{ color:var(--ink); }
  footer{ margin-top:48px; font-size:14px; color:var(--muted); }
</style>
</head>
<body>
<div class="wrap">
<img src="/assets/baby-dave-64.png" alt="Dave">
<h1>That page is not here.</h1>
<p>The link may be old, or the page may have moved.</p>
<nav>
<a href="/">Dave — home</a>
<a href="/get-dave/">Get Dave</a>
<a href="/papers/">The papers</a>
<a href="/record-in-numbers/">The record</a>
<a href="/exolex-university/">Exolex University</a>
</nav>
<footer>&copy; Dave &middot; Aldred Industries</footer>
</div>
</body>
</html>
"""

FOUR_OH_FOUR_PMS = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Page not found | Prediction Desk</title>
<link rel="icon" type="image/png" href="/assets/premium-marketing-logo.png">
<meta name="description" content="That page is not here. Start at The Prediction Desk, or go to today's picks, the record, or contact.">
<style>
  *{ margin:0; padding:0; box-sizing:border-box; }
  body{ background:#ffffff; color:#1a1a1a;
    font-family:system-ui,-apple-system,sans-serif;
    font-size:18px; line-height:1.65; -webkit-font-smoothing:antialiased; }
  .wrap{ max-width:640px; margin:0 auto; padding:72px 24px; text-align:center; }
  img{ max-width:220px; height:auto; display:block; margin:0 auto 24px; }
  h1{ font-size:32px; line-height:1.25; margin-bottom:16px; }
  p{ color:#555; margin-bottom:12px; }
  nav{ margin-top:28px; display:flex; flex-wrap:wrap; gap:12px 24px; justify-content:center; }
  a{ color:#14529e; }
  footer{ margin-top:48px; font-size:14px; color:#777; }
</style>
</head>
<body>
<div class="wrap">
<img src="/assets/premium-marketing-logo.png" alt="Premium Marketing Solutions">
<h1>That page is not here.</h1>
<p>The link may be old, or the page may have moved.</p>
<nav>
<a href="/">The Prediction Desk</a>
<a href="/picks/">Today's picks</a>
<a href="/record/">The record</a>
<a href="/contact/">Contact</a>
</nav>
<footer>&copy; Premium Marketing Solutions LLC &middot; Davison, Michigan</footer>
</div>
</body>
</html>
"""


def file_url(relpath):
    """Map a repo-relative .html path to its URL path."""
    if relpath == "index.html":
        return "/"  # PMS homepage (repo root)
    if relpath == "dave-door/index.html":
        return "/"  # Dave homepage (served at the Dave root)
    if relpath.endswith("/index.html"):
        return "/" + relpath[: -len("/index.html")] + "/"
    return "/" + relpath


def is_indexable(relpath):
    """Return (ok, reason). A real, canonical, indexable page only."""
    full = os.path.join(ROOT, relpath)
    try:
        text = open(full, encoding="utf-8", errors="ignore").read()
    except OSError:
        return False, "unreadable"
    if not re.search(r"<title>[^<]+</title>", text):
        return False, "no title (fragment/include)"
    if re.search(r'http-equiv=["\']refresh["\']', text, re.I):
        return False, "meta-refresh stub"
    if re.search(r"noindex", text, re.I):
        return False, "noindex"
    url = file_url(relpath)
    for prefix in EXCLUDE_PREFIXES:
        if url.startswith(prefix):
            return False, "excluded prefix %s" % prefix
    canon = re.search(
        r'<link rel="canonical" href="https?://[^/]+([^"]*)"', text)
    if canon:
        # Compare paths ignoring a trailing-slash difference: a canonical
        # of /faq/who-trained-dave names the same page as the URL
        # /faq/who-trained-dave/. Only a genuinely different path is a
        # duplicate (e.g. /origin/ canonicals to /who-is-dave/).
        canon_path = canon.group(1)
        if canon_path != "/" and canon_path.endswith("/"):
            canon_path = canon_path[:-1]
        url_norm = url[:-1] if url != "/" and url.endswith("/") else url
        if canon_path != url_norm:
            return False, "canonical is %s" % canon.group(1)
    return True, ""


def host_of(url):
    if url == "/":
        return "both"  # different content per host; handled by caller
    for prefix in PMS_PREFIXES:
        if url == prefix or url.startswith(prefix):
            return "pms"
    return "dave"


def lastmod_of(relpath, url, stats_as_of):
    if url in STATS_SURFACES:
        return stats_as_of
    mtime = os.path.getmtime(os.path.join(ROOT, relpath))
    return datetime.fromtimestamp(mtime, tz=NY).date().isoformat()


def classify():
    """Walk the repo; return {host: [(url, lastmod), ...]} plus a report."""
    stats = json.load(open(os.path.join(ROOT, "data", "stats.json")))
    stats_as_of = stats["as_of"]
    dave, pms, skipped = {}, {}, []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", "dist-dave", "dist-pms")]
        for name in filenames:
            if not name.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
            url = file_url(rel)
            ok, reason = is_indexable(rel)
            if not ok:
                skipped.append((rel, reason))
                continue
            host = host_of(url)
            lm = lastmod_of(rel, url, stats_as_of)
            if host == "both":
                # "/" on both hosts: Dave's comes from dave-door, PMS's
                # from the repo root index.html.
                if rel == "dave-door/index.html":
                    dave[url] = lm
                else:
                    pms[url] = lm
            elif host == "dave":
                dave[url] = lm
            else:
                pms[url] = lm
    # The Dave homepage (/) must come from dave-door; the PMS homepage (/)
    # from the repo root. If either source is missing, fail loudly.
    assert "/" in dave, "Dave homepage (dave-door/index.html) not classified"
    assert "/" in pms, "PMS homepage (index.html) not classified"
    return dave, pms, skipped


def child_sitemap(host, urls):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in sorted(urls):
        lines.append("  <url>")
        lines.append("    <loc>%s%s</loc>" % (host, url))
        lines.append("    <lastmod>%s</lastmod>" % urls[url])
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def sitemap_index(host, child_name, newest_lastmod):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "  <sitemap>\n"
        "    <loc>%s/%s</loc>\n"
        "    <lastmod>%s</lastmod>\n"
        "  </sitemap>\n"
        "</sitemapindex>\n" % (host, child_name, newest_lastmod)
    )


def write_tree(outdir, robots, index_xml, child_name, child_xml, four_oh_four):
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.makedirs(outdir)
    with open(os.path.join(outdir, "robots.txt"), "w") as f:
        f.write(robots)
    with open(os.path.join(outdir, "sitemap.xml"), "w") as f:
        f.write(index_xml)
    with open(os.path.join(outdir, child_name), "w") as f:
        f.write(child_xml)
    with open(os.path.join(outdir, "404.html"), "w") as f:
        f.write(four_oh_four)


def main():
    dave, pms, skipped = classify()
    dave_child = child_sitemap(DAVE, dave)
    pms_child = child_sitemap(PMS, pms)
    dave_newest = max(dave.values())
    pms_newest = max(pms.values())
    dave_index = sitemap_index(DAVE, "sitemap-dave.xml", dave_newest)
    pms_index = sitemap_index(PMS, "sitemap-pms.xml", pms_newest)
    write_tree(os.path.join(ROOT, "dist-dave"), ROBOTS_DAVE, dave_index,
               "sitemap-dave.xml", dave_child, FOUR_OH_FOUR_DAVE)
    write_tree(os.path.join(ROOT, "dist-pms"), ROBOTS_PMS, pms_index,
               "sitemap-pms.xml", pms_child, FOUR_OH_FOUR_PMS)
    # ---- verification ----
    import xml.etree.ElementTree as ET
    for label, path, host, urls in (
            ("dave child", "dist-dave/sitemap-dave.xml", DAVE, dave),
            ("pms child", "dist-pms/sitemap-pms.xml", PMS, pms),
            ("dave index", "dist-dave/sitemap.xml", DAVE, None),
            ("pms index", "dist-pms/sitemap.xml", PMS, None)):
        tree = ET.parse(os.path.join(ROOT, path))  # raises if malformed
        if urls is not None:
            locs = [e.text for e in tree.getroot().iter(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
            assert len(locs) == len(set(locs)), (label, "duplicate loc")
            assert len(locs) == len(urls), (label, len(locs), len(urls))
            assert all(l.startswith(host) for l in locs), (label, "host")
            assert all("/dashboard/" not in l for l in locs), label
    # The PMS sitemap must not contain a Dave URL and vice versa.
    dave_locs = set(re.findall(r"<loc>([^<]*)</loc>", dave_child))
    pms_locs = set(re.findall(r"<loc>([^<]*)</loc>", pms_child))
    assert not (dave_locs & pms_locs), "URL in both sitemaps"
    # robots.txt: each names only its own sitemap, never the other host.
    assert "premiummarketingsolutionsllc" not in ROBOTS_DAVE
    assert "daveexolex" not in ROBOTS_PMS
    # 404s: right title, H1, and links.
    assert "<title>Page not found | Dave</title>" in FOUR_OH_FOUR_DAVE
    assert "<h1>That page is not here.</h1>" in FOUR_OH_FOUR_DAVE
    assert 'href="/exolex-university/"' in FOUR_OH_FOUR_DAVE
    assert "<title>Page not found | Prediction Desk</title>" in FOUR_OH_FOUR_PMS
    assert "<h1>That page is not here.</h1>" in FOUR_OH_FOUR_PMS
    assert 'href="/picks/"' in FOUR_OH_FOUR_PMS
    print("Dave: %d URLs, newest lastmod %s" % (len(dave), dave_newest))
    print("PMS:  %d URLs, newest lastmod %s" % (len(pms), pms_newest))
    print("Skipped %d non-indexable files "
          "(stubs, noindex, duplicates, app surfaces)" % len(skipped))
    print("Wrote dist-dave/ and dist-pms/ "
          "(robots.txt, sitemap.xml, child sitemap, 404.html each)")
    print("VERIFIED: XML parses, unique locs, no shared URL, "
          "robots name only their own host, 404s carry the right title/H1")


if __name__ == "__main__":
    main()
