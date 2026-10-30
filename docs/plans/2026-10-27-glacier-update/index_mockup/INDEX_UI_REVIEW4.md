# Creature Index UI review 4 (v7 PC + phone v1, Glacier update)

Reviewed: `INDEX_MOCKUP_v7.png` (PC 1519x753), `INDEX_MOCKUP_v7_common.png`, `INDEX_MOCKUP_v7_secret.png`, `capture_v7_mythic.jpg`, `INDEX_v7_inspect_states.png`, `INDEX_PHONE_v1_grid.png`, `INDEX_PHONE_v1_inspect.png`, `INDEX_PHONE_v1_both.png`, and the round-3 review. Crops were made at 2x to 4x and text heights were measured from pixels.

---

## 1. Scores

| Platform | Score | Ships? |
|---|---|---|
| **PC v7** | **8.5 / 10** | Not yet (at the minimum; 9+ needs P1 to P3) |
| **Phone v1** | **6.5 / 10** | No (needs H1 to H5) |
| **Overall** | **6.5 / 10** | No |

**Overall = 6.5** because the owner's rule (nothing ships below 8.5) applies to each platform the game ships to. The weaker score is the one that decides it. Averaging would give 7.5 and hide the phone problems.

**Verdict:** PC is at the bar. The footer, pets, tiers and inspect states all read well. The phone concept is right (horizontal tabs, horizontal cards, inspect sheet), but the layout is not inside the phone's safe area, it collides with Roblox's top-left buttons, and some text is too small.

---

## 2. Round-3 MUST check (PC v7)

| Round-3 item | Measured in v7 | Status |
|---|---|---|
| MUST 1 Pets (visible at least 80 px, cards h 0.245) | Visible pets 78 to 83 px, card about 140 px | Met |
| MUST 2 Footer tighten (slate gap) | Footer ends at 0.99 of face, slate gap 5 px (was 24 px) | Met |
| MUST 3 Bottom edge 4 px | Bottom is 8 px dark (y 682 to 689): 4 px outline plus a 4 px depth band. Top is 4 px | **Partly met.** Still heavier at the bottom |
| MUST 4 CLAIM ALL Skip amber with count badge | Amber gradient, white "1" badge, correct | Met |
| MUST 5 Inspect states (common, SECRET, MYTHIC) | Three distinct states with matching selected card | Met |

---

## 3. PC v7: what works and what's left

**Works:**
- Pets now read as heroes in the cards (78 to 83 px).
- Footer is tight. Reward strip, trough, CLAIM ALL and book medallion align.
- Three inspect tiers read clearly:
  - common: ice disc, navy pill;
  - SECRET: gold disc, pink pill;
  - MYTHIC: lilac disc with rainbow ring, dark pill with rainbow edge.
- Tabs: distinct colours, stars and "!" sit in the corners.
- Header is clean. Book inside, title centred, X sized right.
- Top-left HUD clear of the window.

**Left to fix (ranked):**
1. **Selected MYTHIC edge is incomplete.** At 4x, the rainbow edge shows on the top and left only. The right and bottom sides look dark. In the unselected MYTHIC (common state) the rainbow runs on all four sides. So the selection outline or card frame is covering the backing edge when the card is selected. This needs a Studio check.
2. **Footer colour clash.** The trough fill (orange) and CLAIM ALL (amber) are the same warm family, side by side in one row. CLAIM ALL is supposed to be the action; the trough competes with it.
3. **Bottom edge still 8 px dark.** Top is 4 px. The depth band makes the window look heavier at the bottom.
4. **CLAIM ALL text contrast.** White text on amber is about 1.6:1. The black stroke helps, but the label is weak at a glance.
5. **Name width on FROSTCROWN DRAGON.** The name fills the card to within about 3 px of each edge.
6. **GLACIER "!" touches the R** of the tab label.

---

## 4. PC MUST list to 9+ (exact numbers)

Coordinates: face fractions, origin top-left, as in earlier rounds.

**P1. Selected MYTHIC: rainbow edge on all four sides.**
- Backing frame: 2 px outside the card on every side, UIGradient Day-7 spectrum at rotation 45 (as now).
- Put the white selection outline **outside** the backing frame, 1 px wide, so both read.
- Check in Studio: the card's child order or a clipping frame is hiding the right and bottom edges when selected.

**P2. Footer trough off the warm family.**
- Trough fill: Glacier blue, gradient (120, 200, 255) to (60, 140, 230), bevel (20, 60, 130) 2 px.
- Trough geometry unchanged: x 0.217 to 0.560, y centred in the footer.
- CLAIM ALL stays Skip amber, so it is the only warm button in the footer.

**P3. Bottom edge.**
- Make the bottom 4 px total, the same as the top: one 4 px outline and no extra depth band.
- If depth is wanted: a soft shadow 2 px, 40% transparency, below the outline. No solid band.

**P4 (NICE for 9+, cheap). CLAIM ALL legibility.**
- Black stroke 3 px on the label, plus a 2 px drop shadow at (60, 30, 0).

**P5 (NICE). Name clearance.** Cap the card name at 0.09 of card h (about 13 px) for names over 14 characters, so long names keep about 6 px of margin.

**P6 (NICE). GLACIER "!"** Move the badge 2 px right and 2 px up so it clears the R.

---

## 5. Phone v1: what works and what's left

**Works:**
- Exact 844x390 content. The file is 858x406 because of a 7 px black device bezel on every side. The bezel is not UI.
- Seven tabs in one row, 44 px tall (touch-safe), stars and "!" in the corners.
- Horizontal cards with the portrait on the left. Cards are about 80 px tall and the pets are visible at about 68 px, so pets are the hero here.
- Bottom row with label, four chips, CLAIM! and CLAIM ALL with its badge.
- Inspect sheet: disc with rainbow ring, name, rarity pill, four stat rows.
- DISCOVERED count sits under the title, as the spec asked.

**Left to fix (ranked by impact):**

1. **The layout is not inside the phone's safe area.** The Phone UI notes give the emulator safe area as 733 x 392. The mock uses the full 844 width, so it is 111 px wider than the safe area (about 55 px cut on each side on a notched device). Left and right cards and the header corners are at risk.
2. **Book icon collides with Roblox's top-left buttons.** Measured at content x 11 to 48, y 1 to 46. Roblox's top-left menu and chat buttons sit in that same corner, so the icon would be covered.
3. **Bottom row is 6 px from the bottom edge** (ends at content y 384 of 390). Landscape phones have a home indicator and gesture area along that edge, so the row would be covered.
4. **Two close buttons in the inspect sheet.** The window's X sits directly above the sheet's X, so players will see two "close" targets stacked.
5. **Text is too small for a phone.** Measured cap heights, converted to px:
   - tab names about 11 px (cap 8 px); the spec said at least 12 px;
   - tab counts about 11 px;
   - bottom label "COMPLETE GLACIER / 5/5 · BONUS 1/1" about 11 to 12 px;
   - chips "+5%" about 12 px;
   - DISCOVERED about 11 px;
   - card names about 14 px (fine);
   - inspect stat labels about 10 to 11 px (estimated).
6. **Inspect sheet covers the header.** The sheet's top edge runs over the right half of the title and the DISCOVERED line.

---

## 6. Phone MUST list (exact px, content coordinates, origin top-left of the 844x390 content)

The phone numbers below are targets for the layout. The insets are estimates from the Phone UI notes (733 x 392 emulator area, top bar 36 to 58 px, home indicator about 18 px). Verify in the phone emulator and adjust.

**Safe box (everything inside it):** x 56 to 788 (732 px wide), y 40 to 372.

**H1. Fit the safe box.** Scale the window to the 732 px safe width. Keep the window's own edge inside the safe box, not at the screen edge.

**H2. Move the book icon off the Roblox corner.** Put it inside the header at x 72 to 104, y 52 to 84 (32 px), or drop it on phone. It must not touch y < 40 or x < 56.

**H3. Lift the bottom row to clear the home indicator.** Bottom row at y 318 to 362 (44 px). The row ends 10 px above the safe-box bottom (372) and 28 px above the content bottom (390).

**H4. One close button.** While the inspect sheet is open, hide the window's X. The sheet's own X sits at the sheet's top-right corner, 30 x 30 px, inset 8 px.

**H5. Text minimums on phone (px):**
- Title 22; DISCOVERED 12;
- tab name 14 (cap about 10); tab count 12;
- card name 14; pill 13;
- bottom label 12; chips 12; CLAIM! 14; CLAIM ALL 13;
- inspect name 16; stat labels 12; stat values 14.
Tabs are 44 px tall, which fits two lines at 14 and 12 px with 6 px of padding.

**Layout that fits the safe box (px, from y 40):**

| Block | y | x | Notes |
|---|---|---|---|
| Header | 40 to 88 (48 px) | 56 to 788 | Title 22 px, DISCOVERED 12 px under it |
| Tab strip | 94 to 138 (44 px) | 61 to 783 | 7 tabs, each 98 px wide, gap 6 px |
| Cards row 1 | 144 to 224 (80 px) | 61 to 783 | 3 cards, each 235 px wide, gap 8 px |
| Cards row 2 | 230 to 310 (80 px) | 61 to 783 | Same columns |
| Bottom row | 318 to 362 (44 px) | 61 to 783 | Label 150 px; 4 chips 46 px each, gap 6 px; CLAIM! 120 px; CLAIM ALL 140 px |

Card contents (80 px tall):
- Portrait square 72 px on the left, inset 4 px (keeps pets at about 70 px visible).
- Name at 14 px, top-right of the card, 14 px inset.
- Pill and rarity tag below the name, 13 px text.

Inspect sheet: x 349 to 774, y 40 to 362. Sheet X at the top-right inside the sheet.

**Score targets:** H1 to H5 done takes the phone to about 8.5. After that the phone needs a fresh review to reach 9+.

---

## 7. NICE (not required for 8.5 or 9+)

- Inspect sheet: lower it so it does not cover the header title (H6). Start the sheet at y 88, the bottom of the header.
- The phone's dimmed grid behind the sheet is clear enough. Keep the dim at its current level.
- Phone pills: "0.1%" and "2.5%" are readable. Keep the dark pill style.

---

## 8. Caveats

- PC cap heights and pet sizes are measured from the v7 pixels. The 9+ items are judgements; check them in the owner's PC screenshot.
- The selected-MYTHIC edge (P1) is inferred from a 4x crop. Confirm in Studio before fixing.
- Phone text sizes are cap heights converted to px (font size about cap height divided by 0.72). Accurate to about 1 px.
- Phone safe-area and top-bar numbers are from the vault notes, not measured on a device. The layout in section 6 is a target.
- Process: still mockups. Per the owner's 2026-10-22 rule, nothing ships until the owner sees the next version and says yes.
