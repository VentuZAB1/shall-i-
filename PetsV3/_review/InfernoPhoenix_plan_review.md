# Inferno Phoenix - plan review (2026-10-14) - CONCEPT APPROVED; PALETTE, ACT, ROAR, POSTURE, TAIL and CREST REVISED

**Verdict: build v1 to this brief.**

**Keep from the plan:**
- the concept: a volcanic fire-raptor, the Magma egg's 2 % secret
- the Thunderbird pipeline: the wingbiped rig, `wing3.Wing`, the CLOAK FOLD, LIFT1→4, `plant_frames`, `lift_air_frames`
- a long S-neck that lifts the head above the shoulders
- the 2 heroes: a 5-plume flame crest and 3 tail streamers
- the knee hidden in the belly, the hooked gold beak, black hooked talons
- ground pose **A (cloak fold)**
- the full Fly clip set

**Replace:**
- **The palette.** EMBER (196,42,34) is **2° from Ivonrath's RED** (same egg). LAVA (255,104,24) is **2° from MoltenBoar's MAGMA**, the Boar's one accent. FLAME (255,184,36) is **0.3° from Ivonrath's FLAME**, its accent and crown colour. BASALT (44,38,44) has lum 40: in game ≈ (26,23,26), a black hole with no visible studs.
- **The REBIRTH act.** The forward wing-wrap cocoon → burst is **Cvetibara's `act_bloom`** (bud → bloom: "the wings wrap forward round the body", then "burst open wide and up"). FIERCE_PLAN §7 lists "wrapped round the body (Cvetibara bud)" as an owned wing shape.
- **The roar.** "Rear up, wings flare to the full V, screech" is the **Griffin's roar** (sky screech, tall V) plus the **Thunderbird's roar** (raised V + screech), and rear-up belongs to **NightmareStallion** only.
- **Posture 35°.** Thunderbird v1 failed at 32° ("person in a bird costume", head stacked on top). Use 40°.
- **The 7-feather tail fan.** The fan is the Thunderbird's hero, and it would cut the streamers in every lift. No fan.
- **The flame-eye paddles.** A round blob at the end of a tail is **Ivonrath's spade**. A curled-up tip is the **Celestial Dragon's crescent**.
- **The brow sun-disc.** That is **SolarLion's brow sun mark**.
- **The lava-crack seams on the mantle.** MoltenBoar and LavaGolem own seams and cracks; Rex owns glowing seams.
- **The Mouth / fire-breath anchor.** Fire breath belongs to **Ivonrath** only.
- **The slit pupil.** It reads as a dragon. Use the Thunderbird's approved lid-heavy eye.

**What I looked at:**
- your plan
- `pets/Thunderbird.py` (all of it), `wing3.py`, the `blockkit.py` API, `run3.py`
- petkit VIEWS / `camera_for` / `shots`; `_tools/path_test.py`, `fold_search.py`, `headless_model.py`
- Thunderbird reviews 1-3, `Thunderbird/renders/_model_sheet`, `_fold_sheet`, `_icons_strip_64`
- `_tools/_magma_flyers.png`, `_icons_sheet.png`, `_ALL_FIERCE_progress.png`
- the Ivonrath, BlackDragon and CelestialDragon icons
- the headers / palettes / crown, spade, mane and ray code of Ivonrath, BlackDragon, SolarLion, CelestialDragon, MoltenBoar, LavaGolem, Cerberus, Griffin and StormWyvern
- the palettes of all 28 `pets/*.py`
- FIERCE_PLAN §0, §4-6 and the §7 uniqueness table
- `LESSONS_ALL_PETS.md`, `ANIM_REFERENCES_1014.md`
- `studio/CreatureVFX.lua`
- the CosmicLeviathan review (the format exemplar only; I touched no Leviathan file)
- sizes of the comparison pets (`<Name>_bu.json`, HEIGHT / H_MODEL constants)

**How I measured:**
- Hue distances were computed in HSV against every RGB constant in `pets/*.py`; lum = 0.299R + 0.587G + 0.114B.
- I ran two headless experiments on the approved **Thunderbird** body, which uses the same wing3 recipe. Scripts and renders are ONLY in `C:\Users\ventu\AppData\Local\Temp\phx_review\` (`droop_test.py`, `env_test.py`, `sheet1.png`, `sheet2.png`):
  1. The full REBIRTH wing path (§7.7), keyed with bezier, checked at **step 1 on every frame** with all Thunderbird `check_pairs()` (wings vs head, neck, tail, legs, chest, spine) plus `joints()`. **Result: 0 hits.**
  2. The folded-wing envelope behind the body at FOLD / LIFT1 / LIFT2 / BREATH / LIFT3, used to place the streamers (§4.6).
- Nothing in the project was written except this file. Blender ran with `sys.dont_write_bytecode = True`.

---------------------------------------------------------------------------------------------------------------------
## 0. Your questions, answered

1. **Ground pose: A, the cloak fold.**
   - B ("rising mantle") is **the Griffin's ground pose**: `Griffin.FOLD = (40,-4,0,100)`, commented "heraldic raised V".
   - The Thunderbird reviewer tested a raised V as the icon pose: in tq the wings go edge-on and the pet shrinks to a sliver at 64 px (Thunderbird review 2, §8).
   - B would also need a new fold search and a raised-wing walk, and it would put the wingtips into the crest and streamer space.
   - The heraldic "phoenix rising" frame still exists: it is the airborne climax of the act (§7.7, f68-76), where it means something.
2. **Streamers: yes, 3, with changes** (§4.6).
   - Centre 1.40 long, sides 1.27.
   - Each is a **lanceolate vane** (length ≥ 3.5 × width) ending in a **straight** stepped tongue.
   - No round "eye" and no paddle blob (Ivonrath's spade). No curl over 20° (the Celestial Dragon's crescent / hook).
   - They are tail plumes: no standing blades on the back, so nothing like the Black Dragon's mane.
3. **Crest: 5 plumes, yes, re-specified** (§4.5).
   - They rise 44-55° from inside a plain **GOLD circlet** (the secrets' gold, no points). The centre plume is the model top.
   - **Sun-disc: NO.** It is SolarLion's brow sun mark, and a gem on the brow sits exactly where Ivonrath wears its crown.
   - The gold anchor is the circlet plus the beak (§2).
4. **Palette: no** (see the remix list above). Use **"BLACKBODY"** (§3): an ash-basalt bird whose fire gets hotter toward every extremity (EMBER → LAVA → FLAME → HOT), with a vermilion hide, a molten-cream underside and the house gold.
5. **REBIRTH:** keep the name, replace the mechanics. It becomes **"ASHES TO FLAME"**:
   - **pyre**: the wings droop open, wide, low and swept back
   - **ember sleep**
   - **two heartbeats**
   - the head wakes first
   - **an airborne rise on two wingbeats**
   - a screech at the top, then land and fold

   The wing path is **tested: 0 hits at step 1** on the Thunderbird body (§7.7).
6. **Remixes: 14 found** (§1 table).
   **Missing jackpot factors:**
   - one owned fire language: the curved, stepped feather ramp on every feather
   - a moving hero in the idle: streamer licks and the crest flare
   - a game-camera money shot in the roar: the fire train
   - the gold circlet
   - secret-tier size (HEIGHT 10)
   - the VFX package (§8)

**Sizes:** HEIGHT **10** (the plan's 9.5 is under the other secrets, which are all 10). **H_MODEL 2.05** (centre crest tip at idle f0). Reasoning in §4.9.

---------------------------------------------------------------------------------------------------------------------
## 1. One-line read and remix sweep

**One-line read (64 px):** "a black, crowned fire-raptor: a gold-ringed flame crest, wings and three long tail plumes that burn hotter toward their tips."

**How it must differ from each named pet:**

| pet | what that pet owns | the Phoenix instead |
|---|---|---|
| **Thunderbird** (same kit, Storm 5 %) | bulky 46° teal breast, white head, white bolt-tipped FAN, gold feet, harpy crest swept back 14-22°, KINKED 2-step bolts that alternate direction | slim breast (hw 0.22 vs 0.27) at 40°; a long S-neck (head front ≥ 0.10 ahead of the breast); BASALT hood; **no fan** (3 streamers); **EMBER scaled tarsi**; crest **rising 44-55°** from a gold circlet, the model top; **curved stepped tongues, all curving the same way (flowing), never jogged** |
| **Ivonrath** (same egg, 4 %) | crimson body (≥ 60 % red), crimson bat membranes, horns, a 3-point FLAME crown between the horns, a diamond spade on the tail tip, fire breath, the U-bellow act | dark ash-basalt dominant (≥ 32 % side); vermilion hide at 14° (not crimson), ≤ 24 %; feathers only (no horns, scales or membranes); **circlet with no points**, flames swept back; streamers end in long lanceolate vanes, never a diamond; no breath anywhere |
| **Black Dragon's flame mane** | a ROW of standing flame blades along the spine, and flame blades streaming back flat from the poll | no blades on the back or neck; the hackles are a **flat-laid cape** (shingles laid back 60-75°); the crest grows from the crown top inside a ring and rises steeply, it does not stream flat off the poll |
| **Celestial Dragon's crescent tail** | one long tail ending in a white crescent blade; the tail arcs over the head in its act | three plumes; no crescent, hook or curl > 20° at any tip; streamer tongues are collinear (§4.6), so lifting them never makes a hook; in the roar the plumes stop at ≤ 85° and stay behind the hips (y ≥ 0.95), never over the head |
| **SolarLion** | a radial ray wheel behind the head, a sun mark on the brow, rays that spin | the crest occupies only the **upper-rear quadrant** (every plume direction has y ≥ +0.5, z > 0); no plume points forward, sideways or below horizontal; nothing rotates as a wheel; no brow mark |

**Remix table (everything in the plan that is owned by someone else):**

| in the plan | remixes | replace with |
|---|---|---|
| EMBER (196,42,34) | **Ivonrath RED 2.2°** | EMBER vermilion (232,78,32) on a basalt-dominant body (§3) |
| LAVA (255,104,24) | **MoltenBoar MAGMA 2.2°** (its one accent) | LAVA (255,128,24), used ONLY as a ramp step inside a feather, never as a mark |
| FLAME (255,184,36) | **Ivonrath FLAME 0.3°** (its accent and crown) | FLAME (255,214,72), ramp step only |
| lava-crack seams on the mantle | MoltenBoar seams, LavaGolem cracks, Rex glowing seams | a tonal BASALT mantle; the fire lives only in feather tips |
| brow sun-disc + gem | **SolarLion** brow sun mark; a brow jewel where Ivonrath wears its crown | none; gold = circlet + beak |
| ground pose B | **Griffin** FOLD (heraldic raised V) | A, cloak fold |
| 7-feather tail fan | **Thunderbird** white fan | no fan; 3 rump shingles over the streamer knuckles |
| paddle with a flame "eye" | **Ivonrath** spade, **Celestial Dragon** crescent | lanceolate vane + straight tongue |
| nape hackles as "flame-edged rows" | **Black Dragon** mane blades | flat cape, EMBER, LAVA tips on the hem row only |
| wing-wrap cocoon → burst | **Cvetibara** `act_bloom` | PYRE → heartbeat → airborne rise (§7.7) |
| roar: rear up + full V + screech | **Griffin** roar, **Thunderbird** roar, **Stallion** rear-up | FIRE-TRAIN SCREECH (§7.6): streamers rise behind; wings only to BREATH; Spine ≥ −6 |
| Mouth anchor "fire breath" | **Ivonrath** fire breath (FIERCE_PLAN §7) | `Beak` anchor for a screech shock only |
| land absorb in the raised V | Thunderbird / Griffin V | hold LIFT4 (§7.5) |
| idle "predatory head tilt" | **Griffin** one-eye head cock | one look back over the shoulder at the owner, held (§7.1) |

Also not allowed anywhere: kinked or alternating zig-zag tips, white moon accents, violet, round eyes or spots, rings around the head other than the circlet, standing back blades, a glowing chest core gem, Neon, B.poly.

---------------------------------------------------------------------------------------------------------------------
## 2. Decisions

| item | decision | why |
|---|---|---|
| ground pose | **A, cloak fold** | §0.1. Tested on this kit; it keeps the walk clean; the icon pose stays compact. The silhouette difference from the Thunderbird comes from the posture, neck, crest, no fan, streamers and colour. |
| posture | **body axis 40° ± 2** from vertical (chest 40°, lower body 48°) | 35° risks the Thunderbird v1 costume read; 46° is the Thunderbird's own. The S-neck, not the lean, makes it proud. |
| streamers | **3**, C 1.40 / L-R 1.27, lanceolate vane + straight stepped tongue, BASALT → EMBER → LAVA → FLAME → HOT along the length | §0.2, §4.6 |
| tail fan | **none** | Thunderbird hero; it would collide with the streamer lifts; the streamers ARE the tail |
| crest | **5 plumes** from inside a **plain GOLD circlet**, rising 44-55°, curved stepped tongues EMBER → LAVA → FLAME → HOT, centre = model top | the hero must read at 64 px as a crowned flame. The circlet gives the secret's gold ring from the game camera (gold on the black hood) without crown points (Ivonrath). |
| gold anchor | **GOLD circlet + GOLD beak** (GOLD_D cere / mandible / circlet inner face). **No sun-disc, no gold feet** | the beak is the bird read at 64 px on a dark face; with the circlet it frames the head as the gold focal point. Gold feet are the Thunderbird's and Griffin's; the Phoenix gets scarlet EMBER tarsi. Target GOLD 3-6 % tq. |
| palette | **BLACKBODY**, §3 | the plan's ramp sits on three sibling accents; basalt was too dark |
| eye | Thunderbird eye: lid-heavy BLACK socket, FLAME iris, HOT spot, **no pupil** | a slit pupil reads "dragon"; the approved raptor eye is fierce at 64 px |
| act | **`act_rebirth` "ASHES TO FLAME"**, 104 f, tested wing path | §0.5, §7.7 |
| roar | **"FIRE-TRAIN SCREECH"**, 66 f | §7.6; the streamers are the one part no sibling has, so the roar shows them |
| HEIGHT | **10** | every 1-2 % secret is 10 (Rex, Orca, Mantis, Leviathan); Magma egg: Boar 6.6 / Golem 7 / Ivonrath 7.5 / Cerberus 8.5; Thunderbird 8.5 |

---------------------------------------------------------------------------------------------------------------------
## 3. PALETTE - "BLACKBODY" (decided)

**The idea:** a black-body heat ramp. The bird's crust is cool ash-basalt, its hide is vermilion, and every extremity gets hotter toward its tip (feathers, crest, streamers).
- The 3 bands = **BASALT** armour (hood, mantle, wing cloak) / **EMBER** hide (neck, breast sides, hackle cape, coverts, tarsi) / **PALE** molten underside (belly keel, an upward flame tongue on the breast).
- No sibling has a multi-step ramp; the Magma siblings use one accent each in seams, eyes or tips. **The Phoenix owns the FORM (a 4-step curved tongue on every fire part), not a hue.** In the amber band (37-45°) every fire pet's accent already sits, so a free hue does not exist.

### Palette (Blender values; in game ≈ ×0.6)
| role | RGB | hue / lum | in game | where | studs |
|---|---|---|---|---|---|
| **BASALT** | **(80, 70, 74)** | 336°, s 0.12, **lum 73** | (48,42,44) | hood (cranium top/back + face mask), dorsal saddles, mantle shingles, rump + shingles, arm bar outer, hand bar, secondary bodies, trousers, streamer seg 1, streamer knuckles | studded |
| BASALT_D | (54, 46, 52) | lum 49 | | primary bodies (contrast for the fire), brows, malar stripes, tarsus scale bands, trouser cuff alternates | studded |
| **EMBER** | **(232, 78, 32)** | 13.8°, s 0.86 | (139,47,19) | neck segs, hackle cape, breast + keel, lower-body flanks, flank skirt top row, cheeks / chin / throat, arm-bar shoulder patch, coverts + hand coverts, crest plume roots, secondary-tip first step, streamer seg 2, tarsi + toes | studded |
| **PALE** molten cream | **(248, 216, 160)** | 38°, s 0.35 | (149,130,96) | belly keel strip, the upward breast tongue (shingles), thigh-skirt inner edge only if needed | studded |
| LAVA | (255, 128, 24) | 27° | | ramp step 2: crest, primaries, secondary tongue points, streamer vanes, cape hem tips | smooth |
| FLAME | (255, 214, 72) | 45° | | ramp step 3: crest, primaries, streamer tongues; the eye iris | smooth |
| HOT | (255, 244, 210) | 45°, s 0.18 | | ramp points: crest tips, primary points, streamer points, eye hot spot | smooth |
| **GOLD** | (255, 196, 50) | house gold | (153,118,30) | circlet, upper beak, hook segment | smooth |
| GOLD_D | (214, 150, 30) | | | cere, mandible, circlet inner face, tomial tooth | smooth |
| BLACK | (14, 14, 22) | | | eye sockets, nostrils, hook tip, talons | smooth |
| MOUTH | (96, 26, 30) | | | gape plates (Thunderbird recipe) | smooth |

### Sibling check (nearest hues; full list in my temp run)
| mine | nearest | verdict |
|---|---|---|
| BASALT lum 73 | LavaGolem DARK 4°, Boar DARK, Cerberus COLLAR | the Magma dark family = intended. Darker than the siblings' rock (lum ~103), so it reads "black-feathered" next to grey rock. Passes the Orca rule (dominant dark lum ≥ ~65). |
| EMBER 13.8° | Ivonrath RED **13°**, Ivonrath BELLY copper 7° (s 0.61, far lighter), Boar MAGMA 9°, coral of Turtle / Hammerjaw (Water egg) | **Accepted risk.** The hide is a 16-24 % band on a black body, where Ivonrath is ≥ 60 % red. Gated by the Ivonrath A/B (checklist 5). If it fails, do NOT shift the hue; raise BASALT coverage (neck back, coverts) first. |
| LAVA 27° | Boar MAGMA 4° | allowed ONLY as a ramp step (never a seam, crack, stripe, spot or eye) |
| FLAME 45° | house GOLD 2-3°, SolarLion GOLD, Ivonrath FLAME 4° | ramp step only; the GOLD metal parts are separated from FLAME by an EMBER/LAVA step and by shape (circlet, beak) |
| PALE 38°, s 0.35 | SolarLion PALE 1° (its muzzle / underside) | a pale underside tone is shared family language, not an accent |

**Rules:**
- No role above 45 % in any view; BASALT alone ≤ 40 %.
- **No LAVA, FLAME or HOT outside a ramp** (feather tip, crest plume, streamer, hackle hem tip, eye).
- GOLD only on the circlet and beak.

### Share targets (flat palette-ID, idle f0 = fold pose; `headless_pack` + `pack_post`)
| role | side | tq | game | front |
|---|---|---|---|---|
| BASALT + BASALT_D | 32-42 | 26-36 | 38-48 | 18-30 |
| EMBER | 16-24 | 20-28 | 14-22 | 28-40 |
| PALE | 5-10 | 6-12 | ≤ 3 | 12-22 |
| FIRE (LAVA + FLAME + HOT) | 14-22 | 14-22 | 18-26 | ≥ 8 |
| GOLD + GOLD_D | 2.5-5 | 3-6 | ≥ 1.5 | 3-7 |

(The Thunderbird's measured game view was STORM+PRI 44 / bolts 16, so these are realistic for a cloak-folded bird.)

---------------------------------------------------------------------------------------------------------------------
## 4. GEOMETRY (model units: −Y forward, Z up, ground z 0; L = +x, R = −x; idle f0 = cloak fold)

### 4.1 Body stations (Thunderbird recipe, slimmer and 6° more upright)
| part | bone | geometry | colour |
|---|---|---|---|
| **Breast** | Chest | `B.add((0,-0.14,1.02), (0.22,0.21,0.27), rot=(40,0,0), bot=(0.60,0.55), top=(0.90,0.90), rnd=0.40)`. Top centre ≈ (0,−0.31,1.23), bottom centre ≈ (0,0.03,0.81). | EMBER |
| Keel bulge | Chest | `B.seg((0,-0.36,1.14),(0,-0.22,0.74), 0.14, 0.07, top=(0.55,0.8), ext=0.02, rnd=0.4)`. The breast is the most forward body mass. | EMBER |
| Dorsal saddle (chest back) | Chest | `chest.world((0,0.08,0))`, half (0.20,0.15,0.25), `R=chest.R`, same tapers (Thunderbird review 2 fix 2) | BASALT |
| **Lower body** | Spine | `B.add((0,0.08,0.70), (0.17,0.17,0.16), rot=(48,0,0), bot=(0.22,0.66), top=(0.92,0.90), rnd=0.38)`. Bottom ≈ z 0.48-0.50: **it swallows the knee (z 0.55)**. Chest:belly width 0.22:0.17 = 1.29, a deliberate step (Lessons #1). | EMBER |
| Dorsal saddle (lower back) | Spine | `low.world((0,0.06,0))`, half (0.155,0.12,0.15), `R=low.R` | BASALT |
| Rump | Spine | `B.add((0,0.30,0.60),(0.11,0.10,0.08), rot=(30,0,0), rnd=0.4)`; houses the streamer knuckles (§4.6) | BASALT |
| Rump shingles | Spine | 3 shingles over the knuckles at y 0.28-0.40, x (−0.06, 0, 0.06), size (0.055,0.02,0.08), laid back 60°, `bot=(0.2,1.0)`; EMBER flush edge bar on the bottom 25 % | BASALT |
| Belly strip (pale underside) | Spine | flush strip following the keel: `seg((0,-0.06,0.60),(0,0.20,0.52), 0.09, 0.03)`, ≤ 0.01 proud (Lessons #2 surface rule) | PALE |
| Breast tongue (pale) | Chest | `face_shingles` on the breast face, 4 rows (local z 0.16 / 0.05 / −0.06 / −0.17), xs as the Thunderbird. Colour by row: row 0 all EMBER; row 1 centre PALE, sides EMBER; row 2 centre 2 PALE; row 3 centre 3 PALE. That makes an **upward-pointing flame** rising from the belly. **No V bib pointing down** (that is the Thunderbird's white bib). | PALE / EMBER |
| Mantle | Chest / Spine | Thunderbird mantle rows (1 centre shingle at local z 0.18, then 4 and 3; lower back 3 and 2). Tonal, no seams. | BASALT |
| Flank skirt | Spine | top row: 2 spikes per side at x ±0.15, dy (−0.06, 0.04), z 0.72, dir (s·0.25,0.65,−0.72), L 0.18, w 0.05 (EMBER). Lower row: B.bar blades at **x0 ±0.225** (outside the trouser swing band: trouser x 0.14 + hw ≤ 0.08), z 0.63, dir (s·0.40,0.62,−0.68), L 0.15, width 0.10, thick 0.02 (BASALT) (Thunderbird review 3 lesson) | EMBER / BASALT |

**Side-view targets:**
- The line from breast-top to rump: **38-42°** from vertical.
- The belly line rises from the keel to the legs.
- No femur or knee shows.
- Visible leg (belly edge → ground) ≤ 0.51 = **≤ 25 %** of H_MODEL.

### 4.2 The S-neck (2 bones)
| seg | bone | geometry | note |
|---|---|---|---|
| Neck 1 | Neck | `B.seg((0,-0.24,1.12),(0,-0.43,1.38), 0.15, 0.15, ext=0.06)` | leans **35° forward**; bottom buried in the breast top |
| Neck 2 | Neck2 | `B.seg((0,-0.43,1.34),(0,-0.37,1.57), 0.13, 0.13, ext=0.03, ext1=0.03)` | leans **15° back**; its top meets the back of the head at mid-height (Lessons #4) |

- **The S read** (side): the throat is concave under the chin (Neck1 front ≈ y −0.57 at z 1.36 → Neck2 front ≈ −0.50 at z 1.50 → chin ≈ −0.58), and the nape is convex.
- Neck hw 0.13-0.15 ≥ 0.9 × head hw (0.13). Never thinner: a thin long neck is the ostrich / chicken read.
- Check the back view for a dark slot between Neck2 and the hood.
- **Hackle cape** (Thunderbird hackle-cape recipe, extended):
  - 4 rows of down-pointing shingles laid back 60-75° on the nape and neck sides: 2 rows on Neck2 (t 0.70 / 0.35), 2 rows on Neck (t 0.70 / 0.30). xs per row: 3 / 4 / 3 / 4. Size (0.06,0.02,0.09), `bot=(0.2,1.0)`.
  - Colour: EMBER. **Only the lowest row** gets a LAVA tip: the last 30 % as a separate smooth block, top 0.14. That gives a burning collar hem over the BASALT mantle from the game camera.
  - It is a cape lying on the surface, NOT standing blades (Black Dragon).

### 4.3 Head (falcon, built at final size; must be fierce at 64 px and from behind)
**HC (cranium centre) = (0, −0.47, 1.62).**

| part | bone | geometry (HC-relative unless absolute) | colour |
|---|---|---|---|
| Cranium (hood) | Head | `B.add(HC, (0.13,0.125,0.115), top=(0.85,0.85))`; top ≈ z **1.735** | BASALT |
| Face block | Head | HC + (0,−0.10,−0.045), half (0.10,0.06,0.075), top (0.9,1) | BASALT |
| Cheeks / chin / throat | Head | HC + (0,−0.03,−0.075), half (0.118,0.10,0.055), rnd 0.35. It overlaps the cranium bottom, so the lower head is EMBER and the hood is BASALT (falcon hood). | EMBER |
| Malar stripe ("tear mark") | Head | flush bar per side from HC + (s·0.100,−0.13,−0.01) to HC + (s·0.112,−0.08,−0.10), width 0.03, ≤ 0.01 proud, seated with `surf_hit` on the EMBER cheek | BASALT_D |
| **Eye** | Head | Thunderbird `eye()` at HC + (s·0.098,−0.128,0.024), **sc 1.15**, yaw 26: lid-heavy BLACK socket, **FLAME** iris, HOT spot on the outer half, **no pupil** | BLACK / FLAME / HOT |
| Brow (fused V) | Head | HC + (s·0.078,−0.088,0.070), half (0.082,0.038,0.031), rot (0,−s·21,s·22), **top=(0.8,0.85)** (front taper, Thunderbird review 3 fix 3), ≥ 50 % buried, overhang ≤ 0.025, the pair meeting in a V over the cere | BASALT_D |
| Cere | Head | HC + (0,−0.155,−0.015), half (0.068,0.034,0.036), top (0.85,1); nostrils = BLACK (0.004,0.011,0.008) at HC + (±0.07,−0.163,−0.005) | GOLD_D |
| Upper bill | Head | `seg(HC+(0,-0.15,-0.012), HC+(0,-0.28,-0.036), 0.064, 0.056, top=(0.6,0.6))` | GOLD |
| Hook segment | Head | `seg(HC+(0,-0.255,-0.006), HC+(0,-0.325,-0.050), 0.038, 0.044, top=(0.8,0.8))` | GOLD |
| Hook tip | Head | `spike(HC+(0,-0.32,-0.046), (0,-0.55,-1), 0.075, 0.032)` (continues the curve; not an icicle) | BLACK |
| Tomial tooth (falcon) | Head | small spike per side at HC + (s·0.052,−0.255,−0.058), dir (0,0,−1), L 0.028, w 0.020 | GOLD_D |
| Mandible | **Jaw** | `seg(HC+(0,-0.15,-0.088), HC+(0,-0.27,-0.088), 0.050, 0.020, top=(0.7,1))`. Modelled **closed**: key = total angle. | GOLD_D |
| Gape | Head / Jaw | MOUTH roof plate (Head) + floor plate (Jaw) + gape lines (Thunderbird L253-256) | MOUTH |

- Beak tip ≈ HC + (0,−0.345,−0.105) = (0,−0.815,1.515).
- Head length incl. beak ≈ 0.47 (Thunderbird 0.51): a compact falcon head. **Its front must be ≥ 0.10 ahead of the breast front** (anti-stack, Thunderbird v1 lesson e).
- **64 px:** a black hood, a gold hook, a fire-yellow eye slit, red cheeks, and the gold ring plus fire plumes on top.
- **Game camera:** black hood, the gold ring all round, the plumes, and the EMBER cape with its LAVA hem.

### 4.4 Gold circlet (the secret's gold ring)
- A **closed band** hugging the crown behind the brow:
  - front bar at y −0.53 (x ±0.10)
  - back bar at y −0.37 (x ±0.10)
  - side bars at x ±0.118 (y −0.37…−0.53)
  - small corner blocks
- All at z 1.69-1.74. Section 0.03 radial × 0.05 tall. Seat every bar with `surf_hit`, ≤ 0.01 proud.
- GOLD outside, GOLD_D inner face.
- **No points, no gem** (Ivonrath's crown has 3 points; the Leviathan / Rex / Orca crowns have points). The flames are the points.
- Bone: Head (static).

### 4.5 HERO 1 - the FLAME CREST (5 plumes, Crest bone)
- Roots sit on the crown top **inside the circlet's back half**.
- Every plume is a diamond-section leaf with **width : thickness ≈ 2 : 1**.
- Its broad face normal is ⟂ to the plume direction, in the plane of the direction and x. So the centre plume shows its face to the side view, and the splayed ones turn partly toward the front and the game camera.

| plume | root | direction (unit, before the curl) | length | root width (full) | tip ≈ |
|---|---|---|---|---|---|
| C (tallest) | (0, −0.44, 1.725) | (0, 0.57, 0.82), rise 55° | 0.44 | 0.10 | (0, −0.19, 2.07) |
| inner L/R | (±0.045, −0.45, 1.725) | (±0.20, 0.60, 0.77), rise 50°, splay 18° | 0.37 | 0.09 | (±0.12, −0.23, 2.01) |
| outer L/R | (±0.085, −0.43, 1.72) | (±0.38, 0.62, 0.69), rise 44°, splay 31° | 0.29 | 0.08 | (±0.20, −0.25, 1.92) |

**Each plume = 4 stepped blocks, a curved tongue (all smooth / nostud):**

| step | span of the length | width (× root) | colour | curl vs the previous step |
|---|---|---|---|---|
| 1 | 0-32 % | 1.0 → 0.9 | EMBER | - |
| 2 | 32-60 % | 0.9 → 0.75 | LAVA | +11° backward |
| 3 | 60-84 % | 0.75 → 0.5 | FLAME | +11° |
| 4 | 84-100 % | 0.5 → point (top 0.14) | HOT | +11° |

- The curl is about the plume's broad-face normal, toward +y (back). **Every plume curls the same way**: flames licking back.
- Overlap the steps by 0.006. No sideways jog (that is the Thunderbird bolt).
- Vary lengths as given (±15 %).
- **H_MODEL = 2.05 ± 0.04**, measured on the C tip after the curl, at idle f0. The crest is the model top in the bind pose AND at idle f0 (check the bind-pose wingtips stay below it).
- 64 px: about a 10 × 9 px flame fan on a 1-2 px gold ring.
- From the front: 5 tongues fanning to ±0.20 above a head of hw 0.13, a flame crown.
- From the side: plumes swept up and back over the nape.
- **Never** a radial corona: no plume below 40° rise, none pointing forward or sideways.
- Bone `Crest`: pivot (0,−0.43,1.72), parent Head. **Kit sign: Crest +pitch = ERECT** (rears the plumes up and forward); −pitch = laid back. Anchor `CrestTip` = the C tip (child of Crest).

### 4.6 HERO 2 - the STREAMERS (3 chains × 3 bones, under the empty `Tail` bone)
**Envelope I measured** (Thunderbird FOLD, wing verts behind y 0.2): the folded wing never comes inside |x| 0.23 and never below z 0.33.
- On the Phoenix (wing Δx −0.05, Δz +0.06, §4.7) expect |x| ≥ 0.18 and z ≥ 0.39.
- At LIFT2 / BREATH the wing stays at |x| ≥ 0.37 (Phoenix ≈ 0.32).
- So the streamers live **low (z ≤ 0.33 after y 0.6) and narrow (|x| ≤ 0.30)**.

**Knuckles (narrow roots, the Orca / Mantis lesson):**
- Each streamer starts in a round BASALT knuckle, half (0.045,0.05,0.045), rnd 0.45, on its own X1 bone with its pivot at the knuckle centre. It rotates in place, so it never sweeps out of the rump.
- Knuckle centres:
  - C (0, 0.38, 0.60)
  - L (0.075, 0.37, 0.53) and R (−0.075, 0.37, 0.53)
  - spacing 0.10, so the knuckles clear each other by 0.01
- Each seg-1 shaft starts inside its own knuckle (same X1 bone, so the overlap is legal) and must leave the rump
  (Spine) surface within 0.03. Nothing on an X1 bone may sit deeper than 0.03 inside a Spine block except the round
  knuckle itself.

**Rest curves (side: back-and-down, a long low glide, the vane lifting ≤ 20°):**

| chain | seg 1 (X1) BASALT | seg 2 (X2) EMBER | seg 3 (X3) vane LAVA | tongue (X3) FLAME → HOT | total |
|---|---|---|---|---|---|
| C | (0,0.40,0.58) → (0,0.78,0.31), hw 0.05, hd 0.04 | → (0,1.12,0.135), hw 0.046, hd 0.036 | → (0,1.48,0.20) | → tip (0,1.64,0.27) | 1.40 |
| L (R mirrored) | (0.08,0.39,0.51) → (0.12,0.72,0.27) | → (0.20,1.03,0.14) | → (0.27,1.33,0.21) | → tip (0.30,1.46,0.28) | 1.27 |

**The vane:**
- Lanceolate, built from 2 blocks: widening from w 0.12 to **0.20 at 45 %**, then narrowing to 0.13. Diamond section, half-thickness 0.05 (w : t ≈ 2 : 1), so it reads from the side AND from above.
- **Length ≥ 3.5 × its max width.** Never round, never diamond-short.

**The tongue:**
- FLAME block (0.6 of the tongue length, w 0.12 → 0.07), then a HOT point (top 0.14).
- **Collinear, no curl**: a raised streamer must never form a hook.

**Lowest points (at rest, bottom surface):** C trough ≥ **0.10**, L/R ≥ 0.10. Vanes rise to the tip.

**Rest clearances:**
- folded wing → streamers ≥ **0.06** (pairs below)
- folded primaries end ≥ 0.15 above the vanes
- side streamers behind the legs (the hallux never reaches y > 0.25 in the walk)

**Bones:**
- `Tail` (empty, pivot (0,0.36,0.56), parent Spine): lifts / yaws all three.
- `StreamerC1/C2/C3`, `StreamerL1/L2/L3`, `StreamerR1/R2/R3`. Pivots: X1 = knuckle centre, X2 = seg1 end, X3 = seg2 end.
- Anchors `StreamerEnd_C/L/R` at the tongue tips (children of X3).

**Kit sign: +pitch LIFTS the streamers**; yaw + swings rear parts toward −x (the pet's right). So "fan out" = L yaw −, R yaw +.

### 4.7 Wings (wing3, Thunderbird `wing()` adapted)
**Geometry:** the Thunderbird points shifted by **Δ = (−0.05, −0.02, +0.06)** (x mirrored per side), so the root sits on the slimmer, higher shoulder (S.x = chest hw, the Thunderbird rule).
- `_S0 = (0.22, -0.12, 1.22)`, `_BB0 = (0.19, 0.20, 1.04)`
- pre-raise: W (0.88, −0.06, 1.38), H2 (0.74, 0.60, 1.18), TIP (1.74, 0.28, 1.48)
- **ELEV 16**, `_ROT` as Thunderbird. Span ≈ 3.5 open, the same class as the Thunderbird. The plan's 2.2 would make it smaller than the 5 % bird.
- **No shoulder blocks** (Thunderbird review 2: they block the fold).

**Feathers (counts and sizes as Thunderbird L126-165; colours and tips new):**

| row | count, bone | body | tip (curved tongue, `tongue()` below) |
|---|---|---|---|
| arm bar | Wing | EMBER S→38 % (shoulder patch) · BASALT 38 %→W · BASALT wrist knuckle | - |
| hand bar | WingTip | BASALT | - |
| secondaries | 7, Wing | BASALT, width 0.27 | tipf 0.22: EMBER band (55 %) → LAVA point (45 %), curl +10° toward the trailing edge |
| inner coverts | 6, Wing | EMBER, width 0.22 | none |
| inner primaries | 3, Wing | BASALT_D, width 0.25 | tipf 0.42: LAVA (30 %) → FLAME (40 %, +12°) → HOT point (30 %, +12°) |
| outer primaries | 5, WingTip | BASALT_D, width 0.23 | same as the inner primaries; the 3rd one carries anchor `WingFire_L/R` |
| hand coverts | 4, WingTip | EMBER, width 0.20 | none |

**`tongue()` replaces `bolt()`:**
- Consecutive stepped blocks in the feather plane (`frame(dir, nrm)`).
- Widths 0.82w → 0.62w → 0.34w → point (top 0.14). 0.006 overlaps.
- **Each step is rotated by `curl` about `nrm`, toward the trailing edge.**
- **The same sign on every feather of one wing** (mirrored L/R), and **no lateral jog**. This is the flowing flame, not the alternating Z bolt.
- Bodies studded; tongue steps smooth.

**Fold read:**
- At FOLD the cloak shows its under-layer outward: a black cloak with an ember-lava hem (secondaries) and fire-tipped primaries trailing above the streamers.
- In flight and the act, the upper side shows: red shoulders and coverts, black wing, fire edge.

**Waypoints (start values = the Thunderbird's tested ones):** FOLD (86,10,−80,0), LIFT1 (84,16,−80,−15), LIFT2 (70,24,−55,0), LIFT3 (50,20,−25,10), LIFT4 (35,8,−8,10), BREATH (80,26,−65,−10), OPEN (30,0,0,0), BOT (−38,8,6,4), BRAKE (24,16,−10,−4), plus the act's PYRE family (§7.7).

**After the model is built, re-run (required):**
1. `fold_search.py` with `FOLD_GRID="76,82,86,90,96;0,6,10,16;-70,-80,-90;-15,0,10"` and `FOLD_TAIL` = the C vane start.
   - Acceptance: 0 hits (incl. Chest / Spine / Neck / Neck2 / every Streamer), **half-width 90 % ≤ 0.48**, wing min z ≥ 0.30, primaries end above the streamers (never below), wingtip → C-vane-start distance ≤ 0.45.
2. `path_test.py` on all 8 Thunderbird review 2 paths, the act path (§7.7) and the roar wing path (FOLD→LIFT1→LIFT2→BREATH→LIFT1→FOLD).

### 4.8 Legs
| joint | Thunderbird | **Phoenix** | why |
|---|---|---|---|
| HIP | (0.14, 0.12, 0.62) | **(0.12, 0.10, 0.68)** | narrower body, higher belly |
| KNEE | (0.16, −0.04, 0.50) | **(0.14, −0.06, 0.55)** | inside the lower body (bottom ≈ 0.48-0.50) |
| ANKLE | (0.16, 0.07, 0.22) | **(0.14, 0.06, 0.27)** | tarsus 0.26 vs 0.22: slender, still ≤ 25 % visible leg |
| TOE | (0.16, −0.05, 0.035) | **(0.14, −0.06, 0.035)** | |

- **Leg_:** hidden thigh block only (EMBER).
- **Shin_ (trousers):**
  - BASALT, hw 0.065 at the knee flaring to 0.08 at the cuff, rnd 0.45.
  - Mirrored 7-spike ragged cuff (Thunderbird L287-292), L 0.11-0.14, alternating BASALT / BASALT_D. No EMBER on the cuff, so the scarlet tarsus emerges cleanly.
  - Front view: the trouser outer edge stays inside the belly silhouette (≤ x 0.21).
- **Foot_ (bare tarsus):**
  - **EMBER**, hw 0.052, with 3 BASALT_D scale bands.
  - Toes EMBER: L 0.10, hw 0.026, outer toes splayed 18°.
  - Talons BLACK, 2-part hooks; **hallux talon 0.11** (the biggest).
  - `FOOT_LIFT` 0.014 (Thunderbird review 3 ground fix: start 0.001 higher).
- `add_leg2(..., knee=(0,−1,0))`.

### 4.9 Size, H_MODEL, PITCH
- **H_MODEL 2.05** (C plume tip, idle f0) · head top 1.735 · shoulders ≈ 1.30.
- Bounds at idle f0 ≈ 2.45 long (beak −0.815 → C tip 1.64) × ~0.96 wide (fold) × 2.05 tall. L:H ≈ 1.2 (Thunderbird 1.24).
- **HEIGHT 10** → `PITCH = round(0.042 * (2.05/10) / (1.498/8.0), 4) ≈ 0.0460`.
- In game at ×1: 10 studs tall, ~12 long, span ~17 open.
  - It stands over its whole egg (Cerberus 8.5, Ivonrath 7.5) and the 5 % Thunderbird (8.5).
  - It matches the other secrets.
- **Tris:** target ≤ 12k (cap 15k). Expect ≈ 11k: no tail fan (−27 blocks); crest 20 blocks (Thunderbird 28); streamers 21; +2 blocks per primary / +1 per secondary.
- If over: cut secondaries 7 → 6, hackle rows 4 → 3, cuff spikes 7 → 5, in that order.

---------------------------------------------------------------------------------------------------------------------
## 5. Rig, anchors, pairs, capsules

### 5.1 Bones (joint positions at rest)
| bone | pivot | parent | note |
|---|---|---|---|
| Spine | (0, 0.10, 0.70) | Root | tail=(0,−0.2,0.35) |
| Chest | (0, −0.04, 0.92) | Spine | |
| Neck | (0, −0.24, 1.14) | Chest | |
| Neck2 | (0, −0.43, 1.36) | Neck | |
| Head | (0, −0.39, 1.52) = HC + (0,0.08,−0.10) | Neck2 | throat pivot |
| Jaw | (0, −0.59, 1.545) = HC + (0,−0.12,−0.075) | Head | |
| Crest | (0, −0.43, 1.72) | Head | geometry rides on it |
| Wing_L/R, WingTip_L/R | WING.S / WING.W | Chest / Wing | as Thunderbird |
| Leg_, Shin_, Foot_ L/R | HIP / KNEE / ANKLE | Spine | `add_leg2` |
| Tail | (0, 0.36, 0.56) | Spine | empty parent of the 3 X1 |
| StreamerC1/L1/R1 | knuckle centres (§4.6) | Tail | |
| StreamerC2/L2/R2, C3/L3/R3 | seg ends | X1 / X2 | |

**Anchors (empty bones; VFX only, no mesh, no glow):**

| anchor | parent | position |
|---|---|---|
| `CrestTip` | Crest | C tip |
| `Beak` | Head | HC + (0,−0.34,−0.09) |
| `Core` | Chest | (0,−0.30,1.00), inside the breast at the top of the pale tongue |
| `WingFire_L/R` | WingTip | 3rd outer primary tip |
| `StreamerEnd_C/L/R` | X3 | tongue tips |
| `Pyre` | Root | (0, 0.05, 0.02) |

### 5.2 `check_pairs()`
- **Thunderbird list**: every Wing / WingTip vs Head, Neck, Leg_/Shin_/Foot_ L/R, Chest, Spine, plus wing-vs-wing. Add **Neck2** and **Crest** to the wing targets, and replace Tail1 / Tail2 with all 9 streamer bones.
- (Leg_L, Leg_R), (Shin_L, Shin_R), (Foot_L, Foot_R), (Shin_L, Spine), (Shin_R, Spine).
- (Head, Chest), (Jaw, Chest), (Jaw, Neck), (Head, Neck), (Crest, Neck), (Crest, Neck2), (Crest, Chest).
- **Streamers:**
  - every L-chain bone vs every C-chain bone; C vs R; L vs R
  - each X1/X2/X3 vs Shin_L/R and Foot_L/R
  - each X1 vs Spine (root sweep)

### 5.3 `joints()` capsules
- `WING.joints()` + (S, BB, 0.12, Wing_*), as Thunderbird.
- **Knee:** (K − d·0.08) → (K + d·0.15), r **0.10**, Shin_* (Thunderbird review 3 tight version, thinner trousers).
- **Neck → Neck2:** ((0,−0.36,1.36), (0,−0.50,1.36), 0.15, "Neck2").
- **Throat:** ((0,−0.33,1.52), (0,−0.55,1.52), 0.15, "Head"). It stops below the crest roots, so the crest still counts.
- **Crest root:** ((0,−0.47,1.72), (0,−0.40,1.72), 0.06, "Crest").
- **Jaw hinge:** ((−0.08,−0.59,1.545), (0.08,−0.59,1.545), 0.04, "Jaw").
- **Streamer roots:** per chain (knuckle − dir·0.03) → (knuckle + dir·0.06), r 0.07, X1.
- **Streamer mid-joints:** (J − d·0.03) → (J + d·0.04), r 0.055, X2 / X3.

### 5.4 Limits (kit signs: + pitch = nose DOWN for forward bones, LIFTS rear bones and the crest; yaw + = toward the pet's left for the head)
| joint | limit |
|---|---|
| Head + Neck + Neck2 pitch up | **≤ 14° net** in roar / act (never chin-to-sky = Raiju's howl); hard limit 30 |
| pitch down | ≤ 20 in general; **≤ 44 total** only for the act's pyre bow, with (Head/Jaw, Chest) clean |
| yaw | Neck ±8, Neck2 ±12, Head ±24 (total ±44); ≤ 30° per 6 f; no reversal faster than 6 f (no shakes) |
| Chest vs Spine | ≤ ±5° |
| Crest | +16 erect / −10 laid back |
| Jaw | ≤ 34 |
| Streamer X1 | +56 lift / −24 drop, yaw ±12 |
| Streamer X2 / X3 | ±30 / ±25, yaw ±10 |
| Spine pitch | −6 … +10 on the ground (no rear-up); FPITCH in flight (§7.3) |
| Spine z | −0.14 … +0.46 (act only) |
| Wings | ONLY the waypoint family, stroke poses and the act's PYRE family; **never RAISED_V on the ground** (Griffin / Thunderbird) |

**Run the ground lift pass in every clip; ground ≥ −0.02 on EVERY frame** (sample every frame, not every 2nd: Thunderbird review 3 caught −0.0203 at walk f26).

---------------------------------------------------------------------------------------------------------------------
## 6. Jackpot factors (what makes it a 2 % pull)
1. **One owned fire language:** the curved stepped tongue (EMBER → LAVA → FLAME → HOT) on crest plumes, primaries, streamers and the cape hem. Repetition makes it read "designed", not "decorated" (Leviathan lesson).
2. **The crowned flame:** a gold ring on a black hood with 5 fire plumes rising from it. The tallest point of the pet, and it reads from the game camera.
3. **The richest tail in the game:** 3 burning plumes trailing behind, and the only pet whose roar raises its tail into a fire train facing the follow camera.
4. **A moving hero in the idle:** streamer licks (L, C, R), a crest flare and ember events every loop, so it is never a statue behind the player.
5. **Material contrast:** studded basalt, ember and cream against smooth glassy fire and polished gold.
6. **Size tier:** HEIGHT 10.
7. **Index portrait:** idle f0 (cloak fold). The crest sits top-left, and the streamers balance bottom-right. Do not use a raised-wing icon pose.

---------------------------------------------------------------------------------------------------------------------
## 7. CLIPS (30 fps; references BEFORE keying, owner rule)

**References to pull from animationreference.org** (cite in `ANIM_REFERENCES_1014.md`; already-logged ones are free to reuse):
- #5 *Bird Flight - Flapping* (logged): fly, takeoff, land.
- #3 *Sea Beasts* roar (logged): the jaw lags the head lift by 3-4 f.
- #6 *Monsters University* deimatic pop (logged): roar train-rise timing, crouch → spread in 5-7 f.
- #7 *HTTYD* cautious approach (logged): the look-back hold.
- **NEW:**
  - a large bird taking off from standing (`/tags/flying`) for the act's rise
  - a heavy creature collapsing or slumping (`/tags/creature-animation`) for the pyre
  - a tail-raise display, peacock or turkey if available, for the train rattle

**General rules:**
- Every ground clip starts and ends at FOLD; every fold↔open change runs LIFT1→LIFT4 in order.
- Head gyro in walk and fly: cancel ≥ 70 %, spread Neck 0.2 / Neck2 0.25 / Head 0.3.
- **Streamer motion is always a travelling wave:** X1 → X2 → X3 lag 2-3 f in the ground clips, 0.08-0.10 cycle in the loops. L / C / R never move in unison (phase offsets).
- Any swing > 60° in one frame gets an in-between.
- 0 collisions at step 1; linear 0; loops closed.

### 7.1 idle (120 f loop) - "SMOULDER"
| f | beat | keys | event |
|---|---|---|---|
| 0-120 | bellows breath (2 cycles) | Spine z +0.008 and Chest −1.5 at inhale peaks f22 / f82; Crest +4 on each inhale; Neck2 / Head counter so the head stays level | `ember` f24, f84 (CrestTip + back) |
| 0-120 | streamer drift | X1/X2/X3 pitch ±1.5/±3/±5 and X3 yaw ±3, lag 0.08 cycle per segment, 2 cycles; phases L 0 / C 0.33 / R 0.66 | |
| 10-22 | proud rise | Neck −4, Neck2 −4, Head +7: the S straightens, the head stays level and rises ~0.03; hold to f38 | |
| 18-34 | **lick L** | StreamerL2 +8, L3 +18 over f18→23 (the tip licks up); fall over 7 f with a −4 overshoot (f30); 0 by f34 | `lick` f23 (StreamerEnd_L) |
| 38-46 | **look back** | over the LEFT shoulder toward the follow camera: Neck yaw +8, Neck2 +12, Head +24 (44°) over 8 f | |
| 46-64 | hold | dead still for 18 f; the fire eye faces the game camera | |
| 48-64 | lick C | StreamerC2 +8, C3 +18 (same shape) | `lick` f53 |
| 64-74 | return | yaw to 0 over 10 f; hold f74-82 | |
| 78-94 | lick R | StreamerR2 +8, R3 +18 | `lick` f83 |
| 84-100 | **crest flare + glare** | Crest +12 (erect) at f88, hold to f94, back by f100; Head +6 (chin down, glaring forward); Jaw +4 (a crack of gape) f88-96 | `flare` f88 |
| 92-104 | heat lift | wings `blend(FOLD, LIFT1, 0.5)` at f98, back to FOLD at f104 (on the tested FOLD↔LIFT1 path) | |
| 56-62 | talon re-grip | Leg_R lifts 0.03, toes curl (Thunderbird `regrip`) | |
| 104-120 | settle | exact rest at f120 | |

Not in this idle: no L-R scanning (Raiju core beat), no hunting stare (Thunderbird), no head cock (Griffin), no preen (ForestStag owns grooming), no wing breath to BREATH (Thunderbird).

### 7.2 walk (28 f loop) - "STALKING STRUT"
- Thunderbird `walk()` machinery (approved): `cm.biped_walk` n 28, stride half 0.15, **lift 0.10**, duty 0.6, rolling strut (roll 4, yaw 3), asymmetric contact dip −0.04, swing foot +0.025 wide, toes curled 22, gyro head.
- Wings: FOLD with a 0-15 % LIFT1 blend on contacts.
- **Streamers:**
  - X1 baseline **+3** (ground clearance through the dip)
  - yaw follows the body yaw ×0.5 / ×1.0 / ×1.5 lagging 3 / 6 / 9 f
  - pitch ±2 / ±3 / ±4 twice per cycle, lagging the contact dip by 3 / 5 / 7 f
- **Crest:** follow-through +2 lagging the contact dip by 3 f.
- Ground: the streamer troughs ≥ −0.02 on every frame (dip 0.04 + roll 4° at x 0.2 + pitch ≈ −0.08 from 0.10).

### 7.3 fly (32 f loop) - "BURNING WAKE"
- **Wings:** `wing3.stroke(ph, top=34, bot=-40, down=0.45, sweep=10, twist=10, fold=36)`. Slightly slower than the Thunderbird (28 f) for a heavier, regal beat. The body rises 0.07 on the downstroke.
- **FPITCH 44-46:** tune so the breast-to-rump line is horizontal ±5°. Neck ≈ −8, Neck2 ≈ −8, Head ≈ −28: tune so the beak points forward and the head is level ±2.
- **Legs:** tucked, balled talons under the streamer roots (THI 76, SHI −40, FOO 76).
- **Streamers:**
  - X1 −22, so they trail 10-15° below the body line (the +46 body pitch lifts them)
  - travelling S-wave X1/X2/X3 ±5/±9/±13, lag 0.10 cycle per segment, X1 peaking 0.15 cycle after the downstroke start
  - fan L yaw −8 / R yaw +8 (a forked trail), X3 lateral ±3 offset 0.25
- **Crest:** −6 (laid back by the airflow) ±2 with the stroke.
- It is the only flyer that trails a 3-plume fire wake. The anchors (`WingFire`, `StreamerEnd`) carry ribbon trails (§8).

### 7.4 takeoff (30 f)
- **Wings and body:** exactly the Thunderbird keys. FOLD→LIFT1 (f3) → LIFT2 (f6) → LIFT3 (f8) → LIFT4 (f9) → OPEN (f10), crouch −0.12, LAUNCH downbeat at f11 (event `launch`), legs push then tuck, `fly_pose` from f23.
- **Streamers DRAG:**
  - X1 −4 at the crouch (f3-10)
  - at the launch they hang: X1 −18, X2 −8, X3 −4, lagging 2 f (f13-16)
  - they swing back into the flight trail by f23, overshooting +6 at f21
- **Crest:** +8 at f10.
- `lift_air_frames(13..30)`; check the hanging streamers on the ground (ground ≥ −0.02).

### 7.5 land (32 f)
- **Thunderbird keys** to f15: flare, brake (24,16,−10,−4), legs reach, talons thrown forward.
- **Streamers FLARE** on the brake (the tail fans to brake, ref #5): X1 +20, X2 +10, X3 +6 at f6-15.
- **TOUCH f17** (event `touch`): wings at **LIFT4, not the raised V**. Hold LIFT4 f17-22 → LIFT3 f24 → LIFT2 f26 → LIFT1 f28 → FOLD f31. That is the tested "brake → LIFT4 … FOLD" path (Thunderbird review 1, path 2).
- **Streamers swing down** with the momentum: overshoot −6 at f20, then settle by f30. The vanes must not dip below −0.02.

### 7.6 roar (66 f) - "FIRE-TRAIN SCREECH" (replaces rear-up + V)
| f | beat | keys | event |
|---|---|---|---|
| 0-10 | gather | Spine z −0.04, pitch +4; Neck +6, Neck2 +4, Head +4 (head pulls in, eyes on the camera); wings FOLD → LIFT1 (f5) → LIFT2 (f10); streamers sag X1 −4 (anticipation) | |
| 10-20 | **TRAIN RISE** | wings LIFT2 → **BREATH** (f16), hold (wings lifted off the body = a smouldering cloak, **never the V**); streamers X1 −4 → **+56** (f17), X2 **+24** (f19), X3 **−14** (f20): 2 f lag per segment, ease-out; NO extra fan (the rest splay is enough; extra yaw drives the side vanes into the wings); Crest **+14** erect (f18); Spine pitch −4, z 0 | |
| 20-24 | thrust | Neck +8, Neck2 −6, Head −6: the head goes forward, 4° chin-up net (≤ 12) | |
| 23-27 | **SCREECH** | Jaw 0 → 34 at f26, starting 3 f after the head (Sea Beasts lag) | `screech` f25 (Beak shock + CrestTip / StreamerEnd flares) |
| 27-46 | hold + **TRAIN RATTLE** | jaw buzz 34 ± 2 every 3 f (the head stays still); streamers shiver X2 ±3 / X3 ±5 on a 4-f period, L / C / R offset 1 f; crest holds; wings hold BREATH | `rattle` f30 |
| 46-56 | release | jaw 34 → 0 by f52; streamers fall to X1 −6 at f54 (overshoot), 2 f lag down the chain; wings BREATH → LIFT1 (f52) → FOLD (f56); Crest relaxes f50 | |
| 56-66 | settle | streamers rebound +3 (f59) → 0 (f62); exact rest at f66 | |

**Targets at f20 (C chain):**
- seg1 ≈ +22° above horizontal, seg2 ≈ +52°, vane **75-85°**: never past vertical, never curling forward.
- C vane top z **1.45-1.62**, y ≥ 0.95 (behind the hips).
- Side vanes |x| ≤ 0.30, and ≥ 0.05 clear of the wings at BREATH. The measured wing inner edge is 0.37 on the Thunderbird, ≈ 0.32 expected here, so **keep the side chains at |x| ≤ 0.24 below z 1.35**.

**From the game camera** (camera-up ∝ −0.65y + 0.76z), the raised plumes stand as three fire tongues low behind the bird, faces toward the camera, framing it. The head and crest stay above them in screen space.

Not in this roar: no rear-up (Spine ≥ −6), no raised V, no chin-to-sky, no breath, no forward tail arc, no head motion during the buzz. Root y within ±0.03.

### 7.7 act_rebirth (104 f) - "ASHES TO FLAME" (signature)
**The story:**
1. The crest ignites, and the phoenix opens its wings and lets them sink into a burning pyre around it; its head bows, the plumes lie down, and it goes still.
2. Two heartbeats.
3. The head wakes first. Then one huge sweep and two beats lift it off the ground into the heraldic "phoenix rising" frame with a screech.
4. It lands and folds.

**Why it is unique:**
- The open, low, back-swept droop is a new wing shape. It is NOT the Griffin's tent: that one is swept FORWARD over prey, with the head glaring between the wings.
- It is NOT Cvetibara's bud: nothing wraps or closes; the wings never cross in front of the chest.
- The **heartbeat** and an **airborne rebirth** belong to no one.
- No stoop or dive (Thunderbird); no spin; no breath.

| f | beat | keys (deg; Spine loc in model units) | event |
|---|---|---|---|
| 0-10 | **IGNITE** | Crest +14 by f8; Neck −4, Neck2 −2, Head +6 (the neck straightens, head level); Spine z −0.02; wings FOLD → LIFT1 (f4) → LIFT2 (f8); streamers +8 | `ignite` f8 (CrestTip + Core flare) |
| 10-26 | **PYRE** | wings LIFT3 (f10) → LIFT4 (f11) → OPEN (f13) → (−20,−10,4,−6) (f17) → (−45,−15,6,−8) (f21) → **PYRE (−60,−22,10,−6)** (f26); Spine z → **−0.13**, pitch +9 (f26); **bow**: Neck +12, Neck2 +12, Head +20 (beak to the breast); Crest −10 (laid back: the fire dies); streamers settle ONTO the ground (X1 ≈ −6, X2 −4, X3 −2, tuned so the troughs sit at z 0.02-0.05) | `pyre` f20 (fire ring at Pyre, flames along the wings) |
| 26-34 | **EMBER SLEEP** | dead still: no breath, nothing moves | `ash` f30 (flames out → smoke, dim embers) |
| 34-46 | **HEARTBEAT ×2** | f36: Chest −3 and Spine z +0.012 in 2 f, back in 4 f, Crest +4 flicker, X3 +5 twitch. f42: Chest −5, z +0.018, Crest +8, X3 +8 | `heartbeat1` f36, `heartbeat2` f42 (Core pulse) |
| 46-50 | **AWAKEN** | the head snaps up FIRST: Neck +12 → −4, Neck2 +12 → −4, Head +20 → −6 (f46 → 50; ≤ 25° per 2 f); Crest +16 (f49); wings still PYRE | |
| 50-54 | wind-up | wings PYRE → (−45,−15,6,−8) f51 → (−20,−10,4,−6) f52 → OPEN f54; Spine z −0.14, pitch +4; streamers +10 | |
| 54 | **LAUNCH** | the downbeat starts | `rebirth` f54 (Core burst + Pyre shock ring) |
| 54-58 | beat 1 | OPEN → BOT (−38,8,6,4) f58; Spine z +0.14, pitch −2; legs push, then FK (24,−10,40) f58; streamers drag down (X1 −16, 2 f lag) | |
| 58-64 | up-stroke | BOT → OPEN f64; z 0.30; streamers whip up (X1 +6, X2 +14, X3 +18, 2 f lag) | |
| 64-68 | beat 2 | OPEN → BOT f68; z 0.44; legs (50,−30,66) | |
| 68-76 | **PHOENIX RISING** | BOT → OPEN f72, hold to f76; z **0.46**; body upright (pitch −4); Neck −6, Neck2 −4, Head −4 (≤ 14° up); Jaw 0 → 30 at f72 with a ±2 buzz; streamers hang straight down and swing (X1 −24, X2 −6, X3 +4) | `reborn` f72 (screech + CrestTip / WingFire / StreamerEnd flares) |
| 76-82 | descend + brake | OPEN → BRAKE (24,16,−10,−4) f80; z 0.16 at f80; jaw shut by f80; legs reach (−14,6,−20); streamers flare up (+16) | |
| 82 | **TOUCH** | wings LIFT4; Spine z −0.05 (absorb) | `touch` f82 |
| 82-92 | fold | LIFT4 → LIFT3 (f85) → LIFT2 (f87) → LIFT1 (f89) → FOLD (f92); streamers overshoot −4 (f86) → settle | |
| 92-104 | settle | one slow breath; Crest overshoot −3 (f96) → 0; **exact rest at f104** | |

**Feet and ground:**
- Feet planted f0-53 (`plant_frames`) and f82-104.
- `lift_air_frames(range(54, 82))`.
- Root y within ±0.05; ground ≥ −0.02 on every frame.

**Tested evidence** (Thunderbird body, `droop_test.py`, bezier keys, step 1, every frame, all check_pairs + joints + Wing-vs-Chest/Spine):

| path | result |
|---|---|
| FOLD→LIFT1-4→OPEN→(−20,−10,4,−6)→(−45,−15,6,−8)→**(−55,−20,8,−8)** held f24-42 (Spine −0.12/+9, Neck +20, Head +22) → back → OPEN → BOT → OPEN → BOT → OPEN → BRAKE → LIFT4-1 → FOLD | **0 hits**; wing min z 0.42 in the pyre; half-width 1.67 |
| deeper **(−62,−24,10,−6)** at Spine −0.14/+10, Neck +22, Head +24, plus (−50,−26,4,10) | **0 hits**; wing min z **0.25**; half-width 1.55 |

- Sheets: `phx_review\sheet1.png` and `sheet2.png`. The pyre reads from the game camera as a wide, low, back-swept burning spread.
- **Use PYRE = (−60,−22,10,−6)** (between the two tested ones). The fallback is (−55,−20,8,−8).
- Re-run `path_test` on the Phoenix body: Neck2, the crest and the streamers are new, and your frame spacing (4 f) is tighter than my test (3-5 f). If bezier overshoot appears on the 4-f beats, add in-betweens, never linear keys.

**Pose sheet frames to return:** f8, f20, f26, f36, f42, f48, f54, f62, f72, f82, f92 (tq + side + game).

---------------------------------------------------------------------------------------------------------------------
## 8. Studio VFX plan (VFX Studio plugin only, owner rule; no Neon; the mesh must look complete without it)
1. **CrestTip:** a soft flame flicker and rising embers, always on; a flare on `ignite` / `flare` / `reborn`.
2. **WingFire_L/R + StreamerEnd_C/L/R:** short fire **ribbon Trails** (flame → ember → smoke-dark) in fly, takeoff, land and the act's rise. At rest, slow ember drips.
   - **Not** a flame jet on the tail tip: Cerberus and Ivonrath own that preset.
3. **Core:** a warm PointLight that pulses on `heartbeat1` / `heartbeat2` and bursts on `rebirth`.
4. **Pyre:** a ground fire ring on `pyre`, smoke + dimming embers on `ash`, an outward fire shock ring on `rebirth`.
5. **Beak:** a heat-ripple shock on `screech` / `reborn`. **No breath.**
6. **Idle:** `ember` puffs off the back, `lick` flares at the StreamerEnd anchors.
7. **Body:** the Magma `embers` family on Chest, plus the shared secret aura.
8. Add an `InfernoPhoenix` entry to the VFX presets when the owner wires it (not now).

---------------------------------------------------------------------------------------------------------------------
## 9. v1 SIGN-OFF CHECKLIST (model round; each item pass/fail, all must pass)

1. **Side silhouette (600 px, idle f0):**
   - body axis 38-42°; breast the most forward BODY mass; the **head front ≥ 0.10 ahead of the breast front**
   - a visible S: throat concave under the chin, nape convex
   - knee and femur invisible; visible leg ≤ 25 % of H_MODEL
   - the crest C tip is the model top (H_MODEL **2.05 ± 0.04**)
   - three streamers trail low behind (troughs ≥ 0.10), vanes lifting ≤ 20°, no hook
2. **Front view:**
   - a shield torso (breast hw 0.22 → belly 0.17) and the PALE tongue rising (pointed UP) from the belly
   - no down-pointing bib, no penguin front; PALE ≤ 22 %
   - trousers inset (≤ x 0.21), scarlet tarsi, no parallel columns
   - the crest fans to ±0.20 above the head as a flame crown
3. **Game camera (~38°, behind):**
   - a black cloak with an ember-lava hem
   - fire-tipped primaries above three fire-tipped streamers
   - the BASALT hood with a **gold ring all round** and five plumes
   - the EMBER cape with its LAVA hem row
   - no rails, no shark teeth, no backpack (Thunderbird lessons); the wings hug (half-width 90 % ≤ 0.48)
4. **64 px icon (idle f0 portrait) and strip** with MoltenBoar, LavaGolem, Cerberus, Ivonrath, Thunderbird, Griffin, SolarLion, BlackDragon, CelestialDragon, ThunderRex, AbyssalOrca and ThornbladeMantis.
   - I can name: "fire bird", "flame crest with a gold ring", "long burning tail plumes".
   - It is the most striking icon of the Magma row and holds its own next to the other secrets.
   - The crest is not cropped.
5. **A/B pairs (64 px):**
   - Phoenix | Thunderbird: different value (black vs teal / white), silhouette (S-neck, crest up, streamers vs a fan), tip shape (curved tongues vs kinked bolts) and feet (scarlet vs gold).
   - Phoenix | Ivonrath: they must NOT read as the same family. Black-dominant vs red-dominant, feathers vs membranes, a ring + plumes vs a 3-point crown, vanes vs a spade.
   - **If Ivonrath fails:** raise BASALT on the neck back and coverts. Do not shift the EMBER hue.
6. **Shares** (flat palette-ID, idle f0, side / tq / game / front) inside the §3 table. No role > 45 %; BASALT alone ≤ 40 %. GOLD only on the circlet and beak. LAVA / FLAME / HOT only inside ramps.
7. **Face close sheet (front, side, tq at 700 px):**
   - the fused BASALT_D V brow (no visor from the side, no nubs from behind)
   - lid-heavy FLAME eyes, readable from front and side, **no pupil, no glint**
   - malar stripes flush
   - hooked GOLD beak with a black tip that continues the curve, the tomial tooth, GOLD_D cere and mandible
   - the circlet seated (≤ 0.01 proud, closed at the back)
8. **Crest:**
   - 5 plumes, rise 44-55°, all in the upper-rear quadrant
   - 4 stepped blocks each, curling backward the same way, no jog, smooth
   - widths ≥ 0.08 at the root
   - not a corona from any view
9. **Wings and fold:**
   - wing3 points at Δ (−0.05,−0.02,+0.06); `fold_search` re-run and accepted (§4.7)
   - tongues curved and same-sign per wing
   - secondaries end EMBER → LAVA (no yellow on the hem); primaries LAVA → FLAME → HOT
   - no B.poly; no zig-zags
10. **Streamers:**
    - 3 chains on narrow round knuckles; shafts ≥ 0.09 wide
    - lanceolate vanes ≥ 3.5:1, max width 0.20, diamond section
    - collinear tongues, no round eye, no diamond, no crescent
    - ≥ 0.06 clear of the folded wing at rest
11. **Remix sweep, none of these anywhere:**
    - seams or cracks, kinked bolts, a tail fan
    - a brow disc or gem, crown points, horns, scales, membranes
    - standing back blades, white crescents, violet, round eye-spots, a glowing core gem
    - a slit pupil, gold feet
12. **Hard rules:**
    - no Neon, no glow mesh; ≤ 12k tris (cap 15k)
    - nothing floating or buried (circlet, brows, eyes, malar stripes, shingles `surf_hit`-seated)
    - no detail under 0.02
    - BASALT lum ≥ 70
    - HEIGHT 10 / H_MODEL measured / PITCH recomputed
    - all constants plain (no `os.environ` reads in the shipped spec, Thunderbird review 2 fix 9)
13. **Rig at rest and at the limits:**
    - `collision_free: true` at rest, with every §5.2 pair and §5.3 capsule
    - **static limit poses render clean (0 hits), all 6 required:**
      1. FOLD
      2. head look-back 44° (Neck 8 / Neck2 12 / Head 24)
      3. pyre bow (Spine −0.13/+9, Neck 12, Neck2 12, Head 20, wings PYRE)
      4. roar train peak (X1 +56 / X2 +24 / X3 −14, wings BREATH, Crest +14)
      5. streamer drop (X1 −24) on the ground
      6. fly downstroke bottom with the streamer wave at its extreme
    - `path_test` passes: the 8 Thunderbird paths, the act wing path and the roar wing path
    - every anchor from §5.1 exists
14. **Deliverables:**
    - a 600 px model sheet (tq / front / back / side / game, bind pose) + a separate 600 px tq
    - a **fold sheet** (idle f0: tq / side / game / back / front)
    - the face close sheet
    - the 64 / 128 icon strip (item 4) and the 2 A/B pairs (item 5)
    - the flat-ID share table (4 views)
    - the tri count; the `fold_search` top-5 table; the `path_test` JSON
    - the 6 limit-pose renders

    **Render the model views LAST:** `headless_closeup` overwrites `model_tq` at 200 px.

**Clips come after this model gate:**
- `idle`, `walk`, `fly`, `takeoff`, `land`, `roar`, `act_rebirth`, as §7, with the references cited in `ANIM_REFERENCES_1014.md`.
- Return: pose sheets (tq / side / game) of every clip (act frames as §7.7); `collision_free: true` at step 1; linear 0; loops closed; walk slide 0; ground_min_z sampled on **every** frame; the events list.
- Studio names to register: `act_rebirth`; events `ignite`, `pyre`, `ash`, `heartbeat1`, `heartbeat2`, `rebirth`, `reborn`, `touch`, `screech`, `rattle`, `launch`, `ember`, `lick`, `flare`.
