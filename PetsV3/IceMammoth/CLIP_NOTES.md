# Ice Mammoth - clip notes (clip gate, 2026-10-27)

References: `ANIM_REFS.md`: Muybridge plate 733 "Elephant walking", read frame by frame, plus 1014 refs #3, #5 and #9. No
animationreference.org clip could be played (the pane was hidden and Chrome froze).

| clip | frames | loop | events (frame) | what it is |
|---|---|---|---|---|
| idle | 120 | yes | `exhale` f80 | trunk swing: a lagged side-to-side chain (tip about ±19 deg, 2 cycles), 3 breaths (chest 4.5 deg, back rises 0.03; lungs empty at f80), an ear flap at f40 (18 deg out + 16 lift), exhale at f80 with the head lifting (head 8 + neck 4 deg + neck_lift: the dome rises 0.077 BU f70 -> f80), the trunk tip lifting and the ears flicking out; tusks still |
| walk | 40 | yes | `stomp` f10 (FL touch-down) | heavy lateral-sequence walk (BL f0, FL f10, BR f20, FR f30), duty 0.72; the body is at -0.022 at the hind contacts and sinks 0.030 to the fore contacts, ±2.5 deg roll, 0.7 deg pitch rock; feet lift 0.15 and stay nearly flat (5 deg toe; the fore sole's lowest point rises 0.132); trunk pendulum about 11 deg + side swing 6 deg a step; tail lags. Stride 0.319 |
| roar | 66 | no | `trumpet` f26 | TRUMPET: head tuck f0-8; head up 13 + neck 2 (15) by f22 with the neck reaching forward; the trunk rises straight to the sky (f16-26); jaw opens after the lift; hold f26-50 with a ±2 deg trunk tremble, ears spread, tail up; slower return f50-66 |
| act_dustover | 100 | no | `scoop1` f20, `dust1` f56, `scoop2` f66, `dust2` f74, `scoop3` f80, `dust3` f86 | DUST OVER THE BACK: scoop at the forefeet; lift in front of the face; cocked hold f44-48; flick up and back over the brow f48-56; two smaller scoop + flick beats; one tail flick; exact rest |

## VFX anchor bones (no mesh)
`FX_SnowSpray` [Trunk_Tip], `FX_TuskSparkle_L` [Tusk_L], `FX_TuskSparkle_R` [Tusk_R], `FX_FrostPuff` [Back], `FX_IceCrack` [Foot_FL],
`FX_BreathCloud` [Breath].

## Checks (headless_full step 1 + `_scratch/limits.py`)
- **Collisions:** `collision_free: true`, step 1, all 4 clips.
- **ground_min_z:** idle 0.018, walk 0.015, roar 0.018, act 0.018 (the dark foot soles).
- **Audit:** linear 0; idle and walk loops closed (loop_pos 0, loop_rot 0); walk slide 0.0; idle foot drift 0.
- **Pose limits:**

  | clip | neck max | chest vs spine | head + neck pitch-up | max adjacent-frame swing |
  |---|---|---|---|---|
  | idle | 0.6 | 0.5 | 1.1 | 4.0 |
  | walk | 0.8 | 1.7 | 0.2 | 6.1 |
  | roar | 2.0 | 1.0 | 16 | 20.8 |
  | act_dustover | 2.0 | 0 | 17 (plan cap 20) | 43.6 (Trunk4, flick 1 → scoop 2) |

## Changes made for the clips
- **Model, round-2 NICE:**
  - Tusk cap edge: a pale ICE_MINT ring (190,240,230) from t 0.52 to 0.60, +0.002 proud, under the mint cap.
  - Two big wool head clumps replace the four small ones.
  - Eye socket tightened to (0.078, 0.012, 0.024).
- **Model, for the clips:**
  - The skull and the wool dome are 0.04 shorter at the back (back faces y -0.82 → -0.865 world). Without this, the
    dome hit the shoulder hump when the head lifted.
  - The head's pitch-up is paired with the neck reaching forward (`neck_lift`: up to -0.05 y and +0.045 z), so the dome
    clears the hump.
- **Rig:** a throat hinge in `joints()` (r 0.09 across the throat). The skull's lower back corner meets the chest bib at
  the pivot, and those slivers are ignored.
- **Height** is unchanged at 1.76 (HEIGHT 9.0). Tris 13,716.

## Round 3 (clip review 3, 2026-10-27)
Every number below comes from `_scratch/verify.json`, one saved run of `_scratch/verify.py` (it replaces the unsaved
`limits.py` lines). The step-1 JSON is in `_scratch/full_step1.txt` and the measured footfalls in `_scratch/footfalls.txt`.

### M1: the scoops reach the snow
- At each scoop the head dips 13-14 deg (neck 3, with the neck reaching forward so the chin clears the bib) and Trunk4
  pitches +45, so the tip opening turns down into the snow.
- **FX_SnowSpray** (the spray anchor at the tip opening):
  - world z f20 0.016, f66 0.018, f80 0.018; act minimum 0.008.
- **Trunk_Tip bone head:**
  - f20 0.057, f66 0.059, f80 0.059; minimum 0.045 at f65.
  - That bone sits in the middle of the tip block, 0.058 above its underside, so the mesh is on the snow when the bone
    reads ~0.06.
- **ground_min_z** act -0.019 at f65 (the tip touching); collision_free true at step 1.
- Scoops 2 and 3 are slightly shallower than scoop 1, and flicks 2 and 3 are smaller, keeping each reversal under the swing
  limit: max 46.6 deg on the trunk tip, f62.

### M3: the limits, reconciled
- `chest_vs_spine` is the Chest bone's LOCAL rotation; the Chest is parented to the Spine, so that IS the chest-vs-spine
  angle.
- Mammoth maxima:
  - chest vs spine: idle 0.5, walk 1.68, roar 1.0, act 0
  - neck: 0.6 / 0.8 / 2.0 / 3.0
  - jaw: 1.5 / 1.0 / 14.0 / 2.0
  - head pitch-up: 1.1 / 0.2 / 16.0 / 17.0
- The "6 / 4.4" in my gate message were the maxima across all three pets (the Rhino neck 6.0, the Yeti chest 4.4), not
  the Mammoth.

### M4: end at rest
- Largest per-bone rotation, frame 0 vs the last frame: roar 0.0, act 0.0.
- Both also match the bind pose (0.0).

### M5: the throat-hinge exemption
- Raw step-1 crossings with no hinge: Head-Chest idle 6, walk 15, roar 6, act 7. That is all of them; with the hinge the
  count is 0, so every crossing lies inside the throat capsule.
- Close-ups at roar f22 and act f48: `renders/_throat_close.png`. The cheek, ear and chest bib meet with no visible cut.
- The trumpet jaw (14 deg) at the mouth: `renders/_jaw_roar_sheet.png`. No see-through; the trunk and pale chin cover it.

### Walk fix found while verifying
- `cm.quad_walk(gait="walk")` measured as touch-downs BL f0, FR f10, BR f20, FL f30. That is a DIAGONAL sequence, not
  plate 733's lateral one.
- The walk now sets its own offsets (BL 0, FL 0.75, BR 0.5, FR 0.25). Measured: **BL f0, FL f10, BR f20, FR f30**
  = LH, LF, RH, RF.
- `stomp` moved to f10 (0.25), the FL touch-down, for `FX_IceCrack`. The body roll is re-phased toward the planted side.
  Slide 0.0; loop closed.

### Event convention (all pets)
- Events are clip-length fractions, `round(f / n, 3)`, the same as live ThunderRex.
- `CreatureAnimator._events` fires at `t = frac * len` seconds; loops use the phase, so the walk is covered too.

### NICE
- **1:** the eye slit is narrower: MINT (0.070, 0.008, 0.012) and pupil (0.008, 0.004, 0.011), in the same black socket.
- **2:** FX_SnowSpray at the scoops sits at 0.016-0.018 (above).
- **3 (C1 aqua check):** still open for the Studio capture.
- **4:** the walk beats now include f5 and f35 (`renders/_beats_rw_*`).

### References
- M2 is pending: the central `_review/ANIM_REFERENCES_1027.md` has not landed yet.

### References round (2026-10-27)
The central `ANIM_REFERENCES_1027.md` refs are cited in `ANIM_REFS.md` (the "Central references" section), with the timing changes they caused. After the changes the checks were re-run: step-1 collision_free true; all limits and end-at-rest unchanged (`_scratch/verify.json`, `_scratch/full_step1.txt`).

## Final 8.5 gate round (2026-10-28, `_review/IceMammoth_final85.md`)
Numbers: `_scratch/verify.json` (03:22), step 1 + export `_scratch/export_result_f85.txt` (03:21).
- **C1 idle:** trunk roll amplitudes (2.0, 3.0, 3.5, 3.5) -> (2.7, 4.0, 4.7, 4.7) (tip +-12 -> +-16 deg); a second ear
  flap `8 * bell(f, 40, 6)`; TO9 2: chest breath 0.5 -> 1.2 deg. Idle foot drift 0; ground 0.018. Ref: the
  `/tags/elephants` clip is now readable (see `ANIM_REFS.md`). Sheets: `renders/_beats_f85_irw_tq.png` / `_side.png`
  (idle f0 / 20 / 40 / 60 / 80 / 100, roar f0 to f66, walk f0 / 10 / 20 / 30).
- **C2 scoops:** each scoop holds its deepest pose 4 frames: f18-22, f64-68, f78-82. To keep FX_SnowSpray <= 0.012
  across the holds while the trunk only grazes the snow, the tip curl at the holds is 40 (scoop 1) / 38 (scoops 2-3), was
  45, and the head dips 0.5 deg more. FX_SnowSpray z on the hold frames: **0.010** (f18-22), **0.0111** (f64-68, f78-82).
  Trunk mesh lowest on the holds -0.013 / -0.014; act ground_min_z **-0.016** (f24, the roll-through; was -0.019).
  Getting into and out of the holds 1-2 frames faster pushed the one-frame swing over 60, so: a curl-in key at f63 and
  f76 (the tip curls before it reaches the snow; without them the tip dug to -0.026 / -0.021), flick 2 and flick 3 are
  smaller (still smaller than flick 1). Max one-frame swing **53.7** (FX_SnowSpray, f76). Events unchanged. Sheets:
  `renders/_beats_f85_act_tq.png` / `_side.png` (f10 to f100, every hold frame).
- **TO9 3 roar:** jaw 14 -> 18 at f34 (16 at f50); the trunk root lifts 0.02 (Trunk1 loc, with the trunk's rise); a dark
  mouth interior on the jaw. Head pitch-up 16.0; jaw max 18.0.
- **Limits:** neck max 0.6 / 0.8 / 2.0 / 3.0 (<= 8); chest vs spine 1.2 / 1.68 / 1.0 / 0 (<= 5); head pitch-up roar 16.0,
  act 17.0 (<= 30); one-shots end at rest 0.0.
- **Step 1 (with export):** collision_free true; ground_min_z idle 0.018, walk 0.015, roar 0.018, act -0.016; linear 0;
  loops closed; walk slide 0; idle foot drift 0.

## Final gate round 2 (2026-10-28)
Numbers: `_scratch/verify.json` (03:48), step 1 + export `_scratch/export_result_f85r2.txt` (03:51).
- **CM1 roar mouth from the side:** Trunk1 lifts 10 deg more from f26 to f30 and holds to f50 (-66 -> -76, the tremble
  rides on it); jaw f34 18 -> 20 (f50 16); with the hinge moved back the chin drops clear of the cheek, and the dark
  interior shows from the side as a dark wedge between the cheek and the dropped chin (`renders/pclose_side_roar_34.png`),
  and fully from tq / front / below (`renders/_roar_mouth.png`, camera on the Jaw). From a pure side view the tusk root
  and cheek still cover part of it (that is where a mammoth's mouth sits). Jaw max 20.0 (<= 22), head pitch-up 16.0.
- **Polish:** idle chest breath 1.2 -> 2.0 deg (chest vs spine 2.0); f40 ear flap 8 -> 10; roar hold tremble +-2 -> +-3 deg
  (f28-48).
- **Limits:** neck 0.6 / 0.8 / 2.0 / 3.0; chest vs spine 2.0 / 1.68 / 1.0 / 0; head pitch-up roar 16.0, act 17.0; max
  one-frame swing roar 20.8, act 53.7; FX_SnowSpray on the scoop holds 0.010 / 0.0111; ends at rest 0.0.
- **Step 1:** collision_free true; ground idle 0.018, walk 0.015, roar 0.018, act -0.016; linear 0; loops closed; slide 0;
  idle foot drift 0. Sheets: `renders/_beats_f85r2_irw_tq/side.png` (idle, roar f0-f66 incl. f30 / f34, walk f0 / 10 / 15
  / 20 / 25 / 30), `renders/_beats_f85r2_act_tq/side.png`.

## Final gate round 3 (2026-10-28 04:38, exported 04:42)
- CM1b roar mouth from the side:
  - Jaw f34 is now 22 deg (verify jaw_max 22.0 @ f34).
  - The cheek blocks (z down to ~0.97) hang over the chin, so from the side the hinge alone only showed a thin wedge. The roar Jaw key also slides the jaw down `JAW_DROP * max(0, jw - 6) / 16`, which is 0.020 at f34, 0.0125 at f50 and 0 outside f22-58.
  - In `pclose_side_roar_34` the dark opening is a 26 px band (y 204-229, column x 140) over a 47 px chin block = 0.55 of the chin height (target >= 0.25).
  - The head pitch-up was left at 16. A pure side camera looks along the pitch axis, so pitching the head can't uncover what the cheek hides. The 30 limit is untouched.
- 9+ act flick: the Trunk1 root is 5 deg higher on the f44/48/52/56/58 keys (-55/-57/-65/-70/-68). FX_SnowSpray z at f56 = 1.730, at the dome-top height (bbox top 1.76), so the flick now passes over the brow. Max swing is still 53.7 (f76), head pitch-up 17, and the hold tips stay at 0.0111.

## Per-clip audit round 4 (2026-10-28 05:56, exported 05:57)
- Idle (8.3):
  - Ear flap at f40: 10 -> 13 deg. Chest breath: 2.0 -> 3.0 deg (chest vs spine 3.0). Trunk roll amplitudes: (2.7, 4.0, 4.7, 4.7) -> (3.2, 4.8, 5.6, 5.6).
  - Tip (FX_SnowSpray) travel f0 -> f20 is 0.253 BU: (0.069, -1.439, 0.114) -> (-0.142, -1.532, 0.219).
  - In `beat_f85r4_iw_side_idle_040` (390 px), the ear fringe's front edge sits 10 px further forward than at f30 (x 172 -> 162) and shows 3x the area. The flap is a yaw about the vertical axis, so from the side it reads through the fringe and the ear's shading, not the outline.
- Walk (8.4):
  - Body roll ±1.5 -> ±2.5 deg (same phase, toward the planted side). Spine pitch rock 0.4 -> 0.7 deg, sink 0.008 -> 0.012, so the back line moves.
  - Trunk side swing (one cycle) 3 -> 6 deg summed (1.2, 1.6, 1.6, 1.6). The fore-aft pendulum per step is (2.3, 3.0, 3.0, 3.0), phase 0.2 -> 0.3 so it peaks at the steps.
  - Tip travel f10 -> f20 is 0.214 BU, all in the side plane: (-1.616, 0.220) -> (-1.425, 0.124). The prescribed 6 deg on the pendulum alone gave 0.094, and the lower bones' lag cancels at f10/f20, so the pendulum needed about 11 deg plus the phase shift.
  - Stride 0.3194, slide 0.0, foot_z_var 0.0, loops closed.
- NICE: MOUTH_IN moved 0.01 back (y -1.09). The side roar f34 dark band is still 26 px.
- Gates: collision_free true; ground idle 0.018 / walk 0.015 / roar 0.018 / act -0.016; idle foot drift 0; neck 0.6 / 0.8 / 2.0 / 3.0; chest vs spine 3.0 / 1.68 / 1.0 / 0; walk max swing 7.9. The roar and act are unchanged: jaw 22, pitch-up 16 / 17, act max swing 53.7.
- Sheets: `_beats_f85r4_iw_side.png` and `_beats_f85r4_iw_tq.png` (390 px, 05:57, file 05:56), plus `_roar_mouth.png`.

## Final gate round 5 (2026-10-28 08:14, exported 08:16)
- M1, idle ear flap at f40: 18 deg out (was 13), plus a new 16 deg lift of the back edge (a pitch, in the side plane). `ears()` gained a `lift` argument.
  - Ear vertex travel f30 -> f40 (`_scratch/vert_travel.py`): 0.0619 BU in the side (y, z) plane (target 0.06) and 0.064 BU out. The 18 deg out-swing alone moved the edge only about 0.005 in the side plane.
  - In the 390 px side render, the fringe's front edge moves 9 px forward (x 172 -> 163). The scale is about 112 px/BU (dome-to-sole 198 px for 1.76 BU), so 0.062 BU is about 7 px.
- M2, idle breath: chest 4.5 deg (chest vs spine 4.5 @ f0). The Spine breath term is now +0.03 (the back rises). The back line moves 2-7 px across the idle (x 200 / 230 / 260: 2 / 7 / 3 px). Idle foot drift 0; idle ground 0.018.
- M3, walk:
  - (Corrected in round 6: b = 0.5 - 0.5 cos(4 pi f / 40) is 0 at the HIND touch-downs f0 / f20 and 1 at the FORE touch-downs f10 / f30. It is not 0 at all contacts.) The suggested `-0.004 - 0.030*b` raised the body 0.018 at the hind contacts (f0 / f20), and the straight hind stance legs could not reach the ground: slide 0.0013, foot_z_var 0.0088.
  - I used `-0.022 - 0.030*b` instead. The body is highest (-0.022, as before) at the hind touch-downs and lowest (-0.052) at the fore touch-downs, a 0.030 sink per step. The Spine head moves z 0.978 -> 0.948. This is 3x the 0.010 Williams basis in `ANIM_REFS.md` and goes against plate P5 ("the back stays level"). It is a deliberate exaggeration for phone-scale readability, asked for in round 5 (M3); see `ANIM_REFS.md`.
  - Slide 0.0, foot_z_var 0.0, stride 0.3194, walk ground 0.015.
  - Back-line travel in the 390 px side render: 4 / 5 / 3 px at x 200 / 230 / 260 (0.030 BU is about 3.4 px). Trunk tip f10 -> f20 is 0.206 BU.
- Per clip:
  - Idle: chest vs spine 4.5, neck 0.6, pitch-up 0.8, max swing 6.4 (Ear_L f38).
  - Walk: chest vs spine 1.68, neck 0.8, max swing 7.7.
  - Roar: jaw 22, pitch-up 16, neck 2.0.
  - Act: pitch-up 17, max swing 53.7, holds 0.0111.
  - collision_free true; loops closed; tris 14,688.
- Sheets, all rendered from the 08:14 file:
  - `_beats_f85r5_iw_side.png`, `_tq.png` and `_game.png` (390 px).
  - `_beats_f85r5_act_tq.png` and `_side.png`.
  - `_model_sheet.png` and `_close_sheet.png`. The icon and strips are re-made.

## Final gate round 6 (2026-10-28 08:53, exported 08:55)
- MUST 1, idle exhale (f80):
  - The head lifts 8 deg (was 1.5) and the neck 4 deg (was 1.0). The Neck takes `loc=neck_lift(head + neck)`, so it reaches up and forward.
  - The breath phase moved 0.25 -> 0.75, so the lungs are empty at f80. At the old phase f80 was the full-inhale peak: the 4.5 deg nose-down chest breath dropped the head 0.036 BU against the lift, and the dome only rose 0.029.
  - I also tried flipping the chest breath to nose-up. It raised the shoulders 0.06 and the straight forelegs lifted off (idle foot drift 0.056), so it was dropped.
  - Dome top (the head's highest vertex, `_scratch/top_low.py`): 1.7558 at f70 -> 1.8323 at f80 = **0.077 BU** (target 0.07). In the 390 px renders it is **5 px in game**, 9 px side and 9 px tq.
  - Idle: neck 4.0 (limit 8), head + neck 12, pitch-up 11.67, chest vs spine 4.5 (limit 5), idle foot drift 0, loop closed.
- MUST 2, walk foot lift 0.075 -> 0.15:
  - `pk.walk_cycle` is inlined in `walk()` so the lifted foot can keep a nearly flat sole (toe 5 deg x lift fraction). The kit's 35 deg toe-down at full lift kept the pad's front edge only 0.066 up.
  - Fore sole lowest point: 0.018 planted -> 0.150 at f4 (FL) and f24 (FR) = **0.132 BU**, about 15 px in the 390 px side render at about 112 px/BU. Hind soles: 0.018 -> 0.061.
  - From the game camera (behind and above) the fore feet are mostly behind the barrel. The lift reads in the side and tq views.
  - Slide 0.0, foot_z_var 0.0, stride 0.3194, walk ground 0.018, collision_free true (cuffs vs the other legs: none). Walk max swing 11.3 (Shin_FL).
- Notes fixed: b and the contacts (above), the walk sink against Williams and P5 (`ANIM_REFS.md`), and the summary table rows.
- Per clip:
  - Idle: chest vs spine 4.5, neck 4.0, pitch-up 11.67.
  - Walk: chest vs spine 1.68, neck 0.8, pitch-up 0.47.
  - Roar: jaw 22, pitch-up 16, neck 2.0.
  - Act: pitch-up 17, max swing 53.7, holds 0.0111.
  - Ground 0.018 / 0.018 / 0.018 / -0.016; tris 14,688.
- Sheets:
  - `_beats_f85r6_idle_game.png`, `_side.png` and `_tq.png` (390 px).
  - `_beats_f85r6_walk_game.png`, `_side.png` and `_tq.png` (390 px).
  - `_model_sheet.png` and `_close_sheet.png`. The icon is re-made.

## Final gate round 7 sign-off (2026-10-28; no re-export, the ship file is still the 08:55 export)
- Fore-sole lift per frame (the lowest vertex of the Foot bone's mesh, `_scratch/top_low.py`; planted = 0.018; lift = low - 0.018):

| frame (FL) | 0 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| sole low z | 0.0617 | 0.1406 | 0.1499 | 0.1489 | 0.1376 | 0.1169 | 0.0885 | 0.0546 | 0.018 |
| lift | 0.044 | 0.123 | **0.132** | 0.131 | 0.120 | 0.099 | 0.071 | 0.037 | 0 (lands) |

  FR is the same curve 20 frames later: f23 0.123, **f24 0.132**, f25 0.131, f26 0.120, f27 0.099, f28 0.071, f29 0.037, f30 lands.
  - The peak lift is f4-f5 (f24-f25). By f8 the foot is already coming down (0.071), so the f5-f8 range in the round-6 MUST spans the peak and the descent.
  - The reviewer's ~0.10 at f8 from pixels is probably the pad's heel or its centre: the toe tilt is 5 deg x lift fraction, so the back of the pad sits a little higher than its lowest point.
- `pets/IceMammoth.py`: the walk body comment (the sink, b at the hind/fore contacts, the roll, the lift) now matches the code. Comment only, so no re-export.
