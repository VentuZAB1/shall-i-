# ICE MAMMOTH - concept plan v2 (Glacier Egg, MEDIUM 26 %, area 7 Frostfall Glacier)

Planner: pet planner (concept only). The lead builds `pets/IceMammoth.py`. There is NO old IceMammoth file in PetsV3, so
this is built from scratch. Binding for the build. Not built.

## v2 changes (from GLACIER_PLAN_REVIEW.md)
APPROVED WITH CHANGES, 7/10. Applied:
- Idle (MUST 1): the ground sniff is dropped (the Bramble Badger's idle is the same motion). New idle: the trunk swings slowly
  (tip +/-12 degrees, two cycles), one exhale puff at f80, and the tusks stay still.
- Accent (MUST 2): MINT (140,236,222) becomes (150,236,210), #96ECD2 (H 162, S 0.36). That is 29 degrees from the Lynx ICE
  and 22 degrees from the Yeti AURORA.
- Build gate (MUST 3): the kit has no trunk tube. Prototype the 4-segment trunk (`B.seg` taper chain) before the full model.
  Check at 64 px that it reads as a trunk, not a hose.
- NICE: the act (`act_dustover`) stays as planned.
- Builder gates from review section 6 apply.

## 0. Facts
| | |
|---|---|
| Tier | Medium |
| Odds | 26 % (money x1.26) |
| Egg / area | Glacier Egg, area 7 |
| Rig | quad (heavy, columnar legs, trunk) |
| Closest kit file | `pets/ThunderBull.py` (heavy quad, horn kit, charge pattern). Trunk tube: none in the kit, build from a `B.seg` taper chain (see the build gate) |
| HEIGHT | 9.0 studs (top of the wool hump) |
| Tris | 8-11k (cap 15k) |

## 1. Read in one line
"A huge woolly mammoth in charcoal-teal wool blocks, with cracked ice tusks and a trunk that scoops snow."
At 64 px: a dome hump, two long pale tusks curving forward, and a trunk hanging down the front. It must NOT read as:
- ThunderBull (navy-violet bison, cape, horns, charge act). The Mammoth has tusks and a trunk, not horns.
- a plain elephant. The wool mane blocks, the ice tusk cracks and the teal palette keep it in the glacier theme.

## 2. Rarity ladder
- Medium (26 %). Beats the starter (Lynx 50 %) on size and presence.
- Must be beaten by Yeti (14 %), Roc (7.4 %), Titan (2.5 %), Absolute Zero (0.1 %).
- Must look more like a brute than the Glacier starter, and it must not match the Yeti's bulk.

## 3. Silhouette and anatomy (x H, H = 9.0 studs)
- Barrel body, chest 0.40H deep, body 1.25H long. One dome hump at 0.80H over the shoulders, sloping down to the rump at 0.55H.
- Head low and forward. Head top 0.62H. Head length 0.30H.
- Tusks: two, out of the upper jaw, curving forward and up. Each tusk 0.42H long, 3 tapered segments, the outer one with 2 crack lines (MINT).
- Trunk: 0.38H long, 4 segments, hangs and curls up at the tip. The tip has two finger blocks (DARK).
- Legs: columnar, thick (leg width 0.30H). Ground to shoulder 0.36H. Feet are flat pads, 1.2 x leg width, DARK toenails.
- Ears: small and flat on the side of the head, not floppy.
- Tail: thin, 0.25H, with a wool tuft (WOOL_D).
- No box belly: the belly line tapers from the chest up to the waist.

## 4. Palette (Blender RGB; body brightest channel 188 >= 170)
| Name | RGB | Hex | Where | Share (side) |
|---|---|---|---|---|
| CHAR_TEAL | 150,184,188 | #96B8BC | body, legs, trunk, head (studded) | 42 % |
| WOOL_D | 96,118,124 | #60767C | wool mane blocks on the back, hump, tail tuft, brows | 18 % |
| BELLY_PALE | 206,214,216 | #CED6D8 | belly strip that follows the slope, inside of the trunk | 10 % |
| TUSK_ICE | 238,246,250 | #EEF6FA | tusks (smooth) | 6 % |
| MINT | 150,236,210 | #96ECD2 | THE accent: tusk crack lines, eye slits | 4 % |
| DARK | 52,62,68 | #343E44 | tusk roots, trunk tip, toenails, foot pads | 6 % |
| BLACK | 14,14,22 | #0E0E16 | eye slit pupils | <1 % |
| MOUTH | 86,18,30 | #56121E | mouth | <1 % |

- In game about (90,110,113): a dark teal-grey brute.
- Accent family: GLACIER MINT (pale teal). Nearest after the change: Yeti AURORA (22 degrees) and Lynx ICE (29 degrees). Pharaoh's saturated turquoise is cross-egg and accepted (review ruling 9).
- Gold: none.

## 5. Part list (x H)
- Torso: barrel block 0.40H deep x 0.46H wide x 0.70H long, `rnd 0.30`, bottom taper, belly tuck.
- Hump: a dome of 3 wool blocks (WOOL_D) on the shoulders, top at 0.80H.
- Wool mane: 3 rows of stacked tapered blocks down each flank (down to 0.35H). Blocks only.
- Head: wedge skull 0.30H long, low; cheek blocks; tusk sockets; brow shelf (WOOL_D) 0.04H proud.
- Tusks: 2 x 3 tapered segments (0.42H total), TUSK_ICE, outer segment with 2 MINT crack lines (flush inlays, 0.012H).
- Trunk: 4 segments, 0.38H total, body colour, DARK tip. Build gate: prototype first (section 0).
- Legs: 4 columns, 2 blocks each (thigh 0.20H, shin 0.16H), pads 1.2 x width.
- Hero piece: none required (Medium). The signature shape is the trunk and the tusks.
- Stud skin on body, head, trunk, legs and hump. Not on tusks, crack lines, toenails, eyes.

## 6. Face spec
- Eye: small, deep-set. A DARK socket with a MINT slit (0.07H x 0.02H), tilted 15 degrees, inner corner low. BLACK slit pupil.
- Brow: WOOL_D shelf over each eye, 15 degrees inner-down. Heavy, not cute.
- Tusk roots in DARK. Mouth closed. No tongue.
- No glint, no round eyes.

## 7. Clips (30 fps)
- **idle (120 f loop): "trunk swing" (review 2.2 MUST 1).** The trunk swings slowly, tip +/-12 degrees, two cycles. One exhale puff at f80 (VFX). The tusks stay still. No ground sniff.
- **walk (40 f loop, quad walk):** heavy and slow. The trunk swings 3 degrees per step. Walk slide ~0.
- **roar (66 f): "trumpet".** f0-20 the head lifts 15 degrees (pitch up, within 30). f20-30 the trunk curls up over the head and extends to the sky (trunk up 70 degrees). f30-50 hold, the trunk trembles +/-2 degrees. f50-66 the trunk lowers, the head returns. No rear-up.
- **act_dustover (100 f, in place): "dust over the back".** Elephants throw dust over themselves. No shake-off, no spin.
  1. f0-22: the trunk drops and curls into the snow (trunk tip down, scoop open).
  2. f22-48: the trunk scoops and lifts, curling up and over the head. The head pitches up no more than 20 degrees.
  3. f48-64: the trunk flicks the load back over the withers. Event `dust1` f56 (frost puff on `Back`).
  4. f64-92: two smaller scoops and flicks (events `dust2` f74, `dust3` f86).
  5. f92-100: the trunk returns to rest. The tail flicks once. Exact rest pose.

## 8. VFX anchor bones (named after the effect; parent bone in brackets)
- `FX_SnowSpray` [Trunk_Tip]: snow spray on the scoops.
- `FX_TuskSparkle_L` [Tusk_L], `FX_TuskSparkle_R` [Tusk_R]: a sparkle on the tips.
- `FX_FrostPuff` [Back]: a frost puff on the dust-over.
- `FX_IceCrack` [Foot_FL]: an ice crack puff on the foot plant.
- `FX_BreathCloud` [Breath]: a small breath cloud at the exhale.

## 9. Distinctness
- ThunderBull (Thunder, navy-violet bison, horns, charge): the Mammoth has a trunk, tusks, teal-grey colours, and the dust act.
- Glacier Yeti (biped): the Mammoth is quad and has a trunk. The Yeti is upright, and it is not a trunk animal.
- Treant (Grass): wood, brown. The Mammoth is wool and ice.

## 10. Animation references
TBD by builder. Suggested tags: "elephant trumpet", "elephant dust bath", "elephant walk".

## 11. Reviewer gates
1. Build gate (before the full model): the trunk prototype reads as a trunk, not a hose, at 64 px.
2. 64 px: the dome hump, the two pale tusks and the trunk read.
3. Game camera: the body is dark teal-grey; the MINT cracks show on the tusks.
4. The wool is blocks, not fringe. The idle is a trunk swing, not a sniff.
5. Builder gates (review section 6): step-1 tris, collision_free, ground_min_z >= -0.02, linear 0, loops closed; icon strip at 64 and 128 px next to the Yeti and ThunderBull; value shares; pose sheet of the dust-over.
