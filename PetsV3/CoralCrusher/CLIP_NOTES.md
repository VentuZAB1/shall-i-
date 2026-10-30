# Coral Crusher - clip notes (CLIP GATE, 2026-10-27)

References: `ANIM_REFS.md` (rock-crab walk footage C1, fiddler-crab wave C2, refs #5 / #6 / #7).
Gate run: `headless_full ... 1` (step 1) -> `_scratch/clipgate.txt`. Sheet: `renders/_pose_tq_sheet.png` (21 beats, labelled).

## WALK MARGIN (2026-10-28, after `_review/CoralCrusher_final85_r6.md`: PASS on every clip, walk 8.5 on the floor) - EXPORTED 08:52
Backups:
- the 06:20 export: `_scratch/CoralCrusher_exported_walk_r6.py`
- this export: `_scratch/CoralCrusher_exported_walk_r7.py`
- **Fore-aft spine pitch +/-1.5 deg**, two cycles per walk, with the extremes on the tripod contacts.
  - Phase choice: **nose UP at each contact** (f13.8 / f28.8), nose down mid-step.
  - The nose-down-at-contact phase gave the shell top-centre only 3.8 px; nose-up gives 4.5 px (`_scratch/walkpx_pitch*.txt`).
  - Lift 0.10, bob 0.016, roll 2.4, crusher sway 6, duty 0.55, n 30 and the C1 timing are unchanged.
- **Phone-size motion** (`_scratch/walk_px.py`, game camera 390 px, f0-15 = contact to contact):
  - Carapace top centre **4.5** px (was 3.5) - now >= 4 on its own.
  - Rims 7.9 / 5.2; leg tips 12.1-21.7 (16.4-22.5 over the full cycle).
  - Data: `_scratch/walkpx_final_r6.txt` / `_full.txt`.
- **Step 1** (`_scratch/export_walk_r7.txt`):
  - collision_free **true**; ground -0.013; linear 0; loops 0 / 0.
  - Walk slide **0.0001**; foot drift 0; stride 0.3091; tris 12,452.
  - FBX 08:52.
- **Idle f0 is pixel-identical** to the 06:20 portrait (diff bbox None), so `CoralCrusher_portrait_alt.png` stays.
- **Renders** (title bar 08:53): `renders/_walk_strip_game.png` / `_walk_strip_tq.png` (f0-27 every 3 f, 390 px).
- **Docs:** `ANIM_REFS.md` now states the current walk (lift 0.10, bob 0.016, roll 2.4, pitch +/-1.5, sway 6) and why
  the R1 / O2 level shell is softened (phone-size read).

## WALK ROUND (2026-10-28, after `_review/PERCLIP_AUDIT_crusher_mammoth.md`: walk 8.4 under the per-clip floor) - EXPORTED 06:20
Backups:
- the 05:24 export: `_scratch/CoralCrusher_exported_eyes_r4.py`
- this export: `_scratch/CoralCrusher_exported_walk_r6.py`

Walk block only.
- **Changes:**
  - Leg lift **0.07 -> 0.10 BU**.
  - Carapace bob **0.010 -> 0.016 BU** (as asked).
  - Spine walk roll **1.2 -> 2.4 deg**, same phase and 2 cycles, so the timing is unchanged.
  - Why the roll: with the asked bob alone the carapace moved only 2.4 px on screen (see below). The game camera
    foreshortens vertical motion: bob 0.020 added only +0.3 px, so I kept 0.016 and let the roll rock the shell.
  - Unchanged: claw sway 6 deg, duty 0.55, n 30, stride 0.309, the crab-footage timing (the sand1 / sand2 events).
- **Phone-size motion** (`_scratch/walk_px.py`, game camera 390 px, fixed camera, f0-15 = contact to contact):

  | point | before (05:24) | lift + bob only | **final (+ roll 2.4)** |
  |---|---|---|---|
  | carapace top centre | 1.9 | 2.4 | **3.5** |
  | carapace rim +x | - | 4.6 | **8.1** |
  | carapace rim -x | - | 2.4 | **5.2** |
  | leg tips | 12.1-20.0 | 12.1-21.8 | **12.1-21.7** |
  - Over the full cycle (f0-30) the leg tips move 16.4-22.4 px.
  - Pass >= 4 px: the leg tips and both carapace rims (the body silhouette) pass. The top-centre point of the shell
    reads 3.5 px. It sits on the roll axis, so only the bob moves it.
  - Data: `_scratch/walkpx_before.txt`, `walkpx_after.txt` (lift + bob), `walkpx_roll24.txt`, `walkpx_final.txt`,
    `walkpx_final_fullcycle.txt`.
- **Renders** (title bar 06:22): `renders/_walk_strip_game.png` and `renders/_walk_strip_tq.png`, f0-27 every 3 f at 390 px.
- **Portrait:** idle f0 is pixel-identical to 05:24. I compared the kit portrait before and after (diff bbox None), so
  `CoralCrusher_portrait_alt.png` (05:44) stays.
- **Step 1** (`_scratch/export_walk_r6.txt`):
  - collision_free **true**; ground -0.013; linear 0; loops 0 / 0.
  - Walk slide **0.0016** (<= 0.002); foot z var 0.0008; idle foot drift 0; stride 0.3091.
  - Tris 12,452. FBX `C:\cdimp\CoralCrusher.fbx` 06:20.

## EYE ROUND (2026-10-28, after `_review/CoralCrusher_final85_r4.md`: still PASS 8.5 / 8.5; eye follow not shown at phone size) - EXPORTED 05:24
Backups:
- the 04:43 (9+) export: `_scratch/CoralCrusher_exported_9plus.py`
- this export: `_scratch/CoralCrusher_exported_eyes_r4.py`

The patch is `_scratch/fix_eyes_r4.py`.

- **Geometry (model only, no clip keys changed):**
  - `ES, EB = 1.25, 1.20`: the eyestalk vector is x1.25, (0.02, -0.055, 0.07) -> (0.025, -0.069, 0.0875).
  - The bulb, its offset, the eye (socket / rose slit / black slit pupil, sc 1.1 -> 1.32) and the slate lid are x1.2.
  - The stalk thickness and the joint anchor are unchanged.
  - The look stays fierce: dark copper bulb, black socket, narrow rose slit, black slit pupil, angry slate lid at 18 deg.
    The eyes stand a little taller over the front rim; I don't think they read as cartoony.
  - `renders/_eyes_r4_face.png` shows before / after, front + high 3/4; `renders/_model_sheet.png` (05:25).
- **Phone-size eye travel** (`_scratch/eye_px.py`, game camera at 1x = **390 px**, fixed camera aimed at rest):
  - Projected per eye:
    - tip = the eye vertex farthest from the joint.
    - cen = the slit-eye cluster.
    - own = the eye's motion on screen minus where the same point would sit if rigid with the Spine (the body roll / bob
      taken out).
  - Results, top f30 -> trough f41 (before -> after, px):

    | measure | eye | before | after |
    |---|---|---|---|
    | own motion, cen | L | 4.3 | **5.5** |
    | own motion, cen | R | 5.8 | **7.2** |
    | own motion, tip | L | 5.5 | **6.6** |
    | own motion, tip | R | 6.2 | **7.4** |
    | total travel, tip | L | 10.8 | **12.4** |
    | total travel, tip | R | 6.4 | **7.2** |
  - At the second trough (f66) the after values are own cen 6.2 (L) / 6.7 (R) and total tip 11.0 / 6.3.
  - The tops (f30 / f53 / f76) are identical frames.
  - Pass >= 4 px: met for both eyes at both troughs. Before the change it was already 4.3-6.2 own; the review's 1-3 px
    was an estimate.
  - Raw data: `_scratch/eyepx_before.txt` / `eyepx_after.txt`.
- **Claw over the right eye:**
  - Ray cast from the game camera to every vertex of each eye's front cluster: **vis 1.0** at f30 / 36 / 41 / 44 / 53 / 60
    / 62 / 66 / 76 for both eyes, so no other bone's faces are in front.
  - Seen in `renders/_eyes_r4_game1x.png`: f30 / 41 / 53 / 62 / 66, the full 390 px frame plus the eye box x4
    (nearest-neighbour). At the troughs the crusher's lower edge passes just above the right stalk and does not cover it.
  - `renders/_eyes_r4_game_cmp.png` compares the eye box before vs after at f30 / f41 / f66.
- **Step 1** (`_scratch/export_eyes_r4.txt`):
  - collision_free **true** (claw vs Eye_L / Eye_R are in check_pairs); ground -0.013 everywhere.
  - Linear 0; loops 0 / 0; walk slide 0.002; tris **12,452** (unchanged); stride 0.3091.
  - FBX `C:\cdimp\CoralCrusher.fbx` 05:24.
- **Portrait alt (r5 housekeeping, 05:44:59):** `CoralCrusher_portrait_alt.png` was re-made from the 05:24 file with the same
  game camera (`_tools/game_raw.py`, idle f0, 512 px RGBA, then copied as before). The 04:44 copy is in
  `_scratch/stale_0444/`.

## 9+ ROUND (2026-10-28, after `_review/CoralCrusher_final85_r3.md`: model 8.5 + clips 8.5 PASS) - EXPORTED 04:43
Backup of the r2 export: `_scratch/CoralCrusher_exported_r2.py`.
- **Eyes (final):**
  - Left yaw **-22 x track** (was -12). Right **30 x track** (was 4 base + 20 x track). Both are 2 f behind the wave,
    with the mirrored-bone signs re-checked.
  - The lower trough (below) changed the geometry: the claw tip now passes almost in front of the right eye at both the
    tops and the troughs. So the right eye **stays locked on the tip** (tip angle 3.0 at the tops, 3.5 at the troughs),
    and the review's tip-angle swing no longer measures how much it moves.
  - The probe (`_scratch/eye_probe.py`, `eye_r3.txt`) now also reports each stalk's world heading:

    | eye | heading, troughs (f41 / 64) | heading, tops (f30 / 53 / 76) | heading swing | tip angle, troughs -> tops |
    |---|---|---|---|---|
    | left | 72.7 | 34.5 | **38.2 deg** | 64.1 -> 44.0 (**20.1 deg**) |
    | right | 23.7 | 39.3 | **15.6 deg** | 3.5 -> 3.0 (locked on the tip) |

    The right eye turns exactly as far as the tip moves as seen from it; more yaw would make it leave the claw.
    At f36 the right eye lags the claw's first drop (tip angle 23.4) and catches up by f41 - the 2 f lag.
  - Rest at f0 / f110 is exact (L 50.9 / R 4.6).
- **Shell roll +/-4** (was 3): -6 at the tops, +2 at the troughs. The crusher-side shoulder sits -0.0625 at the tops and
  +0.0209 at the troughs, a swing of **0.083 BU** (target >= 0.08).
- **Idle guard breath +/-6** (was 5), on the same 35 f arc; the f70 tap stays.
- **Act trough, lower:**
  - Merus trough **2** (was 16) and palm (wrist) trough **+2** (was -40); the top is unchanged (merus 40, wrist -6).
  - collision_free stays true. The full gate was re-run at merus 12, 8 and 2, then with the wrist change.
  - World angles at f41: merus 22.6 deg and carpus 19.2 deg above horizontal; the palm-to-tip is **46.5 deg** (was
    71.5). The tip drops **0.36 BU** from top to trough (was 0.18).
- **N1, model:** the two dome rose clusters taper - wider ROSE_D base (0.060 x scale, was 0.045) and pointed ROSE spikes
  (top 0.22, base 0.030 x scale). `renders/close_domeclusters.png`.
- **Step 1** (`_scratch/export_r3.txt`):
  - collision_free **true**; ground_min_z -0.013 in every clip.
  - Linear 0; idle and walk loops 0 / 0; idle foot drift 0; walk slide 0.002.
  - Tris **12,452**. Events are unchanged.
- **Renders (title bar = render time, 2026-10-28 04:40):**
  - `_act_eyes_roll.png` - game + front cameras, f0 / f30 / f41 / f53, from the current file.
  - `_model_sheet.png`, `_beats2x_idle.png` (idle f0 / 20 / 45 / 62 / 80 / 110), `_pose_tq_sheet.png`, `_wave_strip.png`.
  - `close_domeclusters.png`, `_icons3_strip_128.png`, `gamelook_game.png`.
- **Export:** `C:\cdimp\CoralCrusher.fbx` (04:43, after the left-eye raise). `CoralCrusher_portrait_alt.png` is re-made
  from the game camera (04:44).

## FINAL 8.5 ROUND 2 (2026-10-28, after `_review/CoralCrusher_final85_r2.md`, model 8.5 PASS, clips 8.0) - EXPORTED
- **CM-R2-1, idle:** the crusher guard breathes **+/-5 deg** (was 3) over the same 35 f arc (troughs f45 / f80, peak f62).
- **CM-R2-2, act:**
  - The right eye's tracking yaw is **20 x track** (was 12); the left stays -12. The eye bones are mirrored, so L is
    - and R is +, re-checked with the probe.
  - Horizontal angle from each stalk to the crusher tip (`_scratch/eye_probe.py`, `eye_r2.txt`):

    | eye | troughs (f41 / 64) | tops (f30 / 53 / 76) | f36 | tracking |
    |---|---|---|---|---|
    | right | 21.5 | 5.2 | 0.7 | **16.3 deg** |
    | left | 71.8 | 56.8 | – | **15.0 deg** |

    Both eyes are >= 10 deg.
  - **Shell roll +/-3 deg** with the beat (was 2): -5 at the tops, +1 at the troughs. The crusher shoulder sits
    0.052 lower than the cutter's at the tops and 0.010 higher at the troughs.
- **CM-R2-3, walk sway:**
  - At 4 deg the crusher did not visibly move in a game-camera preview (every 3 f, 320 px). It is now **6 deg** (spread,
    twice per 30 f cycle, between the tripod contacts); `renders/_walk_sway_strip.png` shows the 6 deg version.
  - `renders/_walk_sway_claw.png` (a crusher crop of the same frames with a fixed reference line) shows the tip moving.
  - **Walk slide stays 0.002** (foot_z_var 0.001).
- **Step 1** (`_scratch/export_r2.txt`):
  - collision_free **true**; ground_min_z -0.013 in every clip.
  - Linear 0; idle and walk loops 0 / 0; idle foot drift 0.
  - Tris 12,644. Clips and events are unchanged.
- **Renders:** `_pose_tq_sheet.png` (26 beats incl. idle f0-110) and `_wave_strip.png` (re-made); the walk strips above.
- **Export:** `C:\cdimp\CoralCrusher.fbx` (2026-10-28 03:48). `CoralCrusher_portrait_alt.png` re-made from the game
  camera.

## FINAL 8.5 (2026-10-28, after `_review/CoralCrusher_final85.md`, FIX clips 7.5) - EXPORTED
- **CM1, the idle breathes:**
  - The crusher guard breathes **20 +/- 3 deg** over one 35 f arc: troughs f45 / f80, peak f62, back to 20 by f98.
    The tap at f70 still reads.
  - The body bob is **0.008** (was 0.004), two breaths per loop, and the loop is closed.
  - Evidence: `renders/_pose_tq_sheet.png`, row 1 = idle f0 / 20 / 45 / 62 / 70 / 80 / 98 / 110.
- **CM2, secondary motion on the wave:**
  - The eyestalks track the crusher, 2 f behind the wave: a 0-1 track curve with tops held f28-36 / f51-59 / f74-82
    and troughs f41 / f64. Yaw **12 deg** toward the crusher on both eyes; the eye bones are mirrored, so L is - and
    R is +. The right eye also keeps a 4 deg base glance.
  - Probe (`_scratch/eye_probe.py`, horizontal angle from each stalk to the crusher tip) - both eyes point closer to the
    tip at the tops:

    | eye | tops (f30 / 53 / 76) | troughs (f41 / 64) |
    |---|---|---|
    | left | 57.9 | 71.4 |
    | right | 15.8 | 20.7 |
  - The r5 static `r=-8` actually turned the right eye AWAY from the crusher; it is now +4.
  - **Shell weight:** the roll is -2 +/- 2 deg with the beat (-4 at the tops, 0 at the troughs). The crusher shoulder
    sits 0.042 lower than the cutter's at each top and level at the troughs.
  - Evidence: `renders/_wave_strip.png` (tq + game, f18-82 every 2 f).
- **CM3:** the lead ruling is written into `ANIM_REFS.md`: the Wikimedia crab footage (C1) sets the walk timing; the
  site Ohmu (S1) backs only the leg alternation and the level shell.
- **TO 9+ 4, walk:** the crusher sways **4 deg** (spread) twice per 30 f cycle, phase-shifted between the tripod contacts.
  The cutter keeps its lift wave only.
- **Step 1** (`_scratch/export_f85.txt`):
  - collision_free **true**; ground_min_z -0.013 in every clip (the r5 value, the toe tips).
  - Linear 0; idle and walk loops 0 / 0; idle foot drift 0; **walk slide 0.002**, foot_z_var 0.001.
  - Clips and events are unchanged (act `wave1` 30, `wave2` 53, `wave3` 76, `tap1` 90, `tap2` 96).
- **Export:** `C:\cdimp\CoralCrusher.fbx` (2026-10-28 01:48, 1,223,484 B). The Index portrait is
  `CoralCrusher_portrait_alt.png`, re-made from the game camera.

## ROUND 5 (2026-10-27, after `_review/CoralCrusher_review4.md`, APPROVED 8/10): NICE pass, then EXPORT
- The wave tops are now **held 8 f** (f26-34 / f49-57 / f72-80). Events sit on the hold centres: `wave1` f30, `wave2` f53,
  `wave3` **f76**.
- The down-stroke is now **5 f** (trough f39 / f62; S2 H3's drop is 3-5 f) and the up-sweep 10 f.
- The act stays **120 f**. The time came out of the rest tail:
  - point out f80-86;
  - cutter taps **f90 / f96** (`tap1`, `tap2`);
  - swing in f96-103, fold down f103-110;
  - exact rest f110-120.
- The act is keyed every frame so the odd-frame troughs land exactly (Lua 58.7 KB).
- Step 1 (`_scratch/clipgate_r5.txt`): collision_free **true**, ground_min_z -0.013, linear 0, loops 0 / 0, slide 0.002.
- `renders/_wave_strip.png` re-rendered: tq + game, every 2 f, f18-82, holds / troughs labelled. I checked it: the three
  holds are still poses, and each drop to the in-front trough is visible.

## ROUND 4 (2026-10-27, after `_review/CoralCrusher_review3.md`, APPROVED WITH FIXES 8/10)
- **M1, site refs:** `ANIM_REFS.md` S1 = the *Nausicaa* Ohmu run (site `/tags/creature-animation` -> Sakugabooru #270689,
  f1987-f2042: alternating leg sets, level shell). It agrees with the Wikimedia read, so **the walk is unchanged**.
  S2 = James Baxter's dancing horse (site `/tags/creature-animation` -> Sakugabooru #170480: raise f34-42, hold f42-90 while
  the other foreleg works, quick drop f90-92). No site opens spent. The tags tried and the rejected clips are in the log.
- **M2, the wave re-timed (act length 120):** three slow display arcs. The tops hold 4 f (f26-30 / f48-52 / f70-74);
  `wave1` f28, `wave2` f50 and `wave3` f72 sit on the held peaks. Troughs at f38 / f60; the up-sweep takes 10 f, the
  return 8 f. Top = the claw raised high; trough = swung down and forward in front. Rotation between top and trough
  (world, `_scratch/swing_probe.py`): **merus 36.7 deg, carpus 42.1 deg, claw 36.7 deg** (all >= 30). After the waves
  (f74-80) the claw points out and holds while the cutter taps (`tap1` f84, `tap2` f90). f90-104 it swings in first, then
  folds down. f104-120 exact rest.
  - A first try waved only the carpus (8 <-> 44 deg). Its "peak" folded the claw BACK over the shell, lower, not up
    (`_scratch/tip_probe.py`). The final keys move the merus, spread, carpus and palm together.
  - Two collision-free limits shaped the trough. With the merus below ~16 deg and the claw spread out, the carpus cut into
    the front rim (`collide_where`: 74-112 tri pairs at f38-41). So the trough keeps the merus at 16 and brings the claw IN
    (spread 6); the palm drop (-40) carries the "down".
- **N2:** the act stands taller: body rise 0.05 -> **0.10 BU**, pitch -3 -> **-5**. All six feet stay planted (foot drift
  0.0 every frame, `_scratch/plant_probe.py`).
- **N3:** the roar claws lift to **30 deg** (from 25); the clacks stay cocked open 30 deg.
- **N1 (optional belly dome):** not done. It is a model change for a view the game camera never shows; it can go into a
  later model pass if wanted.
- **Gate (step 1, `_scratch/clipgate_r4.txt`):** collision_free **true**, ground_min_z -0.013 (rest), linear 0, idle loop
  0 / 0, walk loop 0 / 0, slide 0.002, foot_z_var 0.001.
- **Renders:** `renders/_wave_strip.png` (tq + game, every 2 f, f18-78, tops / troughs labelled);
  `renders/_pose_tq_sheet.png` rebuilt with the new roar + act beats (the round-3 act renders moved to `_scratch/old_r3_poses/`).

## Numbers (step 1)
- **collision_free: true** (all clips, every frame). ground_min_z -0.013 (the black leg tips at rest; never lower).
- Audit: linear 0 everywhere; idle loop_pos 0 / loop_rot 0 / idle_foot_drift 0; walk loop 0 / 0, **slide 0.002**,
  foot_z_var 0.001. Stride 0.309 BU per cycle. Tris 11,900. Lua 55 KB.
- **Crossfade (review 2 M2, option A):** every clip rests at the walk's 45 deg spine yaw, so the idle -> walk blend turns
  nothing. Simulated blend (`_scratch/crossfade.py`, 0.3 s): **max ankle travel 0.077 BU** (target <= 0.2; was 0.79 with
  the idle at yaw 0), ankles never below 0.066. Sheet `renders/_crossfade_sheet.png`, numbers `_scratch/xfade_r3.txt`.

## Clips
| clip | frames | loop | events (frame) | what it does |
|---|---|---|---|---|
| idle | 120 | yes | `tap` 70 | CLAW GUARD: base pose at yaw 45; the crusher lifts 20 deg to guard f12-28 and holds to f98; the eyestalks swivel one at a time (L f18-50, R f54-86) with freezes between (ref #7); the cutter taps once (lift f60-66, down f70); mandible twitch; legs planted. f0 = the base pose (portrait). |
| walk | 30 | yes | `sand1` 13.8, `sand2` 28.8 (tripod touch-downs) | diagonal scuttle at yaw 45 (C1 R2; the site Ohmu clip S1 is a RUN: it supports the leg alternation, not the walk timing), tripods L1/R5/L3 vs R4/L2/R6, duty 0.55, lift 0.10, carapace bob 0.016, roll 2.4, fore-aft pitch +/-1.5 (nose up on the contacts), crusher sway 6 (2026-10-28), claws folded 10 deg low (review 2 N5, C1 R3), the eyes lag. |
| roar | 60 | no | `clack1` 22, `clack2` 30, `clack3` 38, `bubble` 24 | CLACK THREAT: a short crouch f0-4, the body rises 0.05 H and both claws lift forward 30 deg (round 4) + spread f4-14 (ref #6); three clacks, each a cocked open (30 deg) then a 2-frame snap shut and a hard stop (ref #5); the mandibles open f14-44; lower and settle f40-60. |
| act_semaphore | 120 | no | `wave1` 30, `wave2` 53, `wave3` 76, `tap1` 90, `tap2` 96 | THE FIDDLER WAVE (round 5): stand tall f0-18 (rise 0.10 BU, pitch -5); three slow arcs with 8-f held tops (f26-34, f49-57, f72-80), troughs f39 / f62, 10 f up / 5 f down; f80-86 the claw points out and holds while the cutter taps twice (f90, f96); f96-110 swing in, then fold down; exact rest f110-120. Legs planted every frame. |

## VFX anchor bones (plan section 8)
`Claw_Tip_L` / `Claw_Tip_R` (rose sparkle on the waves, bubble on the clacks), `Foot_1`..`Foot_6` (sand puff on
`sand1/2`), `Mouth` (`bubble`). No eyestalk anchors.

## Signature act in one line
The fiddler wave: the crab stands tall and waves its giant crusher claw in three slow arcs, holding each top, then
answers with two taps of the small claw.

## Changes made for the clips (rig / geometry)
- Pincer hinge zone in `joints()` 0.08c -> 0.12c, and the finger-tip curl 0.48 -> 0.36: at rest the two finger tips
  touched, so any pinch reported Claw|Pincer contacts; now the clacks are clean.
- `pinch` sign kept (+ opens).

## Round-3 model fixes (review 2) shipped with these clips
- **M1 claws:** the cream claw undersides are DROPPED (the review allowed "or drop them entirely"); palm, fingers and
  the shoulder / elbow / wrist knuckles are smooth (nostud); studs stay on the merus + carpus arm blocks.
- **M1 pale share - needs a ruling:** with the claw cream gone, BELLY_PALE is **0.9 % side / 0.4 % tq / 0.8 % game**.
  I raised the cream lip (now a ledge 0.034 proud of the rim band, `hw + 0.034` at 0.05 below the rim) and tested a
  cream rim band: neither moves the side share, because from the 10-deg side camera the flank under the rim is fully
  covered by the six legs (coxa + merus plates reach z 0.37, the rim is at 0.36-0.41) and the margin spines - see
  `_scratch/lipchk.png`. The cream underside, lip and sternum show from below / low front (`renders/_under_sheet.png`).
  The only way to reach >= 5 % side was cream on the claws (rejected). Options for the reviewer: accept the underside
  as built (pale visible from low angles only), or allow a thin flush ventral claw edge back (the test gave 4.6 % side,
  ~83 % of it on the claws: `_scratch/shares_r3_with.json`).
- **M2:** option A (base pose yaw 45) - done, see the crossfade numbers above.
- **M3 portrait:** `CoralCrusher/CoralCrusher_portrait_alt.png` = the GAME-CAMERA render of idle f0 (512 px, transparent,
  kit framing: fill 0.72 x 0.66). The Index should show this file. (The kit's `CoralCrusher_portrait_raw.png` is the
  flat-slug view - do not use it.)
- **N1** a second raised plate row across the rear dome; **N3** rear ledge 0.01 lower; **N4** margin spines alternate
  large / small; **N5** walk claws 10 deg lower.
- Shares now (strict): side BRONZE 49.6 / BRONZE_D 12.1 / SHELL_D 19.2 / ROSE+ROSE_D 11.1 / pale 0.9;
  game ROSE+ROSE_D 11.3, SHELL_D 16.2.

## Lead rulings (2026-10-27, after the clip gate)
- Pale share ACCEPTED as built (0.9 % side; the underside / lip read from low angles). The claw edge stays out.
