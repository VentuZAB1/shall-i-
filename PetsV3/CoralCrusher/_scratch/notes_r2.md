## ROUND 2 (2026-10-27, after `_review/CoralCrusher_review1.md`, REVISE 6/10) - every MUST + NICE applied

Numbers now: **12,156 tris**; H_MODEL 1.049 BU (the rest claws dropped 15 deg, N3); **HEIGHT 7.5 -> 6.1 studs** so the
in-game body stays the round-1 size (7.5 x 1.049 / 1.287; keeping 7.5 would have scaled the whole crab up 23 %, about 14
studs wide). Stud pitch 0.0386.

Walk build gate re-run on the new legs (`headless_full`, step 1, yaw 45): **collision_free true, ground_min_z -0.013,
walk slide 0.0003, foot_z_var 0.0002, loops closed (pos 0 / rot 0), linear 0, idle foot drift 0**, stride 0.309 BU,
tripods unchanged (L1 / R5 / L3 vs R4 / L2 / R6). Sheet `renders/_walkgate_sheet.png` (walk f0/6/12/18 + the act wave
f26/40 with the claw lifted 45 deg from the new lower rest).

Strict value shares (background AND anti-aliased edge / speckle pixels excluded - the r1 sampler issue):

| colour | side | tq | game | target |
|---|---|---|---|---|
| BRONZE | 43.3 | 43.2 | 54.8 | 40 |
| BRONZE_D (new) | 15.7 | 9.6 | 12.5 | - |
| SHELL_D | **18.2** | 17.8 | 14.5 | <= 20 (r1 35) |
| BELLY_PALE | **5.4** | **10.3** | 1.2 | >= 5 side, >= 4 tq (r1 1.2 / 3.7) |
| ROSE + ROSE_D | **12.3** | 13.4 | 13.3 | >= 10 (r1 ~9) |

| # | item | done |
|---|---|---|
| M1 | walk turn | **lead ruling: yaw 45** (`YAW_WALK = 45`, diagonal scuttle, crusher side leads), no pivot clip. Crossfade evidence: `CoralCrusher/_scratch/crossfade.py` simulates the CreatureAnimator blend (walk weight 0 -> 1 over 0.3 s, per-bone quaternion slerp of idle f0 and the walk running from phase 0) -> `renders/_crossfade_sheet.png` (9 frames, yaw 0 -> 45). Ankles stay at 0.066-0.068 (never sink), but a runtime blend cannot re-plant feet: the outer feet are carried round with the body, **max ankle travel 0.79 BU over the 0.3 s at w = 1** (~0.73 of it is the 45 deg turn itself; a 90 deg turn would be ~1.3). That is the price of a yaw-in-clip walk; a planted pivot needs the runtime hook the lead ruled out. |
| M2 | legs | knees at **z 0.30 / 0.30 / 0.29**, pulled out (r 0.21-0.23 from the hip), hip -> knee -> ankle = **0.49 BU = 0.38 H at round-1 H** (r1 0.67); shell underside and hips unchanged. Merus + knee in **BRONZE_D (146,96,62)**; slate only on the coxa, propodus, dactyl (+ black tips). |
| M3 | mandibles | two small **SHELL_D** plates (0.020 x 0.034) at x +/-0.030 under the brow plate, one small **ivory hook tip** each (0.014); no pale blocks on the face. |
| M4a | armour | the H-groove ridges are raised slate **plates** (half-thickness 0.022, 0.020 proud, bevel 0.008) + a **stepped rear plate**: a slate ledge round the rear half of the shell (y 0 -> 0.52, 0.40 of the dome height, up to 0.016 proud) above the rim band. |
| M4b | pale underside | the lip at the old height was hidden by the rim overhang and the legs from the side (pale stayed ~1.4 %). Now: a **cream lip that sticks out past the slate rim band** (shell width + 0.040 at 0.042 below the rim), a cream skin over the whole underside (belly view), and - because six legs cover the lower flank from the side - **broad cream claw undersides**: the lower third of each palm (flush, full palm length, 206-334 deg) running into a **cream fixed finger** (dark finger tips kept). Real crab claws are pale below; it is a two-tone claw, not a strip (the r1 strips are gone, see N2). |
| M5 | portrait icon | the kit portrait camera is fixed in petkit (tq, ~20 deg up) and I may not edit the kit, so two options are rendered: `_scratch/portrait_alt.py` = the same pose from ~37 deg up and 1.45 x size -> `CoralCrusher_portrait_alt_raw.png` / `CoralCrusher_icon_alt.png`, and the game-camera icon `CoralCrusher_icon_game.png`. Strip `renders/_icons3_strip_64/128.png` = [kit portrait, ALT portrait, game-camera icon, Kappa, Turtle, Kraken, Hammerjaw, Orca]. **Recommendation: ship the game-camera icon (or the ALT) as the Index portrait** - the lead / Studio import decides which file is uploaded. |
| M6 | rose | claw merus spikes 0.075c -> 0.10c (w 0.034c), carpus spike 0.10c, palm outer spikes x1.28 (w 0.036c), dactyl spike 0.10c, margin teeth x1.3 length, leg merus spikes 0.085. Rose 12.3 % side. |
| M7 | halo | `_scratch/normals_check.py` splits every mesh into islands and tests every face normal against its island centre: **no inside-out parts** (the only flags were the open palm keel shells, which are thin open strips by design, now removed). The "glass" read was same-colour same-stud BRONZE parts interpenetrating (eye bulbs into the carapace front, the merus root into the shell), so the stud pattern ran across the seam. Fixed by colour: eye stalks + bulbs BRONZE_D and smooth (nostud), a BRONZE_D shoulder knuckle ball at the merus root (same knuckle language as the elbow and wrist). |
| N1 | brows | the centre pair is one slate V plate (~0.14 wide, two overlapping halves, inner ends down 14 deg). |
| N2 | keels | the white palm keel + merus strip are dropped. |
| N3 | rest claws | the whole claw chain rotated 15 deg down about the shoulder (palm 57 -> 42 deg up); the act lift is 45 so the wave reaches the same height. |
| N4 | copper | BRONZE (200,136,88). |
| N5 | rose | ROSE (255,135,165). |
| N7 | lineup | see `_icons3_strip_128.png` / `_icons2_strip_128.png`. |

Deliverables: `renders/_model_sheet.png` (tq/front/side/back 600), `_close_sheet.png` (face front + high, claw tq + side),
`_icons_strip_64/128.png`, `_icons2_strip_64/128.png`, `_icons3_strip_64/128.png`, `_crossfade_sheet.png`,
`_walkgate_sheet.png`, `flat_*.png`, `gamelook_*.png`; numbers in `_scratch/shares_strict.json`, `_scratch/full_r2.txt`,
`_scratch/xfade_r2.txt`.

---- (round 1 notes below, kept for history) ----

