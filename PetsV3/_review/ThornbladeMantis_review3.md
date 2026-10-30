# Thornblade Mantis - art director review 3 (2026-10-14) - CLIPS ROUND 1: REVISE 2 (strike + groom)

**Model: APPROVED, 8.5/10 for a 2% SECRET.** M1-M4 and S1-S5 all landed:
- smooth gold, with the cone rings
- flush diamond jewels
- ruby domes with the pupils at the inner-front under the lid
- crystal thorns instead of dice

The mesh is locked. The only exception is the small eye-spot tweak in C3, which is hidden at rest.

**Clips:**

| clip | verdict |
|---|---|
| walk | APPROVED |
| roar | APPROVED (C3 is a cheap model-side polish) |
| idle | APPROVED except the groom (C2) |
| act_thornstrike | **REVISE: re-stage (C1)** |

Thank you for the semantic helpers, `pose_try` and the hindwing path. That was the right engineering, and my tables
were inconsistent.

What I looked at:
- the animation section of `pets/ThornbladeMantis.py`
- the `_clips_r1_*` sheets, `_model_sheet`, `_close_sheet` and `_arm_sheet`
- my own 520 px poses (rig + anim built without `write_clips`), in
  `C:\Users\ventu\AppData\Local\Temp\mantis_rev\c1\`:
  - roar f20/24/30/50/66 in tq, front, game and side
  - thornstrike f20/25/27/34/35/40/66 in tq, side, game and front
  - idle f0/40/80 and walk f0/8/16 in tq and game
  - Open `S_act.png`, `S_roar.png` and `S_idlewalk.png` first.

---------------------------------------------------------------------------------------------------------------------
## 1. Rulings on your deviations
1. **Semantic signs: APPROVED.** Keep the helpers and the docstring mapping. All values below are semantic (your
   helper names).
2. **Roar head-lock: APPROVED.** It is better than my table. The head stays on the threat (about 18° up in world).
3. **Wing fan: APPROVED.**
   - The splay-after-raise, the 13-waypoint HIND path, the fold order (hindwings first, tegmina un-splay before landing)
     and the articulation strip at r 0.07 are all accepted.
   - **Result:** in tq f30 it is the money shot: raised gold claws, the jade tegmina in a V, a dark fan with a ruby
     target.
   - In the game view the fans read as dark fins. The eye-spots are small, because the BLACK outer ring disappears into
     the dark wing. C3 fixes that on the model side.
4. **Strike: the idea is right (a FORWARD strike), the result is not.** See C1.
   - At f25 the femurs go horizontal and the tibiae open only 85°, so they hang straight DOWN like two extra legs. The
     front view reads as six legs, and the side view reads as pawing the ground.
   - The X-cross (f34-35) drives a tibia to the ground: your own ground_min_z is -0.014 for Blade_R at f35.
   - **From the game camera the whole strike is invisible.** It happens low, under and in front of the head; at f25-40
     only gold specks show beside the prothorax. The tell (up 8 / out 12) is also too small to read from behind.
5. **No abdomen lag: APPROVED.** That was the correct call for interleaved rigid parts.
6. **Model tweaks** (hindwing lowered to -0.042, thin 0.004 rings, tip t 0.86, last band t 0.95): **APPROVED.**
7. **Groom: REVISE (C2).** The tibia opens 30° and points down and forward (tq idle f80). It reads as "pointing at the
   ground", not "cleaning the blade at the mouth".
8. **Walk trot** (duty 0.6, stride half 0.07, lift 0.045, 2° blade counter-swing, Chest counter-yaw -0.8): **APPROVED.**
   Slide 0, loop closed.

---------------------------------------------------------------------------------------------------------------------
## 2. Fixes

### C1 - act_thornstrike: re-stage it HIGH and FORWARD, so it reads from the game camera (must)
A mantis strike is: raise and cock → the whole raptorial leg shoots forward nearly STRAIGHT → the tibia snaps shut and
pulls back. Keep your timing (it follows the "Attack" reference well): lock-on f0-14, cock f14-20, a 4 f tell
f20-24, 2 f snap, recoil, X-cross, hold, groom, settle. Change the poses to these world-space targets. Use `pose_try`
to find the angles; L and R are mirrored unless stated.

| f | beat | target (world, model units) |
|---|---|---|
| 14-20 | **COCK (big)** | `out` to **22** first (from f14), then `up` to **30** from f16 (arm rule), `fore` +15 (femur tucked back), `blade` -10 (shut tight). The knee spines must stand **above the eye tops (z ≥ 1.30)**, beside the head. That is the "raised scythes" tell, readable from behind and in tq. Body: Chest -10, Spine y +0.03 (weight back), antennae back -12 |
| 20-24 | **tell (hold)** | Freeze, with a 1° tremble on the Blade (±1 every 2 f). That is the "cocked hand" of the reference |
| 25 | **STRIKE 1: REACH** | The whole foreleg is nearly straight and forward. Tibia opened **≥ 140°** (not 85). The femur points forward and slightly up (about 15-25° above horizontal). **Tibia tips at y ≈ HC.y - 0.50 (-1.02 ± 0.05), z 0.55-0.85**, with `out` +6 so they show either side of the head from the game camera. Spine y -0.07, Chest -10 |
| 27 | **SNAP** | Tibiae shut to 10 (the hooks close upward onto the saw). Femurs pull back halfway (prey caught). Hard stop |
| 27-33 | recoil | Back to a half-cock (`up` 12 / `out` 18, so the arm rule holds) |
| 34-35 | **STRIKE 2: X-cross at CHEST height** | Tibiae open ≥ 120°. The arms sweep IN and slightly down to cross **in front of the prothorax at z 0.60-0.85**. L leads by 1 f and passes 0.05 higher. **No part except the feet below z 0.10** at any frame |
| 36-50 | **executioner hold** | Blades crossed in an X in front of the chest (z 0.6-0.85), tibiae shut (clutch). ONE head tilt of 12°, Jaw 15. The X should read in tq and front, and the two gold elbows from the game camera |
| 50-60 | back to prayer | Ease (not linear) |
| 60-72 | groom | As C2. **Ease in over f60→66**: today the left arm jumps from rest (f60) to the full groom pose (f64) in 4 frames |
| 72-100 | settle | As now |

**Checks:**
- collision_free with the same pairs
- ground_min_z of the act = the planted feet only (Blades ≥ 0.10)
- reach ≤ 0.6 in front of HC

**Picks to return:** f16 / 20 / 24 / 25 / 27 / 34 / 35 / 40 / 66, in tq, side and **game**.

At f20 and f25 the gold scythes must be clearly visible in the game view.

### C2 - Groom: bring the BLADE to the MOUTH (idle f62-102, act f60-78) (must)
The tibia should stay shut along the femur. The arm swings IN so its upper third passes in front of the mandibles, and
the head turns down to meet it:
- **Arm:** `out` **-18** (IN, no raise), `fore` -6, `blade` **-5** (shut, not +30 open).
- **Head:** turns toward the grooming arm **yaw 12**, `up` **-8**. Jaw chomps ×2 as now.
- **Target:** the upper third of the tibia (z 0.90-1.00) sits at **|x| ≤ 0.06, 0.02-0.04 in front of the mandible
  tips**. That reads as the blade being drawn through the jaws.
- **If (Fore_L, Head) or (Blade_L, Jaw) collides:** first drop the head to -6, then reduce `out` to -15. Allow the
  0.02 tolerance on Blade/Jaw only.

### C3 - Hindwing eye-spots: contrast, not size (should; the model side, hidden at rest)
The wing is too narrow for a bigger disc (r 0.10 already reaches both edges). Make the spot read as an EYE on the dark
wing instead. Keep the 0.004 rings and the top + underside copies.

**Ring order, outside → in:**

| ring | colour | r |
|---|---|---|
| outer | **RUBY_HOT** (pale rim; replaces BLACK) | 0.10 |
| | RUBY_D | 0.078 |
| | RUBY | 0.058 |
| centre | **BLACK slit pupil** | 0.03, `sx 0.45, sy 1.4` |

**Also:**
- `sy` 1.15 → **1.35** on the rings (longer along the wing; there is room lengthwise).
- Centre at `leaf(s, 0.55, 0.40)` (S4).

The visible spot then grows from r ≈ 0.073 to the full 0.10, about +85% area. It reads as a demon eye from tq and from
the game camera, where the dark fans are today.

---------------------------------------------------------------------------------------------------------------------
## 3. Approved as is (notes for the record)
- **idle** (apart from the groom):
  - the leaf-sway with a head counter-roll
  - one tilt at f18-56 (no shake)
  - antenna flicks
  - It reads as a still hunter.
- **walk:** the jerky trot is correct for a mantis, and the head lag is subtle.
- **roar:**
  - crouch 10 f → explode by f24 (Monsters University timing)
  - a 34 f hold with shiver, two clacks and two blade pumps
  - fold in the right order, settle
  - From the game camera, the two raised gold tibiae beside the crown are the strongest read on any frame of the
    clips.
  - Events land on f24/34/44.

**Owner to-do once C1-C3 pass:** the Studio import of the FBX as creator ZAB Studio, and VFX Studio effects on Crown,
EyeSpot_L/R (roar `display`) and BladeTip_L/R (`strike1`/`strike2` slash trails). Then Save + Publish.

**Return:**
- the C1 picks (tq, side and game)
- idle groom f80 and act groom f66 (tq + front)
- roar f30 in tq and game after C3
- headless_clips summary: collision_free, ground_min_z per clip, audit, events
