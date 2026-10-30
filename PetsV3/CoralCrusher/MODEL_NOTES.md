# Coral Crusher - model notes (MODEL GATE + sideways-walk BUILD GATE, 2026-10-27)

Tide / Water egg, MEDIUM 15 %. Plan: `_review/CoralCrusher_plan.md` v2. File: `pets/CoralCrusher.py` (model + rig + check_pairs
+ joints + the build-gate PROTOTYPE clips: idle hold, walk, a test wave; the final idle / roar / act come after the verdict).

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

## FINAL 8.5 (2026-10-28, after `_review/CoralCrusher_final85.md`, FIX model 7.5) - EXPORTED
Single gate file: `_scratch/gate_f85.json`. Backup of the r5 export: `_scratch/CoralCrusher_exported_r5.py`.
- **MM1, rust copper:** BRONZE **(214,110,70)**, BRONZE_D **(150,74,50)**, SHELL_D **(80,46,34)**, exactly as specified.
  BELLY_PALE and ROSE are unchanged.
  - `renders/gamelook_game.png` (0.6x) reads a rust red-brown, not tan.
  - In `renders/_icons3_strip_128.png` (kit portrait, ALT, game icon, Kappa, Turtle, Kraken, Hammerjaw, Orca) the crab is
    a solid copper-orange. Hammerjaw stays navy with orange stripes and the Kraken red, so the copper reads as the
    crab's own colour.
- **MM2, pale edge:**
  - The rim band is now **BELLY_PALE**: 0.030 proud, 0.080 tall, deepening toward the rear to 0.065 proud and 0.170
    tall. A thin SHELL_D seam sits above it, inside the band edge, so from above the cream top shows past it.
  - The cream lip is lower (zc - 0.10) and wider (+0.040, rear +0.070).
  - **The 4 % target is NOT met:** BELLY_PALE is **side 1.6 %, game 2.2 %** (tq 0.8, back 5.6), all figure
    pixels. Strict counts: side 1.6, game 2.2.
  - From the side camera (45 deg base yaw) the crusher claw, the margin spines and the leg plates cover the rim. From the
    game camera only the rear edge shows; it now reads as a cream two-tone edge (`renders/model_tq.png`,
    `_under_sheet.png`).
  - Doubling the share would need a pale skirt around the whole shell or cream on the claws (rejected in review 2).
    **This needs the owner's written no-pale sign-off, as the review says.**
- **TO 9+ 1:** merus 0.084 x 0.110 (+20 %), coxa 0.080, top plate and spike raised with it.
- **TO 9+ 2:** the finger roots sit 0.097 c off the palm axis (was 0.085), giving a gape of about 0.06 H on the crusher.
  The four molars are bigger (0.030 x 0.026 x 0.022 c) on the inner edges of both fingers (they already existed but
  were small). Evidence: `renders/close_crushertq.png`, `close_crusherin.png`.
- **TO 9+ 3:** two taller ROSE_D + ROSE coral clusters on the dome centre (scale 1.30 / 1.20) at (0.075, 0.075) and
  (-0.085, 0.02).
- **Shares (all figure pixels, flat renders, %):**

  | view | BRONZE | BRONZE_D | SHELL_D | pale | rose |
  |---|---|---|---|---|---|
  | game | 51.6 | 12.6 | 16.5 | 2.2 | 13.1 |
  | side | 46.9 | 12.4 | 19.2 | 1.6 | 13.7 |
  | tq | 50.1 | 8.0 | 19.7 | 0.8 | 15.5 |
  | back | 44.2 | 15.3 | 15.3 | 5.6 | 16.2 |
- **Tris 12,644** (cap 15k). Lua 58,671 B.
- **Renders (2026-10-28):** `_model_sheet.png`, `_close_sheet.png` (crusher front / in / tq, face front / high),
  `_under_sheet.png`, `_icons_strip_*`, `_icons2_strip_*`, `_icons3_strip_*`, `gamelook_*.png`, `flat_*.png`.
- **Index portrait:** `CoralCrusher_portrait_alt.png` is re-made (= the game-camera render of idle f0, as ruled).

## ROUND 3 (2026-10-27, after `_review/CoralCrusher_review2.md`, APPROVED WITH FIXES 7/10) - shipped with the clips
- **M1** the cream claw undersides are dropped; palm, fingers and knuckles nostud. Pale share: **side 0.9 % / tq 0.4 % /
  game 0.8 %** - the >= 5 % side target is NOT met (the legs and margin spines cover the flank under the rim from the side
  camera; `_scratch/lipchk.png`). A flush ventral claw edge test gave 4.6 % side, ~83 % of it on the claws
  (`_scratch/shares_r3_with.json`) - against the <= 1/3 rule, so not shipped. Needs a ruling (see `CLIP_NOTES.md`).
- **M2** base pose at the walk's 45 deg spine yaw in every clip: crossfade ankle travel **0.077 BU** (was 0.79).
- **M3** `CoralCrusher_portrait_alt.png` = the game-camera icon of idle f0 (512 px, transparent).
- NICE N1 second plate row on the rear dome, N3 rear ledge 0.01 lower, N4 alternating margin spines, N5 walk claws 10 deg
  lower. Evidence: `renders/_close_sheet.png` (front, high, clawtq, clawside), `renders/_under_sheet.png`,
  `renders/_crossfade_sheet.png`, `_scratch/shares_strict.json`, `_scratch/xfade_r3.txt`.

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

## Numbers (round 1)
- Tris: **9,932** (cap 15k).
- HEIGHT 7.5 studs = top of the raised claws; H_MODEL 1.287 BU (measured); stud pitch 0.0385.
- Footprint 2.34 x 1.98 BU (13.6 x 11.5 studs at x1): a wide, low crab (carapace 1.40 x 1.08 x 0.44 BU).

## What I built
- Carapace: a smooth domed bronze loft (8 superellipse stations, flatter belly), a dark slate rim band + a pale lip under it (the
  two-tone crab edge), slate H-groove (midline, cervical V, two branchial arcs = the plan's ridge seams), 8 rose-coral margin teeth
  per side (largest at the front), 3 small rounded rose coral growths on the rear (read from the game camera).
- Front: short thick eyestalks (0.07H) out of the front edge with **wedge rose slits** + thin black pupils, each hooded by a slate
  lid (18 deg inner-down), a slate V brow plate between them; pale mandible plates splayed in a V over a dark mouth with small
  ivory teeth.
- Claws: bronze merus with 2 rose spikes, slate knuckles, carpus with a spike, an **oval lofted palm** (tube, 0.34 tall x 0.24
  thick on the crusher) with 4 rose spikes on its outer face and a pale keel strip, a fixed finger and a hinged dactyl (bronze ->
  slate -> black tip, curved toward each other, slate molars on the inner edges). **Asymmetric: right = CRUSHER (x1.20), left =
  cutter (x0.98).**
- Six slate legs (coxa, flat merus with a bronze top plate + a rose spike, slate knee, propodus, dactyl, black tip), low splayed
  crab stance.

## Palette and value shares (flat renders, %)
| Name | RGB | side | tq | game | plan (side) |
|---|---|---|---|---|---|
| BRONZE | 186,124,80 | 49.7 | 49.5 | 56.7 | 40 |
| SHELL_D | 100,66,46 | 34.5 | 31.1 | 28.6 | 14 |
| BELLY_PALE | 240,226,200 | 1.2 | 3.7 | 0.4 | 8 |
| ROSE | 255,120,150 | 6.3 | 6.7 | 5.7 | 8 |
| ROSE_D | 200,70,110 | 2.4 | 2.6 | 3.9 | 3 |
| BLACK | 14,14,22 | 3.9 | 4.6 | 3.1 | 3 |
| MOUTH / IVORY | | 1.9 / 0 | 1.7 / 0 | 1.7 / 0 | <1 |

## Deviations from the plan (and why)
1. **Colours deepened, same hues:** BRONZE (196,150,104) -> (186,124,80), SHELL_D (132,96,66) -> (100,66,46). The plan values read
   pale tan next to the approved Water pets in the strip. In game about (112,74,48): a dark copper-bronze.
2. **Claw asymmetry** (crusher + cutter): the plan's idle and act already speak of "the big claw" and "the small claw".
3. **Legs longer than 0.30H** (about 0.6H along the chain): 0.30H legs cannot hold the shell 0.20H up with an arched crab knee.
4. **Additions:** rim band + pale lip, the H groove, coral growths, a rose spike + bronze plate on each leg merus, pale keel strips.
5. **Shares off the plan:** SHELL_D is high (the six legs are a big area in profile); BELLY_PALE is low because the overhanging
   carapace hides the belly in profile (pale shows on the lip, the claw keels and the mandibles; tq 3.7 %). Rose is 6.3-6.7 %
   (+2.4-2.6 % ROSE_D) vs plan 8 + 3.

## BUILD GATE: the six-leg sideways walk (plan section 11.1)
- The game moves every pet along its facing (-Y). So the walk clip turns the carapace **90 deg (Spine yaw +90, the crusher side
  leads)** and the six legs step along the travel axis in alternating tripods (L1+R2+L3 | R1+L2+R3, small 0.04 stagger), duty 0.55,
  half stride 0.085, lift 0.07, 24 f, stride 0.309 BU per cycle. **No yaw wobble inside the cycle** (body yaw constant). The turn
  into / out of it is the CreatureAnimator idle <-> walk crossfade (~0.3 s). Dactyls keep their rest direction turned with the body.
- Result (headless_full, step 1, final model): **walk slide 0.0, foot_z_var 0.0, loop_pos 0, loop_rot 0, linear 0,
  collision_free true, ground_min_z -0.010.**
- Wave test (`act_semaphore` prototype): body stands 0.05 taller, the crusher lifts (merus 30 + spread 35) and the carpus waves
  8 <-> 38 deg three times; **all six feet planted every frame (IK), idle_foot_drift 0.0, collision-free.**
- Sheet: `renders/_walkgate_sheet.png` (walk f0/6/12/18, wave f26/40).
- A pinch sign / eyestalk clearance issue found in the first gate run was fixed in geometry (eyes moved out of the shell front,
  the brow plate shortened, the claw shoulder moved forward/out).

## Rig
Spine (carapace), Mouth (mandibles), Eye_L/R (stalks), Arm/Fore/Claw/Pincer L/R (merus, carpus, palm + fixed finger, dactyl),
Leg_1..6 / Shin_1..6 / Foot_1..6 (1-3 = left front -> back, 4-6 = right front -> back; IK, knee poles up-out).
VFX anchors: `Claw_Tip_L/R` (rose sparkle / bubble burst, on the dactyl tips), `Foot_1..Foot_6` (sand puffs = the leg tip bones),
`Mouth` (bubble burst).

## Evidence
`renders/_model_sheet.png`, `renders/_close_sheet.png` (face), `renders/_icons_strip_64.png` / `_128.png`,
`renders/_icons2_strip_64.png` / `_128.png` (portrait + game-camera icon + Kappa, Turtle, Kraken, Hammerjaw, Orca),
`renders/gamelook_*.png`, `renders/_walkgate_sheet.png`.
Note: the kit's portrait camera sees the wide crab low and small; the game-camera icon reads better (claws + shell).
