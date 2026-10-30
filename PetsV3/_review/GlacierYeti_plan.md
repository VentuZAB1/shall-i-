# GLACIER YETI - concept plan v2 (Glacier Egg, BIG 14 %, area 7 Frostfall Glacier)

Planner: pet planner (concept only). The lead builds `pets/GlacierYeti.py`. Binding for the build. Not built.

## v2 changes (from GLACIER_PLAN_REVIEW.md)
APPROVED WITH CHANGES, 7/10. Applied:
- Idle (MUST 1): the knuckle rake is removed (it was the act's arm sweep). New idle: plates lift 4 degrees and settle twice
  (f30-50). The head lowers 6 degrees at f55-75 with no snow contact. Back to rest by f100.
- Eyes (MUST 2): the AURORA slits are removed (8 degrees from the Stag's green eyes). New eyes: a BLACK socket with a PLATE_ICE
  (206,226,240) slit and a BLACK pupil. AURORA stays on the plate seams only.
- HEIGHT (NICE): 9.5 becomes 9.0 (the Roc is 9.0 and rarer, so the Yeti must not be taller).
- Kept (NICE): POLAR_NAVY (3 degrees from ThunderBull's body, cross-egg, accepted); the plates and the aurora seams are the separators.
- Act: the skid-and-brake act is accepted (review ruling 2). No change.
- Builder gates from review section 6 apply.

## 0. Facts
| | |
|---|---|
| Tier | Big |
| Odds | 14 % (money x1.56) |
| Egg / area | Glacier Egg, area 7 |
| Rig | biped (hunched, knuckle-walk capable) |
| Closest kit file | `pets/LavaGolem.py` (biped hulk, arms and knuckle rest). Hunch and arm plates are new |
| HEIGHT | 9.0 studs (top of the head at rest) |
| Tris | 8-11k (cap 15k) |

## 1. Read in one line
"A hunched navy snow beast with long arms plated in pale ice, a flat fierce face and a fanged underbite."
At 64 px: a hunched body with pale shoulder plates, a dark head with a brow shelf and pale plate-grey slits. It must NOT read as:
- LavaGolem (basalt-grey golem, magma seams, fist pound). The Yeti is navy with ice plates and no magma.
- an ape or a gorilla. Its arms carry ice plates and a skid act. It is not a chest beater.

## 2. Rarity ladder
- Big (14 %). It must beat Medium (Mammoth 26 %) and the starter (Lynx 50 %) on presence.
- Must be beaten by Roc (7.4 %), Titan (2.5 %) and Absolute Zero (0.1 %).
- Its hunched bulk must look bigger and heavier than the Mammoth's upright read.

## 3. Silhouette and anatomy (x H, H = 9.0 studs)
- Hunched: torso leans forward 25 degrees. Head forward and low. Head top 1.0H.
- Shoulders broad: 0.55H across. Chest 0.35H deep. Hips 0.30H wide, 10 % smaller than the chest.
- Arms long: elbow at 0.38H, knuckles down to 0.14H above the ground when hanging. Forearms thick (0.14H).
- Upper arms and shoulders wear PLATE_ICE slabs (smooth), like broken ice shelves.
- Legs short and thick: thigh 0.32H, shin 0.30H, feet 0.10H with 3 toes.
- Head: wide and flat, 0.22H wide. The brow shelf overhangs. The lower jaw juts with 2 IVORY underbite fangs.
- Ears: small and flat, set low.
- No tail.

## 4. Palette (Blender RGB; body brightest channel 200 >= 170)
| Name | RGB | Hex | Where | Share (side) |
|---|---|---|---|---|
| POLAR_NAVY | 120,128,200 | #7880C8 | torso, legs, head, arms under the plates (studded) | 52 % |
| PLATE_ICE | 206,226,240 | #CEE2F0 | shoulder and arm plates (smooth); the eye slits | 12 % |
| SNOW | 232,240,248 | #E8F0F8 | muzzle, chest V, face mask | 10 % |
| AURORA | 120,240,160 | #78F0A0 | THE accent: plate seam lines ONLY | 4 % |
| BROW | 52,58,96 | #343A60 | brow shelf, toes | 6 % |
| BLACK | 14,14,22 | #0E0E16 | claws, eye sockets and pupils, nostrils | 4 % |
| IVORY | 238,234,220 | #EEEADC | underbite fangs | 1 % |
| MOUTH | 86,18,30 | #56121E | mouth | <1 % |

- In game about (72,77,120): a dark navy.
- Accent family: AURORA GREEN, on seams only. Eyes are plate-grey, so the Stag's green eyes are not echoed.
- Gold: none.

## 5. Part list (x H)
- Torso: 2 blocks (chest 0.35H deep, waist 0.28H), taper bottom 0.66, a tuck segment from chest to waist.
- Shoulder plates: 2 per side, PLATE_ICE, 0.18H long, tilted up 20 degrees. Smooth.
- Arms: upper (0.25H) + forearm (0.18H) + fist (0.10H, 3 knuckle plates in PLATE_ICE).
- Legs: 2-bone (thigh 0.32H, shin 0.30H), feet 0.10H x 0.16H with 3 toes and BLACK claws (0.05H).
- Head: wide skull (0.22H), brow shelf (BROW), cheek blocks (POLAR_NAVY), SNOW muzzle (0.12H), jaw with 2 IVORY fangs (0.06H).
- AURORA seams: thin inlays along the plate edges (0.012H, flush).
- Hero piece: none required (Big). The signature shape is the hunch plus the ice-plate arms.
- Stud skin on torso, legs, arms, head. Not on plates, seams, fangs, claws or eye slits.

## 6. Face spec
- Eyes: BLACK socket with a PLATE_ICE slit (0.09H x 0.025H), BLACK slit pupil, tilted 20 degrees, inner corner low. Under a heavy BROW shelf 25 degrees inner-down.
- Nose: wide, BLACK, flat.
- Underbite: the lower jaw juts 0.03H past the upper. Two IVORY fangs.
- No glint, no round eyes, no smile.

## 7. Clips (30 fps)
- **idle (120 f loop): "plate settle" (review 2.3 MUST 1).** A slow weight sway (hip yaw +/-4 degrees). The plates lift 4 degrees and settle twice (f30-50). The head lowers 6 degrees at f55-75 with no snow contact. Back to rest by f100.
- **walk (48 f loop): knuckle walk.** Hunched. The fists plant on the ground in the stride. Torso bobs 0.02H per step. Walk slide ~0.
- **roar (60 f): "shoulder-heave bellow".** f0-12 the shoulders pull back. f12-24 they heave forward (shoulder yaw 10 degrees), twice. The head pitches up 15 degrees (within 30). f20-45 the jaw opens and the fangs show. f45-60 the jaw closes, the shoulders settle. No chest beat, no arms raised.
- **act_skid (100 f, in place): "snow skid and brake".** Beats:
  1. f0-16: the arms plant wide on the snow and the chest drops 0.06H. Ground contact stays >= -0.02.
  2. f16-34: the arms sweep forward and back in a wide arc (like a sled), the plates scrape the snow. Event `skid1` f22.
  3. f34-52: the chest slides low, the body stays in place (root moves 0.00H net). Event `skid2` f42.
  4. f52-66: the arms dig in and brake. A burst of ice shards from the fists. Event `brake` f58 (VFX on `Hand_L`, `Hand_R`).
  5. f66-100: the Yeti pushes up with a shoulder heave, rises to standing, the plates settle, and the body returns to rest.
  Limits: root net travel 0; ground_min_z >= -0.02 at the chest low point.

## 8. VFX anchor bones (named after the effect; parent bone in brackets)
- `FX_ShardBurst_L` [Hand_L], `FX_ShardBurst_R` [Hand_R]: ice shard burst on the brake.
- `FX_SnowPuff` [Chest]: snow puff on the skid.
- `FX_BreathCloud` [Mouth]: breath cloud on the roar.
- `FX_AuroraDust_L` [Plate_L], `FX_AuroraDust_R` [Plate_R]: faint aurora dust trickle.
- No eye anchors.

## 9. Distinctness
- LavaGolem (Fire): basalt-grey, magma seams, fist pound. The Yeti is navy, has ice plates and no magma, and its act is a skid.
- Treant (Grass biped): wood. The Yeti is fur-free and ice-plated.
- ThunderRex (Thunder biped): storm shells and cyan crystal. The Yeti is hunched and navy, with plate-grey eyes.
- Mammoth (Medium quad): the Yeti is biped, tailless, and has no trunk.
- Titan (Secret): upright, mauve, rounded studded pauldrons. The Yeti is hunched with tilted plates.

## 10. Animation references
TBD by builder. Suggested tags: "gorilla knuckle walk", "bear slide", "bear roar".

## 11. Reviewer gates
1. 64 px: the hunch, the pale shoulder plates and the dark head read.
2. Game camera: navy reads dark; the PLATE_ICE arms are the lightest part.
3. The act is a skid and a brake. It is not a pound, not a slam, not a chest beat.
4. The idle has no rake and no snow contact in the head drop.
5. Builder gates (review section 6): step-1 tris, collision_free, ground_min_z >= -0.02, linear 0, loops closed; icon strip at 64 and 128 px next to the Roc and LavaGolem; value shares; pose sheet of the skid beats.
