# Frostcrown Dragon - clip notes (clip round 3 after review 5, builder D, 2026-10-28)

Code: `pets/FrostcrownDragon.py` (from "animation (clip round 1)" down). References: `FrostcrownDragon/ANIM_REFS.md`
(site tags -> Sakugabooru: #260630 heron landing / takeoff / head press, #236985 Earthsea dragons, #174482 Maid Dragon S
NCOP, #256671 The Cat Returns walk, W0 #174333; banshee #8; Sea Beasts #3).

## Review 8 (clip round 6): cheap 9+
- **Act finish snap: +10** wing-arm lift at f60 / f64 (was +6). Collision-free; act largest step 13.5.
- **Deeper fly stroke: not done.** The takeoff hands over to fly f0, and the fly passes at 8.6, so I left the stroke as
  it is.
- Step 1 on the final build: collision-free, linear 0, loops closed, walk slide 0; ground -0.005 / walk -0.010 / fly
  +0.089; Neck 7.5, chest vs spine 3.0; rest delta 0.00 (roar, act, land); seam takeoff f28 = fly f0, 0.00.
- All 14 sheets re-rendered from `_scratch/FrostcrownDragon_r9final.py.txt` with labels.

## Review 7 (clip round 5): evidence from the round-8 build
- No key changes. All 14 sheets are re-rendered from `_scratch/FrostcrownDragon_r8final.py.txt` with frame / time
  labels and a render-time footer: `renders/_pose_<tq|game>_<clip>_sheet.png`.
- Step 1: collision-free, linear 0, loops closed, walk slide 0. Ground -0.005 (walk -0.010), fly +0.089. Largest
  step 25.9 (takeoff f8, FX bone). Neck 7.5, chest vs spine 3.0.
- Rest delta: roar, act, land 0.00. Seam: takeoff f28 vs fly f0 0.00.
- Min-z table (`_scratch/minz_r8.txt`), lowest vertex, Foot_FL in every case:

  | frame | takeoff f26 | takeoff f27 | takeoff f28 | fly f0 | fly f1 | fly f27 |
  |---|---|---|---|---|---|---|
  | min z | 0.0894 | 0.0899 | 0.0940 | 0.0940 | 0.1012 | 0.0899 |

## Review 6 fixes (clip round 4)
- **5. Act finish snap:** the wing-arm snap at f60 / f64 is **+6** (was +4). The tip still flicks -6.
- **4. Evidence from the final build:** every clip was re-rendered in the tq and game views from
  `_scratch/FrostcrownDragon_r7final.py.txt` (= `pets/FrostcrownDragon.py`). Each frame is labelled with the frame
  and the time, and each sheet has a render-time footer: `renders/_pose_<tq|game>_<clip>_sheet.png`.
  - act_stillfreeze: f0 / 16 / 44 / 50 / 58 / 60 / 62 / 64 / 66 / 80 / 110
  - takeoff: f0 / 8 / 11 / 12 / 14 / 19 / 27 / 28
  - idle: f0 / 32 / 60 / 80 / 120
- **Re-run checks on the final build:**
  - Rest delta, last frame vs the ground rest pose (`_scratch/rest_delta.py`): roar 0.00, act 0.00, land 0.00.
  - Seam: takeoff f28 vs fly f0 = **0.00 deg / 0.000**.
  - Step 1: collision-free, linear 0, loops closed, walk slide 0. Ground -0.005 / walk -0.010 / fly +0.089.
  - Largest step 25.9 (takeoff f8, FX bone). Neck 7.5, Neck2 7.0, chest vs spine 3.0. Tris 9,632.

## Review 5 fixes (clip round 3, 2026-10-28)
- **C1 takeoff -> fly handoff (verified, then rebuilt):** f20-28 of the takeoff now run the flight cycle at the FLY
  tempo (`fly_pose` + `fly_legs` at phase 1 + (f - 28) / 28), so the last frame IS fly f0. Lowest vertex z
  (`_scratch/minz.py`, every vertex, Foot_FL in all cases):
  | frame | takeoff f26 | takeoff f27 | takeoff f28 | fly f0 | fly f1 | fly f27 |
  |---|---|---|---|---|---|---|
  | min z | 0.0894 | 0.0899 | **0.0940** | **0.0940** | 0.1012 | 0.0899 |
  Gap at the switch: **0.000** (takeoff f27 = fly f27 and takeoff f28 = fly f0). Rest delta takeoff f28 vs fly f0: 0.
  (The fly clip's lowest point is 0.089 at f26; the 0.098 in review 5 was an older fly pose.)
- **TO 9+ takeoff downbeat:** the wings rise higher at the gather (f10 up 40 -> 44) and sweep further down (f14 -24 ->
  -30, f15 -36 -> -42): an 86 deg downbeat over 5 frames, the launch still at f11. Largest takeoff step 25.9 deg (FX
  bone), wing bones <= 24.
- **TO 9+ act finish beat:** two small wing snaps as the frost lands: SPREAD f58 -> snap f60 -> SPREAD f62 -> snap f64
  -> SPREAD f66 (snap = up +4, tip -6), then HALF f70, FOLD f80, rest f80-110. `renders/_pose_sheet.png` (act f44 /
  58 / 60 / 62 / 64 / 110).
- **TO 9+ idle fin tick:** 2 -> **3 deg** (f32, f92), all seven fins together.
- **TO 9+ HTTYD:** tried again via `/tags/how-to-train-your-dragon`. Its items are YouTube clips or site-hosted HLS
  streams (no Sakugabooru source). Opening the site item "How to Train Your Dragon" (`/video/PvGMeNA9bK8xXXQRNYAC`)
  froze the tab again (no script or screenshot returned), so I closed it and read no frames. Per the lead's rule, it is
  not used.

## Review 4 fixes (clip round 2)
- **MUST 2, the act peak:** the wings flare FOLD -> HALF (f38) -> SPREAD (f44), HOLD SPREAD f44-58 through the frost
  burst (`frost` f50), then HALF f70, FOLD f80. The fins rise to **30**. The f44-58 frames show the wings open, the
  fins up and the head pressed together (`renders/_pose_tq_act_stillfreeze_sheet.png`, f44 / f50 / f58).
  - Collision fix: Fin_2 cut Neck2 at the 30 deg fin rise, so the two neck fins now move at 0.42 of the group angle
    (was 0.5, max 12.6 deg).
- **N1:** the head press is now Neck 7 / Neck2 7 / Head 11 (total 25).
- **N2:** the takeoff launch has in-betweens (f12, f14, f15; the airborne key moved f17 -> f19). Feet are planted to
  f12. The launch step is 24.6 deg (was 42.4), and it is no longer on the wing bone.
- **MUST 3, rest frames:** the end frames are in the sheets: roar f66, act f110, land f27 + f28, takeoff f27 + f28.
  Rest delta (`_scratch/rest_delta.py`, max per-bone rotation of the last frame against the ground rest pose = roar
  f0 = `rest_keys`):
  - roar f66 **0.00 deg**, act_stillfreeze f110 **0.00 deg**, land f28 **0.00 deg**, all exact.
  - Takeoff ends in the FLIGHT cycle (`fly_pose` phase 0.2 = fly f5.6, legs keyed), not on the ground.
  - Idle f0 differs from the rest pose only by the idle's own tail sway phase (Tail3 10.4 deg). That is a loop, not an
    end frame.

## Step 1 (`_tools/headless_full.py -- FrostcrownDragon - 1` and `_tools/headless_clips.py`, every frame; round 3)
- collision_free **true**. Audit linear 0 on every clip. Loops are closed (idle / walk / fly: loop_pos 0, loop_rot 0).
  Walk slide 0.0, foot_z_var 0.0, idle_foot_drift 0.0, stride 0.484. Tris 9,288.
- ground_min_z: idle -0.005, walk -0.010, takeoff -0.005, land -0.005, roar -0.005, act_stillfreeze -0.005, fly +0.089.
- Largest per-frame bone step (`BlizzardRoc/_scratch/step_check.py`): 25.9 deg (takeoff f8, FX_FrostTrail). Every
  other clip is <= 17.8. Neck max 7.5, Neck2 max 7.0. Chest vs Spine max 3.0. Head + neck pitch-up max 15 (roar).
- Rest delta (`_scratch/rest_delta.py`, last frame vs roar f0): roar f66 0.00, act f110 0.00, land f28 0.00; takeoff
  f28 = fly f0 (0.00).

## Clips (30 fps)
| clip | frames | loop | events | what it does |
|---|---|---|---|---|
| idle | 120 | yes | `frostpuff` f80 | FROST HUM: slow breath. The wings half-fold and reopen (FOLD -> HALF f14-30, back by f60). The seven fins tick 3 deg TOGETHER (f32, f92). Slow head sway (yaw +-8, long holds). A jaw puff at f80 (frost at the Mouth). Tail sway. |
| walk | 40 | yes | - | Lateral-sequence quad walk (stride half 0.15, lift 0.08). Wings folded with a 2 deg bob. The head is held steady against the body yaw / roll. Tail sway. |
| fly | 28 | yes | - | D3 stroke: top 40 / bottom -24, the outer wing folds on the upstroke. The body rises on the downstroke (+-0.04) at pitch 10. The head is level, the tail streams with a small lagging wave, and the fins lie back 4. D2 legs: front paws tucked, hind legs trailing with a small pump. |
| takeoff | 28 | no | `launch` f11 | H1 + E1: crouch (-0.08) while the wings unfold to the stroke top (f0-10). LAUNCH on the first downstroke plus the hind-leg push, split by in-betweens f12-15. The legs tuck; f20-28 run the flight cycle at its own tempo and end exactly on fly f0. |
| land | 28 | no | `touch` f16 | H1 + E1: flare (pitch -10) with a braking beat, legs reach. TOUCH f16, absorb (-0.05), the wings fold through a half fold to FOLD. Ends exactly at rest. |
| roar | 66 | no | `roar` f24 | CRYSTAL-CHIME ROAR: the head lifts 15 and the wings spread to SPREAD (f0-14). The jaw opens and lags the head (D5). The seven fins stand up 15 together. Hold f28-52: the fins buzz +-2 as one group, the jaw rumbles, the horns hum +-1. Close f52-66. |
| act_stillfreeze | 110 | no | `click` f16, `frost` f50 | SIGNATURE, ABSOLUTE STILLNESS (in place): inhale and go still (f0-14). All seven fins rise 30 together with one frost click (f16). The head presses toward the ice (Neck 7 / Neck2 7 / Head 11, body dips 0.05) while the jaw opens (H1 + W0). The wings flare open and HOLD SPREAD f44-58 through the frost mist cone (f50), which is the peak frame. Finish beat: two wing snaps f60 / f64 as the frost lands. Then HALF f70, FOLD f80, as the fins fall together and the head lifts. Exact rest pose f80-110. |

## Decisions / deviations
- **Fins move as ONE group** (no stagger, no tail-to-neck wave): same frames and the same angle on all seven. The two
  neck fins (Fin_1, Fin_2) move at half amplitude so they never lean into the skull or the upper neck.
- **Fin_2 re-seated** for the clips: it now sits on the neck root top (`FIN_PARENTS[1] = "Neck"`, base y -0.56,
  z 1.27, h 0.46). The Neck saddle starts at 40 % of the bone. Its root capsule is 0.16 long. Before this, Fin_2
  under Neck2 cut the neck when the head pressed down.
- **Wing capsules** in `joints()`: the root capsule runs S -> BB + 30 % (r 0.17), plus an arm-root capsule (r 0.13).
  These are hinge slivers at the shoulder during the fold <-> open transitions. All FOLD / HALF / SPREAD / takeoff /
  land paths are 0 hits (`_tools/path_test.py`).
- The takeoff's 42.4 deg step is the launch snap on the hand bone (under the 60 deg limit). It is the D1 push beat.
- roar: the head lifts 15 (D5), well inside the 30 limit, so the crown stays readable from the game camera.

## Renders
`renders/_pose_tq_<clip>_sheet.png` for all seven clips (frames labelled, including the end frames: idle f120,
walk f40, takeoff f27 / f28, land f27 / f28, roar f66, act f110).
