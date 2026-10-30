# Frostfang Lynx - FINAL 8.5 GATE, round 5 (model + clips) - 2026-10-28

**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.**

Clip scores: idle 8.5, walk 8.5, roar 8.5, act 8.5. The clip score is the floor of the four (owner rule), so 8.5.

Round 4's only sub-bar clip was the walk (8.0). W1 now measures 26.9 px at 1x and 55.5 px at 2x, above the 15 / 30 px bar. Every other round-4 item passes, and no MUST blocks 8.5. The TO 9+ list below is for polish.

## What I looked at
- Brief: `_review/GLACIER_REVIEWER_BRIEF.md`. Round 4: `_review/FrostfangLynx_final85_r4.md`. Builder notes: `FrostfangLynx/CLIP_NOTES.md` (round 4 section and the older sections for the rig).
- Numbers: `_scratch/fullcheck.json`, `_scratch/clipmetrics.json`, `_scratch/fc_r4.txt`, `_scratch/export.log`, `_scratch/gate6.log`.
- Source: `pets/FrostfangLynx.py` is byte-identical to `_scratch/FrostfangLynx_f85r4.py` (the 03:56 export).
  - Round 2 to round 3 changed only animation lines 439, 444, 447, 468.
  - Round 3 to round 4 changed only animation lines from 419 on.
  - The model section has not changed since round 2.
- Renders (newest set): `renders/_walk_tail_r4.png` (1x and 2x walk f6 / f18), `_idle_game_r4.png`, `_breath_side_r4.png`, `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png` / `_128.png`, `_pose_tq_sheet.png`, `_pclose_side_sheet.png` (act and roar, side), `pclose_game_act_clawflex_50.png`, `pose_tq_idle_00/26/62.png`, and `_walk_tail_r3.png` (for the correction check).
- Measurements: this Python has no PIL and I did not run Blender, so I used a stdlib-only PNG decoder fed from stdin (no files written). It reproduces the builder's tail and ear numbers exactly, using the same centroid and top-ICE-pixel methods. This confirms the builder's numbers; it is not an independent method.
- Vault: `06 Modelling and Art` (Creature Style, Creature Animation, Model Review Checklist), `01 Rules` (Taste and Quality), and `ANIM_REFS.md`.
- Not seen or not measured: walk frames f5 and f7 (knee step); a game-camera breath pair; act and roar at 1x (the sheets are 300-400 px). The contact frames (FR f6, FL f18) are taken from the builder's note and were not re-derived.
- Evidence dates: the model sheet, close sheet, icon strips, and the act and roar sheets are timestamped 01:37-01:38, before the 03:21 round-2 source. I treated them as current. The model sheet shows the round-2 rosette pale centres. The rest-pose paw pixels match the 03:56 render (79 vs 80 ICE pixels in the paw band; lowest rows 254 and 266 in both). I could not confirm the 0.095 claw length to the pixel at 300 px.
- Lead rulings (not counted): frost-silver coat; ICE sparks on claw1 f48 and claw2 f60 (not verified here).

## Round-4 items
| Item | Result | Evidence |
|---|---|---|
| W1 walk tail counter-sway | PASS | f6 to f18, game camera, Root-fixed. At 1x the tip moves 26.9 px (bar 15); at 2x 55.5 px (bar 30). Black-tip centroid (max channel < 90, lower 60 % of frame): 1x (430.4, 529.7) to (456.2, 522.2); 2x (418.5, 378.7) to (472.4, 365.6). Source: Tail1 yaw `12*wave(f,n,0.5)` + roll `6*wave(f,n,0.5)`, Tail2 at 0.6x, Spine yaw 1.8 unchanged, opposite phase. Gates: walk loop 0.0 / 0.0, slide 0.0, collision_free true, linear 0, quaternion flips 0. **Correction verified:** re-measuring `_walk_tail_r3.png` (4 panels, same method) gives f6 to f18 = 2.4 px. The 23 px claim is corrected, as the builder says. Visible by eye: at 1x the tip swings sideways about as far as the idle tail (29 px). |
| P1 ear twitch 12 deg | PASS | Pricked-ear tip f62 to f70: 13.6 px at 1x, 30.7 px at 2x (head camera). The other ear moves 2.0 / 5.0 px (head motion). Ear_R presses -7.2 (`pr = -0.6*tw`), rebound at f72. |
| P2 breath 0.04H | PASS (side camera) | Back top edge, median of 13 columns: 21 px lower at f60 than f0 (range 15-22; round 3 was 16). Idle foot drift 0.0. Not measured at game camera. |
| P3 stale comment | PASS | Line 438 now reads "breath weight 0..1 (3 breaths, peaks f20/60/100)". The Spine line reads "r4 P2: breath dips 0.04H". |
| P4 walk head nod | PASS (as built) | `nod = 0.5 - 0.5*cos(4*pi*(f-1)/24)`: peaks f7 / f19, one frame after the builder's FR f6 / FL f18 contacts. Neck +1.5 and Head +3.5, a 5 deg dip in total. Head pitch-up max 0.85. Conflicts with the ANIM_REFS L0 "steady head" note; see TO 9+ 1. |
| Known knee step, 12.45 deg local at FR f6 | Not visible as a pop; not a MUST | The local figure is joint-relative. The world-space change of every Leg_*, Shin_*, Foot_* and Claw* bone is capped at 7.8 deg/f in every clip (clipmetrics `swing_max_limb`), the same cap as the other legs. The leg silhouette therefore moves at its normal speed. I could not check f5 to f7 by eye. |
| Idle tail 22 deg (carried over) | PASS | f26 to f62: 29.3 px at 1x, 57.9 px at 2x. Re-measured. |
| Gates | PASS | collision_free true; linear 0 in all clips; idle and walk loops 0.0 / 0.0; idle foot drift 0.0; walk slide 0.0; ground min -0.0 (idle, walk, roar), -0.002 (act); tris 8,396 (cap 15k); neck max 5.63 idle, 1.94 walk, 4.0 roar, 7.36 act (cap 8); chest vs spine max 3.35 (cap 5); head pitch-up max 1.32 (cap 30); head yaw rate max 3.26 deg/f, no shakes; act and roar end at 0.0 vs f0; 0 quaternion flips. |

## Clip scores
- **Idle 8.5.** The tail sways 29 px at 1x, the ear twitch reads at 1x (13.6 px), the head turns +14 deg and holds, and the breath dips 21 px on the side camera. The one unmeasured piece is the breath at game distance.
- **Walk 8.5.** W1 is met, the loop closes and the slide is 0. The tail counter-sway is now about the same size as the idle sway. The walk is still a generic lateral cat walk; the tail carries it, with the 5 deg head nod as a second beat.
- **Roar 8.5.** Unchanged since round 3 (no roar lines in the round 3 to 4 diff). The pose sheet shows the cheek ruffs flared and the jaw open at f30. It reads as a threat.
- **Act 8.5.** Unchanged since round 3. The crouch and the head-locked stare read in `pclose_game_act_clawflex_50` and in the side sheet. The claw flex is small at phone scale (thin cyan wedges). The lead's ICE sparks (not counted) should carry it.

## Model 8.5
- Reads fierce: narrow cyan slits in dark sockets under heavy angled brows, a dark nose, fangs and cheek ruffs. The close-up holds up.
- Lynx silhouette: tall tufted ears with cyan tips, a short black-tipped tail, rosette flanks (dark broken rings with pale centres), long legs and snowshoe paws.
- Studded blocky skin on body, legs and head; eyes, claws and tufts are smooth, as the style asks.
- At 64 px and 128 px (icon strips) the Lynx reads as a spotted pale cat and sits apart from the Badger and ShadePanther.
- Limits (none blocks 8.5): the underside is paler on the plan than in the render (flat share SNOW 7.8 % in side view vs the plan's 20 %); the body colour is the lead's frost-silver ruling (not counted); the face is small at game distance.

## New MUSTs
None. Nothing in the model or the clips blocks 8.5.

## TO 9+ (not required for 8.5)
1. **Walk head nod vs reference.** ANIM_REFS L0 says the head and back stay level (a steady head). The P4 nod is a 5 deg deviation. Either note it in `ANIM_REFS.md` as a deliberate foot-contact nod, or reduce it to about 3 deg total (neck +0.9, head +2.1). Keep pitch-up at or under 30 deg.
2. **FR touchdown knee (f6, local 12.45 deg).** Optional smoothing: add an in-between key at f5 or f6 so the local step is split across two frames (about 6 deg each). The vault limit is 60 deg per frame, so this is polish, not a fix.
3. **Act claw flex at phone scale.** The flex is a thin cyan wedge at 1x. If the ICE sparks do not carry it, widen the claws about 15 % (half-width 0.017 to 0.020, length kept) and re-check `pclose_game_act_clawflex_50` at 1x. This is a model change, so re-run the model gate.
4. **Underside contrast.** The plan asks for a pale SNOW underside at about 20 % of the side view; the measured share is 7.8 %. A SNOW band on the lower third of the ribcage would restore the pale-underside rule without changing the body colour. Re-check the flat side render and its shares.
5. **Fangs.** The lower fangs read pale cyan in the close front view, not the plan's TEETH ivory (238, 234, 220). Check the palette ID; if they are ICE, set them to TEETH per the plan.
6. **Breath at game distance.** Measure the 1x game-camera back line for f0 vs f60 (the side camera shows 21 px). If it is under 8 px at 1x, consider 0.05H, keeping idle foot drift at 0.0.
7. **Evidence hygiene.** Send the next gate with fresh model, act and roar sheets rendered from the current 03:56 FBX, plus the 2x walk pair, so no sheet is older than the source it judges.
