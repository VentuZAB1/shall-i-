# Creature Index build review 3 (after review 2 and the lead's MUST fix)

## Score

- **PC: 8.8 / 10** (passes the 8.5 bar; unchanged since review 2)
- **Phone: 7.8 / 10** (below the bar)
- **Overall: 7.8 / 10** (the weaker platform, same rule as reviews 1 and 2)

## Verdict

**REVISE, for the phone only.** PC passes. The review 2 MUST is fixed. What holds the phone back is the owner's open decision on small text, plus NICE items that the owner also sees. No MUST is left on the build itself.

## What works

- **Review 2 MUST fixed (capture 21 against 18).** CLAIM! now sits inside its green button with clear space on both sides. In 18 its "!" was cut at the edge. CLAIM ALL sits inside its orange button, and the count badge clears the letters.
- **Reward chips** "+5%" and "x1" are one size and one line. In the regression capture (19c) they wrapped; that is gone.
- **Layout and placement** are as in review 2: the window clears the top bar and the bottom edge, and nothing overlaps the Roblox HUD, joystick or jump button.
- **Colour:** the CLAIM ALL fill is the review 5 burnt orange on both platforms (200,88,0 on PC, about 192,80,0 on the phone), so the contrast fix is still in place.
- **Measured clearances** (builder: CLAIM! 6.2 px, CLAIM ALL 7.3 px each side). My read of capture 21 at 6x is about 6-9 px for CLAIM! and about 7-10 px for CLAIM ALL. Consistent.

## MUST

None on the build. The round 2 MUST is fixed, and I found no new clipping or overlap in capture 21.

## Owner decision: small text

The phone still has about 20 visible labels under 9 px at the real device size. The lead's fix put CLAIM ALL, the four chips and the count digit back to the PC proportion, so they are now about 8 px. The rest is as in review 2. This is still the owner's call.

Scores by option (my estimates, not measured):

| Option | Phone | Still under 8.5? |
|---|---|---|
| Build as it is (small text open) | 7.8 | Yes |
| Owner accepts the small text as it is | about 8.1 | Yes |
| Owner takes cheapest items 1-4 (below) and they are measured | about 8.4 | Yes |

**Is the owner decision the only thing between the phone and 8.5?** No. Even with the text accepted, I rate it about 8.1, for three reasons:
- The phone tabs are about 31 px tall, under the 44 px touch guideline. The one-layout rule limits this.
- CLAIM ALL is about 8 px, smaller than the DISCOVERED line beside it. On PC the two match. The footer's main action now reads weakest.
- The Glacier portraits look washed out (NICE 2). This is also on PC, which is why PC is 8.8 and not higher.

**Cheapest items 1-4** (from review 2, for the owner to choose):
1. Rarity pill: drop "MYTHIC" from the text, since the MYTHIC badge already shows on the card. A copy change.
2. "Income (best KG)": shorten to "Income". A copy change; the row is shared with its value.
3. Card name plates: widen to the full card width with a 2 px inset, or shorten the long names (owner's call). This is the only one that can bring the names near 9 px. Roblox TextLabels have no letter-spacing, so tracking is not an option.
4. Chance pills: make them 2-3 px taller inside the card.

These are container changes on the shared layout, so they change PC too. The owner should decide them for both platforms.

## NICE

1. **CLAIM ALL vs DISCOVERED on the phone.** Capture 21 footer: the DISCOVERED line keeps the review 1 floor and is larger than CLAIM ALL. On PC they match. The owner should choose which one moves.
2. **Footer small text has a thin outline.** The chips and CLAIM ALL keep a thin outline at 8 px. They are legible, but they are the softest text in the footer.
3. **Glacier portraits look washed out** (review 2 NICE 2, report only). The builder's fix is a black outline of about 6 px at 512, or a 256 px downscale. This affects PC too.
4. **White labels on light fills** (CLAIMED! about 1.7:1, CLAIM! about 1.4:1) still rely on the black stroke. Unchanged from review 1 NICE 6.
5. **Tests not verified by me.** The notes report 60/60 and say v8claim and legacy were not re-run. I have no Studio access, so I have not checked these.

## Review 2 status

| Review 2 item | Status |
|---|---|
| MUST 1: CLAIM! and CLAIM ALL edges | Fixed (capture 21). |
| Owner decision: small text | Open, owner's call. |
| NICE 1: CLAIM ALL colour owner yes | Open, owner's call. |
| NICE 2: Glacier portraits | Open, report only. |
| NICE 3: white labels on light fills | Open. |
| NICE 4: phone tabs about 31 px | Open, note for owner. |
| NICE 5: BUILD_NOTES M3 status | Done. Notes now say M3 is done (capture 18). |
