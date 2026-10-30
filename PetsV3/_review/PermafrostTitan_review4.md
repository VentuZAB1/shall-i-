# Permafrost Titan - round 4 re-check of review 3 MUSTs (model + clips) (2026-10-27) - APPROVED WITH FIXES (NICE only)

**Score: 8/10 for a 2.5 % SECRET.** Ship at 8/10 or better. **No MUST is left.** Every round-3 MUST is met on the numbers I could
check. The remaining items are small documentation and polish points (NICE).

## Round-3 MUST check

| # | Round-3 MUST | Result | Evidence (what I checked) |
|---|---|---|---|
| 1 | Kneel reads from the front, the 3/4, and behind | **MET** | The Spine rolls -7.0 deg in the hold (sign: toward +X, the pet's right = the kneeling side). Chest counter-roll +3.5. The front render at f18 and f40 shows the kneeling leg visibly lower than the standing one. The 2x game-camera beats show one knee down with the foot lying back. |
| 1a | Chest vs spine <= 5 deg | **MET** | Chest local angle 4.04 deg in the hold, 4.29 at the f20 dip, **4.67 at the f58 lean**. |
| 1b | Pelvis drop keeps the knee on the snow | **MET** | Spine y min -0.280 at f20 (the settle), -0.272 held, back to 0 by f84. The gate reports ground -0.009 at f20. |
| 2 | Refs: 1-3 real clips, concrete, cited (owner rule) | **MET (lead ruling)** | `ANIM_REFS.md` section C is concrete: the site tag `/tags/kaiju-no-8`, Sakugabooru posts #257646 and #254909, timestamps and frames, five-part observations (K8a-c), and a per-clip use. See the caveats below. |
| 3 | Back pale share >= 11-12 % on the stated method | **MET** | I reproduced the method: nearest palette colour for every figure pixel of `flat_game.png` (background = max channel < 6). **ICE_W 13.5 %** (lead: 13.5). |

Other round-3 items:
- Back gold, game camera at 64 px: **21 px** by my hue count (builder 22, gate 20). PASS, with a thin margin.
- Portrait gold at 64 px: 31 px by my count (builder 36, gate 25). PASS.
- Caps in source (`pets/PermafrostTitan.py` L246, L254): 0.150 x 0.170 x 0.036 and 0.084 x 0.152 x 0.035, as stated. No spikes, no crown.

## What I looked at

- Clips: `PermafrostTitan.json` (4 floats per frame per bone, identity = rest), recomputed with my own decomposition: roll and pitch
  of each bone, per-frame swings, combined forward pitch, rest match. `_scratch/clipgate_r4.txt`.
- Renders: `_kneel_views.png` (f18 / f40 / f58 from front, tq, back, game camera), `_beats2x_kneel.png`, `_beats2x_roar.png`,
  `_model_sheet.png`, `_icons_strip_64.png`, `_icons2_strip_128.png`, `flat_game.png`, `flat_back.png`, `flat_side.png`, `model_back.png`.
- Notes: `CLIP_NOTES.md` (ROUND 4), `MODEL_NOTES.md` (ROUND 4), `ANIM_REFS.md` (sections A-C).
- Not re-run: Blender (the brief forbids it). The knee heights (left 0.498, right 0.196 at f30) are the builder's forward-kinematics
  values; I did not recompute them, but the front render shows the asymmetry they describe.

## Clip-gate numbers (recomputed from the JSON)

| check | value | limit | result |
|---|---|---|---|
| collision_free | true (gate) | true | PASS |
| ground min z | idle / walk / roar 0.000, act -0.009 at f20 (settle) | >= -0.02 | PASS |
| loops | idle 0 / 0, walk 0 / 0 | 0 | PASS |
| walk slide, foot z var | 0.0, 0.0 | ~0 | PASS |
| stride | 0.645 BU, root in place (z range 0) | - | PASS |
| max per-frame swing (any bone) | 22.2 deg (act, Shin_L f7) | <= 60 | PASS |
| quaternion sign flips | 0 | 0 | PASS |
| spine lean (not capped) | -4 deg hold, -10 deg at f58 (forward, K3) | - | note |
| combined forward pitch (spine+chest+head) | max -20.0 deg at f58; -18 in the hold | - | note |
| head alone (Head bone = head + neck) | -12 to -13.5 deg down, roar +10 up | down <= 20, up <= 30 | PASS |
| roar arms | 9.0 deg peak (f34); 8 at f22 and f50 | - | PASS (as noted) |
| roar per-frame swing | 2.2 deg | <= 60 | PASS |
| act rest match vs idle f0 | 0.00 deg torso/arms/feet, 0.40 deg legs (bind offset) | exact | PASS |
| event frames | events are stored as clip fractions; 0.25 x 120 = f30 (frost1), 0.3 x 100 = f30 (core1), 0.18 x 100 = f18 (icecrack) | match the notes | PASS |
| total triangles | 7,552 (gate) | <= 15k | PASS |

The elbows bend 4 deg more (`Fore` max 26 deg, was 22). The kneel settle is a 0.008 dip at f20, back by f23, as stated.

## Model round 4 (short)

- Shoulder caps read as crust, not a shelf, and they add pale mass to the back without a spike or a crown (`_model_sheet`, back view).
- The back ring (0.27 BU) reads from the game camera at 128 px (112 px of gold on the game-camera icon).
- The round-3 NICE items are in source (shin guard 0.028, chest taper 0.66, brows 30 deg).

## Judgement on the outclass question (from behind)

- **Gold:** clear separation. The Titan's game-camera icon carries 21 px of gold; the Yeti's back carries none.
- **Pale mass:** now at the owner's target (13.5 % on the stated method). The Yeti's round-2 pale figure was 28 % on a palette game
  view, but that was a different method, so I do not compare the two numbers directly. On the lit back render (same mask as before):
  Titan 8.8 %, Yeti 16.8 %. So the Titan's back is still paler-poor on the lit view, and its presence rests on the gold ring.
- Not a MUST, because the owner's target is met. If the owner wants the Titan clearly paler than the Yeti from behind, that is a
  separate design call.

## NICE (do these too)

1. **Mislabelled round-4 MUST number.** `CLIP_NOTES.md` ROUND 4 names the kneel settle "MUST 2". The coordinator's list has MUST 2 as
   the refs. Rename the settle to "NICE (ref K8a)" so the numbering matches the review.
2. **Reference frames are not on disk.** The K8 frames were stepped in a browser and nothing was saved to `renders/`. Save the three
   contact sheets (or the crops for K8a, K8b, K8c) to `PermafrostTitan/renders/refs/` so a future reviewer can check the observations.
3. **Order of the refs.** The owner rule says to look at references before keying. Section C was added after the clips were keyed
   (CLIP_NOTES says so). The lead accepted the section, and the clips were not changed except the settle. Record this in ANIM_REFS
   (one line), so the timeline is clear.
4. **Gold margin at the game camera is thin (21 px, gate 20).** Optional: a 0.01 BU larger back ring (0.28 BU) would give about 25 px.
5. **Kneel from the 3/4 still reads mainly through the tilt.** The knee-down is clear at f40 in the game-camera beat, and fine in the
   front. If the next review wants more, the kneeling foot could be turned out 10 deg so the sole shows.
6. **Documentation:** CLIP_NOTES says "chest vs spine <= 4.7 deg (the f58 lean = the Spine 10 deg + the Chest 4 deg)". The JSON gives
   the Chest local angle at f58 as 4.67 deg, so the text is correct. Keep it.

## Pass / fail checklist (round 4)

| Check | Result |
|---|---|
| Round-3 MUST 1: kneel reads from front, 3/4, behind | PASS |
| Chest vs spine <= 5 deg (4.0 hold, 4.7 at the lean) | PASS |
| Knee on the snow, drop keeps the contact (ground -0.009) | PASS |
| Round-3 MUST 2: refs, 1-3 clips, concrete, cited | PASS (concrete; NICE 2, 3) |
| Round-3 MUST 3: back pale >= 12 % on the stated method (13.5 %) | PASS |
| Back gold >= 20 px at the game camera (21) | PASS (thin) |
| Portrait gold >= 25 px (31) | PASS |
| collision_free, loops, slide 0, linear 0 | PASS |
| Per-frame swing <= 60 deg (max 22) | PASS |
| Head + neck: down <= 20, up <= 30 (no separate Neck bone) | PASS |
| No head shake, no airborne spin, no sign flips | PASS |
| Acts in place, end in rest (<= 0.40 deg on legs) | PASS |
| Roar: head lift and arms out read as a bellow (2x beats) | PASS |
| Tris <= 15k (7,552) | PASS |
| No crown, spikes, cyan, glow, or Neon | PASS |
| Reference frames saved on disk | NOT DONE (NICE 2) |
| Clip gate | PASS |

## Next round

- None required. The clip gate and the model are approved. Apply the NICE items (1 and 2 are documentation and file saves) and report.
