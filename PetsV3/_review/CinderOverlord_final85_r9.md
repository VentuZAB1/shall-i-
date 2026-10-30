**Model: 8.4/10 - FIX. Clips: 8.5/10 - PASS.**

# Cinder Overlord - FINAL 8.5 GATE, ROUND 9 (fresh reviewer, 2026-10-28)

Round 8 changes are real and visible: the head group is bigger (HEAD_XF 1.45, centre blade 0.40), the six rear vent slits are flush and 30 % shorter, the dorsal spikes are longer, and the Body4 ring is gone. The clips still hold at 8.5. The model does not clear the bar, because the game-camera read is still a thin, even tube with a crown on top. At 64 px and 128 px the game icon reads as an eel or worm, not a dragon. From the front, the snout and chin are still two round stacked bulbs, the pig-nose read the owner rejected. Model stays FIX at 8.4.

## 0. What I looked at, and the limits

- Brief `_review/GLACIER_REVIEWER_BRIEF.md`. Round 8 `_review/CinderOverlord_final85_r8.md`.
- Builder notes `CinderOverlord/MODEL_NOTES.md` (round 8, export 09:32), `CLIP_NOTES.md` (round 8 header), `_scratch/gate_f85.json` (09:36). Parameter lines from `pets/CinderOverlord.py` (grep).
- Freshness: `C:\cdimp\CinderOverlord.fbx` 09:32; renders 09:33-09:35, title bars "final 8.5 round 8". All current, so the clip re-check is on the new head.
- Images opened and loaded: `renders/gamelook_game.png`, `CinderOverlord_icon_game.png`, `renders/_icons_alt_strip_64.png` and `_128.png`, `CinderOverlord_portrait_alt.png`, `renders/close_front.png`, `renders/_close_sheet.png`, `renders/_model_sheet.png`, `renders/_pose_tq_sheet.png`, `renders/_cv_walk_game.png` and `_side.png`, `renders/_cv_roar_front.png` and `_side.png`, `renders/_molt_r8_front.png` and `_tq.png`, `renders/_icons2_strip_64.png` and `_128.png`, `InfernoPhoenix/renders/_model_sheet_600.png`. No image failed to load.
- Limits: no pixel tool and no Blender run (reviewer rule). Counts and proportions are by eye from the PNGs. Gold, area and share numbers are the builder's gate file. I assumed the Index card uses the portrait icon (IndexConfig.PORTRAITS); I did not open the Index UI.

## 1. Clip table (lowest clip = 8.5, so Clips = 8.5 PASS)

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.5 | Head held near level through the 0 / 30 / 60 / 90 beats; crown breath is small; no head shake; the bigger head does not sag or drift. Breath amplitude is a Studio check (lead ruling). | `renders/_pose_tq_sheet.png` (idle row); `_scratch/gate_f85.json` `audit.idle` (loop 0 / 0) |
| walk | 8.5 | The lateral S runs head to tail in the side view and holds its line; no body poke through the ground; the blue vent marks stay flush and do not swing. The tail crops at the bottom edge of the game tile at f0 and f40 (framing, see TO 9+ 2). | `renders/_cv_walk_side.png`; `renders/_cv_walk_game.png` |
| roar | 8.5 | Crown flare from f14; jaw opens and the mouth is visible at f30-f44 in both front and side views; closes by f58. The bigger head shows no contact with the crown or the crest. | `renders/_cv_roar_front.png`; `renders/_cv_roar_side.png` |
| act_molt | 8.5 | Blades lift one by one; the fan is visible f22-f40 from the front; reseat f84-f100; rest at f110. The taller centre blade and bigger head show no visible contact with the spike crest. Outer blades peak at 55.84 deg (gate). | `renders/_molt_r8_front.png`; `renders/_molt_r8_tq.png`; `_scratch/gate_f85.json` `molt_blade_speed_deg_per_f` |

Headless numbers from the builder (`_scratch/gate_f85.json`, not re-run here): `collision_free` true in all four clips; `ground_min_z` -0.006; linear 0; idle and walk loops 0 / 0; stride 5.0089 per 48 f; tris 11,384.

Note: the clip scores hold on the current file only. MUST 1 and MUST 2 below change geometry, so the four-clip check must be re-run after them.

## 2. Round 8 items

| item | result | evidence |
|---|---|---|
| R8 MUST 1a, head + crown >= 0.30 of icon height; HEAD_XF 1.45, centre blade 0.40 | **PASS per lead ruling.** Measured against the figure height: 0.302 (builder). By eye in `gamelook_game.png` the head + crown is about 0.28 of the figure, which is within my reading error of 0.302. Not counted against the score. | `_scratch/gate_f85.json` `game_icon_head_share`; `MODEL_NOTES.md` round 8 |
| R8 MUST 1b, one dark ring dropped (Body4); game obsidian <= 25.0, game body >= 40 | **PARTIAL.** The Body4 ring is dropped (`CinderOverlord.py` line 320, keep-set). Shares pass (game body 53.0, obsidian 25.0). But from the game camera `gamelook_game.png` still shows three dark rings with spike clusters on the back and flank, not two. | `renders/gamelook_game.png`; `_scratch/gate_f85.json` `shares_pct.game` |
| R8 MUST 1c, six blue vent slits 30 % shorter and flush; no slit tip outside the outline from the game camera | **PASS.** The blue marks sit on the flank in the game view and the walk game tile; nothing stands off the outline. | `renders/gamelook_game.png`; `renders/_cv_walk_game.png`; `MODEL_NOTES.md` round 8 |
| R8 MUST 1, "dragon, not worm" at 64 px | **FAIL.** The game-camera icon at 64 px (`_icons2_strip_64.png`, tile 2) and 128 px (`_icons2_strip_128.png`, tile 2) reads as a thin red eel with a gold crown on top. The silhouette is one even tube; the forearms are hidden under the neck. | `renders/_icons2_strip_64.png`; `renders/_icons2_strip_128.png`; `CinderOverlord_icon_game.png` |
| R8 MUST 2, gold >= 103 at 64 px | **PASS** (builder counter). Portrait_alt 136 (kit window H 29-58) vs Phoenix 93, Ivonrath 25. At 128 px: 537 vs 357 / 112. | `_scratch/gate_f85.json` `icons_64_128`; `renders/_icons_alt_strip_64.png` |
| R8 MUST 2, area >= 0.36 | **PASS.** Portrait_alt 0.373 vs Phoenix 0.267, Ivonrath 0.295. | same |
| R8 MUST 2, game area >= 0.18 (lead ruling: area and visual read) | **PASS** on area: 0.188. The visual read fails (see MUST 1). | same; `renders/_icons2_strip_128.png` |
| R8 MUST 2, head and crown above the Phoenix head line at 128 px | **PASS** on the stated test. The Cinder's crown reaches the top of its tile, above the Phoenix's crest (by eye). | `renders/_icons_alt_strip_128.png` |
| R8 MUST 2, "hero, not the louder read" | **PARTIAL** (judgment). The gold crown is the loudest element on the Cinder's card. The Phoenix's upright wings and flame still read as the bigger, busier figure at 128 px, and Thunder Rex and Cosmic Leviathan read as flashier (see TO 9+ 3). | `renders/_icons_alt_strip_128.png`; `renders/_icons2_strip_128.png` |
| R8 MUST 2, molt collision-free | **PASS** per gate. No visible contact in the molt frames. | `_scratch/gate_f85.json` `collision_free`; `renders/_molt_r8_front.png` |
| R8 TO 9+ 1, chin flatter (not done in r8) | **FAIL.** From the front, the nose is a round red bulb with two nostril diamonds, and the chin below it is a second round bulb. This is the pig-snout read. Promoted to MUST 2. | `renders/close_front.png` (lower centre); `renders/_close_sheet.png` |
| R8 TO 9+ 2, eye socket outer ends | **PASS** (by eye, not measured). The blue sockets sit under the brows and do not sit on the skull outline from the front. | `renders/close_front.png` |
| R8 TO 9+ 3, nostrils >= 0.02 BU | **PASS.** Black diamonds read clearly in the close-up. | `renders/close_front.png`; `MODEL_NOTES.md` round 7 |
| R8 TO 9+ 4, walk game framing | **OPEN.** The tail still crops at the bottom of `_cv_walk_game.png` at f0 and f40. A Studio camera check. | `renders/_cv_walk_game.png` |
| R8 TO 9+ 5, stale renders | **PASS.** No `crown_*.png`, `mr4_*` or `mr6_*` in `renders/`. | `renders/` listing |
| R8 TO 9+ 6, pose-limit reading | **Not re-measured** (no Blender run). Builder reports neck 7.5 per bone (limit 8) and spine 4.5 (limit 5). Lead to confirm. | `CLIP_NOTES.md` round 8 / round 4 |
| R8 TO 9+ 7, tier record | **PARTIAL.** `MODEL_NOTES.md` line 3 says MYTHIC (PASS). `GLACIER_CONCEPTS.md` no longer says "ultra-rare" and both tier lines say mythic. But the look text and swatches still show the old plum and rose build (body #B684AC, vents #FF6096, "Plum-obsidian serpent, rose lava vents"). | `_review/GLACIER_CONCEPTS.md` lines 46 and 116 |
| R8 TO 9+ 8, breath | Studio check (lead ruling). Not scored. | |
| Tris <= 15k | **PASS.** 11,384. | `_scratch/gate_f85.json` `tris` |
| Slither stride | **PASS.** 5.0089 per 48 f (builder). | `_scratch/gate_f85.json` `export.meta_stride_BU_per_48f` |
| Molt outer lift >= 55 deg | **PASS** per gate (55.84). Not re-measured. | `_scratch/gate_f85.json` |

## 3. Model score: 8.4 - FIX

**Holds:**
- The face reads fierce from the front: heavy brows, narrow blue slit eyes, no glints, no smile, no googly eyes. The nostrils read.
- The crown wins the counter and the area against the Phoenix and Ivonrath on the portrait icon at 64 and 128 px.
- The vents are flush slits now. Studs cover the whole skin. Tris 11,384, collision-free through the roar and the molt with the bigger head.
- The head and crown are larger on the game icon than in round 8 (0.302 of the figure, lead ruling PASS).

**Blocks 8.5:**
1. **The game-camera read is still a worm, not a dragon.** The game icon at 64 and 128 px is a thin even tube with a crown, and the forearms that would give it dragon limbs sit under the neck where no camera sees them. (MUST 1.)
2. **The front reads as a pig-nose.** The snout and chin are two stacked round bulbs (close_front lower centre). That is the cute cue the owner rejected, and it was the round 8 TO 9+ item that was not done. (MUST 2.)

## 4. New MUSTs (block 8.5 on the model; a re-check of all four clips is required after either)

**MUST 1 (model): the game-camera read must be a dragon, not a worm.**
Evidence: `renders/_icons2_strip_64.png` and `_128.png` tile 2 (eel with a crown); `renders/gamelook_game.png` (one even tube, three dark rings, spike clusters on the back). The forearms are at x +/-0.17 to +/-0.28 BU, inside the chest outline, so they do not show from above (`CinderOverlord.py` lines 541-542; default anchors at line 501).
- (a) **Forearms out.** Move the elbow anchor (line 541) to x +/-0.40, and the hand anchor (line 542) to x +/-0.36, same y and z. Each forearm must stand at least 0.08 BU outside the chest outline at z 0.6-0.7. The claws must show beside the neck in `gamelook_game.png`. Apply the same move to the line 501 fallback (currently s*0.24 / s*0.28).
- (b) **Head wider than the neck from above.** Scale the Head and Jaw groups by x x1.15 about the throat, x only. Y and Z stay the same, so the head + crown share stays at 0.302 of figure height. Keep Crown_1..5 out of the x-scale (they sit in the HEAD_XF list at line 546); the blades must keep their socket spacing. Re-check the molt and roar collisions.
- (c) **Two ring bands on the back, not three.** Remove the Tail4 ring from the keep-set at line 320, and keep the Spine-base and Body1 rings. Re-count the dark rings in `gamelook_game.png`; the target is two.
- **Pass:** game area >= 0.18 (now 0.188); `collision_free` true in all four clips; `ground_min_z` >= -0.02; stride 5.0089 unchanged; re-render `gamelook_game.png`, `CinderOverlord_icon_game.png`, `_icons2_strip_64.png` and `_128.png`. A fresh reviewer must then say "dragon, not worm" for the game icon at 64 px.

**MUST 2 (model): the front must not read as a pig snout.**
Evidence: `renders/close_front.png` lower centre (round nose bulb with two nostril diamonds, then a second round chin bulb with a cream line); `renders/_close_sheet.png` shows the same stack in the 3/4 view. Built by the snout loft stations 0.74-1.0 (lines 389-393) and the jaw / chin front (line 426).
- (a) The jaw station at 0.85 (now rh 0.040, per MODEL_NOTES round 8) goes to rh 0.032, so the chin tapers into the jaw.
- (b) Pull the chin cover's front face back 0.02 BU in -Y, so the lower jaw tip sits behind the snout tip.
- (c) Keep the nostril pits on the snout top (lines 401-411) unchanged.
- **Pass:** in `close_front.png` the outline from the nostril line down to the chin is one continuous taper. The chin no longer reads as a separate round bulb.

## 5. TO 9+ (not blocking)

1. **Game-camera presence.** Game area is 0.188 against the Phoenix's 0.267; the Phoenix's spread wings make its game silhouette larger. A frill of two or three obsidian spikes behind the skull (the back-of-skull pair at line 451, lengthened by about 1.5x, plus one pair on Neck2) would widen the top read.
2. **Walk game framing.** The tail crops at the bottom edge of `_cv_walk_game.png` at f0 and f40. Check the follow camera in Studio, or pull the walk tile back.
3. **Outclass the 1 % secrets.** At 128 px Thunder Rex and Cosmic Leviathan read bigger and flashier (`_icons2_strip_128.png` tiles 9-10). The Cinder's only bright read is the gold crown. One more lit sulfur-blue accent on the body or flank would help.
4. **Index card pose.** The portrait is a low 3/4 coil at the molt peak; the Phoenix stands upright. Fill height is 0.89 against 0.91, so the gap is pose, not size.
5. **Hygiene.** `_review/GLACIER_CONCEPTS.md` lines 46 and 116 still list the plum body (#B684AC), the rose vents (#FF6096) and the "Plum-obsidian serpent, rose lava vents" look. The current build is an ember body with sulfur-blue vents (20, 92, 250) and near-white cores (226, 240, 255). Tier wording is already fixed.
6. **Pose limits.** Lead to confirm the per-bone reading (neck 7.5 per bone against the limit of 8; spine 4.5 against 5). Carried from round 8.
7. **Breath.** Studio check, as ruled.

## 6. Checklist

| check | result |
|---|---|
| Model >= 8.5 | FAIL (8.4) |
| Clips, every clip >= 8.5 | PASS (8.5 each; lowest 8.5) |
| Tris <= 15k | PASS (11,384) |
| Stride 5.0089 | PASS |
| Gold >= 103 at 64 px (portrait) | PASS (136) |
| Game area >= 0.18 | PASS (0.188) |
| Head + crown >= 0.30 of figure height | PASS (lead ruling; 0.302) |
| Game silhouette reads dragon at 64 px | FAIL (worm / eel) |
| Front face not a pig-snout | FAIL |
| Stale renders moved | PASS |
| Tier record MYTHIC | PASS (MODEL_NOTES); PARTIAL (GLACIER_CONCEPTS swatches) |
