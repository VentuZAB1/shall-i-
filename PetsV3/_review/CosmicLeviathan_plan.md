# COSMIC LEVIATHAN — build plan v1 (Celestial egg, 1 % SECRET: the rarest pet in the game, x3.9 income)

Builder: me, in the PetsV3 kit (`pets/CosmicLeviathan.py`, headless Blender), following the house pipeline:
plan → plan review → build → visual reviews → clips → clip review → export.
This plan is for the plan reviewer. Decide or adjust everything marked **[DECIDE]**.

## 1. Role and the one-line read
"A colossal sky-sea leviathan that swims through the night sky, with a crowned skull-armoured head, a huge fanged
underbite, starfield wing-fins and a long body rising in an S like a sea serpent breaching."

At 64 px it must read as **a crowned sea-serpent / sky-whale**. It must NOT read as:
- a dragon. Black Dragon = legged purple eastern dragon with gold antlers and a pearl. Celestial Dragon = indigo winged
  western dragon with an orbiting star crown and a crescent tail tip.
- a whale. That is the Abyssal Orca: horizontal torpedo, angler lantern.

## 2. Silhouette and proportions (side view; −Y = forward, Z = up; rest = idle pose)
The pet is LEGLESS and floating: the lowest point is about 0.10–0.15 above the ground, like the Orca's 0.088.

Body centreline: a smooth S through these stations (y, z, ring half-width × half-height):

| station | y | z | hw × hh | bone |
|---|---|---|---|---|
| skull | −1.05 | 1.28 | (head, see §4) | Head |
| throat / neck | −0.82 | 1.02 | 0.20 × 0.22 | Neck |
| chest (widest) | −0.55 | 0.72 | 0.30 × 0.30 | Chest |
| mid body | −0.15 | 0.45 | 0.27 × 0.26 | Spine |
| belly low point | 0.20 | 0.40 | 0.23 × 0.22 | Spine |
| tail 1 | 0.55 | 0.48 | 0.18 × 0.17 | Tail1 |
| tail 2 | 0.90 | 0.62 | 0.13 × 0.12 | Tail2 |
| tail 3 | 1.20 | 0.78 | 0.085 × 0.08 | Tail3 |
| tail 4 / fluke root | 1.42 | 0.90 | 0.05 × 0.05 | Tail4 |

Size and limits:
- Overall: about 2.9 long × 0.6 wide (body) / about 1.9 with the fins; about 1.55 tall to the crown top.
- HEIGHT 10 studs, measured to the crown top (like the Orca's "dorsal tip"). In game that is about 18–19 studs long; the
  reviewer should say if that is too big next to the Orca at 10 / Celestial Dragon.
- The hull is built with the **Tube loft** (as on the Orca): rings perpendicular to the centreline spline, one tube per
  bone with overlapping joints, superellipse n 2.4, flush `band()` shells for the armour.
- No box segments on the body, so there are no creases.

## 3. Colour blocking (3-band, flat palette-ID shares measured)
**[DECIDE] palette.**

Option A, "ECLIPSE GOLD" (recommended):
| role | colour | where |
|---|---|---|
| ARMOR | obsidian blue-black (24, 26, 48) | dorsal saddle plates, skull, jaw armour, fin rays, tail rings |
| HIDE | deep sapphire (34, 74, 190) | flanks (saturated, NOT Celestial Dragon indigo 70, 76, 182: bluer and darker) |
| STAR | starfield panels: navy (16, 20, 60) + white star studs | fin membranes and dorsal-fin windows |
| BELLY | pale gold-cream (248, 230, 178) | throat, belly plates (ventral scutes), fluke inner |
| GOLD + GOLD_D | (255, 200, 56) / (204, 140, 30) | hero crown, armour rims, fangs base, fin leading edges |
| NOVA ×3 | deep (90, 40, 200) → violet (160, 90, 255) → hot (235, 220, 255) | eye cores, crown gem, chest star-core, dorsal crystal tips |

Option B, "DAWN SERAPH":
- ivory-pearl armour (232, 226, 210) with gold rims
- deep cosmic navy hide with star dots
- gold belly
- the same NOVA accent

B risks clashing with the Celestial Dragon's pearl horns and Pharaoh Asparuh's cream.

Share targets (game cam, Option A):
- ARMOR 30–40 %, HIDE 25–35 %, BELLY ≥ 7 % in the side view
- GOLD ≥ 8 %, with the crown ≥ 3 % on its own
- NOVA ≥ 4 %, STAR ≤ 15 %

## 4. Head (built at its final size; the hero zone)
- **Skull:**
  - a long armoured skull (about 0.46 long, 0.34 wide, 0.26 tall)
  - heavy ARMOR brow ridges forming a V over deep-set **NOVA star eyes**: a dark socket, a violet iris and a hot slit,
    with no glint (fierce, never cute)
  - cheek plates flaring back like gill-armour
- **Jaw:**
  - a massive UNDERBITE lower jaw (Jaw bone), modelled 6° open (key = plan − 6)
  - two big upward ivory-gold tusk fangs at the front plus a row of small fangs
  - a dark violet mouth
- **HERO, [DECIDE]:**
  - H1, recommended: **ARMILLARY CROWN**.
    - Two thick GOLD rings cross above the skull like an astrolabe or gyroscope (one tilted 25° forward, one 25° sideways).
    - They are mounted on a gold diadem band with a NOVA star gem at the centre.
    - The rings are 0.30 in diameter and 0.04 thick, lathed with the Tube band primitive so they are smooth, not studded.
    - It reads at 64 px as a gold sphere-crown. In the act the Crown bone can rotate the rings slowly around their own
      axis (not a body spin).
  - H2: **COMET HORN**. One huge swept-back gold horn from the forehead (0.45) trailing 3 NOVA crystal shards like a
    comet tail.
  - H3: a gold **sun-corona** of blades. Rejected by me: it remixes the Solar Lion's ray mane.
- **Mane, optional:** 3 swept-back ARMOR gill-spines per side behind the cheeks.

## 5. Body features
- **Dorsal sail:** 3 swept-back dorsal fins along the S (chest, mid, tail1). Each is a dark ARMOR frame with a STAR
  window and a NOVA crystal tip. They are not ridge shards (Thunder Rex owns those).
- **Ventral scutes:** pale BELLY band plates (`band()` shells) from the throat to tail2, giving the 3rd band in the side
  view.
- **Wing-fins (signature):**
  - two big pectoral fins from the chest sides (Fin_L / Fin_R + FinTip_L / FinTip_R), 0.85 span each
  - swept back 35° and slightly down, like a manta or whale-flipper hybrid
  - GOLD leading edge, ARMOR rays, STAR membrane panels with 6–8 white star studs per fin
- **Tail:** ARMOR rings at each tail joint (gold-rimmed), then a **split star fluke**. That is a horizontal whale fluke
  with 2 lobes, NOT a crescent (Celestial Dragon owns the crescent) and NOT the Orca's notched black-white fluke.
  - [DECIDE] fluke style: a NOVA-tipped twin-blade fluke, or a gold-rimmed STAR fluke.
- **Chest star-core:** a NOVA crystal set in the chest armour (the VFX anchor "Core").

## 6. Rig ("fish" rig like the Orca; motion "Swim", floats)
Bones:
- Root, Spine, Chest, Neck, Head, Jaw
- Tail1, Tail2, Tail3, Tail4, Fluke
- Fin_L/R, FinTip_L/R, Dorsal1-3

VFX anchors:
- Crown: the gem
- Core: chest
- Mouth: in front of the jaw, for the breath
- Fluke: tail tip
- Eye_L/R: optional

Collision pairs and joint capsules:
- Pairs:
  - Head|Neck, Jaw|Neck, Jaw|Chest
  - Fins vs body, Fin vs FinTip
  - Dorsals vs neighbours
  - Tail segments vs each other at the S
  - Fluke vs Tail2
- Joint capsules: Jaw hinge, fin roots, neck pivot.

## 7. Clips (animation references from animationreference.org will be pulled and cited BEFORE animating, per the owner's rule)
| clip | frames | idea |
|---|---|---|
| idle | 120 loop | Slow floating S-undulation travelling head → tail, the fins sculling, a slow look-around (no head shake), one deep breath that lights the chest core (event) |
| swim | 36 loop | Travel undulation, a bigger S-wave and fin strokes, like the Orca's body_wave / tail_wave but serpent-long (phase lag per segment) |
| roar | 64 | Rears up (the front S rises), jaw opens wide after the head snap lands, fins flare, tail lashes |
| act_stareater | about 120 | **STAR-EATER** (signature) |

STAR-EATER beats:
1. Coils back (anticipation).
2. The crown rings spin up (Crown bone; event "crown").
3. The jaw gapes; it INHALES with the stars pulled into the mouth (VFX on Mouth; event "inhale").
4. Gulp: the head snaps shut.
5. A light pulse runs down the body (events core → tail).
6. Exhales a nova from the mouth (event "nova").
7. Settles.

Rules: no head shakes, no airborne spins, the body stays at ≥ 0.02 above the ground, and 0 collisions at step 1.

## 8. Budget and deliverables
- Body: ≤ 12 K tris; Tube rings 20–24 segments.
- Model-review deliverables:
  - a 600 px model sheet (tq / front / back / side / game)
  - a face close sheet
  - a 64 px icon strip next to the Celestial siblings (SolarLion, Griffin, CelestialDragon, Cvetibara) and ThunderRex
  - flat palette-ID shares

## 9. Questions for the plan reviewer
1. Palette A or B, or your own. Is the hide hue clearly separate from the Celestial Dragon and Thunder Bull blues?
2. Hero H1 (armillary crown) or H2 (comet horn), or your own. Will it read at 64 px?
3. The S-pose and size (HEIGHT 10 to the crown top): too big, too small, or too similar to the Black Dragon's S?
4. Fluke design.
5. Is anything here a remix of a sibling's signature feature? Any missing "jackpot" factor for the rarest pet?
