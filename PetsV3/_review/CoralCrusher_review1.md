# Coral Crusher - model gate review 1 (2026-10-27) - REVISE

**Score: 6/10 for a 15 % Medium (ship bar 8).** The crab reads as a crab with a clear signature: two raised claws with rose
spikes, a bronze dome and heavy slate brows. The eyestalks no longer read as a snail, so the plan-review "childish" concern is
solved. Seven things still hold it back, and four of them change geometry or the walk. **No clips yet.** Fix M1-M4 in the model,
then re-run the walk build gate on the new legs. Then send round 2 with everything at once.

## What I looked at
- `pets/CoralCrusher.py` (504 lines): carapace L29-33 and L150-158, eyes L189-205, mandibles L206-210, claws L214-281,
  legs L282-294, stud skin L304-305, walk constants L377-386
- `CoralCrusher/MODEL_NOTES.md`, `_review/CoralCrusher_plan.md` v2, the GLACIER_PLAN_REVIEW section 2.8 and the owner decisions
- `renders/`: `_model_sheet.png`, `_close_sheet.png`, `close_front/high/tq.png`, `model_side/front.png`, `flat_side/tq/game.png`,
  `gamelook_game/tq.png`, `_walkgate_sheet.png`, `_icons_strip_64/128.png`, `_icons2_strip_64/128.png`
- The comparison pets: Kappa, SeaTurtleWarrior, Kraken, HammerjawShark and AbyssalOrca (model sheets and icon strips), AbyssWeaver
  `_model_sheet_600.png`, and `_ALL_FIERCE_progress.png`
- Vault rules: Creature Style, Model Review Checklist, Creature Animation
- Note: `_walkgate_sheet.png` and `_pose_tq_sheet.png` are byte-identical (same md5). Only the walk and act-wave prototype
  poses exist so far. There is no full clip set yet.

## Value shares (checked)
I re-measured the flat renders against the palette IDs. The flat renders carry (1,1,1) speckle on the background (not pet
pixels). When I drop that speckle, the builder's numbers reproduce (side: bronze 50.3, shell_d 34.9, rose 6.3, belly 0.8-1.2).
Fix the sampler, not the model.

| view | BRONZE | SHELL_D | ROSE + ROSE_D | BELLY_PALE | plan (side) |
|---|---|---|---|---|---|
| side | 50 | 35 | 6.3 + 2.4 | **1.2** | 40 / 14 / 8+3 / 8 |
| tq | 49.5 | 31 | 6.7 + 2.6 | 3.7 | |
| game | 57 | 29 | 5.7 + 3.9 | 0.4 | |

Size: 9,932 tris (cap 15k). HEIGHT 7.5 studs to the top of the raised claws. Legs: the leg chain is about 0.5H, which is about 1.8x
the plan's 0.30H.

## 1. Review-plan items
1. **Eyes / stalks: PASS.** The stalks are now short and sunk under slate lids, and the rose slits read as angry, not googly.
2. **Face: PARTIAL.** The lids and slits pass. The mandibles fail (M3). The four dark front bars read like a moustache (N1).
3. **64 px read: PARTIAL.** The game-camera icon reads as a crab. The portrait icon fails (M5). The dark legs make it borderline spider.
4. **Rose accent: FAIL at 64 px.** About 9 % of the pet is rose, but in the 64 px strip it is a few pink specks (M6).
5. **Hard rules: PASS** (no Neon, no glow, studded body, smooth details, 9.9k tris, nothing floating in the renders). The
   **pale underside fails** (1.2 % side vs plan 8 %; see M4).
6. **Walk / build gate: PARTIAL.** The tripods are correct (N6). The 90° turn is a risk (M1), and the legs need the change in M2.

## 2. Deviations (builder's list)
1. **Colours deepened** (BRONZE 196,150,104 to 186,124,80; SHELL_D to 100,66,46): **ACCEPT.** The brightest channel stays above 170,
   and it is needed for the Roblox 0.6x darkening. The copper lift is a NICE item (N4).
2. **Claw asymmetry** (crusher x1.20 / cutter x0.98): **ACCEPT.** It is hard to see in the front view, so make it obvious: keep
   the crusher palm at x1.20 and check it in the side and 3/4 views.
3. **Legs about 2x (as built about 1.8x) the plan length:** **REJECT as built.** The legs are long dark stilts. The knees arch to
   z 0.37 BU (about 0.29H), above the shell underside (about 0.26 BU, about 0.20H). That is spider stance, not a crab. Fix M2.
4. **Walk turns the shell 90° (yaw +90) and relies on the 0.3 s crossfade:** **NOT ACCEPTED as built.** Crabs do walk sideways, so
   the idea is right. But a 90° body turn inside about 0.3 s is about 300° per second, and it will read as a snap-spin every time
   a pet starts or stops walking (the game moves pets; they wander a lot). Fix M1.
5. **Additions** (rim band, pale lip, rose coral growths, leg top plates): **ACCEPT.**

---------------------------------------------------------------------------------------------------------------------
## 3. MUST (before clips; in priority order)

### M1 - The walk turn: no 90° snap (YAW_WALK L385; crossfade note L378-380)
Pick one of these two and say which:
- **A (preferred):** keep yaw 90 but add a **pivot clip** `turn_to_walk` (about 0.6-0.8 s, 18-24 f each way): the shell rotates
  in place, all six feet planted, the crusher leads, and the tripod pattern starts only after the turn is done. The game then
  plays the pivot before the walk. If the CreatureAnimator cannot chain a clip, ask the lead to add the hook. The plan asked for
  this kind of build gate anyway.
- **B:** yaw 45 (a diagonal scuttle). The crossfade is then 45° (about 150° per second), which is halved and reads as a scuttle,
  not a spin.
- Either way, send a **9-frame sheet of the idle-to-walk crossfade** (yaw 0 to walk, every 2-3 frames over 0.3 s) with the feet
  planted. That is the real test.

### M2 - Legs: shorter, lower knees, less dark mass (LEGP L38-40; coxa/merus L288-293)
- Knee z: **0.37 to 0.30 BU**, so it stays under the shell's underside line (about 0.26 BU). Pull the knee outward, and bend it
  low, not up.
- Leg chain: **0.5H to about 0.38H** (about 1.25x the plan). Keep the hip under the shell edge and the shell underside at
  **0.20H (about 0.26 BU at H 1.29)**. Do not raise the shell to fit long legs.
- Merus (L289-293): **SHELL_D (100,66,46) to BRONZE_D (146,96,62)** so the dark slate sits only on the propodus and the black tips.
  Target: SHELL_D at 20 % or less of the side view (now 35 %).
- Coxa stays SHELL_D. The rose spike on the merus (L294) stays.
- Re-run the walk build gate after the change. Target: collision_free true, `ground_min_z` >= -0.02, slide 0, tripods unchanged.

### M3 - Mandibles read as buck teeth (L206-210)
The two BELLY_PALE plates (`(0.030, 0.012, 0.052)` at x +/-0.050, z 0.330) with IVORY teeth are big white blocks from the front
(close_front, model_front). That is the most "cartoon" thing on the face.
- Shrink to about **0.020 x 0.034**, change the colour to **SHELL_D (100,66,46)** with **IVORY tips only** (two small hooked teeth,
  0.012 long), and pull them in to x +/-0.030 under the brow plate.
- Target: no pale block bigger than 2 % of the front view. The black MOUTH slot (L207) stays.

### M4 - Armour and pale underside (carapace L153-170; pale lip L155-157)
- **(a) Armour:** the dome is smooth bronze with thin seams. The Turtle reads more armoured, and the plan says the crab must too.
  Raise the three H-groove ridges (`bar_on`, thickness 0.007, L160-170) to **plates**: thickness 0.007 to **0.022**, 0.02 BU
  proud. Add one **stepped rear plate** on the rim at the mid station, a little higher than the rim band.
- **(b) Pale underside:** 1.2 % side (plan 8 %). Widen the **pale lip (L157) from 0.030 to 0.050** and drop it by about 0.02 so it
  shows as a cream edge from the side. Keep the sternum (L155). Target: **BELLY_PALE at 5 % or more** of the side view, and at
  least 4 % in tq.

### M5 - The portrait icon is a flat slug (first item of all four strips)
In `_icons_strip_64/128` and `_icons2_strip_64/128`, the first item (the kit portrait) reads as a low tan lozenge with spikes,
not a crab. The game-camera icon (second item) does read as a crab. Either:
- re-frame the portrait camera higher (about 35-40° elevation) and closer, so both claws and the legs fill the frame; or
- ship the game-camera icon as the portrait.
Re-render all four strips and check the crab reads at 64 px next to Kappa, Turtle, Kraken, Hammerjaw and Orca.

### M6 - Rose accent is too small at 64 px (claw spikes L223, L226, L262, L281; margin teeth L172-178)
- Claw outer spikes: length **0.075c to 0.10c**, width **0.026c to 0.034c** (L223, L262, L281). The carpus spike (L226) to
  0.10c as well.
- Carapace margin teeth (L172-178): about **1.3x** length.
- Keep the ROSE_D bases. Target: **ROSE + ROSE_D at 10 % or more** of the side view (now about 9 %). In the 64 px strip, the claw
  spikes should show as pink points, not specks.

### M7 - Check the glassy halo (eye bulbs L194-196; lid L200; claw shoulder L219)
In `close_high`, `close_tq` and `close_front`, a faint semi-transparent outline shows around each eye lid and each claw
shoulder. It is most likely the smooth BRONZE eye bulbs and shoulder blocks sitting proud of the studded skin (no stud skin on
them). But check for inside-out or coplanar faces too. Backface culling is on in game, so a flipped face disappears from the
player's side. Fix or confirm in writing, and say which.

---------------------------------------------------------------------------------------------------------------------
## 4. NICE (do these too)

- **N1 Front brows:** the four dark bars (two lids plus the two central V bars, L202-204) read like a moustache. Merge the
  centre pair into one **slate V brow plate** (about 0.14 wide, one piece).
- **N2 Claw keels:** the white palm and merus strips (L255, L258-259) read as plastic inserts in the front view. Make them
  **SHELL_D**, or drop them.
- **N3 Rest claw height:** the claws sit about 50-60° up in the rest pose (CLAW, L43-44). Drop the rest about 15° so the act's
  60° wave reads as a lift, not a boxer's guard.
- **N4 Copper lift:** BRONZE (186,124,80) gives a game colour of about (112,74,48), a chocolate. Try **(200,136,88)** so the game
  colour is a warmer copper. Still over 170 in the brightest channel.
- **N5 Rose lightness:** ROSE (255,120,150) goes dusty mauve at 0.6x (about 153,72,90). Try **(255,135,165)**, which keeps the
  hue about 350 and stays clear of the Wyrm's hot pink.
- **N6 Walk tripods: PASS.** Leg_1/3/5 (L front, R middle, L back) and Leg_2/4/6 (L middle, R front, R back) are proper tripods,
  and `WALK_OFF` (L386) matches.
- **N7 Armour vs Turtle:** once M4 lands, check the lineup. The crab should read as more armoured and more interesting than
  SeaTurtleWarrior (25 %), and it should not look like a brown rock beside the teal pets.
- **N8 Next-round deliverables:** the tq/front/side/back renders (the model sheet is four 600 px panels), the close sheet, the
  two icon strips with the comparison pets, the crossfade sheet (M1), and the walk frames after M2.

---------------------------------------------------------------------------------------------------------------------
## 5. Pass / fail checklist

| # | check | result |
|---|---|---|
| 1 | Silhouette at 64 px: the species reads instantly | PARTIAL (game-camera icon yes, portrait no: M5) |
| 2 | Crab, not a bug or spider | **FAIL** (legs: M2) |
| 3 | Fierce, not cute (no stalks, slits, brows, no glint) | PASS, except the buck-tooth mandibles (M3) |
| 4 | No box belly; belly line rises to the legs | PASS (domed loft; the tuck is the pale lip, see M4) |
| 5 | Dark body + pale underside + ONE accent | PARTIAL (dark body and accent pass; pale underside **FAIL**, M4b) |
| 6 | Rose accent reads at 64 px and in game | **FAIL** at 64 px (M6); PARTIAL in game |
| 7 | Armoured, more interesting than the Turtle | **FAIL** (smooth dome: M4a) |
| 8 | Hard rules: studs on body, details smooth, no Neon, <= 15k tris | PASS (9,932 tris) |
| 9 | Floating, intersecting or see-through parts | PARTIAL (halo check: M7) |
| 10 | Palette shares reproduce from flat renders | PASS (after excluding background speckle) |
| 11 | Walk: legs planted, tripods, no snap | PARTIAL (tripods pass; turn **FAIL**: M1; legs: M2) |
| 12 | Deviations accepted only where better | Colours ACCEPT; claw asymmetry ACCEPT; legs REJECT; walk turn NOT ACCEPTED |

Round-2 target: **8/10 or better**, with M1-M7 done and the walk gate re-run on the new legs.

REVISE, 6/10. Ship bar 8.
