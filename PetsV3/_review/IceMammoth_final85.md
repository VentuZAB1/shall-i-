# Ice Mammoth - FINAL 8.5 GATE (2026-10-28) - FIX

**Model: 7.5 / 10.  Clips: 8.0 / 10.  Verdict: FIX.** Neither reaches 8.5, so it does not ship yet.
Owner bar (2026-10-28): 8.5 is the minimum and higher is better. The MUST list below gets both to 8.5. The TO 9+ list is what takes it past that.

The mammoth reads as a mammoth in every view: dome hump, white tusks with mint caps, a ridged trunk, studded skin, a pale underside, 13,716 tris, no glow. Every round-1 to round-4 MUST is met on the numbers. What holds it at 7.5 on the model is the look from the player's eye: the body reads pale aqua, the eyes read as pale windows at close range, and the legs are four plain columns. The clips pass every gate, but the idle is too quiet at 5 studs and each snow scoop touches for a single frame.

## What I looked at
- **Read:** `_review/IceMammoth_plan.md`; `IceMammoth_review1-4.md`; `IceMammoth/MODEL_NOTES.md`, `CLIP_NOTES.md`, `ANIM_REFS.md`, `_scratch/verify.json`; Obsidian `Creature Style.md`, `Model Review Checklist.md`, `Creature Animation.md`; `PetsV3/FIERCE_GUIDE.md`; `_review/GLACIER_CONCEPTS.md` (owner decisions); `pets/IceMammoth.py` (palette L17-24, eyes L166-175, legs L288-299, idle L431-452, act beat table about L519-540).
- **Model images:** `renders/_model_sheet.png`, `_close_sheet.png`, `close_front.png`, `model_game.png`, `flat_game.png`, `under.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `final/throat/*`, `final/mouth/*`, `_final_mouth.png`, `_final_throat.png`.
- **Clip images:** `_beats_act_side.png`, `_beats_rw_side.png`, `_beats_scoops_side.png` (22:02, after the final file at 21:57).
- **Comparison pets:** `Raiju/renders/_model_sheet.png`, `GlacierYeti/renders/_model_sheet.png`, `FrostfangLynx/renders/_icons_strip_64.png`, `_ALL_FIERCE_progress.png`.
- **Measured:** body colour from the 128 px icon strip (background tile excluded, median HSV). Mammoth V 0.82, S 0.45, hue 196. Yeti V 0.94. Bramble Badger V 0.79. ThunderBull V 0.63. Mossback V 0.51. MoltenBoar V 0.49. Verify numbers are in the clip section.
- **Not done:** no Blender, no Studio, no game capture. The in-game colour is still the 0.6x estimate (review 2 C1, open for three rounds).

## MODEL: 7.5 / 10

**Strong:** the species reads at 64 px. The tusks with mint caps and cracks are the best accent in this set at icon size. The silhouette is dome, tusks and trunk. The stud skin is consistent, the pale belly band shows, and the mint is clear at 128 px. The tusk sockets, brows and trunk tip are clean. No floating or poking parts show in the five views or under.png.

**Why it is not higher:**
1. **The body reads pale aqua.** The lit icon body (V 0.82) is the second-lightest body in the strip after the Yeti, and the navy and violet pets sit well below it. Hue 190 to 196 at high value reads as baby blue next to them, the look the owner has rejected. The brightest-channel rule is met (184), but the lit look is what the shop icon and the player see.
2. **The eyes read as pale windows, not slits.** In `close_front.png` and the `_close_sheet` panels, each eye is a white-cyan rectangle with a black dash. The mint slit (L172, MINT 150,236,210) renders almost white, and the dark socket (L170) is a thin frame. That is the googly or goggle read FIERCE warns about. The brow V helps, but it does not carry the face.
3. **The legs are four plain stud columns** (L295, L299) with a flat black pad. The lower half is one aqua field. The Raiju and the Yeti both break the legs with a second colour, and this does not.
4. **Colour in game is unverified.** Review 2 asked for a Studio capture at the 5-stud camera (C1). It has not been done, and the pale read above is the only evidence.

## CLIPS: 8.0 / 10

**Pass on the numbers** (`_scratch/verify.json`, step 1): `collision_free` true for all four clips. `ground_min_z` idle 0.018, walk 0.015, roar 0.018, act -0.019 (thin margin). Loops closed, linear 0, walk slide 0.0. End-at-rest 0.0 for roar and act. Neck max 3.0, chest max 1.68, head pitch-up 16 and 17, max adjacent swing 46.6 (f62). Hinge crossings were reported raw (6/15/6/7), with 0 after the hinge.

**Read:** the walk is heavy and planted, with a lateral sequence and a still head. The roar's trunk rises to the sky with a readable head lift. The act's scoop, lift, snap over the brow, two smaller beats and exact rest all read in the side and tq beat sheets.

**Why it is not higher:**
1. **The idle is too quiet at 5 studs.** The only real motion is the trunk chain (tip +/-12 deg over 120 f, about 0.3 studs of tip travel). The chest breath is 0.5 deg (L444). Ears move 3 deg plus one bell at f82.
2. **Each snow scoop is a one-frame tap.** The FX_SnowSpray anchor is 0.016 (f20), 0.018 (f66) and 0.018 (f80). It reaches 0.008 only at f65 (verify). A tap does not read as a scoop.
3. **The roar's open mouth is hidden at the peak.** In `final/mouth/pclose_side_roar_34` (jaw 14) the trunk root covers the mouth from the player's side. The trumpet reads from the trunk alone.

**Owner decision, not scored:** the animationreference.org rule. The walk is a Muybridge plate (733), not a site clip. The elephant site clip was never played. W0 is a wolf clip from the site tag. The roar and act use the 1014 refs (#3, #5, #9). Review 4 accepted this. The owner should confirm it stands.

---

## MUST (to 8.5 on both)

**Model**
- **M1. Body colour: deeper, bluer teal.** `pets/IceMammoth.py` L17: `CHAR_TEAL (96,168,184)` becomes **(80,150,176)**. Brightest 176 (passes 170), hue 196 (was 190), S 0.55, V 0.69 (was 0.72). Keep `WOOL_D (80,110,124)` on L18. Target: the icon body median V at or below 0.70 in `_icons_strip_128`, next to ThunderBull and the Yeti (was 0.82). Then run the C1 Studio capture at the 5-stud camera (open since round 2) and report it.
- **M2. Eyes: a black socket and a dark-mint slit.** In the eye loop (L166-175):
  - L170 socket: `DARK` becomes `BLACK (14,14,22)`, size (0.078, 0.012, 0.024) becomes (0.084, 0.012, 0.028).
  - L172 slit: `MINT` becomes a new constant `EYE_MINT = (56,196,168)`. Keep the size (0.070, 0.008, 0.012).
  - L174 pupil stays BLACK.
  - Check: `close_front.png` at 5 studs shows a narrow teal slit in a black frame, with no white block.
- **M3. Legs: a shaggy wool cuff on each shin.** In the legs section (L288-299), add a `WOOL_D` sleeve on the top 25 % of each of the four shins: a `B.seg` from the knee toward the hip, length 0.06, radius 0.02 wider than the shin (shin radius 0.155 and 0.14), studs on. Real mammoths have shaggy forelegs, and this gives the body a second band. Check: a dark band on all four legs in the side and close views. Step 1 `collision_free` must stay true.

**Clips**
- **C1. Idle: visible life at 5 studs.** In `idle()` (L431-452):
  - Raise the trunk tip swing from +/-12 to about +/-16 deg: the roll amplitudes on L441 `(2.0, 3.0, 3.5, 3.5)` become `(2.7, 4.0, 4.7, 4.7)`.
  - Add a second ear flap at f40: change L448 to `ears(k, f, 3*pk.wave(f, n, 0.3, 2) + 9*bell(f, 82, 8) + 8*bell(f, 40, 6))`.
  - Keep the feet planted (`idle_foot_drift` 0). Check: `collision_free` true, ground_min_z at or above -0.02, and a pose at f40 and f60 with the ear out and the trunk swung.
- **C2. Act: hold each scoop on the snow.** In the act beat table (about L519-540, the SCOOP rows at f20, f66 and f80): hold the deepest tip pose for 4 frames at each scoop, f18-22, f64-68 and f78-82. Do not go lower than the current pose: `ground_min_z` act is already -0.019, and the floor is -0.02. Check: the FX_SnowSpray z stays at or below 0.012 across each hold, and the max swing stays under 60. Pose sheet at f18, f20 and f22.

---

## TO 9+ (highest impact after the MUST items)
1. **Scowl brow.** L167 (the WOOL_D brow shelf, size (0.108, 0.042, 0.036)): change `rot=(-14, -s*22, 0)` to `rot=(-22, -s*28, 0)` and move z from 1.418 to 1.410. The brow then overhangs the slit and shades the eye from above.
2. **Visible breath.** L444: chest rise `0.5*br` becomes `1.2*br`, so the three breaths read at 5 studs. Keep the exhale at f80.
3. **Open jaw at the roar peak.** Open the jaw to about 18 deg at f34 (currently 14) and lift the trunk root by 0.02 so the mouth shows from the player's side. Check with `final/mouth` side views at f34 and f50.
4. **Body colour fallback.** If the C1 capture still reads aqua after M1, go to (72,140,164) and recheck the icon strip. This is the only path to 9+ on colour, and it is a judgement call.

## Pass / fail checklist

| check | result | note |
|---|---|---|
| **MODEL** | | |
| Tris <= 15k | PASS | 13,716 (verify tris_body) |
| HEIGHT 9.0 | PASS | builder number, 1.76 units; not re-measured |
| Species reads at 64 px | PASS | |
| Studded body, head, legs, trunk; details smooth | PASS | |
| No glow, no Neon | PASS | |
| Body brightest channel >= 170 | PASS | 184 (L17) |
| Body reads dark rich, not pale aqua | **FAIL** | icon V 0.82; M1 |
| Eyes: narrow fierce slit in a black socket | **FAIL** | pale window at close range; M2 |
| Brow V fierce | PASS | |
| Dome silhouette, no spikes | PASS | |
| Pale underside visible | PASS | side and under views |
| Mint accent at 64 px | PASS | tusk caps |
| Tusks read at 64 px | PASS | |
| Three-band read on the legs | **FAIL** | plain columns; M3 |
| Floating, poking, intersecting parts | PASS | 5 views and under.png |
| Parts visible from below | PASS | under.png |
| Studio game-camera capture (C1, review 2) | **OPEN** | open for three rounds; M1 |
| **CLIPS** | | |
| collision_free, all 4 clips | PASS | step 1 |
| ground_min_z >= -0.02 | PASS | act -0.019 (thin) |
| Loops closed (idle, walk), linear 0 | PASS | |
| Walk slide ~0, idle feet still | PASS | 0.0 |
| Roar and act end at rest | PASS | 0.0 both |
| Neck <= 8, chest vs spine <= 5 | PASS | 3.0 and 1.68 |
| Head + neck pitch-up <= 30 | PASS | 16 roar, 17 act |
| Max adjacent swing <= 60 | PASS | 46.6 |
| No head shakes, no airborne spins | PASS | |
| Acts in place | PASS | |
| Walk and roar beats readable | PASS | |
| Idle readable at 5 studs | **FAIL** | quiet; C1 |
| Scoop reads as contact | **FAIL** | single-frame touch; C2 |
| Roar open mouth readable | **FAIL** | trunk covers it; TO 9+ 3 |
| ANIM_REFS rule | OWNER DECISION | see above |
