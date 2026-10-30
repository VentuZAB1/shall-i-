# Bramble Badger - FINAL 8.5 GATE, ROUND 6 (2026-10-28) - Model FIX, Clips FIX

**Model: 8.4/10 - FIX. Clips: 8.2/10 - FIX.**

Overall: FIX. The round-5 neck clause is still not met. The magenta evidence (the 06:08 render of the current pet file) shows Neck-bone geometry that is mantle-coloured and visible in front of the mantle's front face, on its top-front, and under the chin. The round-5 claim that "nothing shows" does not match these renders. The act beats also need a legible close-up check, since the sheets sample them thinly. Everything else holds close to the round-5 level. One Neck-segment edit (`pets/BrambleBadger.py` line 150) plus a re-render should clear the neck item.

## What I looked at
- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; round 5 `_review/BrambleBadger_final85_r5.md`; `BrambleBadger/CLIP_NOTES.md` (round-5 section); `BrambleBadger/ANIM_REFS.md`; vault `06 Modelling and Art/Creature Animation.md`.
- Images opened (all in `BrambleBadger\renders\`): `_neck_evidence_r5.png`, `_walk_sheet_r5.png`, `_idle_sheet_r5.png`, `_act_sheet_r5.png`, `_roar_sheet_r5.png`, `_breath_game_r5.png`, `_ear_twitch_r5.png`, `_model_sheet.png`. No image failed to load.
- My own zoomed crops (outside the project, `C:\Users\ventu\AppData\Local\Temp\bb_r6\`): `pair_r3_rest_magenta_vs_normal.png`, `pair_r3_f64_magenta_vs_normal.png`, `pair_r3_f68_magenta_vs_normal.png`, `pair_r1_rest.png`, `pair_r1_f64.png`, `pair_r2_f64.png`, `act_side_row.png` (act side row at 1x, cropped).
- Code `pets/BrambleBadger.py` (mtime 06:03:31): mantle block line 138-139; Neck segments line 150 (mantle) and 151 (throat); head line 175; ears line 351; roar drop line 389; roar tremble line 392; thorns line 399; act KICK table line 436.
- Timestamps: the pet file was last written 06:03:31, so the r5 renders (06:06-06:09) are current. Two evidence files are older than the current build: `_model_sheet.png` and `_icons_strip_64.png` (04:39), and `_scratch/measure_breath_b0.json` / `b1.json` (04:24). The rigged blend is 06:10:08.
- I did not run Blender or Studio. The builder's clearance, collision and pose-limit numbers are carried from the notes, not re-measured.

## Neck clause (round-4 M2 neck / round-5 MUST 1): what the renders show

Code facts (before MANTLE_TILT -10):
- Mantle block centre (0, -0.364, 0.44), half-size (0.245, 0.11, 0.135). Its front face is at y -0.474 and its underside at z 0.305.
- Neck segment (line 150): from (0, -0.42, 0.42) r 0.15 to (0, -0.58, 0.41) r 0.12, ext 0.04. Its front end reaches about y -0.62, 0.10 to 0.15 in front of the mantle face. Its underside sits at z 0.27 to 0.29, 0.015 to 0.035 below the mantle underside.

What the magenta (Neck-bone parts) renders show:
1. **High 3/4 over the mantle top, rest / f64 / f68** (`pair_r3_rest_magenta_vs_normal.png`, `pair_r3_f64_magenta_vs_normal.png`, `pair_r3_f68_magenta_vs_normal.png`): a magenta plate covers the cape's front-top, from the thorn-1 base down to the white head. In normal colours the same plate reads as a continuous grey cape front. The nape is therefore visible in front of the mantle face and flush with its top. It does not gap or poke, but it is the exact case the pass rule bans.
2. **Low front-left 3/4, act f64** (`pair_r2_f64.png`): a magenta plate sits under the white chin, between the head and the dark throat. In normal colours it is lilac (MANTLE), not the BELLY_D throat. So mantle-coloured Neck geometry is visible below the cape's lower edge. The builder's note that "below the cape edge only the dark throat" shows is not what the render shows.
3. **Low side camera, z 0.15, rest and f64** (`pair_r1_rest.png`, `pair_r1_f64.png`): the magenta column between the head and the cape front is the neck and is expected. The band under the chin reaches down to the throat, the same as item 2.

Judgement: the column between head and cape is correct anatomy and is allowed. Items 1 and 2 break the pass rule: "no MANTLE-coloured Neck geometry visible below the mantle's lower edge, in front of the mantle's front face, or through its top". In normal colours the plate matches the cape, so this is a shape and visibility defect, not a colour one. A player at the game camera will not see it. The brief still judges parts visible from below and in front of the cape, and the rest pose (frame 0 of every clip) is also the model, so the model gate is affected too.

## Clip scores (lowest = the clips score)

| Clip | Score | Why | Evidence file |
|---|---|---|---|
| idle | 8.3 FIX | Nape plate visible at rest and in the sniff (neck clause). Breath is only 5.5 px at 1x at the game camera. Ear twitch is 351 px (f36) and 465 px (f114) at 1x. The nose sniff reads well in the side view at f36. | `_neck_evidence_r5.png`, `_breath_game_r5.png`, `_ear_twitch_r5.png`, `_idle_sheet_r5.png` |
| walk | 8.4 FIX | The sheet (f0-27 every 3 f, game/side/tq) reads: diagonal rhythm, body roll and crest ripple are all visible across the loop. Held back by the rest-pose nape plate. The f1 knee step (10.35 deg) is not in the sheet, so I cannot confirm it. | `_walk_sheet_r5.png`, `pair_r2_f64.png` |
| roar | 8.3 FIX | Hunker drop, the jaw open at f30 and the rise read at sheet scale. Held back by the nape plate in the rest and drop poses. | `_roar_sheet_r5.png`, `pair_r3_rest_magenta_vs_normal.png` |
| act | **8.2 FIX (lowest)** | Deepest neck overlap at f64 (-0.042): visible nape underside under the chin, and the plate over the cape top-front at f64 and f68. The three scoops (f8-38) are sampled at f20 only. The kick peaks (f44, f50-53) are sampled at f44 only. At 1x in the side row the paws are a few px and read as small changes. The head pop and look-around read. | `_act_sheet_r5.png`, `act_side_row.png`, `pair_r2_f64.png`, `pair_r3_f64_magenta_vs_normal.png`, `pair_r3_f68_magenta_vs_normal.png` |

**Model: 8.4 FIX.** The carried round-5 model score of 8.6 assumed no visible nape underside. The low views show one (brief: "parts visible from below"). The model sheet and icon strip are from 04:39, older than the 06:10 build, so the model score cannot be signed until they are re-rendered (MUST 1, step 4). Silhouette, face, palette and tris are unchanged from round 5. Once MUST 1 is fixed and re-rendered, the model returns to 8.6.

## Round-5 items (PASS / PARTIAL / FAIL)

| Item | Verdict | Evidence |
|---|---|---|
| MUST 1 neck clause | **FAIL** | Items 1 and 2 above (magenta renders). The builder's "nothing shows" claim is contradicted. |
| TO 1 ANIM_REFS matches build | PASS | Roar drop `0.10 * H_U` (line 389). Thorns `-22` (line 399). Ears `3.5 * 8 = 28` (line 351). Tremble `2.5` (line 392). Act KICK 0.070 / 0.028 and touchdown 0.058 (line 436). All match ANIM_REFS. |
| TO 2 ear twitch readable at phone size | PARTIAL | 351 px (f36) and 465 px (f114) at 1x, target 1000. Lead ruling: a 9+ item, not a MUST. |
| TO 3 breath at the player's eye | PARTIAL | `_breath_game_r5.png` (2x, head framed): rump moves 11 px at 2x (5.5 px at 1x). The 27 px mid-back figure includes the crest bristle (peaks f70-78), so it does not isolate breath. Subtle at phone size. |
| TO 4 walk judged across the loop | PASS | `_walk_sheet_r5.png`: f0 to f27 every 3 f, three views. The f1 knee step is not in the sheet (see walk row above). |
| TO 5 sheet framing (snout complete) | PASS | Act f5 / f20 and roar f12 / f30 / f59 tq rows show the snout in full. |
| TO 6 breath-only numbers re-run on current file | FAIL (not done) | `measure_breath_b0/b1.json` are 04:24:26, older than the 06:03:31 pet write. Re-run needed. |
| TO 7 breath visibility (optional) | Not done | Optional. |
| TO 8 model polish (optional) | Not done | Side silhouette still reads as a loaf; no mantle crown. Optional. |

Round-5 pass/fail checklist (carried items are marked, not re-measured):

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Reads at 64 / 128 px | Carried PASS | Icon strip is 04:39, pre-build. Re-render. |
| 2 | Fierce face, no glint | Carried PASS | `_close_sheet.png` not re-opened this round. |
| 3 | Tris under cap | Carried PASS | 6,544 (r5). |
| 4 | Breath lifts as one (breath-only) | PARTIAL | Numbers from the 04:24 JSON (TO 6). |
| 5 | Snout held (breath-only) | PARTIAL | 0.0017 from the 04:24 JSON (TO 6). |
| 6 | Literal f50-f70 pair | FAIL as written | Unchanged; breath-only is the real test. |
| 7 | Head / jaw clearance to chest blocks | PASS (carried) | act 0.0116, roar 0.0277, walk 0.0231 (builder numbers, not re-measured after 06:03). |
| 8 | Neck clearance / no visible contact | **FAIL** | MUST 1. |
| 9 | Act, roar, walk renders current | PASS | Renders 06:06-06:09 are later than the 06:03 pet write. |
| 10 | Nose lift 10, sniff roll 3.5 in build | PASS (carried) | From r5 notes. |
| 11 | Ear twitch visible at phone size | PARTIAL | TO 2. |
| 12 | ANIM_REFS matches build | PASS | Checked against code this round. |
| 13 | Walk, roar, act judged across the loop | PARTIAL | Walk PASS. Act beats not legible at sheet scale (MUST 2). |
| 14 | Loops, ground, collision, pose limits | PASS (carried) | Builder numbers (`collision_free` true, ground -0.002, neck 7.87, chest vs spine 2.92, pitch-up 6.25). Not re-run. |
| 15 | No head shake, no airborne spin | PASS (carried) | Head yaw 2.99 deg/f max (r5). |

## New MUSTs (block 8.5 on the model or on ANY clip)

**MUST 1. Neck nape: keep it inside the cape footprint (fixes items 1 and 2; also the model score).**
- Current: Neck seg line 150, `B.seg((0, -0.42, 0.42), (0, -0.58, 0.41), 0.15, 0.12, MANTLE, "Neck", ext=0.04)`. Its front end is about y -0.62 (0.10 to 0.15 in front of the mantle face at y -0.474) and its underside is at z 0.27 to 0.29 (below the mantle underside at z 0.305).
- Direction: keep the nape's front end at y >= -0.470 and its underside at z >= 0.305 along the whole segment (before tilt). For example: start (0, -0.42, 0.44) r 0.13, end (0, -0.47, 0.44) r 0.12, ext 0.0. Tune as needed; the two limits are the rule. Keep the throat (line 151, BELLY_D) as the only neck geometry under the chin.
- Check the head still overlaps the nape end (the skull starts at y -0.56 and its rear reaches about y -0.41). If a gap opens between the nape end and the head in the low side view, fill it with the BELLY_D throat, not MANTLE.
- Pass (renders at rest, act f64 and act f68, same three views as `_neck_evidence_r5.png`, 2x crops): magenta appears only between the head and the cape front. There is no magenta on the cape's top-front (high 3/4) and none below the cape's lower edge in the low front-left view except the BELLY_D throat.
- Re-run the head and neck clearance over act f5-68 and roar f0-45, and paste the new numbers into `CLIP_NOTES.md`. Re-run `measure_breath_b0/b1` on the new file (TO 6) in the same pass.
- Re-render `_model_sheet.png` and `_icons_strip_64/128.png` from the current build (04:39 files are older than the 06:10 blend). Model score is only signed after this.

**MUST 2. Act beats must be readable (blocks the act clip).**
- Current: act sheet samples the scoops at f20 only (f8-38 window) and the kick peak at f44 only. At 1x the paw strokes are a few px.
- Evidence: a 2x close side crop and a 2x game-camera crop at each scoop peak (f16, f26, f36) and each kick peak (f44, f53), with the forepaw and hind-foot lift marked.
- Pass: each scoop lift (0.026 units in code) and each kick lift (0.028) is at least 15 px at 2x in the side crop. If it fails, raise the scoop lift to 0.035 and the kick lift to 0.035 (keep ground >= -0.02, keep the act's chest vs spine <= 5 deg) and re-measure.

## TO 9+ (after the MUSTs; all optional for the 8.5 bar)
1. **Ear twitch to 1000 px at 1x.** The builder's own test says the ears are too small at this camera. Options: move each ear 0.02 units outboard (a model change), or keep 28 deg and extend the twitch. Target: at least 1000 px changed at 1x (`BADGER_TWITCH` on vs off). Owner ruled this a 9+ item.
2. **Breath readable at phone size.** At the game camera the rump moves only 5.5 px at 1x. Scale the Spine lift from +/-0.014 to +/-0.020 and set the head counter-pitch to `+2.9*b` (keeps the nose still, TO 7 carry). Target: at least 9 px at 1x. Keep the breath-only mantle-to-hull slip at 0.0000 (re-measure on the 06:03 file).
3. **Walk knee step at touchdown.** Shin_FL f1 steps 10.35 deg in one frame. Add an f0-f2 strip at the game camera and side camera to confirm it does not pop. If it does, spread the step over two frames (about 5 deg each) or ease it.
4. **Silhouette.** Add a 0.02-unit waist tuck in the flank hull and the 0.01-unit crown on the mantle top (TO 8 carry). The side view is still a long loaf.
5. **Owner/lead note.** If the lead rules the seamless nape plate on the cape a deliberate "cape hood", record it in `CLIP_NOTES.md` with the render paths. The brief's rule is literal, so this review still scores it as a FAIL.

## Scores
- Model: 8.4 FIX (returns to 8.6 once MUST 1 is fixed and re-rendered).
- Clips: idle 8.3 FIX; walk 8.4 FIX; roar 8.3 FIX; act 8.2 FIX (lowest, the clips score).
