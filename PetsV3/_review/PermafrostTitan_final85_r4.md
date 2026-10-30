# Permafrost Titan - FINAL 8.5 GATE, ROUND 4 (model + clips, export 2026-10-28 04:21) - FIX

**Model: 8.3/10 - FIX. Clips: 7.7/10 - FIX.**

Per clip: idle 7.5, walk 7.5, roar 8.0, act (kneel) 7.8.

Owner bar: 8.5 is the floor for model and for every clip, and higher is better. Nothing under 8.5 ships.

Round 4 fixed the things round 3 asked for in the knee, the belt and the hips. The model is now a clean, fierce, readable titan with a strong gold hero. It still reads as a stack of blocks: the torso is a straight column, so it looks box-built rather than sculpted. The clips are the weaker half. The idle and the walk barely move the upper body, the kneel's game-camera L is still weak, and the roar's mouth reads as a grey slab.

## What I looked at

- Brief, round 3 review, and the builder notes: `MODEL_NOTES.md` and `CLIP_NOTES.md` (both "FINAL 8.5 ROUND 3" sections), plus `_scratch/clipgate_r3.txt` (headless gate JSON), `fist_r3.txt`, `gold_windows_r3.txt`, `shares_all_r3.json`.
- Script lines read: `pets/PermafrostTitan.py` L104-115 (hips, belt, waist, chest), L203-225 (neck, skull, brow, eyes, jaw cavity), L292-302 (ankle, wedge foot, toes).
- Renders, all from the newest set (title bars 04:19-04:21). All images opened and loaded:
  - Model: `_model_sheet`, `_close_sheet`, `flat_side`, `flat_game`, `gamelook_game`, `gamelook_tq`.
  - Icons: `_icons_strip_64` and `_128`, `_icons2_strip_64` and `_128`. The second icon of `_icons2` is the Titan's own game-camera icon, not a sibling (MODEL_NOTES L233).
  - Clips: `_pose_tq_sheet` (24 beats), `_beats2x_idle`, `_beats2x_roar`, `_beats2x_kneel`, `_walk_sheet`, `_kneel_2x_f40_f50` (tq and game), `_kneel_views` (front, tq, back, game at f18, f40, f58), `hx_game_act_kneelrise_40`, `hx_tq_act_kneelrise_40`, `_roar_jaw_close`.
- My own 2x crops (outside the review folder, in the temp dir): the tq f40 left fist against the thigh, the game f40 kneeling knee and sole, and the game f40 arms.
- Note: the game camera sits behind the Titan (MODEL_NOTES, "the game camera (from behind)"). The head is bowed 12 deg in the kneel, so the face is hidden in game view. Judge the game-camera items from behind.

## Numbers (from the logs, not re-run)

- Tris 7,664 (under 15k).
- collision_free true. Loops 0 / 0. Walk slide 0. Idle foot drift 0.
- ground_min_z: idle 0.000, walk 0.000, roar 0.000, act -0.014 at f20.
- Chest vs spine: idle 4.85, roar 3.00, act 4.68 (limit 5, all pass).
- Head pitch: roar 15, act 14.1 (down-limit 20 and up-limit 30 are not exceeded). See the ruling note below.
- Gold at 64 px: kit counter 52 portrait / 27 game; render window 47 / 20. The gold ring is clear in the first icon of `_icons_strip_64`.
- Fist probe (`fist_r3.txt`, f30 / f40 / f46): fist_to_thigh_min_gap 0.019, fist_centre_to_thigh_surface 0.294, fist centre z 0.514, chest line z 0.832.

## Round-3 items

**Model**

1. **M1 knee step: PASS.** The shin top equals the thigh's knee width. In `_kneel_views` front and `_model_sheet` side the leg tapers as one tube. The knee plate is a flat plum slab that stands off the shin. No ledge at the knee in the side view.
2. **M2 belt groove: PASS.** The belt seam is now a thin dark line at the waist (Spine, half-height 0.02). The side silhouette reads as one torso, with a thin seam and the pale belly strip below it. A second, slightly thicker seam at the chest/waist gap (L115) still shows. It reads as a seam, not a box.

**Clips**

3. **M3 left fist on the thigh: PARTIAL.**
   - From 3/4 (`_kneel_2x_f40_f50` tq, my crop of the tq f40): PASS on the read. The left fist sits against the front of the kneeling thigh at knee height, well below the chest line. It reads as a hand resting on the knee.
   - Against the numeric test: FAIL. `fist_r3.txt` logs a fist-to-thigh minimum gap of 0.019 and a fist-centre-to-surface distance of 0.294. The test asks for the centre within 0.03 of the surface. The notes say "0.094 from the thigh surface", which does not appear in any log. The notes and the log disagree and must be reconciled.
   - From the game camera (behind): not readable. The left fist is hidden behind the body.
4. **M4 game-camera kneel L-shape: PARTIAL.** The sole is visible and the kneeling shin is pulled back, so the leg is no longer a straight column. But from behind the knee does not read as a knee on the snow. The kneeling leg reads more as a leg stepping back, and a dark slate block sits on the rear top of the kneeling foot (my game f40 crop) and reads as a separate piece.
5. **M5 idle torso life: PARTIAL.** The arms sway, but at ±2.5 deg it is too small to see at 5 studs. `_beats2x_idle` f0 / f30 / f60 / f90 reads as "legs shuffle": the hips, legs and fists move, the pauldrons and shoulders barely move. The chest counter still cancels the hip yaw (chest vs spine 4.85 is at the limit, so the chest cannot take more yaw).
6. **Polish:**
   - Walk arm swing 5.5 deg: the arms still barely move in `_walk_sheet` (tq and side). Walk stays at 7.5.
   - Breath 1.8 and knee settle 0.005: PASS (act ground min -0.014).
   - Roar jaw close re-rendered: PASS as a render. At f27 the open mouth is a flat grey slab, not a dark cavity (see roar MUST).
   - Gold at 64 px: PASS.
   - Tris: PASS.

**Round-3 checklist, other rows**

- Fierce face (heavy brows, slit eyes, closed mouth): PASS (`_close_sheet`).
- Blunt ice, no spikes or glow: PASS.
- Roar reads as a bellow (arms out f22-50, head lift): PASS.
- Pauldrons read as crust: PASS.
- Knuckles read as fingers: PASS.
- Anim refs cited (Muybridge Plate 27 walk, Plate 356 kneel, per CLIP_NOTES and ANIM_REFS.md): PASS in the notes. I did not re-check each reference.
- Colour: left to the lead's Studio ruling, not scored.

## New MUSTs (only what blocks 8.5)

**Model (8.3 -> 8.5)**

- **MM1. Box torso (the front reads as a straight column).** `pets/PermafrostTitan.py` L109, the Spine body block `B.add((0, 0.02, 1.10), (0.262, 0.19, 0.08), MAUVE, "Spine", bot=(0.95, 0.95), top=(1.08, 1.06), ...)`. Change `bot=(0.95, 0.95)` to `bot=(0.86, 0.86)`, so the waist narrows from about 0.262 to about 0.225 half-width at the belt. Keep the belt seam at 0.262 as a lip, and keep `top` as it is.
  - Clearance: the hip block is 0.27 wide and the thigh tops sit outside it, so 0.225 leaves room. Re-run `collide_where` on Spine vs Leg_L and Leg_R (expect 0 pairs).
  - Acceptance: `_model_sheet` side and front show a waist (a clear step in from the chest and the hips). Chest vs spine is unchanged (no bone change). Tris within ±200 of 7,664.

**Clips (7.7 -> 8.5)**

- **MC1. Game-camera kneel L (M4 and the act read).** In the kneel hold (f20-52), lean `Shin_L` back about 10 deg about the knee so the ankle swings behind the knee and the sole faces the camera. Keep `Knee_L` on the snow: its z stays between -0.02 and 0.00 (lower the pelvis by the amount the knee rises, not more than 0.01). Also flatten the dark slate block on the kneeling foot's rear top to a seam (half-height at most 0.01; check whether it is the ankle band at L292-294).
  - Acceptance: from the game camera (behind) at 2x, f40 and f50 show a visible L: the thigh drops from the hip, the shin lies back, the sole faces the camera, no lump at the knee. In plan view the heel sits at least 0.10 BU behind the knee in f30-50. `collide_where` 0 pairs, ground_min_z at or above -0.02, chest vs spine at or under 5.
- **MC2. Idle torso life (M5).** `Arm_L` and `Arm_R` rot z go from ±2.5 deg to ±5.0 deg (opposite signs, on the same sine as the hip yaw at L416-420). Arm bones are not in the chest-vs-spine count, so the chest limit is untouched.
  - Acceptance: `_beats2x_idle` f0 vs f30 shows the pauldron tips and fists move at least 0.05 BU (about 5 deg at arm length). Feet planted (idle foot drift 0). `collide_where` 0 pairs for the fists against the thighs at the swing extremes.
- **MC3. Walk (7.5 -> 8.5).** `Arm_L` / `Arm_R` walk swing goes from 5.5 deg to 9 deg (opposite phase, same as now). Stride and the leg timing do not change.
  - Acceptance: `_walk_sheet` shows the fists swing clearly from f0 to f42 at tq. `collide_where` 0 pairs at the swing extremes (fist at least 0.03 BU from the thigh). Walk slide stays 0.
- **MC4. Roar mouth (roar 8.0 -> 8.5).** The jaw cavity at L225 `B.add((0, -0.335, 1.707), (0.086, 0.040, 0.018), JOINT_D, "Head", ...)` is slate (52, 60, 84), so the open mouth reads as a grey slab (`_roar_jaw_close` f27). Change its colour to a near-black (28, 24, 34) so the open mouth reads as a dark cavity.
  - Acceptance: `_roar_jaw_close` f27 (front and tq) shows a dark opening between the brow and the lower jaw, with no lighter slab. Roar head pitch unchanged.

## TO 9+ (not blocking)

- Head: the skull is 0.32 wide on a 0.52 chest. It reads small and sunk. This follows the plan ("a small bare head sunk between the shoulders"), so it is not a MUST. If the lead wants a bigger head, a 6-8% increase in skull half-width (L206, 0.160 to about 0.170) would help.
- Belly strip (L110, ICE_W 0.16 x 0.012): a flat pale box under the bezel. It is the main "box belly" tell in the front view. Making it slightly narrower (0.16 to 0.13) would soften it.
- Ice crusts on the pauldrons and fists read as clusters of small white slabs. At 64 px they become white noise around the shoulders. Fewer, larger crust blocks would read better.
- Eye slits (ICE_W) read as bright white bars in `_close_sheet`. Within the brief they are not glints, but they are the brightest thing on the face. Consider a slightly darker ice tone (about 200, 220, 236) for the slits.
- Chest/waist seam (L115) is a second seam below the belt. It reads fine; it could be thinned to match the belt seam (0.035 to 0.02).
- Walk and idle are the lowest clip scores. MC2 and MC3 are the largest lift for the least risk.
- Notes accuracy: MODEL_NOTES and CLIP_NOTES say "0.094 from the thigh surface". The log says 0.019 (min gap) and 0.294 (centre). Pick the metric the test asks for, log it, and quote the same number in the notes.
- Gold counts: 52 portrait / 27 game (kit counter) and 47 / 20 (render window). Both pass; state which one the ship bar uses.

## Ruling needed (not scored)

- The brief lists "neck <= 8 deg". The rig has no Neck bone (CLIP_NOTES round 3, L160), and the head pivots at the throat. The builder applies the head + neck limits (up <= 30, down <= 20) to the Head bone and treats the 8-deg neck rule as not applying. Head pitch in roar is 15 deg and in act 14.1 deg. If the lead counts the Head bone as the neck, both exceed 8. I did not score it as a FAIL, but the lead should rule.

## Summary

- Model 8.3 (FIX). Clips 7.7 (FIX): idle 7.5, walk 7.5, roar 8.0, act 7.8.
- Round-3 model items: M1 PASS, M2 PASS.
- Round-3 clip items: M3 PARTIAL (3/4 PASS, numbers FAIL, game camera not readable), M4 PARTIAL, M5 PARTIAL, walk arm swing PARTIAL.
- MUSTs: MM1 box torso (waist taper); MC1 game-camera kneel L; MC2 idle arm sway to ±5; MC3 walk arm swing to 9; MC4 roar mouth colour.
