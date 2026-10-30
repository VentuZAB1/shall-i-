# FIERCE PLAN - 21 pets, art + animation direction (2026-10-09)

Owner, 2026-10-09: the chibi pets are "too CHILDISH... for babies". The approved look is the storm-wolf Raiju
(`Raiju/renders/_RAIJU_FIERCE_preview*.png`, "The design is fire!"). His one note: the stomach read as a BOX.
Refs: `_refs/fierce/f_54..f_71` (Spideron, Lunar/Ice Dragon, Cerberus, Bronto, Orca, King Mammoth, Royal Sphinx...).
This file REPLACES STYLE_BIBLE.md section 3 and its lovely/bold/chibi tables. Bible section 2 kit numbers still
apply where they don't conflict (rounding roles, overlap rules, tri budget <= 15k, no Neon, VFX table).

## 0. Global rules (all builders)
Units: **SH** = withers height (quads), **BL** = chest front to rump, **H** = standing height (bipeds), **D** = serpent
tube diameter, **M** = Kraken mantle height. The canon is `pets/Raiju.py`: copy its build pattern (plates=False,
`bk.stud_skin`, hand-built eyes, throat pivot, 2-bone legs, check_pairs/joints).
- **A. Anatomy canon (Raiju, SH 1.0):** BL 1.15 | chest depth 0.50 (brisket 0.50 off the ground) | waist underline 0.62 |
  ribcage W 0.40, waist 0.30, hips 0.34 | head L 0.55 (snout = 55 % of it), head W 0.29, head top 1.30 | neck 0.30 thick,
  rising 40-50 deg | elbow 0.45, wrist 0.11, hock 0.47 | forearm 0.12 W, thigh 0.16 W x 0.28 deep | paw 0.14 x 0.17 with 4
  claws 0.06 | tail 0.75. Leg (ground to elbow) by family: cats 0.42, canids 0.45-0.50, bovids/boar 0.36-0.40, deer/horse
  0.55-0.58. Head L: cats 0.30-0.38, canids 0.45-0.55, deer 0.42, horse 0.55, boar 0.50. A head is 25-35 % of the
  standing height and is NEVER the biggest mass. Legs always 2-3 visible segments (thigh / shin / pastern + paw).
- **B. No box bellies:** ribcage block `bot=(0.66, 0.56)`, `top=(0.90, 0.95)`, `rnd=0.30`; the lowest point (brisket) sits
  just behind the front legs; the underline rises 12-18 deg to the waist (Raiju's tuck `seg`); waist W = 0.72-0.78 x
  ribcage W; hips are a separate block 10-15 % smaller, rotated -8 deg. Side view: no flat bottom edge longer than
  0.25 BL. Front view: the chest is a keel/V, never a rectangle. The light underside is a thin strip that FOLLOWS the
  slope (Raiju PALE seg), not a slab.
- **C. Colour:** dark rich base (V 20-45 %, S 25-60 %), a darker back/saddle/brows/socks (V 10-20 %), a lighter underside +
  muzzle + throat (+25-35 % V), plus ONE saturated accent (S 70-95 %) at <= 10 % of the surface, in 2-4 big marks
  >= 0.05 SH wide (Raiju bolts 0.055), and the eyes in the accent. Teeth (238,234,220) and claws (14,14,22) are neutral.
  2-3 tones per zone. Flat inlays <= 0.012 proud, bent to tapered faces (`_review/LESSONS_ALL_PETS.md` item 2).
- **D. Eye recipe (Raiju):** black socket 0.11 x 0.052 SH, rotated 18 deg with the inner corner down -> accent slit
  0.092 x 0.028 inset in it -> a hot highlight (accent lerped 60 % to white) 0.04 x 0.014 on the OUTER half -> a dark brow
  block 0.14 x 0.06 x 0.056 at 20 deg inner-down, 0.045 above the slit, 0.03 proud. Place each eye where the skull meets
  the snout, 0.5 HW off-centre, yawed 18-25 deg out, so both read from the front AND the side. No round eyes, no
  face_eyes "lovely/bold", no blush, no smiles. Cats/reptiles may add a vertical dark pupil 0.012 wide.
- **E. Weapons:** fangs: upper canine 0.075 SH, lower 0.05, lip teeth 0.035; claws 0.06, angled forward-down 30 deg;
  hackle/crest spikes laid back 50-72 deg, 0.10-0.18 SH long, shrinking toward the tail; horns/antlers in 3 tapered
  segments; signature shapes (bolt, blade, spade) are FLAT broad prisms seen from the side, ending in a point.
- **F. Studs:** `B = bk.Blocks(k, seed=.., tier=.., plates=False)` + `bk.stud_skin(k, PITCH)` at the end of model(k).
  Keep studs the same WORLD size on every pet: PITCH = 0.042 x (U / U_raiju), with U = model units per Roblox stud
  (model height / HEIGHT). No raised plate grid on the fierce pets.
- **G. Size test:** at 64 px the black silhouette must name the species: head wedge + ears/horns + ONE big signature shape
  (antlers, keeled shell, mane rays, wings, 3 heads...). At 10M (~20 studs tall) nothing under 0.02 SH thick, no seams or
  gaps (check the back view), and the accent marks stay chunky. Render tq/front/side/back + a 512 px face crop + 64 px.
- **H. Animation:** idle = 120 f loop (4 s), roar 54-66 f, signature `act_<word>` 45-105 f at 30 fps. Everything plays IN
  PLACE: the root may lift, turn or travel <= 0.5 SH but ends exactly on the rest pose. Hold key poses >= 6 f,
  anticipate 6-10 f, and give the main mover >= 15 deg arcs so it reads at 30 studs. No head shakes, ever. Head pivots
  sit at the throat. `collision_free: true` at step 1. Flyers flap wings AND pump legs; wings never pass through each
  other or the body. Rigid bones only: anything that has to move (lids, petals, roots, lips) gets its own bone.
- **I. Uniqueness checklist (run before authoring, re-check the table in section 3):** each MOTIF has exactly one owner
  across all 63 clips. Signature owners: retreat-into-shell, antler scratch, take root, shiko stomp, trident twirl,
  constrict, barrel roll, hoof scrape + charge, wing clap, back-roll wallow, fist ground pound, fly snapping,
  stalk + pounce, rear-up, corkscrew rise, sun-ray burst, mantle over prey, tail-over-head bite, bud-to-bloom,
  U-pose bellow, kneading. Roar/idle owners: howl, chest beat, yawn, bark, fire breath, paw swipe, buck, body stretch,
  sitting, dozing, rooting, cud chewing, flehmen, hiss + stand tall. RETIRED (nobody uses them): head shake, shake-off,
  happy twirl, hover-and-dive, proud wing stretch, generic "look left/right" as a core beat (Raiju only).

---

## 1. Grass tier

### MossbackTortoise (quad, `pets/MossbackTortoise.py`) - the tank
**Research**
- Giant tortoises (Galapagos, Aldabra) rest 16+ h a day and bask; when startled they pull the head straight back and
  the air pushed out of the lungs makes an audible HISS.
- They fold the armoured forelegs across the shell opening as a shield (the scaled side of the leg faces out).
- Dominance: the male stands tall on straightened legs, neck stretched high, mouth gaping. Rivals ram shells.
- Alligator snapping turtle: 3 rows of keeled, pyramid-like scutes, a hooked beak, a spiked tail. This is the "tank".
- Galapagos tortoises rise up and hold the neck out so finches can clean them (a still, held, neck-high pose).
**Design brief** (S = shell length)
- Anatomy: giant tortoise body and legs + alligator-snapper head, shell ridges and tail.
- Proportions: shell L 1.0 S, W 0.80 S, dome 0.48 S above the plastron; the plastron rides 0.20 S off the ground
  (shell top 0.68 S). Head 0.30 L x 0.20 W x 0.17 H with a 0.06 S hooked beak tip. Neck 0.32 S out, 0.16 thick, 2
  wrinkle rings. Columnar elephant legs 0.17-0.18 S wide; the front faces are covered in 3 rows of big scales. 5 claws
  (0.05 S) front, 4 back. Tail 0.18 S with 5 small spikes.
- Silhouette: a high domed shell with 3 rows of keeled ridges (centre row of 5 pyramids 0.10 S tall, side rows of 4 at
  0.07 S), a serrated back rim (6 saw points), and a front HOOD that overhangs the neck opening by 0.10 S.
- Palette: shell (58,54,38) · seams/ridge shadows (30,28,22) · skin (70,78,62) · plastron, jaw, under-neck
  (142,132,98) · beak + claws (36,32,28) · **accent moss lime (150,230,50)**: moss + fern tufts in the valleys between
  ridges, eyes.
- Change from chibi: drop the lovely eyes, blush, smile, bonsai, flowers and mushroom; the round face becomes a
  wedge reptile skull with a hooked beak; the stepped 3-tier shell becomes the keeled dome; the stump legs become tall
  columns that hold the shell up.
- Build: the shell must be HOLLOW at the front (rim + dome blocks, no fill in the front 0.35 S of the interior) so the
  head and forelegs can retract inside without collisions. Bones: keep Spine, Tree (now the moss/fern crest), Neck,
  Head, Jaw, legs, Tail1. ADD Lid_L/Lid_R (eyelid plates, children of Head).
**IDLE - DOZE (120 f):** sleeps standing. 0-25 the neck sinks until the chin rests on the ground; 25-35 the lids close;
2 slow breaths (shell +0.01 S); 70-78 one lid cracks open, looks, closes again; 95-120 the head drifts back up
(loops).
**ROAR - STAND TALL & HISS (60 f):** 0-12 all 4 legs straighten (shell rises 0.08 S); 12-20 the neck shoots up and out
30 deg; 20-44 the beak gapes 35 deg with a jaw tremble (hiss, moss VFX shakes loose); 46 one hard beak SNAP; 48-60
sinks back down.
**SIGNATURE `act_hide` - RETREAT INTO THE SHELL (96 f):** startled awake, it hides, peeks, hides again, then comes out.
- 0-8 rest. 8-14 startle: the head jerks up 10 deg and freezes.
- 14-24 WITHDRAW (fast): Neck slides back 0.30 S into the hood (loc +y, pitch +40 S-fold), Head counter-pitches;
  the forelegs swing in and up (roll +-60 deg) so their scaled faces close the opening; the hind legs fold under; the
  tail tucks; Spine drops 0.16 S so the plastron THUDS onto the ground at f22 (dust VFX), with a 2 deg bounce.
- 24-48 hold: a closed shell; one 3 deg rock at f34.
- 48-60 PEEK: the head slides out halfway (eyes just under the hood). 60-70: looks left 25 deg (hold 4), right 25 deg.
- 70-74 snaps back in. 74-82 hold.
- 82-96 EMERGE: the legs push the shell up, the neck extends to rest with a 3 deg overshoot, settle.
**Size:** the ridge rows and the hood carry the silhouette; moss tufts are >= 0.08 S chunks, never confetti.

### ForestStag (quad, `pets/ForestStag.py`) - the royal stag
**Research**
- Red deer and wapiti stags in the rut ROAR in bouts with the neck stretched forward and the mouth open, and grow a
  dark, shaggy neck mane.
- Deer groom by twisting the neck round and scratching the flanks and back with the antler tines; they also scratch
  the head with a hind hoof.
- They test the wind with the nose raised and turn the ears independently. Alarm = a freeze, then a tail flag.
- A "royal" stag carries 12 points (6 per side), with a brow tine reaching forward over the face.
**Design brief**
- Anatomy: red deer stag. BL 1.15 SH; chest depth 0.48 (brisket 0.52); the underline tucks up to 0.58 at the flank.
  Legs: elbow 0.56 SH, thin cannon bones 0.06 W, a visible knee and hock, split hooves 0.08 SH. Neck 0.45 SH long at
  50 deg, 0.32 thick at the base under a shaggy dark mane (fur spikes laid back, LESSONS_ALL_PETS item 5). Head 0.42 L x 0.17 W,
  tapering to a 0.10 muzzle. Ears 0.15 SH, leaf-shaped, set back.
- Silhouette: ANTLERS. The beam is 0.045 SH thick and rises 0.75 SH above the skull; span 0.95 SH; 6 tines per side
  (brow tine forward over the face, bez, trez, and a crown of 3 at the top).
- Palette: back (66,42,30) · flanks chestnut (110,66,40) · neck mane (38,28,22) · throat, belly, rump patch
  (200,180,146) · antlers (188,170,136) with bone tips (236,228,206) · hooves (24,20,18) · **accent emerald
  (40,220,130)**: 3 hanging moss/leaf tufts per antler (flat, >= 0.06 SH), eyes.
- Change from chibi: the fawn with the big head, spots, blossom and bib becomes an adult royal stag: a long neck, the
  head at ~1/3 of its old size, real antlers. No lovely eyes, no lashes.
- Bones: keep all. ADD Neck2 (between Neck and Head) so the neck can curl 90 deg round to the flank.
**IDLE - SCENT THE WIND (120 f):** 0-20 the nose lifts 12 deg with 3 sniff ticks (Head 2 deg + Jaw 2 deg); 20-50 the ears
swivel independently (L forward / R back, swap); 50-64 an alert FREEZE (everything still); 64-100 relaxes and dips to
nibble low twice; 100-120 head back up, one tail flick.
**ROAR - RUT ROAR (64 f):** 0-10 braces wide, the neck drops to horizontal; 10-46 neck stretched FORWARD and level,
jaw 30 deg, 3 roar bouts (the Chest pumps, the jaw closes to 12 deg between bouts), tail flag up; 46-56 the head
pitches down 25 deg so the antlers point at the viewer (threat); 56-64 back to rest.
**SIGNATURE `act_scratch` - ANTLER SCRATCH (90 f):** the owner's example: scratches its tummy/flank with its antlers.
- 0-8 weight shifts onto the right legs.
- 8-22 Neck yaws +55, Neck2 +35, Head rolls 20 and pitches down 25, so the antler tines reach the LEFT flank/belly
  (stop 0.02 short of the body). Leg_BL lifts 25 deg forward to open the flank.
- 22-62 SCRATCH: 4 strokes (10 f each), the antlers rake down-and-back 12 deg and return; the ears flop sideways in
  bliss; the tail flicks on stroke 3.
- 62-72 one long last rub, then the head swings back to the front. 72-80 the hind leg goes down; a contented ear flick.
- 80-90 settle to rest.
**Size:** antlers + neck mane read at any scale; the moss tufts must stay chunky. Thin legs: at least 0.06 SH.

### Treant (biped, `pets/Treant.py`) - the ancient ent
**Research**
- Tree spirits (the Green Man, Tolkien's Ents and Huorns) are slow, ancient and deliberate; they can "take root" and
  pass for ordinary trees, then uproot and walk.
- Real trees sway and creak in the wind, flex in gusts, and grow toward the sun.
- Old oaks: deeply fissured vertical bark, burls, gnarled limbs thicker at the elbows.
**Design brief**
- Anatomy: a hunched oak giant. Legs 0.40 H (each leg a trunk that splits into root-feet with 3-4 splayed root toes,
  0.12 H); torso trunk 0.35 H tapering at the waist (0.28 H wide) and flaring to the shoulders (0.45 H) with a burl
  hump on the back. No neck: the head is the top of the trunk (0.15 H) with the face sunk under a heavy knot brow.
  Arms 0.50 H, reaching the knee, gnarled (the forearm is thicker than the upper arm); hands = 3 long twig talons
  (0.10 H).
- Silhouette: a crown of twisted branches (antler-like, span 1.0 trunk W) carrying 4-5 dark leaf clumps; long hanging
  arms; root feet.
- Face: amber slit eyes deep in dark knot sockets, a jagged mouth gash with wooden splinter teeth, a moss beard.
- Palette: bark (60,44,32) · fissures (34,24,18) · heartwood face/inner limbs (112,84,58) · canopy (40,72,38) /
  (58,98,46), moss (74,110,52) · **accent amber sap (255,170,30)**: eyes + 3 sap-filled cracks (chest, left arm,
  right thigh, 0.05 H wide).
- Change from chibi: the friendly barrel with a grin and a round canopy becomes a gnarled, hunched giant; bark =
  vertical fissure ridges (0.02 H proud), not plates; no blossoms, no mushroom.
- Bones: keep Spine, Chest, Head, Jaw, Crown, Arm/Fore/Hand, Leg/Shin/Foot (Vine_ may stay unused). ADD Root_L/Root_R
  (toe-roots, children of Foot) for the signature.
**IDLE - WIND SWAY (120 f):** the whole body sways +-4 deg (Spine roll) with the arms lagging 6 f like heavy branches
and the Crown counter-swaying; 55-75 a GUST bends the crown 10 deg and swings the arms; 90-110 a slow creaking
back-stretch (Chest -8 deg).
**ROAR - TIMBER LEAN (60 f):** 0-12 creaks back 6 deg; 12-30 tips FORWARD 28 deg from the ankles like a falling tree
(feet planted, IK), arms hanging forward with the twig fingers splayed, jaw wide; 30-46 holds roaring, the crown whips
forward; 46-60 hauls itself back upright with an overshoot.
**SIGNATURE `act_takeroot` - TAKE ROOT & UPROOT (100 f):** it turns into a tree, then tears itself free.
- 0-10 plants its feet wide, knees bend.
- 10-25 the Root toes drive down 40 deg, Spine sinks 0.05 H (root VFX: dirt).
- 25-40 the arms rise up and out into a branch V (Arm -140, roll +-30, Fore 20 deg bend, fingers spread); the head tilts
  up and the Crown lifts.
- 40-62 TREE HOLD: frozen; only the Crown sways +-4 deg (leaf VFX). One second of stillness = a tree.
- 62-68 the head snaps forward (eyes "on").
- 68-86 UPROOT: two effortful yanks free the left foot (Leg -40, Spine lean 8 deg), then the right; the roots curl back.
- 86-100 the arms lower, settle to rest.
**Size:** the crown + long arms make the silhouette; leaf clumps are 3-5 big blocks, not many small ones.

---

## 2. Water tier

### Kappa (biped, `pets/Kappa.py`) - the river imp
**Research**
- A yokai ("river child") with a turtle shell, a beak, webbed hands and a water-filled DISH (sara) on the head; if
  the water spills it loses its strength.
- It is compulsively polite and must return a bow, which spills the dish. People beat it this way.
- It loves cucumbers and challenges people to SUMO. It drags horses and swimmers into rivers.
- Usually described as crouched and monkey-like, clumsy on land, at home in water.
**Design brief**
- Anatomy: a hunched lean biped (snapping turtle + frog + monkey). Head 0.22 H (0.24 H long including a hooked 0.08 H
  beak). Carapace 0.40 H long on the back, a plastron front with 2 rib ridges. Arms 0.50 H, reaching the knee; webbed
  3-claw hands. Crouched legs (thigh/shin 0.22 H each, knees 40 deg bent at rest); webbed 3-toe feet 0.14 H long.
  Narrow waist.
- Silhouette: the dish ring (0.16 H wide) with 7 shaggy hair spikes swept back, the shell hump, long hanging arms.
- Palette: skin (34,80,72) · shell (44,56,38) with ridges (26,32,24) · plastron (138,132,92) · hair (18,30,28) · beak
  (52,46,34) · mawashi rope belt (20,24,48) · **accent aqua (40,230,220)**: dish water, eyes, 2 gill stripes per side
  of the neck.
- Change from chibi: the pear body with the big head and asymmetric lovely brows becomes a lean, crouched imp with a
  narrow-eyed predator face. The mawashi becomes a dark rope belt (it justifies the sumo).
- Bones: keep all.
**IDLE - DISH GUARD (120 f):** a frog squat; the body bobs with breathing but the head stays dead LEVEL
(counter-rotated); 35-55 cups the right hand over the dish to protect it; 65-90 a sly sideways leer (head yaw 20 deg,
held); 95-110 one deep frog-squat bounce.
**ROAR - SCREECH CROUCH (58 f):** drops into a low crouch, arms flung wide with the claws spread, beak gaping forward at
head height, trembling hold, snaps back up.
**SIGNATURE `act_sumo` - SHIKO & TSUPPARI (100 f, keep the concept, re-author for the new rig):**
- 0-12 sinks into a deep sumo squat, hands on the thighs.
- 12-30 weight to the right; the left leg swings HIGH out to the side (Leg_L roll 70), held 26-30.
- 30-36 STOMP (dust + water-drop VFX from the dish).
- 36-58 the same for the right leg.
- 58-64 back into the squat. 64-88 three tsuppari palm thrusts R-L-R at chest height, each with a beak snap.
- 88-100 rises; one hand checks the dish (it didn't spill).
**Size:** the dish ring + hair spikes and the long arms read from far. The gill stripes are >= 0.03 H wide.

### SeaTurtleWarrior (biped + trident, `pets/SeaTurtleWarrior.py`) - the tide soldier
**Research**
- Loggerheads have huge heads and crushing jaws; leatherbacks have ridged (keeled) carapaces. Sea turtles cannot
  pull the head in.
- They "fly" underwater with the front flippers and surface to gulp air (a big head lift and breath).
- Poseidon/Neptune's trident struck the rock of the Acropolis and a spring burst out; he raised storms and quakes with it.
**Design brief**
- Anatomy: a broad-shouldered biped. Shoulders 0.42 H; head 0.18 H tall x 0.22 H long with a massive hooked
  loggerhead beak; short thick neck; carapace 0.45 H long with 5 keels and a serrated rear rim; plastron of 3 armour
  segments; forearms flattened like flipper blades (0.12 W x 0.06 thick) ending in 3-claw hands that grip; legs 0.40 H,
  thick, with wide paddle feet and 2 claws.
- Silhouette: a keeled shell + a tattered war-band with 2 tails + the trident (1.15 H tall: shaft 0.035 H, 3 barbed
  prongs 0.18 H).
- Palette: skin (40,90,80) with a darker scale pattern (24,58,54) · shell (26,50,66), keels (16,32,44) · plastron
  (160,148,108) · trident dark bronze (112,86,48) · pearl (220,230,236) · **accent coral (255,100,70)**: war-band,
  2 trident shaft wraps, eyes.
- Change from chibi: the smirking bold eyes, gold-rimmed dome and gold trident go; it gets a heavy beak brow over the
  slit eyes, keels on the shell, battle-worn gear.
- Bones: keep all (Trident, Band1/Band2).
**IDLE - SURFACE BREATH (120 f):** guard stance; 15-40 the head lifts and GULPS a big breath (jaw opens, chest swells)
and slowly exhales; 60-85 taps the trident butt on the ground twice; the band tails flutter throughout.
**ROAR - TRIDENT THRUST (60 f):** steps into a lunge stance and thrusts the trident forward at chest height twice with
both hands, beak wide on each thrust; the band whips; recovers.
**SIGNATURE `act_twirl` - TIDE-SPRING TWIRL (100 f, keep the concept):** Poseidon's spring strike.
- 0-12 raises the trident overhead in both hands. 12-20 tips it flat.
- 20-60 two full helicopter spins overhead (Trident yaw 720), body braced; the left hand lets go on spin 2 (fist out).
- 60-72 catches it vertical. 72-80 raises it high.
- 80-86 DRIVES the butt into the ground, knees bending (water-spring VFX burst).
- 86-100 rises into a proud stance, back to rest.
**Size:** the trident and the war-band read from far; the shell keels must be >= 0.03 H proud.

### Kraken (kraken rig, swims, `pets/Kraken.py`) - the deep terror
**Research**
- The giant squid has the largest eyes in the animal kingdom. Squid have arrowhead fins at the top of a long mantle.
- Octopus "deimatic display": spreads its arms and web wide to look huge.
- Blue-ringed octopus: flashes bright blue rings as a warning.
- Octopuses CONSTRICT prey by wrapping and squeezing. The Kraken legend wraps ships and drags them down; it is
  mistaken for an island.
**Design brief** (M = mantle height)
- Anatomy: giant squid mantle + octopus arms. Mantle: a tall bullet 1.0 M high x 0.75 M wide, leaning back 15 deg,
  with 2 arrowhead fins at the top (span 1.1 M). An eye band at the mantle base: big sunken sockets 0.22 M wide with
  horizontal slit pupils under a heavy brow ridge. 8 arms 1.4 M long, 0.18 M thick at the base tapering to 0.04 M,
  4 segments, light sucker discs underneath. Hovers 0.3 M off the ground.
- Silhouette: tall pointed mantle + fins + a crown of curling arms.
- Palette: mantle maroon (92,24,40) · back/spots (50,12,24) · underside + suckers (168,98,96) · barnacle crust
  (60,56,52) on the mantle top · **accent electric blue (40,150,255)**: 6 rings on the mantle (0.12 M), eyes.
- Change from chibi: the rounded crimson blob with bold eyes and a barnacle fin becomes a tall squid-octopus with
  arrowhead fins, sunken fierce eyes and blue warning rings.
- Bones: keep Spine, Head, Fin_L/R, T1..T8 a/b/c. ADD T1d..T4d (tip bones) on the 4 front arms so they can coil.
**IDLE - HOVER WAVE (120 f, keep):** a slow bob, a travelling wave rolls round the arm ring (each arm lifts and curls in
turn), the fins ripple.
**ROAR - KRAKEN RISE (60 f, keep):** sinks, then rears up with all 8 arms flared UP like a spiked crown (deimatic),
tips writhing, blue rings flash (VFX); crashes back down.
**SWIM (keep):** jet propulsion - the arms snap together, then umbrella open.
**SIGNATURE `act_wrap` - SHIP CRUSHER COIL (100 f, NEW - replaces the drum slams, too close to a ground pound):**
- 0-14 the 4 front arms rise and reach forward-up as if grabbing a mast; the side arms brace on the ground.
- 14-30 they COIL round an imaginary mast (0.6 M thick, 0.8 M in front): b/c/d joints curl 60-80 deg, left arms
  clockwise, right arms anticlockwise, tips spiralling.
- 30-60 SQUEEZE x3: the coils tighten +15 deg, the mantle pulses down/up (Spine z +-0.04 M, pitch forward 6), the fins
  flare (crack VFX).
- 60-76 DRAG DOWN: the coiled arms pull the "mast" to the ground; the mantle leans forward 15 deg.
- 76-90 releases: the arms unfurl outward in a splash (bubble VFX). 90-100 back to the hover rest.
**Size:** the fin + mantle point is the silhouette; the rings must be big plates, not dots.

---

## 3. Storm tier

### Raiju (quad, `pets/Raiju.py`) - APPROVED, keep
**Research**
- Raiju, the "thunder beast", companion of the thunder god Raijin: a blue-white wolf wrapped in lightning, calm until
  a storm, then it leaps from tree to tree.
- It falls from the sky as a BALL OF LIGHTNING; lightning-struck trees carry its claw marks. Its cry is thunder.
- It sleeps in people's navels during storms.
**Design brief:** the canon - do not redesign. Finish the owner's fix: the belly must not read as a box (section 0 B:
ribcage taper, sloped tuck, underline strip). Palette as built: fur (44,56,98) · dark (26,30,56) · pale (112,132,176)
· **accent bolt yellow (255,202,36)**.
**IDLE - ALPHA SENTINEL (keep):** snappy scans with holds, ear flicks, lip snarl, chest + chin lift.
**ROAR - HOWL (keep):** leans back, chin to the sky, jaw wide, ears pinned.
**SIGNATURE `act_thunderflip` - BALL-LIGHTNING ROLL (keep, 64 f):** crouch, explodes up into a full barrel roll with the
legs tucked (it becomes the ball of lightning; spark VFX), lands on all fours, proud power pose.
**Size:** approved; the bolt marks are 0.055 SH wide, keep them at that size.

### ThunderBull (quad, `pets/ThunderBull.py`) - the storm bison
**Research**
- Bison and gaur bulls carry a massive shoulder hump, hold the head LOW, and grow a shaggy cape on the forequarters.
- Before a charge a bull paws the ground, throws dirt over its back, raises its tail stiffly, then lowers its horns.
- Threat display: stands BROADSIDE to show its size, and bellows.
- Lightning strikes leave branching "Lichtenberg figures" on skin and ground. The Mesopotamian Bull of Heaven's
  snorts tore pits in the earth.
**Design brief**
- Anatomy: American bison x gaur. The hump top is SH 1.0, the rump only 0.78 (the back slopes down to small hips).
  Chest depth 0.55 (brisket 0.45); short legs (elbow 0.38 SH); head 0.42 SH long held low (forehead at 0.62 SH, nose at
  0.35 SH). Horns 0.08 SH thick at the base, curving out-up-forward in 3 tapered segments, span 0.85 SH. A shaggy
  cape on the head, hump and front legs (darker, a ragged shingle edge at mid-ribcage); lean hindquarters (hip W = 0.70
  x shoulder W); a thin tail with a tuft; split hooves.
- Silhouette: hump + low head + horns. NO cloud mesh (the storm cloud is a VFX emitter on the hump).
- Palette: hindquarters (52,58,92) · cape (34,36,62) · muzzle + belly (96,104,140) · horns (210,204,186), tips
  (30,30,40) · hooves (16,16,24) · **accent electric blue (70,190,255)**: branching Lichtenberg scars on the hump and
  both flanks (a trunk 0.05 SH wide + 3 branches), eyes. Drop the gold nose ring.
- Change from chibi: the crate head with a big brow and a cloud on the hump becomes a real bison/gaur: low head,
  real hump, cape, lean rump.
- Bones: keep all.
**IDLE - CUD & FLIES (120 f):** the jaw grinds side to side (Jaw yaw +-6, 3 cycles); the tail swats the left flank at
f45 and the right at f90; ear flicks; 65-85 a slow glare toward the viewer, held.
**ROAR - BROADSIDE BELLOW (64 f):** turns its body 35 deg to show the flank, tail raised stiff, head low, mouth opens
25 deg and the bellow pumps the flanks twice (Chest pulses); turns back.
**SIGNATURE `act_charge` - SCRAPE & CHARGE (90 f, keep, buck removed):**
- 0-30 paws the ground twice with the right fore-hoof, flinging dirt back (dust VFX), head low.
- 30-40 lowers the horns, the tail goes stiff and up, the body rocks back onto the haunches.
- 40-52 LUNGES forward 0.15 SH over planted feet (IK).
- 52-62 HORN HOOK: the head hooks up and to the right 35 deg (spark VFX).
- 62-90 back to rest; one snort.
**Size:** the hump and the horns read from far; the scars must be chunky branches, never thin lines.

### StormWyvern (wingbiped, flies, `pets/StormWyvern.py`) - the sky raptor
**Research**
- A heraldic wyvern: 2 legs + wings. Real analogues: pterosaurs (long crested skulls, wing membrane on the arm and a
  long finger), bats (thumb claw at the wrist), raptors (talons).
- Wood pigeons CLAP their wings together above the back in display flights; the clap carries far.
- Swans "busk": wings arched up over the back like a hood as a threat.
- Red sprites: bright red lightning flashes above thunderstorms.
**Design brief**
- Anatomy: upright 30 deg forward. Head 0.20 H long, a long crested skull (a back crest horn 0.12 H), a jaw with 4
  fangs. Neck 0.22 H S-curved. Deep keel chest 0.30 H. Digitigrade legs: thigh 0.18 H, shin 0.20, metatarsus 0.12, 3
  forward talons + 1 back. Wing arm 0.45 H with 3 fingers, span 2.6 x body length, a wrist thumb claw 0.06 H. Tail
  1.2 H long ending in a flat arrow blade.
- Silhouette: crest skull + big membrane wings + long blade tail.
- Palette: body (42,40,70) · membrane (60,56,96) with darker inner panels (44,40,74) · belly bands (120,118,150) ·
  wing bones + claws (18,16,30) · crest + horns (190,184,200) · **accent red-sprite crimson (255,50,90)**: eyes,
  tail blade, crest tip, 3 zigzag lines on each membrane near the fingers.
- Change from chibi: the big-head stocky wyvern becomes a lean long-skulled predator; the head drops to ~0.20 H.
- Bones: keep all.
**IDLE - GARGOYLE PERCH (120 f):** crouched low with the wings folded high on the shoulders like a hunched cloak (wrists
above the head), head low; slow breaths; f40 the tail tip whip-cracks once (Tail3 snap); 70-80 the jaw clacks twice;
90-110 a slow head turn and back.
**ROAR - HOOD SHRIEK (60 f):** the wings arch up and forward over the head like a hood (wrists high, tips down in
front, swan busking), the head held low between them, jaw wide shrieking, the tail lashes once; folds.
**SIGNATURE `act_thunderclap` - THUNDER CLAPS (90 f, NEW: grounded wing clap; the old rear-up/leap is retired):**
- 0-10 crouches, the tail braces on the ground, wings half open.
- 10-22 the wings sweep up and back over the back.
- 22-26 CLAP 1: the wings snap together ABOVE the back (tips 0.02 apart, vertical); spark burst VFX; the head thrusts
  forward with a jaw snap.
- 26-36 open wide. 36-40 CLAP 2. 40-50 open. 50-56 CLAP 3, the biggest: up on its toes, tail lifted.
- 56-70 holds the wings high and open, jaw wide (thunder). 70-90 folds to rest.
**FLY:** bat-like. Deep full-arm downstrokes; the WingTip folds on the upstroke; the legs are pulled back like an eagle
and pump on each downstroke; the tail S-waves as a rudder; the body rises on each beat.
**Size:** the crest and blade tail read at 64 px; the membrane zigzags are 0.04 H wide.

---

## 4. Magma tier

### MoltenBoar (quad, `pets/MoltenBoar.py`) - the volcano hog
**Research**
- Wild boars are wedge-shaped (a massive head and shoulders, small hips); the head is about a third of the body length.
- They root the soil with a disc snout and WALLOW in mud to cool, rolling on their sides and backs.
- Threat: raises the spinal bristle crest, CHAMPS its jaws (teeth clacking, foam), then slashes upward with the tusks.
- They rub against "rubbing trees".
**Design brief**
- Anatomy: withers SH 1.0, rump 0.85; BL 1.3; head 0.50 SH long, a conical snout ending in a disc, small high eyes;
  upper tusks curling up 0.18 SH; short legs (elbow 0.36 SH), thin lower legs with dewclaws; a bristle crest of 7
  spikes from the head to mid-back on the Mane bone; a short tufted tail.
- Silhouette: wedge + tusks + crest.
- Build: rock armour slabs over the head, back, shoulders and thighs; magma shows in the gaps (>= 0.04 SH wide) and
  across the belly.
- Palette: rock (46,40,46) · rock tops (74,66,72) · dark (24,20,24) · tusks (226,214,190) · snout disc (90,64,62) ·
  **accent magma orange (255,110,20)**: cracks, belly, eyes, crest tips.
- Change from chibi: smaller head (0.50 SH long, not 1.05 TW), longer jointed legs, narrow eyes in rock sockets, a real
  snout disc instead of a flat pad.
- Bones: keep all (Mane = the crest).
**IDLE - ROOT & SNORT (120 f, keep):** head low, quick sniffs, roots the ground twice with the snout, lifts the head and
SNORTS (the body jolts, the crest flares); an ear flick, the tail twirls.
**ROAR - CREST & CHAMP (60 f):** head low, the crest bristles up (Mane pitch -30), the jaw champs 4 fast clacks
(0 -> 25 -> 0 deg x4, ember VFX), then a squeal with the head raised 20 deg, ears pinned; settles.
**SIGNATURE `act_wallow` - LAVA WALLOW (100 f, keep):**
- 0-10 kneels on the front legs.
- 10-22 flops onto its left side (Spine roll 90 + root drop).
- 22-50 rolls onto its BACK (roll 160) and bicycles all four legs in the air, wriggling the back (Spine yaw +-8);
  lava splashes (VFX).
- 50-62 rolls back onto its side.
- 62-76 springs up onto its legs. 76-90 one big snort, the crest flares. 90-100 rest. (No shake-off.)
**Size:** tusks and crest read from far; the magma gaps must be wide bands, not hairlines.

### LavaGolem (biped, `pets/LavaGolem.py`) - the volcano silverback
**Research**
- Silverback gorilla display: hoots, rises upright, throws plants, BEATS its chest with cupped hands (heard about 1 km
  away), kicks, runs sideways, thumps the ground.
- Anatomy: an arm span 1.5 x its height, arms reaching below the knees, a massive trapezius hump that sinks the head, a
  sagittal crest on the skull, a heavy brow ridge; it knuckle-walks.
- Golem myth: a body of earth animated by a word (emet) inscribed on the forehead.
**Design brief**
- Anatomy: shoulders 0.55 H wide; a trapezius hump (the head top barely clears the shoulders); head 0.16 H with a rock
  sagittal crest spike and a brow shelf; chest barrel 0.30 H wide; arms reach below the knee, forearms thicker than
  the upper arms, boulder fists 0.15 H; short legs 0.35 H.
- Silhouette: an inverted triangle (huge shoulders, small legs) + crest + fists.
- Palette: basalt (44,40,46) · tops (70,64,70) · dark (22,20,24) · obsidian claws (14,14,22) · **accent molten
  yellow-orange (255,170,30)**: a heart cluster, crack seams from the heart to the shoulders and knees (0.03 H wide),
  eyes, a glyph on the forehead (the "emet" mark: 3 chunky bars).
- Change from chibi: the flat "TV" chest panel and the uniform cubes go; silverback proportions with lava seams.
- Bones: keep all.
**IDLE - KNUCKLE REST (120 f):** leans forward onto its knuckles (fists planted), heavy breaths; 40-80 lifts the right
fist and turns it to inspect it, then cracks the knuckles against the left palm; 90-120 plants it back.
**ROAR - CHEST BEAT (60 f):** rises tall from the lean, chest out, head back, then 6 rapid alternating chest beats
(4 f each, cupped fists, ember VFX at each hit), jaw wide, a final hoot; drops back.
**SIGNATURE `act_pound` - GROUND POUND (100 f, keep):**
- 0-14 raises the right fist high. 14-20 SMASHES it into the ground (crack VFX). 20-34 the left.
- 34-50 clasps both fists overhead, crouches.
- 50-62 JUMPS (root +0.25 H). 62-68 a double-fisted smash on landing (shockwave VFX).
- 68-86 holds the impact crouch, head up glaring. 86-100 rises to rest.
**Size:** the shoulder mass + crest; the seams stay at 0.03 H minimum.

### Cerberus (quad, 3 heads, `pets/Cerberus.py`) - the hellgate hound
**Research**
- The three-headed hound guarding Hades: it lets the dead in and none out. Several versions give it a SERPENT
  tail and a mane of snakes.
- Orpheus lulled it to sleep with music; the Sibyl drugged it with a honey cake; Heracles dragged it to the surface,
  and its spilt saliva grew the poisonous aconite.
- Real dogs snap at flies; mastiffs/Rottweilers have broad muzzles and huge chests.
**Design brief**
- Anatomy: a mastiff-wolf. BL 1.2 SH; a broad chest 0.50 SH wide carrying 3 necks (0.20 SH thick, fanned +-28 deg) from
  a shoulder yoke; waist 0.34 W; legs elbow 0.48 SH, thick; heads 0.45 SH long with broad muzzles (the centre one 10 %
  bigger and 0.05 SH higher); a hackle spike ridge; the tail ends in a SERPENT head (small wedge with 2 fangs).
- Silhouette: 3 heads in a fan (like ref f_70) + spiked collars + serpent tail.
- Palette: charcoal (36,34,42) · back (20,20,26) · rust points (124,64,36) on the muzzles, brow dots, chest V and socks
  · collars (28,24,28) with steel spikes (170,170,180) · **accent hellfire red (255,50,40)**: eyes, mouth interiors,
  the serpent tail's eyes.
- Change from chibi: the goof/grump faces with bold eyes and a tongue go; all three are fierce. Personality now comes
  from the ears and pose: LEFT ears back (the hothead), CENTRE upright (alpha), RIGHT one torn ear (the veteran).
- Bones: keep all (Neck_/Head_/Jaw_ L C R). The serpent head rides on Tail3.
**IDLE - SIBLING SQUABBLE (120 f):** CENTRE keeps guard (slow turns with long holds); LEFT pants with its jaw pulsing
15 deg; RIGHT eyes the left head, and at 70-80 darts in and nips at its ear (no contact) - LEFT flinches away, CENTRE
glances at them; settle.
**ROAR - THREE-HEAD FAN SNARL (60 f):** the body braces back, all three heads drop low, then FAN OUT wide (L -40 yaw,
R +40, C up 15), jaws open trembling in a snarl, front paws spread, hackles up (fire VFX on the heads); holds; returns.
**SIGNATURE `act_triplesnap` - FLY SNAPPING (95 f, re-authored: the pounce is gone, that is ShadePanther's):**
- 0-10 all three heads track a buzzing fly (necks follow the same circle together).
- 10-22 CENTRE snaps up at it overhead (neck up 30, jaw clap).
- 22-34 LEFT lunges far left and snaps. 34-46 RIGHT lunges far right and snaps.
- 46-56 the fly lands in front: all three snap DOWN together in a fan (jaws clamp at f52), body braced, tail lifts.
- 56-75 the three jaws chew and look smug. 75-95 back to rest.
**Size:** the 3-head fan IS the silhouette; collar spikes >= 0.04 SH.

### Ivonrath (SECRET of the Magma egg; wingquad, flies, `pets/Ivonrath.py`) - the crimson wyrm
**Research**
- Western fire dragons are drawn on crocodilian and Komodo-monitor bodies: low-slung, sprawled elbows, a heavy tail.
- An alligator BELLOWS with the head and tail raised and the back arched down into a U; the infrasound makes the
  water on its back "dance". It also HEAD-SLAPS the water with its jaw.
- Komodo dragons are patient ambushers; dragons of legend hoard and guard.
**Design brief**
- Anatomy: a croc-dragon. BL 1.6 SH; sprawled legs (elbows out, elbow 0.42 SH); a croc head 0.55 SH long with a heavy
  jaw and teeth along the lips; 2 back-swept horns 0.40 SH in 3 segments + 2 cheek spikes; 2 rows of back crest
  spikes; membrane wings spanning 2.6 BL; tail 1.8 BL with a spade blade.
- Silhouette: horns + croc jaw + wings + spade tail.
- Palette: crimson (110,22,24) · dark (60,12,16) · belly bands (170,96,62) · membrane (90,20,24) with inner (60,14,18) ·
  horns (70,56,48) · **accent flame (255,170,30)**: horn tips, a crown band between the horns (hero set), back-spike
  tips, eyes.
- Change from chibi: the big head, stubby legs and smirk become a croc-dragon with real limbs; the crown stays as the
  SECRET hero piece.
- Bones: keep all. ADD Chest (for the back vibration), Neck2, and Shin_/Foot_ on all 4 legs (2-bone legs).
**IDLE - CLAW DRUM (120 f):** impatient: drums the 4 claws of the right forefoot one after another (the Foot pitches in
4 ticks, twice); 50-70 a slow lip-curl that shows one fang; 80-115 the tail curls round its front feet like a cat's
and uncurls.
**ROAR - FIRE BREATH (64 f):** inhales (chest swells, head back 20, wings half raised), then thrusts the neck forward
and blasts (fire VFX from the Breath bone), holding 1 s with ONE slow 30 deg sweep left to right; jaw closes, settles.
**SIGNATURE `act_emberdance` - EMBER DANCE (90 f, NEW; replaces the proud wing stretch):**
- 0-12 lowers its belly to the ground (legs fold, Spine -0.2 SH).
- 12-24 lifts head and tail high so the body forms a U (Neck -35, Tail1 -35); wings spread low and flat.
- 24-60 RUMBLE: the back vibrates (Spine/Chest pitch +-1.5 deg every 3 f); the back spikes buzz and embers DANCE off the
  back (VFX burst). Jaw closed, throat pulsing.
- 60-66 HEAD-SLAP: the head drops and claps its lower jaw against the ground (ember wave VFX).
- 66-76 rises back onto its legs. 76-90 settle, tail curl.
**FLY:** heavy dragon. Fast powerful strokes with a strong body bob on each beat; front legs tucked, hind legs kick back
on each downstroke; the tail lashes side to side as a counterweight.
**Size:** horns + spade tail; the accent tips must be big (>= 0.06 SH).

---

## 5. Void tier

### ShadePanther (quad, `pets/ShadePanther.py`) - the ghost leopard
**Research**
- A black panther is a melanistic leopard; its "ghost rosettes" still show in raking light.
- Ambush hunter: a low stalk, a hind-end wiggle, then the pounce. It drags kills up trees.
- Big cats bat and swipe with the forepaw, claws out, and snarl with the ears flat.
- Long play-bow stretches; the tail tip twitches when focused.
**Design brief**
- Anatomy: a leopard. BL 1.45 SH (long and low); elbow 0.42 SH; deep chest, a strong tuck; a SMALL round head 0.30 SH
  long with a short muzzle; small rounded ears (0.07 SH); big paws; a thick tail 0.95 BL curving up at the tip;
  prominent shoulder blades.
- Silhouette: long low body + long tail.
- Palette: base (34,28,52) · ghost rosettes (22,18,34) as rings of 3-4 inlays · underside + muzzle (70,60,98) ·
  **accent violet (170,80,255)**: eyes, a crystal cluster on each shoulder blade and on the tail tip (solid colour).
- Change from chibi: the big cat head and tall lined ears become real leopard proportions: a small head, small ears, a
  long body.
- Bones: keep all.
**IDLE - BIG-CAT STRETCH (120 f, keep):** the play-bow stretch (paws slide forward, chest sinks, rump high), back up;
then watches something off to the left with the tail tip twitching.
**ROAR - SNARL & SWIPE (60 f):** crouches, ears flat, lips curl (jaw 25), the right forepaw SWIPES the air across its
face claws-out, a snarl, then settles.
**SIGNATURE `act_pounce` - STALK & POUNCE (100 f, keep):**
- 0-30 sinks into a low stalk; the front paws creep in slow motion.
- 30-44 the hind-end wiggle.
- 44-58 LEAPS forward (<= 0.5 SH) through the air, front paws reaching.
- 58-70 lands, pins and bites. 70-100 springs back to its spot, rest.
**Size:** long body + tail; the rosettes must be big (>= 0.08 SH rings) or they vanish.

### NightmareStallion (quad, `pets/NightmareStallion.py`) - the dark Friesian
**Research**
- Stallions REAR to fight, striking with the front hooves; they BUCK, kicking both hind legs out.
- Flehmen response: the horse lifts its head and curls back its upper lip to read a scent.
- At rest it cocks one hind hoof (a hip-shot rest).
- Myth: the "mare" was a night spirit that rode sleepers' chests; the black horses of Hades drew his chariot.
**Design brief**
- Anatomy: a Friesian. BL 1.1 SH; chest depth 0.45 (brisket 0.55); long legs (elbow 0.58 SH) with thin cannons, big
  hooves and feathering (long hair at the fetlocks); a long arched neck 0.55 SH; a long narrow head 0.55 SH x 0.13 W
  with flared nostrils; ears pricked; 2 short swept-back horns (nightmare) 0.12 SH; a mane of long flame blades; the
  tail reaches the hocks.
- Silhouette: an arched neck + flame mane + long legs.
- Palette: coat (30,24,48) · dark (16,12,26) · muzzle + underside (64,54,92) · hooves (12,10,18) · mane base (54,30,90)
  · **accent magenta (255,60,200)**: mane-blade tips, feathering tips, eyes.
- Change from chibi: the "horse exception" short muzzle and big eyes go; real horse proportions.
- Bones: keep all. ADD Lip (upper lip plate, child of Head) for the flehmen.
**IDLE - HIP-SHOT FLEHMEN (120 f):** rests the right hind hoof on its toe (hip dropped), the tail swishes, the ears turn;
70-95 FLEHMEN: lifts the head 30 deg and curls the upper lip back (Lip -40), holds, relaxes.
**ROAR - SQUEAL & BUCK (60 f):** pins the ears and squeals with the neck arched (jaw opens); then drops the head and
BUCKS, kicking both hind legs high behind (rump up 0.15 SH); lands.
**SIGNATURE `act_rear` - REAR & STRIKE (95 f, keep):**
- 0-14 gathers itself (haunches under).
- 14-30 REARS up onto the hind legs (body pivots 50 deg at the hips), mane streaming.
- 30-60 strikes the air with alternating front hooves, 3 strikes, whinnying.
- 60-74 crashes down onto the front hooves (dust + wisp VFX). 74-95 settle to rest.
**Size:** the neck arch + mane read from far; the mane blades are flat and broad (>= 0.08 SH).

### BlackDragon (serpent, flies without wings, `pets/BlackDragon.py`) - the storm lung
**Research**
- The Chinese long has "nine resemblances": stag antlers, a camel's head, demon eyes, a snake's neck, a clam's belly,
  carp scales, eagle claws, tiger soles, ox ears.
- A lump on its head, the CHIMU, lets it fly without wings.
- It brings rain clouds, rises into the sky in spring, and eternally CHASES the flaming pearl, spiralling through the
  clouds (the dragon dance follows the pearl the same way).
**Design brief** (D = tube diameter)
- Anatomy: a body 14-16 D long in 10 segments (D tapering 1.0 -> 0.35). A camel-like head 2.2 D long x 1.4 D wide with
  an open jaw and 4 fangs; a chimu bump on the brow; stag antlers 1.5 D with 2 tines; ox ears; 2 long drooping
  whiskers 3 D; a mane of flame blades along the spine; a clam belly (light transverse bands); 4 short legs 2 D with
  eagle claws (4 talons).
- Silhouette: the S-body + antlers + whiskers.
- Palette: ink (26,22,40) · dark (14,12,22) · belly bands (88,78,110) · mane (44,30,70) · pearl (230,226,250) ·
  **accent gold (255,196,50)**: antlers, talons, whiskers, chimu, eyes.
- Change from chibi: the 1.8 D chibi head becomes a long camel head; more, thinner segments; real eagle talons.
- Bones: keep Spine, Neck, Head, Jaw, Pearl, legs. EXTEND CHAIN to 8-10 body bones (Body1..Body5, Tail1..Tail3) so the
  corkscrew bends smoothly.
**IDLE - PEARL NUDGE (120 f, keep):** a lazy side-wave down the body; the pearl drifts away and the dragon nudges it back
with its snout twice; the tail tip curls.
**ROAR - S-COIL STRIKE (60 f):** pulls the neck and front body back into a tight S (Body1 -30, Neck +40, Head -30), mane
bristling, whiskers lifted; then STRIKES forward and up with the jaw wide, whiskers whipping back; holds; settles.
**SIGNATURE `act_pearlchase` - CHASE THE PEARL (100 f, NEW; replaces the coil):**
- 0-10 the pearl darts up and away to the left.
- 10-30 the head follows it into a rising loop: the front body lifts and spirals (each chain bone adds +40 yaw and
  +10 pitch), a corkscrew around the body centre.
- 30-60 the head chases the pearl one full circle around above its own body (radius ~1.2 D, height ~2.5 D); cloud VFX.
- 60-70 the front claw SNATCHES the pearl; the jaws snap beside it.
- 70-90 uncoils back down; a wave runs to the tail tip. 90-100 rest, the pearl back at the cheek.
**FLY (keep):** wingless swimming - vertical waves travel from the chest to the tail, the head stays level, the legs make
small grasping strokes, the whiskers stream.
**Size:** antlers and whiskers are gold and thick (beam >= 0.18 D).

### PharaohAsparuh (SECRET of the Void egg; quad, sphinx rest, `pets/PharaohAsparuh.py`) - the cat king
**Research**
- The Great Sphinx: a lion body with a pharaoh's head in a nemes headdress, lying with the paws stretched forward.
  Cats were sacred to Bastet.
- Persian cats: a cobby, heavy-boned body, short legs, a broad round head and short muzzle, a long ruff and a plume tail.
- Cat behaviours: KNEADING ("making biscuits") with alternating front paws, the slow blink (trust), the yawn that shows
  every fang.
**Design brief** (SH = standing withers height; rest = lying sphinx)
- Anatomy: lying height to the head top 0.95 SH; BL 1.3 SH; front legs stretched forward 0.55 SH; round haunches; head
  0.34 SH long x 0.32 W, short muzzle, small ears; a cheek-and-chest ruff 0.12 SH deep; plume tail 0.9 BL, 0.14 thick.
- Silhouette: the sphinx pose + nemes flaps + uraeus.
- Palette: keep his real coat (cream fur (226,212,188), shade (176,156,128)), a deliberate exception: the dark rich
  values come from the costume. Nemes stripes lapis (26,40,110) + antique gold (190,140,40) · kohl (24,20,30) · nose
  (150,96,104) · **accent turquoise (40,230,210)**: uraeus gem, the middle usekh band, eyes. (If the owner wants him
  dark: black-smoke fur (40,38,46) with the same costume.)
- Change from chibi: the lovely half-lidded "w"-mouth face goes; narrow kohl-lined regal slit eyes, a calm but dangerous
  face, real Persian body proportions.
- Bones: keep all (Lid_L/R included).
**IDLE - ROYAL GAZE (120 f, keep):** chin up, looks down his nose to one side and then the other, the ears twitch
independently, the tail tip flicks on the ground.
**ROAR - YAWN-SNARL (60 f):** a huge yawn (eyes shut, jaw wide, every fang showing, ears back) that turns into a snarl at
its peak (head forward, ears flat, lip curl), then closes slowly.
**SIGNATURE `act_knead` - ROYAL BISCUITS (90 f, NEW; replaces the paw-licking groom, which overlapped the stag's scratch):**
- 0-10 the lids half close, the chin lifts.
- 10-70 KNEAD: the front paws alternately lift HIGH (Foot_F +0.15 SH) and press down, L-R-L-R-L-R (10 f each); the
  claws splay on each press (Foot pitch); the shoulders roll (Spine roll +-4); a tiny purr vibration; the tail tip
  curls up.
- 70-82 stops and gives the viewer a SLOW BLINK (lids close 6 f, hold 6 f, open).
- 82-90 settle.
**Size:** nemes + uraeus are the silhouette; costume stripes are >= 0.05 SH wide.

---

## 6. Celestial tier

### SolarLion (quad, `pets/SolarLion.py`) - the black-maned sun king
**Research**
- A lion's roar carries about 8 km; it is given with the flanks heaving and ends in a series of grunts.
- A dark mane signals a strong, healthy male (the Kalahari "black-maned" lions).
- Lions rest up to 20 h a day, often SITTING upright like a statue to survey.
- The Persian "Lion and Sun" emblem shows a lion with one forepaw raised and the sun rising behind its back.
**Design brief**
- Anatomy: BL 1.35 SH; heavy forequarters; elbow 0.42 SH; head 0.38 SH long and broad; a huge dark mane from the cheeks
  to the shoulders and chest (0.18 SH deep); tail 0.9 BL with a dark tuft; big paws.
- Silhouette: the mane + 12 flat gold sun-ray blades radiating from behind it (the emblem).
- Palette: tawny (150,98,46) · back shade (110,68,32) · mane (52,30,20) -> inner mane (96,52,26) · underside
  (198,164,110) · **accent sun gold (255,180,30)**: ray tips (the outer 40 % of each ray), a sun mark on the brow,
  eyes.
- Change from chibi: the round orange two-ring mane goes; a black-maned real lion with the rays behind the mane.
- Bones: keep all (Rays + Ray1..12).
**IDLE - KING'S SIT (120 f, keep):** sits down on its haunches, chest high, surveys with long holds, the tail swishes
on the ground, stands back up.
**ROAR - LION ROAR (64 f):** lowers its head to chest level as the mouth opens, then the full roar rises (head to
level, jaw 35, the flanks pump via Chest), then 3 grunts (jaw pops) at the end; the tail lashes.
**SIGNATURE `act_sunburst` - LION AND SUN (90 f, keep the ray burst, re-staged as the emblem):**
- 0-12 plants its paws, puffs out the chest, the tail lifts.
- 12-24 chin up; the rays pull in close to the mane (gather).
- 24-34 the rays SHOOT outward (rotate out 25 deg from the head plane) and the Rays wheel starts a full turn (34-64),
  like the sun rising behind its back.
- 40-60 the emblem pose: the right forepaw raised high, head at 3/4 to the viewer (sparkle VFX).
- 64-76 the rays snap back in, the paw down. 76-90 a proud huff, rest.
**Size:** the ray crown makes it read as "the sun lion" from across the map; the rays are >= 0.06 SH wide.

### Griffin (wingquad, flies, `pets/Griffin.py`) - the gold guardian
**Research**
- Eagle head and wings, lion body; it guards gold, nests in gold, lays agate eggs, and hates horses.
- Golden eagles are dark brown with a golden nape, a huge hooked beak and yellow feet.
- Raptors MANTLE over a kill: wings spread low like a tent over the prey, then they tear with the beak. They strike
  with the feet.
- Raptors stabilise the head while the body moves and cock it to look up with one eye.
**Design brief**
- Anatomy: BL 1.25 SH; eagle front (head 0.40 SH long with a 0.16 SH hooked beak, feathered ear tufts, a brow ridge,
  a neck ruff of shingle feathers, scaly forelegs with 4 talons 0.08 SH), lion hind legs and tail; 3-row feather wings
  spanning 2.6 BL.
- Silhouette: hooked beak + ear tufts + huge wings.
- Palette: eagle body (70,48,34) · golden nape (150,104,48) · lion hind (140,98,52) · coverts (60,42,30) -> primaries
  (34,24,20) · underside (176,150,112) · talons (14,14,22) · **accent raptor yellow (255,200,40)**: beak, scaly
  shanks, eyes.
- Change from chibi: the white bland box head goes; a dark golden-eagle griffin with real proportions.
- Bones: keep all.
**IDLE - RAPTOR WATCH (120 f):** snappy head turns (6 f turn, 25 f hold, the head stays stabilised while the body
breathes); 60-80 cocks its head 40 deg to look up at the sky with ONE eye; 85 a beak clack; 95-110 re-tucks the wings
(wrists lift 6 deg and settle); the tail tuft flicks.
**ROAR - SKY SCREECH (60 f):** chest up, both wings flung UP into a tall V, beak gaping forward (not skyward), holds;
folds.
**SIGNATURE `act_mantle` - MANTLE THE KILL (95 f, NEW; replaces the hover-dive):**
- 0-12 spots prey in front: the head drops and locks on.
- 12-24 reaches forward with the right talon and strikes down onto it (Leg_FR forward + grip), body forward 0.15 SH.
- 24-36 MANTLES: both wings spread wide and LOW, arched forward like a tent over the prey (tips near the ground in
  front), head low between them glaring up at the viewer.
- 36-70 two tearing pulls: bite down, yank up 30 deg, the shoulders heave.
- 70-80 the head snaps up, beak open. 80-95 folds the wings, steps back, rest.
**FLY:** an eagle. Flap-flap-GLIDE: 2 powerful strokes with the primaries spread, then a glide hold; talons tucked under
the chest, lion hind legs trailing and pumping on each downstroke.
**Size:** the beak and wings read from far; the feather rows are 3 clear value steps.

### CelestialDragon (wingquad, flies, `pets/CelestialDragon.py`) - the moon eater
**Research**
- Eclipse myths across Asia: a dragon (or Rahu, or the heavenly dog) SWALLOWS the sun or the moon, then lets it go.
- Draco, the dragon constellation, winds around the celestial pole.
- Monitor lizards threaten with an arched neck and an inflated throat, and lash the tail.
**Design brief**
- Anatomy: a western dragon. BL 1.3 SH; an S-neck 0.75 SH (2 bones); a wedge head 0.45 SH long with a crown of 4
  swept horns (0.30 SH); 2-bone legs (lizard elbows out in front, digitigrade hind); membrane wings 2.8 BL; a tail 2.0 BL
  ending in a CRESCENT MOON blade 0.35 SH; a row of back spines.
- Silhouette: the horn crown + the crescent tail + wings.
- Palette: midnight blue (26,32,74) · dark (14,16,40) · underside pearl-grey (150,158,196) · membrane (34,40,92) with
  inner (22,26,62) · **accent moon white (236,242,255)**: the crescent blade, horn tips, eyes, constellation dots on
  the wings (1x1 inlays in star patterns), 5 floating star shards on the Orbit bone.
- Change from chibi: the pearl-white body with gold trim becomes a midnight dragon; real limbs; long neck and tail; no
  gold.
- Bones: keep Spine, Neck, Head, Jaw, Breath, Wing/WingTip, Tail1-3, Flame (= the crescent), Orbit. ADD Neck2, Chest,
  and Shin_/Foot_ on all 4 legs.
**IDLE - STARGAZE (120 f):** slow breathing; 0-40 the head tilts up following the circling Orbit stars; 40-70 holds the
gaze; the tail draws a slow S-curl along the ground; 90-110 the wings tighten their fold.
**ROAR - ROYAL ARCH (60 f):** the neck rises into a high arch and the head bends DOWN at the viewer (head pitch +40),
jaw wide roaring downward, horns forward, tail lifted; wings stay folded; settles.
**SIGNATURE `act_eclipse` - SWALLOW THE MOON (100 f, NEW; replaces the happy twirl):**
- 0-12 the tail sweeps round along the ground to the right.
- 12-30 it rises in a high arc OVER the back (Tail1 -60, Tail2 -50, Tail3 -40) until the crescent hangs above and in
  front of the head, like the moon.
- 30-42 the head rises and gazes up at it (S-neck); wings half open as a frame.
- 42-50 the jaws open wide. 50-56 SNAP: the jaws close around the crescent (jaw stops at 10 deg, the blade passes
  between the teeth; sparkle burst VFX) = the eclipse.
- 56-70 holds the moon in its jaws. 70-80 releases; the tail whips back down and round.
- 80-100 settle, wings fold.
**FLY:** majestic. Slow strokes (period 1.5 x the other flyers) with long glide holds; the S-neck held forward; the
tail streams with the crescent; front legs tucked like a cat's, hind legs trailing and pumping gently.
**Size:** the crescent and horns are the read; the constellation dots are >= 0.04 SH or skip them.

### Cvetibara (SECRET of the Celestial egg; wingquad, flies, `pets/Cvetibara.py`) - the blossom capybara
**Research**
- The capybara is the largest rodent: a barrel body, no tail, short legs with partly webbed feet, a blunt deep head with
  the eyes, ears and nostrils set HIGH in a line so it can soak with only the top of the head above water.
- Famously calm (other animals sit on it); Japanese zoos give capybaras hot yuzu baths, where they doze up to the chin.
- It flicks its ears rapidly to shed water and BARKS as an alarm. Males have a dark scent gland (the morillo) on the
  snout.
- Name: "tsvete" = flower.
**Design brief**
- Anatomy: a barrel body BL 1.6 SH; elbow 0.30 SH; 4 front toes, 3 hind; head 0.55 SH long, square and deep, eyes high
  and narrow (heavy-lidded), small round ears; big incisors (226,200,150) showing; a dark morillo bump on the snout;
  feathered wings from the shoulders spanning 2.2 BL; a floating halo; a 5-petal star-lotus on the head.
- Silhouette: the blunt square head + wings + lotus + halo.
- Palette: fur (86,54,36) · back (58,36,26) · cheeks + underside (138,98,68) · feet, nose, morillo (34,24,20) ·
  wings umber (70,46,32) -> feather tips · halo dark brass (170,136,64) · **accent magenta (255,70,170)**: lotus
  petals, feather tips, eyes.
- Change from chibi: the lovely loaf with a huge head, blush and lilac glint eyes becomes a real capybara with calm,
  heavy-lidded, dangerous eyes. Real colours.
- Bones: keep Spine, Head, Flower, Halo, Ear_, Wing/WingTip. ADD Neck, Jaw, Shin_/Foot_ on all 4 legs, Lid_L/R, and
  Petal1..5 (children of Flower).
**IDLE - ZEN EAR FLICK (120 f):** stands calm, lids half shut, a slow sway; 3 rapid ear flicks (left at f30, right at
f75); nose twitches (Head pitch ticks of 1.5 deg); the halo bobs; the lotus sways.
**ROAR - ALARM BARK (54 f):** 3 sharp barks: each one = a body jolt forward 0.03 SH, the jaw pops 25 deg, the wings snap
half open, the ears go forward; settle.
**SIGNATURE `act_bloom` - HOT-SPRING BLOOM (100 f, NEW; replaces the happy hop):**
- 0-16 SPA SOAK: sinks belly-down as if into a hot spring (legs fold, Spine -0.25 SH), chin on the "water line", lids
  shut, one ear flick.
- 16-34 curls into a BUD: the wings wrap forward round the body like closing petals (0.02 clear of the body), the head
  tucks down, the lotus petals fold shut.
- 34-44 holds the bud (a small quiver).
- 44-54 BLOOMS: springs up onto all four legs, the wings burst open wide and up, the petals snap open, head up (petal
  + sparkle VFX).
- 54-74 holds the bloom with a slow head turn; the wings shimmer (small flutter).
- 74-100 folds the wings, settles to rest.
**FLY:** "swims" through the air. Quick short wingbeats while all four legs paddle in a diagonal swimming gait; the
head stays level like a capybara crossing a river.
**Size:** head block + lotus + halo; the lotus petals are big flat blades (>= 0.10 SH).

---

## 7. Uniqueness table (verified: every cell is the only one of its kind)

| Pet | IDLE | ROAR | SIGNATURE |
|---|---|---|---|
| MossbackTortoise | doze: chin on the ground, lids close, one-eye peek | stand tall on straight legs + hiss + beak snap | `act_hide` retreat into the shell, peek, re-hide, emerge |
| ForestStag | scent the wind: nose up, ear swivels, alert freeze, nibble | rut roar: neck level forward, 3 bouts, antlers lowered | `act_scratch` scratches its flank/tummy with its antlers |
| Treant | wind sway, a gust, a creaking back-stretch | timber lean: tips forward 28 deg like a falling tree | `act_takeroot` roots down, becomes a tree, tears free |
| Kappa | dish guard: head kept level, hand cups the dish, squat bounce | screech crouch: arms wide, claws spread | `act_sumo` shiko leg-raise stomps + tsuppari thrusts |
| SeaTurtleWarrior | surface breath gulp + 2 trident taps | trident thrust x2 | `act_twirl` helicopter trident twirl + spring strike |
| Kraken | hover with a wave round the arm ring | kraken rise: 8-arm crown flare | `act_wrap` coils a mast, squeezes x3, drags it down |
| Raiju | alpha sentinel scan + lip snarl | howl, chin to the sky | `act_thunderflip` ball-lightning barrel roll |
| ThunderBull | cud grind + tail fly-swats + glare | broadside bellow, tail stiff | `act_charge` hoof scrape, lunge, horn hook |
| StormWyvern | gargoyle perch, tail whip-crack, jaw clacks | hood shriek: wings arched over the head | `act_thunderclap` 3 wing claps above the back |
| MoltenBoar | roots the ground + snort | crest bristle + jaw champs | `act_wallow` rolls on its back, legs bicycling |
| LavaGolem | knuckle rest, fist inspect, knuckle crack | gorilla chest beat | `act_pound` fist pounds + jumping double smash |
| Cerberus | sibling squabble (right head nips left) | three-head fan snarl | `act_triplesnap` heads snap at a fly in turn, then together |
| Ivonrath | claw drum + one-fang lip curl + tail curl | fire breath with one slow sweep | `act_emberdance` alligator U-bellow, back vibrates, jaw slap |
| ShadePanther | big-cat play-bow stretch | snarl + forepaw swipe | `act_pounce` stalk, wiggle, leap, pin |
| NightmareStallion | hip-shot rest + flehmen lip curl | squeal + hind-leg buck | `act_rear` rears up, strikes the air x3 |
| BlackDragon | serpentine sway, nudges its pearl | S-coil strike | `act_pearlchase` corkscrew rise chasing the pearl, claw catch |
| PharaohAsparuh | royal gaze down the nose, ear twitches | yawn turning into a snarl | `act_knead` kneads biscuits + slow blink |
| SolarLion | king's sit | lion roar ending in grunts | `act_sunburst` Lion-and-Sun: rays burst, paw raised |
| Griffin | raptor watch: head-lock turns, one-eye sky look | sky screech, wings in a tall V | `act_mantle` talon strike, wings tent over the prey, tearing |
| CelestialDragon | stargaze following the orbit stars | royal arch, roaring down at the viewer | `act_eclipse` tail arcs overhead, jaws close round the moon |
| Cvetibara | zen ear flicks + nose twitch | alarm barks x3 | `act_bloom` hot-spring soak -> bud -> bloom |

Duplicate check (one owner each): barrel roll = Raiju only; ground pound = LavaGolem only (Kraken's drum slams
retired); pounce = ShadePanther only (Cerberus' pounce finish removed); rear-up = NightmareStallion only (Wyvern's and
Cvetibara's rear-ups retired); buck = Stallion roar only (the bull's buck removed); shake-off = nobody; head shake =
nobody; spins: Raiju rolls the body, the turtle spins only its trident, the lion only its rays, the BlackDragon
corkscrews its body along a path - no two the same; howl = Raiju only (Cerberus' howl chorus retired); yawn = Pharaoh
only (Cerberus' yawn retired); stretch = ShadePanther only (Ivonrath's wing stretch and the Wyvern/CelestialDragon
wing stretches retired); grooming = ForestStag only (Pharaoh's paw-lick and Griffin's preen retired); sitting = SolarLion
only; sleeping = MossbackTortoise only; snort as the core beat = MoltenBoar only; fire breath = Ivonrath only
(CelestialDragon's star breath retired); wings forward: hood over the head (Wyvern roar), a tent over the prey
(Griffin act) and wrapped round the body (Cvetibara bud) are three different shapes.
New clip names to register in Studio/PetAnimator: act_hide, act_scratch, act_takeroot, act_wrap, act_emberdance,
act_pearlchase, act_knead, act_mantle, act_eclipse, act_bloom (renamed from act_shellspin, act_pronk, act_branchlash,
act_crush, act_stretch, act_coil, act_groom, act_strike, act_twirl (CelestialDragon), act_happy). act_twirl now belongs to
SeaTurtleWarrior only.
