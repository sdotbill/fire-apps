# Portraits build log — photorealistic faculty headshots

Bill's order, Nov 16 2026 (02:21 EST): every professor's cartoon portrait
is replaced by a photorealistic AI-generated headshot, and the
"Voice: <name> (<accent>)" label comes off every page.

**Series style (identical for all 760):** photorealistic professional
university faculty portrait photograph, head and shoulders, facing the
camera, warm confident approachable expression, soft natural window
light, warm neutral beige studio background, shallow depth of field,
natural skin texture, 85mm lens, vertical portrait orientation.
Per-professor variation comes from the roster record itself: gender,
background group (the build-stageb.py name pools), the catalogue
portrait parameters (skin tone, hair colour and style, glasses, beard),
a deterministic age (35–62), and department-appropriate dress.

**Priority order:** Carmen Vega (Spanish flagship) → the 50 department
heads → the College ten faces → the rest, by department.

**Wiring:** files land in `portraits/<classId>.jpg`;
`wire-photos.py` points catalogue.json / roster.json / professors.json
`photo` fields at them. Professors without a landed portrait show a
plain initials monogram — the cartoon figure is never served again.
Voice data stays in the data files (lessons still speak); the printed
"Voice:" line is removed from the page.

## Batches

- **Wiring + voice-label removal** (commit 0c272910): `portraitSVG`
  deleted from index.html; the classroom card now renders the real
  photo when the professor's `photo` field is set, else an initials
  monogram. The `<div class="pvoice">Voice: …</div>` line is removed —
  grep confirms zero `Voice:` / `pvoice` / `portraitSVG` in index.html.
- **Batch 0 — Carmen Vega** (commit 885a4e94): 1/760.
  `portraits/espanol-i-speak-from-zero.jpg` (382 KB), wired into
  catalogue.json, roster.json and professors.json (she also heads
  Languages of the World).
- **Verification (headless Chromium, local serve):** Spanish classroom
  renders Carmen's photograph in the card, no SVG, 0 "Voice:" lines in
  the page text. A classroom whose portrait has not landed yet
  (Cosmology — Aurelia Voss) renders the plain "AV" monogram, no SVG,
  0 "Voice:" lines. Screenshots taken and eyeballed.
- Batches in flight: heads (49), college-a/b/c/d (232), rest-a…f (478).
- **Carmen Vega — flagship glamour spec** (Bill, Nov 16 02:30 EST):
  her portrait was regenerated to a spec that overrides the generic
  faculty spec for her alone — beautiful Spanish woman, warm and
  flirty energy, fitted deep-V neckline top in a rich warm tone,
  elegant and confident, same series lighting/background. The new
  file (426 KB) replaced the original at
  `portraits/espanol-i-speak-from-zero.jpg`; the glamour prompt is
  recorded on her manifest entry so any future regeneration keeps it.
