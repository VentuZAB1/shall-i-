**Model: 8.3/10 - FIX. Clips: 8.5/10 - PASS (lowest clip 8.5; sign-off waits on MUST 3).**

# Cinder Overlord - FINAL 8.5 GATE, ROUND 11 (fresh reviewer, 2026-10-28)

Round 10 did what it set out to do on the paws, the skull frill and the collision proof for those parts. The game camera did not move. From behind and above, at 64 px and 128 px, the Cinder is still a thin red tube with a gold crown on top. The owner's question has the same answer as round 10: it reads as a red worm or eel with a crown, not a dragon-serpent. The jaw is narrower, but the round red nose cap is unchanged and still reads as a bulb. Model stays FIX at 8.3. The owner's decided next step applies: a raised cobra stance (MUST 1).

## 0. What I looked at, and the limits

- Brief `_review/GLACIER_REVIEWER_BRIEF.md`. Round 10 `_review/CinderOverlord_final85_r10.md`. Builder notes `CinderOverlord/MODEL_NOTES.md` (round 10, export 13:14) and `CinderOverlord/CLIP_NOTES.md` (round 10 entry). Gate file `CinderOverlord/_scratch/gate_f85.json` (written 13:22).
- Code read in `pets/CinderOverlord.py`: PAW_BOX line 210, PAW_GX 212, SH_Z 213, FRILL 217-218, paw block 403-412, frill loop 449, SKS and the nose station 418-420, nose cap ring 423, jaw loft 457-458, crown blades 495-496, rig 529-531, check_pairs 548-570, joints 571-589, HEAD_XF line 596.
- Proof files: `_scratch/coll_probe_r10.txt` (the four-clip probe), `_scratch/pawpx_r10.txt` (paw outline distances), `_scratch/headshare_r10.txt`, `_scratch/face_id_r10.png`, `_scratch/b3_bend.png`.
- Images opened, all of them: `renders/gamelook_game.png`, `gamelook_tq.png`, `close_front.png`, `_icon_game_64_128.png`, `_icons2_strip_64.png`, `_icons2_strip_128.png`, `_icons_alt_strip_64.png`, `_icons_alt_strip_128.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `_model_sheet.png`, `_close_sheet.png`, `_pose_tq_sheet.png`, `_molt_r10_front.png`, `_molt_r10_tq.png`, `_cv_roar_front.png`, `_cv_roar_side.png`, `_cv_walk_game.png`, `_cv_walk_side.png`, `CinderOverlord_portrait_alt.png`, `_scratch/face_id_r10.png`, `_scratch/b3_bend.png`.
- Limits: no Blender run and no pixel tool (reviewer rule). Gold, area, clearance and pose numbers are the builder's files. "By eye" means my reading of the PNGs. The pose limits (neck 7.5 per bone, spine 4.5) are the builder's and were not re-measured. The palette is not scored (lead ruling).

## 1. Clip table (lowest clip = 8.5, so Clips = 8.5 PASS, conditional on MUST 3)

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.5 | Head held near level through the 0 / 30 / 60 / 90 beats; the paws sit clear of the chest in the tq beats; breath small; loop 0 / 0. The only strict-run crossings are the arm roots in the neck (seat, MUST 3b). | `renders/_pose_tq_sheet.png` (idle beats); `_scratch/coll_probe_r10.txt` (A2 idle) |
| walk | 8.5 | The lateral S runs head to tail in the side view and holds its line; the paddles do not poke through the body; the close-ups at f12 / f19 / f26 show no pinch at the Body3 bend (`_scratch/b3_bend.png`). The tail tip crops at the bottom of the game tile at f8 / f16 / f24 / f32 / f40. Per the lead ruling that is framing, not a model fault, and it does not drop this clip. | `renders/_cv_walk_side.png`; `renders/_cv_walk_game.png` |
| roar | 8.5 | Crown flare from f14; jaw opens with a dark mouth and white fangs f30-f44 in both views; closes by f58. The jaw-to-neck clearance at f30 is 0.026 (>= 0.02). The crown 3|4 graze at f59 is 0.005 (MUST 3a). | `renders/_cv_roar_front.png`; `renders/_cv_roar_side.png` |
| act_molt | 8.5 | Blades lift one by one; the fan reads from the front at f22-f40; reseat by f100; exact rest at f110. The crown 2|3 graze at f16 is 0.003 (MUST 3a), sub-visual at phone size. | `renders/_molt_r10_front.png`; `renders/_molt_r10_tq.png`; `_scratch/coll_probe_r10.txt` (B_min) |

Headless numbers (builder, `_scratch/gate_f85.json`): kit `collision_free` true (83 pairs, joint-aware); ground_min_z -0.006; linear 0; idle and walk loops 0 / 0; stride 5.0089; tris 11,396; clip keys unchanged (CLIP_NOTES round 10).

Clip proof, the strict run: `coll_probe_r10.txt` `A2_collision_free` is **false**. The strict run (each pair's own hinge only) lists crossings for the arm roots against Neck1, Neck2 and Spine in all four clips, Neck2|Spine in all four, and Body4|Body2 at walk f19 and act f82. It lists no entries for the claws, the head, the jaw or the frill. The builder calls the arm and neck crossings seated and hidden, but the per-frame depths are not in the proof file. That is MUST 3b. The gate file's `collision_free true` is the joint-aware check only and should say so.

## 2. Round 10 items

| item | result | evidence |
|---|---|---|
| R10 MUST 1a, paws bigger (box 0.070 / 0.062 / 0.056, claws 0.110 / 0.020, hand x +/-0.39) | **PASS on numbers.** Near paw 0.378 BU past the neck outline, far paw 0.107 (>= 0.10 both). At game size the paws still read as short sticks, not claws (lower left and right of the neck in the game render). | `pets/CinderOverlord.py` lines 210-212, 403-412 (paw block); `_scratch/pawpx_r10.txt`; `renders/gamelook_game.png`; `renders/_model_sheet.png` (claws visible front and tq) |
| R10 MUST 1b, skull frill (two swept-back obsidian spikes per side, tips 0.20 past the skull, 0.123 from the crown) | **PASS.** Built with `B.spike` on the Head bone (FRILL lines 217-218, loop at line 449). Visible as dark spikes behind the crown in the front close-up and the game render. Clearance numbers from `coll_probe_r10.txt` (SPIKES|Crown_1 0.123 at roar f26). | `pets/CinderOverlord.py` lines 217-218, 449; `renders/close_front.png`; `renders/gamelook_game.png` |
| R10 "dragon, not worm" at 64 px from the GAME camera (the core test) | **FAIL.** The game icon at 64 px and the game tile at 128 px read as a thin red tube with a crown on top: a worm or eel. The frill helps at 128 px, but the silhouette is still one even column from the crown to the tail. Only the three-quarter view (`gamelook_tq.png`, the model sheet's side panel) reads as a serpent-dragon. | `renders/gamelook_game.png`; `renders/_icon_game_64_128.png`; `renders/_icons2_strip_64.png` tile 2; `renders/_icons2_strip_128.png` tile 2 |
| R10 MUST 2a, jaw tip 0.046 / 0.020 -> 0.034 / 0.016 | **PASS.** | `pets/CinderOverlord.py` line 458 |
| R10 MUST 2b, jaw station 0.85 rw 0.098 -> 0.078 | **PASS.** | `pets/CinderOverlord.py` line 457; `_scratch/face_id_r10.png` (visible jaw narrower) |
| R10 MUST 2 pass, one taper from the nostril line to the chin, not a pig snout | **PARTIAL.** The jaw is now narrower than the nose. The round red nose cap (station 1.0 at 0.044 / 0.032, line 420; cap ring at 0.80 scale, line 423) still reads as a round red bulb with two nostrils, with the fangs below it. The builder named this cap as the next lever. | `renders/close_front.png`; `renders/_close_sheet.png`; `_scratch/face_id_r10.png` |
| R10 MUST 3, collision proof covers the paws and the skull | **PARTIAL.** Met for the paws and the skull: the strict run has no claw, head, jaw or frill entries, and the proxy-free clearance is >= 0.02 for paw-to-neck (min 0.148), skull-to-neck (min 0.134), jaw-to-neck (min 0.026) and frill-to-crown (min 0.123). Open: the crown neighbours (Crown_2|3 0.003 at act f16, Crown_3|4 0.005 at roar f59); the arm roots against Neck1 / Neck2 (depths not in the file; Arm_L|Neck2 0.000 at act f12); Body4|Body2 contact at walk f19 and act f82 (hidden in `b3_bend.png`). | `_scratch/coll_probe_r10.txt` (A, A2, B_min); `pets/CinderOverlord.py` lines 548-589 (check_pairs / joints in code) |
| R10 gates: stride 5.0089, head + crown >= 0.30 of figure height, gold portrait_alt >= 103, game area >= 0.18, tris <= 15k, ground >= -0.02, loops 0 / 0 | **PASS.** Stride 5.0089; head + crown 0.306 of figure height (`_scratch/headshare_r10.txt`); gold portrait_alt 127, kit portrait 104, game 45; game area 0.197; tris 11,396; ground -0.006; loops 0 / 0. | `_scratch/gate_f85.json`; `_scratch/headshare_r10.txt` |
| Outclass (lead ruling: judged on kit gold + area + the 64 px read) | **PASS on numbers, PARTIAL on read.** Portrait gold 127 vs InfernoPhoenix 93 and Ivonrath 25 (64 px). Portrait area 0.376 vs Phoenix 0.267, Ivonrath 0.295, ThunderRex 0.372. At 64 px the portrait is a crowned serpent, distinct from the others. The game tile is the weak spot (see the core test). | `_scratch/gate_f85.json` `icons_64_128`; `renders/_icons_alt_strip_64.png`; `renders/_icons_alt_strip_128.png` |

## 3. Model score: 8.3 - FIX

**Holds:**
- The brows and the blue slit eyes read fierce from the front. No glints, no smile, no round eyes.
- Paws now show claws in the model sheet, and the skull frill reads as a dark mane around the crown.
- Gold and area clear the Phoenix and Ivonrath on the portrait icon.
- The jaw is narrower and the visible jaw is about 0.267 BU wide (face ID).
- The collision proof for the paws, skull, jaw and frill is real (proxy-free clearance and strict-run coverage).
- Tris 11,396; stride 5.0089; ground -0.006; loops 0 / 0.

**Blocks 8.5:**
1. **The game camera still reads as a worm or eel with a crown.** The game icon at 64 px and the game tile at 128 px are one even tube. Raising the paws and adding the frill did not change the silhouette. (MUST 1.)
2. **The front still reads as a round nose bulb.** The jaw is narrower now, but the round nose cap is unchanged and still reads as a snout bulb with two nostrils. (MUST 2.)

Answer to the owner's question: from the game camera the Cinder still reads as a red worm or eel with a crown. It becomes a dragon-serpent in the three-quarter and side views. The owner's decided next step is a raised cobra stance (MUST 1).

## 4. MUST list (block 8.5)

**MUST 1 (model): raised cobra stance (the owner's decided next step).** Evidence: `renders/gamelook_game.png`; `_icon_game_64_128.png`; `_icons2_strip_64.png` / `_128.png` tile 2. The head and crown currently sit at the same height as the neck top, so the silhouette is a column.
- Raise the throat and the front neck (`pets/CinderOverlord.py`):
  - `THROAT` line 80: `(0, -0.50, 1.50)` -> `(0, -0.50, 1.68)`;
  - `FRONT[4]` (line 76-77): z 1.16 -> 1.28;
  - `FRONT[5]` (line 76-77): z 1.42 -> 1.60.
- Move the head group with the throat: `HEAD_XF` line 596 pivot `(0, -0.50, 1.50)` -> `(0, -0.50, 1.68)`, and fix its z offset so the head group sits 0.18 higher. Move the jaw pivot `JP` line 452 `(0, -0.55, 1.555)` by +0.18 in z, and the Jaw joint at line 531 to match.
- Head + crown share: a 0.18 rise takes the figure from about 2.10 to about 2.28 BU, so head + crown falls to about 0.28 of figure height. Restore >= 0.30 by raising `HEAD_XF` 1.45 -> about 1.54. Re-measure with `_scratch/head_share.py`.
- Neck pitch: each neck bone <= 8 deg, and the head + neck pitch-up <= 30 deg. Re-measure per bone. The builder's 7.5 per bone (round 4) does not hold automatically after this change.
- Re-run the strict collision run (A2) and the kit run (A) in all four clips, ground >= -0.02, stride 5.0089, loops 0 / 0.
- Pass: in `gamelook_game.png` the head and crown stand clearly above the highest body line, and the neck rises in one cobra arch. A fresh reviewer calls the game icon at 64 px "dragon", not "worm".

**MUST 2 (model): flatten the round nose cap.** Evidence: `renders/close_front.png`; `_close_sheet.png`.
- Nose tip station at line 420: `(1.0, 0.044, 0.032, -0.036)` -> half-height 0.032 -> **0.022** (width 0.044 kept).
- Cap ring at line 423: `skf(1.0)[4] * 0.80` -> `* 0.60` (height only; keep the width at 0.80).
- Keep the nostril pits (line ~ `npt` at -1.07) on the flatter top.
- Pass: from the front, the nose's visible half-height is <= 0.022 and there is no round red bulb below the nostril line. The fangs stay visible, and the mouth still opens in the roar.

**MUST 3 (clips, proof): crown socket gaps and the arm-root / body-bend proof.**
- (a) Crown neighbours. Move Crown_2 and Crown_4 out by 0.018 BU at line 495 `(-0.150, ...)` -> `(-0.168, ...)` and line 496 `(0.150, ...)` -> `(0.168, ...)`. Target Crown_2|3 and Crown_3|4 >= 0.02 in all four clips (now 0.003 at act f16 and 0.005 at roar f59). If Crown_1|2 drops below 0.02, move Crown_1 out by 0.010 (line 495 `-0.300` -> `-0.310`). Re-measure, because MUST 1 changes the head height.
- (b) Documentation. Add to the proof file (`_scratch/coll_probe_r10.txt`, or a round-11 file) the per-frame depths of the strict-run crossings for Arm_L/R vs Neck1 / Neck2 / Spine, Neck2|Spine and Body4|Body2. Each depth must be <= 0.035 BU and must not reach a visible skin, or the seat must change: `SH_Z` at line 213 (r10 tried 0.74) or the Body3 bend amplitude. State in `gate_f85.json` that the strict run is not collision-free as an A2 count, and list the seated contacts by name. Without this the MUST 3 clip sign-off cannot be checked from the file.
- Pass: A and A2 both show no crossings except the listed seats; crown neighbours >= 0.02 in all four clips; the paw, skull, jaw and frill clearances stay >= 0.02 after MUST 1.

## 5. NICE list (not blocking)

1. **Paws at game size.** Widen the claw fan: `PAW_GX` line 212 0.042 -> 0.050. Makes the claws read as claws, not sticks, from the game camera.
2. **Frill length.** `FRILL` lines 217-218: lengths 0.22 / 0.17 -> 0.26 / 0.21, so the mane reads from the game camera. Clearance to the crown must still be >= 0.02 after the change.
3. **Index portrait.** `CinderOverlord_portrait_alt.png` is still a low coil at the molt peak, while the Phoenix stands. Re-frame the portrait camera for the raised cobra stance (MUST 1) so the head and crown show.
4. **Walk tile framing.** Pull back the game-camera walk tile so the tail tip is not cropped at f8 / f16 / f24 / f32 / f40 (lead ruling: framing, not a model fault).
5. **Molt fan at frame scale.** Raise the molt portrait camera slightly so the blade sheds read at game distance (`_molt_r10_front.png` f22-f40 is small).
6. **128 px outclass.** After MUST 1 the gold crown rises. Re-check `_icons2_strip_128.png` tiles 9-10 (Thunder Rex, Cosmic Leviathan) against the Cinder.
7. **Pose limits.** After MUST 1, re-measure every neck bone (<= 8 deg) and the head + neck pitch-up (<= 30 deg) with a fresh probe, not the round-4 numbers.
8. **Breath.** Studio check (lead ruling). Not scored.

## 6. Checklist

| check | result |
|---|---|
| Model >= 8.5 | FAIL (8.3) |
| Clips, every clip >= 8.5 | PASS (idle 8.5, walk 8.5, roar 8.5, act_molt 8.5; lowest 8.5), conditional on MUST 3 |
| Tris <= 15k | PASS (11,396) |
| Stride 5.0089 | PASS |
| Gold >= 103 at 64 px (portrait) | PASS (127) |
| Game area >= 0.18 | PASS (0.197) |
| Head + crown >= 0.30 of figure height | PASS (0.306); AT RISK after MUST 1 |
| Paws >= 0.10 BU past the neck, both sides | PASS (0.378 near, 0.107 far) |
| Paws read as claws at game size | FAIL (stubs at game size) |
| Frill present, clear of the crown | PASS (0.123 clearance) |
| Game silhouette reads dragon at 64 px | FAIL (worm / eel with a crown) |
| Front face: one taper, not a pig snout | PARTIAL (jaw narrower; round nose cap unchanged) |
| Collision proof covers paws and skull | PASS (strict run has no claw / head / jaw / frill entries; clearances >= 0.02) |
| Crown neighbours >= 0.02 | FAIL (0.003 act f16; 0.005 roar f59) |
| Arm-root and body-bend contacts documented in the proof file | FAIL (depths not in `coll_probe_r10.txt`) |
| Gate file states the strict-run result | FAIL (`gate_f85.json` shows only the joint-aware `collision_free true`) |
| Walk tail-tip framing | OPEN (framing, not counted) |
| Palette hygiene | Not scored (lead ruling) |
