# Cinder Overlord - FINAL 8.5 GATE, ROUND 2 (export 2026-10-28 01:31, 10,588 tris)

**Verdict: FIX.** Both scores are under the owner's 8.5 bar.
- **Model: 7.5/10** (round 1 of this gate: 7/10). Real progress on bulk, head and molt legibility.
- **Clips: 8/10** (round 1 of this gate: 7.5/10). The molt now reads from the front. The walk speed (C3) and the reference disclosure (C4) were skipped by lead ruling, so they stay open.

Summary: the builder landed the mass, head and molt changes. What is left is the neck bands from above, the dark brow bars from the front, and the Cinder still being the dimmest serpent at 128 px.

## 0. What I looked at

- Notes: `CinderOverlord/MODEL_NOTES.md` (FINAL 8.5 section), `CLIP_NOTES.md` (FINAL 8.5 section), `_scratch/gate_f85.json` (the only gate file), `fan_f85.txt`, `ang_f85.txt`, `fix_f85e.py` (docstrings only).
- Renders (all 01:25-01:30, newer than the last model edit `fix_f85d.py` at 01:23; export at 01:31): `_model_sheet.png`, `close_front.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `_icons2_strip_128.png`, `gamelook_game.png`, `gamelook_tq.png`, `_molt_r4_front.png`, `_molt_r4_side.png`, `_pose_tq_sheet.png` (26 beats: idle, walk, roar, molt).
- No stale renders in this set.

Not verified:
- I did not re-measure the gold count (the brief is read-only). The 32 / 24 figures are the builder's single kit-counter run.
- Walk speed and the disclosure were skipped per lead ruling.
- Idle breath (T3) cannot be judged from stills at game distance.

## 1. Round-1 MUSTs and TO 9+, checked

| Item | Result | Note |
|---|---|---|
| M1 mass, not a worm | PARTIAL | Body is visibly sturdier in `_model_sheet` (side) and `gamelook_tq`. From above (`gamelook_game`) the neck still shows 3-4 dark bands and reads as a caterpillar. |
| M2 angular head | PASS (mostly) | The flat dark cheek plate reads in the side close-up (`_close_sheet`, middle). Jaw bulge is smaller. The snout tip still shows round stud dots (TO 9+). |
| M3 eyes | PASS | Blue slits are larger. The near eye reads in `close_front` and at 128 px. The far eye is hidden at the 3/4 angle, as the builder notes. |
| M4 crown mount | PARTIAL | Side blocks gone and mount ends short (good). But the brows still read as two dark bars from the crown base down to the eye pads in `close_front`. |
| M5 gold | PASS (builder count) | The rounded gold tips show on the centre and blades 2 / 4. The centre blade leads at 64 and 128 px. The count itself is unverified by me (section 0). |
| T1 belly | PASS | Pale share side 12.5 %, tq 12.9 %; cream belly band reads in the model sheet. |
| T2 tail | PASS | Tail1-3 thicker in the model sheet. The tip is still long in `gamelook_tq`. |
| T3 idle breath | UNVERIFIED | Not judgeable from stills at game distance. |
| T4 outer gold | PASS | Blades 1 and 5 stay plain. |
| C1 molt from the front | PASS | `_molt_r4_front`: outer blades visibly splay at f34-40. Probe: front fan 48.0 deg at f0, 85.0 at f34-40 (+37), each fanned blade 16-18.5 deg. |
| C1 reseats | PASS | Probe max fall per blade (outer 5.80 at f49, centre 3.17 at f92) is under rise (outer 7.47, middle 7.10, centre 5.18). |
| C2 renders | PASS | All clip sheets re-made from the current model (01:28-01:30). |
| Roar | PASS | `_pose_tq_sheet` roar 0-66: neck gathers, blades flare, jaw opens. |
| Shares | PASS | Game body 45.0 % (floor 40), obsidian 28.6 % (ceiling 40). Side body 47.6, obsidian 20.5, pale 12.5. |
| Tris, height | PASS | 10,588 (cap 15k). Height 10.5 studs. |

## 2. Scores

**Model 7.5/10.** Why not 8:
1. **Neck bands from above.** `gamelook_game.png`: the neck (Neck1-3) keeps three or four dark rings, so the top view still reads as a caterpillar.
2. **Brows read as horns from the front.** `close_front.png`: the two dark brow bars run from the crown base down toward the eye pads. This is the "horn" read that M4 was meant to fix.
3. **Outclass at 128 px.** In `_icons_strip_128.png` the Cinder is still the dimmest, least massive serpent next to the Phoenix and Ivonrath. Colour is a settled ruling, so the levers are the accent and the neck read.

**Clips 8/10.** All measured gates pass (section 1), the molt reads from the front, and every render is current. What holds it at 8: the walk speed has never been tested in Studio (C3), and the reference source is undisclosed (C4). Both were skipped by lead ruling. If they are reinstated and pass, the clips can reach 8.5.

## 3. MUST list to 8.5 (model)

- **R2-M1. Neck bands (game view).** The neck ring calls (ring_band at line 275, neck loop i >= 1): keep rings on Neck1 and Neck3 only. Narrow the Neck2 band from 0.50-0.84 to 0.62-0.80. Check in `gamelook_game.png` that the neck reads as one armoured column.
- **R2-M2. Brows.** Shorten the brow bars (half-length 0.090 to about 0.070), reduce the roll from 16 to about 10 deg, and drop them 0.01 so their outer ends sit below the crown line. Pass if no dark bar reaches the crown line in `close_front.png`.
- **R2-M3. Outclass at 128 px (accent, not colour).** Lengthen the blue vent slits by about 15 % (the vent slit length in the vent calls near line 299, and the vent() bar near line 191). The ROSE/CROWN_IN colour stays (ruling A). Pass if the flank blue reads clearly in `_icons_strip_128.png` next to the Phoenix.
- **R2-M4. Gold check on two windows.** Keep the kit counter (32 / 24) as the gate, but also record the rendered window (H 40-62, s >= 0.6, v >= 0.55) in `gate_f85.json` beside it. Round 6 had 26 on one window and 22 on the other. Both windows must read at least 25 on the portrait.

## 4. MUST list to 8.5 (clips; open only if reinstated)

- **R2-C1 (= C3). Walk speed in Studio.** At the pet's real follow speed, check the 48-frame slither does not skate. The stride is 5.19 BU per cycle, about 24 studs in 1.6 s at 30 fps (about 15 studs/s). Record the number in `CLIP_NOTES.md`.
- **R2-C2 (= C4). Reference disclosure.** Idle and walk cite Haku (a flying dragon, Sakugabooru #225387) and Wikimedia studies, not the site overlay. The owner needs the clip titles, tags and frames before the gate.

## 5. TO 9+ list

- **T-a. Snout stud dots.** Fewer or smaller stud dots on the snout tip only; the close-up still reads bubble-wrap there.
- **T-b. Tail length.** Drop one tail segment (Tail4 or the tip) so the `gamelook_tq` silhouette is tighter.
- **T-c. Idle breath from 5 studs.** Confirm the 3 deg per neck bone breath reads in motion (no stills show it).

## 6. Pass / fail checklist

| # | Check | Result |
|---|---|---|
| 1 | Tris <= 15k | PASS (10,588) |
| 2 | Height 10.5, tallest of the Fire egg and the secrets | PASS |
| 3 | Species reads at 64 px | PASS |
| 4 | Near eye reads at 64 px | PASS (builder's note; far eye hidden) |
| 5 | Face reads at 5 studs | PASS (eye slits and cheek plate visible) |
| 6 | Head is angular, not plush | PASS (cheek plate); snout dots remain (T-a) |
| 7 | Body reads as mass, not a worm (game view) | PARTIAL (neck bands, R2-M1) |
| 8 | Brows do not read as horns | FAIL (R2-M2) |
| 9 | Dark rich body main colour (game 45.0 %) | PASS |
| 10 | Obsidian <= 40 % (game 28.6 %) | PASS |
| 11 | Gold >= 25 at 64 px, kit counter | PASS (builder's 32; not re-measured) |
| 12 | Gold >= 25 at 64 px, second window | NOT RECORDED (R2-M4) |
| 13 | Gold reads as the hero | PASS |
| 14 | Accent and cores distinct from siblings | PASS (ruling A, not reopened) |
| 15 | Outclasses the Fire egg and 1 % secrets at 128 px | FAIL (R2-M3) |
| 16 | Parts floating, poking or wrong from below | PASS (builder's collision numbers) |
| 17 | Clip: neck, spine, head pitch, reseat, loops, rest, ground | PASS (builder's numbers, not re-run) |
| 18 | Clip: molt legible from the front | PASS |
| 19 | Clip: reseat slower than rise | PASS |
| 20 | Clip: renders current | PASS |
| 21 | Clip: roar | PASS |
| 22 | Clip: walk speed in Studio | OPEN (R2-C1, lead ruling skipped) |
| 23 | Clip: reference disclosure | OPEN (R2-C2, lead ruling skipped) |

## 7. Do not re-open

- The deep sulfur-blue accent and white-hot cores (ruling A). The cold-blue vent read is accepted (ruling B).
- The body colour: do not lift it (round 4 and 5 NICE). R2-M1 changes the neck shape, not the colour.
- House gold stays the hero. The ember and blue flame aura is VFX for later.

## 8. Next round

Send with the fixes applied:
- `close_front.png` and `_close_sheet.png` (R2-M2, M3).
- `gamelook_game.png` (R2-M1, the neck bands).
- `_icons_strip_64.png` and `_icons_strip_128.png` (R2-M3, the 128 px blue read).
- `gate_f85.json` with both gold windows (R2-M4).

The model goes to the owner at 8.5 or better after R2-M1 to M4. The clips go to the owner at 8.5 after R2-C1 and C2, if the lead reinstates them.
