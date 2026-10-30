# Eclipse Seraph - model + clip gate review 8 (2026-10-28) - final gate

**Model: 8.5/10 - PASS. Clips: 8.0/10 - FIX.**

The round-7 MUST (far lower wing reach) is met, so the model clears the 8.5 floor with no margin. The clips are held at 8.0 by one visible defect: in the game view the far upper wing's outer feather edge is seen edge-on, so it reads as a straight dark-tipped rod across the mane and chest in the roar hold, and across the halo rim at takeoff f10. It is one twist change to fix (MUST 1).

---

## What I looked at

- Index card `EclipseSeraph_icon.png` (06:09), with 3x crops of both flanks and the face (scratch in `C:\Users\ventu\AppData\Local\Temp\r8scratch`; nothing written to the pet or review folders).
- Strips `renders\_icons_strip_64.png` and `_128.png` (7 cells: Seraph, Solar Lion, Frostcrown, Griffin, Celestial Dragon, Cvetibara, Cosmic Leviathan), `_icons2_strip_64/128.png`, `renders\_model_sheet.png`, `renders\idle_front.png`.
- All 21 clip sheets: `renders\_pose_<tq|game|front>_<idle|walk|fly|takeoff|land|roar|act_wingcascade>_sheet.png`.
- 3x crops of game roar f30, game land f8, game takeoff f10, game fly f7, game cascade f40, tq idle f0 head, front fly f0 and f14.
- `_ALL_FIERCE_progress.png` (dated 10-09, before the Glacier pets, so it has no Frostcrown or Leviathan; the 7-cell strips cover those).
- `ANIM_REFS.md`, `CLIP_NOTES.md`, `MODEL_NOTES.md` (round 8), and the vault `Model Review Checklist.md` and `Creature Animation.md`.

**Freshness check.** `pets/EclipseSeraph.py` is dated 05:42:00. The `_scratch\full_step1.txt` run is 05:43:56, the latest headless log `_scratch\clips_last.txt` is 05:46:52, the sheets are 05:46-05:47, and the icon and strips are 06:09. All renders post-date the source. The round-8 constants are present in the source: far C tip (0.835, 1.228, 1.05) at line 99; lower-pair fly stroke top 24 / bottom -14 at line 527; takeoff gather TOP A (40, 4, 24, -10) at line 416; cheek ruff 0.20 / 0.19 at lines 305-306. The visibility log `_scratch\vis_final.txt` (05:44) gives rest x_min -0.171, matching the builder.

**Counts I redid myself:**
- 64 px punch, strip cells, tile background removed (see the Round-7 table).
- Far-lower-tip reach, same 3x crop scale as the round-7 crop.
- Collisions and ground, from `clips_last.txt`: `collision_free` true, `collisions` {}, linear 0 on all seven clips, loops closed, ground minimum -0.013 (takeoff f12).
- Tris 11,336 (`tris_body` in `clips_last.txt`).

**Taken from the builder, not re-run:** the 0-hit cut-through ray test, the pose-limit numbers (neck 6.0, chest vs spine 2.5, head + neck pitch-up 15, largest step 21.6 deg), halo clearance (0.055), the rest-pose delta, and the dark share on the raw render.

---

## Round-7 items

| item | result | evidence |
|---|---|---|
| MUST 1 (b): far lower tips >= 0.15 H outside the mane | **PASS** | `icon_left_3x.png` (this round) vs the round-7 crop at the same 3x scale. Tips sit about 56-62 px left of the muzzle edge at 512 px (round 7: about 36-38 px). H is about 320 px, so about 0.17-0.19 H (target 0.15 H, about 48 px). Eyeballed from crops, so +/- 4 px. |
| MUST 1 (a): six wings countable on the card | **PASS** | Card: far upper fan above the halo; far middle fan left of the halo; far lower group left of the muzzle (three tips); near upper blade; near middle horizontal; near lower reaching past the foreleg. The far lower group is still the weakest (three tips, not a full wing). |
| MUST 1 (c): cut-through 0 hits; all clips collision-free | **PASS** | `clips_last.txt`: collisions {}, collision_free true (cut-through ray test taken from the builder). |
| MUST 1 (d): icon and 64 / 128 strips re-rendered | **PASS** | Dated 06:09, after the source (05:42). |
| Front view, three tiers per side | **PASS** | `idle_front.png`, `_pose_front_idle_sheet.png`, `_pose_front_act_wingcascade_sheet.png`. |
| Rest pose not crowded at the face (tq) | **PASS** | `tq_idle_f0_head_3x.png`: the far tips sit clear to the left of the muzzle. The reach moved out, not forward. |
| MUST 2 punch vs Solar Lion (64 px) | **PASS** | My count, strip cell 0 vs cell 1, tile background (52,62,74) removed, outline in: Seraph mean S 0.406, share S>0.35 65.0 % (builder 0.406 / 64.9 %); Solar Lion 0.391 / 56.4 % (builder 0.391 / 56.5 %). Frostcrown 0.379 / 57.5 %, Griffin 0.342 / 45.4 %. Seraph's lead holds. Near-white on the strip cell 10.4 % (guard 30 %). |
| Halo clearance (rest, roar peak) | **PASS (builder)** | 0.055 / 0.055 per builder; not re-measured. |
| Face: muzzle no longer a white cat muzzle | **PASS** | `icon_face_4x.png`: lilac-grey muzzle, only the chin pale, black nose, red slit eyes under heavy OBSID brows. |
| Lion read at 64 / 128 px | **PARTIAL (unchanged)** | At 64 px the Seraph reads as a winged creature with a halo; Solar Lion reads as a lion at the same size. The 0.03 longer cheek ruff is not visible on the card. Carried as TO 9+ 1. |
| Halo unoccluded at launch (f10-20) | **PARTIAL, now a clip item** | Game takeoff f10: far upper rod crosses the halo's left rim (`game_takeoff_f10_3x.png`). f13-17 clear of the gold. Folded into MUST 1 (clips). |
| Front fly lower beat | **PARTIAL (unchanged)** | `front_fly_f0_3x.png` / `_f14_3x.png`: the lower pair reads as tucked blades behind the middle pair, not a separate beat. Carried as TO 9+ 2. |
| Tris <= 15k | **PASS** | 11,336 (`clips_last.txt`). |
| Colours (violet vs lilac-ivory) | **Not scored** | On hold per lead ruling. |

---

## Clips

| clip | score | why | evidence (`renders\`) |
|---|---|---|---|
| idle (120 f loop) | 8.5 | Calm breath; halo and wings hold; no rods or clipping in the game or front views. Motion is subtle (four snapshots look nearly alike). | `_pose_game_idle_sheet.png`, `_pose_tq_idle_sheet.png`, `_pose_front_idle_sheet.png` |
| walk (40 f) | 8.5 | Lateral-sequence legs step; back level; wings held in the fan; tail sways; no clipping. | `_pose_game_walk_sheet.png`, `_pose_tq_walk_sheet.png` |
| fly (28 f) | 8.5 | Three strokes read as tiers in front and game views. Far upper blade is a rod at f7 for a few frames (TO 9+ 3). Front lower beat partial (TO 9+ 2). | `_pose_front_fly_sheet.png`, `_pose_game_fly_sheet.png`, scratch `game_fly_f7_3x.png` |
| takeoff (28 f) | **8.0 FIX** | Crouch and launch read. The far upper wing is a straight rod across the mane at f10-13 and touches the halo rim at f10. | `_pose_game_takeoff_sheet.png`, scratch `game_takeoff_f10_3x.png` |
| land (28 f) | 8.5 | Flare, touch f16, settles into the display fan by f28. The rod crosses the body only at f8, for a few frames. | `_pose_game_land_sheet.png`, scratch `game_land_f8_3x.png` |
| roar (66 f) | **8.0 FIX** | Halo lifts and tilts (tq f14 / f30); jaw opens in the front view. But the far upper rod crosses the mane and chest in the game view for about 36 frames (f14-50). | `_pose_game_roar_sheet.png`, `_pose_tq_roar_sheet.png`, `_pose_front_roar_sheet.png`, scratch `game_roar_f30_3x.png` |
| act_wingcascade (110 f) | 8.5 | Three tiers per side in the front hold (f58-70); star fan in the game view; reverse ripple readable. Far wings read as fans; the near upper spike at f40 is narrow but feathered. | `_pose_front_act_wingcascade_sheet.png`, `_pose_game_act_wingcascade_sheet.png`, scratch `game_cascade_f40_3x.png` |

**Clips score = lowest clip = 8.0 (takeoff and roar).**

Pose and gate checks (builder logs, cross-checked where possible): collision_free true, 0 collisions on all seven clips, linear 0, loops closed (idle, walk, fly), walk slide 0.0004, ground minimum -0.013 (takeoff, bar -0.015), neck 6.0 (bar 8), chest vs spine 2.5 (bar 5), head + neck pitch-up 15 (bar 30), largest step 21.6 deg (under the 60 deg vault rule). No head shakes or airborne spins seen. ANIM_REFS.md cites H1, R5, E1, C1, W0, D3/D5 with frame ranges, which meets the owner's references rule.

---

## MUST list (blocks 8.5 on the clips)

**MUST 1 - the far upper wing rod in roar and takeoff (clips: roar 8.0, takeoff 8.0).**
- **What:** in the game view the far upper wing (`Wing_A_L`, the viewer's left) is rolled so that its outer primary edge faces the camera. Only the leading edge shows, so it reads as one straight dark-tipped rod crossing the mane and chest (roar f14-50, see `game_roar_f30_3x.png`) and the halo rim (takeoff f10, `game_takeoff_f10_3x.png`).
- **Where:** `pets/EclipseSeraph.py`. The upper pair's twist in `TOP["A"]` (line 416, currently 24) is the takeoff gather. Apply the same change to the upper pair's twist keys in the roar hold (roar function, around lines 627-640; the wing fields there are the ones carrying twist for A).
- **Direction:** change the A twist by -12 and by +12 in those keys and test both. Keep the one where the far upper blade shows at least three separate feather rows in the game view. Do not change the approved fly stroke top (f24-28) or the DISPLAY_POSE.
- **Acceptance:**
  - game roar f30 and takeoff f10 re-rendered at 3x: the far upper wing shows at least three separate feather rows, and no straight rod crosses the mane or the halo rim;
  - takeoff halo visible at f10 (builder metric: hidden at most 10 % over f0-10);
  - front roar f30 still shows three tiers per side;
  - headless: collision_free true, 0 collisions on all seven clips, linear 0, ground minimum >= -0.015;
  - the roar halo clearance stays >= 0.050 BU at the f30 peak.

No model MUST: the model holds at 8.5 without a change.

---

## TO 9+ list (not required for 8.5)

1. **Lion read at 64 / 128 px.** Enlarge the MUZZLE pads in `pets/EclipseSeraph.py` line 257 from `(0.085, 0.095, 0.066)` to about `(0.10, 0.11, 0.075)` (+15-20 %), keeping the chin pale and the OBSID ruff unchanged. Check that the card face and the 128 px strip read as a lion.
2. **Front lower-pair beat.** The lower pair (`Wing_C_L/R`, root line 98 at (0.26, 0.06, 1.05)) is hidden behind the middle pair from the front. Move the C root out by 0.03 BU per side (x 0.26 -> 0.29) so it shows beside the flank at the 24 / -14 beat in front fly f0 and f14. Re-run step 1.
3. **Fly f7 far upper rod.** The same edge-on rod shows for a few frames of the fly. Re-check after MUST 1: if the twist change also clears it, keep it; if not, leave the approved fly alone.
4. **Far lower group on the card.** Three tips read as a cluster, not a wing. One more feather row on the far C wing would make it read as a wing (NICE).

---

## Pass / fail checklist (round 8)

**Model**

| item | result |
|---|---|
| Round-7 MUST 1: far lower reach >= 0.15 H | PASS (about 0.17-0.19 H) |
| Six wings countable on the card | PASS |
| Front view, three tiers | PASS |
| Rest pose not crowded (tq) | PASS |
| Punch vs Solar Lion (my count) | PASS (0.406 / 65.0 % vs 0.391 / 56.4 %) |
| Tris <= 15k | PASS (11,336) |
| Step 1 (collision, linear, loops, ground) | PASS (headless log) |
| Lion read at 64 / 128 px | PARTIAL (TO 9+ 1) |
| Front lower beat | PARTIAL (TO 9+ 2) |

**Clips**

| item | result |
|---|---|
| Collisions 0 on all seven clips | PASS |
| Ground >= -0.015 | PASS (-0.013) |
| Pose limits (neck, chest vs spine, pitch-up) | PASS (builder logs) |
| No head shakes or airborne spins | PASS |
| Acts in place and end at rest | PASS (builder) |
| ANIM_REFS rule | PASS |
| Halo unoccluded at launch (f10-20) | FAIL (rod crosses rim at f10; MUST 1) |
| Roar: no poke or rod across the mane | FAIL (MUST 1) |
| Idle, walk, land, cascade | PASS |
