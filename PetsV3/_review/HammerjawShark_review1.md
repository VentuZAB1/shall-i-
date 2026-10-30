# Hammerjaw Shark - art director review 1 (2026-10-14) - REVISE (rebuild the look, keep the plan)

**Score: 4/10 for a 5.5% pet.** It is the right animal with the right parts: a T-head, a tall dorsal, a crescent
tail, a hover, coral accents, and 5 gill slashes. But it reads as a **blue toy jet plane**, not a war shark. It does
not beat the Tide commons. It is less finished than the Kraken (8 studded arms, sucker rows, warning rings, an eye
band) and the SeaTurtleWarrior (a trident, an armoured shell, a war-band). The bones, the hover height, the PITCH
formula and the concept are all fine. Everything visible needs rebuilding: the body, the hammer, the fins and the
colour blocking.

What I looked at:
- `HammerjawShark/renders/_model_sheet.png` and all 5 single renders at full size
- `pets/HammerjawShark.py`
- the Tide siblings (Kappa, SeaTurtleWarrior, Kraken: sheets and scripts)
- `_ALL_FIERCE_progress.png` and `_icons_sheet.png`
- the Thunder Rex reviews 1-3, its scripts and the owner preview
- owner ref `_refs/fierce/f_63` (Orca)
- the kit (`blockkit.py` Poly/seg/spike/bar)

I also made my own slate cut-out at 64 px and a 0.6x "in-game" darkened copy.

How I measured: I flood-filled the background and classified the pet pixels by hue, saturation and value
(about ±3%). "ARMOR" means STEEL_D pixels that stay dark under lighting.

| view | ARMOR (STEEL_D) | STEEL | BELLY | CORAL | notes |
|---|---|---|---|---|---|
| side | 2.6% | **84.1%** | 3.7% | 6.8% | steel value p10-p90 = 0.54-0.88: one band |
| game cam | 5.3% | **86.2%** | 1.4% | 4.5% | |
| tq | 0.3% | **83.3%** | 2.6% | 11.2% | |
| back 3/4 | 4.0% | **81.3%** | 7.3% | 5.6% | |
| front | 0.2% | 79.5% | 5.8% | 11.5% | |

---------------------------------------------------------------------------------------------------------------------
## 0. The builder's four concerns, answered

1. **"Plain and boxy": yes.** The body is two boxes plus a cone, with steps between them, and one flat colour
   covers it. See 1.2 and 1.6. Fixes: 2.1 and 2.3.
2. **"War-plates barely read": yes, and here is why in numbers.**
   - STEEL_D (44,64,102) has the same hue and saturation as STEEL (78,118,170): 219° / 0.57 vs 214° / 0.54. It
     only has 0.6x the value.
   - Under lighting, a lit plate top is as bright as a shaded flank, so the plates drop into the steel band. Only
     0.3-5% of pixels stay "dark".
   - The plates are also short, flat-topped and narrower than the body (hx 0.12-0.18 vs body hw 0.18-0.225), and
     they sit only on the top.
   - Fixes: 2.3 and the palette.
3. **"Steel too close to Thunder Rex": the hue is not the real problem.**
   - STEEL is 214°; Rex HIDE is 234° and Raiju FUR is 227°.
   - The problem is the flat mid-value. Rex v1 failed in exactly the same way (review 1: "one flat colour =
     unpainted plastic").
   - Still, move STEEL to true steel-blue **(70,130,180), 207°**. Paired with gunmetal armour, a white belly and
     coral (against Rex's navy, cyan and gold), it cannot be mistaken for Rex.
4. **"Fins are flat polys": yes, and the kit can't fix that for you.**
   - `bk.Poly` is a uniform-thickness prism. It has no studs, no bevel and no taper (`blockkit.py` L99-131).
   - So every fin is an unstudded sheet of paper with ruler-straight edges.
   - Fix: see 2.5.

---------------------------------------------------------------------------------------------------------------------
## 1. Why it looks cheap (specific)

1. **It reads as an aircraft.**
   - **Pectoral span 1.32 is 42% wider than the hammer (0.93).** From the game camera the widest things are
     swept "wings", not the hammer.
   - The body is a straight fuselage held dead level.
   - The dorsal is a flat-topped trapezoid (`dors` L103-104: the top runs y -0.12 to 0.02 at z+0.62/0.60) with a
     painted coral cap, which reads as an airliner tail.
   - Constant-width coral stripes along every leading edge read as aircraft livery.
   - The 64 px icon and the game view both say "jet".
2. **One flat mid-blue.** STEEL is 81-86% of the pixels in every view, the same failure as Rex v1. BELLY is only
   1.4-7%, so there is no countershading read. Nothing in the colour says "war".
3. **The war-plates read as car-roof windows or hatches.**
   - From the game camera there are 5 dark rounded rectangles sitting on top.
   - The coral seams are 0.03 bars on the top only, so you can't see them from the side.
   - The plate-edge spikes (0.09, pointing down and out) read as random dark triangles stuck on the flank.
4. **The hammer is a plank, not a weapon.**
   - It is one straight bar (hx 0.40, 0.11 thick).
   - The 5 small upright cap spikes read as a comb or a bench back from behind.
   - The dark leading-edge band (L74) reads, from the front, as a visor slot or a closed mouth. The front view
     looks like a robot visor.
   - The eyes are flat coral rectangles on the outer faces. They read as headlights or tail lights, and they are
     invisible from above. From the game camera the pet has no face at all.
5. **The jaw is a small box hidden under the hammer.**
   - The teeth are 0.035-0.045 long and show only in the straight front view.
   - The roof of the mouth is the studded BELLY underside (L91), so every open-jaw frame will show white Lego.
6. **The body is two boxes plus a cone.**
   - There are steps where Chest meets Spine (hw 0.225 → 0.18, hz 0.235 → 0.195) and again at Tail1.
   - The head core (hw 0.16) is narrower than the chest (0.225), which reads as a neck. Sharks have none.
   - The body stays full depth to y 0.34 and then cones. There is no fusiform taper.
7. **The fins are paper.**
   - Every fin is a flat, unstudded slab with straight edges and no root. The studded body stops dead at a
     smooth sheet.
   - The lower caudal lobe (0.42) is almost as long as the upper (0.58). A hammerhead's upper lobe dominates.
8. **The "battle scars" read as racing stripes or air vents.** They are constant-width pale bars in parallel pairs.
   A scar needs taper, irregularity and asymmetry.
9. **Detail.** At 3.3k tris it is the simplest pet in its egg, and it is meant to be the rarer one.

**Keep:**
- the concept and the hover (Z0 0.62, MOTION Swim)
- coral as the accent (it is the Tide egg's war colour; SeaTurtleWarrior uses it too)
- the 5 gill slashes as a feature
- the bone names
- the PITCH formula

---------------------------------------------------------------------------------------------------------------------
## 2. Redesign brief - "THE REEF BREAKER" v2

**Concept:** an armoured war-hammerhead.
- Its head is a war-hammer: a dark armour helm outlined in coral, with heavy armoured eye lobes and back-swept
  brow spikes.
- Its back is a row of shingled gunmetal armour lames split by coral seams.
- A steel-blue hide shows below the lames, over a crisp white belly.
- It has a tall sickle dorsal fin with bite notches and a deep crescent jaw with two rows of teeth.

**Egg and family rules:**
- **No gold.** Gold crowns are the secrets' language (Ivonrath, Rex).
- **No black-and-white orca blocking.** That is reserved for the 1.5% Abyssal Orca, so the shark must leave it room.
- Coral is shared with SeaTurtleWarrior. The shark's tier step is the **3-step coral gradient**
  (CORAL_D → CORAL → CORAL_HOT), the "no-Neon glow" that Rex's crystals use. The commons only have flat coral.

Coordinates below use the v1 frame (z relative to Z0; -y is forward).

### 2.1 Silhouette and proportions (biggest single win)
- **Make the hammer the widest thing.**
  - Hammer outer span **1.04** (x ±0.52 including the eye lobes).
  - Pectoral tips at x ±0.46 (span 0.92).
  - Rule: hammer span ≥ pectoral span + 0.10.
  - From above it must read as a T before anything else.
- **One continuous fusiform taper,** deepest and widest just behind the gills:

  | station y | half-width | top z | bottom z |
  |---|---|---|---|
  | -0.80 (head joins) | 0.20 | +0.17 | -0.12 |
  | -0.48 (shoulder, max) | **0.25** | **+0.29** | **-0.23** |
  | -0.10 | 0.21 | +0.25 | -0.19 |
  | 0.30 | 0.15 | +0.17 | -0.15 |
  | 0.66 | 0.095 | +0.12 | -0.10 |
  | 0.98 (peduncle) | 0.055 | +0.10 | -0.04 |

  - The back line rises from the hammer cap to a shoulder hump, then falls steadily.
  - The belly line is deepest under the pectorals and rises continuously to the tail.
  - No step between neighbouring sections may exceed 0.02 (now 0.045).
- **No neck.**
  - The head core's rear is ≥0.20 hw (85% of the shoulder) and buried 0.10 into the Chest block.
  - The head flows into the body.
- **Length ≤ 2.45** (now 2.50). The hammer edge moves forward to y -1.16, so take 0.08 out of Tail2. The caudal
  tip ends near y 1.30.
- **Height:** dorsal tip at z+0.80 (now +0.62) and caudal upper tip at z+0.60. L:H in the side view **≤ 2.2:1**
  (now ~2.55).
- **Size:**
  - HEIGHT 7.0 → **8.0**, and H_MODEL = the new dorsal tip (~1.42), so PITCH recomputes. That keeps v1's world
    scale (5.6 vs 5.8 studs per unit).
  - It then stands above Kappa (7) and Kraken (7.5) and leaves room for the secret above.
- **Mass:** look at f_63. The owner's Orca reads because it is **bulky**: a fat body, a heavy head and thick stepped
  fins. Copy the bulk, not the colours.

### 2.2 Head and hammer - THE WAR-HAMMER (the hero feature for this pet)
This is the thing players must name at 64 px and from the game camera.

**Planform (seen from above)**
- **Centre block:** y -1.16..-0.90, hw 0.17, half-thick 0.06 at z+0.075, top taper (0.88, 0.85). STEEL.
- **Two wing blocks** from x ±0.14 to ±0.44:
  - chord 0.20 → 0.15
  - thickness 0.12 → 0.09
  - **swept back 14°** (tip trailing edge near y -0.86)
- **Eye lobes ("the hammer faces"):**
  - ARMOR blocks, half (0.07, 0.11, 0.075), at (±0.47, -0.97, z+0.075), rnd 0.40.
  - They should be chunky. They are the striking faces of the war-hammer.
- **Leading edge:** a rounded STEEL edge with a **0.035-deep median notch** at x = 0 (the great-hammerhead notch).
  Build it as two segs meeting at the notch.
- **Underside:**
  - A BELLY plate under the whole hammer.
  - The bottom must be **flat and level at z+0.015** with no anhedral, so the whole front edge strikes the ground
    together in the act.

**The armour helm (top of the hammer)**
- An ARMOR cap plate, 0.03 thick, studded, over the centre and the wings, inset 0.025 from the edges.
- A **CORAL rim inlay**, 0.022 wide and flush, along the cap's front and rear edges (Ivonrath `surf_strip`). From
  the game camera the head becomes a **dark T outlined in coral**.
- A **central keel ridge**: ARMOR, 0.05 wide x 0.035 tall, running from y -1.10 back over the head core into lame 1.
  It makes one continuous sawback line from the hammer to the dorsal.
- **Delete:**
  - the 5 upright cap spikes (L72-73)
  - the STEEL_D leading-edge band (L74)
  - the front-face nostril dashes (L87-89). Put small dark nostril slits on the leading edge near x ±0.36 instead,
    where real hammerheads have them.

**Eyes and brows**
- Use **`fierce_eye`** (`pets/ThunderRex.py` L112-126). Copy it and add colour params, as Ivonrath's has `brow_c`:
  - CORAL iris, CORAL_HOT hot spot, black pupil, ARMOR brow.
  - Place it on the **outer-front face of each lobe**: yaw ~60° (sideways and 30° forward), tilt 18 (inner end
    low), sc 1.5.
  - Both eyes then read in the front, side and tq views. No more flat "headlights".
- **Brows:** a heavy ARMOR brow over each eye, overhanging 0.03, plus a **back-swept brow spike** growing from the
  lobe top:
  - two-tone, ARMOR → CORAL tip (MoltenBoar `spike2`)
  - L 0.13, w 0.035, direction (±0.45, 0.80, 0.40)
  - From behind, two horns frame the T. From the front, it gives a frown.

**Head core:** studded STEEL, rear hw ≥0.20, buried 0.10 into the Chest, with BELLY underneath.

**Jaw: a deep crescent, set back** (needed for the signature; see rig item H)
- The jaw front sits at y -0.95, **≥0.21 behind the hammer edge**.
- The jaw underside sits at z-0.115, **≤0.13 below the hammer underside**.
- **Lower jaw:** a centre seg plus 2 side segs angled back 25° (a crescent from the front), hw 0.17. BELLY, with an
  ARMOR chin plate. **Rest it open 10°**, so the teeth and the dark mouth show in the icon.
- **Teeth:**
  - Upper: 7 per side, broad triangles (w 0.016-0.020, L 0.055 at the front → 0.035 at the back). Set them
    **outside the lower lip** (Rex review-2 fix E) and tilt them out 6-10°.
  - Lower: 6 per side, narrow needles (w 0.012, L 0.045 → 0.03).
  - Make one lower tooth broken (L 0.02) as battle damage.
- **Mouth interior:** dark MOUTH plates on the Head (roof) and on the Jaw (floor) (`pets/ThunderRex.py` L244-245).
  No studded white roof.
- If the portrait still hides the mouth, lower the **portrait camera ~8°** for this pet. This follows the Rex
  precedent of a per-pet icon camera tweak.

### 2.3 The war-back (supporting feature): shingled armour lames with coral seams
- **6 lames from y -0.76 to 0.46**, about 0.20 long each, plus 3 smaller rings on Tail1-Tail3.
  - Lames 1-3 are on the Chest; lame 3 overhangs the Chest/Spine joint.
  - Lames 4-5 are on the Spine.
  - Lame 6 is on Tail1.
- **Wrap them down the flank** to local za ≈ +0.0..+0.02, about 45% of the body depth. Use
  `shell(B, block, y0, y1, za, ARMOR, rnd=0.42)` from `pets/ThunderRex.py` L54-65 (MoltenBoar's shell).
  - From the side this makes a dark saddle, not a roof line.
- **Shingled:**
  - Each lame's rear edge overhangs the next by 0.03.
  - Each lame belongs to the **front** bone.
  - This hides every body joint during the S-wave.
- **Jagged lower edge:** 3 short armour teeth per side per lame, lengths 0.07/0.05/0.06, hy 0.045
  (`pets/ThunderRex.py` L202-208).
- **Coral seams:**
  - A flush CORAL band, 0.035 wide, fills every gap, from the keel down to the lame's lower edge
    (`pets/ThunderRex.py` L209-210, or LavaGolem `band()`).
  - The two shoulder seams get a 0.012 CORAL_HOT centre line.
  - From the game camera you then get a dark segmented back with coral rings running into the tail. It is the
    strongest read after the hammer.
- **The keel ridge** from the helm continues along the lame tops (0.035 tall) and rises into the dorsal's armoured
  root.
- **Delete** the 5 roof plates, their 10 flank spikes (L37-43) and the 4 top-only coral bars (L44-47).

### 2.4 Palette (Blender values; in-game is about x0.6)
| role | Blender RGB | in game ~ | where | target share (side / game cam) |
|---|---|---|---|---|
| ARMOR | **(46, 60, 88)** gunmetal navy | (28,36,53) | lames, hammer helm, eye lobes, brows, chin plate, keel, fin root fairings, peduncle keels | 28-35% / 32-40% |
| STEEL | **(70, 130, 180)** true steel-blue (brightest ch. 180 ≥ 170) | (42,78,108) | flanks below the lames, head core, hammer edge and wings, fins, tail sides | 30-40% |
| FIN_IN | (56, 104, 150) | | inner panel of the pectorals and caudal (2-tone, like Ivonrath MEM_IN) | ~4% |
| BELLY | (232, 236, 244) | (139,142,146) | lower flanks, belly, hammer underside, jaw, tail underside | **≥12%** side / ≥5% game |
| BELLY_D | (196, 204, 222) | | belly shadow lines, scar rims | small |
| CORAL_D | (196, 58, 36) | | roots of the fin edges, seam ends | |
| CORAL | (255, 118, 58) | (153,71,35) | seams, helm rim, gill flaps, fin leading edges, eyes, brow-spike tips | coral family **9-14%** |
| CORAL_HOT | (255, 206, 150) | | fin-edge tips, eye hot spots, shoulder-seam centre lines | ~2% |
| SCAR | (236, 176, 160) | | tapered claw gouges | <1% |
| MOUTH | (60, 16, 28) | | mouth roof and floor, gill slits | |
| TEETH (240,236,222), BLACK (14,14,22) | | | teeth / sockets, pupils, nostrils | |

- ARMOR vs STEEL is now a **value and saturation** step: V 0.35 vs 0.71, sat 0.48 vs 0.61. It is no longer the same
  colour at 0.6x, so the lames will survive lighting.
- No single colour may exceed 45% of the visible pixels.

### 2.5 Fins (build them, don't cut them out of paper)
**General rule.** Every big fin is built from three parts:
- a **studded, tapered root block** (ARMOR fairing or STEEL)
- 1-3 **stacked tapered blocks** stepping toward the tip, thickness root 0.07-0.09 → tip 0.03. This is the stepped
  look of the Orca ref, done with Ivonrath's two-part `crest()`.
- a **3-step coral leading edge**: chained bars CORAL_D → CORAL → CORAL_HOT, the same colour-step logic as Rex's
  `shard()`

Use `B.poly` only to fill the thin trailing area. No flat coral caps on fin tips.

- **Dorsal (the highest point; a falcate sickle):**
  - The root runs y -0.16..+0.16 on lames 3-4 with an ARMOR fairing. It is on the **Spine** bone, and its root is
    entirely behind the Chest pivot (see rig item C).
  - The leading edge curves up and back to the tip at (y +0.14, z+0.80). The trailing edge is concave, down to a
    free rear tip at (y +0.22, z+0.30).
  - Build it as 3 stacked blocks stepping back, half-thickness 0.045 → 0.032 → 0.022, STEEL.
  - Cut **2 V-notches into the trailing edge** (0.05 deep). Bite marks in the silhouette are the best "battle-scarred"
    read there is.
- **Pectorals (falcate, swept and drooped, not wings):**
  - Root chord 0.22 (y -0.46..-0.24) on a studded Chest fairing.
  - Tip at (±0.46, -0.08, z-0.32): swept back ~35°, drooped ~25°.
  - 2 tapered blocks, half-thickness 0.045 → 0.02.
  - FIN_IN inner panel plus the 3-step leading edge.
  - Slightly concave trailing edge.
- **Caudal (heterocercal crescent):**
  - Upper lobe curves to (y 1.34, z+0.60). Lower lobe goes to (y 1.16, z-0.22), about 55% of the upper.
  - Build both lobes as curved strips between two arcs (CelestialDragon crescent, `pets/CelestialDragon.py`
    L288-309) on the new **Tail4** bone, with a studded root block.
  - Add a small subterminal notch near the upper tip and one bite notch in the upper lobe.
  - 3-step coral on both leading edges.
- **Small fins:**
  - 2nd dorsal and anal: keep them, STEEL with CORAL_D tips.
  - Pelvic fins move onto Tail1, or entirely in front of y 0.28 (rig item D).
  - Add **ARMOR peduncle keels** on Tail3: lateral keels, 0.12 long, 0.03 thick. They read "fast predator" from
    the game camera.

### 2.6 Gills and scars
- **Gills:**
  - 5 per side on the Chest flank at y -0.70..-0.46, spaced 0.06, crossing the countershading line.
  - Heights 0.20/0.21/0.20/0.18/0.15 (the rear ones shorter).
  - Each slit is a slight backward curve built from 2 bars: a MOUTH slit (0.02) plus a CORAL flap behind it (0.03),
    tapered at both ends (top=(1, 0.3)).
  - Optional: put the flaps on Gill_L/R bones for the gill pump (rig item I).
- **Scars:**
  - Delete the 6 pale paired bars (L49-53).
  - Replace them with **left-side-only** (asymmetric) 3 tapered claw gouges in SCAR, curving across lames 2-3.
    Use `crack()` (`pets/ThunderRex.py` L85-90) with tapered ends.
  - Together with the fin notches and the broken tooth, that is enough battle damage. Don't add more specks.

### 2.7 Detail density (budget: v1 3.3k → v2 **9-12k**, hard cap 15k)
| area | rough tris |
|---|---|
| body sections, lames with teeth, seams, keel, belly | ~3.5k |
| war-hammer: blocks, helm, rim, lobes, eyes, brows, spikes, nostrils | ~2.0k |
| jaw, 26 teeth, mouth plates | ~1.2k |
| fins: stacked blocks, coral edges, crescent strips, notches, keels | ~2.5k |
| gills (10 x 2 parts), scars, misc | ~0.8k |

- **Studded:** ARMOR, STEEL, FIN_IN and BELLY blocks.
- **Smooth** (`nostud=True` or role "detail"): all coral, teeth, eyes, scars and mouth parts.
- No detail under 0.02. Seat every plate, keel and fin root on the real surface with `surf_hit`
  (`pets/ThunderRex.py` L93-109), so nothing floats.

### 2.8 What to copy, and from where
| what | file | lines | use it for |
|---|---|---|---|
| `prof` / `shell` / `side_pt` / `fpt` | pets/ThunderRex.py | L47-82 | armour lames over the tapered body blocks |
| shell loop, jagged teeth, seam bands, cracks | pets/ThunderRex.py | L196-214 | the war-back (2.3) |
| `crack` | pets/ThunderRex.py | L85-90 | tapered claw-gouge scars |
| `surf_hit` | pets/ThunderRex.py | L93-109 | seating the keel, lames, fin roots and helm rim |
| `fierce_eye` (add colour params) | pets/ThunderRex.py / pets/Ivonrath.py | L112-126 / L93-110 | hammer-tip eyes and brows |
| `shard` (colour-step logic) | pets/ThunderRex.py | L129-157 | 3-step coral fin edges |
| teeth outside the lip, MOUTH roof/floor | pets/ThunderRex.py | L234-251 | jaw (2.2) |
| tail shells, belly, joint bands | pets/ThunderRex.py | L327-345 | tail rings on Tail1-3 |
| anchors via module globals (`CORE`, `RIDGE_TIPS`) | pets/ThunderRex.py | L37-39, L185, L371 | Slam / Mouth / Wake anchors |
| `seat_plate`, `surf_strip` | pets/Ivonrath.py | L62-90 | coral helm rim, keel strips |
| `crest` (two-part blade) | pets/Ivonrath.py | L112-124 | stacked dorsal blocks |
| membrane edge bars + 2-tone membrane | pets/Ivonrath.py | L131-156 | pectoral/caudal edges, FIN_IN panel |
| `spike2` (two-tone, buried root) | pets/MoltenBoar.py | L78-88 | brow spikes |
| `band` / `seam` | pets/LavaGolem.py | L82-91 | seam bands |
| crescent strip between two arcs | pets/CelestialDragon.py | L288-309 | curved caudal lobes, falcate dorsal outline |
| side-facing slit eye with a lower lid and brow | pets/Kraken.py | L118-133 | fallback eye construction for the lobes |
| `ground_lift` (floor solve) | pets/Kraken.py | L214-240 | head-contact solve for the act |
| `fins()`, hover-bob idle | pets/Kraken.py | L259-273 | Fin_L/R keying, bob values |
| `chain()` travelling wave | ../PetsV2/pets/_common.py | L34-40 | the carangiform S-wave |
| bulk + stepped thick fins | _refs/fierce/f_63 (Orca) | - | mass and fin build only. Not its colours (secret's) |

---------------------------------------------------------------------------------------------------------------------
## 3. v2 checklist (each item pass/fail; all must pass)

1. **Lineup:**
   - model_tq next to Kappa, SeaTurtleWarrior and Kraken at the same scale.
   - It is clearly the most finished and striking Tide pet.
   - A fresh viewer says "shark" or "hammerhead", never "plane" or "jet".
   - It does not read as a Thunder Rex palette.
2. **64 px test** on slate, with an outline (the `icon3.py` pipeline): you can name three things. Hammer (T) head,
   teeth/jaw, and coral eyes or coral-seamed armour.
3. **Game camera:**
   - The hammer is the widest element (span ≥ pectorals + 0.10).
   - The dark lames with coral seams read as segmented armour.
   - The coral-rimmed helm and the brow spikes frame the T.
4. **Value blocking (side view):**
   - ARMOR 28-35%, STEEL 30-40%, BELLY ≥12%, coral family 9-14%. No colour over 45%.
   - In the game view, ARMOR ≥30% and coral ≥8%.
   - Re-measure with the same method as the table above.
5. **Silhouette:**
   - L:H ≤ 2.2:1 in the side render.
   - The dorsal tip is the highest point.
   - The caudal upper lobe is ≥1.8x the lower.
   - No section step > 0.02.
   - ≥2 bite notches show in the silhouette.
   - No neck.
6. **Face:**
   - In front and tq, both coral eyes are visible at the hammer tips under brow overhangs.
   - The crescent mouth rests 10° open, with dark interior, upper teeth outside the lower lip and two rows visible.
   - No dark visor band. No nostril dashes on the front face.
7. **Fins:**
   - No fin is a single flat sheet.
   - Each has a studded root, a thickness taper (≥0.06 at the root → ≤0.03 at the tip), a 3-step coral leading edge
     and a curved (falcate) outline.
8. **Hard rules:**
   - Studs on ARMOR, STEEL, FIN_IN and BELLY; coral, teeth, eyes and scars smooth.
   - No Neon or glow. Tris ≤15k (target 9-12k).
   - Nothing floats; no detail under 0.02.
   - H_MODEL = the real top.
9. **Family and egg fit:**
   - fierce_eye construction; same stud world size (PITCH formula).
   - STEEL's brightest channel ≥170.
   - No gold, and no black/white orca blocking.
10. **Rig readiness:** see section 4, items A-H. In particular, a test pose (Spine +22, Chest +10, Head +8) with
    the hammer's lowest vertex at 0.005 shows **the hammer edge as the lowest point, the jaw ≥0.03 above the
    ground and the pectorals above the ground.**
11. **Deliverables:**
    - model sheet (tq at 600)
    - face close sheet (front / side / tq)
    - game-camera render
    - the slam contact test render
    - a 64/128 px icon strip with Kappa / SeaTurtleWarrior / Kraken through `icon3.py`

---------------------------------------------------------------------------------------------------------------------
## 4. Rig concerns and animation notes

### Rig: fix these in rig() and model() before animating
- **A. Add `Tail4`, the caudal fin bone.**
  - Today the whole caudal sits on Tail3, so it cannot lag or flick, and a carangiform wave needs that last lag.
  - New layout: Tail3 = the peduncle (y ~0.92 → 1.04, carrying the keels); Tail4 = the caudal fin.
- **B. Head pivot at the throat, inside the body.**
  - v1 has (0, -0.80, z+0.02) at the head/body seam, with only 0.06 overlap (core rear -0.78 vs chest front -0.84).
    Any pitch opens a gap or drives the core's rear-top into lame 1.
  - Move the pivot to **(0, -0.74, z-0.05)** and bury the core 0.10.
  - Limits: Head vs Chest ±12° pitch, ±6° yaw. Do big moves with Spine and Chest (a shark has no neck).
- **C. The dorsal straddles the Chest pivot.**
  - Its root runs y -0.30..0.08 on the Spine bone, with the Chest pivot at -0.22. Its front root sits inside
    Chest's plate and shears on every Chest yaw.
  - Fix: keep the root behind y -0.16 (as in 2.5), or skin the whole fin to Chest.
- **D. The pelvic fins straddle Spine/Tail1.** Their rear points (y 0.38-0.40) are past the 0.32 joint. Move them
  onto Tail1, or entirely in front of 0.28.
- **E. Telescoping sections.**
  - Each rear body section's front end is buried ≥0.08 inside the front section, with a slightly smaller
    cross-section.
  - The lames (owned by the front bone) overhang each joint.
  - Result: no flank gaps at ±10° per joint.
- **F. Pectoral pivots.**
  - Fin_L/R sits at the root's front end (y -0.48) of a 0.28 chord. A 25° trim swings the rear root corner ~0.12
    out of the body.
  - Use the 0.22 chord, put the pivot at its middle (y ~-0.35), and add a studded Chest fairing over the root.
- **G. Mouth.** Add the MOUTH roof and floor (2.2). The Jaw pivot at the mouth corner, (0, -0.80, z-0.10), is fine.
- **H. Hammer-first contact. This blocks the signature act.**
  - In v1 the jaw bottom (z-0.21) is **0.255 below** the hammer bottom (z+0.045) and only **0.11 behind** its
    front edge. So the jaw hits the ground first at any nose-down angle under ~67°.
  - With the 2.2 numbers (Δy ≥0.21, Δz ≤0.13), the hammer leads from ~32°. The strike uses ~40° in total, which
    leaves the jaw ~0.035 clear.
  - Make the checklist-10 test render before animating.
- **I. Optional: `Gill_L/R`** (children of Chest) carrying the 5 coral flaps, for the gill pump. If you skip
  them, replace the gill pump with a jaw "breath" (see idle).
- **J. Anchors** (empty bones, like Rex's):
  - `Mouth`: bubbles / roar
  - `Slam`: under the hammer centre at contact; sand burst and shock ring
  - `Wake`: caudal tip; water trail
  - `DorsalTip`: spray when swimming
  - Record their positions in model() through module globals, the Rex way.
- **K. check_pairs.**
  - Keep v1's.
  - Add (`Fin_L/R`, `Tail1`), (`Fin_L/R`, `Tail2`) for the roar's dropped pectorals.
  - Add (`Tail4`, `Fin_L/R`) and (`Jaw`, `Chest`) for the wide gape.

**Pose limits:**
- Head vs Chest: ±12° pitch, ±6° yaw.
- Chest vs Spine: ±12° pitch, ±5° yaw.
- Each tail joint: ±12° yaw, with the caudal at ≤ ±35° cumulative.
- Fins: tips up ≤25°, down ≤40°.
- Jaw: 0-40°.

**No head shakes, shark edition** (the owner's rule; the wide hammer magnifies any yaw):
- **Head world yaw ≤ ±3° in any looping motion.**
- **No** hammerhead "metal-detector" side-to-side sweep.
- **No** feeding head-shake in the bite.
- A look-around is **one** slow turn (≥20 f) and back, at most once per loop.
- No body roll in the roar hold. A rolling hammer reads as a head wobble.

(+ pitch = nose-down. On the tail bones, + lifts the tail and - lowers it.)

### idle (120 f, loop): "PATROL HOVER"
- **Hover:**
  - Spine z 0.03 + 0.025 bob (1 cycle per loop). Pitch +3 (nose-down hunting posture) ±1.5.
  - It is never dead level.
- **Lazy S-wave:**
  - `cm.chain` on Tail1-4, sway 3 (relative), 2 cycles per loop, lag 0.12. That is about 40% of the swim.
  - Chest counter-yaws ∓1, and the Head cancels the rest, so the world head yaw stays ≤ ±1.5°.
- **Fin trims:** pectorals at L +6 / R -4 for f0-60, then eased and swapped for f60-120 (balancing), plus a ±2
  flutter.
- **Gill pump:** every 30 f the flaps open 8° over 6 f and close over 12 f. Without gill bones: a jaw breath of
  10 → 16 → 10° every 60 f.
- **One slow banked glance:** f70-100, roll 8° plus Head yaw 10 (a single turn, eased), back by f110.
- **Teeth flash:** the jaw goes 10 → 18 → 10 at f40-52.
- This is distinct from the Kraken idle (bob + arm-ring wave) and from Rex's look-around.

### swim (32 f, loop): CARANGIFORM S-WAVE
- **Travelling wave:**
  - Relative yaw per bone: Spine ±2, Tail1 ±6, Tail2 ±9, Tail3 ±10, Tail4 ±9, lag 0.12 cycle per bone.
  - Cumulative caudal angle about ±30-35°; tail tip lateral excursion about ±0.25.
  - The front two-thirds stay nearly rigid. That is what makes it read "shark" rather than "eel".
- Chest counter-yaws ∓1.5. **Head world yaw ≤ ±2°.**
- **Thrust:** Spine loc y ±0.012 and z ±0.01 at twice the stroke frequency (one pulse per tail stroke). Tail4 rolls
  ±5° on each stroke reversal, so the fin twists.
- **Pectorals:** held at ~10° down (planing) with ±2 trims. **They never flap**, which would read as a bird or a
  plane. The dorsal stays stiff.
- Body pitch +3. This is distinct from the Kraken's jet contraction swim.

### roar (66 f): "THREAT DISPLAY"
Use the real grey-reef-shark agonistic display, not a Kraken-style rise. It stays low.

| f | beat | keys |
|---|---|---|
| 0-10 | gather | Spine z -0.05, pitch +4; Head +4; pectoral tips up 10; jaw 6 |
| 10-20 | display | Spine +6, Chest -6 (the back hunches into a hump); Head -10 (snout up; Head+Chest 16); Tail1-2 -6/-6 (tail droops); **pectorals DROP to 38° down**; jaw 0 → 38 by f20 (ease in, hard stop); event `roar` f18 |
| 20-46 | hold | jaw buzz ±3 every 3 f; Tail3/Tail4 shiver ±8 at ~3 Hz (tail only); gill flaps held 10 open; body still, no roll |
| 46-52 | snap | jaw 38 → 0 by f50 (hard stop); event `snap` f50 |
| 52-66 | settle | back to rest; the pectorals overshoot 4° up, then settle |

The roster already has a "hiss (arched back)". This display owns its own read: dropped pectorals, snout-up gape and
tail shiver.

### act_hammerslam (~104 f): "STINGRAY PIN"
This is the real great-hammerhead hunt: one strike, then a pin, a pivot and a bite. **The pin and the pivot are the
signature; the slam is one beat of it.** That is what keeps it apart from Kraken's ship-crusher drum slams,
SeaTurtleWarrior's trident twirl + slam and LavaGolem's ground pound, two of which are in this egg.

| f | beat | keys |
|---|---|---|
| 0-14 | spot | slows down; Spine +8, Head +6 (looks at the ground); pectoral tips up 15 (brake); the tail sway decays; event `spot` f8 |
| 14-28 | rear up | Spine -8, Chest -8, Head -10 (26° up in total, ≤30); Spine z +0.10; tail follows (-4); pectorals up 20; jaw shut; 4-frame hang f24-28 |
| 28-34 | **strike** | 6 frames, ease in, **hard stop**: Spine +22, Chest +10, Head +8 (~40° at the hammer); Spine z solved so that the hammer's lowest vertex = 0.005 at f33; Tail1-3 -6/-8/-10 (counter-curl: the Spine tilt lifts the tail, this bends it back down so the tip stays ≤ ~1.75 world); Tail4 flick; pectoral tips up 25 to clear the ground; event `slam` f33 |
| 33-38 | impact | Chest overshoot +2 and back by f35; pectorals slap down 10; tail-tip shiver ±6 |
| 38-70 | **pin and pivot** | the hammer contact point is **PINNED** (≤0.01 slide; re-solve Spine loc every frame); the body pivots around it, Spine yaw 0 → +20 over f38-54, then holds; 2 press pulses at f46 and f58: Chest +3 plus a strong Tail2-4 stroke ±14; jaw shut; event `pin` f40 |
| 70-80 | bite | the head lifts 0.06 (Chest -6); jaw 0 → 34 at f74, then **one** snap shut at f78 (hard stop) over the pinned spot; event `bite` f78; no shaking |
| 80-104 | release | yaw back to 0; pitch back up; glides back 0.10 and rises to the hover; one recovery stroke; pectorals flare 12 → 0; **ends exactly in the rest pose** |

- **Contact solve:** write `head_contact(k, frames, z=0.005)` on the pattern of Kraken's `ground_lift` (L214-240).
  - Measure the min z of the Head vertex group, key Spine z so it touches on the pin frames, and keep the global
    floor (`ground_min_z` ≥ -0.02) on every frame.
  - The pectorals, jaw and dorsal must never touch the ground.
- **Footprint:** the pivot yaw is ≤20°, so the tail tip swings ≤ ~0.85 units sideways (about 5 studs at x1).
  - Do not go bigger. Rex review 3 rejected a sweeping tail through the owner's avatar.
- **Return:** a pose sheet at f24, f33, f46, f60, f74, f78 and f96, plus the collision and audit pass.

**For all clips:** 0 collisions at step 1, `ground_min_z` ≥ -0.02, audit linear 0, idle and swim loops closed, and
acts that play in place and end in the rest pose.
