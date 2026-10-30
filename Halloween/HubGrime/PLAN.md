# HUB GRIME: builder plan (2026-10-13)

Status: **PLAN ONLY. Waiting for approval.** No textures have been generated yet.

What I read first:
- `HubGrime\BRIEF.md` and `Halloween\AGENT_BRIEF.md`.
- The style references `review_head_front.png`, `PumpkinEggs\review_day_25studs.png`, `Graveyard\review_25studs.png` +
  `review_close_Grave_A.png` + `REVIEW.md`, and `TPTrees\review_hi_tree_25studs.png`.
- `hkit.py`.
- The real in-game look of the hub (`previews\night\DAY_original_restored.jpg` and `A_Moonlit.jpg`, both from
  2026-10-13).

Read-only environment checks:
- System Python 3.12.10 has numpy 2.5.3 and Pillow 12.3.0. scipy is not installed, so I write my own blur and distance
  helpers in numpy.
- Headless Blender 5.2.2 LTS starts. Its numpy is 2.3.4 and it has no PIL.

---

## 1. The approach in one paragraph

The textures are made with **numpy + PIL (system Python)**, as 2D vector-like shapes:
- **Cracks** are signed-distance fields of jagged polylines whose width varies along their length.
- **Moss and slime** are metaball height fields, shaded with a fake light.
- **Stains** are domain-warped blobs with tide lines.

Each texture is composited in linear light and drawn at 2-3x size, then box-downsampled for clean anti-aliasing. It is
exported as **straight-alpha RGBA PNG**. The RGB under transparent pixels is filled by **push-pull colour bleeding**,
so mips and bilinear filtering can never pull in black or white.

**Headless Blender (Eevee)** is used only for the lit **preview renders**:
- a studded floor mock and a studded wall mock, built exactly like Roblox draws them (flat plastic with a 1-stud stud
  normal/AO texture);
- each decal on its own transparent carrier plane, 0.03-0.05 above the surface;
- lighting calibrated against the real in-game screenshots.

PIL also makes the 2D check sheets (swatches, fringe test, seam test).

**Why not bake Blender procedural shaders?** These are 2D decals with no normal map (a Roblox Decal is colour + alpha
only), so all the shape and shading has to be painted into RGBA. numpy gives me:
- exact control of the alpha and of the colour under the transparent pixels;
- exactly periodic noise for the seamless MossBase;
- crisp analytic edges;
- deterministic seeds and fast iteration.

**Fallback, only if the moss cushions look flat in the previews:** render a displaced metaball moss mesh top-down in
Blender (ortho, Cycles, transparent film, AO). It would then be composited through the same numpy alpha pipeline.

---

## 2. Facts this plan is built on

| Fact | Consequence |
|---|---|
| Floor green (128,170,96) = L\*65. Wall blue (96,132,170) = L\*54. Cream (222,205,170) = L\*83. | The darks must sit near L\*10-25 to read as cracks on all three. The moss body sits at L\*20-50: darker and yellower than the floor green. |
| In-game the hub renders bright and hazy. Measured from `DAY_original_restored.jpg`: the green floor is about (176,221,160) and the cream plaza about (245,237,226), almost white. At night (Moonlit) green is about (93,159,88) and cream about (184,177,185). | Contrast gets lifted by the haze, so low-alpha stains must not be too faint on green and blue. On cream they pop much harder, so NOTES gives cream its own transparency rule. The preview lighting is **calibrated to these numbers** (section 7.3). |
| A Decal is colour + alpha, lit like the surface, with no normal map or gloss. | Every bevel, cushion and gloss highlight is painted, with one consistent fake light. |
| Studs are a flat surface texture (`SurfaceType.Studs`), not geometry. Decals sit on a carrier 0.03-0.05 above. | Opaque pixels hide the studs and transparent ones show them. I use this on purpose (the "stud logic" in section 4). |
| A decal stretches over the carrier face. | Each PNG has the same aspect as its intended size in studs, so the lead sizes the carrier 1:1. |
| Roblox max texture side is 1024, compressed (BC3 / ASTC), mipmapped from straight-alpha data. | Every texture is ≤ 1024. The colour under alpha is bled (no fringes in mips). The soft alpha ramps are dithered against compression banding. |
| Floor decals seen from eye height 5 at 25 studs are foreshortened about 5x vertically. | Floor features are drawn **bolder** than wall features: wider crack cores and big chips. They are tested at eye height and at the third-person camera. |
| The owner rejected a global lighting retune as "very ugly". | The decals don't touch Lighting. The previews use the restored original lighting look (warm, hazy) and the picked "A Moonlit" night. Every key view also gets a **before/after** pair. |

---

## 3. Palette (sRGB 0-255)

### Opaque colours (cover the studs)
| Key | RGB | Use |
|---|---|---|
| D1 crack core | (32, 30, 22) | deepest part of a crack or hole; a warm umber-olive, never pure black |
| D2 crack inner wall | (66, 60, 42) | the lit inner wall of a wide crack or hole, giving depth |
| M1 moss underside | (40, 56, 28) | cushion bases, crevices between clumps |
| M2 moss body | (78, 98, 40) | olive body |
| M3 moss lit | (112, 130, 52) | lit tops |
| M4 moss tips | (166, 182, 72) | yellow-green tips, only on lit high points (a minority) |
| M5 tip sparks | (196, 204, 98) | a few brightest tips |
| G1 / G2 / G3 dead grass | (178,156,98) / (122,112,66) / (70,62,40) | straw sprigs in a few cracks, matching the graveyard dead grass |
| S1 slime deep | (44, 98, 20) | slime edges, thin parts |
| S2 slime body | (118, 192, 34) | lime body |
| S3 slime light | (170, 226, 70) | lit lobes |
| S4 slime gloss | (236, 255, 190) | painted specular blobs and rim lights (not emissive) |
| S5 slime outline | (30, 62, 16) | a thin crisp edge, alpha 0.7-1 |

### Glazes (semi-transparent, adopt the base hue, keep the studs visible)
| Key | RGB | Alpha | Use |
|---|---|---|---|
| W1 damp | (42, 46, 30) | 0.15-0.40 | stains, damp bands, moss halos |
| W2 tide line | (34, 36, 24) | 0.40-0.55 | the darker edge of a dried watermark |
| W3 mud | (62, 48, 32) | 0.30-0.55 | G_Stain_B, some crack surrounds |
| W4 shadow | (30, 34, 24) | 0.25-0.50 | the shadow lip of a bevel, contact shadows |
| W5 bevel light | (238, 232, 205) | 0.25-0.45 | the lit chipped lip; lightens the base in its own hue |
| W6 chip face | (210, 200, 168) | 0.20-0.35 | exposed "broken plastic" inside a shallow chip |
| W7 slime contact | (24, 40, 16) | 0.25-0.40 | the soft shadow ring around slime |

### Why it reads on green, blue and cream (CIE76 ΔE, checked numerically)
| Colour | vs green | vs blue | vs cream |
|---|---|---|---|
| D1 crack core | 66 | 52 | 73 |
| M2 moss body | 28 | 58 | 49 |
| M4 moss tips | 21 | 81 | 41 |
| S2 slime body | 37 | 101 | 66 |
| W1 at 0.30 (linear blend) | 10 | 8 | 11 |
| W2 at 0.50 | 18 | 15 | 20 |
| W5 at 0.35 | 21 | 26 | 4 |

- **Darks:** tinted umber-olive. They read as dirt or a hole on every base, and none is black or grey. On blue they add
  a warm "dirty" contrast, not a cold hole.
- **Glazes:** a translucent dark or light colour mixes with the surface under it. A stain on green becomes darker
  green, and on blue darker blue. The same PNG is correct on every surface, and the studs stay visible through it
  ("on the plastic").
  - The bevel light (W5) disappears on cream (ΔE 4). That is fine: the crack still reads from its dark core.
- **Moss:** reads on green by **value and hue**, not by being green:
  - the body (M1/M2) is clearly darker and yellower than the floor;
  - a soft W1 damp halo separates it from the floor;
  - the yellow tips (M4) are kept to a minority, because tips alone are close to the floor (ΔE 21).
  - On blue it pops strongly.
- **Slime on green** is the weakest pair (ΔE 37). It gets value structure: the S5 dark outline, the W7 contact shadow,
  and the bright S4 highlights. NOTES favours cream and plaza edges for slime.
- **Robustness:** I also checked an orange swatch (230,150,105) (section 11, open questions). Every key colour has
  ΔE ≥ 48 there.
- **Family:** the palette is in the same family as the HQ props: the graveyard's olive moss with yellow-green specks,
  the straw dead grass, and the warm stone. It is not a new style.

---

## 4. Shared drawing rules

### Stud logic
- **Things that sit on the surface** (moss, slime, crack holes) are **opaque** and hide the studs.
- **Things that are in the surface** (stains, damp, bevel light/shadow, chip faces) are **glazes**, so the studs show
  through.
- **Chunks of broken slab** (G_Crack_C) are left **transparent inside**. Only their gap lines and bevels are painted,
  so a chunk is literally the real studded surface, on green, cream or brown alike.

### One fake light per surface
| Surface | Light vector (texture space, −y = texture top) | Notes |
|---|---|---|
| Wall | L = (−0.2, −0.75, 0.63) | from above, slightly left. On a groove the **lower lip is lit** (W5) and the upper lip is in shadow (W4). Inside wide cracks the lower inner wall gets D2 and the upper part gets D1. |
| Floor | L = (−0.25, −0.45, 0.86) | mostly from overhead, so the bevel asymmetry is ≤ 30 %, and a floor decal can take any yaw without looking wrongly lit. NOTES: optionally point the texture top roughly toward the sun azimuth. |

Moss cushions and slime are shaded from their height field with the same light: wrap-Lambert plus a cavity term.

### Scale rules (studs)
| Feature | Floor | Wall |
|---|---|---|
| Main crack core, at its widest | 0.22-0.45 | 0.15-0.35 |
| Crack tips (hairline) | taper to 0.04-0.06 | taper to 0.04-0.06 |
| Bevel band | 0.06-0.12 each side | 0.06-0.12 each side |
| Spalls (chipped-off lens areas) | 0.4-1.0 | 0.4-1.0 |

- **Floor cracks are bolder** because of foreshortening.
- **Moss:**
  - cushions 0.4-2.5 studs;
  - micro-clumps 0.08-0.2 studs, the smallest shaded feature (at least 6 px);
  - satellites 0.15-0.6 studs.
- **Nothing is noise for its own sake.** Noise is used only to warp shapes and to place clumps, never as a grainy
  surface fill.
  - **Frequency budget:** no painted feature is smaller than about 0.08 stud, except anti-aliasing.
  - **Thumbnail test:** at 1/8 size, every texture must still read as what it is.

### Alpha pipeline (identical for all 14 textures)
1. **Draw.** Each element is drawn at **2x** size (3x for crack line work) as premultiplied linear RGBA layers and
   composited with the correct "over" operator.
2. **Downsample.** Box-downsample the premultiplied data to the target size, which gives analytic anti-aliasing.
3. **Clean.** Alpha < 2/255 becomes 0, so there is no invisible fog over the carrier rectangle.
4. **Border.** The outer 3 px border is alpha 0 everywhere, except on edges that must touch something:
   - the MossBase bottom row and left/right edges;
   - the W_Drip top row;
   - the W_Crack_C bottom row.
5. **Un-premultiply** to straight alpha, then convert linear to sRGB.
6. **Bleed.** Push-pull colour bleed: an alpha-weighted mip pyramid down, then fill the transparent texels from the
   coarser levels on the way up. Every alpha-0 texel then carries the colour of the nearest visible content. There are
   no black or white fringes even when Roblox builds naive straight-alpha mips.
7. **Dither.** Add a ±0.5 LSB triangular dither on the soft alpha ramps (stains, damp, halos) against 8-bit and BC3
   banding.
8. **Save.** PIL RGBA PNG, 8 bit, no ICC or gamma chunk.

Edge character:

| Element | Edge |
|---|---|
| Crack cores | crisp, 1-1.5 px anti-aliasing |
| Bevel glazes | soft over the bevel band |
| Moss cushions | crisp 2 px outline, with a soft W1 damp halo (0.3-0.6 stud) |
| Stains | soft feather 0.2-0.4 stud, but a readable tide line |
| Slime | crisp outline + soft contact ring |
| Damp streaks | soft sides, crisp-ish rounded ends |

---

## 5. The textures

All are PNG RGBA straight alpha, in `HubGrime\decals\`. Every size is a multiple of 4, for 4x4 compression blocks.

| Name | Intended size (studs, W x H) | Pixels | px / stud |
|---|---|---|---|
| G_Crack_A | 14 x 7 | 1024 x 512 | 73 |
| G_Crack_B | 10 x 10 | 768 x 768 | 77 |
| G_Crack_C | 12 x 8 | 960 x 640 | 80 |
| G_Moss_A | 8 x 8 | 576 x 576 | 72 |
| G_Moss_B | 10 x 6 | 720 x 432 | 72 |
| G_Stain_A | 10 x 10 | 512 x 512 | 51 (soft, low frequency) |
| G_Stain_B | 12 x 8 | 576 x 384 | 48 (soft) |
| G_Slime_A | 5 x 5 | 512 x 512 | 102 (crisp gloss) |
| W_Crack_A | 5 x 10 | 384 x 768 | 77 |
| W_Crack_B | 8 x 10 | 608 x 760 | 76 |
| W_Crack_C | 6 x 12 | 448 x 896 | 75 |
| W_MossBase_A | 24 x 6 | 1024 x 256 | 42.7 (the 1024 cap) |
| W_MossBase_B | 24 x 6 | 1024 x 256 | 42.7 |
| W_Drip_A | 4 x 11 | 320 x 880 | 80 |
| W_Drip_B | 4 x 8 | 320 x 640 | 80 |

**GPU memory:** 14 unique textures at roughly 0.3-1.3 MB each once compressed with mips, about 10 MB in total.

### Floor (G_)

**G_Crack_A: long branching (14 x 7)**
- **Alpha:** the core is opaque D1/D2; the bevels, chip faces and halo are glazes; the moss and grass are opaque.
- **Main fracture:**
  - about 12 studs along the long axis, as an angular zigzag (a kink every 0.6-1.5 studs, ±25°);
  - widest in the middle third (0.4 stud), tapering to a hairline at both ends.
- **Branches:** 3-5 branches of 2-4 studs leave at 25-55°, and one of them has a sub-branch.
- **Spalls:** 2 lens-shaped spalls (0.6-1.0 stud) along the widest part. Each has a W6 chip face, a W5 lit lip and a W4
  shadow lip.
- **Growth:**
  - 2-3 small moss cushions (0.3-0.5 stud) wedged in the widest gap;
  - 2 short dead-grass sprigs at one junction;
  - 3-4 loose chips nearby, each with a highlight top and a contact shadow.
- **Dirt halo:** a faint W1 halo along the core, ≤ 0.25 stud, so it doesn't look like a clean pen line.

**G_Crack_B: star burst (10 x 10)**
- **Impact crater:** about 1.4 studs, a sunken disc:
  - W4 glaze, with a D2 inner wall on its lit side;
  - a broken rim with 2-3 chunks missing (D1 pockets);
  - a small moss cushion in the bottom.
- **Rays:** 6-8 radial cracks (2-4.5 studs) with a slight curve and zigzag.
- **Rings:** 1-2 partial concentric arc cracks linking the rays. This classic spider-web fracture is what reads as an
  "impact" at distance.
- **Chips** at the roots of the rays.
- **Alpha:** as in A. The crater floor is a glaze (studs faintly visible, "sunken") and its pockets are opaque.

**G_Crack_C: split with chunks (12 x 8)**
- **The band:** two roughly parallel main cracks, 0.6-1.2 studs apart, make a broken band. Cross cracks split the band
  into 3-5 slab chunks.
- **Chunks are transparent islands** (stud logic):
  - one chunk is **missing**: an opaque D1-to-D2 hole with a depth gradient, and moss plus a dead-grass sprig at its
    bottom;
  - one chunk is **tilted**: a half W4 glaze, with a W5 lit edge on the raised side.
- **Rubble:** 4-6 rubble pebbles beside the band.
- **Ends:** the outer cracks continue as single tapering cracks to the ends of the texture.

**G_Moss_A: round damp moss patch (8 x 8)**
- **Damp base:** an irregular W1 base (about 6.5 studs) with a W2 tide line.
- **Main group:** 3-5 overlapping cushions (1-2.5 studs), built from a metaball dome plus micro-clump domes. The
  colour ramp follows height and light: M1 → M2 → M3, and M4/M5 only on the lit high points.
- **Satellites:** 6-12 cushions (0.15-0.6 stud), thinning out with distance.
- **Crack:** one short hairline crack runs out of the patch.
- **Alpha:** the cushions are opaque with a crisp 2 px outline and an M1 underside rim. The halo and the base are
  glazes.

**G_Moss_B: moss along a joint (10 x 6)**
- **Main run:** a chain of cushions along a gentle S-curve (a hidden joint), thickest in the middle.
- **Around it:** a W1 damp band under the chain, a few satellites, and one dead-grass sprig.
- **Purpose:** it gives a linear variant to break up the round patches.

**G_Stain_A: watermark puddle (10 x 10)**
- **Shape:** a lobed outline from a domain-warped circle (low-frequency warp only).
- **Interior:** W1 at alpha 0.25-0.32, a little darker toward the centre.
- **Edges:**
  - a W2 tide line at the edge (0.12 stud, alpha about 0.5);
  - 1-2 faint inner tide rings (offset contours of the field);
  - a soft 0.3-stud outer feather.
- **No grain.**

**G_Stain_B: mud drag (12 x 8)**
- **Shape:** an elongated irregular W3 mud stain with a denser core and a tide line.
- **Splatter:** 5-10 drop satellites, all on one side.
- **Dried edges:** 2 tiny cracked-mud lines in the densest part.
- **Colour:** warmer than A, so the two stains don't look like copies.

**G_Slime_A: slime puddle (5 x 5)**
- **Shape:** a main puddle (about 3.2 studs) with 3-4 lobes, plus 3-5 droplets. It is a metaball height field with a
  flat top and rounded edges.
- **Shading:**
  - S2 body and S3 on the lit lobes;
  - S1 toward the thin edges, which are slightly translucent (alpha 0.85);
  - an S5 outline on the shadow side;
  - S4 painted highlights: one crisp main highlight per lobe, offset toward the light, a thin rim light on the lit
    edge, and 2-3 bubbles with highlights.
- **Contact ring:** a W7 ring (0.15-0.3 stud).
- **No emissive** (the owner's rule). The gloss is painted only.

### Wall (W_): texture top = up

**W_Crack_A: vertical (5 x 10)**
- **Fracture:** a vertical zigzag with 2-3 short branches and hairline ends.
- **Mid spall:** about 0.8 stud, with the lit lower lip.
- **Ledge:** one tiny moss tuft on a ledge in the lower third.

**W_Crack_B: diagonal (8 x 10)**
- **Fracture:** a diagonal from the upper right to the lower left, with angular kinks.
- **Fan:** a branch fan at the upper end.
- **Missing corner:** a chipped-off corner piece in the middle, as an opaque D1/D2 recess with depth shading.

**W_Crack_C: from the floor up (6 x 12)**
- **Base:** opens at the bottom edge (0.5 stud wide), with a broken triangular notch (about 1.5 studs) missing at the
  base.
- **Fork:** it forks at about 4 studs, and one fork reaches about 10 studs, ending in hairlines.
- **Growth:** moss cushions sit in the notch and creep 1-2 studs up the crack, with W1 damp darkening around the foot.
- **Bottom row:** opaque, so it meets the floor and pairs with MossBase.

**W_MossBase_A: "mossy" (24 x 6)**
- **Damp band:** a W1 band rising from the base, 1.5-3 studs, with a wavy W2 tide line.
- **Moss along the base:** a continuous run, 0.4-1.6 studs tall, with bigger cushions every 3-6 studs (up to 2.5 tall).
- **Creeping tongues:** 2 tongues climb to 4-4.5 studs and break up into patches upward. A few spores reach up to
  5 studs.
- **The fade upward comes from density and size, not from blurring the moss.** Only the damp glaze fades by alpha.
- **Edges:**
  - the bottom row is opaque, so the moss meets the floor;
  - the top 0.3 stud is fully transparent.

**W_MossBase_B: "damp" (24 x 6)**
- **Damp:** taller rising damp: a W1 band with 2 darker "wicking" plumes reaching 4-5 studs, each with stacked tide
  lines.
- **Moss:** thinner, lower and gappier along the base, with a few dead-grass blades.
- **Pairing:** A is the mossy one and B the damp one, so alternating them gives a natural rhythm.

**W_Drip_A: dark damp streaks (4 x 11)**
- **Source:** a soft dark seep band at the top, under the trim, with 2-3 tiny moss tufts.
- **Streaks:** 3-5 streaks (3-10 studs long) that narrow downward:
  - W1 at alpha 0.2-0.4;
  - W2 tide edges along their sides;
  - a slightly darker dried end at the bottom.
- **Top row:** opaque-ish (alpha ≥ 0.6) so it tucks under the trim. The rest is glaze.

**W_Drip_B: slime drips (4 x 8)**
- **Goo band:** 0.5-0.8 stud at the top, with a wavy lower edge.
- **Drips:** 4-6, between 1 and 7 studs long. Each is a tapering tube ending in a teardrop bulb, and one detached drop
  sits below.
- **Shading:**
  - cylinder shading across each drip: a lit left-edge highlight streak and a darker right edge;
  - S4 gloss streaks;
  - an S5 outline.
- **Trail:** a faint W1 trail below the longest drip, as if it dripped there before.
- **Style:** the same stylized-realistic language as the candle wax drips in `PumpkinEggs\review_day_25studs.png`.

---

## 6. How the MossBase strips are made seamless

**The goal:** A|A, B|B, A|B and B|A must all chain with no seam.

### Making each strip tile with itself
- Everything is generated **periodic in x with period W** (1024 px = 24 studs):
  - the gradient noise lives on a lattice that wraps modulo the period;
  - domain warps use that noise;
  - the damp-band height h(x) is a periodic function.
- Every clump, spore and tongue is stamped at x, x − W and x + W. A clump that crosses an edge wraps around.
- All the blurs (halos, damp feathering) wrap with `np.roll`.

### Making A and B fit each other: a shared seam band
1. A **shared set of seam objects** (clumps, spores, damp control points) is generated from a common seed, with centres
   within ±1.2 studs of x = 0. Both A and B stamp this set, wrapped.
2. **Unique objects are kept clear of the seam.** Each strip's own objects are placed only where |x − edge| >
   1.2 + their radius + their halo. They can never touch the seam columns.
3. **The damp height is blended as a scalar field, not as pixels.** h(x) = mix(h_unique(x), h_shared(x), w(x)), with
   w = 1 within 1.5 studs of the edges, easing to 0 by 3 studs. A smooth scalar function gives no ghosted
   half-transparent double clumps, which pixel crossfades would.
4. **Result:** the content within about 1.5 studs of the edges is identical in A and B, so every combination is
   continuous.
5. **The seam motif is ordinary on purpose:** medium-low moss, no landmark cushion. It repeats every 24 studs along a
   long run, and should not be noticed.

### Verification
- `sheets\mossbase_seams.png`: the chain A|A|B|B|A|B at 1:1, with seam ticks drawn outside the strip.
- `checks.json`: for each seam, the maximum absolute RGBA difference across the seam must be no larger than the median
  difference between neighbouring columns inside the strip.
- The wall preview shows an A|B seam in frame.

### In Roblox (written in NOTES)
- **Prefer a `Texture`** (StudsPerTileU = 24, StudsPerTileV = 6) on a carrier of any run length, with a random
  OffsetStudsU per run:
  - a 50-stud wall gets one carrier and no squash;
  - a narrower carrier simply crops the strip.
  - Texture sampling wraps, so even the edge filtering is seamless.
- With plain Decals, the carriers must abut exactly at multiples of 24.000.
- End runs at pillars, corners or props.

---

## 7. Preview renders

### 7.1 Studded mocks
- **Stud tile:** made in numpy as 128 px per stud:
  - a height field for a round stud (diameter about 0.6 of the pitch, rounded top edge, the faint cell outline of
    Roblox's stud texture), giving a tangent normal map plus a colour multiplier (AO ring at the stud foot);
  - tiled 1 stud per tile on a **flat** plane, so the studs line up with the patch edges.
  - **Why flat:** this is how Roblox draws `SurfaceType.Studs`. Modelled bumps would poke through a 0.04 carrier and
    misrepresent the game. The pitch is exactly 1 stud and the grid is aligned.
- **Floor patch, 40 x 24:**
  - green plastic (128,170,96), roughness about 0.75;
  - an **8-wide cream path** (222,205,170) crossing the right third, with 1-stud brown edges (150,118,88);
  - this tests every floor decal on green, cream and the edge.
- **Wall section:**
  - 40 wide x 24 tall x 6 thick, blue (96,132,170);
  - the top trim (69,95,132) at 22.9-24.5, sticking out 0.3;
  - standing on a 40 x 12 studded green floor strip, so the wall-foot junction shows;
  - a **placeholder garland** (a brown sagging rope 3.5 below the top, with a few orange / black / purple pennants), to
    show the band the decals keep out of.
- **Scale dummy:** a neutral 5-stud blocky character stand-in next to the decals, to judge scale.
- **Carriers:**
  - one plane per decal, 0.03 / 0.04 / 0.05 above the surface (stain < crack < moss / slime / drip), so there is no
    z-fighting;
  - Image Texture with sRGB and `alpha_mode = STRAIGHT`, linear filtering with mips;
  - Principled BSDF with roughness 0.8 and low specular;
  - `surface_render_method = DITHERED` with 128 TAA samples, for correct order-independent stacking;
  - **`visible_shadow = False`**, so the carriers cast no shadow on the surface.
- **The "realistic mix":**

| Mock | Decals |
|---|---|
| Floor (one each, varied yaw and scale ±15 %) | G_Crack_A, G_Crack_B, G_Crack_C, G_Moss_A, G_Moss_B, G_Stain_A, G_Stain_B, G_Slime_A. One crack and one stain straddle the cream path or its edge. G_Moss_B is tucked against a G_Crack. |
| Wall | MossBase A + B chained (the A\|B seam is in view), W_Crack_A, W_Crack_B, W_Crack_C (its foot under the moss), W_Drip_A, W_Drip_B (off to the side of the garland swag), and one G_Stain_A on the floor strip at the wall foot |

- **Coverage:** about 25-30 % of each mock surface, which is the density cap I'll recommend.

### 7.2 Cameras
- **Format:** every frame is 1920 x 1080 with a **vertical FOV of 70°**, as in Roblox (`sensor_fit = VERTICAL`).
- **Crops:** `_crop` variants use a render border on the same camera, so the pixel density is the true in-game one.
- **Before/after:** `_before` = the same shot with no decals.

| File | Camera |
|---|---|
| `floor_eye25_day` (+ `_before`) | eye height 5, 25 studs from the patch centre, aimed at the centre |
| `floor_eye60_day` (+ `_crop`) | eye height 5, 60 studs (the grazing-angle noise and moiré test) |
| `floor_tp_day` | Roblox default follow cam: about 12.5 studs behind and above the dummy's head, height about 8.8, pitch −20° (the view players mostly see the floor from) |
| `floor_top_ortho` | orthographic top view with the stud grid and 1-stud ticks (scale check) |
| `floor_close6_day` | eye height 5, 6 studs from G_Slime_A and G_Crack_C (edge, halo and gloss check) |
| `wall_eye25_day` (+ `_before`) | eye height 5, 25 studs from the wall face, looking level |
| `wall_eye60_day` (+ `_crop`) | eye height 5, 60 studs |
| `wall_oblique20_day` | 20 studs, 40° off the wall normal (walking along a wall) |
| `wall_close8_day` | 8 studs, at MossBase height (seam and edge check) |
| `floor_eye25_night`, `floor_tp_night`, `wall_eye25_night` | the same cameras under the Moonlit night |
| `wall_eye25_night_candle` (optional) | night plus one warm point light, like the pumpkin-egg candles |

### 7.3 Lighting, calibrated to the real game
- **Day:**
  - Eevee, view transform AgX (the kit's standard);
  - a warm sun (1, 0.95, 0.86) at about 55° elevation, coming from behind-left of the floor camera and from above-left
    on the wall;
  - kit sky fill (0.36, 0.5, 0.72);
  - **haze** from a thin world Volume Scatter (density about 0.001-0.003). This avoids the Blender 5.x compositor API
    churn.
  - **Calibration gate (before any decal goes on):** render the plain mocks and adjust the exposure and haze until a
    plain studded patch at 25 studs matches the screenshot within about 15 levels per channel:
    - green about (176,221,160);
    - cream about (245,237,226).
  - If AgX cannot reach that saturation, I switch to Standard plus exposure, and the choice is logged in the script.
- **Night ("A Moonlit"):**
  - ambient (110,115,150) and outdoor (140,145,185);
  - a cool moon key (200,210,255) at about 40°;
  - a blue haze;
  - calibrated in the same way to green about (93,159,88) and cream about (184,177,185).

### 7.4 2D sheets and automatic checks (PIL, numpy)
- **`sheets\swatches.png`:** every decal at 1:1 over flat green, blue, cream and orange (orange is the robustness
  case), plus a 1/8-size thumbnail row (the shape-read test).
- **`sheets\fringe.png`:** every decal over black, white and magenta, at mip levels 1/2, 1/4 and 1/8. The mips are
  built the **naive straight-alpha way**, as a GPU would build them.
- **`checks.json`**, per file:
  - size, mode RGBA, ≤ 1024;
  - alpha min / max and % transparent;
  - the border rule;
  - the maximum fringe error between the naive straight-alpha mips and correct premultiplied mips, over green and blue.
    Target ≤ 8/255 at the edges.
  - the MossBase seam metric.

---

## 8. Placement guidance I intend to write in NOTES.md

The hub coordinates are taken from the project notes:
- plaza centre (0,−33), r about 25;
- spawn (0,−22);
- back-wall pillars at x = ±13.3, ±39.8, ±66.4, ±93, ±119.5, inner face at z about 104;
- base slots: Base1 x −140..−76 z 4..84, Base2 x −38..26 z 16..96, Base3 x 76..140;
- garden props now stand on the floor;
- 12 pumpkin-egg clusters.

### General rules
- **Compose in clusters, not a sprinkle.** Make 12-16 floor "grime clusters" of 2-4 decals each: a crack plus moss
  plus a stain, or a stain plus slime. Place them where grime would collect: wall feet, under trees, beside graves,
  path edges, around the pumpkin clusters.
- **Keep clean space between clusters.** At least 60 % of any 40 x 40 area stays clean, and decal coverage in an area
  never exceeds about 25-30 %.
- **Floor yaw:** random. Scale ±15 % uniform; don't stretch non-uniformly by more than 10 %.
- **Wall decals:** no rotation beyond ±10°, because they carry "light from above". Get variety from scale and choice.
- **Layer heights:** stain 0.03 < crack 0.04 < moss / slime / drip 0.05. Moss goes over a crack's foot, never under it.
- **Carrier parts** go in `Workspace.HalloweenDecor.Grime`:
  - Anchored, Transparency 1;
  - CanCollide / CanTouch / CanQuery false (the owner's no-collision rule);
  - CastShadow false;
  - Decal Face Top for the floor and Front for the wall.

### Exclusions
- Nothing within **8 studs of spawn** (0,−22).
- **Plaza centre:** keep r ≤ 12 around (0,−33) clean (the statue plinth). Allow 2-3 cracks and 1 stain at the plaza
  rim (r 18-25) so the spawn view gets some Halloween grime.
- **Gameplay areas:** none inside the base slots (+4 margin), on treadmill pads, on stall plinths, on VIP doors, on the
  tutorial arrow route or on leaderboards.
- **Never on the runway.**

### Per-texture counts for the whole hub (a starting point, tuned after the test patch)
| Texture | Count | Where |
|---|---|---|
| G_Crack_A/B/C | 14-18 total, about 1 per 250-300 st² of open green inside clusters | mixed shapes; never the same shape twice within 30 studs |
| G_Moss_A/B | 8-12 | wall feet (tying into MossBase), under trees, next to graves, in shade |
| G_Stain_A/B | 10-14 | under drips, wall feet, path edges, under trees |
| G_Slime_A | 3-5 in the whole hub | near 1-2 pumpkin clusters, the foot of a slime drip, the plaza rim. Never two in one view from spawn. Prefer cream and plaza edges. |
| W_MossBase_A/B | along the wall bottoms with gaps | runs of 1-3 strips (24-72 studs), gaps of 6-20 studs. Back wall: one strip per bay (bays are 25-28 wide, so the pillars make the gaps). Alternate A/B, random OffsetStudsU. A 4-6 stud cropped piece at some pillar feet. |
| W_Crack_A/B/C | 10-15 | about 1 per 1-2 bays, in the lower half (base to about 12 studs), centred in a bay below the garland swag; never behind a vine or web. W_Crack_C always sits on a MossBase run. |
| W_Drip_A/B | 6-10 (about 2/3 of them A) | mostly on wall stretches without garlands (side walls, front diagonals, corners). On the back wall at most 1 per 3 bays, off-centre so the pennants don't cover it. Top edge exactly at the trim bottom (y 22.9). |

**Cream paths and plaza:**
- Cream renders almost white in game, so dark glazes pop about twice as hard there.
- Use Decal.Transparency 0.25-0.35 for stains on cream.
- Place at most 1 decal per about 30 studs of path, at the path edge (straddling the brown edge) rather than centred.

**Test patch for the owner** (written as a ready recipe in NOTES):
- one back-wall bay: MossBase A, W_Crack_C, W_Drip_A;
- the green floor in front of it: G_Moss_A at the wall foot, G_Crack_A, G_Stain_A;
- one plaza-rim spot: G_Crack_B, G_Slime_A;
- with exact positions and sizes relative to the bay.

---

## 9. Risks and how I avoid them

| Risk | Mitigation |
|---|---|
| **Noisy / photo-grunge** | No photo sources and no fractal grain fills. Noise only warps shapes or places clumps. Frequency budget: no feature < 0.08 stud. Detail only where a shape needs it (bevels, clumps, tide lines). Cluster placement leaves clean space. Thumbnail test at 1/8. |
| **Flat / cartoon** | Painted depth on everything: two-sided bevels with D2 inner walls, AO and underside rims on moss, a cushion height-field shading, tide lines on stains, gloss and rim lights plus a contact ring on slime. Only slime carries an outline. Cracks have a dark core, not a black pen line. |
| **Halos and fringes** | Straight alpha, push-pull colour bleed under every alpha-0 texel, a clean alpha floor, 3 px clear borders, a measured naive-mip fringe test, and close-up renders at 6-8 studs. |
| **Tiling seams (MossBase)** | Periodic generation, the shared seam band, the scalar-field blend, a numeric seam test, and a rendered A\|B seam. NOTES recommends Texture tiling. |
| **Scale mismatch with the studs** | The px/stud density is fixed per texture, and features are specified in studs. The ortho top view shows the stud grid and ticks, with the 5-stud dummy in frame. The floor features are bolder to survive foreshortening. |
| **Not reading on green (moss, slime)** | Read by value and hue rather than "green": dark M1/M2 body, a damp halo, a minority of yellow tips; slime gets an outline, a contact ring and gloss. Checked on the 4-colour swatches and in the lit mocks. |
| **Too dark or gloomy for a cheerful hub** | Tinted darks, never black. Glazes keep the base hue. The coverage cap. The playful slime accent. Before/after pairs for the owner. |
| **Night: moss becomes black blobs** | M1 is not darker than (40,56,28). Night renders are a required gate. |
| **Lighting** | The decals don't touch Lighting. The previews are calibrated to the restored original day and the picked Moonlit night. |
| **Z-fighting / overlap** | Staggered carrier heights in the previews and in NOTES. |
| **Repetition** | 3 crack shapes per surface. Clusters mix the types. "Not the same shape twice within 30 studs". MossBase A/B alternation with a random offset. |
| **Compression banding on soft stains** | ±0.5 LSB dither on the alpha ramps. No large flat areas of very low alpha. |
| **MossBase softness up close** (42.7 px/stud) | The design uses clumps ≥ 0.6 stud and no fine linework in the strips. Checked in `wall_close8_day`. This is a known limit of 24 studs on a 1024 px cap. |

---

## 10. Files, run commands, build order

```
HubGrime\
  PLAN.md  BRIEF.md  NOTES.md (after build)  checks.json
  gen\grime_lib.py      numpy: periodic noise, warps, polyline SDF raster, metaballs, height shading, blur,
                        layer compositing, push-pull bleed, straight-alpha save, checks
  gen\make_decals.py    one function per texture, fixed seeds -> decals\*.png + checks.json
                        (python gen\make_decals.py [names...])
  gen\make_sheets.py    swatches / fringe / seam sheets
  gen\make_studs.py     stud tile colour + normal -> mock\
  gen\mock_preview.py   headless Blender: mocks, carriers, calibrated day/night, cameras -> renders\
                        ("blender.exe" -b --factory-startup --python gen\mock_preview.py -- --set day|night|calib)
  decals\  mock\  renders\  sheets\  logs\
```

Long Blender jobs run with a timeout, and their output goes to `logs\`.

### Build order
1. **Calibrate:** the stud tile, the plain mocks, and the calibration renders matched against the screenshots
   (`renders\calib_*`).
2. **Make the textures by family:** cracks, then moss, then stains, then slime, then MossBase, then drips. After each
   family, run the swatch and fringe sheets and the checks, then self-review.
3. **Day previews:** the before/after pairs, then iterate.
4. **Night previews.**
5. **NOTES.md:** sizes, px, where, counts, the test-patch recipe and the Studio properties.
6. **Self-review:** go through the risk table and the reviewer's checklist before reporting. Fix anything that would
   not pass a senior game-art lead.

No Studio, no GUI Blender MCP, no downloads, no edits to `hkit.py` (read-only) or other agents' files, no git commits.

---

## 11. Open questions for the lead (the defaults I'll use if there's no answer)

1. **Wall colour.** `DAY_original_restored.jpg` shows salmon / orange side walls in the plaza view, while the brief
   says the walls are blue (96,132,170).
   - **Default:** follow the brief (blue mock) and add orange as a swatch-sheet robustness check. The palette ΔE
     there is ≥ 48 for all the key colours.
2. **Drips vs garlands.**
   - **Default:** drips mostly on the walls without garlands, at most 1 per 3 back-wall bays.
3. **MossBase as a `Texture` (tiled) rather than a Decal.**
   - **Default:** recommend Texture in NOTES, and keep the files usable as plain Decals too.
