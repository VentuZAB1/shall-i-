**Model: 8.3/10 - FIX. Clips: 8.5/10 - PASS.**

# Cinder Overlord - FINAL 8.5 GATE, ROUND 10 (fresh reviewer, 2026-10-28)

Round 9 changes are real: the forearms stand out beside the chest, the skull is broader, the Tail4 ring is gone, and the muzzle tip is narrower. The model still does not clear the bar. From the game camera the Cinder is still a long even tube with a gold crown on top, at 64 px and at 128 px. The front still has a round red nose tip with a wider chin tip under it. Model stays FIX at 8.3, down 0.1 from round 9 because the round-9 blocking read did not move. The clips hold at 8.5 on every clip.

## 0. What I looked at, and the limits

- Brief `_review/GLACIER_REVIEWER_BRIEF.md`. Round 9 `_review/CinderOverlord_final85_r9.md`. Builder notes `CinderOverlord/MODEL_NOTES.md` (round 9, export 10:00) and `CLIP_NOTES.md` (round 9 header and entry).
- Gate file `CinderOverlord/_scratch/gate_f85.json` (written 10:02). Numbers below are the builder's, not re-run.
- Code read in `pets/CinderOverlord.py`: lines 210 and 496 (HEAD_WX 1.15 `_xscale`), 341 (ring keep-set), 399 and 401 (claw box and spikes), 408 (skull muzzle stations), 443-444 (jaw loft), 523-526 (arm and claw anchors), 553-565 (collision proxy list), 568 (HEAD_XF).
- Images opened, all loaded: `renders/gamelook_game.png`, `_icon_game_64_128.png`, `_icons2_strip_64.png`, `_icons2_strip_128.png`, `_icons_alt_strip_64.png`, `_icons_alt_strip_128.png`, `_icons_strip_128.png`, `CinderOverlord_portrait_alt.png`, `renders/close_front.png`, `_close_sheet.png`, `_model_sheet.png`, `_cv_walk_game.png`, `_cv_walk_side.png`, `_cv_roar_front.png`, `_cv_roar_side.png`, `_molt_r9_front.png`, `_molt_r9_tq.png`, `_pose_tq_sheet.png`.
- Limits: no pixel tool and no Blender run (reviewer rule). Gold, area and fill numbers are the builder's gate file. "By eye" means my reading of the PNGs. I did not open the Index UI, so I assumed the Index card uses the portrait icon (IndexConfig.PORTRAITS).

## 1. Clip table (lowest clip = 8.5, so Clips = 8.5 PASS)

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.5 | Head held near level through the 0 / 30 / 60 / 90 beats; breath small; the paws sit clear of the chest in the tq beats; loop 0 / 0 per gate. | `renders/_pose_tq_sheet.png` (idle beats); `_scratch/gate_f85.json` `audit.idle` |
| walk | 8.5 | The lateral S runs head to tail in the side view and holds its line; the paws do not poke through the body; stride 5.0089 unchanged. Framing: the game tile crops the tail tip at the bottom edge in f0, f8, f32 and f40 (TO 9+ 3). The neck-side paw stubs read as sticks at game size (MUST 1). | `renders/_cv_walk_side.png`; `renders/_cv_walk_game.png` |
| roar | 8.5 | Crown flare from f14; jaw open with a dark mouth and fangs f30-f44 in both views; closes by f58; no contact with the wider skull. | `renders/_cv_roar_front.png`; `renders/_cv_roar_side.png` |
| act_molt | 8.5 | Blades lift one by one; the fan reads from the front at f22-f40; reseat by f100; no visible contact with the wider skull. The fan is small at frame scale (TO 9+ 5). | `renders/_molt_r9_front.png`; `renders/_molt_r9_tq.png` |

Headless numbers from the builder (`_scratch/gate_f85.json`): `collision_free` true in all four clips; `ground_min_z` -0.006; linear 0; idle and walk loops 0 / 0; stride 5.0089 per 48 f; tris 11,348. The proxy gap behind that claim is MUST 3. The visible check (paws, skull, crown in the four clips) shows no contact, so the clip score stays 8.5. Clip sign-off still waits on MUST 3.

## 2. Round 9 items

| item | result | evidence |
|---|---|---|
| R9 MUST 1a, forearms out (elbow +/-0.40, hand +/-0.36) | **PARTIAL.** Moved out in code (line 523 fallback) and visible in `_model_sheet` (front and 3/4): both paws stand beside the chest with three claws each. From the game camera the arms read as short sticks beside the neck, with stubs on both sides (about x 190-210 and 285-295 in `gamelook_game.png`), so the far side is not hidden. The claw box is still only 0.052 x 0.046 x 0.042 (line 399) and does not read as a claw at 64 px. | `renders/gamelook_game.png`; `renders/_model_sheet.png`; `pets/CinderOverlord.py` lines 399, 401, 523 |
| R9 MUST 1b, head x1.15 in x only, crown kept | **PASS.** `_xscale` on Head, Jaw and Mouth at HEAD_WX 1.15 (lines 210, 496); crown mount untouched. The skull reads broader than the neck from above and from the front. | `pets/CinderOverlord.py` lines 210, 496; `renders/close_front.png` |
| R9 MUST 1c, Tail4 ring removed (two bands on the back) | **PASS.** Ring keep-set (line 341) now keeps only Spine and Body1; the Neck1 band is separate. | `pets/CinderOverlord.py` line 341; `renders/gamelook_game.png` |
| R9 MUST 1 pass, game area >= 0.18 | **PASS.** 0.192 (kit counter 47 px). | `_scratch/gate_f85.json` `icons_64_128.game` |
| R9 MUST 1 pass, collision_free in all four clips | **PARTIAL.** Builder says true. The proxy list does not check the paws or the widened cheeks (MUST 3). | `pets/CinderOverlord.py` lines 553-565 |
| R9 MUST 1 pass, ground >= -0.02, stride 5.0089, re-render | **PASS.** ground -0.006; stride 5.0089; renders 10:00-10:01. | `_scratch/gate_f85.json` |
| R9 MUST 1 core, "dragon, not worm" at 64 px (fresh reviewer) | **FAIL.** `_icon_game_64_128.png` and the game tile in `_icons2_strip_64.png` (tile 2) read as a red worm or eel with a gold crown. The silhouette is one even tube plus the crown. | `renders/_icon_game_64_128.png`; `renders/_icons2_strip_64.png`; `renders/_icons2_strip_128.png` |
| R9 MUST 2a, jaw station 0.85 rh 0.040 -> 0.032 | **PARTIAL.** Height done (line 443: rh 0.032). Width still 0.098, and the jaw tip is still wider than the nose tip (see MUST 2). | `pets/CinderOverlord.py` lines 443-444 |
| R9 MUST 2b, chin 0.02 back | **PASS (builder).** Not measured separately. | `MODEL_NOTES.md` round 9 |
| R9 MUST 2c, nostril pits unchanged | **PASS.** Two black nostril diamonds read in the close-up. | `renders/close_front.png` |
| R9 MUST 2 pass, one continuous taper from nostril line to chin | **FAIL.** The nose tip is still a round red bulb with two nostrils, and the lower jaw below it is a separate red pad with white fangs at each side. Code: the jaw tip is 0.046 wide against the nose tip's 0.044, so the chin overhangs the nose and reads as a second bulb. | `renders/close_front.png`; `renders/_close_sheet.png`; `pets/CinderOverlord.py` lines 408, 443-444 |
| R9 TO 9+ 1, game presence (frill of 2-3 spikes behind the skull) | **OPEN.** Not done. Area is 0.192, so it passes the floor, but the top silhouette is still a single crown. | `renders/gamelook_game.png` |
| R9 TO 9+ 2, walk framing (tail crop) | **OPEN.** The tail tip still crops at the bottom of `_cv_walk_game.png` at f0, f8, f32 and f40. | `renders/_cv_walk_game.png` |
| R9 TO 9+ 3, outclass the 1% secrets | **OPEN.** At 128 px Thunder Rex and Cosmic Leviathan still read bigger and flashier. The Cinder's only bright read is the gold crown. | `renders/_icons2_strip_128.png` tiles 9-10 |
| R9 TO 9+ 4, Index card pose | **OPEN.** The portrait is still a low coil at the molt peak, while the Phoenix stands. Fill 0.91 (Phoenix 0.91, Ivonrath 0.67). | `CinderOverlord/CinderOverlord_portrait_alt.png` |
| R9 TO 9+ 5, hygiene (GLACIER_CONCEPTS swatches) | **FAIL (stale).** `_review/GLACIER_CONCEPTS.md` line 46 and line 116 still list the plum body #B684AC, rose vents #FF6096 and "Plum-obsidian serpent, rose lava vents". Not scored, but fix before the owner reads it. | `_review/GLACIER_CONCEPTS.md` lines 46, 116 |
| R9 TO 9+ 6, pose limits | **Not re-measured** (no Blender run). Builder: neck 7.5 per bone (limit 8), spine 4.5 (limit 5). | `CLIP_NOTES.md` round 9 |
| R9 TO 9+ 7, breath | Studio check (lead ruling). Not scored. | |

## 3. Model score: 8.3 - FIX

**Holds:**
- The brows and the blue slit eyes read fierce from the front. No glints, no smile, no round eyes.
- Gold and area clear the Phoenix and Ivonrath on the portrait icon: gold 135 vs 93 / 25 at 64 px, area 0.378 vs 0.267 / 0.295 (builder gate). Fill height 0.91 vs Ivonrath 0.67.
- Tris 11,348; the vents are flush; the molt and roar do not hit the wider skull.
- The forearms now show beside the chest in the model sheet, and the skull is broader.

**Blocks 8.5:**
1. **The game camera still reads as a worm.** The 64 px and 128 px game icons are one even tube with a crown. The paws are too small to read as claws, and the top of the silhouette has no width beyond the crown and skull. (MUST 1.)
2. **The front still reads as a round nose bulb, with a wider chin tip under it.** The lower jaw tip (0.046 wide) is wider than the nose tip (0.044 wide). That is the pig-snout read from round 9, still there in code. (MUST 2.)

## 4. New MUSTs (block 8.5)

**MUST 1 (model): the game-camera read must be a dragon, not a worm.**
Evidence: `renders/gamelook_game.png`; `renders/_icon_game_64_128.png`; `renders/_icons2_strip_64.png` tile 2. Causes in code: the paw box at `pets/CinderOverlord.py` line 399 is 0.052 x 0.046 x 0.042, with 0.075-long claw spikes at line 401; nothing on the skull or neck pushes the top silhouette wider than the crown.
Fix (both parts needed):
- (a) Paws: change the hand box at line 399 to (0.070, 0.062, 0.056). Lengthen the claw spikes at line 401 from 0.075 to 0.110 BU, and widen their base from 0.015 to 0.020. Pass: both paws extend at least 0.10 BU outside the neck outline in `gamelook_game.png`, on both sides.
- (b) Skull frill: add one pair of swept-back OBS_D frill spikes per side on the rear skull. Use the same `B.spike` call as the cheek spikes at line 436, with base about x +/-0.22, y -0.20, z 1.42 on the Head bone, swept back about 35 degrees, length 0.22 BU, base width 0.05. Alternatively, lengthen the back-of-skull pair (round-9 TO 9+ 1) by 1.5x. Pass: frill tips reach at least 0.15 BU beyond the skull side (top view), and they clear the crown mount (line 478) with no collision in any clip.
- Keep: head + crown at 0.30 or more of figure height; game area >= 0.18; `collision_free` true in all four clips (after MUST 3); ground >= -0.02; stride 5.0089.
- Re-render `gamelook_game.png`, `CinderOverlord_icon_game.png` and `_icons2_strip_64/128.png`. A fresh reviewer must then call the game icon at 64 px "dragon", not "worm".

**MUST 2 (model): the front must be one taper from the nostrils to the chin.**
Evidence: `renders/close_front.png` (round nose tip with a second red pad under it, white fangs at each side). Code: the skull's last station (line 408, `(1.0, 0.044, 0.032, -0.036)`) is 0.044 wide; the jaw's tip station (lines 443-444, `(1.0, 0.046, 0.020, 0.0)`) is 0.046 wide. The chin overhangs the nose.
- (a) Jaw tip station (1.0) to half-width 0.034 and half-height 0.016 (was 0.046 / 0.020).
- (b) Jaw station (0.85) half-width 0.098 -> 0.078 (keep rh 0.032 and the tip 0.02 back).
- Pass: from the front, no station below the nostril line is wider than the nose tip (0.044). In `close_front.png` the outline runs from the nostril line to the chin as one taper. The fangs stay visible, and the mouth still opens in the roar.

**MUST 3 (clips, verification gate): the collision proxies do not cover the paws or the widened skull.**
Evidence: `pets/CinderOverlord.py` lines 562-564 give one arm sphere at (+/-0.17, -0.71, 0.77) r 0.09 and one claw sphere at (+/-0.40, -0.82, 0.65) r 0.07. The paw centre (+/-0.36, -0.93, 0.59) is 0.13 from the claw sphere, so no proxy checks the paw. Lines 557-558 give one head sphere (r 0.20) and one jaw sphere (r 0.10) at x = 0, so the new cheek width (x1.15) has no proxy. The walk paddles (6 deg) and the roar spread move the paws, so `collision_free true` does not prove the paws stay clear.
- Fix: add a proxy `((s*0.36, -0.93, 0.59), same, 0.07, "Claw_"+side)` for each paw. Add two skull-side proxies at the Head's widest point (x +/-0.22 to +/-0.30, at the Head bone's centre height; take the exact centre from the Head group bounds), r 0.12.
- Pass: re-run `collision_free` in all four clips (idle, walk, roar, act_molt) with the new proxies. Report the minimum clearance (at least 0.02 BU). Loops stay 0 / 0.

## 5. TO 9+ (not blocking)

1. **Outclass the 1% secrets.** At 128 px the Cinder's only bright read is the gold crown. One lit sulfur-blue accent on the flank or the back, or a wing-like frill, would help. Thunder Rex and Cosmic Leviathan still look louder.
2. **Index card pose.** The portrait is a low coil at the molt peak. Phoenix stands. The fill is already 0.91; the gap is pose, not size.
3. **Walk framing.** The tail tip crops at the bottom of `_cv_walk_game.png` (f0, f8, f32, f40). Check the follow camera in Studio, or pull the walk tile back.
4. **Hygiene.** `_review/GLACIER_CONCEPTS.md` lines 46 and 116: swap the plum body (#B684AC), rose vents (#FF6096) and "Plum-obsidian serpent, rose lava vents" for the current ember body, sulfur-blue vents and the current look line.
5. **Molt fan at frame scale.** The fan is visible from the front, but small. A slightly higher molt portrait camera would make the sheds read at game distance.
6. **Pose limits.** Lead to confirm the per-bone reading (neck 7.5 per bone against 8, spine 4.5 against 5). Not re-measured here.
7. **Breath.** Studio check, as ruled.

## 6. Checklist

| check | result |
|---|---|
| Model >= 8.5 | FAIL (8.3) |
| Clips, every clip >= 8.5 | PASS (8.5 each; lowest 8.5), with MUST 3 to close the collision proof |
| Tris <= 15k | PASS (11,348) |
| Stride 5.0089 | PASS |
| Gold >= 103 at 64 px (portrait) | PASS (135) |
| Game area >= 0.18 | PASS (0.192) |
| Head + crown >= 0.30 of figure height | PASS (builder: 0.306) |
| Forearms out | PARTIAL (visible in model sheet; stubs at game size) |
| Head x1.15 in x only | PASS |
| Tail4 ring removed | PASS |
| Game silhouette reads dragon at 64 px | FAIL (worm / eel) |
| Front face one taper, not a pig-snout | FAIL (jaw tip 0.046 vs nose 0.044) |
| Collision proof covers paws and widened skull | FAIL (proxy gap; MUST 3) |
| Stale renders moved | PASS |
| Tier record MYTHIC | PASS (MODEL_NOTES line 3); FAIL (GLACIER_CONCEPTS lines 46, 116) |
