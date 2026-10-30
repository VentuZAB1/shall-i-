# Creature Index build review 4 (phone only, real Device-emulator captures)

## Score

| Device | Viewport | Page scale | Score (as built) | Score (after MUST 1) |
|---|---|---|---|---|
| Samsung S22 Ultra (22) | 677 x 338 | 0.452 | **7.5** | about 7.7 |
| iPhone 13 (23) | 749 x 389 | 0.529 | **8.0** | about 8.1 |
| iPhone 16 Pro Max (24) | 831 x 439 | 0.577 | **8.3** | about 8.5 |
| **Phone overall** (the weakest device) | | | **7.5** | **about 7.7** |

- The phone overall is the lowest device, because the one-layout rule means every size must work, and the bar applies to each.
- "After MUST 1" figures are my estimates, not measurements.
- PC is not re-reviewed here. The coordinator reports it is unchanged (PC suite 60/60), so it keeps the review 3 score of 8.8.

## Verdict

**REVISE.** The phone overall is below 8.5 on every device except the 16 Pro Max, and only the 16 Pro Max gets to the bar after the fix. The phone is ready in layout and placement. It is held back by one builder MUST and by the small text on the two smaller screens.

## What works

- **Window placement.** All three windows sit below the Roblox top bar (y 63-64 against a 58 px bar). The bottom margin is clear on all three: 18 px (S22 Ultra), 26 px (iPhone 13), 49 px (16 Pro Max). Nothing crosses a screen edge, the left HUD, the Shop/Claim/Index buttons, the joystick or the jump button.
- **Coordinator's changes are visible and correct.** The inspect stat now reads "Income". The rarity pill reads "GLACIER · $x8.8" with no MYTHIC word, and the MYTHIC badge still shows on the card.
- **Footer and reward strip** are clean on all three: CLAIM! and CLAIM ALL sit inside their buttons with clear padding, the count badge clears the letters, and the chips "+5%" and "x1" are on one line.
- **Readability by device:**
  - 16 Pro Max: every label reads at native size. The tightest spots are the name plates (below).
  - iPhone 13: the card names, chips and chance pills are small but read with care. The inspect panel is clear.
  - S22 Ultra: the tabs, counts, CLAIM buttons, DISCOVERED line and inspect name read. The small labels are marginal (see NICE 2).

## MUST

**M1. "BONUS 1/1" touches the right edge of its pill on all three devices.** Captures 22, 23 and 24, header pill at the top right of the grid. Zoomed, the "1/1" ends about 1-2 viewport px from the pill border. On the S22 Ultra the text sits about 4 px from the left edge and about 1-2 px from the right, so it is off-centre. This is the same defect as CLAIM! in review 2.
- **Fix (same layout):** centre the text in the pill and keep at least 2 px clear on each side. Lower its cap one step on a phone if needed. Check the S22 Ultra first, since it is tightest. Leave the pill's position alone.

## Owner decision: small text on the smaller screens

I did not re-measure the counts. The coordinator reports 29 labels under 9 px on the S22 Ultra, 18 on the iPhone 13 and 3 on the 16 Pro Max, and the labels I can see are consistent with them.

- **Legibility at native size, S22 Ultra:** "FROSTCROWN DRAGON" in its card (about 5 px) is at the edge of readable. BONUS, PERMAFROST TITAN and the "!" (about 6 px) are marginal. Stat labels and chips (about 7 px) read only when zoomed.
- **Legibility, iPhone 13:** readable with care, though most labels are 6-8 px.
- **Legibility, 16 Pro Max:** readable.

The owner's decision is still open, and it is the main reason the S22 Ultra is at 7.5.

## Is the owner decision the only thing between the phone and 8.5?

**No.** There are two things:
1. **M1 (BONUS).** This is a builder fix and is still open.
2. **The S22 Ultra's small text.** This is the owner's call. Even with M1 fixed and the small text accepted as it is, the S22 Ultra is about 7.7, so the phone overall stays below 8.5.

Scenarios:

| Scenario | S22 Ultra | iPhone 13 | 16 Pro Max | Phone overall |
|---|---|---|---|---|
| As built | 7.5 | 8.0 | 8.3 | 7.5 |
| M1 fixed, small text accepted | about 7.7 | about 8.1 | about 8.5 | about 7.7 |
| M1 fixed + review 2 items 3-4 (estimate) | about 8.1 | about 8.5 | about 8.7 | about 8.1 |

Review 2 items 1-4 (for the owner to choose). Items 1 and 2 are already done (MYTHIC dropped from the rarity pill, "Income" label). The two still open are container changes on the shared layout, so PC changes too:
3. Card name plates: widen or raise the name cap, or shorten the longest names.
4. Chance pills: 2-3 px taller inside the card.

If the owner decides the 677 x 338 screen is not a supported size, the phone overall becomes the iPhone 13. That is about 8.1 after M1, so it still misses 8.5 unless items 3-4 are done.

## NICE

1. **Card names touch their card borders by about 2 px.** On the S22 Ultra PERMAFROST TITAN touches its card's right edge; on the 16 Pro Max PERMAFROST TITAN and FROSTCROWN DRAGON do. Text is not clipped. The fix is owner item 3 (shorter names) or a slightly smaller name cap.
2. **Stat text renders with broken spacing on the S22 Ultra.** "Hatch chance" reads as "Hatc hchanc e" at native size. This is a downscale artefact of the small font. It clears up with a larger font, so it belongs with the owner's small-text decision.
3. **Window size and bottom margin differ by screen.** The window is about 75 % of screen height on all three (76 %, 77 %, 74 %), so the bottom margin is 18, 26 and 49 px. Nothing is clipped, but the 16 Pro Max has a wide empty band below the window. The builder may want to check the height rule across screens.
4. **Tab "!" alerts are about 6-8 px.** They read as red dots, which is probably enough for a status mark. Not a blocker.
5. **Glacier portraits still look washed out** (review 2 NICE 2, a PC item). It shows here too.

## Review 3 status (phone)

| Item | Status |
|---|---|
| Review 2 items 1-2 (rarity pill, "Income" label) | Done. "Income" and "GLACIER · $x8.8" read on all three. |
| Review 2 MUST (CLAIM! and CLAIM ALL edges) | Still fixed on all three. |
| Review 2 owner decision (small text) | Open, owner's call. |
| Review 2 NICE 4 (phone tabs about 31 px) | Open. Tabs read on all three. |
| New MUST 1 (BONUS pill edge) | Open. |
