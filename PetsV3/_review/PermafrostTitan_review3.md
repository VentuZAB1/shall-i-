# Permafrost Titan - model round 3 + CLIP GATE review (2026-10-27) - APPROVED WITH FIXES

**Score: 7/10 for a 2.5 % SECRET** (model round 2 was 7/10). Ship at 8/10 or better.

- **Model (round 3): APPROVED.** The back gold is now a clear rarity cue from the game camera (23 px at 64 px, my count),
  and the Yeti has none. One target is borderline: the back pale share is 10.5 % by my palette count (builder 11.5 %, target 11).
- **Clips: the technical gate PASSES** (0 collisions, ground >= -0.005, linear 0, loops closed, walk slide 0, swings <= 14 deg/frame,
  rest matches, chest-vs-spine and head+neck limits hold). **Two things block the 8/10:** the kneel does not read as a kneel from the
  front or the player's 3/4 view, and the owner's animation-reference step is incomplete.

## What I looked at

- Model: `PermafrostTitan/MODEL_NOTES.md` ROUND 3, `renders/model_back.png`, `under_lowback.png`, `gamelook_game.png`, `flat_game.png`,
  `_icons2_strip_64.png` / `_128.png`, `close_back.png`, `_scratch/game_icon.json`, `_scratch/clipgate.txt`, source `pets/PermafrostTitan.py`
  (L110, L138, L191, L210, L246, L254).
- Clips: `PermafrostTitan.json` (the actual keyframes: 4 floats per frame per bone, identity = rest), `CLIP_NOTES.md`, `ANIM_REFS.md`,
  `renders/_pose_tq_sheet.png` (24 beats, small), `renders/_cv_kneel_side.png` and `_cv_kneel_front.png` (10 beats each, fixed cameras),
  `cv_tq_act_kneelrise_18/40/58.png` (3/4 view), `_review/PermafrostTitan_plan.md` section 10 (the suggested reference tags).
- Vault: `06 Modelling and Art/Creature Animation.md` (clip gate), owner rule `feedback-animation-references` (1-3 clips from animationreference.org).
- Not re-run: the Blender gate (the brief forbids running Blender). The clip numbers are read from the JSON, not from the builder's text.

## Measured facts

**Model**
- Game-camera gold at 64 px: **23 px** (builder 24; gate 20). At 128 px: 114 px (round 2: 71). PASS.
- Portrait gold at 64 px: **31 px** (builder 37; gate 25). PASS.
- Back ring solid: the centre matches the ice caps again (not a hole). Ring is a ring only (no settings, spikes, or crown). PASS.
- Back pale share, palette render `flat_game.png` (back 3/4 game view; the ring sits on the hump), figure pixels only: **ICE_W 10.5 %**
  (builder 11.5 %). Round 2 builder figure was 10.4 %. The target is 11, so this is borderline.
- Same lit mask on `model_back.png` (back camera): Titan **8.3 %** (round 2: 8.1 %), Yeti **16.8 %** (round 2: 16.3 %). The shoulder cap
  change did not move the back-camera pale share by a measurable amount.
- Yeti reference (its round-2 notes, palette game view): PLATE_ICE **28.1 %**. The Titan is still well short on pale mass from behind.
- NICE items landed in source: shin guard depth 0.028, chest bottom taper 0.66 (L110), brows 30 deg (L210), back ring outer
  dia 0.27 BU (L138), upper cap 0.130 x 0.150 x 0.033 (L246), lower cap 0.076 x 0.145 x 0.034 (L254).
- Tris: 7,552 (the gate's body count). Cap 15k. PASS.
- Value shares, flat palette on figure pixels: MAUVE 54.7 (game) / 59.8 (side) / 59.1 (tq), PLUM 14.8 / 9.4 / 12.0, GOLD 1.9 / 1.6 / 3.9.
  The palette render is the un-darkened colour, so it does not show the in-game colour.
- In-game preview (`gamelook_game.png`): dominant bucket still about (72,64,104). The lift to (146,101,178) does not show in game. NICE 3 stays
  open until Studio (not possible from here).

**Clips** (all numbers from `PermafrostTitan.json`; identity = rest)

| clip | check | value | limit | result |
|---|---|---|---|---|
| all | collisions | 0 | 0 | PASS |
| act | ground min z | -0.005 (f18, knee cap and toes on the snow) | >= -0.02 | PASS |
| idle / walk / roar | ground min z | 0.000 | >= -0.02 | PASS |
| idle, walk | loop closure | 0 / 0 | 0 | PASS |
| walk | slide, foot z var | 0.0, 0.0 | ~0 | PASS |
| walk | stride | 0.645 BU, root in place (z range 0.000, y bob 0.038) | - | PASS |
| act | rest match vs idle f0 | 0.00 deg on torso, arms, feet; 0.40 deg on legs (the rig's bind offset) | exact | PASS |
| all | max per-frame swing (any bone) | 14.0 deg (act, Shin_R) | <= 60 deg | PASS |
| all | quaternion sign flips | 0 | 0 | PASS |
| act, roar | chest vs spine (chest local) | 4.0 deg (act), 3.5 deg (roar) | <= 5 | PASS |
| act | spine lean (not capped by the rule) | 10.0 deg | - | note |
| act | head bow (pitch down), Head bone | 12.0 deg | head+neck down <= 20 | PASS |
| roar | head lift (pitch up), Head bone | 10.0 deg; spine+chest+head sum 15.1 deg | up <= 30 | PASS |
| roar | head motion | tuck -4 deg, lift +10, settle to 0 (no oscillation) | no shake | PASS |
| act | root (Spine pos) | drops 0.30 BU vertically (y), 0.09 BU forward (z), back to 0 by f84 | in place | PASS |
| act | leg peaks (kneel) | Leg_L 65.3, Shin_L 76.2, Leg_R 20.7, Shin_R 78.1, Foot_R 69.7 deg | - | note (see MUST 1) |

- **Neck:** the rig has no Neck bone (the head pivots at the throat). The head+neck pitch limits apply to the Head bone and pass
  (ThunderRex's review applied the neck limit to a separate Neck bone). Not a MUST, but say so in CLIP_NOTES.
- **Events:** `frost1`, `core1`, `frost2`, `core2`, `glint`, `icedust`, `icecrack` are numbered where repeated, and none is named `end`. PASS.
- **Notes disagree:** ANIM_REFS says "chest 10 deg" for the forward lean. The JSON says the Spine leans 10 deg and the Chest 4 deg,
  so ANIM_REFS is wrong (NICE 1).

## Beat-by-beat judgement (player's read)

- **idle (120 f):** weight shift and breathing, small (max 3 deg on the spine). Reads as a giant standing and breathing. PASS.
- **walk (48 f):** heavy flat-foot stride, body sinks at contact, low swing, arms 4 deg. Reads as heavy and planted. PASS.
- **roar (66 f):** lean in, head lifts 10 deg, arms out 9 deg (notes say 8), core and glint pulses, slow settle. Reads as a bellow. PASS.
- **act_kneelrise (100 f):**
  - **Side view:** clear. The right knee goes to the snow at f18, the rear shin lies back, and the body sinks and rises. PASS.
  - **Front view (`_cv_kneel_front`):** not clear. Both legs look the same height, the body just looks lower and wider. The leg step
    is toward the camera, so it is foreshortened.
  - **Player's 3/4 (`cv_tq_18/40`):** reads as a crouch with the bezel showing. The kneeling knee is barely visible.
  - **Game camera (behind):** not rendered. The game camera sits behind the pet, so this is the view that matters most.
  - Fists rest at the sides beside the thighs (the no-IK liberty). Accept: no visible intersection in the side or front views.
  - Rise and rest read correctly (f76-84).

## MUST (in priority order)

1. **The kneel must read as a kneel from the front and the player's 3/4 (and from behind).** Right now only the side view shows the knee down.
   - The left leg steps forward (Leg_L 65 deg) while the right knee bends (Shin_R 78 deg). The step is toward the camera from the front,
     so it is hidden.
   - Give the kneel a lateral asymmetry: roll the **Spine** about 6-8 deg toward the kneeling side (right) from f10 to f50, and counter-roll
     the **Chest** so chest-vs-spine stays within 5 deg.
   - Also widen the left-foot step (`foot forward 0.22` in the notes) to about 0.30 BU, so the standing leg separates from the kneeling one.
   - Target: in the front view at f30, the right knee cap is at least 0.10 BU lower than the left knee cap.
   - Render `act_kneelrise` at f18, f40, f58 from the **front, 3/4, and game camera (behind 3/4)** and show the three renders
     with the next round. Keep the 0 collisions and the ground >= -0.02 limit (the knee may touch the snow, but no further than -0.02).

2. **The owner's animation-reference rule is not complete (VERY IMPORTANT).** The rule says to pull 1-3 clips from animationreference.org
   before keying, and to cite them.
   - ANIM_REFS shows the builder browsed `/tags`, `/tags/walk-cycle`, `/tags/body-mechanics`, `/tags/creature`, `/tags/dragon`, and the locomotion
     guide. It never tried the three tags the plan itself suggests (section 10): **"giant walk heavy", "knight kneel", "golem roar".**
   - The builder fell back to Muybridge Plates 27 and 356 (still frames). The brief's fallback applies only when no video can be opened, and the
     builder could open tag pages, so the fallback is not yet justified.
   - Fix: try the three suggested tags (kneel and roar first), open **1-3 clips**, and add a Reference table with the clip title, the tag, the
     frames, and what is taken (the kneel and roar notes should cite the clip, not only the plates).
   - Save the reference crops or contact-sheet frames used (for example `renders/refs/`), so K1-K4 and W1-W5 can be checked. The folder
     has no reference images, so I could not verify those observations.
   - The `kaiju-no-8` cuts are not in ANIM_REFS. If they were not tried, list them as tried or not tried.
   - The Muybridge plates may stay as a supplement, but not as the only reference.

3. **Back pale share: target met only by the builder's count (MUST 2 of round 2).** My palette count is 10.5 % (target 11), and the back
   camera is 8.3 % (round 2 was 8.1 %, so the cap change did not move it). The Yeti's back is about 28 % pale plate by its palette count.
   - Make the upper shoulder caps a little bigger: **0.140 x 0.160 x 0.035** (L246), which adds about 1-2 points on the back. Keep `rnd`
     0.30, the three chunks, and no spikes or crown on the hump.
   - Report the pale share with a stated method: the `flat_game.png` palette, figure pixels only, background excluded. Target **>= 12 %**
     on that method, so it clears 11 with margin.

## NICE (do these too)

1. ANIM_REFS: fix "chest 10 deg" to "spine 10 deg, chest 4 deg" (the JSON says so).
2. CLIP_NOTES: say that the Titan has no Neck bone, and that the head+neck limits (up <= 30, down <= 20) apply to the Head bone. The neck <= 8 limit does not apply.
3. The roar arms are 9 deg in the JSON, not 8. Correct the text, or make it 8.
4. Gold counts: state the method. Builder 24 / 37 vs my 23 / 31 (same 64 px cells, different threshold). Both pass the gates.
5. The 24-beat pose sheet is too small to judge a kneel (280 px tiles). Render the kneel and roar beats at 2x.
6. In-game colour (round 2 NICE 3) and pet-facing (NICE 5) still need Studio.
7. The fists hover at the sides in the kneel. It is fine. A slight elbow bend (3-4 deg) at f30-50 would make them read as resting on the thighs.

## Pass / fail checklist (model round 3 + clip gate)

| Check | Result |
|---|---|
| Back gold visible from the game camera (gate 20 px at 64) | PASS (23 px) |
| Back gold big enough to read from behind at 128 px | PASS (114 px) |
| Back ring solid, not a see-through hole | PASS |
| Back pale share >= 11 % (palette game view) | BORDERLINE (10.5 % mine, 11.5 % builder; MUST 3) |
| Round-2 NICE items (shin guard, chest taper, brows 30 deg) | PASS (in source) |
| Portrait gold >= 25 px | PASS (31 px) |
| No crown, spikes, cyan, glow, or Neon | PASS |
| Tris <= 15k | PASS (7,552) |
| collision_free | PASS |
| ground_min_z >= -0.02 on every clip | PASS (-0.005) |
| Audit: linear 0, loops closed, walk slide 0 | PASS |
| Walk heavy, in place | PASS |
| Idle, weight shift, no head tilt, feet planted | PASS |
| Roar reads as a bellow, head lift within limits | PASS |
| Chest vs spine <= 5 deg | PASS (4.0) |
| Head+neck pitch: up <= 30, down <= 20 | PASS (up 10, down 12, Head bone) |
| Neck <= 8 deg | N/A (no Neck bone; see NICE 2) |
| No head shake | PASS |
| No airborne spins or flips; no quaternion sign flips | PASS |
| Per-frame limb swing <= 60 deg | PASS (max 14) |
| Acts play in place (root returns to 0) | PASS (y drop 0.30 BU, z 0.09 BU, back to 0) |
| Act ends exactly in rest | PASS (<= 0.40 deg) |
| Kneel reads from the side | PASS |
| Kneel reads from the front and the player's 3/4 | FAIL (MUST 1) |
| Kneel reads from the game camera (behind) | NOT CHECKED (MUST 1) |
| Events named after the effect, numbered, no `end` | PASS |
| Animation references: 1-3 clips from animationreference.org, cited | FAIL (MUST 2) |
| Reference observations checkable (reference frames saved) | FAIL (MUST 2) |
| Liberty: fists at the sides (no arm IK) | ACCEPTED (NICE 7) |

## Next round (short, clips and back only)

- The three kneel renders (front, 3/4, game camera behind 3/4) at f18, f40, f58, with the Spine/Chest roll values.
- `ANIM_REFS.md` updated: the three suggested tags tried, 1-3 clips cited with titles, tags, frames, and the reference frames saved.
- `model_back.png` and `flat_game.png` with the caps change, and the pale share stated on the method above.
- No full model gate again. The clip gate closes after MUST 1-2 land.
