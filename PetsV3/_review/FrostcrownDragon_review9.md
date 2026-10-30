# Frostcrown Dragon - scores review 9 (2026-10-28) - FINAL GATE

**Model: 8.6/10 - PASS. Clips: 8.6/10 - PASS.**

Model clears the 8.5 bar: the round-8 blocker (MUST 2, flank seams) now passes the 80 % coverage rule on all four torso seams, and ice-white and gold still pass. The model is only 0.1 above the floor; the open TO 9+ items (face eye, body value, diadem span) are what would move it to 9. Clips: the lowest clip is 8.6 (idle, walk, fly, takeoff, land). Only the act beat changed (snap +10), which lifts act to 8.7. No clip MUST.

## What I looked at
- Brief (`_review\GLACIER_REVIEWER_BRIEF.md`), round-8 review (`_review\FrostcrownDragon_review8.md`), `FrostcrownDragon\MODEL_NOTES.md` (round 9 section), `FrostcrownDragon\CLIP_NOTES.md` (review 8 section).
- Images, all from the round-9 build (renders dated 08:39-08:41; `_scratch\FrostcrownDragon_r9final.py.txt`), read directly under `FrostcrownDragon\`:
  - `renders\model_side.png`, `renders\model_tq.png`, `renders\_model_sheet.png`, `renders\_close_sheet.png`, `renders\_crown_sheet.png`, `renders\_icons_strip_128.png`, `FrostcrownDragon_icon_game.png`, `_scratch\seam_zoom4.png`;
  - all 14 clip sheets `renders\_pose_<tq|game>_<clip>_sheet.png` (idle, walk, fly, takeoff, land, roar, act_stillfreeze);
  - my own 3x / 8x / 10x zooms of the flank seams, the hip, the head close-up, and fly f0 / takeoff f11 / act f60 cells.
- Logs: `_scratch\clips_last.txt` (headless step 1), `_scratch\seam.txt`, `_scratch\rest_delta.txt`, `_scratch\steps.txt`.
- My own read-only checks, in the Windows temp folder (`fc_r9`), nothing written to the project: a pure-Python PNG reader, per-pixel class maps on `model_side.png`, the ice-white mask on the 128 px strip, and the gold count on the 64 px game icon. The mask definitions are the same as the builder's.

## Per-clip scores (clips score = lowest = 8.6)

| clip | score | why | evidence file |
|---|---|---|---|
| idle | 8.6 | Frost hum: wings half-fold (f32 open, f60-f120 folded), slow head sway, f80 puff. Fin tick (3 deg) is in no sheet (no f92 frame). | `renders\_pose_tq_idle_sheet.png`, `renders\_pose_game_idle_sheet.png` |
| walk | 8.6 | Lateral quad cycle, unchanged from round 8. Legs alternate across f0/10/20/30, head steady, slide 0.0, ground -0.010. Stiff but readable. | `renders\_pose_tq_walk_sheet.png`, `renders\_pose_game_walk_sheet.png`, `_scratch\clips_last.txt` |
| fly | 8.6 | Stroke reads (f0 high, f7 mid, f14 low and back, f21 mid), body level, tail streams, min z +0.089. Bottom still -24 (TO 9+). | `renders\_pose_tq_fly_sheet.png`, `renders\_pose_game_fly_sheet.png` |
| takeoff | 8.6 | Crouch, wings up f8/f11, downbeat f12/f14, airborne by f19, last frame = fly f0 (0.0 deg). Largest step 25.9 is the FX_FrostTrail bone, not a wing. | `renders\_pose_tq_takeoff_sheet.png`, `renders\_pose_game_takeoff_sheet.png`, `_scratch\seam.txt` |
| land | 8.6 | Flare, touch f16, absorb, one wing folds through a half-fold, rest at f28 (0.0 deg vs roar f0). | `renders\_pose_tq_land_sheet.png`, `renders\_pose_game_land_sheet.png`, `_scratch\rest_delta.txt` |
| roar | 8.7 | Wings spread, head lifts 15 deg, jaw opens f14-f40, closes to rest (0.0 deg at f66). Head lift is small at game distance; the wings carry it. | `renders\_pose_tq_roar_sheet.png`, `renders\_pose_game_roar_sheet.png`, `_scratch\rest_delta.txt` |
| act_stillfreeze | 8.7 | Up from 8.6: the +10 snap now reads (tq f58 mid, f60 high, f62 low, f64 high, f66 mid). Head press visible f44-f58, wing flare holds f44-f58, rest at f110 (0.0 deg). | `renders\_pose_tq_act_stillfreeze_sheet.png`, `renders\_pose_game_act_stillfreeze_sheet.png`, `FrostcrownDragon_r9final.py.txt` L837 |

Limits (`_scratch\clips_last.txt`, `steps.txt`): collision_free true, linear 0 on every clip, loops closed (idle/walk/fly), walk slide 0.0, foot_z_var 0.0, ground_min_z idle -0.005 / walk -0.010 / fly +0.089 / takeoff, land, roar, act -0.005, tris 10,460. Neck 7.5 and chest vs spine 3.0 are from CLIP_NOTES (I did not re-run them). Pose limits and ANIM_REFS: PASS.

## Round-8 items

| # | item | result | evidence |
|---|---|---|---|
| MUST 1 | Ice-white >= 9.2 % portrait (strip cell 0) | **PASS** | My count on `renders\_icons_strip_128.png`, cell 0, crop 6-133, same mask: portrait **9.77 %**, loose **10.68 %**, mean luma 106.7. Builder: 9.8 / 10.7 / 107. |
| MUST 2 | Flank seams continuous >= 3 px over >= 80 % of each torso block | **PASS (marginal on seam D)** | Measured on `renders\model_side.png` (600 px). Flank rows = from the dark saddle edge down to the belly or leg edge, per core column: **A** x 205-207: 97 / 90 / 85 %; **B** x 219-220: 92 / 97 % (x 221 72 %, the lower end bends right at y 341-351 and stays continuous); **C** x 237-239: 94 / 94 / 88 %; **D** x 253-254: **81 / 82 %** (rows 342-347 above the leg stay plain flank). Hip x 298: 92 % of 13 rows. Width 3-4 px at y 324 / 332 / 340 on all four seams. The builder's "about 90 %" holds for A, B, C but overstates D by about 8 pts. |
| M1 | Horns read as horns | **PASS** | `renders\_crown_sheet.png`, unchanged. Front span still 1.65 x head (TO 9+). |
| M2 | Gold, brief rule, game icon | **PASS** | `FrostcrownDragon_icon_game.png` 512 -> 64 px, alpha > 128: brief rule **NEAREST 30, BOX 29** (builder 30 / 29, reproduced). LANCZOS (builder 28) not re-run. Gate 25. |
| M3 | Ice-white (round-7 table) | **PASS** | As MUST 1. |
| M4 | Flank banding reads at 300 px | **PASS** | 2x box-downscale of `model_side.png`: the four seams read as light stripes at 300 px (soft); crisp at 600 px. |
| C1 | Takeoff -> fly handoff | **PASS** | `_scratch\seam.txt`: takeoff f28 vs fly f0 = 0.0 deg. |
| C2 | Gap checks (rest, min z, steps) | **PASS** | `_scratch\clips_last.txt`, `steps.txt`, `rest_delta.txt`: see the limits line above. |
| C3 | Act wing snap | **PASS (now +10)** | `FrostcrownDragon_r9final.py.txt` L837 `snap` = SPREAD +10 (was +6); visible in the tq sheet at f60 and f64 against f58 / f62 / f66. |
| C4 | Labelled sheets from final build | **PASS** | All renders dated 08:39-08:41, after the r9 start (08:34): 14 clip sheets, `_model_sheet`, `_close_sheet`, `_crown_sheet`, `_icons_strip_128/64`, `model_side`, `model_tq`. |

Round-8 TO 9+ items (status):
- Body value, STEEL_BLUE (62,104,176) -> (56,94,162): **OPEN** (code unchanged; dark share 24.5 % at round 8).
- Diadem span 1.65 x head: **OPEN**.
- Near-horn second GOLD_HI ridge: **OPEN** (not in the round-9 notes).
- Face, EYE_HOT slit: **OPEN**. The eye is still a ~3 px pale dash under the brow spine (`renders\_close_sheet.png`, head cell at 2x). It does not read from 5 studs.
- Fly stroke bottom -24 -> -32: **OPEN** (builder declined; the reason is in CLIP_NOTES).
- Act snap +10: **DONE**.
- Idle f92 frame in the idle sheet: **OPEN**.

## New MUSTs
**None.** Nothing blocks 8.5 on the model or on any clip.

## TO 9+ (not blocking, most valuable first)
1. **Face, eye (model).** The EYE_HOT slit reads as a ~3 px pale dash under the brow spines, so the face loses its narrow-slit-eye read at game distance. Lengthen the slit by 20 % and drop its upper edge about 0.01 BU so the brow spine no longer covers its top third. Keep the BLACK slit pupil. Re-render `_close_sheet.png` and the game icon at 64 px.
2. **Seam D (model).** Rows 342-347 at x 253-254 are plain flank under the end of the waist 0.24 seam (coverage 81-82 %). Extend that band's lower end from z 0.69 to the belly ray-hit (about 0.65 BU). Target: coverage >= 90 % at x 253-254, and `collision_free` still true.
3. **Body value (model).** STEEL_BLUE (62,104,176) -> (56,94,162), the round-8 line. Dark share toward 28 % (24.5 % at round 8; re-measure on the 128 px strip).
4. **Diadem span (model).** Lower the diadem's outer ends by about 15 % so the front span is 1.5 x the head or less (now 1.65 x).
5. **Horn value (model).** Add a second GOLD_HI ridge on the horn root segment (`horn()`).
6. **Fly stroke (clips).** Bottom -24 -> -32 (fly min z stays >= 0.05). Re-run the fly-tempo part of takeoff f20-28 so takeoff f28 still equals fly f0 (0.0 deg).
7. **Roar head lift (clips).** 15 deg -> about 20 deg (limit 30) so the head lift reads at game distance.
8. **Idle evidence (clips).** Add the f92 frame to the idle sheet so the 3 deg fin tick is shown.
9. **Act hold (clips, optional).** Hold SPREAD two frames before HALF f70 so the two snaps land as holds.

## Notes for the lead (not scored)
- Gold: brief rule reproduces (29 BOX, 30 NEAREST). The 28 LANCZOS is not re-run; the gate is 25 either way.
- Seam coverage: the rule is reproducible with the class map above (dark < 85 luma, seam >= 165, ground B-R <= 25). The builder should state the same method for the record. The "about 90 %" claim is true for A, B, C; D is 81-82 %.
- The model is 0.1 above the floor. The face eye (TO 9+ item 1) is the most visible open point.
- Lead rulings applied as given: gold scored on the brief rule; VFX in Studio not judged; walk speed not judged.
