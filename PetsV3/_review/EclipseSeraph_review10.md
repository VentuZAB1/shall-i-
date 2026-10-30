# Eclipse Seraph - model + clip gate review 10 (2026-10-28) - final gate

**Model: 8.5/10 - PASS. Clips: 8.0/10 - FIX.**

The model holds at 8.5 with no regression (unchanged this round). The clips stay at 8.0 because the far upper wing (`Wing_A_L`, viewer's left) is improved but not yet fixed. It is no longer a thin rod: at the game camera it now shows 4-5 separate dark tips in roar f30 and takeoff f10, and the blade width roughly doubled (builder metric 3.7 -> 7.0 in roar, 3.5 -> 8.3 at takeoff f10). Two defects remain. In the roar hold (f14-50) it is still one straight blade across the mane's top-left. At takeoff f4-f8 it still touches the halo's lower-left rim. Roar and takeoff are both 8.0 FIX. Land now passes.

---

## What I looked at

- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; round 9 `_review/EclipseSeraph_review9.md`; builder `EclipseSeraph/CLIP_NOTES.md` (review-9 section, "clip round 7").
- Source `pets/EclipseSeraph.py` (09:37): far-side overrides grepped. `A_L` keys sit only at TOP (line 417), LOW (line 430), ROAR_W (line 432), BRAKE (line 439) and the takeoff gather (line 602). Nothing else references them.
- Round-10 rod crops (3x): `renders\_rod_check_roar_3x.png` (f14 / f30 / f50), `_rod_check_takeoff_3x.png` (f6 / f10), `_rod_check_land_3x.png` (f7 / f8 / f10 / f12).
- Round-10 game-view sheets (09:38): `_pose_game_roar_sheet.png`, `_pose_game_takeoff_sheet.png`, `_pose_game_land_sheet.png`.
- Round-10 tq and front sheets (09:38): `_pose_tq_roar_sheet.png`, `_pose_tq_takeoff_sheet.png`, `_pose_tq_land_sheet.png`, `_pose_front_roar_sheet.png`, `_pose_front_takeoff_sheet.png`, `_pose_front_land_sheet.png`, `_tiers_check_front_roar_3x.png`.
- Idle, walk, fly and act_wingcascade game sheets (`_pose_game_idle_sheet.png`, `_pose_game_walk_sheet.png`, `_pose_game_fly_sheet.png`, `_pose_game_act_wingcascade_sheet.png`). These are stamped 08:32-08:33, before the 09:37 source change. See the stale-evidence note below.
- Front fly sheet `_pose_front_fly_sheet.png` (08:32): opened this pass, so round-9 TO 9+ 2 is checked.
- Model gate: `_model_sheet.png`, `EclipseSeraph_icon.png`, `renders\_icons_strip_64.png`, `renders\_icons_strip_128.png`.
- NOT opened: tq and front sheets for idle, walk, act_wingcascade, and tq fly. The front cascade sheet was also not opened.
- NOT re-run: headless step 1, halo measurements, blade metric. Builder numbers are taken from `CLIP_NOTES.md` and marked "builder".
- Stale-evidence note: the idle, walk, fly and cascade game sheets were rendered 08:32-08:33, before `pets/EclipseSeraph.py` was saved at 09:37. The grep shows the far-side overrides do not touch those clips, and the builder says their rest and stroke are unchanged. I scored them on those sheets with that caveat (NICE 5).

---

## Per-clip table

| clip | score | why | evidence (`renders\`) |
|---|---|---|---|
| idle (120 f loop) | 8.5 PASS | Calm breath; halo and wings hold; no rods or clipping in the game view. Stamped 08:32 (see stale-evidence note). | `_pose_game_idle_sheet.png` |
| walk (40 f loop) | 8.5 PASS | Legs step; fan held; tail sways; no clipping in the game view. Stamped 08:33. | `_pose_game_walk_sheet.png` |
| fly (28 f loop) | 8.5 PASS | Three strokes read; the approved stroke is untouched. The far upper blade is still thin at f7 (TO 9+ 3), which is not new. Stamped 08:32. | `_pose_game_fly_sheet.png`, `_pose_front_fly_sheet.png` |
| takeoff (28 f) | **8.0 FIX** | Crouch and launch read. The far upper wing fans at f10-14 with 4-5 separate tips and sits clear of the halo at f10. At f4-f8 the far blade still touches the halo's lower-left rim (the 3x crop at f6). | `_rod_check_takeoff_3x.png`, `_pose_game_takeoff_sheet.png`, `_pose_tq_takeoff_sheet.png` |
| land (28 f) | 8.5 PASS | Flare, touch f16, settles into the display fan by f28. Far blade at f7-f8 is narrow (builder metric 6.6 at f8, above the 3-4 rod band) and crosses the mane flank, not the body. | `_rod_check_land_3x.png`, `_pose_game_land_sheet.png`, `_pose_front_land_sheet.png` |
| roar (66 f) | **8.0 FIX** | Halo lifts and tilts; jaw opens; front view shows three tiers per side. The far upper wing is still one straight dark-tipped blade across the mane's top-left at f14, f30 and f50. | `_rod_check_roar_3x.png`, `_pose_game_roar_sheet.png`, `_tiers_check_front_roar_3x.png` |
| act_wingcascade (110 f) | 8.5 PASS | Star fan at f58 / f70; three-tier hold; reverse ripple readable. Stamped 08:32 (see stale-evidence note). | `_pose_game_act_wingcascade_sheet.png` |

**Clips score = lowest clip = 8.0 (roar and takeoff).**

Gate values (builder, `CLIP_NOTES.md` round 10, not re-run): collision_free true; 0 collisions on all seven clips; linear 0; loops closed; walk slide 0.0004; ground minimum -0.013 (takeoff; bar -0.015); roar f30 halo clearance 0.055 (bar 0.050); takeoff halo hidden f0-10 10/10/8/6/4/3/2/1/1/1/2 % (bar 10 %); neck max 6.0 (bar 8); chest vs spine 2.5 (bar 5); largest step 21.6 deg. No head shakes or airborne spins seen in the sheets.

---

## Model

**8.5 PASS.** Round 10 did not change the model. The icon, the 64 px and 128 px strips and the model sheet show no regression. The lion read at 64 px is still partial (TO 9+ 1), so there is no margin above the floor. Colour is on hold and not scored.

---

## Round-9 items

| item | result | evidence |
|---|---|---|
| MUST 1: far upper wing rod (roar 8.0, takeoff 8.0) | **PARTIAL** | Improved, not fixed. Blade width roughly doubled (builder). Still a straight blade across the roar mane and touching the takeoff halo rim at f4-f8. `_rod_check_roar_3x.png`, `_rod_check_takeoff_3x.png` |
| MUST 1 acceptance: game roar f30 and takeoff f10 at 3x show at least three separate feather tips on the far wing | **PASS** | About 4 tips at roar f30 and 4-5 at takeoff f10 on the far upper wing. `_rod_check_roar_3x.png` (middle panel), `_rod_check_takeoff_3x.png` (right panel) |
| MUST 1 acceptance: no straight rod across the mane or the halo rim | **FAIL** | Roar f14-50: the far blade runs straight over the mane's top-left in all three panels. Takeoff f6: the blade touches the halo's lower-left rim. Clear at f10 only. |
| MUST 1 acceptance: takeoff halo hidden at most 10 % over f0-10 | **PASS (builder)** | 10/10/8/6/4/3/2/1/1/1/2 %. Not re-measured. |
| MUST 1 acceptance: front roar f30 still shows three tiers per side | **PASS** | At f30 the upper V, the middle pair and the lower pair read as three separate tiers on both sides. `_tiers_check_front_roar_3x.png`, `_pose_front_roar_sheet.png` |
| MUST 1 acceptance: collision_free, 0 collisions, linear 0, ground >= -0.015 | **PASS (builder log)** | ground -0.013 (takeoff). Not re-run. |
| MUST 1 acceptance: roar halo clearance >= 0.050 at f30 | **PASS (builder)** | 0.055. Not re-measured. |
| MUST 1 acceptance: land f8 rod gone or at most 4 frames | **PASS** | Builder metric at f8 6.6 (round 9: 3.4). The far blade no longer crosses the body in the front view. `_rod_check_land_3x.png`, `_pose_front_land_sheet.png` |
| MUST 1 acceptance: fly stroke (f24-28) and DISPLAY_POSE not touched | **PASS (builder)** | Source keys unchanged; the fly and display frames match the round-9 sheets at sheet scale. |
| TO 9+ 1: lion read at 64 / 128 px | **PARTIAL (unchanged)** | The cheek ruff was not touched. At 64 px the Seraph still reads as a winged halo creature more than a lion. `_icons_strip_64.png`, `_icons_strip_128.png` |
| TO 9+ 2: front lower-pair beat (C root x 0.29) | **PASS at sheet scale** | The lower pair shows at the flanks at fly f0, f7, f14 and f21, and beats. `_pose_front_fly_sheet.png` (08:32) |
| TO 9+ 3: fly f7 far upper rod | **PARTIAL (unchanged)** | Still a thin blade at f7. Stroke approved, not changed. `_pose_game_fly_sheet.png` |
| TO 9+ 4: far lower group on the card | **PARTIAL (unchanged)** | The far lower tips still read as a cluster. `EclipseSeraph_icon.png` |
| Round-7 items (far lower reach, cut-through, icon and strips, face) | **PASS (not re-measured)** | No regression in the icon, the strips or the model sheet. |

---

## New MUST (block 8.5 on roar and takeoff)

**MUST 1 (still open) - far upper wing (`Wing_A_L`), roar 8.0 and takeoff 8.0.** Two separate defects, each with its own fix.

**(a) Roar mane crossing, f14-f50.**
- **What:** the far blade runs straight from the upper-left across the mane's top at every roar frame. It reads as a rod across the mane, though it now has tips.
- **Where:** `pets/EclipseSeraph.py`, `ROAR_W["A_L"] = (30, -8, 26, 0)` (line 432). Tuple order is (up, fwd, twist, tip).
- **Fix:** raise the far roar wing from up 30 to **36** (first value 30 -> 36). Keep fwd -8, twist 26, tip 0. If the halo or the neck collides, step to 40 (the TOP value).
- **Acceptance:** game roar f14 / f30 / f50 at 3x: the far wing reads as a fan (rod metric at least 7.0 at all three frames) with no straight blade over the mane. Mane visible at f30 at least 0.73 (builder metric). Roar f30 halo clearance at least 0.050. collision_free true.

**(b) Takeoff halo rim touch, f4-f8.**
- **What:** the far blade's upper edge touches the halo's lower-left rim at f4-f8 (the 3x crop at f6). The rim is clear by f10.
- **Where:** `pets/EclipseSeraph.py`, `TOP["A_L"] = (34, -4, 34, -10)` (line 417) and the f6 gather key `A_L=(34, -0.8, 29.2, -9.2)` (line 602). Keep twist 34.
- **Fix:** lower the far takeoff wing from up 34 to **31** in both places (first value 34 -> 31). This moves the blade down and away from the halo. Expected blade width by interpolation between the builder's up-30 and up-34 results (6.4 / 7.1 at up 30, 7.1 / 8.3 at up 34): about 6.6 at f6 and about 7.4 at f10.
- **Acceptance:** at 3x the far blade no longer touches the halo's lower-left rim at f4-f8. Takeoff halo hidden at most 10 % over f0-10 (builder metric). Rod metric at least 6.0 at takeoff f6 and f10, and at least 6.0 at land f6-f8 (TOP also feeds the land flare). Step 1 passes (ground at least -0.015).

**MUST 1 overall acceptance:** after (a) and (b), re-run step 1: collision_free true, 0 collisions on all seven clips, linear 0, ground minimum at least -0.015, roar halo clearance at least 0.050 at f30. The fly stroke (f24-28) and DISPLAY_POSE stay untouched.

---

## TO 9+ list (not required for 8.5)

1. **Lion read at 64 px (round-9 TO 9+ 1, still open).** Lengthen the OBSID cheek ruff by 0.03 (lines 305-306, currently 0.20 / 0.19, so 0.23 / 0.22) so the mane frames the pale muzzle. Check `_icons_strip_64.png` first. Colour stays on hold.
2. **Tq view: the upper wing is a single thin spike.** In the three-quarter view the upper wing reads as one thin spike from takeoff f4-f8 and roar f8-f58 (`_pose_tq_takeoff_sheet.png`, `_pose_tq_roar_sheet.png`). The game camera is clean, so this is not a MUST. Adding one or two tip feathers to `Wing_A` would make it read as a fan from the three-quarter view too.
3. **Fly f7 far upper rod (round-9 TO 9+ 3, unchanged).** Leave it unless the far-side keys clear it without moving the stroke top.
4. **Far lower group on the card (round-8 NICE).** Add one more feather row on `Wing_C_L` so the far lower group reads as a wing.
5. **Re-render the stale clip sheets.** Idle, walk, fly and act_wingcascade (game, tq and front) are stamped 08:32-08:33, before the 09:37 source. Re-render them from the final file so the evidence matches the code.
