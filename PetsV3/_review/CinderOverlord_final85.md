# Cinder Overlord - FINAL 8.5 GATE (round 6, colours final, as exported) - 2026-10-28

**Verdict: FIX.** Both scores are under the owner's 8.5 bar (2026-10-28).
- **Model: 7/10** (round 5 was 7/10).
- **Clips: 7.5/10** (round 4 was 8/10 with fixes; the clip numbers are unchanged, but the molt is weak at game distance, the walk speed was never checked, and the walk and roar renders are stale).

Round 6 does what it set out to do. The deep sulfur-blue accent (20,92,250) and white-hot cores (226,240,255) no longer copy a sibling (`_scratch/blue_cmp.png`), the gold crown is the hero at 64 px, and the game body share passes (41.9 %). But the problems the earlier rounds named are still there: the body reads as a long segmented worm, the head is soft, the eyes do not resolve at 64 px, and the gold margin is one pixel.

## 0. What I looked at

- Plan `_review/CinderOverlord_plan.md`; reviews 1-5; the brief `_review/GLACIER_REVIEWER_BRIEF.md`.
- `CinderOverlord/MODEL_NOTES.md` (round 6), `CLIP_NOTES.md` (round 6), `ANIM_REFS.md`.
- `_scratch/gate_r6.json` (the single gate file), `gold_windows_r6.txt`, `game_icon.json`, `shares_all.json`, `clipgate_r6.txt`.
- Current renders (dated 23:04-23:05): `_icons_strip_64.png`, `_icons_strip_128.png`, `_icons2_strip_64.png`, `_icons2_strip_128.png`, `_model_sheet.png`, `_close_sheet.png`, `close_front.png`, `flat_game.png`, `flat_side.png`, `gamelook_game.png`, `gamelook_tq.png`, `_molt_r4_front.png`, `_molt_r4_side.png`.
- Stale renders (see section 2.3): `_cv_walk.png` (18:07), `_cv_molt_front.png` (18:07), `pose_tq_*` (18:14), `cv_*_roar_*` (18:07).
- Comparisons: `Raiju/renders/_model_sheet.png` (the owner's favourite), `ThunderRex`, `CosmicLeviathan`, `Ivonrath` model sheets, `_ALL_FIERCE_progress.png`. The InfernoPhoenix model sheet is not in its renders folder, so the Phoenix read comes from the 64 and 128 strips.
- Source: `pets/CinderOverlord.py` lines 15-52, 196-223, 268-299, 316-392, 585-616.

Not verified: no Blender or Studio run. The collision (`collision_free` true), ground minimum (-0.006) and linear 0 are the builder's headless numbers, accepted as stated.

## 1. Model judgement (player's eye, about 5 studs, FOV 70, phone size)

**What works**
- The species reads at 64 px: a serpent under a gold crown. 10.5 studs, the tallest of the Fire egg. 10,852 tris (cap 15k).
- Colour: no pink and no copy. The body is ember (166,66,50). The accent and cores are a cold deep blue, distinct from Kraken, ThunderRex and the Phoenix at 128 px. The cold-blue read is the lead's accepted ruling (B); it is not reopened here.
- The gold crown is the clear hero in both strips and in `flat_game`.
- The side profile has a real crocodile wedge skull, fangs and brow points. It is fierce from the side.
- Game shares pass: body 41.9 % (floor 40), obsidian 33.6 % (ceiling 40). Side body 48.7, tq 40.3.

**What fails (the reasons for 7/10)**
- **A. Worm, not a mythic.** From above (`gamelook_game.png`, `flat_game.png`) and in the 128 strip, the body is a long, slim tube with a dark ring on almost every segment. It reads as a caterpillar or centipede. From 3/4 (`gamelook_tq.png`) it is milder, but the body is still thin next to the head and the crown. The mass is too low for a 0.5 % pet next to Raiju's bevelled armour blocks and ThunderRex's bulk. Raised radii in rounds 1-2 were only +10 to +15 %.
- **B. Soft head.** In `close_front` and `_close_sheet` (side panel) the snout is rounded, the jaw and cheeks bulge like a plush face, and the head studs look like large bubbles. The brief asks for angular, bevelled, tapered blocks.
- **C. Eyes lost at 64 px.** In `_icons_strip_64.png` the face is a red blob under a yellow top. The blue eye slits are too small to read at icon size.
- **D. Crown mount clutter.** From the front (`close_front`), the mount ends and side blocks (lines 374-377) drop as dark arms onto the brows. That reads as horns or forks, not a clean crown.
- **E. Gold margin.** The gate file says portrait 26 (gate 25; one pixel spare). The windows file gives 28 for the same kit window. The rendered window gives 22, which is below the gate. The two files disagree and must be reconciled.
- **F. Outclass fails at icon size.** At 128 px the Cinder is the dullest, least massive serpent in the strip. The Phoenix and Ivonrath read brighter; ThunderRex and CosmicLeviathan read bigger. The body colour is a settled ruling (do not lift it), so the lever is A and B, not colour.

Distinctness: Ivonrath is 7.5 deg in hue but separated by silhouette (wingless serpent) and by the blue accent. Pass.

## 2. Clip judgement

### 2.1 Measured numbers (builder's JSON, unchanged since round 4; not re-run)
- Neck bones 7.5 deg (limit 8). Spine (chest) 4.5 (limit 5). Head plus neck pitch-up 0 to 2 deg (limit 30). No sign flips, no head shake, no spin. Joint step max 6.3 deg per frame (limit 60).
- Centre-blade reseat peak 4.62 deg/f against a rise peak of 5.18 deg/f. Reseat below rise: pass.
- Idle and walk loops closed (0.000 and 0.76 deg). Roar and molt end at exact rest. Linear 0. Ground minimum -0.006 for all clips. `collision_free` true.
- Owner rule: roar and molt cite animationreference.org (#3, #6, #9): pass. Idle and walk cite Haku (a flying eastern dragon, Sakugabooru #225387) and Wikimedia snake studies: not the site overlay, so the disclosure in C4 applies.

### 2.2 Fails and unverified items
- **Molt is weak at game distance.** `_molt_r4_front.png` (current) at f0 and f40 looks almost the same from the 5-stud front. The lift only reads in the side view (`_molt_r4_side.png`, f34-f50). The signature act does not land where the player sees it.
- **Walk speed unverified.** The walk is a slither in place (no root travel). Stride 5.19 BU per 48-frame cycle (CLIP_NOTES). At H 2.254 BU = 10.5 studs (1 BU is about 4.66 studs) and 30 fps, that is about 24 studs in 1.6 s, roughly 15 studs/s of bend travel. That is only right if the pet's game speed matches. This has been open since round 3 and was never tested in Studio.
- **Stale renders.** `_cv_walk.png`, `cv_game_walk_*`, `_cv_molt_front.png`, `cv_*_roar_*` (18:07) and `pose_tq_*` (18:14) predate the current palette and the round 2-4 clip fixes. The walk sheet still shows the old mauve-pink body. There is no current roar render at all. Walk and roar are not judged in the current model.

### 2.3 Animation references (owner rule)
- Roar and molt: PASS (site clips #3, #6, #9).
- Idle and walk: the frames came from a flying dragon and a Wikimedia study, stepped on a Sakugabooru post. Round 4 passed this with a disclosure. The disclosure must reach the owner before the gate (C4).

## 3. MUST list (to reach 8.5)

### Model
- **M1. Kill the worm read; add bulk (A).**
  - Rings: drop every second ring on Body2-4 and Tail1-4 (keep the Spine, Body1 and the neck). Narrow the rest: body ring band from 0.55-0.84 to 0.62-0.80, tail from 0.62-0.79 to 0.66-0.76 (ring calls near lines 246-258 and 275).
  - Radii (line 45): `RAD` from `[0.265, 0.275, 0.250, 0.225, 0.180, ...]` to about `[0.297, 0.308, 0.280, 0.252, 0.200, ...]`, which is +12 % on RAD[0..3]. Leave the tail radii for T2.
  - Neck (line 52): `FRAD` +5 % (`[0.282, 0.275, 0.257, 0.231, 0.208, 0.189]`) so the neck keeps the head proportion.
  - Re-run the ground and collision test after the change. Vents, rings and forearms follow the radii.
- **M2. Angular head, not a plush face (B).**
  - Cut the jaw-muscle ellipsoid bulges (the cheek bulge calls after line 332, round-2 M5) to about 60 % of their size, and make the cheek a flat, tapered OBS_D plate on each side.
  - Make the head stud size equal to Body1's stud size, not the larger head studs.
  - Verify in `close_front` and the `_close_sheet` side panel: the cheek must read as a plate, not a ball.
- **M3. Eyes at 64 px (C).**
  - Line 362: the rose eye slit from `(0.085, 0.007, 0.0165)` to `(0.110, 0.010, 0.020)`.
  - Line 361: the black socket from `(0.098, 0.010, 0.032)` to `(0.125, 0.010, 0.036)`.
  - Keep the deep blue (accent ruling). Keep the eyes angled and set under the brow. No glints, no round eyes.
  - Pass if two blue slits show in `_icons_strip_64.png` at the face position.
- **M4. Clean crown mount (D).**
  - Lines 374-375: shorten the mount ends from `s * 0.30` to `s * 0.22`, and drop them 0.02 so they sit behind the blades.
  - Line 376-377: remove the two side blocks (`s * 0.27`, rot 14). The blades alone carry the crown.
  - Check in `close_front`: no dark arms over the brows. The five blades stay the hero.
- **M5. Gold margin and one number (E).**
  - Add a gold tip cap on the centre blade (the top about 0.06 H), not a wider frame. Wider frames touched in the molt at 0.040 / 0.030 (round 6 notes).
  - Targets: at least 30 gold px on the kit counter, at least 25 on the rendered window (`40-62, s .6, v .55`).
  - Reconcile to one file: 26 (`gate_r6.json`) vs 28 (`gold_windows_r6.txt`) for the same window. Quote one count.

### Clips
- **C1. Molt legible at game distance.**
  - In `act_molt` (lines 585-616): raise the four outer blades (Crown_1, 2, 4, 5) from 35 to 45 deg rise. Keep the centre at 40.
  - Stretch the reseat windows so every reseat peak stays below its rise peak: centre f84-95 to f84-100; outers f84-104 to f84-108.
  - Pass if the front frames f22, f34 and f40 show the blades visibly fanned against f0 (at least 15 deg apart in the front view) in `_molt_r4_front.png`.
  - Recheck collisions at 45 deg.
- **C2. Current renders for every clip.** Re-render from the 23:04 model: `pose_tq` sheets for idle, walk, roar and molt; `_cv_walk.png` and the game walk; `_cv_molt_front.png`. The roar needs a current render before it is judged.
- **C3. Walk speed in Studio.** At the pet's real follow speed, check the bend travel does not skate. The 48-frame cycle implies about 15 studs/s. If the pet walks slower, lengthen the cycle (for example to 72 frames); if faster, shorten it. Record the number in `CLIP_NOTES.md`.
- **C4. Disclose the reference source to the owner.** Idle and walk cite Haku (a flying dragon, Sakugabooru #225387) and Wikimedia snake studies, not the site overlay. The owner needs the clip titles, tags and frames before the gate. Do not present it as an animationreference.org clip.

## 4. TO 9+ list (highest impact, after the MUSTs)
- **T1. Pale 3-band read from the game camera.** The pale belly is 2.1 % in game and invisible from above. Widen the Body1-4 scute arc by about 10 deg on each side, or lift the throat ladder onto the chest front so it shows in `gamelook_tq`.
- **T2. A tail that is not a whip.** `RAD[5..7]` (Tail1-3) from 0.134 / 0.108 / 0.082 to about 0.168 / 0.135 / 0.103 (+25 %). The taper stays.
- **T3. Idle breath at game distance.** Raise each neck bone's breath from about 2 deg to about 3 deg (the limit is 8). The breath should read from 5 studs.
- **T4. Icon gold read.** After M5, check the gold on blades 1 and 5 is not wider than the centre blade's gold (it should not outshine the hero).

## 5. Pass / fail checklist

| # | Check | Result |
|---|---|---|
| 1 | Tris <= 15k | PASS (10,852) |
| 2 | Height 10.5, tallest of the Fire egg and the secrets | PASS |
| 3 | Species reads at 64 px | PASS |
| 4 | Face (eyes) reads at 64 px | FAIL (M3) |
| 5 | Face reads at 5 studs (`close_front`) | PARTIAL (slits small; M3) |
| 6 | Fierce, not cute | PARTIAL (side fierce; head soft, M2) |
| 7 | Body reads as a mythic mass, not a worm | FAIL (M1) |
| 8 | Dark rich body is the main colour (game 41.9 %) | PASS |
| 9 | Obsidian <= 40 % (game 33.6 %) | PASS |
| 10 | Accent distinct from every sibling | PASS (ruling A, not reopened) |
| 11 | Gold >= 25 at 64 px, kit counter | PASS by 1 px (26; the windows file says 28) |
| 12 | Gold >= 25 at 64 px, rendered window | FAIL (22) (M5) |
| 13 | Gold reads as the hero at 64 px | PASS |
| 14 | Crown clean (no horn-like mount ends) | FAIL (M4) |
| 15 | Fire identity (cold-blue read accepted) | PASS (ruling B) |
| 16 | Distinct from Ivonrath, Phoenix, Leviathan | PASS |
| 17 | Outclasses the Fire egg and the 1 % secrets at 128 px | FAIL (A, B, F) |
| 18 | Parts floating, poking or wrong from below | PASS (builder's collision numbers) |
| 19 | Clip: neck, spine, head pitch, reseat, loops, rest, ground | PASS (builder's numbers, not re-run) |
| 20 | Clip: molt legible at game distance | FAIL (C1) |
| 21 | Clip: walk speed checked in Studio | UNVERIFIED (C3) |
| 22 | Clip: renders current for every clip | FAIL (C2) |
| 23 | Animation refs: roar and molt | PASS (#3, #6, #9) |
| 24 | Animation refs: idle and walk | PASS only with disclosure (C4) |

## 6. Do not re-open
- The sulfur-blue accent and the white-hot cores (ruling A). The cold-blue vent read is accepted (ruling B).
- The body colour: do not lift the body value (round 4 and 5 NICE). M1 changes mass, not colour.
- House gold stays the hero. The aura (ember and blue flame particles) is VFX for later, so its absence is not a fault now.

## 7. Next round
Send with the fixes applied:
- `close_front.png`, `_close_sheet.png` (M2, M3, M4).
- `_icons_strip_64.png` and `_128.png` with both eyes visible (M3) and the gold count from one file (M5).
- `gamelook_game.png` and `gamelook_tq.png` with the new body mass and rings (M1).
- Current `_molt_r4_front.png` and `_molt_r4_side.png` at f0, f22, f34, f40 (C1).
- Current `pose_tq` sheets for idle, walk, roar and molt, and the Studio walk-speed number (C2, C3).
- The owner disclosure text for the references (C4).

The model goes to the owner at 8.5 or better after M1-M5. The clips go to the owner after C1-C4. Both are below the bar today.
