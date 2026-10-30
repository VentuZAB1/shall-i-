# Cinder Overlord - clip notes (CLIP GATE, 2026-10-27)

References: `ANIM_REFS.md` (snake-on-sand slither S1, reared king cobra S2, refs #3 / #6 / #9).
Gate run (current): the export run `_scratch/export_r14.txt` (round 14, 14:53: hood rim colour only, see MODEL_NOTES;
clip keys as round 13); single gate file `_scratch/gate_f85.json`.
Current sheets (2026-10-28 14:53-14:55, from the round-14 file): `renders/_pose_tq_sheet.png` (26 beats),
`_cv_idle_game.png` / `_cv_idle_front.png`, `_hood_back_2x_idle_f0_f20.png`, `_cv_walk_side.png` /
`_cv_walk_game.png`, `_cv_roar_front.png` / `_cv_roar_side.png`, `_molt_r14_front.png` / `_molt_r14_tq.png`,
`_molt_game.png`. Older sheets and frames are in `_scratch/stale_r6_renders/` ... `stale_r14_renders/`.

## FINAL 8.5 ROUND 13 (2026-10-28) - act_molt hold for the game camera
- **act_molt:** the arch hold goes -22.5 -> **-9** (3 deg per neck bone) and the head hold 20.5 -> **9** (`MOLT_ARCH`,
  `MOLT_HEAD`), so the head stays level.
  - Keys, timing, blade lifts / fans / reseat, ripple and events are unchanged (lift1 0.2, lift2 0.436, shed 0.509).
  - Why both: the review's head 20.5 -> 14 alone gave a 31.8 px gap (worse), because nose-up tips the back of the head
    toward the game camera.
  - Game-camera head gap at every beat: **52.5-62.2 px** (r12 34.8-62.4; target >= 50). See NEW
    `renders/_molt_game.png`.
  - Pose limits: neck 3.0 per bone (<= 8), head 9.0, chest 4.5 (<= 5), head + neck pitch-up 1.0 (<= 30).
- **Idle, walk and roar keys unchanged.** Gaps: idle 50.7-65.8, walk 61.8-63.0, roar 47.5-62.2 px.
- **Crown neighbours** with the taller side blades (lift + fan in the molt and roar) >= **0.0357** in all clips.
- **Collision:** kit gate **true**; strict run only the two shoulder seats (<= 0.0277). Loops 0 / 0; stride 5.0089;
  ground -0.006.

## FINAL 8.5 ROUND 12 (2026-10-28) - cobra hood; clip keys unchanged (clips APPROVED 8.5 in round 12)
- The hood panels are skinned to **Neck2** (lower) and **Neck3** (upper), so they move with the neck.
  - Idle cobra sway: the hood swings with the neck (`renders/_hood_back_2x_idle_f0_f20.png`, fixed cameras).
  - Roar gather and molt arch: the hood leans back with the neck.
- **Hood clearance**, proxy-free, every frame of all four clips:
  - head 0.051 (idle f96);
  - jaw 0.078 (roar f32);
  - frill / cheek spikes 0.089 (idle f34);
  - crown >= 0.462;
  - paws >= 0.485;
  - arms >= 0.325.
- **Pose limits unchanged** (`stance_r12.txt`): neck <= 7.5 per bone, chest 4.5, head + neck pitch-up <= 4.
- **Game-camera head gap:** idle 50.9-66.0 px, walk 61.9-63.2 px.
- **Collision:**
  - Kit gate **true** (85 pairs).
  - Strict run: only the two shoulder seats (<= 0.0277).
- Loops 0 / 0; stride 5.0089; ground -0.006.

## FINAL 8.5 ROUND 11 (2026-10-28) - RAISED COBRA STANCE: idle redone, walk / roar / act_molt re-checked
- **Idle = COBRA SWAY** (`idle()`; refs S2 reared king cobra, C1 / C2):
  - The neck stands upright and sways side to side: roll **2.2 deg per neck bone**, one sway per 120-frame loop, plus a
    0.4 deg yaw.
  - The head follows about 5 frames later. It counter-rolls 4.4 deg, so it stays near level, and turns 3 deg into the
    sway.
  - Two breaths stay small: neck pitch 1 deg per bone, head +0.8, jaw 2.25, crown lift 2.25, paws 3.
  - The tail flick at f80 is unchanged. Events are unchanged (smoke1 0.25, flick 0.667, smoke2 0.75).
  - Why: the r10 idle leaned the neck back 13.5 deg on each breath, which brought the head toward the game camera.
    Game-camera head-to-body gap over the loop: r10 idle **27.7-42.2 px**, r11 idle **50.9-66.1 px**.
  - Sheets: `renders/_cv_idle_game.png`, `_cv_idle_front.png`; idle beats in `_pose_tq_sheet.png`.
- **Walk keys unchanged:** the head holds full height through the cycle (gap 62.0-63.3 px; head pitch +/-0.6 deg;
  neck bones 1.12 deg). The raised stance comes from the rest pose.
- **Pose limits, re-measured on this file** (`_scratch/stance_probe.py`, max rotation vs rest):

  | clip | neck bones (each) | head | Spine | neck pitch sum | head pitch-up (world) |
  |---|---|---|---|---|---|
  | idle | 2.45 | 5.36 | 0 | -3.05 | 1.82 |
  | walk | 1.12 | 0.74 | 3.00 | 0.00 | 0.60 |
  | roar | 4.00 | 10.00 | 0 | -12.00 | 4.00 |
  | act_molt | 7.50 | 20.50 | 4.50 | -22.50 | 2.00 |

  - Neck <= 8 per bone, chest (Spine) <= 5, head + neck pitch-up <= 30: **PASS** in all four clips.
- **Collision:**
  - Kit gate (joint-aware) **true**: 83 pairs, every frame.
  - Strict run (own hinge only): the only entries are the two shoulder seats, seat depth <= **0.0277** (limit 0.035).
  - Per-frame depths of every seated pair are in `_scratch/coll_depths_r11.json`. Neck2|Spine and Body4|Body2 have
    no crossing in any frame.
  - Crown neighbours >= 0.0307. Jaw to neck 0.077 (roar f30).
- Loops 0 / 0; stride 5.0089; ground -0.006.

## FINAL 8.5 ROUND 10 (2026-10-28) - MUST 3 collision proof (`_scratch/coll_probe.py` -> `coll_probe_r10.txt`)
- **How the kit check works** (`blockkit.overlap_report`):
  - Mesh triangles of two bone groups are tested for crossings.
  - Contacts already present at rest are ignored.
  - A crossing whose points all lie within r of any `joints()` segment counts as a hinge sliver and is IGNORED.
  - So a proxy hides crossings; it does not add a check.
- **Injection test** (idle f0, pose set by hand):

  | test | no proxies | pet joints | + review's extra proxies |
  |---|---|---|---|
  | left paw 0.16 into Neck1 | 51 | 0 | 0 |
  | left paw 0.22 into Neck1 | 89 | 0 | 0 |
  | Crown_5 swung down 60 deg | 51 | 0 | 0 |
  | Crown_5 swung down 100 deg | 112 | 41 | 41 |

  - The paw spot is inside the Neck1 hinge sphere (r 0.34). That is why I prove the paws and the skull by surface
    clearance, not by more proxies.
- **Kit gate:** 83 pairs (+19: paws / arms vs Spine, Body1, Neck2; Head / Jaw vs Neck1; Crown_1..5 vs Head).
  collision_free **true**, every frame of idle, walk, roar and act_molt.
- **Proxy-free minimum surface clearance**, every frame of the four clips (BU):
  - Paws: Neck1 0.148 (walk f12), Neck2 0.265 (roar f44), Spine 0.158 (walk f12), Body1 0.654 (idle f29), Jaw 0.440 (roar f32), Head 0.591 (act_molt f18), Claw_R 0.640 (act_molt f110).
  - Skull / jaw / frill: Head|Neck1 0.374 (act_molt f18), Head|Neck2 0.134 (act_molt f84), Head|Arm_L 0.465 (act_molt f18), Jaw|Neck2 0.026 (roar f30), SPIKES|Crown_1 0.123 (roar f26), SPIKES|Crown_2 0.230 (roar f22), SPIKES|Neck2 0.389 (walk f39), SPIKES|Neck3 0.284 (walk f44).
  - Crown neighbours: Crown_1|Crown_2 0.039 (roar f21), Crown_2|Crown_3 0.003 (act_molt f16), Crown_3|Crown_4 0.005 (roar f59), Crown_4|Crown_5 0.039 (roar f21).
  - Every paw, skull, jaw and frill pair is >= 0.02.
- **Arm root vs Neck2 = 0.000:** the shoulder ball is rooted in the neck at rest (0.005 at rest). Its crossing box
  stays where it is at rest, inside Neck1.
- **Fixed this round:** the centre crown's side gold frames started 0.012 below the blade foot and grazed blades 2 / 4
  in the molt (proxy-free run). They now start 0.033 above it.
- **Clip keys:** unchanged; loops 0 / 0; stride 5.0089.

## FINAL 8.5 ROUND 2 (2026-10-28) - EXPORTED to `C:\cdimp\CinderOverlord.fbx` (03:42)
- **Idle breath x1.5:**
  - Neck 13.5 deg in total = **4.5 per bone** (measured 4.55; limit 8), with the head counter-pitching 9, so it stays
    near level.
  - The jaw, the crown breath (2.25) and the forearm paddle (3) scale with it. The loop is closed.
- **Walk:** the stride is 5.01 BU per 48 f after the shorter Tail4 (the walk-speed check is the coordinator's).
- **Molt:** unchanged.
  - Front fan spread f0 / 22 / 34 / 40: 48.0 / 66.9 / 85.0 / 85.0 deg.
  - Rise vs fall peaks are unchanged (`_scratch/ang_r2.txt`).
- **Step 1** (`_scratch/export_r2.txt`): collision_free **true**; ground_min_z -0.006 in every clip; linear 0; idle and
  walk loops 0 / 0. Events are unchanged.
- **Renders re-made:** `_pose_tq_sheet.png` (26 beats), `_cv_walk_side/game.png`, `_cv_roar_front/side.png`,
  `_molt_r4_front/side/tq.png`, `_cv_molt_front.png`, `_model_sheet.png`, `_close_sheet.png`, the icon strips and
  `gamelook_*`. The round-1 renders are in `_scratch/stale_f85_renders/`.

## FINAL 8.5 (2026-10-28, after `_review/CinderOverlord_final85.md`, FIX clips 7.5) - EXPORTED
- **C1, the molt reads from the front:**
  - The four outer blades lift **45 deg** (was 35). The centre lifts 35, then 40, as before.
  - The lifts start at **f12** (was f18), with a 3-frame lag and the same 10-frame rise. Blade 1 is fully up at
    `lift1` f22.
  - The middle blades' fan goes from 10 to 14 deg (outer 18), scaled by the lift.
  - Front-view fan spread, Crown_1 to Crown_5 (`_scratch/fan_probe.py`): **f0 48.0, f22 66.9, f34 85.0, f40 85.0
    deg**. That is +18.9 / +37.0 / +37.0 vs f0. Each fanned blade moves 16-18.5 deg in the front view at f34-40.
  - Evidence: `renders/_molt_r4_front.png` (f0 ... f110), `_scratch/molt_fan_zoom.png` (crown crop f0 / 22 / 34 / 40)
    and `renders/_cv_molt_front.png`.
  - Reseats are stretched: the centre goes 40 -> 6 over **f84-100** (was f84-95) and to 0 at f106; the outer blades
    reach 2 at f100 / 98 / 94 / 92 and 0 at f108.
  - Speeds (`_scratch/ang_probe.py`, deg/f) - every fall stays under its rise:

    | blade | rise | fall |
    |---|---|---|
    | outer (1 / 5) | 7.47 | 5.80 |
    | middle (2 / 4) | 7.10 | 5.56 |
    | centre | 5.18 | 3.17 |
  - The blades are collision-free at 45 deg.
- **T3, idle:** the neck breath is 3 deg per bone (was 2; total 9) and the head counter-pitch is 6. The head stays
  near level.
- **C2, renders re-made from the current model and palette** (stale ones moved to `_scratch/stale_r6_renders/`):
  - `_pose_tq_sheet.png`: 26 beats - idle 0/30/60/90, walk 0/12/24/36, roar 0/14/22/30/44/66, and molt 0 ... 110.
  - `_cv_walk_side.png`, `_cv_walk_game.png` (walk f0-40 from the fixed side and game cameras).
  - `_cv_roar_front.png`, `_cv_roar_side.png`.
  - `_molt_r4_front.png` / `_side.png` / `_tq.png` (14 frames each), `_cv_molt_front.png` (f0 / 22 / 34 / 40).
- **C3 (walk speed in Studio) and C4 (owner disclosure): skipped per the coordinator.** The walk stride stays 5.19 BU
  per 48 f.
- **Step 1** (`_scratch/clipgate_f85.txt`, export run `_scratch/export_f85.txt`):
  - collision_free **true**; ground_min_z -0.006 in every clip; linear 0; idle and walk loops 0 / 0.
  - Tris 10,588. Events are unchanged (molt `lift1` 22, `lift2` 48, `shed` 56).
- **Export:** `C:\cdimp\CinderOverlord.fbx` (2026-10-28 01:31, 1,287,228 B). The portrait raw is re-made.

## ROUND 6 (2026-10-27): FINAL, EXPORTED to `C:\cdimp\CinderOverlord.fbx`
- The colours changed (deep sulfur-blue accent, white-hot cores, trimmed rings); the clips did not.
- Step 1 (`_scratch/clipgate_r6.txt`): collision_free true, ground_min_z -0.006, linear 0, loops 0 / 0.
- The molt beats are re-rendered in the final palette: `renders/_molt_r4_front/side/tq.png`.

## ROUND 5 (2026-10-27, after `_review/CinderOverlord_review4.md`, clips APPROVED WITH FIXES 8/10)
- The molt beats are re-rendered from the current model (sulfur-blue accents, taller crown): `renders/_molt_r4_front.png`,
  `_molt_r4_side.png`, `_molt_r4_tq.png`.
- The taller crown blades stay collision-free through the roar and the molt.
- Step 1 (`_scratch/clipgate_r5.txt`): collision_free true, ground_min_z -0.006, linear 0, loops 0 / 0. Events unchanged.
- ANIM_REFS now says plainly that Haku is a flying eastern dragon. It lists what came from him (the head -> tail bend,
  the level head) and what came from the Wikimedia snake study (the lateral ground bend, the pace, the cobra neck, the flick).

## ROUND 4 (2026-10-27, after `_review/CinderOverlord_review3.md`, REVISE 7/10)
- **MUST 1, site refs for idle + walk:** `ANIM_REFS.md` section D: Haku in *Spirited Away* (site `/tags/creature-animation`
  -> Sakugabooru #225387). D1 / D2 = the bend runs head -> tail with the head on a level line (f146-186, f636-680); D3 = the
  head holds level while the body moves (f696-760). The tags tried are listed. No opens spent.
- **MUST 2, chest:** the molt ripple on the **Spine (the chest base) is now 4.5 deg** (Body / Tail bones keep 6).
  Measured per bone (`_scratch/ang_probe.py`): Spine max **4.5** (<= 5), each Neck bone max **7.5** (<= 8, NICE 6 margin).
- **MUST 3, centre blade reseat:** Crown_3 rises at a peak of **5.18 deg/f** and now reseats at **4.62 deg/f** (f84-95,
  was f84-92 at 6.3). The outer blades rise at 5.81 and fall at 4.15.
- **NICE 3:** the blades lift one by one with a **3-frame** lag (was 2), so the sequence reads at game distance.
- **NICE 6:** the molt neck arch is 22.5 deg in total (7.5 per bone), and the head counter-pitch is 20.5.
- **Gate (step 1, `_scratch/clipgate_r4.txt`):** collision_free **true**, ground_min_z -0.006 in every clip, linear 0,
  idle + walk loops 0 / 0. Events unchanged (molt `lift1` f22, `lift2` f48, `shed` f56).
- **Renders:** molt beats f0-110 from three fixed cameras: `renders/_molt_r4_front.png`, `_molt_r4_side.png`,
  `_molt_r4_tq.png`.

## Numbers (step 1)
- **collision_free: true.** ground_min_z -0.006 in every clip (= the rest pose: all body bends are yaw, in the ground
  plane, so nothing sinks).
- Audit: linear 0; idle + walk loops closed (0 / 0). Walk = the slither (no feet, so no slide metric). Stride 5.19 BU
  per cycle (the body travel if the bends stay put on the ground: segment length / 3-frame lag x 48 f). Tris 10,852.
  Lua 40 KB.
- Pose limits (round 4): each neck bone <= 7.5 deg (molt arch 22.5 deg over three bones); the Spine (chest base) <= 4.5; head + neck pitch-up max 2 deg net (the
  head counter-pitches to stay level); no head shake, no spin.

## Clips
| clip | frames | loop | events (frame) | what it does |
|---|---|---|---|---|
| idle | 120 | yes | `smoke1` 30, `flick` 80, `smoke2` 90 | EMBER BREATHING: two slow breaths - the neck rises 9 deg (3 per bone, final 8.5) and sinks back with the head held near level, a slow +/-2 deg sway with head counter-yaw (S2 C1), the crown blades breathe 1.5 deg, the vents smoke on the breaths; one quick tail flick 8 deg at f76-86 (S2 C2). |
| walk | 48 | yes | `paddle1` 12, `paddle2` 36 | SLITHER (S1 U1-U4): a lateral curvature wave runs **head -> tail** (each chain bone lags the one in front by 3 f; amplitude 3/6/9/10/10/9/8/7/6 deg), the reared neck counter-yaws so the head stays on its line, the forearms paddle 6 deg. |
| roar | 66 | no | `flare` 20, `roar` 30 | CROWN FLARE: f0-14 the neck gathers 12 deg with the head held level; the blades rise 15 deg and fan out 10 deg, centre first, the outer blades 2 / 4 frames later (`flare`); the jaw opens late to 26 deg and the forearms spread (`roar`, ref #3); f44-66 close, the blades settle back slower (ref #9). |
| act_molt | 110 | no | `lift1` 22, `lift2` 48, `shed` 56 | THE CROWN SHEDS: f0-18 the neck arches 22.5 deg, head level; f12-34 the blades lift one by one (3-frame lag) - the four outer blades 45 deg, the centre 35 (final 8.5) - and fan open like a crest (front read), lifting off their sockets; f44-56 the centre blade rises furthest (40 deg) and holds while the outer blades drop back (`shed`); f62-86 a 6-deg ripple runs tail -> head along the body (plan); f84-108 the blades reseat in reverse order, slower than they rose (the centre blade over f84-100); exact rest at f110. |

## VFX anchor bones (plan section 8)
`Crown_1`..`Crown_5` (FX_EmberSpark on `lift1/lift2/shed`), `Vent_1`..`Vent_6` (FX_VentSmoke on `smoke1/2`), `Mouth`
(FX_EmberPuff on `roar`), `Tail_Tip` (FX_EmberTip on `flick`), `Claw_L` / `Claw_R` (FX_EmberPaddle on `paddle1/2`).

## Signature act in one line
The overlord arches its neck and lifts its five obsidian crown blades one by one like a flaring crest, sheds them back
with a ripple down its body, and reseats them.

## Deviation for the reviewer
- **Slither direction:** the plan says the S-wave runs "from the tail to the head". Real lateral undulation (S1, U1)
  runs head -> tail; a tail -> head wave reads as the snake swimming backwards, so the slither runs head -> tail. The
  molt's shedding ripple keeps the plan's tail -> head direction (it is not locomotion).

## Round-3 model fixes (review 2) shipped with these clips
- **M1** obsidian cap lower edge 55 -> 65 deg, rose slits 0.018 proud (+ pupils): the eyes read from the front again.
- **M2** V muzzle: the last two skull stations 0.070 / 0.048 and 0.055 / 0.040.
- **M3** dorsal saddle 9 deg (body) / 8 deg (tail), the neck saddle dropped (the rings carry the neck):
  **game PLUM_OBS 43.2 % / OBS_D 37.8 %** (targets >= 40 / <= 40).
- **M4** RAD[1..3] = 0.275 / 0.250 / 0.225.
- **M5** lava hot core w x 0.50; the crown centre gem is LAVA (ROSE_H retired).
- **NICE 1** outer-blade gold 0.020; NICE 3: the centre blade's gold 0.034 and the centre blade 0.30 tall (the hero
  grew a little to keep the gold margin). **Gold at 64: portrait 27 px** (brief counter 56), game camera 20.
- Shares (strict) side / tq / game: PLUM_OBS 50.0 / 41.8 / 43.2, OBS_D 25.0 / 28.5 / 37.8, PALE_S 7.9 / 9.5 / 0.6,
  ROSE 6.0 / 5.2 / 6.2, LAVA 2.7 / 1.7 / 1.9, GOLD+GOLD_D 2.3 / 7.1 / 5.7. H_MODEL 2.232, stud pitch 0.0477.

## Lead rulings (2026-10-27, after the clip gate)
- Slither head -> tail ACCEPTED; the molt ripple keeps tail -> head.
- Gold: portrait 27 / game 20 passes the 25-px portrait gate (the earlier 56 came from a different counter).
