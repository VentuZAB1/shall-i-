# Eclipse Seraph - model + clip gate review 9 (2026-10-28) - final gate

**Model: 8.5/10 - PASS. Clips: 8.0/10 - FIX.**

The model holds at 8.5 with no regression from the round-9 changes (muzzle pads +17 %, lower root x 0.29). The clips stay at 8.0 because the same defect is still there: the far upper wing (`Wing_A_L`, the viewer's left) reads as one straight dark-tipped rod across the mane in the roar hold (f14-50) and across the halo's left rim at takeoff (f6-10). The round-9 twist change fixed the near (viewer's right) upper wing only. Score unchanged from round 8.

---

## What I looked at

- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; round 8 `_review/EclipseSeraph_review8.md`; builder `EclipseSeraph/MODEL_NOTES.md` (round 9) and `CLIP_NOTES.md` (round 9).
- Rod checks: `renders\_rod_check_roar_3x.png` (f14 / f30 / f50), `renders\_rod_check_takeoff_3x.png` (f6 / f10).
- Game-view sheets for all seven clips: `renders\_pose_game_<idle|walk|fly|takeoff|land|roar|act_wingcascade>_sheet.png`.
- tq and front sheets for roar and takeoff only (`_pose_tq_roar_sheet.png`, `_pose_tq_takeoff_sheet.png`, `_pose_front_roar_sheet.png`, `_pose_front_takeoff_sheet.png`).
- NOT opened this pass: tq and front sheets for idle, walk, fly, land and act_wingcascade, and `_pose_front_fly_sheet.png`. The front lower-beat item (TO 9+ 2) is therefore unchecked.
- Icon `EclipseSeraph_icon.png`, strips `renders\_icons_strip_64.png` / `_128.png`, `renders\_model_sheet.png`.
- Source `pets/EclipseSeraph.py`: `key()` lines 66-72, `make_wing` / `WC` lines 82-99, `TOP` line 416, `ROAR_W` line 421, roar keys lines 637-641.
- Not re-run: headless step 1, halo measurements, pose limits. Taken from `CLIP_NOTES.md` round 9 and marked "builder" below.
- PIL is not installed here, so I could not enlarge the crops beyond the 3x renders the builder supplied.

---

## Per-clip table

| clip | score | why | evidence (`renders\`) |
|---|---|---|---|
| idle (120 f loop) | 8.5 | Calm breath; halo and wings hold; no rods or clipping in the game view. Motion is subtle. | `_pose_game_idle_sheet.png` |
| walk (40 f loop) | 8.5 | Legs step; fan held; tail sways; no clipping in the game view. | `_pose_game_walk_sheet.png` |
| fly (28 f loop) | 8.5 | Three strokes read in the game view. Far upper blade is a rod at f7 for a few frames (TO 9+ 3). Approved stroke left alone. | `_pose_game_fly_sheet.png` |
| takeoff (28 f) | **8.0 FIX** | Crouch and launch read. The far upper blade is a straight dark-tipped rod from f6 to f13 and crosses the halo's left rim at f6-f10. The near upper wing now fans. | `_rod_check_takeoff_3x.png` (f10 right panel), `_pose_game_takeoff_sheet.png`, `_pose_tq_takeoff_sheet.png` |
| land (28 f) | 8.5 | Flare, touch f16, settles into the display fan by f28. The far rod crosses the body at f8 for a few frames, as in round 8. | `_pose_game_land_sheet.png` |
| roar (66 f) | **8.0 FIX** | Halo lifts and tilts; jaw opens; front view shows the upper wings spread. The far upper blade is one straight dark-tipped rod across the mane and chest, f14-50, in every panel of the 3x check. The near upper wing shows a feather fan at f14 / f30 / f50. | `_rod_check_roar_3x.png` (all three panels), `_pose_game_roar_sheet.png`, `_pose_tq_roar_sheet.png`, `_pose_front_roar_sheet.png` |
| act_wingcascade (110 f) | 8.5 | Star fan in the game view at f58 / f70; three-tier hold; reverse ripple readable. | `_pose_game_act_wingcascade_sheet.png` |

**Clips score = lowest clip = 8.0 (takeoff and roar).**

Gate values (builder, `CLIP_NOTES.md` round 9, not re-run): collision_free true, 0 collisions on all seven clips, linear 0, loops closed, walk slide 0.0004, ground minimum -0.013 (takeoff; bar -0.015), neck 6.0 (bar 8), chest vs spine 2.5 (bar 5), head + neck pitch-up 15 (bar 30), largest step 21.6 deg (under 60). No head shakes or airborne spins seen in the sheets. ANIM_REFS rule met per the builder.

---

## Model

**8.5 PASS.** The round-9 changes show no regression in the icon, the 64 / 128 px strips or the model sheet. The lion read at 64 px is still partial (TO 9+ 1), so there is no margin above the floor. The colour is on hold and not scored.

---

## Round-8 items

| item | result | evidence |
|---|---|---|
| MUST 1 (clips): far upper rod in roar and takeoff | **FAIL** | the near wing fanned; the far wing is still a straight rod. `_rod_check_roar_3x.png`, `_rod_check_takeoff_3x.png` |
| MUST 1 acceptance: game roar f30 and takeoff f10 show at least three separate feather rows on the far upper wing; no straight rod across the mane or halo rim | **FAIL** | same crops. Mane and rim are still crossed. |
| MUST 1 acceptance: takeoff halo visible at f10 (hidden at most 10 % over f0-10) | **PASS (builder)** | builder 2 % at f10. Visually the rod still touches the rim at f6-f10. |
| MUST 1 acceptance: front roar f30 still shows three tiers per side | **PARTIAL** | upper and middle tiers read at sheet scale; the lower pair is not resolvable in `_pose_front_roar_sheet.png`. |
| MUST 1 acceptance: collision_free true, 0 collisions, linear 0, ground >= -0.015 | **PASS (builder log)** | ground -0.013 (takeoff). Not re-run. |
| MUST 1 acceptance: roar halo clearance >= 0.050 at f30 | **PASS (builder)** | 0.055 (builder). Not re-measured. |
| Round-7 items (far lower reach, cut-through, icon and strips, face) | **PASS (not re-measured)** | unchanged in silhouette on the icon and the model sheet. |
| TO 9+ 1: lion read at 64 / 128 px | **PARTIAL** | muzzle pads +17 % (builder). The 128 px cell shows a pale muzzle under a dark mane; at 64 px the Seraph still reads more as a winged halo creature than a lion. `EclipseSeraph_icon.png`, `_icons_strip_128.png`. |
| TO 9+ 2: front lower-pair beat (C root x 0.26 -> 0.29) | **NOT CHECKED** | `_pose_front_fly_sheet.png` not opened this pass. Builder says the root moved. |
| TO 9+ 3: fly f7 far upper rod | **PARTIAL (unchanged)** | `_pose_game_fly_sheet.png` f7 still shows a rod-like blade from the upper left. The fly stroke is approved and was not changed. |
| TO 9+ 4: far lower group on the card | **PARTIAL (unchanged)** | the far lower tips still read as a cluster. `EclipseSeraph_icon.png`. |

---

## New MUST (blocks 8.5 on roar and takeoff)

**MUST 1 (still open) - far upper wing rod, roar 8.0 and takeoff 8.0.**

- **What:** the far upper wing (`Wing_A_L`, viewer's left) is edge-on to the game camera. It reads as one straight dark-tipped rod across the mane and chest in the roar hold (f14-50) and across the halo's left rim at takeoff f6-f10. The round-9 change applied to both wings at once, so the near (right) fan was gained and the far rod stayed.
- **Why it is still there:** `key()` (`pets/EclipseSeraph.py` lines 66-72) applies one twist to both sides with the sign mirrored, so one twist value cannot suit both sides from this camera.
- **Where:** `pets/EclipseSeraph.py`. `TOP["A"]` line 416 (takeoff gather). `ROAR_W["A"]` line 421 (roar hold). The roar keys at lines 637-641 use `mix(..., ROAR_W, ...)`.
- **Fix:** give the far side its own twist. Call the A key separately with `side="L"` and `side="R"` in the takeoff gather and the roar hold. Keep the near side (`side="R"`) at the current -18 twist with the 8 deg sweep back. For the far side (`side="L"`), test these twist values, in this order: -30, +6, +18. Keep the first value where the far upper wing shows at least three separate feather tips in `game roar f30` and `game takeoff f10` at 3x, with the halo rim and the mane clear.
- **Acceptance:**
  - game roar f30 and takeoff f10 at 3x: the far upper wing shows at least three separate feather tips; no straight rod crosses the mane or the halo rim;
  - takeoff halo hidden at most 10 % over f0-10 (builder metric);
  - front roar f30 still shows three tiers per side;
  - re-run step 1: collision_free true, 0 collisions on all seven clips, linear 0, ground minimum >= -0.015, roar halo clearance >= 0.050 at f30;
  - land f8: the rod across the body is gone or lasts at most 4 frames (`TOP` also feeds the land's first flare key).
  - Do not touch the approved fly stroke (f24-28) or the DISPLAY_POSE.

---

## TO 9+ list (not required for 8.5)

1. **Lion read at 64 px.** Make the OBSID cheek ruff longer by a further 0.03 (lines 305-306, currently 0.20 / 0.19) so the mane frames the pale muzzle. Check `_icons_strip_64.png` first. Colour stays on hold.
2. **Front lower-pair beat.** After the C root change, check `_pose_front_fly_sheet.png` at f0 and f14. If the lower pair still hides behind the middle pair, move the C root out another 0.02 per side (x 0.29 -> 0.31) and re-run step 1.
3. **Fly f7 far upper rod.** Unchanged. The fly stroke is approved, so leave it unless the new far-side twist also clears it without moving the stroke top.
4. **Far lower group on the card.** Add one more feather row on `Wing_C_L` so the far lower group reads as a wing (round-8 NICE).

---

## Scope note

The tq and front sheets for idle, walk, fly, land and act_wingcascade were not opened in this pass, and the front fly lower-beat check was skipped. The clip scores for those five rest on the game-view sheets plus the round-8 evidence.
