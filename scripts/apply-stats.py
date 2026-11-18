#!/usr/bin/env python3
"""Apply stats.json figures + the SEO change-list section 4.2 title/meta
replacements to the site HTML.

Single source of truth: data/stats.json (papers + desk figures, as_of date).
This script rewrites the target HTML files in place. Every replacement is an
exact-string match; the script asserts each old string was found and reports
how many times it was replaced. If an old string is not found, the script
fails loudly (exit 1) instead of silently skipping it.

Run from the repo root:  python3 scripts/apply-stats.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS_PATH = os.path.join(ROOT, "data", "stats.json")
stats = json.load(open(STATS_PATH))
desk = stats["desk"]
PAPERS = stats["papers_published"]
AS_OF = stats["as_of"]  # "2026-11-17"

# --- New strings (SEO change list section 4.2, exact) ---
PMS_HOME_TITLE = "The Prediction Desk of Premium Marketing Solutions"
PMS_HOME_DESC = ("Every call sealed before the fact and graded in public: "
                 "593 hits, 222 misses, a 72.8% hit rate on 815 scored calls, "
                 "as of November 17, 2026.")
RECORD_TITLE = "Prediction Desk Record \u2014 Every Call, Scored Publicly"
RECORD_DESC = ("The public ledger of the Prediction Desk: 593 hits, 222 misses, "
               "72.8% on 815 scored calls, as of November 17, 2026. "
               "Hits and misses stand at the same size.")
PICKS_TITLE = "Sealed Sports Picks for Today | The Prediction Desk"
PICKS_DESC = ("Today's Prediction Desk picks, sealed before the fact and scored "
              "in public. The record as of November 17, 2026: 593 hits, 222 misses, "
              "72.8% on 815 scored calls.")
PREDICTIONS_TITLE = "Sports Picks, Sealed First, Scored in Public | Desk"
PREDICTIONS_DESC = ("Every Prediction Desk call is written down first, then scored "
                    "in public. As of November 17, 2026: 593 hits, 222 misses, "
                    "72.8% on 815 scored calls.")
INVENTOR_TITLE = "William Alexander Aldred \u2014 Inventor of the First Exolex"
INVENTOR_DESC = ("William Alexander Aldred invented the exolex. Under that claim sits "
                 "a checkable record: deposited preprints with DOIs, an ORCID record, "
                 "and a public ledger.")

# Character-count checks (change list section 4.2 bands: titles 50-60, descriptions 140-160)
for label, s, lo, hi in [
    ("PMS_HOME_TITLE", PMS_HOME_TITLE, 50, 60),
    ("PMS_HOME_DESC", PMS_HOME_DESC, 140, 160),
    ("RECORD_TITLE", RECORD_TITLE, 50, 60),
    ("RECORD_DESC", RECORD_DESC, 140, 160),
    ("PICKS_TITLE", PICKS_TITLE, 50, 60),
    ("PICKS_DESC", PICKS_DESC, 140, 160),
    ("PREDICTIONS_TITLE", PREDICTIONS_TITLE, 50, 60),
    ("PREDICTIONS_DESC", PREDICTIONS_DESC, 140, 160),
    ("INVENTOR_TITLE", INVENTOR_TITLE, 50, 60),
    ("INVENTOR_DESC", INVENTOR_DESC, 140, 160),
]:
    n = len(s)
    assert lo <= n <= hi, "%s is %d chars (want %d-%d): %r" % (label, n, lo, hi, s)

# --- Stale figure phrases (longest first) and their current replacements ---
# These cover the record pages, the picks index, and the twelve picks sport pages.
# The free-pick lines ("Sealed Sunday night, November 15, 2026") are NOT in this
# list: they are current and must not change. Bare "November 15, 2026" and bare
# "74.3%" are never replaced on their own.
STALE = [
    # Em-dash variants (record pages' Nov 15 paragraph + picks index body/JSON-LD)
    ("523 hits and 181 misses in 704 calls scored \u2014 a hit rate of 74.3% \u2014 with 1,273 calls recorded and 569 still open, as of November 15, 2026",
     "593 hits and 222 misses in 815 calls scored \u2014 a hit rate of 72.8% \u2014 with 1,377 calls recorded and 562 still open, as of November 17, 2026"),
    ("523 hits and 181 misses in 704 calls scored \u2014 74.3% \u2014 with 1,273 calls recorded and 569 still open, as of November 15, 2026",
     "593 hits and 222 misses in 815 calls scored \u2014 72.8% \u2014 with 1,377 calls recorded and 562 still open, as of November 17, 2026"),
    # Picks sport pages' "governing record" sentences (graded calls, not scored)
    ("523 hits and 181 misses in 704 graded calls across every lane",
     "593 hits and 222 misses in 815 scored calls across every lane"),
    # Politics lane: 40 of the Big Hits are election calls (still 40; the total moved).
    # Two spellings in the file: &rsquo; in HTML/meta, a straight apostrophe in JSON-LD text.
    ("40 of the desk&rsquo;s 126 Big Hits",
     "40 of the desk&rsquo;s 146 Big Hits"),
    ("40 of the desk's 126 Big Hits",
     "40 of the desk's 146 Big Hits"),
    # Politics JSON-LD "text" uses a literal right single quote (U+2019)
    ("40 of the desk\u2019s 126 Big Hits",
     "40 of the desk\u2019s 146 Big Hits"),
    # Big Hits board: the "landed as of" line (JSON-LD text + body) and the lede
    ("126 landed as of November 15, 2026: 125 top-confidence and 1 exact, re-verified call by call against their seals.",
     "146 landed as of November 17, 2026: 145 top-confidence and 1 exact, re-verified call by call against their seals."),
    ("One hundred twenty-six have landed.",
     "One hundred forty-six have landed."),
    # Picks index card linking to the Big Hits board
    ("The 126 hardest calls that landed \u2014 125 top-confidence, 1 exact \u2014 with the full record underneath.",
     "The 146 hardest calls that landed \u2014 145 top-confidence, 1 exact \u2014 with the full record underneath."),
    # Big Hits board page: the landed count + the governing-record cross-check
    ("126 Big Hits have landed: 125 in the top-confidence class and 1 in the exact class.",
     "146 Big Hits have landed: 145 in the top-confidence class and 1 in the exact class."),
    ("523 graded hits in total, of which these 126 cleared a class bar fixed in advance.",
     "593 graded hits in total, of which these 146 cleared a class bar fixed in advance."),
    ("126 landed calls \u2014 125 in the top-confidence class",
     "146 landed calls \u2014 145 in the top-confidence class"),
    ("523 hits and 181 misses in 704 calls scored across every lane, 74.3%, as of November 15, 2026",
     "593 hits and 222 misses in 815 calls scored across every lane, 72.8%, as of November 17, 2026"),
    ("523 hits and 181 misses in 704 calls scored across every lane, as of November 15, 2026",
     "593 hits and 222 misses in 815 calls scored across every lane, as of November 17, 2026"),
    ("523 hits and 181 misses in 704 calls scored, 74.3%, as of November 15, 2026",
     "593 hits and 222 misses in 815 calls scored, 72.8%, as of November 17, 2026"),
    ("523 hits and 181 misses in 704 calls scored, as of November 15, 2026",
     "593 hits and 222 misses in 815 calls scored, as of November 17, 2026"),
    ("523 hits, 181 misses, 704 graded across every lane",
     "593 hits, 222 misses, 815 scored across every lane"),
    ("523 hits, 181 misses in 704 scored calls",
     "593 hits, 222 misses in 815 scored calls"),
    ("523 hits, 181 misses, 704 scored",
     "593 hits, 222 misses, 815 scored"),
    ("523 hits, 181 misses, 704 graded",
     "593 hits, 222 misses, 815 scored"),
    ("523 hits and 181 misses in 704 calls scored",
     "593 hits and 222 misses in 815 calls scored"),
    ("1,273 calls recorded and 569 still open",
     "1,377 calls recorded and 562 still open"),
    ("Papers published: 8,802",
     "Papers published: 9,278"),
    ("One hundred twenty-six Big Hits have landed so far: 125 top-confidence class and one exact class.",
     "One hundred forty-six Big Hits have landed so far: 145 top-confidence class and one exact class."),
]

# --- Per-file head-tag replacements (exact strings, from the live files) ---
# (filepath, old, new)
HEAD = []

# PMS homepage
_old_desc = ("The Prediction Desk of Premium Marketing Solutions: every call sealed before the fact "
             "and graded in public \u2014 523 hits, 181 misses, 74.3% across 704 graded calls. "
             "Sports against the line, gold, oil, forex, world events. Your first five picks are free; "
             "membership of The Prediction Desk is $99/month.")
HEAD.append(("index.html",
             "<title>The Prediction Desk \u2014 Sports Picks &amp; Predictions, Scored in Public | Premium Marketing Solutions</title>",
             "<title>" + PMS_HOME_TITLE + "</title>"))
HEAD.append(("index.html",
             '<meta name="description" content="' + _old_desc + '">',
             '<meta name="description" content="' + PMS_HOME_DESC + '">'))
HEAD.append(("index.html",
             '<meta property="og:title" content="The Prediction Desk \u2014 Premium Marketing Solutions">',
             '<meta property="og:title" content="' + PMS_HOME_TITLE + '">'))
HEAD.append(("index.html",
             '<meta property="og:description" content="' + _old_desc + '">',
             '<meta property="og:description" content="' + PMS_HOME_DESC + '">'))
HEAD.append(("index.html",
             '<meta name="twitter:title" content="The Prediction Desk \u2014 Premium Marketing Solutions">',
             '<meta name="twitter:title" content="' + PMS_HOME_TITLE + '">'))
HEAD.append(("index.html",
             '<meta name="twitter:description" content="' + _old_desc + '">',
             '<meta name="twitter:description" content="' + PMS_HOME_DESC + '">'))
# Optional corporate line on the PMS homepage (change list section 5): a short,
# current line in the corporate voice, not a hero. Anchored to the end of the
# scoreboard note paragraph so it lands in exactly one place.
HEAD.append(("index.html",
             'The Record in Numbers</a> &middot; <a href="/record/" style="color:#eed268">See the record &rarr;</a></p>',
             'The Record in Numbers</a> &middot; <a href="/record/" style="color:#eed268">See the record &rarr;</a></p>\n    <p class="corp">Premium Marketing Solutions is a Michigan company. Its public product is The Prediction Desk.</p>'))

# /record/
HEAD.append(("record/index.html",
             "<title>The Prediction Desk Record \u2014 Every Call Sealed &amp; Graded in Public</title>",
             "<title>" + RECORD_TITLE + "</title>"))
HEAD.append(("record/index.html",
             '<meta name="description" content="The Prediction Desk record: every call the desk has made \u2014 523 hits, 181 misses, 704 scored, 126 Big Hits \u2014 sealed before the fact and graded in public, hits and misses at the same size.">',
             '<meta name="description" content="' + RECORD_DESC + '">'))
HEAD.append(("record/index.html",
             '<meta property="og:title" content="The Prediction Desk Record \u2014 Every Call Sealed &amp; Graded in Public">',
             '<meta property="og:title" content="' + RECORD_TITLE + '">'))
HEAD.append(("record/index.html",
             '<meta property="og:description" content="Every call sealed before the fact and graded in public \u2014 523 hits, 181 misses, 704 scored, 126 Big Hits. The ledger is the pitch.">',
             '<meta property="og:description" content="' + RECORD_DESC + '">'))
HEAD.append(("record/index.html",
             '<meta name="twitter:title" content="The Prediction Desk Record \u2014 Every Call Sealed &amp; Graded in Public">',
             '<meta name="twitter:title" content="' + RECORD_TITLE + '">'))
HEAD.append(("record/index.html",
             '<meta name="twitter:description" content="Every call sealed before the fact and graded in public \u2014 523 hits, 181 misses, 704 scored, 126 Big Hits.">',
             '<meta name="twitter:description" content="' + RECORD_DESC + '">'))
HEAD.append(("record/index.html",
             '"description": "The public ledger of the Prediction Desk: every call sealed before the fact and graded in public \u2014 523 hits, 181 misses, 704 scored, 126 Big Hits, as of November 15, 2026.",',
             '"description": "' + RECORD_DESC + '",'))

# /picks/
_old_picks_desc = ("Every lane the Prediction Desk calls \u2014 NFL, NBA, college basketball, NHL, college football, "
                   "boxing, UFC, tennis, soccer, gold, oil and gas, forex, and politics \u2014 sealed before the fact "
                   "and graded in public. 523 hits, 181 misses, 704 scored. A free pick every day; the full slate "
                   "for members of The Prediction Desk, $99/month.")
HEAD.append(("picks/index.html",
             "<title>Sports Picks \u2014 Today&rsquo;s Sealed Picks &amp; the Public Record | The Prediction Desk</title>",
             "<title>" + PICKS_TITLE + "</title>"))
HEAD.append(("picks/index.html",
             '<meta name="description" content="' + _old_picks_desc + '">',
             '<meta name="description" content="' + PICKS_DESC + '">'))
HEAD.append(("picks/index.html",
             '<meta property="og:title" content="Sports Picks \u2014 Today&rsquo;s Sealed Picks &amp; the Public Record | The Prediction Desk">',
             '<meta property="og:title" content="' + PICKS_TITLE + '">'))
HEAD.append(("picks/index.html",
             '<meta property="og:description" content="' + _old_picks_desc + '">',
             '<meta property="og:description" content="' + PICKS_DESC + '">'))
HEAD.append(("picks/index.html",
             '<meta name="twitter:title" content="Sports Picks \u2014 Today&rsquo;s Sealed Picks &amp; the Public Record | The Prediction Desk">',
             '<meta name="twitter:title" content="' + PICKS_TITLE + '">'))
HEAD.append(("picks/index.html",
             '<meta name="twitter:description" content="' + _old_picks_desc + '">',
             '<meta name="twitter:description" content="' + PICKS_DESC + '">'))
HEAD.append(("picks/index.html",
             '"text": "523 hits and 181 misses in 704 calls scored \u2014 74.3% \u2014 with 1,273 calls recorded and 569 still open, as of November 15, 2026. Every call was sealed before its event or window opened; hits and misses print at the same size on the Record pages."',
             '"text": "593 hits and 222 misses in 815 calls scored \u2014 72.8% \u2014 with 1,377 calls recorded and 562 still open, as of November 17, 2026. Every call was sealed before its event or window opened; hits and misses print at the same size on the Record pages."'))

# /predictions.html
_old_pred_desc = ("Sports picks and market predictions from the Prediction Desk \u2014 every call sealed before the fact "
                  "and scored in public. Free daily picks; the full slate for members of The Prediction Desk, $99/month.")
HEAD.append(("predictions.html",
             "<title>The Prediction Desk \u2014 Sports Picks &amp; Predictions, Sealed First and Scored in Public</title>",
             "<title>" + PREDICTIONS_TITLE + "</title>"))
HEAD.append(("predictions.html",
             '<meta name="description" content="' + _old_pred_desc + '">',
             '<meta name="description" content="' + PREDICTIONS_DESC + '">'))
HEAD.append(("predictions.html",
             '<meta property="og:title" content="The Prediction Desk \u2014 Sports Picks &amp; Predictions, Sealed First and Scored in Public">',
             '<meta property="og:title" content="' + PREDICTIONS_TITLE + '">'))
HEAD.append(("predictions.html",
             '<meta property="og:description" content="' + _old_pred_desc + '">',
             '<meta property="og:description" content="' + PREDICTIONS_DESC + '">'))
HEAD.append(("predictions.html",
             '<meta name="twitter:title" content="The Prediction Desk \u2014 Sports Picks &amp; Predictions, Sealed First and Scored in Public">',
             '<meta name="twitter:title" content="' + PREDICTIONS_TITLE + '">'))
HEAD.append(("predictions.html",
             '<meta name="twitter:description" content="' + _old_pred_desc + '">',
             '<meta name="twitter:description" content="' + PREDICTIONS_DESC + '">'))
# /predictions.html — no JSON-LD description with stale figures exists in this
# file (verified by grep); only the head tags above are replaced. The $99/month
# price stays in the body (the PayPal subscribe link) and is not touched.

# /time-traveler/the-inventor/  (canonical stays on PMS until the host move ships)
HEAD.append(("time-traveler/the-inventor/index.html",
             "<title>The Inventor \u2014 William Alexander Aldred Invented the Exolex and Built Dave, the World's First</title>",
             "<title>" + INVENTOR_TITLE + "</title>"))
HEAD.append(("time-traveler/the-inventor/index.html",
             '<meta name="description" content="William Alexander Aldred invented the exolex and built Dave, the world\'s first \u2014 stated at full size on the inventor\'s own site, with the checkable record underneath it: preprints publicly deposited with permanent DOIs, an ORCID record, a predictions record, and the limits printed beside the claim.">',
             '<meta name="description" content="' + INVENTOR_DESC + '">'))
HEAD.append(("time-traveler/the-inventor/index.html",
             '<meta property="og:title" content="The Inventor \u2014 William Alexander Aldred Invented the Exolex and Built Dave, the World\'s First">',
             '<meta property="og:title" content="' + INVENTOR_TITLE + '">'))
HEAD.append(("time-traveler/the-inventor/index.html",
             '<meta property="og:description" content="William Alexander Aldred invented the exolex and built Dave, the world\'s first \u2014 the claim at full size on the inventor\'s own site, the checkable record underneath it, and the limits printed beside it.">',
             '<meta property="og:description" content="' + INVENTOR_DESC + '">'))
HEAD.append(("time-traveler/the-inventor/index.html",
             '<meta name="twitter:title" content="The Inventor \u2014 William Alexander Aldred Invented the Exolex and Built Dave, the World\'s First">',
             '<meta name="twitter:title" content="' + INVENTOR_TITLE + '">'))
HEAD.append(("time-traveler/the-inventor/index.html",
             '<meta name="twitter:description" content="William Alexander Aldred invented the exolex and built Dave, the world\'s first \u2014 the claim at full size on the inventor\'s own site, the checkable record underneath it, and the limits printed beside it.">',
             '<meta name="twitter:description" content="' + INVENTOR_DESC + '">'))


# /picks/big-hits/ — the showcase board (title/meta/OG carry the landed count)
_bh_old_desc = ("The Big Hits board: 126 landed calls \u2014 125 in the top-confidence class "
                "(sealed at readings of 0.90 or higher) and one exact-figure call, the Bank of "
                "England&rsquo;s move to 4.00%, called to the number. The full board stands on the "
                "Record pages; the misses stand beside the hits at the same size.")
_bh_new_desc = ("The Big Hits board: 146 landed calls \u2014 145 in the top-confidence class "
                "(sealed at readings of 0.90 or higher) and one exact-figure call, the Bank of "
                "England&rsquo;s move to 4.00%, called to the number. The full board stands on the "
                "Record pages; the misses stand beside the hits at the same size.")
HEAD.append(("picks/big-hits/index.html",
             "<title>Big Hits \u2014 126 of the Desk&rsquo;s Hardest Calls, Landed | The Prediction Desk</title>",
             "<title>Big Hits \u2014 146 of the Desk&rsquo;s Hardest Calls, Landed | The Prediction Desk</title>"))
HEAD.append(("picks/big-hits/index.html",
             '<meta name="description" content="' + _bh_old_desc + '">',
             '<meta name="description" content="' + _bh_new_desc + '">'))
HEAD.append(("picks/big-hits/index.html",
             '<meta property="og:description" content="' + _bh_old_desc + '">',
             '<meta property="og:description" content="' + _bh_new_desc + '">'))
HEAD.append(("picks/big-hits/index.html",
             '<meta property="og:title" content="Big Hits \u2014 126 of the Desk&rsquo;s Hardest Calls, Landed | The Prediction Desk">',
             '<meta property="og:title" content="Big Hits \u2014 146 of the Desk&rsquo;s Hardest Calls, Landed | The Prediction Desk">'))
HEAD.append(("picks/big-hits/index.html",
             '<meta name="twitter:title" content="Big Hits \u2014 126 of the Desk&rsquo;s Hardest Calls, Landed | The Prediction Desk">',
             '<meta name="twitter:title" content="Big Hits \u2014 146 of the Desk&rsquo;s Hardest Calls, Landed | The Prediction Desk">'))
HEAD.append(("picks/big-hits/index.html",
             '<meta name="twitter:description" content="' + _bh_old_desc + '">',
             '<meta name="twitter:description" content="' + _bh_new_desc + '">'))
HEAD.append(("picks/big-hits/index.html",
             '"name": "Big Hits \u2014 126 of the Desk&rsquo;s Hardest Calls, Landed | The Prediction Desk"',
             '"name": "Big Hits \u2014 146 of the Desk&rsquo;s Hardest Calls, Landed | The Prediction Desk"'))


def apply_file(rel, replacements, required=True):
    path = os.path.join(ROOT, rel)
    text = open(path, encoding="utf-8").read()
    changed = 0
    for old, new in replacements:
        n = text.count(old)
        if n == 0:
            if new in text:
                print("  %s: already applied: %r" % (rel, old[:70]))
                continue
            print("  MISSING in %s: %r" % (rel, old[:100]))
            if required:
                raise SystemExit("FAILED: old string not found in %s: %r" % (rel, old[:160]))
            continue
        text = text.replace(old, new)
        changed += n
        print("  %s: replaced %d x %r" % (rel, n, old[:70]))
    open(path, "w", encoding="utf-8").write(text)
    return changed


def main():
    total = 0
    print("== head-tag replacements ==")
    by_file = {}
    for rel, old, new in HEAD:
        by_file.setdefault(rel, []).append((old, new))
    for rel, reps in by_file.items():
        total += apply_file(rel, reps)

    print("== stale figure phrases (record pages, picks index, picks sport pages) ==")
    targets = ["record/index.html", "record-in-numbers/index.html", "picks/index.html"]
    import glob
    targets += sorted(glob.glob(os.path.join(ROOT, "picks", "*", "index.html")))
    # also the picks big-hits page
    targets = sorted(set(t if os.path.isabs(t) else os.path.join(ROOT, t) for t in targets))
    for path in targets:
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding="utf-8").read()
        changed = 0
        for old, new in STALE:
            n = text.count(old)
            if n:
                text = text.replace(old, new)
                changed += n
                print("  %s: replaced %d x %r" % (rel, n, old[:70]))
        if changed:
            open(path, "w", encoding="utf-8").write(text)
            total += changed
    print("TOTAL replacements: %d" % total)
    print("stats: papers=%d desk=%d/%d/%d recorded=%d open=%d rate=%.1f%% big_hits=%s as_of=%s"
          % (PAPERS, desk["hits"], desk["misses"], desk["scored"], desk["recorded"],
             desk["open"], desk["hit_rate_pct"], desk["big_hits"], AS_OF))


if __name__ == "__main__":
    main()
