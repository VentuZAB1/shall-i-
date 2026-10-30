# Cosmic Leviathan - plan review (2026-10-14) - CONCEPT APPROVED; PALETTE, HERO, ACT and S-CURVE REVISED

**Verdict: build v1 to this brief.**

**Keep from the plan:**
- the concept: a legless, floating sky-sea leviathan
- the Tube hull, the fish rig and the bone names
- the 3-band idea
- the underbite face
- the pectoral wing-fins as the signature, the 3 dorsals and the ventral scutes
- HEIGHT 10

**Replace:**
- **Palette A.** Its NOVA violet is 1° from the Black Dragon's mane, and its sapphire is the 8th blue body.
- **Both heroes.** H1 reads as Cvetibara's halo or the Orca's caged orb, and it is 1-px lines at 64 px. H2 alone is
  one thin spike.
- **The star-dot fins.** They are the Celestial Dragon's constellation wings.
- **STAR-EATER.** It repeats the Celestial Dragon's moon-swallow (same egg), the Orca's gulp and Rex's breath.
- **The S-curve.** The v0 hull test reads as a banana from the side and a bowling pin from the front.

**What I looked at:**
- your plan, `pets/CosmicLeviathan.py` v0 and `curveloft.py`
- `CosmicLeviathan/renders/_model_sheet.png` and `model_side.png` (3x crop)
- `_ALL_FIERCE_progress.png` and `_icons_sheet.png`
- the model sheets of CelestialDragon, SolarLion, Griffin, Cvetibara, BlackDragon, ThunderRex, AbyssalOrca and
  ThornbladeMantis
- the Orca and Rex 64 px strips
- the palettes of all 27 `pets/*.py`
- every review for ThunderRex (1-3), AbyssalOrca (1-4), ThornbladeMantis 1 and VenomBasilisk 1
- `LESSONS_ALL_PETS.md`, FIERCE_PLAN §6-7 (the act uniqueness table), `ANIM_REFERENCES_1014.md` and
  `studio/CreatureVFX.lua`
- owner refs f_70 and f_71
- a read-only query of the live place: the egg template colours and `IndexConfig` area colours

**How I measured:**
- Hue distances were computed in HSV against every palette constant in `pets/*.py`.
- Lum = 0.299R + 0.587G + 0.114B.
- Temp files were kept outside the project. Nothing but this file was written.

---------------------------------------------------------------------------------------------------------------------
## 0. Your five questions, answered

1. **Palette:** neither A nor B. Use my own **"NEBULA SOVEREIGN"**: obsidian armour, plum-nebula hide, ivory belly,
   and periwinkle-azure starfire, which is the game's own Celestial colour, plus a gold crown only. See §1. A's hide is
   NOT separate: it is 2° from Raiju, 8° from ThunderBull, 10° from Rex and 12° from the Celestial Dragon.
2. **Hero:** neither H1 nor H2. Use **H4 "COMET CROWN"**: the house gold coronet with a big swept-back gold comet
   horn and an azure ✦ star gem. It reads at 64 px as ~35-45 solid gold px. See §2.
3. **S-pose and size:** HEIGHT 10 is right, keep it. The S is wrong:
   - The v0 stations make a U (a banana or crescent, and the crescent is the Celestial Dragon's mark).
   - The front view is a bowling pin.
   - Use my station table in §3. Its rearing "?" neck + trough + flattening tail reads nothing like the Black Dragon's
     low horizontal wave.
4. **Fluke:** a **swallowtail fluke**, the twin-blade option. It has long, pointed, 42°-swept lobes, a deep V notch,
   and it steps obsidian → plum → azure → starlight point. No gold. See §4.3.
5. **Remixes:** 9 found (§6 table). Missing jackpot factors (§6): one fin-light language, the Celestial identity
   colours, a moving hero read in the idle, and a VFX package.

---------------------------------------------------------------------------------------------------------------------
## 1. PALETTE - "NEBULA SOVEREIGN" (decided)

**Why not A:**

| A colour | nearest existing (hue distance) | problem |
|---|---|---|
| HIDE sapphire (34,74,190), hue 225° | Raiju FUR 2°, Bull BODY 8°, Rex HIDE 10°, **CD BODY 12°** | the 8th blue body in a roster with Raiju, Bull, Wyvern, CD, Rex, Hammerjaw and BlackDragon; the egg already has a blue pet (CD) |
| NOVA violet (160,90,255), hue 265° | **BlackDragon MANE 1°**, Panther VIOLET 5°, Basilisk VENOM_DEEP 7° | violet crystals on a blue serpent with gold = the Black Dragon's exact palette; also the Shadow egg's wisp colour |
| ARMOR (24,26,48), lum 28 | - | in game ≈ (14,16,29): pure black, no visible studs, merges with the slate Index card (Orca rule: a dominant dark needs lum ≥ ~65) |
| STAR panels + white star studs | CelestialDragon wings (white constellation dots on indigo membranes) | same egg, same signature |

**Why not B:**
- Pale armour breaks the house 3-band rule (dark armour on top), and the game camera would see an ivory pet.
- The pearl repeats the Celestial Dragon's horns, and the cream repeats Pharaoh Asparuh.
- A gold belly merges with the gold crown.

**What anchors my choice: the game's own Celestial identity.**
- `IndexConfig` area 6 is gold (255,240,170) → periwinkle (120,170,255).
- `HatchClient` is white + gold (235,190,80), and the CelestialEgg mesh is white + ice (225,240,255).
- The Celestial VFX sparkles are (255,244,180) → (200,220,255).

So the Celestial secret glows **periwinkle-azure and gold**, the Orca precedent of "glow in your egg's colour".
**Plum** carries it: no Celestial pet is purple, it is the complement of gold, and purple + gold + ivory is the
classic royal scheme.

### Palette (Blender values; in game ≈ ×0.6)
| role | RGB | in game | where | target share |
|---|---|---|---|---|
| **ARMOR** obsidian | **(62, 62, 96)** lum 66 | (37,37,58) | skull cap, nasal plates, mandible plates, cheek-fin roots, saddle plates (nape → Tail4), wing-fin spars, dorsal roots, fluke roots | side 34-42 % · game 32-42 % · tq ≥ 28 % |
| ARMOR_D | (40, 40, 66) | | brows, lip line | ≤ 3 % |
| **HIDE** plum nebula | **(170, 54, 170)** hue 300°, brightest ch. 170 ✓ | (102,32,102) | flanks between the saddle and the belly, neck sides, snout sides and cheeks, wing-fin inner halves, dorsal mid-bands, fluke mid-thirds | side 22-32 % · game 18-28 % |
| **BELLY** ivory | **(244, 228, 192)** | (146,137,115) | chin, throat, ventral scutes, jaw underside | side 7-12 % · front ≤ 22 % |
| BELLY_D | (204, 182, 140) | | scute gap bars | - |
| DEEP | (66, 64, 214) hue 241° | | the 0.05-0.06 "bridge" step between HIDE and AZURE on every fin; gem facets | ~2-3 % |
| **AZURE** starfire | **(90, 148, 255)** hue 219° (the IndexConfig periwinkle hue) | (54,89,153) | fin outer halves, dorsal tops, fluke outer thirds, cheek-fin tips, eye slits, the ✦ gem | AZURE family (DEEP+AZURE+STAR): tq 12-18 % · game 14-20 % |
| STAR | (224, 234, 255) | | fin points, eye hot spots, gem centre, horn-tip spike | ≤ 3 % |
| **GOLD** | (255, 196, 50) | (153,118,30) | **the crown ONLY**: band, points, comet horn, gem bezel | tq 3-6 % · game ≥ 2.5 % · side ≥ 2 % |
| GOLD_D | (214, 150, 30) | | horn keel, band inner face, bezel rim | ≤ 1 % |
| IVORY | (240, 234, 214) | | tusks, teeth | - |
| MOUTH | (46, 16, 46) | | mouth roof and floor plates | - |
| BLACK | (14, 14, 22) | | pupils, nostrils | - |

- No role may exceed 45 % in any view.
- The crown is 100 % of the GOLD. Gold anywhere else (fin edges, tail rings, armour rims) dilutes the crown: that was
  Mantis lesson 1, where the costal stripes out-weighed the crown.
- **Studded:** ARMOR, ARMOR_D, HIDE, BELLY.
- **Smooth (`nostud=True` / role "detail"):** DEEP, AZURE, STAR, GOLD, IVORY, eyes. Glassy starfire against a studded
  hide is the material contrast.

### Sibling check (hue distance to the nearest saturated colours)
| mine | nearest | verdict |
|---|---|---|
| HIDE 300° | Nightmare MANE_D 17°, Basilisk VENOM 19°, Cvetibara MAG 28°, Panther VIOLET 29°, BlackDragon MANE 36°, **BlackDragon INK 53°**, **CD BODY 63°** | It sits in the gap between the Shadow violets and the magentas. The neighbours are ACCENTS on other-coloured bodies (a pink horse mane, a violet lizard frill, pink lotus petals), never a body colour. It is clearly red-violet against the Black Dragon's blue-violet. |
| AZURE 219° | Rex DEEP 3° (a 3 % crystal root), CD BODY 18°, Bull SCAR 20°, **Rex CYAN 26°** | It is a bright smooth accent (v 1.0) on a plum body, so it never reads as a blue BODY. It is clearly periwinkle against Rex's cyan. |
| ARMOR 240°, s 0.35 | Orca INK, Rex ARMOR, Hammerjaw ARMOR | Dark armour is shared family language (every secret has it). |
| GOLD | every secret's crown, Lion/Griffin accents | Crown-only use = the house "secrets wear gold" rule, not a remix. |

**Risk I accept, and the gate for it:** plum + gold is still "a purple serpent with gold" in a sentence. The Black
Dragon A/B test (checklist item 5) must pass.

---------------------------------------------------------------------------------------------------------------------
## 2. HERO - H4 "COMET CROWN" (decided)

**Why not H1 (armillary):**
- **64 px:** the icon frame is ~24 px per model unit. A 0.04 ring is 1 px, so the hero becomes 1-px gold lines
  (Mantis lesson: thin lines never read as a crown).
- **Remix:** at 64 px, gold rings over the head read as **Cvetibara's gold halo** (same egg). A gold cage around a
  glowing gem reads as **the Orca's lantern**.

**Why not H2 (comet horn) alone:** about 0.03 unit² of gold in a single line, ~15-18 px. It reads as a "spike", not a
crown, and as a cousin of the Mantis's gold cone.

**H4 = the house coronet + a comet horn + a ✦ gem.**
- Coordinates are model units (−Y forward); "w" = B.spike half-width, "hw/hd" = B.seg half-sizes.
- Head geometry is in §5. The skull top at the crown seat is ~z 1.385.

| part | geometry | colour |
|---|---|---|
| **Band** | A closed loop hugging the skull top behind the brow: front bar at y −1.00 (x ±0.17), back bar at y −0.84 (x ±0.17), side bars at x ±0.19 (y −0.84..−1.00), corner blocks. All at z 1.33-1.40, section 0.035 radial × 0.07 tall. Seat it on the skin with `surf_hit` (≤ 0.01 proud). The back bar is what the game camera sees (Rex fix 1: "close the circlet"). | GOLD; inner face GOLD_D |
| **Points** (6) | Front corners (±0.15, −0.99, 1.40) h 0.10; sides (±0.20, −0.92, 1.39) h 0.12, splayed 20° out; back corners (±0.15, −0.85, 1.39) h 0.09. All swept back 15°, w 0.030. | GOLD |
| **Comet horn** (the hero mass) | Root block `B.seg((0,−0.95,1.37), (0,−0.80,1.52), hw 0.055, hd 0.045, top (0.8,0.8))`, then a spike from (0,−0.80,1.52) along (0, 0.707, 0.707), length 0.22, w 0.045, then a STAR tip spike 0.05 long, w 0.02. Add a GOLD_D keel (w 0.018) under the full length. The tip lands at ≈ (0, −0.63, 1.70). | GOLD (+ STAR tip) |
| **✦ star gem** (the comet's head) | On a GOLD front plate (hw 0.075 × 0.02 × hz 0.06) at (0, −1.01, 1.38), facing forward and tilted 20° up. Centre (0, −1.025, 1.39). Four DEEP-rooted AZURE spikes (up / down / left / right in the gem plane), length 0.06, w 0.022. A STAR centre cube 0.035. The gem sits in front of the horn root. | AZURE / DEEP / STAR, GOLD plate |

- **Hierarchy:** the horn tip is the model top (H_MODEL ≈ 1.70) and the crown is the only gold.
- **64 px estimate:** the projected gold in the tq view is ≈ 0.07 unit², about 35-45 px, a solid band + blade. That
  is ≥ 3 % of the pet's pixels.
- **Game camera:** a gold ring all round the head, with the gold blade pointing back at the camera and lit from above.
- **Separation:**
  - It is not Rex's crown: Rex has kinked lightning prongs and twin horns.
  - It is not the Mantis's: the Mantis has a vertical cone.
  - It is not a halo, cage, crescent or ray wheel.
- **Rig:** `Crown` anchor = the gem centre; `Horn` anchor = the horn tip. Both are children of Head, with no moving
  parts.

---------------------------------------------------------------------------------------------------------------------
## 3. SILHOUETTE, PROPORTIONS, SIZE

### 3.1 What the v0 hull test shows (`_model_sheet.png`, 09:18)
1. **Side and tq: a U, a banana, a crescent.** The neck keeps rising straight into the head (no forward turn), and
   the tail keeps rising to its end, so there is only ONE bend. A crescent body is the Celestial Dragon's mark.
2. **Front: a bowling pin or penguin.** A small blue cap sits on a wide cream bib, because the belly band reaches
   `zhi −0.45`.
3. **The head is the loft's rounded end cap,** a sausage tip with no skull.
4. **No studs show.** It looks like vinyl. n 2.4 is too round. The Orca reviewer accepted the Tube *because* "n 2.6
   keeps the family's soft-box read".
5. **Bone splits:**
   - The armour band is ONE piece on `Spine`, spanning Chest → Tail2.
   - The belly band is ONE piece on `Chest`, spanning Neck → Tail3.
   - Both will tear in the first swim cycle.
6. **Artefacts:**
   - a crease at the neck/chest joint (side view, left)
   - a short vertical sliver under the saddle at mid-body (side render x ≈ 255, y ≈ 300)
7. **ARMOR** (24,26,48) is a flat black hole (§1).

### 3.2 New centreline (`curveloft` stations y, z, hw, hh)
The new centreline is a **true S**:
- ∩ at the front: the neck rears at ~50° and the skull turns forward to horizontal
- ∪ at the belly trough
- a gentle ∩ where the tail rises, then flattens into the fluke

The chest is deep and keeled, and the rear thins to a tall, narrow peduncle. Massive front, whip-thin rear: that
reads predator, not slug. Use **n 2.6**, seg 24.

| st | y | z | hw | hh | bone | note |
|---|---|---|---|---|---|---|
| N0 | −0.86 | 1.12 | 0.19 | 0.19 | Neck | loft start, buried under the skull back and the jaw hinge |
| N1 | −0.76 | 1.00 | 0.21 | 0.22 | Neck | |
| N2 | −0.64 | 0.84 | 0.25 | 0.27 | Neck / Chest | |
| C | −0.46 | 0.64 | **0.30** | **0.34** | Chest | max girth, deeper than wide; wing-fin hubs |
| M | −0.12 | 0.42 | 0.25 | 0.27 | Spine | |
| B | 0.22 | 0.36 | 0.20 | 0.21 | Spine | trough; **lowest point z 0.15** |
| T1 | 0.54 | 0.44 | 0.15 | 0.17 | Tail1 | |
| T2 | 0.84 | 0.56 | 0.105 | 0.13 | Tail2 | taller than wide from here on |
| T3 | 1.10 | 0.66 | 0.07 | 0.095 | Tail3 | |
| T4 | 1.32 | 0.71 | 0.045 | 0.065 | Tail4 | fluke root; the tail **flattens** (−13°) |

**Bends:**
- The turns at C, M and B are 20-24° over 0.3-0.35 of length. That is a bend radius ≥ 0.75, more than twice the
  local hh, so no rings fold on the inner side.
- Keep this rule if you tune: radius ≥ 1.5 × hh at every station.

**The skull is NOT the loft's end.** Build it as its own head tube with constant-y rings, like Orca `hull_tube`
(§5.1). The neck loft runs 0.06 into it.

**Joints:**
- Keep your JOINT_Y values for Neck, Chest, Spine and Tail1-3.
- Tail4 → 1.22; add Fluke at 1.32.
- Neck pivot ≈ N2, Head pivot at the throat ≈ (0, −0.80, 1.04), Jaw hinge ≈ (0, −0.90, 1.07).

### 3.3 Size: HEIGHT 10 (approved, do not change)
- The bounds are ≈ 3.0 long (chin y −1.36 → fluke tips 1.64) × 1.96 wide (fin tips) × 1.70 tall (horn tip).
- L:H = 1.76 (Orca gate ≤ 1.85).
- **In game at ×1: 10 studs tall, ~17.5 long, ~11.5 wide.**
  - That is the same height class as Rex, Orca, Mantis and the Celestial Dragon (all 10).
  - The fins and length give it the biggest footprint in its egg.
  - A 1 % secret must not be smaller than the 13 % Celestial Dragon, and going above 10 would only make the in-act
    fluke-up taller.
- H_MODEL is measured to the horn tip, so PITCH recomputes from 1.70 and the studs match the siblings' pitch.

### 3.4 The legless floating read, and the Black Dragon
- **Legless:** lowest point 0.12-0.16 (the B trough). Every fin tip stays at z ≥ 0.45 at rest, so nothing reads as a
  leg from the side. The hover shadow does the rest.
- **The Black Dragon** is a low, horizontal, legged wave with a small head and the head at body height. The
  Leviathan:
  - rears a tall "?" neck with a massive crowned head at the top
  - has a deep chest and no legs
  - has 2-m-span fan wing-fins and a swallowtail fluke

  Together with obsidian dominance and the azure fins, it separates. Checklist item 5 verifies it at 64 px.

### 3.5 Hull colour blocking (the 3 bands, split per bone, Orca precedent)
- **Saddle armour:**
  - Top `band()` with zlo **+0.25** (the upper ~40 % of the perimeter, so it shows as the top third in profile), from
    N1 to T4.
  - **One piece per bone,** plus extra breaks at mid-Chest and mid-Spine, so the plates are 0.22-0.35 long.
  - Leave **0.03 HIDE gaps** between plates. The armour reads as segmented scutes, not a wetsuit stripe.
  - The gaps are plum hide, NOT glow (Rex owns glowing seams).
  - The nape plates continue into the skull cap.
- **Belly:**
  - Bottom band zhi **−0.50** (the lower ~28 %), from the chin (head tube) through N0 → T2, one piece per bone.
  - BELLY_D gap bars (flush, 0.02 wide) every ~0.12 from N1 to T1. These are the ventral scutes; they break the front
    "bib".
- **HIDE** is the tube itself (the band between).

---------------------------------------------------------------------------------------------------------------------
## 4. FINS - one language for every fin: "CORONA FIN"
**Every fin follows the same code:**
- an obsidian (ARMOR) root or spar, studded
- a plum (HIDE) inner field, studded
- a thin DEEP bridge step (smooth)
- an AZURE outer field (smooth)
- a STAR point (smooth)

The light lives at the **outer and trailing edges**, like an eclipse corona. This is the Leviathan's own glow form:
- Rex has crystals and seams; the Orca has beads and veins; Cvetibara has a thin row of tip feathers.
- Here the outer half of a broad fan is lit.

**Construction rules:**
- No B.poly anywhere (Orca lesson). Build from tapered, bevelled B.seg panels.
- No zig-zag or kinked edges (Thunderbird owns lightning edges).
- No white dots or constellations (Celestial Dragon).

### 4.1 Wing-fins (signature): a "flying-fish fan", Fin_L/R + FinTip_L/R
**Hub:** (±0.28, −0.44, 0.56), seated on C's lower flank with `surf_hit`.

**Panels:** 4 panels fan backward from the hub. Azimuth is measured back from +x; e = elevation.

| panel | azimuth | e | length | root half-chord | tip ≈ (left side) | colours root → tip |
|---|---|---|---|---|---|---|
| P1 spar (leading edge) | 35° | 8° | 0.86 | 0.07 | (0.98, 0.05, 0.68) | ARMOR full length + STAR spike 0.06 |
| P2 | 50° | 7° | 0.76 | 0.09 | (0.77, 0.14, 0.65) | HIDE 0-50 % · DEEP 50-57 % · AZURE 57-100 % · STAR spike 0.05 |
| P3 | 65° | 6° | 0.62 | 0.09 | (0.54, 0.12, 0.63) | same split |
| P4 | 78° | 5° | 0.46 | 0.08 | (0.37, 0.02, 0.60) | same split |

**Panel build:**
- Thickness half 0.025 at the root → 0.6× at the tip; top taper (0.25, 0.6). Point tips.
- Offset the panels ±0.004 along the fin normal (the spar on top), so the overlaps never z-fight.
- The fan is closed for the inner ~60 %, and the outer ~40 % splits into 4 clean points: a manta / flying-fish read.
  It is not a bat wing (no wrist, no finger bones).

**Bones:**
- The HIDE halves ride `Fin_*`.
- The DEEP/AZURE halves ride `FinTip_*`. The FinTip pivot is on the spar at 45 % ≈ (±0.59, −0.22, 0.61), and the
  colour split sits on the bone split with 0.02 overlap.
- Add anchors `FinEnd_L/R` at the spar tips.

**Clearance:**
- P4's inner edge must stand ≥ 0.02 off the flank beyond 35 % of its length.
- Rest span = 1.96.
- Optional, only if the cosmic read is weak at 64 px: one ✦ (as on the crown, 0.08 across) on each fin's HIDE field
  near the hub. NOT dots.

### 4.2 Dorsal fins (3, falcate, swept 45-55°, NOT a sail, NOT ridge shards)
Each dorsal is 3 stacked tapered segs (chord shrinking, `top_shift` back), with thickness half 0.04 at the root →
0.022.

| fin | bone | root (y from → to, on the top skin) | tip | colour stack (by height) |
|---|---|---|---|---|
| D1 | Chest | −0.40 → −0.20 | (0, −0.10, 1.22) | ARMOR 0-45 % · HIDE 45-70 % · DEEP step · AZURE 75-100 % · STAR spike 0.04 |
| D2 | Spine | −0.04 → 0.18 | (0, 0.28, 0.98) | same (tallest relative fin, ~0.34) |
| D3 | Tail1 | 0.46 → 0.62 | (0, 0.74, 0.86) | same, ~0.24 |

- Add a flush AZURE trailing-edge bar (0.02 wide) on the HIDE section of each dorsal, so the light runs down the
  trailing edge, not only at the tip. That is what separates it from Rex's shard ramp.
- The gaps between dorsals are wide (≥ 0.2), so it never reads as a continuous sail (Basilisk).

### 4.3 Fluke: the swallowtail (decided)
**Root:** at T4 (1.32, 0.71).

**Each lobe, 3 segs + a point:**
- Leading edge from (±0.04, 1.30, 0.71) to the tip (±0.40, 1.64, 0.75), a 42° sweep.
- Trailing edge from the tip forward into a **deep V notch** at (0, 1.48, 0.71), so the tips trail 0.16 behind the
  notch.
- Chord 0.20 → 0.14 → 0.07 → point. Thickness half 0.03 → 0.015.
- Colours: root seg ARMOR, mid seg HIDE, outer seg DEEP step + AZURE, STAR spike 0.06.
- No gold. No fill at the notch (Orca fix 5: no knob).

**Bones:** Fluke (lobes) with anchors `FlukeL/R` at the tips.

**Why it is not a sibling's fluke:**
- the Celestial Dragon's crescent is a vertical moon-white blade
- the Orca's is a black/white crescent with green veins

### 4.4 Cheek fins (head width from the front and the game camera; replaces the optional gill-spines)
**One broad swept fin per side.** Gill-spine fans would read as Basilisk's frill, a Raiju ruff or "fingers"
(lessons #5).

**Build:**
- Root at (±0.19, −0.86, 1.14), behind the jaw hinge; tip at (±0.40, −0.62, 1.30).
- Seg 1: ARMOR, 0-55 %, half-chord 0.07 → 0.05, thickness half 0.015, studded.
- Seg 2: AZURE, 55-100 %, chord → 0.02, smooth.
- A STAR spike 0.05 at the tip. Head bone.

**Result:** the head reads ±0.40 wide from the front (the body is ±0.30), so the bowling pin is gone.

---------------------------------------------------------------------------------------------------------------------
## 5. HEAD (built at final size; must be fierce at 64 px and from behind and above)

### 5.1 Skull (head tube, constant-y rings, Head bone)
| y | zc | hw | hh | what |
|---|---|---|---|---|
| −0.80 | 1.22 | 0.17 | 0.15 | occiput (over the neck top) |
| −0.90 | 1.22 | **0.21** | 0.17 | jaw hinge / cheeks: the widest point, so the head is wider than the neck |
| −0.98 | 1.22 | 0.19 | 0.16 | brow and eyes (top 1.38) |
| −1.08 | 1.15 | 0.15 | 0.09 | snout root: **the brow step**; the snout top here is 1.24 |
| −1.20 | 1.13 | 0.12 | 0.08 | |
| −1.32 | 1.12 | 0.095 | 0.07 | snout tip |

- **Skull cap:** ARMOR top band (zlo 0.30) from −0.80 to −1.06, continuing the nape plates.
- **Snout and cheeks:** sides in HIDE.
- **Nasal plates:** 3 ARMOR plates on the ridge at y −1.12 / −1.20 / −1.27, hw 0.045 / 0.04 / 0.035, flush (0.008).
- **Nostrils:** BLACK slots at the snout-tip front corners (±0.05, −1.32, 1.16) only. No dashes on top (Rex v1
  "second pair of eyes").

### 5.2 Brows and eyes
- **Brows:** ARMOR_D bars from (±0.18, −0.93, 1.37) to (±0.05, −1.04, 1.31): 22° down toward the midline, w 0.05,
  thick 0.04, overhang 0.025. They meet in a **V** over the nasal ridge, and their back ends run into the crown's
  front corners, so the crown grows out of the scowl.
- **Eyes:** `fierce_eye` (Orca/Rex version), sc 1.2, yaw 25, centre (±0.155, −1.00, 1.29), seated with `surf_hit`.
  - AZURE slit iris, STAR hot spot, BLACK slit pupil ≤ 70 % of the iris height.
  - **No glint.** Mantis lesson: a glint plus a round pupil = googly eyes.
  - The snout top in front of the eyes (1.24) is ≥ 0.03 below the slit, so both eyes read in the front view.

### 5.3 Jaw: the underbite (Jaw bone, hinge ≈ (0, −0.90, 1.07), modelled 6° open, key = total − 6)
- **Lower jaw:** hw 0.21 at the hinge → 0.12 at the chin. Lip line at z ~1.06, bottom ~0.96. The chin juts to
  **y −1.36** (0.04 past the snout tip).
  - Outer sides: ARMOR mandible plates (flush). Underside: BELLY.
- **Tusks:** 2 at (±0.118, −1.31, 1.08), direction (0, −0.25, 1), length 0.11, full width 0.034, IVORY.
  - They stand OUTSIDE the snout side (hw 0.095 there), so they close clean.
  - Keep them ≤ 0.11 and straight, so they read as fangs, not MoltenBoar tusks.
- **Lower fangs:** 4 per side behind the tusks (y −1.24 … −1.04), 0.05-0.07 long, full width ≥ 0.026. They overlap
  the upper lip from outside, which is what makes the underbite.
- **Upper teeth:** 6 per side, 0.035-0.05 long, full width ≥ 0.024, inside the lower jaw rim. Offset half a pitch
  from the lower fangs and vary the angles ±8°, so there is no picket fence.
- **Mouth:**
  - A MOUTH roof plate under the snout (Head) and a floor plate on the Jaw (Rex fix C).
  - No glowing throat: that is Rex's "charged mouth".
  - Anchor `Mouth` at (0, −1.40, 1.06).
- **Throat:** BELLY from the chin into the scutes.

### 5.4 Reads to verify
- **64 px:** a heavy scowling wedge with a gold crown and blade on top, 2 azure slits and 2 white tusks.
- **Game camera** (35-40° from behind and above): the gold band ring + blade, the ARMOR skull cap, and the two
  azure-tipped cheek fins either side. The face is unseen, so from behind the fierceness comes from the crown and the
  fins.
- **Head length:** 0.52 incl. the jaw, ~18 % of the length. Fine for a leviathan; do not shrink it.

---------------------------------------------------------------------------------------------------------------------
## 6. Remixes removed, and the missing jackpot factors

| in the plan | remixes | replace with |
|---|---|---|
| STAR membranes with white star studs | **CelestialDragon** constellation wings (same egg) | the Corona-fin gradient (§4) |
| NOVA violet crystals (eyes, gem, dorsal tips) | **BlackDragon** violet back crystals (1°), **ShadePanther** violet crystal clusters, the Shadow wisp colour | AZURE / DEEP / STAR |
| sapphire + gold + violet as a whole | **BlackDragon**'s palette | §1 |
| armillary rings over the head | **Cvetibara** gold halo (same egg); **AbyssalOrca** gold cage around a glowing orb | the Comet Crown (§2) |
| chest NOVA star-core | **ThunderRex** chest storm core / LavaGolem heart | no mesh core; keep an empty `Core` anchor for VFX |
| gold-rimmed tail rings | ThunderRex's tail joint bands; and it dilutes the crown | plain ARMOR plates with plum gaps |
| gold fin leading edges (≥ 8 % gold) | dilutes the crown (Mantis lesson); edge-lit wings (Thunderbird) | ARMOR spars; gold = crown only, 3-6 % |
| STAR-EATER act | **CelestialDragon `act_eclipse`** "swallow the moon" (same egg); **Orca `act_lure`** gulp; **Rex `act_stormbreath`** (light runs along the body, then a breath); breath = Ivonrath/Rex only; the ring spin echoes **SolarLion**'s wheel | `act_sounding` (§7) |
| roar "rears up" | rear-up = **NightmareStallion** only (FIERCE_PLAN §7); Kraken rise | the Ripple Roar (§7) |
| swim "like the Orca's body/tail wave" | vertical fluke drive = **Orca**; lateral sweep = Hammerjaw | Manta flight (§7) |

**Jackpot factors to add or confirm:**
1. **Celestial identity on its skin:** gold + periwinkle, the exact Index-card pair. No other secret glows in its
   egg's Index colours this literally.
2. **The richest silhouette in the game:** crown + blade, a rearing S, 2-m fan fins, 3 dorsals, a swallowtail. From
   the game camera the fins and fluke face the camera with plum → azure → starlight.
3. **One owned light language** (Corona fins), repeated on 4 fin types. Consistency is what makes it read "designed",
   not "decorated".
4. **A moving hero read in the idle:** the fins "breathe" and the fin-edge glow event fires every loop (§7), so it is
   never a static statue behind the player.
5. **Material contrast:** studded obsidian and plum against glassy azure and polished gold.
6. **VFX package** (§8): the comet trail on the crown, fin-edge ribbons, Celestial sparkles and the secret aura.
7. **Index portrait:** the rearing S + spread fins ≈ a square. Raise the icon camera ~8° so the crown sits on the top
   edge (Rex note).

---------------------------------------------------------------------------------------------------------------------
## 7. CLIPS

**Owner rule:** pull and cite references BEFORE keying. Suggested:
- a humpback/whale **fluke-up sounding dive** (`/tags/creature-animation`, `/tags/liquid-and-water`)
- a **manta ray or flying-fish** flight (`/tags/flying`)
- the logged Sea Beasts #3 for the jaw-lag roar

**Kit signs:** + pitch = nose DOWN on body bones, + = tail UP on tail bones. Render one test pose to confirm before
keying (Orca review 4 sign bug).

### 7.1 Signature `act_sounding` - "COMET SOUNDING" (120 f, in place, ends exactly in rest)
**The story:** the crown ignites, then the leviathan arches and plunges head-first into the sky-sea like a comet. Its
swallowtail fluke towers behind it, shedding starlight, then slips down, and it resurfaces with a proud lift.

**Why it is unique:**
- It is the only act with a held tail-up dive.
- The Orca's see-saw is a 3-frame strike whip. The Celestial Dragon's tail arcs OVER its back to the front of the
  head. The Thunderbird's stoop is a folded-wing bird drop. The Hammerjaw slams its head.
- No breath, gulp, eating, spin, wheel, coil, rear, pounce or head shake.

| f | beat | keys (deg; Root loc in model units) |
|---|---|---|
| 0-14 | **rise & ignite** | Root z +0.06; Spine −5 (nose up), Chest −3, Neck −4, Head −8; Jaw +4 (a silent snarl); fins flap up 14 / FinTip +8; dorsals erect; tail sags (Tail1-3 −4/−6/−6). Event `ignite` f12 (Crown + Horn flare) |
| 14-22 | hold the breath | Root z +0.06→+0.07; fins hover |
| 22-40 | **the plunge** | Travelling wave head → tail, 3 f lag per bone: Head +18 (f26), Neck +10 (f28), Chest +6 (f30), Spine **+22** (f32); Root z → 0.0; Jaw shut by f28. Tail1 +14 (f34), Tail2 +20 (f36), Tail3 +24 (f38), Tail4 +22 (f40), Fluke +18 (f40): the fluke rises and turns to face back. Fins sweep back 30 and flap down 10 (streamlined). Event `plunge` f28 (Horn comet trail on). Ease in. |
| 40-70 | **FLUKE-UP** | Hold the arch. Two slow fluke swings (Tail4 yaw ±6, Fluke roll ±4; extremes f46 / f58). Head +2 more (it sinks). Events `starfall1` f48, `starfall2` f60 (stars shed from Fluke / FlukeL / FlukeR) |
| 70-82 | **the slip** | The fluke sweeps down past rest: Tail1-4 → −6/−8/−10/−8 at f80 (overshoot); Spine +22 → +6; Head +18 → +6. Event `splash` f78 (star ring at Fluke). Hard-ish stop at f80 |
| 82-102 | **resurface** | Counter-wave tail → head, 2 f lag: Spine −6, Chest −3, Neck −4, Head −8 at f96 (the crown lifts; Head+Neck ≤ 12° up here, never chin-to-sky = Raiju's howl). Two fin sculls ±12 (f86, f96). Event `glow` f96 |
| 102-120 | settle | rest, exactly |

**Targets:**
- At f50: the fluke root z ≥ 1.35 and the fluke plane ≥ 40° from horizontal, so from the game camera it rises into
  view above the dorsal line.
- Snout lowest ≥ 0.10; fin tips ≥ 0.05; ground_min_z ≥ 0.02.
- Root y within ±0.05; nothing sweeps sideways (footprint).

**Return:**
- a pose sheet at f12, f30, f40, f50, f60, f78, f96 (tq + side + game)
- `collision_free: true`, linear 0, ground_min_z

### 7.2 idle (120 f loop): "SKY DRIFT"
- **Base motion:**
  - heave z ±0.03 (2 cycles)
  - fins breathe ±8 (FinTip lag 4 f, ±5)
  - a tail micro-wave (Tail1-4 pitch ±2/±3/±5/±7, lag 0.08 cycle; Fluke ±8)
- **f20-62, look-around:** ONE slow look left (Head yaw +18, Neck +6 over f20-28, hold to f36), then ONE look right
  (f40-48, hold to f56), back by f62. That is ±24° total; never faster than ~40° per 8 f.
- **f70-90, crown glint:** Head −6, Neck −3, fins lift 6. Event `glow` f78 (Crown/Horn flare, fin edges brighten).
  This replaces the chest-core breath.
- **f92-112, fluke flick:** Tail3 +8, Tail4 +12, Fluke +16, then back with a small overshoot.
- No belly roll: that is the Orca's idle.

### 7.3 swim (36 f loop): "MANTA FLIGHT" (the wing-fins drive it)
- **Fins:**
  - Fin ±26°, FinTip ±16° lagging 4 f, so the wave runs out along the fin.
  - The power downstroke takes 45 % of the cycle.
- **Body:**
  - heave z +0.04 at the end of the downstroke
  - a low vertical wave down the body (Spine/Tail1-4 ±2/±4/±7/±10/±14, lag 0.08 per bone) in phase with the fins
  - Fluke ±10 lagging
- **Head and dorsals:** the head is stabilised (≤ ±2°) and the dorsals are rigid.

It is the only pet that flies on pectoral fins, so it never shares a cycle with the Orca (fluke drive) or the
Hammerjaw (lateral sweep).

### 7.4 roar (66 f): "RIPPLE ROAR" (replaces the rear-up)
| f | beat | keys |
|---|---|---|
| 0-12 | gather | Root z −0.05; Spine +4; Neck +6, Head +8 (chin tucks, Sea Beasts ref); fins fold back 18 / down 10; tail cocked down (Tail1-3 −8/−10/−12) |
| 12-24 | ripple | a lifting wave runs Fluke → Tail4 → … → Neck, 2 f lag, each bone −8 then back; Root z → +0.03; it reaches the head at f22: Head −10, Neck −6 |
| 22-28 | roar | the jaw opens from f24 to 40 total by f27 (a beat after the head lift); fins SNAP to max span (flap up 22, sweep forward 10); dorsals erect; event `roar` f26 (Mouth star shock-ring) |
| 28-50 | hold | jaw buzz ±2 every 3 f; fin tips quiver ±3; Tail4/Fluke shiver ±5 |
| 50-66 | release | jaw closes over f50-60; fins settle with an overshoot; rest |

- No rear-up (Stallion), no chin-to-sky (Raiju), no strike or bite (Black Dragon's S-coil), no downward roar at the
  viewer (Celestial Dragon). Root y within ±0.04.

### 7.5 Rig, anchors, pairs, limits
- **Bones:**
  - Root, Spine, Chest, Neck, Head, Jaw
  - Tail1-4, Fluke
  - Fin_L/R, FinTip_L/R
  - Dorsal1-3 (rigid, for the erect/fold key)
- **Anchors:**
  - Crown (gem) and Horn (horn tip), on Head
  - Mouth
  - Core (chest underside, empty)
  - FinEnd_L/R
  - FlukeL/R
  - Eye_L/R
- **check_pairs** (keep yours and add):
  - (Head, Dorsal1), (Neck, Dorsal1): the horn and cheek fins on pitch-up
  - (Fin_L/R, Chest), (Fin_L/R, Spine), (FinTip_L/R, Spine): P4 on the fold and the upstroke
  - (Fluke, Tail2), (Fluke, Dorsal3), (Tail4, Dorsal3): the fluke-up
  - (Jaw, Neck), (Jaw, Chest)
- **Joint capsules:** the jaw hinge, fin hubs and FinTip hinges.
- **Limits:**

  | joint | limit |
  |---|---|
  | Head+Neck pitch-up | ≤ 30° (at 30° the horn tip is still ≈ 0.5 above Dorsal1's leading edge) |
  | pitch-down | ≤ 30° |
  | Head yaw | ±22°, with Neck ±8° (the cheek-fin tips stay ≥ 0.3 above the chest) |
  | Chest vs Spine | ≤ ±6° (saddle plates, fin hubs) |
  | Spine (whole body) | ±25° |
  | Tail1-4 | ±18 / ±24 / ±30 / ±30 |
  | Fluke | ±25 |
  | Fin flap | +28 / −20, with tips ≥ 0.05 above the ground |
  | Fin sweep-back | ≤ 32° |
  | Jaw | ≤ 40° total (key ≤ 34) |

  Run `ground_lift()` (Kraken) in every clip.

---------------------------------------------------------------------------------------------------------------------
## 8. Studio VFX plan (VFX Studio plugin only, owner rule; no Neon; the mesh must look complete without it)
1. **Crown/Horn:**
   - an always-on short comet Trail from Horn (gold-white → periwinkle)
   - a soft glow at the gem
   - a flare on `ignite` / `glow`
2. **FinEnd_L/R, FlukeL/R:** thin periwinkle → white ribbon Trails in swim and act, plus sparkle motes off the fin
   edges.
3. **Act events:**
   - `starfall1/2`: falling ✦ sparkles from the fluke
   - `splash`: a star ring
   - `plunge`: the comet trail lengthens
4. **`roar`:** a starlight shock-ring from Mouth.
5. **Body:** the Celestial `sparkles` preset on Chest/Spine and Tail2-3 (as for the Celestial Dragon), the shared
   secret aura, and a periwinkle PointLight on Core (pulses on `glow`).
6. **Eyes:** a small periwinkle glow.
7. Add a `CosmicLeviathan` entry to `CreatureVFX.lua` PRESETS when the owner wires it (not now).

---------------------------------------------------------------------------------------------------------------------
## 9. v1 SIGN-OFF CHECKLIST (model round; each item pass/fail, all must pass)

1. **S-silhouette (side, 600 px):**
   - ∩ neck/head + ∪ trough + a flattening tail. No U or banana; no crescent read.
   - The horn tip is the model top (H_MODEL 1.70 ± 0.03).
   - Lowest point 0.12-0.16; L:H ≤ 1.8.
   - The head is a separate skull wider than the neck at the cheeks (hw 0.21 vs 0.19).
2. **Front view:**
   - fins visible to ±0.95-1.0 and cheek fins to ±0.40, so the outline is a T / manta
   - BELLY ≤ 22 % of the front view, broken by scute gaps
   - no bowling pin, no penguin bib, no sausage cap
3. **Game camera (35-40° from behind and above):**
   - the wing-fins and fluke face the camera with a visible plum → DEEP → azure → star gradient
   - a gold ring all round the head plus the blade
   - segmented armour plates with plum gaps, not one stripe
   - dorsals read as fins, not saw teeth
4. **64 px slate cut-out from the icon pipeline:** a strip with SolarLion, Griffin, CelestialDragon, Cvetibara,
   ThunderRex, AbyssalOrca, ThornbladeMantis and BlackDragon. I can name three things:
   - a crowned sea-serpent / leviathan
   - a gold crown with a blade (≥ 25 gold px)
   - glowing periwinkle fins

   It is the most striking icon of the Celestial row.
5. **Black Dragon / Celestial Dragon A/B:** a 64 px pair image (Leviathan next to BlackDragon, then next to
   CelestialDragon). They must not read as the same family: different value (obsidian vs mid-indigo), different
   silhouette (rearing + fins vs low + legs), different light (periwinkle vs violet crystals / white dots).
6. **Shares (flat palette-ID, side / tq / game / front):**

   | role | target |
   |---|---|
   | ARMOR | 34-42 / ≥ 28 / 32-42 / – |
   | HIDE | 22-32 / 22-32 / 18-28 / – |
   | BELLY | 7-12 / ≤ 12 / ≤ 6 / ≤ 22 |
   | AZURE family | 8-14 / 12-18 / 14-20 / – |
   | GOLD | ≥ 2 / 3-6 / ≥ 2.5 / – |

   No role > 45 % in any view. GOLD exists only on the crown.
7. **Face close sheet (front, side, tq at 700 px):**
   - a V brow over azure slit eyes, the eyes ≥ 0.03 above the snout line from the front, no glint
   - the underbite chin 0.04 ahead, 2 tusks outside the upper lip, interlocking irregular teeth (none under 0.024
     wide)
   - a dark mouth roof and floor, nostrils only at the snout tip
8. **Fins:**
   - no B.poly; tapered, bevelled panels
   - HIDE halves studded, DEEP/AZURE/STAR smooth
   - each wing-fin fan closed for the inner ~60 % with 4 clean points; no z-fighting at the overlaps
   - a swallowtail fluke with a clean V notch and no knob
   - no zig-zag edges, dots or constellations
9. **Hull:**
   - curveloft at n 2.6; studs visible on ARMOR, HIDE and BELLY at the sibling pitch
   - no creases or slivers at the joints (the v0 neck/chest crease and mid-body sliver are gone)
   - no ring folds on the inner bends
   - every band split per bone, plus the mid-Chest and mid-Spine plate breaks
10. **Remix sweep:** none of the following exist anywhere:
    - white star dots, crescents, violet crystals, a chest core gem
    - gold outside the crown
    - rings or halos, beads or veins
    - crystal shards, glowing seams or cracks
    - a dorsal sail
11. **Hard rules:**
    - no Neon; ≤ 12 k tris (cap 15 k)
    - nothing floating or buried (crown, gem, eyes, teeth and fins all `surf_hit`-seated)
    - no detail under 0.02 (the fierce_eye pupil excepted)
    - HIDE brightest channel ≥ 170; ARMOR lum ≥ 62
    - HEIGHT 10 to the horn tip
12. **Rig at rest and at the limits:**
    - `collision_free: true` at rest
    - 4 static limit poses render clean: Head+Neck +30 up; Head yaw 22 + Neck 8; fins +28 / −20 flap; the act's
      fluke-up pose (Spine +22, Tail +14/+20/+24/+22, Fluke +18) with fluke root z ≥ 1.35
    - all anchors from §7.5 exist
13. **Deliverables:**
    - a 600 px model sheet (tq / front / back / side / game) + a separate 600 px tq
    - the face close sheet
    - the 64/128 icon strip (item 4) and the A/B pair (item 5)
    - the flat-ID share table
    - the tri count
    - the 4 limit-pose renders

    Render the model views LAST: `headless_closeup` overwrites `model_tq` at 200 px.

**Clips come after this model gate:** `idle`, `swim`, `roar`, `act_sounding` as in §7, with the references cited in
`ANIM_REFERENCES_1014.md`. The act's pose sheet frames are listed in §7.1.
