# INFERNO PHOENIX — build plan v1 (Magma egg, 2 % SECRET, x2.9 income)

Builder: me, in the PetsV3 kit (`pets/InfernoPhoenix.py`, headless Blender). House pipeline:
plan → plan review → build → visual reviews → clips → clip review → export.

This plan is for the plan reviewer. Decide or adjust everything marked **[DECIDE]**.

Reused, already-approved machinery:
- the Thunderbird's **wingbiped** rig: the `wing3.Wing` 3-row feather wing, the CLOAK FOLD ground pose, LIFT1→4 fold↔open
  waypoints, gyro-stabilised head, and `plant_frames` / `lift_air_frames`
- the standard **Fly** clip set (idle, walk, fly, takeoff, land, roar, act), as on Griffin, Celestial Dragon, Storm Wyvern
  and Thunderbird

## 1. Role and the one-line read
"A volcanic phoenix: a slender, fierce fire-raptor with basalt-black plumage cracked with lava, wings that burn from
black to orange to white-gold, a tall gold flame crest, and three long fire streamers trailing from its tail."

At 64 px it must read as **a fire bird with a flame crest and long burning tail plumes**. It must NOT read as:
- **Thunderbird** (Storm 5 %): a bulky white-headed eagle, teal breast, kinked lightning-bolt tips, a fan tail. The
  Phoenix is slender, long-necked and dark-bodied, with flame-tongue tips (curved stepped, never kinked) and streamers.
- **Ivonrath** (Magma friend pet): a red chibi dragon. No dragon parts (no horns, scales or bat wings).
- **Solar Lion**: a radial sun-ray mane. The crest is a swept-back plume fan, not a corona.
- **Griffin**: brown, a 4-legged lion body.

## 2. Silhouette and proportions (side; −Y forward, Z up; rest = idle f0 = cloak fold)
- **Posture:** an upright raptor, body leaning about 35° (more upright than the Thunderbird's 46°), on a long S-neck that
  lifts the head clearly above the shoulders (the Thunderbird's head sits low on a bulky breast).
- **Slender build:**
  - body about 0.50 wide × 0.62 deep × 0.80 long (the Thunderbird's breast is much heavier)
  - long gold tarsi (0.38), basalt "trousers" to the hock, black hooked talons
- **Head:**
  - a falcon / harpy head, about 0.34 long
  - a hooked GOLD beak with a black tip and a slight open gape (the lower beak on a Jaw bone, 4° open)
- **HERO 1, the FLAME CREST:** 5 swept-back stepped flame plumes rising from the crown, the centre one tallest (crest tip
  = the model top, H_MODEL ≈ 1.95). Each plume is GOLD → FLAME → HOT in 3 stepped tongues. It is a swept-back fan, NOT a
  radial corona.
- **HERO 2, the STREAMERS:** 3 long tail streamers (Streamer_L / Streamer_C / Streamer_R), each 1.1–1.3 long, built in
  3 segments.
  - Each is a narrow BASALT shaft that broadens into a flame "eye" paddle at the end (like a quetzal or fenghuang
    tail), coloured LAVA → FLAME → HOT.
  - At rest they arc back and down, with the paddles curling up off the ground (lowest ≥ 0.05).
  - Above them sits a short 7-feather tail fan, BASALT with LAVA edges.
- **Wings:**
  - The `wing3` 3-row wing, span about 2.2 when open.
  - Primaries and secondaries are BASALT at the root, then LAVA, then a stepped FLAME-tongue tip (2-step curved tongue:
    FLAME → HOT), the fire gradient. The coverts are EMBER.
  - Folded (cloak fold), the black and ember wings lie along the flanks with the flame tips trailing beside the
    streamers.

**[DECIDE] ground pose:**
- A, recommended: the Thunderbird's CLOAK FOLD. It is proven collision-free and keeps the walk clean. The silhouette
  comes from the crest, the neck and the streamers.
- B: the "RISING MANTLE": wings half-raised in a heraldic V at rest (the classic phoenix crest-and-wings pose). It is
  stronger at 64 px, but it needs a new fold search, a raised-wing walk and more collision risk.

## 3. Colour blocking (3-band, flat palette-ID shares measured)
| role | colour (Blender) | where |
|---|---|---|
| BASALT | (44, 38, 44) charcoal (the Magma family base) | back mantle, wing roots, shafts, trousers, tail fan |
| BASALT_D | (28, 24, 30) | primary bodies (contrast for the fire) |
| EMBER | (196, 42, 34) deep crimson | breast, belly, neck, coverts |
| LAVA | (255, 104, 24) | wing mid-bands, the lava-crack seams on the mantle (thin flush bars, NOT glow), streamer paddles |
| FLAME | (255, 184, 36) | flame tongues, crest mid |
| HOT | (255, 246, 206) | tongue points, eye hot spot, crest tips |
| GOLD + GOLD_D | (255, 206, 72) / (214, 146, 30) | beak, tarsi and toes, crest base diadem, a gold "sun disc" brow jewel |
| BLACK | (14, 14, 22) | talons, beak tip, eye slit |

Share targets (game cam):
- BASALT family 30–40 %
- EMBER 18–28 %
- the fire family (LAVA + FLAME + HOT) 18–26 %
- GOLD 4–8 %
- No role above 45 %. Side: EMBER ≥ 15 %, so the bird reads red-black, not just black.

## 4. Head (the fierce zone)
- **Eyes:** molten FLAME iris, a black vertical slit pupil and a HOT spot; no glint. A heavy BASALT brow shelf forms a V
  that lids the eye tops (the Mantis / Leviathan lesson: brows ON the eye, never floating).
- **Face mask:** a basalt cheek mask from the beak back past the eye (falcon "moustache"), with an EMBER crown and nape.
- **Beak:** a GOLD hooked beak (upper + lower on Jaw), a black hook tip and a GOLD_D cere.
- **Brow jewel [DECIDE]:** a small gold sun-disc with a LAVA gem at the crest base. It is the gold anchor for the 64 px
  read, if the gold crest + beak aren't enough.
- **Hackles:** 3 rows of EMBER → LAVA nape hackles flowing down the neck (stepped, flame-edged).

## 5. Rig (wingbiped, as Thunderbird)
- Root, Spine, Chest, Neck (2 bones, for the S), Head, Jaw
- Wing chain per side (as `wing3`)
- Leg_L/R, Shin, Foot (+ toe)
- Tail (fan)
- Streamer_L/C/R × 3 segments each (secondary motion with phase lag)
- Crest (1 bone, for an "erect" key)

VFX anchors:
- Crest (the flame crown)
- Mouth (the fire breath)
- WingTip_L/R (fire trails)
- StreamerEnd_L/C/R (ember trails)
- Core (chest, for the rebirth flash)

Pairs and capsules:
- Pairs: Wing vs Chest / Spine / Leg / Tail, Streamers vs each other and vs Leg / Shin, Neck vs Wing (fold), Jaw vs Neck
- Joint capsules: the wing root, the streamer roots (3 out of one tail base), the jaw hinge

## 6. Clips (references pulled from animationreference.org and cited BEFORE animating, owner rule)
| clip | frames | idea |
|---|---|---|
| idle | 120 loop | Proud upright stance; a slow S-neck sway, one predatory head tilt (no shakes), the crest flares once (Crest key), the streamers drift with lag; one wing-rouse (a half-lift through LIFT1–2, then back) |
| walk | 32 loop | A high-stepping raptor strut, the head stabilised, streamers trailing with a wave |
| fly | 36 loop | Deep downstrokes, the outer wing tucks on the upstroke (Thunderbird fly recipe), the streamers whip in a travelling S-wave behind |
| takeoff / land | as Thunderbird | the same LIFT path; the streamers drag on takeoff and flare on landing |
| roar | about 80 | Crouch, rear up, wings flare to the full RISING V, the crest erects, the beak gapes (screech), hold, fold |
| act_rebirth | about 120 | **REBIRTH** (signature) |

REBIRTH beats:
1. Ignite: the crest flares, event `ignite`.
2. The wings wrap FORWARD around the body into a closed flame cocoon (the inverse mantle; wing tips cross in front of the
   chest), the head tucks, the body sinks. Event `cocoon`, at about f40.
3. The cocoon holds and trembles (the streamers curl in).
4. BURST: the wings explode open to the full rising V, the head snaps up, the streamers lash out, a slight hop (feet stay
   ≤ 0.15 off the ground). Event `burst` at about f70.
5. Hold the V with a screech.
6. Fold back through LIFT4→1 into the cloak.

Rules:
- no head shakes, no airborne spins, no stoop-dive (Thunderbird owns the stoop)
- 0 collisions at step 1, ground ≥ −0.02 every frame, no linear keys, loops closed
- in-betweens on any swing over 60° in one frame (Mantis F1 lesson)

## 7. Budget and deliverables
- Body ≤ 12 k tris (cap 15 k). HEIGHT 9.5 studs to the crest tip [DECIDE].
- Model gate:
  - a 600 px model sheet (tq / front / back / side / game) + a separate tq
  - a face close sheet
  - the 64/128 strip with MoltenBoar, LavaGolem, Cerberus, Ivonrath, Thunderbird, Griffin and SolarLion
  - an A/B pair (Phoenix next to the Thunderbird, then next to Ivonrath)
  - flat shares, tris
  - limit poses (the fold, the rising V, the cocoon wrap, the streamer lash)

## 8. Questions for the plan reviewer
1. Ground pose A (cloak fold) or B (rising mantle)?
2. Is the streamer design (3 long shafts + flame paddles) safe from the Celestial Dragon's crescent tail and the Black
   Dragon's flame mane? Length and count?
3. Crest: 5 swept plumes OK? A gold brow sun-disc, yes or no?
4. Palette: is the basalt + ember + fire gradient distinct from Ivonrath's red and the Magma pets' grey + orange seams,
   while still clearly "Magma egg"?
5. Is the REBIRTH act feasible with wing3 (a forward wrap means a new waypoint path)? Any simpler signature move?
6. Anything that remixes a sibling's signature? A missing jackpot factor for a 2 % secret?
