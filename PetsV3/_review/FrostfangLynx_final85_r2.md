# Frostfang Lynx - FINAL 8.5 GATE, round 2 (2026-10-28)

## Verdict
- **Model: 8.5 / 10 - PASS** (at the bar; no MUST left, NICE/TO 9+ only)
- **Clips: 8.0 / 10 - FIX** (two MUSTs, C1 and C2, both small and codeable)
- Overall: **FIX** (clips only). Re-send the clip renders after C1-C2; the model is ready to ship as it is.

Round 1 was 7.5 model / 7.0 clips. The round-2 build fixed every round-1 item and the T1-T3 items: one dorsal band, coat-coloured paws with a thin sole (game SNOW 3.8 %), ICE on fangs, chest points, throat, elbow tufts and 60 % of the cheek ruff (game ICE 3.5 %), frost-silver coat, 18 deg stare, deeper crouch, longer claws, -55 deg claw open, -20 deg toe roll, idle sway and breath.

## What I looked at
- Round-2 renders (all dated 01:01-01:03): `renders/_model_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `game_view.png`, `_pose_tq_sheet.png`, `_pclose_tq_sheet.png`, `_pclose_side_sheet.png`, `pclose_game_act_clawflex_50.png`, `_throat_f85.png`.
- `_scratch/clawtmp/claw_paw_f85.png` (claw fan at f0 / f50 / f85), `_scratch/coat/_coat_game.png` (warm / sand / frost).
- Gates: `_scratch/fullcheck.json` (collision_free true, ground_min_z -0.002 worst, loops 0.0), `_scratch/gate5.log` (game shares), `_scratch/export.log`, `_scratch/clipmetrics.json` (act neck 7.36, chest vs spine 3.35).
- Source `pets/FrostfangLynx.py` (dorsal band, chest seg 174-175, paw sole, claw spike 271, idle breath 437, idle sway 445, act drop 513, claw open 524, toe roll 539) and `_scratch/patch_f85_clips.py`.
- Not checked: the flat palette PNGs (used the gate5 shares), the per-frame PNGs beyond the sheets, the .blend.
- Note: `CLIP_NOTES.md` has no round-2 clip section (the crouch, claw, idle and stare numbers are only in the source and the patch script). Documentation only, not a gate.

---------------------------------------------------------------------------------------------------------------------
## 1. Model: 8.5 / 10 (PASS)

**What now works (round-1 items closed):**
- **One dorsal band.** `game_view.png` shows one dark stripe from nape to tail root. No tiles, no gaps. Round-1 M1 closed.
- **Paws.** Coat colour with a thin white sole (line ~288-290). In the front and side renders the feet read as paws, not white boots. The white reads only as a sole line. Round-1 M2 closed.
- **Frost accent.** ICE is on the fangs, the cheek-ruff tips (60 %), the chest points, the throat tufts and the elbow tufts. The ears are untouched (no horn read at 128 px). Game ICE 3.5 %. Round-1 M3 closed.
- **Coat.** Frost-silver (168,176,188) with slate spots. At 64 px and 128 px the strip reads as a snow lynx, next to the Ice Mammoth (teal) and Glacier Yeti (navy). It is distinct from the Panther (violet) and the Raiju (blue). The face keeps the fierce read: black sockets, cyan slits, heavy V brows, ICE fangs.
- **Stud skin** is consistent. Ice claws and fangs are smooth (`role=detail`). Tris 7,772 (cap 15k).

**Why not higher (NICE, not gates):**
1. **Shin socks (line ~259, SNOW 0.060 x 0.064, 0.035 tall).** From the side and game views the white ankle bands read as white stockings. This is the round-1 NICE item coming back. Trim the sock to 0.02 or make it the sole colour only.
2. **Chest underside seg (line 174-175).** Now rounded and studded (no plank), but from the front it still reads as a light bar between the forelegs. Lower the snow to a 0.02 half-depth, or let it taper into the chest.
3. **Chest ICE points.** The four chest points with ICE tips form a busy column of cyan triangles from the front (`_throat_f85.png`). Keep the outer pair only.
4. **Rosettes.** The slate rings read as dark blotches at 128 px in the side view. They are not yet clearly rings. The share is 21 %, so the coverage is right. This is T1 below.
5. **Coat risk (owner check, not a builder MUST).** The frost-silver is the cool end of the palette. In `game_view.png` and the pose sheets it reads silver-grey, which is near the owner's rejected "grey plastic toy". The slate spots and the cyan accent keep it from reading that way, but the owner should see it in game next to the Mammoth and the Yeti before ship.

---------------------------------------------------------------------------------------------------------------------
## 2. Clips: 8.0 / 10 (FIX)

**What works:**
- **Act: crouch and stare.** The crouch is now visibly lower than idle in `_pclose_tq_sheet.png` (act 30 and 50). The 18 deg stare locks, and the tufts sit flat at -12 deg. Neck 7.36 (limit 8), chest vs spine 3.35 (limit 5), head pitch 0.32 (limit 30). All pass.
- **Act: claw fan.** In `claw_paw_f85.png` the four claws on each paw split into separate cyan wedges at f50 and f85, and they close back at rest. In `_pclose_side_sheet.png` (act 30 / 50) the fan reads from the side. Round-2 claim confirmed at close range.
- **Roar** is still the best beat (ruff flare, jaw open to the frost fangs). Unchanged, and it reads.
- **Gates:** collision_free true, linear 0, idle and walk loops closed (0.0), ground_min_z -0.002 at worst (act), idle foot drift 0.0, no head shake.

**Why it is not 8.5 yet:**
- **C1, the claw fan is too small at the game camera.** In `pclose_game_act_clawflex_50.png` the fan is a few small cyan dashes at the paws. The claws are 0.072 units (about 0.43 studs), 0.014 half-width. The fan reads well at tq and side close-up, but not from the default game camera, and that is the one moment the act has to sell itself.
- **C2, the idle is still too quiet at game distance.** The tail sway is 8 deg at the base (line 445). Measured as a tip move with the bobtail's chain, that is about 0.25 studs peak. The breath is 0.01H, about 0.07 studs. The idle reads as a static look-around in the game view.

---------------------------------------------------------------------------------------------------------------------
## 3. MUST list (clips only: to reach 8.5)

### C1 (claws read at game distance)
- Line ~271 (claw spike): length `0.072` becomes `0.095`; half-width `0.014` becomes `0.017`. Keep `ICE` and `role=detail`.
- Line ~524-525: keep `-55.0` (the open angle is right). Keep the centre and outer splay.
- Add the ICE sparkle at each claw event (`claw1` f48, `claw2` f60) on the existing `FX_IceSpark_L` / `R` anchors. That is VFX, so the coordinator does it through the VFX pipeline. Do not hand-make the particle.
- Pass: `pclose_game_act_clawflex_50.png` shows the four claws of each forepaw as separate cyan wedges, readable at the same scale as the body.
- Re-check: collision_free true, ground_min_z >= -0.02 (the longer claws must not dig in), neck <= 8.

### C2 (idle has visible life at game distance)
- Line ~445 (`bobtail(..., sway=...)`): `sway=8.0 * math.sin(2 * math.pi * f / n)` becomes `sway=14.0 * math.sin(2 * math.pi * f / n)`. Tail tip peak about 0.45 studs, visible at game distance. If it reads too slow, use `2 * math.pi * 2 * f / n` (two cycles per 120 f). Both keep the loop closed (sin of 2π or 4π at f=120 is 0).
- Line ~437 (breath): `0.01 * H_U` becomes `0.02 * H_U`, a dip of about 0.14 studs. Keep it dipping below rest so the planted feet do not drift. Re-check the idle foot drift is 0.0.
- Pass: `_pose_tq` idle 26 and idle 62 differ visibly in the tail tip and the back line. Loop seam 0.0.

**Re-send list for C1-C2:** `pets/FrostfangLynx.py` diff; `renders/pclose_game_act_clawflex_50.png`; `renders/pose_tq_act_clawflex_50.png`; `renders/pose_tq_idle_26.png` and `idle_62.png`; the new `_scratch/fullcheck.json`.

---------------------------------------------------------------------------------------------------------------------
## 4. TO 9+ list (higher is better; not needed for 8.5)
- **T1 Rosettes as rings (highest impact).** Make the open centre lighter (a warm or near-white coat tone inside each slate ring, about 0.5 of the ring radius) so each spot reads as a rosette at 128 px. Current rings read as blotches.
- **T2 Quiet the chest.** Keep the outer two chest ICE points only (drop the inner pair). The front view stops reading as a column of spikes.
- **T3 Socks.** Trim the shin socks to 0.02 (see NICE 1). The ankles then read as coat, with the sole as the only white.
- **T4 Owner check on the coat.** Show the owner the frost-silver in game next to the Ice Mammoth and the Glacier Yeti before ship. If it reads grey plastic to the owner, the lead decides between frost and a slightly warmer frost (for example (172,180,192)).

---------------------------------------------------------------------------------------------------------------------
## 5. Pass / fail checklist

**Model (8.5)**

| # | item | result |
|---|---|---|
| 1 | 64 px species reads at once | PASS (frost-silver lynx, cyan tips) |
| 2 | 128 px: no horn or goat read | PASS (ears short; cheek fan reads as frost) |
| 3 | Face fierce: slit eyes, heavy brow, no glint, no smile | PASS |
| 4 | Coat per lead ruling (frost-silver, slate spots) | PASS |
| 5 | Accent ICE at least 3 % in game | PASS (3.5 %) |
| 6 | No floating, plate or tile parts | PASS for the band and paws. PARTIAL for the chest bar (NICE 2) |
| 7 | Not cute (no white boots, no collar of white) | PARTIAL (white shin socks, NICE 1) |
| 8 | Rosettes at least 20 % of the side view | PASS (21 %), readability PARTIAL (T1) |
| 9 | Tris at most 15k | PASS (7,772) |
| 10 | Distinct from Panther, Raiju, Mammoth, Yeti | PASS |
| 11 | Stud skin; details smooth (claws, fangs, sole) | PASS |

**Clips (8.0)**

| # | item | result |
|---|---|---|
| 1 | collision_free true | PASS |
| 2 | Linear 0 in every clip | PASS |
| 3 | Loops closed (idle, walk) | PASS (0.0 / 0.0) |
| 4 | ground_min_z >= -0.02 | PASS (act -0.002) |
| 5 | Pose limits: neck <= 8, chest vs spine <= 5, head pitch <= 30 | PASS (7.36 / 3.35 / 0.32) |
| 6 | No head shake, no airborne frames | PASS |
| 7 | Acts in place and end at rest | PASS (per CLIP_NOTES / fullcheck) |
| 8 | Signature beat readable at game distance | PARTIAL (C1) |
| 9 | Idle has visible life at game distance | PARTIAL (C2) |
| 10 | Walk reads as a cat walk | PASS |
| 11 | Roar reads as a threat | PASS (best beat) |
| 12 | ANIM_REFS rule | PASS as recorded in review 4 (not re-verified here) |

**Scores:** model 8.5 (PASS), clips 8.0 (FIX: C1 and C2).
