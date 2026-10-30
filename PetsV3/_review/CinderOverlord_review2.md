# Cinder Overlord - MODEL GATE review 2 (2026-10-27) - REVISE

**Verdict: REVISE. Score 6/10** (review 1 was 5/10). Target to ship: 8/10 or better.

Round 2 fixed the two things that made it read wrong: it is no longer a magenta serpent (so it no longer copies the CosmicLeviathan's family), and it now reads volcanic (lava cores, gold crown, dark saddle) rather than candy. But three new problems came with it, and the pet still does not outclass the Phoenix, Ivonrath, ThunderRex or CosmicLeviathan:

1. The obsidian saddle overshot. In game the obsidian is 53.5 % of the surface and the wine body only 28 %, so the body is no longer the main colour and the 3-band read collapses into dark on dark.
2. The eyes disappeared from the front. The rose slits are not visible from the front in round 2 (round 1 showed them), so the face reads as two black marks.
3. The muzzle front is still a blunt square, not a wedge. The side profile is now a good crocodile wedge, but the front view is a rounded dome.

Do NOT send it to the clip gate yet.

## 0. What I looked at

- Round-2 notes: `CinderOverlord/MODEL_NOTES.md` (the "ROUND 2" section, items M1-M8, N1-N5) and the rulings requested.
- Renders in `CinderOverlord/renders/`: `_model_sheet.png`, `_close_sheet.png`, `close_front.png`, `_icons_strip_128.png`, `_icons2_strip_64.png`, `flat_side.png`, `flat_tq.png`, `flat_game.png`, `gamelook_game.png`, `gamelook_tq.png`, `_pose_crown_sheet.png`.
- Round 1 comparison: `_review/CinderOverlord_review1.md`, and my own round-1 close-up reading (the pink eye slits were visible from the front then).
- Source: `pets/CinderOverlord.py` (constants at lines 15-27, `RAD` line 40, `FRAD` line 47, dorsal saddle call lines 253 and 271, skull loft `SKS` lines 312-315, cap lines 317-323, eye code lines 352-360).
- Icon strips were judged at native size (no image tool is installed to upscale them). The 64 px read is from the 64 px strip itself.

Not reviewed: clip gate (no clips yet). The 11,124 tris, the 0-collision crown poses and the strict share numbers are the builder's own counts. I did not re-measure them.

## 1. Round-1 items, checked

| Item | Status | Note |
|---|---|---|
| M1 body off the Leviathan magenta | PASS (with a new problem) | oxblood (144,80,96), H 345, is not pink and is 45 deg from the Leviathan's H 300. The obsidian overshoot (M3 below) is the new problem. |
| M2 crown not a tiara | PASS | gold on the upper edges and the centre blade's sides; the gold count is 28 px at 64 px (gate 25). |
| M3 Fire read (lava cores, tail tip) | PARTIAL | visible on the flanks in `flat_side` and the 128 strip, and on the tail tip. At 64 px the orange is barely there (MUST 5). |
| M4 rose ~6 % | PASS | rose 6.6 % side / 7.0 % game, plus lava 1.1 % in game. Visible in `flat_side`. |
| M5 head not a brick | PARTIAL | the side profile is a clear wedge (PASS). The front is still a blunt rounded square, and the eyes are lost from the front (FAIL, MUST 1 and 2). |
| M6 bulk +15 % | PARTIAL | `RAD[0..4]` raised as stated. The lower body still reads as a thin worm in `gamelook_game` (MUST 4). |
| M7 pale underside | PARTIAL, ruled | side 7.7 %, tq 9.5 %. Visible in `flat_side`, `flat_tq`, and the throat in `gamelook_tq`. Not visible in the high `gamelook_game` (ruling 3). |
| M8 BlackDragon in strips | PASS | second after the Cinder in the 128 and 64 strips. |
| N1 tail rings thinner | PASS (not checked in detail) | the tail reads thinner. |
| N2 beams thinned | PASS | the nasal ridge is a thin line on the muzzle tip; the crown mount reads as two tapered halves. |
| N3 brow points | PASS | the V brows read in `_close_sheet`. |
| N4 eye slits wider | FAIL (regression) | the slits are wider (0.085), but they do not show from the front. Only two black socket marks show (see MUST 1). |
| N5 crown molt check | PASS (visual) | `_pose_crown_sheet.png` shows the five blades lifting and bowing with no visible overlap. Collision numbers not re-checked. |

## 2. Numbers

| Colour | side | tq | game | Target |
|---|---|---|---|---|
| PLUM_OBS (body) | 45.9 | 39.6 | **28.0** | body must be the main colour: game >= 40 % |
| OBS_D (obsidian) | 30.0 | 31.6 | **53.5** | game <= 40 % (plan was 16 % side) |
| PALE_S | 7.7 | 9.5 | 0.6 | side / tq 7-10 %; game not gated (ruling 3) |
| ROSE + ROSE_H | 6.6 | 5.6 | 7.0 | ~6 % |
| LAVA | 1.7 | 1.1 | 1.1 | < 2 % (fine) |
| GOLD + GOLD_D | 2.2 | 6.5 | 5.4 | 3 % (fine) |
| Gold at 64 px | portrait 28 | | game cam 19 | >= 25 (portrait) |

The body is the wine colour (luma ~101, so it passes the luminance clause of the rule). The problem is not the body value. It is that the obsidian saddle takes the body's place in the game view.

## 3. Rulings on the three deviations

**(1) Body (144,80,96) oxblood + obsidian saddle + obsidian skull cap: ACCEPTED IN PRINCIPLE, two parts need correction.**
- The hue is right: oxblood H 345 is off the Leviathan's magenta by 45 deg, and it no longer reads pink. Accepted.
- The skull cap hides the eyes from the front (MUST 1). Accepted only with that fixed.
- The saddle overshot in game (MUST 3). Accepted only with its width reduced.
- Note: oxblood H 345 is 11-16 deg from Ivonrath's crimson and dark (H 1 and H 356). The two are separated by saturation (Cinder S 0.44, Ivonrath S 0.79) and by silhouette. Keep the lineup check (NICE 2).

**(2) Lofted wedge skull, squared muzzle (the kit caps rounding at 0.45): ACCEPTED for the side profile, REJECTED for the front.**
- The side profile (`_close_sheet` middle panel, `flat_side`) is a clear crocodile wedge. That is a real fierce gain over round 1's box.
- The front view (`close_front.png`) is a rounded dome with a blunt muzzle. The muzzle tip is 0.080 wide and 0.052 tall (`SKS` last station, line 315), which is still a rounded block at 5 studs (MUST 2).
- The stated reason (the 0.45 rounding cap) I could not confirm from `blockkit.py`: the grep finds the 0.45 only in an offset clamp, not in the rounding. The loft is accepted on its visual result, not on that reason.

**(3) In-game pale 0.6 %: judge the 3-band from `gamelook_game.png`. ACCEPTED as a method, but the 3-band currently FAILS on it.**
- The high rear camera cannot see the belly, so the game pale share is not a fair gate. Accepted.
- The pale throat is visible from the 3/4 view (`gamelook_tq`), and the belly from the side (`flat_side`). That is the third band, where it can be seen.
- But judged from `gamelook_game`, the read is dark maroon, near-black obsidian and gold. The wine flanks and the obsidian saddle merge, so the game 3-band reads as two bands. That fails until MUST 3 lands.

## 4. Questions from the coordinator

**Does it read as Fire?** Partly. It reads volcanic: lava orange on the flanks and the tail tip, a dark obsidian back and a gold crown. At 128 px and in close-ups the Fire family is clear. At 64 px the lava is too small to carry it (MUST 5), so the icon reads "dark red serpent with gold crown".

**Does it outclass Phoenix (2 %), Ivonrath (4 %), ThunderRex (1 %) and CosmicLeviathan (1 %)?** Not yet.
- InfernoPhoenix: no. The Phoenix is brighter, more flame, and has a stronger silhouette at 64 px.
- Ivonrath: no on impact, yes on rarity. The red wyrm with wings is brighter and wider.
- ThunderRex: no. The Rex is heavier, more saturated (blue with cyan crystals), and reads bigger.
- CosmicLeviathan: no on mass and impact. The Cinder is now distinct from it (the hue is 45 deg apart and it has no magenta), so the distinctness gate passes. But the Leviathan has more mass and fins, and the Cinder is the darkest pet in the lineup at 64 px.

The Cinder is the darkest and lowest-contrast Fire pet in the strip. Against the dark slate icon background it recedes. For a 0.5 % pet, that is the opposite of outclassing.

**Fierce or cute?** Fierce on the side profile (no pink, a wedge skull, a dark back, fangs). The front face is blank (the eyes are lost), so the face does not read as a predator at 5 studs. Fixed by MUST 1 and 2.

**Most impressive pet of the Fire egg?** No. InfernoPhoenix and Ivonrath read more striking at 64 px. The Cinder has to become the most imposing of the egg, and it is not yet.

## 5. MUST list (prioritized)

**MUST 1 - The eyes are lost from the front (regression from round 1).**
- In round 1 the rose eye slits showed as pink triangles beside the brows in the front close-up. In round 2 the front shows only two black socket marks (`close_front.png`).
- The likely cause: the obsidian skull cap (lines 317-323, `aa, ab = 55 deg, 125 deg`) covers the eye slits at the cap's lower edge. The eye code (lines 352-358, `ep`, `en`, the socket at 0.098 wide) sits right at that edge.
- Fix: raise the cap's lower edge clear of the eyes. Change the lower angle `aa` from 55 deg to about 65 deg, so the cap stops above the eye line. Push the rose slit proud of the skull by about 0.010 (the `ep + en * 0.008` offset at line 357 to about 0.018). Keep the socket.
- Verify: `close_front.png` must show two pink slits at 5 studs, not only black marks.

**MUST 2 - The muzzle front is a blunt square, not a wedge.**
- The last loft station `(1.0, 0.080, 0.052, -0.036)` at `SKS` (line 315) leaves a 0.16 wide, 0.10 tall muzzle tip. From the front that is a rounded block.
- Narrow the last station to about 0.055 half-width and 0.040 half-height, and the one before it (`0.96`, line 314) to 0.070 / 0.048, so the front tapers to a V.
- Verify: the front view (`close_front.png`) reads a wedge: the cheeks wider than the muzzle tip, and the muzzle tip narrower than the eyes apart.

**MUST 3 - Obsidian overshoot: the saddle takes the body's place in game.**
- Game shares: OBS_D 53.5 %, PLUM_OBS 28.0 %. The obsidian is the main colour; the body is the accent. The rule is the reverse: dark rich body, pale underside, one accent.
- The saddle is `dorsal(a, b, ..., 32 if i < 5 else 26)` at line 253, and the neck saddle `dorsal(..., 32, up=(0,1,0))` at line 271. Each is a 64 deg band around the top of every segment.
- Narrow the body saddle half-angle from 32 to about 18 deg on Spine to Body4, from 26 to 16 deg on Tail1-4, and the neck saddle from 32 to about 20 deg. Keep the rings (they drop down the flanks) and the obsidian skull cap.
- Target game shares: PLUM_OBS >= 40 %, OBS_D <= 40 %. Re-run the strict share script and re-render `gamelook_game.png`.
- Note: this also fixes the 3-band read in game without asking for a lighter body (which would reintroduce pink).

**MUST 4 - The lower body still reads as a worm.**
- Round 2 raised `RAD[0..4]` by 15 % (line 40). In `gamelook_game` the middle and rear body are still a thin worm, which is why it does not outclass the Rex or the Leviathan.
- Raise `RAD[1..3]` by about 10 % more: Body1 0.250 to 0.275, Body2 0.230 to 0.250, Body3 0.205 to 0.225. Leave the tail (`RAD[5..9]`) as it is, so the taper stays.
- Re-check the vents and forearms after the change (the vents are placed from the radii, the forearms from line 259-265).

**MUST 5 - The Fire read at 64 px.**
- At 64 px the lava hot cores are too thin to show. The vent hot core is `w * 0.38` (line 187). Raise it to `w * 0.50` so the orange line reads at icon size.
- The crown centre gem is still ROSE_H, the pale pink (line 24 and the `gem=(i == 2)` call at line 380). Change the gem to LAVA (255,128,24), so there is one warm spark at the top of the icon.
- Verify on `_icons2_strip_64.png`: an orange spot must be visible on the Cinder's crown and flank, not only at 128 px.

## 6. NICE list

1. **Outer crown gold tops are wide.** The gold on blades 1 and 5 is the widest of the five, so the crown still reads as a yellow tiara from the front. Narrow the outer blades' gold top half to about 0.020 (round 2 has 0.025).
2. **Ivonrath hue proximity.** Oxblood H 345 is 11-16 deg from Ivonrath's crimson. Keep the saturation gap (S 0.44 against 0.79) and check the lineup at 128 px. If the portrait starts to read as "red Ivonrath", move the body hue to about H 335 (for example (144,84,100)).
3. **Game camera gold is 19 px.** Fine for the crown read, but the crown is the hero. If MUST 3 leaves the crown too small in `gamelook_game`, lift the gold on the centre blade's sides.
4. **Belly pale in the game camera.** Not gated (ruling 3). If the owner wants a pale band from above, do it with the throat ladder (already visible in `gamelook_tq`), not with a lateral pale stripe, which would run into the vents.

## 7. Pass / fail checklist (round 2)

| # | Check | Result |
|---|---|---|
| 1 | Tris <= 15k | PASS (11,124, builder's count) |
| 2 | Height 10.5 >= Rex and Leviathan (10.0) | PASS on the number |
| 3 | Silhouette at 64 px: the species reads (serpent, crown) | PASS |
| 4 | Face reads at 64 px (eyes, muzzle) | FAIL (eyes not visible) |
| 5 | Face reads at 5 studs (front close-up) | FAIL (eyes lost, muzzle blunt) |
| 6 | Fierce, not cute | PASS on the side profile; FAIL on the front face |
| 7 | Dark rich body is the main colour (game) | FAIL (obsidian 53.5 % vs body 28 %) |
| 8 | Three bands readable in game (`gamelook_game`) | FAIL (dark on dark); PASS from the 3/4 view (throat) |
| 9 | One bright accent (rose) strong enough in game | PASS (rose + lava 8.1 %) |
| 10 | Gold hero readable at 64 px, >= 25 px | PASS (28) |
| 11 | Fire-egg identity reads | PARTIAL (volcanic at 128 px; too weak at 64 px) |
| 12 | Distinct from CosmicLeviathan (1 %) | PASS (45 deg hue apart, no magenta) |
| 13 | Distinct from Ivonrath (4 %) | PARTIAL (oxblood 11-16 deg; saturation and silhouette separate them) |
| 14 | Outclasses ThunderRex (1 %) at icon size | FAIL |
| 15 | Outclasses CosmicLeviathan (1 %) at icon size | FAIL (distinct, but thinner and darker) |
| 16 | Outclasses InfernoPhoenix (2 %) and Ivonrath (4 %) | FAIL (not the most impressive Fire pet) |
| 17 | Parts floating, poking, or wrong from below | PASS (visual; crown and claws sit on their bones) |
| 18 | Icon gate incl. BlackDragon (64 / 128) | PASS |
| 19 | Clip gate | NOT REVIEWED (no clips yet) |

## 8. Next round

Send with the fixes applied:
- `close_front.png` and `_close_sheet.png` (the eye and muzzle check, MUST 1 and 2);
- `gamelook_game.png` with the new strict shares (the 3-band check, MUST 3 and 4);
- `_icons2_strip_64.png` and `_icons_strip_128.png` (the 64 px orange, MUST 5, and the lineup);
- the strict share numbers for PLUM_OBS and OBS_D in game.

The clip gate starts after this model gate passes at 8/10.
