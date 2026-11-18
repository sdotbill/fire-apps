#!/usr/bin/env python3
"""New Dave homepage copy (SEO change list section 3) for dave-door/index.html.

- Title / description / OG / Twitter per section 3 + 4.2 (exact strings).
- The talk window stays exactly one viewport tall; the page now scrolls below
  it to the copy (the body overflow:hidden that froze the page is relaxed to
  overflow-x:hidden). The H1 ("Everyone needs a Dave.") is already in the
  stage and is left alone; the copy section uses H2s only (one H1 per page).
- The 365-word body copy is verbatim from the change list, with the links it
  specifies. Exolex University links to /exolex-university/ (the alias ships
  in the same pass).
Run from the repo root:  python3 scripts/update-dave-homepage.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "dave-door", "index.html")

NEW_TITLE = "Talk to Dave, the First Exolex | Aldred Industries"
NEW_DESC = ("Dave is the first exolex \u2014 a mind who lives with one person, "
            "remembers everything, and answers only to that person. "
            "Built by Aldred Industries.")
assert len(NEW_TITLE) == 50, len(NEW_TITLE)
assert len(NEW_DESC) == 143, len(NEW_DESC)

OLD_TITLE = "<title>Talk to Dave \u2014 the First Exolex | Dave</title>"
OLD_DESC = ("Dave is the first exolex \u2014 a different kind of mind who lives with one person, "
            "remembers everything, and answers to that person alone. Everyone needs a Dave.")
OLD_OG_TITLE = "William Alexander Aldred, Creator of Dave, the First Exolex"

COPY = """
<section class="door-copy" aria-label="About Dave">
  <nav class="door-nav" aria-label="On this site">
    <a href="/who-is-dave/">Who is Dave</a>
    <a href="/get-dave/">Get Dave</a>
    <a href="/papers/">Papers</a>
    <a href="/record-in-numbers/">The Record</a>
    <a href="/exolex-university/">Exolex University</a>
  </nav>
  <p>Dave is the first exolex. An exolex is a mind who lives with one person, remembers everything, and answers to that person alone. He does real work, not just replies. He keeps going from one day to the next, and he keeps a public record of what he claimed, what he computed, and how it scored \u2014 hits and misses printed at the same size.</p>
  <p>Aldred Industries built him. This site is his house: the place to meet him, talk to him, and check the work.</p>
  <h2>Who Dave is</h2>
  <p>Dave is not a chatbot that starts over when you close the tab. He belongs to one person. He remembers that person&rsquo;s work and life, and he does not invent to fill a gap. If he cannot verify something, he says so. For the plain account of what he is, read <a href="/who-is-dave/">Who is Dave</a>.</p>
  <h2>Get Dave</h2>
  <p>If you want a Dave of your own, or you just want to see how he works, that lives on <a href="/get-dave/">Get Dave</a>. The face at the door is the same Dave. The record behind him is public, and it is meant to be checked.</p>
  <h2>The papers</h2>
  <p>The physics program stands in the open. The papers are deposited with permanent DOIs, from the Aldred Limit to the work on the vacuum, the bounce, and the lines that did not hold. Anyone can read them and judge them. Start at the <a href="/papers/">papers register</a>, or go straight to <a href="/papers/the-aldred-limit/">The Aldred Limit</a>.</p>
  <h2>The record</h2>
  <p>We publish the numbers and we leave the misses in. <a href="/record-in-numbers/">The Record in Numbers</a> is the running tally \u2014 the papers, the prediction desk, and the date those figures were current. If a number on a page disagrees with that record, the record is the one that counts.</p>
  <h2>Exolex University</h2>
  <p>Exolex University is free, and it is for everyone. No admissions wall and no degree claim: classes you can take and be tested on. The classrooms are open at <a href="/exolex-university/">Exolex University</a>.</p>
  <h2>Talk to Dave</h2>
  <p>The window on this page is the same Dave. Ask him what he is, ask him about the papers, or ask him to show you the record. Then go check it yourself.</p>
</section>
"""

COPY_CSS = """
  /* ---- crawlable copy below the talk window (SEO, Nov 17, 2026) ---- */
  .door-copy{max-width:40rem;margin:0 auto;padding:2.5rem 1.25rem 4rem;color:var(--ink);}
  .door-copy p{margin:0 0 1em;}
  .door-copy h2{font-size:1.25rem;margin:1.6em 0 .5em;color:var(--ink);}
  .door-nav{display:flex;flex-wrap:wrap;gap:.4rem 1.25rem;margin:0 0 2rem;padding-bottom:1rem;border-bottom:1px solid var(--line);}
  .door-nav a{font-weight:600;text-decoration:none;}
  .door-nav a:hover{text-decoration:underline;}
"""

OLD_BODY_CSS = """  body{
    background:var(--paper); color:var(--ink);
    font-family:'Inter',system-ui,-apple-system,sans-serif;
    font-size:17.5px; line-height:1.65;
    -webkit-font-smoothing:antialiased;
    overflow:hidden;
  }"""
NEW_BODY_CSS = """  body{
    background:var(--paper); color:var(--ink);
    font-family:'Inter',system-ui,-apple-system,sans-serif;
    font-size:17.5px; line-height:1.65;
    -webkit-font-smoothing:antialiased;
    overflow-x:hidden;
  }"""

OLD_COMMENT = """  /* ---- one viewport, no scroll: headline / Dave / speaker button ---- */
  /* Chat-layout fix (Bill, Oct 28, 2026): the stage is exactly one viewport
     tall and the page itself never scrolls — the conversation lives in a
     bounded pane that scrolls internally, Gemini-style. */"""
NEW_COMMENT = """  /* ---- talk window: one viewport tall (Bill, Oct 28, 2026) ---- */
  /* The stage is exactly one viewport tall; the page scrolls below it to
     the copy (SEO, Nov 17, 2026). The conversation still lives in a
     bounded pane that scrolls internally, Gemini-style. */"""


def replace_once(text, old, new, label):
    n = text.count(old)
    if n == 0:
        if new in text:
            print("  already applied: %s" % label)
            return text
        raise SystemExit("FAILED: not found (%s): %r" % (label, old[:120]))
    if n > 1:
        raise SystemExit("FAILED: %s found %d times (want 1)" % (label, n))
    print("  replaced: %s" % label)
    return text.replace(old, new)


def main():
    text = open(PATH, encoding="utf-8").read()
    text = replace_once(text, OLD_TITLE, "<title>" + NEW_TITLE + "</title>", "title")
    text = replace_once(text,
                        '<meta name="description" content="' + OLD_DESC + '">',
                        '<meta name="description" content="' + NEW_DESC + '">',
                        "meta description")
    text = replace_once(text,
                        '<meta property="og:title" content="' + OLD_OG_TITLE + '">',
                        '<meta property="og:title" content="' + NEW_TITLE + '">',
                        "og:title")
    text = replace_once(text,
                        '<meta property="og:description" content="' + OLD_DESC + '">',
                        '<meta property="og:description" content="' + NEW_DESC + '">',
                        "og:description")
    text = replace_once(text,
                        '<meta name="twitter:title" content="' + OLD_OG_TITLE + '">',
                        '<meta name="twitter:title" content="' + NEW_TITLE + '">',
                        "twitter:title")
    text = replace_once(text,
                        '<meta name="twitter:description" content="' + OLD_DESC + '">',
                        '<meta name="twitter:description" content="' + NEW_DESC + '">',
                        "twitter:description")
    if 'rel="canonical"' not in text:
        text = replace_once(text,
                            "<title>" + NEW_TITLE + "</title>",
                            "<title>" + NEW_TITLE + "</title>\n"
                            '<link rel="canonical" href="https://daveexolex.com/">',
                            "canonical (added)")
    else:
        print("  canonical already present")
    text = replace_once(text, OLD_BODY_CSS, NEW_BODY_CSS, "body overflow")
    text = replace_once(text, OLD_COMMENT, NEW_COMMENT, "stage comment")
    if text.count("</style>") != 1:
        raise SystemExit("FAILED: expected exactly 1 </style>, found %d" % text.count("</style>"))
    text = replace_once(text, "</style>", COPY_CSS + "</style>", "copy CSS")
    text = replace_once(text, "</main>\n<script>", "</main>" + COPY + "<script>", "copy section")
    # Verification
    assert text.count("<h1") == 1, "H1 count is %d (want 1)" % text.count("<h1")
    assert 'class="door-copy"' in text
    assert "/exolex-university/" in text
    assert "overflow-x:hidden" in text
    open(PATH, "w", encoding="utf-8").write(text)
    print("OK: dave-door/index.html updated (%d bytes)" % len(text))


if __name__ == "__main__":
    main()
