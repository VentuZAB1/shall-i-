# Eclipse Seraph - model + clip gate review 11 (2026-10-28) - final gate

**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.**

Round 10 was model 8.5, clips 8.0 (roar 8.0, takeoff 8.0). Round 11 lifts roar and takeoff to 8.5 under the binding lead ruling. The far upper wing (`Wing_A_L`, viewer's left) is no longer a rod: it is about 2x wider, shows 4-5 separate dark tips, and its takeoff f4-f10 halo overlap is gone. Both clips sit on the 8.5 floor with no margin. Roar is the weakest clip and the call there is marginal (see roar row). The model is unchanged from round 10.

---

## What I looked at

- Brief `PetsV3\_review\GLACIER_REVIEWER_BRIEF.md`; round 10 `_review\EclipseSeraph_review10.md`; builder `EclipseSeraph\CLIP_NOTES.md` ("Review 10 fixes", clip round 8).
- Source `PetsV3\pets\EclipseSeraph.py` (saved 09:51), grepped: `TOP["A_L"] = (31, -4, 34, -10)` (line 417), `ROAR_W["A_L"] = (36, -8, 26, 0)` (line 433), gather `A_L=(31, -0.8, 29.2, -9.2)` (line 603), `BRAKE["A_L"] = (36, 6, 34, 0)` (line 440), `LOW["A_L"] = (18, -6, 48, 4)` (line 431). The builder's round-11 numbers match the file. No fly key sets `A_L`.
- Sheets (all stamped 09:53, newer than the source): every clip in game, tq and front views. All 21 `renders\_pose_<view>_<clip>_sheet.png` were opened this pass. The round-10 stale-evidence problem is resolved.
- 3x rod crops: `renders\_rod_check_roar_3x.png` (f14 / f30 / f50), `_rod_check_takeoff_3x.png` (f4 / f6 / f8 / f10), `_rod_check_land_3x.png` (f7 / f8 / f10 / f12).
- Height comparison: `renders\_roar_far_wing_height_cmp.png` (A_L up 24 / 30 / 36 / 40).
- Roar front 3-tier check: `renders\_tiers_check_front_roar_3x.png`.
- Model gate: `renders\_model_sheet.png`, `EclipseSeraph_icon.png`, `renders\_icons_strip_64.png`, `renders\_icons_strip_128.png`.
- NOT re-run: headless step 1, halo measurements, blade metric. Numbers are the builder's, marked "builder". Per-frame rod widths for takeoff f6 / f10 and land f6 / f8 are not listed in the notes.

---

## Per-clip table (player's eye = game camera; tq and front are secondary)

| clip | score | why | evidence (`renders\`) |
|---|---|---|---|
| idle (120 f loop) | 8.5 PASS | Breath and halo drift read; game camera clean on every frame. In the tq view the upper wing is still one thin spike (TO 9+ 2, unchanged). | `_pose_game_idle_sheet.png`, `_pose_tq_idle_sheet.png`, `_pose_front_idle_sheet.png` |
| walk (40 f loop) | 8.5 PASS | Lateral steps, display fan held, tail sway; no clipping in game or front view. | `_pose_game_walk_sheet.png`, `_pose_tq_walk_sheet.png`, `_pose_front_walk_sheet.png` |
| fly (28 f loop) | 8.5 PASS | Three strokes read; approved stroke untouched (no fly key sets `A_L`). Far upper blade is still narrow at f7 (TO 9+ 3, unchanged). | `_pose_game_fly_sheet.png`, `_pose_tq_fly_sheet.png`, `_pose_front_fly_sheet.png` |
| takeoff (28 f) | 8.5 PASS | Halo rim clear at f4-f10 on the 3x crop; the round-10 touch is gone. Far blade is 5.7-7.5 builder width over f4-10 with 4-5 tips at f10. Halo hidden 10/9/6/3/1/0 % (builder). Crouch and launch read. | `_rod_check_takeoff_3x.png`, `_pose_game_takeoff_sheet.png`, `_pose_tq_takeoff_sheet.png`, `_pose_front_takeoff_sheet.png` |
| land (28 f) | 8.5 PASS | Flare, touch f16, settle into the display fan by f28. Far blade f7-f12 is broad with tips and crosses the mane flank, not the body. Not re-measured after the TOP change (the first flare key uses TOP). | `_rod_check_land_3x.png`, `_pose_game_land_sheet.png`, `_pose_tq_land_sheet.png`, `_pose_front_land_sheet.png` |
| roar (66 f) | 8.5 PASS (floor, marginal) | The far wing is no longer a rod: 8.9 builder width, 4-5 separate tips, a visible gap to the halo rim at f30. It still reads as one feathered lance crossing the mane's top-left. Feather tips sit only on its outer third, so it is a feathered blade more than a fan along its length. Lead ruling accepts the overlap, so this is not counted against the score. The halo lift and tilt read; the front view shows three tiers per side. Mane 0.60 (builder; the old 0.73 bar is waived by the ruling). If the lead reads the far wing as a blade and not a fan, this drops to 8.0. | `_rod_check_roar_3x.png`, `_roar_far_wing_height_cmp.png`, `_pose_game_roar_sheet.png`, `_pose_front_roar_sheet.png`, `_tiers_check_front_roar_3x.png` |
| act_wingcascade (110 f) | 8.5 PASS | Star fan at f58 / f70, reverse ripple, exact rest at f110. Unchanged from round 10. | `_pose_game_act_wingcascade_sheet.png`, `_pose_tq_act_wingcascade_sheet.png`, `_pose_front_act_wingcascade_sheet.png` |

**Clips score = lowest clip = 8.5.** All seven clips sit on the 8.5 floor.

---

## Model

**8.5 PASS.** No model edits this round; `_model_sheet.png`, the icon and the 64 px and 128 px strips match round 10. At 64 px the first icon reads as a winged, halo-crowned beast. The lion read is still partial: the dark mane is a mass and the pale muzzle is small (TO 9+ 1). Colour is on hold and not scored.

---

## Round-10 items (under the lead ruling)

| item | result | evidence |
|---|---|---|
| MUST 1a: far upper wing as a rod across the mane (roar) | **PASS** (floor, marginal) | Width 8.9 builder (round 10: 7.0); 4-5 separate tips; no longer a rod. Silhouette is still one lance (see roar row). `_rod_check_roar_3x.png`, `_roar_far_wing_height_cmp.png` |
| MUST 1a: rod metric >= 7.0 at roar f14 / f30 / f50 | **PASS (builder)** | Builder lists 8.9 for the in-file value; per-frame f14 / f50 not listed. Not re-measured. |
| MUST 1a: mane visible >= 0.73 at f30 | **WAIVED** by lead ruling | 0.60 (builder). The lead ruled that overlap is physically unavoidable. Not counted. |
| MUST 1a: roar f30 halo clearance >= 0.050 | **PASS (builder)** | 0.055 (builder); a visible gap between the far wing and the halo rim on the crop. |
| MUST 1a: fanned, feathered far wing (lead's criteria) | **PASS** (marginal) | Separate tips and width well above rod: met. Fanned along its length: only partly. |
| MUST 1b: far blade clear of the takeoff halo rim, f4-f8 | **PASS** | Clear on the 3x crop at f4 / f6 / f8 / f10. Builder overlap 0-1 % from f4. `_rod_check_takeoff_3x.png` |
| MUST 1b: takeoff halo hidden <= 10 % over f0-10 | **PASS (builder)** | 10 / 9 / 6 / 3 / 1 / 0 %. Not re-measured. |
| MUST 1b: rod metric >= 6.0 at takeoff f6 and f10 | **UNVERIFIED** | Builder range 5.7-7.5 over f4-10; per-frame f6 / f10 values not listed. Visually the blade is wider than round 10. |
| MUST 1b: land f6-f8 rod >= 6.0 (TOP feeds land's first flare key) | **UNVERIFIED** | Not re-measured after the TOP change. Visually no regression on the land sheets. |
| MUST 1 overall: collision_free, 0 collisions, linear 0, ground >= -0.015 | **PASS (builder log)** | Ground -0.013 (takeoff). Not re-run. |
| Fly stroke (f24-28) and DISPLAY_POSE untouched | **PASS** | No fly key sets `A_L`; fly sheets match round 10 at sheet scale. |
| Front roar three tiers | **PASS** | At f30 the upper V, the middle pair and the lower pair read as three separate tiers per side. `_tiers_check_front_roar_3x.png` |
| Round-10 TO 9+ 5: re-render stale sheets | **DONE** | All 21 sheets stamped 09:53, after the 09:51 source. |
| Round-10 TO 9+ 1: lion read at 64 / 128 px | **PARTIAL (unchanged)** | Cheek ruff not touched. `_icons_strip_64.png`, `_icons_strip_128.png` |
| Round-10 TO 9+ 2: tq upper wing is a thin spike | **PARTIAL (unchanged)** | Still a spike in tq roar f8-58, takeoff f4-10, fly f7-10, idle. Game camera clean. |
| Round-10 TO 9+ 3: fly f7 far upper rod | **PARTIAL (unchanged)** | Still narrow at f7. Stroke approved. |
| Round-10 TO 9+ 4: far lower group on the card | **PARTIAL (unchanged)** | Lower far tips still read as a cluster. `EclipseSeraph_icon.png` |

---

## New MUSTs

**None.** Nothing in the round-11 evidence blocks 8.5 on the model or on any clip under the lead ruling.

Residual risk, not a MUST: the roar's far wing is a feathered lance rather than a fan along its length. If the lead scores that as a blade, roar drops to 8.0 and the fix is the TO 9+ 1 below.

---

## TO 9+ list (not required for 8.5, each measurable)

1. **Far upper fan (roar and takeoff).** Give the far blade separate tips along its outer half, not only at the tip. Test a tip step of about 8 on `ROAR_W["A_L"]` (line 433, tip 0) and on `TOP["A_L"]` (line 417, tip -10), keep whichever sign widens the far tips on the 3x crop, and keep it only if collision_free holds and roar f30 halo clearance stays >= 0.050. Target: rod metric >= 12 at roar f30 and takeoff f10 (the fanned A_R band measures 12-17). Do not touch the fly stroke.
2. **Verify the per-frame rod numbers.** Report takeoff f6 / f10 and land f6 / f8 as separate values (the round-10 bar is >= 6.0). Takeoff f4 is the narrowest (5.7).
3. **Lion read at 64 px (TO 9+ 1).** Lengthen the OBSID cheek ruff by 0.03 (lines 305-306, 0.20 / 0.19 to 0.23 / 0.22).
4. **Tq upper-wing spike (TO 9+ 2).** Add one or two tip feathers to `Wing_A` so the tq roar, takeoff and fly read as a fan.
5. **Far lower group on the card (TO 9+ 4).** Add one feather row to `Wing_C_L`.
6. **Trade-off, not a fix.** `A_L` up 24 / twist 30 shows the mane at 0.83 but a narrower blade (6.4). The builder notes it as a one-line swap. The lead chose 36, so I did not score it.
7. **Head from the game camera (no fix proposed).** At every game-camera roar frame the muzzle sits behind the mane. It is readable in the front and tq views, and this is unchanged from round 10. Owner call only.

---

## Verdict

**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.** Lowest clip 8.5 (roar marginal). No MUSTs. Ship at the floor; TO 9+ 1 and 2 are the next round if the owner wants margin.
