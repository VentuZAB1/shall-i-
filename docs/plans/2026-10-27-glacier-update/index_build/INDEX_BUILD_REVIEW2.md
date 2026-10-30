# Creature Index build review 2 (after review 1)

## Score

- **PC: 8.8 / 10** (passes the 8.5 bar)
- **Phone: 7.5 / 10** (below the bar)
- **Overall: 7.5 / 10** (the weaker platform, same rule as reviews 1 and 5)

## Verdict

**REVISE.** Overall 7.5 is below 8.5. The PC build is ready for the owner's yes on the CLAIM ALL colour (NICE 1). The phone needs one fix (MUST 1) and the owner's decision on small text (see "Owner decision").

## What works

- **Real device (capture 18, iPhone 17 Pro emulator, Roblox top bar on):** the window clears the top bar (top at 63.5 vs a 58 px bar) and the bottom edge (18.5 px). M2 and M3 are met on a real device.
- Tabs, grid, reward strip, footer and inspect panel are all present and in order. Nothing overlaps the Roblox HUD, the joystick or the jump button.
- **PC (captures 16 and 17):** no regression from the phone changes. The N3 header matches v8. The N4 unfound pill shows the area name only. The N5 silhouette has a single "???" name plate and no centre "?".
- **CLAIM ALL colour:** the fill is still the review 5 M1 burnt orange (200,88,0 measured in 16 and 17), with white-label contrast about 4.3 to 5.2:1. The build notes call it "amber"; that is wording only.
- **Numbers reconcile:** the emulator tabs add up to the 9/42 test save (1+0+1+1+0+0+6 = 9).

## Measurement notes

- The builder's "22 labels below 9 px" includes six "!" badges on tabs that are not claimable. In capture 18, only GLACIER shows a "!". The visible count is closer to 16. This does not change the verdict.
- The 844 x 390 mocks (14 and 15) draw text about 10 % larger than the real 749 x 381 view. Judge the phone from capture 18.

## MUST

**M1. CLAIM! and CLAIM ALL labels touch their button edges on the phone** (a regression from the M1 text floor). Capture 18: zoom on the reward strip (x 890-920, y 575-600) and the footer (x 800-925, y 565-655). The "!" of CLAIM! sits flush against the green button's right edge and appears cut. The count badge "1" on CLAIM ALL sits on the last "L".
- **Fix (same layout):** fit each label inside its button with at least 3 px clear on each side, lowering its cap a step if needed. Move the count badge 2-3 px up and right so it clears the letters. Re-check in the emulator. The boxes do not move.

## Owner decision: small text (not a MUST)

16 or more labels are still under 9 px at the real device size. The cheapest same-layout options are listed below for the owner to choose. Items 3-5 change containers on the shared layout, so they would also change PC, and the owner should decide them for both.

1. **Rarity pill** "GLACIER · MYTHIC · $x8.8" (6.7 px, width-limited): drop "MYTHIC" from the pill text, since the MYTHIC badge already shows on the card. This is a copy change.
2. **"Income (best KG)"** (5-6 px, row shared with its value): shorten the label to "Income". This is a copy change and gives the row room for a larger font. The builder should re-measure.
3. **Card names** FROSTCROWN DRAGON (6 px) and PERMAFROST TITAN (6.7 px, card width): widen the name plate to the card's full width with a 2 px inset, or shorten the names (the owner's call). Roblox TextLabels have no letter-spacing, so a tracking change is not an option.
4. **Chance pills** (7.4 px, pill height-limited): make the pill 2-3 px taller inside the card.
5. **"!" badges** (7.9 px, circle-limited): enlarge the circle by about 2 px.

**Is the phone ship-ready?** On placement, real-device verification and layout, yes. On the CLAIM! clip, no until MUST 1 is fixed. On text, no: it stays under 8.5 until the owner takes items 1-4 or accepts the small text in writing. If items 1-4 are taken, I expect the phone to reach the bar. The next review has to measure that.

## NICE

1. **CLAIM ALL colour needs the owner's yes.** It is a visible change from v8. Show capture 16 before Save and Publish. Correct the build notes from "amber" to "burnt orange".
2. **Glacier portraits look washed out** (no black outline, unlike the 30 older portraits). Ice Mammoth in captures 16 and 18 is the clearest case. The builder's report-only fix: add a black outline of about 6 px at 512, or upload a 256 px downscale. This is the highest-priority NICE, and I'd expect PC to reach 9.0 with it. That is an estimate, not measured.
3. **White labels on light fills** (CLAIMED! about 1.7:1, CLAIM! about 1.4:1) still rely on the black stroke. Unchanged from review 1 NICE 6.
4. **Phone tabs are about 31 px tall**, under the 44 px touch guideline. This follows from the one-layout rule; note it for the owner.
5. **BUILD_NOTES still says M3 "NOT done"** (notes saved 01:39, capture 18 at 01:41). Update the status to point at capture 18.

## Review 1 status

| Review 1 item | Status |
|---|---|
| M1 phone text floor | Applied where the box allows. The rest is the owner decision above. M1 regression: MUST 1. |
| M2 window bottom | Met on device (18.5 px clear). |
| M3 emulator capture | Done (capture 18). Notes not updated. |
| N1 CLAIM ALL colour | Kept at the review 5 M1 colour. Owner yes still needed. |
| N2 Glacier portraits | Report only, not fixed (NICE 2). |
| N3 header size | Done. |
| N4 unfound pill | Done. |
| N5 silhouette centre "?" | Done. |
| N6 white labels, N7 phone tabs | Not addressed (NICE 3 and 4). |
