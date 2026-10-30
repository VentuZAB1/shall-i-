# BLIZZARD ROC - concept plan v2 (Glacier Egg, HIGH 7.4 %, flyer, area 7 Frostfall Glacier)

Planner: pet planner (concept only). The lead builds `pets/BlizzardRoc.py` on the Thunderbird kit. Binding. Not built.

## v2 changes (from GLACIER_PLAN_REVIEW.md)
APPROVED WITH CHANGES, 6/10. Applied (the Roc read as a recoloured Thunderbird; these break that):
- Tail (MUST 1): no 7-feather white fan. Four plain tail feathers, CHAR tips, FROST_V tip bars.
- Crest (MUST 2): the three plumes stand erect, 60-75 degrees from the head (not swept back). Plume tips FROST_V.
- Head (MUST 3): SNOW kept, plus a CHAR eye mask and brow. The eye is a BLACK socket with a FROST_V slit.
- Body (MUST 4): STORM_GREY (176,182,196) becomes (176,178,186), #B0B2BA (H 228 -> 222, S 0.10). It leaves the blue cluster.
- Act (MUST 5): `act_bow` has zero net root travel. The forward-back bob is a vertical bob (root z +/-0.03H, two bobs). The tail-fan
  shake is replaced by two tail flicks of 6 degrees.
- Walk (MUST 6): no hop. A plain walk with the wings folded.
- NICE: three CHAR breast bars (snowy-owl style) on the SNOW breast, so the white bird keeps dark tones.
- Builder gates from review section 6 apply.

## 0. Facts
| | |
|---|---|
| Tier | High (flies) |
| Odds | 7.4 % (money x1.95) |
| Egg / area | Glacier Egg, area 7 |
| Rig | wing-biped flyer (the Thunderbird kit: `wing3.Wing` 3-row feather wing, cloak-fold ground pose, LIFT1-4 fold/open) |
| Closest kit file | `pets/Thunderbird.py` (wingbiped). Clip set: fly / takeoff (event `launch`) / land (event `touch`) |
| HEIGHT | 9.0 studs (top of the crest at rest) |
| Wingspan | 2.0-2.4 x H tip to tip |
| Tris | 9-13k (cap 15k) |

## 1. Read in one line
"A giant snowy bird of prey: white breast and head, a storm-grey back, charcoal flight feathers, an erect frost crest and frost-violet trim."
At 64 px: a white-breasted bird with a grey back, big wings spread, and an upright crest of frost plumes. It must NOT read as:
- Thunderbird (white head, teal breast, gold beak, bolt tips, a white fan tail, stoop act). The Roc has grey wings, violet trim, no fan and no bolts.
- Griffin (brown eagle-lion, mantle act, sky screech). The Roc is a true bird with no lion body.
- a dove or a chibi bird. The beak is a hook; the eye is a fierce slit under a CHAR mask.

## 2. Rarity ladder
- High (7.4 %). It must look bigger and more striking than the Yeti (14 %) and the Mammoth (26 %).
- Must be beaten by Permafrost Titan (2.5 %) and Frostcrown Dragon (0.1 %).
- High beats Big on look, so the wing span and the crest carry it.

## 3. Silhouette and anatomy (x H, H = 9.0 studs)
- Body leans 35 degrees. Chest deep 0.30H. Body length (head to tail base) 0.90H.
- Neck S-curve, 0.28H long (0.12H thick). Head 0.20H long, rounded skull with a brow ridge (CHAR).
- Beak: steel hook, 0.10H long, curved down with a notch.
- Crest: 3 plumes standing erect, 60-75 degrees from the head (SNOW blocks, FROST_V tips). They are upright, not swept back.
- Wings: open span 2.0-2.4H. Three feather rows (coverts, secondaries, primaries) per wing.
- Tail: four plain feathers, 0.40H long, CHAR tips with FROST_V bars. No fan.
- Legs: scaled, 0.25H, 3 front toes and 1 back talon, BLACK talons 0.06H.

## 4. Palette (Blender RGB; body brightest channel 226 >= 170)
| Name | RGB | Hex | Where | Share (side) |
|---|---|---|---|---|
| SNOW | 238,242,250 | #EEF2FA | head, breast, belly, crest | 36 % |
| STORM_GREY | 176,178,186 | #B0B2BA | mantle, back, wing coverts | 25 % |
| CHAR | 58,64,80 | #3A4050 | primaries, tail tips, legs, eye mask and brow, breast bars | 16 % |
| PALE_G | 206,214,226 | #CED6E2 | breast shading strip that follows the slope | 6 % |
| FROST_V | 176,140,255 | #B08CFF | THE accent: eye slits, primary-tip bars, crest tips, tail-tip bars | 5 % |
| BEAK | 62,60,72 | #3E3C48 | beak, cere | 3 % |
| BLACK | 14,14,22 | #0E0E16 | talons, eye sockets | 3 % |
| MOUTH | 96,26,30 | #601A1E | inside beak | <1 % |

- Dark rich back and CHAR mask on a pale breast: a snowy raptor, not a white plate.
- Accent family: FROST VIOLET (pale lilac). Nearest: BlackDragon PEARL_C (Void, d 4) and ShadePanther PALE (Void, d 5). Accepted (review ruling, Roc FROST_V vs Panther VIOLET).
- Gold: none.

## 5. Part list (x H)
- Body: chest block 0.30H deep, body block 0.90H, taper under the belly, `rnd 0.30`.
- Neck: 2 segments, 0.28H total, SNOW front / STORM_GREY back.
- Head: skull block 0.20H, CHAR brow ridge (0.03H proud), CHAR eye mask, beak root + hook (BEAK).
- Crest: 3 plumes, each 0.10H long, standing erect (60-75 degrees from the head), SNOW with FROST_V tips.
- Breast: 3 CHAR bars (0.03H thick) across the SNOW breast, following the slope.
- Wings (x2): wing3 kit (coverts STORM_GREY, secondaries STORM_GREY, primaries CHAR with FROST_V tip bars).
- Tail: four feathers (0.40H), CHAR tips with FROST_V bars.
- Legs (x2): 2-bone, 0.25H, BLACK talons.
- Hero piece: none required (High). The signature is the span and the erect crest.
- Stud skin on body, neck, head, mantle. Feathers are smooth blocks with a saw edge (no studs on the feather tips).

## 6. Face spec
- Eye: CHAR mask around a BLACK socket, FROST_V slit (0.08H x 0.02H), tilted 18 degrees, inner corner low. BLACK slit pupil. Under the CHAR brow ridge.
- No glint, no round eye.
- Beak: hooked, notch, BEAK colour, MOUTH inside.

## 7. Clips (30 fps; flyers flap wings AND pump legs; wings never through each other or the body)
- **idle (120 f loop): "frost shed".** The wings lift half-open and fall (f10-40). Frost falls off the primary tips (VFX on `Wing_Tip_L/R`). The tail lowers and raises 6 degrees. The head turns slowly (yaw +/-10 degrees, neck +/-8). No head shake. NOT a watch-scan (Griffin owns the watch).
- **fly / takeoff / land (kit set):** the standard wingbiped set. Takeoff event `launch` at the first lift. Land event `touch` at the ground contact. Flap wings and pump legs in the flight loop.
- **walk (30 f loop, ground): plain walk, wings folded.** No hop. The walk is a normal stride, not an airborne hop (review MUST 6).
- **roar (60 f): "snap-open".** f0-14 the crest and neck gather (neck pitch-up 12 degrees). f14-22 the wings snap out to full span and hold. f18 event `roar`. f22-40 hold; the crest stays erect; the beak opens. f40-60 the wings fold back in, the crest settles.
- **act_bow (110 f, in place): "courtship bow" (review MUST 5).** Root travel is zero net.
  1. f0-22: the chest lowers. The head and neck bend forward (head pitch down 25 degrees). The tail lifts behind.
  2. f22-44: two vertical bobs (root z +/-0.03H, net root travel 0). The wings droop half-open.
  3. f44-64: the neck rises, the crest flares erect, the wings lift and snap closed. Event `snap` f58 (frost puff on `Wing_Tip_L/R`).
  4. f64-88: two tail flicks of 6 degrees (the four tail feathers snap). No head shake.
  5. f88-110: back to the rest pose.
  Limits: no airborne spin, no flip; pitch-down <= 30 degrees; ground_min_z >= -0.02.

## 8. VFX anchor bones (named after the effect; parent bone in brackets)
- `FX_FrostTrail_L` [Wing_Tip_L], `FX_FrostTrail_R` [Wing_Tip_R]: frost trail ribbons in flight (the signature trail).
- `FX_CrestSparkle` [Crest]: frost sparkle on the crest.
- `FX_BreathCloud` [Beak]: a small breath cloud.
- `FX_FrostDust` [Tail]: a frost dust drift.
- `FX_SnowPuff_LandL` [Foot_L], `FX_SnowPuff_LandR` [Foot_R]: snow puff on landing.

## 9. Distinctness
- Thunderbird (Thunder, wingbiped): white head, teal breast, bolts, a white fan tail, stoop act. The Roc has a grey back, CHAR mask, four tail feathers, an erect crest, violet trim, and the bow act.
- Griffin (Celestial, wingquad): brown lion body, mantle act, watch idle. The Roc is a bird only.
- StormWyvern (Thunder, wyvern): membrane wings, hood shriek. The Roc has feather wings.
- Ivonrath, CelestialDragon: dragon wings. The Roc has feathered wings.

## 10. Animation references
TBD by builder. Suggested tags: "bird display", "bird fly", "eagle take off".

## 11. Reviewer gates
1. 64 px: the white breast, the CHAR mask and the grey back read. The erect crest reads.
2. Game camera: the back is the darkest part; no white fan, no teal.
3. Flight: wings never through the body; legs pump; `collision_free: true`.
4. The bow is not a stoop; the snap-open is not Griffin's sky screech; the walk has no hop.
5. Builder gates (review section 6): step-1 tris, collision_free, ground_min_z >= -0.02, linear 0, loops closed; icon strip at 64 and 128 px next to the Thunderbird and Griffin; value shares; pose sheet of the bow beats.
