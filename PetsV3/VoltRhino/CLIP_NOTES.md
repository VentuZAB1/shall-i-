# Volt Rhino - clip notes (clip gate, 2026-10-27)

References: `ANIM_REFS.md`: the Muybridge "Walking bison" plate and plate 733 "Elephant walking", both read frame by frame,
plus 1014 refs #3, #5, #6 and #9. No animationreference.org clip could be played.

| clip | frames | loop | events (frame) | what it is |
|---|---|---|---|---|
| idle | 120 | yes | `stamp` f46, `flick` f90 | horn tilt: one slow weight shift, head and neck yaw ±6 (the horn tilts side to side, one cycle), the left foreleg lifts 0.03 and stamps down (f30-46), ear twitches, one tail flick |
| walk | 40 | yes | - | heavy lateral-sequence walk, duty 0.70, body sunk 0.022, plus a 0.014 sink per step, ±2 deg roll, head low and dipping on front contacts, tail lags. Stride 0.343 |
| roar | 60 | no | `bellow1` f20, `bellow2` f28, `bellow3` f36 | BELLOW: tuck f0-6; head and neck up 16 by f16, snout forward, the neck reaching forward; the jaw opens late; three pulses (jaw 19 deg + flank pump); slower return f40-60 |
| act_horntap | 100 | no | `tap1` f30, `tap2` f42, `tap3` f54, `snap` f60, `charge` f70 | LIGHTNING TAPS: the head drives down at the throat (chest 2 + neck 6 + head 62), horn forward and the snout clear; three taps (a cocked lift, then a 2-3 f strike, tip to the snow); the head snaps up to horn-to-the-sky in 6 f (f56-62); hold while the inlays flash; slow return |

## VFX anchor bones (no mesh)
`FX_BoltTrail` [Horn_Tip], `FX_ChargeGlow` [Horn_Base], `FX_BoltSpark_L` [Shoulder_L], `FX_BoltSpark_R` [Shoulder_R], `FX_DustTap` [Foot_FL],
`FX_BellowRing` [Mouth].

## Checks (headless_full step 1 + `_scratch/limits.py`)
- **Collisions:** `collision_free: true`, step 1, all 4 clips.
- **ground_min_z:** idle 0.0, walk -0.002, roar 0.0, act -0.002 at f30 (the horn tip on the snow at tap1; the snout stays
  ~0.06 above the snow).
- **Audit:** linear 0; loops closed; walk slide 0.0; idle foot drift 0 (FR, BL, BR planted; FL does the stamp).
- **Pose limits:**

  | clip | neck max | chest vs spine | head + neck pitch-up | max adjacent-frame swing |
  |---|---|---|---|---|
  | idle | 2.1 | 0.7 | 0.4 | 27.5 (Tail3 flick) |
  | walk | 2.5 | 2.1 | 0.6 | 6.0 |
  | roar | 3.5 | 1.0 | 16.0 | 4.9 |
  | act_horntap | 6.0 | 2.0 | 16.0 | 23.2 (the snap) |

## Deviation from the plan (act_horntap)
- The plan says "pitch down 25 deg". With our horn (it curves UP from the nose), a 25 deg dip leaves the tip ~0.5 above the
  snow, and any dip under ~70 deg puts the snout into the snow before the horn.
- So the head drives down ~70 deg in total at the throat: chest 2, neck 6 (under the 8 limit), head 62. This is the pose of
  a bull dropping its horns. The horn tip is the only ground contact (tip -0.002, snout +0.06).
- The plan's limits hold: no pitch-up limit applies to a pitch-DOWN, and the legs stay planted.

## Changes made for the clips
- **Model, round-2 MUST fixes:**
  - Horn growth rings now 0.0015 proud (flush bands); the root collar is kept.
  - Brow sunk 0.010 into the skull.
  - One tapered elbow/knee fold wedge on the outer face of each leg; the front shin gaiter is removed.
  - Saddle rear edge f 0.22 → 0.06.
  - StormWyvern added to the 64/128 icon strips.
- **Model, round-2 NICE:**
  - Horn zig sunk (about 0.006 shows).
  - A lime tip band on the horn (t 0.84-0.90) for the game camera.
  - Rump plate rear edge tapered (f -0.02 → 0.06).
- **Model, for the clips:**
  - The head loft's rear station moved y -0.92 → -0.975 and the body loft's front station -0.98 → -0.94, so the back of
    the skull no longer sits inside the chest front. Both are hidden inside the neck.
  - The head's pitch-up is paired with the neck reaching forward (`neck_lift`).
- **Tris:** 12,284. Height 1.57 (HEIGHT 8.5).
- **Shares after the fixes (side / game):**
  - IRON_D 44.8 / 66.5
  - IRON 36.6 / 23.7
  - PALE 8.2 / 0.8
  - VOLT 3.8 / 3.1

## Round 3 (clip review 3, 2026-10-27)
Every number below comes from `_scratch/verify.json`, one saved run of `_scratch/verify.py`. The step-1 JSON is in
`_scratch/full_step1.txt` and the measured footfalls are in `_scratch/footfalls.txt`.

### MUST 2: the brace
- At each strike (f30, f42, f54) the Spine drops 0.024 and pitches +1.5, and the Chest pitches 3.8 relative to the spine.
  The chest's lowest point goes 0.591 → 0.528. The neck holds the head (Neck loc +0.08 z), so the horn geometry is
  unchanged.
- The front knees fold **+29.8 deg** at the strikes and +6.7 deg on the approach (f22-27). This is the interior knee angle
  vs rest; Shin_FL and Shin_FR are the same.
- The 4-8 deg and 0.1 asks cannot both hold on this pillar leg. It stands at 98 % of its length at rest, so +8 deg of fold
  is only a 0.012 drop. I kept the chest drop, because that is what reads as a charge (see `_beats_act_side` f30 / f42 / f54).
- **Horn tip (Horn_Tip bone z):** tap1 f30 0.013, tap2 f42 0.024, tap3 f54 0.013. The horn mesh bottoms at -0.002 at
  tap1 / tap3 and 0.008 at tap2. The snout stays 0.043-0.045 above the snow.
- **ground_min_z** act -0.002; collision_free true (step 1).
- **NICE 2:** tap 2 lands a touch shallower, then drags the horn sideways (head yaw 6 deg, tip x 0 → 0.12, f42-46) while
  staying on the snow (0.008 → 0.030).

### MUST 3
- **(a) Beats:** `renders/_beats_act_side.png` and `_tq.png` now hold f16, 22, 27, 30, 39, 42, 46, 54, 58, 62, 86, 100.
- **(b) End at rest** (largest per-bone rotation): roar end vs start 0.0 and vs the bind pose 0.0; act 0.0 and 0.0.
- **(c) Chest vs spine:** this is the Chest bone's LOCAL rotation, and the Chest is parented to the Spine, so it is the
  chest-vs-spine angle. Rhino maxima: idle 0.68, walk 2.09, roar 1.0, act 3.8 (the brace).
  - The 4.4 in my gate message was the maximum across all three pets (the Yeti's act_skid), not the Rhino.
- **(d) Jaw:** the kit has no joint limits, so I defined one. `JAW_MAX = 14` is the opening the mouth covers.
  - A new MOUTH-coloured interior block rides the Jaw, hidden inside the snout when closed. With it, a 14 deg opening
    shows a dark mouth instead of the background. At 19 deg the old model showed see-through (`renders/_jaw_roar_sheet.png`).
  - The bellow pulses are now 14 deg (was 19), with 9 deg between pulses and an 11 deg hold. Jaw max: roar 14.0,
    act 8.0, idle 2.0, walk 1.5.

### MUST 4: the event convention
- Events are clip-length fractions, `round(f / n, 3)`. That is the same convention as approved, live pets: ThunderRex's
  exported Lua has `roar = {peak = 0.381, ...}`.
- The runtime (`ROBLOX PLAYBOOK/slingshot-code/ReplicatedStorage/CreatureAnimator.lua`, `_events`) fires at
  `t = frac * len` seconds. Loops use the phase, so it also covers the walk. The VFX fires on the keyed frame.

### Walk fix found while verifying
- `cm.quad_walk(gait="walk")` measured as touch-downs BL f0, FR f10, BR f20, FL f30. That is a DIAGONAL sequence, not the
  lateral one the bison / elephant plates show.
- The walk now sets its own offsets (BL 0, FL 0.75, BR 0.5, FR 0.25). Measured: BL f0, FL f10, BR f20, FR f30 = LH, LF,
  RH, RF.
- The body roll is re-phased toward the planted side, and the head dip now lands 2 f after each front touch-down.
  Slide 0.0; loop closed.

### NICE
- **1:** the idle tail flick is spread over 82-107. Its largest one-frame swing is now 15.1 deg (was 27.5).
- **3:** the bolt events fire on the tap frames (tap1-3).
- **4:** the jaw opens late (from f16) and the pale chin reads at the pulses.

### Raw collisions before the throat-hinge exemption
- The throat hinge has been in `joints()` since the model gate. Before the exemption, step 1:
  - idle: Head-Chest 25, Jaw-Chest 10, Jaw-Neck 26
  - walk: 15, 9, 8
  - roar: 35, 6, 27
  - act: 51, 62, 58
- With the hinge the count is 0, so every crossing lies within r 0.26 of the throat segment (inside the neck).

### References
- MUST 1 is pending. The central animationreference.org pull (`_review/ANIM_REFERENCES_1027.md`) has not landed yet, and
  per the lead I did not retry the browser.

### References round (2026-10-27)
The central `ANIM_REFERENCES_1027.md` refs are cited in `ANIM_REFS.md` (the "Central references" section), with the timing changes they caused. After the changes the checks were re-run: step-1 collision_free true; all limits and end-at-rest unchanged (`_scratch/verify.json`, `_scratch/full_step1.txt`).

## Round 4 (2026-10-28)
- **Renders from the FINAL file**, rendered 2026-10-28 00:00. The time is in the file names:
  - `renders/_beats_rw_final_1028_0000_side.png` / `_tq.png`: walk f0 / 10 / 20 / 30 (lateral touch-downs); roar f6 / 16 /
    20 / 28 / 36 / 50.
  - `renders/_beats_act_final_1028_0000_side.png` / `_tq.png`: act f16, 22, 27, 30, 39, 42, 46, 54, 58, 62, 86, 100.
  - `renders/_final_jaw_throat.png`: the roar f28 mouth (side, below) and the act f42 throat (side, below), 10-27 23:59 /
    10-28 00:00. No skin poke-through at 70 deg of pitch.
- **Feet at the taps:** Foot_FL and Foot_FR stay at their rest ankle points (±0.25, -0.53, 0.22), and the foot soles stay at
  z 0.000 at f30, f42 and f54 (`_scratch/feet_taps.txt`).
- **NICE 1 (open jaw):** the pale lower jaw tapers to the chin (top 0.78 / 0.62) and the mouth interior tapers inward
  (0.70 / 0.75). It reads as a mouth, not a plank. Step-1 re-run: collision_free true; ground unchanged.
- **References:** the per-animation table and the W0 source frames are in `ANIM_REFS.md`; plan section 10 is filled.

## Final 8.5 gate round (2026-10-28, `_review/VoltRhino_final85.md`)
Numbers: `_scratch/verify.json` (01:38), step 1 + export `_scratch/export_result_f85.txt` (01:37).
- **C1 idle reference:** `/tags/elephants` "Video by projectarcheology" (an adult elephant standing with its calf,
  stepped from the tag page's preview video, no clip open used). The row with frames and the no-fit note for
  `/tags/animals` and `/tags/creature-animation` is in `ANIM_REFS.md` and plan section 10. What it changed: the idle
  weight shift now moves OFF the lifting foreleg (phase 0 -> 0.433; it peaks on the right at f38, mid-lift of FL).
  Before, the body leaned onto the lifting leg.
- **C2 idle renders:** `renders/_beats_f85_ir_tq.png` / `_side.png` (01:36): idle f0 / 30 / 38 / 46 (stamp) / 60 / 70 /
  72 (snort) / 90 (flick) / 120, roar f0 / 6 / 16 / 18 / 20 / 22 / 28 / 36 / 50 / 60. FR, BL and BR stay planted
  (idle_foot_drift 0).
- **C3 act strikes:** each strike holds 2 frames on the snow (f30-31, f42-43, f54-55) and rebounds 3 frames after the hit
  (f33, f45, f57: head 4 deg up, chest back to 2.0, spine 0.010 down instead of 0.024, the brace releases). Tap3 strikes
  2.5 deg deeper (head 62.2) with the neck reaching 0.045 forward and lifting 0.039, so the tip still only touches and the
  cheek clears the brisket (without the reach: Head|Chest 18, Jaw|Chest 11 at f54). Tap2 stays shallower and drags the
  horn sideways during its hold (yaw 0 -> 3), flicking off at the rebound (yaw 6). Horn_Tip z on the hold frames: 0.0078
  / 0.0078 (tap1), 0.0076 / 0.0079 (tap2), 0.0035 / 0.0035 (tap3). Feet stay at their rest points. Sheets:
  `renders/_beats_f85_wa_tq.png` / `_side.png` (walk f0 / 10 / 20 / 30, act f22 to f100 incl. every hold and rebound).
- **N3 roar pump:** on each bellow (f20 / f28 / f36) the neck lifts 2 deg more (3.5 -> 5.5) while the head tips 2 deg
  back (-11 -> -9.5), eased over f-2 .. f+2. Head + neck stays 15 (+ chest 1 = 16 pitch-up); the snout stays forward.
- **T3 idle snort:** f70-73, head 2 deg up and jaw +2, then back (one beat, no repeat).
- **Limits (verify.json):** neck max idle 2.06 / walk 2.48 / roar 5.5 / act 6.0 (<= 8); chest vs spine 0.72 / 2.09 / 1.0 /
  3.8 (<= 5); head pitch-up roar 16.0, act 16.0 (<= 30); max one-frame swing 30.8 (FX_BoltTrail at the snap); one-shots
  end at rest 0.0.
- **Step 1 (with export):** collision_free true; ground_min_z idle 0.000, walk -0.002, roar 0.000, act -0.008; linear 0;
  loops closed; walk slide 0; idle foot drift 0.
- Events unchanged: idle stamp 0.383, flick 0.75; roar bellow1-3 0.333 / 0.467 / 0.6; act tap1-3 0.3 / 0.42 / 0.54,
  snap 0.6, charge 0.7.

## Final gate round 2 (2026-10-28)
Numbers: `_scratch/verify.json` (04:06), step 1 + export `_scratch/export_result_f85r2.txt` (04:09).
- **MC1:** idle Leg_FL lift 0.032 -> 0.060 (f30-46 window, stamp event f46 = 0.383 unchanged); the lift peaks at f38.
  `renders/_idle_stamp.png` (f30 / f38 / f46 side) and `beat_f85_ir_side_idle_030/038/046.png`. FR, BL, BR planted, idle
  foot drift 0, idle ground 0.000.
- **T-c:** snort 2 -> 4 deg on head and jaw (f70-73). **T-d:** rebounds 4 -> 6 deg up with a 1.5 deg spine recoil (spine
  pitch +1.5 at the strike -> -1.5 at f33 / f45 / f57). **T-e:** roar neck pump 3 deg (neck -3.5 -> -6.5, head -11 -> -8.5,
  so head + neck stays 15 and pitch-up stays 16.0).
- **Limits:** neck max idle 2.06 / walk 2.48 / roar 6.5 / act 6.0; chest vs spine max 3.8; pitch-up 16.0; max one-frame
  swing 26.7 (FX_BoltTrail, snap); end at rest 0.0. Horn_Tip on the hold frames 0.0078 / 0.0078 / 0.0076 / 0.0079 /
  0.0035 / 0.0035.
- **Step 1:** collision_free true; ground idle 0.000, walk -0.002, roar 0.000, act -0.008; linear 0; loops closed; slide 0;
  idle foot drift 0. Sheets `renders/_beats_f85_ir_*` (idle, roar), `_beats_f85_wa_*` (walk, act incl. every hold and
  rebound), 04:07.

## Final gate round 3 (2026-10-28 05:09, exported 05:11)
- MUST 3, idle stamp:
  - The FL lift goes from 0.060 to 0.120 (f30-46, stamp event f46 = 0.383). Foot_FL is at z 0.22 / 0.34 / 0.22 at f30 / f38 / f46.
  - The kit tips a lifted foot 35 deg toe-down at 0.12, which would have kept the sole's lowest point at only 0.045. `plant()` now passes `toe = 3 * sin(pi u)`, so the sole's lowest point is 0.110 at f38 (probe_feet).
  - In `beat_f85r3_idle_side_idle_038` (360 px) the near sole bottom is at y 259-260 against 271-272 at f30, so it is 11-12 px higher.
  - FR, BL and BR stay planted (idle_foot_drift 0). collision_free true; ground idle -0.0.
- MUST 4, process: `probe_feet.py` was re-run on the final save (05:09:54) at 05:11:31, log in `_scratch/feet_taps_f85r3.txt`. The act soles are 0.000 at f30/42/54, and the Horn_Tip is at 0.008/0.008/0.004.
- 9+ snort: the head toss is now 6 deg up at f71-72 (was 4), with the jaw at 4. It settles past rest at f76 (1.5 deg nose-down) and is back at f78. Idle head pitch-up is 5.46 at f71.

## Final gate round 4 polish (2026-10-28 06:08, exported 06:10)
- T5 snort: the head toss is 8 deg (was 6) at f71-72, settling at f76. Idle pitch-up 7.47 @ f71.
- T6 roar pump: 5 deg.
  - Keys: neck base -2.8 (f16, f24, f32, f40), in-between -5.3 (f18/22/26/30/34/38), pulse -7.8 (f20, f28, f36). Head counters each step at -11.7 / -9.2 / -7.2, so head + neck = 14.5 / 14.5 / 15.0.
  - The suggested pulse -8.5 would have broken the neck limit 8, so it peaks at -7.8 (neck_max 7.8 @ f20). Pitch-up is still 16.0.
- T7 act snap: spread over f57-64, eased 10 / 13 / 14 / 13 / 9 / 6 / 2 deg per frame. Horn to the sky at f64 (was f62); the snap event at f60 and charge at f70 are unchanged. Act max swing 26.7 (FX_BoltTrail f58) -> 16.8 (Head f60).
- f54 check: the snout (head mesh without the horn) is 0.048 above the snow at f54 and f55, the horn tip 0.004. The nose cap sits in front of the forelegs, clear of the brisket (`_evidence_r4`, `beat_f85r4_wa_*_act_horntap_054`). collision_free true.
- Gates: tris 14,532; ground idle -0.0 / walk -0.002 / roar -0.0 / act -0.008; slide 0; idle foot drift 0; chest vs spine 0.72 / 2.09 / 1.0 / 3.8.
- `probe_feet` was re-run on the 06:08:57 save (`_scratch/feet_taps_f85r4.txt`): soles 0.000 on the taps; the FL sole lift is unchanged.

## Final gate round 5 (2026-10-28 08:25, exported 08:31)
- MUST 1, roar mouth: the mouth interior's front end is now `top=(0.45, 0.76)`. JAW_MAX is still 14.
  - The asked-for (0.45, 0.60) gave 23 px and (0.45, 0.68) gave 25 px with the reviewer's test (R > G+25 and R > B+20), so the front was made a little deeper.
  - 360 px side frame: 33 px at f20/f28/f36 (was 13). The tq frame: 51 px (target 40).
  - Closed f0: 0 px in side and tq. No maroon below the snout in `closeb_cbelow` or `under.png` (0 px).
- MUST 2, act from below: `pose_under.py` renders the posed frames with the ground hidden, at f42 and f54, under + underside (`_under_act_r5.png`).
  - The pale brisket is unbroken behind the lowered head. No head skin shows through it.
  - The raw Head|Chest overlap without hinges sits inside the throat hinge capsule, so no head lift was needed. The horn tip stays at 0.0076 / 0.0035.
- MUST 3, walk reference: `ANIM_REFS.md` now cites a site clip, `/tags/elephants` "Video by projectarcheology". It was stepped from the tag page's preview at 10.0-11.4 s in 0.2 s steps, with no clip open. The other tags checked are listed there. Plan section 10 is updated.
- Per clip:
  - Idle: chest vs spine 0.72, neck 2.06, pitch-up 7.47.
  - Walk: chest vs spine 2.09, neck 2.48, slide 0, foot_z_var 0.
  - Roar: neck 7.8, jaw 14, pitch-up 16.
  - Act: chest vs spine 3.8, neck 6.0, max swing 16.8.
  - collision_free true; ground -0.008 or higher; tris 14,532.
- Probe log: `_scratch/feet_taps_f85r5.txt` (run on the 08:25 save).
- Sheets: `_beats_f85r5_wr_side.png` and `_tq.png` (walk + roar), `_under_act_r5.png`, `_chin_sheet.png`. The icon and strips are re-made.

## Final gate round 6 verification (2026-10-28 09:0x; no file change, the ship file is still the 08:25 save / 08:31 export)
- The act hold frames (f30/31, f42/43, f54/55) and the idle snort frames (f68, f70-74, f76) were re-rendered from the final save in game, side and tq: `_beats_f85r6_check_game.png`, `_side.png` and `_tq.png`, 360 px.
- With the reviewer's test (R > G+25 and R > B+20), the mouth interior shows 0 px in all 39 frames. The wider front (top=(0.45, 0.76)) stays hidden with the jaw closed, during the taps and during the snort (jaw up to about 6 deg).
