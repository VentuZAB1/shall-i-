# Abyssal Orca - art director review 1 (2026-10-14) - REJECT (rebuild the mesh, keep the concept)

**Score: 2.5/10 for a 1.5% SECRET.** The concept is right: a black-and-white orca with an anglerfish lure and abyssal
lights is a strong, unique jackpot idea. The execution is not secret tier, and it would not pass as a common either.
On a 64 px slate icon strip it is the weakest pet in its own egg. The 5.5% Hammerjaw and the common Kraken both read
better. The builder's four worries are all real. Three of them are worse than the builder thinks, and one (mint vs
cyan) is a smaller problem than it looks (see 1.9).

What I looked at:
- `AbyssalOrca/renders/_model_sheet.png` and all 5 single renders at full size, plus `pets/AbyssalOrca.py`
- the owner refs f_63 (Mythic Orca), f_70 and f_71, `FIERCE_GUIDE.md` and `_review/LESSONS_ALL_PETS.md`
- the Thunder Rex reviews 1-3 and its owner preview
- the Tide egg siblings (Kappa, SeaTurtleWarrior, Kraken, `pets/HammerjawShark.py` and its sheet), `_ALL_FIERCE_progress.png` and `_icons_sheet.png`
- the act docstrings of all 25 pet specs and the accent constants of every pet

How I measured:
- Same method as the Rex rounds: background removed and pet pixels classified by colour (approximate, ±3%).
- My own 64 px slate cut-outs with an outline, next to Thunder Rex, Hammerjaw, Kraken and Kappa. These are temp files only; nothing in the project was written except this verdict.

| view | INK | WHITE | GREY (saddle + glare) | MINT | GOLD |
|---|---|---|---|---|---|
| side | **74%** | 13% | 7% | 6% | 0.4% |
| tq | **79%** | 8% | 4% | 8% | 0.7% |
| game cam | **75%** | 6% | 14% | 4% | 0.5% |
| back | 58% | 11% | **26%** (sky glare on flat fins) | 4.5% | 0.5% |

For reference, a real orca from the side is about 30% white, and Rex's gold gate was 1.5-2%.

---------------------------------------------------------------------------------------------------------------------
## 1. Why it looks cheap (specific)

1. **The hull is three equal boxes, a "bus with a stick tail".**
   - L38-40: Chest hw 0.275, Spine 0.262, Head 0.255. All three touching blocks are within ±10% of each other's size,
     which LESSONS #1 forbids. The Chest block has top=(0.96, 0.96), so it has a flat top and no taper.
   - The head is as wide as the body and ends in a flat 0.17 x 0.15 front face.
   - At y 0.5 the body steps abruptly down to a 0.15 tail stock, which is wider than it is tall. A real orca peduncle
     is the opposite: tall and narrow.
   - The body is only 0.55 deep against 2.9 long (5.3:1), so it is a long thin log.
   - Result: three panel seams on the back in tq, a flat roof from the side, and a box from the front.
2. **The orca pattern is missing, so the one thing that makes an orca read at 64 px is not there.**
   - White is 6-13% of the pixels. On the icon it is 1-2 px slivers.
   - The white parts are proud slabs stuck on, not a pattern:
     - The eye patch (L51) is 0.06 thick at x ±0.245 on a head side at x ≈ 0.20, about 0.07 proud.
     - The belly (L44) is a flat 0.40-wide box, the box belly FIERCE_GUIDE forbids.
     - The flank sweep (L48) is a tilted white plank.
     - The saddle (L53) is a raised grey pillow.
   - LESSONS #5 says white zones must be flush inlays (≤ 0.01 proud).
3. **All the fins are flat planks, and they use the 5.5% sibling's recipe.**
   - The dorsal, pectorals and flukes are `B.poly` slabs: untapered, unbevelled, unstudded (blockkit `Poly` L99-131).
     They catch flat sky glare (26% of the back view) and read as plastic cut-outs or aircraft parts.
   - From the front and back, the dorsal is a 0.07 stick ("periscope"). The pectorals read as helicopter skids and
     the flukes as an airplane tail.
   - "Poly fin plus an accent edge strip" (L124-138) is exactly how `HammerjawShark.py` builds its fins (L103-131).
     So the secret is built like the 5.5% pet in the same egg.
4. **The hero lure is a teal dice on a black wire.**
   - The bulb is a rounded cube with hw 0.07 (0.14 across, L85-88). At 64 px that is 3-4 px, and no gold shows at all.
   - The cage fangs are 0.10 long with w 0.016, under the 0.02 detail floor (L90-94). They point forward, so from
     the side they are yellow sparks.
   - The stalk is INK_D on an INK body (invisible), and it tops out at z 1.06, well under the dorsal tip (1.62).
   - Rig bug: the `Lure` joint (L151) sits at the stalk ROOT, so any VFX on "Lure" would glow on the forehead, not
     at the bulb.
5. **There is no face.**
   - The eye parts sit at x ±0.235, but the tapered head side there is at x ≈ 0.20, so they hover ~0.03 off the
     skin. The front view shows them as two black tabs sticking out.
   - The iris is 0.024 tall, so the eyes are invisible from the side at game distance.
   - The teeth are w 0.015-0.016 (under 0.02).
   - The red MOUTH plate shows as two red specks at the lower corners of the front view. They read as a second pair
     of red eyes, the same trap as Rex v1's nostril dashes.
   - From the front the pet is a studded box.
6. **The photophores are specks, and half of them are buried.**
   - They are 0.012-thick squares. Row 1 (L99-104) sits at x 0.259-0.271 on a hull side at about 0.27, so it is
     half sunk.
   - Row 2 (L105-108) at x 0.24, z-0.15 is inside the hull, which is why only one row shows.
   - The dorsal veins are 0.012-0.014 wide (under 0.02).
7. **INK is far too dark.**
   - (40, 44, 64) has luminance 45. In Roblox it becomes about (24, 26, 38): pure black, no visible studs, and the
     same value as the slate Index card.
   - Our approved black pets sit at luminance 72-76: Nightmare COAT (74, 70, 92) and BlackDragon INK (78, 68, 158).
8. **The proportions waste the height on a thin fin.**
   - With H_MODEL 1.55 = 9 studs, the body is only ~3.2 studs deep but ~17 studs long at x1 (37 at x2.2), so the
     pet shrinks to a line in the square Index portrait.
   - Body length to (belly → dorsal tip) is 2.4:1.
9. **Mint vs Thunder Rex's cyan: partly right, but for the wrong reason.**
   - Hue: MINT is 161°, Rex CYAN 193° (32° apart, distinguishable side by side).
   - Aqua is the Tide egg's identity, as cyan is Storm's and flame-gold is Magma's, so the secret SHOULD glow in the
     egg's colour.
   - The real problems are:
     - **Pastel.** Luminance 210 against WHITE patches at 240 means there is no value contrast where photophores
       touch white, and it goes a murky sea-green at 0.6x.
     - **It is all specks.** Only 4-8% of the pixels.
     - **Crowding.** It sits 13° from PharaohAsparuh's TURQ (another secret) and 16° from Kappa's AQUA (same egg).
   - Fix it with a saturated jade, a teal (not blue) DEEP root, and a green-white (not blue-white) HOT. Then
     separate it from Rex by FORM: beads and organic veins, never crystals, shards, seams or cracks. See the palette.

**Keep:**
- the concept (orca + angler lure + abyss lights) and the black/white/grey scheme
- the dorsal fin as the signature silhouette, and gold on the lure
- MOTION Swim / RIG fish, the bone names, the PITCH formula, the Blow anchor
- the GOLD constant (255, 196, 50): the family's "secrets wear gold" gold
- the triangle headroom: 2.9k of 15k used

---------------------------------------------------------------------------------------------------------------------
## 2. Redesign brief - "THE DEEP SOVEREIGN"

**Concept:** a bull orca from the abyss. A heavy torpedo hull in crisp black and white, with a tall sickle-blade
dorsal fin veined with jade light. Rows of lantern photophores run along its waterline and down its spine. Over its
head it carries a crowned angler lantern: a gold coronet on the brow, a gold-ringed rod, and a big jade orb clasped in
gold fangs.

**Family rule:**
- Same blockkit, stud skin and fierce_eye/brow/fang language as the approved pets.
- Nothing from its egg siblings:
  - no coral (Turtle, Hammerjaw)
  - no ring spots or barnacles (Kraken)
  - no armour plates, back spike row, gill slashes or flank scars (Hammerjaw)
- Nothing from Rex: no crystals, shards, armour seams or cracks.

### Palette (Blender values; in-game is about x0.6)
| role | Blender RGB | in game ~ | where | target share (side / game cam) |
|---|---|---|---|---|
| INK | (64, 70, 102) | (38, 42, 61) navy-black | hull top and sides, head, dorsal, pectorals, fluke tops (lum 71, the black-pet band) | 45-55% / ≤ 62% |
| INK_D | (36, 40, 64) | | brows, lip line, blowhole, dorsal serrations, lure rod | ≤ 4% |
| WHITE | (240, 244, 252) | (144, 146, 151) | lower jaw, throat, belly band, eye patches, flank lobes, fluke undersides, tail-stock streak | 22-30% / ≥ 10% |
| SADDLE | (150, 162, 194) | (90, 97, 116) | saddle patch behind the dorsal (the 3rd value band, and what the game camera sees) | 4-7% / ≥ 6% |
| DEEP | (8, 118, 100) | | bead sockets, vein roots | ~2% |
| GLOW | (30, 236, 160) "abyss jade", hue 158° | (18, 142, 96) | the orb, beads, fin veins, eye slits | 8-14% |
| HOT | (214, 255, 226) green-white | | bead centres, vein cores, orb glint and drip tip, eye hot spot | 2-3% |
| GOLD | (255, 196, 50) | (153, 118, 30) | ONLY the coronet, rod rings, orb collar and cage fangs | **2-3% / ≥ 1.5%** |
| GOLD_D | (214, 150, 30) | | inner faces of the cage fangs, ring edges (optional) | - |
| TEETH (240, 236, 222), MOUTH (70, 16, 40), BLACK (14, 14, 22) | | | teeth / mouth roof and floor / sockets and pupils | - |

The DEEP → GLOW → HOT steps are our "no-Neon glow" (the Rex method), done in jade. Studio VFX should use a brighter
jade than the mesh, e.g. (120, 255, 200) → (30, 236, 160).

### Changes, ordered by impact

**1. Silhouette and proportions: a lofted torpedo hull (the biggest single win).**
Replace L38-40 with a chain of 7 `B.seg` blocks between these stations (Z0 = 0.62). Each seg runs from station i to
i+1 with `top=(hw[i+1]/hw[i], hh[i+1]/hh[i])`, so the ends match and there are no steps. Use rnd 0.40, and set
`ext` ≥ the next block's rounding radius (~0.4 × min(hw, hh)) so the joints do not pinch into "sausage links".

| station | y | hw | hh | centre z | bone |
|---|---|---|---|---|---|
| S0 rostrum tip | -1.30 | 0.10 | 0.085 | Z0-0.07 | Head |
| S1 eye / mouth corner | -1.06 | 0.19 | 0.20 | Z0-0.03 | Head |
| S2 back of skull | -0.82 | 0.26 | 0.28 | Z0 | Head / Chest |
| S3 max girth (pectoral roots) | -0.50 | **0.30** | **0.32** | Z0+0.01 | Chest |
| S4 under the dorsal (back hump) | -0.14 | 0.285 | 0.31 | Z0+0.03 | Chest / Spine |
| S5 hips / saddle | 0.20 | 0.23 | 0.265 | Z0+0.02 | Spine |
| S6 peduncle (taller than wide) | 0.50 | 0.13 | 0.19 | Z0+0.02 | Tail1 |
| S7 fluke root | 0.80 | 0.065 | 0.10 | Z0+0.03 | Tail2 |

- **Side view:** the back rises in a hump under the dorsal, the belly line climbs from S3 to S7, and there is no flat
  bottom. Max girth sits ~33% back from the snout. The head is a rounded melon that tapers to a short rostrum (snout
  ~40% of the max width), not a flat front face.
- **Size:** the dorsal tip is the top. H_MODEL ≈ 1.80. Set **HEIGHT 10**, like Thunder Rex: a secret stands above
  its egg (Turtle 9). The length then drops from ~17 to ~14 studs at x1, which fills the Index square better.
- **L:H:** (lure orb front → fluke tips) : (belly bottom → dorsal tip) ≤ **1.85:1**. Today it is 2.4:1.

**2. Hero piece: the crowned angler lantern (it must read gold + jade at 64 px).**
- **Coronet** (Head bone, so it does not swing with the rod) around the rod root at (0, -0.94, ~0.84):
  - an octagonal GOLD ring of 8 short bars at r 0.075 (the BlackDragon pearl band, `pets/BlackDragon.py` L225-229)
  - 5 GOLD points of heights 0.06/0.09/0.12/0.09/0.06, w 0.028 (Ivonrath crown band, `pets/Ivonrath.py` L235-240)
  - The game camera sees this gold on the head top from behind.
- **Rod:** 4 tapered INK_D segs (w 0.048 → 0.032), P0 (0, -0.94, 0.84) → P1 (0, -0.98, 1.10) → P2 (0, -1.10, 1.32) →
  P3 (0, -1.27, 1.42) → hook P4 (0, -1.36, 1.38). This is a big "?" over the head: the anglerfish silhouette.
  **GOLD rings** at P1, P2 and P3 (hw 0.065, 0.044 long) make the arc read against the black body.
- **Orb:**
  - Centre at (0, -1.38, 1.15), **hw 0.15 (0.30 across, 2.1x v1)**. It hangs below the hook on a GOLD collar
    (0.12 x 0.06).
  - Build it as BlackDragon's faceted pearl (`pets/BlackDragon.py` L222-224): 3 rounded cubes rotated (0,0,0) /
    (0,0,45) / (45,0,0), rnd 0.45, in GLOW. That gives a gem, not a dice.
  - Add a flush HOT glint facet (0.05) on the upper front, and a HOT drip spike at the bottom (0.08 long) so it reads
    as a teardrop lure.
- **Cage:**
  - 5 GOLD fangs from the collar, clasping the upper 2/3 of the orb like a jewel setting.
  - Each fang: a GOLD seg (w 0.035, 0.12) plus a GOLD spike (0.08) bent inward, with GOLD_D inner faces.
  - The orb's lower third and drip tip stay exposed.
  - No fang under 0.03 wide.
- **Placement:**
  - The orb top sits at ~72% of the dorsal-tip height and the rod apex at ~79%.
  - The orb hangs above and just ahead of the snout tip, so the face stays visible below it in the front view.
  - From behind, the game camera's line of sight clears the dorsal.
- **Target:** GOLD 2-3% of pet pixels in tq and game. The orb is a ≥ 6 px jade dot with a yellow rim at 64 px.

**3. Orca pattern blocking (flush, studded, angular in our blocky style, as in f_63).**
Hull blocks are INK. All white and saddle zones are flush inlays, ≤ 0.010 proud, seated with `surf_hit`/`seat_plate`/
`surf_strip` (`pets/CelestialDragon.py` L56-104; keel example L183). They must carry studs like the hull: if
`surf_strip` bars come out smooth because their thinness gives them auto role "detail", pass role="limb".
- **Lower jaw:** a solid WHITE block (Jaw bone). An INK_D lip bar runs along the upper-jaw edge.
- **Belly band:** chin → throat → between the pectorals (~0.40 wide). It narrows to ~0.14 behind the pectorals, then
  ends in a point on the tail-stock underside at y ~0.62. Use 2-3 parallel strips on the curve, not one wide bar that
  floats at its edges.
- **Flank lobes:**
  - A white tongue on each side that rises from the belly behind the pectorals up and back to a point at about
    (y 0.38, z Z0+0.10), ~60% of the local body height.
  - Build it from 3 tapering strips (tip1=True).
  - This is the white the game camera sees on the flanks.
- **Eye patches (the 64 px orca read):**
  - An angular lens, pointed at both ends, from (y -0.97, z Z0+0.04) to (y -0.72, z Z0+0.10), ~0.10 tall at its
    widest. It rises ~12° toward the back.
  - It wraps onto the upper side of the head, so it also shows in the front view and from the game camera.
  - Its front tip meets the back end of the brow, so the patch, the brow and the slit eye form one angry mark.
- **Saddle:**
  - SADDLE grey on the back from y 0.12 to 0.46 at the midline, wrapping down to ~55% of the flank.
  - Its front edge is concave around the dorsal's trailing root, and it ends in a chevron point toward the tail.
  - **Split it at the Tail1 joint** (two pieces, Spine + Tail1), or it tears in the swim.
- **Fluke undersides:** a WHITE plate under each fluke, so the swim downstroke flashes white.
- **Delete:** the proud slabs (L42-58), the pillow saddle (L53) and the box belly (L44).

**4. Face: fierce, and readable from the side, the tq and the game camera.**
- **Eyes:** `fierce_eye()` (`pets/Ivonrath.py` L93-110, or Rex's sc version `pets/ThunderRex.py` L112-127) in
  GLOW/HOT, sc 1.15, yaw 22.
  - Seat the socket on the hull surface with `surf_hit` at about (y -1.00, z Z0-0.05), just above the mouth corner.
  - Brow colour INK_D, angled down toward the snout.
- **Mouth:**
  - The line runs straight, stepping DOWN slightly at the back: a snarl, never the orca "smile curve".
  - Rest jaw open ~8°.
  - Jaw hinge under the eye, behind the last tooth: (0, -0.94, Z0-0.12).
- **Teeth (ivory, conical, seated on the lip edges with `surf_hit`):**
  - Upper: 7 per side, 0.065-0.08 long, w 0.026, the front two longest.
  - Lower: 6 per side, 0.06 long, w 0.024, interlocking half a pitch back.
  - At rest ≥ 6 teeth per side must show in the side view.
- **Mouth interior:** MOUTH roof plate on Head and floor plate on Jaw, as in Rex fix C (`pets/ThunderRex.py`
  L244-245). There is no glowing throat: that is Rex's "charged mouth".
- **Blowhole:** an INK_D slit 0.07 x 0.025 on top at y -0.76 (Blow anchor). Delete the red-speck mouth plate L70.

**5. Fins as tapered, bevelled, studded blocks (no B.poly for dorsal, pectorals or flukes).**
- **Dorsal: the "sovereign blade", the tallest point.**
  - Root on the back from y -0.36 to 0.14 (z ~0.95). Tip at (0, 0.12, ~1.80), 0.85 above the back.
  - The leading edge sweeps back ~29°. The trailing edge is near-vertical and slightly concave (falcate).
  - Build it from 4 stacked INK blocks (chord hy 0.25 → 0.19 → 0.115 → spike tip; thickness hw 0.055 → 0.045 →
    0.037 → 0.03), each shifted back with `top_shift`. The visible steps echo f_63's stepped fin and keep the studs.
  - From the front and back it is a 0.11-thick wedge, not a stick.
  - **Serrations:** 3 INK_D spikes on the trailing edge at z 1.05 / 1.28 / 1.50, pointing back-down (0, 1, -0.35),
    L 0.10 / 0.09 / 0.08, w 0.035.
- **Pectorals: broad rounded orca paddles** (not shark blades, which is Hammerjaw's look).
  - Root (±0.26, -0.50, Z0-0.20), tip (±0.64, -0.30, Z0-0.42), ~0.48 long.
  - Chord 0.24 at the root, 0.30 mid, rounding to 0.14 at the tip. Thickness 0.08 → 0.035. 3 segs.
  - Angled 30° down and 25° back.
- **Flukes: a crescent with swept tips and a centre notch.**
  - Per side, 3 segs: (±0.05, 0.84) → (±0.20, 0.92) → (±0.34, 1.00) → tip (±0.46, 1.12), at z ≈ Z0+0.03.
  - Chord 0.20 → 0.17 → 0.12 → point. Thickness 0.06 → 0.03. Notch at the centre trailing edge (y ~0.96).
  - Generate the arc points with CelestialDragon's crescent math (`pets/CelestialDragon.py` L288-308), but build
    blocks between them, not polys.

**6. Abyssal lights: beads on the body, veins on the fins (one clear, systematic language).**
- **Beads (photophores)** are domed lanterns, never rings (rings are the Kraken's motif):
  - each bead is a GLOW dome (rnd 0.6, ~0.012 proud) plus a HOT centre (≥ 0.024 across)
  - the front 4 per side also get a DEEP socket under the dome
  - seat every bead with `seat_plate`/`surf_hit`, so nothing floats or sinks
  - **Waterline rows:** 10 per side on the INK just above the white boundary, from behind the eye to the tail stock,
    0.065 → 0.04, about 0.15 apart.
  - **Spine row (the game camera's view):** 3 beads on the midline from the blowhole to the dorsal root (y -0.66,
    -0.54, -0.42), then 4 behind the dorsal (y 0.28, 0.42 on the saddle, 0.56, 0.68 on the tail stock). This is a
    runway of lights leading the eye to the lantern.
- **Veins:** flush `surf_strip` (tip1=True), organic: smooth gentle curves forking at ~30°, no zig-zags.
  - **Dorsal:** on both faces, a trunk from the root to ~85% of the height. The trunk is GLOW 0.04 wide with a HOT
    core 0.02 on its lower 2/3, and 2 forward-up branches at z 1.15 and 1.38 (0.16 and 0.12 long).
  - **Pectoral and fluke tops:** 1 trunk and 1 branch each. On the flukes, add a HOT tip bead (trail anchor).

**7. Detail density (target 10-12k tris, cap 15k).**

| part | ~tris |
|---|---|
| hull loft + white/saddle inlays | 2.0k |
| head: jaw, 26 teeth, eyes, brows, patches, mouth plates | 2.0k |
| dorsal: 4 blocks + 3 serrations + veins | 1.2k |
| lantern: coronet, rod + rings, orb, collar, cage | 1.5k |
| pectorals + flukes + veins + white undersides | 1.3k |
| ~27 beads x 2-3 parts | 2.5k |

If it goes over: drop the DEEP sockets on the small beads first, then the waterline row's last 2 beads.

**8. Techniques to copy**

| what | file + lines |
|---|---|
| lofted hull chain (dims list + ext) | `pets/CelestialDragon.py` L277-282; tapered hull blocks `pets/HammerjawShark.py` L34-35 |
| flush seated inlays, keel | `pets/CelestialDragon.py` L56-104 (`surf_hit` / `seat_plate` / `surf_strip`), keel L183 |
| fierce eye + brow | `pets/Ivonrath.py` L93-110 or `pets/ThunderRex.py` L112-127 |
| faceted orb + gold octagon band | `pets/BlackDragon.py` L222-229 |
| gold crown points | `pets/Ivonrath.py` L235-240; gem + gold prongs `pets/ThunderRex.py` L271-299 |
| hot-centre gem layering (glint) | `pets/LavaGolem.py` L108-114 |
| crescent arc maths (flukes) | `pets/CelestialDragon.py` L288-308 |
| mouth roof / floor plates | `pets/ThunderRex.py` L244-245 |
| hover floor rule | `pets/Kraken.py` L214-240 `ground_lift()` |
| vertical travelling wave (swim) | `pets/BlackDragon.py` L294-300 `waves(pitch=...)` |
| chain rotation split (lure rod) | `pets/ThunderRex.py` L436-438 `tail(each=...)` |

### Studio VFX plan (VFX Studio plugin per the owner's rule; the mesh must look great without it, no Neon)
Add empty anchor bones the way Rex did:
- **Bulb**: child of Esca, at the orb centre
- **Maw**: mouth gap at the front, child of Head
- **Glow1/2/3**: on spine beads y -0.54 (Chest), 0.42 (Spine), 0.68 (Tail2)
- **DorsalTip**: child of Dorsal
- **FlukeL/FlukeR**: fluke tips, children of Tail3
- keep **Blow**

The effects:
1. **Bulb (hero):**
   - a jade PointLight (~Brightness 2, Range 12) and a glow billboard
   - slow "marine snow" motes rising off the orb, and a soft pulse every ~3 s
   - in act_lure: a quick flare on each twitch, a big flare on relight
2. **Glow1-3 + beads:** a soft twinkle, a head → tail ripple chain on the `ripple` events, and a fade on `dim`.
3. **Dorsal → DorsalTip:**
   - a Beam along the leading edge with a slow scrolling "current" texture
   - thin dark-ink wisps trailing off the tip while swimming
4. **FlukeL/FlukeR:** pale jade water-ribbon Trails in the swim, and splash rings on the roar `lash` events.
5. **Blow:** the spout on the idle `blow` event (white mist with jade sparkles, ~0.8 s).
6. **Maw:** the `gulp` burst (jade sparks, a bubble ring and a soft shock ring), and bubbles on the roar `clap` events.
7. **Body:** a few slow bubbles rising from Chest, which sells "swimming through the air".
8. **Eyes:** a small jade glow on Head at the eye positions. They go out on `dim` and snap on FIRST at `relight`.
9. **Secret aura:** the same shared sparkle aura as the other secrets.

---------------------------------------------------------------------------------------------------------------------
## 3. Approval checklist for v2 (each item pass/fail; all must pass)

1. **Lineup:** model_tq at the same scale next to Kappa, SeaTurtleWarrior, Kraken, Hammerjaw, Thunder Rex and Ivonrath.
   - It is clearly the most striking pet of the Tide egg.
   - It does not read as a Hammerjaw variant: no plates, spike row or poly fins.
   - It does not read as a Rex palette-swap: no crystals or seams.
2. **64 px test** on slate with an outline (the real icon pipeline, not an opaque crop). You can name 3 things:
   - an orca (white eye patch ≥ 3x2 px plus the dorsal blade)
   - a glowing lantern with gold
   - the black/white pattern

   The 5.5% Hammerjaw icon must not out-read it.
3. **Value blocking:**
   - side and tq: INK ≤ 55%, WHITE ≥ 20%, SADDLE ≥ 4%
   - game cam: INK ≤ 62%, WHITE + SADDLE ≥ 15%
   - back view: sky glare ≤ 8%, which proves the flat polys are gone
4. **Accent:**
   - GLOW family 8-14% in tq and game. Every bead shows GLOW + HOT, and every vein trunk has a HOT core.
   - **GOLD ≥ 1.5% in tq and game** (target 2-3%), with gold visible on the head top from the game camera.
5. **Silhouette:**
   - The dorsal tip is the highest point. The orb sits at 60-80% of the total height, above and just ahead of the
     snout tip.
   - L:H ≤ 1.85:1. Max girth is at 30-40% from the snout. The belly line rises into the tail stock. The peduncle is
     taller than wide.
   - From the front and back, the dorsal is a wedge (≥ 0.10 thick at the root), not a stick.
6. **Face (close sheet, 700 px):**
   - Slit eyes are visible in the side view and the 3/4 front, under a V brow, with the white patch flush behind
     and above them.
   - The open mouth shows ≥ 6 teeth per side, all ≥ 0.024 wide. The mouth interior is dark (no studded INK).
   - No red specks and no tabs on the head sides in the front view.
7. **Fins:** no `B.poly` on the dorsal, pectorals or flukes. All are tapered, bevelled and studded.
8. **Hard rules:**
   - no Neon; ≤ 15k tris
   - INK luminance ≥ ~70
   - white/saddle zones are flush (≤ 0.010) and studded
   - nothing floats or is buried: every inlay, bead, eye and tooth is `surf_hit`-seated
   - no detail under 0.02 (the fierce_eye pupil excepted)
   - no two touching blocks within ±10% except matched-end loft joints with no visible step or pinch
9. **Rig:**
   - The Bulb anchor is at the orb centre.
   - Maw, Glow1-3, DorsalTip and FlukeL/R exist.
   - The check pairs include the new ones in section 4, and `collision_free: true` holds.
10. **Deliverables:**
    - model sheet (tq, front, game, side, back) and a 600 px tq
    - face close sheet
    - a game-camera render at ~38°
    - a 64/128 px icon strip on slate with the Tide egg siblings + Thunder Rex, plus the pixel-share table

---------------------------------------------------------------------------------------------------------------------
## 4. Animation, rig and the signature act

### Rig (pivots for the v2 hull; Z0 = 0.62)
- **Body chain:**
  - Spine (0, -0.05, Z0), child of Root
  - Chest (0, -0.42, Z0)
  - **Head at the throat, low/back** (0, -0.80, Z0-0.08)
  - Jaw (0, -0.94, Z0-0.12)
  - Tail1 (0, 0.26, Z0+0.02), Tail2 (0, 0.50, Z0+0.02), Tail3 (0, 0.79, Z0+0.03)
- **Fins:** Fin_L/R (±0.26, -0.50, Z0-0.20), children of Chest. Dorsal (0, -0.10, ~0.95), child of Spine.
- **Lure chain: one rod bone cannot dangle.** Use three bones:
  - **Lure** (rod root, (0, -0.94, 0.84), child of Head)
  - **Lure2** (P2 (0, -1.10, 1.32), child of Lure)
  - **Esca** (hook P4 (0, -1.36, 1.38), child of Lure2; the orb hangs below it like a pendulum)

  The coronet stays on Head. Blow (0, -0.76, ~0.91) stays on Head.
- **Weights:**
  - Every inlay rides the bone of the hull under it.
  - Split the saddle and the flank lobes at the Tail1 joint.
  - Keep ≥ 0.10 between the dorsal's trailing root and the Tail1 pivot, or tail-up flexes push Tail1 into the
    serrations.
- **check_pairs, add:**
  - (Esca, Head), (Esca, Jaw)
  - (Lure2, Dorsal), (Esca, Dorsal)
  - (Tail1, Dorsal), (Tail2, Dorsal)
  - (Fin_L, Chest), (Fin_R, Chest) for the fold pose
  - keep the v1 pairs
- **Pose limits:**
  - Head pitch ±10°, yaw ±15° (a whale has no neck: share turns with Chest ±8°)
  - Jaw ≤ 45°
  - Lure + Lure2 back-rotation ≤ 45° total (verify the dorsal clearance at that pose)
  - Tail1/2/3 pitch ±16 / ±24 / ±32
  - Spine roll ≤ 22°, with the low-side pectoral raised 15°
  - Run Kraken's `ground_lift()` in every clip: the pectoral tips are the lowest vertices.
- **Same-egg note for the coordinator:** Hammerjaw should swim with a LATERAL (yaw) tail sweep, as sharks do. The
  orca swims with a VERTICAL fluke drive. Then the two Tide swimmers never share a cycle.

### swim (36 f loop, 1.2 s): "FLUKE DRIVE", a dorsoventral wave, in place
- A travelling pitch wave down Spine → Tail1 → Tail2 → Tail3 (BlackDragon `waves(pitch=...)`, lag ~0.08 per bone).
  Amplitudes ±2.5 / ±7 / ±13 / ±22.
- **Asymmetric:** the power downstroke takes 45% of the cycle, the recovery upstroke 55%.
- Spine loc z +0.035 at the end of the downstroke, -0.02 at the end of the recovery.
- The head is stabilised (counter ≤ ±1.5°). Pectorals hold a 10° dihedral and trim ±5° with the heave.
- The lure follows through: Lure ±3, Lure2 ±6 (lag 4 f), Esca pendulum ±10 (lag 6-8 f).
- The dorsal is rigid. Roll ≤ ±2°.

### idle (120 f): "SOVEREIGN PATROL & BLOW"
- A slow heave (z ±0.03, 2 cycles), 2 lazy fluke beats (Tail 4/8/12), alternate pectoral sculls (±6), and the lure
  pendulum lagging behind.
- **f30-58, spyhop glance:** nose up (Spine -8, Head -4), then ONE slow look left and ONE slow look right (Chest ±6,
  Head ±10), each ~8 f with a ≥ 8 f hold. Not a shake.
- **f62-70, the BLOW:** the head dips 3°, the body rises 0.04, event `blow` f66, and the pectorals flick 8°.
- **f80-110:** a lazy 14° roll that shows the white belly to the camera, and back. Loop closed.

### roar (64 f): "JAW-CLAP THREAT" (real orca threat display; in place, NOT a rear-up, which is the Kraken's roar)
| frames | beat | keys |
|---|---|---|
| 0-12 | gather | Spine loc y +0.06 (draws back), nose up -6, jaw 10, pectorals tucked back 15, flukes cocked down +12 |
| 12-20 | face-off | snaps forward to y -0.04, nose DOWN +10 (at the viewer), jaw 44 by f20, pectorals flare out and down 30 (brake display), the lure thrusts forward over the snout (Lure +14, Lure2 +10); event `roar` f20 (Maw bubbles, Bulb flare) |
| 20-44 | 3 JAW CLAPS | f26 / f32 / f38: jaw 44→12→44 in 2+3 f (events `clap1-3`), a ±2 jaw buzz between claps; two vertical tail LASHES f24 / f36 (Tail chain -18 → +22, events `lash1/2` on FlukeL/R) |
| 44-64 | release | the jaw closes slowly, the body settles to 0, the lure swings back with an overshoot, ends at rest |

### SIGNATURE `act_lure`: "THE ABYSSAL LURE" (the angler ambush), 120 f, in place, ends exactly in rest
The orca switches its own lights off, dangles its lantern in front of its jaws as bait, twitches it, then GULPS. When
it relights, the photophores ripple back on from head to tail.

Why it is unique in the roster:
- It is the only act that uses the pet's own body part as bait.
- It is the only act built on a lights-off / lights-on show (it drives the Bulb, Glow1-3, Maw and eye VFX).
- It has no breath (Rex, Ivonrath), no airborne spin (Raiju, BlackDragon), no coil (Kraken), no rear-up, and no leap
  or pin (ShadePanther's pounce leaps and pins; this stays put and strikes from a hover).
- It is in place: the lunge is 0.22 units, ~1.2 studs at x1.

| frames | beat | keys (rot in deg; + = nose/fin/tail down) |
|---|---|---|
| 0-12 | **lights out** | fluke beat stops; Spine z -0.05, pitch +5; Fin_L/R fold back 20 / up 8, kept ≥ 0.02 off the hull; event `dim` f6 (beads, veins, eyes fade; the orb stays lit) |
| 12-42 | **the dangle** | Lure +16, Lure2 +20: the orb drops to ~0.10 ahead of and 0.12 above the snout tip (≥ 0.04 clearance). **3 bait twitches** at f20/28/36: Esca ±12 and Lure2 ±4 in 2 f, then a 5 f hold. The body is dead still apart from a ±0.01 breath; Head +3 (it watches the bait); events `twitch1-3` |
| 42-56 | **draw back** | Spine loc y +0.10; Chest -4, Head -5; Jaw slowly to 14 (unhinging); Tail1-3 cock +8/+12/+16 (loading); pectorals flare 12 (brake); Lure counter-rotates so the orb stays where it hung |
| 56-58 | **lure up** | Lure -18, Lure2 -24: the orb whips up and back out of the strike line BEFORE the jaw opens wide, so no tooth ever crosses the orb |
| 58-62 | **GULP** | one hard fluke kick (Tail1-3 -14/-22/-30 at f59); Spine loc y -0.12 (0.22 in 3 f); Head +6; Jaw 44 at f59, then **SHUT at f62** (hard stop); event `gulp` f61 (Maw) |
| 62-90 | **savour** | the jaw stays shut; 2 swallow pulses (Chest -2 at f66 and f72); a lazy 22° roll showing the white belly (f64-90), with the low-side pectoral raised 15° |
| 90-104 | **relight** | the lure swings back to rest with an overshoot (Lure +6 → 0, Esca 10 → -5 → 0); event `relight` f92 (orb flare, eyes snap on); `ripple` f96 with Glow1 f96, Glow2 f100, Glow3 f104 |
| 104-120 | resume | 2 soft fluke strokes, back to the rest hover |

- Ease into the twitches. Use hard stops on f59 (strike) and f62 (jaw shut).
- No head shakes anywhere: the twitches live on Esca, and the savour is a roll, not a shake.
- **Return for the gate:**
  - a pose sheet at f6, f28, f50, f57, f60, f62, f78 and f96
  - `collision_free: true`, `ground_min_z` ≥ -0.02 in all 4 clips, linear 0, loops closed

---------------------------------------------------------------------------------------------------------------------
## 5. Summary for the coordinator
- **Mesh: REJECT, 2.5/10.** Rebuild it to this brief and keep the concept.
- **In order of impact:**
  1. a lofted torpedo hull with a hump, melon head and tall narrow peduncle
  2. a 0.30 jade orb in gold fangs on a gold-ringed rod, with a gold coronet
  3. a flush, studded orca pattern: eye-patch lens, belly band, flank lobes, saddle
  4. a fierce face
  5. fins as stepped studded blocks, never polys
  6. jade beads on the body and veins on the fins
- **Palette:**
  - INK goes up to (64, 70, 102).
  - MINT is replaced by GLOW jade (30, 236, 160) with a teal DEEP and a green-white HOT.
  - GOLD is reserved for the lantern.
- **Answers to the builder's worries:**
  - Low detail: yes, but fix the shape first.
  - Small cube bulb: yes. Make it 2.1x and faceted.
  - Blocky body: yes. It breaks lesson #1.
  - Mint vs cyan: keep the Tide aqua family, but make it a saturated jade and separate it from Rex by form.
- **Signature:** `act_lure`, as specified. Also: idle "patrol & blow", roar "jaw-clap threat", swim "fluke drive"
  (vertical).
- **Next round:** I review the v2 model with the section 3 checklist before any clip is authored.
