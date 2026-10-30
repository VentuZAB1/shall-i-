# ABSOLUTE ZERO DRAGON - concept plan v2 (Glacier Egg, MYTHIC 0.1 %, area 7 Frostfall Glacier)

Planner: pet planner (concept only). The lead builds `pets/FrostcrownDragon.py`. Binding. Not built.
This is the rarest pet in the game. It must beat every pet, including Thunder Rex (1 %) and Cosmic Leviathan (1 %).

## v2 changes (from GLACIER_PLAN_REVIEW.md)
APPROVED WITH CHANGES, 7/10. Applied:
- HEIGHT (MUST 1): 11.0 becomes 11.5. The mythic is now one of the two tallest pets in the game, tied with the Eclipse Seraph (also 11.5). ForestStag (16 %) is 11.0.
- Body (MUST 2): STEEL_BLUE (150,176,206) becomes (124,160,216), #7CA0D8 (H 216, S 0.43). In game about (74,96,130), not grey.
- Act (MUST 3): `act_stillfreeze` no longer runs a lagged wave (that was Cinder's tail-to-head ripple). All five frost fins rise
  together, with no lag. Six beats, as the review wrote them.
- Tris (MUST 4): step-1 gate at 13k. The 15k cap is the ceiling. Report the count before the full build.
- Dorsal (NICE): the seven ICE_W shards become five flat frost fins (blade section, width 2:1), so they read as a fin row and
  not Rex's spike row. Five is the count; if the step-1 tris leave room, the owner may ask for seven.
- Builder gates from review section 6 apply.

## 0. Facts
| | |
|---|---|
| Tier | MYTHIC (gold horn crown hero) |
| Odds | 0.1 % (money x8.80) |
| Egg / area | Glacier Egg, area 7 |
| Rig | wing-quad flyer (the CelestialDragon wingquad kit: wings, horns, legs) |
| Closest kit files | `pets/CelestialDragon.py` (wingquad, horn and crown work). `pets/Ivonrath.py` (wingquad, membrane wings, claw fingers) |
| HEIGHT | 11.5 studs (top of the horn crown). The tallest pet in the game |
| Wingspan | 2.3 x H tip to tip |
| Tris | 13k target (step-1 gate), 15k cap |

## 1. Read in one line
"A colossal steel-blue ice dragon: studded scales, a row of five ice-white frost fins down its back, membrane wings of frost, and a gold horn crown that breathes out a cold mist."
At 64 px: a dragon with big wings, a gold crown of horns on the head, and a row of white fins along the back. It must NOT read as:
- CelestialDragon (indigo wingquad, pearl horns, star crown, eclipse act). AZD is steel-blue, has gold horns, white fins, and the stillfreeze act.
- Ivonrath (red bat dragon, fire breath). AZD is cold blue, with a frost mist, not fire.
- BlackDragon (violet serpent, gold antlers, pearl). AZD has four legs and wings, and its gold horns sweep back from the brow, not from the antlers.

## 2. Rarity ladder
- Mythic (0.1 %). It must beat all 29 other pets in look and presence.
- Must beat the 1 % secrets (Thunder Rex, Cosmic Leviathan) and the Glacier Titan (2.5 %).
- Nothing beats it. It is the top of the whole game. It is tied for the tallest pet (11.5) with the Eclipse Seraph.

## 3. Silhouette and anatomy (x H, H = 11.5 studs)
- Four-legged dragon. Shoulders 0.55H. Chest 0.38H deep. Body length (chest to tail base) 1.25H.
- Long S-neck (0.35H), head on top at 1.0H. Head skull 0.26H long, wedge, brow spines.
- Horns: two long gold horns from the brow, swept back 0.35H, with a diadem band (3 tiny gold points).
- Wings: bat-like. Upper arm 0.30H, forearm 0.36H, 4 finger bones, membrane between the fingers (thin, >= 0.035H). Span 2.3H.
- Dorsal fins: FIVE flat ICE_W frost fins (blade section, width 2:1) down the neck and back, 0.12-0.18H tall, spaced 0.30H apart. They read as a fin row, not spikes.
- Legs: 4 columns, 2 bones each; 4 BLACK claws per foot.
- Tail: long, 0.9H, ends in an ICE_W crystal spike tip, not a leaf or a crescent.
- Chest: pale belly plates (ICE_BELLY) from throat to belly.

## 4. Palette (Blender RGB; body brightest channel 216 >= 170)
| Name | RGB | Hex | Where | Share (side) |
|---|---|---|---|---|
| STEEL_BLUE | 124,160,216 | #7CA0D8 | body, neck, legs, tail, head (studded) | 40 % |
| ICE_BELLY | 210,226,246 | #D2E2F6 | throat, belly plates | 14 % |
| ICE_W | 236,246,252 | #ECF6FC | dorsal frost fins, tail tip, claws (smooth) | 10 % |
| MEMBRANE | 190,206,236 | #BECEEC | wing membranes (smooth) | 8 % |
| DARK | 66,72,108 | #42486C | brow spines, back line, claw bases | 6 % |
| GOLD | 255,196,50 | #FFC432 | THE hero: horn crown (horns, diadem, tips) | 4 % |
| GOLD_D | 214,150,30 | #D6961E | horn inner faces, diadem inner | 1 % |
| EYE_HOT | 244,250,255 | #F4FAFF | eye slit | 1 % |
| MOUTH | 46,40,80 | #2E2850 | mouth cavity (cold dark violet, not red) | 1 % |
| BLACK | 14,14,22 | #0E0E16 | pupils, nostrils, claws | 2 % |

- In game about (74,96,130) for the body: a steel-blue dragon, with gold and white on top.
- Gold: house GOLD, the crown only (the owner's rule). It is the same gold as Black Dragon's antlers, so the silhouette separates them: horns from the brow, swept back.
- Accent family: ICE WHITE (crystal fins) plus the gold crown. No other pet has a steel-blue body with white frost fins and a gold horn crown.
- Hue check: steel-blue (216 deg, S 0.43). Nearest saturated: CosmicLeviathan DEEP (Celestial, a small bridge step) and CelestialDragon BODY (indigo, S 0.62). The AZD is a lighter, cooler blue, so it reads differently in value and hue.

## 5. Part list (x H)
- Torso: chest block 0.38H deep x 0.50H wide x 0.85H long, belly taper (0.66, 0.56), `rnd 0.30`, tuck to the waist.
- Neck: 3 segments on an S, 0.35H total, STEEL_BLUE with ICE_BELLY throat.
- Head: skull 0.26H, brow spines 2 x 0.06H (DARK), cheek plates, snout 0.14H, nostrils BLACK.
- HERO horn crown (GOLD):
  - Two main horns from the brow, 0.35H long, swept back 30 degrees, base 0.05H thick, tips GOLD_D.
  - Diadem: a thin band (0.03H tall) around the skull top with three small gold points (0.05H).
  - At 64 px: gold horns read as a crown from the front and the game camera.
- Dorsal frost fins: 5 ICE_W blades, flat, width 2:1 (chord to thickness), 0.12-0.18H tall, smooth. Each sits on its own bone (`Fin_1` to `Fin_5`).
- Wings: arm bone, 4 finger bones, membranes MEMBRANE (smooth panels, thickness 0.035H). Scallop trailing edges.
- Legs: 4 x 2 bones, 0.30H upper, 0.28H lower, 4 BLACK claws per foot (0.05H).
- Tail: 4 segments, 0.9H total, ICE_W crystal tip (0.08H).
- Stud skin on body, neck, head, legs, tail base. Not on the fins, the membranes, the horns, the claws.

## 6. Face spec
- Eye: long slit, EYE_HOT (0.10H x 0.025H), BLACK slit pupil, tilted 20 degrees, inner corner low. Under a DARK brow spine.
- No glint. No round pupil.
- Nostrils: BLACK slits on the snout tip.
- Mouth: MOUTH cavity. Ice-white teeth (ICE_W) on the upper jaw.

## 7. Clips (30 fps)
- **idle (120 f loop): "frost hum".** The wings half-fold and open (f0-60). The five fins tick 2 degrees together (one bone group, no stagger). The head sways slowly (yaw +/-8 degrees, neck +/-8). A small frost mist puff from `Mouth` at f80 (VFX). Settle.
- **walk (40 f loop, quad walk):** a four-legged stride. Wings folded. Walk slide ~0.
- **fly (flap loop):** wings flap and the legs pump. Takeoff event `launch`, land event `touch`. Wings never cross the body.
- **roar (66 f): "crystal-chime roar".** f0-14: the head rises 15 degrees and the wings spread to half. f14-30: the jaw opens; the five fins stand up 15 degrees and buzz (+/-2 degrees, fast). Event `roar` f24 (frost ring at Mouth). f30-54: hold; the horns hum (tiny +/-1 degree ticks). f54-66: the jaw closes, the wings fold. Head pitch-up <= 30.
- **act_stillfreeze (110 f, in place): "absolute stillness" (review 2.6 MUST 3, six beats as written).**
  1. f0-14: the dragon inhales (chest rises 0.02H). Wings and tail go still.
  2. f14-22: all five fins rise together 25 degrees, no lag. One frost click at f16 (event `click`).
  3. f22-44: the head presses down to the ice (pitch down 25 degrees, within 30). The jaw opens. The snout is the only low point (>= -0.02).
  4. f44-58: a frost mist cone from `Mouth` (event `frost` f50, VFX).
  5. f58-80: all five fins fall together. The head lifts.
  6. f80-110: the wings fold, exact rest pose.
  Limits: no spin, no flip, no head shake. No wave: the fins never run tail-to-neck.

## 8. VFX anchor bones (named after the effect; parent bone in brackets)
- `FX_FrostBreath` [Mouth]: frost breath cone (small; the breath is VFX, not the act's identity).
- `FX_IceTrail_L` [Horn_L], `FX_IceTrail_R` [Horn_R]: a thin ice trail from the horn tips.
- `FX_FinSpark_1` to `FX_FinSpark_5` [Fin_1 to Fin_5]: tiny sparkle on each frost fin (the click and the frost events).
- `FX_FrostTrail_L` [Wing_Tip_L], `FX_FrostTrail_R` [Wing_Tip_R]: frost trail in flight.
- `FX_IceDust` [Tail_Tip]: ice dust.
- `FX_ColdLight` [Core]: an empty anchor at the chest for a cold-light PointLight (no glow mesh).

## 9. Distinctness
- CelestialDragon (Celestial, indigo): royal arch, eclipse act, pearl horns. AZD: steel-blue, gold horns, five white fins that rise together, the stillfreeze press.
- Ivonrath (Fire, red wyrm): fire breath, emberdance act. AZD is cold, with a frost mist.
- BlackDragon (Void, violet serpent): gold antlers, pearl, pearlchase act. AZD has legs and wings and gold horns from the brow.
- CosmicLeviathan (Celestial, fish): obsidian and plum, gold crown. AZD is a dragon, not a fish.
- Thunder Rex: cyan crystals, storm breath. AZD is steel-blue with white fins and a frost mist.

## 10. Animation references
TBD by builder. Suggested tags: "dragon fly", "dragon roar", "dragon idle".

## 11. Reviewer gates (the strictest)
1. Step 1: tris count reported (target 13k, cap 15k). `collision_free: true`, ground_min_z >= -0.02 at the head press, linear 0, loops closed.
2. 64 px: the gold horns plus the white fin row read from the front and the side. The gold crown is >= 25 gold px.
3. The tallest pet check: AZD and the Eclipse Seraph are both 11.5, the two tallest models in the roster. Both are above ForestStag (11.0) and every other pet.
4. A/B pairs at 64 px: AZD next to CelestialDragon, BlackDragon, Ivonrath and ThunderRex. None reads as the same family.
5. The act is a fin rise and a frost press, all together. It is not an eclipse, a pearl chase, an ember dance or a storm breath.
