# PERMAFROST TITAN - concept plan v2 (Glacier Egg, SECRET 2.5 %, area 7 Frostfall Glacier)

Planner: pet planner (concept only). The lead builds `pets/PermafrostTitan.py`. Binding once the owner picks a hero option
(section 5). Not built.

## v2 changes (from GLACIER_PLAN_REVIEW.md)
REVISE 5/10. Rewritten to the review's items 2.5 MUST 1-9. Nothing from v1 is kept except the upright giant, the height and
the biped rig.
- Hero: the head crown is removed (it copied Thunder Rex's crown band). Two options are written in full, both marked
  OWNER PICKS (section 5). The owner chooses A or B.
- Gold: PALE_GOLD removed. House GOLD (255,196,50) and GOLD_D (214,150,30) only.
- Core: ICE_CORE removed (it was 5 degrees and 20 RGB from the Lynx's ICE). The core inset is ICE_W (226,240,250). The glow is
  VFX only.
- Body: SLATE_VIOLET (160,152,200) becomes MAUVE (184,150,200), H 281. This moves the Titan out of the blue-violet cluster.
- Shoulders: the tilted ICE_W slabs are removed (same build as the Yeti's plates). They are now two rounded, studded MAUVE
  pauldrons per side, each with an ICE_W cap.
- Eyes: ICE_W slits in JOINT_D sockets, BLACK pupils (no cyan, no glow mesh).
- Roar: the slab flare is removed (it was the Yeti's shoulder heave). New roar: `core bellow`.
- Act: `act_crownflare` is removed (Cinder's crown-plate lift and Cvetibara's bloom). New act: `act_kneelrise`.
- Idle: the crown creak is removed. New idle, no head tilt.
- HEIGHT stays 10.0 (equal to Rex).
- The builder gates in review section 6 apply (section 11 below).

## 0. Facts
| | |
|---|---|
| Tier | Secret |
| Odds | 2.5 % (money x2.85) |
| Egg / area | Glacier Egg, area 7 |
| Rig | biped (upright giant, rounded shoulders) |
| Closest kit files | `pets/LavaGolem.py` (biped golem skeleton, heavy build). `pets/ThunderRex.py` (secret biped: gold hero-piece pattern only) |
| HEIGHT | 10.0 studs (top of the head or the hero, per option) |
| Tris | 9-12k (target 13k gate, cap 15k) |

## 1. Read in one line
"A walking mauve-stone ice giant with rounded pauldrons, an ice-white chest core, and one gold hero piece."
At 64 px: a bulky mauve figure with a gold ring on the chest (option A) or a gold arch over the head (option B). It must NOT read as:
- ThunderRex (storm-blue shells, cyan crystal, a gold crown band with pale spikes). The Titan has no spikes, no crown band and no cyan.
- LavaGolem (basalt golem, magma seams, fist pound). The Titan is ice and mauve, with no magma and no pound.
- the Glacier Yeti (hunched, navy, tilted ice plates). The Titan is upright, mauve, with rounded studded pauldrons.

## 2. Rarity ladder
- Secret (2.5 %). It must outclass Roc (7.4 %), Yeti (14 %), Mammoth (26 %) and Lynx (50 %).
- It must also be readable as a secret next to Thunder Rex (1 %), so its hero piece must be as clear as Rex's.
- Only Frostcrown Dragon (0.1 %) is rarer in this egg.

## 3. Silhouette and anatomy (x H, H = 10.0 studs)
- Upright. Head top 1.0H (with the hero). Shoulder line 0.82H.
- Shoulders wide, 0.50H across. Each shoulder carries a rounded pauldron (see the part list).
- Chest deep 0.42H. Waist 0.70 x chest width. Hips 0.46H wide.
- Arms long: forearm 0.40H, fists reach knee height (0.45H above the ground).
- Legs pillar-like: thigh 0.34H, shin 0.30H. Feet blocky (0.14H tall), 3 toe blocks.
- Head small for the body: skull 0.16H long, 0.14H wide, sunk between the shoulders. Brow ridge in JOINT_D.
- No tail.

## 4. Palette (Blender RGB; body brightest channel 200 >= 170)
| Name | RGB | Hex | Where | Share (side view) |
|---|---|---|---|---|
| MAUVE | 184,150,200 | #B896C8 | body, arms, legs, head, pauldron bodies (studded) | 48 % |
| ICE_W | 226,240,250 | #E2F0FA | pauldron caps (tip 0.05H), chest core inset, eye slits, knuckle shards (smooth) | 12 % |
| JOINT_D | 52,60,84 | #343C54 | joints, gaps, brow ridge, eye sockets, toe blocks | 9 % |
| GOLD | 255,196,50 | #FFC432 | THE hero piece (option A bezel or option B arch) | 4 % |
| GOLD_D | 214,150,30 | #D6961E | inner faces of the hero piece | 1 % |
| BLACK | 14,14,22 | #0E0E16 | eye pupils, claws | 2 % |
| MOUTH | 86,18,30 | #56121E | mouth slit | <1 % |

- In game about (110,90,120) for the body: a mauve stone. The white caps and the gold hero are the light parts.
- Accent: the gold hero (house gold, the secret rule). ICE_W is the white crystal. No cyan, no violet.
- Gold check: house gold is used by Rex, Leviathan, Orca, BlackDragon. The Titan's gold takes its own shape (a bezel or an arch).

## 5. Part list (x H) and HERO OPTIONS

### Common parts (both options)
- Torso: chest block 0.42H deep x 0.50H wide x 0.40H tall, waist block 0.70 x chest, `rnd 0.30`.
- Chest core: ICE_W inset on the front of the chest, 0.12H x 0.10H, flush, smooth (`role detail`). Glow is VFX only.
- Pauldrons (4 total): 2 per side, rounded studded MAUVE blocks, 0.16H across, 0.12H tall, with an ICE_W cap (0.05H tip, smooth). Not tilted slabs.
- Arms: upper 0.22H, forearm 0.40H (with the wrist), fists 0.14H with 3 ICE_W knuckle shards (0.06H, smooth).
- Legs: thigh 0.34H, shin 0.30H, foot 0.14H with 3 toe blocks (JOINT_D).
- Head: skull 0.16H, brow ridge (JOINT_D), flat closed mouth line (MOUTH).
- Stud skin on torso, arms, legs, head, pauldron bodies. Not on the caps, shards, core, the hero piece.

### 5.1 OPTION A - GOLD CHEST BEZEL (OWNER PICKS: A or B)
- Ring: a closed annulus of 12 GOLD segments around the chest core. Outer diameter 0.22H. Band 0.03H radial, 0.05H deep, proud of the chest by 0.02H.
- Tilt: the ring plane tilts 10 degrees up from the chest face.
- Centre: the ICE_W core inset sits in the ring's centre, flush.
- Inner edge: GOLD_D (214,150,30), 0.01H strip on the inside of the ring.
- Mount: `surf_hit` on the chest front face, centred at chest height.
- No head piece in option A. The head stays bare: the skull, the brow and the ICE_W eye slits.
- Pass check: at least 25 gold px in the 64 px icon (review gate 2.5 MUST 1). Print the gold count.
- Reads as: a gold ring on a mauve chest with a white core. Not a crown. No spikes.

### 5.2 OPTION B - GOLD ARCH HEADDRESS (OWNER PICKS: A or B)
- Arch: one gold bridge over the skull top, from the left temple over the crown to the right temple (a lateral arch across the head).
- Span: 0.26H between the temples (0.13H each side of the centre line). Rise: 0.12H above the skull top.
- Section: 0.04H thick. 0.05H tall at the crown, tapering to 0.03H tall at each end.
- Ends: two GOLD_D end caps (0.04H cubes) at the temples, flush with the skull.
- Inner face: a GOLD_D strip (0.01H) along the underside of the arch.
- No spikes, no points, no band. The arch is smooth (`role detail`).
- No chest bezel in option B. The chest core stays (ICE_W inset).
- Pass check: at least 25 gold px in the 64 px icon. The arch is the only gold above the eyes.
- Distinct from Rex: Rex's crown is a closed band with pale spikes. The arch is an open bridge with no spikes.

## 6. Face spec
- Eyes: ICE_W slits (0.06H x 0.02H) in JOINT_D sockets, BLACK slit pupils, under the JOINT_D brow ridge (20 degrees inner-down). No glow mesh.
- No smile. A flat closed MOUTH line.
- Option A: the face is bare, so the eyes and the brow carry the read. Option B: the arch frames the brow.

## 7. Clips (30 fps; collisions 0 at step 1; ground_min_z >= -0.02)
- **idle (120 f loop, review 2.5 MUST 9):** weight shift (hip yaw +/-3 degrees, one cycle). The pauldrons settle 2 degrees at f30 and f70. The core pulses at f40 and f100 (VFX on `Core`). No head tilt. Settles to rest.
- **walk (48 f loop, biped):** heavy stride, weight rolls to each foot. Each arm swings 4 degrees. Walk slide ~0.
- **roar (66 f): `core bellow` (review 2.5 MUST 7).** The head lifts 10 degrees. The arms go out 8 degrees (not a stand-tall, not a spread). The core pulses (VFX on `Core`) at f22 and f34. Option A: the bezel pulses too. Held f22-50, back to rest by f66.
- **act_kneelrise (100 f, in place) (review 2.5 MUST 8):**
  1. f0-18: the right knee drops to the ground (contact >= -0.02). The head bows 12 degrees. The fists rest on the thighs.
  2. f18-50: hold the kneel. The core pulses at f30 and f44 (VFX, event `core`). The fists do NOT touch the ground (the AZD owns the press).
  3. f50-84: the Titan rises from the knee. The root y returns to 0 within +/-0.04.
  4. f84-100: exact rest pose, 0 collisions.

## 8. VFX anchor bones
- `FX_CorePulse` [Core]: a periwinkle glow and a small PointLight pulse on the core events. No glow mesh.
- `FX_FrostDrift_L` [Pauldron_L], `FX_FrostDrift_R` [Pauldron_R]: frost drift off the caps.
- `FX_IceDust_L` [Fist_L], `FX_IceDust_R` [Fist_R]: ice dust on the roar.
- `FX_IceCrack` [Knee_R]: ice crack puff on the kneel.
- `FX_HeroGlint` [Hero]: a small sparkle on the hero piece only (option A: the bezel; option B: the arch).

## 9. Distinctness
- ThunderRex (Thunder secret): storm shells, cyan crystal, gold crown band with spikes. The Titan has no spikes, no cyan, and a gold ring or arch.
- LavaGolem (Fire): basalt golem, magma seams, fist pound. The Titan is mauve and ice, and it kneels instead of pounding.
- Glacier Yeti (Big): hunched navy, tilted ice plates, skid act. The Titan is upright, mauve, with rounded studded pauldrons, a core roar and a kneel act.
- Glacier Lynx (Starter): ICE cyan. The Titan's eyes are ICE_W, and its core is ICE_W, not cyan.
- Frostcrown Dragon (Mythic): the press. The Titan's fists stay off the ground.

## 10. Animation references
TBD by builder (owner rule). Suggested tags: "giant walk heavy", "knight kneel", "golem roar".

## 11. Reviewer gates (review section 6 applies)
1. Step 1: tris count reported (target 13k, cap 15k), `collision_free: true`, `ground_min_z >= -0.02` on every frame, linear 0, loops closed.
2. The chosen hero (A or B) shows at least 25 gold px in the 64 px icon. Icon strip at 64 and 128 px next to Thunder Rex and the Yeti.
3. Value shares printed: the MAUVE body share, the ICE_W share, the gold share.
4. Pose sheet of the kneel and the core bellow before export.
5. The act is a kneel, not a crown flare and not a press. The roar is a core bellow, not a shoulder heave.
