# Creature Index UI review 1 (Glacier update)

Reviewed: `INDEX_MOCKUP_v4_bigger.png` (main, PC 1519x753), `INDEX_MOCKUP_v3_fullscreen.png`, `capture_fullscreen_big_v4.jpg` (raw capture), the shipped Index (tool-result image, 744x674), and the reference frames/contact sheets (PS99, Steal an Egg, Steal a Brainrot, Grow a Garden, Sol's RNG, Anime Vanguards, Bubble Gum Sim). Style rules: Check-UI Rules, Check-UI Skill (full rules), Screen Layout and Windows, Phone UI, Menus and Windows, UI Anti-patterns, Visual Identity and Style.

Method: crops of the v4 mockup upscaled 3x, plus pixel sampling and run-length scans of the 1519x753 image. Measured values are marked as such. Nothing was rendered for phone: the phone numbers in section 6 are computed from the Check-UI scale rule, not seen.

Process note: owner rule (2026-10-22) is that any visible UI change needs an approved mockup first. Treat this as the brief for mockup v5, not a shipped change.

---

## 1. Verdict and score

**Verdict: not ready. Rebuild the mockup before Studio.**

The bones are right and should stay: the Check-UI slate window with a 3.5 px outline, the blue Codes-style header with the checker and big white title, the 3D red X, the lime CLAIM!, the 2 x 3 card grid the owner asked for, and the dark inspect card with a hero portrait. The look is the approved Check-UI cartoon style.

It still reads as scuffed for four reasons:
1. Colour collisions: three tabs are the same amber, every card has a green bevel, and the rainbow card is louder than the rest of the window.
2. Text is 7 to 10 px in the places that matter: card pills, rarity badges, reward chips, tab counts.
3. Layout problems: the window overlaps the top-left HUD, the book icon runs off the top of the screen, the stat labels collide with their values, and there are dead areas.
4. Hierarchy: the bright lime CLAIM and the rainbow card pull the eye before the creatures do. The creature portraits are too small for the cards.

On phone (844x390) the layout does not survive a scale-down. It needs its own layout (section 6).

**Polish score: 4 / 10.**

---

## 2. Top 10 scuffed things (ranked by impact)

1. **Window sits too high and collides with the top-left HUD.** The window's top dark border is at y 17 px and its bottom at y 672 px, so there is 81 px below and 17 px above. The HUD gear (about x 268-312, y 12-56) sits on the window's top-left corner. The book icon runs up to the top screen edge (y about 0). Fix: window top at or below 68 px and vertically centred (section 4.1).

2. **Every card has a green 3D bevel.** Sampled under the cards at x 520, y 336-348: RGB about (14-36, 108-124, 16-40). This is off-palette. It sits under the blue Glacier cards, the gold SECRET card and the rainbow MYTHIC card alike, and it makes the grid look like it sits on grass. Fix: each card's bevel takes that card's own darker tone (section 4.4).

3. **Text is too small across the window.** Approximate font sizes from cap heights:
   - card names about 13-14 px;
   - pill percentages about 10 px;
   - SECRET and MYTHIC badges about 7-8 px;
   - reward chip "+5%" about 7 px;
   - stat labels about 12 px;
   - footer "DISCOVERED" about 18 px.
   Badges and chips are the least readable things in the window, and on phone they would be about half this size. Fix: text sizes in section 4.8.

4. **Three tabs share one amber.** Sampled fills: THUNDER (234-244, 162-178, 0-38), FIRE (233-255, 161-175, 0-1), CELESTIAL (235-254, 158-172, 0-2). They are the same colour, so the element colour code breaks. The SECRET card (251, 207, 102) is also amber and sits next to them. The GLACIER tab is the selected one but the most muted: (119-132, 139-168, 163-218), which reads as disabled. Its white label on pale blue is weak. Stars and the red "!" cover letters: the star covers the R in THUNDER ("THUNDEK"), the "!" covers the R in GLACIER. CELESTIAL fills its tab edge to edge. Fix: section 4.2 colour table; move the star and "!" to the tab corner.

5. **Portraits are small and the cards are busy.** A portrait is about 55 x 67 px inside a card of about 161 x 127 px, so roughly a third of the card is portrait and the rest is checkerboard. The damier checker at full strength behind a 67 px creature is noise. Column gaps are about 5 px while row gaps are about 15 px (including the green bevel), so the grid spacing is uneven. Fix: section 4.4.

6. **Inspect panel: label and value collide, and there is a dead band.** "Hatch chance" runs straight into "0.1%" with no gap (the pixels touch). The "$x8.8" multiplier is crammed into the same row. Below the last stat row there is an empty band from about y 580 to 625 (about 45 px) of dark frame with nothing in it. The glow disc is purple (54, 70, 129), which doesn't match the Glacier theme. Fix: section 4.7.

7. **Footer bar: progress trough stops short, and the bottom edges don't line up.** The dark trough runs from about x 384 to x 760, but the blue bar runs to x 921, leaving a 160 px empty stub. The fill is light blue on a blue bar (low contrast). Check-UI's progress spec is gold-to-orange fill on a dark trough, and the area bar here is green. There is no visible CLAIM ALL slot. The column bottoms don't align: tabs end at y about 548, the reward strip at about 566, the footer at about 622, the inspect panel at about 625. Fix: section 4.6 and section 4.7.

8. **Rarity treatment is loud and confusable.** The MYTHIC card is a full rainbow with a rainbow badge and a rainbow outline, which reads as a sticker. Its white outline also looks like the selected-card state, so mythic and "selected" are easy to mix up. The SECRET card is orange-gold rather than gold, so it sits next to the orange tabs. Fix: section 5.

9. **Reward strip is off-palette and the claim button dominates.** The chips are dark navy (44, 51, 93), which is not the Check-UI card colour (26, 44, 52). The chip icons and "+5%" are tiny. The Money potion and Hatch potion icons are two similar round orbs at about 24 px. The lime CLAIM! is the brightest element in the lower half and pulls focus from the creatures. Fix: section 4.5.

10. **Progress semantics are confusing.** The area header and the Glacier tab show 6/6 because the mythic counts toward x/6, but the area claim only needs the 5 non-mythic cards. A player can see 5/6 with an enabled CLAIM and not know why. Fix: show the claim progress as 5/5, and mark the mythic as a separate BONUS pip (section 4.3).

**Minor, but fix in the same pass:**
- The X is about 66 x 66 px. Check-UI's 38 px button at the 1.18 window scale is about 45 px. The X is oversized next to the title.
- The book icon overhangs the header top edge. The shipped Index does this too, which is fine, but it has to stay below the top bar.
- The window body is two tones: the outer margin is slate (59, 88, 102), but the centre and inspect panels are dark teal (25, 46, 49). This is acceptable as recessed panels; keep it deliberate and consistent.
- Undiscovered cards: no silhouette or "???" state is visible in this mockup. The shipped Index has them. Keep the odds on undiscovered cards too (they are the hook).

---

## 3. Keep as is

- Slate window (59, 88, 102) with a 3.5 px (24, 30, 34) outline and 4 px corners. This is Check-UI.
- The blue Codes header with the damier, top highlight and 2-tier divider, and the big white title with a black stroke.
- The 3D red X style (Check-UI §3.1). Only its size changes.
- Tab shape with a bevel and a count line under the name.
- The 2 x 3 grid itself. The owner asked for it and it works.
- The inspect card's structure: portrait hero, big name, stat rows, dark card frame.
- The CLAIM! lime colour for an enabled claim. Keep the colour, shrink its footprint.
- Element icons (book, stars, "!" alert) as the language for states.

---

## 4. Redesign spec (build from this)

### 4.0 How to map the coordinates

All x and y values are **fractions of the window face** (the frame that holds the header, the columns and the footer). Origin is top-left. Anchor 0,0 unless stated.

The PC reference is the window face at **972 x 617 px** (window Size 0.64 x 0.82 on a 1519x753 screen). Pixel values in brackets are at that size.

If IndexPage is the body only (below the header), subtract 0.15 from every y and divide every height by 0.85. The x values do not change.

### 4.1 Window and header

| Element | x | y | w | h | PC px |
|---|---|---|---|---|---|
| Window (screen) | 0.5 (anchor 0.5, centred) | 0.5 (anchor 0.5, centred) | 0.64 | 0.82 | 972 x 617; top edge at 68 px; bottom margin 68 px; aspect about 1.58 |
| Header bar | 0 | 0 | 1 | 0.15 | 972 x 93 |
| Book icon | 0.065 (centre) | 0.075 (centre) | 0.075 | 0.14 | 73 x 86; may overhang the top by at most 0.02 (12 px) |
| Title "Creature Index" | 0.5 (centre) | 0.075 (centre) | auto | text 0.42 of header h | cap about 39 px; white, 3 px black stroke |
| Close X | 0.955 (centre) | 0.075 (centre) | 0.046 | 0.073 | 45 x 45 px |

Notes:
- Keep the window at Scale 0.64 x 0.82 so the top stays below the 58 px top bar.
- The header is the Codes theme from Check-UI §2.2 (cyan to blue).
- Divider: a 3 px dark blue line (0, 50, 110) plus a 3 px black line, as in Check-UI.

### 4.2 Tab column (7 tabs)

Column: x 0.012, w 0.118 (115 px). Vertical span 0.165 to 0.94.

| Tab | Top y | h |
|---|---|---|
| 1 GRASS | 0.165 | 0.1004 (62 px) |
| 2 WATER | 0.2774 | 0.1004 |
| 3 THUNDER | 0.3898 | 0.1004 |
| 4 FIRE | 0.5022 | 0.1004 |
| 5 SHADOW | 0.6146 | 0.1004 |
| 6 CELESTIAL | 0.727 | 0.1004 |
| 7 GLACIER | 0.8394 | 0.1004 |

Gap between tabs: 0.012 (7 px). Tab top y = 0.165 + (i-1) x 0.1124.

Tab text:
- Name: centred, 0.32 of tab h (max 20 px, shrink to 15 px to fit, one line). Padding 0.012 W each side.
- Count "x/6": centred below the name, 0.22 of tab h (about 14 px).
- Star or "!" badge: centred on the top-right corner of the tab, size 0.03 W (about 29 px). It must not cover a letter: keep the name box inside x 0.012 to 0.10 of the tab width.

Tab colours (top to bottom gradient, then a 3 px darker bevel at the bottom; all labels white with a black stroke):

| Tab | Top RGB | Bottom RGB | Bevel RGB |
|---|---|---|---|
| GRASS | 160, 240, 40 | 110, 200, 20 | 50, 110, 10 |
| WATER | 60, 200, 255 | 0, 130, 235 | 0, 70, 150 |
| THUNDER | 255, 236, 80 | 255, 205, 0 | 160, 110, 0 |
| FIRE | 255, 140, 60 | 230, 60, 20 | 130, 25, 10 |
| SHADOW | 170, 80, 255 | 110, 30, 200 | 60, 10, 120 |
| CELESTIAL | 40, 230, 200 | 0, 170, 160 | 0, 90, 90 |
| GLACIER | 150, 225, 255 | 60, 140, 230 | 20, 60, 130 |

The three ambers are now separated: yellow (THUNDER), red-orange (FIRE), and CELESTIAL moved to teal. Teal is distinct from WATER in hue.

Selected tab: 3.5 px white outline (255, 255, 255), a 0.008 W shift right (as now), and a brighter top. The GLACIER tab must read as selected at full colour, not muted.

### 4.3 Area header (centre column top)

| Element | x | y | w | h | PC px |
|---|---|---|---|---|---|
| Area header | 0.148 | 0.165 | 0.568 | 0.10 | 552 x 62 |
| Title "GLACIER CREATURES" | 0.02 (of header) | 0.12 (of header) | 0.6 | 0.42 | cap about 24 px |
| Subtitle "Hatched from the Glacier Egg" | 0.02 | 0.56 | 0.6 | 0.26 | about 14 px |
| Progress trough | 0.64 | 0.32 | 0.33 | 0.36 | 182 x 22 px |
| Progress count "5 / 5" | centred in trough | | | | about 14 px |

- Claim progress: count **non-mythic cards only**. The trough shows 5 / 5 and fills gold-to-orange (255, 200, 0) to (255, 106, 0) while incomplete, then turns lime (180, 255, 25) to (105, 225, 0) when complete. Check-UI §3.3 defines the gold-orange fill.
- Mythic bonus: a small pip to the right of the trough, labelled BONUS, showing 0/1 or 1/1 in gold. It is not part of the claim fraction.
- Area header background: the Glacier theme. Top (200, 240, 255) to bottom (60, 120, 220), damier at 0.88 transparency.

### 4.4 Card grid (6 cards: 2 rows x 3)

Grid region: x 0.148 to 0.716, y 0.28 to 0.72.

| Element | x | y | w | h | PC px |
|---|---|---|---|---|---|
| Card column 1 | 0.160 | row | 0.1733 | 0.21 | 168 x 130 |
| Card column 2 | 0.3453 | row | 0.1733 | 0.21 | 168 x 130 |
| Card column 3 | 0.5306 | row | 0.1733 | 0.21 | 168 x 130 |
| Row 1 top | | 0.28 | | | |
| Row 2 top | | 0.51 | | | |

Gaps: 0.012 W (12 px) between columns, 0.02 H (12 px) between rows. Both equal in px. The reward strip starts at 0.735 (below the second row).

Inside each card (fractions of the card, card 168 x 130 px):

| Element | x | y | w | h | Text size |
|---|---|---|---|---|---|
| Rarity ribbon (SECRET / MYTHIC only) | 0.5 (centre) | -0.03 (overhangs the top edge by 4 px) | 0.52 | 0.14 | text 0.62 of ribbon h (about 11 px), black stroke |
| Name | 0.04 | 0.13 | 0.92 | 0.11 | max 0.11 of card h (14 px), min 10 px, one line, shrink to fit |
| Portrait | 0.5 (centre) | 0.25 | 0.52 (square, 68 x 68 px) | 0.52 | Fit scale, no stretch |
| Chance pill | 0.22 | 0.80 | 0.56 | 0.13 | text 0.72 of pill h (about 12 px) |
| Bevel | | | | 4 px at the bottom | per card tint (see below) |

Notes:
- Portrait grows from about 55 x 67 px to 68 x 68 px. Crop the new portraits to their bounding box before upload (MOCKUP_NOTES already says this).
- Name stays on one line for every card so the row reads straight across. Undiscovered cards show "???" in the name slot and the silhouette in the portrait slot.
- Pills show the chance on every card, including undiscovered, as now.

Card fill and bevel (normal cards, tinted by area):
- Glacier card: top (226, 246, 255) to bottom (160, 210, 245). Bevel (60, 120, 190). Outline 3 px (24, 30, 34).
- Damier: 0,0,0 at transparency 0.9 (currently much stronger). The checker should be a texture, not a pattern competing with the creature.
- Each area uses its own tint for the bevel. Never green on a non-green card.

Selected card: 3 px white outline (255, 255, 255) and UIScale 1.04. Keep this as the only selection cue.

### 4.5 Reward strip

Region: x 0.148, y 0.735, w 0.568, h 0.08 (49 px PC: 552 x 49). Background: Check-UI card bg (26, 44, 52) with a 2 px inner highlight (75, 125, 145) and a 3 px (24, 30, 34) outline.

| Element | x | y | w | h | Text |
|---|---|---|---|---|---|
| Label "COMPLETE GLACIER:" | 0.012 | 0.1 | 0.18 | 0.8 | two lines, gold (255, 210, 60), 0.28 of strip h each (about 14 px), black stroke |
| Chip 1 (+5% money) | 0.205 | 0.2 (centred vertically) | 0.076 | 0.66 | icon 0.5 of chip h; "+5%" 0.36 of chip h (about 13 px) |
| Chip 2 (+5% speed) | 0.287 | same | 0.076 | 0.66 | same |
| Chip 3 (x1 Money potion) | 0.369 | same | 0.076 | 0.66 | same |
| Chip 4 (x1 Hatch potion) | 0.451 | same | 0.076 | 0.66 | same |
| CLAIM! | 0.545 | 0.2 | 0.155 | 0.66 | Check-UI Claim lime, 3 px bevel (15, 120, 15), text 0.5 of button h (about 18 px) |

Chip colours: card bg (26, 44, 52), 2 px highlight (75, 125, 145), black outline. CLAIM disabled state: silver (216, 222, 228) to (148, 160, 176), bevel (72, 82, 96).

Potion icons: make the Money and Hatch potion icons distinct in shape or colour at 24 px. Two round orbs are not readable.

### 4.6 Bottom bar (footer)

Region: x 0.148, y 0.828, w 0.568, h 0.112 (552 x 69 PC).

| Element | x | y | w | h | Notes |
|---|---|---|---|---|---|
| Book medallion | 0.152 | 0.5 (centred) | 0.05 | 0.09 | 49 x 56 px; no overhang |
| Progress trough (no CLAIM ALL) | 0.215 | 0.5 (centred) | 0.485 | 0.0515 (32 px) | runs to the right edge of the footer |
| Progress trough (CLAIM ALL shown) | 0.215 | 0.5 | 0.345 | 0.0515 | shrinks to make room |
| CLAIM ALL | 0.575 | 0.5 | 0.125 | 0.06 | Check-UI Claim lime; only when something is claimable |

Trough: (20, 30, 36) with a 2 px (12, 18, 22) stroke. Fill: gold (255, 200, 0) to orange (255, 106, 0), bevel (153, 60, 0) 2 px, per Check-UI §3.3. Text "DISCOVERED 33 / 42": white, 0.55 of trough h (about 18 px), black stroke.

The trough must fill the footer width. Right now it stops about 160 px short.

### 4.7 Inspect panel

Region: x 0.73, y 0.165, w 0.258, h 0.775 (251 x 478 px PC). The panel reaches the footer's bottom edge (0.94) so the dead band disappears.

Background: Check-UI card bg (26, 44, 52), 2 px highlight (75, 125, 145), 3 px (24, 30, 34) outline, 4 px corners.

| Element | x | y | w | h | Text / colour |
|---|---|---|---|---|---|
| Portrait stage (glow disc) | 0.755 | 0.19 | 0.208 | 0.30 | disc diameter about 0.88 of stage width (about 176 px), centred at (0.859, 0.335); portrait fits inside 0.9 of disc |
| Name | 0.74 | 0.515 | 0.238 | 0.05 | 0.5 of box h (about 16 px), white, black stroke, one line |
| Rarity pill | 0.75 | 0.575 | 0.218 | 0.04 | "GLACIER · MYTHIC" or similar, 0.55 of pill h (about 13 px); the money multiplier "$x8.8" goes here, not in the stat rows |
| Stat row 1 "Income (best KG)" | 0.745 | 0.645 | 0.23 | 0.058 | label 0.40 of row h (about 13 px), lavender (190, 205, 255); value 0.44 of row h (about 16 px), green (120, 235, 90) for money |
| Stat row 2 "Best weight" | 0.745 | 0.713 | 0.23 | 0.058 | value white |
| Stat row 3 "Hatched" | 0.745 | 0.781 | 0.23 | 0.058 | value white |
| Stat row 4 "Hatch chance" | 0.745 | 0.849 | 0.23 | 0.058 | value white, e.g. "0.1%" |

Stat rows: dark rounded row background (24, 36, 44), 2 px outline (12, 18, 22). Labels left-aligned in x 0.04 to 0.54 of the row; values right-aligned in x 0.56 to 0.96.

Disc colour: tinted to the creature's area or rarity: Glacier disc (150, 210, 255) at transparency 0.6. For MYTHIC, see section 5.

Stat rows now end at y 0.907 and the panel ends at 0.94, so the bottom band is about 20 px of padding, not 45 px of dead space.

### 4.8 Text sizes (relative, at the PC reference)

| Text | Size rule | PC px (approx) | Min |
|---|---|---|---|
| Window title | 0.42 of header h | 39 | 24 |
| Area title | 0.42 of area header h | 24 | 16 |
| Area subtitle | 0.26 of area header h | 14 | 11 |
| Tab name | 0.32 of tab h, max 20, shrink | 20 | 15 |
| Tab count | 0.22 of tab h | 14 | 11 |
| Card name | 0.11 of card h, one line, shrink | 14 | 10 |
| Chance pill | 0.72 of pill h | 12 | 10 |
| Rarity badge | 0.62 of badge h | 11 | 9 |
| Reward label | 0.28 of strip h per line | 14 | 11 |
| Reward chip value | 0.36 of chip h | 13 | 11 |
| Claim button | 0.5 of button h | 18 | 14 |
| Footer count | 0.55 of trough h | 18 | 13 |
| Inspect name | 0.5 of name box h | 16 | 13 |
| Stat label | 0.40 of row h | 13 | 11 |
| Stat value | 0.44 of row h | 16 | 12 |

Rule: no text under 10 px at the PC reference, and every text uses a black stroke as in Check-UI.

### 4.9 Colour summary

| Use | RGB |
|---|---|
| Window body outer | 59, 88, 102 |
| Window and panel outline | 24, 30, 34 |
| Inner panel (cards, reward strip, inspect, chips) | 26, 44, 52 |
| Inner highlight | 75, 125, 145 |
| Stat row bg | 24, 36, 44 |
| Header Codes gradient | 0, 205, 255 to 0, 130, 245 |
| Header top highlight | 180, 240, 255 |
| Header divider dark | 0, 50, 110 (plus black 3 px) |
| Close X face | 255, 125, 175 to 255, 20, 40; bevel 115, 0, 16 |
| Claim lime | 180, 255, 25 to 105, 225, 0; bevel 15, 120, 15 |
| Progress fill | 255, 200, 0 to 255, 106, 0; bevel 153, 60, 0 |
| Progress trough | 20, 30, 36 |
| Gold text (reward label) | 255, 210, 60 |
| Green money value | 120, 235, 90 |
| Lavender stat label | 190, 205, 255 |
| Glacier card top / bottom | 226, 246, 255 to 160, 210, 245 |
| SECRET pink badge | 255, 20, 128 to 212, 0, 85; bevel 120, 10, 45 |

---

## 5. Rarity treatment (inside Check-UI)

Use only Check-UI tokens: the Music pink badge, the gold/amber family, the Day-7 rainbow spectrum, and the existing bevel/outline rules.

### SECRET (gold card + pink badge)

- Card: vertical gradient top (255, 224, 96) to bottom (232, 160, 28). This is clearly gold, not orange.
- Card damier: 0,0,0 at transparency 0.9.
- Inner highlight: 1.2 px (255, 250, 210) at transparency 0.4.
- Bevel: 4 px (150, 80, 0). Outline 3 px (24, 30, 34).
- Ribbon badge: Check-UI Music pink, gradient (255, 20, 128) to (212, 0, 85), bevel (120, 10, 45), highlight (255, 176, 208), text "SECRET" white with a black stroke.
- To keep it apart from the orange tabs, the card's bevel and outline do the separating, not a new colour.

### MYTHIC (dark card + thin rainbow edge)

The rainbow is only an edge, not the whole card.

- Card body: vertical gradient top (40, 34, 84) to bottom (16, 14, 40). Dark, so the card contrasts with the light blue grid.
- Card damier: 255,255,255 at transparency 0.93 (faint).
- Rainbow edge: a backing frame 3 px larger than the card on every side, with a UIGradient using the Check-UI Day-7 spectrum at rotation 45:
  - (255, 30, 80) at 0.00
  - (255, 140, 0) at 0.18
  - (255, 230, 0) at 0.35
  - (40, 230, 50) at 0.52
  - (0, 210, 255) at 0.70
  - (90, 60, 255) at 0.85
  - (220, 0, 230) at 1.00
  The card body sits on top of that backing frame, so the rainbow only shows as a 3 px edge.
- Optional: rotate the backing gradient at most 20 deg/s, paused when the window is hidden, as the sunbursts are.
- Badge: dark pill (20, 14, 40) with the same rainbow edge at 2 px, text "MYTHIC" white with a black stroke.
- Name text: white, same as other cards (not gold, not rainbow).
- Portrait: a faint white disc (255,255,255 at transparency 0.9) behind the creature. No rainbow in the art area.
- Inspect panel: the glow disc gets a 3 px rainbow ring (same backing-frame technique), nothing else.

### Selected state (separate from rarity)

- Selected: 3 px white outline (255, 255, 255) just outside the card, UIScale 1.04.
- A MYTHIC card can be selected too: the white outline sits outside the rainbow edge, so both read.
- This keeps "selected" and "mythic" visually separate.

---

## 6. Phone fit (844 x 390): verdict and layout

**Verdict: fails.** This is computed from the Check-UI scale rule, not rendered.

- Check-UI scale at 844x390: min(844/1050, 390/620) = min(0.804, 0.629) = **0.629**. The floor of 0.52 is not hit.
- v4 window (Scale 0.9 x 0.93) at 0.629: about **478 x 228 px**. With the Phone UI x1.4 bump (scale 0.88): about **668 x 319 px**.
- Cards are about 20% of the window height, so at 319 px tall each card is about 63 px. Name text at 0.11 of card h is about 7 px, pills about 5 px. Unreadable.
- Tabs at 36 px are below the 42 px touch rule in Phone UI.
- The emulator note in Phone UI uses 733 x 392 (scale 0.632), which gives the same result.

The root problem: all text is sized relative to the card height, so it shrinks with the window. Scale-down alone cannot work. The phone layout needs to be a different arrangement.

**Phone layout (height below 520):**
- Window: Scale (0.96, 0.94) with **WindowScale 1.0**. Exempt the Index window from the 0.52 floor on short screens, because its Scale sizes already fill the screen. Keep all text relative to the card height.
- Tabs become a **horizontal strip** under the header: y 0.15, h 0.12 (about 44 px, touch-safe). Seven tabs each w about 0.13 W, showing "NAME x/6" on one line.
- Cards: 3 x 2 grid in the full width, y 0.29 to 0.77. Each card is about 257 x 84 px at 810 x 367 face. Use a horizontal card: portrait square about 0.9 of card h on the left (about 76 px), name and pill stacked on the right. Name 0.22 of card h (about 18 px), pill 0.2 of card h.
- Inspect panel hidden by default. Tapping a card opens it as an overlay sheet on the right (x 0.40 to 0.98, y 0.12 to 0.93) with its own X. The stat table uses 4 rows at h 0.09.
- Reward strip and footer: collapse to one row of text plus the CLAIM button at h about 44 px. Show the chips in the overlay sheet, not at the bottom, where they are only about 6 px tall.
- Header: title at 0.40 of header h. DISCOVERED count goes under the title as small text, not a separate footer.

These numbers are estimates. Check the phone layout in Studio's phone emulator before anyone signs off.

---

## 7. Priority list for the lead (short)

1. Move the window to top 68 px, centred, size 0.64 x 0.82. Keep the book icon inside the header.
2. Recolour the card bevels to each card's own tint. Remove the green. Reduce the card damier to 0.9 transparency.
3. Fix the tab colours (yellow THUNDER, red-orange FIRE, teal CELESTIAL) and move the star and "!" off the letters.
4. Enlarge card names to 14 px and portraits to 68 px. Put the rarity badge on a ribbon at the top edge. Make the column and row gaps 12 px.
5. Fix the inspect panel: no label/value collision, multiplier moved to the rarity pill, stat rows filling the panel down to 0.907.
6. Make the MYTHIC card a dark card with a 3 px rainbow edge, and make the SECRET card gold with the pink ribbon.
7. Footer trough full width, Check-UI gold fill, a CLAIM ALL slot when claimable, and the area bar counting non-mythic cards only (5/5, with a BONUS pip).
8. Build a separate phone layout (section 6), not a scaled-down copy.

---

## 8. Notes and caveats

- Portraits in v4 are pasted approximations (MOCKUP_NOTES). The card portrait sizes above assume the real portraits will be cropped to their bounding box.
- The phone numbers are computed from the Check-UI rule and the v4 window size, not rendered.
- MOCKUP_NOTES.md has the v2 header and body numbers in places. The measured v4 header is about 0.16 of the window height and the window is 1008 x 655 px. The spec above uses the measured values.
- Reference frames were viewed at contact-sheet size. The PS99 "Equip More Pets" frame (pet-simulator-99_14vDyTwoUZc_f1) was the closest collection-window match, and it supports the decisions here: a clean panel, one primary action, a tight grid, no decoration on the cards.
- Nothing in this review edits the game, the mockup, or any file other than this one.
