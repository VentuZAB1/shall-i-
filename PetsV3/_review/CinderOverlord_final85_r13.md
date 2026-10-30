**Model: 8.3/10 - REVISE. Clips: 8.3/10 - NOT APPROVED (lowest clip act_molt 8.3; idle 8.5, walk 8.5, roar 8.5).**

# Cinder Overlord - FINAL 8.5 GATE, ROUND 13 (fresh reviewer, 2026-10-28)

Round 13 is the owner's chosen fix from round 12: a COBRA HOOD on the raised cobra stance. The hood is real and
clean in the front and three-quarter views, and the gold gate is met. But the owner's core question is still
answered "not yet" from the game camera. Behind and above, at phone size, the hood fuses with the dark frill and
the crown into one obsidian mass on top of a red column. The round-12 snout lump is still there, the Cinder is
still slightly under Thunder Rex on area, and the molt head still drops into the coil from the game view. Model
stays under the bar at 8.3.

## 0. What I looked at, and the limits

- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; round-12 review `_review/CinderOverlord_final85_r12.md` (format and MUST list);
  `GLACIER_CONCEPTS.md` owner decisions (names, no Glacier wave); `CinderOverlord/ANIM_REFS.md` (S1 slither, S2 reared
  king cobra as the clip reference).
- Builder notes: `CinderOverlord/MODEL_NOTES.md` (round 12, lines 7-93) and `CinderOverlord/CLIP_NOTES.md` (round 12, lines 11-27).
- Code read in `pets/CinderOverlord.py`: palette lines 19-35 (PLUM_OBS (176,72,54), OBS_D (62,50,64), PALE_S,
  ROSE (20,92,250), LAVA, GOLD); HEIGHT line 15; FRONT / HEAD_LIFT lines 77-80; PAW_CLAW line 213; FRILL lines 222-223
  and cheek / frill spikes lines 536-541 (OBS_D); crown blade table line 586 (centre `0.40`); HOOD constants lines 330-345
  and `cobra_hood()` lines 373-406; SKS nose stations line 508 (0.82 -> 0.066, 0.96 -> 0.028); snout tube lines 512-516;
  idle roll line 761 (`2.2 * sw` per neck bone); act_molt head keys line 830 (`(18, 20.5), (84, 20.5)`).
- Images opened (all of the brief's list, title bars 14:21-14:24, "final 8.5 round 12"): `renders/_hood_back_2x_idle_f0_f20.png`,
  `gamelook_game.png`, `gamelook_tq.png`, `_icon_game_64_128.png`, `_icons2_strip_64.png` / `_128.png`, `_cv_idle_game.png`,
  `_cv_idle_front.png`, `../CinderOverlord_portrait_alt.png`, `../CinderOverlord_icon_alt.png`, `_icons_alt_strip_64.png` /
  `_128.png`, `_icons_strip_64.png` / `_128.png`, `close_front.png`, `_close_sheet.png`, `_model_sheet.png`,
  `_pose_tq_sheet.png`, `_molt_r12_front.png`, `_molt_r12_tq.png`, `_cv_roar_front.png`, `_cv_roar_side.png`,
  `_cv_walk_game.png`, `_cv_walk_side.png`.
- Proof text: `_scratch/gate_f85.json` (`gold_gate`, `collision_proof_r12`, `stance_r12`, `icons_64_128`, `history_pre_r12`),
  `coll_probe_r12.txt`, `stance_r12.txt`, `headshare_r12.txt`, `face_id_r12.txt`, `gold_r12.json`.
- Limits: no pixel tool and no Blender run (reviewer rule). Area, gold, clearance and pose numbers are the builder's
  files; I checked them against the code and the images by eye, and they are internally consistent. The vault style notes
  and `FIERCE_GUIDE.md` were not re-read this round; the style bar used is the brief's summary plus the round-12 review.
  The game-camera molt (`_molt_game`) was NOT rendered. The palette is not scored (lead ruling). HEIGHT 11.72 and the hood
  width (|x| 0.64) are accepted (lead ruling).

## 1. The owner's question, answered

**From the GAME camera (behind and above, phone size): not yet a cobra king.** It is a hooded worm with a crown, one
step better than round 12.
- `_cv_idle_game.png` (f0-f105) and `gamelook_game.png`: the neck is still a red column. The hood shows only as a dark
  band directly under the crown, and it is the same obsidian as the frill spikes, the crown sockets and the dorsal
  saddle (`OBS_D` (62,50,64) at `cobra_hood()` back plate, FRILL, cheek spikes, crown sockets, dorsal). From behind
  the hood, frill and crown merge into one dark block. No spread shape reads at 64 px.
- `_icons2_strip_64.png` tile 1 and `_icons_alt_strip_64.png`: a red coil with a gold top and a dark head mass. The
  hood is not separate. The 128 px kit tile (`_icons_alt_strip_128.png`) shows a dark collar behind the head, which is
  better, but the shape reads as a frill, not a cobra hood.

**From the FRONT and 3/4 views: yes, a hooded cobra-dragon.**
- `close_front.png`, `_model_sheet.png` (panel 2), `gamelook_tq.png` and `_cv_roar_front.png` show the two ember
  panels flaring out behind the jaw, with the dark rim, the ribs and the blue spot. This is the clearest cobra read in
  the set.

**Is the hood clean?** Yes in geometry, with two notes.
- Geometry: every hood clearance is >= 0.051 BU; no floating panel, no gap, no poke in any frame. The panels are attached
  to Neck2 and Neck3 and sway with them (`_hood_back_2x_idle_f0_f20.png`).
- Note A: from the side (`_close_sheet.png` panel 2) the lower panel is a thin dark slab edge-on at jaw height. It is
  attached, but it reads as a plate, not a fan.
- Note B: the hood is the same obsidian as the frill and the crown, so the three merge from behind (the game camera).

## 2. Clip table (per-clip floor: the clips score is the LOWEST clip)

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.5 | The cobra sway is upright and level. The hood moves with the neck. Game-camera head gap 50.9-66.0 px. Breath stays small. The sway is still small at phone size (2.2 deg per neck bone, line 761; r11 NICE 3 not done). | `_cv_idle_game.png` (f0-f105), `_cv_idle_front.png`, `_hood_back_2x_idle_f0_f20.png`; `stance_r12.txt` (idle) |
| walk | 8.5 | The slither holds its line. Head gap 61.9-63.2 px, pitch +/-0.6 deg. The tail tip is cropped in the game tile at f8-f40 (lead ruling: framing, not scored). The hood sways with the neck in the side view. | `_cv_walk_side.png`, `_cv_walk_game.png`; `stance_r12.txt` (walk) |
| roar | 8.5 | The jaw opens with white fangs at f30-f44 (side). The head clears the jaw (Jaw|Neck2 0.0769 at f30). The hood does NOT spread for the threat: the same wings show at f0 and f30 in the front view, because the hood is rigidly on the neck. The lowest roar gap is 47.7 px (no gate; observed). | `_cv_roar_front.png`, `_cv_roar_side.png`; `coll_probe_r12.txt` (Jaw|Neck2); `stance_r12.txt` (roar) |
| act_molt | **8.3** | The game-camera head drops to a gap min of **34.8 px** at the hold (f18-f84, head key `20.5` at line 830). The r11 NICE 2 target (>= 50 px) is not done. The molt is not rendered from the game camera. At phone size the blade lift is small. The head reads into the coil from the game view. | `_molt_r12_front.png`, `_molt_r12_tq.png`; `stance_r12.txt` (act_molt screen gap [34.8, 62.4]) |

**Clip floor: min(8.5, 8.5, 8.5, 8.3) = 8.3. NOT APPROVED.** The molt hold is the clip that blocks the 8.5.

## 3. Round-12 items (PASS / PARTIAL / FAIL / OPEN)

| r12 item | result | evidence |
|---|---|---|
| MUST 1, cobra hood (thin plates on Neck2 and Neck3, ember face, obsidian back, rim, ribs, blue eye spot; widest |x| 0.64) | **PARTIAL.** Built as specified and clean. It reads as a cobra hood from the front and 3/4 views. From the game camera it fuses with the frill and crown (same `OBS_D`). It does not give the 64 px read. | `pets/CinderOverlord.py` lines 330-345, 373-406; `close_front.png`; `_model_sheet.png`; `gamelook_game.png`; `_icons_alt_strip_64.png` |
| Hood clearance, all frames: head >= 0.051; jaw >= 0.078; frill / cheek >= 0.089; crown >= 0.462; paws >= 0.485; upper arms >= 0.325; Neck1 >= 0.154; chest >= 0.380 | **PASS.** Each number matches the file: head 0.0509 (idle f96); jaw 0.0783 (roar f32); spikes 0.0894 (idle f34); crown 0.4616-0.4903; paws 0.4855 (roar f44); arms 0.3245 (rounds to 0.325); Neck1 0.1543 (act_molt f85); chest 0.3798 (act_molt f18, rounds to 0.380). | `_scratch/coll_probe_r12.txt` (B_min, HOOD rows); `gate_f85.json` (`collision_proof_r12.hood_clearance_all_frames`) |
| MUST 2, flatter snout (stations 0.82 / 0.96 -> 0.066 / 0.028) | **PARTIAL.** The skull stations are lowered in code (line 508). The front still shows a round red mass under the nostrils, which is not the skull station: it is the lower-face / snout-tube pad part (lines 512-516). The stations are not the visible lump. | `close_front.png` (centre-bottom under the nostrils); `_close_sheet.png` (panels 1 and 3); code line 508 |
| MUST 3, one gold number (game_icon.py `gold_px_portrait_64` = 113, floor 103) | **PASS on the number. Proof tidy still open.** `gold_gate.value` = 113 and `gold_hist` agrees. But `history_pre_r12.gold_method` still reads "Kit counter (game_icon.py) at 64: portrait 91, game 35" and `history_pre_r12.gold_px_64` still carries the 91 field. They are labelled history, but the contradicting text is still in the gate file. | `_scratch/gate_f85.json` (`gold_gate`, `history_pre_r12`); `gold_r12.json` (kit_portrait 113) |
| Snout / nostril re-seat / fangs and roar mouth still work | **PASS.** Fangs and roar mouth read in `_close_sheet.png` panels 2-3 and `_cv_roar_side.png` (f30). | `_close_sheet.png`; `_cv_roar_side.png` |
| Gates: kit collision true (85 pairs); strict run only the 2 shoulder seats (<= 0.0277); crown neighbours >= 0.0307; jaw-neck 0.077; paw-neck 0.148; ground -0.006; loops 0 / 0; stride 5.0089; HEIGHT 11.72 (accepted); tris 13,580; neck <= 7.5 per bone; chest 4.5; head + neck pitch-up <= 4; head share 0.320; game gap idle 51-66 and walk 62-63 px; game area 0.208; portrait area 0.365; paws past body 0.406 / 0.145 | **PASS.** All reproduce from the gate files. The strict run lists only Arm_L|Neck1 and Arm_R|Neck1 (depth 0.0264 rest, 0.0277 max). | `gate_f85.json` (`step1`, `collision_proof_r12`, `stance_r12`, `game_icon_head_share`, `paws_past_body_outline_game_cam_BU`); `coll_probe_r12.txt` |
| Outclass (lead ruling: kit gold + area + the 64 px read) | **Gold PASS. Area FAIL (by a hair). 64 px read FAIL.** Gold: kit 113 vs InfernoPhoenix 93, Ivonrath 25, Thunder Rex 13, Cosmic Leviathan 20. Area: kit 0.365 vs Thunder Rex 0.372 (the Cinder is 2 % under the 1 % secret). The 64 px read is the merge in section 1. | `gate_f85.json` (`icons_64_128`); `_icons_alt_strip_64/128.png` |
| NICE 1 (r12), walk tile framing | **OPEN.** The tail tip is still cropped at f8-f40. Lead ruling: framing, not scored. | `_cv_walk_game.png` |
| NICE 2 (r11 carried), molt head hold; game-view molt render | **FAIL.** Gap min 34.8 px (target >= 50). Head key 20.5 unchanged (line 830). No `_molt_game` render. | `stance_r12.txt`; `CinderOverlord_r12` code line 830 |
| NICE 3 (r11 carried), idle sway at phone size | **OPEN.** Roll still 2.2 per neck bone (line 761). | code line 761; `_cv_idle_game.png` |
| NICE 4 (r12), area over Thunder Rex (centre crown blade 0.40) | **FAIL.** Centre blade still `0.40` (line 586). Kit area 0.365 < 0.372. | code line 586; `gate_f85.json` |
| NICE 5 (r12), claws at game size (PAW_CLAW 0.110) | **OPEN.** Still 0.110 (line 213). | code line 213 |
| NICE 6 (r12), breath | Studio check (lead ruling). Not scored. | - |

## 4. Model score: 8.3 - REVISE

**Holds:**
- The hood is built as specified and is clean: thin panels per side on Neck2 and Neck3, the rim, the ribs, the blue spot,
  and the clearance numbers all reproduce.
- From the front and 3/4 views it reads as a hooded cobra-dragon, which is the best cobra read so far.
- The gold gate is met on one counter (113). Stride, tris, ground, loops, collision and seats are all green.
- Crown neighbours and the head share (0.320) are fixed.

**Blocks 8.5:**
1. **The game camera still reads as a hooded worm with a crown.** The hood, frill and crown share one obsidian and
   fuse at 64 px. (MUST 1.)
2. **The snout front still has a round red lump under the nostrils.** The skull stations are lower; the visible lump is a
   different part. (MUST 2.)
3. **Area is 2 % under Thunder Rex** (0.365 vs 0.372) on the kit portrait, and the molt hold reads into the coil at the
   game camera (act_molt 8.3). (MUST 3, MUST 4.)
4. **Proof hygiene:** the contradicting 91 is still in the gate file's history text. (MUST 5.)

## 5. MUST list (model and clips, all block 8.5)

**MUST 1 (model, the 64 px read): separate the hood from the frill and the crown.** Evidence: `gamelook_game.png`,
`_cv_idle_game.png`, `_icons_alt_strip_64.png`.
- Cause: the hood back plate uses `OBS_D` (62,50,64) (`cobra_hood()`, the `dark` tubes at lines 384-390, `HOOD_DARK` 0.010),
  and so do the frill spikes (lines 539-541), the cheek spikes, the crown sockets and the dorsal saddle.
- Fix: in `cobra_hood()`, change the hood back plate (the `dark` tubes, lines 384-390) from `OBS_D` to the ember
  `PLUM_OBS` (176,72,54). Keep the obsidian rim (`OBS_D`, the `rim` segs, lines 391-396). Change the three ember ribs
  (`B.bar(..., PLUM_OBS, ...)`, line 402) to pale `PALE_S` (222,194,158) so the ribs read on the red plate. Keep the blue spot.
  Geometry does not change, so the clearance proof stays valid; re-run the collision kit gate anyway.
- Pass: in `gamelook_game.png` and the 64 px icon, the hood is a red fan with a dark rim and pale ribs, separate from the
  dark frill and crown. The 64 px tile reads "hooded", not "crowned worm".

**MUST 2 (model): the front snout lump under the nostrils.** Evidence: `renders/close_front.png` (centre-bottom).
- The skull stations at line 508 are already at 0.066 / 0.028 and are not the lump. Find the part with a hide test:
  render the front with the snout tube (`snout = B.tube(...)`, lines 512-516, its +0.004 pads) and the Mouth / Jaw front
  (`_jaw` loft, line 546) hidden, one at a time.
- Flatten the front of the part that is left: the visible half-height under the nostril line <= 0.03 (with the skull
  station 0.028), no round bulb. Keep the fangs and the roar mouth.
- Pass: from the front, no rounded red lump under the nostrils; the snout reads as a wedge.

**MUST 3 (model, outclass area): the kit icon area >= 0.372 (Thunder Rex).** Evidence: `_scratch/gate_f85.json`
(`icons_64_128.kit_portrait.64.area` 0.365).
- Centre crown blade (line 586, `(0.0, 0.40, 0.064, 0, 24)`): height 0.40 -> 0.44 (the r12 NICE 4 value).
- Re-check Crown_3|Head clearance >= 0.02 (the centre blade's socket is `Crown_3`), and the crown neighbours >= 0.02
  (0.0307 now).
- Pass: kit icon area >= 0.372 at 64 px on the icon-3 recipe, gold still >= 103.

**MUST 4 (clips, the molt hold): game-camera head gap >= 50 px at every molt beat.** Evidence: `stance_r12.txt`
(act_molt screen gap min 34.8), `_molt_r12_tq.png` (f34-f84).
- Lower the molt head hold: line 830 `head = [(0, 0), (18, 20.5), (84, 20.5), (100, 3), (110, 0)]`, change `20.5` -> `14`.
  If the gap still drops below 50 px, lower the neck arch on the same beat (the neck keys just below line 830, in `act_molt`).
- Render `_molt_game` from the game camera (the render was never made), and re-measure with `_scratch/stance_probe.py`.
- Pass: game-view gap >= 50 px at every molt beat; the head holds clear of the coil from the game camera.

**MUST 5 (proof): remove the contradicting figure from the gate file.** Evidence: `_scratch/gate_f85.json`,
`history_pre_r12.gold_method` and `history_pre_r12.gold_px_64`.
- Delete the text "Kit counter (game_icon.py) at 64: portrait 91, game 35" and the `gold_px_64` block from the gate file
  (or replace them with one line: "superseded by gold_gate, round 12"). Keep `gold_gate` as the only gold number.
- Pass: the gate file has exactly one gold number that gates (113, floor 103), and no other gold figure under a
  "game_icon.py" label.

## 6. NICE list (not blocking)

1. **Hood spread in the roar (the threat display).** The hood is rigid on the neck, so the roar front shows the same wings
   at f0 and f30. Give each side its own hood hinge (a `Hood_L` / `Hood_R` bone off Neck3, skinned to the hood panels).
   Roll each hinge outward 10-15 deg from f14 to f30 and back to rest by f58. Re-run the hood clearance (>= 0.02) at the
   spread. This is the cobra's threat move and the biggest single gain for the roar.
2. **Hood side slab.** From the side (`_close_sheet.png` panel 2) the Neck2 panel is an edge-on dark slab at jaw height.
   Taper the outer edge of the Neck2 outline (`HOOD_PANELS` lines 339-341, `(1.25, 0.37), (1.30, 0.41)`) so it reads as a fan
   from the side, not a plate.
3. **Idle sway at phone size (r11 NICE 3, carried).** Roll 2.2 -> 3.0 deg per neck bone (line 761); head counter-roll
   -4.4 -> -6.0 deg (line 762). Keep the neck pitch at 1 deg per bone and the head level; re-measure the game head gap
   (must stay >= 50 px).
4. **Walk tile framing.** Pull the walk game camera back about 8 % so the tail tip stays in frame at f8-f40 (lead ruling:
   framing, not a model fault).
5. **Claws at game size.** `PAW_CLAW` 0.110 -> 0.130 (line 213) so the claw read survives at 64 px.
6. **Breath.** Studio check (lead ruling). Not scored.

## 7. Pass / fail checklist

| check | result |
|---|---|
| Model >= 8.5 | FAIL (8.3) |
| Clips, every clip >= 8.5 (lowest clip) | FAIL (act_molt 8.3; idle 8.5, walk 8.5, roar 8.5) |
| Game silhouette reads a hooded cobra at 64 px (owner core test) | FAIL (hood fuses with the frill and crown) |
| Front / 3/4 read: hooded, crowned cobra-dragon | PASS |
| Hood clean: no floating panel, gap or poke (all frames) | PASS (side slab noted, NICE 2) |
| Hood clearance >= 0.02 to every part | PASS (min 0.0509, head) |
| Front face: one taper, no round nose bulb | FAIL (round lump under the nostrils) |
| Fierce eyes and brows; no glints; no smile | PASS (`_close_sheet.png`, `_cv_roar_front.png`) |
| Gold >= 103 at 64 px, one counter | PASS (113) |
| Gate file: no contradicting gold figure | FAIL (91 still in the history text, labelled) |
| Outclass Thunder Rex on kit area (0.372) | FAIL (0.365) |
| Outclass Phoenix / Ivonrath / Thunder Rex / Cosmic Leviathan on kit gold | PASS |
| Tris <= 15k | PASS (13,580) |
| Stride 5.0089; ground >= -0.02; loops 0 / 0; linear 0 | PASS (5.0089; -0.006; 0 / 0; 0) |
| Kit collision (joint-aware, 85 pairs) | PASS (true) |
| Strict run: only the shoulder seats, depth <= 0.035 | PASS (0.0264 rest / 0.0277 max) |
| Crown neighbours >= 0.02 in all clips | PASS (0.0307) |
| Paws >= 0.10 BU past the neck outline (both sides) | PASS (0.406 / 0.145) |
| Paw-to-neck >= 0.02 | PASS (0.148) |
| Head + crown >= 0.30 of figure height | PASS (0.320) |
| Game area >= 0.18 | PASS (0.208) |
| Neck <= 8 deg per bone | PASS (7.5) |
| Chest vs spine <= 5 deg | PASS (4.5) |
| Head + neck pitch-up <= 30 deg | PASS (r12 measure: head pitch-up 4.0 max) |
| Game head gap >= 50 px: idle / walk | PASS (50.9 / 61.9) |
| Game head gap >= 50 px: roar | Observed 47.7 px (no gate set; note) |
| Game head gap >= 50 px: act_molt hold | FAIL (34.8) |
| No head shakes; acts in place; ends at rest | PASS |
| Shoulder seats not visible in any render | PASS (lead ruling accepts them) |
| Palette hygiene | Not scored (lead ruling) |
| Breath | Studio check; not scored |
| HEIGHT 11.72; hood width |x| 0.64 | Accepted (lead ruling) |
| Walk tail-tip framing | OPEN (framing, lead ruling, not counted) |
