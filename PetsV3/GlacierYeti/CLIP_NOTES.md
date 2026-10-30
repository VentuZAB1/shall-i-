# Glacier Yeti - clip notes (clip gate, 2026-10-27)

References: `ANIM_REFS.md`: Muybridge plate 747 "Baboon walking on all fours" (read frame by frame), plus 1014 refs #3, #5,
#6 and #9, and the Badger's ref B (Pluto heavy drop). No animationreference.org clip could be played.

| clip | frames | loop | events (frame) | what it is |
|---|---|---|---|---|
| idle | 120 | yes | `settle1` f40, `settle2` f50 | plate settle: hip yaw ±4 (one cycle), 3 breaths; the shoulder crusts (Plate bones) lift 4 deg and settle twice f30-50; the head lowers 6 deg f55-75, back by f100; arms hang |
| walk | 48 | yes | `stomp` f24 | KNUCKLE WALK, diagonal sequence (LH, RF, RH, LF), duty 0.62; hunched (spine +8, torso -0.075, bob 0.033 = 0.02H); the fists plant on the snow (fist bottom 0.02); the chest counter-yaws; head level. Stride 0.387 |
| roar | 60 | no | `roar` f24 | SHOULDER-HEAVE BELLOW: shoulders pull back f0-12; two heaves (torso yaw +10 / -10, the forward shoulder's arm swinging) f12-24; head up 15; jaw opens late, peak 24-26 deg f28-45; settle f45-60 |
| act_skid | 100 | no | `skid1` f22, `skid2` f42, `brake` f58 | SNOW SKID AND BRAKE: drops onto wide-planted fists (torso -0.10); sled sweeps forward / back; slides low (-0.14, feet planted, root net 0); cocked lift f52-56, then the fists drive in at f58 (hard stop); push-up with a shoulder heave f66-80; exact rest |

## VFX anchor bones (no mesh)
`FX_ShardBurst_L` [Hand_L], `FX_ShardBurst_R` [Hand_R], `FX_SnowPuff` [Chest], `FX_BreathCloud` [Mouth], `FX_AuroraDust_L` [Plate_L],
`FX_AuroraDust_R` [Plate_R].

## Checks (headless_full step 1 + `_scratch/limits.py`)
- **Collisions:** `collision_free: true`, step 1, all 4 clips.
- **ground_min_z:** 0.002 in every clip (the toes; the planted fists bottom out at 0.02).
- **Audit:** linear 0; loops closed; walk slide 0.0 (feet and fists); idle foot drift 0.
- **Pose limits:**

  | clip | chest vs spine | head pitch-up | max adjacent-frame swing |
  |---|---|---|---|
  | idle | 1.9 | 0.6 | 1.4 |
  | walk | 4.3 | 0 | 4.0 |
  | roar | 4.1 | 15.1 | 7.2 |
  | act_skid | 4.4 | 4.1 | 9.2 |

  The torso lean and twist live on the Spine (pelvis) so the chest stays under 5 deg relative to it. The Yeti has no Neck
  bone.

## Changes made for the clips
- **Model, round-2 MUST fixes:**
  - The upper-arm shelf moved back +0.08 y, down the arm to 0.50, and is 25 % shorter (outline x0.85 / x0.75).
  - The front crust icicle now points straight out (s 0.65, 0, -1) and sits further back (ly -0.03).
- **Model, round-2 NICE:**
  - Pecs sunk (proud 0.024 → 0.014; ab 0.016).
  - Fists tapered into knuckle wedges (top 0.82 / 0.78, rnd 0.40).
  - A navy bicep block on the front of each upper arm.
- **Model, for the clips:**
  - The deltoid crust, its 2 icicles and its aurora seam now ride the `Plate_L/R` bones, so the idle can lift them.
  - Thigh hip width 0.19 → 0.178 (top 0.84), so the inner thighs no longer cut each other in the stride.
- **Rig:**
  - `joints()` gains a neck-sleeve hinge (the skull sits inside the Chest's neck block by design, r 0.18) and a crotch
    hinge (r 0.09).
  - When the head pitches up it also slides forward out of the sleeve (up to 0.05).
  - `check_pairs` adds Plate_L/R vs Head.
- **Tris:** 6,048. Height 1.63 (HEIGHT 9.0).
- **Shares after the fixes (side / game):**
  - POLAR_NAVY 51.8 / 40.8
  - NAVY_D 13.3 / 15.7
  - PLATE_ICE 15.6 / 29.7
  - AURORA 3.0 / 4.3
  - BROW 12.8 / 7.9

## Round 3 (clip review 3, 2026-10-27)
Every number below comes from `_scratch/verify.json`, one saved run of `_scratch/verify.py`. The step-1 JSON is in
`_scratch/full_step1.txt` and the measured footfalls in `_scratch/footfalls.txt`.

### MUST 1: the walk IS diagonal (measured); no change made
- The offsets in `legs` are phase LEADS, not step order. In `petkit.gait_target`, `t = (f/n + offset) % 1` and the foot
  touches down at t = 0, so a limb with offset 0.25 touches down at f/n = 0.75.
- **Measured touch-downs:** Leg_L f0, Arm_R f12, Leg_R f24, Arm_L f36 = LH, RF, RH, LF. That is the diagonal sequence of
  plate 747.
- The suggested swap would make it lateral (LH, LF, RH, RF), so it is not applied.
- Beats: `renders/_beats_rw_*` walk f0 / f12 / f24 / f36. At f12 the right fist plants; at f36 the left.
- `stomp` f24 is the Leg_R (RH) touch-down.

### Mesh
- **MUST 2:** the front crust icicle is deleted. The back one now sweeps out and back, `(s*1.0, 0.30, -0.15)`; no white
  point hangs below the crust's front half in profile (`renders/model_side.png`).
- **MUST 3:** shelf 2 is another +0.06 back (+0.14 in total). In profile it sits on the back half of the arm, behind the
  chest line.
- **NICE 6:** two broad, low knuckle plates per fist (was three).
- **Jaw:** a MOUTH-coloured interior rides the jaw, hidden in the muzzle when closed. The roar's 26 deg opening shows a dark
  mouth from the side, not the background (`renders/_jaw_close.png`).
- **IK poles:** the leg poles now match the modelled knee, `(s*0.31, -0.95, 0)`, and the arm poles the modelled elbow,
  `(s*0.89, 0.46, 0)`. One-shots now start and end at the bind pose: roar 0.056 deg, act_skid 0.234 deg (was 16.6 deg
  on the shins).

### MUST 4: the neck, per the lead ruling
- The Yeti has no Neck bone; the Head joint carries head + neck.
- **Head joint local maximum:** idle 6.7, walk 6.0, roar 22.6 (f22), act_skid 16.0. All are under the head + neck ≤ 30
  rule. Armature pitch-up: roar 20.1, act 4.1.

### MUST 6: Plate vs Jaw
- `("Plate_L", "Jaw")` and `("Plate_R", "Jaw")` are added to `check_pairs`.
- Step 1 is collision_free in all clips, including the roar peak f28-30 and skid f22-28; ground_min_z is 0.002 everywhere.

### Other numbers
- **Chest vs spine** (the Chest bone's local rotation; the Chest is parented to the Spine): idle 2.8, walk 4.27, roar 4.08,
  act 4.39.
- **Largest one-frame swing:** 9.4 deg (Arm_R, act f78).
- **Raw crossings before the hinges** (step 1, Head-Chest, the skull in its neck sleeve): idle 49, walk 76, roar 75,
  act 76. With the hinges the count is 0.
- **Walk:** slide 0.0; loops closed.

### NICE
- **1:** the skid's open mouth is now only the brake GASP (jaw 18 at f58). The rest of the skid keeps it at 2-6 deg.
- **2:** jaw rest is unified. One-shots start and end at 0; idle and walk breathe 0-1 deg.
- **3:** the roar head lift is 20 (head joint 22.6 incl. the chest pull-back), and the jaw peaks at 26 at f28-32.
- **4:** the idle plates lift 6 deg twice, and the chest breath is 2.4 deg.
- **5:** idle to walk is a 0.2 s cross-fade in CreatureAnimator (it blends layer weights), so there is no pop.

### Events (all pets)
- Events are clip-length fractions, `round(f / n, 3)`, as in live ThunderRex.
- The runtime fires them at `t = frac * len`.

### References round (2026-10-27)
The central `ANIM_REFERENCES_1027.md` refs are cited in `ANIM_REFS.md` (the "Central references" section), with the timing changes they caused. After the changes the checks were re-run: step-1 collision_free true; all limits and end-at-rest unchanged (`_scratch/verify.json`, `_scratch/full_step1.txt`).

## Round 4 (2026-10-28)
- **Renders from the FINAL file**, rendered 2026-10-28 00:03:
  - `renders/_model_sheet.png` and `model_tq/front/side/back.png`;
  - `renders/_beats_walk_final_1028_0003_side.png` / `_tq.png` (walk f0 / 12 / 24 / 36);
  - `renders/_beats_skid_final_1028_0003_side.png` / `_tq.png` (skid f7, 16, 22, 28, 42, 55, 58, 66, 74, 80, 90, 100);
  - `renders/_final_mouth.png` (mouth closed at idle f0 vs open at roar f30, front + side).
- **Checked in the renders:**
  - In profile no icicle points down at the muzzle; the one rim icicle sweeps out and back from the crust's rear half.
  - Shelf 2 sits on the back half of the upper arm, not on the chest front.
- **Fixed while checking:** the mouth-interior block's front corners poked through the muzzle as two red dots in the front
  view. The block is now smaller, (0.082, 0.062, 0.042) at y -0.69: the closed muzzle is clean and the open roar still
  shows a dark mouth. Step-1 re-run below.
- **Final export step 1** (with the smaller mouth block): collision_free true, ground_min_z 0.002 in all clips, linear 0, loops closed, slide 0.

## Final 8.5 gate round (2026-10-28, `_review/GlacierYeti_final85.md`)
Numbers: `_scratch/verify.json` (01:14), step 1 + export `_scratch/export_result_f85.txt` (01:13), cross-fade
`_scratch/xfade.json` (01:14).
- **T1 Neck bone:** Chest -> Neck (0, -0.29, 1.42, mid-sleeve) -> Head (throat). `head()` gives the Neck a third of every
  head pitch / yaw (pitch capped at 7.5 so pitch + yaw stays under 8) and the Head the rest. Neck hinges in `joints()`:
  the sleeve root (r 0.20) and the throat fold (r 0.08, where the neck underside meets the chest's front cap when the head
  lifts; 20 tri pairs at roar f19 before it, a seam slide, no poke in `renders/_throat_check.png`). New check pairs:
  Neck vs Chest / Plate_L / Plate_R / Arm_L / Arm_R.
- **C2 roar:** head lift -15 -> -18 (f17) and -20 -> -24 (f22, f28, f45). Roar peak f22: Neck 7.69, Head joint 18.79,
  Neck + Head 26.5 (<= 30); armature pitch-up 24.1. Jaw 26 (f32).
- **C3 idle:** plate keys 6 -> 9 (f35, f45), chest breath 2.4 -> 3.5, hip yaw 4 -> 5. Chest vs spine 3.79.
- **C4 walk:** fist LIFT 0.07 -> 0.10, body bob 0.033 -> 0.050. Walk slide 0.0, loops closed.
- **T5 walk:** the review's chest yaw +-6 would put chest vs spine over 5 (4.27 at +-4 already), so the Chest's own yaw
  is +-4.5 (roll 1.5 -> 1.0, pitch base 1.0 -> 0.9) and the Spine now turns WITH it (-1.5, was a +2 counter-turn): the
  shoulder line swings +-6 in the world (was +-2). Chest vs spine 4.61.
- **Limits:** chest vs spine idle 3.79 / walk 4.61 / roar 4.08 / act 4.39; neck max 2.27 / 2.05 / 7.69 / 5.44; head
  joint 4.41 / 3.98 / 18.79 / 10.56; max one-frame swing 9.4 (Arm_R act f78); one-shots end at rest (roar 0.056, act
  0.234).
- **Step 1 (with export):** collision_free true; ground_min_z 0.002 in all clips; linear 0; loops closed; slide 0;
  idle foot drift 0. Raw crossings before the hinges are listed in verify.json; 0 with the hinges.
- **C1 sheets (re-rendered 03:25 from the final 01:12:59 file, title bars carry the times):** `renders/_beats_f85_ir_tq.png` / `_side.png` (idle f0 / 30 / 45 /
  60 / 75 / 100, roar f0 / 12 / 17 / 22 / 28 / 45 / 52 / 60), `renders/_beats_f85_ws_tq.png` / `_side.png` (walk every
  6 f, skid f7 to f100).
- **C5 cross-fade (offline proxy, Studio is off-limits for builders):** `_scratch/xfade.py` replays CreatureAnimator's
  blend from the read-only code snapshot (weights `w += (target - w) * min(1, dt * 6)` at 60 fps, per-bone Lerp of the
  local transforms, walk from phase 0). Cases: start from idle f0 / f40 / f75, stop from walk f24. Every case:
  collision-free (step 1, hinges), ground_min_z -0.002 to -0.004, and the largest per-step bone change in the blend
  (5.19 deg) is below the pure walk's own (5.85 deg): no pop. Stop: 4.14 deg in the first step as the arms settle.
  Sheet: `renders/_xfade_sheet.png`. The Studio runtime check stays open for the lead / owner.
- **Note for the runtime:** CreatureAnimator's look turn adds `look * 0.5` yaw to BOTH Neck and Head, so with the new Neck
  the head look-turn is about twice the old one (same as other pets that have a Neck).
- Events unchanged: idle settle1 0.333 / settle2 0.417; walk stomp 0.5; roar 0.4; act skid1 0.22 / skid2 0.42 / brake
  0.58.

## Final gate round 2 (2026-10-28)
- **P3:** idle head drop at f65-75 6 -> 9 deg (Neck 3.27, Head joint 6.35). Sheets `renders/_beats_f85r2_ir_*` (idle
  incl. f65 / f75, roar) and `_beats_f85r2_ws_*` (walk, skid), 03:57.
- Step 1 + export (`_scratch/export_result_f85r2.txt`): collision_free true, ground 0.002 in all clips, linear 0, loops
  closed, slide 0. Limits unchanged otherwise (`_scratch/verify.json` 03:59): roar neck 7.69, head joint 18.79, pitch-up
  24.08; chest vs spine max 4.61; max swing 9.4.

## Per-clip audit round 4 (2026-10-28 06:13, exported 06:22)
- Idle (8.1):
  - Plate-settle keys 9 -> 13 deg (f35, f45). Head drop 9 -> 11 deg (f65, f75). Chest breath 3.5 -> 4.2 deg.
  - Chest vs spine is 4.45 @ f80, under 5, so nothing moved into the Spine. Neck 3.94 @ f75, idle pitch-up 3.62.
  - Loops closed, idle foot drift 0, collision_free true, ground 0.002.
  - Reference: `ANIM_REFS.md`, "Idle reference, per-clip round 4" (/tags/subtle, the Kung Fu Panda card, stepped 9.5-16.0 s).
- The other clips are unchanged: walk / roar / act chest vs spine 4.61 / 4.08 / 4.39, neck 2.05 / 7.69 / 5.44, roar pitch-up 24.08.
- Sheets: `_beats_f85r4_idle_side.png`, `_tq.png` and `_game.png` (f0-120 every 10 frames, plus f35/f45/f65; 06:22, file 06:13).

## Final gate round 5 (2026-10-28 08:33, exported 08:33)
- M1, idle plate beat: `PL = [(0,0),(30,0),(35,13),(45,13),(60,0),(120,0)]`: a 5-frame rise, a 10-frame hold at 13 deg and a 15-frame settle.
  - Events moved to match: settle1 at f35 (top of the lift, 0.292) and settle2 at f60 (the landing, 0.5). They were f40 / f50.
- Per clip:
  - Idle: chest vs spine 4.45, neck 3.94, pitch-up 3.62, max swing 4.0, loop closed, foot drift 0.
  - Walk: chest vs spine 4.61, slide 0, foot_z_var 0.
  - Roar: neck 7.69, jaw 26, pitch-up 24.08.
  - Act: chest vs spine 4.39, neck 5.44.
  - collision_free true; ground 0.002; tris 7,728.
- M2: per the lead's ruling, the stepped tag-page preview counts. `ANIM_REFS.md` ("Idle reference, per-clip round 4") lists the tag page (`/tags/subtle`), the card ("Kung Fu Panda"), the stepped times (9.5-16.0 s, every 0.5 s) and the key poses. The head drops with the shoulders rising at 10.0-10.5, 11.5-12.0, 13.0-13.5 and 15.0-15.5 s; the head lifts at 11.0, 12.5 and 14.0 s; the up-beats are short and the hunched holds long.
- Sheets: `_beats_f85r5_idle_side.png`, `_tq.png` and `_game.png` (f0-120 every 10 frames, plus f35/45/55/65; 08:33, file 08:33).
