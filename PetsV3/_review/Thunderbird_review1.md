# Thunderbird - art director review 1 (2026-10-14) - REVISE (rebuild body, legs, fold and palette; keep the head and wing recipe)

**Score: 4/10 for a 5% pet.** When the wings are spread (the bind pose, `model_game`), it is the best-looking Storm flyer
we have. But players almost never see that pose. On the ground (90% of screen time, and the pose the Index icon is
rendered from: `petkit.portrait` uses `idle` f0), it is a blue column with human thighs, and the wings are either a tall
slab or two arms sticking out. As it stands it does not beat Raiju, ThunderBull or StormWyvern. The head, the wing
recipe, the feet and the concept are worth keeping. The body, legs, fold, palette and accents need a v2.

What I looked at:
- `pets/Thunderbird.py` (all of it), plus `pets/Griffin.py`, `pets/StormWyvern.py`, `pets/Raiju.py` and `pets/ThunderRex.py`
- `wing3.py`, `_tools/fold_search.py` and `_tools/fold_render.py`
- the v1 renders: `_model_sheet`, `_pose_tq_sheet`, `_fold_sheet`, model_side/front/game/tq at full size, and a face crop
- for comparison: the `_ALL_FIERCE_progress`, `_icons_sheet`, Griffin and StormWyvern sheets, the Thunder Rex preview, and the
  `act_*` docstrings of all 22 other pets

**I ran my own fold experiments** (headless Blender, run3 + this spec, monkey-patched wing positions). The outputs went
ONLY to `C:\Users\ventu\AppData\Local\Temp\tb_review\`; no project file was touched.
- Scripts you can reuse:
  - `fold_try.py`: search/render, with env `TB_DX` (shift the wing in x) and `TB_ARM` (arm length factor)
  - `path_try.py`: checks the transitions between keys at step 1
  - `posture_try.py`
- Look at these sheets: `trysheetC.png` (cloak-fold candidates), `postsheet.png` (cloak fold + body pitched 14/20 deg: the
  target read), `trysheetV.png` (raised V / beat-down / lift poses) and `strip64.png`.

---------------------------------------------------------------------------------------------------------------------
## 1. What works and what doesn't (specific)

**Keep:**
- The eagle head from the front: V brow, yellow slit eyes, gold hooked beak (Griffin's recipe, fully in-family).
- Griffin's 3-row feather wing with the stud skin.
- The gold scaly feet with black talons.
- The rig type (wingbiped) and the flight clip set.
- No glow anywhere.

**Fails, ordered by impact:**
1. **The ground fold is broken, and that pose is also the icon.**
   - The Griffin fold (40,-4,0,100) stacks the wings into a tall slab behind the head (pose sheet).
   - The searched candidates hold the arm bar out sideways at ±0.64, 2.5x the body half-width (`fold_sheet`).
   - Why the search missed better folds: the grid only covered up ≤ 40 and twist ∈ {0,-15}.
   - Also, `check_pairs()` has no Wing-vs-Chest/Spine pairs (Griffin has them, `pets/Griffin.py` L292-293), so the
     search could not see a wing cutting through the chest.
2. **"Person in a bird costume" (the builder's concern is correct). The causes:**
   - **(a)** The femur is modelled as a visible blue "trouser" column: hip z 0.70 → knee z 0.42, hw 0.11-0.14, angled
     forward like a squatting human thigh. On an eagle the femur and knee sit inside the body.
   - **(b)** The gold "shank" is on the tibiotarsus (KNEE→ANKLE), which is exactly the part that is feathered on an
     eagle. So the leg reads as thigh + shin + foot, which is a human leg.
   - **(c)** The visible leg is 0.70 of 1.80 (39%). On a perched eagle it is about 25%.
   - **(d)** The torso is two same-coloured boxes at 32°. From the front, that is a rectangle on two parallel
     rectangles.
   - **(e)** The head sits straight on top, so the side profile is a vertical stack.
3. **Colour: it isn't teal, and it is one flat colour.**
   - BODY (46,112,172) has a hue of 209° (azure). The egg already has Raiju at 227°, ThunderBull 232°, Rex hide 234° and
     Wyvern 245°, so this is a 5th blue.
   - That one mid-blue covers the chest, waist, trousers, neck base, coverts and arm bars: roughly 60% of the body.
     There is no dark top or light underside. In game it is about (28,67,103), a plain steel blue.
   - From the game camera, the lone BODY_D back plate (L153) reads as a little black "backpack".
   - The bottom shingle row (L155-159, WHITE_D, z 0.87) is buried in the chest. Only two tips show, as two white
     "buttons" on the belly (`model_tq`, `model_front`).
4. **The lightning reads as paint-dipped tips.**
   - The tips are flat tapered yellow ends (tipf 0.26-0.28) that read as yellow nails or flames. Nothing is bolt-shaped.
   - The yellow sits right next to Raiju's BOLT (255,202,36).
   - The white secondary tips line the bottom edge of any folded wing like a skirt fringe.
5. **The tail** is a thin dark stick from the side with a small dark fan. It adds nothing at 64 px.
6. **The crest:**
   - It has 5 feathers; the longest is 0.34.
   - From the front it reads as a little yellow tiara over the brow, and from behind as a tuft. It never reaches the top
     of the silhouette.
7. **The brow:**
   - The navy slabs (L191-192) float as a separate cap or visor in the side view.
   - From the game camera they poke up as two dark nubs on the white head (`model_game`). This is the same "goggle
     slab" problem Rex v1 had.

---------------------------------------------------------------------------------------------------------------------
## 2. Redesign brief - "THE STORM HERALD" v2 (ordered by impact)

### 2.1 Ground fold: the CLOAK FOLD (tested, collision-free). This is the single biggest win.
**Geometry change (required):** move the whole wing out to the body surface: **+0.07 in x for S, BB, W, H, H2 and TIP**.
In the code: `_S0 = (0.27, -0.10, 1.16)`, `_BB0 = (0.24, 0.22, 0.98)`, and +0.07 on the x of the three `_raise()`
inputs (L48). In v1 the shoulder sits 0.05 inside the chest (S x 0.20 vs chest hw 0.25), so any fold that lays the wing
along the flank cuts through the breast:
- With dx = 0, every cloak candidate hit Chest/Spine (8-27 tri-pairs).
- With +0.07 they are clean.
Do **not** shorten the arm to fix the fold: the arm was never the blocker. A 0.85x arm gives the same fold and is 0.1
shorter (optional, only if the wingtips end up too far past the tail).

**FOLD = (up 100, fwd 20, twist -80, tip -15).** This is a different region of wing3 space from the one searched: a big
raise followed by a big twist about the REST arm axis swings the wing back down along the flank.

| ground fold (v1 body, wing +0.07 x) | half-width max / 90% | wing back y | wing min z | cut-throughs incl. Chest/Spine |
|---|---|---|---|---|
| v1 Griffin fold (40,-4,0,100), dx 0 | slab, crosses | - | - | (the pose sheet shows the cross) |
| v1 best searched (25,-12,-15,60) | 0.64 | - | - | Chest/Spine not checked |
| **cloak A (100,20,-80,-15)** | **0.44 / 0.37** | 1.46 | 0.22 | **0** |
| cloak B (90,10,-90,0) | 0.55 / 0.47 | 1.27 | 0.15 | 0 |

How it looks (`trysheetC.png` row 1, `postsheet.png`):
- The arm bar lies along the top of the flank pointing BACK, as the shoulder line. Nothing sticks out sideways.
- The dark wing covers the flank and the thigh.
- The primaries trail back to the tail.
- Folded, the wing shows its under-layer (secondaries and primaries) outward. So the dark storm colours show on the
  ground, and the light coverts show in flight and in the roar. Colour them with that in mind (2.3).

**Transition waypoints (each tested at step 1, 0 hits on the v1 body with the +0.07 move). Every fold↔open change must
pass through them, in order, both ways:**

| key | (up, fwd, twist, tip) |
|---|---|
| FOLD | (100, 20, -80, -15) |
| LIFT1 | (90, 30, -70, -15) (wings lifted off the body: also the idle "wing breath") |
| LIFT2 | (70, 30, -50, 0) |
| LIFT3 | (50, 20, -25, 10) |
| LIFT4 | (35, 8, -8, 10) |
| then any open pose | (30,0,0,0), (-34,8,6,4), (24,16,-10,-4), (22,6,6,-4), (-6,2,0,-8), **raised V (40,0,0,-10)** |

Paths I tested, all clean:
- FOLD → LIFT1-4 → (30,0,0,0)
- Flight bottom (-34,8,6,4) → land brake (24,16,-10,-4) → LIFT4 → … → FOLD
- FOLD → LIFT1-3 → raised V ↔ (4,4,4,-6) ×2 → LIFT3-1 → FOLD
- FOLD → LIFT1 → (80,30,-60,-10) → LIFT1 → FOLD

What fails:
- A shortcut (FOLD → LIFT2 → (30,0,0,0)) cuts the chest.
- Direct FOLD ↔ open interpolation cuts the legs, spine and chest (170-450 tri-pairs).
- v1's cocked pose (60,-6,0,40) makes the wingtips cross behind the back once the wing is moved out (1,300+ tri-pairs).
  Use the raised V instead.

**After the body changes in 2.2, re-run the search,** because the tilt moves everything:
- Grid: ups 80-110, fwds 0-30, twists -70..-100, tips -30..+15.
- Add `(Wing_*/WingTip_*, Chest|Spine)` to `check_pairs()` permanently (Griffin L292-293).
- Acceptance:
  - 0 hits
  - half-width ≤ 0.50
  - wing min z ≥ 0.12
  - the wingtips end within ±0.12 (y and z) of the tail tip, resting beside or over the fan like a real eagle
- Then re-check the waypoints.

### 2.2 Body posture, proportions and legs (removes the costume)
`postsheet.png` shows that just pitching v1 forward 14-20° already turns the side view into an eagle. Build that pose
into the mesh:
- **Body angle:** chest block rot 32 → **46°**, lower body 32 → **52°**. The line from the breast-top to the tail base
  should be 44-50° from vertical.
- **Breast (the biggest, most forward mass):**
  - Chest at ~(0,-0.12,0.98), half-size (0.27, 0.25, 0.27), bot (0.62,0.56), rnd 0.40.
  - Add a forward keel bulge: `B.seg((0,-0.38,1.10),(0,-0.20,0.68), 0.17, 0.08, TEAL, "Chest", top=(0.55,0.8))`, the
    StormWyvern keel (`pets/StormWyvern.py` L106).
  - Add shoulder masses for the moved wing root: StormWyvern flight muscles (L104-105) at (±0.20,-0.10,1.12), size
    (0.10,0.12,0.11), so the wing roots on a shoulder and not in the air.
- **Lower body:**
  - (0,0.10,0.64), size (0.20,0.20,0.17), rot 52, bot (0.72,0.66), rnd 0.38. Its bottom at z ≈ 0.46 must **swallow the
    knee**.
  - Chest vs belly is 0.27 vs 0.20: a deliberate step (Lessons #1).
  - Side view check: the belly line rises from the breast to the legs.
- **Flank skirt:**
  - 3 rows of the v1 skirt spikes (L161-163) at z 0.70 / 0.60 / 0.50 and x ±0.18, pointing down-back, L 0.16-0.20.
  - Top row TEAL, lower rows STORM.
  - They hang over the knee so no thigh is ever visible.
- **Legs (new joints):**
  - HIP (0.14,0.12,0.62), **KNEE (0.16,-0.04,0.50), inside the belly**, ANKLE (0.16,0.07,0.22), TOE (0.16,-0.05,0.035).
    Keep knee pole (0,-1,0).
  - Leg_ bone: a hidden TEAL thigh block only.
  - **Shin_ = the trousers:** STORM, 0.08 hw at the top flaring to 0.10 at the bottom. Add a fringe of 5 down-pointing
    spikes (L 0.10-0.13, w 0.045) that hangs over the top of the tarsus (Griffin fringe L229-231, moved to the ankle).
    These are the "dark socks" that frame the gold feet.
  - **Foot_ = the bare gold tarsus:** hw 0.058 (v1 0.045), with 3 GOLD_D scale bands (Griffin L233-236).
  - Toes: L 0.10, hw 0.028, outer toe splayed 18°.
  - Talons: BLACK 0.10 x 0.024, each a 2-part hook (a spike plus a short down-turned spike at its tip). The **hind
    (hallux) talon is the biggest, 0.11** (the eagle's killing claw).
  - Target: the visible leg (belly edge to ground) is **≤ 26% of the height** (v1: 39%).
- **Front view target:**
  - A shield shape: widest at the breast and shoulders (hw ~0.29), tapering to ~0.20 at the belly.
  - The trousers emerge inset under the belly, with the feet at x ±0.17.
  - No parallel columns.
- **Neck and head:**
  - The neck is shorter and thicker (hw 0.15 → 0.17).
  - The head moves forward and down with the tilt (HC ≈ (0,-0.46,1.50)), with the cranium top at ~1.62.
  - Update H_MODEL to the new top (the crest tips) so PITCH recomputes. Keep HEIGHT 8.5.

### 2.3 Palette: a real storm teal in three values (Blender values; in game about x0.6)
| role | Blender RGB | in game ~ | where | target share (game cam / side) |
|---|---|---|---|---|
| STORM | (26, 80, 100) | (16,48,60) | back mantle, folded-wing outside (secondaries), trousers, tail base, crest band, lower flank skirt | 30-38% |
| PRIMARY | (16, 46, 62) | (10,28,37) | primary and tail-feather bodies before the bolts (maximum contrast for the yellow) | 6-10% |
| TEAL | (36, 138, 160) | (22,83,96) | breast, belly, shoulders, upper skirt, arm bar (lum 118 ≥ 95 OK) | 18-25% |
| COVERT | (82, 176, 190) | (49,106,114) | upper-wing coverts (seen in flight and roar), top breast-shingle row, secondary tip edges | 4-8% |
| WHITE / WHITE_D | (236,240,248) / (194,206,224) | | head, ruff, bib, **tail fan** / brow ridge, ruff shading, nape hackles | 15-22% |
| GOLD / GOLD_D | (246,166,38) / (204,120,24) | | beak, cere, tarsus, toes / hook, scale bands | 4-7% |
| BOLT / HOT | (255,234,56) / (255,252,214) | | lightning tips (primaries, tail, crest), iris / bolt points, eye hot spot | 10-15% |
| BLACK, MOUTH | keep | | sockets, nostrils, talons / gape | - |

Why these values:
- The hues sit at 188-201°, 25-55° away from every sibling, so Thunderbird finally owns a colour in the Storm egg.
- GOLD is 37° and BOLT 54° (lemon), so the beak and feet stop competing with the lightning, and the lightning stops
  matching Raiju's amber.
- No single colour may exceed 45%.

### 2.4 Hero feature: THUNDER WINGS, lightning-edged primaries
This is the one thing the pet is "about". Everything else stays quiet (storm, teal, white) so the edges carry it.
- **Every primary** (5 outer and 3 inner) **and every tail feather** ends in a **kinked 2-step bolt**:
  - PRIMARY feather body → a BOLT segment (the first 55% of a tip that is 30% of the feather length), jogged sideways
    in the wing plane by 0.35 x width → a HOT point (the last 45%, top=(0.12,…)), jogged back the other way. That makes
    a Z.
  - Alternate the jog direction on neighbouring feathers so the edge reads jagged, not combed.
  - Build it like ThunderRex's `shard()` kink (`pets/ThunderRex.py` L148-153), but in the wing plane: use
    `(tip-root).cross(nrm)` as "back".
  - Bolt parts are `nostud=True`. Feather bodies keep their studs.
- **Secondaries:** no yellow. Replace the WHITE tips (L109) with a COVERT edge at tipf 0.15. The folded wing's lower
  edge then becomes a clean two-tone saw, not a white skirt.
- **The result:**
  - Folded, the bolts form a jagged yellow lightning line down the rear of each flank, ending at the tail. That is
    exactly what the game camera sees.
  - Opened in the roar or in flight, the whole hand is edged in lightning.

### 2.5 Head and crest
- **Head:**
  - +10% (cranium hw 0.135 → 0.148). It is the white beacon from the back camera and at 64 px.
  - Beak +15% in length and depth (cere→hook 0.165 → 0.19, upper bill hw 0.066 → 0.074, hook spike 0.11 → 0.13, GOLD_D).
- **Brow:**
  - Delete the navy slabs (L191-192).
  - Build one heavy **WHITE_D** brow per side, ≥ 50% buried in the cranium, overhanging the eye by 0.02-0.025, angled
    20-22° down toward the middle so the pair meets in a V at the cere (the Raiju brow shape, `pets/Raiju.py` L73-75).
  - Eye `sc` 1.1 → 1.25, so the black socket line under the brow carries the fierce V.
  - From behind: no dark nubs.
- **Crest = a harpy-eagle double crest growing from the BACK of the crown** (roots at y +0.06..+0.10 on the cranium top):
  - Back row: 4 long feathers, 0.40-0.46, spread ±30° in x, rising 35-50°.
  - Front row: 3 short feathers, 0.22-0.26, between them.
  - Each one: WHITE root → a thin STORM band at 55% → a kinked BOLT/HOT tip (the same bolt builder as 2.4).
  - Vary lengths ±15%.
  - The crest tips are **the highest point of the pet** (0.15-0.2 above the head top) and read from the game camera.
  - Build it as real raptor anatomy, not a "war-bonnet" headdress. It reads fiercer, and it avoids the headdress look in
    a kids' game.
  - Check the roar's head-up pose (Head -12, Neck -6): the crest must clear the ruff and mantle.
- **Ruff and hood:**
  - Keep the white spikes (L166-170).
  - Add a jagged white V bib on the upper breast (3 down-pointing shingles).
  - Add a WHITE/WHITE_D hackle cape over the shoulders (Griffin L173-181), so white → teal is a feathered edge and not
    a collar.

### 2.6 Tail: the white bald-eagle fan
- 9 feathers (v1 has 7), L 0.58-0.66 with the centre longest, width 0.15, spread ±50°.
- WHITE with kinked BOLT/HOT tips (2.4), on a STORM base: 3 upper-tail-covert shingles over Tail1.
- At rest, pitch it -8..-12 (raised) so it faces the game camera and clears the ground.
- The tail tip ends within ±0.1 of the folded wingtips.
- **White head + white tail is the bald-eagle read at 64 px.** From behind, the white fan sits between the two dark,
  bolt-edged wings.

### 2.7 Back, breast and cleanup
- Delete the BODY_D back plate (L153). Replace it with a **STORM mantle**: 3 brick rows of shingles from the nape to the
  tail base (Griffin hackle cape L173-181 in STORM). It fills the strip between the folded wings.
- Delete the WHITE chest shingles (L155-159, the "buttons"). Replace them with **4 rows of breast shingles** following
  the new 46° breast (Griffin L164-169 recipe): top row COVERT, middle rows TEAL, bottom-row tips STORM.
- Make the arm bar (L99-101) TEAL instead of COVERT and taper it, so it doesn't read as two light rails on the back from
  the game camera.
- Studs on all body and feather masses. Smooth: bolt parts, talons, beak hook, eyes. No detail under 0.02. Budget ≤ 15k
  tris (expect ~8-10k).

### 2.8 Copy map
| what | from |
|---|---|
| feather wing, eye, eagle head base | own v1 L68-143 (= `pets/Griffin.py` L73-147) |
| Wing-vs-Chest/Spine pairs | `pets/Griffin.py` L292-293 |
| keel bulge + flight-muscle shoulders | `pets/StormWyvern.py` L104-106 |
| breast shingles / hackle cape / mantle | `pets/Griffin.py` L164-169 / L173-181 |
| trousers fringe, scale bands, talons | `pets/Griffin.py` L227-242 (move the fringe to the ankle) |
| kinked bolt tips | `pets/ThunderRex.py` `shard()` L129-157 (kink logic L148-153) |
| brow shape | `pets/Raiju.py` L73-75 |
| dark-socks framing idea | Cerberus / CelestialDragon, as in the Rex review |

### 2.9 VFX anchors (VFX Studio plugin later; the mesh must look good without them)
Add empty bones for the anchors:
- **WingBolt_L/R**: 3rd-primary tip, on WingTip_*
- **TailBolt**
- **Crest**
- **Beak**
- **Strike**: on Root, 0.18 in front of the feet

The effects:
- Sparks crawling along the wing edges.
- A lightning flash on each roar beat.
- A bolt plus a ground scorch on the strike.
- A small crackle at the crest.
For a 5%, keep it modest: no aura (that is the secrets' language).

---------------------------------------------------------------------------------------------------------------------
## 3. v2 checklist (pass/fail; all must pass)
1. **Posture (side view):**
   - The body axis is 44-50° from vertical, and the breast is the most forward mass under the head.
   - The belly line rises to the legs.
   - No femur or knee is visible.
   - The visible leg is ≤ 26% of the height.
2. **Front view:** a shield torso tapering to the belly, trousers inset, no parallel columns, no lone shingle "buttons".
3. **Fold:**
   - The FOLD has 0 hits including Wing-vs-Chest/Spine, and a half-width ≤ 0.50.
   - The arm lies along the top of the flank (nothing sticks out).
   - The wingtips end within ±0.12 of the tail tip.
   - Every fold↔open change goes through LIFT1-4 with 0 hits at step 1.
4. **Game camera (~38°, behind):**
   - It reads as an eagle from behind: white head and crest on top, two dark bolt-edged wings converging on a white
     fan.
   - Not a column, no rails, no backpack.
5. **64 px:**
   - The Index icon (idle f0) on the slate background. You can name "eagle", "lightning wings" and "white head/tail".
   - In a strip with Raiju, ThunderBull, StormWyvern and ThunderRex it is clearly the teal one, and it beats the three
     commons.
6. **Palette:**
   - STORM+PRIMARY 35-45%, TEAL+COVERT 20-30%, WHITE 15-22%, BOLT+HOT ≥ 10%, GOLD 4-7%, measured in the game and side
     views.
   - No colour above 45%.
7. **Lightning:** every primary, tail-feather and crest tip is a kinked BOLT→HOT 2-step. No dipped tips, no white
   secondary fringe, no stickers.
8. **Face:**
   - A tonal brow fused to the skull: no visor from the side, no nubs from behind. The V reads from the front.
   - Eyes are visible from the front and the side.
   - The beak is +15% with a clear hook.
   - The crest is the top of the silhouette and clears the neck in the roar.
9. **Tier:**
   - It reads above the 3 commons and below Thunder Rex: no crown, no crystals, no aura.
   - Hard rules: studs, no glow, ≤ 15k tris, nothing floating, no detail under 0.02.
10. **Deliverables:**
    - model sheet (tq/front/side/back + game)
    - face close sheet
    - **fold sheet** (tq/side/game/back of idle f0)
    - 64 px strip with the Storm egg
    - pose sheet of every clip
    - collision/audit pass

---------------------------------------------------------------------------------------------------------------------
## 4. Animation notes (30 fps)
**General:**
- Every ground clip starts and ends at the new FOLD. Every fold↔open change uses LIFT1→LIFT4 in order (2.1).
- The tested paths stay valid only if the keys are not overshot. If Bezier handles bulge on the fast 1-frame keys, use
  linear interpolation there, and always re-run step 1.
- Birds stabilise their heads: in walk and fly, counter-rotate Head against the Spine/Chest pitch and roll (≥ 70%).
- **No head shakes:** no yaw reversal faster than 6 frames. A jaw buzz is fine.

- **idle (~132 f):**
  - v1 bug: f34→36 swings the head ~58° in 2 frames (Neck ny 30→-28 x 0.3 plus Head x 0.7). That reads as a
    twitch/shake. Snap ≤ 30° per 3-4 frames instead, and go L → hold → centre (6 f) → R → hold.
  - Beats:
    - breath swell (keep)
    - look left and look right, each with a hold
    - **a hunting stare**: Neck +10, Head +12 down at the ground in front, dead still for 20 f (the predator moment)
    - a sky glance
    - **wing breath**: FOLD→LIFT1→(80,30,-60,-10)→LIFT1→FOLD over ~24 f (tested, 0 hits). This replaces v1's one-wing
      stretch, which was built on the old fold.
    - **talon re-grip**: one foot lifts 0.03, the toes curl (Foot +20), it re-plants; then the other foot
    - tail flick (keep)
- **walk (28 f):**
  - Replace the head bob (Neck/Head ±4, twice per cycle) with a stabilised head. On a big raptor a pigeon bob reads as
    comedy.
  - Make it a rolling strut:
    - Spine roll ±5 over the stance leg, yaw ±3.
    - Lift 0.12, toes curled in the swing (the existing toe hack) and spread before contact.
    - An asymmetric contact dip: -0.04 within 3 f of contact, then a slow rise, as in Rex's approved walk.
  - Wings stay folded with a 0-15% blend toward LIFT1 on each contact, for balance (stays on the tested path).
- **fly (28 f):**
  - Keep the stroke recipe. Go deeper (top 34 / bot -40) if it stays collision-free: eagle beats are slow and deep.
  - Head level with the beak forward; head bob ≤ ±2.
  - With the shorter legs, tuck the talons balled under the tail fan.
  - The tail steers (keep).
  - Optional, if the follow system allows a longer loop: 2 beats plus a 10 f glide with the primaries spread (tip -10).
- **takeoff (30 f):**
  - Crouch with FOLD→LIFT1→LIFT2 (f0-6), then LIFT3→LIFT4 (f6-9), and the stroke top (30,0,0,0) by f10.
  - **LAUNCH** on the big downstroke at f11 (event); the legs push, then tuck.
  - Never skip waypoints. A 3-key shortcut cut the chest.
- **land (32 f):**
  - v1's ref beats are right: flare, brake with the wings swept forward, legs reach, touch, absorb.
  - Add **open talons thrown forward before the touch** (Foot -20, toes spread): eagles land feet-first.
  - Absorb crouch with the wings in the **raised V (40,0,0,-10)** for 4-6 f, then fold via LIFT4→LIFT1→FOLD (tested from
    the brake pose).
- **roar = SKY SCREECH (~70 f):**
  - f0-8: gather; the head pulls in, and the wings go LIFT1→LIFT2.
  - f8-14: rear up (Spine -10, chest up). The wings go LIFT3 → **raised V (40,0,0,-10)**. The V shows the upper wing and
    the lightning edges to the game camera. v1's flat OPEN shows the wings edge-on, as "arms out" (`pose_tq_roar_28`).
  - f14-48: head up, beak 34-38 with a ±2 jaw buzz, and **2 thunder beats**: V → (4,4,4,-6) → V at f20-26 and f32-38.
    The body lifts 0.03 on each downbeat, and the tail fan flares. Events beat1 f23 and beat2 f35 (bolts from the
    WingBolt anchors).
  - f48-70: fold via LIFT3-1, then settle.
  - The whole path is tested (0 hits). No head yaw.
- **act_talonstrike → make it a STOOP STRIKE (~84 f).**
  - Why: v1's beats (a hop, both feet forward, the strike, the head down over the kill) overlap Griffin's `act_mantle`
    (a talon strike with the head down over the prey) and LavaGolem's `act_pound` (a jump, a double smash, a glare).
  - The beat no other pet has, and the most raptor thing there is: **the stoop**. The wings tuck tight for a dive, and
    the talons are thrown forward at the last moment.

| frames | beat | keys |
|---|---|---|
| 0-10 | **lock on** | crouch: Spine z -0.08, pitch +8. Neck +10 / Head +10 aimed 0.2 in front, dead still for 6 f. Wings FOLD→LIFT1→LIFT2 |
| 10-14 | **launch** | LIFT3→LIFT4→(30,0,0,0), then one huge downbeat (-34,8,6,4) at f14 (event `launch`). Spine z +0.30 by f18; legs tuck (FK) |
| 14-24 | **hover** | one short beat at the apex; body nose-down +10, tail fanned -14, talons balled, head locked on the target |
| 24-30 | **stoop** | the wings snap back LIFT4→LIFT3→LIFT2→LIFT1→FOLD (one key per frame). Body pitches +25 nose-down and drops (z +0.30→+0.08): a teardrop |
| 30-33 | **throw** | the feet swing forward (FK thigh -40, shin +50), talons open; wings flare FOLD→LIFT1-3→raised V (1-frame keys); body pitches back -12 |
| 33 | **STRIKE** | both feet slam 0.18 in front (event `strike` at the Strike anchor); recoil z -0.06; talons clench by f36; tail fan flares up |
| 36-42 | grip hold | head low, glaring at the strike point (Neck +6, Head +10); wings held in the V; a 2-frame shudder in the chest (±2 pitch, not the head) |
| 42-60 | **scream to the sky** | Neck -6, Head -12, beak 36 with a ±2 buzz, wings high in the V (event `scream` at f44). Different from the roar: no beats, talons clenched, body low |
| 60-72 | fold + return | V→LIFT3→LIFT2→LIFT1→FOLD; two small hop-steps back to the rest spots (dy +0.09 each) |
| 72-84 | settle | back to rest |

  - Do **not** use v1's cocked poses (60,-6,0,40) or (46,-8,0,40); they collide once the wing is moved out.
  - The footprint stays in place: the strike lands 0.18 in front, which is under 2 studs at x2.2.
  - ground_min_z must stay ≥ -0.02 in the stoop.

---------------------------------------------------------------------------------------------------------------------
## 5. Summary for the coordinator
- **REVISE, 4/10 for a 5% pet.** The spread wings are great, but the ground pose (which is also the icon) reads as a
  blue man in a bird suit with broken wings.
- **The fold is solved:**
  - Move the wing root +0.07 in x.
  - FOLD = (100,20,-80,-15): ±0.44, 0 hits including the chest.
  - Use the 4 tested LIFT waypoints for every transition.
  - Add Wing-vs-Chest/Spine to `check_pairs`.
  - Re-run the search after the body change.
- **Rebuild:**
  - the body at 46-52° with a big keeled breast
  - the knee hidden in the belly
  - STORM trousers on the shin, bare gold only on the tarsus
  - the teal 3-value palette
  - kinked lightning tips (the hero: THUNDER WINGS)
  - a white bald-eagle tail fan
  - a tonal fused brow and a harpy double crest
- **Clips:**
  - Rebuild idle (fix the 58° whip), walk (no bob), takeoff, land and roar (raised V, 2 beats) on the new fold.
  - Turn the signature into the STOOP STRIKE.
- **Expected v2:** 7.5-8/10, sitting between the commons and Thunder Rex. Next review needs the model sheet, close sheet,
  **fold sheet** and 64 px strip first; then the pose sheet after the clips.
