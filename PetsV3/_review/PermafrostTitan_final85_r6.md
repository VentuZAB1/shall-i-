# Permafrost Titan - FINAL 8.5 GATE, ROUND 6 (model + clips, export 2026-10-28 08:24) - FIX

**Model: 8.4/10 - FIX. Clips: 7.9/10 - FIX.**

Per clip: idle 8.0, walk 8.2, roar 8.1, act (kneel) 7.9. The clips score is the lowest, so it is **7.9 (act)**.

Owner bar: 8.5 is the floor for the model and for every clip. Nothing under 8.5 ships.

Summary: round 6 fixed the head (MD1) and the shoulder/fist crust plates (MD2, at 2x). The kneel now turns the whole body 18 deg, so the shin is no longer straight at the game camera, but it still does not read as a kneel from behind. The idle and walk arm travel is better but still small at phone size. The roar arms are asymmetric in this build. The torso still reads as stacked bands, and the 64 px crust check is not on the current build.

## What I looked at

- Brief: `GLACIER_REVIEWER_BRIEF.md`. Round 5 review: `PermafrostTitan_final85_r5.md`. Builder notes: `PermafrostTitan\MODEL_NOTES.md` (ROUND 5 section), `CLIP_NOTES.md` (ROUND 5 section), `ANIM_REFS.md`.
- Source: `PetsV3\pets\PermafrostTitan.py` (line numbers below).
- Renders, newest set, all opened and loaded: `renders\_model_sheet.png` (08:22), `_kneel_2x_f40_f50.png` (08:22, tq and game), `_kneel_views.png` (08:22), `_beats2x_idle.png` (08:22), `_beats2x_roar.png` (08:22), `_beats2x_kneel.png` (08:22), `_walk_sheet.png` (08:22), `_roar_jaw_close.png` (08:22), `_pose_tq_sheet.png` (08:24).
- **Stale files (not the round 6 build):** `_icons_strip_64.png` and `_icons_strip_128.png` are dated 04:21 (round 4 build). `_close_sheet.png` is dated 03:28. Neither shows the round 5 head or crust changes. I judged the face on `_roar_jaw_close` f0 and `_model_sheet` instead. The 64 px check is open (MD-B).
- Logs (`PermafrostTitan\_scratch\`): `export_r5.txt` (headless result), `arm_r5.txt` (ARMPROBE), `ang_r5.txt` (ANGALL), `tris_r5.txt`, `joints_r4_f40.txt`.
- No image failed to load.

## Numbers (logs, not re-run)

- Tris body **7,820** (cap 15k). PASS.
- `collision_free` true, `collisions` {} (no pairs in any clip, so head vs neck/shoulders 0 pairs). PASS.
- Linear 0 on all clips. Loops 0 / 0 (idle, walk). Walk slide 0.0. Idle foot drift 0.0. PASS.
- `ground_min_z`: idle 0.000, walk 0.000, roar 0.000, act **-0.017** (f20). PASS (limit -0.02, at the edge).
- Chest vs spine (max, deg): idle 4.85, walk 3.61, roar 3.0, act 4.68. All <= 5. PASS.
- Head pitch (lead ruling: head + neck <= 30, no Neck bone): roar 15.0, act 14.1. PASS. Idle head yaw 13.5 (one slow look, not a shake).
- Fist travel (ARMPROBE): idle L f0-f30 **0.105**, R f0-f30 **0.023** (cycle ranges L 0.106, R 0.087); closest fist-to-thigh gap idle 0.068 (L) / 0.066 (R). Walk: cycle range 0.206 each side, f0-f30 L 0.083 / R 0.071, closest gap 0.060.
- Gold at 64 px: **not measured on the current build** (the icon strip is stale). Round 4 figures for reference: 27 kit counter, 20 render window (gate edge).

## Per-clip scores

| clip | score | one line why | evidence |
|---|---|---|---|
| idle | 8.0 | Hip weight shift, breath and the one head look read; the fist range per cycle (L 0.106, R 0.087) is still small at phone size, and R travels only 0.023 from f0 to f30. | `renders\_beats2x_idle.png`; `_scratch\arm_r5.txt` |
| walk | 8.2 | Tq and side read as a heavy stride with clear arm swing (cycle range 0.206 per side). From the game camera (behind) it reads as a bob: the legs are hidden and the lateral motion is small. | `renders\_walk_sheet.png` (tq, game, side rows) |
| roar | 8.1 | Fierce bellow, head 15, jaw opens late and the core pulses. The arms are asymmetric in this build (one out near horizontal, the other drops forward to hip height). Mouth still grey in the kit render (Studio judges it). | `renders\_beats2x_roar.png` (f22, f27, f50); `renders\_roar_jaw_close.png` |
| act (kneel) | **7.9** | Tq kneel reads (knee down, fist on the thigh). The game-camera kneel is better than round 4 (sole turned toward the camera) but still reads as one leg stepping back: the knee on the snow is not legible, and the shin still points close to the camera line. | `renders\_kneel_2x_f40_f50.png` (game f40, f50); `renders\_kneel_views.png` (game f40, f58) |

## Round 5 items

| item | status | evidence |
|---|---|---|
| **MD1** skull 0.172, face offsets x1.075 | **PASS** | Head wider in `_model_sheet` (front and 3/4); brows and slits sit on the skull in `_roar_jaw_close` f0; `collisions` {} in `export_r5.txt`. Head 0.344 BU per MODEL_NOTES. |
| **MD2** crusts two plates, each >= 0.06 | **PARTIAL** | Tris 7,820 PASS. Two plates per pauldron and per fist read at 2x (`_kneel_2x` tq, `_walk_sheet` tq). The 64 px acceptance cannot be checked: `_icons_strip_64` is the 04:21 build. See MD-B. |
| **MC1'** kneel from the game camera (18 deg body yaw) | **PARTIAL** | Yaw works: the shin and foot run off the camera line and the sole and heel plate face the camera at f40 and f50 (`_kneel_2x` game). The knee on the snow is still not visible from behind. Ground -0.017 PASS, collisions none. Still reads as a step, not a kneel. See ACT-1. |
| **MC2'** idle forearm bend +/-4 | **PARTIAL** | Numbers PASS on L (travel 0.105 >= 0.05, gap 0.068, foot drift 0). R travel f0-f30 is 0.023 (fails if both sides are required; its cycle range is 0.087). Visually the idle still reads small at 1x (`_beats2x_idle`). See IDLE-1. |
| **MC3'** walk forearm bend +/-6 | **PASS** | Fist cycle range 0.206 each side (ARMPROBE), closest fist-to-thigh 0.060 (>= 0.03), walk slide 0.0. Visible in `_walk_sheet` tq f12-f30. |
| **MC4'** roar mouth cavity (10, 10, 14) + 0.012 lip | **PARTIAL (open until Studio)** | Kit cavity luma ~81 (79, 81, 84) vs 88 in round 4. Not below 60, so the item stays open until Studio (lead ruling: not scored). Front f27 shows a dark slot under a lit lip, better than round 4's grey panel, but still grey in the kit render. |

Round 5 "TO 9+" status: torso belt bevel **open** (see MD-A); bright white eye slits **open** (visible in `_roar_jaw_close` f0); idle and walk **improved, still open** (IDLE-1, WALK-1); kneel snow puff **Studio** (VFX added in Studio); roar deeper bellow **open** (optional).

ANIM_REFS rule: **PASS** (Plate 27 walk, Plate 356 kneel and rise, #3 / #9 roar, K8a-c cited; the late K8 cuts are disclosed).

## New MUSTs (only what blocks 8.5)

**Model (8.4 -> 8.5)**

- **MD-A. Torso reads as stacked bands (the 8.4 reason, unchanged this round).** From the front the torso shows a dark chest/waist seam (`pets/PermafrostTitan.py` L120, JOINT_D at z 1.165), the ICE_W belly band (L116, z 1.098), the dark belt seam (L113, z 1.03) and then the hips. The side view shows the same stepping.
  - Fix: recolour the chest/waist seam at L120 from `JOINT_D` to `MAUVE`. Geometry and collisions stay the same. The dark band goes, so the chest and waist read as one mass.
  - Acceptance: `_model_sheet` side view shows one dark seam above the hips (the belt); front view shows chest and waist as one mass; `collide_where` no new pairs; ICE_W share on `flat_game` still >= 12 % (`_scratch\shares_all.py`).

- **MD-B. Evidence for MD2 and the gold check is stale.** `_icons_strip_64.png` and `_icons_strip_128.png` (04:21) and `_close_sheet.png` (03:28) predate round 5.
  - Fix: re-render these three on the 08:24 build (no model change). Log the game-camera gold px at 64.
  - Acceptance: the first 64 px icon shows the shoulder crust as two clear masses, not a white fringe; gold stays >= 20 px on the game camera (round 4: 20 on the render window, at the gate edge).

**Clips (each below 8.5)**

- **ACT-1. Game-camera kneel (act 7.9 -> 8.5).** The round 5 body yaw (`YAW_K = 18.0`, L79) puts the shin about 21 deg off the game camera line, which is still close enough that the leg reads as one block. The round 4 shin rise (21.5 deg, `joints_r4_f40.txt`) is unchanged, since round 5 changed only yaw. I am not re-proposing the ankle change the lead ruled out.
  - Fix: raise `YAW_K` from 18 to **30** (same ease in f12-18, hold to f52, out by f62, same pivot on the planted right ankle). This is above the 15-20 deg range in the brief, so the lead must rule on it.
  - Acceptance: from the game camera at 2x, f40 and f50 show the shin as its own limb (not overlapping the thigh), the sole and heel plate toward the camera, and the knee cap on the snow; `ground_min_z` >= -0.02; `collide_where` 0 pairs; chest vs spine <= 5.

- **IDLE-1. Idle arm motion too small (idle 8.0 -> 8.5).** Fist cycle range is 0.106 (L) and 0.087 (R), and R moves only 0.023 from f0 to f30.
  - Fix: arm sway amplitude `sway = 5.0 * sn(f, n)` (L449) to **7.0**. The chest is not touched, so chest vs spine stays put.
  - Acceptance (ARMPROBE): fist cycle range >= 0.12 BU on both sides; closest fist-to-thigh gap >= 0.04; `collide_where` 0; idle foot drift 0; chest vs spine <= 5.

- **WALK-1. Walk not readable from behind (walk 8.2 -> 8.5).** From the game camera the legs are hidden and the lateral motion is only the pelvis roll (0.022 BU) and the chest roll (3.0 deg).
  - Fix: in the walk keys (find the pelvis roll and the per-step chest roll), raise the pelvis roll over the stance foot from 0.022 to **0.035 BU**, and the chest roll from 3.0 to **3.5 deg**.
  - Acceptance: `_walk_sheet` game row (f0, f12, f24, f36) shows the shoulder line tilting step to step; chest vs spine <= 4.5 (now 3.61); walk slide 0.0; `collide_where` 0.

- **ROAR-1. Roar arms asymmetric (roar 8.1 -> 8.5).** At f22, f27 and f50 the screen-left arm goes out near horizontal, while the other arm drops forward with its fist at hip height (`_beats2x_roar`; `pose_tq_roar_22`). `arms_fk` (L425-429) sends both sides the same `out` value with opposite signs (`-s*out`), so both arms should go out. The asymmetry points at the Arm_R bone roll or the mirror sign of the out term.
  - Fix: check the Arm_R bone roll against Arm_L and the `-s*out` sign; correct so both arms swing out equally.
  - Acceptance: re-render a FRONT roar sheet (f0, f22, f27, f50). At f27 the two fists are at the same height within 0.03 BU, and each arm's out angle matches within 2 deg.

**Open, Studio (not scored, per lead ruling)**

- MC4' roar mouth: judge the dark opening in Studio. Stays open until seen there.
- Kneel snow puff (icecrack anchor `Knee_L`): VFX in Studio.

## TO 9+ (not blocking)

- Belt seam at L113: a 0.02 BU bevel on the belt lip (round 5 suggestion), to soften the step.
- Eye slits: darken the bright white highlights toward (200, 220, 236) (round 3 suggestion; still open).
- Roar: the head pitch of 15 leaves room for ~18 deg, for a deeper bellow if the lead wants more drama.
- Idle: the head look happens once; a second, smaller look later in the cycle would add life.
- Walk: a small shoulder counter-rotation against the pelvis roll would make the upper body read as weighted.

## Pass / fail checklist

- Silhouette and species at phone size: PASS (fierce titan; reads as a titan).
- Face (brows, slits, closed mouth): PASS on the current build.
- Gold hero: PASS in the 1x views (not re-measured at 64 px; MD-B).
- Stud skin, no spikes, no glow: PASS.
- Tris 7,820 (cap 15k): PASS.
- Stacked torso bands: **FAIL** (MD-A).
- Crust at 64 px: **UNVERIFIED** (MD-B).
- Collision-free, linear 0, loops closed, idle drift 0, walk slide 0: PASS.
- Ground minimum -0.017 (act): PASS (edge).
- Chest vs spine <= 5: PASS (all clips).
- Head + neck pitch <= 30: PASS.
- Kneel legible from the game camera: **FAIL** (ACT-1).
- Idle readable at phone size: **FAIL** (IDLE-1).
- Walk readable from behind: **FAIL** (WALK-1).
- Roar arms symmetric: **FAIL** (ROAR-1).
- ANIM_REFS rule: PASS.
