# SLINGSHOT pets - STYLE BIBLE (PetsV3 quality pass, 2026-10-08)

Target look: Steal an Egg block creatures (`_refs/ref_01..25`). Our renders: `_review/<Name>_model.png`.
Units (always measured on the FINAL model, after any HEAD_XF):
- `TW / TH / TL`: full width / height / length of the main torso block.
- `HW / HH`: full width / height of the head (cranium) block. `H`: standing height of the pet.
- `h_min`: smallest half-size of a block. `cell`: plate grid cell. `V` / `S`: HSV value / saturation.
- Pets face -y, z up.

---------------------------------------------------------------------------------------------------------------------
## 1. Why ours look low quality (ranked by impact)

**1. Proportions: small heads, long thin legs ("robot dog").** Refs: head ≈ torso width and 38-45 % of the standing
height (dog ref_02, cat ref_05, frog ref_03, turtle ref_11); legs short and thick (dog ≈ 0.6 TH long, ≈ 0.4 TW wide).
Ours: Raiju head was 0.75 TW / 0.65 TH before HEAD_XF with legs 1.05 TH long; Stag, Stallion and Panther legs are
about 0.25 TW wide. FIX: build heads at their final size (stop using HEAD_XF, which scales bevels and plates wrongly)
and hit this table:

| archetype | pets | HW/TW | HH/TH | head % of H | leg len/TH | leg W/TW | eye H/HH |
|---|---|---|---|---|---|---|---|
| quad lovely | Tortoise*, Stag, Cvetibara, Pharaoh | 1.00-1.15 | 0.90-1.05 | 38-45 | 0.45-0.70 | 0.38-0.45 | 0.30-0.36 |
| quad cool/fierce | Raiju, Bull, Boar, Cerberus*, Panther, Stallion*, Lion, Griffin | 0.85-1.00 | 0.75-0.90 | 28-36 | 0.60-0.85 | 0.32-0.40 | 0.20-0.26 |
| biped | Treant, Kappa, SeaTurtle, Golem* | 0.95-1.15 | 0.80-1.00 | 30-40 | 0.45-0.65 | 0.40-0.48 each | 0.24-0.30 |
| bird / winged | Wyvern, Ivonrath, CelDragon, Griffin | 0.85-1.05 | 0.80-1.00 | 28-42 | 0.50-0.70 | 0.32-0.38 | 0.22-0.30 |
| serpent | BlackDragon | 1.7-1.9 D (tube) | 1.3-1.5 D | - | 0.7 D | 0.35 D | 0.22 |
| blob / floater | Kraken | mantle = head | - | 55-60 | tentacle 1.1-1.3 mantle H | base 0.20 mantle W | 0.24 mantle H |

`*` = pet-specific numbers in section 3. Never "squishy": a blob keeps crisp plates, firm faces and readable limbs.

**2. Dead faces.** Refs: every eye is layered (outline, coloured iris, pupil, 1-2 white highlight squares: dog, cat,
duck ref_04), 25-35 % of HH; angry pets still have an iris and a highlight (pharaoh ref_23, fire ref_16). Noses are big
and rounded (≈ 0.3 HW); mouths are a closed "w" line or open with 2 fangs. Ours: yellow slits 12-20 % of HH, no iris,
no highlight, an angry brow on every pet = the same robot everywhere. FIX: eye builder §2c, one mood per pet,
highlights always (SAME side in both eyes), brows only for bold/fierce moods.

**3. Hard CAD boxes.** Refs: big masses are soft boxes (bevel ≈ 20-25 % of the half-size, round, blended shading)
with crisp small plates on top; soft mass + crisp detail IS the look. Ours: a 1-segment 45° chamfer at 3-8 % of the
half-size with flat shading, so a bright facet line shows on every edge. FIX (§2a): masses 0.22·h_min / 3 segments /
smooth; limbs 0.18·h_min / 2 / smooth; details 0.12·h_min / 1 / flat; edges sharper than 30° stay hard; plates flat.

**4. Plates invisible and random.** Refs: plates 0.11-0.13 TH wide on a regular brick grid (cell ≈ 0.2 TH), covering
25-38 % of head, legs and body alike, in the surface tone with a lit top; they read from across the map. Ours: random
scatter plus an 8-cell neighbour block = 10-15 % coverage, many 2x1 slivers, same-colour tops; in game
(`Raiju/ingame_*.jpg`) the pet reads as a smooth box. FIX (§2b): brick grid, cell 0.18 TH, plate 0.62 cell, relief
0.30 × plate width, fill by tier, top ×1.08 V / foot ×0.90 V, tighter AO bake.

**5. Kit-bashed build (seams, gaps, floating boxes).** Ours: torsos split into 2 equal boxes (Raiju, Lion, Panther,
Stallion), haunch boxes sticking out (Raiju, Bull), leg segments offset sideways (Boar, Bull), an odd-coloured separate
neck (Stag). FIX: 1 torso block; an optional chest block must be ≥ 15 % bigger and overlap the hips by ≥ 35 % of its
length. Touching blocks are never within ±10 % of each other's size on the shared face. Legs: T1-2 = 1 block + paw;
T3+ thigh + shin, shin top buried ≥ 30 % into the thigh; leg tops buried ≥ 25 % of leg length in the torso; no gaps.

**6. Monotone dark palettes, no colour zones.** Refs: 3 tones + 1 accent in clear zones (base ≈ 60 %, light
belly/muzzle/socks ≈ 20 %, dark nose/pupils/hooves ≈ 8 %, accent ≤ 10 %); dark creatures keep a hue (lava lizard navy
(48,44,72) + orange). Ours: Panther, Stallion, BlackDragon, Bull, Golem ≈ 85 % one near-black; Kraken 95 % one red. FIX:
- 4-5 tones per pet, 1 flat tone per zone (plates take their zone's tone); gradients only on wings/manes (3 steps).
- Base S 45-80 %, V 55-90 % (dark pets V ≥ 28 %, S ≥ 25 %). Light ≥ +30 % V over base, S 8-35 %. Dark V 12-25 %.
  Accent S 70-95 %. Never pure (0,0,0) / (255,255,255): use (24,20,34) / (246,244,250).
- Every pet: a belly/bib/muzzle zone of 15-25 % of the surface + a sock/paw zone. Neighbouring zones differ ≥ 25 % V or
  ≥ 60° hue. The top view shows ≥ 2 zones.

**7. Greebles and stickers instead of patterns.** Refs mark surfaces only with plates and designed patterns (cat
stripes in 3s, raccoon mask, fox eye mask, pharaoh armour bands). Ours: thin vents (Raiju back), outline bars (Golem),
bolt decals floating on flat flanks (Bull), one-colour "TV screen" panels (Golem, Cerberus chests). FIX: no bar thinner
than 0.45 cell unless it is one of ≥ 3 parallel marks; patterns = chunky stripes 0.5-0.8 cell wide in sets of 2-4,
spots/rosettes made of plates, masks; no flat light/hot rectangle bigger than 3 × 3 cells (break it into plates).

**8. Paper appendages.** Refs: phoenix wing (ref_20) = 3 overlapping feather rows dark → mid → light, saw edge, plates
on every feather; bird ref_13 has an orange tip layer. Ours: one-colour flat Wyvern membrane, stick Griffin feathers,
straw Stag antlers, straight stick Kraken tentacles, a flat square Lion mane. FIX: minimum thickness membrane ≥ 0.04 TH,
feather ≥ 0.05 TH, antler beam ≥ 0.12 HW, tail root ≥ 0.25 TW; wings per §2d; manes = 2 rings of blocks ≥ 0.3 HW deep.

**9. Feet read as shoes or slabs.** Refs: socks (last 25 % of the leg in a contrast tone), paws wider than the leg with
toe splits (dog, raccoon), dark claws (lava lizard), 3-toe bird feet. Ours: boots with thin bands, slab feet, tiny
claws. FIX: paw 1.12 × leg W, 1.2 × leg depth, 0.35 × leg W tall, 2 toe grooves (dark inlays 0.05 paw W) or 3 toe
blocks; fierce claws = 3-4 spikes L 0.30 / W 0.10 paw W; hooves = dark block 1.08 × leg W with a light feather ring
above (horses); socks 22-28 % of leg height.

**10. Rarity shown by recolour or glow, not by design.** Refs: commons are a simple animal with plates; rares get
layered silhouettes (phoenix), armour over a core (lava lizard), costume sets with gems (pharaoh), body props (snail
castle) and VFX. Ours: tiers differ only in colour and in neon bits (now removed). FIX: tier ladder in §2d; each SECRET
also gets one bespoke hero costume set.

---------------------------------------------------------------------------------------------------------------------
## 2. Kit spec (numbers for blockkit.py)

### 2a. Base block rounding
```
ROUND = {"mass": (0.22, 3, True), "limb": (0.18, 2, True), "detail": (0.12, 1, False)}  # (bevel x h_min, segs, smooth)
role auto (override Block(role=...)): h_min >= 0.10*TH -> mass ; h_min >= 0.035*TH -> limb ; else detail
_box_bm: off = min(frac*mn, 0.45*mn); bmesh.ops.bevel(segments=segs, profile=0.5, clamp_overlap=True)
smooth: copy f.smooth when copying tmp -> part bm; then e.smooth = (both faces smooth and calc_face_angle < 30°);
        k.part(..., smooth_shade=False) so the flags survive. If Studio shows faceted bevels: FBX mesh_smooth_type="OFF"
inlays (thinnest half < 0.02*TH: face plates, stripes): bevel min(0.012, 0.6*thick), 1 seg, flat (on_face default)
tapers: torso bot (0.90,0.95) | head top (0.94,0.94) | muzzle top (0.88,0.85) | thigh bot (0.88,0.90)
spikes/horns/claws: spike(top=(0.12,0.12)); 2-tone = base spike top=(0.45,0.45) + accent tip spike at 30 % length
budget: <= 18k tris/pet (Roblox cap 20k) | <= 14 "mass" blocks | <= 450 plates (18 tris each)
AO bake (petkit.bake_and_export): col * (0.60 + 0.40*AO)  (was 0.72/0.28), AO distance 0.20*TH (was 0.6)
Studio: SmoothPlastic, Reflectance 0. NEVER Neon / emissive textures (NO_GLOW stays True).
```

### 2b. Surface plates (replace `_studs_for`)
```
cell    = 0.18*TH  (floater 0.18*mantle W; serpent 0.30*D) - one cell size per pet
plate   = 1x1 width 0.62*cell; half a = cell*(w - 0.38)/2 (gap 0.38 cell); relief stud_h = max(0.186*cell, 0.02)
top     = chamfer inset 0.30*min(a, b); straight wall for the lower 50 % of the relief
layout  = brick rows along the face's long axis, row k shifted (k % 2)*0.5 cell; mark ONLY occupied cells (drop the
          -1..w+1 neighbour ring)
fill    = per-cell chance T1 .55 | T2 .60 | T3 .65 | T4 .70 | T5 .72 | T6 .75 | SECRET .45  (coverage ~25 % -> 35 %)
mix     = 1x1 60 % | 1x2 vertical 25 % | 2x1 15 % ; T4+: 2x2 = 10 % of picks on faces >= 4x4 cells
margin  = blk.bevel + 0.30*cell ; faces < 2x2 cells: none ; -z: none ; limbs: outer side + front only
keep-out= head front: eyes + muzzle rectangle + 0.5 cell ; any inlay/pattern (contains() test)
colour  = foot ring x0.90 V, top ring + top face x1.08 V (clamp), per-plate jitter ±3 % V (seeded)
variants= "shingle" tilt 20° about u, lower edge proud (ruffs, chest feathers, ref_09)
          "diamond" rotated 45° about n (dragon scales)
          "flush" thick 0.004, x0.80 V (fake inset square, ref_03)
test    = pet rendered 128 px tall: each 1x1 plate >= 3 px (plate >= 2.3 % of H)
```

### 2c. Eye / face builder: `eye(B, head, side, mood, iris)`. Sizes are × HW unless noted.
```
               lovely          bold            fierce (wedge)
outline WxH    0.30 x 0.32     0.28 x 0.28     0.30 x 0.20, top=(1.0,0.7), rot 14° inner corner down
iris    WxH    0.22 x 0.25     0.20 x 0.21     0.22 x 0.13
pupil   WxH    0.11 x 0.14     0.10 x 0.12     0.05 x 0.13 (slit)
highlights     0.08 + 0.04     0.07 + 0.035    0.06
centre x / z   ±0.24 / 0.55HH  ±0.25 / 0.58HH  ±0.25 / 0.62HH   (z up the head front face)
brow           none            0.26x0.05, 6°   0.30x0.06, 20° inner-down, 0.03 above outline, 0.03 proud
layers (on_face thick): outline .010, iris .016, pupil .022, highlights .028 -> each 0.003 HW prouder
```
- **Colours:** outline (24,20,34). Iris: S ≥ 60 %, V 45-80 %, never the base colour. Pupil (16,12,24). Highlights
  (250,250,255).
- **Dark faces** (base V < 30 %): use a light rim (232,226,255) instead of the dark outline.
- **Pupil and highlights:** pupil offset 0.02 toward the nose and 0.02 down. Highlight 1 in the upper-LEFT iris corner
  on BOTH eyes (do not mirror), inset 0.02. Highlight 2 lower-right.
- **Options:** sclera crescent (dog look): white 0.04 band on the inner-lower edge. Lids (regal/grumpy): a base-colour
  plate over the top 25-35 % of the outline, 0.032 proud.
- **Blush** (lovely, SECRET): 0.13 × 0.05 at x ±0.33, z 0.36 HH, colour lerp(base, (255,120,150), 0.55).
- **Nose:** W 0.20 (cats) / 0.24 (dogs, wolves). H 0.6 W, depth 0.5 W, role "limb". Dark (34,26,40) or pink
  (240,140,165), with a 0.035 white sheen square at the upper left.
- **Mouth, closed:** "w" or smile of 3-4 bars, 0.07 × 0.022, 0.10 below the nose.
- **Mouth, open:** roof (110,26,44) 0.40 × 0.12; jaw block; tongue (236,110,140) 0.16; fangs = spike W 0.045, L 0.09.
- **Muzzle:** W 0.55-0.65, H 0.40-0.50 HH, protrudes 0.30-0.50, light tone, buried ≥ 35 % of its depth in the head.
- **Ears:** depth ≥ 0.25 × ear W, inner plate at 65 % size in light/pink. Lovely ears 0.45-0.60 HH.

### 2d. Per-tier extras (the mesh is solid colour only; glow/fire/aura = ParticleEmitter VFX, never Neon parts)
| tier | area | mood | tones | mesh extras | idle VFX |
|---|---|---|---|---|---|
| T1 | Grass | lovely | 3+1 | 1 nature prop (moss/leaves/flowers/mushroom), ≤ 8 blocks | leaves on acts only |
| T2 | Water | lovely-bold | 4 | shell/fins + 1 costume prop (dish, bandana, trident) | bubbles |
| T3 | Storm | bold-cool | 4 | horns/spikes ≤ 8, ankle/wrist bands, bolt inlays | sparks |
| T4 | Magma | cool-fierce | 4+core | armour-over-core rock slabs, cracks, spike crest 5-9 | embers + smoke |
| T5 | Void | fierce | 4+crystal | crystal clusters 2-3, floating shards ≤ 4 on an "Orbit" bone | wisps |
| T6 | Celestial | majestic | 4+gold | gold trim + rivets, layered wings, sun/halo/star pieces | sparkles |
| SECRET | its egg | lovely-chibi hero | 5 | 1 bespoke hero costume set + gems, plate fill .45 | area VFX + 1 bespoke |

- **Spikes:** L 0.15-0.35 TH, base W 0.35 L. Rows step 100/80/60 %. Accent tip covers 30 % of the length.
- **Crystals:** a cluster is 1 shard (L 0.30 TH, W 0.07 TH, top=(0.10,0.10), rotated 45° about its axis) plus 2-3
  shards at 0.55-0.70 L, splayed 18-30°. Lower 60 % mid tone, tip light. Rock collar at the base.
- **Cracks:** zigzag of 3-5 `bar()` segments, W 0.45-0.5 cell, thick 0.4 stud_h. Turns 35-70°, 1 branch, starting
  from a seam or the core.
- **Armour:** plates 0.05-0.08 TH thick, role "limb", overhanging 4 %. Gold (244,192,60) or steel (172,178,198). Each
  plate gets 1 gem inset (35 % W, rotated 45°) and 4 gold rivets (1x1, 0.05 TH).
- **Feather wing:** arm bar W 0.10 TH + 3 rows: coverts 6-8 feathers at 0.25 half-span (base tone, plates .5),
  secondaries 7-9 at 0.40 (mid tone), primaries 5-7 at 0.55 (light/accent). Feather = Block W 0.12-0.16 TH, thick
  0.05 TH, top=(0.25,1), 40 % overlap, fan step 8-12°, tip lengths ±10 % (saw edge).
- **Membrane wing:** arm bar W 0.10 TH. 3-4 finger bars, W 0.06 TH tapering to 0.4. Poly panels thick 0.035 TH, inner
  panel ×0.80 V. Pull each trailing edge in by 12-18 % between fingers (scallops). Wrist claw. Plates on the bars only.
- **Wing span:** tip to tip 2.4-3.0 × body length.
- **VFX setup:** ParticleEmitter parented to the Bone (a Bone is an Attachment), LightInfluence 0. At most 2 idle
  emitters (SECRET 3) and 40 live particles; acts may call `:Emit(n)`. Size and speed are × H (pet height in studs at
  scale 1). Check once that Model:ScaleTo scales them with KG.

| VFX | Rate | Life | Size ×H | Speed ×H/s | Colour | LightEm | notes |
|---|---|---|---|---|---|---|---|
| leaves/petals | 1.5 | 2.5-3.5 | 0.03 | 0.05 | (120,210,90)/(255,170,205) | 0 | Accel -0.1H, Rot ±90 |
| bubbles | 2 | 1.2-1.8 | 0.015→0.03 | 0.08 up | (200,235,255) | 0.2 | Transp 0.3→1 |
| sparks | 3 (+8 on act) | 0.12-0.25 | 0.04→0 | 0.6 | (255,232,90)→(150,200,255) | 0.8 | Spread 180 |
| embers | 6 | 1.0-1.6 | 0.012→0 | 0.25 up | (255,200,60)→(255,80,20) | 0.6 | Spread 25 |
| smoke | 2 | 2-3 | 0.06→0.14 | 0.1 up | (60,50,56) | 0 | Transp 0.55→1 |
| flame tip | 18 | 0.35-0.55 | 0.07→0.01 | 0.15 up | (255,230,110)→(255,90,20)→(120,20,10) | 0.7 | ZOffset 0.3 |
| wisps | 4 | 1.0-1.5 | 0.05→0 | 0.05 up | (170,100,255)→(40,20,90) | 0.35 | Transp 0.35→1 |
| sparkles | 3 | 1.2-1.8 | 0→0.035→0 | 0.03 | (255,244,180)/(200,220,255) | 0.7 | star texture |

**Gate before showing a pet to the owner:** (1) the 64 px black silhouette is identifiable and the head is the
2nd-biggest mass; (2) plate test §2b passes; (3) every eye has an iris + highlight; (4) palette rules (item 6) pass;
(5) no Neon mesh part; (6) ≤ 18k tris; (7) `overlap_report` clean.

---------------------------------------------------------------------------------------------------------------------
## 3. Per-pet art direction
Each palette lists base · light · dark · accents · iris.

**MossbackTortoise** (T1 Grass, quad lovely, low). A wide 3-tier stepped shell (rim 1.0 S, mid 0.82 S, cap 0.60 S;
S = shell width) carrying a small garden. A big friendly head sits forward on a short thick neck, with the face at
80-90 % of the shell height. HW 0.55 S, HH 0.42 S. Stump legs 0.24 S wide, 0.18 S visible, splayed 8°. Palette: skin
(104,176,76) · jaw (214,226,150), plastron (226,204,140) · (60,42,30) · shell (132,88,52), scute gaps (88,58,36), moss
(92,190,72)/(150,220,96), flowers (255,156,196)/(255,228,110) · iris (70,44,28). Face: lovely eyes on the FRONT face,
blush, 3-bar smile. Signature: a scute shell of dense raised 2x2 plates with dark gaps and a tan rim band of 1x2 plates
(ref_11). On top, a moss carpet with ONE chunky bonsai (trunk 0.09 S, 3 round canopy blocks), 2 flower clusters and a
red mushroom. 3 light toenails per foot. Avoid: pyramid shell with tiny decals, grey mouth box, side-only eyes, brows.

**ForestStag** (T1 Grass, quad lovely). A compact fawn with its head high, oversized ears and a wide V of thick antlers
(span 1.8 HW). HW 0.95 TW, HH 0.85 TH. Short thick neck (W 0.65 TW, length 0.55 TH) in the body colour. Legs 0.80 TH
long but 0.30 TW thick. Ears 0.5 HH. Palette: fawn (200,124,64) · cream (250,236,212) on muzzle, bib, belly, tail, ear
inners and spots · (64,42,32) · antler (140,98,62), leaves (104,200,88)/(66,160,74), blossom (255,168,206) · iris
(58,36,24). Face: lovely eyes with 2 lash blocks at the outer corner, a round dark nose with sheen, a small smile.
Signature: antler beam 0.12 HW with 2 tines per side, 2 leaf clusters and 1 blossom per antler; 8 cream fawn spots in
2 rows along the spine; a fluffy 3-tuft cream bib and an upright tail flag. Avoid: long thin dark neck, straw antlers
with white "tooth" tips, stilt legs.

**Treant** (T1 top, biped). A barrel trunk whose upper half IS the face (head = torso, like ref_19), under a canopy
1.3 × trunk W. Stubby root legs; arms reach the knee and end in 3 twig fingers. Heights: canopy 30 %, trunk/face 45 %,
legs 25 % of H. Each eye 0.26 trunk W. Palette: bark (128,88,54) · face panel (206,162,106) · grooves and sockets
(78,52,32) · leaves (92,186,74)/(156,222,96), blossoms (255,172,208), mushroom (226,70,60)+(255,240,230) · iris
(120,210,80). Face: big eyes in dark-bark sockets, mossy flat brows at 6°, a wide grin with 2 square wooden teeth.
Signature: bark made of vertical 1x2 plates only (fill .70); 4-5 overlapping rounded canopy blocks in 2 greens with
blossoms; a red mushroom shelf on one hip and moss pads on the shoulders. Avoid: a separate small head box on top,
stick branches, robot shoulders.

**Kappa** (T2 Water, biped lovely-mischief). A pear shape: big head (HW 1.10 TW, 40 % of H), short round body, legs
0.5 TH, hands reaching the hips, a turtle shell on the back and a water dish on the head. Palette: skin (66,196,166) ·
plastron and webs (236,232,176) · hair, shell rim and claws (28,96,84) · beak (255,190,56), shell (88,132,74), dish
(214,240,255) + water (96,190,244), mawashi (64,72,170) · iris (40,64,130). Face: lovely eyes, asymmetric brows (left
flat, right raised 12° for mischief), a duck beak with a grin line. Signature: the dish rim with an inset water plate
and a ring of 7 dark hair spikes; a shell backpack with big 2x2 plates; webbed 3-toe feet; a chunky mawashi belt.
Avoid: tall thin body, long limbs, slit eyes.

**SeaTurtleWarrior** (T2, biped bold-heroic). A broad A-stance with a big head, red bandana tails blowing back, a
gold-rimmed shell and a trident planted at the side, taller than the pet. HW 1.0 TW, HH 0.85 TH, legs 0.55 TH, arms
0.30 TW, fists 1.3 × arm W. Palette: skin (98,204,140) · plastron and jaw (246,234,184) · (24,60,70) · shell
(34,112,146) with plates (56,150,184), gold (246,196,64), bandana (222,52,52)/(160,30,40), pearl (230,244,255) · iris
(34,70,130). Face: bold eyes, 8° thick brows, a one-sided smirk. Signature: 2 bandana tails (W 0.12 HW); 2x2 scutes on
the gold-rimmed shell; a trident with a 0.08 TW shaft, 3 barbed prongs and a pearl in the fork; wrist and ankle wraps.
Avoid: thin stick trident, square robot torso, flat beak box.

**Kraken** (T2 top, floater; crisp, not squishy). One tall rounded mantle (top=(0.78,0.78), H 1.1 × W) hovering
0.3 mantle H off the ground, with eyes at 35-45 % of its height. 8 thick tentacles, each 0.20 mantle W at the base
tapering to 0.35×, 1.2 mantle H long, in 4 segments with the last 2 curled 40° up. 2 fins on top. Palette: crimson
(220,64,92) · underside and suckers (255,200,176) · spots and fin rims (128,26,56) · barnacles (226,222,206) · iris
(255,196,48). Face: bold-size eyes with horizontal bar pupils, a 15° brow ridge, a small beak below. Signature: rows of
light 1x1 sucker plates under every tentacle; dark 2x2 spots on the mantle; a barnacle cluster on one fin; bubble VFX.
Avoid: straight stick legs, the stepped cone-hat mantle, slit eyes, a one-colour body.

**Raiju** (T3 Storm, quad cool; the approved direction, so refine, don't redesign). A proud wolf with its chest forward,
tall ears and the bolt tail held high. HW 1.0 TW, HH 0.85 TH, head 32 % of H. One torso: the chest block is 10 % larger
and overlaps the hips by 40 %. Legs 0.65 TH, 0.36 TW. Palette: blue (52,104,236) · white (236,242,255) on muzzle, bib,
ruffs and belly · navy (30,36,86) on socks, nose and brows · yellow (255,206,46) on bolts and inner ears · iris
(255,214,60). Face: fierce wedge eyes WITH an iris, slit pupil and highlight; 18° brows; an open grin with 2 fangs; a
big nose with sheen. Signature: a thick bolt tail (≥ 0.12 TW, 3 zig blocks); chunky bolt inlays on the flanks
(0.6 cell wide); big white cheek ruffs (4 tapered blocks per side); navy socks with toe grooves; spark VFX. Avoid: back
"vent" stripes, thin leg bands, separate haunch boxes, neon.

**ThunderBull** (T3, quad heavy fierce). A front-heavy wedge: a huge shoulder hump (chest 1.3 × hips), the head held
low, wide upswept horns (span 2.2 HW), short pillar legs and a storm cloud riding the hump. HW 0.80 chest W, HH 0.75
chest H, legs 0.50 TH, 0.40 TW. Palette: slate-blue (74,86,146), lighter than now · muzzle and belly (176,188,236) ·
hooves and nostrils (34,38,64) · horns (242,234,212) with tips (70,70,96), cloud (238,242,255)/(184,194,226), bolts
(255,206,46) · iris (255,214,60). Face: a heavy 20° brow RIDGE across the forehead; a light muzzle 0.65 HW with 2 dark
nostril plates; a gold nose ring of 4 blocks. Signature: a two-tone cloud of 3-5 blocks with spark VFX; horns in
3 curving tapered segments; bolt inlays on the shoulders; split hooves. Avoid: crate head, bolt stickers, all one dull
slate.

**StormWyvern** (T3 top, winged biped). An upright wyvern with a big head, a deep chest, thick hind legs and a long
tail (1.6 TL, tapering 1.0 → 0.35) ending in a bolt. Wing span 2.8 × body length. HW 0.95 TW, HH 0.85 TH, short neck.
Palette: storm blue-violet (78,84,200) · belly bands (196,206,255) · bones and claws (36,30,90) · membrane
(150,150,250) with inner (110,104,220), horns (242,236,220), bolt and chest gem (255,214,60) · iris (255,214,60).
Face: fierce eyes, a 20° brow, a jaw with 4 fangs, 2 swept-back horns and 2 cheek frills. Signature: membrane wings
built to §2d; light 2x1 belly armour bands; sparks from the wing tips while flapping. Avoid: paper membranes, cyan
edges, a small head on a thin neck.

**MoltenBoar** (T4 Magma, quad fierce, armour-over-core like ref_17). A wedge: a massive head and shoulders, the back
sloping down to small hips, short legs, big upturned tusks (0.6 HW) and a rock spike crest. HW 1.05 TW, HH 0.85 TH,
legs 0.50 TH, 0.40 TW. Palette: rock (54,46,62) · rock tops (90,78,98) · (30,26,34) · magma core (255,112,32)/
(255,192,64), tusks (250,240,222), snout pad (150,96,96) · iris (255,184,44). Face: fierce eyes in rock sockets, a 22°
brow, a flat snout pad with dark nostrils. Signature: raised rock slabs (2x2 and 2x1, 1.5 × relief) on the head, back
and shoulders, leaving 30-40 % orange showing on the belly, inner legs and gaps; a crest of 7 spikes in 3 sizes with
orange tips; ember and smoke VFX. Avoid: a grey box with thin orange zigzags, orange-square nostrils.

**LavaGolem** (T4, biped brute). A gorilla build: huge shoulders, boulder fists (1.4 × head W), the head sunk between
the shoulders, arms 1.2 TH, legs 0.45 TH. Brute exception: HW 0.70 TW and HH 0.60 TH, but the eyes keep fierce sizes.
Palette: basalt (62,54,66) · tops (98,88,102) · (30,26,34) · magma (255,118,30)/(255,200,70) · iris (255,200,70).
Face: a deep brow shelf sticking out 0.12 HW; an underbite with 4 square teeth. Signature: a magma heart made of a
recessed cluster of orange 2x2 plates framed by rock; crack inlays (§2d) running from the heart to the shoulders and
knees; shoulder spikes and knuckle plates; ember and drip VFX. Avoid: thin orange outline bars, the "TV screen" chest,
uniform grey cubes.

**Cerberus** (T4, quad fierce, 3 heads). A broad chest carries 3 big heads in a fan: each HW 0.60 TW, HH 0.55 TH; the
centre head is 15 % larger and 0.1 HH higher; the side heads are yawed 20° out. Legs 0.60 TH, 0.38 TW, with a
flame-tipped tail. Palette: charcoal (44,40,54) · Rottweiler tan (214,124,54) · noses (20,18,28) · collars
(204,44,54) with spikes (222,222,232), tongue (236,110,140) · iris (255,176,44). Faces with 3 personalities:
left = goofy (bold eyes, tongue out); centre = alpha snarl (fierce, fangs, 24° brow); right = grumpy (half lids). Each
gets tan brow dots, a tan muzzle, plus a tan chest V and tan socks on the body. Signature: a spiked collar on each
neck; flame VFX on the tail tip; 3 different ear poses. Avoid: 3 identical heads in a row, the orange chest panel.

**Ivonrath** (SECRET Magma, winged quad, chibi but proud). A big head (HW 1.05 TW, HH 1.0 TH, 42 % of H), a rounded
chest, stubby legs (0.5 TH), 2 big swept horns, wings spanning 2.4 × body length and a curled tail. Palette: red
(222,52,42) · belly bands (255,192,92) · bones and claws (112,22,32) · horns (255,224,160), membrane (255,124,52) with
inner (204,64,40), gold (255,204,64) · iris (255,176,30). Face: lovely-fierce eyes with slit pupils and 2 highlights, a
10° brow, a smirk with 1 fang. Hero set: a gold crown band between 3-segment curved horns; back spikes with gold tips;
2-tone scalloped wings; ember and tail-flame VFX. Avoid: neon fire, slit-only eyes, a skinny neck.

**ShadePanther** (T5 Void, quad fierce-sleek). A long low feline with a big cat head, tall ears and a thick tail
curling up at the end. HW 0.95 TW, HH 0.80 TH, legs 0.65 TH, 0.34 TW, tail root 0.25 TW. Palette: indigo-violet
(60,48,100) · muzzle, belly and socks (124,108,182) · rosettes and nose (28,22,48) · crystals (190,130,255)/
(236,200,255) · iris (186,116,255). Face: almond wedge eyes with a light rim (dark-face rule), slit pupils, 2
highlights, 3 whisker bars per side, a small fang. Signature: rosettes of 4 dark plates around 1 mid-tone plate;
crystal clusters on both shoulder blades and the tail tip; wisp VFX at the paws. Avoid: monotone navy with pink
squares, a dog head, stick legs.

**NightmareStallion** (T5, quad fierce). An arched thick neck (W 0.6 TW), a long horse head (length 0.9 TH, HW 0.60 TW
= horse exception), legs 0.85 TH by 0.32 TW. Palette: indigo (52,42,88) · blaze and muzzle (152,132,222) · hooves
(24,18,40) · mane (170,90,255) → (232,176,255) · iris (236,96,206). Face: a fierce glare with a light rim, 1 highlight,
flared nostrils, a star blaze. Signature: a mane of 6-7 overlapping blade blocks tilted 35°, 2-tone; a tail cascade of
4 blades; light feathering plates at the hooves with smoke/wisp VFX. Avoid: the pale duck-bill muzzle box, spiky tail
balls, stilt legs.

**BlackDragon** (T5 top, eastern serpent flyer). A 10-14 segment tube (D tapering 1.0 → 0.35) in an S-curve
(amplitude 0.6 D), floating 1.2 D up, with 4 short legs and 3 gold talons each. The head is 1.8 D wide and 2.4 D long
with an open jaw. Palette: ink-indigo (40,34,64) · lilac belly (132,112,184) · (18,14,30) · gold (255,200,70) on
antlers, whiskers and talons; mane (160,96,255)/(220,170,255); pearl (236,226,255) · iris (255,200,60). Face: fierce
with slit pupils, heavy brows and 4 fangs. Signature: gold antlers (beam 0.18 D, 1 branch each) and 2 thick drooping
3-segment whiskers; a violet flame-blade mane from neck to tail; "diamond" scale plates with a light belly band per
segment; a pearl in one front claw; wisp VFX. Avoid: a lizard on stick legs (current), straw antlers, pure black.

**PharaohAsparuh** (SECRET Void, Persian cat in a sphinx pose). Lying down: belly on the ground, front paws stretched
forward (0.6 TL), round haunches, the tail curled along one side, chest up and a huge fluffy upright head (HW 1.15 TW,
45 % of H, TL 1.3 TW). Palette: cream fur (250,244,236) · shade (226,214,200) · kohl (34,26,40) · gold (245,196,60),
lapis (40,80,200), turquoise (40,200,190), nose (240,150,170) · iris (240,150,40). Face: a flat Persian face with big
regal half-lidded eyes, kohl wing bars (0.08 HW, 15° up), 2 highlights, a tiny pink nose, a "w" mouth and blush. Hero
set: a nemes cap of alternating gold and lapis stripes (0.6 cell) with flaps falling past the chin; a gold uraeus with
a red gem; a 3-band usekh collar (gold, turquoise, gold) with drop gems; a fluffy cheek ruff of 6-8 tapered blocks;
sparkle and wisp VFX. Avoid: an angry face, a slim body, a standing pose.

**SolarLion** (T6 Celestial, quad majestic). A big head framed by a sun mane (radius 1.5 HW): an inner ring of
8 rounded orange blocks and an outer ring of 12-16 gold rays alternating long and short. Stocky body, legs 0.65 TH by
0.38 TW; HW 0.95 TW, HH 0.85 TH. Palette: gold fur (240,180,70) · muzzle, belly and paws (255,236,190) · nose and tail
tuft (120,60,30) · mane (255,140,40), rays (255,214,80) with tips (255,248,200) · iris (230,120,20). Face: bold eyes,
10° brows, a broad muzzle with 2 small fangs. Signature: the two-ring mane (≥ 0.3 HW deep); a gold diamond sun emblem
on the forehead; a sun-shaped tail tuft; sparkle VFX. Avoid: the flat square mane plate, thin legs, one orange slab.

**Griffin** (T6, winged quad). An eagle head with a big hooked beak, a feathered chest ruff, lion hindquarters and
large layered wings. HW 0.90 TW, HH 0.85 TH, legs 0.70 TH: eagle forelegs with talons, lion hind paws. Palette: white
(246,246,250) · shade (210,214,230) · talons (40,40,50) · lion gold (226,160,70), beak (255,196,50), wings white → sky
(120,170,255) → royal (60,90,220) with gold tips (255,206,70) · iris (255,170,30). Face: fierce-noble with a heavy 20°
white brow ridge and ear tufts. Signature: 3-row feather wings (§2d); a "shingle" chest ruff pointing down (ref_09);
gold primary tips; sparkle VFX. Avoid: stick feathers, thin legs, a bland white box head.

**CelestialDragon** (T6 top, winged quad). A majestic S-neck (0.9 TH), a crown of 4 horns, broad membrane wings and a
long tail ending in a crescent-moon blade. HW 0.95 TW, HH 0.85 TH, legs 0.65 TH. Palette: pearl (232,236,255) · shade
(190,200,240), belly (255,226,150) · (40,48,110) · royal blue (60,90,220) → membrane (120,160,255), gold (255,200,60) ·
iris (60,120,230). Face: fierce-majestic, 2 highlights, gold brow plates. Signature: constellation patterns of gold
1x1 plates on the wings and back; gold trim bands with rivets on the neck; the crescent tail blade; 5 small floating
gold stars on an "Orbit" bone; sparkle VFX. Avoid: all-white with no blue contrast, neon.

**Cvetibara** (SECRET Celestial; the approved lovely V2 capybara rebuilt in blocks). A loaf body (TL 1.4 TW), a huge
head (HW 1.0 TW, HH 0.95 TH, length 1.2 HW) with a blunt square snout, tiny legs (0.40 TH), a floating halo and a
flower on the head. Palette: caramel (214,140,80) · snout and belly (240,190,140) · nose and feet (90,50,40) · wings
white (250,250,255) → gold tips (255,206,70), halo gold, flower (255,150,200) with centre (255,230,120), blush
(255,140,160) · iris (110,80,220). Face: lovely lilac-glint eyes with 2 highlights, blush, small round nostrils. Hero
set: a halo ring of 8 gold blocks; a pink star-lotus flower; 4 gold star plates on the back; 3-row white-to-gold
feather wings; sparkle VFX. Avoid: dense rough plates (use fill .45 and the softest rounding), neon trim.
