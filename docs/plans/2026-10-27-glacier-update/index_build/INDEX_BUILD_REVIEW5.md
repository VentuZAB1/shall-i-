# Creature Index build review 5 (all devices, against the 8.5 bar)

Owner's ask: every device at least 8.5, with 8.3 as the floor for the hardest one.

## Scores

| Device | Capture | Score | Against the bar |
|---|---|---|---|
| PC (1519 x 753 viewport) | 29 | **8.8** | Passes 8.5 |
| Samsung S22 Ultra (677 x 338) | 26, 26b | **8.1** | **Below the 8.3 floor** |
| iPhone 13 (749 x 389) | 27 | **8.4** (provisional) | Below 8.5 |
| iPhone 17 Pro (749 x 381) | 30 | **8.4** | Below 8.5 |
| iPhone 16 Pro Max (831 x 439) | 28, 28b | **8.9** | Passes 8.5 |
| **Phone overall (the weakest device, the S22)** | | **8.1** | Below the floor |

Notes on the scores:
- The phone overall is the lowest device, since the bar applies to each device.
- The iPhone 13 score is provisional. Capture 27 is a window-only crop, so I cannot see the top bar, the screen edges or the bottom margin. Placement is only supported by the builder's `v8device` test. Its text is judged on what the capture shows.
- Capture 29 (PC) is 897 x 567, a crop of the Index window rather than the full 1519 x 753 viewport. It is enough to judge the window and its text, not the placement.

## Verdict

**REVISE.** Three of the four phones are below 8.5, and the S22 is below its 8.3 floor. The PC and the 16 Pro Max pass. The shortfall comes from one thing: the FROSTCROWN DRAGON card name (and PERMAFROST TITAN on the S22) cannot reach 9 px in one line inside its card. The window is already at its widest, so the name is width-bound.

Placement is good on every phone I could see. The window is below the top bar, clears the screen edges, and the money and speed pills are clear. The rarity pill reads "GLACIER · $x8.8", "Income" reads on every device, and the reward chips sit on one line.

## What the captures show

- **PC (29):** the window reads as v8. The pills and badges at the new sizes are clean. The PC still reads "Income (best KG)" and "GLACIER · MYTHIC · $x8.8", so the phone-only shortening has not leaked onto PC. Nothing is clipped.
- **S22 Ultra (26, 26b):** the window is wider and clears the top bar and the left HUD by about 11 px. The jump button is partly covered (the arrow stays visible). The BONUS text is now centred with clear space on both sides. The SECRET badge clears PERMAFROST TITAN by a thin gap. The MYTHIC badge sits a couple of pixels above the name line. The chips and CLAIM! are on one line, and the count badge is clear. The FROSTCROWN name is legible at 2x but is the smallest text on the screen.
- **iPhone 13 (27):** the grid, footer and inspect panel read clearly. Only the FROSTCROWN name is under 9 px.
- **iPhone 17 Pro (30):** the window sits below the top bar and clears the bottom edge. The SECRET and MYTHIC badges clear their cards. The inspect panel reads well. The FROSTCROWN name is under 9 px.
- **iPhone 16 Pro Max (28, 28b):** the window is narrowed to fit beside the pills, as built. Every label I checked reads at native size. The MYTHIC badge clears the chance pill above it by a few pixels.

## MUST (blockers for 8.5 and the 8.3 floor)

**M1. The FROSTCROWN DRAGON and PERMAFROST TITAN card names are too small on the phones.**
- S22 Ultra: FROSTCROWN 6 px, PERMAFROST 7 px. This is the 8.3 floor failure.
- iPhone 13: FROSTCROWN 8 px.
- iPhone 17 Pro: FROSTCROWN 7 px.
- iPhone 16 Pro Max: FROSTCROWN 9 px (passes).

These names are width-bound: the phone window is already as wide as the pill row allows, so a bigger font wraps or clips. A same-layout fix is one of these two, applied on every device including PC:
1. **Two-line name plate** for any name that cannot fit at 9 px in one line. The plate grows a little and the portrait gives up the same height. This is a layout change, so it needs the owner's yes, and PC changes too.
2. **Shorter display name** for the two long creatures (for example, "FROSTCROWN" alone). This is a content change, so it is the owner's call.

I recommend option 2 if the owner accepts it, since it changes no layout. Option 1 keeps the names intact.

**Estimate only, not measured:** with M1 fixed so both names reach 9 px, I expect the S22 at about 8.4, the iPhone 13 and 17 Pro at about 8.6, and the 16 Pro Max at about 9.0. That would meet the owner's ask. The next round of captures has to confirm it.

## Owner's ask: answer

Not yet. The PC and the 16 Pro Max pass. The S22 is below its floor, and the iPhone 13 and 17 Pro are below 8.5. M1 is the only blocker, and it is an owner decision (option 1 or 2 above), so the builder cannot close it alone.

## NICE

1. **Jump button under the open window (phones).** On the S22 the window covers about the left third of the jump button; the arrow stays visible. The coordinator notes this is deliberate. Owner's call. It is normal for a full menu, so it is not a blocker.
2. **Small text that is not a blocker.** On the S22 the reward chips, the "!" alerts, SECRET, CLAIM ALL, the subtitle, BONUS and the count sit at 8 px. They read at 2x and are legible, so they do not block the 8.3 floor. Lifting them to 9 px would need the same container changes the owner has already been asked about.
3. **SECRET badge against the PERMAFROST name (S22).** The clearance is thin, about 1 px at the zoom I saw. It is clear, as measured by the builder, but it is tight. A 1 px move down would give more room.
4. **Glacier "!" on the S22 tab.** About 7 px, sitting on the tab corner. It reads as a red alert, which is enough.
5. **Glacier portraits look washed out (PC and phones).** The Ice Mammoth on the pale card is the clearest case. This is the review 2 NICE 2 item, still open, and it is the main reason the PC is 8.8 rather than higher. The builder's fix is a black outline or a 256 px downscale.
6. **Missing capture for the iPhone 13 placement.** Capture 27 is a window crop. A full-screen capture like 30 or 28b would confirm the top bar and bottom margin. If the placement is confirmed, the iPhone 13 score stays 8.4 until M1 is fixed.
7. **White labels on light fills** (CLAIMED! and CLAIM!) still rely on the black stroke. Unchanged since review 1.

## Review 4 status

| Review 4 item | Status |
|---|---|
| M1: BONUS text touching its pill | Fixed. Centred, clear on every phone. |
| Owner items 3-4 (card-name plates, chance pills) | Chance pills done (9 px on the S22, was 7). The wider window grew the names, but FROSTCROWN and PERMAFROST are still under 8 px on the S22: see M1. |
| Review 2 MUST (CLAIM! and CLAIM ALL edges) | Still fixed on all four phones. |
| Small-text owner decision | Still open. Now only the two names are below 8 px on the phones. |
