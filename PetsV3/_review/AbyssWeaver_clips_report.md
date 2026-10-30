# Abyss Weaver - builder report for the CLIP review (2026-10-14)

## Model fixes from review 1 (applied exactly as written)
- **FIX 1** eyes: socket 0.028, lens 0.0165, pupil 0.0115, the HOT spot deleted, thin V-brow (+0.040, n 0.010, 0.022 /
  0.026).
- **FIX 2** rift: torn ORCHID edge (JAG), the meandering HOT crack (ZZ) + 2 side fractures; the closed lip frame kept.
- **FIX 3** belly band: `shell(..., nr=6)`, 205-335, off 0.014.
- Now: tris **11,956** (ceph 672 · head 1,252 · face 1,400 · abdomen 4,632 · legs 4,000) · H 1.10 · lowest -0.005 ·
  idle f0 `collision_free`.
- **Shares (side / tq / game / front):**
  - ARMOR 28.0 / 26.1 / 39.8 / 23.7
  - ARMOR_D 36.2 / 43.8 / 32.0 / 43.6
  - dark 64.2 / **69.9** / 71.8 / 67.3
  - VELVET 21.8 / 12.0 / 9.2 / 14.4
  - SILK 3.3 / **1.1** / 1.1 / 0.7
  - glow 1.8 / 3.9 / 4.9 / 3.6
  - GOLD 4.1 / 7.1 / 8.9 / 7.6
  - BLACK (edge artefact) 4.8 / 5.1 / 4.2 / 5.6
- **Gold @64:** my counter 45 / 73 · **your brief's counter 56 / 86** (gate >= 45 / >= 60). Both are in
  `_tools/game_icon.py` now.
- **Pack (`AbyssWeaver/renders/`):**
  - `_model_sheet_600.png` (bind), `_model_tq_600.png`
  - `_face_close.png` (front / PORTRAIT direction / tq, 700 px), `_rift_close.png` (tq / game / top)
  - `_icons2_strip_64/128.png` (portrait + game-cam icons + the 6 comparisons), `_icons_strip_64/128.png`
  - `_AB_ThornbladeMantis_64/128.png`, `_AB_Kraken_64/128.png`
  - `_flat_sheet.png`, `_shares.txt`
  - `_limits_sheet.png` (rest, roar s35 tq / game / FRONT, present, cast, Spine yaw, Head yaw + pitch): **0 hits all**

## Clips (brief section 6 + your section 6 rules) - the gate
| clip | n | loop | result |
|---|---|---|---|
| idle "STILL HUNTER" | 120 | yes | linear 0, loop closed, planted-foot drift 0 |
| walk "SCUTTLE" | 32 | yes | linear 0, loop closed, **slide 0**, foot_z_var 0, stride 0.293 |
| roar "FANG FLARE" | 72 | no | linear 0 |
| act_riftweave "RIFT WEAVE" | 120 | no | linear 0 |
- **`collision_free: true` at step 1, every frame**, all section 5.5 pairs + 5.6 capsules.
- ground_min_z -0.005 on every clip (claw tips).
- **Events:**
  - idle: pulse1 .333, flex .583, pulse2 .833
  - roar: flare .306, rasp .361, pulse .500, stab .556
  - act: rift .200, silk1 .283, silk2 .400, silk3 .517, cast .667
  - The kit stores one time per event name, so repeated beats are numbered.
- **Pose renders** `pose_<tq|side|game|front>_<clip>_<f>.png`:
  - roar 10 / 22 / 40 / 60
  - act 12 / 24 / 34 / 48 / 62 / 80 / 92
  - idle 13 / 40 / 70
  - walk 0 / 8 / 16
  - overview strips `_clips_v1_tq.png`, `_clips_v1_game.png`, `_clips_v1_side.png`, `_clips_v1_front.png`

## How the clips implement the brief (and where they differ - please approve / overrule)
- **References** (`_review/ANIM_REFERENCES_1014.md`): #7 HTTYD (idle), #4 + the metachronal math (walk), #6 MU scare
  pop (roar), #5 "Attack" tell -> snap (cast). No spider clip exists on animationreference.org or Sakugabooru
  (search logged); no credits spent.
- **Walk:** `walk8` = petkit `walk_cycle` with the per-pair lift; offsets / duty 0.58 / stride half 0.085 as section
  5.4; body bob 0.006 x 2, yaw 1.2, roll 0.8, head counter-yaw 0.5, abdomen yaw lag (-0.06 phase) + lift 1.0 x 2; palps
  alternate +-6 (pitch, L / R opposite) with legs 1.
- **Idle:** your table. The taps are claw lifts solved every frame; the listen turn = Spine yaw +8 with the Head
  leading by 2 f; the fang flex, palp rasp, pump and twitch as briefed.
- **Roar W1 - the crouch palps:** in the gather the palps LIFT -6 (the brief's "tuck +12" swings their tips down into
  the ground: -0.053 at f10).
- **Roar W2 - the flare palps:** spread 28, base pitch **+12** with the rasp +-7 on pitch, which stays inside the
  femur-clear band +5..+19 found in W4. At +5 the rasp's -3 cut the leg-1 femurs.
- **Roar W3 - the FK start:** legs 1 start the FK at the rest shape at **f14** (planted IK to f13) and legs 2 at
  **f16** (IK to f15). At the brief's f12 the gather crouch (z -0.04, nose +5) would put a rest-shape FK claw about
  0.08 under the ground.
- **Roar W4 - the raise and land:** the raise is keyed every 2 f to (15, 80, 20) at f22, with the **s35 shin forward
  yaw easing with the opening (35 x shin / 80)**. Legs 2: (5, 40, 10), no shin yaw. Tremble +-2 every 3 f.
  - Landing (shin closes first): legs 2 (3, 18, 5) f60 -> (1, 6, 2) f61 -> IK f62.
  - Legs 1 (15, 55, 14) f62 -> (12, 25, 8) f64 -> (3, 8, 3) f65 -> IK f66.
  - The leg-1 ankle peaks at (0.479, -1.594, 1.305): your raised limit 1.32.
- **Roar W5 - the fang stab:** "Fang +12" is played as the closing strike: unfold 65 -> 53 at f40 -> 65 at f44, since
  77 would break the 70 limit.
- **Act:** your table.
  - Root z +0.02 / +0.06; Spine +3 / -6; Pedicel -4; Abd +8 -> -8 (PRESENT, rift to the game cam) -> -8 / +1 (f77
    in-between) / **+10 hard stop f80** -> -2 f92 -> 0 f100; Root y +0.03 at f78; fangs unfold 35 at f80.
  - Draws L4 f28 / R4 f42 / L4 f56: lift 0.04 (+2 f) -> (+-1.02, 0.70, 0.45) (+6 f, toe 30) -> hold 2 f -> back to rest
    (+12 f) -> planted. Per draw: Spinner flick -12 (3 f), Abd pump -3, Pedicel yaw 4 AWAY from the drawing leg (the
    abdomen tip swings to the far side).
- **Not keyed:** the optional Leg2 shin yaw -15, and the SILK_D spinneret tips (optional; not done).
