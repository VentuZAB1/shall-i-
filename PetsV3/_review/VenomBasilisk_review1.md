# Venom Basilisk - art director review 1 (2026-10-14) - REJECT v1 (revise the build, keep the design)

**Score: 5/10 for a 5% rare.** The concept is good, unique in the roster and correct for its tier: a frill-crowned
viper-lizard, a violet accent that no Grass sibling uses, and no gold. The build doesn't deliver it yet. Four
problems would make the owner say "cheap" again:
- **The body is a highlighter-green toy.** It is the brightest pet in the roster.
- **The crown frill doesn't read as the hero.** At 64 px it merges with the back sail into one purple crest, and from
  the front it reads as a maple leaf.
- **The head is Ivonrath's crocodile head, recoloured.** It is not a viper.
- **The stripes and belly band look like stickers.**

None of this needs a new design. Every fix is a colour, a parameter, or a head rebuild with the kit you already
use. A v2 review is needed.

What I looked at:
- `pets/VenomBasilisk.py`
- `_model_sheet`, `_close_sheet` and every single render at full size
- my own extra renders: game-camera head close, top-down, high tq at the icon angle, and an icon-pipeline portrait
- the Grass siblings' sheets and icons (Mossback, Stag, Treant)
- Ivonrath (model, close and code), ShadePanther, Cerberus, ThunderRex v3
- `_ALL_FIERCE_progress`, `_icons_sheet`, `LESSONS_ALL_PETS`, ThunderRex reviews 1-3
- the act docstrings of all 23 pets
- `pets/ThornbladeMantis.py` header (the 2% secret's palette, so we don't collide with it)

Evidence saved next to this file:
- `VenomBasilisk_r1_icons.png`: a 64/128 px slate strip built with the real `icon3` outline recipe. It shows the
  Grass egg, v1, mock A, mock B, Ivonrath and Panther.
- `VenomBasilisk_r1_mock.png`: v1 compared with a quick palette and hierarchy mock. The mock was a temp copy of your
  file with colours and a few numbers changed. It is a value check, not a design.

How I measured: I classified the pet pixels in the renders after removing the background (±3%). Luminance is
Rec.709 on the sRGB values.

| side view | light (≥0.65) | mid | mid-dark | notes |
|---|---|---|---|---|
| **Venom Basilisk v1** | **30%** | 46% | 23% | the only pet with more than 18% light |
| Ivonrath / ShadePanther / Treant | 7 / 2 / 4% | 12 / 19 / 21% | 78 / 78 / 75% | |
| ThunderRex v3 / Raiju | 18 / 8% | 16 / 44% | 65 / 48% | |
| ForestStag / Mossback (Grass) | 15 / 18% | 59 / 53% | 24 / 28% | |
| mock B (palette + wider saddle only) | 10% | 50% | 41% | game cam: light 8%, mid-dark 49% |

| v1 colour share | mid green | dark green + shading | pale | purple |
|---|---|---|---|---|
| side | 60% | 23% | **2.6%** | 14% |
| game cam | **64.5%** | 22% | 0.2% | 13% |
| tq / back / front | 59 / 60 / 64% | 22 / 22 / 14% | ≤1.3% | 17 / 17 / 21.5% |

Size: 3.20 long × 1.35 tall (L:H 2.38), 5,532 tris.

---------------------------------------------------------------------------------------------------------------------
## 1. What works (keep)

- **The concept and its parts.** Crown frill + back sail + banded whip tail + tail-frill echo. No other pet has this
  silhouette, and none of it remixes a sibling's accent: Mossback is lime, Stag emerald, Treant amber sap. Violet
  is free in the Grass egg.
- **The tier discipline.** No gold or "jackpot" piece. Ivory and violet only. The 2% Mantis owns GOLD and RUBY, so
  keep it that way.
- **Clean construction.** `surf_hit`/`surf_strip` seat the inlays on the tapered faces, the `thorn()` and `web()`
  helpers work, and the `frill_dirs()` cupped ruff, the seated sail roots and the frill collar are all good. Nothing
  floats, and 5.5k tris leaves lots of headroom.
- **The rig.** Throat pivot, Jaw, Tongue, Frill and the Venom anchor are all there. `check_pairs` already covers
  Frill against Neck, Neck2 and Chest.
- **Frill tilt of 12°.** That is the right compromise between the tq/icon camera (front face) and the game camera
  (back face). Keep it at 10-15°.
- **Dark socks, black splayed claws and elbow/knee spurs.** Family language, and they read.
- **Tail rings.** From above and from the game camera, the banded tail is the clearest read on the pet.
- **HEIGHT 8.** Sits between Mossback (7) and Treant (10), with the Mantis at 10 above it.

---------------------------------------------------------------------------------------------------------------------
## 2. Fix list, ranked (all in `pets/VenomBasilisk.py`)

### FIX 1 - Value structure and palette (MUST; the biggest single win)

**Why:** `GREEN (72,182,78)` has a luminance of 0.59. Every approved hide sits at 0.29-0.44: Ivonrath RED 0.29,
ThunderRex HIDE 0.37, Treant BARK 0.39, Mossback SHELL 0.41, Stag FLANK 0.44. Green is ~72% luminance by nature, so
the "brightest channel ≥170" rule from the Rex review doesn't transfer to green; use luminance instead. The second
problem is that GREEN_D only appears as a 0.022 saddle, slashes and socks. The result is one bright value band over
~60% of the pet, the "unpainted plastic" failure Rex v1 had. The accent makes it worse: VENOM's luminance is 0.46,
**darker than the hide**. So the eyes vanish, and the frill pops only by hue.

**Palette (Blender RGB):**

| role | new | was | luminance | where |
|---|---|---|---|---|
| HIDE | **(52,144,66)** | (72,182,78) | 0.47 | flanks, legs, neck sides, snout sides |
| DORSAL | **(22,72,44)** | GREEN_D (26,90,50) | 0.23 | back shells, head top V, neck/tail top, stripes, socks, thorn shafts on body |
| PALE | (224,228,150) | (218,232,146) | ~0.87 | throat, chin, underside band, tail underside (slightly warmer) |
| VENOM_DEEP | **(92,30,146)** new | - | 0.20 | sail membrane, frill shafts, frill inner band |
| VENOM | (198,78,255) | same | 0.46 | fang tips, tail-frill, sail top edge |
| VENOM_L | **(222,128,255)** new | - | 0.62 | frill outer membrane, tongue |
| EYE | **(232,170,255)** new | VENOM in the eye | 0.74 | eye slit (VENOM_HOT stays the highlight) |

- **Keep the hue at ~125-130°, true green.** Don't drift toward teal: the Mantis is jade/teal (36,182,146) on dark
  teal.
- **In-game check (×0.6).** HIDE becomes (31,86,40) and VENOM_L becomes (133,77,153), so the frill keeps ~1.3× the
  hide's value in game. The frill will look pink in Blender renders. Judge it in game, not in the Blender render.

**Dorsal blocking (construction):**
- Put DORSAL shells over the chest, waist and hips blocks. Each shell covers the top plus the upper ~35% of the
  flank (shell from `za ≈ 0.3·h.z` to the top). Use MoltenBoar's `shell()` and `prof()` (`pets/MoltenBoar.py`
  L46-58), or ThunderBull's cape (`pets/ThunderBull.py` L103-113).
- These shells replace the saddle (L139) and the shoulder block (L135).
- Continue the band:
  - up the neck as a top strip (ForestStag `B.bar` on Neck2, `pets/ForestStag.py` L88)
  - onto the head as the V marking (Fix 3)
  - down the tail as a top strip on each tail seg (top half only, so the rings and the pale underside still show
    from the side)

**Targets in the side and game views:** DORSAL 30-35%, HIDE ≤ 45%, PALE 7-10% (side), violet family 15-20%. Light
band ≤ 15%, mid-dark ≥ 40%. Mock B (only the new HIDE/DORSAL plus a wider saddle) already moved the side view from
light 30% to 10% and mid-dark 23% to 41%.

### FIX 2 - The crown frill must be THE hero (MUST)

**Why:**
- **At 64 px** (`VenomBasilisk_r1_icons.png`, "VB v1"), the frill sits just in front of the first sail spine, at the
  same height and in the same violet. The two read as one long stegosaur crest. The crown is invisible as a crown.
- **From the front**, 7 dark-GREEN shafts on lobed violet with deep V notches (scallop 0.28, web to 0.90 L) form a
  maple or cannabis leaf. Green veins on a lobed fan read as a leaf.
- **In the sail**, the scallop of 0.32 makes the side-view outline a sawblade (LESSONS #5: saw teeth).

**Changes:**
1. **Shape: a rounded fan with bone points, not a leaf.**
   - `FRILL_L = (0.38, 0.46, 0.52, 0.56, 0.52, 0.46, 0.38)` (was 0.27-0.51).
   - Frill `web(..., scallop=0.12)` with a `reach` parameter of 0.86 (was a hard-coded 0.90). The ivory points then
     stand ~0.07 clear of the membrane and read as a crown of bone spikes.
   - Mock A/B used exactly these numbers. Look at the front view in `VenomBasilisk_r1_mock.png`: the leaf is gone.
2. **Frill shafts → VENOM_DEEP.** Give `thorn()` a `col=` argument. Body and sail thorns stay DORSAL.
3. **Two-tone membrane.**
   - Inner band, root to 0.35 L: VENOM_DEEP.
   - Outer band: VENOM_L.
   - Build: two polys per panel, the outer one 0.004 proud. `B.poly` fans from `pts[0]`, so start the outer poly at
     the left inner-band point and keep the scallop ≤ 0.15 so the polygon stays star-shaped.
   - This gives the "light at the edge" step that Rex's DEEP→CYAN→HOT shards use, with no Neon.
4. **Separate the frill from the sail.** Covered in Fix 5: the sail starts further back and goes dark.
5. **Tail-frill:** the same treatment, smaller: DEEP shafts, VENOM_L membrane, scallop 0.15. It echoes the crown.

**Target:** at 64 px on slate you can point at a bright violet fan on the head, separate from a darker back sail.
Mock B is already close; the head rebuild and the dorsal colour will finish it.

### FIX 3 - A real viper head, not Ivonrath's (MUST)

**Why:** compare L170-203 with `pets/Ivonrath.py` L201-229. The skull, dark crown plate, snout, snout ridge, nostrils,
teeth row, lower jaw (0.105 vs 0.104), chin (0.075 vs 0.075), mouth plate, jaw muscle, eye socket, `fierce_eye`
(yaw 26) and the two cheek spikes per side (almost the same vectors) are a 1:1 copy. In `_close_sheet` it is
Ivonrath's head in green. Ivonrath is a 4% pet a player may own, so this reads as a recolour. A viper head is an
**arrowhead from above**: wide venom-gland cheeks, a flat top, a short tapering snout, and a narrower neck behind it.

| part | now | v2 |
|---|---|---|
| skull seg (L170) | hw 0.17, hd 0.095, top (0.72,0.9) | **hw 0.20, hd 0.085, top (0.55,0.9)**: flat and wedge-tapered |
| jaw muscle → venom-gland cheeks (L190) | (0.145,0.07,0.05) at y -0.90 | **(0.205,0.08,0.055) at (0,-0.88,0.70), top (0.9,0.9)**: the widest point of the head, right behind the eyes |
| snout seg (L172) | tip y -1.30, hw 0.118, top 0.62 | **tip y -1.24, hw 0.11, top (0.55,0.8)**: tip hw ≈ 0.06 |
| lower jaw (L184-185) | to y -1.28, top 0.68 | **to y -1.22, top (0.55,0.9)**, so the fangs hang outside it |
| Neck2 (L164) | hw 0.135 | **0.12** ("neck pinch"). LESSONS #4's "≥0.9 HW" is about gaps; here the frill collar hides the junction, so check the back view for a dark slot |
| dark crown plate (L171) + snout ridge (L173) | a flat rectangle + a thin rod that reads as a loose stick from the side and a "tie" from the front | **delete both.** Add a viper **V marking** instead: two DORSAL bars, 0.035 wide, from the skull's rear corners (±0.13, -0.84) converging at (0, -1.12), laid flush with your `surf_strip` (proud 0.008) |
| cheek thorns (L202-203) | Ivonrath's exact pair | **delete**. The frill's ±84° spines already frame the cheeks, and the gland bulge supplies the width |

Check from the top view: the widest point (cheeks, 0.205) should be ≥ 1.6× Neck2, and the outline should be a
spade.

### FIX 4 - Face read: eyes, horns, fangs, nostrils, tongue (MUST)

- **Eyes.** In my high tq (icon angle) render the eyes are completely hidden under the brow slabs. In the close views
  they are tiny dark-pink squares, because VENOM is darker than the hide.
  - Main slit colour → EYE (232,170,255).
  - `sc` 0.95 → 1.15, yaw 26 → 30.
  - Seat the eye on the corner of the new flat skull, about (±0.12, -1.02, 0.86).
  - If the brow still covers more than 40% of the slit at a 40° tq, shrink the brow's forward offset in your local
    `fierce_eye` from `n*0.022` to `n*0.012`.
  - Delete the raised green socket block (L196). From the side it sits in front of the eye.
- **Horned-viper brows.** Two stubby slabs per side currently read as a visor or cat ears. Use **one horn per
  side**: `thorn(B, (s*0.115, -1.00, 0.895), (s*0.30, 0.35, 1), 0.13, 0.026, "Head")` (DORSAL shaft, ivory point).
  Delete the second spike (dx 0.03).
- **Fangs (the venom read).** Today the ivory shaft (f0 x ±0.048, L 0.085) is buried inside the lower jaw (x ±0.072
  at that y, z 0.644-0.706), and only the violet tips poke out under the chin as two "drips".
  - Move `f0` to **(s*0.068, -1.19, 0.728)**.
  - Ivory: dir **(s*0.10, -0.18, -1)**, L **0.10**, w 0.02.
  - Venom tip: L 0.045, in VENOM.
  - With the narrowed lower jaw (Fix 3), the sabres hang outside the lower lip, visible from the side and as two
    ivory fangs flanking the chin from the front. That is the same fix that landed on Rex (review 3, item 6).
  - Upper teeth: 4 → **3 per side, L 0.03**, so the fangs are ≥3× any tooth.
- **Nostrils.** The black dashes on the snout's front face (L175) read as a second pair of sleepy eyes from the front
  (Rex v1 lesson).
  - Move them to the top-front corners of the snout tip, about (±0.04, -1.225, 0.80), angled 25° outward.
  - Add **pit-viper heat pits**: a BLACK block (0.008, 0.018, 0.014) on each side face at (±0.085, -1.13, 0.775).
    It is a cheap, unmistakable "viper" detail in the side view.
- **Tongue.** It is too thin to read, and it is VENOM_D inside a dark MOUTH.
  - seg hw 0.016 → **0.024**, hd 0.006 → **0.010**.
  - forks L 0.06 → **0.08**, w 0.008 → **0.016**.
  - colour → **VENOM_L**.
  - Add a MOUTH-coloured **rostral notch** (0.03 wide) at the snout tip's lower edge, so idle flicks can slide the
    tongue out ≥ 0.10 past the snout without opening the jaw.

### FIX 5 - Sail hierarchy (MUST, pairs with Fix 2)

- **Start the sail further back and lower it,** so the dark neck shows between the frill and the sail:
  - `sy = (-0.32, -0.18, -0.04, 0.10, 0.24, 0.36)`
  - `sl = (0.22, 0.32, 0.36, 0.34, 0.26, 0.18)`
- **Sail membrane → VENOM_DEEP**, `scallop 0.12`, `reach 0.92`. It now reads as one continuous basilisk sail instead
  of saw teeth, and it is clearly second to the frill. Optional: a thin VENOM strip (0.025) along the top 25% of the
  sail, so the game camera still catches a violet line.
- **Tail1 mini-sail (L252-255).** From the game camera it reads as a stray fin with a gap in front of it. Pick one:
  - delete it, or
  - give it the same DEEP membrane and move its first root to y 0.50, so the gap after the last back spine is ≤ 0.12.

### FIX 6 - Stripes and belly: kill the stickers (MUST)

- **Stripes (L151-155).** Five 0.05 × 0.18 slashes per side float mid-flank. From the side they read as scattered
  scratches, the Rex v1 sticker problem.
  - **Delete them.**
  - Cut **4 stripe teeth per side** into the lower edge of the new dorsal shells at y ≈ -0.40, -0.18, 0.04, 0.26.
    Each one is a flush poly on the flank (`side_pt()` from MoltenBoar L61-67, or ThunderBull's ragged cape edge
    L110-113): ~0.10 wide where it leaves the shell, ending in a point 0.20-0.24 lower, slanted back 25°.
  - The stripes then *grow from the dark back*, the way a tiger's or a jungle viper's do.
  - Give each upper leg one DORSAL band, matching the tail rings, so the legs aren't plain green tubes.
- **Belly band (L146-150).** At z 0.41-0.50 and 0.065 wide it reads as a cream racing stripe in the side view and as
  a "banana" sliver from the game camera.
  - Lower it until its bottom edge sits ~0.01 above the torso's lower silhouette.
  - Width → **0.12**.
  - Move the PALE_D scute gaps (L156-160, currently under the belly where nobody sees them) onto this band: 5 gaps.
  - Target PALE 7-10% in the side view (now 2.6%).

### FIX 7 - Proportions (SHOULD; the sprawl is strongly recommended)

- **Tail.** About 43% of the length, a long thin stick in the game view, and the main reason the 64 px icon is a
  horizontal line (the same lesson as Rex v1). Shorten it ~13%:
  `TAILP = [(0,0.52,0.54),(0,0.80,0.47),(0,1.06,0.40),(0,1.30,0.35),(0,1.50,0.32)]`.
  - With the shorter snout and the taller frill, L:H goes from 2.38 to ~2.05.
  - In **idle**, hold a gentle S-curve (Tail2-4 yaw 6/9/12°, swapping sides slowly), so the game camera never sees a
    straight stick.
- **Body width.** From the top view it is a stick. Widen by ~10%: chest hw 0.22 → **0.245**, waist 0.17 → **0.19**,
  hips 0.19 → **0.21**. LESSONS #1 still holds (chest = 1.17× hips).
- **True lizard sprawl.** The legs are Ivonrath's dragon stance (knee x 0.36, foot x 0.31, feet *under* the
  elbows). That plus the copied head is why the side view is "Ivonrath without wings". A basilisk stands with its
  feet *outside* the elbows. This also turns the game-camera silhouette from a stick into an X.

  ```
  LEGS = {"F": ((0.20, -0.40, 0.50), (0.42, -0.33, 0.30), (0.40, -0.44, 0.09), (0.40, -0.50, 0.04)),
          "B": ((0.20, 0.34, 0.50), (0.43, 0.24, 0.32), (0.42, 0.44, 0.12), (0.42, 0.38, 0.04))}
  ```

  Re-run `collision_free`: the Shin/Foot vs Head/Jaw/Frill pairs already exist.

### FIX 8 - Frill flare rig (SHOULD, before animating)

A single `Frill` bone can only tilt, and the whole frill is already fully open at rest. So the "flare" in the hiss
would be a small nod.
- **Minimum (single bone):** the roar folds the frill back +20° (anticipation), then snaps it to -8° (upright and
  slightly forward) in 3 frames, with a 3° overshoot. A fold-then-snap reads as a flare.
- **Better (recommended):** split it into `Frill` (the 3 centre spines and their 2 webs) and `Frill_L`/`Frill_R` (the
  2 outer spines per side).
  - Put the boundary webs (between ±30° and ±58°) on the outer bones.
  - Extend each boundary web's inner edge 15° under the centre membrane, 0.008 behind it, so the outer groups can
    rotate +15° outward in the fan plane (to about ±100°) without opening a gap.
  - Rest = as modelled. Hiss = outer groups spread +15°, the whole fan snaps upright, then a quiver.
  - Add `Frill_L`/`Frill_R` to `check_pairs` against Neck, Neck2 and the front legs.

---------------------------------------------------------------------------------------------------------------------
## 3. Signature act - my pick: the hind-leg SPRINT ("BASILISK DASH"), not the spit

**Why the sprint reads better:**
- **From the game camera** (high, behind), the sprint is the only option with a big silhouette change seen *from
  behind*:
  - the body tilts up
  - the sprawled hind legs cycle on both sides of the body
  - the tail whips left and right right in front of the camera
  - the frill streams back flat

  A rear-up and spit is aimed *away* from the camera. The frill hides the head from behind, so the spit lives or
  dies on VFX.
- **Uniqueness.**
  - Nobody in the roster sprints on two legs, and it is *the* real basilisk behaviour.
  - A spit repeats the pet's own roar climax (frill flare, jaw open).
  - It also repeats Thunder Rex's mouth-projectile structure (charge → fire), which that review approved precisely
    as "the only breath act".
  - The rear-up repeats NightmareStallion's `act_rear`.
  - The Grass Mantis's roar is a threat-display reveal too. One display per egg is enough; the Basilisk's act should
    be motion.
- **Fierce, not goofy.**
  - No upright cartoon run with spinning legs.
  - A low predator burst: trunk at 35-40°, head locked level on the target, frill flat like a blade, tail a straight
    counterweight.
  - Short and fast, with a hard skid-stop and a frill *flash* as the payoff.

**Footprint:** a straight line ahead, ~0.62 model units out and back (≈3.7 studs at x1, ≈8 at x2.2). The lateral
footprint is the body width. If the follow system parks pets *directly behind* the owner, cut the travel to 0.45 and
check it in Studio.

**ACT_DASH, 104 f (3.5 s).**

| frames | beat | keys (+ pitch = nose-down; forward = -y) |
|---|---|---|
| 0-14 | **anticipation: lock on** | Spine z -0.05, y +0.05 (weight back onto the haunches), pitch +4; Chest +2; Neck +6; Head +2 (snout on target); Frill +20 (folded flat back, streamlined); Tail1-2 -4 (pressed down); tongue flick f4-10; Tail4 yaw twitch ±8 at f8/f11 |
| 14-22 | **rear and launch** | Spine pitch +4 → **-36** by f20 (fast ease-out), z +0.10, y -0.08. Front legs released from IK and tucked by f19 (Leg_F back 40°, Shin_F folded 70°, toes curled). Head +24 / Neck -4, so the snout stays ~10° above level (pitch-down relative, inside the limits). Tail1 counter-pitched ~30° up relative, so the tail stays near horizontal (tip ≥ 0.12 off the ground). First hind push f18 |
| 22-42 | **sprint: 5 hind steps**, one every 4 f (f22/26/30/34/38) | IK feet, stride 0.10, lift 0.07, knees out (sprawl). Spine y -0.08 → -0.58; pitch -36 ±3 on the beat; roll ±6 alternating; z bob 0.015 (down on contact). Tail yaw ±10 against the roll, Tail3-4 lagging 2 f (whip). Arms pump ±8. Head yaw counters the roll, so the head stays *locked* in world space (that is not a shake). Frill stays folded, jaw shut |
| 42-50 | **skid and brake** | hind feet plant at f42/f44 and STAY planted (slide audit 0). The body brakes by leaning back: pitch -36 → -44 at f46, y -0.58 → -0.62. Tail1 drops until the tail drags at f46 |
| 50-56 | **slam down** | pitch -44 → +6 by f55 (ease-in, accelerating like it is falling). Front feet unfold and plant at f54-55, claws splayed. Spine z -0.04 on impact at f55. Tail slaps down at f56. Event `stomp` f55 |
| 56-72 | **frill flash** (the payoff) | Frill +20 → -8 in 3 f (f56→59), overshoot -11 at f60, settles -8 by f62 (split-frill rig: outer groups +15° at f59). Jaw 18° at f58 (short hiss, tongue stays IN, so it doesn't copy the roar). Hold f60-70 with the frill quivering ±2° every 2 f and a Chest tremble of ±1. Head level, no yaw. Events `frill_flash` f58 (Frill), optional `venom_drip` f60 (Venom anchor: a drip, not a spit) |
| 72-96 | **back off to the spot** | jaw shut by f74; Frill → 0 by f82. Four sprawled backpedal steps (diagonal pairs, 6 f each: f74/80/86/92), Spine y -0.62 → 0, facing unchanged. Head stays on the target until f88, then relaxes; the tail sways back to centre |
| 96-104 | **settle** | Spine z 0; exhale (Chest +1 → 0); a sign-off tongue flick f98-103 |

- Limits: Neck ≤ 8 (+6/-4). Chest vs Spine ≤ 5 (+2/±1). Head+Neck pitch-UP never above 0 here, since the head only
  pitches down to stay level. No head shake: the locked head and the frill quiver don't oscillate the head.
- Use hard stops at f20 (launch), f55 (slam) and f59 (frill snap).
- Run `plant_frames` for every planted range, plus `collision_free` (tucked front feet vs the neck and jaw, the tail
  vs the ground during the rear) and `ground_min_z ≥ -0.006`.
- Return a pose sheet at f10, f20, f30, f46, f55, f60 and f86, including one *game-camera* pose at f30.
- **If travel is ruled out** (owner or follow-system decision), take the spit instead. Even then, don't rear: make it
  a viper STRIKE.
  - coil back (Neck -6, Head -10, Spine y +0.04)
  - lunge (Spine y -0.15 in 3 f), with `venom_spit` at the apex
  - snap back
  - Keep the roar's frill flare out of it.

**Notes for the other three clips:**
- **Idle:**
  - tongue flicks through the notch: 2 per loop, out 6 f, back 4 f
  - look-around of ~±25° total (the Rex review lesson: 12° is invisible from the game camera)
  - frill twitches: ±4°, 3 f
  - the tail S-curve from Fix 7
- **Walk:** the lizard S-sway has to come from Spine yaw (±8) plus tail plus Neck (≤8), because Chest vs Spine is
  capped at 5°. Sprawled feet need a wide arcing swing, not a straight fore-aft step.
- **Roar:** a slow build (the frill rises over ~10 f), jaw ~36°, tongue fully out, long hold, Head+Neck ≤ 30. That
  keeps it clearly different from the act's instant flash.

---------------------------------------------------------------------------------------------------------------------
## 4. Approval checklist for v2 (all must pass)

1. **64/128 px strip** on slate using the real icon recipe, with Mossback, Stag, Treant, Ivonrath and Panther. You can
   name three things: a lizard, a violet crown-fan on the head that is separate from the back sail, and stripes.
   It looks rarer than Treant and NOT like a recoloured Ivonrath.
2. **Value:** side and game views have ≤ 15% light and ≥ 40% mid-dark. Shares are DORSAL 30-35 / HIDE ≤ 45 / PALE
   7-10 (side). The violet family is 15-20%, with ≥ 50% of it in the frill (tq and game).
3. **Frill:** it is the highest point and the brightest violet on the pet. No leaf from the front (scallop ≤ 0.15,
   points stand ≥ 0.06 clear). From the game camera it reads as a fan.
4. **Head:** an arrowhead from the top (cheeks ≥ 1.6× Neck2, snout tip hw ≈ 0.06). The V marking is in, and none of
   Ivonrath's crown plate, snout rod or cheek spikes remain.
5. **Face** (close sheet plus a 40° high-tq crop): both eyes clearly visible as lilac slits; one horn per side; ivory
   fangs visible from the side AND the front; nostrils at the tip; heat pits; nothing reads as a second pair of eyes.
6. **Pattern:** stripes grow out of the dorsal; no floating slashes; the pale underside reads as a belly, not a
   racing stripe.
7. **Proportions:** L:H ≤ 2.1, feet outside the elbows, chest hw ≥ 0.24.
8. **Hard rules:**
   - no Neon or glow
   - ≤ 15k tris
   - nothing floats
   - `collision_free` with the new legs and frill bones
   - no detail under 0.02 except the family pupil
   - no gold anywhere
   - hue stays true green, away from the Mantis's jade
9. **Deliverables:** model sheet (tq/front/side/back/game), close sheet, high-tq face crop, top-down render, the icon
   strip. Then, once the model passes, the clip pose sheets.
