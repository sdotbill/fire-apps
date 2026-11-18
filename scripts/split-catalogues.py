#!/usr/bin/env python3
"""Split the two catalogue pages into slim landings + category pages
(SEO change list sections 2.2 and 2.3).

for-the-world/index.html (1,240,978 bytes, 699 cards):
  landing = H1 + honest note + licence intro (2 licence cards) + one
  card/link per category (10) + "Given, not sold" + footer. Target < 100 KB.
  category pages = /for-the-world/<slug>/ with that category's designs.
world-problems/index.html (919,088 bytes, 832 cards, 49 categories):
  landing = H1 + "How the work is done" + "The catalogue" + one card/link
  per category (49) + CTA + "The model: designs for licence" +
  "Given, not sold". category pages = /world-problems/<slug>/.
  The change list named 10 categories; the page actually holds 49 (the
  10 named + Children, Old age, Home water + 36 more). A category page is
  built for EVERY category H2, so no paper is orphaned by the slim
  landing. Slugs for the 10 named categories match the change list
  exactly; the rest are slugified from their H2 text.

Both pages: one H1 per page; JSON-LD is one CollectionPage + one
ItemList of the items on that page only (the 158 KB / 203 KB whole-
catalogue dumps in the heads are gone). Descriptions shortened to the
140-160 band. Relative links (../...) are made root-absolute so they
resolve from the category pages (one level deeper). The design/paper
cards link to DOIs (absolute) and are carried verbatim; no world-
problems paper has a /papers/{slug}/ article page (0 of 832 DOIs match
the 285 article pages), so the DOI links stand as published.

Structure: each page is a series of <section> blocks in <main> (one
H2 per section, except one H2-less CTA section in world-problems).
Sections are parsed as <section>...</section> blocks (depth-counted),
not H2-to-H2 spans. Cards are loose <div class="card"> siblings inside
their section; they are split on their start markers with a depth-count
that falls back to the chunk when a card is missing its closing </div>.

Run from the repo root:  python3 scripts/split-catalogues.py
"""
import json
import os
import re
from urllib.parse import urljoin

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://daveexolex.com"

FTW_SLUG = {
    "Health": "health", "Water": "water",
    "Food & Agriculture": "food-agriculture", "Energy": "energy",
    "Housing & Shelter": "housing-shelter",
    "Observation & Instruments": "observation-instruments",
    "Transport": "transport", "Computing & Data": "computing-data",
    "Environment": "environment", "Other": "other",
}
WP_SLUG = {
    "Water": "water", "Food and farming": "food-and-farming",
    "Energy where people live": "energy",
    "Health without money": "health",
    "Shelter and infrastructure": "shelter",
    "Air, fire and disaster": "air-fire-disaster",
    "Body and mobility": "body-and-mobility",
    "Dangerous work": "dangerous-work", "Cities": "cities",
    "Sea and shore": "sea-and-shore", "Children": "children",
    "Old age": "old-age", "Home water": "home-water",
}


def slugify(text):
    s = text.lower()
    s = s.replace('&', ' and ')
    s = re.sub(r"['\u2019]", '', s)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s or '').strip()


def parse_sections(main):
    """<section>...</section> blocks in <main>, depth-counted.
    Returns (pre_html, [(h2_text_or_None, section_html), ...])."""
    sec_re = re.compile(r'<section\b[^>]*>|</section>')
    open_re = re.compile(r'<section\b[^>]*>')
    sections = []
    pos = 0
    first_start = None
    while True:
        m = open_re.search(main, pos)
        if not m:
            break
        if first_start is None:
            first_start = m.start()
        start = m.start()
        depth = 0
        j = start
        end = None
        while j < len(main):
            mm = sec_re.search(main, j)
            if not mm:
                break
            if mm.group(0).startswith('</'):
                depth -= 1
                j = mm.end()
                if depth == 0:
                    end = j
                    break
            else:
                depth += 1
                j = mm.end()
        if end is None:
            raise SystemExit("unbalanced <section> at %d" % start)
        sec_html = main[start:end]
        h2 = re.search(r'<h2[^>]*>(.*?)</h2>', sec_html, re.S)
        h2_text = strip_tags(h2.group(1)) if h2 else None
        sections.append((h2_text, sec_html))
        pos = end
    pre = main[:first_start] if first_start is not None else main
    return pre, sections


def extract_cards(section_html):
    """Cards in a section (loose <div class="card"> siblings). Returns
    (intro_html, [card_html, ...]). intro_html is the section content
    before the first card (with the leading <section> tag and H2 kept)."""
    starts = [m.start() for m in re.finditer(r'<div class="card">', section_html)]
    intro = section_html[:starts[0]] if starts else section_html
    cards = []
    div_re = re.compile(r'<div\b[^>]*>|</div>')
    for i, s in enumerate(starts):
        nxt = starts[i + 1] if i + 1 < len(starts) else len(section_html)
        depth = 0
        j = s
        end = None
        while j < nxt:
            m = div_re.search(section_html, j)
            if not m or m.start() >= nxt:
                break
            if m.group(0).startswith('</'):
                depth -= 1
                j = m.end()
                if depth == 0:
                    end = j
                    break
            else:
                depth += 1
                j = m.end()
        if end is not None:
            cards.append(section_html[s:end])
        else:
            chunk = section_html[s:nxt].rstrip()
            # Drop a trailing </section> if the chunk ran to the section end.
            chunk = re.sub(r'</section>\s*$', '', chunk)
            opens = len(re.findall(r'<div\b[^>]*>', chunk))
            closes = chunk.count('</div>')
            if opens > closes:
                chunk += '</div>' * (opens - closes)
            cards.append(chunk)
    return intro, cards


def absolutize(html, base_path):
    def repl(m):
        attr, href = m.group(1), m.group(2)
        if href.startswith(('http://', 'https://', '/', '#', 'mailto:', 'data:')):
            return m.group(0)
        return '%s="%s"' % (attr, urljoin(BASE + base_path, href)[len(BASE):])
    return re.sub(r'(href|src)="([^"]*)"', repl, html)


def json_ld(page_url, page_title, page_desc, items):
    graph = [
        {"@type": "CollectionPage",
         "@id": page_url + "#webpage",
         "url": page_url,
         "name": page_title,
         "description": page_desc,
         "isPartOf": {"@id": BASE + "/#website"},
         "inLanguage": "en-US"},
        {"@type": "ItemList",
         "itemListElement": [
             {"@type": "ListItem", "position": i + 1,
              "name": it['name'], "url": it['url']}
             for i, it in enumerate(items)]},
    ]
    return ('<script type="application/ld+json">\n' +
            json.dumps({"@context": "https://schema.org", "@graph": graph},
                       ensure_ascii=False, separators=(',', ':')) +
            '\n</script>')


def card_name_url(card_html):
    m = re.search(r'<h3[^>]*><a href="([^"]*)">(.*?)</a></h3>', card_html, re.S)
    if m:
        return strip_tags(m.group(2)), m.group(1)
    m2 = re.search(r'<h3[^>]*>(.*?)</h3>', card_html, re.S)
    if m2:
        return strip_tags(m2.group(1)), None
    m3 = re.search(r'10\.5281/zenodo\.(\d+)', card_html)
    return ("Design " + m3.group(1)) if m3 else "Design", (
        "https://doi.org/10.5281/zenodo." + m3.group(1)) if m3 else None


def check_desc(desc, label):
    if not (140 <= len(desc) <= 160):
        raise SystemExit("description out of band (%s, %d chars): %s"
                         % (label, len(desc), desc))
    return desc


def fit_desc(prefix, tails, label):
    """Category descriptions: the category name varies from 5 to 45
    characters, so no single fixed template lands in the 140-160 band
    for all of them. Pick the longest tail that keeps the total in band."""
    for tail in tails:
        d = prefix + tail
        if 140 <= len(d) <= 160:
            return d
    # Fallback: shortest tail, truncated at a word boundary to 160.
    d = prefix + tails[-1]
    if len(d) > 160:
        cut = d[:160]
        cut = cut.rsplit(' ', 1)[0] + '.'
        return cut
    raise SystemExit("cannot fit description in band (%s): %s" % (label, d))


FTW_TAILS = [
    "published openly with permanent DOIs and licensed to manufacturers, so others can build them all.",
    "published openly with permanent DOIs and licensed to manufacturers, so others can build them.",
    "published openly with permanent DOIs and licensed to manufacturers so others can build them.",
    "published with permanent DOIs and licensed to manufacturers so others can build them.",
    "published openly with DOIs and licensed to manufacturers.",
    "published with DOIs and licensed to manufacturers.",
]
WP_TAILS = [
    "published with DOIs: working designs, honest bounds, and published disproofs of false hopes.",
    "published with DOIs: working designs, honest bounds, and disproofs of false hopes.",
    "published with DOIs: working designs, honest bounds, and disproofs.",
    "published with DOIs: working designs and honest bounds.",
    "published with DOIs.",
]


def parse_page(path):
    text = open(path, encoding='utf-8').read()
    head_start = text.find('<head>')
    ld_start = text.find('<script type="application/ld+json">')
    head = text[head_start:ld_start]
    body_start = text.find('<body>')
    main_start = text.find('<main')
    main_end = text.find('</main>')
    header = text[body_start:main_start]
    closing = text[main_end:]
    assert closing.rstrip().endswith('</html>')
    main = text[main_start:main_end]
    pre, sections = parse_sections(main)
    return text, head, header, closing, pre, sections


def build_page(head, header, main_inner, closing, page_url, page_title,
               page_desc, items, base_path):
    h = head
    h = re.sub(r'<title>.*?</title>', '<title>' + page_title + '</title>',
               h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="' + page_desc + '">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">',
               '<meta property="og:title" content="' + page_title + '">', h)
    h = re.sub(r'<meta name="twitter:title" content="[^"]*">',
               '<meta name="twitter:title" content="' + page_title + '">', h)
    h = re.sub(r'<meta property="og:description" content="[^"]*">',
               '<meta property="og:description" content="' + page_desc + '">', h)
    h = re.sub(r'<meta name="twitter:description" content="[^"]*">',
               '<meta name="twitter:description" content="' + page_desc + '">', h)
    h = re.sub(r'<link rel="canonical" href="[^"]*">',
               '<link rel="canonical" href="' + page_url + '">', h)
    h = re.sub(r'<meta property="og:url" content="[^"]*">',
               '<meta property="og:url" content="' + page_url + '">', h)
    h = absolutize(h, base_path)
    assert ('<title>' + page_title + '</title>') in h
    assert ('content="' + page_desc + '"') in h
    assert ('href="' + page_url + '"') in h
    ld = json_ld(page_url, page_title, page_desc, items)
    return (h + ld + '\n</head>\n' + absolutize(header, base_path) +
            main_inner + absolutize(closing, base_path))


def strip_section_h2(section_html):
    """Remove the first <h2>...</h2> from a section (the category page
    carries the name as its H1 instead)."""
    out, n = re.subn(r'<h2[^>]*>.*?</h2>', '', section_html, count=1, flags=re.S)
    assert n == 1, "no H2 to strip"
    return out


def split_for_the_world():
    path = os.path.join(ROOT, "for-the-world", "index.html")
    text, head, header, closing, pre, sections = parse_page(path)
    base = "/for-the-world/"
    sec = {}
    for h2t, html in sections:
        assert h2t is not None, "a for-the-world section has no H2"
        sec[h2t] = html
    assert set(FTW_SLUG) <= set(sec), set(FTW_SLUG) - set(sec)
    assert len(sections) == 13, len(sections)
    cats = []
    for name, slug in FTW_SLUG.items():
        intro_h, cards = extract_cards(sec[name])
        cats.append({'name': name, 'slug': slug, 'intro': intro_h,
                     'cards': cards})
    total_cards = sum(len(c['cards']) for c in cats)
    assert total_cards == 697, total_cards
    land_desc = check_desc(
        "For the World: Aldred Industries' design catalogue \u2014 inventions "
        "for water, health, food, energy, and shelter, published with DOIs, "
        "licensed to manufacturers.",
        "for-the-world landing")
    land_title = "For the World \u2014 Inventions Built to Help the World | Aldred Industries"
    land_items = [{'name': c['name'] + " \u2014 " + str(len(c['cards'])) + " designs",
                   'url': BASE + base + c['slug'] + '/'} for c in cats]
    cat_links = []
    for c in cats:
        cat_links.append(
            '<div class="card">\n<h3><a href="%s">%s</a></h3>\n'
            '<p>%d designs, published openly with permanent DOIs and licensed '
            'to manufacturers. <a href="%s">See the %s designs &rarr;</a></p>\n</div>'
            % ("/for-the-world/" + c['slug'] + "/", c['name'], len(c['cards']),
               "/for-the-world/" + c['slug'] + "/", c['name']))
    # Landing: pre (<main>) + honest-note section + licence section +
    # category links + "Given, not sold" section.
    landing_inner = (pre + sec["An honest note on what these designs are"] +
                     sec["Licence a design"] +
                     '<section>\n<h2>Designs by field</h2>\n' +
                     '\n'.join(cat_links) + '\n</section>\n' +
                     sec["Given, not sold"])
    landing = build_page(head, header, landing_inner, closing,
                         BASE + base, land_title, land_desc, land_items, base)
    assert landing.count('<h1') == 1
    assert len(landing) < 100000, len(landing)
    open(path, 'w', encoding='utf-8').write(landing)
    print("for-the-world/ landing: %d bytes (was %d)" % (len(landing), len(text)))
    for c in cats:
        items = []
        for card in c['cards']:
            name, url = card_name_url(card)
            items.append({'name': name, 'url': url or (BASE + base)})
        desc = fit_desc(
            "%s designs \u2014 For the World. %d inventions, " % (c['name'], len(c['cards'])),
            FTW_TAILS, "for-the-world/" + c['slug'])
        title = "%s \u2014 For the World | Aldred Industries" % c['name']
        header_cat = header.replace('<h1>For the World</h1>',
                                    '<h1>%s</h1>' % c['name'])
        assert header_cat != header, "H1 not found in header for " + c['slug']
        # The category page carries the name as its H1 (in the header), so
        # the section's H2 is stripped; the intro <p> and the balanced
        # cards are kept, closed by the section's own </section>.
        body_intro = strip_section_h2(c['intro'])
        inner = ('<main>\n%s\n%s\n</section>\n<p><a href="/for-the-world/">&larr; Back to For the World</a></p>\n'
                 % (body_intro, '\n'.join(c['cards'])))
        page = build_page(head, header_cat, inner, closing,
                          BASE + base + c['slug'] + '/', title, desc, items, base)
        assert page.count('<h1') == 1, c['slug']
        outdir = os.path.join(ROOT, "for-the-world", c['slug'])
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        print("  for-the-world/%s/: %d bytes (%d designs)"
              % (c['slug'], len(page), len(c['cards'])))
    return len(cats), total_cards


def split_world_problems():
    path = os.path.join(ROOT, "world-problems", "index.html")
    text, head, header, closing, pre, sections = parse_page(path)
    base = "/world-problems/"
    sec = {}
    cta = None
    for h2t, html in sections:
        if h2t is None:
            assert cta is None, "two H2-less sections"
            cta = html
        else:
            assert h2t not in sec, "duplicate H2: " + h2t
            sec[h2t] = html
    assert len(sections) == 54, len(sections)
    framing = {"How the work is done", "The catalogue",
               "The model: designs for licence", "Given, not sold"}
    cat_names = [h2t for h2t, _ in sections
                 if h2t is not None and h2t not in framing]
    assert len(cat_names) == 49, len(cat_names)
    slugs = {}
    for name in cat_names:
        slugs[name] = WP_SLUG.get(name) or slugify(name)
    assert len(set(slugs.values())) == len(slugs), "slug collision"
    cats = []
    for name in cat_names:
        intro_h, cards = extract_cards(sec[name])
        cats.append({'name': name, 'slug': slugs[name], 'intro': intro_h,
                     'cards': cards})
    total_cards = sum(len(c['cards']) for c in cats)
    assert total_cards == 832, total_cards
    land_desc = check_desc(
        "Aldred Industries attacks the world's practical problems \u2014 safe "
        "water, food, energy, health, shelter, disaster warning \u2014 every "
        "result published with a DOI.",
        "world-problems landing")
    land_title = "Solving the World's Problems \u2014 The World-Problems Papers | Aldred Industries"
    land_items = [{'name': c['name'] + " \u2014 " + str(len(c['cards'])) + " papers",
                   'url': BASE + base + c['slug'] + '/'} for c in cats]
    cat_links = []
    for c in cats:
        cat_links.append(
            '<div class="card">\n<h3><a href="%s">%s</a></h3>\n'
            '<p>%d papers. <a href="%s">See the %s papers &rarr;</a></p>\n</div>'
            % ("/world-problems/" + c['slug'] + "/", c['name'], len(c['cards']),
               "/world-problems/" + c['slug'] + "/", c['name']))
    # Landing: pre (<main> + hero H1) + How the work is done + The
    # catalogue + category links + CTA + The model + Given, not sold.
    landing_inner = (pre + sec["How the work is done"] + sec["The catalogue"] +
                     '<section>\n<h2>Problems by subject</h2>\n' +
                     '\n'.join(cat_links) + '\n</section>\n' +
                     (cta or '') + sec["The model: designs for licence"] +
                     sec["Given, not sold"])
    landing = build_page(head, header, landing_inner, closing,
                         BASE + base, land_title, land_desc, land_items, base)
    assert landing.count('<h1') == 1, landing.count('<h1')
    assert len(landing) < 100000, len(landing)
    open(path, 'w', encoding='utf-8').write(landing)
    print("world-problems/ landing: %d bytes (was %d)" % (len(landing), len(text)))
    for c in cats:
        items = []
        for card in c['cards']:
            name, url = card_name_url(card)
            items.append({'name': name, 'url': url or (BASE + base)})
        desc = fit_desc(
            "%s \u2014 Solving the World's Problems. %d papers, " % (c['name'], len(c['cards'])),
            WP_TAILS, "world-problems/" + c['slug'])
        title = "%s \u2014 Solving the World's Problems | Aldred Industries" % c['name']
        body_intro = strip_section_h2(c['intro'])
        inner = ('<main>\n<h1>%s</h1>\n%s\n%s\n</section>\n<p><a href="/world-problems/">&larr; Back to Solving the World\'s Problems</a></p>\n'
                 % (c['name'], body_intro, '\n'.join(c['cards'])))
        page = build_page(head, header, inner, closing,
                          BASE + base + c['slug'] + '/', title, desc, items, base)
        assert page.count('<h1') == 1, c['slug']
        outdir = os.path.join(ROOT, "world-problems", c['slug'])
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(page)
    print("  world-problems: %d category pages, %d cards total"
          % (len(cats), total_cards))
    return len(cats), total_cards


def main():
    n1, t1 = split_for_the_world()
    n2, t2 = split_world_problems()
    import glob
    for f in [os.path.join(ROOT, "for-the-world", "index.html"),
              os.path.join(ROOT, "world-problems", "index.html")] + \
             sorted(glob.glob(os.path.join(ROOT, "for-the-world", "*", "index.html"))) + \
             sorted(glob.glob(os.path.join(ROOT, "world-problems", "*", "index.html"))):
        t = open(f, encoding='utf-8').read()
        assert t.count('<h1') == 1, (f, t.count('<h1'))
        ld = re.findall(r'<script type="application/ld\+json">.*?</script>', t, re.S)
        assert len(ld) == 1, (f, len(ld))
        # One CollectionPage + one ItemList of the page's own items only
        # (never the whole catalogue). A category with many items runs
        # larger than a landing: cap 60 KB, far below the old 158 KB dump.
        assert len(ld[0]) < 60000, (f, len(ld[0]))
    print("VERIFIED: %d + %d category pages; %d + %d cards; one H1 each; "
          "JSON-LD < 60 KB each" % (n1, n2, t1, t2))


if __name__ == "__main__":
    main()
