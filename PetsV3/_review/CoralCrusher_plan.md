# CORAL CRUSHER CRAB - concept plan v2 (Water Egg, MEDIUM 15 %, area 2 Water / Tide)

Planner: pet planner (concept only). The lead builds `pets/CoralCrusher.py`. Binding. Not built.

## v2 changes (from GLACIER_PLAN_REVIEW.md)
APPROVED WITH CHANGES, 6/10. Applied:
- Eyes (MUST 1): the eyestalks are shortened from 0.14H to 0.07H and made thicker (0.05H wide). The rose slit eyes sit in the
  SHELL_D brow plate, angled 15 degrees inner-down. The cartoon snail read is gone.
- Build gate (MUST 2): before the full model, prototype the six-leg sideways walk (body yaw 0). Check that the legs stay planted
  through the act's wave.
- NICE: ROSE (255,120,150) is 7 degrees from the Wyrm's ROSE. Accepted (review ruling). Watch it in the lineup.
- Builder gates from review section 6 apply.

## 0. Facts
| | |
|---|---|
| Tier | Medium |
| Odds | 15 % (money x1.52) |
| Egg / area | Tide (Water) Egg, area 2 |
| Rig | crab-multi-leg (6 walking legs, 2 raptorial claws, 2 short eyestalks). No crab kit yet |
| Closest kit files | `pets/AbyssWeaver.py` (multi-leg spider chain, IK legs). `pets/ThornbladeMantis.py` (raptorial claw pattern) |
| HEIGHT | 7.5 studs (top of the raised claw) |
| Tris | 7-10k |

## 1. Read in one line
"A giant armoured crab in bronze carapace, with rose-coral spikes on two big claws and a fierce, low stance."
At 64 px: a wide low shell with two big claws raised in front and rose spikes, and a brow plate with rose slits. It must NOT read as:
- Hammerjaw (steel shark, coral spikes in orange). The crab is a crustacean with claws.
- Kraken (red octopus with tentacles). The crab walks sideways on six legs.
- Kappa (teal river imp with a dish and a screech crouch). The crab is not biped.

## 2. Rarity ladder
- Medium (15 %). Rarer than the Turtle (25 %) and Kappa (45 %), commoner than the Kraken (9 %).
- It must look more armoured and more interesting than the Turtle (25 %).
- Must be beaten by Kraken (9 %), Hammerjaw (4.5 %) and Orca (1.5 %).

## 3. Silhouette and anatomy (x H, H = 7.5 studs)
- Wide low carapace: width 1.0H, length 0.75H, height 0.30H. The top is a dome with three ridges.
- Claws: two big pincers held out in front, arm 0.25H, pincer 0.45H long, 0.18H thick. The claws are the biggest mass after the shell.
- Legs: 6 walking legs (3 per side), each 0.30H, 2 joints. They hold the shell 0.22H above the ground.
- Eyestalks: two short stubs (0.07H, 0.05H thick) on the front edge. The rose slit eyes sit in the brow plate on top of them.
- Front: one heavy brow plate over the eyes, and two pale mandibles below.
- Edges: the carapace rim has rose spikes (smooth) spaced 0.12H.
- Belly pale, seen from the front view and when the crab rises.

## 4. Palette (Blender RGB; body brightest channel 196 >= 170)
| Name | RGB | Hex | Where | Share (side) |
|---|---|---|---|---|
| BRONZE | 196,150,104 | #C49668 | carapace top, claw bodies, studded | 40 % |
| SHELL_D | 132,96,66 | #846042 | legs, seams, claw knuckles, brow plate (the eye plate) | 14 % |
| BELLY_PALE | 240,226,200 | #F0E2C8 | underside, mandible plates | 8 % |
| ROSE | 255,120,150 | #FF7896 | THE accent: claw spikes, carapace rim spikes, eye slits | 8 % |
| ROSE_D | 200,70,110 | #C8466E | spike bases | 3 % |
| BLACK | 14,14,22 | #0E0E16 | claw tips, pupils | 3 % |
| IVORY | 240,236,222 | #F0ECDE | mandible teeth | <1 % |
| MOUTH | 86,26,40 | #561A28 | mouth | <1 % |

- In game about (118,90,62): a dark sandy bronze.
- Accent family: REEF ROSE (pink-coral). Nearest: Wyrm ROSE (7 degrees, cross-egg, accepted), StormWyvern RED_HOT (Thunder, d 1). The Water egg has coral (Hammerjaw) but no rose.
- Gold: none.

## 5. Part list (x H)
- Carapace: 1 dome block 0.75H long x 1.0H wide x 0.30H tall, `rnd 0.30`, bottom taper (0.85, 0.9). Three ridge blocks along the top (SHELL_D seams).
- Brow plate: one SHELL_D block over the front edge, 0.22H wide, 0.04H proud. It carries the rose slit eyes.
- Eyestalks: 2 x (stub 0.07H, 0.05H thick, BRONZE). Eyes: ROSE slits (0.05H x 0.02H) set into the brow plate.
- Claws (x2): arm (0.25H, BRONZE), pincer upper and lower (0.45H long, 0.18H thick), outer edge with 6 ROSE spikes (0.05H, smooth). A gap between the jaws 0.04H.
- Walking legs (x6): 2 segments (0.18H and 0.14H), SHELL_D, dark tip.
- Mandibles: 2 BELLY_PALE plates with IVORY teeth (3 per plate).
- Hero piece: none (Medium). The signature shape is the two raised claws with rose spikes.
- Stud skin on the carapace and the arm blocks. Not on the spikes, eyes, claws, teeth, legs.

## 6. Face spec
- Eyes: ROSE slits (0.05H x 0.02H), BLACK slit pupils, set in the SHELL_D brow plate, angled 15 degrees inner-down. Fierce, not round.
- Mandibles: pale, slightly open, with IVORY teeth.
- No glint, no bulge.

## 7. Clips (30 fps; a crab walks SIDEWAYS, body yaw stays 0)
- **idle (120 f loop): "claw guard".** The big claw lifts to guard (claw up 20 degrees), held. The short eyestalks swivel slowly (yaw +/-10 degrees, one at a time). One small tap of the other claw on the shell (f70). Settles.
- **walk (30 f loop, crab walk):** sideways. Legs step in alternating tripods (3 legs at a time). The eyes lag. Walk slide ~0.
- **roar (60 f): "clack threat".** f0-14 the body rises 0.05H on the legs. The claws open wide and lift forward (claw bones forward 25 degrees). f14-40 the pincers clack three times (events `clack1` f22, `clack2` f30, `clack3` f38; the claw tips meet). The mandibles open. f40-60 the claws lower and the body settles. (Kappa's roar is a crouch with arms wide; the crab rises, claws forward, and clacks.)
- **act_semaphore (100 f, in place): "the fiddler wave".** Real fiddler crabs wave their big claw to show off. Beats:
  1. f0-18: the crab stands tall, the big claw lifts to 60 degrees (arm up).
  2. f18-62: the big claw waves up and down in three slow arcs (30 degrees each). Events `wave1` f26, `wave2` f40, `wave3` f54 (ROSE sparkle at `Claw_Tip_R`).
  3. f62-72: the claw points straight out and holds, then the small claw answers with two small taps on the shell (f66, f70).
  4. f72-88: the big claw lowers back to the guard.
  5. f88-100: the body settles to the rest pose exactly.
  Limits: no airborne movement; the legs stay planted in every frame of the wave.

## 8. VFX anchor bones (named after the effect; parent bone in brackets)
- `FX_RoseSparkle_L` [Claw_Tip_L], `FX_RoseSparkle_R` [Claw_Tip_R]: rose sparkle on the wave; a small bubble burst on the clack.
- `FX_SandPuff_1` to `FX_SandPuff_6` [Foot_1 to Foot_6]: sand puff on each step of the walk.
- `FX_BubbleBurst` [Mouth]: small bubble on the roar.
- No eyestalk anchors.

## 9. Distinctness
- Kappa (Water biped): teal river imp with a dish and a screech crouch. The crab is not biped, is bronze, and waves its claw in the semaphore.
- Hammerjaw (Water shark): steel-blue, coral spikes in orange. The crab is a crustacean with rose spikes and claws.
- SeaTurtleWarrior (Water biped turtle): a trident and a teal shell. The crab has no weapon, and its shell is bronze.
- Kraken (Water octopus, red): tentacles. The crab has six legs and two claws.

## 10. Animation references
TBD by builder. Suggested tags: "crab walk sideways", "fiddler crab wave", "crab claw".

## 11. Reviewer gates
1. Build gate (before the full model): the six-leg sideways walk with body yaw 0; the legs stay planted through the wave.
2. 64 px: the wide bronze shell, the two raised claws with rose spikes, and the rose slits on the brow plate read. No cartoon stalks.
3. Game camera: the shell is a dark sandy bronze; the rose spikes are the bright part.
4. The act is a fiddler wave. The roar is a rise with a clack, not Kappa's crouch.
5. Builder gates (review section 6): step-1 tris, collision_free, ground_min_z >= -0.02, linear 0, loops closed; icon strip at 64 and 128 px next to the Wyrm (rose check) and Turtle; value shares; pose sheet of the wave.
