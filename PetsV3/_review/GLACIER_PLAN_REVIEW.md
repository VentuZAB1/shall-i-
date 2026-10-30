# Glacier Egg - plan review (2026-10-27) - 12 pets, NONE ship as drafted

**Verdict:** 11 plans APPROVED WITH CHANGES, 1 plan REVISE (Permafrost Titan). The concepts are sound. The problems are colour
clashes with existing pets, acts or heroes copied from siblings, and two props (a wall) and sizes that break the rules.
Target for ship is 8/10 or better. Mythics are at 7 until their MUST items land.

## 0. What I checked

- Style: `Creature Style.md`, `Model Review Checklist.md`, `FIERCE_GUIDE.md`, the FIERCE act table in `FIERCE_PLAN.md`.
- Earlier plan reviews for format and strictness: InfernoPhoenix, CosmicLeviathan, AbyssWeaver (section headings).
- The 12 plans and `GLACIER_CONCEPTS.md` (sections 1-5).
- The lineup `_ALL_FIERCE_progress.png`. It shows 21 of the 30 pets (no Phoenix, Thunderbird, Thunder Rex, Leviathan,
  Orca, Hammerjaw, AbyssWeaver, Basilisk, Mantis), so those were checked from palettes and sheets.
- Model sheets of ThunderRex and CosmicLeviathan (the 1% secret bar that the mythics must beat).
- Owner refs `_refs/fierce/f_70`, `f_71` (in-game Cerberus secret, flames and dark studded hide).
- The RGB palette of all 30 `pets/*.py`, and every act and roar name in those files.
- Hue (H, degrees), saturation (S) and value for each new colour against every existing colour (`dH` = hue distance).
  Brightest channel of every body colour is >= 170. In-game values are x0.6.
- Odds tables sum to 100 in each egg. Money bonus formula checked on all 12 pets.

## 1. Summary

| Pet | Verdict | Score | One line |
|---|---|---|---|
| Frostfang Lynx | APPROVED WITH CHANGES | 7 | Clean cat read; the wall act is a prop, the body is plain silver |
| Ice Mammoth | APPROVED WITH CHANGES | 7 | Good shape; idle sniff copies the Badger; mint sits 20 deg from the Lynx |
| Glacier Yeti | APPROVED WITH CHANGES | 7 | Strong hunch silhouette; idle rake is the act's motion; green eyes copy Stag |
| Blizzard Roc | APPROVED WITH CHANGES | 6 | Reads as a recoloured Thunderbird (tail fan, crest, white head) |
| Permafrost Titan | REVISE | 5 | Crown copies Thunder Rex's crown; slabs, core, roar and act copy siblings |
| Frostcrown Dragon | APPROVED WITH CHANGES | 7 | Good mythic hero; height ties ForestStag; crystal wave copies Cinder |
| Bramble Badger | APPROVED WITH CHANGES | 7 | Most readable starter in the batch; add a mantle band; fix the dig paws |
| Coral Crusher | APPROVED WITH CHANGES | 6 | Good claws; stalked eyes read childish; no crab kit yet |
| Volt Rhino | APPROVED WITH CHANGES | 7 | Lightning horn works; body is a plain grey plate |
| Cinder Overlord | APPROVED WITH CHANGES | 7 | Strongest concept in the batch; body too dull; must beat the 1% secrets too |
| Wraith Hound | APPROVED WITH CHANGES | 6 | Ghost read works if tinted; indigo sits on the Void violets |
| Eclipse Seraph | APPROVED WITH CHANGES | 7 | New six-wing lion; halo is an open ring, body reads grey, height 11 |

---

## 2. Per pet

### 2.1 Frostfang Lynx (Starter, 50 %)
**APPROVED WITH CHANGES - 7/10**

Works: a cat with ear tufts reads at 64 px and differs from every existing pet. The ICE accent is pale (S 0.41), so it does not
copy Thunder Rex's saturated cyan.

MUST:
1. Body: WARM_SILVER (184,172,160) becomes **(190,172,150)** (H 33, S 0.21). The old value is close to the Badger's grey
   (176,172,180, about 22 RGB apart) and both are starters. The warmer sand-silver is the Lynx's own read.
2. Pattern: add **BACK_SHADE (126,116,110) rosette spots** on the flanks, at least 20 % of the side view. Plain silver is the
   "grey plastic toy" risk.
3. Act: **no wall.** A wall is a prop the pet does not own. The forepaws-on-the-chest lift is also NightmareStallion's
   `act_rear` (rears, strikes the air). Replace `act_wallclaw` with **`act_clawflex`** (96 f, in place):
   - f0-20: crouch stare. Body lowers 0.05H. Head yaws 14 deg toward the follow camera and holds to f40. Tufts flatten 8 deg.
   - f20-40: tufts rise 12 deg and hold.
   - f40-72: the forepaws flex one after the other (lag 8 f). Each claw bone rotates 35 deg out. ICE spark on each claw
     (events `claw1` f48, `claw2` f60). Paws stay on the ground.
   - f72-84: claws retract. Tail tip flicks 10 deg once.
   - f84-96: exact rest pose. Hind feet planted in every frame.
4. Idle: head yaw +/-14 is fine, but **neck yaw stays within 8 deg** (the head takes the rest of the drift).

NICE: keep ICE_CLAW smooth and the tufts as blocks only, as planned.

### 2.2 Ice Mammoth (Medium, 26 %)
**APPROVED WITH CHANGES - 7/10**

Works: dome hump, tusks and trunk read at 64 px. The teal body (brightest 188) sits well under the Lynx.

MUST:
1. Idle: **drop the ground sniff.** The Bramble Badger's idle is a nose-down sniff, so the same motion is shared.
   New idle: trunk swings slowly (tip +/-12 deg, two cycles), one exhale puff at f80, tusks stay still.
2. Accent: MINT (140,236,222) becomes **(150,236,210)** (H 162, S 0.36). That is 29 deg from the Lynx ICE (H 191) and 22 deg
   from the Yeti AURORA (H 140). The old mint was 20 deg from the Lynx, too close inside the Glacier six.
3. Build gate: the kit has no trunk tube. Prototype the 4-segment trunk (`B.seg` taper chain) before the full model, and
   check it reads as a trunk, not a hose, at 64 px.

NICE: the act (`act_dustover`) is fine. No existing pet throws dust or uses a trunk.

### 2.3 Glacier Yeti (Big, 14 %)
**APPROVED WITH CHANGES - 7/10**

Works: hunched body plus ice-plate arms is a unique silhouette. The skid-and-brake act is accepted (ruling 3.2).

MUST:
1. Idle: the **knuckle rake** (f30-50, fist raking the snow) is the same motion as the act's arm sweep (act beat 2, plates
   scraping). Replace the rake with a **plate settle**: plates lift 4 deg and settle twice (f30-50). Head lowers 6 deg at f55-75
   with **no snow contact**. Back to rest by f100.
2. Eyes: the AURORA (120,240,160) slits sit 8 deg from the Grass Stag's green eyes (H 148, EYE 70,240,150). Eyes become a
   **BLACK socket with a PLATE_ICE (206,226,240) slit** and a BLACK pupil. AURORA stays on the plate seams only.

NICE:
- HEIGHT 9.5 is bigger than the Roc (9.0) while the Yeti is the commoner (14 % vs 7.4 %). Set the Yeti to **9.0**.
- POLAR_NAVY (120,128,200) is 3 deg in hue from ThunderBull's BODY (98,108,178). Accepted as cross-egg (ruling 3.9). Keep the
  plates and the aurora seams as the separators.

### 2.4 Blizzard Roc (High, 7.4 %)
**APPROVED WITH CHANGES - 6/10**

Works: a large winged bird, grey back, frost crest. The wing kit is proven.

Main problem: as drafted the Roc is a **Thunderbird with new colours.** The Thunderbird owns the white head (WHITE 236,240,248,
the Roc's SNOW is 238,242,250), the 7-feather white fan (its hero, which the Phoenix review already removed) and a swept-back
crest (14-22 deg).

MUST:
1. Tail: **no 7-feather fan.** Use four plain tail feathers, CHAR tips, FROST tip bars.
2. Crest: the three plumes stand **erect, 60-75 deg from the head** (not swept back). Plume tips FROST_V.
3. Head: keep SNOW, but add a **CHAR eye mask and brow** so the white head is not the Thunderbird's plain white head. The eye is
   a BLACK socket with a FROST_V slit.
4. Body: STORM_GREY (176,182,196) becomes **(176,178,186)** (H 228, S 0.05). The old blue-grey joined the blue cluster that
   the AZD and Titan sit in.
5. Act `act_bow`: root travel must be **0 net**. Replace the 0.15H forward-back bob with a vertical bob (root z +/-0.03H, two
   bobs). Replace the tail-fan shake (f64-88) with two tail flicks of 6 deg.
6. Walk: no hop. A hop reads as airborne. Use a plain walk with wings folded.

NICE: add CHAR breast bars (snowy-owl style) for dark tones on the white bird.

### 2.5 Permafrost Titan (Secret, 2.5 %)
**REVISE - 5/10**

Why: the hero is a copy. Thunder Rex (1 %) has a gold crown band with pale spikes (see its model sheet, front view). The
Titan's gold band with five ICE spikes reads the same at 64 px. Several other parts copy siblings too.

MUST:
1. **Hero:** remove the head crown. New hero is a **GOLD chest bezel**: a ring 0.22H across around the chest core, tilted up
   10 deg. Outer GOLD (255,196,50), inner GOLD_D (214,150,30). The bezel must show at least 25 gold px in the 64 px icon.
   (Owner decision, see section 7, item 1.)
2. Gold: PALE_GOLD (250,226,158) becomes **house GOLD (255,196,50)**. The pale tint is 10 RGB from Treant's SAP_HOT (255,228,150).
3. Core: remove ICE_CORE (170,232,255). It is 5 deg and 20 RGB from the Lynx ICE (150,236,255). The core inset is **ICE_W
   (226,240,250)**. The periwinkle glow stays VFX only.
4. Body: SLATE_VIOLET (160,152,200, H 250) becomes **MAUVE (184,150,200)** (H 281, S 0.25). Four Glacier bodies were at H 212-250
   (blue-violet). The mauve takes the Titan out of that cluster.
5. Shoulders: the two ICE_W slabs per side, tilted 20 deg, are the same construction as the Yeti's shoulder plates. Replace them
   with **two rounded, studded MAUVE pauldron blocks per side, each with an ICE_W cap** (tip 0.05H). No tilted slabs.
6. Eyes: the ICE_CORE slits are the same cyan as the Lynx and Rex eyes. Use **ICE_W slits** in JOINT_D sockets, BLACK pupils.
7. Roar: remove the slab flare (the Yeti's shoulder heave). New **`core bellow`**: head lifts 10 deg, arms out 8 deg, the chest
   bezel pulses (VFX on `Core`) at f22 and f34, held f22-50, back to rest by f66.
8. Act: remove `act_crownflare`. Its crown spikes fanning one by one with lag and a frost bloom copy Cinder's crown-plate lift
   and Cvetibara's bloom. New **`act_kneelrise`** (100 f, in place):
   - f0-18: right knee drops to the ground (contact >= -0.02). Head bows 12 deg. Fists rest on the thighs.
   - f18-50: hold the kneel. Core pulses at f30 and f44 (VFX, event `core`). Fists do not touch the ground (AZD owns the press).
   - f50-84: rises from the knee. Root y back to 0 within +/-0.04.
   - f84-100: exact rest pose, 0 collisions.
9. Idle: the crown creak goes. New idle: weight shift (hip yaw +/-3), core pulse at f40 and f100, pauldrons settle. No head tilt.

NICE: keep the build height at 10.0 (equal to Rex). It stays below the 1 % secrets on tier.

### 2.6 Frostcrown Dragon (Mythic, 0.1 %)
**APPROVED WITH CHANGES - 7/10**

Works: no existing pet is steel-blue with gold horns and a white crystal spine. The gold horns (swept, banded) are a different
shape from BlackDragon's antlers. The "frost press" head drop is distinct.

Outclass check: as drafted it is **11.0 tall, the same as ForestStag** (16 %, the commonest Grass stag). The mythic is not the
tallest pet, so it does not outclass.

MUST:
1. HEIGHT **11.0 becomes 11.5.** The mythic must be the tallest pet in the game.
2. Body: STEEL_BLUE (150,176,206) becomes **(124,160,216)** (H 216, S 0.43). The old value is near grey in game (about 90,106,124)
   and reads as a grey-blue plastic dragon. The new value keeps the steel read with colour (about 74,96,130 in game).
3. Act `act_stillfreeze`: the crystal wave runs tail to neck with a 3-frame lag per bone. That is Cinder's `act_molt` ripple
   (tail to head). Change it so **all seven shards rise together, no lag:**
   - f0-14: inhale (chest +0.02H). Wings and tail still.
   - f14-22: all seven dorsal shards rise together 25 deg. One frost click at f16 (event `click`).
   - f22-44: head presses down to the ice (pitch down 25 deg, within 30). Jaw opens. Snout is the only low point (>= -0.02).
   - f44-58: frost mist cone from `Mouth` (event `frost` f50, VFX).
   - f58-80: all shards fall together. Head lifts.
   - f80-110: wings fold, exact rest pose.
4. Tris: the plan's 12-15k sits at the 15k cap. Set the step-1 gate at **13k**, and report the count before the full build.

NICE: make the shards flat frost fins (blade section, width 2:1) so they read as a fin row, not Rex's spike row. Five fins are
enough if the tris are tight.

### 2.7 Bramble Badger (Starter, 40 %)
**APPROVED WITH CHANGES - 7/10**

Works: a grey back with an amber thorn row is the most readable Grass starter. The inverted colouring (pale back, dark belly)
is the real badger's read. Accepted (ruling 3.4).

MUST:
1. Back: the grey (176,172,180, S 0.04) is one flat tone. Add a **mid-dark mantle band (110,104,116)** over the shoulders and
   nape, at least 10 % of the side view. Keep the cool grey on the rest.
2. Act `act_burrow`: the plan says both "forepaws dig in turns" and "forepaws stay on the ground". Those conflict. Rule: the
   forepaws scoop (lift at most 0.05H) and touch down at each scoop. Ground contact >= -0.02.

NICE: keep the thorns short and low. The Basilisk owns the frill; the badger must not become a row of tall spikes.

### 2.8 Coral Crusher (Medium, 15 %)
**APPROVED WITH CHANGES - 6/10**

Works: bronze shell, rose-spiked claws, and the fiddler wave is a new act (no existing claw wave).

Risk: there is no crab kit. Six legs, two claws and two eyestalks is a new rig.

MUST:
1. Eyes: the 0.14H eyestalks read as a cartoon snail and risk the owner's "too childish" rejection. Shorten the stalks to
   **0.07H** and make them thicker. Set the rose slit eyes into the SHELL_D brow plate, angled 15 deg inner-down.
2. Build gate: prototype the six-leg sideways walk (body yaw 0) and check the legs stay planted through the act's wave, before
   the full model.

NICE: ROSE (255,120,150) is 7 deg from the Wyrm's ROSE. Accepted (ruling 3.9). Watch it in the lineup.

### 2.9 Volt Rhino (High, 6 %)
**APPROVED WITH CHANGES - 7/10**

Works: the long lightning horn is a clear hero. The VOLT lime (210,255,80) is 21 deg from the Thunderbird's bolt yellow, so the
accent is distinct inside the Thunder egg.

MUST:
1. Body: IRON (176,180,186, S 0.05) is a plain grey plate. Give **IRON_D (104,110,120) the back, shoulder shield and skin
   folds**, at least 25 % of the side view. IRON stays on the flanks and legs. The PALE belly stays.
2. Roar: "horn-to-the-sky" stays, but **head pitch-up is 16 deg or less** (not 22), and the snout stays forward during the bellow.
   Raiju's howl is chin-to-sky. The rhino must not read as that.

NICE: HEIGHT 9.0 sits above the Thunderbird (8.5) while the rhino is the commoner (6 % vs 4 %). Set it to **8.5**.

### 2.10 Cinder Overlord (Ultra-rare, 0.5 %)
**APPROVED WITH CHANGES - 7/10**

Works: the strongest concept in this batch. The obsidian crown with a gold rim is distinct from Ivonrath's three-point flame
crown, the rose vents copy no Fire pet, and `act_molt` is new.

Tier note: 0.5 % is **rarer** than Thunder Rex (1 %) and Cosmic Leviathan (1 %). The plan only says it must beat the Phoenix
and Ivonrath. It must beat the 1 % secrets as well.

MUST:
1. Body: PLUM_OBS (176,150,168, S 0.15) is a dull mauve-grey in game. Use **(182,132,172)** (H 312, S 0.27). OBS_D stays for scales.
2. Outclass gate: at 64 px, the gold rim shows at least 25 gold px in the icon. HEIGHT 10.5 stays above Rex's and Leviathan's 10.0.

NICE:
- The roar's plate tilt (25 deg) and the molt's plate lift (35 deg) use the same plates for the same motion. Cut the roar tilt to
  15 deg, so the act owns the big plate lift.
- A/B against BlackDragon's `act_pearlchase` at step 1 (both are serpent kits).

### 2.11 Wraith Hound (Medium-high, 10 %)
**APPROVED WITH CHANGES - 6/10**

Works: a streaming soot mane and two indigo eye slits. The `act_smokecloak` is distinct.

Issues: the ash body (176,176,190, S 0.07) is a plain grey, the grey-plastic risk. The indigo eyes (H 254) sit 17 deg from
ShadePanther's VIOLET (H 271) and 10 deg from BlackDragon's MANE (H 264). Panther and BlackDragon are **in the same Void egg**,
so this is a sibling accent copy.

MUST:
1. Body: ASH (176,176,190) becomes **lavender-ash (170,160,206)** (H 253, S 0.22). That keeps the ghost pale without a grey read.
2. Dark saddle: SOOT (92,92,116) runs as a **solid saddle along the spine, at least 18 % of the side view**, not only the mane tips.
3. Accent: INDIGO (120,84,240) becomes **(100,120,240)** (H 231). INDIGO_L (176,150,255) becomes **(160,176,255)** (H 230).
   That is 40 deg from Panther VIOLET and 33 deg from BlackDragon MANE.

NICE: keep the mane as SOOT blocks only. Ears as planned.

### 2.12 Eclipse Seraph (Mythic, 0.1 %)
**APPROVED WITH CHANGES - 7/10**

Works: a pale lion with six wings and a dark halo is a new silhouette. `act_wingcascade` is the only wing-ripple act. The
cascade read is distinct.

MUST:
1. HEIGHT **11.0 becomes 11.5** (same reason as the AZD, ForestStag at 11.0).
2. Halo: as drafted it is an open annulus. From above it reads as Cvetibara's brass ring. Make it a **solid OBSID disc** (fill
   the centre), a GOLD rim band of 0.02H, and the BLOOD ring just inside the rim on the disc face.
3. Body: MOON_IVORY (226,222,236, S 0.06) is a grey lion in game (about 136,133,142). Use **(232,208,240)** (H 285, S 0.13), a lilac
   ivory. IVORY_D shading stays.
4. Six wings gate: build the three pairs as a step-1 test. Report the tris count and a 64 px read. Target 13k, ceiling 15k.
   If the gate fails, see section 7, item 2.

NICE: the lower pair (0.6H) is small. Keep it tucked at the flank, so the read is two big pairs plus a tuck.

---

## 3. Rulings on the planner's doubts

1. **Gold crowns: YES.** The house gold (255,196,50) and GOLD_D are the secret / ultra / mythic hero colour, used only on the hero
   piece. Existing gold heroes: Thunder Rex, Cosmic Leviathan, Orca, BlackDragon. New gold heroes: Titan chest bezel, AZD horn
   pair, Wyrm rim plates, Seraph halo rim. Each gold piece must have its own shape. The Titan changes from pale gold to house
   gold (2.5 MUST 2). Style rule, decided.
2. **Yeti act swap (ground slam to skid and brake): ACCEPT.** The kit's pounds belong to LavaGolem (`act_pound`) and Hammerjaw
   (`act_hammerslam`). A skid is different. The idle rake is removed (2.3 MUST 1) so the skid owns the arm motion.
3. **Titan pale gold vs Treant sap: REVISE to house gold** (2.5 MUST 2). Pale gold reads cream.
4. **Badger inverted colouring: ACCEPT.** The real badger's read is the strongest at 64 px. The cool grey back and the mantle
   band (2.7 MUST 1) keep it from being a plain grey plate.
5. **Ash-grey Wraith: APPROVED WITH CHANGES.** A pale ghost is allowed as the exception to the dark-body rule, but only tinted
   (lavender-ash) with a solid dark saddle (2.11 MUST 1 and 2). Plain grey is not allowed.
6. **White Roc: ACCEPT.** White head and breast are a snowy-raptor colour. The dark tones come from the CHAR eye mask, the
   flight feathers and the optional breast bars.
7. **Lynx act needing a wall: REJECT the wall.** The owner rule is that acts cannot rely on a prop the pet does not own.
   Replace with `act_clawflex` (2.1 MUST 3).
8. **Seraph's six wings: ACCEPT, with a step-1 gate.** Three pairs are the mythic read. If the gate fails (tris over 15k or a
   64 px blob), the fallback is four wings, and that needs the owner (section 7, item 2).
9. **Cross-egg accents:**
   - Badger amber vs Solar Lion: **ACCEPT.** The amber is on the thorns. The Solar Lion's tawny is a body colour.
   - Volt lime vs Mossback eyes: **ACCEPT.** The lime is 21 deg from the Thunderbird (a sibling) and 8 deg from Mossback (another egg).
     Keep (210,255,80). The lightning stays on the horn.
   - Mammoth mint vs Pharaoh turquoise: **ACCEPT**, because the mint is pale (S 0.36) and Pharaoh's turquoise is saturated (S 0.83).
     The Mammoth mint still moves (2.2 MUST 2) to get away from the Lynx.
   - Titan pale gold vs Treant sap: **REVISE** (see item 3).
   - Seraph blood vs Ivonrath and Cerberus reds: **ACCEPT.** The blood is a 4 % corona on a lilac pet. Ivonrath's red is the body.
   - Lynx ice vs Thunder Rex cyan: **ACCEPT.** The Lynx ice is pale (S 0.41), Rex's cyan is saturated (S 0.76), and Rex is another egg.
   - Crab bronze vs Treant heart: **ACCEPT.** Treant's heart is its face, and its body is bark.
   - Rhino roar vs Raiju howl: **ACCEPT with the pitch limit** (2.9 MUST 2).

**Extra rulings I made (not in the planner's list):**
- Crab ROSE vs Wyrm ROSE (H 347 vs 340, RGB 26 apart): **ACCEPT, cross-egg.** The Water egg has coral and aqua, so the Crab
  cannot use a warmer tone. Both are rose-accent pets on different eggs. Watch in the lineup.
- Yeti navy vs ThunderBull (3 deg of hue, cross-egg): **ACCEPT.** The silhouette and the plates separate them.
- Roc FROST_V vs Panther VIOLET (12 deg, cross-egg): **ACCEPT.** The Roc is the Glacier's only violet and the eyes are not
  violet on the Wraith after its change.

## 4. Problems the planner did not list (cross-pet)

| # | Problem | Pets | Where it is fixed |
|---|---|---|---|
| a | Titan crown is the Thunder Rex crown (gold band, pale spikes) | Titan / Rex | 2.5 MUST 1 |
| b | Titan ICE_CORE is the Lynx ICE (5 deg, 20 RGB) | Titan / Lynx | 2.5 MUST 3 |
| c | Titan shoulder slabs are the Yeti's shoulder plates (same tilt, same size) | Titan / Yeti | 2.5 MUST 5 |
| d | Titan roar slab flare is the Yeti's shoulder heave | Titan / Yeti | 2.5 MUST 7 |
| e | Mammoth idle ground sniff is the Badger's idle sniff | Mammoth / Badger | 2.2 MUST 1 |
| f | Yeti idle rake is the Yeti's own act motion | Yeti | 2.3 MUST 1 |
| g | Yeti aurora eyes sit 8 deg from the Stag's green eyes | Yeti / Stag | 2.3 MUST 2 |
| h | AZD crystal wave is the Cinder's ripple (tail to neck, lag per bone) | AZD / Cinder | 2.6 MUST 3 |
| i | Lynx wall claw is the Stallion's rear and strike | Lynx / Stallion | 2.1 MUST 3 |
| j | Roc tail fan and swept crest are the Thunderbird's heroes | Roc / Thunderbird | 2.4 MUST 1 and 2 |
| k | Roc white head is the Thunderbird white head (same RGB) | Roc / Thunderbird | 2.4 MUST 3 |
| l | Wraith indigo sits on the Void violets (Panther 17 deg, BlackDragon 10 deg) | Wraith / Panther, BlackDragon | 2.11 MUST 3 |
| m | Lynx warm silver is close to the Badger's grey (about 22 RGB, two starters) | Lynx / Badger | 2.1 MUST 1 |
| n | Crab stalked eyes read childish | Crab | 2.8 MUST 1 |
| o | 0.5 % Wyrm is rarer than the 1 % secrets, so it must beat them too | Wyrm / Rex, Leviathan | 2.10 MUST 2 |
| p | ForestStag (11.0, 16 %) is as tall as both mythics | AZD, Seraph / Stag | 2.6 MUST 1, 2.12 MUST 1 |
| q | Roc (9.0) is taller than the Thunderbird (8.5, rarer); Yeti (9.5) taller than the Roc (7.4 %, rarer) | Roc / Thunderbird, Yeti | 2.3 NICE, 2.4 NICE |

## 5. Glacier lineup check

**As drafted: FAIL.** Four of six bodies sit at hue 212-250 with saturation 0.2-0.4 (Titan 250, Yeti 234, Roc 222, AZD 212).
Together with the pale value they read as "six pale-blue animals".

**After the MUST changes: PASS.**

| Pet | Body (after) | H | S | In game (approx) | Silhouette |
|---|---|---|---|---|---|
| Lynx | (190,172,150) | 33 | 0.21 | (114,103,90) warm sand-silver | cat, tufts |
| Mammoth | (150,184,188) | 186 | 0.20 | (90,110,113) charcoal teal | elephant, trunk, tusks |
| Yeti | (120,128,200) | 234 | 0.40 | (72,77,120) navy | hunched ape, plates |
| Roc | (176,178,186) | 228 | 0.05 | (106,107,112) storm white | wing bird, white head |
| Titan | (184,150,200) | 281 | 0.25 | (110,90,120) mauve stone | upright giant, bezel |
| AZD | (124,160,216) | 216 | 0.43 | (74,96,130) steel blue | four-legged wing dragon |

Accents after the changes:

| Pet | Accent | H | Where |
|---|---|---|---|
| Lynx | ICE (150,236,255) | 191 | eyes, tuft tips |
| Mammoth | MINT (150,236,210) | 162 | tusk cracks, eyes |
| Yeti | AURORA (120,240,160) | 140 | plate seams only |
| Roc | FROST_V (176,140,255) | 259 | crest tips, primary bars |
| Titan | GOLD (255,196,50) | 43 | chest bezel |
| AZD | GOLD (255,196,50) | 43 | horn crown |

Silhouettes are six different animal shapes (cat, elephant, ape, bird, giant, dragon). Gold appears on the two secret and
mythic heroes only, and each gold piece has its own shape. Non-gold accent hues are at least 22 deg apart. The two golds are
the same house gold on two different heroes.

## 6. Gates for every builder

- Step 1: tris count (target 13k, cap 15k), `collision_free: true`, `ground_min_z >= -0.02` on every frame, linear 0, loops closed.
- Icon strip at 64 px and 128 px, next to the nearest existing pets (siblings and the 1 % secrets for the rare tiers).
- Value shares printed against the rule: dark body share, pale underside, one accent, gold share.
- Pose sheet of the key beats of every act before export. Acts play in place and end on the exact rest pose.
- Act references pulled from animationreference.org and cited, per the owner's rule.

## 7. OWNER items

1. **Titan hero location.** This review puts the gold hero on a chest bezel, because a head crown would copy Thunder Rex. The
   other option is a head headdress with no spike row, as a gold arch. Owner chooses before the build.
2. **Seraph six wings (conditional).** Only if the step-1 gate fails (tris over 15k, or a 64 px blob), the fallback is four wings.
   The owner decides whether to accept it.
