# Cloudflare Bulk Redirect lists — ready to upload, NOT yet uploaded.
#
# These two CSVs are the off-host 301s from change-list section 1.5.
# They are NOT live until they are uploaded in the Cloudflare dashboard
# (or via the Cloudflare API with a token for the zone):
#
#   offhost-to-pms.csv  -> upload to the daveexolex.com zone, list name
#                          "offhost-to-pms", rule: if hostname is
#                          daveexolex.com, run this list. (Dave is already
#                          on Cloudflare, so this one can go live first.)
#   offhost-to-dave.csv -> upload to the premiummarketingsolutionsllc.com
#                          zone, list name "offhost-to-dave". BLOCKED until
#                          the PMS domain is put behind Cloudflare (Step B
#                          in section 1.5: add the domain to the same
#                          Cloudflare account, then point DNS at it).
#                          Do NOT upload this one until that is done.
#
# Do NOT delete the meta-refresh stub pages until the corresponding
# Cloudflare 301s are confirmed live (section 5): deleting a stub before
# its 301 fires would 404 the URL instead of 301ing it.
#
# Coverage: offhost-to-dave.csv covers every top-level Dave path in the
# publish manifest (dist-dave/sitemap-dave.xml) plus the stub paths that
# are not in any sitemap (/dave/, /dave-door/, /what-is-an-exolex/,
# /first-exolex/, /blueprints/, /origin/, /john-titor/, /run-it-back/,
# /time-traveler-evidence/, /ufo-evidence/, /lab/). /notebook/ is NOT
# in offhost-to-dave.csv: it is assigned to PMS (its canonical is the
# PMS host; the Dave notebook lives at /dave-notebook/).
# offhost-to-pms.csv lists the desk-ledger /record/ URLs individually
# (never a /record prefix) so /record-in-numbers/ stays on Dave.
#
# Same-host retired URLs live in _redirects (the platform-layer record)
# and must ALSO be added as Cloudflare 301s on the owning host
# (section 1.5, "Same-host retired URLs"). _redirects is the list, not
# the mechanism — GitHub Pages ignores it.
