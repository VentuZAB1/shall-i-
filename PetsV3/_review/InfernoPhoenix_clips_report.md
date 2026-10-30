# Inferno Phoenix - builder report for the CLIP review (2026-10-14)

## Model fixes from review 1 (all applied; regenerated pack)
- **F1-F3** taken verbatim from your `specs\PhxF2.py` (STREAM table, toe splay -14 / 0 / +20 mirrored, hood-tail cape +
  one burning collar row). **F4** from `PhxB.py` (continuous culmen: hook seg + tip). **F5** `H_MODEL = 2.034`.
- Also removed: the PALE belly shingles on the `low` block (your review: invisible, +0.1 %). They sat between the legs
  and were in the walk's collision zone.
- Now: tris **11,120** · H 2.04 (crest anchor 2.034) · idle f0 `collision_free` · `path_test` **0 hits on all 10** ·
  the 6 limit poses **0 hits** (L4 roar now with LIFT1; L5 rising frame with X1 -18 / X2 -6 / X3 +4, lowest 0.134).
- Shares (side / tq / game / front): BASALT+D 42.3 / 35.6 / 46.1 / 24.0 · EMBER 24.0 / 32.9 / 23.6 / 40.3 · PALE
  1.6 / 5.5 / 1.3 / 11.5 · FIRE 23.8 / 15.3 / 20.1 / 8.7 · GOLD 3.0 / 4.6 / 2.5 / 5.0 (you accepted the misses as
  tolerances).
- Pack (all `InfernoPhoenix/renders/`): `_model_sheet_600.png` (bind), `_model_tq_600.png`, `_fold_sheet_600.png`
  (idle f0), `_face_close.png` (F4 beak), `_icons_strip_64/128.png` (Phoenix + 12), `_AB_Thunderbird_64/128.png`,
  `_AB_Ivonrath_64/128.png`, `_flat_sheet.png`, `_shares.txt`, `_limits_sheet.png`.

## Clips (all brief section 7 + your section 6 rules) - the gate
| clip | n | loop | result |
|---|---|---|---|
| idle "SMOULDER" | 120 | yes | linear 0, loop closed, foot drift 0 |
| walk "STALKING STRUT" | 28 | yes | linear 0, loop closed, **slide 0**, foot_z_var 0, stride 0.50 |
| fly "BURNING WAKE" | 32 | yes | linear 0, loop closed |
| takeoff | 30 | no | linear 0 |
| land | 32 | no | linear 0 |
| roar "FIRE-TRAIN SCREECH" | 66 | no | linear 0 |
| act_rebirth "ASHES TO FLAME" | 104 | no | linear 0 |
- **`collision_free: true` at step 1** on every clip, every frame (all check_pairs + joints).
- **ground_min_z** (every frame): idle -0.012 · walk -0.015 · fly +0.437 · takeoff -0.012 · land -0.012 · roar -0.012 ·
  act -0.012 (all at the talon tips).
- **Events:**
  - idle: lick1 .192, ember1 .200, lick2 .442, lick3 .692, ember2 .700, flare .733
  - takeoff: launch .367
  - land: touch .531
  - roar: screech .379, rattle .455
  - act_rebirth: ignite .077, pyre .192, ash .288, heartbeat1 .346, heartbeat2 .404, rebirth .519, reborn .692, touch .788
  - The kit stores ONE time per event name, so repeated beats are numbered (lick1-3, ember1-2): the Studio side matches
    the prefix.
- Pose sheets (300 px, tq / side / game) for every frame the brief names: `pose_<view>_<clip>_<f>.png`, plus overview
  strips `_clips_v1_tq.png`, `_clips_v1_side.png` and `_clips_v1_game.png` (idle 46 / 88, walk 7, fly 0 / 16, takeoff
  13, land 6 / 17, roar 20 / 26 / 40, act 26 / 36 / 58 / 72 / 80).

## References (owner rule; `_review/ANIM_REFERENCES_1014.md`)
#5 bird flapping + #8 banshee (fly, takeoff, land, the rise) · #3 Sea Beasts (jaw lags the head) · #6 Monsters
University (train rise) · #7 HTTYD (look-back hold) · #9 humpback mass (pyre slump) · #4 dragon walk (strut). The three
NEW references the brief asked for "if available" (bird takeoff, creature slump, tail display) do not exist on
animationreference.org (search logged in the refs file); no credits spent.

## Deviations in the clips (please approve or overrule)
- **C1 walk: lift 0.08 (brief 0.10) + the swing foot 0.06 wide (Thunderbird 0.025).** At mid-swing the high step drives
  the trouser's inner face into the belly / lower body (Shin|Spine 16-19 tri pairs at f6-7 / f20-21; rest-space x
  -0.07..-0.15, z 0.34-0.61 vs the belly x -0.01..-0.10, z 0.55-0.67). Tested: lift 0.07 / 0.08 alone -> 11-18; dip
  -0.03 -> 15; roll 2 -> 4; stride half 0.11 -> 13-18; **wide swing 0.06 + lift 0.08 -> 0**; wide swing + lift 0.10 -> 10.
- **C2 idle re-grip:** Leg_R lifts 0.045 with a 6-deg toe curl (brief 0.03 + the Thunderbird's 14 deg: the curled
  talons went to -0.041).
- **C3 crouches (your rule 1):** takeoff crouch -0.02 / -0.035 / -0.045 / -0.05 (f3-10; brief -0.04 .. -0.12); land
  absorb -0.04 at the touch (Thunderbird -0.09); act pyre and wind-up at -0.05 (brief -0.13 / -0.14) with heartbeats
  +0.012 / +0.018 on top.
- **C4 streamer floors (your rule 2/3):** idle drift biased up (X1 0..+3, X2 -1..+3, X3 -1..+5) and the licks overshoot
  only -1; walk X1 4 +-2, X2 +-3, X3 2 +-4 (X3 >= -2); roar release X1 -4 / X2 -2; land overshoot -3 / -2 / -2; act pyre
  -4 / -4 / -2; takeoff drag X1 -12; act rising hang X1 -18 / X2 -6 / X3 +4 and X1 >= -6 in beat 1 (until z 0.30).
- **C5 roar (your rule 4):** the cloak holds LIFT1 from f5 to f52 (FOLD f56); the train keys are the brief's
  (+56 / +24 / -14 with a 2-f chain lag, the rattle +-3 / +-5 with L / C / R 1 f apart).
- **C6 fly:** FPITCH 45, Neck -8 / Neck2 -8 / Head -28 with the gyro split .75 / .75 / 1; legs D9 (THI 60, roll 18,
  SHI -40, FOO 70); plumes per brief (X1 -22, travelling S +-5 / 9 / 13, lag .10, X1 peak .15 after the downstroke,
  fan L -8 / R +8, X3 lateral +-3 offset .25), chains offset .03 cycle.
- **C7 act legs (D8):** FK (24, -10, 40) f57 -> (50, -30, 66, spread 15) f66-76 -> reach (-14, 6, -20) f80; planted
  f0-53 and f82-104; `lift_air_frames(54..81)`.
