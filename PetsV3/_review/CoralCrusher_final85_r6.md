**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.** (Clips = lowest per-clip score: walk 8.5.)

# Coral Crusher - FINAL GATE round 6 (walk fix check), 2026-10-28

Fresh reviewer. Walk now sits on the 8.5 floor, with no margin. Idle, roar and act are unchanged, and the model is unchanged. Nothing blocks ship at 8.5.

## What I looked at
All images opened; none failed to load.
- `renders/_walk_strip_game.png` (title 06:20:22, lift 0.10, bob 0.016, roll 2.4, 390 px): f0-27 every 3 f.
- `renders/_walk_strip_tq.png` (same stamp).
- `renders/wk6_game_walk_00.png` and `_09.png` (390 px, full size); `renders/wk6_tq_walk_00.png` to `_27` (not opened one by one; the strip covers them).
- `renders/pose_tq_walk_00/08/15/23.png` (06:20): not opened individually; the walk strip covers the same frames.
- `renders/pose_tq_idle_45.png`, `_62.png` (06:20); `renders/pose_tq_act_semaphore_30.png` (06:20); `renders/pose_tq_roar_22.png` (06:20).
- `renders/_pose_tq_sheet.png` (05:24; walk-only edit, so idle, roar and act are unchanged).
- `renders/_model_sheet.png` (05:25, eye round).
- `renders/_eyes_r4_game1x.png` (05:19 crop, 05:26 file).
- `CoralCrusher_portrait_alt.png` (05:44, idle f0 game camera, 512 px). It is the current Index portrait.

Numbers (read from files, not re-run; I did not run Blender, per the reviewer brief):
- `_scratch/walkpx_before.txt`, `walkpx_after.txt`, `walkpx_roll24.txt`, `walkpx_final.txt`, `walkpx_final_fullcycle.txt`.
- `_scratch/export_walk_r6.txt` (06:20): collision_free true; ground_min_z -0.013 in all four clips; linear 0 in all clips; idle and walk loops 0 / 0; walk slide 0.0016; foot_z_var 0.0008; idle foot drift 0; stride 0.3091; tris 12,452. Events: sand1 0.46, sand2 0.96 (walk 13.8 and 28.8 of 30), act wave1 0.25, wave2 0.442, wave3 0.633, tap1 0.75, tap2 0.8, unchanged.
- `CLIP_NOTES.md` (WALK ROUND, 06:20) matches those files.

## The walk fix: meets the floor, not above it
Phone-size motion at 390 px, f0 to f15 (contact to contact), from the builder's probe:

| point | before (05:24) | final (lift 0.10, bob 0.016, roll 2.4) | bar (>= 4 px) |
|---|---|---|---|
| leg tips (Leg_1 to Leg_6) | 12.1 to 20.0 | 12.1 to 21.7 (full cycle f0-30: 16.4 to 22.4) | pass |
| carapace rim, +x silhouette | (not measured) | 8.1 | pass |
| carapace rim, -x silhouette | (not measured) | 5.2 | pass |
| carapace top centre | 1.9 | 3.5 | **short by 0.5 px** |

- The leg tips pass clearly. The claw sway is also visible: the upper claw tip moves between `wk6_game_walk_00` and `_09`.
- The shell silhouette passes on both rims. I count the silhouette because it is the body edge the player sees. The top-centre point is on the roll axis, so the bob mostly moves it out of the view, and the builder found that bob 0.020 added only +0.3 px. The 4 px bar in the audit names "body"; the top-centre point is the only body point below it, and I say so openly. The lead decides whether that point counts (see the lead decision below).
- The walk is still legs-dominant at phone size. The shell now moves about 2 to 8 px, and it reads as a body that is moving, but only just.

## Per-clip table

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.6 | The guard lift is clear at f62 against f45 (claw tip higher, body breathing). The eyestalk swivel and the f70 tap are not readable at phone size. Idle is unchanged by the walk round: same gate numbers, drift 0. | `renders/pose_tq_idle_45.png`, `pose_tq_idle_62.png` (06:20); `_pose_tq_sheet.png` (05:24); `_scratch/export_walk_r6.txt` |
| walk | 8.5 | Legs alternate in tripods, claws sway, and the shell rolls and bobs. The leg tips move 12 to 22 px, both shell rims pass the 4 px bar (8.1 and 5.2 px), and the claw sway shows. The top-centre point is 3.5 px, and the reference-level shell is now a 2.4 deg roll. This is the floor, not above it. Timing is a lead ruling, not counted. | `renders/_walk_strip_game.png`, `_walk_strip_tq.png` (06:22); `renders/wk6_game_walk_00.png` vs `_09.png`; `_scratch/walkpx_final.txt`; `_scratch/export_walk_r6.txt` |
| roar | 8.7 | Both claws are up in a clack threat with the mandibles open, readable at f22. Unchanged. | `renders/pose_tq_roar_22.png` (06:20); `_pose_tq_sheet.png` (05:24) |
| act (fiddler wave) | 8.8 | The top at f30 has the claw raised high, readable at 300 px. The eye track is a secondary read. Unchanged. | `renders/pose_tq_act_semaphore_30.png` (06:20); `renders/_eyes_r4_game1x.png` (05:19 crop) |

Model: 8.5 PASS. The model geometry is unchanged since the 05:25 sheet. The walk round touched the walk block only. The model reads as a fierce, studded crab, with a clean silhouette, slit eyes and a rose accent.

## Regression check
- No regression found. The export gate numbers match the 05:24 values (collision_free true, ground -0.013, linear 0, loops 0 / 0). The walk-only edit does not change idle, roar or act poses, and the current 06:20 frames I checked match the earlier reads.
- The portrait is current (05:44, idle f0 game camera).

## MUST (blocks 8.5 on the model or any clip)
None. The walk meets the 8.5 floor on the silhouette measure.

## Lead decision (not a MUST, but read this before you ship)
- **Walk centre point, 3.5 px vs the 4 px bar.** If the lead counts only the carapace top centre, the walk is 8.4 and needs one more lever. Bob cannot do it (the camera foreshortens it). The fix would be a fore-aft spine pitch in the walk, about ±1.5 deg, in phase with the tripod contacts. Pass: the top-centre track is >= 4 px between f0 and f15 in the 390 px game frame. Re-run the gate after the change.
- **Walk reference conflict.** `ANIM_REFS.md` still says "carapace bob 0.010 (R1)" and cites R1 and O2 ("the shell stays level"). The walk now uses bob 0.016 and a 2.4 deg roll. The change is measured and documented in `CLIP_NOTES.md`, so the result is accepted, but the reference note is stale. Update the walk line in `ANIM_REFS.md` to say that the audit overrode R1/O2 with a measured body motion. This is housekeeping, not a score item.

## TO 9+
1. **Eyes at phone size** (r5 point, still open). The eye travel is 10 to 12 px on the left and 6 to 7 px on the right, but the eyes read as small dark marks in the full 390 px frame. Option: a further 10 to 15 % step on the bulb and lid (`EB`), keeping the rose slit narrow and the lid angled.
2. **Walk body at phone size.** The rims move 5 to 8 px. For a 9+ read, the shell needs a bigger silhouette move, e.g. the roll at 3 deg (the reference level-shell limit is the lead's call).
3. **Rose fin, front-left dome cluster** (r4 NICE, still open per r5). Replace the flat spike with a cone like the others. Not re-checked this round.
4. **Pale underside (about 2.2 % game share)**, lead ruling pending. Not counted.
5. **Walk timing**, lead ruling pending (Wikimedia crab footage C1). Not counted.

## Pass / fail checklist

| check | result |
|---|---|
| Model >= 8.5 | PASS (8.5) |
| Idle >= 8.5 | PASS (8.6) |
| Walk >= 8.5 | PASS (8.5, floor; centre point 3.5 px noted) |
| Roar >= 8.5 | PASS (8.7) |
| Act >= 8.5 | PASS (8.8) |
| Evidence current for each clip | PASS (walk 06:20-06:22; idle, roar, act 06:20 renders plus 05:24 sheet; model 05:25) |
| Gate numbers (collision, ground, linear, loops, slide, tris) | PASS (`export_walk_r6.txt`) |
| Portrait | PASS (05:44) |
