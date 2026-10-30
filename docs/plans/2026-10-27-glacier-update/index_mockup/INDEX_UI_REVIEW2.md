# Creature Index UI review 2 (v5, Glacier update)

Reviewed: `INDEX_MOCKUP_v5.png` (main, PC 1519x753), `capture_v5.jpg`, `INDEX_BEFORE_AFTER_v4_v5.png`, and the round-1 review (`INDEX_UI_REVIEW1.md`). Crops were made at 3x and pixels were measured with PIL.

**Coordinate system:** same as round 1. All x and y are fractions of the window face, origin top-left, anchor 0,0. Face = outline to outline. I measured it at about 905 x 577 px; the brief says 897 x 569. The px values below are for the 897 x 569 face, so scale them if your face differs.

---

## 1. Verdict and score

**Score: 7 / 10** (v4 was 4 / 10).

The round-1 fixes landed. The three ambers are now distinct (yellow THUNDER, red-orange FIRE, teal CELESTIAL). The green bevels are gone and the bevels are now card-tinted. The stars and "!" no longer cover letters. The reward strip labels and chips are readable, and the CLAIM! button sits in its own slot. The footer, the tab column and the inspect panel now share a bottom edge. MYTHIC and SECRET read as two different tiers. The inspect panel is balanced, and the stat rows no longer collide.

**Still scuffed, in order of impact:**
1. **The pets are still too small in the cards.** This is the main ask from the owner, and v5 misses it.
2. **Dead space under the footer.** About 30 px of empty slate, then a 16 px dark slab at the bottom edge.
3. **The window is still high,** and its top corner touches the top-left HUD gear.
4. **The bottom edge is heavy.** It is 16 px at the bottom and 4 px at the top.

Everything else is polish.

---

## 2. Answers to the points you asked me to check

**Are the pets big enough in the cards? No.** Measured visible creatures: Frostfang Lynx about 47 x 57 px, Ice Mammoth about 62 x 60 px, Glacier Yeti about 52 x 60 px, Blizzard Roc about 60 px tall, Permafrost Titan about 60 px tall. The cards are about 155 x 121 px. So a creature fills about 50% of the card height and about a third of the card width, and the rest is checkerboard and name. The portrait box is 68 px and the visible sprite is about 85% of it. That is the number to move (MUST 1).

**The empty band under the footer: yes, fix it.** Footer panel bottom is at face 0.918. Then about 28 px of slate body (face 0.92 to 0.97), then a 16 px dark slab (face 0.97 to 1.00). The slab is the window's bottom edge. The top edge is only 4 px. The inspect panel ends at the same line, so the dead space runs under both columns (MUST 2 and MUST 3).

**MYTHIC vs SECRET read: good, keep it.** The dark indigo MYTHIC card with a thin rainbow edge and dark pill reads as the premium tier, clearly apart from the warm gold SECRET card with the pink ribbon. The rainbow stays small. The one issue is the double edge when a MYTHIC is selected: the white selection outline and the rainbow edge sit next to each other and look busy (NICE 4).

**Inspect panel balance: good.** The disc, name, rarity pill and four stat rows fill the panel. The stat labels no longer touch their values. The empty space under the last row is about 18 px, which is fine. The lilac disc is good for MYTHIC, but the rule for other rarities is not defined (NICE 5).

**Tab column: good.** The colours are distinct and the labels fit. Remaining issue: the stars overhang the tab edge by about 8 px and push into the gap (NICE 2).

---

## 3. What changed vs your deviations (judgement)

- **Reward strip:** label and chips no longer overlap. Chips read at about 13 px. Keep.
- **Grid panel and gaps:** the recessed panel reads. Column gap is about 11 px and row gap about 10 px, which matches the spec. Keep.
- **Area header:** the 5/5 trough with the BONUS 1/1 pip fixes the counting question. The pip text is about 11 px, which is small (NICE 7).
- **Inspect disc:** lilac with a rainbow ring works for MYTHIC. The disc colour needs a rule (NICE 5).
- **Portrait slot:** no change. The slot is still too small (MUST 1).

---

## 4. MUST (exact numbers, face fractions)

### MUST 1. Make the pets bigger in the cards

Target: visible creature at least 70 px tall, from about 58 px in v5.

Grid rows and card size:
- Row 1 top y = 0.272 (unchanged).
- Card height h = 0.225 (was 0.21), so about 128 px. Card width unchanged at about 0.1733 (155 px).
- Row 2 top y = 0.513 (row gap 0.016).
- Row 2 bottom = 0.738. Grid panel bottom = 0.750.
- Column x unchanged: 0.160, 0.3453, 0.5306. Gap 0.012 (11 px).

Card contents (fractions of the card):

| Element | x | y | w | h | Notes |
|---|---|---|---|---|---|
| Ribbon (SECRET / MYTHIC) | 0.5 (centre) | -0.03 | 0.52 | 0.14 | Unchanged |
| Name | 0.04 | 0.11 | 0.92 | 0.12 | Moved down 0.01 so it clears the ribbon by 3 px. Text max 0.09 of card h, one line |
| Portrait box | 0.1 | 0.22 | 0.8 | 0.68 | Square fit, so about 87 x 87 px. The sprite must fill at least 0.85 of the box |
| Chance pill | 0.22 | 0.83 | 0.56 | 0.12 | Overlaps the bottom of the portrait box by about 0.04 (5 px). Text 0.72 of pill h |

Result: visible creature about 74 px tall (from about 60). Pills and names keep their current sizes.

If the lead wants more, the next step is to drop the name to 0.10 of card h and move the box to y 0.20. Do not shrink the cards further.

### MUST 2. Use the empty band under the footer

Vertical stack (face fractions):

| Block | Current v5 | New |
|---|---|---|
| Area header | 0.167 to 0.26 | unchanged |
| Grid panel | 0.272 to 0.728 | 0.272 to 0.750 |
| Reward strip | 0.713 to 0.791 | 0.762 to 0.842 (h 0.080, about 46 px) |
| Footer | 0.803 to 0.918 | 0.852 to 0.952 (h 0.100, about 57 px) |
| Bottom padding to outline | 0.082 (about 47 px) | 0.048 (about 27 px) |

The footer's internal layout stays as v5: book medallion at x 0.152, trough at 0.217 to 0.559 when CLAIM ALL is shown, CLAIM ALL at x 0.575 to 0.700.

Tab column and inspect panel: both end at y 0.952 to match the footer.
- Tabs: top 0.167, pitch 0.114, h 0.102. Tab i top = 0.167 + (i - 1) x 0.114.
- Inspect panel: y 0.167 to 0.952.

### MUST 3. Fix the bottom edge

Measured: the window's bottom edge is a 16 px dark slab (face 0.97 to 1.00, colour about 25, 30, 34). The top edge is 4 px (24, 30, 34).

Fix: make the bottom 4 px like the top. If you want depth, use a 4 px drop shadow at 40% transparency below the window, not a solid 16 px slab. Keep the 3.5 px (24, 30, 34) outline and 4 px corners.

### MUST 4. Move the window down and centre it

Measured: outline top at y 56 px (the top-left topbar zone is 12 to 56 px). Outline bottom at about 632. Space above 56 px, below about 121 px. The gear's bottom-right corner (312, 56) touches the window's top-left corner (307, 56).

Fix: Position Y = 0.5, AnchorPoint Y = 0.5. At 569 px tall this puts the top at about 92 px and the bottom at about 661 px, with the gear 36 px clear. X is already centred (outline 307 to 1211).

---

## 5. NICE (exact numbers, face fractions)

**NICE 1. CLAIM ALL (1) text.** In the footer the "(1)" reads as "(I)". Use a count badge: a 0.03 x 0.06 gold circle at the button's top-right corner with the count in black, 0.5 of badge h. Keep the label "CLAIM ALL" at about 14 px.

**NICE 2. Tab stars overhang.** The WATER and THUNDER stars sit about 8 px outside the tab edge. Move them inside the top-right corner: x 0.82 to 0.97 of tab w, y -0.10 to 0.18 of tab h (so they stay in the tab's own corner and do not push into the gap). The GLACIER "!" should follow the same rule.

**NICE 3. Name to ribbon spacing.** On SECRET and MYTHIC cards the name sits 3 px under the ribbon. MUST 1 already moves the name to y 0.11. Check that this clears the ribbon bottom at 0.11.

**NICE 4. MYTHIC double edge when selected.** The white selection outline sits outside the rainbow edge, and the two read as a double border. Options: (a) keep the white selection outline and inset the rainbow edge to 2 px; or (b) when a MYTHIC is selected, replace the rainbow with the white outline only. Option (a) keeps the rarity visible. Pick one.

**NICE 5. Inspect disc rule.** Lilac (150, 140, 230) to (60, 52, 130) with a rainbow ring works for MYTHIC. Define the rule for the other tiers so the disc colour means something:
- Common and Glacier: ice tint (150, 210, 255) at 0.6 transparency, as in round 1.
- SECRET: gold (255, 224, 96) to (232, 160, 28), with a 2 px gold ring.
- MYTHIC: the lilac disc with the 3 px rainbow ring, as now.

Note: no SECRET inspect state is in v5, so the SECRET disc is not judged here.

**NICE 6. Reward potion icons.** The Money potion (yellow) and Hatch potion (green) are distinct by colour at 24 px. This is acceptable. If you want more separation, give the Hatch potion a different shape.

**NICE 7. BONUS pip text.** The "BONUS 1/1" text is about 11 px. Make it 13 px (0.55 of pip h) and keep the gold fill.

**NICE 8. Footer count position.** "DISCOVERED 33 / 42" straddles the fill edge (orange on the left, dark trough on the right). It stays readable with the black stroke. Optional: move the count to the trough's right end so it sits on the dark part.

**NICE 9. Mythic ribbon text.** The "MYTHIC" text in the dark pill is about 9 px. Make the pill 0.14 of card h and the text 0.62 of pill h (about 11 px), as in round 1.

---

## 6. KEEP

- Tab colours and shapes (yellow THUNDER, red-orange FIRE, teal CELESTIAL, pale GLACIER with white outline).
- Tab name and count sizes. The star and "!" placement is better than v4 (NICE 2 is minor).
- MYTHIC card treatment: dark indigo body, thin rainbow edge, dark pill, faint white disc behind the portrait.
- SECRET card: warm gold with the pink ribbon.
- Reward strip layout: label, four chips, CLAIM!.
- Footer structure: book medallion, orange-gold fill trough, CLAIM ALL.
- Inspect layout: disc, name, rarity pill with the multiplier, four stat rows with the green money value.
- Header: Codes-style gradient, title, X, book inside the header.
- Grid gaps: 11 px columns, 10 px rows.

---

## 7. Phone

Not judged in this round. Round 1 section 6 still applies: at 844x390 the desktop layout needs its own phone version (horizontal tab strip, tap-to-open inspect sheet). The MUST 1 change (taller cards) makes the phone version harder, not easier, so do the phone layout as a separate mockup.

---

## 8. Caveats

- Pet sizes are measured from the v5 pixels (about 47 to 62 px wide, about 57 to 60 px tall). The MUST 1 target of 70 px visible height is a judgement. Check it in the owner's screenshot at PC.
- The face size is 905 x 577 measured, 897 x 569 per the brief. Fractions are the spec; the px values are for 897 x 569.
- Process: this is still a mockup. Per the owner's 2026-10-22 rule, no shipped change until the owner sees v6 and says yes.
