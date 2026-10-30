# CINDER WYRM OVERLORD - concept plan v2 (Fire Egg, ULTRA-RARE 0.5 %, area 4 Fire / Magma)

Planner: pet planner (concept only). The lead builds `pets/CinderOverlord.py` on the BlackDragon serpent kit. Binding.
Not built. The top pet of the Magma egg.

## v2 changes (from GLACIER_PLAN_REVIEW.md)
APPROVED WITH CHANGES, 7/10. Applied:
- Body (MUST 1): PLUM_OBS (176,150,168) is dull in game. It becomes (182,132,172), #B684AC (H 312, S 0.27). OBS_D stays for the scales.
- Outclass gate (MUST 2): at 64 px the gold rim must show at least 25 gold px in the icon. HEIGHT 10.5 stays above Rex's and
  Leviathan's 10.0.
- Tier (review section 0): 0.5 % is RARER than Thunder Rex (1 %) and Cosmic Leviathan (1 %). The Wyrm must beat those two too, not
  only the Phoenix and Ivonrath.
- Roar (NICE): the crown plate tilt is cut from 25 to 15 degrees, so the act owns the big plate lift (35 degrees).
- Step-1 A/B (NICE): compare against BlackDragon's `act_pearlchase` at step 1 (both are serpent kits).
- Builder gates from review section 6 apply.

## 0. Facts
| | |
|---|---|
| Tier | Ultra-rare (obsidian crown with a gold rim as the hero) |
| Odds | 0.5 % (money x5.01) |
| Egg / area | Magma (Fire) Egg, area 4 |
| Rig | serpent (no wings, no hind legs; two small clawed forearms at the chest) |
| Closest kit file | `pets/BlackDragon.py` (serpent S-coil and tube kit) |
| HEIGHT | 10.5 studs (top of the rearing head at the crown) |
| Length | about 3.0 x H, tail tip to snout |
| Tris | 10-14k |

## 1. Read in one line
"A volcanic serpent-dragon: mauve-obsidian scales with rose lava vents down the flanks, an obsidian crown with a gold rim, and two small clawed forearms."
At 64 px: a dark serpent head with a crown of obsidian plates and a gold rim, and a row of rose slits along the body. It must NOT read as:
- BlackDragon (violet eastern serpent with gold antlers, a pearl and legs). The Wyrm has no legs, no antlers, no pearl, and the crown is obsidian.
- Ivonrath (red bat-winged wyrm with fire breath). The Wyrm has no wings and no breath.
- InfernoPhoenix (feathered fire bird). The Wyrm is a serpent.

## 2. Rarity ladder
- Ultra-rare (0.5 %). The top of the Fire egg. It must beat Phoenix (2 %), Ivonrath (4 %), Cerberus (13 %), Golem (27 %) and Boar (53.5 %).
- It must ALSO beat the 1 % secrets: Thunder Rex and Cosmic Leviathan (review section 0). The Wyrm is rarer than both.
- Beaten only by the mythics (Absolute Zero 0.1 %, Eclipse Seraph 0.1 %).

## 3. Silhouette and anatomy (x H, H = 10.5 studs)
- Serpent body, 3.0H long, thickness 0.22H at the chest, tapering to 0.04H at the tail tip. No legs.
- The front third rises in an S: the neck lifts the head to 0.85H, then the head is at the crown height 1.0H.
- Head: wedge skull 0.22H long, brow ridges (OBS_D), a heavy jaw with 4 IVORY fangs (0.08H).
- Crown: 5 obsidian plates on the skull top. Centre plate tallest (0.12H). The plates have gold rims (the hero).
- Forearms: two small arms (0.12H) at the chest, each with 3 BLACK claws (0.05H). They are arms, not legs.
- Vents: 6 pairs of rose slits along the flanks (flush).
- Dorsal spikes: 5-6 small obsidian spikes down the back, shrinking to the tail (no sail).
- Tail: long, thin, tipped with a rose ember spike.

## 4. Palette (Blender RGB; body brightest channel 184 >= 170)
| Name | RGB | Hex | Where | Share (side) |
|---|---|---|---|---|
| PLUM_OBS | 182,132,172 | #B684AC | body scales (studded) | 44 % |
| OBS_D | 96,84,96 | #605460 | crown plates, brow ridges, dorsal spikes, scale bands | 16 % |
| PALE_S | 226,210,214 | #E2D2D6 | belly scutes, throat | 10 % |
| ROSE | 255,96,150 | #FF6096 | THE accent: flank vent slits, eye slits, crown edge lines | 8 % |
| ROSE_H | 255,190,214 | #FFBED6 | hot centres of the vents, ember tip | 2 % |
| GOLD | 255,196,50 | #FFC432 | THE hero: gold rim on the crown (house gold, crown only) | 3 % |
| BLACK | 14,14,22 | #0E0E16 | claws, eye sockets | 3 % |
| IVORY | 238,234,220 | #EEEADC | fangs | 1 % |
| MOUTH | 96,26,30 | #601A1E | mouth | 1 % |

- In game about (110,79,103): a dark mauve obsidian, with rose vents.
- Accent family: LAVA ROSE. No other Fire pet is rose. Nearest: BlackDragon TONGUE (Void, d 2, a small detail), AbyssWeaver VELVET (Void, a dark wine). Cross-egg, accepted.
- Gold: the crown rim. Gold is the hero rule for secrets; it is 3 % only.
- Why not orange: Fire already has four orange accents (Boar, Golem, Ivonrath, Phoenix). The Wyrm's rose is the one new family in the egg.

## 5. Part list (x H)
- Body: 12 segments along the S, each a tapered B.seg with an oval section (rnd 0.30). Thickness 0.22H at the chest down to 0.04H at the tail.
- Head: wedge skull, brow ridges (OBS_D), jaw block, 4 IVORY fangs.
- CROWN (hero):
  - 5 obsidian plates on the skull top (OBS_D), the centre 0.12H tall, two at 0.09H, two at 0.07H.
  - A GOLD rim: a thin gold band (0.012H) along the top edge of each plate, flush.
  - A ROSE_H tip on the centre plate.
  - At 64 px: a dark crown with a gold rim and a rose tip on a dark head.
- Forearms (x2): 2 blocks (0.12H), OBS_D with 3 BLACK claws each.
- Vents (x6 pairs): ROSE slit inlays (0.04H x 0.012H), flush.
- Dorsal spikes: 5-6 OBS_D spikes, smooth (`role detail`).
- Tail: 4 segments, a ROSE_H ember tip (0.05H).
- Stud skin on the body, the head, the crown base. Not on the vents, the gold rim, the spikes, the claws, the fangs.

## 6. Face spec
- Eyes: ROSE slits (0.07H x 0.02H), BLACK slit pupils, under a heavy OBS_D brow ridge (20 degrees inner-down).
- Fangs: 4 IVORY (0.08H), two upper, two lower, showing when the jaw opens.
- Nostrils: BLACK slits on the snout tip.
- No glint, no round eyes, no smile.

## 7. Clips (30 fps; no legs; the arms are small; no airborne spin)
- **idle (120 f loop): "ember breathing".** The head rises 6 degrees and sinks back (neck bones, +/-8 degrees limit). The flank vents pulse with the breath (VFX on each vent; the vents are flush, not moving). The tail tip flicks 8 degrees once at f80. Settles.
- **walk (48 f loop): slither.** A lateral S-wave runs from the tail to the head, with a 3-frame lag per bone. The forearms paddle at the chest (small, 6 degrees). No feet.
- **roar (66 f): "crown flare" (review NICE: plate tilt 15 degrees).** f0-14: the head is held level and the neck gathers (pitch up 12 degrees, within 30). f14-26: the crown plates tilt out and up (each plate rotates 15 degrees, lag 2 frames). Event `flare` f20 (ember spark on each crown plate). f26-44: the jaw opens, fangs show; the forearms spread. Event `roar` f30 (ember puff at `Mouth`). f44-66: close, the plates settle back.
- **act_molt (110 f, in place): "the crown sheds" (the act owns the big plate lift, 35 degrees).**
  1. f0-18: the neck arches gently (pitch up 25 degrees, within 30). The head stays level.
  2. f18-40: the crown plates lift one by one (lag 2 frames, each plate rotates 35 degrees up on its own bone). Event `lift1` f22 (ember sparks from the first plate).
  3. f40-62: the centre plate lifts the furthest and holds, then the outer plates drop back (events `lift2` f48, `shed` f56: small ember sparks falling).
  4. f62-84: the body ripples: a wave from the tail to the head (3-bone lag, 6 degrees per bone), shedding the old scale.
  5. f84-110: the plates reseat in reverse order, the neck returns to rest, and the body settles to the rest pose exactly.
  Limits: pitch-up <= 30; neck bones <= 8 degrees per axis; no spin; no head shake; ground_min_z >= -0.02 (the body lies on the ground in the ripple).

## 8. VFX anchor bones (named after the effect; parent bone in brackets)
- `FX_EmberSpark_1` to `FX_EmberSpark_5` [Crown_1 to Crown_5]: ember sparks on the lift and the shed.
- `FX_VentSmoke_1` to `FX_VentSmoke_6` [Vent_1 to Vent_6]: small smoke wisps (no fire breath; the breath is Ivonrath's).
- `FX_EmberPuff` [Mouth]: ember puff on the roar.
- `FX_EmberTip` [Tail_Tip]: an ember spark.
- `FX_EmberPaddle_L` [Claw_L], `FX_EmberPaddle_R` [Claw_R]: ember spark on the paddle.

## 9. Distinctness
- BlackDragon (Void): violet, gold antlers, a pearl, legs, the pearlchase act. The Wyrm is mauve-obsidian, with a crown of plates, no antlers, no legs, and the molt act.
- Ivonrath (Fire): crimson bat-winged wyrm, fire breath, emberdance act. The Wyrm has no wings, no breath, and a rose accent.
- InfernoPhoenix (Fire): feathered phoenix. The Wyrm is a serpent.
- Cerberus, LavaGolem, MoltenBoar (Fire): quads and golems. The Wyrm is a serpent with a crown.

## 10. Animation references
TBD by builder. Suggested tags: "snake slither", "dragon roar", "snake coil".

## 11. Reviewer gates (ultra-rare: must outclass Phoenix, Ivonrath, Thunder Rex and Cosmic Leviathan)
1. 64 px: the dark serpent head with a crown of plates and a gold rim reads. At least 25 gold px show in the icon.
2. Game camera: the body is dark mauve; the rose vents show along the flank; no orange, so it does not read as a Boar or a Golem.
3. Step 1: A/B the Wyrm against BlackDragon (`act_pearlchase` pose) and Ivonrath. No shared silhouette or colour family.
4. The act is a crown shed, not a pearl chase, not an ember dance, not a breath.
5. Builder gates (review section 6): step-1 tris, collision_free, ground_min_z >= -0.02, linear 0, loops closed; icon strip at 64 and 128 px next to Rex and Leviathan; value shares; pose sheet of the molt beats.
