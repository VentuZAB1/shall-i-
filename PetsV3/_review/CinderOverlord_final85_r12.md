**Model: 8.2/10 - REVISE. Clips: 8.5/10 - APPROVED (lowest clip 8.5; idle, walk, roar, act_molt all 8.5).**

# Cinder Overlord - FINAL 8.5 GATE, ROUND 12 (fresh reviewer, 2026-10-28)

Round 12 is the raised cobra stance (MUST 1 of round 11). The numbers behind it are real: the head rides higher, the
head + crown share is 0.320, the game-camera gap at idle is 62 px (r10 42), the crown neighbours and the strict seat
proof are fixed, and the nose tip is lower. But the owner's question still has the round-11 answer from the game
camera. Behind and above, at 64 px and 128 px, the Cinder is still a straight, equal-width red column with a crown on
top. It reads as a red worm with a crown, not a reared cobra. The three-quarter view does read as a crowned
serpent-dragon. Model stays under the bar at 8.2.

## 0. What I looked at, and the limits

- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; Creature Style, Model Review Checklist and Creature Animation (vault, 06 Modelling and Art); `FIERCE_GUIDE.md`; `_review/CinderOverlord_plan.md` v2; `GLACIER_CONCEPTS.md` owner decisions; round-11 review `_review/CinderOverlord_final85_r11.md`.
- Builder notes: `CinderOverlord/MODEL_NOTES.md` (round 11, lines 7-97) and `CinderOverlord/CLIP_NOTES.md` (round 11, lines 11-41).
- Code read in `pets/CinderOverlord.py`: HEIGHT line 15; FRONT and HEAD_LIFT lines 77-82; FRAD line 80; PAW_GX line 214; SH_X/SH_Y line 216; EXT caps lines 217-218; FRILL lines 222-223; CR_X lines 224, 503-505; SKS nose stations lines 426-428; cap ring line 431; crown mount line 499; crown blade gold line 510-513; jaw line 464-466; idle lines 665-688; walk lines 691-711; roar lines 714-736; act_molt lines 739-772; rig lines 530-553; check_pairs and joints lines 556-601; HEAD_XF lines 608-609.
- Kit check: `blockkit.py` `head_point` (lines 758-766) and `overlap_report` (lines 988-991). The Head, Jaw and Crown joints in the rig and in the collision proxies are both transformed by HEAD_XF, so the joint-aware gate measures the real hinges (no issue found).
- Images opened, all of them: `renders/gamelook_game.png`, `gamelook_tq.png`, `_icon_game_64_128.png`, `_icons2_strip_64.png`, `_icons2_strip_128.png`, `_cv_idle_game.png`, `_cv_idle_front.png`, `../CinderOverlord_portrait_alt.png`, `../CinderOverlord_icon_alt.png`, `_icons_alt_strip_64.png`, `_icons_alt_strip_128.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `close_front.png`, `_close_sheet.png`, `_model_sheet.png`, `_pose_tq_sheet.png`, `_molt_r11_front.png`, `_molt_r11_tq.png`, `_cv_roar_front.png`, `_cv_roar_side.png`, `_cv_walk_game.png`, `_cv_walk_side.png`. Comparison: `_scratch/stale_r10_renders/hx10_front.png`, `hx10_game.png`.
- Proof text: `_scratch/stance_r11.txt` (against `stance_r10.txt`), `coll_probe_r11.txt`, `coll_depths_r11.json` (per-frame seat depths), `headshare_r11.txt`, `pawpx_r11.txt`, `face_id_r11.txt`, `gold_r11.json`, `gate_f85.json`.
- Limits: no Blender run and no pixel tool (reviewer rule). Gold, area, clearance and pose numbers are the builder's files; I checked their internal consistency and the code lines. "By eye" means my reading of the PNGs. The palette is not scored (lead ruling). HEIGHT 11.72 is accepted (lead ruling), not scored.

## 1. The owner's question, answered

From the GAME camera (behind and above, phone size), the Cinder is **still a red worm or eel with a crown**.
- `gamelook_game.png` and `_icon_game_64_128.png`: the head is hidden under the crown and the frill. What shows is a straight column of about the same width as the body, with a crown on top and a black frill around it. There is no hood and no visible arch. The 64 px tile (`_icons2_strip_64.png`, tile 1) is a red tube with a gold top.
- `_cv_walk_game.png` shows the same column at every walk beat (f0-f40).

From the 3/4 and side views it reads as a serpent-dragon: `gamelook_tq.png`, `_model_sheet.png` (panels 3 and 4), and the portrait. The head now shows a snout, fangs, brow and slit eyes, and the crown sits above the coil.

So the round-12 stance fixed the head height and the head share, but not the silhouette the owner sees. The neck needs a visible cobra flare, which is what the builder's round-11 hood trial was after. It was rejected because a uniform radius scale read as a barrel (`_scratch/r11_hood_trial_rejected.png`). The fix has to be flat ribs, not a radius scale (MUST 1).

## 2. Clip table (lowest clip = 8.5, so Clips = 8.5 APPROVED)

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.5 | The cobra sway is upright with the head held level. Head gap 51-66 px over the loop (r10 28-42). Loop 0 / 0. Breath is small. The f80 tail flick is unchanged. The sway is small at phone size (2.2 deg per neck bone), so the idle reads as nearly still from the game camera (NICE 3). | `renders/_cv_idle_game.png`, `_cv_idle_front.png`; `renders/_pose_tq_sheet.png` (idle beats 0 / 30 / 60 / 90); `_scratch/stance_r11.txt` |
| walk | 8.5 | The slither reads head to tail in the side view and holds its line. The head holds full height through the cycle (gap 62.0-63.3 px, pitch +/-0.6 deg). The tail tip is cropped at the bottom of the game tile at f8, f32 and f40. Per the lead ruling that is framing and does not drop the clip (NICE 1). | `renders/_cv_walk_side.png`; `renders/_cv_walk_game.png` |
| roar | 8.5 | Crown flare visible from the front at f14-f22. Jaw opens with dark mouth and white fangs f30-f44 in the side view. The head clears the neck (Jaw|Neck2 0.077 at f30). Head pitch 10 deg, neck 12 deg (within limits). Closes by f58. | `renders/_cv_roar_front.png`; `renders/_cv_roar_side.png`; `_scratch/coll_probe_r11.txt` (B_min) |
| act_molt | 8.5 | Blades lift one by one. The centre blade and the fan read from the front and the 3/4 view at f22-f40. Reseat by f100, exact rest at f110. Two things are weaker than they look: the lift is small at phone scale, and at the hold the head drops toward the coil in the game view (screen head y 156 -> 180, gap min 34.9 px; r10 min 18.8). That is better than r10 but not the clear head the owner asked for (NICE 2). | `renders/_molt_r11_front.png`; `renders/_molt_r11_tq.png`; `_scratch/stance_r11.txt` (act_molt screen) |

Clip floor: min(8.5, 8.5, 8.5, 8.5) = 8.5 APPROVED. Clips are not the blocker this round.

## 3. Round-11 items (PASS / PARTIAL / FAIL)

| r11 item | result | evidence |
|---|---|---|
| MUST 1a, rise: FRONT[4] 1.28, FRONT[5] 1.60; HEAD_LIFT 0.18; HEAD_XF offset -0.08 -> +0.10; scale 1.45 -> 1.60 | **PASS on numbers.** I confirmed the Head joint lands at 1.60 (rig line 538 + `head_point`, blockkit lines 758-766). | `pets/CinderOverlord.py` lines 77-79, 538, 608-609 |
| MUST 1b, head + crown share >= 0.30 | **PASS 0.320** | `_scratch/headshare_r11.txt`; `gate_f85.json` (head_crown_of_figure_h 0.32) |
| MUST 1c, game gap up from r10 (idle f0 42 px -> 62 px) | **PASS on numbers.** Walk 62-63 px. Molt hold min 34.9 px (new finding, NICE 2). | `_scratch/stance_r11.txt`, `stance_r10.txt` |
| MUST 1d, pose limits: neck <= 8 per bone, chest <= 5, head + neck pitch-up <= 30 | **PASS.** Neck 7.5 per bone (act), chest 4.5 (act), neck sum 22.5 + head 2.0 = 24.5 (act). | `_scratch/stance_r11.txt`; `CLIP_NOTES.md` round 11 table |
| MUST 1e, pass: in the game icon the neck rises in one cobra arch and the 64 px read is "dragon, not worm" | **FAIL.** The neck is a straight equal-width column; no flare; the head is hidden under the crown from the game camera. | `renders/gamelook_game.png`; `renders/_icon_game_64_128.png`; `renders/_icons2_strip_64.png` tile 1; `renders/_cv_walk_game.png` f0 |
| MUST 2a, nose tip half-height 0.032 -> 0.022; cap ring x0.80 -> x0.60 | **PASS on numbers.** | `pets/CinderOverlord.py` lines 428, 431 |
| MUST 2b, pass: no round red bulb below the nostril line; visible half-height <= 0.022 | **PARTIAL.** Lower and flatter than r10 (`hx10_front.png` has a clear round bulb). A rounded red lump still sits under the nostrils. The 0.96 and 0.82 stations keep a round front (line 426-427: heights 0.040 and 0.082 at widths 0.060 and 0.112). | `renders/close_front.png`; `renders/_close_sheet.png` (panel 2, side); `_scratch/stale_r10_renders/hx10_front.png` (r10 reference) |
| MUST 3a, crown neighbours >= 0.02 in all four clips (blades 2/4 at 0.168, 1/5 at 0.310) | **PASS.** Minimum 0.0307-0.0311 (1|2 roar f21; 2|3 idle f26; 3|4 idle f26; 4|5 roar f21). | `pets/CinderOverlord.py` lines 224, 503-505; `_scratch/coll_probe_r11.txt` (B_min) |
| MUST 3b, seats: depth <= 0.035 and not visible; per-frame depths in the file; strict run named | **PASS.** Seat depth 0.0264 at rest, max 0.0277 (walk:10, walk:34). The strict run (A2) lists only Arm_L|Neck1 and Arm_R|Neck1. Per-frame depths are in `coll_depths_r11.json` (the proof text has only rest and max; acceptable). Neck2|Spine and Body4|Body2 depth 0. | `_scratch/coll_probe_r11.txt`; `_scratch/coll_depths_r11.json`; `gate_f85.json` (collision_proof_r11) |
| Chest / Neck2 and Body2 / Body4 caps shortened (no end-cap contacts in bends) | **PASS.** | `pets/CinderOverlord.py` lines 217-218, 356-357 |
| Kit gate (joint-aware, 83 pairs) | **PASS.** collision_free true. Labelled joint-aware in the gate file. | `_scratch/gate_f85.json` step1; `_scratch/coll_probe_r11.txt` (A) |
| NICE 1, claw fan 0.042 -> 0.050 | **PASS on numbers.** Claws read on the 3/4 view, still small at game size. | line 214; `renders/_cv_walk_game.png` |
| NICE 2, frill 0.22 / 0.17 -> 0.26 / 0.21, clear of crown >= 0.02 | **PASS.** Frill to crown 0.135 (roar f44). | lines 222-223; `coll_probe_r11.txt` (SPIKES|Crown_1 0.1349) |
| NICE 3, portrait re-framed to show the head and crown | **PASS.** The portrait shows the crowned head above the coil, a clear improvement on the r10 molt-peak coil. | `CinderOverlord_portrait_alt.png`; `CinderOverlord_icon_alt.png` |
| NICE 4, walk tile framing (tail tip) | **OPEN.** Still cropped at f8, f32, f40. Framing per lead ruling; does not drop the clip. | `renders/_cv_walk_game.png` |
| NICE 5, molt fan at frame scale | **PARTIAL.** Blade sheds are small at the game camera. | `renders/_molt_r11_front.png` |
| NICE 6, 128 px outclass (Thunder Rex, Cosmic Leviathan) | **PASS on gold, PARTIAL on area.** See outclass row. | `renders/_icons_alt_strip_128.png` |
| NICE 7, re-measure pose limits (not the round-4 numbers) | **PASS.** | `_scratch/stance_r11.txt` |
| Outclass (lead ruling: kit gold + area + the 64 px read) | **Gold PASS. Area PARTIAL. 64 px read FAIL.** Kit gold 114 vs InfernoPhoenix 93, Ivonrath 25, Thunder Rex 13, Cosmic Leviathan 20. Area at parity with Thunder Rex: 0.344 vs 0.372 (icon recipe, `gate_f85.json` icons_64_128), 0.374 vs 0.372 (gold window). The 64 px read is the worm problem above. | `_scratch/gate_f85.json`; `_scratch/gold_r11.json` |
| Gate: portrait gold >= 103 at 64 px | **PARTIAL / OPEN.** 112 on the icon-3 recipe, but the same gate file records "Kit counter (game_icon.py) at 64: portrait 91, game 35", and `gold_px_64` shows portrait_alt 91. The file contradicts itself and the gate passes only on the larger number (MUST 3). | `_scratch/gate_f85.json` (`gold_method`, `kit_counter_64`, `gold_px_64`) |

Other gates, all PASS: stride 5.0089; tris 11,460 (<= 15k); ground_min_z -0.006 (>= -0.02); loops 0 / 0; linear 0; paws past the body outline 0.387 near / 0.164 far (>= 0.10); paw-neck 0.148; jaw-neck 0.077; skull-neck 0.197; game area 0.195 (>= 0.18); head + crown 0.320.

## 4. Model score: 8.2 - REVISE

**Holds:**
- The numbers for the stance are real: head + crown 0.32, game gap 62 px, rise 0.18, pose limits, and the head joint placement is consistent (checked through `head_point`).
- Crown neighbours, seats, caps and the strict-run proof are fixed and documented.
- Claws and frill are wider; the portrait shows the head and crown.
- Front eyes and brows read fierce; no glints, no smile.

**Blocks 8.5:**
1. **The game camera still reads as a worm or eel with a crown.** No cobra flare, so the straight column shows from behind. (MUST 1.)
2. **The front snout still has a rounded red lump under the nostrils.** Lower than r10, not a flat wedge. (MUST 2.)
3. **The gold gate is not clearly met.** The gate file gives 112 and 91 for the same kit counter. (MUST 3.)

## 5. MUST list (model, all block 8.5)

**MUST 1 (model): a cobra FLARE visible from the game camera.** Evidence: `renders/gamelook_game.png`, `_icon_game_64_128.png`, `_icons2_strip_64.png` tile 1.
- Add a pair of flat, studded hood ribs on each side of Neck2 and Neck3, built in the front-rise loop (`pets/CinderOverlord.py` lines 374-384). Each rib is a tapered block (role limb or mass) in the front plane (x-direction), lying across the neck side from the top of Neck2 down to Neck1. They should stick out about 0.12 BU beyond the neck side at their widest, so the neck's half-width at Neck2 grows from 0.231 (line 80) to about 0.35 (about 1.5x).
- Do NOT scale the neck radius. The r11 trial (radius x2.1) read as a barrel.
- Keep the head above the ribs. Re-run the strict and kit collision runs. Every rib-to-crown, rib-to-frill and rib-to-cheek clearance must be >= 0.02. Paw-to-neck must stay >= 0.148.
- Pass: in `gamelook_game.png` the neck flares below the head, and the 64 px tile reads a hooded crown above a coil. A fresh reviewer calls it "cobra / dragon", not "worm".

**MUST 2 (model): flatten the snout front.** Evidence: `renders/close_front.png`, `_close_sheet.png` panel 2 (side).
- Station `(0.82, 0.112, 0.082, -0.026)` at line 427: half-height 0.082 -> 0.066 (width kept).
- Station `(0.96, 0.060, 0.040, -0.034)` at line 427: half-height 0.040 -> 0.028 (width kept).
- The tip at line 428 (0.022) and the cap ring at line 431 (x0.60) stay as they are.
- Re-seat the nostril pits (line 452, `surf_hit`) on the lower top.
- Pass: from the front, visible half-height below the nostril line <= 0.03, with no rounded red lump. The fangs and the roar mouth still work.

**MUST 3 (proof): one gold number, and enough gold.** Evidence: `_scratch/gate_f85.json` (`gold_method`, `kit_counter_64`, `gold_px_64`).
- Re-run the game_icon.py kit counter on the export renders. State in `gate_f85.json` which counter the >= 103 gate uses, and remove the contradicting figure.
- If the game_icon.py counter gives < 103 (it gave 91 for the portrait), add at least +12 gold px at 64 px. Options: centre-blade nib 0.17 -> 0.22 (line 513), or the centre gold side frames gw0 0.038 -> 0.044 (line 510). Re-render `_icons_alt_strip_64.png`.
- Pass: one counter, >= 103, written once in the gate file.

## 6. NICE list (not blocking)

1. **Walk tile framing.** Pull the game camera back about 8 % or re-centre the walk tile so the tail tip stays in frame at f8, f16, f24, f32, f40. Lead ruling: framing, not a model fault.
2. **Molt hold: keep the head clear.** The game-view head drops to screen y 180 (gap min 34.9 px; 62 at rest). Reduce the molt head hold (line 748, `head` keys: 20.5 -> about 14) or the neck arch (line 747), then re-measure with `_scratch/stance_probe.py`. Target gap >= 50 px at every molt beat. Also render the molt from the game camera (`_molt_game`) and send it to the next round.
3. **Idle sway you can see at phone size.** Roll 2.2 -> 3.0 deg per neck bone (line 679); head counter-roll -4.4 -> -6.0 deg (line 680). Keep the neck pitch at 1 deg per bone and the head level. Re-measure the head gap (must stay >= 50 px).
4. **Area over Thunder Rex.** Centre crown blade height 0.40 -> 0.44 (line 504, `(0.0, 0.40, 0.064, 0, 24)`). Re-check Crown_3|Head clearance >= 0.02. Icon area target >= 0.37 on the icon-recipe method.
5. **Claws at game size.** `PAW_CLAW` 0.110 -> 0.130 (line 213) so the claw read survives at 64 px. Optional.
6. **Breath.** Studio check (lead ruling). Not scored.

## 7. Checklist

| check | result |
|---|---|
| Model >= 8.5 | FAIL (8.2) |
| Clips, every clip >= 8.5 | PASS (idle 8.5, walk 8.5, roar 8.5, act_molt 8.5; lowest 8.5) |
| Tris <= 15k | PASS (11,460) |
| Stride 5.0089 | PASS |
| Ground >= -0.02; loops 0 / 0; linear 0 | PASS (-0.006; 0 / 0; 0) |
| Kit collision (joint-aware, 83 pairs) | PASS (true) |
| Strict run: only the shoulder seats, depth <= 0.035, named in gate | PASS (0.0264 / 0.0277) |
| Crown neighbours >= 0.02 in all four clips | PASS (0.0307) |
| Paws >= 0.10 BU past the neck outline, both sides | PASS (0.387 / 0.164) |
| Paw-to-neck >= 0.02 | PASS (0.148) |
| Head + crown >= 0.30 of figure height | PASS (0.320) |
| Frill clear of crown >= 0.02 | PASS (0.135) |
| Game area >= 0.18 | PASS (0.195) |
| Gold >= 103 at 64 px (portrait) | PARTIAL (112 on icon recipe; 91 on game_icon.py per the gate's own note) |
| Neck <= 8 deg per bone | PASS (7.5) |
| Chest vs spine <= 5 deg | PASS (4.5) |
| Head + neck pitch-up <= 30 deg | PASS (24.5) |
| No head shakes; acts in place; end at rest | PASS |
| Game silhouette reads cobra / dragon at 64 px (owner core test) | FAIL (worm with a crown) |
| Front face: one taper, no round nose bulb | PARTIAL (lower than r10; rounded lump remains) |
| Outclass the secrets: gold, area, 64 px read | PARTIAL (gold PASS; area at parity with Thunder Rex; read FAIL) |
| Walk tail-tip framing | OPEN (framing, lead ruling, not counted) |
| Palette hygiene | Not scored (lead ruling) |
| Shoulder seats not visible in any render | PASS (lead ruling accepts them) |
