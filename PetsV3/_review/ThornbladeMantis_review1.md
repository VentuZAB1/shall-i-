# Thornblade Mantis - art director review 1 (2026-10-14) - REJECT (revise to v2, keep the concept)

**Score: 5/10 for a 2% SECRET.** As a common or uncommon this would pass. It is the first insect in the roster, and it
is the most saturated, most colourful pet in a brown and olive egg. The concept ("jade executioner", Empusa-style
cone-crown, ruby eye-spot reveal) is right, so **do not redesign it.** The problem is the execution of the three things
a secret is judged on, which all read cheap:
- **Face.** A white robot mask, red "goggles" from the front and red "headphones" from the side and back.
- **Weapons.** Flat jade slabs (oven-mitts). The gold and ruby only show as a thin strip on their front edge.
- **Game camera.** Players see a teal stick insect with a gold-trimmed leaf. The crown is a thin yellow tick, the
  scythes are hidden behind the prothorax, and the eyes are dark maroon boxes.

It needs a v2 with a new model sheet, close sheet and icon test. That is why this is not APPROVE WITH FIXES.

What I looked at:
- `pets/ThornbladeMantis.py`, plus `_model_sheet` and `_close_sheet` and all 5 single renders.
- My own transparent re-renders: tq, game, side, back, front, a head close-up from the front and from the game camera,
  an arm side view, and a top view with the tegmina hidden (temp, outside the project:
  `C:\Users\ventu\AppData\Local\Temp\mantis_rev\out\`).
- A 64/128 px slate icon strip made with the icon3 recipe, next to Mossback, Stag, Treant, Thunder Rex and Ivonrath.
- Thunder Rex reviews 1-3, `LESSONS_ALL_PETS.md`, `_icons_sheet`, `_ALL_FIERCE_progress`, and the palettes of the
  Grass siblings and of VenomBasilisk.

Pixel classifier (background removed, about ±4%; BELLY includes the white specular edges, so the real BELLY is lower):

| view | ARMOR | HIDE (+HIDE_L) | BELLY* | GOLD | RUBY | sat. median |
|---|---|---|---|---|---|---|
| game cam | 27% | **51%** | 12% | 6.3% (crown 2.8, costal stripes 3.4) | **2.2%** | 0.50 |
| side | 28% | **54%** | 9% | 5.4% | 2.3% | 0.56 |
| back 3/4 | 27% | 44% | 19% | 5.9% | 2.1% | 0.53 |
| tq | 24% | 48% | 10% | 9.1% | 4.8% | 0.53 |
| front | 14% | 51% | 19% | 8.0% | 5.3% | 0.58 |

- **Saturation is fine.** It is better than Rex v1's.
- **There is enough gold, but it has the wrong shape.** The 64 px icon has 43 gold pixels; Rex has 17 and Ivonrath 36.
  It is all thin lines (costal stripes, scythe edges, a needle cone), so no single solid gold mass reads as "crown".
- **HIDE dominates every view.** The dark armour sits only on the legs. The top surfaces the camera sees (prothorax,
  femurs, head) are all jade.

---------------------------------------------------------------------------------------------------------------------
## 1. Keep list
- **Concept and palette.** Dark teal / jade / pale mint, with gold and ruby as the accents. It stands out in its egg:
  Mossback, Stag and Treant are brown/olive and VenomBasilisk is green+purple with no gold. **Do not shift HIDE's hue**:
  greener collides with VenomBasilisk (hue 123°), bluer with SeaTurtleWarrior/Kappa teal (167°). The value fixes below
  separate it from those enough.
- **The tegmina.** Dark rim, light-jade panel, dark veins and the gold costal stripe. This is the best thing on the
  model from the game camera, and it reads as a gold-trimmed leaf cloak.
- **The hindwings.** Dark wings with RUBY eye-spots. With the tegmina hidden, the top view reads as a big demon face.
  That is a great reveal, as long as it is visible (see W1).
- **`ruby_gem()`.** Its 3-step DEEP→RUBY→HOT construction. Use it everywhere ruby appears.
- **The anatomy.** The prayer pose (coxa → femur up → folded tibia), raised prothorax, rising abdomen tip and cerci.
- **The Empusa cone-crown idea.** It is anatomically real and unique in the roster. Make it bolder; keep the idea.
- **The rig.** Its layout and bone names, 2-bone IK on 4 legs, and the Strike anchor.
- **Materials.** Studs on HIDE/ARMOR; smooth gold and ruby.

---------------------------------------------------------------------------------------------------------------------
## 2. Ranked fix list (line numbers = current `pets/ThornbladeMantis.py`)

### FIX 0 - BUG: the left antenna is skinned to `Antenna_R` (must fix, 1 line)
- **Cause:** the head loop (L136) is `for s in (1, -1):`, but L157-158 use `"Antenna_" + side`. `side` is left over
  from the tegmina loop, so it is "R" for both antennae.
- **Proof:** the built parts list contains `P_Antenna_R` and no `P_Antenna_L`.
- **Effect:** any antenna twitch makes the left antenna orbit the right root.
- **Fix:** `for s, side in ((1, "L"), (-1, "R")):` at L136.

### FIX 1 - Head rebuild: bigger triangular head, dark "executioner hood", no mask (L132-158)
The head is 16% of the height, and its brightest spot is the white face plate, which is the main "robot" read at
64 px. Rebuild the head at its final size (LESSONS 4). Expect about +30% linear, and a head span of ±0.237 instead of
±0.183. Use `HC = (0, -0.52, 1.14)` and leave HEADP at `(0, -0.45, 1.02)`.

**Head block:** `B.add(HC, (0.15, 0.09, 0.11), HIDE, "Head", bot=(0.38, 0.85), top=(1.0, 0.95), rnd=0.25)`. It spans
z 1.03-1.25.

**Lower face:** `HC + (0, -0.02, -0.145)`, size `(0.065, 0.06, 0.045)`, `bot=(0.6, 0.8)`.

**Delete the BELLY face plate (L134-135).** In its place:
- **Hood** (the dark top of the face; the concept's executioner):
  `B.add(HC + (0, -0.088, 0.055), (0.085, 0.012, 0.05), ARMOR, "Head", bot=(0.35, 1), role="detail", bevel=0.006)`.
  This is an inverted trapezoid between the eyes, from the head top down to about HC.z.
- **V-brow:** two ARMOR bars on the hood edges at `HC + (s*0.065, -0.10, 0.07)`, half `(0.06, 0.016, 0.02)`,
  inner end **30° down**, bevel 0.008.
  - The outer end must overlap the inner-top of each eye bulb by about 0.015. That "lid" is what makes it angry, not
    cute.
  - Copy the logic of Ivonrath's `fierce_eye` brow (`pets/Ivonrath.py` L93-110) and Thunder Rex's V brow.
- **Mouth plate** (the only pale on the face):
  `B.add(HC + (0, -0.083, -0.15), (0.035, 0.008, 0.022), BELLY, studs=[], role="detail", bevel=0.004)`.

**Antennae** start ABOVE the V and must never cross the brows (today they form an X through them):
- `a0 = HC + (s*0.03, -0.095, 0.105)`
- `a1 = a0 + (s*0.05, -0.07, 0.15)`
- `a2 = a1 + (s*0.17, 0.24, 0.02)`
- widths 0.013 / 0.010
- The tips then sit at z ≈ 1.42, below the crown tip (FIX 3).

**Mandibles:** length 0.075 → **0.10**, w 0.018 → **0.024**, from `HC + (s*0.035, -0.05, -0.185)`. IVORY tips 0.045.
Palps 0.085.

**Neck block:** hw 0.06 → 0.07.

### FIX 2 - Eyes: ruby compound-eye DOMES on the top corners, not boxes on the sides (L137-147)
Why they read as goggles and headphones:
- They are rounded cubes stuck to the head's sides, with flat fronts.
- From the front, a flat pink square and a black rectangle sit on them like stickers.
- The RUBY body is only on the front, so from the side and back (the game camera) you see dark RUBY_D boxes.
- The brow bar over them reads as a goggle strap.

Build each eye as a stepped dome that rises above the head line. Use `e = HC + (s*0.165, -0.02, 0.075)`. Roll the top
12° outward and yaw the front 18° outward, so the two eyes form a V from the front.
1. **RUBY_D base shell:**
   `(0.072, 0.07, 0.088)`, `rnd=0.5, bot=(0.70, 0.75), top=(0.60, 0.70), studs=[], nostud=True`.
2. **RUBY body:** `e + (s*0.006, -0.012, 0.014)`, `(0.064, 0.062, 0.078)`, `bot=(0.65, 0.7), top=(0.55, 0.65)`.
   - Offset it UP and OUT, not only forward, so it covers the top, outer side and front.
   - RUBY_D then shows only as a rim at the back-bottom. This fixes the maroon "headphones" seen from behind.
3. **RUBY_HOT cap:** at `e + (s*0.028, -0.04, 0.06)`, `(0.024, 0.022, 0.016)`, `rnd=0.5`. It catches the key light
   from both the front and the game camera.
4. **Pseudo-pupil:** a BLACK vertical slit `(0.013, 0.006, 0.028)` at the inner-front, `e + (-s*0.022, -0.072, -0.004)`,
   with the eye's yaw.
   - That is about 36% of the eye's front height (LESSONS 7).
   - Seat it with a surf_hit like VenomBasilisk L42, because the dome is tapered and rounded.
   - Delete the flat pink highlight and the old brow (L142-147).

**Result:** the eye tops sit at HC.z+0.163, about 0.05 above the head top. That gives the classic mantis "two bulbs on
a triangle" silhouette, and from behind it reads as two ruby bulbs flanking the crown. The crystal stepping follows the
Thunder Rex shards (DEEP→MID→HOT).

### FIX 3 - Crown: a solid gold band + a dominant cone, which must be the HIGHEST point (L160-166)
**Problem 1: the crown doesn't read as a crown.** The model top is the antenna tips (bounds z 1.579), and the crown tip
is only at 1.455. HEIGHT = 10 studs is therefore measured to the antennae, which shrinks the body about 8%. The crown
is a 0.045-wide needle on a band (0.07 × 0.04) that hides between the eyes, so it reads as a "yellow tick/flame", not a
crown.

**Band:** `B.add(HC + (0, 0, 0.12), (0.09, 0.06, 0.032), GOLD, "Head", top=(0.85, 0.85), role="limb", bevel=0.01)`. It
fills the space between the eye bulbs.

**Centre cone:** `B.spike(HC + (0, 0, 0.14), (0, 0.25, 1), 0.34, 0.065, GOLD, "Head")`. The tip lands at z ≈ 1.61 and
becomes the model top, and HEIGHT 10 then applies to the crown tip.

**Side prongs:** base `HC + (s*0.055, 0, 0.14)`, direction `(s*0.5, 0.2, 1)`, length **0.18**, w **0.042**. Don't add
outer prongs; they would clip the eye domes.

**Cone keel:** keep it in GOLD_D, scaled up: from `HC + (0, 0.02, 0.19)`, length 0.16, w 0.03. It gives the cone a
shaded back for the game camera.

**Front gem:** `ruby_gem(B, HC + (0, -0.062, 0.12), (0, -1, 0.15), 0.06, "Head")` (was 0.045).

**Close the circlet for the game camera** (Thunder Rex review-2 FIX 1 did the same: `ThunderRex.py` L276-281):
- a GOLD back plate `(0.07, 0.012, 0.03)` at `HC + (0, 0.062, 0.115)`
- a second `ruby_gem` facing +y, size 0.045

**Hierarchy target:** the crown is the single largest gold mass in the tq and game views (≥ 3% of the pet's pixels on
its own; the costal stripes are 3.4% today). At 64 px it should read as a gold crown shape (band + cone), not a line.

### FIX 4 - Raptorial forelegs: dark scythes with a gold crescent, a ruby saw and a gold knee spine (L168-186)
**Why they read as oven-mitts:**
- The femur is an untapered, studded jade box (0.11 × 0.16 × 0.39) with a flat end.
- The tibia is folded flat against it.
- The knee is a dark cube that reads as a button.
- The gold edge is 0.06 wide and faces forward only, and the thorns point at the camera, so they are foreshortened to
  dots.

New points (raise the knee to head height so the blades frame the face, and spread them so they show beside the
shield from behind):

`ARM = ((0.08, -0.30, 0.84), (0.17, -0.46, 0.62), (0.21, -0.64, 1.00), (0.20, -0.73, 0.66))`

**Coxa:** HIDE, hw/hd 0.05 / 0.055. Joint: ARMOR, `rnd=0.5`, 0.055.

**Femur → ARMOR.** Gold on dark is the contrast the Rex review asked for.
- `B.seg(C1, F1, 0.045, 0.075, ARMOR, fore, ext=0.03, ext1=0.03, top=(0.75, 0.6))`, tapering to the knee.

**Gold crescent** (a flat, broad signature shape, LESSONS 6; CelestialDragon's crescent tail blade shows the way):
- Two GOLD segs, P0 → Pm → P1:
  - `P0 = C1 + fd*0.03 + edge*0.075`
  - `Pm = C1.lerp(F1, 0.5) + edge*0.11`
  - `P1 = F1 - fd*0.03 + edge*0.07`
- Each seg: hw 0.035 (x), hd 0.04 (edge direction), `studs=[], nostud=True, role="limb"`, ends tapered to 0.7.
- From the side, it is a gold band about 0.08 deep along the whole femur.

**Ruby saw (two rows):**
- **Outer row:** 5 `ruby_gem`s at t 0.2 / 0.36 / 0.52 / 0.68 / 0.84 on the crescent's edge, alternating sizes
  **0.075 / 0.05**, direction `edge*0.8 + fd*0.3 + (s*0.45, 0, 0)`. Splayed outward like this, they read from the front
  AND the side.
- **Inner row:** 2 gems at t 0.28 / 0.6, size 0.045, direction `edge*0.8 + fd*0.3 - (s*0.35, 0, 0)`.

**Knee:** an ARMOR knuckle (`rnd=0.5`, 0.045) plus a **GOLD genicular spine**:
`B.spike(F1 + (0, 0, 0.03), (s*0.7, 0.5, 0.5), 0.11, 0.032, GOLD, fore)`. Seen from behind, two gold horns rise beside
the head. That is hero #2 from the game camera.

**Tibia:** GOLD seg F1 → T1, hw 0.032, hd 0.042, `top=(0.7, 0.6)`.
- The new T1 (y -0.73) folds it just in front of the crescent, so it reads as a separate hook.
- Hook: a GOLD spike from T1, direction `td*0.3 - tedge*0.95` (curling back toward the femur), length 0.08, w 0.028.
- Claw: a BLACK spike off the hook tip, 0.05 long, w 0.015.

**Clearances I checked by hand (the builder must confirm with the posed check):**
- Eye bottom (z 1.127) vs knee top (1.045): 0.08 at rest. At Head pitch-down 20° it is about 0.04.
- The spine tip (x 0.28) stays outside the eye's x span (≤ 0.237).
- The tibia (x 0.20) is clear of the lower face (±0.065) and of the mandibles.

### FIX 5 - Pronotum SHIELD: the dark top the game camera sees (replaces L120 keel and L125-129 flares)
- The prothorax top faces the game camera almost head-on (the dot product of the normals is ≈ 0.93), so it is the
  most-seen surface after the wings.
- Today it is a jade stick with a dark "zipper" stripe.
- Make it a studded ARMOR shield, wide at the front third like Rhombodera / shield mantids. That is the executioner's
  cloak, and it delivers most of the missing ARMOR %.

Definitions: `n_up = (0, 0.795, 0.606)` and `A(t) = PRO[0].lerp(PRO[1], t) + n_up*0.09`.

**Shield segs** (studded; don't use `B.poly`, because polys get no studs):
- `B.seg(A(0.15), A(0.45), 0.155, 0.018, ARMOR, "Chest", bot=(0.42, 1))`
- `B.seg(A(0.45), A(0.98), 0.155, 0.018, ARMOR, "Chest", top=(0.35, 1))`
- Start at **t 0.15, not 0**. At t 0 the rear end hits the tegmina root once the prothorax rears up 12-15° (I measured
  about 0.02 of clearance).

**Edge thorns** at t 0.25 / 0.45 / 0.65:
- Base on the shield edge.
- Direction `(s, 0, 0) + d*0.35 + n_up*0.25`.
- ARMOR spikes, lengths 0.07 / 0.09 / 0.07, w 0.024, each with a **RUBY tip spike** from 60% of its length (Ivonrath
  `crest()` two-step, `pets/Ivonrath.py` L112-124).
- From behind they form a thorny diamond with ruby points. That is the "Thornblade" read, and it adds RUBY to the game
  view.

**Throat "tie" (L123-124):** start at t 0.40 instead of 0.15, hw 0.06 → **0.045**, and add 2 BELLY_D bands.

### FIX 6 - Abdomen side: three bands, no picket fence (L75-84)
- Six full-height dark rings at even spacing read as a picket fence in model_side (the same note as Rex v1's teeth).
- **Tergite bands:** use one band per segment at t 0.85, instead of two.
  - Cover only the upper ~60%: centre z = axis + d*0.40, half depth d*0.62, width w*1.04.
- **Sternites:** the BELLY strip goes from w*0.75 / 0.014 thick to **w*0.98 / 0.03**, so its sides show in profile.
  Add BELLY_D gap bars at each band. CelestialDragon's scute keel (L179-186) and Rex review 2 FIX 4 show the way.
- **Targets:** in the side view, three bands (dark wing rim and tergites / jade / mint stripe), and BELLY ≥ 7% without
  the highlights.

### FIX 7 - Wings
- **W1 (must): two-sided eye-spots on the hindwings (L93-97).**
  - When a wing pitches up toward vertical, its TOP face turns to face forward, so the eye-spots show to the front and
    the Index portrait.
  - The game camera (behind) sees the ARMOR underside, so the owner would never see the reveal.
  - Mirror the 4 discs to the underside (z offsets -0.016 / -0.020 / -0.024 / -0.028 below `eye`, then check from
    below).
  - Enlarge r 0.085 → **0.10**.
- **W2 (cheap): a ruby stigma teaser on each tegmen.**
  - 3 stacked discs RUBY_D / RUBY / RUBY_HOT at r 0.035 / 0.025 / 0.012.
  - Place at `leaf(s, 0.42, 0.72)`, seated like the veins (+0.014, then +0.004 per disc).
  - This puts ruby in the resting game view (2.2% today; target ≥ 4% together with the eyes and shield thorns).
- **W3 (cheap): widen the dark tegmen rim.** The inner panel goes from w 0.86 / 0.12 to **0.80 / 0.16**.

### FIX 8 - Walking legs: less spider, more mass for the icon crop (L32-33, L188-199)
- The legs set the bounds width (1.2), so the body fills only about 35% of the icon.
- **Pull the stance in about 15%:**
  - F: knee (0.35, -0.22, 0.64), ankle (0.45, -0.40, 0.11), toe (0.48, -0.51, 0.02)
  - B: knee (0.37, 0.30, 0.64), ankle (0.47, 0.56, 0.11), toe (0.50, 0.67, 0.02)
- **Thicken:** femur 0.042/0.048 → **0.048/0.054**, shin 0.032/0.034 → **0.038/0.040**, foot 0.02/0.018 →
  **0.024/0.022**.
- **Shin spikes (L196-197): GOLD_D → BLACK.** Gold is for the hero pieces; the dots on the legs dilute it.

### Cheap / optional
- **Mandible_L / Mandible_R** bones instead of one Jaw bone, so the mandibles scissor sideways in the clacks. It is
  much more insect-like and fierce. It costs 2 joints.
- Keep the costal stripes as they are. Once FIX 3 lands, the crown outweighs them.

---------------------------------------------------------------------------------------------------------------------
## 3. Animation notes (30 fps)

### Pose limits (the owner's rules plus a proposed prothorax limit)
- **Neck ≤ 8°.** Head+Neck pitch-up ≤ 30°. Head pitch-down ≤ 20°, and ≤ 15° while head yaw is over 15° (eyes vs knee
  spines). Head yaw ≤ ±25°. **Head roll (tilt) ≤ 15°.**
- **Proposed Chest (prothorax) vs Spine limits:**
  - pitch **-10° (lower/lunge) to +12° (rear)**, yaw ±8°, roll ±4°
  - Rex's 5° limit came from its crystal ridge crossing the joint. Nothing crosses this one, and the prothorax is the
    mantis's main expressive joint.
  - The limit is set by the shield's rear end vs the tegmina root (FIX 5). Over +12°, they touch.
- **No head shakes.**
  - A tilt is ONE roll to one side, a hold, then a return. Never alternate L/R tilts back to back.
  - "Peering" is a whole-body lateral sway (Spine x); the head stays world-stable.

### idle (~120 f)
- **Leaf-sway:** Spine roll ±3° and x ±0.015 on planted feet, 40 f period. The head counter-rotates so the gaze stays
  level; that head stabilisation is the predator tell.
- **One predatory tilt:** roll 12° in 5 f, hold 25 f, return in 8 f. Not a slow continuous wobble, which reads cute.
- **Blade groom:** once per loop. One blade rises to the mouth, and the mandibles chew twice. Keep ≥ 0.02 clearance.
- **Antenna flicks:** alternating, ±12°, 3-frame flicks.

### walk
- Gait: diagonal pairs (F_L+B_R / F_R+B_L), duty about 0.6.
- Blades held folded, with a 2° counter-swing.
- Chest counter-yaws against Spine; the head is world-stable with a small lag; the abdomen lags 2-3 f.
- Keep a low-amplitude leaf-sway layer for the real mantis "rocking" walk.
- Slide audit 0.

### roar = deimatic threat display (90 f)
It must not read like VenomBasilisk's frill-flare hiss. Make it body-wide, symmetric, blades plus wings, with the
**eye-spot "face" reveal as the money shot**.

| frames | beat | keys (+ pitch = nose-down; Spine loc in model units) |
|---|---|---|
| 0-10 | **crouch / gather** | Spine z -0.04, pitch +4; Chest -6; Head -6 (glare down); blades tucked (Fore +8); antennae swept back -25 |
| 10-20 | **rear** | Spine z +0.035, pitch -10 (IK feet planted); Chest +12; Neck +6; Head +12 (Head+Neck 18 ≤ 30) |
| 14-26 | **fan** (staggered) | Elytra f14→24: pitch +65, roll out +40 (a V to the sides). Wing f16→26: pitch +80, roll out +15 (upright, between the tegmina, 2 f lag). Tail1/2/3 curl up -8/-12/-16 |
| 16-26 | **arms spread** | Arm yaw out 30°, pitch up 20°; femurs raised outward; **Blade open 75°** (gold sickles and ruby saws face out); mandibles open 20°. **Event `display` f24** (eye-spot flash VFX + sound) |
| 26-60 | **hold** | Wing roll shiver ±3° every 3 f; mandible clacks at f34 / f44 (`clack` events); Blade pumps 75→60→75 at f38-42 and f50-54; Spine leaf-rock ±2°; antenna twitches |
| 60-76 | **fold** | Wing 80→0 over f60-70 (hindwings fold FIRST); Elytra 65→0 over f64-74 (they close over the hindwings); blades fold f60-72; Chest back to 0 by f76 |
| 76-90 | settle | Spine z -0.01 overshoot at f84, then rest |

**Check frame f30.** In tq, front and game it must show both eye-spots whole (front: the top faces; game: the
underside discs from W1), both open gold tibiae, and the crown above the wings.

### act_thornstrike - "THORN STRIKE" (100 f; there is no blade or slash act in the roster yet)
The feet are planted for the whole clip: run `plant_frames` on all frames and set no FK leg keys. Reach stays ≤ 0.6 in
front of HC (about 3.8 studs at x1).

| frames | beat | keys |
|---|---|---|
| 0-14 | **lock-on + peering** | Chest -8; Head -8 (locked); Spine x +0.025 (f4) → -0.025 (f9) → 0 (f14); antennae forward. Event `lockon` f6 |
| 14-24 | **cock + tell** | Arm pitch up +25, Fore +20, Blade folded -10 tighter; Spine z -0.03, y +0.02 (weight back); Chest -10. **Hold f20-24** |
| 24-27 | **STRIKE 1** (2-3 f, hard) | Arm +25 → -45 (forward-down), Fore extends -50, Blade snaps OPEN 85 at f25 and CLOSED 10 at f27; lunge Spine y -0.07, pitch +6. Event `strike1` f25 |
| 27-33 | recoil | Arms back to half-cocked (Arm -10), with a small overshoot |
| 33-36 | **STRIKE 2: X-cross** | Both arms sweep in-down, yaw in ±18. L leads by 1 f and passes 0.05 higher (Arm pitch offset 6°) so the blades never intersect; Blade open-snap; Spine y -0.09. Event `strike2` f34 |
| 36-50 | **executioner hold** | Blades crossed low in an X, tibiae closed ("clutch"); ONE head roll of 12°; mandibles open 15. Event `finish` f36 |
| 50-72 | retract + groom | Back to the prayer pose by f60. Head -8; Blade_L to the mouth (≥ 0.02 clearance); mandible chomps at f64 / f69 (`groom` f64) |
| 72-100 | settle | Head roll back; antenna twitch at f80; Spine z micro-dip; rest |

- Ease into the cock, use hard stops on f25 / f27 / f34, and ease out of the hold.
- The 4-frame tell before each snap is what makes a 2-frame strike readable.

### Rig and collision concerns
1. **FIX 0:** the antenna bone bug.
2. **Posed collision pairs to add:**
   - (Head, Chest): head pitch-down vs the shield
   - (Elytra_L/R, Chest) and (Wing_L/R, Chest): rear-up and fan
   - (Fore_L/R, Chest): shield
   - (Fore_L/R, Leg_FL/FR) and (Blade_L/R, Leg_FL/FR): roar spread
   - (Antenna_L/R, Blade_L/R) and (Antenna_L/R, Fore_L/R): head pitch-down
   - (Elytra_L, Wing_R) and (Elytra_R, Wing_L): fan
   - (Blade_L/R, Jaw) with a 0.02 tolerance: groom
3. **Test poses (must be collision_free):**
   - roar peak f30
   - strike1 f25 and strike2 f34
   - Head -15 with yaw ±25
   - head roll 15
   - Chest +12 and Chest -10
4. **Wing fan axes.** Elytra and Wing need pitch about local x and roll about the bone axis (tail +y). Confirm that the
   roll direction opens the wings OUTWARD on both sides (mirrored sign).
5. **VFX anchors to add** (Rex precedent):
   - `Crown` (cone tip)
   - `EyeSpot_L/R` on Wing_L/R at the eye-spot centres (display flash)
   - `BladeTip_L/R` on Blade_L/R at T1 (slash trails)
   - Move `Strike` to the X-cross point of strike 2, about (0, -0.95, 0.75), on Chest. Verify it after keying.
6. **HEIGHT.** Once FIX 3 lands, confirm the crown tip is the bounds top, so the stud pitch and 10 studs measure to the
   crown, not to the antennae.

---------------------------------------------------------------------------------------------------------------------
## 4. v2 sign-off checklist (all must pass)
1. **64 px slate icon** (icon3 recipe, next to the Grass siblings and Thunder Rex). I can name a mantis, a gold crown and
   ruby eyes. The crown is the biggest gold mass. No white face blob.
2. **Game camera:**
   - I can see a dark shield with ruby thorn tips, the crown with its back gem, two gold knee spines and ruby
     (not maroon) eyes.
   - ARMOR ≥ 35%, HIDE ≤ 45%, RUBY ≥ 4%.
3. **Side view:** three bands, BELLY ≥ 7% without highlights, no picket fence.
4. **Face close sheet:**
   - no pale mask
   - ruby domes rising above the head line
   - a V-brow lidding the eyes, slit pupils
   - antennae clear of the brows
   - front: no goggles; side and back: no headphones
5. **Arms:**
   - front: dark femurs, gold crescents and a splayed ruby saw
   - side: the gold crescent is ≥ 0.08 deep
   - no flat jade slabs
6. **Silhouette:** the crown tip is the highest point; HEIGHT is 10 studs to the crown.
7. **Rig:** Antenna_L is skinned; the pairs are extended; the test poses in 3.3 are collision_free.
8. **Hard rules:**
   - no Neon
   - ≤ 15k tris
   - studs on HIDE/ARMOR (the shield included); gold and ruby smooth
   - nothing floating; seat the eye pupils with surf_hit
9. **Deliverables:**
   - model sheet, close sheet, a game render at 600, and the 64/128 slate strip
   - a top render with the tegmina hidden (W1 check)
   - roar f30 in tq, front and game
