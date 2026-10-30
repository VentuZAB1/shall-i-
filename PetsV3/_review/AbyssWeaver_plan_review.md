# Abyss Weaver - plan review (2026-10-14) - CONCEPT APPROVED; PALETTE, HERO, ROAR STAGING and ACT REVISED

**Verdict: build v1 to this brief.**

**Keep from the plan:**
- the concept: a void spider-queen, obsidian armour, 8 burning eyes, a crowned head, a gold-rimmed rift on the abdomen
- the 3-segment IK legs with knees arched above the carapace (`add_leg2` x 8)
- a gold crown on the ocular turret, IVORY fangs with BLACK tips
- the alternating tetrapod (L1 R2 L3 R4 / R1 L2 R3 L4), duty near 0.55-0.6, 32 f
- the threat display as the roar, and a weave as the signature act (both re-staged below)
- Motion "Walk", <= 12 k tris

**Replace:**
- **The palette.** Every colour in it sits 0-5° from a Void sibling: OBSIDIAN/CARAPACE = the Stallion's and the
  Panther's darks, VELVET = the Panther's VIOLET, the VOID violet = the Black Dragon's MANE (0°), MAGENTA = the
  Stallion's eyes (4°). At 64 px it reads as a black Panther recolour, and OBSIDIAN (lum 29) is a black hole in game.
  Use **"BLOOD ORCHID"** (§2).
- **The round R1 portal.** On the abdomen top facing up-and-back it is invisible from the portrait (tq) camera, and
  concentric DEEP/VIOLET/HOT discs with a black slit pupil remix the Mantis demon eye-spot and the Kraken rings.
  Use **R1b, the long VOID RIFT** draped over the abdomen's crest (§4.7).
- **Violet crystal bristles on the knees** (Shade Panther's crystal colour): use single obsidian **thorns** with
  orchid tips.
- **Magenta hourglass, gold claws, gold fang bases, palp grooming, the venom drip, the crossing weave strokes, the
  front-leg slam:** dropped or replaced (remix table, §1.2).
- **Abd1 + Abd2:** one rigid `Abd` + `Pedicel` + `Spinner` (a split abdomen creases on every bob).

**What I looked at:**
- your plan; `pets/ThornbladeMantis.py`, `pets/Kraken.py`, `PetsV2/pets/_common.py`, `blockkit.py`, `PetsV2/petkit.py`
  (`walk_cycle`, `gait_target`, `solve_leg`, `portrait`, `VIEWS`), `run3.py`, `icon3.py`, `_tools/pack_post.py`
- `_review/CosmicLeviathan_plan_review.md`, ThornbladeMantis reviews 1-4, `LESSONS_ALL_PETS.md`, FIERCE_PLAN §0 and §7
  (motif owners), `ANIM_REFERENCES_1014.md`, `studio/CreatureVFX.lua`, the InfernoPhoenix plan (no overlaps allowed)
- `_tools/_void_strip.png`, the Panther and Mantis model sheets, the Mantis and Void sibling icons
- the palettes of all 28 `pets/*.py` (hue table in §2.2)

**How I measured: a throwaway reviewer MOCK, built and rendered with the kit (nothing written into the project).**
- Mock module: `C:\Users\ventu\AppData\Local\Temp\weaver_rev\mock\AbyssWeaverMock.py` (palette "F" = this brief).
  It is a proportion study, not a build: read it for the abdomen/rift/shell helpers, take the NUMBERS from this file.
- Renders in `C:\Users\ventu\AppData\Local\Temp\weaver_rev\`. Open these first:
  - `sheet_F2.png`: the final layout at rest (tq / side / front / game / back)
  - `strip_F_64x3.png`, `strip_F_128.png`: the 64/128 icon strip (Weaver tq icon, Weaver game-cam icon, Panther,
    Stallion, Black Dragon, Pharaoh, Mantis, Kraken)
  - `strip_B_64x3.png`: the same strip with YOUR palette (the remix, side by side)
  - `sheet_A.png`: mock v1, the cute traps (ball abdomen, stilt legs, fang "U" smile, white belly grin, "hand" crown)
  - `sheet_pose2.png`, `sheet_pose4.png`, `sheet_pose6.png`: the rigged limit tests (roar raise, act presentation)
- Shares are flat palette-ID renders (the `headless_pack` method), gold pixels are counted on the icon3-style 64 px
  icon, hue distances are HSV against every palette constant in `pets/*.py`, Lum = 0.299R + 0.587G + 0.114B.
- Mock numbers: 11.9 k tris; bounds x ±1.05, y −1.10…+1.24, z 0…1.10; 64 px gold = **60 px** (portrait) and **80 px**
  (game cam).
- `overlap_report` on the rigged mock:
  - the final act pose (rift presented + L4 draw): 0 tri pairs vs the abdomen; 1-2 Leg1|Leg2 hip slivers, caused by
    the mock's too-close coxae (fixed in §4.9)
  - the FK roar raise: 3-6 tri pairs Leg1|Leg2 only (tunable)

---------------------------------------------------------------------------------------------------------------------
## 0. Your [DECIDE] items and §10 questions, answered

| # | question | decision |
|---|---|---|
| 1 | Rift R1 / R2 / R3? Crown too? | **R1b: a long gold-lipped VOID RIFT** along the abdomen's dorsal midline, draped over the crest (§4.7). It is the only hero shape that faces BOTH cameras: its front half faces the portrait (tq) camera, its rear half the game camera (measured on the mock). R2 (gold hourglass) is a flat decal and the widow cliché; R3 is 1-px lines. **Crown: YES**, a closed circlet + 8 points (§4.3): the portrait needs gold on the face, and a queen needs a crown. Gold = crown + rift ONLY. |
| 2 | Legs, knee height; bristles vs Panther crystals | Knees 0.90-0.97 above a body held at hip z 0.37 (the carapace top is 0.585): a sharp 58-61° interior knee angle, the tarantula "alert crouch". Heavy, tapered, 4 visible segments, **blood-red knee bands** (§4.9). Thin straight legs are the Halloween-prop and daddy-long-legs read (mock v1). **Thorns, not crystals:** ONE obsidian thorn per knee with an orchid → hot tip (Mantis shield-thorn recipe), plus 4 on the abdomen. Clusters stay the Panther's. |
| 3 | Palette distinct from the Black Dragon and the Panther? | **No.** Replaced by **BLOOD ORCHID** (§2): plum-black armour, blood-wine velvet, a pale silk underside, orchid-UV glow, gold. The only red-black ("widow") pet in a violet egg, while its glow stays in the Void family. In the 64 px strip it is the only pet with that combination. |
| 4 | Tetrapod at 32 f? Rules for 8 IK legs? | **32 f is fine.** Use a **metachronal tetrapod**: back-to-front offsets inside each tetrapod (table §5.4), **duty 0.58** (0.55 lets same-side neighbours swing together; checked numerically). Always ≥ 4 feet down. `pk.walk_cycle` takes any leg list but ONE `lift`: copy it into the pet as `walk8()` with a per-pair lift. Rules in §5.4. |
| 5 | Act unique enough? | **No.** Crossing strokes in front of the face = the Mantis X-cross; a two-leg stab-down = the LavaGolem ground pound (and Hammerjaw's slam). New staging, same name `act_riftweave`: the queen **presents the rift to the game camera**, her **hind legs draw silk** three times (the real swathing move), then a **whip-down cast** (§6.4). No other pet's act is driven by its hind legs. |
| 6 | Remix / jackpot issues | 13 remixes found and replaced (§1.2). Jackpot factors in §1.3. |
| – | H_MODEL | **The pair-2 knee-thorn tips, z ≈ 1.10** (± 0.03). Not the crown (0.89) and not the abdomen (0.94 with lips). The arched knees ARE the spider silhouette; the crown sits inside that "crown of knees". |
| – | HEIGHT | **8.0 studs** (§3). |
| – | Hourglass | **Dropped.** Under the belly nobody sees it; on the back it competes with the rift; and it is the cliché. |
| – | Claws | **BLACK.** Gold dots on 8 feet dilute the hero (Mantis review 1, FIX 8). |
| – | Gold fang bases | **No.** IVORY fangs with BLACK tips; the chelicerae carry a VELVET boss instead. |

---------------------------------------------------------------------------------------------------------------------
## 1. The read, the remix sweep, the jackpot

### 1.1 One-line read
**"The blood-widow queen of the void: a plum-black armoured spider on eight arched, red-kneed legs, a spiked gold
crown over a cluster of eight burning orchid eyes, ivory fangs, and a gold-set rift of void-light split open along her
armoured abdomen."**

At 64 px: **a crowned black spider with red knees and a gold-framed glowing slit on its back.** The mock icons pass
this (both the portrait and the game-cam icon), next to every Void sibling, the Mantis and the Kraken.

### 1.2 Remix sweep (plan item → collision → replacement)

| plan item | remixes | replace with |
|---|---|---|
| obsidian / carapace / velvet / void-violet / magenta palette | Panther FUR_D/PALE/VIOLET (0-5°), BlackDragon MANE (0°), Stallion EYE/MANE_D (2-4°); OBSIDIAN lum 29 = black hole in game | BLOOD ORCHID (§2) |
| round gold portal, concentric DEEP/VIOLET/HOT discs, black slit pupil | **Mantis** demon eye-spot (pale rim → deep → ruby → black slit); **Kraken** concentric warning rings; a gold ring = halo/coronet family (Cvetibara, Orca); faces away from the portrait camera | R1b long rift, NO pupil, NO concentric rings (§4.7) |
| gold cross-clasps over the rift (natural follow-up of R1) | a gold "zipper/ladder" at 64 px (the Mantis v1 dark "zipper" note) | 3-prong claw settings at the two ends only |
| violet crystal bristles on 8 knees | **Panther** crystal clusters (same hue); **Mantis** gold knee spine (its hero #2) | single ARMOR thorns, ORCHID→HOT tips |
| magenta eye irises | **Stallion** eyes (317°) | ORCHID eyes (§2) |
| 3 swept-back crown spikes | **Mantis** cone + 2 prongs (3-point); **Inferno Phoenix** 5 swept plumes (in planning); 2 tall gold horns would read as the **Black Dragon**'s gold antlers (same egg) | closed circlet + 8 straight points rising toward the back (§4.3) |
| "palps groom the fangs" (idle) | grooming = **ForestStag** only (FIERCE §7); also the Mantis idle | single-leg web taps + a fang flex (§6.1) |
| "one predator head-tilt" | a spider has no neck; a tilting turret reads as a puppet | the whole body turns toward a sound, one direction per loop |
| roar "rears up on legs 3-4" | rear-up = **NightmareStallion** only (FIERCE §7) | ≤ 16° nose-up with legs 3-4 planted; the core beat is the FANG FLARE (§6.3) |
| roar "hiss-shiver hold" | "hiss + stand tall" = **Mossback** | a stridulation RASP (palps) |
| roar venom drip event | **VenomBasilisk** `venom_drip` event | `flare` / `rasp` / `stab` events, no venom |
| raised front legs spread sideways | **Kappa** screech crouch (arms wide) | legs 1 point FORWARD-UP at the viewer, legs 2 lower (§6.3) |
| act: crossing weave strokes in front of the face | **Mantis** X-cross | hind-leg silk draws (§6.4) |
| act: both front legs stab down (impact) | ground pound = **LavaGolem**; **Hammerjaw** slam | the abdomen whip-down cast |
| Abd1/Abd2 split abdomen | creases at the split on every pump | one rigid Abd + Pedicel + Spinner |

**Halloween hub props** (24 low-poly spiders hanging on silk Beams from garlands, bobbing): never hang, dangle, bob
on a thread or drop on a silk line in ANY clip. The Weaver must be visibly a different class of object: studded plum
armour plates, a gold crown, a gold-set glowing rift, 8 eyes, thick 4-segment legs with red knees and thorns.

**Real-world spider clichés that read CUTE (all banned; the mock v1 showed four of them):**
1. big round front eyes with white glints (the jumping-spider meme) → slanted, lidded, no glint
2. a round ball abdomen ("bauble", "bowling ball") → a long armoured egg with plates, horns and a pointed rear
3. thin straight stilt legs (daddy-long-legs / Halloween prop) → heavy tapered segments, knuckles, red knee bands
4. two fangs curving inward into a "U" = a white smile or moustache → two separate daggers, tips ≥ 0.04 apart
5. a white belly band that shows as a crescent from behind = a grin → the rear cap plate covers the band's end
6. white/pale leg rings ("striped socks") → the knee bands are blood-wine, never white
7. a fluffy plush body, pastel colours, a big cartoon head with two eyes → studs + plates, a small turret, 8 eyes

### 1.3 Jackpot factors (why a 1.5 % secret beats every pet)
1. **The only 8-legged silhouette in the game**, with a "crown of knees" ring of thorn tips.
2. **Two gold heroes that cover both cameras:** the crown (portrait, front) and the rift (game cam, back; its front
   half also shows in the portrait). Mock: 60 gold px at 64 px in the portrait icon, 80 in the game-cam icon.
3. **A palette nobody else has:** red-black widow colours inside the violet Void egg, lit by the egg's own orchid glow.
4. **Material contrast:** studded plum armour vs glassy orchid lenses/rift vs polished gold.
5. **A moving hero:** the rift pulses in the idle, flares in the roar, faces the camera and bursts in the act.
6. **A VFX package** on dedicated anchors (§7): rift glow + Void wisps, 8-eye flash, silk beams, the cast shock-ring.
7. **Portrait:** the mock's tq crop is 388 × 305 px (1.27 : 1), so the spider fills the square icon better than any
   long serpent or quadruped; body, crown and rift all read.

---------------------------------------------------------------------------------------------------------------------
## 2. PALETTE - "BLOOD ORCHID" (decided)

### 2.1 Colours (Blender values; in game ≈ ×0.6)
| role | RGB | lum / hue | in game | where | studs |
|---|---|---|---|---|---|
| **ARMOR** plum-black | **(76, 58, 88)** | lum 67, 276°, s .34 | (46,35,53) | carapace, turret, chelicerae, femurs, abdomen plates, spine and thorn sockets | studded |
| ARMOR_D | (58, 44, 70) | lum 51 | (35,26,42) | tibiae, metatarsi, tarsi, knee/ankle knuckles, clypeus, brows, carapace grooves | studded |
| **VELVET** blood-wine | **(148, 30, 72)** | 339°, s .80, brightest ch. 148 | (89,18,43) | abdomen hull (shows in plate gaps and flanks), carapace rim band, coxae, knee bands, femur under-strips, chelicera bosses, pedicel, palp knuckles | studded |
| **SILK** | **(214, 204, 224)** | lum 207 | (128,122,134) | sternum, abdomen belly band, spinneret tips | studded (band), smooth (tips) |
| SILK_D | (172, 160, 186) | | | gap bars on the belly band (optional) | – |
| DEEP | (118, 24, 156) | 283° | | rift outer field, small-eye rims, gem frame | smooth |
| **ORCHID** | **(212, 72, 255)** | 286°, s .72 | (127,43,153) | eye lenses, rift body, thorn and spine middles, crown gem | smooth |
| HOT | (246, 222, 255) | | | rift seam, eye hot spots, thorn points | smooth |
| **GOLD** | (255, 196, 50) | | (153,118,30) | **crown + rift lips + rift settings ONLY** | smooth |
| GOLD_D | (214, 150, 30) | | | circlet inner faces, rift lip inner edges | smooth |
| IVORY | (240, 234, 214) | | | fangs | smooth |
| BLACK | (14, 14, 22) | | | claws, fang tips, eye sockets and slit pupils, tibial spines, palp claws | smooth |

- **Glow family = DEEP / ORCHID / HOT.** It lives in the eyes, the rift, the 8 knee thorns and the 4 abdomen spines,
  always stepped DEEP → ORCHID → HOT outward (house crystal rule). No Neon, no emissive.
- **Gold is 100 % hero:** crown, rift lips, rift end settings. Nothing else is gold.
- **Dark-family rule:** ARMOR lum ≥ 62 so studs still read in game (Orca rule); ARMOR_D ≥ 50.

### 2.2 Sibling check (HSV hue distance; why it separates)
| mine | nearest saturated | verdict |
|---|---|---|
| ARMOR 276° s .34 (dark) | Panther FUR 251° (25°), BlackDragon INK 247° (29°), Stallion COAT 251° s .24 (25°) | Every Void body is a cool indigo/charcoal; this is a WARM plum-black. In the mock strip it reads plum, not blue. |
| VELVET 339° | BlackDragon TONGUE 342°, Mantis RUBY_D 343° (crystal roots), Kraken BODY 350° (11°) | No pet has a dark wine BODY band. The Kraken is a saturated red squid; here wine is a secondary band under plum-black armour (A/B gate, checklist 6). |
| ORCHID 286° | VenomBasilisk VENOM_L/EYE 284° (1-2°), Leviathan HIDE 300° (14°), **Panther VIOLET 271° (15°)**, **BlackDragon MANE 264° (22°)**, **Stallion EYE 317° (31°)** | Inside the Void egg it is 15-31° from every accent. Its exact match is the Basilisk's frill: a 5 % GRASS lizard with a green body, different egg and silhouette. As a whole palette (plum-black + wine + orchid + gold) it matches no pet. |
| GOLD | every secret's crown, BlackDragon antlers | Crown/hero-only use = the house "secrets wear gold" rule. |
| SILK 270° s .09 | – | a near-neutral silver-lilac, darker than every pet's white |

**Risk I accept, and its gate:** "dark spider + violet glow + gold" is still Void-family in a sentence. That is
intended (it is the Void secret). The 64 px Void strip (checklist 4) and the A/B pairs (checklist 6) must pass.

### 2.3 Share targets (flat palette-ID; side / tq / game / front)
| role | side | tq | game | front | mock F (side/tq/game/front) |
|---|---|---|---|---|---|
| ARMOR | 25-38 | 24-36 | 34-44 | 22-34 | 28 / 26 / 42 / 25 |
| ARMOR_D | 28-40 | 34-45 | 26-36 | 34-45 | 37 / 44 / 31 / 43 |
| dark total | ≤ 66 | ≤ 70 | ≤ 72 | ≤ 70 | 65 / 71 / 73 / 68 |
| VELVET | 20-28 | 12-18 | **9-14** | 13-19 | 22 / 12 / 8.3 / 14 |
| SILK + SILK_D | **3-7** | 1-3 | ≤ 2 | ≤ 3 | 2.4 / 0.9 / 0.9 / 0.9 |
| glow (DEEP+ORCHID+HOT) | ≥ 1 | 3-6 | 4-7 | 3-6 | 1.1 / 3.3 / 4.8 / 3.1 |
| GOLD + GOLD_D | 3-5 | 6-9 | 7-10 | 6-9 | 4.1 / 7.3 / 8.5 / 7.4 |
| BLACK | ≤ 5 | ≤ 5 | ≤ 5 | ≤ 6 | 4.7 / 4.8 / 4.1 / 5.4 |

- **No single role > 45 % in any view.**
- The mock misses four targets by a hair; the brief's geometry fixes them:
  - SILK side 2.4: the belly band is wider here (§4.6)
  - VELVET game 8.3: plate gaps 0.035-0.04, not the mock's 0.03
  - dark total tq 71 and game 73: the same gaps, plus the knee bands at 0.085 long
- **64 px gold:** portrait icon ≥ 45 gold px, game-cam icon ≥ 60 (mock 60 / 80).

---------------------------------------------------------------------------------------------------------------------
## 3. SILHOUETTE, PROPORTIONS, SIZE

- **Side:** a low body (carapace top 0.585, abdomen top 0.875 + lips) under a ring of arched knees (0.90-0.97, thorn
  tips to 1.10); the abdomen is a long armoured egg rising 10° to a pointed spinneret rear.
- **Front:** a wide "A" of legs, the spiked gold crown over the 8-eye cluster, two ivory daggers below, the rift's
  gold front visible above the crown.
- **Game cam:** the gold-set rift on an armoured dome, the gold crown ahead of it, 8 red-kneed legs with orchid thorn
  tips around it.
- **H_MODEL = 1.10 ± 0.03** = the pair-2 knee-thorn tips (§0). Crown tip 0.89, rift lips 0.94, shoulder horns 0.95.
- **Bounds:** x ±1.07 (leg-3 claws), y −1.15 (leg-1 claws) … +1.26 (spinneret tips), z 0 … 1.10.
  L 2.41 × W 2.14 × H 1.10.
- **HEIGHT = 8.0 studs (decided; the plan said 8.5).**
  - Pitch = 0.2243 × 1.10 / 8.0 ≈ **0.031** (the Mantis formula on the measured bounds).
  - At ×1 that is 8 studs to the knee thorns, the abdomen top at ≈ 6.8 studs, **≈ 15.6 studs wide × 17.5 long**.
  - Height sits between the Panther (7) and the Stallion / Black Dragon (9); the footprint is the largest in the game
    (the Leviathan is 11.5 × 17.5), and the abdomen (≈ 5.7 × 7.7 × 4.5 studs) is the biggest single mass in its egg.
  - 8.5 would make it ≈ 16.6 × 18.6 studs for no gain in the icon; the knee-top HEIGHT already under-states its
    presence.
- **Lowest points:** claw tips 0.00-0.01; everything else ≥ 0.08 (palp claws 0.08, fangs 0.11, abdomen 0.265,
  sternum 0.305).

---------------------------------------------------------------------------------------------------------------------
## 4. GEOMETRY (model units, −Y forward, Z up, ground z 0; left side shown, R = mirror x)

Kit setup: `B = bk.Blocks(k, seed=.., tier=3, plates=False, th=0.26)`. **Pass `th` explicitly:** the carapace and
abdomen are Tubes (excluded from the TH search), so the auto TH would be the 0.06-tall sternum and every block would
get "mass" rounding. End `model()` with `bk.stud_skin(k, 0.2243 * H / HEIGHT)`. Seat every small part (eyes, crown,
lips, settings, thorns, grooves) with the Mantis `surf_hit()` (it works on Tubes via `part_bm`).

### 4.1 Cephalothorax (Spine)
**Carapace:** `B.tube([bk.superellipse(hw, hh, zc, y, n=2.4, seg=20) ...], ARMOR, "Spine")`

| st | y | zc | hw | hh | note |
|---|---|---|---|---|---|
| C0 | −0.58 | 0.48 | 0.150 | 0.080 | front; buried in the turret and clypeus |
| C1 | −0.48 | 0.47 | 0.220 | 0.110 | |
| C2 | −0.34 | 0.46 | 0.260 | 0.125 | widest; top 0.585 |
| C3 | −0.18 | 0.45 | 0.265 | 0.120 | |
| C4 | −0.04 | 0.44 | 0.220 | 0.100 | |
| C5 | 0.04 | 0.44 | 0.140 | 0.070 | rear; into the pedicel |

- **Rim band:** a VELVET tube on C1-C4 with hw + 0.012, hh × 0.75, zc − 0.035. It shows as a wine margin under the
  armour edge (side, tq, game).
- **Fovea + radial grooves:** an ARMOR_D fovea (0.035 × 0.05, flush) at (0, −0.24, top); 3 ARMOR_D bars per side
  radiating from it at −40° / 0° / +40° from ±x, from r 0.07 to 0.19, w 0.03, 0.012 thick, `surf_hit`-seated.
- **Sternum:** SILK block (0, −0.24, 0.335), half (0.17, 0.22, 0.03), rnd 0.4 (bottom 0.305).

### 4.2 Ocular turret, 8 eyes, brows (Head)
- **Turret:** `B.add((0, −0.50, 0.605), (0.12, 0.095, 0.065), ARMOR, "Head", top=(0.80, 0.74), rnd=0.35)`
  → top 0.67, front face y −0.595. **hw ≤ 0.12** (leg-1 femur clearance; at hw 0.135 with the IK raise, leg 1 cut
  the turret; tested together with the LEG-1 RULE).
- **Clypeus:** ARMOR_D (0, −0.60, 0.485), half (0.12, 0.03, 0.06), `bot=(0.8, 1)`.

| eyes | count | centre (L) | build | faces |
|---|---|---|---|---|
| **E1 main** | 2 | (±0.065, −0.598, 0.605) | `fierce_eye` copied from ThunderRex.py L112-126 at **sc 0.9, yaw 18, tilt 20**, with CYAN → ORCHID, HOT → HOT, ARMOR → **ARMOR_D** (its V-brow). BLACK socket 0.047 × 0.023, ORCHID slit lens, HOT spot on the OUTER half, BLACK vertical pupil ≤ 70 % of the lens height at the inner-front. **No glint.** The brow overlaps the top 30 % and the two brows meet in a V over the midline. | forward, 18° out |
| **E2 front row** | 4 | (±0.030, −0.612, 0.548), (±0.098, −0.606, 0.557) | DEEP base (0.020, 0.010, 0.018) + ORCHID (0.013, 0.006, 0.012) 0.008 proud; the OUTER pair sits 0.009 higher = a FROWN line | forward |
| **E3 top-side** | 2 | (±0.115, −0.48, 0.65) | DEEP (0.012, 0.026, 0.026) + ORCHID (0.008, 0.018, 0.018), frame rotated 40° out about Y; a small ARMOR_D lid over the top | out + up (the game cam sees them) |

All lenses `role="detail"` (no studs). The pupils are the only parts allowed under 0.02.

### 4.3 Crown (Head; all GOLD, `nostud=True, role="limb"`)
- **Circlet** (closed, sits on the turret's top edge, z 0.675, ≤ 0.01 proud):
  - front bar (±0.10, −0.585) and back bar (±0.10, −0.415): `B.seg(..., hw 0.032, hd 0.026, side=(0, 0, 1), ext=0.02)`
    (`side=(1,0,0)` is degenerate for an x-direction seg: the frame collapses)
  - side bars x ±0.115 from y −0.59 to −0.41: hw 0.026, hd 0.032
  - GOLD_D 0.012 strips on the four inner faces (depth)
- **8 points** (`B.spike`, w 0.034, `top=(0.12, 0.12)`), bases at z 0.695:

| point | base (L) | length | direction | tip z |
|---|---|---|---|---|
| front | (0.040, −0.585) | 0.10 | (0.22, 0.10, 1) | ≈ 0.79 |
| front corner | (0.105, −0.580) | 0.13 | (0.22, 0.10, 1) | ≈ 0.82 |
| back corner | (0.105, −0.420) | 0.17 | (0.22, 0.22, 1) | ≈ 0.86 |
| back | (0.040, −0.415) | 0.20 | (0.22, 0.22, 1) | ≈ 0.89 |

- **Front gem:** the Mantis `gem_inlay` (DEEP frame → ORCHID → HOT glint, flush 45° diamond), size 0.028, on the front
  bar face at (0, −0.613, 0.675), facing −y.
- **Read:** the crown rises toward the back, so the game camera sees a full ring of points and the portrait sees the
  tall back points over the brow V. Straight flared points, never hooked inward (mock v1's inward-hooked claws read as
  a gold hand), never two tall horns (the Black Dragon's antlers).
- Anchor `Crown` at (0, −0.50, 0.90).

### 4.4 Chelicerae, fangs, palps
| part | bone | geometry (L) | colour |
|---|---|---|---|
| chelicera | Chel_L | `B.seg((0.062, −0.60, 0.45), (0.058, −0.69, 0.28), hw 0.050, hd 0.060, ext 0.03, top (0.78, 0.72))` | ARMOR |
| boss | Chel_L | `B.seg(r0 + (0, −0.055, −0.02), r1 + (0, −0.035, 0.02), 0.036, 0.012, role="detail")`, ≤ 0.01 proud | VELVET |
| fang seg 1 | Fang_L | from (0.058, −0.70, 0.28) along (−0.12, −0.15, −1), length 0.10, w 0.028, `top=(0.62, 0.62)` | IVORY |
| fang seg 2 | Fang_L | from the seg-1 end along (−0.25, 0.45, −0.85) (curving BACK under the chelicera), length 0.06, w 0.019 | IVORY |
| fang tip | Fang_L | 0.03, w 0.012 | BLACK |
| palp femur | Palp_L | (0.15, −0.55, 0.39) → (0.20, −0.72, 0.28), hw 0.028, hd 0.030 | ARMOR |
| palp knuckle | Palp_L | at (0.20, −0.72, 0.28), 0.032 rnd 0.4 | VELVET |
| palp tarsus | Palp_L | → (0.19, −0.81, 0.12), hw 0.024 | ARMOR |
| palp claw | Palp_L | 0.04, w 0.012, toward (0, −0.4, −1) | BLACK |

- The two chelicerae keep a ≥ 0.016 gap at the midline. The fang tips sit at x ±0.024 (≥ 0.04 apart), z ≈ 0.11:
  **two separate daggers**. Never let them curve in to meet (mock v1: a white "U" smile).
- The palps sit outside the chelicerae (x 0.15-0.20 vs ≤ 0.112) and never touch the ground.

### 4.5 Pedicel and abdomen hull
- **Pedicel** (Pedicel): VELVET seg (0, −0.02, 0.45) → (0, 0.20, 0.505), hw 0.075, hd 0.065, buried both ends.
- **Abdomen hull** (Abd): `B.tube` of superellipse rings, **n 2.3, seg 24**, VELVET, in a frame tilted 10° rear-up:
  origin **A0 = (0, 0.14, 0.50)**, axis AX = (0, 0.985, 0.174), dorsal UP = (0, −0.174, 0.985). Ring point at angle α:
  `A0 + AX·u + (hw·sgn(cos α)|cos α|^(2/n), 0, 0) + UP·hh·sgn(sin α)|sin α|^(2/n)` (the mock's `abd_ring`).

| st | u | hw | hh | centre (y, z) | note |
|---|---|---|---|---|---|
| A0 | 0.00 | 0.10 | 0.10 | (0.140, 0.500) | buried in the pedicel |
| A1 | 0.08 | **0.21** | 0.19 | (0.219, 0.514) | narrow front = the leg-4 femur clearance (tested) |
| A2 | 0.22 | 0.35 | 0.28 | (0.357, 0.538) | |
| A3 | 0.40 | 0.39 | 0.31 | (0.534, 0.570) | widest 0.78; top 0.875; lowest 0.265 |
| A4 | 0.60 | 0.36 | 0.29 | (0.731, 0.604) | |
| A5 | 0.80 | 0.26 | 0.22 | (0.928, 0.639) | |
| A6 | 0.96 | 0.14 | 0.13 | (1.086, 0.667) | |
| A7 | 1.06 | 0.05 | 0.05 | (1.184, 0.684) | spinneret base |

A long egg, 1.06 × 0.78 × 0.62: not a ball (mock v1 at hw 0.41 and length 0.98 read as a bauble).

### 4.6 Abdomen plates, gaps, belly band, spines (Abd)
**Plates:** open shell bands (`B.tube(rings, ARMOR, "Abd", closed=False)`, the mock's `shell()`), 0.022 proud of the
hull, 0.03 thick, studded. α runs from +x (0°) over the top (90°) to −x (180°); negative = under +x.

| plate | u | α | note |
|---|---|---|---|
| P1 front | 0.05-0.165 | 10°-170° | full width, ahead of the rift; carries the shoulder horns |
| P2 L / R | 0.20-0.40 | 14°-78° / 102°-166° | flank the rift; the gold lips sit on the 78°/102° edges |
| P3 L / R | 0.44-0.64 | 14°-78° / 102°-166° | |
| P4 rear cap | 0.675-0.99 | −15°-195° | wraps down the rear, so the belly band never shows from behind |

- **Gaps 0.035-0.04 in u** between plates = VELVET seams (more wine in the game view than the mock's 0.03).
- **Belly band:** SILK open shell, 0.012 proud, 0.02 thick, **u 0.14-0.64, α 205°-335°** (the lower ~38 %; the mock's
  225-315° gave only 2.4 % side). It ends before P4. Optional SILK_D gap bars across it at u 0.30 / 0.47.
- **Spines** (ARMOR socket 62 % of L, w 0.05 / 0.042 → ORCHID from 50 % of L, w 0.026, `top=(0.25, 0.25)` → HOT point
  0.18 L, w 0.012; ORCHID/HOT nostud):

| spine | base | direction (L) | length |
|---|---|---|---|
| shoulder horn ×2 | P1 at u 0.20, lateral 0.70·hw | (0.35, 0.25, 0.90): up, slightly out and BACK | 0.17 |
| rear-side spine ×2 | at u 0.60, lateral 0.95·hw | (0.90, 0.35, 0.25) | 0.12 |

The shoulder horns point up-back, never forward: forward horns reached the leg-4 knees in the roar test. Keep their
tips ≥ 0.10 from the leg-4 knuckles at rest and in every clip.

### 4.7 HERO: the VOID RIFT (Abd)
**Placement:** along the dorsal midline from **u 0.19 to u 0.76** (world y ≈ 0.28 → 0.85 along the top, ≈ 0.62 along
the curve), over the crest (apex z ≈ 0.90 incl. lift). Its front half faces forward-up (the portrait), its rear half
faces back-up (the game camera). Half-width profile `w(t) = 0.15 · sin(π t)^0.8`, t = 0…1 along the rift.

| layer | half-width | lift above hull | colour | build |
|---|---|---|---|---|
| void field | w(t) | 0.010 | DEEP | lofted open band, or ≥ 14 `B.bar` strips following the hull |
| glow body | 0.63 · w(t) | 0.016 | ORCHID | same |
| seam | 0.12 · w(t), ≤ 0.018 | 0.021 | HOT | same |
| gold lips L/R | seg chain at x = ±(w(t) + 0.035), **hw 0.045 (0.09 wide)**, hd 0.028 | 0.020 | GOLD (inner edge strip GOLD_D) | ≥ 14 segs, ext 0.01 |
| end settings | at u 0.17 and u 0.78: 3 prongs each (centre 0.09, sides 0.065 at ±35°, w 0.03), pointing along the axis (front prongs forward, rear prongs back), tilted 20° up off the surface | 0.020 | GOLD | spikes |

- **Lips ≥ 0.09 wide:** that is ≥ 2 px at 64 px. A 0.04 lip is a 1-px line (the Leviathan's ring problem).
- **NO pupil, NO concentric rings, NO cross-clasps.** It must read as a gold-set tear of light, not an eye, a target
  or a zipper. Use ≥ 14 segments or a lofted band: the mock's 9-bar layers showed as candy stripes.
- Anchor `Rift` at (0, 0.55, 0.90) (u 0.47 surface point), tail = the surface normal.
- **Facing rule (tested):** tilting the abdomen REAR-DOWN turns the rift to the game camera; rear-UP turns it to the
  front. Every "present the rift" beat is rear-down.

### 4.8 Spinnerets (Spinner)
- 2 big: ARMOR spikes from the A7 top, x ±0.035, along (±0.25, 0.8, −0.55), length 0.10, w 0.032; SILK tips from
  70 %, length 0.045, w 0.020, nostud.
- 2 small inner: length 0.06, w 0.022, same recipe.
- Anchor `Spinneret` at the big pair's midpoint tip ≈ (0, 1.27, 0.62).

### 4.9 Legs (Leg/Shin/Foot per pair; hip z 0.37)
Azimuth a from +x toward +y (back). Positions = hip_xy + r·(cos a, sin a), z as listed.

| pair | a | hip (x, y, z) | knee (r, z) → point | ankle (r, z) → point | toe (r, z) → point |
|---|---|---|---|---|---|
| 1 | −54° | (0.16, −0.45, 0.37) | (0.34, 0.92) → (0.360, −0.725, 0.92) | (0.76, 0.10) → (0.607, −1.065, 0.10) | (0.83, 0.035) → (0.648, −1.121, 0.035) |
| 2 | −20° | (0.21, −0.32, 0.37) | (0.36, 0.97) → (0.548, −0.443, 0.97) | (0.80, 0.10) → (0.962, −0.594, 0.10) | (0.87, 0.035) → (1.028, −0.618, 0.035) |
| 3 | +16° | (0.22, −0.18, 0.37) | (0.36, 0.95) → (0.566, −0.081, 0.95) | (0.78, 0.10) → (0.970, 0.035, 0.10) | (0.85, 0.035) → (1.037, 0.054, 0.035) |
| 4 | +44° | (0.18, −0.05, 0.37) | (0.35, 0.90) → (0.432, 0.193, 0.90) | (0.82, 0.10) → (0.770, 0.520, 0.10) | (0.89, 0.035) → (0.820, 0.568, 0.035) |

- **Lengths / reach:** femur L1 0.63-0.70, shin L2 0.91-0.98; rest hip→ankle = **0.50-0.55 × (L1+L2)**; knee
  interior 58-61°, femur elevation 57-59°. The planned extremes stay ≤ 0.75 (act draw).
- **Spacing:** hips ≥ 0.13 apart (coxae never overlap at rest: overlapping coxae become hinge slivers in every pose),
  knees 0.33-0.36 apart, toes ≥ 0.60 apart.
- **Leg 1 vs the turret:** ≥ 0.07 at turret height at rest (x 0.19 vs 0.12).
- **Leg 4 vs the abdomen:** the knee is ≥ 0.18 outside/above A1-A2 at rest; the tibia passes ≥ 0.10 outside the hull.

**Segments** (studded unless noted; "out" = the leg's horizontal direction):

| part | bone | span | half-size (start → taper) | colour |
|---|---|---|---|---|
| coxa | Leg | block at hip − (0,0,0.01), 0.066 × 0.066 × 0.05, rnd 0.45 | | VELVET |
| femur | Leg | hip (ext 0.05 into the sternum) → knee (ext1 0.02) | 0.060 × 0.066, `top=(0.78, 0.78)` | ARMOR |
| femur under-strip | Leg | hip + 0.08 → knee − 0.06, offset 0.05 along the femur's down-perpendicular | 0.046 × 0.022 | VELVET |
| patella knuckle | Shin | at the knee, 0.064, rnd 0.42 | | ARMOR_D |
| knee band | Shin | knee + 0.045 → knee + 0.13 along the tibia | 0.054 × 0.056 | **VELVET** ("blood knees") |
| tibia | Shin | knee → M, **M = knee.lerp(ankle, 0.5) + out·0.06** (an outward bow) | 0.050 × 0.052, `top=(0.85, 0.85)` | ARMOR_D |
| T/M knuckle | Shin | at M, 0.046, rnd 0.42 | | ARMOR_D |
| metatarsus | Shin | M → ankle | 0.040 × 0.042, `top=(0.82, 0.82)` | ARMOR_D |
| tarsus | Foot | ankle → toe (ext 0.015) | 0.030 × 0.030 | ARMOR_D |
| claw | Foot | from the toe along (toe − ankle) + (0, 0, −0.6), length 0.045, w 0.016 | | BLACK; **tip z 0.00-0.01** |
| tibial spines ×2 | Shin | on the tibia at t 0.35 / 0.70, pointing out + down, length 0.045, w 0.013 | | BLACK |
| knee thorn | Shin | from knee + d·0.045, **d = norm((0, 0.35, 1) + out·0.25)**: ARMOR socket 0.05 (w 0.028) → ORCHID 0.05 (w 0.019) → HOT 0.022 (w 0.010) | | ORCHID/HOT nostud |

The pair-2 thorn tips are the model top (H_MODEL 1.10).

### 4.10 Stance footprint and lowest point
- Toe points (L): leg 1 (0.648, −1.121), leg 2 (1.028, −0.618), leg 3 (1.037, 0.054), leg 4 (0.820, 0.568).
- Support polygon ≈ 2.07 wide × 1.69 deep. The abdomen overhangs it behind (spinnerets at y ≈ 1.26); the body mass
  centre is inside it.
- Lowest: claw tips 0.00-0.01. No other part below 0.08 at rest.

### 4.11 Tri budget (≤ 12 k, cap 15 k; the mock is 11.9 k)
| group | budget |
|---|---|
| 8 legs (≈ 13 blocks each) | ≤ 4.4 k |
| abdomen hull + plates + band + spines | ≤ 2.4 k |
| rift (3 layers + lips + settings) | ≤ 1.2 k |
| cephalothorax + turret + eyes + grooves | ≤ 1.6 k |
| crown + gem | ≤ 0.6 k |
| chelicerae + fangs + palps + spinnerets | ≤ 0.9 k |

Tubes at seg 20-24. Blocks under ~0.05 can take 1 bevel segment.

---------------------------------------------------------------------------------------------------------------------
## 5. RIG

### 5.1 Bones
| bone | parent | head | tail | carries |
|---|---|---|---|---|
| Spine | Root | (0, −0.22, 0.44) | (0, −0.30, 0) | carapace, rim, sternum, grooves |
| Head | Spine | (0, −0.47, 0.50) | (0, −0.10, 0.10) | turret, clypeus, 8 eyes, brows, crown, gem |
| Chel_L/R | Head | (±0.062, −0.60, 0.45) | (0, −0.09, −0.17) | chelicera + boss |
| Fang_L/R | Chel_* | (±0.058, −0.70, 0.28) | (∓0.012, −0.015, −0.10) | fang |
| Palp_L/R | Spine | (±0.15, −0.55, 0.39) | (±0.05, −0.17, −0.11) | palp |
| Pedicel | Spine | (0, 0.00, 0.47) | (0, 0.12, 0.03) | pedicel |
| Abd | Pedicel | A0 (0, 0.14, 0.50) | AX × 0.9 | hull, plates, band, spines, rift |
| Spinner | Abd | (0, 1.13, 0.66) | (0, 0.10, −0.06) | spinnerets |
| Leg{i}_L/R | Spine | hip_i | knee − hip | coxa, femur, under-strip |
| Shin{i}_L/R | Leg{i} | knee_i | – | knuckles, knee band, tibia, metatarsus, spines, thorn |
| Foot{i}_L/R | Shin{i} | ankle_i | toe − ankle | tarsus, claw |

Name the legs `Leg1_L … Foot4_R`: `split("_")[0].rstrip(digits)` gives Leg/Shin/Foot, so the kit treats them as
limbs.

**RIG = "quad"** (the label the Studio side already stores; the Mantis precedent). A new "spider" label is only safe
if nothing in the owner's animator branches on the Rig attribute.

### 5.2 Anchors (bones with no mesh, for the Studio VFX)
| anchor | parent | position |
|---|---|---|
| Crown | Head | (0, −0.50, 0.90) |
| EyeGlow | Head | (0, −0.63, 0.60) |
| FangTip_L/R | Fang_* | the fang tips |
| Rift | Abd | (0, 0.55, 0.90), tail = the surface normal |
| Spinneret | Spinner | (0, 1.27, 0.62) |
| Silk_L/R | Foot4_* | the leg-4 claw tips (the act's silk beams) |

### 5.3 IK
`k.add_leg2("Leg{i}_s", "Shin{i}_s", "Foot{i}_s", knee=(s·px, py, pz))`. The poles are the measured offset of each
knee from its hip→ankle line:

| pair | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| knee pole (L) | (0.19, −0.27, 0.94) | (0.31, −0.11, 0.95) | (0.32, 0.09, 0.94) | (0.24, 0.22, 0.94) |

- `solve_leg` keeps each tarsus at its rest world orientation (+ the automatic 35°·lift/0.12 toe tilt), so planted
  claws never slide or dip.
- **Raised-ankle helper** (tested): to put an ANKLE at world point P, call
  `k.solve_leg(leg, f, P − (ankle_rest − hip_rest) in xy, z = P.z − ankle_rest.z, toe=…)`.

### 5.4 Gait (walk) and the 8-leg rules
**Metachronal tetrapod**, back-to-front inside each tetrapod. A larger offset = swings earlier (`gait_target`):

| leg | R4 | L3 | R2 | L1 | L4 | R3 | L2 | R1 |
|---|---|---|---|---|---|---|---|---|
| tetrapod | A | A | A | A | B | B | B | B |
| offset | 0.18 | 0.12 | 0.06 | 0.00 | 0.68 | 0.62 | 0.56 | 0.50 |
| swing starts (n 32, duty 0.58) | f12.8 | f14.7 | f16.6 | f18.6 | f28.8 | f30.7 | f0.6 | f2.6 |

| pair | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| lift | 0.075 | 0.060 | 0.055 | 0.050 |

Stride half 0.085 for all legs (all legs share one duty, so they must share one stride, or the planted feet slide).

**Rules for 8 IK legs:**
1. **duty 0.58:** at any frame ≥ 4 feet planted, and same-side neighbours never swing together (0.55 breaks this;
   checked over the whole cycle).
2. **Plant everything you do not animate:** idle/roar/act end with `cm.plant(k, n, LEGS8, frames)` on the planted
   legs and frames; set `k.meta["planted"]`. Raised legs are keyed separately (FK or the raised-ankle helper) and
   only planted on their ground frames.
3. **Never leave an IK leg unsolved across a body move:** solve every frame (as `walk_cycle` does), not every 2nd.
4. **Same pole all clip.** If a raise needs another pole (leg 1), override `k.legs2[leg]["knee"]` only for those
   frames and **restore it** before the next solve (my test harness forgot once: legs 1 crossed legs 2 at f0).
5. **Coxae ≥ 0.13 apart** and hip capsules r 0.10 (§5.6).
6. Keep `k.meta["legs"]` and `k.meta["duty"]` on `walk8()` so `pk.audit` computes the slide.

### 5.5 check_pairs()
- **Same-side neighbours** (1-2, 2-3, 3-4): all 9 Leg/Shin/Foot cross combinations.
- **Roar raise:** (Leg1_s, Head), (Shin1_s, Head), (Leg2_s, Head), (Shin1_s, Chel_s), (Shin1_s, Palp_s),
  (Leg1_s, Palp_s), (Foot1_s, Palp_s), (Shin1_L, Shin1_R), (Foot1_L, Foot1_R).
- **Face:** (Chel_L, Chel_R), (Fang_L, Fang_R), (Fang_s, Palp_s), (Chel_s, Palp_s), (Fang_s, Spine).
- **Abdomen:** (Leg4_s, Abd), (Shin4_s, Abd), (Foot4_s, Abd), (Leg3_s, Abd), (Shin3_s, Abd), (Abd, Spine),
  (Abd, Head), (Spinner, Shin4_s), (Spinner, Foot4_s).

### 5.6 joints() (hinge capsules)
- hips: (hip, hip, 0.10, Leg{i}); knees: (knee, knee, 0.08, Shin{i}); ankles: (ankle, ankle, 0.05, Foot{i})
- pedicel: ((0, 0.00, 0.47), A0, 0.10, Abd) and ((0, 0.00, 0.47), (0, 0.00, 0.47), 0.09, Pedicel)
- turret base: ((−0.12, −0.50, 0.55), (0.12, −0.50, 0.55), 0.05, Head)
- chelicera roots 0.07, fang roots 0.045, palp roots 0.045, spinner root 0.05

### 5.7 Limits
| joint | limit |
|---|---|
| Head (fused turret) | pitch ±8°, yaw ±10°, roll ±6° (a glance, never a tilt-wobble) |
| Spine | pitch −16° (nose up) … +8°, yaw ±10°, roll ±4°; Root z −0.05 … +0.07; Root x/y ±0.04 |
| Pedicel | pitch ±8°, yaw ±6° |
| Abdomen, world pitch | −22° (rear down) … +12° (rear up) |
| Spinner | ±15° |
| Chel | yaw out ≤ 12°, pitch −20° … +5° |
| Fang | unfold ≤ 70° |
| Palp | roots at x ±0.15 (at ±0.13 the spread chelicerae cut the palps even with the palps spread 28°, tested); spread ≥ the Chel spread + 12°, pitch ±20° |
| Legs | reach ≤ 0.85 (L1+L2); raised ankle z ≤ 1.25 (leg 1), ≤ 0.70 (leg 2), ≤ 0.60 (leg 4) |
| Ground | claws ≥ −0.02 every frame; any other part ≥ 0.05 |

**Rules learned on the mock (all tested):**
- **LEG-1 RULE** (the Mantis arm rule again): never raise leg 1 by lifting its femur past vertical; it swings into the
  turret and crown (IK raise to a forward-up target: Leg1|Head 107-180 tri pairs). Raise it by **opening the knee**
  (the shin swings up) with the femur leaning **out** (FK fem +15 / shin +80 / foot +20: clean vs the head).
- **ABDOMEN LEVEL RULE:** when the Spine pitches nose-up, Pedicel + Abd counter-pitch so the abdomen does not drop
  into the leg-4 tibias. Tested:
  - Spine −14 with Pedicel −2 / Abd +4 (the abdomen follows the body): Leg4/Shin4|Abd 28-50 tri pairs
  - Pedicel +6 / Abd +8: 18-20, all at the forward-pointing shoulder horns
  - plus the horns pointing up-back (§4.6): 0
- **RIFT FACING RULE:** rear-down presents the rift to the game camera (§4.7).
- **Kit signs:** `k.key` pitch + = nose DOWN for −Y bones (Spine, Head), + = LIFT for +Y bones (Pedicel, Abd,
  Spinner), + swings the tip BACK for −Z bones (Fang, legs). For FK leg raises about the leg-plane axis
  t = (−sin a, cos a, 0) on L and (sin a, cos a, 0) on R, **the R side takes the opposite angle** (mirrored axis).
  Write semantic helpers (Mantis style): `body()`, `abdomen(lift, yaw)`, `fangs(spread, unfold)`, `palps()`,
  `leg_raise(i, side, fem, shin, foot)` (via `cm.key_axis`, the Kraken `tent()` precedent). Render one test pose per
  helper before keying.

---------------------------------------------------------------------------------------------------------------------
## 6. CLIPS (30 fps; everything in place; ends exactly on rest)

**Owner rule first:** pull 1-3 clips from animationreference.org BEFORE keying, note the key poses and frames, and
cite them in the clip docstrings and in `ANIM_REFERENCES_1014.md`. Suggested:
- a many-legged creature or spider walk: `/tags/creature-animation` and the free
  `/resources/locomotion-animation-reference` page (metachronal timing)
- a spider/creature threat rear-and-flare for the roar; the logged #6 Monsters University "scare pop" (crouch 5 f →
  explode 5-7 f → hold) is the timing model
- the logged #5 "Attack" (tell → 2-frame snap) for the cast, and #7 How to Train Your Dragon (step, freeze, scan) for
  the idle

General: no head shakes, no spins, no jumps, no linear keys, `collision_free: true` at step 1, ground ≥ −0.02 every
frame, slide 0. **Any limb or body part that swings > 60° between two frames gets an in-between key** (Mantis F1).

### 6.1 idle (120 f loop) - "STILL HUNTER"
| f | beat | keys |
|---|---|---|
| 0-120 | base | The abdomen breathes: Abd lift ±1.5° (2 cycles), Pedicel ±0.5°; Spine z ±0.006 (2 cycles). All legs planted except the taps. Event `pulse` f40 (Rift swell). |
| 8-22 | **tap L1** | The ankle lifts 0.05 (f10), taps down (f13), lifts (f15), down (f18), still by f22: testing a web line. Solve every frame. Palp_L twitch −10° at f12 (3 f). |
| 30-60 | **listen** | The body turns toward a sound: Spine yaw +8° over f30-38 (the planted legs absorb it), Head yaw +6° leading by 2 f; hold to f50; back by f60. One direction per loop. |
| 64-86 | **fang flex** | Chel spread 8° (f64-70); Fang unfold 25° (f70), hold 6 f, fold by f84; palps rasp ±6° every 2 f (f70-78). Event `flex` f70 (fang glint). |
| 90-108 | **tap R2** + rift pump | R2 taps twice (as L1, f92-106); Abd +3° at f100 (2 f in, 6 f out). Event `pulse` f100. |
| 108-120 | settle | exactly rest at f120 |

No grooming (ForestStag), no ring-wave of the legs (the Kraken's idle), no leaf-rock sway (the Mantis's idle).

### 6.2 walk (32 f loop) - "SCUTTLE"
- `walk8()`: the §5.4 phase table, duty 0.58, stride half 0.085 (0.293 per cycle ≈ 2.1 studs at HEIGHT 8), per-pair
  lift 0.075 / 0.060 / 0.055 / 0.050.
- **Body:** Spine z 0.006·wave(f, n, 0.10, 2) (one bob per tetrapod), yaw ±1.2° (1 per cycle), roll ±0.8°.
- **Head:** counter-yaw −0.5 × the Spine yaw.
- **Abdomen lags 2 f:** Abd yaw −1.5·wave(f, n, −0.06), Abd lift 1.0·wave(f, n, 0.04, 2).
- **Palps** alternate ±6° in phase with legs 1; chelicerae and fangs still.
- **Return:** slide 0, loop closed, linear 0, foot_z_var ≤ 0.005. If the game plays it too fast at follow speed,
  raise stride half to 0.10; never shorten n below 28.

### 6.3 roar (72 f) - "FANG FLARE" (threat display)
| f | beat | keys (semantic) |
|---|---|---|
| 0-10 | gather | Root z −0.04; Spine +5 (nose down); palps tuck +12; Chel closed. All legs planted. |
| 10-20 | rear | Root z +0.06; Spine **−14** (nose up) with Pedicel **+6**, Abd **+8** (ABDOMEN LEVEL RULE). Legs 3-4 planted all clip; legs 1-2 planted to f11. |
| 12-22 | **raise** | Legs 1 FK (LEG-1 RULE): fem +15, shin +80, foot +20 → ankles ≈ z 1.2, in front of and outside the face, tips forward-up at the viewer. Legs 2 FK, starting 2 f later (f14-22): fem +5, shin +40, foot +10 → ankles ≈ z 0.65, forward-out and LOWER than legs 1. Keys every 2 f (the shin swings 80° over 10 f). Start the FK at the rest leg shape at f12 (no pop from the f11 IK pose). |
| 18-24 | **FANG FLARE** | Chel yaw out 12, pitch −18 (lifted forward); Fang unfold 65 (daggers forward-down); palps spread 28 (≥ Chel + 12), pitch −15. **Event `flare` f22** (8-eye flash + fang glint). |
| 24-54 | hold + rasp | Stridulation: palps rasp ±8° every 2 f (f26-50); leg-1 shins tremble ±2° every 3 f; Abd thrum ±2° every 3 f; ONE fang stab: Fang +12 at f40 (2 f), back by f44. Events `rasp` f26 (sound), `pulse` f36, `stab` f40. |
| 54-66 | drop | Fangs fold f54-62; legs 2 land first (f58-62), legs 1 land f60-66 (the shin closes BEFORE the femur returns: the raise in reverse); Spine 0 by f66; plant each leg from its landing frame. |
| 66-72 | settle | Root z −0.01 at f68; exactly rest at f72. |

- **Limits:** body nose-up ≤ 16°, Root z ≤ +0.07, abdomen lowest ≥ 0.06; Foot1_L|Foot1_R never cross; no part below
  −0.02.
- **Starting values tested** (`sheet_pose6.png`): FK fem/shin/foot (15, 80, 20) and (5, 40, 10) with the body above
  → 3-6 tri pairs Leg1|Leg2, plus 1 Leg3|Leg4 hip sliver (the mock's coxae were too close; §4.9 fixes it). Tune
  legs 2 lower or further back with `pose_try` until 0.
- **Why it is the Weaver's own:**
  - not the Stallion's rear (50° on the hind legs, hoof strikes)
  - not the Kraken's rise (8 radial arms up)
  - not the Kappa's arms-wide screech (sideways)
  - not the Mantis's wing fan
  - not the Mossback's stand-tall hiss
  - no venom drip (Basilisk)

### 6.4 act_riftweave (120 f) - "RIFT WEAVE" (signature)
**The story:** the queen sinks, then tips her abdomen to show you the rift. Her hind legs draw three threads of
void-silk out of it, one after the other, and she whips the abdomen down to cast the woven net.

| f | beat | keys (semantic) |
|---|---|---|
| 0-12 | wind-up | Root z +0.02; Abd lift +8 (rear up: the rift turns away); Spine +3; palps tuck. |
| 12-26 | **PRESENT** | Root z +0.06; Spine **−6** (nose up); Pedicel **−4**; Abd **−8** → the abdomen tilts rear-DOWN ≈ 18° in world and the rift faces the game camera (tested, `sheet_pose2.png` game view). Ease out by f24. **Event `rift` f24** (Rift flare). |
| 26-72 | **WEAVE ×3** | Legs 4 draw alternately: **L4 f28-42, R4 f42-56, L4 f56-70.** Each draw: the ankle lifts (+2 f), sweeps OUT-BACK-UP to **(±1.02, 0.70, 0.45)** by +6 f (raised-ankle helper, toe +30), holds 2 f, returns to its rest spot by +12 f, planted 2 f. **Events `silk1` f34, `silk2` f48, `silk3` f62** (silk Beam Spinneret → Silk_L/R). On each draw: Spinner flick −12° (3 f) and back; Abd pump −3° (2 f); Pedicel yaw ∓4° (AWAY from the drawing leg). Legs 1-3 planted; Head still. |
| 72-84 | **CAST** | Abd −8 → +10 over f74-80 (in-between at f77), Pedicel −4 → +2; Root y +0.03 at f78, then 0; Spine −6 → +2 (the head dips with the snap); Fang unfold 35 at f80. **Event `cast` f80** (Rift void shock-ring + Spinneret silk burst). Hard stop at f80. |
| 84-120 | settle | Abd +10 → −2 (f92) → 0 (f100); fangs fold by f96; Spine, Pedicel, Root to rest; exactly rest at f120. |

- **Targets:**
  - at f24-70 the rift is face-on in the game view (lips ≥ 70 % of their rest projected length)
  - the leg-4 draw is collision-free (tested at (1.02, 0.70, 0.45): 0 tri pairs vs Abd)
  - reach ≤ 0.85; abdomen world pitch inside −22 … +12; Root y within ±0.04
- **Why it is unique:**
  - it is the only act driven by the hind legs
  - no crossing strokes (Mantis), no ground pound (LavaGolem) or slam (Hammerjaw)
  - no coil or wrap (Kraken), no cocoon (Cvetibara, Phoenix), no spin, no jump, no thread-hanging (Halloween props)

### 6.5 Events summary
| clip | events |
|---|---|
| idle | `pulse` f40, `flex` f70, `pulse` f100 |
| roar | `flare` f22, `rasp` f26, `pulse` f36, `stab` f40 |
| act_riftweave | `rift` f24, `silk1` f34, `silk2` f48, `silk3` f62, `cast` f80 |

**Return with the clips:**
- a pose sheet (tq + side + **game**): roar f10 / f22 / f40 / f60, act f12 / f24 / f34 / f48 / f62 / f80 / f92,
  idle f13 / f40 / f70, walk f0 / f8 / f16
- headless_clips: `collision_free`, `ground_min_z` per clip, audit (slide, loops, linear), the events

---------------------------------------------------------------------------------------------------------------------
## 7. Studio VFX plan (VFX Studio plugin only; no Neon; the mesh must look complete without it)
1. **Rift:** an always-on soft orchid glow + Void wisps (the egg's preset colours (170,100,255) → (40,20,90)); a swell
   on `pulse`; a flare on `rift` / `flare`; a void shock-ring on `cast`.
2. **EyeGlow:** a small 8-eye glow; a flash on `flare`.
3. **Crown:** the shared secret aura / sparkle.
4. **FangTip_L/R:** a glint on `flex` and `stab`.
5. **Spinneret + Silk_L/R:** silk-white → lilac Beams on `silk1-3`; a silk web burst on `cast`.
6. Optional: Void wisps at Foot1 / Foot4 (the Panther/Stallion preset style).
7. Add an `AbyssWeaver` entry to `CreatureVFX.lua` PRESETS when the owner wires it (not now).

---------------------------------------------------------------------------------------------------------------------
## 8. v1 SIGN-OFF CHECKLIST (model round; each item pass/fail, all must pass)

1. **Silhouette (side, 600 px):**
   - arched knees above a low body; the pair-2 knee-thorn tips are the model top (H_MODEL 1.10 ± 0.03)
   - an egg abdomen (not a ball) rising 10° to a pointed rear
   - 4 visible segments per leg; the bounds match §3 within ±0.05
2. **Front view:**
   - the spiked crown above the 8-eye cluster
   - the V brow over two slanted orchid eyes, the 4-eye frown row
   - two separate ivory daggers (no U, no moustache)
   - the rift's gold front visible above the crown
   - the leg "A" frame
3. **Game camera:**
   - the gold-set rift faces the camera and reads as a glowing slit, not an eye, a target or a zipper
   - the crown ring is visible ahead of it
   - plates with wine seams, red knee bands and orchid thorn tips all round
   - the belly band is not visible from behind
4. **64 px slate strip** (icon3 recipe; portrait icon + a game-cam icon, then ShadePanther, NightmareStallion,
   BlackDragon, PharaohAsparuh, ThornbladeMantis, Kraken):
   - I can name a crowned spider, a gold crown, and a gold-framed glowing slit on its back
   - gold px ≥ 45 (portrait) / ≥ 60 (game cam)
   - it is the most striking icon of the Void row
5. **Cute traps (§1.2 list):** none of the 7 present. In particular: no round eyes or glints, no ball abdomen, no
   stilt legs, no white leg rings, no white grin from behind.
6. **A/B pairs at 64 px:**
   - Weaver vs ThornbladeMantis: low and wide vs upright; plum/wine vs jade; a rift vs scythes
   - Weaver vs Kraken: jointed straight legs vs curling arms; plum-black with wine accents vs a red body
7. **Shares** (flat palette-ID, side / tq / game / front): inside the §2.3 table; no role > 45 %; gold only on the
   crown and the rift.
8. **Face close sheet** (front, side, tq at 700 px):
   - fierce_eye main pair with pupils ≤ 70 %, no glint
   - the brows lid the eye tops and meet in a V
   - the crown seated on the turret (≤ 0.01 proud), the gem flush
   - chelicerae with a ≥ 0.016 gap, fang tips ≥ 0.04 apart
   - the palps outside the chelicerae
9. **Rift close-up** (tq, game and top):
   - 3 layers without stripes (≥ 14 segments or lofted)
   - lips ≥ 0.09 wide with a GOLD_D inner edge
   - 3-prong settings at both ends; no pupil, no rings, no cross-clasps
10. **Legs:**
    - femur ARMOR, knee band VELVET, tibia/metatarsus/tarsus ARMOR_D, claws BLACK touching z 0.00-0.01
    - one thorn per knee; tibial spines ≥ 0.013 wide
    - hips ≥ 0.13 apart; leg 1 ≥ 0.07 from the turret
11. **Hard rules:**
    - no Neon; ≤ 12 k tris (report per-group counts vs §4.11)
    - studs on ARMOR / ARMOR_D / VELVET / the SILK band; the glow, gold, ivory and black parts smooth
    - nothing floating or buried (all `surf_hit`-seated); no detail under 0.02 (pupils excepted); no B.poly anywhere
    - `th=0.26` passed; ARMOR lum ≥ 62; HEIGHT 8.0; RIG "quad"
12. **Rig at rest and at the limits** (static poses, `collision_free` with the §5.5 pairs and §5.6 capsules):
    - rest
    - the roar peak (§6.3 f22 values)
    - the act PRESENT pose with the L4 draw (§6.4 f34)
    - the act CAST peak (Abd +10)
    - Spine yaw +10 with planted legs
    - Head yaw 10 + pitch 8
    - all anchors from §5.2 exist
13. **Deliverables:**
    - a 600 px model sheet (tq / front / back / side / game) + a separate 600 px tq
    - the face close sheet; the rift close-up
    - the 64/128 strip (item 4) and both A/B pairs (item 6)
    - the flat-ID share table (4 views); the tri count per group
    - the 5 limit-pose renders (item 12) in tq + game
    - Render the model views LAST: `headless_closeup` overwrites `model_tq` at 200 px.

**Clips come after this model gate:** idle, walk, roar, act_riftweave as in §6, with the references cited first.
