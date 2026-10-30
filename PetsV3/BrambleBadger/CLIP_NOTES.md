# Bramble Badger - sign-off check (round 7 PASS, 2026-10-28 08:37)
- Re-run on the final saved `pets/BrambleBadger.py` (08:21:36, byte-identical to `_scratch/BrambleBadger_f85r6.py`, exported 08:25):
  - head/jaw/ears vs chest blocks: act f5-68 **0.0116** (f68), whole act 0.0105 (f90), roar f0-45 **0.0277**, walk **0.0231**, rest 0.037. All >= 0.010.
  - Neck vs chest: -0.022 at rest, -0.028 deepest. This is the tuck, hidden inside the cape.
- The pose limits hold. The numbers are identical to the r6 table (chest vs spine <= 2.92, neck <= 7.87, head pitch-up <= 6.25, head yaw <= 2.99 deg/f, 0 flips).
- collision_free, ground -0.002, loops closed, foot drift / slide 0.0.
- No change, no re-export.

# Bramble Badger - clip notes (8.5 gate round 6, 2026-10-28)

## Round 6 (`_review/BrambleBadger_final85_r6.md`)
- **MUST 1, the nape slab is gone:**
  - The lavender MANTLE nape seg is removed: it read as a second box on the cape.
  - The neck between the head and the cape is now ONE dark BELLY_D column. The throat seg grew up to just under the skull top: (0,-0.43,0.38)->(0,-0.58,0.385), half 0.11 x 0.12. It is narrower than both the head (0.15) and the cape (0.245).
  - Nothing MANTLE-coloured is on the Neck bone any more. The reviewer's limits (front y >= -0.470, underside z >= 0.305) hold trivially.
  - The shorter test nape (start (0,-0.42,0.44) r 0.13 -> end (0,-0.47,0.44) r 0.12) left a see-through gap between the skull and the cape in the low side view, so it was not kept.
  - Thorn 1 sits on the dark neck: y -0.455, z 0.505.
  - Evidence: `renders/_neck_evidence_r6.png`, rest / act f64 / act f68 x low side / low front-left 3/4 / high 3/4. Normal colours, plus `BADGER_NECKDBG=1` (all Neck parts magenta).
    - Magenta shows only between the head and the cape front and as the throat under the chin; none on the cape top or front, none below the cape edge.
  - Head clearance is unchanged: act f5-68 0.0116 (whole act 0.0105), roar 0.0277, walk 0.0231.
  - Neck vs chest overlap is now -0.022 at rest and -0.027 deepest (act f14), shallower than r5 (-0.033 / -0.042). It is hidden inside the cape.
- **MUST 2, readable act beats:** `renders/_act_beats_r6.png`. 2x side (dist 1.6) and 2x game (dist 1.9) at 600 px; red lines are the paw lift, projected and measured.
  - At the first try (lifts 0.026 / 0.028) the game scoops were 13.1-13.6 px, under 15. So the scoop and kick lifts are now **0.035** (kick toe -8.75).
  - Scoop peaks f11 / f21 / f31: side **28.3 px**, game **16.0 / 15.5 / 16.0 px**.
  - Kick peaks f44 / f53: side **28.3 / 28.3 px**, game **17.6 / 17.7 px**.
  - f16 / f26 / f36 are the dig-event sweeps: the paw is on the ground there, with 0 lift.
  - Note: from the game camera (behind / above) the FRONT scoops sit under the body, so they are hidden even though their projected lift is >= 15 px. The hind kicks are visible.
  - Act ground -0.002, chest vs spine 1.25.
  - The scoop stroke is now the fastest limb motion: Foot_FL 21.1 deg/f local, Shin_FL 16.2 armature-space at f10.
- **Breath:** the Spine is **+-0.023** (one notch over the asked 0.020, which gave 8.0 px at 1x), and the head counter-pitch is `+3.35*b`.
  - Breath isolated (`BADGER_BREATH` on vs off, same frame): mantle / hull / centre **+-0.0230**, slip **0.0000**, snout at most 0.0024.
  - Game camera f50 -> f70: the rump moves **21 px at 2x = 10.5 px at 1x** (target >= 9). `renders/_breath_game_r6.png`.
  - Lowest head / jaw Z 0.0206; idle foot drift 0.0.
- **Walk knee step:** `renders/_walk_touchdown_r6.png` (f0-2 and f15-17, side 2x + game).
  - The 10.35 deg Shin_FL f0->1 step was not a touchdown flick. It was the leg almost straight at touchdown (body bob highest at f0 / f15).
  - Fixes:
    - the bob now puts the body LOWEST at each touchdown (weight acceptance);
    - the body is carried 0.010 lower;
    - the feet use the Wraith's soft path.
  - Shin_FL f0->1 is now **4.9**, f1->2 2.7; Shin_FR f15->16 5.3. **Walk max limb local step 5.30** (Shin_FR f16), armature-space 5.04.
- **Optional silhouette:** a 0.02 waist tuck on the hull flank, centred at y 0.08, with the waist skirt following. The side no longer reads as a straight loaf. I skipped the mantle crown: a flat 0.01 slab would only add a step.
- **Per-clip sheets** (game / side / tq, whole pet, with the time): `renders/_idle_sheet_r6.png`, `_walk_sheet_r6.png`, `_roar_sheet_r6.png`, `_act_sheet_r6.png`.
- **Per-clip numbers:**

  | clip | chest vs spine | neck | head pitch-up | head yaw max (deg/f) | limb local max | limb armature-space max |
  |---|---|---|---|---|---|---|
  | idle | 1.0 | 7.87 | 3.35 | 1.29 | 4.36 | 2.73 |
  | walk | 2.92 | 3.47 | 0.07 | 1.08 | 5.30 | 5.04 |
  | roar | 1.5 | 7.0 | 0.2 | 0 | 7.46 | 4.37 |
  | act | 1.25 | 6.0 | 6.25 | 2.99 | 21.09 (scoop stroke) | 16.18 |

- All clips: collision_free, ground -0.002, linear 0, loops closed, idle foot drift 0.0, walk slide 0.0, 0 quaternion flips. Acts end at rest.

---

# Bramble Badger - clip notes (8.5 gate round 5, 2026-10-28)

## Round 5 (`_review/BrambleBadger_final85_r5.md`)
- **MUST 1, neck tuck evidence:** `renders/_neck_evidence_r5.png`.
  - Rest, act f64 (the deepest overlap, -0.042) and act f68, from three cameras: a low side camera at z ~0.15, a low front-left 3/4 looking up at the mantle and nape undersides, and a high 3/4 over the mantle top. Each is a close camera ~0.6 units wide.
  - Each frame is shown in normal colours and with the new `BADGER_NECKDBG=1` test switch, which paints every Neck-bone part magenta (nape, dark throat, thorn-1 base).
  - Result: the Neck geometry shows only where the neck is meant to be, between the mantle's front face and the head. Below the cape's lower edge you see only the dark throat (BELLY_D, designed). Nothing pokes through the mantle top or its sides at rest, f64 or f68.
  - So the tuck stays as built. It is a **deliberate deviation** from the >= 0.01 neck clause: the nape's rear end starts inside the cape so there is no gap at the shoulders when the head drops. The lead can rule on it.
  - Head and jaw clearance is unchanged: act f5-68 0.0116, roar 0.0277, walk 0.0231.
- **Walk evidence:** `renders/_walk_sheet_r5.png`, every 3 f (f0-f27), game / side / tq rows, fixed cameras, whole pet. The time is in the title.
- **Per-clip sheets:** `renders/_idle_sheet_r5.png` (f0 / f36 / f50 / f70 / f114), `_act_sheet_r5.png` (f5 / f20 / f44 / f64 / f68 / f80), `_roar_sheet_r5.png` (f12 / f30 / f59). Each has game + side + tq rows, the whole pet and the time.
- **Game-camera crops fixed:** every r5 game frame uses the gate's game camera (target (0,-0.20,0.30), dist 2.8) or wider, so the whole pet is in frame.
  - Breath at the game camera, 2x: `renders/_breath_game_r5.png`. f50 -> f70, the rump block moves **11 px at 2x (5.5 px at 1x)**, measured by cross-correlation.
  - At f50 the head is down behind the hump, as in the sniff.
- **9+, ANIM_REFS:**
  - roar drop 0.10H (code `0.10*H_U`), thorns 22 deg, ears 28 deg, tremble 2.5 deg;
  - act kick 0.070 back + 0.028 lift, touchdown 0.058;
  - the nose-tap numbers.
  - The roar docstring and the kick comment in the code are fixed too.
- **9+, ear twitch:**
  - The outward flick is **28 deg** (`3.5*TWITCH_DEG`), plus 8 deg forward. It does not clip the crest (the ears sit at x 0.128, the thorns on the centre line); collision_free.
  - From the game camera the ears hide behind the mantle hump while the head is down. At the f36 sniff peak the on/off change is only **351 px at 1x** (was 345 at 20 deg).
  - So I added one more twitch at **f111-117, with the head back up**, where the ears clear the hump: **465 px at 1x**.
  - The reviewer's 1000 px target is not reached. The ears are small at that camera, so reaching it would need bigger or more outboard ears (a model change), not more angle. `renders/_ear_twitch_r5.png`.
- **Gates:**
  - collision_free true, linear 0;
  - loops closed, idle foot drift 0.0, walk slide 0.0;
  - ground -0.002 in every clip;
  - 0 quaternion flips.
  - Per clip:

    | clip | chest vs spine | neck | head pitch-up |
    |---|---|---|---|
    | idle | 1.0 | 7.87 | 2.0 |
    | walk | 2.92 | 3.47 | 0.07 |
    | roar | 1.5 | 7.0 | 0.2 |
    | act | 1.25 | 6.0 | 6.25 |

  - Head yaw rate max 2.99 deg/f (act).
  - Local limb steps: walk 10.35 (Shin_FL f1, the touchdown), roar 7.46, act 17.85 (Foot_FL f10, the scoop stroke).

---

# Bramble Badger - clip notes (8.5 gate round 4, 2026-10-28)

## Round 4 (`_review/BrambleBadger_final85_r4.md`)
All numbers are measured headless on the posed, skinned mesh (`_scratch/badger_measure.py`, results in `_scratch/measure_*.json`).

**Correction to round 3:** the r3 idle check compared f0 and f40, which are both breath-neutral (b = 0), so it proved nothing. Thanks to the reviewer for the arithmetic.

- **M1, breath lifts the chest:**
  - Chest pitch `rot=(1.0*d, 0, 0)` (no `1.8*b`). Head pitch `15.5*d - 10*lf + 2.0*b`. Spine loc `-0.010*d + 0.014*b` is unchanged.
  - **Breath isolated** (the same frame with the `BADGER_BREATH` test switch on vs off, so d / lf / yw are identical):
    - at every breath peak / trough (f10 / 30 / 50 / 70 / 90 / 110), the mantle top edge, the shoulder-top centre and the Spine hull top all move **+-0.0140** (0.028 peak-to-peak, about 0.29 studs);
    - the mantle-minus-hull change is **0.0000**, so there is no slip;
    - the snout changes by **at most 0.0017** (limit 0.003); the 2 deg head counter-pitch holds the nose.
  - **f50 (b +1) vs f70 (b -1)**, as the review asked:
    - the shoulder-top centre (x = 0) drops **0.0251** (limit >= 0.024);
    - the mantle top EDGE point at x -0.178 drops only 0.0116, and the mantle-minus-hull difference between those two frames changes 0.0096. Both are the sniff roll (yaw -6 at f50, +4.2 at f70, `3.5*yw/8`) tilting off-centre points, not slip: the breath-isolated slip is 0.0000.
  - Lowest Head / Jaw Z over idle f0-120: **0.0226** (f28), so the nose stays off the floor.
  - Idle: chest vs spine 1.0, neck 7.87, head pitch-up 2.0.
  - Evidence: `renders/_breath_side_r4.png`, idle f50 (peak) vs f70 (trough), Root-fixed side camera, 1100 px, with the ground line. Back top drops **18 px at the shoulder / mantle, 17 px mid-back, 16 px at the rump**: the back moves as one. The nose differs only by the f70 sniff lift.
- **M2, fresh renders on the current model:**
  - `renders/_pose_side_r4.png` (head + mantle framed) and `renders/_pose_tq_r4.png`: act f5 / f20 / f44 / f68, roar f12 / f30 / f59, walk f0 / f8. The time is in each sheet's title bar.
  - **Head-group (Head, Jaw, ears) vs Chest-blocks (mantle + grey shoulder + chest plate) signed clearance:**
    - act f5-68: min **0.0116** (f68), with a 0.0171 hold over the dig;
    - whole act: 0.0105 (f90);
    - roar f0-45: min **0.0277**;
    - walk: 0.0231;
    - rest: 0.037.
  - What was touching: before the fix it was -0.0001 at act f68. The cheek ruff's rear-bottom corner met the mantle's front-bottom edge while the head looked right. I shortened the cheek ruff rear by 0.018 (see MODEL_NOTES round 6).
  - The Neck nape block is built tucked under the cape: -0.033 at rest, deepest -0.042 (act f64). It is hidden under the mantle, never a visible contact. collision_free true.
- **N1:** nose lift `-10*lf` (was 6), matching ref A's 10-15 deg. The head stays below rest elevation (head pitch-up max 2.0).
- **N2, ear twitch:** a 6 f triangle (f33-36-39, f49-52-55, f65-68-71), now 8 deg forward + 20 deg OUTWARD.
  - `ears(splay=)` is new. The sign was checked in a front render: both ears tip out.
  - The outward flick is what reads from the game camera behind the badger; pitch alone is along the view line.
  - Game camera f36, twitch on vs off (`BADGER_TWITCH` test switch): **345 changed px at 1x, 1957 at 2x** (ear region). `renders/_ear_twitch_r4.png`.
  - Idle ear swing max 10.9 deg/f.
- **N3:** sniff roll `3.5*yw/8` (was 2.5).
- **N4:** `ANIM_REFS.md` now matches the build (idle beats, walk numbers, act thorns).
- **N5 (model):** see MODEL_NOTES round 6.
- **Gates:**
  - collision_free true, linear 0;
  - loops closed, idle foot drift 0.0, walk slide 0.0;
  - ground -0.002 in every clip;
  - 0 quaternion flips;
  - chest vs spine: idle 1.0, walk 2.92, roar 1.5, act 1.25;
  - neck max 7.87; head yaw rate max 2.99 deg/f (act).
  - Tris 6,544.

---

# Bramble Badger - clip notes (8.5 gate round 3, 2026-10-28)

## Round 3 (`_review/BrambleBadger_final85_r3.md`)
- **MC1, breath:** the Spine z is now `-0.010*d + 0.014*b` (was 0.010), and the Chest pitch is `1.0*d + 1.8*b` (was 1.2). It runs all loop long, 3 breaths per 120 f.
- **MC2, sniff roll:** the Spine roll is 2.5 * yaw / 8 deg (was 1.5), so the body leans into each nose sweep (f36 +8 / f52 -8 / f68 +5).
- **MC3, crest bristle:** `thorns(k, f, 5.0*br)` (was 3.0). It peaks f70-78.
- **T2, ear twitch:** a 6 deg ear twitch at each sniff peak (TWITCH table: f32-40, f48-56, f64-72, peaks f36 / f52 / f68). It adds to the 16 deg flick (f40-52, f96-108). The two never stack past ~22 deg; the ear swing max is 4.28 deg/f.
- **T1, shoulder hump (model):** see MODEL_NOTES round 5.
- **MC4, numbers (from `_scratch/clipmetrics.json` / `_scratch/fullcheck.json`):**
  - idle: neck max 7.87 (limit 8), chest vs spine 2.8, head pitch-up 1.8, head yaw rate 1.4 deg/f;
  - walk chest vs spine 2.92, roar 1.5, act 1.25;
  - 0 quaternion flips (keys and sampled) in every clip;
  - idle f120 vs f0 0.0;
  - idle foot drift 0.0 (the 0.014 breath moves the Spine only; the feet are planted after it);
  - collision_free true;
  - linear 0, loops closed, walk slide 0;
  - ground -0.002 in every clip.
- **2x crops:**
  - `renders/_idle_2x_r3.png`: idle f0 / f40 / f70, side, Chest target;
  - `renders/_idle_close_r3.png`: tq and game camera, f0 / f36 / f40 / f70. f36 is the first sniff peak, with the ear twitch and the body roll; f70 is the bristle peak.
  - `_scratch/r3/_neck_check.png`: thorn 1 (on the Neck) stays seated on the nape block at f0 and f40.

---

# Bramble Badger - clip notes (8.5 gate round 2, 2026-10-28)

## Round 2 (`_review/BrambleBadger_final85_r2.md`)
- **MC1:** the ear and tail flicks are 12 f each (f40-52 and f96-108, peaks f46 and f102). The ear flick is 16 deg
  (was 10) and the tail flick 14 deg. 2x crops of f40 / f46 / f52 (ear row, tail row): `renders/_flick_2x.png`.
- **MC2:** in the sniff the Spine rolls 1.5 · yaw / 8 deg, so the body follows the nose sweeps.
- **MC3 (numbers straight from `_scratch/clipmetrics.json`):**
  - **chest vs spine max 2.92 deg** (walk); idle 2.2, roar 1.5, act 1.25;
  - neck max 7.87;
  - head pitch-up 6.25;
  - head yaw rate max 2.99 deg/f;
  - 0 quaternion flips;
  - idle f120 / act f99 / roar f60 vs f0: 0.0.
  - (The 3.35 in my last report was the Lynx's act value, quoted by mistake.)
- **Step 1:** collision_free true, linear 0, loops closed, walk slide 0, idle foot drift 0, ground -0.002 in every
  clip.

---

# Bramble Badger - clip notes (final 8.5 gate fixes, 2026-10-28)

## Final 8.5 gate (`_review/BrambleBadger_final85.md`): what changed
- **C1, idle breathing:** it runs all loop long; the `(1 - d)` gate is gone.
  - Spine z ±0.010 (0.11 studs), and Chest pitch +1.2 · b.
  - The idle is keyed every frame now (was every 2nd) so the 3-frame flicks are exact.
- **C2, idle life:** a 10 deg ear flick and a 14 deg Tail1 flick at f40-46 and f96-102 (peaks f43 and f99). The loop
  stays closed (f120 vs f0 0.0).
- **C3, walk weight:** body bob 0.020 (was 0.010), roll 4 deg (was 3).
- **T3, growl:** the tremble is 2.5 deg (was 1.5), f24-42.
- **T4, dig scoops:** reach -0.056 / -0.064 (was -0.040 / -0.048); lift still 0.026. Ground and collisions re-checked.
- **Step 1:**
  - collision_free true, linear 0, loops closed, walk slide 0, idle foot drift 0;
  - ground -0.002 in every clip;
  - tris 5,004.
- **Metrics (`_scratch/clipmetrics.json`):**
  - neck max 7.87 (idle);
  - chest vs spine max 2.92 (walk), 2.2 idle;
  - head pitch-up 6.25 (act);
  - head yaw rate max 2.99 deg/f;
  - limb max 14.2 (armature) / 17.9 (local, Foot_FL scoop);
  - 0 quaternion flips;
  - act f99 and roar f60 vs f0: 0.0.
- **Renders:**
  - `renders/_pclose_side_sheet.png` (fixed side camera on Root): idle 0/40/43/100, walk 0/8, roar 12/30, act
    11/21/44/99;
  - `_pose_tq_sheet.png`;
  - model: `_model_sheet.png`, `_body_f85.png`, `crop_side_body.png`.

---

# Earlier clip notes (review 4)
# Bramble Badger - clip notes (clip gate round 2, after review 3, 2026-10-27)

**References:** `ANIM_REFS.md`:
- A: The Pointer #258150 (sniff);
- B: Pluto and the Gopher #143881 (hunker);
- C: Once Upon a Forest #282941 (dig strokes);
- D: ANIM_REFERENCES #4, animationreference.org (trot).

The site tags I tried are listed there.

## Full check, step 1 (`headless_full`, `_scratch/fullcheck.json`)
- **Tris:** 4,956.
- **collision_free:** True.
- **linear:** 0 in every clip.
- **Loops:** idle and walk are closed (0.0 / 0.0).
- **Walk:** slide 0.0, foot_z_var 0.0. Idle foot drift 0.0.
- **ground_min_z:** -0.002 in idle, walk, roar and act_burrow. The kick toe no longer dips (it was -0.012).
- **Stride:** 0.30.

## Clip evidence (`_scratch/clipmetrics.py`, `_scratch/clipmetrics.json`, every frame at step 1)
| Clip | Neck max | Chest vs spine (Chest joint) | Head pitch-up, world | Head yaw max /f | Limb swing max /f | Any bone max /f | Quat flips (keys / frames) | Last frame vs frame 0 |
|---|---|---|---|---|---|---|---|---|
| idle | 7.87 | 1.0 | 0.0 | 1.6 | 2.0 (Shin_FL) | 2.2 (Head) | 0 / 0 | 0.0 deg, 0.0 (f120) |
| walk | 3.47 | 2.92 | 0.1 | 1.1 | 5.3 (Leg_FL) | 5.3 | 0 / 0 | loop |
| roar | 7.0 | 1.5 | 0.2 | 0.0 | 4.4 (Shin_FL) | 5.2 (Jaw) | 0 / 0 | f59 0.21 deg / 0.0003; f60 0.0 |
| act_burrow | 6.0 | 1.25 | 6.25 | 3.0 | 13.0 (Shin_FL, scoop) | 13.0 | 0 / 0 | f99 0.0; f100 0.0 |

How these are measured:
- **Chest vs spine** is the Chest joint's own rotation, which is the bend between chest and spine. Spine pitch tilts the
  whole torso with the chest, so it is not a chest-to-spine bend. The note's old 1.5 deg was wrong: the walk reaches 2.92.
  Limit 5.
- **Head pitch-up** is the head bone direction against rest, in world space. The JSON `head_pitch_up_world_max` is
  **6.25 deg** (act_burrow, the pop-up look); every other clip is 0.2 deg or less.
- **The idle neck** was 8.47 deg (8 deg pitch plus 2.8 deg yaw). Since this round it is 7.5 deg pitch plus 0.30 × yaw,
  which gives at most 7.87. Limit 8.
- **Rest:** every clip's frame 0 is the same pose as the idle's frame 0. The idle tail wave now starts at 0. The pose sits
  4.6 deg off the bind pose at Shin_FL in every clip (the planted-leg solve), so the clips blend seamlessly.

## Clips
| Clip | Frames | Loop | Events |
|---|---|---|---|
| idle | 120 | yes | none |
| walk | 30 | yes | none |
| roar | 60 | no | `growl` f30 (0.5) |
| act_burrow | 100 | no | `dig1` f16, `dig2` f26, `dig3` f36, `kick1` f44, `kick2` f53 |

## Beats
- **idle, "nose-down sniff" (ref A):**
  - f0-20: the head drops to the ground (Spine 4, Neck 7.5, Head 15.5 deg).
  - f20-80: three nose sweeps (yaw +8 / -8 / +5) with a 6 deg nose lift between them.
  - f70: the crest bristles 3 deg.
  - f80-102: the head lifts back, slower than it fell.
- **walk, "waddle-trot" (ref D):** diagonal pairs, stride_half 0.075, lift 0.040, a 3 deg roll toward the planted
  front foot, a head dip per contact, the crest rippling.
- **roar, "hunker growl" (ref B; review 3 M-1):**
  - The shoulders drop **0.10H** (0.058) first and the rump follows 3 f later.
  - The thorns flatten back **22 deg** and the ears go back **28 deg**.
  - The neck goes forward and low while the face stays level (Head -4).
  - The jaw opens 24 deg from f28 to f42 with a 1.5 deg tremble.
  - The badger rises slower than it dropped.
  - Comparison: `renders/_roar_vs_idle_side.png` (fixed camera on Root: idle f0 / roar f12 / roar f30 / roar f59).
- **act_burrow, "dig the burrow" (refs A + C; review 3 M-2, M-3, N-1 to N-3):**
  - f0-8: a quick nose-tap (DN to 0.45, about 8 deg head and 4 deg neck), with no yaw.
  - f8-38: three forepaw scoops, L / R / L, each 10 f. Each reaches, lifts 0.026 (0.045H), sweeps back through contact
    and touches down. The dig events sit on the backward sweeps. The head stays low over the hole (DN 0.75).
  - f41-59: two hind kicks, BL at f41 and BR at f50. Each foot shoves back **0.070** (review 4 NICE; it was 0.060), lifts **0.028** with the toe tilted
    up 7 deg (toe = -7 × lift / 0.028), and steps home. The kicks no longer overlap.
  - f56-61: the head pops up. Then a slow look-around: +14 deg over f60-68, hold, -14 deg over **f72-86 (14 f)**, hold,
    and back to 0 by f98. The world head yaw is at most 3.0 deg per frame, so it is not a shake.
  - f98-100: the exact rest pose (f99 delta 0.0).

## VFX anchor bones
- `FX_DirtPuff_FL` / `FR` / `BL` / `BR` [Foot_*]: the dig and kick events.
- `FX_DustGrowl` [Head]: the growl.
- `FX_LeafDust` [Spine]: the walk and act.

## Change against ANIM_REFS.md (accepted in review 3)
In the roar the head stays level and forward, not down to the ground.

## Renders
- **`renders/_pose_tq_sheet.png`:** idle 0/36/70, walk 0/8/15/23, roar 12/30/59, act 4/10/16/21/25/44/53/68/86/99.
- **`renders/_pclose_tq_sheet.png`:** act 4/10/21/25/44/68/86/99, idle 0, roar 30/59, walk 8.
- **`renders/_pclose_side_sheet.png`:** the same frames plus roar 12, from a fixed side camera on Root, so body drops
  show against the floor.
- **`renders/_roar_vs_idle_side.png`:** the roar hunker against the idle.
