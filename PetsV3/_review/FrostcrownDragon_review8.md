# Frostcrown Dragon - scores review 8 (2026-10-28) - FINAL GATE

**Model: 8.4/10 - FIX. Clips: 8.6/10 - PASS.**

Model stays under the 8.5 bar: MUST 1 (ice-white) is now fixed, but MUST 2 (flank seams) is still short of the 80 % coverage rule on every torso run. Clips clear the bar: the lowest clip is 8.6 (walk, act, idle, fly, takeoff, land all 8.6; roar 8.7). No clip MUST. Round 7 was model 8.4 / clips 8.6.

## What I looked at
- Brief and round-7 review (`GLACIER_REVIEWER_BRIEF.md`, `FrostcrownDragon_review7.md`), plan (`FrostcrownDragon_plan.md`), `MODEL_NOTES.md` (round 8), `CLIP_NOTES.md` (review 7 section), `ANIM_REFS.md`.
- Images, all from the round-8 build (`pets/FrostcrownDragon.py` = `_scratch/FrostcrownDragon_r8final.py.txt`, identical bytes, mtime 06:04; renders 06:05-06:08):
  - `renders\_icons_strip_128.png`, `_icons_strip_64.png`, `FrostcrownDragon_icon_game.png`;
  - `renders\model_side.png`, `model_tq.png`, `_model_sheet.png`, `_close_sheet.png` (fresh, 06:06), `_crown_sheet.png`;
  - all 14 clip sheets (`_pose_tq_<clip>_sheet.png`, `_pose_game_<clip>_sheet.png`, footer 06:07), each read directly; the walk legs and the act crown region were also enlarged.
- Logs: `_scratch\full_step1.txt`, `minz_r8.txt`, `steps.txt`, `rest_delta.txt`, `seam.txt`, `gold.json`, `crown.log`, `pack.log`.
- My own read-only checks (independent numpy/PIL code in `C:\Users\ventu\AppData\Local\Temp` and `/tmp/fc_r8`, nothing written to the project):
  - ice-white on the 128 px strip cell 0 (x 6-133, y 6-133, pet = any channel more than 6 from (52,62,74));
  - seam rows, width and coverage on `model_side.png`;
  - gold on the 64 px game icon.

## Per-clip scores (clips score = lowest = 8.6)

| clip | score | why | evidence file |
|---|---|---|---|
| idle | 8.6 | Calm frost hum; wings half-fold and reopen (f32 clear in game view). The 3 deg fin tick is not visible at sheet scale. f92 frame still has no sheet. | `_pose_tq_idle_sheet.png`, `_pose_game_idle_sheet.png` |
| walk | 8.6 | Lateral quad cycle: legs visibly alternate across f0/10/20/30 (checked at 2x). Head and back steady, slide 0.0, ground -0.010. Stiff but readable. | `_pose_tq_walk_sheet.png`, `_pose_game_walk_sheet.png`, `full_step1.txt` |
| fly | 8.6 | Stroke reads (top f0, mid f7, bottom f14, mid f21), body level, tail streams, min z +0.089 (never touches ground). Bottom still -24 (TO 9+ deepen). | `_pose_tq_fly_sheet.png`, `_pose_game_fly_sheet.png`, `minz_r8.txt` |
| takeoff | 8.6 | Crouch, wing gather (f8/f11), downbeat (f12/f14), airborne by f19-26 (min z 0.089 at f26), handoff to fly f0 = 0.00. Launch step 25.9 on FX_FrostTrail only. | `_pose_tq_takeoff_sheet.png`, `_pose_game_takeoff_sheet.png`, `seam.txt`, `minz_r8.txt` |
| land | 8.6 | Brake, touch f16, absorb, fold, rest 0.00 deg at f28. | `_pose_tq_land_sheet.png`, `_pose_game_land_sheet.png`, `rest_delta.txt` |
| roar | 8.7 | Head up, wings spread, fins up, jaw open, hold, close to rest 0.00 deg. Head lift (15) is small at game distance, but the wings carry it. | `_pose_tq_roar_sheet.png`, `_pose_game_roar_sheet.png`, `rest_delta.txt` |
| act_stillfreeze | 8.6 | All beats present: inhale, fins rise together (30), head press (Neck 7 / Neck2 7 / Head 11) visible as the crown drops and moves forward at f44-66 (partly behind the wing), wing flare held f44-58, snap f60/f64 (+6, subtle), fold, rest 0.00 at f110. Snap size is the weak beat (TO 9+). | `_pose_tq_act_stillfreeze_sheet.png`, `_pose_game_act_stillfreeze_sheet.png`, `rest_delta.txt` |

Limits: neck 7.5 (<= 8), chest vs spine 3.0 (<= 5), head + neck pitch-up 15 (<= 30), ground min z -0.010 walk / -0.005 others, collision_free true, linear 0, loops closed. ANIM_REFS maps every clip to a cited reference: PASS.

## Round-7 items

| # | item | result | evidence |
|---|---|---|---|
| MUST 1 | Ice-white >= 9.2 % portrait rule (strip cell 0) | **PASS** | My count: portrait (L > 215, s < 0.15) **9.59 %** (722 of 7525 px); loose (L > 200, s < 0.20) 10.51 %; mean luma 106.4. Builder's 9.6 / 10.5 / 106 reproduced. |
| MUST 2 | Flank seams continuous >= 3 px over >= 80 % of each torso block | **FAIL (improved, still short)** | Continuous: no internal gaps on any torso run. Width: 3-4 px counting the anti-aliased edge (bright core 2-3 px). Coverage of the visible flank (from the dark arm band to the ground line) is **about 60-70 %**: rib seams 25-27 rows of about 36 (67-69 %), waist seams 21 rows of about 34 (60-62 %), hip seams 11-14 rows under the hind leg. The builder's "about 80 %" does not reproduce. See the fix below. |
| M1 | Horns read as horns | PASS (silhouette, unchanged). Span 1.65 x head stays TO 9+. | `crown_front.png`, `_crown_sheet.png` |
| M2 | Gold, brief rule on the game icon | **PASS** | My count, 64 px, alpha > 128: brief rule **28 LANCZOS / 29 BOX / 30 NEAREST** (gate 25, matches builder). Tool rule 24 / 28 / 28; strict 10 / 11 / 17 (logged only). Note for the lead: tool rule at LANCZOS is 24, below 25. |
| M3 | Ice-white (round-7 table) | PASS (see MUST 1) | |
| M4 | Flank banding reads at 300 px | PARTIAL (see MUST 2) | `model_side.png` at 600 px |
| C1 | Takeoff to fly handoff | PASS | `seam.txt`: takeoff f28 vs fly f0 = 0.00 deg |
| C2 | Gap checks (rest, min z, steps) | PASS | min-z table now RUN (was not re-run): takeoff f26 0.0894, f27 0.0899, f28 0.0940; fly f0 0.0940, f1 0.1012, f27 0.0899. Rest deltas 0.00 (roar, act, land). Step 1 collision_free true. |
| C3 | Act wing snap +6 | PASS (subtle) | Code `snap` L829; visible f60 / f64 vs f58 in the tq sheet |
| C4 | Labelled sheets from final build | PASS | 14 of 14, footer 06:07; `_close_sheet.png` 06:06 (fresh; round 7 used the stale round-2 sheet) |

Round-7 checklist, the rest:
- Front span <= 1.35 x head: FAIL, 1.65 x (TO 9+, not a MUST).
- Dark share >= 28 %: FAIL, 24.5 % by my count (TO 9+, not a brief rule).
- Ice-white loose >= 9 %: PASS (10.5).
- Luminance <= 110: PASS (106.4).
- Tris <= 13k: PASS (10,220).
- Ground >= -0.015: PASS (-0.010).
- Neck <= 7.5, chest vs spine <= 4: PASS (7.5 at limit, 3.0).
- Name, no glow, studs: PASS.

## New MUSTs
No new MUSTs. Nothing new blocks the clips. The one blocker is the round-7 carry-over:

**MUST 2 (carry-over, still open) - flank seams short of 80 % coverage.**
- Measure (`model_side.png`, 600 px): at each torso seam column (x about 206, 224, 238, 252) the seam rows must cover at least 80 % of the rows from the lower edge of the dark arm band down to the ground line in that column (about 29 of 36 rows on the rib, 27 of 34 on the waist). Hip seams: at least 80 % of the visible hide above the leg. Keep the continuous 3 px+ width (edge included).
- Current: rib 67-69 %, waist 60-62 %.
- Fix: in the `trim_band()` calls for the rib, waist and hips (function L126-134; the `zs` lists at each call site), move the LOWER end of each seam from z about 0.70 / 0.75 / 0.77 down to about 0.58-0.60, so it sits about 0.03 BU above the belly line. Keep the bar 0.018 thick, 0.016 off, and the 0.005 overlap. Ray-hit the belly edge at each block's bottom so the bar ends meet the flank.
- Then: re-render `model_side.png` at 600 px and `_scratch` step 1; `collision_free` must stay true (run `fold_pairs` again).

## TO 9+ (not blocking)
- **Model, body value:** STEEL_BLUE is still (62,104,176). Deepen to about (56,94,162) to move the dark share toward 28 % (now 24.5 %).
- **Model, span:** the 347 px diadem makes the front span 1.65 x the head. Lower the diadem outer ends about 15 %.
- **Model, near-horn value step:** add a second GOLD_HI ridge on the root segment (`horn()` L231 area).
- **Model, face:** the fresh close sheet shows the EYE_HOT slit as a small pale dash under the brow. Lengthen the slit by about 20 % or add a BLACK slit pupil contrast.
- **Clips, flight:** fly stroke still 40 / -24. Deepen the bottom to about -32, keep the loop closed and feet >= 0.05.
- **Clips, act:** the 6 deg snap is subtle; a 10 deg snap (arm +10, tip -10) reads at 300 px. Hold SPREAD two frames before HALF f70 so the snaps land as holds.
- **Clips, evidence:** add an idle f92 frame to the idle sheet (fin tick not shown in any sheet).

## Notes for the lead (not scored)
- Gold: brief rule reproduces exactly (28 / 29 / 30). Tool rule at LANCZOS is 24, one below gate 25; the ruling covers the brief rule.
- The builder's 9.4 % (round 7) and the "about 80 %" seam claim in round 8 both fail to reproduce on the stated masks; the builder should state the exact method for seam coverage the way the ice-white mask was stated.
- Act: my first read was that the head press was hidden at game distance. The crown crop (f0/16/44/50/58/66/80/110, game view) shows the crown dropping forward, so the beat is partly readable. Score kept at 8.6.
