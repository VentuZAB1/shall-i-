# Venom Basilisk - art director review 2 (2026-10-14) - APPROVE WITH FIXES (model)

**Score: 7/10 for a 5% rare** (v1 was 5/10). All 8 fixes from review 1 landed, and they landed as specified.
- It now reads as **a viper-headed lizard with a violet crown fan**: a dark back, sabre fangs and a sprawled stance.
- At 64 and 128 px it clearly outclasses Treant, and it no longer reads as a recoloured Ivonrath.

Four issues are left: two older problems that only show in close-ups, and two that the v2 changes created. All four
are small and codeable, and **none of them changes a bone name, a joint or the rest pose. You can start the clips
now.** Fixes 1-4 must be in the mesh before export. I'll check them in the clip review (send the renders listed at
the end); there's no separate model round.

What I looked at:
- `pets/VenomBasilisk.py` v2
- `_model_sheet` and `_close_sheet`
- my own renders (temp, outside the project):
  - the 5 standard views at 520
  - a top-down render, a head from the top and a head from the side
  - a high tq at the icon angle
  - a front close-up
  - a game-camera head close-up and a back-of-frill view
  - a flank close-up at belly height and a sail close-up in tq
- an icon-pipeline portrait (`icon3` outline recipe on slate) of **v2 and of v1** (rebuilt from
  `_tools/rex_versions/VenomBasilisk_v1.py`)

Evidence in this folder:
- `VenomBasilisk_r2_icons.png`: Grass egg + VB v1 + VB v2 + Ivonrath + Panther at 64/128 px
- `VenomBasilisk_r2_issues.png`: 4 labelled close-ups of the remaining issues

How I measured: I removed the background and classified the green by hue, which is bimodal. HIDE renders at
~130-140° and DORSAL at ~150-165°. Shaded hide falls into DORSAL, so DORSAL reads a few % high. Figures are ±3%.

| view | light / mid / mid-dark | DORSAL | HIDE | PALE | violet (of which frill) |
|---|---|---|---|---|---|
| side | **11** / 41 / **48** | 37 | 39 | **4.1** | 15.4 (frill edge-on; sail 55%) |
| game cam | **6** / 38 / **55** | 51 | 30 | 0.6 | 16.1 (**69%** frill) |
| back 3/4 | 10 / 42 / 48 | 41 | 35 | 0.9 | 20.9 (**65%** frill) |
| tq | 19 / 39 / 41 | 35 | 34 | 2.3 | 22.6 |
| v1 side, for reference | 30 / 46 / 23 | - | - | 2.6 | 14.4 |

Size: 1.11 × 2.97 × 1.39 (L:H 2.14), 6,276 tris.

---------------------------------------------------------------------------------------------------------------------
## 1. Review-1 checklist - item by item

1. **64/128 px strip - PASS.** You can name a lizard, a violet crown-fan on the head (now separate from a darker
   sail) and even the white fangs. The stripes don't resolve at 64 px, but the dark back does, which is enough. It
   reads rarer than Treant and holds its own next to Ivonrath. The difference from v1 is obvious side by side.
2. **Value - PASS except PALE.**
   - Light band is 11% (side) and 6% (game), down from 30%. Mid-dark is 48% and 55% (target ≥ 40).
   - The DORSAL/HIDE split is in range. Violet is 15-16%, with 65-69% of it in the frill from the game and back
     cameras.
   - **PALE is 4.1% in the side view against a 7-10% target.** The cause is construction, not size (Fix 2).
3. **Frill - FAIL (narrow).** It is the highest point and the brightest violet; the leaf read is gone, and the bone
   points read. But the outline has **9 membrane points and only 7 bone points.** The boundary panels' ±15°
   pseudo-spine corners poke ~0.05 past the centre panel's scallop notch (centre notch at 15° ≈ 0.417 from the
   root; pseudo corner 0.54 × 0.86 ≈ 0.464). They are visible from the front and from behind (issues sheet, panel 2).
   Fix 1.
4. **Head from the top - PASS.**
   - The cheeks are 1.7× Neck2 and the snout tip hw is 0.06: a clear coffin/arrowhead.
   - The V marking is in, and none of Ivonrath's parts remain.
   - No dark slot at the neck pinch in the back view; the frill collar covers it.
5. **Face - PASS, with cleanup.**
   - Lilac slits read from the front and at the icon angle.
   - One horn per side.
   - The sabre fangs read from the side, front and tq. This is the best single upgrade.
   - The nostrils are at the tip.
   - **But** the snout front now carries 5 black marks: 2 nostrils, 2 heat pits and the rostral notch. From the
     front that is a little "face on the face". Fix 5.
6. **Pattern - FAIL.** Fix 2.
   - **The stripe teeth start just below the shell's rounded lip.** A ~0.02 strip of hide shows between the shell
     and every tooth, so the teeth read as dark flags pinned to the flank, not stripes growing out of the back.
   - **The teeth run through the belly band.** The chest teeth reach z ≈ 0.355; the band spans 0.32-0.51.
   - **The underside is two cream planks with a green plank between them** (the flank band made of `surf_strip`
     bars with visible steps, the HIDE tuck seg, then the old PALE belly seg) instead of one pale underside.
     Issues sheet, panel 1.
7. **Proportions - PASS.**
   - L:H 2.14 against a target of ≤ 2.1. Accepted; don't add length.
   - Chest hw 0.245.
   - Correction to my own checklist: the LEGS numbers I gave put the feet at x 0.40, just *inside* the elbows
     (0.42), not outside them. What matters is a wide sprawl (feet at 2× the hip x), and that reads clearly from the
     front, the top and the game camera. PASS as built.
8. **Hard rules - PASS (collision pending).**
   - No Neon; 6.3k tris; nothing floats; no gold; hue is true green (well clear of the Mantis's jade).
   - The ivory tips are smooth.
   - `collision_free` runs with the clips, as you said.
9. **Deliverables - partial.** I made the high-tq crop, the top-down render and the icon strip myself this round.
   Include them next time (list at the end).

**New issue introduced by v2: the sail reads as a grille** (issues sheet, panel 3). It is six *parallel*, studded,
dark-green rods standing on a smooth deep-violet half-disc, with the ivory tips barely clear (reach 0.92). In tq it
reads as a barred window or a radiator. Fix 3.

**Old issue I missed in review 1: the tongue is buried in the lower jaw.** The tongue is at z 0.678-0.698; the lower
jaw spans 0.644-0.706 at the front. Any slide-out flick will push it out through the *chin's* front face, below the
lip. Fix 4.

---------------------------------------------------------------------------------------------------------------------
## 2. Fixes, ranked (all in `pets/VenomBasilisk.py`)

### FIX 1 - Frill outline: 7 points, each with a bone tip (MUST; L261-278)

Today's boundary panel runs from a ±15° pseudo-spine (L 0.54) to the ±58° spine. That creates the phantom points,
and it also makes 30°→58° one wide sagging scallop with no membrane point at the 30° spine. Replace it with two
pieces per side, both on the outer bone:
- **(a) A visible boundary panel from the ±30° spine to the ±58° spine.** Use `web(B, [roots[4], roots[5]],
  [tips[4], tips[5]], 0.02, (VENOM_DEEP, VENOM_L), "Frill_L")`, mirrored for R with `roots[2]/roots[1]`. Same reach
  and scallop as the centre panels, and no `nback`; it shares the 30° spine edge with the centre panel.
- **(b) A hidden under-flap from ±15° to ±30°,** 0.008 behind the centre membrane (`nback`), so the outer group can
  spread 15° without opening a hole.
  - Build it as a panel between two pseudo-spines: ±15° with **L 0.44** and ±30° with **L 0.50**, at reach 0.86 and
    scallop 0.
  - At rest its corners sit at ~0.38 (15°) and ~0.43 (30°) from the root, safely inside the centre panel's edge
    (0.417 notch, 0.447 corner).
  - Give it the same two-tone (DEEP to 0.35, VENOM_L beyond). From behind, which is the game camera, it then shows
    only as a faint edge line instead of a dark wedge.
- **Verify:**
  - the front and back outlines each show exactly 7 points, all with ivory tips
  - with Frill_L/R rotated +15° in the fan plane (a quick pose test), there is no hole between 30° and 45°

### FIX 2 - One pale underside; stripes that grow from the back and stop above it (MUST; L184-209)

- **Delete** the flank PALE `surf_strip` band and its scute bars (L198-209), the brisket plate (L196) and the
  belly seg (L197).
- **Make the tuck seg (L179) PALE.** It *is* the belly.
- **Add a pale under-shell to each torso block.** Mirror your `shell()`: z from `-h.z - pad` up to **`-0.50·h.z`**,
  using `prof(b, -b.h.z)` / `prof(b, zb)` for the tapers. Use PALE, pad 0.012, rnd 0.3, covering the full block
  length. That gives one clean cream form per block that follows the tapers and wraps up the lower flank, like the
  approved belly reads on Stag and Cerberus.
- **Scute gaps.** Add 4 PALE_D bars per side on each under-shell's flank face (vertical, 0.014 wide, flush via
  `side_pt`). The side view then shows scute rows.
- **Stripe teeth (L187-194):**
  - **Start each tooth 0.03 above the shell edge,** tucked under the shell's rounded lip (`lz = za + 0.03` for the
    top two points). Thickness 0.012 → **0.016**. That removes the hide gap.
  - **End each tip 0.02 above the under-shell:** length = `0.80·h.z - 0.02`, i.e. chest ≈ 0.13, waist ≈ 0.09,
    hips ≈ 0.10 (was 0.22 everywhere).
  - Keep the 0.10 top width and the backward slant. The flank then reads dark back → teeth → green → cream belly.
- **Target:** PALE 7-10% in the side view. If the under-shell lands under 7%, raise its top edge to `-0.45·h.z`
  and shorten the teeth to match.

### FIX 3 - Sail: a spined crest, not a grille (MUST; L282-289)

- **Sail thorn shafts → VENOM_DEEP** (`col=VENOM_DEEP`), so they read as ribs inside the membrane instead of bars in
  front of it.
- **Fan the spines.** Give each spine its own lean back from vertical, front to rear: **8, 13, 18, 23, 28, 33°**
  (`sd_i = (0, sin a_i, cos a_i)`). Today all six share `sd`, so they are parallel. LESSONS #5: parallel blades read
  as fingers or bars.
- **Web:** `reach 0.92 → 0.80`, `scallop 0.12 → 0.20`, `inner 0.75 → 0.60`.
  - The ivory points then stand clear the way they do on the frill, and the VENOM edge becomes a row of points.
  - The sail stays clearly darker and lower than the frill.
  - Same family language, smaller and dimmer: the frill's little brother.

### FIX 4 - Tongue at the lip line (MUST before the idle/roar flicks; L248-251, rig L345)

- Raise the tongue seg and forks from **z 0.688 to 0.703**, and move the `Tongue` joint to match. Its top then sits
  at ~0.713, on the jaw top and under the snout bottom (0.715 at the tip, 0.725 mid-snout). It no longer sits inside
  the lower jaw.
- In the clips, every flick opens the Jaw **3-4°**, so the tongue slides out through the lip gap. The rostral
  notch isn't needed (Fix 5).

### FIX 5 - Snout cleanup (SHOULD; L223, L227-228)

- **Delete the rostral notch block (L223) and both heat pits (L227-228).** I asked for the pits; you were right that
  they risk reading as eyes. At x1 they are ~0.13 studs, so they are invisible in game. In close-ups they only add
  black dots, and together with the notch the snout front shows 5 dark marks. Keep the two tip nostrils.

### FIX 6 - Break up the dorsal slabs (SHOULD, polish)

From the game camera, ~50% of the pet is three large, plain, glossy dark shells.
- Add **2 transverse seams per torso shell**, as flush bars on the shell top: 0.018 wide, colour **(40,104,64)**
  (a lighter dorsal, not HIDE, so they read as plate rows and not as stripes).
- Put them at the y positions between the stripe teeth (≈ -0.29, -0.07, 0.15, 0.31).
- The back then reads as scute rows that continue the tail rings.

### FIX 7 - Venom-gland cheeks in the roar (CHECK during the clips)

The cheek block (0.205 wide, the widest part of the head) is on **Jaw** (L221). At roar jaw ~36° the whole
cheek mass tilts with the lower jaw, which can read as the head coming apart from the side. If it does in the
roar pose sheet, move the block to **Head**, raise it to z ≈ 0.715, and check that the lower jaw clears it when
open. (Ivonrath keeps its jaw muscle on Jaw, but it is only 0.13 wide.)

---------------------------------------------------------------------------------------------------------------------
## 3. Clips - go ahead

- Use the review-1 **ACT_DASH** beat table as written. With the split frill: at the f59 flash, the outer groups
  spread +15° while the centre snaps upright; at f20-56 they fold back -5° with the whole fan.
- **Idle:**
  - tongue flicks: the Jaw opens 3-4° (Fix 4)
  - look-around ~±25°
  - frill twitch ±4°
  - tail S-curve
- **Walk:** S-sway from Spine yaw ±8 plus tail plus Neck ≤ 8 (Chest vs Spine ≤ 5); wide arcing swings for the sprawled
  feet.
- **Roar:** a slow frill rise (~10 f) with the outer groups spreading +15°, jaw ~36°, tongue fully out, Head+Neck ≤ 30.
- Run `collision_free` on all four clips, with particular attention to:
  - Frill_L/R against Neck/Neck2 and the front legs during the dash tuck
  - the tucked front feet against the jaw and cheeks
  - the tail against the ground during the rear
- Also: `ground_min_z ≥ -0.006`, slide 0 in the planted ranges.

**Send with the clip review:**
- a model sheet including the game view
- a flank close-up at belly height (side, target z ≈ 0.45)
- a front close-up
- a back-of-frill view (camera behind the head)
- the icon-pipeline 64/128 strip with the Grass egg
- the pose sheets: dash f10/20/30/46/55/60/86, including one game-camera frame at f30; roar peak; idle tongue frame;
  walk contact

I'll sign off Fixes 1-4 from those renders together with the clips.
