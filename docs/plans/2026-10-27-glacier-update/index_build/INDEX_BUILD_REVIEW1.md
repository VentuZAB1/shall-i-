# Creature Index build review 1 (Glacier update, v8 build)

## Score

- **PC: 8.7 / 10**
- **Phone: 7.5 / 10**
- **Overall: 7.5 / 10** (the weaker platform, same rule as review 5; the 8.5 bar applies to each)

## Verdict

**REVISE.** Overall 7.5 is below 8.5. The PC build is close to v8. The phone is not ready: its text is too small and the window sits too low.

## What works

- Layout, colours and proportions match v8 at the same scale. Window, tab column, header, 2 x 3 grid, reward strip, footer and inspect panel are all in place.
- States are right:
  - Claimed (06): CLAIMED! pill, gold star on the tab, full bar, no BONUS pip.
  - Unfound (05): dimmed cards with "?", SECRET and MYTHIC badges kept on unfound cards.
  - Mythic in another area (04): Cinder Overlord, rainbow edge, white select frame, "2 LEFT".
  - SECRET (02): gold card, pink SECRET badge, SECRET pill in the inspect panel.
  - Common (03): "GLACIER · $x1.3" pill, no rarity word.
- Pets: at 2x side by side with v8, Ice Mammoth, Glacier Yeti, Permafrost Titan and Frostcrown fill their cards within about 5 % of the mockup.
- FROSTCROWN DRAGON fits on one line, with about 8 px clear each side (review 5 NICE).
- Review 5 MUSTs met:
  - CLAIM ALL contrast: white label on the new fill measures about 4.3:1 at the top and 5.2:1 at the bottom.
  - PC: "!" moved and clears the R.
  - Phone: window top is below the top bar (y 64 vs a 58 px bar; y 42 vs 36 px).
- No clipping or overlaps found in any capture (names, badges, pills, tabs).
- Discovered 32/42 is correct. The v8 mock says 33, but its tab counts add up to 32.

## Differences from v8

| Difference | Matters? |
|---|---|
| CLAIM ALL: amber in v8, now burnt orange (review 5 M1) | Intended. It is a visible change, so the owner needs to say yes (see NICE 1). |
| Ice Mammoth portrait looks faded and translucent on the pale card | Yes, a little. It is the hero pet on the default tab (NICE 2). |
| "GLACIER CREATURES" title and subtitle about 7 % smaller | Minor (NICE 3). |
| Window 881 px wide vs 903 in v8 (58 % PC cap) | Minor. Everything is about 2 % smaller. |
| Tab labels a little lighter in weight | Minor. |
| Discovered 32 vs 33 | No. The build is right. |

## MUST (blockers)

**M1. Phone text is too small (fix inside the same layout).** Capture 07 (and 08). Measured on the 844x390 capture: inspect stat labels (Income (best KG), Best weight, Hatched, Hatch chance) and card names are about 7-8 px cap height. The chance pills and the "COMPLETE GLACIER" label are about the same or smaller. Review 5's bar was 9 px cap.
- Fix: enlarge each of these inside its existing box until the text fills about 70 % of the box height or runs out of width. Do not move or rearrange anything.
- Any label that still cannot reach 9 px cap goes to the owner as the 12 px decision (the build notes already flag it). Do not ship the phone with that decision open.

**M2. Phone window sits too low at the bottom.** Capture 07 and 08. The window outline ends at about y 384, about 6 px above the 390 px edge. Review 5 H1 asked for the bottom at y 372, and the footer content already ends near y 372.
- Fix: on the phone, set window height = screen height - (top bar + 6) - 18. That gives 308 px with a 58 px bar (top y 64, bottom y 372) and 330 px with a 36 px bar. It is the same layout, about 4 % smaller, so do M1 after it.

**M3. The phone is not verified on a real device view.** Captures 07 and 08 are a canvas mock; the build notes say so, and no Device emulator run was done. The mock does not show Roblox's real top bar, home bar or real text rendering.
- Fix: after M1 and M2, capture in Studio's mobile Device emulator at 844x390 with the top bar on: Index open on Glacier, one selected card, and the inspect panel. Check the top bar, the bottom edge and text legibility on that capture. The phone stays at 7.5 until this is done.

## NICE

1. **CLAIM ALL colour needs the owner's yes.** It changed from v8 amber to (200,88,0) to (190,68,0). That follows review 5 M1, but the owner rule says visible UI changes need the owner to see them first. Show capture 01 before Save and Publish.
2. **Ice Mammoth looks washed out** (captures 01 and 03, zoomed 4x). Its armour lacks the dark detail of the v8 pet, so it looks translucent against the pale card. Check the uploaded PNG for semi-transparent pixels. If it has them, upload the solid render that v8 used. Frostfang Lynx is also a little greyer than v8.
3. **Header text about 7 % smaller** than v8 ("GLACIER CREATURES" and "Hatched from the Glacier Egg"). The header has room, so restore the v8 size.
4. **Unfound inspect shows the bonus.** Capture 05: the "???" creature shows "CELESTIAL · $x2.4", which gives away its money bonus. Show only the area name until the creature is found.
5. **Double question mark on silhouettes.** The "???" name plate and the centre "?" both show. Keep one.
6. **Low-contrast white labels.** CLAIMED! (white on silver, about 1.7:1), CLAIM! (white on lime, about 1.4:1) and the "5 / 5" pill rely on the black stroke. Same as v8, so not a blocker. Darken the fill or the stroke if you want more margin.
7. **Phone tabs are about 30 px tall**, under the 44 px touch guideline. This follows from the one-layout rule, so it is a note for the owner, not a fix.
