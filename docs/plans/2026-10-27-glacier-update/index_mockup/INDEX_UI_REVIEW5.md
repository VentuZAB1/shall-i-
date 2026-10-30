# Creature Index UI review 5 (PC v8 + phone v2, Glacier update)

Reviewed: `INDEX_MOCKUP_v8.png` (PC 1519x753), `capture_v8.jpg`, `INDEX_PHONE_v2_grid.png`, `INDEX_PHONE_v2_inspect.png`, `INDEX_PHONE_v2_both.png`, `capture_phone_v2_grid.jpg` and `capture_phone_v2_sheet.jpg`, plus the round-4 review. Crops were made at 2x to 4x. Edges, cap heights and contrast were measured from pixels.

**File-name note:** the brief names `capture_phone_v2_inspect.jpg`, but the file in the folder is `capture_phone_v2_sheet.jpg`. I used the sheet capture.

---

## 1. Scores

| Platform | Score | Ships? |
|---|---|---|
| **PC v8** | **8.5 / 10** | Not yet. One MUST (CLAIM ALL contrast) |
| **Phone v2** | **7.5 / 10** | No. One MUST (window top in the top-bar band) |
| **Overall** | **7.5 / 10** | No |

**Overall = 7.5**, the weaker of the two, because the owner's 8.5 bar applies to each platform.

**If both MUSTs are done, the expected scores are PC 9.0, phone 8.5, overall 8.5.** That meets the bar. Phone 9+ needs the extra items in section 5.

---

## 2. Round-4 MUST check

| Round-4 item | Measured in v8 / v2 | Status |
|---|---|---|
| PC P1 Selected MYTHIC rainbow on all four sides | Rainbow ring visible on top, left, right and bottom at 4x. White select frame sits outside it | **Met** |
| PC P2 Footer trough off the warm family | Trough is Glacier blue, CLAIM ALL is the only warm button | **Met** |
| PC P3 Bottom edge 4 px | Top outline y 112 to 115 (4 px). Bottom outline y 682 to 685 (4 px) | **Met** |
| PC P4 CLAIM ALL label contrast (NICE last round) | White label on the fill measures **1.92:1** (fill about 247, 173, 0). Below the 3:1 minimum for large text | **Not met.** Now a MUST |
| Phone H1 Fit the 732 px safe box (x 56 to 788) | Left outer edge x 56, right outer edge about x 787 | **Met** |
| Phone H2 Book icon off the Roblox corner | Book moved right to x 73 to 98, but it still sits at y 18 to 48, inside the top bar band | **Partly met.** Now a MUST |
| Phone H3 Bottom row y 318 to 362 | Row sits at y 318 to 362 | **Met** |
| Phone H4 One close button | Window X hidden while the sheet is open; only the sheet's X shows | **Met** |
| Phone H5 Text minimum 12 px | Cap heights 9 px (about 12 px font) on DISCOVERED, tab names, bottom labels and chips. CLAIM! cap 13 px | **Met** |

---

## 3. PC v8: what works and what's left

**Works:**
- Selected MYTHIC now reads as a complete card: the rainbow ring is on all four sides and the white select frame sits outside it. The double edge is busy at small size but reads correctly.
- Footer trough is blue. CLAIM ALL is the only warm button in the footer, and the count badge is clear.
- Bottom edge is now 4 px, the same as the top.
- Pets, card gaps, tabs, reward strip and inspect panel are unchanged from v7. I checked the grid and footer at 3x and found no regressions.

**Left to fix (ranked):**
1. **CLAIM ALL label contrast: 1.92:1.** White text on Skip amber (247, 173, 0) fails the 3:1 minimum for large text, even with the black stroke. This is the primary footer action, so it's the weakest point on PC.
2. **FROSTCROWN DRAGON name is tight.** The name is about 149 px in a card about 155 px wide, so each side has about 6 px of margin.
3. **GLACIER "!" touches the top of the R** in the tab label. This was in v7 and is unchanged.

---

## 4. PC MUST list to 9+ (exact numbers)

**M1. CLAIM ALL: darker amber so the white label passes contrast.**
- Fill gradient: top (214, 98, 0) to bottom (190, 68, 0). Measured white-text contrast about 3.75:1 at the top and about 5:1 at the bottom.
- Bevel: 3 px (120, 48, 0).
- Label: white, 3 px black stroke (keep the Check-UI white-title rule).
- Count badge: keep the white "1" badge.

*Deviation note:* round 3 asked for Skip amber (255, 208, 0) to (255, 140, 0). That amber fails contrast with white text (1.92:1 measured). This darker amber keeps the Check-UI Skip shape and the white label, and passes the contrast check.

**Optional for 9+ (cheap):** cap the card name at 0.09 of card h (about 13 px) for names over 14 characters. That gives the long names about 8 px of margin. This is the "FROSTCROWN DRAGON" fix.

---

## 5. Phone v2: what works and what's left

**Works:**
- Window x is right: outer left edge at x 56, outer right edge at about x 787.
- Book icon moved off the window's bottom-left corner and sits inside the header.
- Bottom row at y 318 to 362 leaves 28 px above the content bottom (390). That clears the home indicator.
- Single close button when the inspect sheet is open.
- Tab names, counts, card names, chips and labels all meet the 12 px minimum (cap heights 9 px or more).
- Tabs are 44 px tall, cards are about 235 x 80 px, and CLAIM! and CLAIM ALL are 120 px and 140 px wide. All are touch-sized.
- Pets are the hero in the horizontal cards, with the portrait on the left.

**Left to fix (ranked):**

1. **Window top sits inside the top-bar band.** Measured outline top at content y 4 to 6 (header starts y 7). The band from y 0 to 36 holds Roblox's top bar, and its menu and chat buttons sit at the top-left. The brief's safe box starts at y 8, and my round-4 spec said y 40. Measured, the window also runs 2 px past y 372 (outline bottom at y 374).
2. **Book icon sits in that same top-left band.** It measures at content x 73 to 98, y 18 to 48. Moving it right cleared the window's corner, but not the top-bar band. The mock doesn't draw Roblox's top bar, so this has to be checked in the emulator with the top bar on.
3. **Inspect sheet covers the header's right half.** Its top edge sits at about y 49, so the DISCOVERED line and the right side of the title are hidden behind it.
4. **Mythic name wraps to two lines** ("FROSTCROWN / DRAGON") while other names fit on one. Not wrong, but it makes the mythic card's name block taller than the others.

---

## 6. Phone MUST list (exact px, content coordinates, origin top-left of the 844x390 content)

**H1. Move the window into the safe band.** Top at y 40, bottom at y 372 (332 px tall). The window stays at x 56 to 788.

Layout inside that window:

| Block | y | Notes |
|---|---|---|
| Header | 40 to 82 (42 px) | Title cap 16 px (about 22 px font) at about y 46 to 62; DISCOVERED (12 px font) at about y 66 to 76 |
| Tab strip | 88 to 132 (44 px) | Same seven tabs, same 98 px widths |
| Cards row 1 | 138 to 222 (84 px) | Columns unchanged (x 61 to 783) |
| Cards row 2 | 228 to 312 (84 px) | Gap 6 px between rows |
| Bottom row | 318 to 362 (44 px) | Unchanged |
| Window bottom | 372 | 18 px to the content bottom |

**H2. Book icon inside the moved header.** x 72 to 100 (28 px), y 46 to 76 (30 px). It sits fully inside the header and below y 40.

**H3. Inspect sheet aligned to the window.** Sheet top at y 40 (same as the window, not y 49), bottom at y 364. Sheet X at the sheet's top-right corner, 30 x 30 px, inset 8 px.

**Expected after H1 to H3: phone 8.5.**

---

## 7. Phone 9+ items (after H1 to H3)

- **Inspect sheet below the header.** Start the sheet at y 88 (the bottom of the tab strip's header) so the title and DISCOVERED line stay visible. Sheet y 88 to 364 (276 px). The four stat rows (9% each) still fit.
- **Mythic name on one line.** Cap the mythic card name at 13 px so "FROSTCROWN DRAGON" fits in 235 px. Keep the wrap for longer names only if needed.

---

## 8. NICE (not required for 8.5 or 9+)

- PC: the GLACIER tab "!" moves 2 px right and 2 px up so it clears the R.
- PC: the selected MYTHIC's double edge (rainbow plus white outside) is busy at 1x. Keep it, since both read at 4x.
- Phone: stat labels in the inspect sheet are about 12 px. Keep them at 12 px or larger.

---

## 9. Caveats

- PC contrast was measured from the sampled fill and the white label colour (WCAG relative luminance). The proposed amber's contrast is computed, not rendered; check it in the owner's PC screenshot.
- Phone top-bar and safe-area numbers are from the vault notes (733 x 392 emulator safe area; top bar 36 to 58 px). The mock does not draw Roblox's top bar, so H1 and H2 must be confirmed in the emulator with the top bar on.
- The magenta markers the brief describes (x 56 and x 788) are not visible in `capture_phone_v2_grid.jpg`. I measured the window edges from the PNG instead (outer left x 56, outer right about x 787).
- The inspect sheet capture used is `capture_phone_v2_sheet.jpg`.
- Process: still mockups. Per the owner's 2026-10-22 rule, nothing ships until the owner sees the next version and says yes.
