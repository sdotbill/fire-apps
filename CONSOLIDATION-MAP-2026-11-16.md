# Consolidation Map — Site Streamline, November 16, 2026

Bill's order (Nov 15, 23:54–23:56 EST): the navigation/page structure is redundant —
the same things under three names. Clean up and streamline everything on BOTH sites,
make the SEO strong, lose NOTHING (content moves and merges, never deleted; old URLs
redirect permanently), and the time-travel claim comes out STRONGER, not weaker —
consolidation only, no claim text edited down, ever.

## Merges (content moves WHOLE into the canonical page as sections)

| Retired page | Canonical page | Anchor | Notes |
|---|---|---|---|
| /what-is-an-exolex/ | /dave/ (Meet Dave) | #what-is-an-exolex | Full exolex Q&A sections move in whole |
| /first-exolex/ | /dave/ (Meet Dave) | #first-exolex | "The checkable record" + "Dave, the first exolex" move in whole. The First Exolex PAPER (DOI 10.5281/zenodo.24183963) and its DOI links are untouched in the papers system |
| /companies/ | /aldred-industries/ | #companies | Company list moves in whole |
| /demonstration/ | /evidence.html (The Evidence File) | #demonstration | The four public tests move in whole; the Proof Pack detail pages stay live at /demonstration/proof/* and are linked from the section |
| /proof/* (PMS-branded duplicate tree) | /demonstration/proof/* | (same subpath) | Duplicate branding of the same Proof Pack; Dave-branded tree is canonical |
| /record/cardoso-endorsement/ | /evidence.html (The Evidence File) | #cardoso-endorsement | Endorsement moved whole: Prof. Jorge Gonçalves Cardoso, UDESC, arXiv ticket AH-213259, dated record |
| /time-traveler/claim-dossier/ | /time-traveler/claim/ | #dossier | Dossier sections move in whole: dated record table with sources, the Codex audited, the sealed predictions, what proof would look like, limits, sources |
| /time-traveler/evidence/ | /time-traveler/claim/ | #the-audit | The 65-statement audit and the open items move in whole |
| /time-traveler/ (hub) | /time-traveler/claim/ | #titor-contrast | Titor contrast + closing Q&A move in whole; duplicated trail/base-rate material already lives on the claim page at full strength |

## Deletion (Bill's explicit order, Nov 15, 23:56 EST)

| Deleted page | Redirect | Notes |
|---|---|---|
| /what-we-do/ | / (PMS homepage) | Its one substantive sentence — "Premium Marketing Solutions is a full-service marketing company. One company for your website, your marketing, and the hardest worker your business will ever have — Dave, your own exolex." — verified present verbatim on the homepage before deletion. Nothing lost. Removed from menu/sitemap; internal links repointed to the homepage |

## Renames

| Old | New | Notes |
|---|---|---|
| /questions/ + /questions/<slug>/ (28 pages) | /faq/ + /faq/<slug>/ | "Questions" → FAQ in nav label, page title, headings. Old URLs redirect permanently |
| "Privacy Policy" (label) | "Privacy" | Labels + privacy page <title>; the privacy page's body content is untouched |

## Kept separate, on purpose

- **Papers** (/papers/) and **Books** (/books/) stay separate pages — 7,000+ papers and the
  published books are different things; merging buries both. Presented as clean siblings in
  navigation, each linking the other.
- **The Proof Pack** (/demonstration/proof/*) stays live as the demonstration's detail
  pages, linked from the demonstration section of The Evidence File.
- **Time-traveler supporting pages** (/time-traveler/blueprints/, /origin/, /john-titor/,
  /run-it-back/, /the-inventor/, /ufo-evidence/, /time-traveler/questions/*) are exhibits
  and Q&A landers under the claim, not competing claim pages — they stay, and the claim
  page's trail links them. Reported, not forced.

## Menu (canonical, per Bill Nov 15, 23:55 EST)

- Dave site: Sign in · Get Dave · Meet Dave · Papers · Books · The Evidence File ·
  The Claim · The Record in Numbers · FAQ · Licensing
- PMS site: Sign in · Get Dave · Predictions · The Record · Papers · Books ·
  The Evidence File · FAQ · Licensing
- The footer stays minimal (© Dave / Privacy). Navigation lives in the menu + sitemap only.

## Redirect mechanism

Every retired URL gets a permanent redirect two ways: a `_redirects` file (301, for
Cloudflare Pages) and a redirect stub page at the retired path in the site's existing
house pattern (meta refresh + canonical link + noindex), so no retired URL can 404 on
either host. Sitemaps list canonical URLs only.
