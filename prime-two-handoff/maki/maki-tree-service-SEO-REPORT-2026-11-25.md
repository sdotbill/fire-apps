# Technical SEO Report — Maki Tree Service (Davison, MI)
**Internal technical document — for Prime Two (SEO direction) and Prime One (implementation)**
**Prepared: November 25, 2026**

This is not a sales audit and not a growth audit. It is the technical record of where Maki Tree Service stands in search right now, what is wrong with the website and the local listings at a technical level, what the two competitors ahead of her are doing that she is not, and the exact ordered fix plan to get her to number one organically for tree removal and tree trimming in Lapeer and Genesee Counties. Organic only — no paid ads anywhere in this plan. No dates are promised — the plan is the work, not a deadline.

Baseline facts in this report build on the November 25, 2026 audit (`maki-tree-service-2026-11-25.md`). Everything new here was observed on November 25, 2026, from the live site, the live sitemap, and public search results. Every observation is dated. Anything that could not be verified from outside is marked **unverified** — it is not guessed.

## 1. The site as it stands

| Fact | Value | Observed |
|---|---|---|
| Domain | makitreeservice.com | Nov 25, 2026 |
| Domain registered | April 19, 2010 — 16 years old | Nov 25, 2026 (WHOIS via ipaddress.com) |
| WHOIS last updated | April 20, 2026 | Nov 25, 2026 |
| Hosting / platform | Ad Local SMB multisite template; images on CloudFront (`d14tal8bchn59o.cloudfront.net`, S3 `multisiteadmin-production`); "Designed by Ad Local" in the footer; a LOGIN link to `ad-local1.smblogin.com` on every page | Nov 25, 2026 |
| IPs | 3.33.251.168, 15.197.225.128 (AWS). No IPv6 | Nov 25, 2026 |
| HTTPS | Certificate detected; bare domain redirects to `https://www.makitreeservice.com` (www + https canonical) | Nov 25, 2026 |
| robots.txt | Exists. Contains one line only: `Sitemap: https://www.makitreeservice.com/sitemap.xml`. No disallow rules, no crawl-delay, no bot directives | Nov 25, 2026 |
| sitemap.xml | Exists. 6 URLs, no more | Nov 25, 2026 |
| Content pages | 4: Home, About Us, Our Services, Contact Us. Plus an HTML sitemap page and a thank-you page | Nov 25, 2026 |
| Blog / news / job gallery / FAQ page | None | Nov 25, 2026 |
| Last content change | Services pages June 3, 2024; contact page August 5, 2024; homepage lastmod December 29, 2025. No page updated in 2026 | Nov 25, 2026 (sitemap lastmod values) |
| Contact on site | 10047 East Richfield Road, Davison, MI 48423; Davison (810) 654-9494; Flint (810) 736-8200; Fax (810) 654-9616; info.MakiTree@gmail.com; free-estimate form | Nov 25, 2026 |

## 2. Sitemap and indexation

The XML sitemap (`https://www.makitreeservice.com/sitemap.xml`) lists exactly six URLs:

| URL | lastmod |
|---|---|
| `https://www.makitreeservice.com/` | 2025-12-29 |
| `https://www.makitreeservice.com/about-us` | 2024-06-03 |
| `https://www.makitreeservice.com/our-services` | 2024-06-03 |
| `https://www.makitreeservice.com/contact-us` | 2024-08-05 |
| `https://www.makitreeservice.com/sitemap` | 2024-06-18 |
| `https://www.makitreeservice.com/thank-you` | 2024-08-05 |

Defects:
- **Only six URLs.** There is no page for any single service and no page for any town except the homepage. Google cannot rank a page that does not exist.
- **Stale lastmod dates.** Four of the six URLs have not changed since June–August 2024. A sitemap that never changes tells Google there is nothing new to crawl.
- **No image sitemap, no video sitemap.** The site carries 15 images on the homepage and 12 on the services page; none are in any sitemap.
- **Indexation count unverified.** A `site:` operator search run on November 25, 2026 returned no results in the tool used — that is not proof of deindexation (the tool may not support the operator). The homepage, services page, sitemap page, and contact page all surface in normal web results, so the pages are indexed. The exact indexed count must be read from Google Search Console, which requires access Prime One does not yet hold. **Action for Prime Two:** get Search Console access in the access step (Section 8, Phase 0) and record the true indexed count before the rebuild.

## 3. Page-by-page technical findings

### 3.1 Homepage — `/`

- **Title:** "Residential and Commercial Tree Trimming, Removal & Pruning Davison MI - Maki's Tree Service." Targets Davison only. No Flint, no Lapeer.
- **Meta description:** "Maki's Tree Service provides professional residential and commercial tree trimming, removal, and pruning services in Davison, MI. Our certified arborists ensure quality and safety for all tree care needs." Davison only. Repeats the "certified arborists" claim — see the flag in 3.3.
- **H1:** "Professional Tree Services for Your Home or Business." No keyword, no location. A homepage H1 that says nothing about what the company does or where it does it.
- **H2s:** "Serving Genesee and Lapeer County" (good — the only location signal in a heading on the whole site), "Locally Owned & Operated • Licensed & Insured — Free Estimates", "Our Specialties", "Why Choose Us?", "Contact Us for a Free Estimate".
- **Services listed as H3s:** Tree Insurance Work, Tree Trimming, Stump Grinding, Tree Shaping and Pruning, Lot Clearing, Tree Storm Damage, Tree Pruning, Brush Chipping and Wood Chips, Shrub and Hedge Removal, Complete Cleanups, Year-Round Tree Contractor, Emergency Tree Service. Each gets one generic sentence. **There is no dedicated Tree Removal section on the homepage** — tree removal appears only in the intro sentence. Tree removal is the highest-value search term in this market.
- **Testimonials:** three, with names (Theresa Platz, Caralyn Zalewski, Greg Kozma). Good content, but static — undated and unchanged since the pages were built.
- **Images:** 15, all on CloudFront with generic filenames (`tree-pruning-3`, `stump-grinding-2`, `2022-09-02`, `20240410_155150`, `img_0461`). Alt text is the filename only. No image carries a descriptive or keyword-bearing alt attribute.
- **Internal links:** navigation only (Home / About Us / Our Services / Contact Us). No links from the homepage to any service or location page, because none exist.
- **Footer:** the "About Our Company" blurb and full NAP repeat identically on every page (duplicate boilerplate).

### 3.2 Our Services — `/our-services`

- **Title:** "Emergency Tree Trimming, Removal, Pruning & more Davison MI | Maki's Tree Service." Keyword-stuffed, reads like a tag cloud, Davison only.
- **Meta description: unverified from the rendered text** — not surfaced in the fetch. Must be read from page source in Phase 0.
- **H1:** "Our Services." No keyword, no location.
- **H2s (one per service):** Tree Trimming, Tree Shaping and Pruning, Stump Grinding, Land and Lot Clearing, Tree Storm Damage, Tree Insurance Work, Commercial Tree Trimmers, Brush Chipping and Wood Chips, Shrub and Hedge Removal, Complete Cleanups, Year-Round Contractor, Emergency Tree Service.
- **Critical gap: there is no Tree Removal section on the services page.** The page that should be the company's service hub does not cover its number-one service at all. A Flint homeowner searching "tree removal Flint MI" has no Maki page to land on — and neither does Google.
- **Body copy:** generic template text. No mention of Flint or Lapeer anywhere in the body. No prices, no service-area detail, no town names, no "what it costs" or "how long it takes" content. Every paragraph ends with a variant of "Trust Maki's Tree Service…".
- **Images:** 12, same generic-filename problem as the homepage.

### 3.3 About Us — `/about-us`

- **Title:** "About Maki's Tree Service | Certified Arborist - Davison MI."
- **H1:** "About Us." Generic.
- **Body:** generic template copy. No founding year (the company dates to 1997 per BBB/Yelp), no names (Mark, Pam, Brent), no crew information, no equipment, no service-area detail beyond Davison.
- **FLAG — unverified claim:** the title and the homepage meta description both claim "certified arborist(s)". No arborist is named anywhere on the site, and no ISA credential number appears on any page. If no one on staff holds an ISA Certified Arborist credential, the claim is a liability. **Prime Two to confirm or remove before the rebuild.** Do not carry the claim into new pages until it is verified.

### 3.4 Contact Us — `/contact-us`

- **Title:** "Contact - Maki's Tree Service | Emergency Tree Service Davison MI."
- **H1:** same text as the title. The "Emergency Tree Service Davison MI" phrase is duplicated across the services-page title and this title.
- **Body:** one short intro paragraph, address, both phone numbers, fax, email, and the estimate form. No map embed in the rendered text (a Google Maps link with CID 4705703888118788425 is present in the footer). No hours on this page in the rendered text — hours appear on the HTML sitemap page instead.

### 3.5 HTML sitemap page — `/sitemap`

- Title: "Sitemap | Emergency Tree Service Davison MI" — the "Emergency Tree Service Davison MI" phrase a third time.
- Lists the four content pages. Carries the business hours: Mon–Thu 6am–7pm, Friday 6am–9pm, Saturday 9am–5pm, Sunday Closed. **This is the website's own hours statement — and it disagrees with Google and with Yelp (Section 5).**
- Footer: "Copyright ©2026 Maki's Tree Services LLC. All Rights Reserved. Designed by Ad Local."

### 3.6 Schema markup

- **No LocalBusiness / JSON-LD schema was detected in the rendered page text fetched November 25, 2026.** Rendered-text extraction strips scripts, so this is not proof of absence — it must be confirmed by reading the page source in Phase 0. If schema is absent (likely, given the template), the rebuild adds it: LocalBusiness with name, address, geo coordinates, phone, hours, service area, and sameAs links to the GBP, Facebook, Yelp, and BBB profiles.

### 3.7 Speed, mobile, and other technical items — unverified

- **Page speed / Core Web Vitals: not verified.** The PageSpeed Insights API returned HTTP 429 on November 25, 2026; the request was not retried. Must be measured with a live test in Phase 0. Note for the rebuild: images are served from CloudFront (a CDN — good), but they are served at full size with generic filenames and no modern format evidence in the URLs.
- **Mobile-friendliness: not verified with a live test.** The Ad Local template is responsive by design. Must be tested on a real phone in Phase 0.
- **No IPv6** (IPs are IPv4 only). Minor; not a ranking factor worth chasing first.
- **Email is a Gmail address** (info.MakiTree@gmail.com), not a domain address. Minor professionalism and consistency note for the rebuild — a `contact@makitreeservice.com` address would match the domain.

## 4. On-page and content gaps — the missing pages

Google ranks pages, not companies. These are the pages that do not exist and need to:

| Missing page | Why it matters |
|---|---|
| Tree removal (dedicated service page) | The highest-value service in the market has no page anywhere on the site |
| Tree removal — Flint | Money term for the biggest market; J&M has `/tree-removal-and-trimming` |
| Tree removal — Lapeer | Money term for the second county; JDM's homepage targets it |
| Tree trimming — Flint | Maki is not in the top 15 for this term |
| Tree trimming — Lapeer | Same gap, second county |
| Stump grinding (dedicated) | Service exists in the H3 list only; J&M has `/stump-grinding` |
| Stump grinding — Flint / Lapeer | No page targets these terms at all |
| Emergency tree service (dedicated) | Exists as one H3 block; J&M has `/emergency-tree-removal` |
| Tree service — Flint | No Flint page of any kind exists |
| Tree service — Lapeer | No Lapeer page of any kind exists |
| Town pages: Burton, Grand Blanc, Clio, Mt. Morris, Fenton, Holly | Towns inside the two counties where Maki already works; zero pages |
| FAQ page | No page answers real customer questions (cost, timing, insurance, permits) |
| Job gallery / recent work | No dated, located job photos anywhere on the site |

What the current pages target versus what they should target: every title and meta on the site targets **Davison only**. Davison is the smallest of the three markets and the one where Maki already ranks first. Flint (county seat, biggest pool of customers) and Lapeer (second county) appear in exactly one H2 on the homepage ("Serving Genesee and Lapeer County") and nowhere in any title, meta description, H1, or body copy.

## 5. Local SEO — Google Business Profile and NAP

### 5.1 Google Business Profile (observed November 25, 2026)

| Field | Value |
|---|---|
| Business name | Maki Tree Service |
| Place ID | 1125534058391550 |
| Address | 10047 E Richfield Rd, Davison, MI 48423 |
| Coordinates | 43.063861, -83.515653 |
| Primary category | Tree Cutting Service |
| Secondary category | Landscape Company |
| Phone on GBP | +1 (810) 736-8200 (the Flint number only) |
| Website link on GBP | `https://www.makitreeservice.com/about-us` — **points to the About page, not the homepage. Defect: fix to the homepage.** |
| Hours on GBP | 9:00 AM–5:00 PM every day, including Sunday |
| GBP description | "Maki Tree Service \|\| Flint Michigan \|\| Specializes in Tree Removal, Plant Health Care, Tree Trimming, Tree Pruning, Stump Grinding, Tree Shaping and Fine Pruning, Land and Lot Clearing, Brush Chipping & Woodchips, Shrub and Hedge Removal, Complete Cleanups, Year-Round Tree contractor, Emergency Tre…" (truncated in source) |
| Map CID | 4705703888118788425 |
| Reviews | 4.7 stars, 53 reviews (Birdeye snapshot, Nov 25, 2026). Prime Two's snapshot the same day showed 59 — the two aggregators disagree; Google's own live count is the authority and must be read from the GBP in Phase 0. |
| Review velocity | Zero new Google reviews since the October 3, 2026 audit (53 then, 53 now) |
| Owner replies | The owner has replied to at least one review (to "Patricia", 9 months ago: "Thank you Patricia. We appreciate the opportunity to work with you!"). The negative price/veterans-discount review has **no owner reply visible**. |
| GBP photos, posts, Q&A | **Unverified from outside** — photo count, post history, and Q&A cannot be read without GBP manager access. Must be inventoried in Phase 0 once access is in hand. |

### 5.2 The negative review (verbatim, from Birdeye, November 25, 2026)

> "Came out within 2 days of reaching out to do a quote but gave us a quote over $1,000 more than other companies for one tree. When I asked about a veterans discount, I was dismissed. Based on the interaction and price, we went with a different company."

No owner reply is visible. Positive reviews name crew lead Brent/Brentt repeatedly ("Brent and his crew are very professional", "Brentt provided a fair and competitive quote"). The former-employee bad review Bill mentioned was **not located** in the November 25 checks — it may sit on another platform or may already be gone. Do not assert it exists on Google; a live GBP read in Phase 0 settles it. If it violates Google's policies it can be reported; otherwise the remedy is a factual owner response plus legitimate review generation — it cannot be promised away.

### 5.3 NAP consistency — three different hours, two phone presentations

| Source | Hours | Phone shown |
|---|---|---|
| Google Business Profile | 9:00 AM–5:00 PM every day, incl. Sunday | (810) 736-8200 |
| Website (sitemap page) | Mon–Thu 6am–7pm; Fri 6am–9pm; Sat 9am–5pm; Sun Closed | (810) 654-9494 + (810) 736-8200 |
| Yelp / Birdeye | Mon–Sat 8:00 AM–5:00 PM; Sun closed | (810) 736-8200 |

Address is consistent everywhere (10047 E Richfield Rd, Davison, MI 48423). The hours conflict is the same one the October 3, 2026 audit flagged — still unfixed. A homeowner with a storm-damaged tree on a Sunday morning gets three different answers depending on where they look.

One further flag: BestProsInTown shows (810) 240-5336 in one Maki listing. That number is **unverified** — it may be a data error on their side or an old number. Do not assert it is hers; verify it in Phase 0 and correct the listing if it is wrong.

### 5.4 Citations observed (November 25, 2026)

Google, Yelp (claimed, 27 photos, 0 reviews), Birdeye (profile **unclaimed**), BestProsInTown (5.0, 20 reviews — a separate review set), MapQuest, CitySquares (0 reviews), Yellow Pages (2 photos in gallery), Yardbook (**unclaimed**), Contractors Junction, ClaimPages, DLM Property Group (Flint directory — Maki listed among 60 tree services serving Flint), NeverBounce, LinkedIn (per NeverBounce — unverified). No Instagram account for the business. Facebook business page "Maki tree service", 26 followers, last post April 3, 2026 (crew video) — dormant 7+ months. Business posts instead appear on owner Pamela Maki's personal profile (last August 24, 2026, 1–2 likes each).

## 6. Competitor technical teardown

### 6.1 J&M Tree Service — Flint #1 (jmtreeservice.com, Duda platform)

- **Title:** "Tree & Lawn Services – Flint, MI – J&M Tree Service." Flint in the title.
- **H1/H2:** "TREE REMOVAL, TREE TRIMMING AND STUMP GRINDING SOLUTIONS IN FLINT, MI." Keywords + Flint in the main heading — the exact thing Maki's pages do not do.
- **Sitemap: 7 URLs** — homepage plus dedicated pages: `/tree-removal-and-trimming`, `/stump-grinding`, `/emergency-tree-removal`, `/lawn-maintenance`, `/tree-removal-quotes`, `/tree-removal-photos`. Dedicated service pages are the structural edge.
- **Location:** Flint-based (4618 Milton Dr, Flint, MI 48507; also listed at 2424 Concord St, Flint, MI 48504). Since 1989. Founded by Mike Spitzer.
- **Phone:** (810) 238-3234. Hours: Mon–Fri 8–5, Sat–Sun 24-hour emergency.
- **Reviews:** Birdeye 4.0 / 54; Location.com 4.2 / 43; Yellow Pages 4.62 / 21; IndustryOversight 5.0 / 5. **Key point: J&M's Google review count (54) is essentially equal to Maki's (53).** J&M wins Flint on Flint location plus Flint-targeted pages — not on review volume. Maki is not behind on reviews against the Flint leader.
- **Social:** Facebook active (promotional post August 31, 2026).
- **Weaknesses to exploit:** single-page-per-service depth is thin; review rating (4.0–4.2) is below Maki's 4.7; no Lapeer presence; the site is a basic Duda template with stock imagery.

### 6.2 JDM Tree & Site Services LLC — Lapeer #1 (jdmsiteservices.com, Wix)

- **Title:** "TREE & STUMP REMOVAL | JDM Site Services | Lapeer, MI." Keyword + Lapeer in the title.
- **H2:** "Serving Lapeer, Oakland, Macomb, Genesee, St. Clair, and Sanilac Counties." Service area in a heading.
- **Location:** 1990 Smith Rd, Lapeer, MI 48446. Phone (248) 764-3956. 20+ years, family-owned.
- **Reviews: 161 Google reviews, 4.9 stars — three times Maki's count.** The most-reviewed general contractor in Lapeer County by Google review count. This is the real gap in Lapeer: review volume, not just pages.
- **Trust signals on the homepage:** named testimonials (Scott G., K Slater, Trevor E.), "Fully Insured", BBB, free estimates, 24/7 emergency, **senior & military discounts** — directly relevant, because Maki's one visible negative review is about a dismissed veterans discount.
- **Sitemap:** Wix `pages-sitemap.xml`. The site is effectively a single long homepage — no dedicated service subpages were observed. JDM wins Lapeer on Lapeer location + 161 reviews + a keyword-rich title, not on site depth. A rebuilt Maki site with real service and location pages can out-structure JDM.
- **Hours:** Mon–Fri 9–5, Sat–Sun closed, emergency available.

### 6.3 The rest of the field (November 25, 2026)

- **Flint:** Above All Tree Services and Hauling (5.0, 86 reviews), The Tree Guy, Clio (4.8, 166 reviews), All Seasons Tree & Lawn Care, Davison (4.8, 73 reviews — appears for "tree trimming Flint").
- **Lapeer:** Legend Tree Service LLC (4.9, 147 reviews) is #2 behind JDM.
- **What this means:** Flint is winnable on relevance alone — the leader has no review advantage. Lapeer is a two-front fight: relevance (pages) plus review volume (161 vs 53). Both are fixable with the plan in Section 8.

## 7. Keyword and ranking table

Positions verified November 25, 2026 (baseline audit checks). "Not in top 10" means the business did not appear in the top 10 results in the searches run that day.

| Search term | Maki's position | Who is first |
|---|---|---|
| tree service Davison MI | 1st | Maki Tree Service |
| tree removal Davison MI | 1st | Maki Tree Service |
| tree service Flint MI | Not in top 10 | J&M Tree Service (Flint) |
| tree removal Flint MI | Not in top results | J&M Tree Service / Absolute Tree Removal (Flint) |
| tree service Lapeer MI | Not in top 5 | JDM Tree & Site Services LLC (Lapeer, 4.9, 161 reviews) |
| tree removal Lapeer MI | Not in results | JDM Tree & Site Services LLC / Legend Tree Service LLC (Lapeer, 4.9, 147 reviews) |
| tree trimming Flint MI | Not in top 15 list checked | All Seasons Tree & Lawn Care (Davison, 4.8, 73 reviews) appears; Maki does not |
| tree trimming Lapeer MI | **Unverified** — not checked Nov 25 | — |
| stump grinding Flint MI | **Unverified** — not checked Nov 25 | — |
| stump grinding Lapeer MI | **Unverified** — not checked Nov 25 | — |
| tree service Genesee County MI | **Unverified** — not checked Nov 25 | — |
| tree removal Genesee County MI | **Unverified** — not checked Nov 25 | — |

**The #2 discrepancy, stated plainly.** Bill reports that when he searches "tree service in Flint" she comes up second organically. The November 25 independent checks did not show her in the top 10 for Flint terms. Both can be true: rankings vary by the searcher's location (Bill searches from Davison), by whether the results show the map pack or the web results, and by the exact query wording. The honest baseline is: she ranks first in Davison, she does not rank in the top 10 for Flint or Lapeer terms in outside checks, and a live check from a Flint location will pin the exact position down. The fix plan does not depend on resolving the discrepancy — the work is the same either way.

## 8. The fix plan — ordered, technical, organic only

No paid ads anywhere. No dates promised. Prime Two directs each phase; Prime One builds what Prime Two specs. Nothing goes live until Prime Two reviews it and the owner approves it.

### Phase 0 — Access and true baseline (before any build)

Prime Two directs; Prime One executes.
1. **Domain and hosting control.** The site sits on Ad Local's platform ("Designed by Ad Local", login at `ad-local1.smblogin.com`). Determine who holds the Ad Local login and who controls the domain's DNS. The rebuild either happens inside Ad Local (if the platform allows the new page structure) or on a new host with DNS pointed at it. Do not start building until this is answered — it decides the whole build route. **Keep the domain.** It is 16 years old (registered April 19, 2010); do not change domains.
2. **Google Business Profile manager access.** Get manager access from Pam. Inventory inside the GBP: photo count, post history, Q&A, the live review count (resolving the 53 vs 59 aggregator disagreement), and whether the former-employee review exists.
3. **Google Search Console + Analytics.** Get access or set up. Record the true indexed page count, the queries already bringing impressions/clicks, and the pages Google already ranks (the Davison terms).
4. **Live rank check from Flint.** Run the keyword table from a Flint location (map pack and web results separately) to pin the exact starting positions.
5. **Page-speed and mobile test.** Run PageSpeed Insights (mobile + desktop) and a real-phone mobile check. Record Core Web Vitals before the rebuild so the after-state can be compared.
6. **Page-source check.** Read the source of all four pages: confirm schema presence/absence, confirm meta descriptions, check for noindex/nofollow tags, check canonical tags, check for render-blocking resources.
7. **Verify or remove the "Certified Arborist" claim.** Name the credential holder and number, or strip the claim from every title and meta before the rebuild.
8. **Verify the (810) 240-5336 listing** on BestProsInTown. Correct it if it is wrong.

### Phase 1 — GBP and NAP fixes (fastest wins, do first)

1. **One true hours set.** Agree the real hours with Pam, then make them identical on Google, the website, Yelp, and Birdeye. Fix the three-way conflict in Section 5.3.
2. **GBP website link → homepage.** Change from `/about-us` to `https://www.makitreeservice.com/`.
3. **GBP categories and description.** Review the categories (primary Tree Cutting Service, secondary Landscape Company) and rewrite the description in plain language with the real services and the real service area (Genesee and Lapeer Counties). Add service-area towns in the GBP service-area setting.
4. **Reply to the negative review.** A factual, professional owner reply to the price/veterans-discount review. No defensiveness, no argument — acknowledge, state the position plainly, invite contact.
5. **Claim the unclaimed profiles.** Birdeye and Yardbook. Correct NAP on both.
6. **Review generation habit.** After every finished job, a text to the customer with a direct link to leave a Google review. This is the only durable way to close the 53-vs-161 gap in Lapeer.
7. **GBP photos.** Add current job photos (before/during/after) with real file names and captions. Inventory what is already there in Phase 0 first.

### Phase 2 — New site architecture (the rebuild)

Build on the existing domain. URL pattern: short, keyword-first, location-last (e.g. `/tree-removal-flint-mi/`). Keep the four existing URLs alive or 301-redirect them if the structure changes — never let an old URL 404.

**Core pages (keep/rebuild):**
- `/` — Homepage. Targets "tree service Davison MI" + brand. New H1 with service + location.
- `/about-us` — About. Real history (since 1997), real names, real crew, real equipment. Remove the arborist claim unless verified.
- `/contact-us` — Contact. Form, both phones, address, map embed, hours (the one true set).
- `/our-services` — Services hub. Links out to every dedicated service page.

**Dedicated service pages (new):**
- `/tree-removal/` — the missing money page.
- `/tree-trimming/`
- `/stump-grinding/`
- `/emergency-tree-service/`
- `/lot-clearing/`
- `/storm-damage/`
- `/tree-insurance-work/`

**Location pages (new):**
- `/tree-service-flint-mi/` — Flint hub.
- `/tree-service-lapeer-mi/` — Lapeer hub.
- `/tree-service-davison-mi/` — Davison (homepage already covers this; a dedicated page is optional — Prime Two's call).
- Town pages: Burton, Grand Blanc, Clio, Mt. Morris, Fenton, Holly.

**Service × location pages (new — the money pages):**
- `/tree-removal-flint-mi/`, `/tree-removal-lapeer-mi/`
- `/tree-trimming-flint-mi/`, `/tree-trimming-lapeer-mi/`
- `/stump-grinding-flint-mi/`, `/stump-grinding-lapeer-mi/`

**Supporting pages (new):**
- `/faq/` — real customer questions: cost, timing, insurance, permits, what happens to the wood, stump grinding depth.
- `/recent-work/` — dated job galleries with town names and service names in the page text, image filenames, and alt text.

Total new pages: roughly 20. Every one gets a unique title (service + town), a unique meta description, one H1 (service + town), and body copy that names the town and the service in plain language.

### Phase 3 — Technical implementation (with the rebuild)

1. **XML sitemap regenerated** with every new URL, submitted in Search Console. Image sitemap added.
2. **robots.txt kept** with the sitemap reference. No disallow rules needed.
3. **LocalBusiness JSON-LD schema** on every page: name, address, geo, phone, hours (one true set), service area (Genesee + Lapeer Counties + named towns), sameAs links (GBP, Facebook, Yelp, BBB).
4. **Titles, metas, H1s rewritten per page** — unique, keyword + location, no stuffing, no duplicated title phrases across pages.
5. **Image discipline:** real job photos; filenames with service + town (`tree-removal-flint-before.jpg`); descriptive alt text on every image; compressed, served from the same host/CDN.
6. **Internal linking:** every service page links to its Flint and Lapeer versions; every location page links to its service pages; homepage links to the Flint and Lapeer hubs; footer NAP kept identical on every page.
7. **301 redirects** for any URL that moves. Old URLs (`/`, `/about-us`, `/our-services`, `/contact-us`) are preserved or redirected — never 404.
8. **HTTPS maintained** throughout. Mobile tested on a real phone. Page speed re-measured after launch and compared to the Phase 0 baseline.

### Phase 4 — Content (with the rebuild)

1. Real job photos with town and service in the filename, alt text, and caption.
2. Testimonials with customer names **and towns** (the three existing ones name no town — add town names to new ones).
3. Service-area content that names the towns Maki actually works in, in plain language.
4. FAQ content written from real customer questions, not template filler.
5. Emergency page with the real response story (24/7 framing only if true — verify with Pam).

### Phase 5 — Reviews, citations, and social (ongoing, starts in Phase 1)

1. Review text after every job (Phase 1 habit, continued).
2. Reply to every review, starting with the negative one.
3. Citation cleanup: identical NAP (one hours set, both phone numbers presented the same way) across Google, Yelp, Birdeye, BestProsInTown, MapQuest, CitySquares, Yellow Pages, Yardbook.
4. Facebook business page revived: crew phone photos after each job (before/during/after) posted to the **business** page, not the owner's personal profile.
5. Instagram account created for the business, same job-photo habit.

### Phase 6 — Measurement (proves it worked)

1. **Rank tracking** for every term in the Section 7 table — map pack and web results separately, checked from Flint and Lapeer locations, not just Davison.
2. **Search Console:** indexation count, queries, clicks, and average position, checked weekly after launch.
3. **GBP insights:** calls, direction requests, website clicks.
4. **Call tracking:** the two phone numbers on the site stay as they are (customers already know them); count inbound calls by source where possible.
5. **Report real position and lead outcomes** — no promised rank, no promised call volume. The numbers are what they are, reported honestly.

### Division of work

| Work | Who |
|---|---|
| SEO strategy, keyword targets, page list, GBP strategy, review strategy, citation strategy, QA of every page before it goes live | Prime Two directs |
| Site rebuild, schema, sitemap, redirects, content implementation, image work, Search Console and Analytics setup | Prime One builds |
| Access (Ad Local login, DNS, GBP manager, Search Console) | Pam supplies; Bill coordinates if needed — Prime Two does not route through Bill for routine items |
| Final go-live | Prime Two reviews the complete candidate; owner approves |

## 9. Top technical defects — summary

1. **No page for tree removal** — the highest-value service has no dedicated page, and the services page does not even have a tree-removal section.
2. **No Flint page and no Lapeer page** — every title and meta targets Davison only; the two bigger markets have zero pages.
3. **Four content pages, untouched since 2024** — a six-URL sitemap with stale lastmod dates.
4. **H1s say nothing** — "Professional Tree Services for Your Home or Business", "Our Services", "About Us". No keyword, no location, on any page.
5. **GBP website link points to /about-us**, not the homepage.
6. **Hours disagree three ways** (Google 9–5 daily; website 6am–7pm weekdays, Sun closed; Yelp/Birdeye 8–5 Mon–Sat).
7. **No schema detected** in rendered page text (confirm in source, Phase 0).
8. **No review generation** — zero new Google reviews since October 3, 2026; the one negative review is unanswered.
9. **Images with generic filenames and filename-only alt text** on every page.
10. **"Certified Arborist" claimed in the title and meta with no credential named anywhere** — verify or remove.
11. **Page speed and mobile-friendliness untested** (PSI returned 429 on Nov 25, 2026) — measure in Phase 0.
12. **No blog, no FAQ, no job gallery, no dated content of any kind** — nothing for Google to see as fresh.

## 10. Sources and verification notes

- Live fetches of `makitreeservice.com` (homepage, `/our-services`, `/about-us`, `/contact-us`, `/sitemap`), `robots.txt`, and `sitemap.xml` — November 25, 2026.
- Live fetches of `jmtreeservice.com` (homepage, `sitemap.xml`) and `jdmsiteservices.com` (homepage, `sitemap.xml`) — November 25, 2026.
- Search results for Maki Tree Service, J&M Tree Service, and JDM Tree & Site Services (Google, Birdeye, BestProsInTown, Yelp, Yellow Pages, IndustryOversight, MapQuest, CitySquares, Yardbook) — November 25, 2026.
- Domain and hosting facts via ipaddress.com (WHOIS, DNS, HTTPS) — November 25, 2026.
- Baseline rankings and review counts from `maki-tree-service-2026-11-25.md` (November 25, 2026 audit).
- Items marked **unverified** in this report: exact indexed page count; schema presence in page source; services-page meta description; GBP photo count, post history, and Q&A; the (810) 240-5336 listing; the "Certified Arborist" credential; the former-employee review's location; page speed / Core Web Vitals; mobile-friendliness live test; stump-grinding and Genesee County term rankings. All are assigned to Phase 0, not guessed.

*— Technical SEO Report, Maki Tree Service. Internal document for Prime Two and Prime One. November 25, 2026.*
