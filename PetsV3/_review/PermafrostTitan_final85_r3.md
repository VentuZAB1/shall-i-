# Permafrost Titan - FINAL 8.5 GATE, ROUND 3 (model + clips, re-exported 2026-10-28 03:29) - FIX

**Model: 8.0/10 - FIX. Clips: 7.5/10 - FIX.**

Owner bar: 8.5 is the minimum, higher is better. Nothing under 8.5 ships.

Round 3 is a real step. The hips now start from the block, the idle has visible hip life, the kneel reads from the 3/4 with the knee down on the snow, and the roar still reads as a bellow. Both scores are still under 8.5. Four things hold them back: the knee still steps (a 0.006 calf ledge plus a knee cap sitting 0.016 proud), the belt groove still splits the torso into two boxes, the left fist floats beside the chest instead of resting on the thigh, and the kneel is only partly readable from the game camera.

## What I looked at

- Brief and round 2: `_review/GLACIER_REVIEWER_BRIEF.md`, `PermafrostTitan_final85_r2.md`.
- Notes: `PermafrostTitan/MODEL_NOTES.md` (FINAL 8.5 ROUND 2), `CLIP_NOTES.md` (FINAL 8.5 ROUND 2), `ANIM_REFS.md`.
- Newest render set only (the 03:26-03:29 batch). The `cv_*`, `_cv_kneel_*` (01:04-01:05) and `_roar_jaw_close.png` (01:00) files predate the 02:30 cut and were not used. So the roar jaw close-up is NOT verified in this round.
- Opened: `_model_sheet`, `_close_sheet`, `model_front/side/tq/back`, `gamelook_game`, `flat_game/side/tq/back`, `_icons_strip_64/128`, `_icons2_strip_64/128`, `_under_sheet`, `_pose_tq_sheet`, `_kneel_close_f40`, `_kneel_views`, `_beats2x_kneel/roar/idle`, `hx_game_` and `hx_tq_act_kneelrise_40`, `pclose_game_` and `pclose_tq_act_kneelrise_40`, single `pose_tq_act_kneelrise_18` and `_40`, single `pose_tq_idle_30`.
- Read the script `PetsV3/pets/PermafrostTitan.py`: L104-110 (hips and belt), L267-300 (legs), L385-425 (idle), L487-546 (kneel). `blockkit.seg` takes half-extents, so the protrusion figures below are as built.
- Numbers from `_scratch/export_r2.txt`, `_scratch/clipgate_r2.txt`: tris 7,664; collision_free true; ground min 0.000 for idle, walk and roar, -0.018 for the act at f20; loops 0 / 0; walk slide 0; stride 0.645; Lua 32,186 B. Chest vs spine idle: sqrt(2^2 + 4.5^2) = 4.92 from the script constants, which matches the note. Blender was not re-run (the brief forbids it), so the other gate numbers are as reported.

## Round-2 items

**Model**

1. **Legs as one tapered tube: PARTIAL.** The front and 3/4 show a tapered leg (thigh 0.182 to 0.120 at the knee, L275-278). But L276 sets the shin top to the thigh's knee width plus 0.006 ("a slight calf"). The brief says the shin "carries on at that width", so this leaves a small outward ledge at the knee. The knee cap at L286 (`-(SD - 0.004)`, half-depth 0.020) sits 0.016 proud, not the 0.008 flush the brief asks for. The thigh plate (L282-283) and shin guard (L289-291) are 0.008 proud as specified, and the single ankle band (L292) is right. In `model_side` a dark slate band still sits at the knee, so from the side the leg reads as segments.
2. **Legs start from the hip: PASS.** The thigh tops sit under the 0.27 hip block, 0.02 further out (L277), with thinner hip plates (L106-107). In `model_front` the legs taper from the block's underside.
3. **Chest to pelvis as one shape: PARTIAL.** The chest bottom and pelvis now share one front face. The belt joint (L108, JOINT_D, half-size 0.262 x 0.19 x 0.04) is still a dark 0.08 BU band across the torso. In `model_side` it still reads as two boxes with a dark band between them.
4. **NICE 1, belly band: PASS.** L110 is now 0.16 x 0.012. It reads as a pale underside strip.

**Clips**

5. **Kneel readable from the game camera and the 3/4 (MUST 4): PARTIAL.**
   - 3/4 (`pose_tq_act_kneelrise_40`, `_kneel_close_f40` tq, `pclose_tq_40`): **PASS-leaning.** The body drops, the kneeling thigh is on the snow with the sole and claws showing, and the standing leg is clear. The knee reads as a rounded thigh block, not a cap.
   - Game camera (`hx_game_40`, `pclose_game_40`): **PARTIAL.** It reads as a bent back leg with the shin lying back and the sole visible. The knee is not a readable shape: the knee cap faces forward, so the back-side camera cannot see it. The read has to come from the silhouette.
   - **Left fist: FAIL against the brief.** The brief asks for the left fist on the thigh above the knee, and CLIP_NOTES round 2 says it is. But ARM_L at L517 (out 12, fwd 8, bend 48, f30-50) sends the fist out to the side, and the comment at L514-515 says that is on purpose. In `pose_tq_act_kneelrise_18` and `_40` the left fist hangs at waist height beside the chest, about a fist above the thigh. The notes and the brief both say "on the thigh", so I judge against that. If the lead wants the hanging fist, it needs a ruling and the notes must say so.
6. **Idle more life (MUST 5): PARTIAL.** The numbers are as built: hip yaw 6 (L416), chest -0.75 (L419), head -0.25 (L420), so the head stays forward. In `_beats2x_idle` f0 / f30 / f60 / f90 the hips and right leg shift and the fists flex (8 deg, L424). The torso and shoulders barely move: the chest counter-yaw cancels most of the hip yaw, leaving about 1.5 deg of world chest yaw. At 5 studs it reads as "legs shuffle", not "alive". Chest vs spine is 4.92 against the 5 limit, which passes with a margin of 0.08.
7. **NICE 3, kneel close-ups at 2x: PASS.** `_beats2x_kneel` (f0-84) and `_kneel_close_f40` are provided.

**Round-2 checklist, other rows**
- Hero reads at 64 px: PASS. The gold ring is clear in the first icon of `_icons_strip_64`. The builder's counts (52 px portrait, 27 px game) were not re-measured.
- Fierce face (slits, heavy brows, no glint, closed mouth): PASS (`_close_sheet`).
- Blunt ice, no spikes or glow: PASS.
- Knuckles read as fingers: PASS (`model_front`).
- Pauldrons read as crust: PASS.
- Tris at or under 15k: PASS (7,664).
- Roar reads as a bellow: PASS (`_beats2x_roar`, arms out at f22-50, head lift). The jaw close-up is not in the newest set, so the f27 mouth claim is not re-checked.
- Colour: left to the lead's Studio ruling, not scored.

## New MUSTs (only what blocks 8.5)

**Model (8.0 to 8.5)**

- **M1. Knee step.** L276: `SW, SD = TW * TT, TD * TT` (drop the +0.006 calf) so the shin top equals the thigh's knee width (0.120 x 0.128). L286: knee cap centre `-(SD - 0.012)`, which makes the outer face 0.008 proud instead of 0.016. Test: `model_side` and the 3/4 show no outward ledge at the knee and no extra dark band beyond the seam.
- **M2. Belt groove.** L108: the JOINT_D belt joint half-height 0.04 -> 0.02 (keep half-width 0.262 and half-depth 0.19). Test: the side silhouette reads as one torso with a thin seam, not a 0.08 BU dark band.

**Clips (7.5 to 8.5)**

- **M3. Left fist on the thigh.** L517 ARM_L, f30 and f50: out 12 -> 6, fwd 8 -> 22, bend 48 -> 60 (keep the f18 and f62 blend points). Test: `pose_tq_act_kneelrise_40` and `_kneel_close_f40` tq show the left fist resting on the left thigh top, with the fist centre within about 0.03 BU of the thigh surface and below the chest line. Update the comment at L514-515 and CLIP_NOTES to match what is built.
- **M4. Game-camera kneel silhouette.** Acceptance test: `hx_game_act_kneelrise_40` at 2x must show the kneeling leg as one L-shape: the thigh dropping from the hip, the shin lying back and out, the sole visible, with no lump at the knee. Levers (pick one, say which): raise the kneel-side Spine roll during the hold (ROLL_S, L492, f18-50, 7 -> 9), and lift the kneeling foot's back-side sole by 0.02 BU in the L targets (L535-537). Check f40 and f50 from the game camera at 2x.
- **M5. Idle torso life.** In `idle()` add an arm sway that the chest counter does not cancel: `Arm_L` / `Arm_R` rot z = ±2.5 deg, opposite signs, driven by the same sine as the hip yaw at L416. Keep chest vs spine at or under 5. Test: `_beats2x_idle` f0 vs f30 shows the shoulders and pauldrons move, not only the hips. Feet stay planted.

## TO 9+ polish

- Chest vs spine margin: idle 4.92 vs the 5 limit. Breath pitch 2.0 -> 1.8 at L419 gives about 4.6.
- Knee settle: the ground min is -0.018 at f20 (SETTLE L488 is 0.008). 0.005 keeps the knee near -0.015, so it sits in the snow for less time.
- Re-render `renders/_roar_jaw_close.png` into the newest set. The only copy is from 01:00, so the roar jaw claim is not in this round's evidence.
- Gold counts (52 px portrait, 27 px game) are the builder's kit-counter numbers. Re-measure them with the same tool so the reviewer can check them.
- Walk stays at 7. Arms swing 4 deg (L447) and read as little motion at strip size. A 5-6 deg swing would help, with no evidence it is needed for the gate.

**Summary**
- Model 8.0 (FIX) and clips 7.5 (FIX). Both under 8.5.
- Round-2 model items: legs PARTIAL (knee ledge, knee cap 0.016 proud), hips PASS, chest-to-pelvis PARTIAL.
- Round-2 clip items: kneel PARTIAL (3/4 OK, game camera partial, left fist off the thigh), idle PARTIAL.
- MUSTs: M1 knee ledge and cap, M2 belt groove, M3 left fist on the thigh, M4 game-camera kneel silhouette, M5 idle arm sway.
