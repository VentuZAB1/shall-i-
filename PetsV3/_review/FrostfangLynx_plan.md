# FROSTFANG LYNX - concept plan v2 (Glacier Egg, STARTER 50 %, area 7 Frostfall Glacier)

Planner: pet planner (concept only). The lead builds `pets/FrostfangLynx.py`. Binding for the build. Any change needs the
owner's OK. Nothing is built or in Studio.

## v2 changes (from GLACIER_PLAN_REVIEW.md)
APPROVED WITH CHANGES, 7/10. Applied:
- Body: WARM_SILVER (184,172,160) becomes (190,172,150), #BEAC96. A warmer sand-silver, away from the Badger's grey.
- Pattern (MUST 2): BACK_SHADE (126,116,110) rosette spots on the flanks. The rosettes cover at least 20 % of the side view.
- Act (MUST 3): the wall is removed (a prop the pet does not own). `act_wallclaw` is replaced by `act_clawflex` (96 f, in place).
  The forepaws-on-the-chest lift was NightmareStallion's rear. No rear now.
- Idle (MUST 4): the head may yaw +/-14 degrees, but the neck yaw stays within 8 degrees (the head takes the rest of the drift).
- NICE: ICE_CLAW stays smooth, and the tufts stay blocks only.
- Builder gates from review section 6 apply.

## 0. Facts
| | |
|---|---|
| Tier | Starter (the most common Glacier pet) |
| Odds | 50 % (money x1.00 from `max(1, (50/odds)^0.35)`) |
| Egg / area | Glacier Egg, area 7 Frostfall Glacier |
| Rig | quad (cat proportions, paws like snowshoes) |
| Closest kit file | `pets/ShadePanther.py` (cat quad + pounce kit); leg chain from `pets/ForestStag.py` |
| HEIGHT | 7.0 studs (top of the ear tufts) |
| Tris | 6-9k (step-1 gate: report the count; cap 15k) |

## 1. Read in one line
"A lean ice lynx with frosted ear tufts, icy claws and a short tail: quick, fierce, and small."
At 64 px: a cat head wedge with two pale ear tufts, rosette flanks and two cyan slit eyes. It must NOT read as:
- ShadePanther (indigo-black big cat with violet crystals, pounce act). The Lynx is sand-silver, with no crystals.
- a kitten. No round eyes, no smile, no blush.
- Raiju or a wolf (long snout, storm blue).

## 2. Rarity ladder
- Lowest tier of area 7. It beats nothing on rarity.
- Must look finished and fierce, not like a placeholder: at least as strong as the Grass starter (Bramble Badger).
- Beaten by every other Glacier pet (Mammoth 26 %, Yeti 14 %, Roc 7.4 %, Titan 2.5 %, Absolute Zero 0.1 %).

## 3. Silhouette and anatomy (sizes x H, H = 7.0 studs)
- Lean cat, withers 0.62H, chest-to-rump body 0.95H, belly tucked (no box belly; the belly line rises to the hind legs).
- Head: wedge with a flat forehead; skull 0.20H long, 0.13H wide. Short muzzle. Cheek ruffs of SNOW blocks flare out.
- Ear tufts: two tall tapered ears (0.10H), SNOW fronts, BACK_SHADE backs, ICE tips (0.03H). Blocks only, no strand fringe.
- Legs: long and thin for a cat. Ground to elbow 0.42H. Paws 1.25 x leg width (snowshoe look), 4 claws each.
- Tail: short, 0.30H, three segments, a BLACK tip band of 0.05H.
- Neck 40 degrees up; the only neck bend (no S).
- Flanks: rosette spots (BACK_SHADE) over at least 20 % of the side view.

## 4. Palette (Blender RGB; body brightest channel 190 >= 170)
| Name | RGB | Hex | Where | Share (side view) |
|---|---|---|---|---|
| WARM_SILVER | 190,172,150 | #BEAC96 | body, legs, head sides (studded) | 40 % |
| BACK_SHADE | 126,116,110 | #7E746E | back saddle, brows, ear backs, THE rosette spots on the flanks (at least 20 % of the side view) | 26 % |
| SNOW | 240,244,250 | #F0F4FA | underside, muzzle, cheek ruffs, paw socks, ear fronts | 20 % |
| ICE | 150,236,255 | #96ECFF | THE accent: eye slits, ear-tuft tips | 5 % |
| ICE_CLAW | 214,244,255 | #D6F4FF | claws (smooth) | 2 % |
| BLACK | 14,14,22 | #0E0E16 | nose, eye sockets, tail tip band | 3 % |
| MOUTH | 86,18,30 | #56121E | mouth inside | <1 % |
| TEETH | 238,234,220 | #EEEADC | two small fangs | <1 % |

- No gold. No glow.
- Accent family: ICE CYAN, pale (S 0.41). Nearest: Thunder Rex CYAN (saturated, another egg). Accepted (review ruling 9).

## 5. Part list (x H)
- Ribcage: 0.30H deep x 0.26H wide x 0.50H long, bottom taper (0.66, 0.56), `rnd 0.30`, plus a tuck segment from chest to waist.
- Hips: 10-15 % smaller block, rotated -8 degrees.
- Neck: 0.20H thick, 40 degrees up.
- Head: wedge skull, brow block (BACK_SHADE), two cheek ruffs each side (SNOW), muzzle (SNOW, 0.12H).
- Ear tufts: 2 x (ear block 0.10H, tip 0.03H ICE).
- Legs: 4 x 2-bone (upper 0.22H, lower 0.20H), paws 0.12H x 0.14H.
- Claws: 4 per paw, 0.05H, ICE_CLAW, smooth (`role detail`). Each claw is its own bone (for the act).
- Tail: 3 segments, 0.30H total, BLACK tip band.
- Rosettes: 5-7 flat BACK_SHADE spot inlays per flank (0.06H, flush), grouped into rosettes.
- Hero piece: none (starter). The signature shapes are the tufted ears, the rosettes and the icy claws.
- Stud skin on body, neck, head, legs. Not on eyes, claws, tufts, the rosettes or the tail tip.

## 6. Face spec (fierce, no googly eyes)
- Eye: BLACK socket, ICE slit (0.10H x 0.03H), tilted 18 degrees, inner corner low. BLACK slit pupil, 0.012H.
- No highlight, no glint, no round pupil.
- Brow: BACK_SHADE block over each eye, 20 degrees inner-down, 0.04H proud.
- Nose: BLACK, flat, 0.035H wide.
- Mouth: closed, BLACK line, two TEETH fangs (0.04H).

## 7. Clips (30 fps; 0 collisions at step 1; ground_min_z >= -0.02; loops closed)
- **idle (120 f loop):** stands with paws planted. The head yaws +/-14 degrees (f0-60, hold, back by f80). The neck yaw stays within 8 degrees (the head takes the drift). Ear tufts twitch 3 degrees at f70. Tail-tip flick 10 degrees at f90. Settles on the rest pose. No head shake.
- **walk (24 f loop, cm.quad_walk):** light snowshoe walk, springy. Body rises 0.02H at mid-stride. Walk slide ~0.
- **roar (60 f): "ruff-flare threat".** f0-20 the shoulders drop 0.05H and the cheek ruffs and tufts flare out 20 degrees. f20-45 the head drops 8 degrees and pushes forward 0.04H, twice. f25-50 the jaw opens to the fangs. f50-60 close and settle.
- **act_clawflex (96 f, in place) (review 2.1 MUST 3):** no wall, no rear.
  1. f0-20: crouch stare. The body lowers 0.05H. The head yaws 14 degrees toward the follow camera and holds to f40. The tufts flatten 8 degrees.
  2. f20-40: the tufts rise 12 degrees and hold.
  3. f40-72: the forepaws flex one after the other (lag 8 frames). Each claw bone rotates 35 degrees out. An ICE spark on each claw (events `claw1` f48, `claw2` f60). The paws stay on the ground.
  4. f72-84: the claws retract. The tail tip flicks 10 degrees once.
  5. f84-96: exact rest pose. The hind feet are planted in every frame.

## 8. VFX anchor bones (named after the effect; parent bone in brackets)
- `FX_IceSpark_L` [Claw_FL], `FX_IceSpark_R` [Claw_FR]: ICE sparkle on each claw flex.
- `FX_IceDust_L` [Tuft_L], `FX_IceDust_R` [Tuft_R]: a small ice dust drift off the tufts.
- `FX_SnowPuff_FL` [Paw_FL], `FX_SnowPuff_FR` [Paw_FR]: snow puff on the paw plant.
- `FX_SnowFlick` [Tail_Tip]: a tiny snow flick.
- No eye anchors (no glow on the eyes).

## 9. Distinctness
- ShadePanther (Void): indigo-black, violet crystals, pounce act. The Lynx is sand-silver with rosettes, no crystals, and its act is a claw flex.
- Bramble Badger (Grass starter): low grey badger, amber thorn crest, striped face. The Lynx is tall, cyan, with ice tufts.
- NightmareStallion (Void): its rear is not used here.

## 10. Animation references
TBD by builder (owner rule: pull 1-3 clips from animationreference.org and cite them before keying).
Suggested tags: "cat walk snow", "cat claw flex", "cat crouch watch".

## 11. Reviewer gates
1. 64 px: the cat head wedge and two pale ear tufts read. The cyan eyes read.
2. Game camera: the sand-silver body reads as a dark taupe, the rosettes and the SNOW underside show.
3. Claws and tufts are smooth. No fur fringes or flat cloth.
4. The act has no rear, no pounce, no prop. Hind feet planted in every frame.
5. Builder gates (review section 6): step-1 tris, collision_free, ground_min_z >= -0.02, linear 0, loops closed; icon strip at 64 and 128 px next to the Badger and ShadePanther; value shares; pose sheet of the act's key beats.
