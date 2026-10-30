# Frostfang Lynx - SHIP FILE (round 6 PASS, 2026-10-28 09:14)
- The `LYNX_SOFT` test switch is removed, and `walk()` always uses `soft_walk`. Re-exported `C:\cdimp\FrostfangLynx.fbx` (09:14). The ship copy is `_scratch/FrostfangLynx_ship.py`.
- Re-checked on the new export: walk max local limb step **5.49** (Shin_BR f5), slide 0.0, loop closed, collision_free. Tail tip f8 -> f23 at the 1x game camera: **25.8 px**. All identical to 09:08.

# Frostfang Lynx - clip notes (r6 walk polish after the round-5 PASS, 2026-10-28)

## r6: walk knee step (coordinator, after `_review/FrostfangLynx_final85_r5.md`)
- **Was:** Shin_FR 12.45 deg at f6 (FR touchdown), Shin_FL the same at f18, and Foot 11.7 in the 9 f swing.
  - The old foot path set the paw down with vertical speed and swung a 0.22 stride in only 9 frames (24 f cycle, duty 0.62).
- **Now:**
  - `soft_walk`, the same lateral sequence (BL / FL / BR / FR) with soft feet: zero speed at lift-off and touchdown, the lift easing in and out (the Wraith / Badger path).
  - **30 f cycle** (was 24; ANIM_REFS L0 gives a 24-30 f cat walk) with **duty 0.56** (was 0.62), so the swing is 13 f instead of 9.
  - **Lift 0.030** (was 0.050).
  - The FRONT paws trail the shin through the swing (`slerp(flat toe, shin, 0.8*sin^2)`): the paw curls under and reaches flat again for touchdown, which spreads the ankle turn.
  - On the hind paws the trail made the toes dip 0.011 under the ground, so it is front-only.
  - The body bob is unchanged and still lowest at the front touchdowns (f7.5 / f22.5).
- **Result:** walk limb local max **5.49 deg** (Shin_BR f5; target <= 5.63), armature-space 5.57. Touchdown steps: Shin_FR around f7 / f8 is 0.6-0.4.
  - Slide 0.0, loop closed, collision_free, ground -0.0, 0 flips; chest vs spine 2.68, neck 2.0.
  - Stride 0.393 per 1.0 s (meta `walk_len` 1.0).
- **Kept:**
  - the tail counter-sway (12 deg yaw + 6 deg roll): f8 -> f23 (the sway extremes at 30 f) **25.8 px at 1x, 51.1 px at 2x** (r4 at 24 f: 26.9 / 55.5), `renders/_walk_tail_r6.png`;
  - the head nod 1 f after each front touchdown (peaks f8.5 / f23.5);
  - idle, roar and act unchanged.
- Sheets: `renders/_walk_sheet_r6.png` (every 3 f, game / side / tq, with the time), `renders/_walk_tail_r6.png`.

---

# Frostfang Lynx - clip notes (8.5 gate round 4, 2026-10-28)

## Round 4 (`_review/FrostfangLynx_final85_r4.md`)
**Correction to round 3:** the "23 px" walk tail move in my round-3 notes was an eyeball misread. Measured on those r3 renders (`_scratch/tipmeasure.py`, the black tip's centroid), it was **2.4 px**. Every number below is measured from the r4 renders, not estimated.

- **W1, walk tail counter-sway:**
  - Tail1 yaw is `12*wave(f, n, 0.5)`, phase 0.5; the Spine yaw stays 1.8.
  - Yaw 12 alone gave 16.1 px at 1x, so I also added a **roll counter-sway**: `roll = 6*wave(f, n, 0.5)` on Tail1 and 0.6x on Tail2 (`bobtail(roll=)`). The lifted tail then swings sideways.
  - Roll -6 cancelled the yaw (6.3 px), so the sign is +.
  - Measured tip move f6 -> f18: **26.9 px at 1x** (game camera, dist 3.0, 600 px, Root-fixed) and **55.5 px at 2x** (dist 1.5, aimed at the rump). The pass was 15 / 30.
  - Sheet: `renders/_walk_tail_r4.png`. The 2x frames are `renders/pclose_game_walk_06.png` / `_18.png`.
  - Walk loop 0.0 / 0.0, slide 0.0, collision_free true.
- **P1, ear twitch:** 12 deg (`tw = 12*tab(TW, f)`, `pr = -0.6*tw`): Ear_L pricks +12, Ear_R presses -7.2, a rebound at f72, settled at f75.
  - Measured ear-tip move f62 -> f70 (`_scratch/earmeasure.py`, top ICE pixel): **30.7 px at 2x** (head camera) and **13.6 px at 1x**.
  - The other ear moves 5.0 / 2.0 px, which is the head's own motion. Row 3 of `renders/_idle_game_r4.png`.
- **P2, breath:** the Spine dips **0.04H** (`-0.04*H_U*rb`, about 0.28 studs), always below rest.
  - Root-fixed side camera: the back line drops **20-22 px of 800** at f60 vs f0 (r3 0.03H: 16 px). `renders/_breath_side_r4.png`.
  - Idle foot drift 0.0.
- **P3:** the stale comment is fixed. `rb` is the breath weight 0..1 (peaks f20 / f60 / f100), and the Spine line says 0.04H dip.
- **P4, walk head nod:** `nod = 0.5 - 0.5*cos(4*pi*(f-1)/n)`, peaks f7 / f19, 1 f after each front-paw contact (FR lands f6, FL f18, from `gait_target`: touchdown at t = 0).
  - Neck 0.5 + 1.5*nod and Head -2.0 + 3.5*nod (+ = down). That is a 5 deg dip in total that rides the body's own low point at f6 / f18.
  - The old head wobble ran against it, so it is replaced. Walk neck max 1.94, head pitch-up 0.85.
- **Idle tail (C2, unchanged at 22 deg):** f26 -> f62 is **29.3 px at 1x / 57.9 px at 2x** on the r4 cameras.
- **Gates (`_scratch/fullcheck.json`, `_scratch/clipmetrics.json`):**
  - collision_free true, linear 0;
  - idle / walk loops 0.0;
  - idle foot drift 0.0, walk slide 0.0;
  - ground -0.0 / -0.0 / -0.0 / act -0.002;
  - 0 quaternion flips;
  - idle: neck 5.63, chest vs spine 1.44, ear swing max 8.95 deg/f (f72 rebound);
  - act: neck 7.36, chest vs spine 3.35;
  - acts end at rest.
- **Known, unchanged since r3:** walk Shin_FR local step 12.45 deg at f6, the FR touchdown. Its world-space limb swing max is 7.8 deg/f.

---

# Frostfang Lynx - clip notes (8.5 gate round 3, 2026-10-28)

## Round 3 (`_review/FrostfangLynx_final85_r3.md`)
- **C2, tail:** the idle tail sway is **22 deg** (was 14), `22*sin(2*pi*f/120)`. It is one cycle per 120 f, 0 at f0 and f120, so the loop stays closed. Tail2 takes 0.6x of it.
  - Game camera at gate distance (3.0, 600 px): the black tail tip moves **24 px sideways + 10 px down, about 26 px**, between f26 (+21.5 deg) and f62 (-2.3 deg). At 2x it moves about 55 px. The target was 15-20 px.
  - Sheet: `renders/_idle_game_r3.png` (top row 1x, bottom row 2x, f0 / f26 / f62 / f70). The 2x frames are `renders/pclose_game_idle_26.png` / `_62.png`; the 1x frames are in `_scratch/r3/game1x_*.png`.
- **C2, breath:** the Spine dips **-0.03H** (`-0.03*H_U*rb`, about 0.21 studs; was 0.02H), always below rest. Three breaths per loop, peaks f20 / f60 / f100.
  - Fixed (Root) side camera: the back line drops **16 px of 800** at f60 vs f0 (`renders/_breath_side_r3.png`, red line = the f0 back line).
  - Idle foot drift is 0.0.
- **T1, walk counter-sway:** the bobtail sway is `6*wave(f, n, 0.5)` (was `4*wave(f, n, 0.3)`). That is 6 deg in exact opposite phase to the hip yaw (`Spine yaw 1.8*wave(f, n)`), so the tail swings against the hips: f6 hips +1.8 / tail -6, f18 hips -1.8 / tail +6. The tail tip moves about 23 px between f6 and f18 (`renders/_walk_tail_r3.png`). Walk slide 0.0, loop closed.
- **T2, ear twitch:** the f70 twitch is **8 deg** (was 3). Ear_L pricks +8, Ear_R presses -4.8 (`pr = -0.6*tw`), then rebounds -0.5 at f72 and settles at f75. Visible in `_idle_game_r3.png` f70.
- **T3, spark check:** this is the coordinator's job in Studio. The events are unchanged: claw1 f48, claw2 f60, snow_flick f77.
- **Numbers (`_scratch/fullcheck.json`, `_scratch/clipmetrics.json`):**
  - collision_free true, linear 0;
  - loops closed (idle 0.0 / 0.0, walk 0.0 / 0.0); walk slide 0.0;
  - idle foot drift 0.0;
  - ground: idle -0.0, walk -0.0, roar -0.0, act -0.002;
  - 0 quaternion flips in every clip;
  - idle: neck 5.63, chest vs spine 1.44;
  - act: neck 7.36, chest vs spine 3.35;
  - idle swing max 7.52 deg/f (Tail3, the f90 tip flick);
  - acts end at rest (vs f0 0.0).

---

# Frostfang Lynx - clip notes (8.5 gate round 2, 2026-10-28)

## Round 2 (`_review/FrostfangLynx_final85_r2.md`)
- **C1:**
  - the claws are 0.095 long with a 0.017 half-width (were 0.072 / 0.014);
  - the -55 deg open, the splay and the knead are unchanged;
  - ground -0.002 (act f44), so the longer claws do not dig in;
  - the ICE spark VFX on `claw1` / `claw2` is the coordinator's (Studio).
  - Game camera: `renders/pclose_game_act_clawflex_50.png` (in `_game_r2.png`, right).
- **C2:**
  - the idle tail sway is **14 deg** (one cycle per 120 f, 0 at f0 and f120);
  - the breath is **0.02H**, still a dip below rest, so the idle foot drift stays 0.0;
  - `_game_r2.png` left / middle shows idle f26 against f62 from the game camera.
- **Step 1:** collision_free true, linear 0, loops closed (seam 0.0), walk slide 0, idle foot drift 0.0, ground
  -0.002, tris 8,396.
- **Metrics:** act neck 7.36, chest vs spine 3.35 (act) / 2.68 (walk), limb max 16.8 / local 12.0, 0 quaternion
  flips, act f95 / f96 vs f0 0.0.

---

# Frostfang Lynx - clip notes (final 8.5 gate fixes, 2026-10-28)

## Final 8.5 gate (`_review/FrostfangLynx_final85.md`): what changed
- **M4, the claw flex reads from the game camera:**
  - the crouch is **0.10H** (0.118, was 0.05H);
  - Spine pitch 6.0 · c (was 3.5) and Chest 3.0 · c (was 1.5); the head counter-pitches -4 · c, so the face stays
    level and locked on the target;
  - the claws are 0.072 long (was 0.056), half-width 0.014, with the base at z 0.036 and direction (0,-1,-0.5), so
    the rest tips stay above the floor;
  - the claw-fan parent opens **-55 deg** (was -35); the centre claws reach ~61 deg and the outers ~47 deg, with the
    same yaw fan;
  - the flexing paw's toe roll is **-20 deg** (was -12), with the heel at +0.008.
  - See `renders/pclose_side_act_clawflex_50.png`, `pose_tq_act_clawflex_50.png`, `pclose_game_act_clawflex_50.png`
    and `_scratch/clawtmp/claw_paw_f85.png`.
- **M5, idle life:**
  - a breathing settle-and-rise of **0.01H** on the Spine (3 per loop), with a 1.2 deg chest lift;
  - a slow **±8 deg bobtail sway** over the 120 f loop (`sin(2π f / 120)`).
  - Both are 0 at f0, so the loop seam is 0.0 and the idle's f0 is the acts' rest. The breath dips below rest rather
    than rising above it, so the planted legs never overreach (idle foot drift 0.0).
- **T3, the stare:** the head locks at **18 deg** (f4-14, held to f40) with the ear tufts flattened to **-12 deg** (f12-24).
  The neck takes 30 % of the yaw, so the neck total is 7.36 deg at most (limit 8).
- **Metrics (`_scratch/clipmetrics.json`):**
  - act neck 7.36, chest 3.35, head pitch-up 0.32;
  - limb max 16.8 deg per frame (Claw_FR2, the claw open), local max 12.0;
  - 0 quaternion flips; f95 / f96 vs f0 = 0.0;
  - ground -0.002 (act f44); collision_free true.

---

# Earlier clip notes (review 4)

**References:** `ANIM_REFS.md`:
- L0: animationreference.org, The Cat Returns #256671, the cat walk (new);
- L1: Figaro look-around #132474;
- L2: Figaro crouch #132272;
- L3: Figaro paw flex #132391;
- L4: MU threat display, ANIM_REFERENCES #6;
- L5: Pluto hunker #143881.

## Rig and model changes for the clips
- **`Ruff_L` / `Ruff_R`** (round 1, accepted): cheek-ruff hinges, children of Head.
- **Claws, review 3 M2:** each front claw now has its own bone, `Claw_FL1-4` and `Claw_FR1-4`, children of `Claw_FL` /
  `Claw_FR`. Claw x positions are `CLAWX` (-0.043, -0.015, 0.015, 0.043).
  - The rest pose is unchanged, so the four claws still read as four at rest.
  - In the flex, the parent opens 35 deg. The centre two open 6 deg more (41 total) and the outers 8 deg less (27
    total).
  - The outers yaw ±18 deg and the centres ±6 deg, so the claws fan out.
  - There are now 42 bones.
- **Throat, review 3 M1:** the throat seg is thinner (half-width 0.070 → 0.045, half-depth 0.056 → 0.040), with four
  SNOW fur tufts down it (two pairs at 30 % and 62 % of its length, pointing down and forward). It reads as a fur
  fringe, not a plate.
  - The renders `renders/crop_front_throat.png`, `crop_tq_throat.png` and `low_below.png` are newer than the source.
- **Tris:** 6,532 (+48 for the tufts, +128 for their rounded tips).
- **Review 4 NICE:**
  - the throat tuft tips are rounded (top 0.45 / 0.60, rnd 0.40), so they no longer read as a second row of teeth
    (`renders/_throat_r4.png`);
  - the Jaw is 0 deg at rest in every clip (it was 1 deg in idle f0, the roar ends and the act end);
  - the ANIM_REFS claw lines now give the 12 f lag and the fan angles.

## Full check, step 1 (`_scratch/fullcheck.json`)
- **collision_free:** True.
- **linear:** 0 in every clip.
- **Loops:** idle and walk are closed (0.0 / 0.0).
- **Walk:** slide 0.0, foot_z_var 0.0. Idle foot drift 0.0.
- **ground_min_z:** -0.000 in idle, walk, roar and act_clawflex.
- **Stride:** 0.355.

## Clip evidence (`_scratch/clipmetrics.json`, every frame at step 1)
The metric definitions are written into the JSON under `_definitions`.
- **"Limb swing"** is the per-frame change of a bone's armature-space orientation, so it includes the parents' motion.
- **`swing_local_max`** is the same for the bone's local quaternion. That is what a decode of the exported keys gives:
  walk 12.45 deg (Shin_FR f6), act 8.36 deg (Claw_FR f57).
| Clip | Neck max | Chest vs spine | Head pitch-up, world | Limb swing max /f | Any bone max /f | Quat flips (keys / frames) | Last frame vs frame 0 |
|---|---|---|---|---|---|---|---|
| idle | 5.63 | 0.6 | 0.4 | 0.45 | 7.8 (Tail3 flick) | 0 / 0 | f120 0.0 |
| walk | 2.03 | 2.68 | 0.55 | 7.8 (Shin_FL) | 7.8 | 0 / 0 | loop |
| roar | 4.0 | 2.0 | 0.0 | 3.3 | 5.8 (Jaw) | 0 / 0 | f59 0.0, f60 0.0 |
| act_clawflex | 7.0 | 2.12 | 1.59 | 11.7 (Claw_FR2) | 11.7 | 0 / 0 | f95 0.0, f96 0.0 |

- The act neck total is **7.0 deg**, not the 6.5 the last note said (review 3 NICE 3). Limit 8.
- The idle ears now start at 0, so the idle's frame 0 is the exact pose the roar and act start and end on (it was 2 deg
  on the ears).

## Clips
| Clip | Frames | Loop | Events |
|---|---|---|---|
| idle | 120 | yes | none |
| walk | 24 | yes | none |
| roar | 60 | no | `ruff_flare` f13 (0.217), `hiss` f30 (0.5) |
| act_clawflex | 96 | no | `claw1` f48 (0.5), `claw2` f60 (0.625), `snow_flick` f77 (0.802) |

## Beats
- **idle, "watchful look-around" (L1):**
  - The head turns +14 deg over f8-26 and holds; it turns -8 deg over f40-58 and holds; it is back at 0 by f84.
  - The ears follow 4 f late and twitch 3 deg at f70. The tail tip flicks 10 deg at f91.
- **walk (L0):**
  - A lateral-sequence cat walk, stride_half 0.11, lift 0.05.
  - The body drops 0.02H between contact and passing, the head stays steady and the bobtail is carried up.
  - L0's cycle is ~24-30 f, so 24 f stands.
- **roar, "ruff-flare threat" (L4 + L5):**
  - f0-14: the shoulders drop 0.05H. f6-13: the ruffs flare 20 deg, and the tufts go back 24 deg and splay 12 deg.
  - Two head pushes, at f26 and f38.
  - The jaw opens to 24 deg (f22-52) with a tremble.
  - f46-60: settle.
- **act_clawflex, "the claw flex" (L2 + L3):**
  - f0-10: the crouch.
  - f4-16: the head turns 14 deg to the pet's left and holds to f40. The tufts flatten 8 deg, then rise to +4.
  - The left claws fan open over f40-48 (`claw1`) and the right claws over f52-60 (`claw2`). Each flexing paw rolls its
    toes up 12 deg on the heel. A 4 deg knead runs while the claws are open, and the head looks down at the paws.
  - f72-84: the claws retract and the bobtail flicks once.
  - f72-88: the lynx rises to the exact rest pose.
  - All paws are planted in every frame.

## VFX anchor bones
- `FX_IceSpark_L` / `R` [Claw_FL / FR, the claw-fan parents]: `claw1` and `claw2`.
- `FX_IceDust_L` / `R` [Ear_L / R]: `ruff_flare`.
- `FX_SnowPuff_FL` / `FR` [Foot_F*].
- `FX_SnowFlick` [Tail3]: `snow_flick`.

## Deviations (all accepted in review 3)
- The Ruff bones.
- The right paw lags 12 f, so the events land on f48 / f60.
- The 12 deg toe roll.
- The head turns to the pet's left.
- One saddle band (NICE 3) is waived.

## Renders
- `renders/_pose_tq_sheet.png`: idle 0/26/62, walk 0/6/12/18, roar 13/30/59, act 12/36/50/62/95.
- `renders/_pclose_tq_sheet.png` and `_pclose_side_sheet.png`: idle 26, walk 6, roar 13/30/59, act 12/36/50/62/95.
- **The claw fan:**
  - `_scratch/clawtmp/claw_zoom.png`: rest against f50, three-quarter and front, close.
  - `_scratch/clawtmp/claw_paw3.png`: f0 / f50 / f62 from the three-quarter, side and front views.
- **The throat:** `renders/crop_front_throat.png`, `crop_tq_throat.png`, `low_below.png`.
