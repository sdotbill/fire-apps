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

- Wiring + voice-label removal committed first: cartoon retired
  site-wide, monogram fallback live, "Voice:" line gone.
