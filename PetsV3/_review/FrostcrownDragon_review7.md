# Frostcrown Dragon - scores review 7 (2026-10-28) - FINAL GATE

**Model: 8.4/10 - FIX. Clips: 8.6/10 - PASS.**

Model is under the 8.5 bar: the horns and the evidence are fixed, but the flank seams are not a continuous line and the ice-white count is still short on the stated rule. Clips clear the bar: the evidence now comes from the final build, the handoff and rest deltas are 0.00, and the act snap is in. Two model MUSTs remain (both small palette and mesh edits). Round 6 was model 8.2 / clips 8.4.

## What I looked at
Newest set only (the builder's 05:04-05:06 render, code at 05:03):
- `renders\_crown_sheet.png`, `renders\crown_front.png`, `renders\crown_game.png`, `renders\crown_tq.png`.
- `FrostcrownDragon_icon_game.png` (512), `renders\_icons_strip_128.png` / `_64.png`, `renders\_icons2_strip_128.png` / `_64.png`.
- `renders\_model_sheet.png`, `renders\model_side.png`, `renders\model_tq.png`, `renders\model_game.png`, `renders\model_front.png`, `renders\flat_game.png`, `renders\flat_side.png`.
- All 14 clip sheets, labelled, footer "rendered 2026-10-28 05:06": `_pose_tq_<clip>_sheet.png` and `_pose_game_<clip>_sheet.png` for act_stillfreeze, takeoff, roar, fly, land, idle, walk.
- Not usable: `renders\_close_sheet.png` is from 2026-10-27 15:15 (round 2). The face at game distance is judged only from `crown_tq.png` and `model_tq.png`. The `_pose_sheet.png` is unlabelled and was not used.
- Logs and code: `_scratch\full_step1.txt` (05:05), `rest_delta.txt` and `seam.txt` (05:04), `steps.txt`, `gold.json`, `crown.log`, `pack.log`; `pets\FrostcrownDragon.py` (horn L162-236, trim_band L126-134, ICE_W facet L151-153, act snap L829-830, SPREAD L578).
- Lineup context: `PetsV3\_ALL_FIERCE_progress.png`. The Frostcrown is not in it.

My own counts (read-only, pure-Python PNG decode with numpy, nothing written to disk):
- Game icon 512 to 64 px, alpha > 128: brief rule **27 LANCZOS / 28 BOX / 29 NEAREST** (matches the builder exactly, gate 25). Tool rule 24 / 28 / 27. Strict 10 / 11 / 16. Strict is logged only (lead ruling).
- 128 px strip cell 1 (x 6-133, y 6-133), pet pixels = max RGB channel more than 6 away from the slate (52,62,74): luma > 200 & s < 0.2 = **9.6 %** (builder 9.6, match). Luma > 215 & s < 0.15 (the portrait rule) = **8.8 %**; HSL-lightness variant 8.9 %. The builder's **9.4 % is not reproduced**. Mean luma 105 (cap 110), dark (L < 70) 24.5 %.
- Horn silhouette in `crown_front` at 600 px: 58-61 px wide at y 150-190, outer edge x 123 and 476. Diadem x 126-473. Head about 210 px wide. Span 1.65 x the head.

## Round-6 items

| # | Item | Result | Evidence |
|---|---|---|---|
| M1 | Horns read as horns, not slabs | **PASS (silhouette), PARTIAL (span)** | Horns are now lofted octagonal tubes (`horn()` L171-236), rounded in front, tapering to points, with two GOLD_D collars. `crown_front` shows two rounded horns, each about 60 px wide at 600 px, with no flat face. `crown_game` shows the near horn as a rounded tube with a collar. The front span (1.65 x the head) is set by the 347 px diadem that both horns join, not by the horns. |
| M2 | Gold on the game icon (brief rule) | **PASS** | Brief 27 LANCZOS (gate 25, margin 2), reproduced. Lead ruling applies to strict and to the tool rule (24 LANCZOS). |
| M3 | Ice-white >= 9 % on both counts | **FAIL on the portrait rule** | Loose 9.6 % (PASS). Portrait rule 8.8 % (target 9.2 %). Round 6 was 8.9 % on the same method, so the r7 lerp change moved the stricter count by about 0.1 pt, not the claimed +0.4. |
| M4 | Flank banding reads at 300 px | **PARTIAL** | `trim_band` is now 0.030 wide, 0.012 thick, 0.010 off (L126-134, L415 tail 0.027). In `model_side` at 600 px each torso block shows one pale seam, but it is about 2 px wide and 12-15 px tall, with gaps. Not a continuous line of 3 px or more. Tail bars read as separate white dashes. |
| C1 | Takeoff to fly handoff | **PASS** | `seam.txt` (05:04): takeoff f28 vs fly f0 = 0.00 deg, displacement 0.0. `pose_game_takeoff_27` and `_fly_00` match. |
| C2 | Gap checks on the final build (rest, min z, steps) | **PASS, one part not re-run** | `rest_delta.txt`: roar f66, act f110, land f28 = 0.00 deg. `full_step1.txt`: collision_free true, linear 0, loops closed, ground min z -0.010 walk / -0.005 others / +0.089 fly, Neck 7.5, Neck2 7.0, chest vs spine 3.0, largest step 25.9 (FX bone, takeoff f8). Not re-run: the min-z table for takeoff f26-27 / fly f1 (`minz.py` exists, no output logged after 00:59). The f28 = fly f0 identity is covered by `seam.txt`. |
| C3 | Act wing snap +6 | **PASS** | Code: `snap = (SPREAD[0] + 6, SPREAD[1], SPREAD[2], SPREAD[3] - 6)` (L829). The arm goes 40 to 46 and the tip 60 to 54 at f60 and f64. Visible in `_pose_tq_act_stillfreeze` (f60 wing top rises clearly against f58). Subtle at game distance. |
| C4 | Labelled sheets from the final build | **PASS** | All 14 sheets labelled, footer 05:06. Idle sheet shows f0/32/60/80/120; the f92 fin tick (3 deg) is not in any sheet. |

Round-6 checklist, the rest:
- Five crown points from the front: PASS (`crown_front`).
- Back crown ring: PASS (`crown_game`).
- Dark top separate from flanks: PASS (DEEP_STEEL saddle).
- Luminance <= 110: PASS (105).
- Dark share >= 28 %: FAIL (24.5 %). Not a brief rule; TO 9+ (see below).
- Tris <= 13k: PASS (9,632).
- Ground >= -0.015: PASS (-0.010 walk).
- Neck <= 7.5, chest vs spine <= 4: PASS, but the neck is at the limit (7.5).
- End frames at rest: PASS (0.00 deg on roar / act / land).
- Events match the clip table: PASS (launch 0.393, touch 0.571, roar 0.364, click 0.145, frost 0.455 of their clip lengths).
- Name, no glow, studs: PASS (`tglow` empty; studs on the hide).

## New MUSTs (only what blocks 8.5)

**MUST 1 - Ice-white on the portrait rule (M3, still open).**
- Measure: 128 px strip cell 1 (x 6-133, y 6-133), pet pixels = max RGB channel more than 6 away from (52,62,74). Portrait rule (luma > 215 and s < 0.15) must be >= 9.2 %. Loose rule (luma > 200, s < 0.2) stays >= 9.5 %.
- Current: 8.8 % and 9.6 %.
- Fix (palette, no new geometry): raise `ICE_W` (L23) from (236, 246, 252) to **(244, 250, 255)** and use it on the second fin facet (L153, already ICE_W). Keep `ICE_THROAT` (L22) as is. Mean luma must stay <= 110 (about 106 expected).
- Re-render the 128 px strip and report both counts under the mask above. Do not change the fin widths; the r7 lerp already did that.

**MUST 2 - Flank seams are not a continuous line (M4, still open).**
- Measure: `model_side.png` at 600 px, on each torso block (rib, waist, hips) the pale seam must be a continuous run of at least 3 px wide over at least 80 % of the block's flank height, with no ground or hide pixels in between. Currently about 2 px wide with gaps.
- Fix in `trim_band()` (L126-134): bar thickness `0.012` -> `0.018` (L133), and the bar width stays at `0.030`. Also set the seam segments to overlap by 0.01 so that the bar ends meet (the ray-hit `zs` list at L285-291 already gives top-to-bottom points; add one hit point at each block's mid-height if a gap is left).
- Step 1 must stay collision_free (the bars now stand off the flank by 0.010 and are 0.018 thick: re-run `fold_pairs` and the step-1 gates).

## TO 9+ (after the 8.5 items; not blocking)
- **Model, body value:** deepen `STEEL_BLUE` (L20) from (62, 104, 176) to about (56, 94, 162), about -8 %. Moves the dark share toward 28 % (now 24.5 %) and widens the luma margin.
- **Model, diadem and horns:** the 347 px diadem is the wide gold face in `crown_front`. Lower its outer ends about 15 % or add a GOLD_HI ridge to its front edge so the horns read as separate from the diadem.
- **Model, near-horn value step:** a second GOLD_HI ridge on the root segment (L231 crest, extra `t` at 0.10) so the big face in `crown_game` gets a light and dark step.
- **Model, face:** a fresh close render of the face at game distance (the `_close_sheet.png` is round 2 and stale). The EYE_HOT slit (L118) reads only as a notch under the diadem edge in `crown_tq`.
- **Clips, flight:** the fly stroke is 40 / -24 (64 deg) and the takeoff downbeat is 86 deg. Deepen the fly bottom to about -32 (keep the loop closed and feet >= 0.05).
- **Clips, act:** hold SPREAD two frames before HALF f70 so the two snaps land as holds, not a blur. A 6 deg snap is subtle at game distance; a 10 deg snap (arm +10, tip -10) would read at 300 px.
- **Clips, evidence:** run `minz.py` for takeoff f26-27 and fly f1 and log it; add an idle f92 sheet frame.

## Notes for the lead (not scored)
- **Gold:** the brief rule (27 / 28 / 29) reproduces exactly, so the builder's counts are reliable. The tool rule at LANCZOS is 24, one below gate 25. The lead ruling covers the brief rule; mention it in case the tool rule is the one used in Studio.
- **Ice-white method:** the builder's 9.4 % on the portrait rule does not reproduce with the strip-cell mask. The builder should state the exact mask so the next review uses one method.
- **Clip staleness:** the `_close_sheet.png` and `_pose_sheet.png` are not from the final build. The clip gate uses only the labelled sheets.
- **Shared gold:** unchanged from review 6 (Permafrost Titan uses the same GOLD RGB; flagged for distinctness only).

## Pass / fail summary
| Gate | Result |
|---|---|
| Horns read as horns (silhouette, tip, collars) | PASS |
| Front span <= 1.35 x head | FAIL (1.65 x; diadem-bound; TO 9+) |
| Gold, brief rule 64 px (LANCZOS >= 25) | PASS (27) |
| Gold, strict | lead ruling (10) |
| Ice-white loose >= 9 % | PASS (9.6) |
| Ice-white portrait >= 9 % (target 9.2) | FAIL (8.8) - MUST 1 |
| Flank seams continuous >= 3 px | FAIL - MUST 2 |
| Luminance <= 110 | PASS (105) |
| Dark share >= 28 % | FAIL (24.5; TO 9+) |
| Tris <= 13k | PASS (9,632) |
| Step 1 collision-free, loops, linear 0 | PASS |
| Ground >= -0.015 | PASS (-0.010) |
| Neck <= 7.5, chest vs spine <= 4 | PASS (7.5 at limit, 3.0) |
| Takeoff to fly handoff | PASS (0.00) |
| Rest deltas roar / act / land | PASS (0.00) |
| Act snap +6 | PASS (visible in tq; subtle at game distance) |
| Labelled sheets, final build | PASS (14 of 14, 05:06) |
| Min-z table takeoff f26-27 / fly f1 | NOT RE-RUN (not blocking; seam covers f28) |
| Name, no glow, studs | PASS |

Verdict: **Model 8.4 - FIX (MUST 1 and MUST 2). Clips 8.6 - PASS.** After MUST 1 and MUST 2, re-send: the 128 px strip cell with both ice-white counts under the stated mask; `model_side.png` and `model_tq.png` at 600 px; and the Step 1 gate line from the same build.
