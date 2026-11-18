#!/usr/bin/env python3
"""Paginate /papers/ (SEO change list section 2.1).

Source: papers/index.html (6,514,402 bytes, 41,593 lines).

What the source actually is (found by parsing, not by the change list's
estimate): the file holds TWO <main> blocks. main1 is the register
(5,912 cards, 5,906 unique DOIs — two DOIs appear twice). main2 is a
duplicated block (182 cards, every titled card in it also appears in
main1, plus its own duplicate H1). This script paginates main1 ONLY and
drops main2 entirely — which is also how the duplicate H1 is deleted.
The change list estimated 290 articles / 6 pages (the sitemap article
count); the register itself holds 5,912 cards, so at 50/page that is
119 pages. The card order is preserved exactly as published
(newest-first as the register stands; the date sections appear in the
order the build appended them — this pass paginates, it does not
re-sort the register).

Outputs:
- papers/catalogue.json — the register data (doi, title, url, date,
  section, paper_num, page) for all 5,912 cards.
- papers/index.html — slim landing: one H1, full intro, search box,
  latest 50 papers, pagination nav, CollectionPage + ItemList JSON-LD
  for those 50 only. Target < 150 KB HTML, < 20 KB JSON-LD.
- papers/page/2/ ... papers/page/119/ — 50 papers each, newest-first,
  rel="next"/rel="prev", canonical = the page itself, CollectionPage +
  ItemList JSON-LD for that page's papers only.
- papers/page/1/index.html — meta-refresh to /papers/ (a real 301 needs
  Cloudflare; the /papers/page/1/ -> /papers/ 301 is in the redirect
  lists for when that is installed). Canonical points to /papers/.
- The 290 /papers/{slug}/ article pages are NOT touched.

Relative links inside cards (the 285 article-page slugs, e.g.
href="the-sealed-record/") are rewritten to root-absolute
(/papers/the-sealed-record/) so they resolve from /papers/page/N/ too.
The head's relative asset paths (../assets/..., ../background.css) are
likewise made root-absolute. The second JSON-LD block (Aldred
Industries Organization + Person identity data) is kept on every page;
the first block (CollectionPage + 285 ScholarlyArticle nodes, 184 KB)
is replaced by a per-page CollectionPage + ItemList.

Run from the repo root:  python3 scripts/paginate-papers.py
"""
import json
import os
import re
from urllib.parse import urljoin

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "papers", "index.html")
CATALOGUE = os.path.join(ROOT, "papers", "catalogue.json")
PAGE_DIR = os.path.join(ROOT, "papers", "page")

BASE = "https://daveexolex.com"
PAPERS = BASE + "/papers/"
PER_PAGE = 50

NEW_DESC = ("William Alexander Aldred's physics papers, deposited with permanent DOIs "
            "\u2014 from the Aldred Limit to the vacuum problem. "
            "Every paper stands open to be judged.")
assert 140 <= len(NEW_DESC) <= 160, len(NEW_DESC)
OLD_DESC = ("William Alexander Aldred's physics papers \u2014 the complete register, "
            "publicly deposited with permanent DOIs, from the Aldred Limit to the "
            "vacuum-energy problem. Every paper stands open for anyone to judge.")

H1 = "The papers of William Alexander Aldred"


def split_cards(plist):
    """Split a <div class="paper-list"> block into its card HTML strings.

    The source has at least one card missing its closing </div> (a
    derivation-note card in the November 8, 2026 section), so div-depth
    counting swallows the next card. Splitting on the card start markers
    is robust to that: each card runs to the next card's start, and a
    card that is short on </div>s gets the missing closers appended.
    """
    m = re.match(r'\s*<div class="paper-list">', plist)
    assert m, "paper-list block does not start with its opening div"
    inner = plist[m.end():]
    # The last </div> in the block closes the paper-list itself.
    idx = inner.rfind('</div>')
    assert idx != -1, "paper-list block has no closing div"
    inner = inner[:idx]
    starts = [mm.start() for mm in re.finditer(r'<div class="card">', inner)]
    chunks = []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(inner)
        chunk = inner[s:e]
        opens = len(re.findall(r'<div\b[^>]*>', chunk))
        closes = chunk.count('</div>')
        if opens > closes:
            chunk = chunk.rstrip() + '</div>' * (opens - closes) + '\n'
        chunks.append(chunk)
    return chunks


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s or '').strip()


def card_info(card_html, section):
    """Title, DOI, URL, date, paper_num for one card."""
    m = re.search(r'<h3[^>]*><a href="([^"]*)">(.*?)</a></h3>', card_html, re.S)
    href = m.group(1) if m else None
    title = strip_tags(m.group(2)) if m else None
    mdoi = re.search(r'10\.5281/zenodo\.(\d+)', card_html)
    doi = mdoi.group(1) if mdoi else None
    # URL: the h3 link resolved to an absolute URL (article page or DOI).
    url = None
    if href:
        url = urljoin(PAPERS, href)
        # A DOI href stays a DOI link; a slug href becomes the article page.
        if href.startswith('https://doi.org/'):
            url = href
    # Date: from the byline if it carries one.
    date = None
    mb = re.search(r'<p class="byline">(.*?)</p>', card_html, re.S)
    if mb:
        byline = strip_tags(mb.group(1))
        md = re.search(
            r'(January|February|March|April|May|June|July|August|September|'
            r'October|November|December)\s+\d{1,2},\s+\d{4}|'
            r'(January|February|March|April|May|June|July|August|September|'
            r'October|November|December)\s+\d{4}', byline)
        if md:
            date = md.group(0)
    mnum = re.search(r'<span class="paper-num">([^<]*)</span>', card_html)
    paper_num = strip_tags(mnum.group(1)) if mnum else None
    return {'doi': doi, 'title': title, 'url': url, 'date': date,
            'section': section, 'paper_num': paper_num}


def rewrite_card_links(card_html):
    """Make relative hrefs in a card root-absolute (they must resolve from
    /papers/page/N/ as well as from /papers/)."""
    def repl(m):
        href = m.group(1)
        if href.startswith(('http://', 'https://', '/', '#', 'mailto:', 'data:')):
            return m.group(0)
        abs_url = urljoin(PAPERS, href)
        return 'href="%s"' % abs_url[len(BASE):]
    return re.sub(r'href="([^"]*)"', repl, card_html)


def page_nav(current, total):
    """Compact windowed pagination nav."""
    def link(p, label=None, cls=None):
        label = label or str(p)
        href = "/papers/" if p == 1 else "/papers/page/%d/" % p
        c = ' class="%s"' % cls if cls else ''
        if p == current:
            return '<span class="pg-cur"%s>%s</span>' % (c, label)
        return '<a href="%s"%s>%s</a>' % (href, c, label)
    parts = []
    if current > 1:
        parts.append(link(current - 1, "&larr; Previous"))
    # Window: 1, 2, current-2..current+2, total-1, total (deduped, sorted).
    pages = sorted(set([1, 2, total - 1, total] +
                       list(range(max(1, current - 2), min(total, current + 2) + 1))))
    pages = [p for p in pages if 1 <= p <= total]
    last = 0
    for p in pages:
        if p - last > 1:
            parts.append('<span class="pg-gap">&hellip;</span>')
        parts.append(link(p))
        last = p
    if current < total:
        parts.append(link(current + 1, "Next &rarr;"))
    return ('<nav class="paper-pages" aria-label="Register pages">'
            'Page %d of %d &middot; %s</nav>' % (current, total, ' '.join(parts)))


def json_ld(page_url, page_title, page_desc, items):
    """One CollectionPage + one ItemList of this page's papers only."""
    graph = [
        {"@type": "CollectionPage",
         "@id": page_url + "#webpage",
         "url": page_url,
         "name": page_title,
         "description": page_desc,
         "isPartOf": {"@id": BASE + "/#website"},
         "inLanguage": "en-US",
         "about": {"@id": "https://premiummarketingsolutionsllc.com/#william-alexander-aldred"}},
        {"@type": "ItemList",
         "itemListElement": [
             {"@type": "ListItem", "position": i + 1,
              "name": it['title'] or ("Paper " + (it['doi'] or '')),
              "url": it['url']}
             for i, it in enumerate(items)]},
    ]
    return ('<script type="application/ld+json">\n' +
            json.dumps({"@context": "https://schema.org", "@graph": graph},
                       ensure_ascii=False, separators=(',', ':')) +
            '\n</script>')


def main():
    text = open(SRC, encoding="utf-8").read()
    # --- main1 is the register; main2 (a duplicated header + main block
    # appended after main1's </main>, 182 cards, every titled card also in
    # main1, plus its own duplicate H1) is dropped entirely.
    h1_pos = text.find('<h1 class="goldletters">' + H1 + '</h1>')
    assert h1_pos != -1
    m1_start = text.rfind('<main>', 0, h1_pos)
    m1_end = text.find('</main>', h1_pos)
    main1 = text[m1_start:m1_end]
    assert main1.count('<div class="card">') == 5912, main1.count('<div class="card">')
    # The header keeps the site chrome as-is (it contains a small
    # <main><div id="log"></div></main> widget container inside the header
    # form — part of the header, left alone).

    # --- Head template (everything up to the first JSON-LD block), with
    # relative asset paths made root-absolute.
    head_start = text.find('<head>')
    ld_start = text.find('<script type="application/ld+json">')
    head = text[head_start:ld_start]
    head = head.replace('../assets/', '/assets/').replace('../background.css', '/background.css')
    # Keep the second JSON-LD block (identity data) for every page.
    blocks = re.findall(r'<script type="application/ld\+json">.*?</script>', text, re.S)
    assert len(blocks) == 2
    identity_ld = blocks[1]
    # The description is replaced (203 -> 157 chars) on page 1; per-page
    # descriptions are built below.
    assert OLD_DESC in head, "old description not in head"
    head = head.replace(OLD_DESC, NEW_DESC)

    # --- Body parts.
    body_start = text.find('<body>')
    header_html = text[body_start:m1_start]
    assert header_html.rstrip().endswith('<div class="wrap">')
    # Intro: from the H1 through the paper-tools div (ends at the first
    # section H2). The search input is extracted for reuse on every page.
    first_h2 = main1.find('<h2 class="paper-range"')
    intro = main1[len('<main>'):first_h2]
    assert '<h1 class="goldletters">' + H1 + '</h1>' in intro
    m_search = re.search(r'<input type="search"[^>]*>', intro)
    assert m_search, "search input not found"
    search_html = '<div class="paper-tools">%s</div>' % m_search.group(0)
    # The jump nav (links to #range-N anchors) is replaced by pagination.
    intro = re.sub(r'<nav class="paper-jumps".*?</nav>', '', intro, flags=re.S)
    # About + record sections (page 1 only) and the closing (every page).
    # main1's About is the first '<h2>About the author</h2>' after main1
    # starts; the closing is a </main> plus the footer/scripts after the
    # LAST </main> in the file (main2's close) — main2 itself is dropped.
    about_start = text.find('<h2>About the author</h2>', m1_start)
    about_html = text[about_start:m1_end]
    assert about_html.startswith('<h2>About the author</h2>')
    m2_close = text.rfind('</main>')
    closing_html = '</main>\n' + text[m2_close + len('</main>'):]
    assert '<footer class="sitefoot">' in closing_html
    assert closing_html.rstrip().endswith('</html>')

    # --- Sections + cards from main1, in file order (newest-first as published).
    sections = []  # (h2_html, [card_html, ...])
    pos = 0
    while True:
        h2 = re.compile(r'<h2 class="paper-range"[^>]*>.*?</h2>', re.S).search(main1, pos)
        if not h2:
            break
        h2_html = h2.group(0)
        list_start = main1.find('<div class="paper-list">', h2.end())
        assert list_start != -1
        # The paper-list div ends at the next H2 or at the About section.
        next_h2 = re.compile(r'<h2 class="paper-range"', re.S).search(main1, h2.end())
        list_end = next_h2.start() if next_h2 else main1.find('<h2>About the author</h2>')
        plist = main1[list_start:list_end]
        cards = split_cards(plist)
        sections.append((h2_html, cards))
        pos = list_end
    # Flatten to the ordered card list, each tagged with its section text.
    ordered = []
    for h2_html, cards in sections:
        section_text = strip_tags(h2_html)
        for card_html in cards:
            info = card_info(card_html, section_text)
            info['card'] = rewrite_card_links(card_html)
            ordered.append(info)
    assert len(ordered) == 5912, len(ordered)
    total = (len(ordered) + PER_PAGE - 1) // PER_PAGE
    assert total == 119, total
    for i, it in enumerate(ordered):
        it['page'] = i // PER_PAGE + 1

    # --- catalogue.json (the register data, build-time).
    cat = [{k: it[k] for k in ('doi', 'title', 'url', 'date', 'section',
                               'paper_num', 'page')} for it in ordered]
    with open(CATALOGUE, 'w', encoding='utf-8') as f:
        json.dump({"generated": "2026-11-17", "total": len(cat),
                   "per_page": PER_PAGE, "pages": total,
                   "papers": cat}, f, ensure_ascii=False, indent=1)
    print("catalogue.json: %d papers, %d pages" % (len(cat), total))

    # --- Render the pages.
    def render_page(page_no, items, page_intro, page_desc, page_url, page_title):
        h = head
        h = h.replace('<title>Physics Papers \u2014 William Alexander Aldred</title>',
                      '<title>' + page_title + '</title>')
        h = h.replace('<meta property="og:title" content="Physics Papers \u2014 William Alexander Aldred">',
                      '<meta property="og:title" content="' + page_title + '">')
        h = h.replace('<meta name="twitter:title" content="Physics Papers \u2014 William Alexander Aldred">',
                      '<meta name="twitter:title" content="' + page_title + '">')
        h = h.replace('<link rel="canonical" href="https://daveexolex.com/papers/">',
                      '<link rel="canonical" href="' + page_url + '">')
        h = h.replace('<meta property="og:url" content="https://daveexolex.com/papers/">',
                      '<meta property="og:url" content="' + page_url + '">')
        h = h.replace('<meta name="description" content="' + NEW_DESC + '">',
                      '<meta name="description" content="' + page_desc + '">')
        h = h.replace('<meta property="og:description" content="' + NEW_DESC + '">',
                      '<meta property="og:description" content="' + page_desc + '">')
        h = h.replace('<meta name="twitter:description" content="' + NEW_DESC + '">',
                      '<meta name="twitter:description" content="' + page_desc + '">')
        # rel next/prev (appended at the end of the head template, which
        # ends just before the JSON-LD — it holds no </head> to anchor on).
        rels = []
        if page_no > 1:
            prev_url = PAPERS if page_no == 2 else PAPERS + "page/%d/" % (page_no - 1)
            rels.append('<link rel="prev" href="%s">' % prev_url)
        if page_no < total:
            rels.append('<link rel="next" href="%s">' % (PAPERS + "page/%d/" % (page_no + 1)))
        if rels:
            h = h + '\n'.join(rels) + '\n'
        ld = json_ld(page_url, page_title, page_desc, items)
        # Group this page's cards under their section H2s, in the source
        # structure: H2, then a <div class="paper-list"> of its cards.
        body_parts = []
        cur_section = None
        cur_cards = []
        for it in items:
            if it['section'] != cur_section:
                if cur_cards:
                    body_parts.append('<div class="paper-list">\n' + '\n'.join(cur_cards) + '\n</div>')
                    cur_cards = []
                cur_section = it['section']
                for h2_html, _ in sections:
                    if strip_tags(h2_html) == cur_section:
                        body_parts.append(h2_html)
                        break
                else:
                    body_parts.append('<h2 class="paper-range">%s</h2>' % cur_section)
            cur_cards.append(it['card'])
        if cur_cards:
            body_parts.append('<div class="paper-list">\n' + '\n'.join(cur_cards) + '\n</div>')
        body = '\n'.join(body_parts)
        nav = page_nav(page_no, total)
        page = (h + ld + '\n' + identity_ld + '\n</head>\n' + header_html +
                '<main> \n' + page_intro + '\n' + nav + '\n' +
                body + '\n' + nav + '\n')
        return page

    # Page 1: the slim landing (full intro + About/Record + footer).
    p1_items = ordered[:PER_PAGE]
    p1_url = PAPERS
    p1_title = "Physics Papers \u2014 William Alexander Aldred"
    p1 = render_page(1, p1_items, intro, NEW_DESC, p1_url, p1_title)
    # render_page opened <main> and the wrap; close with About + closing.
    p1 = p1 + about_html + closing_html
    assert p1.count('<h1') == 1, p1.count('<h1')
    open(SRC, 'w', encoding='utf-8').write(p1)
    print("papers/index.html: %d bytes (%d cards)" % (len(p1), len(p1_items)))

    # Pages 2..119.
    for page_no in range(2, total + 1):
        items = ordered[(page_no - 1) * PER_PAGE: page_no * PER_PAGE]
        page_url = PAPERS + "page/%d/" % page_no
        span = items[0]['section'] + (" \u2014 " + items[-1]['section']
                                      if items[-1]['section'] != items[0]['section'] else "")
        page_desc = ("Page %d of William Alexander Aldred's physics papers \u2014 %s. "
                     "Deposited with permanent DOIs; every paper stands open to be judged."
                     % (page_no, span))
        if len(page_desc) > 160:
            page_desc = ("Page %d of William Alexander Aldred's physics papers. "
                         "Deposited with permanent DOIs; every paper stands open to be judged."
                         % page_no)
        assert 100 <= len(page_desc) <= 160, (page_no, len(page_desc))
        page_title = "Physics Papers \u2014 William Alexander Aldred \u2014 Page %d" % page_no
        short_intro = ('<h1 class="goldletters">' + H1 + '</h1>\n'
                       '<p>Page %d of %d of the register \u2014 %d papers, newest-first. '
                       'The full register is %d papers; the latest 50 are on '
                       '<a href="/papers/">the register landing</a>.</p>\n%s\n'
                       % (page_no, total, len(ordered), len(ordered), search_html))
        page = render_page(page_no, items, short_intro, page_desc, page_url, page_title)
        page = page + closing_html
        assert page.count('<h1') == 1, (page_no, page.count('<h1'))
        outdir = os.path.join(PAGE_DIR, str(page_no))
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        if page_no in (2, 3, total):
            print("papers/page/%d/: %d bytes (%d cards)" % (page_no, len(page), len(items)))

    # /papers/page/1/ -> /papers/ (meta-refresh; the real 301 rides Cloudflare).
    os.makedirs(os.path.join(PAGE_DIR, '1'), exist_ok=True)
    redirect = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                '<title>Physics Papers \u2014 William Alexander Aldred</title>\n'
                '<link rel="canonical" href="https://daveexolex.com/papers/">\n'
                '<meta http-equiv="refresh" content="0; url=https://daveexolex.com/papers/">\n'
                '</head>\n<body>\n<p><a href="https://daveexolex.com/papers/">'
                'The papers register has moved to https://daveexolex.com/papers/</a></p>\n'
                '</body>\n</html>\n')
    with open(os.path.join(PAGE_DIR, '1', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(redirect)
    print("papers/page/1/: redirect to /papers/ (meta-refresh + canonical)")

    # --- Verification.
    total_cards = 0
    for page_no in range(1, total + 1):
        p = os.path.join(ROOT, 'papers', 'index.html') if page_no == 1 else \
            os.path.join(PAGE_DIR, str(page_no), 'index.html')
        t = open(p, encoding='utf-8').read()
        n = t.count('<div class="card">')
        total_cards += n
        assert t.count('<h1') == 1, (page_no, 'H1 count', t.count('<h1'))
        assert 'ScholarlyArticle' not in t, (page_no, 'ScholarlyArticle still present')
        ld_total = sum(len(b.group(0)) for b in
                       re.finditer(r'<script type="application/ld\+json">.*?</script>', t, re.S))
        assert ld_total < 20000, (page_no, 'JSON-LD too big', ld_total)
        if page_no == 1:
            assert len(t) < 150000, ('page 1 too big', len(t))
    assert total_cards == 5912, total_cards
    print("VERIFIED: %d pages, %d cards total, one H1 each, no ScholarlyArticle, "
          "JSON-LD < 20 KB each, page 1 < 150 KB" % (total, total_cards))


if __name__ == "__main__":
    main()
