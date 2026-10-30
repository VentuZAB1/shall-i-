# Creature Index UI review 3 (v6, Glacier update)

Reviewed: `INDEX_MOCKUP_v6.png` (PC 1519x753), `capture_v6.jpg`, and the round-2 review (`INDEX_UI_REVIEW2.md`). Crops were made at 3x and pixels were measured with PIL.

**Coordinate system:** same as rounds 1 and 2. Fractions of the face, origin top-left. Face = window outline top (y 112) to the top of the bottom slab (y 682), which is 570 px. The bottom slab (y 682 to 693) sits outside that face. Px values below are at the 1519x753 screen.

---

## 1. Verdict and scores

**PC mockup: 8 / 10.** v6 is a clear step up from v5 and the PC layout now reads as finished. The tabs, footer, inspect panel, MYTHIC/SECRET tiers and header are good.

**Overall (what can ship): 7 / 10.** The round-1 brief also asked for a phone fit. v6 has no phone layout, so phone is unscored and unsolved. Until a phone mockup exists and scores 8 or better, the overall score stays at 7 on the owner's scale.

**To reach 9+ on PC:** do MUST 1 to MUST 5 in section 4.

**Round-2 MUST check**

| Round-2 MUST | Measured in v6 | Status |
|---|---|---|
| MUST 1 Pets bigger (visible at least 70 px) | Visible pets 70 to 73 px tall, card about 128 px. Met at 70, but still only about 57% of card height | Met, below hero size |
| MUST 2 Use empty band under footer | Footer ends at 0.953. But a 24 px slate band (y 658 to 681) is still there, which is the 0.048 padding from round 2 | Partly met. The band still reads as dead space |
| MUST 3 Bottom edge 4 px | Bottom is a 12 px dark slab (y 682 to 693). Top outline is 4 px (y 112 to 115) | Not met |
| MUST 4 Window centred | Outline y 112 to 693. Screen centre is 376, window centre is 402, which is the centre of the area below the 58 px top bar | Met, accepted |

**Discrepancy to flag:** the brief says "4 px bottom edge". The pixels show 12 px. The top is 4 px. Please check that the 12 px slab is not a leftover drop shadow or a second frame.

---

## 2. Judgement by area

**Pets and cards: better, not hero yet.** Measured visible creature heights: Frostfang Lynx about 72, Ice Mammoth about 73, Glacier Yeti about 73, Blizzard Roc about 73, Permafrost Titan about 73, Frostcrown Dragon about 70 px. Creature widths range from about 60 to 87 px in a card about 155 px wide. The name line and pill still take about 40% of the card height. Pets are big enough to read, but they are not yet the hero (MUST 1).

**Card text and pills:** names read at about 14 px, pills at about 12 px, ribbons at about 11 px. Names are one line and the ribbon clears the name by about 3 px. Keep.

**Gaps:** column gap about 10 px, row gap about 10 px. Keep.

**MYTHIC vs SECRET:** good. The dark indigo MYTHIC card with a 2 px rainbow edge and the white selection outline outside it reads as the top tier. The gold SECRET card with the pink ribbon reads as the second tier. Keep. The double edge when selected is now clean and not busy.

**Reward strip:** good. Label, four chips and CLAIM! are all readable. Keep.

**Footer:** the trough, book medallion and CLAIM ALL with the gold "1" badge are good. Two problems: the 24 px slate band under it, and CLAIM ALL is the same lime as the reward strip CLAIM! directly above it. Two bright lime buttons stacked on each other compete (MUST 4).

**Tab column:** good. Colours are distinct. Stars and "!" sit in the corners and do not cover letters. Keep.

**Inspect panel:** good. The disc holds the dragon well, the rarity pill and stat rows are clean, and the bottom padding is about 20 px. The only gap: the disc colour rule for non-MYTHIC tiers has still not been shown, so it is unverified (MUST 5).

**Header:** good. The book sits inside the header, the title is centred, and the X is a sensible size. Keep.

**Top-left HUD:** clear. The backpack and gear sit above the window's top edge with no overlap.

---

## 3. What to keep

- Tab colours, shapes, stars and "!" placement.
- Card gaps (10 px), name and ribbon spacing, pill style.
- MYTHIC card: dark indigo body, 2 px rainbow edge, dark rainbow-edged pill, faint white disc.
- SECRET card: gold body, pink ribbon.
- Reward strip layout and chip sizes.
- Footer trough colours and book medallion.
- Inspect layout: disc, name, rarity pill with the multiplier, four stat rows, green money value.
- Header and X.
- Window centring (accepted as centred under the top bar inset).

---

## 4. MUST list to reach 9+ on PC (exact numbers, face fractions)

### MUST 1. Pets to hero size

Target: visible creature at least 80 px tall (about 0.57 of card height today, aim for 0.66 or more).

Grid rows (face fractions):
- Grid panel: y 0.264 to 0.792.
- Row 1: y 0.274, card h 0.245 (about 140 px at the 570 px face).
- Row 2: y 0.535, card h 0.245. Row gap 0.016.
- Columns unchanged: x 0.160, 0.3453, 0.5306; card w 0.1733; gap 0.012.

Card contents (fractions of the card; unchanged except as noted):

| Element | x | y | w | h | Notes |
|---|---|---|---|---|---|
| Ribbon | 0.5 (centre) | -0.03 | 0.52 | 0.14 | Unchanged |
| Name | 0.04 | 0.11 | 0.92 | 0.12 | Unchanged |
| Portrait box | 0.1 | 0.22 | 0.8 | 0.68 | Now about 95 px square at card h 140. Sprite fills at least 0.85 of the box: about 80 px visible |
| Chance pill | 0.22 | 0.83 | 0.56 | 0.12 | Unchanged; overlaps the box bottom by about 0.04 |

Check: portrait box 0.68 x 140 px = 95 px. Visible about 80 px = 0.57 to 0.62 of card h. That is the target.

### MUST 2. Remove the 24 px dead band under the footer

Lower blocks (face fractions):

| Block | v6 now | New |
|---|---|---|
| Reward strip | 0.762 to 0.842 | 0.800 to 0.880 (h 0.080) |
| Footer | 0.852 to 0.952 | 0.890 to 0.993 (h 0.103, about 59 px) |
| Bottom padding | 0.048 (27 px) | 0.007 (4 px) |

Tabs and inspect must end on the same line:
- Tab column: top 0.167, h 0.1077, pitch 0.1197 (tab i top = 0.167 + (i - 1) x 0.1197; gap 0.012 as before). Last tab ends 0.993.
- Inspect panel: y 0.167 to 0.993.

Footer internals: keep as v6 (book, trough 0.217 to 0.56, CLAIM ALL at 0.575 to 0.70).

### MUST 3. Bottom edge to 4 px

The window's bottom edge is currently a 12 px dark slab (y 682 to 693). The top is a 4 px outline (y 112 to 115).

Fix: make the bottom the same 3.5 to 4 px outline as the top. If depth is wanted, use a 4 px soft drop shadow at 40% transparency. Do not use a solid slab.

### MUST 4. CLAIM ALL is not the same button as CLAIM!

Now two lime claim buttons stack on each other (reward strip CLAIM! and footer CLAIM ALL). Keep lime for the area claim (the thing the player is most likely to press). Give CLAIM ALL a different Check-UI button style so it reads as a second-level action:
- Fill: Check-UI Skip amber, gradient (255, 208, 0) to (255, 140, 0).
- Bevel: (153, 76, 0), 3 px.
- Text: white with black stroke, same size.
- Keep the gold "1" count badge.

Check-UI §2.3 lists Skip amber as the header action button; reusing it here keeps everything inside the approved palette.

### MUST 5. Show the other rarity tiers in the inspect panel

The inspect disc colour rule (lilac for MYTHIC, ice for common, gold for SECRET) is still only shown for MYTHIC. Mock the SECRET and common inspect states so the owner can judge them. Until that is shown, the rarity system is unverified and the score cannot pass 8.5.

Spec (from round 2, NICE 5, now a MUST for 9+):
- Common and Glacier: ice tint (150, 210, 255) at 0.6 transparency, 3 px ring in (226, 246, 255).
- SECRET: gold (255, 224, 96) to (232, 160, 28), 2 px gold ring.
- MYTHIC: lilac (150, 140, 230) to (60, 52, 130) with the 3 px rainbow ring (as in v6).

### MUST 6 (for overall, not PC). Phone layout

Not designed yet. This is required for the overall score to pass 8. Spec only. It must be mocked and checked in the phone emulator (733 x 392 safe area per Phone UI notes).

- Window: Scale (0.96, 0.94), WindowScale 1.0 (exempt from the 0.52 floor on short screens).
- Tabs: a horizontal strip under the header, y 0.15, h 0.12 (about 44 px, touch-safe). Seven tabs, w 0.13 each, gap 0.008. Label "NAME x/6" on one line, text min 12 px.
- Grid: 3 x 2 across the full width, y 0.29 to 0.77. Horizontal cards: portrait square about 0.9 of card h on the left, name and pill stacked on the right. Name 0.22 of card h, pill 0.2 of card h.
- Inspect: hidden by default. Tapping a card opens it as an overlay sheet at x 0.40 to 0.98, y 0.12 to 0.93, with its own X. Four stat rows at h 0.09.
- Reward strip and footer: one row of about 44 px with the label, CLAIM! and CLAIM ALL. Chips move into the overlay sheet. DISCOVERED count goes under the title.
- No text under 10 px. All touch targets at least 42 px.

---

## 5. NICE (not required for 9+)

- **Area header BONUS pip:** the gold pip text is now about 13 px. Good. Keep.
- **Stat label size:** labels are about 13 px, values about 16 px. Keep.
- **Card-to-ribbon gap:** about 3 px. Could be 4 px for breathing room (ribbon y -0.03 to 0.10 instead of 0.11).
- **Footer count:** "DISCOVERED 33 / 42" straddles the fill edge. It is readable with the black stroke. Optional: move it to the trough's right end.

---

## 6. Caveats

- Pet sizes are measured from the v6 pixels. The 80 px visible target in MUST 1 is a judgement; check it in the owner's PC screenshot.
- The face measured 570 px tall (outline top to the slab top). The brief's 0.993 height does not match the pixels; the fractions above use the measured face, so re-check them if your face size differs.
- Overall score is capped at 7 until a phone mock exists (MUST 6).
- Process: still a mockup. Per the owner's 2026-10-22 rule, no shipped change until the owner sees v7 and says yes.
