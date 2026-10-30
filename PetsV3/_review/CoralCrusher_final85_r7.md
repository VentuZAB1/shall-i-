**Model: 8.5/10 - PASS. Clips: 8.6/10 - PASS.**

# Coral Crusher - FINAL GATE round 7 (walk pitch check), 2026-10-28

Fresh reviewer. The walk moved from the 8.5 floor to 8.6, and every measured point now clears the 4 px bar. The model is unchanged (tris 12,452, same as r6). Idle, roar and act carry from round 6.

## What I looked at
All three images opened; none failed to load.
- `renders/_walk_strip_game.png`: f0-27 every 3 f, 390 px. Title bar shows lift 0.10, bob 0.016, roll 2.4, pitch 1.5.
- `renders/_walk_strip_tq.png`: same frames and settings.
- `renders/_pose_tq_sheet.png`: idle, roar and act beats. The walk round touched the walk block only, so these carry from r6.
- Numbers (read, not re-run): `_scratch/walkpx_final_r6.txt` (08:52, the r7 walk), `walkpx_pitch.txt` (08:49, the nose-down phase), `export_walk_r7.txt` (08:52).
- I did not re-diff the portrait. The builder reports idle f0 as pixel-identical to the 06:20 portrait.

## Walk verdict: PASS 8.6 (was 8.5)

Phone-size motion, f0 to f15 (contact to contact), 390 px game camera:

| point | r6 (06:20) | r7 (08:52) | bar (>= 4 px) |
|---|---|---|---|
| carapace top centre | 3.5 | 4.5 | pass (was 0.5 short) |
| carapace rim, +x | 8.1 | 7.9 | pass |
| carapace rim, -x | 5.2 | 5.2 | pass |
| leg tips (Leg_1 to Leg_6) | 12.1 to 21.7 | 12.1 to 21.7 | pass |

- The phase choice was measured. The nose-down-at-contact variant gave the top centre 3.8 px; the nose-up phase gives 4.5 px.
- **Rocking-horse question:** at +/-1.5 deg, the pitch is a small move. At 390 px the strips show the shell moving gently with the tripods, and the claw sway still does most of the visible work. I did not see a see-saw. I cannot resolve the nose-up beat itself from thumbnails, so this call rests on amplitude and phase. Nose-up on each planted tripod reads as a plausible push onto the feet. No revert is needed.
- **Why 8.6 and not 8.5:** all four measured points now pass, including the one that was short. The +0.1 is for that cleared measure, not for a clearly better-looking walk. The rim at +x dropped 0.2 px; that is noise and still passes.

## Gate numbers (`export_walk_r7.txt`)
collision_free true; ground_min_z -0.013 in all four clips; linear 0 everywhere; idle and walk loops 0 / 0; walk slide 0.0001; foot_z_var 0.0; idle foot drift 0; stride 0.3091; tris 12,452. Events match r6 timing: walk sand1 0.46 and sand2 0.96 (13.8 and 28.8 of 30); act wave1 0.25, wave2 0.442, wave3 0.633, tap1 0.75, tap2 0.8; roar clacks 0.367 / 0.5 / 0.633; idle tap 0.583.

## Per-clip table

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.6 | Carried from r6. Walk-only edit; f0 pixel-identical per builder. | `renders/_pose_tq_sheet.png`, `_scratch/export_walk_r7.txt` |
| walk | 8.6 | Up from 8.5. All measured points >= 4 px; pitch reads as a subtle scuttle. | `renders/_walk_strip_game.png`, `_walk_strip_tq.png`, `_scratch/walkpx_final_r6.txt` |
| roar | 8.7 | Carried. Unchanged. | `renders/_pose_tq_sheet.png` |
| act | 8.8 | Carried. Unchanged. | `renders/_pose_tq_sheet.png` |

Model: 8.5 PASS, carried (geometry unchanged since 05:25; tris 12,452 same as r6).

Clips = lowest per-clip score = walk 8.6.

## MUST
None. Nothing regressed; every r6 walk point holds or improves.

## NICE (not scored)
1. `CLIP_NOTES.md` is current, but `ANIM_REFS.md` S1 "Walk check" still says "our 30 f crab walk keeps the low lift 0.07". The walk is now lift 0.10. Change that clause; the updated block below it is correct. Housekeeping only.
2. Still open from r6, not re-checked and not counted: the front-left rose fin cone (r4 NICE), eyes at phone size (r6 TO 9+ item 1). Pale underside and walk timing are lead rulings.
3. If the lead wants the nose-up beat confirmed, a full-size look at the 390 px game walk frames near f12 and f9 would settle it.

## Pass / fail checklist

| check | result |
|---|---|
| Model >= 8.5 | PASS (8.5, carried) |
| Idle >= 8.5 | PASS (8.6, carried) |
| Walk >= 8.5 | PASS (8.6; all four measured points >= 4 px) |
| Roar >= 8.5 | PASS (8.7, carried) |
| Act >= 8.5 | PASS (8.8, carried) |
| Walk no regression vs r6 | PASS |
| Gate numbers (collision, ground, linear, loops, slide, tris, events) | PASS (`export_walk_r7.txt`) |
| Pitch revert needed | NO |
| ANIM_REFS current | PARTIAL (one stale lift 0.07 clause; NICE) |
