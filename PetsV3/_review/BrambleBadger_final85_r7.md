# Bramble Badger - FINAL 8.5 GATE, ROUND 7 (2026-10-28) - Model PASS, Clips PASS

**Model: 8.6/10 - PASS. Clips: 8.5/10 - PASS.**

Clips score = the lowest per-clip score: idle 8.5, walk 8.6, roar 8.5, act 8.5. The clips score is at the 8.5 floor with no margin. Nothing blocks the bar. The MUST list is empty. Two evidence steps are listed under "Before signing" (not scoring items).

## What I looked at
- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; round 6 `_review/BrambleBadger_final85_r6.md`; `BrambleBadger/MODEL_NOTES.md` (round 7), `CLIP_NOTES.md` (round 6), `ANIM_REFS.md`, `_shares.json`, `BrambleBadger_meta.json`.
- Vault `06 Modelling and Art/Creature Style.md` (FIERCE rules: no box bellies, tucked waist, fierce eyes, no glints, one accent).
- Plan `_review/BrambleBadger_plan.md`: the inverted palette (pale back, dark belly) is an accepted ruling 4, so it is not scored.
- All 13 listed images opened, none failed: `_neck_evidence_r6.png`, `_act_beats_r6.png`, `_breath_game_r6.png`, `_walk_touchdown_r6.png`, `_idle_sheet_r6.png`, `_walk_sheet_r6.png`, `_roar_sheet_r6.png`, `_act_sheet_r6.png`, `_model_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `game_view.png`, `low_below.png`. Also `_close_sheet.png` (face) and `_scratch/r6/_model_view.png` (post-write model).
- Code `PetsV3/pets/BrambleBadger.py` (mtime 08:21:36): line 40 MANTLE_TILT -10; line 157 throat seg `(0,-0.43,0.38)->(0,-0.58,0.385)` r 0.11/0.12 BELLY_D; line 350 Spine breath `0.023*b`; line 353 Head `-10*lf + 3.35*b`; lines 492/494 act lifts 0.035 and kick 0.070 / touchdown 0.058; line 447 drop `0.10*H_U`; line 457 thorns -22; line 456 ears -28; line 357 twitch 8 fwd + 28 out.
- Measurement files: `_scratch/measure_breath_b0.json` and `b1.json` (08:21:43-45, after the write); `_scratch/fc_r6.txt` and `fullcheck.json` (08:22:48); `_scratch/meas_clear.log` (08:17:39, before the write); `_scratch/gate_r6.txt` (08:20:26).
- Timestamps: the pet file was written 08:21:36. The clip sheets, neck evidence, breath and breath JSON are all after it. The model sheet, icon strips, `game_view`, `low_below`, `flat_*` and `walk_touchdown` are 08:20, before it. The post-write `_scratch/r6/_model_view.png` (08:23) shows the same silhouette, and tris are 6,356 in both the 08:20 gate log and the 08:22 audit, so the model evidence is current.
- I did not run Blender or Studio.

## Per-clip table

| Clip | Score | Why | Evidence file |
|---|---|---|---|
| idle | **8.5 PASS** | The neck is now one dark column and reads as a neck, not a plate. The sniff drop reads at f36 (tq). The breath is now 10.5 px at 1x at the game camera (was 5.5), above the 9 px target. The crest bristle reads at f70. Held at 8.5 by the ear twitch (351 px at 1x in r5, unchanged code, 9+ item) and by the breath still being subtle at phone size. | `_idle_sheet_r6.png`, `_breath_game_r6.png`, `_neck_evidence_r6.png`, `_scratch/measure_breath_b0.json` / `b1.json` |
| walk | **8.6 PASS** | Every 3 frames across the 30 f loop in three views. The body is lowest at each touchdown. Largest knee step is 5.30 deg (was 10.35). The soft-foot path reads. The nape plate no longer shows in the walk pose. | `_walk_sheet_r6.png`, `_walk_touchdown_r6.png` |
| roar | **8.5 PASS** | The hunker drop, the jaw open at f30 (tq and side) and the slower rise read. The nape plate is gone. Held at 8.5 because the drop onset and the rise are each sampled at only one frame (f12, f59), so the thorn and ear flattening is judged from one frame. | `_roar_sheet_r6.png`, `_neck_evidence_r6.png` |
| act | **8.5 PASS (lowest, no margin)** | Side 2x: scoops 28.3 px (f11/f21/f31), kicks 28.3 px (f44/f53). Game 2x: scoops 16.0 / 15.5 / 16.0 px, kicks 17.6 / 17.7 px. All are at least 15 px. The nape is fixed. Held at the floor because from the game camera the front scoops sit mostly under the chest. That is about 8 px at phone size, so only the hind kicks read at a glance. | `_act_beats_r6.png`, `_act_sheet_r6.png` |

## Model: 8.6 PASS
- Reads as a badger at 64 px and 128 px: white striped face, amber crest, dark legs. The first icon is the pet.
- Face fierce, not cute: black wedge sockets with an amber slit, no glint, dark nose (`_close_sheet.png`).
- Palette follows the plan (accepted inverted colouring). The amber thorn crest is the one accent.
- Tris 6,356 (under the 15k cap). Nothing floats or intersects. Parts seen from below (skirt, claws, throat) are seated (`low_below.png`).
- The neck is one dark column between the head and the cape (`_neck_evidence_r6.png`). It reads as a neck.
- Held back from 9 by: the side silhouette is still a long rounded box with a flat dark skirt, and the cape reads as a separate block on the back (see the 9+ list).

## Round-6 items

| Item | Verdict | Evidence |
|---|---|---|
| MUST 1 neck, items 1 and 2 (magenta on the cape top-front and below the cape edge) | **PASS** | `_neck_evidence_r6.png`. Low side (rest, f64, f68): magenta only in the column between the head and the cape front. Low front-left: the plate under the chin is the throat. Its normal colour is now dark BELLY_D, not lilac. High 3/4: the magenta is the neck column between the head and the cape's front-top corner, not the flat top. No MANTLE neck geometry shows anywhere. |
| MUST 1, clearance re-run and numbers in CLIP_NOTES | **PASS on the look; PARTIAL on freshness** | The head clearance numbers (act 0.0116 at f68, whole act 0.0105 at f90, roar 0.0277, walk 0.0231) come from `meas_clear.log` at 08:17:39, before the 08:21:36 write. The 08:22:48 audit says `collision_free` true, so there is no contact. See "Before signing". |
| MUST 2 act beats legible | **PASS** | `_act_beats_r6.png`: every beat above 15 px at 2x in the side crop (28.3) and the game crop (16.0 to 17.7). The scoop and kick lifts are 0.035 in code (lines 492 and 494). |
| TO 1 ANIM_REFS matches build | **PASS** | Drop 0.10 H_U (line 447), thorns -22 (457), ears -28 (456) and twitch 8 + 28 (357), act lift 0.035 and kick 0.070 / touchdown 0.058 (492, 494). Tremble 2.5 carried from r6 (not re-grepped). |
| TO 2 ear twitch readable at phone size (9+ per lead) | **PARTIAL (carried)** | No change since r5: 351 px (f36) and 465 px (f114) at 1x against 1000 px. Not re-measured this round. |
| TO 3 breath at the player's eye | **PASS** | `_breath_game_r6.png`: the rump block moves 21 px at 2x = 10.5 px at 1x (game camera f50 to f70). Target 9. |
| TO 4 walk across the loop | **PASS** | `_walk_sheet_r6.png`, f0 to f27 every 3 f, three views. |
| TO 5 sheet framing (snout complete) | **PASS** | Act and roar tq rows show the full snout. |
| TO 6 breath-only numbers re-run on the current file | **PASS** | `measure_breath_b0/b1.json` (08:21:43-45, after the write). Mantle-minus-hull is identical at every row, so the slip is 0.0000. Snout moves at most 0.0024 (f50). Lowest head/jaw Z 0.0206 (f28). |
| TO 7 breath visibility (optional) | Not done | Optional. |
| TO 8 model polish (optional) | **PARTIAL** | Waist tuck 0.02 added. The side still reads as a loaf, and the mantle crown was skipped. See 9+. |
| Checklist 1 reads at 64 / 128 px | **PASS** | `_icons_strip_64.png`, `_icons_strip_128.png`. |
| Checklist 2 fierce face, no glint | **PASS** | `_close_sheet.png`. |
| Checklist 3 tris under cap | **PASS** | 6,356. |
| Checklist 4 breath lifts as one | **PASS** | Slip 0.0000 at every row. |
| Checklist 5 snout held | **PASS** | At most 0.0024 against a 0.003 limit. |
| Checklist 6 literal f50-f70 pair | **PASS** | Rump moves 10.5 px at 1x. |
| Checklist 7 head/jaw clearance | **PASS** | Figures carried from 08:17 (see "Before signing"). |
| Checklist 8 neck clearance, no visible contact | **PASS** | See MUST 1. |
| Checklist 9 act, roar, walk renders current | **PASS** | Clip sheets are 08:23, after the write. The walk touchdown strip is 08:20, before it, but the 08:23 walk sheet covers the loop. |
| Checklist 10 nose lift 10, sniff roll 3.5 | **PASS** | Line 353 `-10*lf`; line 350 `3.5*yw/8`. |
| Checklist 11 ear twitch at phone size | **PARTIAL** | See TO 2. |
| Checklist 12 ANIM_REFS matches build | **PASS** | See TO 1. |
| Checklist 13 walk, roar, act across the loop | **PASS** | Walk full loop. Act beats at 2x. Roar sampled at f12, f30, f59 only. |
| Checklist 14 loops, ground, collision, pose limits | **PASS** | `fc_r6.txt` (08:22): `collision_free` true, ground -0.002, loops 0.0, linear 0. Neck 7.87 idle (limit 8), chest vs spine 2.92 walk (limit 5), pitch-up 6.25 act (limit 30); the pose numbers are carried from earlier runs. |
| Checklist 15 no head shake, no airborne spin | **PASS (carried)** | Head yaw max 2.99 deg/f (act). Quaternion flips 0 (carried). |

## MUST list
**None.** The model (8.6) and every clip (8.5 lowest) clear the bar on current evidence.

## Before signing (evidence only; these do not change a score)
1. Re-run the head and neck clearance on the 08:21:36 file: act f5-68, whole act, roar f0-45, walk. Paste into `CLIP_NOTES.md`. The 08:17 run predates the write. Only a margin under 0.010 would change a score.
2. Re-run the pose metrics (neck, chest vs spine, pitch-up, yaw) on the final file. The 08:22 audit covers collision, loops, ground and linear only.

## TO 9+ (after the bar, all optional)
1. **Front scoops at phone size.** From the game camera the front scoop lift is about 8 px at 1x (16 px at 2x), and the paws sit under the chest. Target: at least 24 px at 2x in the game crop at f11, f21, f31. Options: raise the scoop lift from 0.035 to about 0.045 (keep ground at or above -0.02 and chest vs spine at or below 5 deg), and/or move the scoop reach 0.02 outward on x so the paw clears the chest line. Re-measure with the `_act_beats_r6` method.
2. **Ear twitch.** Target at least 1000 px changed at 1x (`BADGER_TWITCH` on vs off, game camera f36 and f114). Angle alone will not reach it (r5 said so). It needs a model change: larger ears and/or 0.02 units outboard each. Then re-measure.
3. **Breath at 1x.** Currently 10.5 px. Target at least 12 px. Raise the Spine breath from 0.023 to about 0.026 and the head counter-pitch from 3.35 to about 3.8. Keep the slip at 0.0000 and the snout at 0.003 or less in the breath-only pair.
4. **Belly line.** The skirt rises only 0.04 from chest to rump in side view. The vault rule says the belly line should rise from chest to hind legs. Raise the rump end of the skirt by 0.02 (total rise 0.06), then recheck `low_below.png` and the side silhouette.
5. **Cape reads as a second box.** In side view the lavender cape is a separate block on the back. Slope its front-top edge further (top from (0.86, 0.66) toward about (0.78, 0.58)) so it reads as a shoulder, not a lid. Recheck head clearance after the change.
6. **Roar sampling.** Add roar f0, f5, f50 and f55 to the sheet (evidence only) so the drop onset and the rise are judged, not one frame each.
7. **Idle neck margin.** 7.87 against the 8 limit (0.13 deg). If the nod still reads, take 0.5 deg off the neck pitch.

## Notes (not counted)
- Lead rulings honoured: crest bigger than plan, ear twitch as 9+, VFX in Studio, walk speed in game.
- Sibling distinctness was not re-checked this round.
- The other reviewer items from r6 that depended on the nape plate (roar, walk, act) now show no nape plate in any clip pose I looked at.
