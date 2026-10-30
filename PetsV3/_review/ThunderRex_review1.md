# Thunder Rex - art director review 1 (2026-10-14) - REJECT

**Score: 3/10 for a 1% SECRET.** It would only just pass as a common. The owner is right. The anatomy base is
fine, but nothing in the colour, silhouette or face says "jackpot". It is also the greyest, least saturated pet
in its own egg.

Looked at: `ThunderRex/renders/_model_sheet.png` and `_close_sheet.png`, `pets/ThunderRex.py`, the owner refs
(f_56/61/66/67/70/71 + contact sheet) and our own approved pets (`_ALL_FIERCE_progress.png`, `_icons_sheet.png`,
plus the model sheets of Raiju, StormWyvern, ThunderBull, Cerberus, Ivonrath, BlackDragon, CelestialDragon, SolarLion,
Griffin and MoltenBoar).

---------------------------------------------------------------------------------------------------------------------
## 1. Why it looks cheap (specific)

1. **One flat grey colour = "unpainted plastic".** BODY (98,106,140) covers about 90% of the surface. A rough pixel
   count puts 80-89% of the visible body in ONE mid-value band (back and side views), with a median saturation of
   0.32. Raiju's is 0.47-0.54. The siblings are ThunderBull (98,108,178), Raiju (80,102,182) and StormWyvern
   (96,90,166), so the 1% secret is the dullest pet in the Storm egg. BODY_D only appears on a 0.03-thick saddle
   strip, the brows and the toes. The pale belly is ~1.5% of the side view. With no dark/mid/light structure, the
   studs become the main thing you see, which is what makes it look like a LEGO-grey toy.
2. **The accent is recycled and tiny.** The flank lightning is Raiju's flank-stripe code (`pets/Raiju.py` L131-140:
   the same 4-point Z, the same ~0.055 width) recoloured to ThunderBull's cyan. To a player it looks like a remix of
   two commons. The accent covers only 5-7% of the pixels. The small Z's on the tail read as tick marks or seagulls
   in model_side. All of them are flat decals that ignore the anatomy.
3. **The signature feature is under-played.** The owner's line was "T-rex, crackling back spines". The spines are
   0.13-0.21 long, laid back 64-80 deg (almost flat), and only the top 45% is cyan. In the back views they read as a
   row of little saw teeth, the same size as Raiju's hackles, MoltenBoar's crest or Ivonrath's crest blades. There is
   no step up in tier.
4. **No hero piece.** Every secret has one: Ivonrath has the gold crown band, PharaohAsparuh the headdress,
   Cvetibara the blossom. Even the commons have more: SolarLion's 12-ray sun wheel, CelestialDragon's 4-horn crown
   and floating stars, BlackDragon's gold antlers and pearl. Thunder Rex has two hornlets the size of cat ears.
5. **The silhouette reads "long grey lizard".** It is about 3.5 long by 1.62 tall (2.2:1). The tail is ~45% of the
   length, thin, straight, and fades to a point. The body is narrow (chest hw 0.25). The in-game camera sees it
   from above/behind, which shows a thin stick with dots. In a square 64 px Index portrait it shrinks to a thin
   horizontal line. From the front it is a narrow tower on stilts.
6. **The face doesn't work, especially from the front.**
   - The eyes are buried. The snout top (z ~1.495) is higher than the eye slits (z 1.462), and the snout half-width
     (0.145) matches the eye spacing (x +-0.14). From the front the eyes disappear behind the snout.
   - The front view is a flat studded box with two black nostril dashes on top. Those dashes read as a second pair
     of sleepy, closed eyes, which looks dopey, not fierce.
   - The brows are two separate rectangular slabs. They read as goggles or a visor, not a heavy angry brow.
   - The snout barely tapers, so skull, jaw muscles and neck look like three stacked boxes.
   - The lip line is straight, with a dark plank under it (BODY_D seg) that reads as a separate shelf. Under that
     hangs an even "picket fence" of six equal teeth per side.
7. **The legs are thin.** Shin hw 0.085 and metatarsus 0.07 are thinner than Cerberus's legs, on a much heavier
   animal. The feet are small. The legs are all BODY colour, so there are no dark "socks" to frame the pet (Cerberus,
   CelestialDragon and MoltenBoar all use them).
8. **There is no material contrast.** The kit has one material, so studded vs smooth is the only "material" we can
   show. Here everything is studded except teeth, claws and eyes. There is no glassy crystal against a studded hide.

**Keep:** the anatomy base (drumstick thighs, digitigrade legs, tiny arms, rising belly line), the rig and bone
names, the stud pitch approach, the cyan-eye idea, and the two-tone spine idea. There is lots of triangle headroom
(4.5k used of 15k).

---------------------------------------------------------------------------------------------------------------------
## 2. Redesign brief - "THE STORM KING"

**Concept:** a storm-black armoured tyrannosaur. Glowing cyan seams split its armour shells, a ridge of white-hot
crystal shards runs down its back, it wears a lightning crown, and its tail ends in a thunder-blade. ("Rex" = king.)

**Family rule:** same blockkit, same stud skin, same eye/brow/fang language as the approved pets. Each change below
names the existing pet and file to copy, so it reads as one of ours, just the top of the tier.

### Palette (Blender values; in-game is about x0.6)
| role | Blender RGB | in game ~ | where | target share of visible area |
|---|---|---|---|---|
| ARMOR | (44, 50, 112) | (26,30,67) storm-black navy | back/tail shells, skull cap, brows, nape, thigh plates, shin guards, feet, horn bases | 35-40% |
| HIDE | (76, 88, 200) | (46,53,120) deep storm blue | core body under the shells, flanks below the armour, neck/leg sides (brightest ch. 200 >= 170 OK) | 25-30% |
| BELLY | (176, 196, 240) | (106,118,144) silver-ice | throat, chest keel, belly scute strip, jaw underside, tail underside, inner thighs | ~10% |
| DEEP | (34, 110, 230) | (20,66,138) | crystal roots (armour -> crystal transition) | ~3% |
| CYAN | (60, 214, 255) (= current BOLT) | (36,128,153) | crystal mid sections, seams, eyes, core | ~10% |
| HOT | (215, 250, 255) | (129,150,153) | crystal tips, seam centre lines, eye hot spots, core centre | ~4% |
| GOLD | (255, 196, 50) (= BlackDragon GOLD) | (153,118,30) | crown circlet + core rim ONLY | <= 2% |
| MOUTH | (40, 26, 80) dark indigo + a small CYAN throat block | | open-mouth interior (reads "charged", not red) | - |
| BLACK (14,14,22), CLAW (22,22,34), TEETH (238,234,220) | | | sockets, nostrils, pupils / claws / teeth | - |

The DEEP -> CYAN -> HOT steps along every crystal are our "no-Neon glow": the eye reads it as light.

### The 10 changes, ordered by impact

**1. Palette and value blocking (biggest single win).** Apply the table above. The structure: a dark armour top, a
storm-blue hide showing at the flanks and in the gaps, a silver underside, and bright crystals on top. Leaving the
current colours and only adding parts will NOT fix this. The Cerberus "dark socks / rust points" and ThunderBull
"dark cape over a lighter body" region blocking (`pets/Cerberus.py`, `pets/ThunderBull.py` L103-115) are the
in-house precedents.

**2. The storm ridge: crackling crystal back shards (the owner's "back spines", the main silhouette feature).**
Replace the 9 + 4 small spines with:
- A **centre row** of 10-11 shards from the back of the skull to Tail3. Height profile: 0.20 at the nape, peaking
  at **0.36-0.42 over the shoulders** (Chest y ~ -0.2), 0.26 at the hips, 0.12 at Tail3. Base 0.07-0.08 along the
  spine, 0.045 thick. Laid back only 25-35 deg from vertical (now 64-80, which flattens them). Every second shard
  is **kinked like a bolt**: chain a second spike off the first one's 60% point, offset 25 deg.
- **Side rows** (left/right pairs) from the neck to Tail2, at 0.55x the centre height, splayed 25-30 deg outward and
  offset by half a station. From behind (the game camera) they form a W-shaped crystal fan along the back.
- Each shard in four steps: ARMOR socket (bottom 25%, studded, seated in the shell) -> DEEP -> CYAN -> HOT tip
  (top 20%). Every crystal part nostud=True.
- Copy: Ivonrath's two-row `crest()` (`pets/Ivonrath.py` L112-124, rows L242-247) and MoltenBoar's two-tone
  `spike2()` with buried root (`pets/MoltenBoar.py` L78-88). Extend both from 2 stacked parts to 4.
- Note: `B.poly` fans from pts[0], so a zig-zag outline must be star-shaped around it. Build bolts from chained
  spikes or bars instead.

**3. The storm crown and horns (the secret's hero piece; the head becomes the top of the silhouette).**
- Two big **3-segment back-swept horns** from the rear corners of the skull: ARMOR, ARMOR, then a CYAN spike with a
  HOT tip. About 0.45 long, rising so the tips sit ~0.15 above the shoulder shards. Copy CelestialDragon's upper
  horns (`pets/CelestialDragon.py` L228-235) or Ivonrath's horns (`pets/Ivonrath.py` L229-234).
- Two **lower side horns** out of the jaw hinge, swept back, to widen the head from above and from the front. Copy
  CelestialDragon's Q horns (L236-239).
- Between the horns, a **GOLD circlet** across the skull behind the brow with **5 crystal lightning prongs** (heights
  0.10/0.15/0.20/0.15/0.10, CYAN with HOT tips, the centre one kinked). Copy Ivonrath's crown band
  (`pets/Ivonrath.py` L235-240): it is our established "secrets wear crowns" language.
- Optional stretch, only if the head still reads as a T-rex: an upper-half sunburst of 5-7 lightning shards laid
  back 35 deg behind the crown, using SolarLion's ray wheel (`pets/SolarLion.py` L169-178 + `ray_dir/ray_R`
  L52-66). It matches the "Eternal" lightning-mane refs f_56/f_66.

**4. Head rebuild: a fierce T-rex skull with eyes you can see.**
- **Snout:** taper to ~65% width at the nose (hw 0.145 -> ~0.10). Slope the snout top DOWN ~12 deg from brow to
  nose, so at the eye's y it sits >= 0.03 BELOW the eye slit (today it is 0.03 above). Add 3 small ARMOR nasal
  bumps along the ridge.
- **Eyes:** use Ivonrath's `fierce_eye()` (`pets/Ivonrath.py` L93-110: socket, accent slit, hot spot, reptile pupil
  and brow in one call) with CYAN/HOT. Set sc ~1.3 and yaw 25 so both slits read in the front view.
- **Brow:** one heavy ARMOR brow per side, angled 20-22 deg down toward the middle, so the pair meets in a V above
  the snout ridge. Overhang 0.02-0.03. No floating goggle slabs. The Raiju brow is the reference (`pets/Raiju.py`
  L72-81).
- **Nostrils:** small black blocks at the FRONT corners of the snout tip. Delete the two dashes on top of the snout.
- **Mouth:** make the lip line step down ~0.03 toward the back (a snarl) and remove the dark upper-lip plank. Teeth
  per side: upper 2 fangs (0.11, 0.09) plus 4 graded (0.07 -> 0.045) at varied angles (+-8 deg), lower 4. Copy the
  idea of Ivonrath's interlocking lips (`pets/Ivonrath.py` L200+). Rest-pose jaw open ~6 deg so the teeth and the
  indigo mouth show.
- **Mass:** about +20% head volume, mostly height at the back and width at the jaw hinge (cheek muscles hw 0.05 ->
  0.075). The head should be a wedge from the front. Add 2-3 ARMOR cheek spikes per side with CYAN tips, swept back
  from the jaw hinge (Raiju cheek ruff `pets/Raiju.py` L82-86).

**5. Armour shells with lightning seams (these replace ALL the zig-zag stickers).**
- Over the chest, waist and hips put 3 ARMOR shells, plus a nape shell and 4 tail shells (one per tail bone). Each
  covers the top and upper flanks, with jagged armour teeth along its lower edge hanging over the HIDE. Copy
  MoltenBoar's `shell()` and `side_pt()` (`pets/MoltenBoar.py` L46-67) and its shell loop with rock teeth
  (L105-120).
- Fill every 0.04-0.05 gap with a flush **CYAN band**: lightning glowing through cracks in the armour, the f_71 lava
  look done in our style. Copy MoltenBoar's magma gaps and LavaGolem's `band()` (`pets/LavaGolem.py` L89-91). From
  above, the tail then reads as dark segments with cyan rings, which carries at any distance.
- Add 2 short branching cracks per flank running out of the gaps, using MoltenBoar's `crack()` (L70-75) or
  LavaGolem's `seam()` (L82-86). Give the biggest one a HOT centre bar.
- Delete `zig()` and all its call sites (flanks, thighs, tail).

**6. Chest storm core: a front focal point and VFX anchor.**
- Copy LavaGolem's molten heart (`pets/LavaGolem.py` L108-116): a broken ARMOR socket of 3 rotated plates, a CYAN
  diamond, a HOT centre, ~0.14 across, on the upper chest under the throat, with a thin GOLD rim.
- Run 2 seams from the core up over the shoulders into the ridge (LavaGolem L117-122), so the core visibly "feeds"
  the spines.

**7. Proportions: more compact and heavier up front.**
- Length:height goes from 2.2:1 to ~1.6:1, measured to the crown tips.
- Tail: shorten ~15% (end y 2.06 -> ~1.80). Thicker, taller base (hw 0.19 -> 0.23). It should slope down less, with
  the last two segments curling up 10-15 deg.
- Torso: chest hw 0.25 -> 0.29 and hips 0.215 -> 0.25, so it looks massive from above and behind. Pitch the chest
  nose-up another 6-8 deg and raise the neck so the skull top sits ~0.15 higher.
- The head ends up at ~22-25% of the total length (now 19%). That is still real T-rex anatomy, not chibi.
- Size: keep the in-game top (crown tips) at ~9 studs at x1. Update H_MODEL to the new top so PITCH recomputes and
  the studs stay the same size as the siblings'. Stay within ~18-20 studs at x2.2.

**8. Legs: massive, armoured, planted.**
- Thigh 0.165/0.245 -> 0.20/0.28, with an ARMOR thigh shell on the outside and a cyan seam along its lower edge.
- Shin hw 0.085 -> 0.115 and metatarsus 0.07 -> 0.095, with an ARMOR shin guard. Shin, metatarsus and feet in ARMOR
  form the dark "socks" (Cerberus `pets/Cerberus.py` L166+, CelestialDragon "dark socks" L253+).
- Foot pad 0.095 -> 0.12, toes hw 0.026 -> 0.036, claws +30%, plus one backward spur spike on each ankle.
- Stance x 0.23 -> 0.27, so the front view is an A-shape instead of stilts.
- Arms: keep them tiny but thicker (0.042 -> 0.055), with ARMOR forearms and 2 longer black claws.

**9. Tail hero tip: a thunder-blade.**
- A flat side-view lightning blade: 3 chained flat segments zig-zagging, ~0.32 long, ~0.10 tall, 0.04 thick, plus
  2 small side shards. Colours run ARMOR socket -> CYAN -> HOT tip. Copy CelestialDragon's crescent tail blade
  (`pets/CelestialDragon.py` L277-308) and its `Flame` anchor bone (L349). Raiju's bolt tip (`pets/Raiju.py`
  L149-151) is the simple version.
- This gives the long tail an ending (like Ivonrath's spade or f_71's fire tip) and a place to attach VFX.

**10. Material contrast and cleanup.**
- Studded: ARMOR, HIDE, BELLY. Smooth (nostud=True or role "detail"): every DEEP/CYAN/HOT part, GOLD, seams, teeth,
  claws, eyes. Glassy crystal against studded armour is the only material contrast the kit can make, so use it
  everywhere.
- Remove: the 0.03 dark saddle, the invisible belly grooves, the two cat-ear hornlets (the crown replaces them) and
  the small BODY_D cheek spikes. Replace the belly grooves with a broad silver scute strip with band gaps that shows
  in the side view (CelestialDragon `pets/CelestialDragon.py` L179-186).
- Budget: expect ~10-12k tris. If it goes over 15k, drop the side-row shards on the tail first, then on the neck.

### Studio VFX plan (VFX Studio plugin per owner rule; the mesh must look great without it)
Please add empty anchor bones, as CelestialDragon has its Breath/Flame anchors: **Crown, Core, Breath (mouth), Bolt
(tail blade), Ridge1-3 (the three tallest shoulder shards).**
1. **Ridge (signature):** arcs jumping between neighbouring shard tips (lightning beams, random flicker), cyan sparks
   rising off the ridge, and a soft glow strip along it. This is the show-off effect (the "crackling back spines").
2. **Crown:** sparks crackling between the 5 prongs and the horn tips. Hero option: a tiny storm cloud hovering
   above the crown that strikes it every 4-6 s (flash plus a PointLight pulse).
3. **Core:** a pulsing cyan PointLight that lights the chest and pools on the ground, plus a glow sprite.
4. **Eyes:** a small cyan glow with faint trailing wisps.
5. **Breath:** a few sparks dripping from the jaw at idle; a lightning breath beam in the roar.
6. **Bolt (tail tip):** a crackling ball/burst, like f_71's tail fire.
7. **Footsteps:** a spark ring and small shockwave on each step (walk events).
8. **Secret aura:** the same faint sparkle aura the other secrets use, so all secrets share one rarity language.
If the coordinator wants more pop in game, add PointLights on Core, Crown and Ridge. Do not add Neon to the mesh.

---------------------------------------------------------------------------------------------------------------------
## 3. Approval checklist for v2 (each item pass/fail; all must pass)

1. **Lineup test:** at the same scale, model_tq next to Raiju, ThunderBull, StormWyvern, Ivonrath, SolarLion and
   CelestialDragon. It is clearly the most striking, and does NOT read as a Raiju or ThunderBull remix.
2. **64 px test:** downscaled to 64 px (and as the Index icon on the slate background), you can name three things:
   a T-rex, a crown, a glowing back ridge. If the dark armour merges with the slate background, lighten ARMOR
   toward (56,64,140).
3. **Value blocking:** model_side and model_back show three bands (dark armour top / storm-blue hide / silver
   underside). No single colour is over ~45% of visible pixels. Mid-tone saturation median >= 0.45 (now 0.32).
4. **Accent:** the crystal family (DEEP/CYAN/HOT) is >= 15% of visible pixels in tq and back (now 5-7%). Every big
   shard shows the DEEP -> CYAN -> HOT steps. There are zero flat zig-zag stickers.
5. **Silhouette:** crown/horn tips are the highest point. The ridge peaks at >= 0.30 over the shoulders.
   Length:height <= 1.7:1. The back view shows the W shard fan and a wide body (chest hw >= 0.28).
6. **Face (close sheet):** from the front both eyes sit above the snout line under a V brow, and nostrils are at the
   snout tip only. From the side: a stepped, downturned lip, 2 big fangs per side, irregular teeth, no plank lip.
7. **Legs:** front view A-stance, shins >= 0.11 hw, dark armoured feet, long claws. No stilts.
8. **Hard rules:**
   - Studs on armour, hide and belly; crystals, gold, teeth and claws smooth.
   - No Neon or glow; <= 15k tris.
   - Real T-rex anatomy: head <= 25% of length, belly line rising from chest to hips.
   - No floating parts: every shard and prong sits in a socket.
   - No detail under 0.02 units.
9. **Family fit:** uses our `fierce_eye`/brow/fang construction. The stud pitch matches the siblings. HIDE's
   brightest channel is >= 170 (the 0.6x rule).
10. **Deliverables:**
    - model sheet
    - face close sheet
    - one above-and-behind render at ~35-40 deg elevation (the in-game camera)
    - a 64 px strip with the Storm egg siblings
