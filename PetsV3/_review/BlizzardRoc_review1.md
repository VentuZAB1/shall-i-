# Blizzard Roc - model gate review 1 (2026-10-27) - APPROVED WITH FIXES (model)

**Score: 7/10 for a 7.4 % HIGH flyer** (ship target about 8). The build is clean and distinct. It does not yet have the
presence it needs against the Yeti (14 %) and the Mammoth (26 %). Six small, code-level MUSTs fix that, and they are
all in `pets/BlizzardRoc.py`. Apply them, then send the round-2 renders in section 7 for a short check before the
clips start. No new full gate is needed.

What I looked at (`pets/BlizzardRoc.py`, `BlizzardRoc/MODEL_NOTES.md`, the plan v2, the plan review section 2.4, the
owner decisions, `Creature Style`, `Model Review Checklist`, `FIERCE_GUIDE`):
- `renders/_model_sheet.png` (bind pose), `_close_sheet.png` (face and crest), `_idle_sheet.png` (ground fold),
  `model_game.png`, `idle_game.png`
- `_icons_strip_64.png` and `_icons_strip_128.png` (Roc, Lynx, Mammoth, Yeti, Frostcrown, Thunderbird, Griffin, Phoenix)
- `flat_side.png`, `flat_tq.png`, `flat_game.png`, with my own pixel count (section 2)
- comparison sheets: `Thunderbird/renders/_model_sheet.png`, `GlacierYeti/renders/_model_sheet.png`,
  `IceMammoth/renders/_model_sheet.png`, `_ALL_FIERCE_progress.png`
- not used: `renders/_pose_sheet.png` (written 14:01, before the 14:26 build, so stale; the clip gate comes later)

---------------------------------------------------------------------------------------------------------------------
## 0. Numbers and the deviation log

- Tris 12,284: PASS (cap 15k, plan 9-13k).
- HEIGHT 9.0 studs to the crest tip (model top 1.996 BU; 1 BU = 4.5 studs, 1 % H = 0.02 BU): PASS.
- **Span 3.78 BU = 1.89 H in the bind pose. FAIL.** The plan sets 2.0-2.4 H, and the span is the Roc's named
  signature ("the span and the crest carry it"). MODEL_NOTES says "open flight span ~2.1 H", but no open-flight
  render or measurement is in the folder. The bind-pose figure is the one players see, and it is short. The shortfall
  is not logged as a deviation.
- Value shares, mine against the builder's table (figure pixels, nearest palette colour, ±1 %):

| colour | plan side | side (mine) | tq (mine) | game (mine) | builder game |
|---|---|---|---|---|---|
| SNOW | 36 | 20.1 | 35.6 | **10.9** | 10.7 |
| STORM_GREY | 25 | 28.8 | 21.7 | **47.7** | 46.9 |
| CHAR | 16 | **36.7** | **25.9** | **28.0** | 27.6 |
| PALE_G | 6 | 2.1 | 4.9 | 1.5 | 1.4 |
| FROST_V | 5 | 7.8 | 5.0 | 7.8 | 7.6 |
| BEAK / BLACK | 3 / 3 | 2.9 / 1.4 | 4.7 / 1.8 | 2.3 / 1.7 | 2.2 / 3.4 |

  The builder's numbers hold (within about 1 point). The problems are CHAR (about double its plan share in every view,
  driven by the folded wing's primaries and the coverts' bars), the game-view white (11 %), and PALE_G (under target).

Deviations (accept only if better):
| # | builder's deviation | verdict |
|---|---|---|
| D1 | Wing root out 0.05 (collision-free folds, 0/54 to 36/54) | ACCEPT. It is a collision fix, not a look change. |
| D2 | Crest plumes 0.12-0.15 H (plan 0.10 H), because 0.10 H vanished at 64 px | ACCEPT the length. The plumes still need width (MUST 3). |
| D3 | FROST_H hot spot in the eye | ACCEPT. FIERCE guide asks for a "small hot centre". |
| D4 | CHAR barred tips on the mantle shingles (the back was a flat slab without them) | ACCEPT. It breaks up the grey and avoids the "grey plastic" rejection. |
| D5 | Placeholder idle held at the fold | n/a (replaced at the clip gate). |
| - | Span 1.89 H (below the plan's 2.0 floor) | **NOT DECLARED. REJECT as built.** MUST 1. |

---------------------------------------------------------------------------------------------------------------------
## 1. The lead's three questions

**Q1: Does it read as a recoloured Thunderbird? NO.**
- At icon size the Thunderbird is a teal and gold bird with a white head and a big white fan tail. The Roc has none of
  that: no fan (four feathers), no teal, no gold, and a storm-grey back with a charcoal mask and violet tips. At
  128 px the two are clearly different birds.
- What they share is the wing-biped build: raised three-row wings, a white head, a hook beak. That is the kit, not a
  copy. It is a family resemblance, and it is fine.
- One caution: the Thunderbird's tip pattern is yellow bolts on coverts and primaries. If the Roc's new violet covert
  bars (MUST 2) are zig-zagged, they will echo that pattern. Keep them straight, one bar each (section 3).

**Q2: Does it read as a PLAIN white bird? PARTLY, and only from the front.**
- From the front or the icon angle (tq) it is white-dominant (36 %), but the dark wing and the violet tips stop it from
  being plain. At 64 px it reads as a white bird with dark wings. That is good.
- From behind (the game camera) it is NOT white. It is grey and charcoal: STORM 48 %, CHAR 28 %, SNOW only 11 %. The
  snowy read is lost exactly where the player sees the pet most. The flat game view shows a grey slab with a dark
  wing, and the only white is the crest's bases.
- The fix is to put white where the game camera looks (the nape collar, the crest) and to put violet on the wing bars,
  not to make the body whiter. See MUST 2 and MUST 5.

**Q3: Can it beat the Yeti (14 %) and the Mammoth (26 %) in presence? Not on colour. Only on silhouette.**
- The Yeti is saturated navy with white shoulder plates. The Mammoth is saturated teal with a dark spine ridge and white
  tusks. Both are bulky. In the lineup the Roc will be the palest bird in its egg.
- The Roc must win on silhouette: the span (MUST 1 takes it from 1.9 H to 2.0 H), the erect crest read as violet-tipped
  points (MUST 3), and the dark wing mass against the white front. Do not add saturated blue or teal to chase colour.
  That would copy the Yeti and the Mammoth, and it would break the Glacier hue spread (plan section 5).
- Caution for the map: the Glacier floor is probably ice or snow-pale. A white front has little contrast on that. The
  dark primaries, the CHAR mask and the grey back are what separate the Roc from the floor. Do not lighten them. Check
  the Roc on the Studio Glacier floor at the clip gate.

---------------------------------------------------------------------------------------------------------------------
## 2. Checklist, item by item (player's eye, ~5 studs, FOV 70, phone size)

1. **64 px silhouette - PASS.** A bird with a big spread and an upright crest. The species reads instantly. It is not a
   lion, a dragon or a Thunderbird.
2. **Game camera - PARTIAL.** The back is the largest zone and it is grey. It has studded shingles, so it is not a
   plastic slab. But there is almost no white (11 %), and the crest is thin. (MUST 3, MUST 5.)
3. **Fierce, not cute - PASS.** Narrow slit eyes, a steel hook beak, no smile, no round eye, no glint.
4. **The face reads - PARTIAL.** The CHAR plates (`pets/BlizzardRoc.py` L289-293) and the brow (L299-300) are boxes
   around each eye. From the front they fuse into a visor or goggles. The osprey stripe is the good part. (MUST 4.)
5. **Palette follows the plan - FAIL.** CHAR is 26-37 % against 16. PALE_G is 1.5-4.9 % against 6. Violet is 5-8 % and
   fine. (MUST 2; NICE 2.)
6. **Accent in game colours - PARTIAL.** The violet is on the primary tips and the crest, but from behind it is almost
   only the wing tips. (MUST 2, MUST 3.)
7. **Distinct from Thunderbird and Griffin - PASS.** See Q1.
8. **Body brightest channel >= 170 - PASS.** SNOW 250, STORM_GREY 186. CHAR is a dark accent, which is allowed.
9. **Stud skin, no box belly - PASS.** Breast keel, tapered belly and chevron breast bars. No Neon, no glow meshes.
10. **Tris and rig - PASS.** 12,284 tris, the Thunderbird wing-biped rig with the FX anchors.
11. **Span and proportion - FAIL.** 1.89 H against 2.0-2.4 H. (MUST 1.)
12. **Tail reads as a fan of four - PARTIAL.** The four feathers are 0.15 BU wide with a 0.30 taper (L368). In the bind
    pose they read as thin rods, not a fan. (MUST 6.)
13. **Floating, poking or intersecting parts - PASS (bind and fold).** Nothing floats in the bind or fold renders.
    Collisions are not measured yet (the clip gate runs `collision_free`).
14. **Parts visible from below - NOT CHECKED.** No under-view render is in the folder. Send one (section 7).
15. **Rare-tier rules - n/a.** HIGH has no hero piece. The plan says the signature is the span and the crest.

---------------------------------------------------------------------------------------------------------------------
## 3. MUST list (ranked, all in `pets/BlizzardRoc.py`; units are BU, and 1 % H = 0.02 BU)

### MUST 1 - Span to 2.0 H (L47) - the biggest presence gain
- Current bind span 3.78 BU (1.89 H). Target about 3.99 BU (2.0 H), so each tip out about **+0.11 BU**.
- Change the tip in L47: `_raise((2.00 + WDX, 0.30, 1.40))` to about `_raise((2.11 + WDX, 0.30, 1.40))`. Then re-measure.
- The `span` value printed by `model()` (L378) must read >= 3.98.
- Re-run step 1 (collision and `fold_search`). If the collision-free folds fall under 30 of 54, use ELEV (L37) 14 to 18
  instead, and re-measure the span.
- Note the span in MODEL_NOTES as the bind-pose figure in H.

### MUST 2 - Wing bars: violet covert bars, not charcoal (L133-134)
- The coverts currently carry a CHAR barred tip (`bars=[(CHAR, 0.30)] if t > 0.22`). Change it to `(FROST_V, 0.30)`.
  That puts a violet row across the grey wing, which the game camera sees, and it takes CHAR down.
- Keep each covert bar straight, one per feather. No zig-zags (see Q1).
- Keep the primaries CHAR with violet bars (L94 `PBARS`) and the secondaries' CHAR trailing edge (L128). The dark mass
  and the Glacier-floor contrast come from those.
- Targets after the change (re-measure the flat IDs): CHAR at most 28 % side and 22 % game. FROST_V at most 12 %
  overall. That keeps violet as one accent.

### MUST 3 - Crest: violet on the outer 60 %, plumes fatter (L219, L322-325)
- Plume fractions: the `plume()` default is `fracs=(0.55, 0.45)` (L219), so the violet is 45 %. Change the three
  calls to `fracs=(0.40, 0.60)`, so FROST_V is 60 % of each plume.
- Widths (L322-324): centre 0.10 to **0.115**, sides 0.088 to **0.105**. The crest is then three violet-tipped white
  points that read at 64 px (today they are a few purple ticks, see `_icons_strip_64.png`).
- Length stays as built (D2 accepted).

### MUST 4 - Mask as an osprey stripe, not a visor (L289-300)
- The socket plate `B.add(ec + ..., (0.088, 0.008, 0.044), CHAR, ...)` (L292) is a box around each eye. Reduce its
  half-size to **(0.070, 0.008, 0.028)** (about -0.016 BU, or -0.8 % H, in height).
- The heavy brow `B.add(HC + ..., (0.088, 0.04, 0.034), CHAR, ...)` (L299-300): reduce to **(0.075, 0.04, 0.024)**.
- Keep the two stripes (L294-297) and make the back stripe a little thicker, 0.014 to **0.018** (L295). Its back end
  must taper into the nape.
- Keep the eye slit and the FROST_H spot as they are (D3).
- Test: the close sheet should read as a dark osprey eye-line over a slit, not a helmet.

### MUST 5 - White nape collar, so the snow shows from behind (L282)
- The Neck2 cape row at t=0.85 is STORM_GREY (the default col of `neck_cape()`). Make that row SNOW: split the call so
  row 0.85 uses `col=SNOW` and row 0.50 keeps STORM_GREY.
- This puts white on the nape, which runs up into the white crest, so the game camera sees a white head-and-nape
  silhouette over the grey back.
- Target: SNOW at least 15 % in the game view (today 10.9 %).

### MUST 6 - Tail: four wider feathers, not rods (L364-371)
- The four feathers are 0.15 BU wide with a 0.30 taper, so they read as sticks. Change the width to **0.22** and the
  taper to **0.45** (L368). Keep the lengths (0.74-0.80 BU, about 0.40 H) and the spread (+-2.5 and +-8 deg).
- Keep the four-feather plan (no white fan), the STORM bases and the FROST_V bars.

---------------------------------------------------------------------------------------------------------------------
## 4. NICE list (do them with the MUSTs if cheap)

1. **One violet chevron on the breast (L261-262).** The middle breast bar (`lz 0.01`) becomes FROST_V. It gives the white
   front its one accent at icon angle, and it keeps the "one accent" rule. The two outer bars stay CHAR.
2. **Pale underside (L252).** The belly shade strip is 0.10 wide. Widen it to 0.13 so PALE_G reaches about 4-6 % in
   the side view (plan 6 %). It makes the belly-to-back line cleaner.
3. **Flank slab (idle sheet, side view).** In the ground fold, the folded wing covers the flank as one large CHAR and
   STORM block. Break it with a stagger on the covert row, or let the wing rise 3-4 deg in the fold (check at the clip
   gate, not now).
4. **Bind-pose tail reads as sticks** - fixed by MUST 6. Re-check the fan at 64 px.

---------------------------------------------------------------------------------------------------------------------
## 5. Presence levers (concrete; keeps the "giant white bird")

| lever | change | where | what it does for presence | keeps the white bird? |
|---|---|---|---|---|
| span | tip out +0.11 BU per side (2.0 H) | L47 | the silhouette at distance | yes |
| crest | violet 60 %, plumes wider | L219, L322-325 | three violet points at 64 px | yes (SNOW base) |
| nape collar | top cape row SNOW | L282 | white from behind, joins crest | yes, adds white |
| wing bars | covert bars violet, not CHAR | L133-134 | violet row the game camera sees | yes, dark primaries stay |
| mask | stripe, not plate; lower brow | L289-300 | the fierce osprey eye, not a visor | yes |
| breast | one violet centre chevron | L261 (NICE 1) | accent at icon angle | yes |
| tail | four wider feathers | L364-371 | fan, not rods | yes |

Limits: violet at most 12 % of the figure. No violet on any body mass. No saturated hue. CHAR stays on the primaries,
the secondary trailing edge and the mask.

---------------------------------------------------------------------------------------------------------------------
## 6. Clips - not yet

No clip gate today. The placeholder `anim()` is a held fold pose, so there is nothing to judge yet. The clip brief in
`BlizzardRoc_plan.md` section 7 stands. Keep the bow's zero net root travel, and keep no hop on the walk. Check the
span in the fly and takeoff clips too: the wings must not pass through the body at the new tip.

---------------------------------------------------------------------------------------------------------------------
## 7. Round 2 deliverables (send with the MUSTs applied)

- `renders/_model_sheet.png` (bind pose, 600 px per view) with the span printed in MODEL_NOTES as a bind-pose H value
- `renders/_close_sheet.png` (front and game-angle head) and one crest close-up
- `renders/_icons_strip_64.png` and `_128.png` with Thunderbird, Griffin, Yeti, Mammoth and Phoenix
- `flat_side.png`, `flat_tq.png`, `flat_game.png` with the new value shares in MODEL_NOTES
- an **under view** (camera below) of the wing roots, tail base and trousers (checklist item 14)
- the ground fold `_idle_sheet.png`

---------------------------------------------------------------------------------------------------------------------
## 8. Pass / fail

| # | check | result |
|---|---|---|
| 1 | Tris <= 15k | PASS (12,284) |
| 2 | Height 9.0 to the crest | PASS |
| 3 | Span 2.0-2.4 H | **FAIL** (1.89 H) |
| 4 | 64 px species read | PASS |
| 5 | Game camera: white and presence | **FAIL** (white 11 %, crest thin) |
| 6 | Face reads (narrow slit, no visor) | PARTIAL |
| 7 | CHAR within plan (16 %) | **FAIL** (26-37 %) |
| 8 | PALE_G underside (6 %) | PARTIAL (1.5-4.9 %) |
| 9 | One accent (violet) strong in game | PARTIAL |
| 10 | Not a recolour of Thunderbird | PASS |
| 11 | Fierce, not cute | PASS |
| 12 | Brightest channel >= 170 | PASS |
| 13 | Stud skin, no box belly, no glow | PASS |
| 14 | Floating or poking parts (bind, fold) | PASS |
| 15 | Parts visible from below | NOT CHECKED |
| 16 | Tail reads as a fan | PARTIAL |
| 17 | Deviations logged | **FAIL** (span shortfall not declared) |

Score 7/10. The build is clean and distinct. Six MUSTs, all small code edits, bring it to about 8.
