# Bramble Badger - FINAL 8.5 GATE, ROUND 4 (2026-10-28) - Model PASS, Clips FIX

**Model: 8.6/10 - PASS. Clips: 8.4/10 - FIX.**

Overall: FIX. The clips are under the 8.5 floor. The model passes. The clip MUSTs are M1 (the breath does not lift the chest as built) and M2 (the act, roar and walk renders predate the T1 hump).

## What I looked at

- Brief: `_review/GLACIER_REVIEWER_BRIEF.md`. Round 3: `_review/BrambleBadger_final85_r3.md`. Builder notes: `BrambleBadger/CLIP_NOTES.md` (round 3), `BrambleBadger/MODEL_NOTES.md` (round 5). Numbers: `_scratch/fullcheck.json`, `_scratch/fc_r3.txt`, `_scratch/clipmetrics.json`, `_scratch/cm_r3.log`, `_scratch/export.log`. Vault rules: `Creature Style.md`, `Model Review Checklist.md`, `Creature Animation.md`. Refs: `BrambleBadger/ANIM_REFS.md`.
- Code: `pets/BrambleBadger.py` is byte-identical to `_scratch/BrambleBadger_f85r3.py` (mtime 01:49). Lines checked: THORNS 36-37, mantle 135, LIFT 323, TWITCH 327, idle keys 332-340. The rig's `k.key` convention is in `_tools/petkit_backup_20261014_prekeyquote.py` (rot = pitch about +X, nose down; yaw about +Z; roll about +Y). `bz()` and the DZ shift apply the same offset to joints and blocks, so the relative geometry holds.
- Images, all opened: `renders/_idle_2x_r3.png`; `renders/_idle_close_r3.png`; `_scratch/r3/_neck_check.png`; `renders/_model_sheet.png`; `renders/_close_sheet.png`; `renders/_icons_strip_64.png` and `_128.png`; `renders/game_view.png`; `renders/pclose_side_idle_00.png` and `_40.png`; `renders/pclose_game_idle_00/36/40/70.png`; `renders/pclose_tq_idle_00/36/70.png`. I cropped and enlarged the crest, thorn-1 and mantle regions. The crops are in `C:\Users\ventu\AppData\Local\Temp\bb_r4\` (outside the project).
- Timestamps: `_pose_tq_sheet`, `pclose_side_act_burrow_*`, `pclose_side_roar_*`, `pclose_side_walk_*` and `pclose_tq_act/roar/walk_*` are all 01:28. That is before the T1 hump (pets file 01:49). Only the idle r3 renders (03:17-03:18) are current. The act, roar and walk visual checks are therefore not verified for T1.
- I did not run Blender. The breath numbers below come from the code formulas (`pk.wave` = sin in [-1, 1]) and were computed in a script.

## Breath arithmetic (the main finding)

- b(f) = sin(2*pi*3*f/120). b = 0 at f0, f40, f80, f120. b = +1 at f10, f50, f90. b = -1 at f30, f70, f110.
- Spine loc z = 0.014*b (line 332). Chest pitch = 1.8*b (line 333). Positive X pitch = nose down.
- Peak-to-peak vertical motion, with d held at 1:
  - rump (Spine only): 0.028 units (about 0.3 studs, using the builder's own 0.16 studs per 0.014 units);
  - mantle top (Chest): 0.011 units (about 0.12 studs). The Chest pitch takes about 0.017 units off the Spine lift at the shoulder;
  - head pivot (Chest child): about 0.001 units (no visible motion);
  - mantle against the Spine hull: 0.017 units of relative slip (about 0.2 studs) at each breath, because the shoulder blocks are on Chest and the back hull is on Spine.
- The CLIP_NOTES and brief check "chest top rises on `pclose_side_idle_00` against `_40`" is invalid. Both frames have b = 0, so the difference between them is the sniff pose, not breath.

## Round-3 items

| Item | Verdict | Evidence |
|---|---|---|
| MC1 breath (Spine 0.014*b, Chest 1.8*b) | FAIL (as built) | Code matches (lines 332-333). The numbers above show the Chest pitch cancels most of the Spine lift at the shoulders, the head does not move, and the shoulder blocks slide 0.2 studs against the back. The requested frame pair is breath-neutral. |
| MC2 sniff body roll (2.5*yw/8) | PARTIAL | Code matches (line 332). The term is a roll about +Y, the body axis (confirmed in `Rq`). Numbers pass: chest vs spine 2.8, 0 quaternion flips. Visually subtle: the shoulder top moves about 0.1 studs sideways; no change in the side camera (`pclose_side_idle_40` vs `_00`). |
| MC3 crest bristle (5.0*br, peak f70-78) | PASS | Code matches (line 339, `BRIS` peaks f70-78). In the game crest crop and the tq crop the front thorns stand more upright at f70 than at f0 or f36. No gap at the thorn bases in the crops at f70. |
| MC4 evidence | PARTIAL | Numbers pass: `collision_free` true with `{}`; `ground_min_z` -0.002 in all four clips; linear 0; idle loop closed (f120 vs f0 0.0); neck max 7.87 (limit 8); chest vs spine 2.8 idle (limit 5); head yaw 1.4 deg/f idle and 2.99 deg/f act (limit 3); 0 quaternion flips; tris 6,832 (cap 15k). The breath image pair is invalid (see above). |
| T1 shoulder hump (mantle 0.44 / 0.135, thorns 0.550 / 0.570) | PASS | Code matches (lines 36-37, 135, with taper (0.86, 0.66) and top_shift 0.050). Thorn 1 is seated in `_neck_check` at f0 and f40: its base sits on the mantle's front corner with no daylight under it. The neck block does not step up. The hump reads as shoulder mass in `game_view.png` and `_model_sheet.png`. Caveat: no act, roar or walk render exists since the change (M2). |
| T2 ear twitch (6 deg at f36, f52, f68) | PARTIAL | Code matches (TWITCH table, line 327; peaks exact at f36, f52, f68). But the ramp is 8 frames (f32-40), not the 6 frames in the brief. The ears sit at the back of the head in every camera, and no ear crop at those frames was supplied, so the beat is not visible in the evidence. |
| Idle body life (r3 checklist item 14) | PARTIAL | Improved from FAIL. The head drop and the crest bristle read. The breath does not lift the chest (M1). |
| Walk, roar, act (items 15-17) | PARTIAL | Numbers pass. Renders predate T1, so the hump's clearance over the head and neck in act f5-68 and roar is only checked by the collision test (M2). |
| Model checklist (items 1-10) | PASS | 64 px icon reads as a badger (white head with black bands, grey back, amber crest). Face close sheet shows slit eyes with amber accent and no glint. Game shares: GREY 48.0, MANTLE 10.2, BELLY_D 14.4, AMBER 16.9 (+0.4 hot). Tris 6,832. |

## Model: 8.6/10 - PASS

- Gains since round 3: the shoulder hump gives the front real mass, as the T1 brief asked. The silhouette reads at 64 px and at 128 px. Nothing floats in the views checked. The palette follows the plan.
- Why it is not 9: the mantle is a flat-topped pad, and its rear top corner steps against the grey back in `game_view.png` (see TO 9+ N5).

## Clips: 8.4/10 - FIX

- Gains since round 3: the crest bristle and the flicks are visible beats. Every numeric gate passes. The sniff now has a body response.
- Holding it at 8.4: the one idle beat the owner sees with no sniff (the breath) does not lift the chest, the head stays still, and the shoulder blocks slide against the back. The sniff roll and the ear twitch are still small. The act, roar and walk renders predate the T1 hump.

## New MUSTs (blocking 8.5)

**M1. Breath lifts the chest (fixes MC1).**
- Line 333: `k.key("Chest", f, rot=(1.0 * d + 1.8 * b, 0, 0))` becomes `k.key("Chest", f, rot=(1.0 * d, 0, 0))`. This removes the pitch that cancels the lift. The Chest-bone blocks then move with the Spine hull.
- Line 335: `k.key("Head", f, rot=(15.5 * d - 6.0 * lf, 0.70 * yw, -0.3 * yw))` becomes `k.key("Head", f, rot=(15.5 * d - 6.0 * lf + 2.0 * b, 0.70 * yw, -0.3 * yw))`. The 2.0 cancels the nose drop from the 0.014 Spine lift (the nose is about 0.37 units from the throat pivot). Keep line 332 (Spine loc `-0.010*d + 0.014*b`) unchanged.
- Measure, headless, after the change:
  - mantle-top world Z change between f50 (b +1) and f70 (b -1), both at d 1: at least 0.024 units (currently 0.011);
  - (mantle top) minus (Spine hull top at the shoulder): change of at most 0.002 units between those frames (currently 0.017);
  - snout world Z: with d, lf and yw held equal, the change between b +1 and b -1 is at most 0.003 units. Compute this by switching the breath term on and off in the rig. Do not compare f50 and f70 directly, because the lift term differs there;
  - lowest Head or Jaw world Z over f0-f120: at least 0.000 (no nose in the floor);
  - chest vs spine at most 5 (it will be about 1.0), head pitch-up at most 30, collision_free true, ground_min_z at least -0.02, idle loop closed.
- Evidence: 2x side crops of f50 and f70 at the same framing, showing the rump, the shoulder top, the nose and the ground line.

**M2. Fresh renders after T1 (act, roar and walk).** The T1 hump (01:49) postdates every act, roar and walk pose sheet (01:28). After M1, re-render side and tq sheets for act f5, f20, f44, f68; roar f12, f30, f59; walk f0, f8. Report the minimum clearance between the Head, Jaw or Neck blocks and the MANTLE block over act f5-68 and roar f0-45. It must be at least 0.01 units, with no visible contact. Replace the 01:28 sheets.

## TO 9+ (polish, after the MUSTs)

- **N1. Nose lift to match the reference.** `ANIM_REFS.md` A says the nose lifts 10-15 deg between sweeps. The build uses 6 deg. Line 335: `-6.0 * lf` becomes `-10.0 * lf`. The lift only happens at d 1, so the head stays below its rest elevation and the pitch-up limit is unaffected.
- **N2. Ear twitch you can see.** The brief's 6 frames: make TWITCH a 6-frame triangle (for example (33, 0), (36, 1), (39, 0), and the same at f49-55 and f65-71), at 8 deg instead of 6.
- **N3. Sniff roll.** Line 332: `2.5 * yw / 8.0` becomes `3.5 * yw / 8.0`. Chest vs spine is not affected, because this term is on the Spine.
- **N4. Keep `ANIM_REFS.md` true to the build.** It still says a 3 deg crest lift and a 6 deg nose lift; update it to the built beats (crest 5 deg, roll 2.5 or 3.5 deg, twitch, breath, and N1 once taken).
- **N5. Model: the mantle's rear corner.** It steps against the grey back in `game_view.png`. Soften the back edge: `rnd` 0.40 becomes 0.50 on line 135, or `top_shift` 0.050 becomes 0.070.
- **N6. Model: flat mantle top.** A 0.01 crown on the mantle top face would soften the plane. Optional.

## Pass / fail checklist

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Badger reads at 64 px | PASS | Icon strip, first slot |
| 2 | Reads at 128 px | PASS | |
| 3 | Distinct from the Grass set | PASS | |
| 4 | Fierce face | PASS | Slit eyes, amber accent, black nose; no glint |
| 5 | No stuck-on parts, thigh and rump clean | PASS | |
| 6 | Torso reads as one form | PASS | Hull and mantle on separate bones (see M1) |
| 7 | Palette and accent | PASS | |
| 8 | Shoulder hump (T1) | PASS | Thorn 1 seated |
| 9 | Underside checked | PASS | Carried over; not re-rendered |
| 10 | Tris | PASS | 6,832 |
| 11 | Clip: loops, ground, collision, pose limits | PASS | Numbers |
| 12 | Clip: no head shakes | PASS | Head yaw 2.99 deg/f max |
| 13 | Clip: flicks read | PASS | Carried over |
| 14 | Clip: idle breath | FAIL | M1 |
| 15 | Clip: sniff roll visible | PARTIAL | MC2; subtle |
| 16 | Clip: crest bristle | PASS | MC3 |
| 17 | Clip: ear twitch visible | PARTIAL | T2; no ear evidence |
| 18 | Clip: walk, roar, act on the current model | PARTIAL | M2 (stale renders) |
| 19 | Animation refs cited | PASS | Carried over; text stale (N4) |
