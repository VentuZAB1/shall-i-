# BRAMBLE BADGER - concept plan v2 (Grass Egg, STARTER 40 %, area 1 Grass / Wood)

Planner: pet planner (concept only). The lead builds `pets/BrambleBadger.py`. Binding. Not built.

## v2 changes (from GLACIER_PLAN_REVIEW.md)
APPROVED WITH CHANGES, 7/10. Applied:
- Back (MUST 1): a mid-dark mantle band MANTLE (110,104,116), #6E6874, over the shoulders and nape. At least 10 % of the side
  view. The cool grey stays on the rest of the back.
- Act (MUST 2): `act_burrow` no longer says both "dig in turns" and "stay on the ground". Rule: the forepaws scoop, lifting at
  most 0.05H, and touch down at each scoop. Ground contact >= -0.02.
- Thorns (NICE): kept short and low. 0.08-0.10H (was 0.10-0.14H). The Basilisk owns the frill; the badger is not a spike row.
- Kept: the inverted colouring (pale back, dark belly) is accepted (review ruling 4).
- Builder gates from review section 6 apply.

## 0. Facts
| | |
|---|---|
| Tier | Starter |
| Odds | 40 % (money x1.08) |
| Egg / area | Wood (Grass) Egg, area 1 |
| Rig | quad (low, stocky) |
| Closest kit file | `pets/ForestStag.py` (quad leg chain, scratch act pattern) |
| HEIGHT | 7.0 studs (top of the thorn crest) |
| Tris | 5-8k |

## 1. Read in one line
"A low, grumpy badger: a pale grey back with a dark mantle, a short crest of amber bramble thorns, a black belly and legs, and white face stripes."
At 64 px: a squat grey body with a dark shoulder band, a row of short amber thorns, and a striped white head. It must NOT read as:
- ForestStag (brown stag with antlers). The badger is low, has no antlers, and has a striped face.
- MossbackTortoise (green domed shell). The badger has a thorn crest and four legs.
- VenomBasilisk (green frilled reptile). The badger is a mammal, with fur blocks and no sail.

## 2. Rarity ladder
- Starter, the most common Grass pet (40 %). It beats nothing on rarity.
- Must look like a real pet of the Grass egg, with a clear amber accent.
- Beaten by all other Grass pets: Tortoise (30 %), Stag (16 %), Treant (8.5 %), Basilisk (3.5 %), Mantis (2 %).

## 3. Silhouette and anatomy (x H, H = 7.0 studs)
- Low, wide body. Withers 0.46H. Body length 1.05H, chest deep 0.34H. A heavy front, a narrower rump.
- Head: wedge snout, 0.30H long, flat-topped. Head top 0.70H. Broad cheeks.
- Thorn crest: 9 short tapered AMBER thorns from the nape to the tail base, each 0.08-0.10H tall, shortest at the tail.
- Legs: short and stout. Ground to elbow 0.22H. Forefeet 1.1 x leg width, 4 dark claws (0.06H).
- Tail: stub, 0.22H, with a dark band.
- Belly and legs dark (BELLY_D). The grey back and dark mantle are the real badger's read.

## 4. Palette (Blender RGB; body brightest channel 180 >= 170)
| Name | RGB | Hex | Where | Share (side) |
|---|---|---|---|---|
| GREY | 176,172,180 | #B0ACB4 | back, flanks, shoulders (studded) | 40 % |
| MANTLE | 110,104,116 | #6E6874 | mantle band over the shoulders and nape (at least 10 % of the side view) | 10 % |
| BELLY_D | 72,58,54 | #483A36 | belly, legs, lower skirt | 17 % |
| FACE_PALE | 240,236,226 | #F0ECE2 | head, cheeks, muzzle | 12 % |
| AMBER | 236,150,60 | #EC963C | THE accent: thorn crest (smooth), eye slits | 6 % |
| THORN_D | 120,70,36 | #784624 | thorn bases | 3 % |
| BLACK | 14,14,22 | #0E0E16 | face stripes, nose, claws | 6 % |
| IVORY | 238,234,220 | #EEEADC | two small fangs | <1 % |

- The colour blocking is the real badger's: grey back and mantle, dark belly and legs, white face. This is the one inversion of the house "dark body, pale underside" rule. Accepted (review ruling 4).
- In game about (106,103,108) for the back: a mid-grey, with a darker mantle.
- Accent family: AMBER thorn. Nearest: Treant HEART (Grass, d 1, a brown body), Solar Lion FUR (Celestial, d 1, tawny body). Accepted cross-egg (review ruling 9). The amber is saturated (S 0.75).
- Gold: none.

## 5. Part list (x H)
- Body: torso block 0.34H deep x 0.42H wide x 0.75H long, bottom taper, `rnd 0.30`, a tuck from chest to waist.
- Mantle: a band of MANTLE blocks over the shoulders and nape, flush, at least 10 % of the side view.
- Shoulders: a heavy front block, 0.55H wide.
- Head: wedge skull (0.30H), white FACE_PALE cheek blocks, a dark brow bar.
- Stripes: two BLACK bars from each eye back to the ear (flush inlays, 0.012H thick).
- Thorn crest: 9 short tapered AMBER spikes (0.08-0.10H, smooth, `role detail`), each on a THORN_D base block.
- Legs: 4 x 2 bones (upper 0.12H, lower 0.10H), feet 1.1 x leg width with 4 BLACK claws.
- Tail: stub, 0.22H, BLACK band.
- Hero piece: none (starter). Signature shape = the amber thorn crest on the grey back.
- Stud skin on the grey back, the cheeks and the belly. Not on the thorns, stripes, claws, eyes.

## 6. Face spec
- Eyes: AMBER slits (0.07H x 0.02H), BLACK slit pupils, under a BLACK brow bar angled 20 degrees inner-down. Small and mean.
- Two dark stripes on the white face run back from the eyes (the badger mark).
- Nose: BLACK, wide, flat.
- Mouth: closed, with two small IVORY fangs.
- No glint, no round eyes, no smile.

## 7. Clips (30 fps)
- **idle (120 f loop): "nose-down sniff".** The head drops to the ground (pitch down 25 degrees, within 30), sniffs left and right (yaw +/-8 degrees), then lifts. The thorn crest lifts 3 degrees once at f70. Settles. No head shake.
- **walk (30 f loop, quad walk):** a low, stocky waddle-trot. The body rocks 0.02H per step. Walk slide ~0.
- **roar (60 f): "hunker growl".** f0-20 the body drops (root -0.05H), the thorns flatten back 15 degrees, the ears go back. f20-45 the head drops to the ground and the jaw opens to the fangs, a low growl. Event `growl` f30 (dust puff at `Mouth`). f45-60 close, rise to rest.
- **act_burrow (100 f, in place): "dig the burrow" (review 2.7 MUST 2).** Rule: the forepaws scoop, lifting at most 0.05H, and touch down at each scoop. Ground contact >= -0.02.
  1. f0-18: the nose drops to the ground and sniffs (head pitch down 25 degrees).
  2. f18-50: the forepaws scoop in turns (left, right, left). Each paw lifts at most 0.05H and touches down at each scoop. Events `dig1` f26, `dig2` f36, `dig3` f46 (a dirt puff on the paws).
  3. f50-62: the hind legs kick back twice (dirt kicks, `kick1` f54, `kick2` f60). The hind feet touch down between kicks.
  4. f62-78: the badger pops its head up and looks around (head yaw +/-14 degrees, the thorns lift 3 degrees).
  5. f78-100: back to four paws, exact rest pose.

## 8. VFX anchor bones (named after the effect; parent bone in brackets)
- `FX_LeafDust` [Thorn_1 to Thorn_9, grouped]: optional tiny leaf-dust puff on the act only. The thorns themselves are smooth.
- `FX_DirtPuff_FL`, `FX_DirtPuff_FR`, `FX_DirtPuff_BL`, `FX_DirtPuff_BR` [Paw_FL, Paw_FR, Paw_BL, Paw_BR]: dirt puffs on the dig and kick.
- `FX_DustGrowl` [Mouth]: small dust puff on the growl.
- No eye anchors.

## 9. Distinctness
- ForestStag (Grass, brown stag): antlers, scratch act. The badger is low, has no antlers, and its act is a burrow.
- MossbackTortoise (Grass, green shell): the badger is a mammal, with a thorn crest.
- VenomBasilisk (Grass, green reptile frill): the badger has a striped face and grey fur.
- Treant (Grass, wood): the badger is an animal.
- ThornbladeMantis (Grass, jade mantis, act thornstrike): the badger has four legs and an amber accent, not a jade body with ruby.

## 10. Animation references
TBD by builder. Suggested tags: "badger dig", "badger walk", "badger growl".

## 11. Reviewer gates
1. 64 px: the grey back with the dark mantle band and the amber thorn row read. The white face stripes read.
2. Game camera: the back is mid-grey with a darker mantle; the belly is dark. The amber crest is the brightest accent in the Grass egg.
3. The burrow act is a dig with scoops that lift at most 0.05H. It is not a rooting, not a scratch.
4. The growl is a hunker, not a jaw champ, not a bristle, not a charge.
5. Builder gates (review section 6): step-1 tris, collision_free, ground_min_z >= -0.02, linear 0, loops closed; icon strip at 64 and 128 px next to the Stag and Basilisk; value shares; pose sheet of the dig.
