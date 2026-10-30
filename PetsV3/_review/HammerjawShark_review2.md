# Hammerjaw Shark - art director review 2 (2026-10-14) - REVISE (targeted), then animate

**Score: 7/10 for a 5.5% pet (v1 was 4/10).** This is now a war-hammerhead and clearly one of ours. Several things
land:
- the lofted fusiform hull and the no-neck head
- the T-head as the widest element
- the dark armoured back with coral seams
- the crisp white belly, the tall falcate dorsal and the heterocercal tail
- the fierce eyes and the teeth showing in the tq view

In the lineup it is the most complex Tide pet and it reads "shark", never "plane". **Do not redesign anything.** What
is left is finish work, in six codeable fixes:
- one hard-rule failure: floating keels and scars
- one lost feature: the gills
- three noise problems: bead-chain fin edges, a monotonous stripe rhythm, a padded hammer front
- one checklist count: the second notch

Fixes 1-6 should take it to about 8-8.5. **Once they are in, start animating.** No separate model round is needed;
send the new sheets together with the first clip pose sheets (see section 5).

What I looked at:
- v2 `pets/HammerjawShark.py`
- `_model_sheet`, `_close_sheet`, all 5 model renders and the 3 close renders at full size
- PIL crops of the side and tq details
- my own icon strip: the real `Kappa/SeaTurtleWarrior/Kraken_icon.png` next to icon3-style outlined cut-outs of the
  shark's tq and game renders on slate, at 64 and 128 px
- a 0.6x "in-game" darkened game and side view on grass

How I measured: the same flood-fill classifier as review 1, with one change. The ARMOR/STEEL split now uses hue as
well as value. ARMOR clusters at hue 216-222 and STEEL at 204-212; at value alone, lit lame tops overlap shaded steel.
The figures are approximate, ±3%.

| view | ARMOR | STEEL | BELLY | coral family (CORAL_D+CORAL+HOT) | SCAR | v1 → v2 |
|---|---|---|---|---|---|---|
| side | **34.6%** | **37.3%** | **13.0%** | 8.3% | 1.7% | STEEL 84 → 37, BELLY 4 → 13 |
| game cam | 44.9% | 32.7% | 6.2% | 7.1% | 1.9% | ARMOR 5 → 45 |
| tq | 45.8% | 27.7% | 5.6% | 12.4% | 1.4% | |
| back 3/4 | 37.2% | 38.8% | 9.6% | 4.4% | 1.9% | |
| front | 41.8% | 30.0% | 5.9% | 12.0% | 1.0% | |

Geometry checks:
- L:H is 2.02 in the side render and 2.19 by geometry: 2.50 long (hammer edge -1.16 to caudal tip 1.34) by 1.14 tall
  (pectoral tip 0.30 to dorsal tip 1.44).
- Hammer span 1.08 vs pectoral span ~0.98 including the coral edge.
- Caudal upper lobe ≈ 0.65 vs lower ≈ 0.26 (2.5x).
- Tris 7.6k.

---------------------------------------------------------------------------------------------------------------------
## 1. Review-1 checklist - item by item

1. **Lineup - PASS.**
   - On the 64/128 strip it is the most detailed Tide pet, and it holds its own next to SeaTurtleWarrior's trident.
   - It reads "hammerhead", not "jet". The game-camera icon is an instant T.
   - Nothing about it says Thunder Rex.
   - The only lineup weakness is noise: the back is a regular stripe pattern (fix 4).
2. **64 px test - PASS (narrow, 2.5 of 3).**
   - Hammer T: yes. It is strong in the game view and OK in the tq view.
   - Coral-seamed armour: yes.
   - Teeth: only a faint white smudge under the hammer.
   - The coral eyes are 1-2 px.
3. **Game camera - PASS, with one miss.**
   - The hammer is the widest element: 1.08 vs ~0.98, just over the +0.10 rule.
   - The lames read as segmented armour.
   - The helm reads as a coral-outlined T.
   - **The brow spikes do not read** at this distance (fix 5).
4. **Value blocking - FAIL (narrow).**
   - Side: ARMOR 34.6, STEEL 37.3 and BELLY 13.0 are all on target. The three bands are there, and it is a
     different pet from v1.
   - **Coral is 8.3% in the side view (target 9-14) and 7.1% in the game view (target ≥8).** The main reason is that
     the gills are almost invisible (fix 1).
   - ARMOR is 45.8% in tq, just over the 45% cap, and 44.9% in the game view, right at it (fix 4).
5. **Silhouette - FAIL (one count).**
   - L:H, the dorsal as the highest point, the 2.5x caudal ratio, no section steps and no neck: all pass.
   - **Only 1 bite notch** (target ≥2) (fix 6).
   - Length is 2.50 against my ≤2.45. I waive that, because L:H passes, and L:H was the point of the limit.
6. **Face - PASS.**
   - The eyes show at both lobes in the front and tq views.
   - The mouth rests open with a dark interior.
   - The upper teeth sit outside the lip, and two rows show in the tq.
   - There is no visor band and no front nostrils.
   - Not blocking, but fix 2 is needed: the head keel floats and reads as a suitcase handle from the front.
7. **Fins - PASS on construction, FAIL on finish.**
   - Studded roots, thickness taper, falcate shapes and the 3-step coral are all there.
   - But the coral edges read as **bead chains** in the close-ups and as a **striped rod** on the dorsal from the
     front (fix 3; this is your question d).
8. **Hard rules - FAIL: things float.**
   - Studs, no glow, 7.6k tris and H_MODEL = the dorsal tip all pass.
   - **The keel planks on the lames and on the head float 0.02-0.03 above the surface.** You can see sky under them
     in close_side, and close_front shows the head keel as a handle.
   - **The scars bridge the seam recess** and stick out as pink sticks.
   - Fix 2 covers both.
9. **Family and egg fit - PASS.**
   - fierce_eye construction; PITCH formula; STEEL's brightest channel 180.
   - No gold, and no black/white orca blocking.
10. **Rig readiness - PASS, except H.**
    - A, B, C, D, E, F, G, J and K: pass. Tail4 is in. The head pivot is at the throat inside the chest. The dorsal
      fairing starts at the Chest pivot, so the shear is ≤0.006 at ±12°. The pelvics are on Tail1. The sections
      telescope. The fin pivots are at mid-chord. Mouth roof and floor are in. The anchors and the pairs are in.
    - **H is pending: the contact test render was not delivered.** My geometry check is in section 4. It passes only
      if the jaw is **closed** at the strike.
11. **Deliverables - PARTIAL.**
    - Model sheet, close sheet and game render: delivered (520 px; please render the tq at 600 next time).
    - Missing: the contact test render and the 64/128 icon strip. I built my own strip for this round.

---------------------------------------------------------------------------------------------------------------------
## 2. Fixes, ranked by impact (line numbers are v2 `pets/HammerjawShark.py`)

### FIX 1 - Bring the gills back (v1's best read; it also fixes the coral share). L199-201, L209-216, L234-242
Right now only ~0.04 of each 0.15-0.21 gill is visible, for two reasons:
- **The lame teeth hide the top half.** The jagged teeth on lames 1-2 are 0.09 wide along y (hy 0.045) and spaced
  0.054 apart. That makes a continuous dark fringe from zc+0.046 down to zc-0.05, right over the gill tops.
- **The belly shells bury the bottom half.** The shells are lofted with `grow=0.008`, so they sit 0.008 proud of the
  hull. The gill strips are seated on the hull (`gl = body[:2]`, `proud=0.006`), so everything below zc-0.094 sits
  *inside* the belly shell.

Fix:
- **Skip the jagged teeth on lames 1 and 2** (`if i < 2: continue` before the teeth loop). The five gill slashes
  become the "jagged edge" there.
- **Seat the gills on the outermost surface.** Keep the return values of the belly lofts (L199-201) and use
  `gl = body[:2] + belly[:2]`, so the strips ride on top of the white shell.
- **Make them span the belly line:** zt = zc + 0.01, zb = zc + 0.01 - h, with heights 0.20/0.21/0.20/0.18/0.15. Coral
  on white is the strongest contrast this pet has. Keep the MOUTH slit plus CORAL flap pairing.
- **Target:** coral family ≥9.5% in the side view, and ≥8% in the game view once fix 4 lands.

### FIX 2 - Nothing floats: seat the keels and the scars (hard rule). L217-220, L283, L244-252
- **Lame keels (L217-220):**
  - The problem: the keel's bottom is only 0.002 under the lame top at the centre. The lames are rounded (rnd 0.42,
    a ~0.035 bevel at their front and rear edges), so both keel ends float 0.02-0.03.
  - The fix: for each lame, `surf_hit` straight down at y0+0.03, the middle and y1-0.03 onto `[lame]`. Build the
    keel through those hits with your `strip()` (L104): width 0.05, thick 0.035, `proud=0.027` (bottom 0.008 under the
    surface).
- **Head keel (L283):**
  - The problem: its bottom runs z+0.160 → z+0.187, over a head core whose top is ≈z+0.16, so there is a 0.02-0.03
    gap behind the helm. From the front this is the "suitcase handle".
  - The fix: the same `strip()` through 4 hits at y -1.10 / -0.98 / -0.86 / -0.76 onto `[helm cap, head core block,
    lame_blks[0]]`. Keep the core's return value from L254.
- **Scars (L244-252):**
  - The problem: straight bars through 3 hits on a rounded lame cut across the seam recess and stand off the
    surface as pink sticks.
  - The fix: use **6 hit points** per gouge, put all three gouges **on lame 2 only** (y -0.52..-0.37, so they never
    cross a seam), use `proud=0.004`, and keep them parallel (the same slope, offset in y only).

### FIX 3 - Fin edges: a flush blade edge, not a bead chain or rod (your question d). `edge3` L140-161; calls L183, L330, L361
**Keep the 3-step coral edge, but make it part of the fin.** Four things cause the current look:
- 4 rounded sub-segs per colour step make the bead chain.
- `top=tp` on the last sub-seg of *each* step makes chevrons at the colour joins.
- The edge sits *in front of* the fin (`out=-c*0.012`).
- On the dorsal the edge is wider than the fin: edge hw 0.028 vs a top-block half-thickness of 0.022. That is the
  coral rod you see from the front.

Fix:
- `n = 2` sub-segs per step, `rnd=0.12`, and `top=(1, 1)` everywhere except the very last CORAL_HOT sub-seg
  (keep (0.25, 0.4) there).
- `out = Vector()` and `ext=0.01`, so the edge is buried 0.01 into the fin.
- **hw ≤ 0.9 x the local fin half-thickness.** Give `edge3` an `hw1` and taper it along the edge. Dorsal: 0.040 →
  0.018. Pectorals: 0.038 → 0.018. Caudal lobes: 0.034 → 0.016.
- **Less red.** Change the colour split to CORAL_D 0-0.20 / CORAL 0.18-0.80 / CORAL_HOT 0.78-1.0. The current
  CORAL_D share (42%) reads as raw meat.
- From the front, the dorsal should then show a thin coral line on a steel blade.

### FIX 4 - War-back rhythm: plates, not loaves, getting smaller toward the tail. L203-233
Now there are 6 equal lames, 5 equal seams and 3 rings: 14 equal beats that read as a tiger or wasp stripe. Each lame
is also a rounded pillow (rnd 0.42, grow 0.024) separated by 0.011-deep coral trenches.

- **Graduated lames.** The lengths go 0.22 → 0.11 and the seams 0.045 → 0.025, so the rhythm speeds up toward the
  tail:
  ```
  lames = [(-0.80, -0.58, "Chest"), (-0.535, -0.345, "Chest"), (-0.305, -0.135, "Chest"),
           (-0.10, 0.05, "Spine"), (0.08, 0.21, "Spine"), (0.235, 0.345, "Spine")]   # lame 6 overhangs the Tail1 joint
  ```
  The seam bands follow from the gaps automatically (L222-226).
- **Lame `rnd` 0.42 → 0.28 and `grow` 0.024 → 0.018.** Seam `grow` 0.013 → 0.016. The seams become nearly flush:
  coral light in a crack, not a trench.
- **Coral heat fades toward the tail.** Seams 1-2 stay CORAL with the HOT centre line (as now), seams 3-4 are CORAL,
  and seam 5 is CORAL_D.
- **Tail rings (L232-233):**
  - Delete the Tail3 ring. Together with the peduncle keel it forms a "+" cross in the side view.
  - Turn the Tail1 and Tail2 rings into **top saddles**: `loft(..., zlo=0.10, zhi=1.0, grow=0.014)`, 0.10 and 0.08
    long, centred at y 0.50 and 0.72, with no seams. Full dark rings read as hose clamps from the side.
- **Move the scars (fix 2) onto the new lame 2 span.**
- **Target:** ARMOR ≤42% in the tq and game views (now 45.8 / 44.9). Side ARMOR should stay ≥28%.

### FIX 5 - The hammer: a crisp blade, not a pool noodle; brow spikes that read. L254-296
**The front of the hammer.** It is 4-5 studded rounded bulges:
- the centre block (rnd 0.30)
- the wings (rnd 0.32)
- two lead-edge segs (rnd 0.5, studded)

From the front it reads as a padded blue noodle. Fix:
- Lead-edge segs (L262-265): rnd 0.5 → **0.20**, `studs=[]` on both (the top surfaces stay studded), and hd 0.05 →
  **0.045**.
- Wings (L258) and the centre block (L255): rnd → **0.18**.

**Brow spikes (L290-296).** They are ~0.015 thick across x and only show in the close-ups. Make them **1.5x**:
- the ARMOR part, half (0.022, 0.05, 0.065)
- the CORAL part, half (0.016, 0.028, 0.05), with the same `d`

Check in the game render that two coral horn tips frame the T.

**Optional:** fierce_eye `sc` 1.4 → 1.6 (L289). The eyes are 1-2 px at 64.

### FIX 6 - A second bite notch, in the caudal (your questions a and b). After L361
- Add a **trailing-edge fill poly** to the upper caudal lobe, in the same way as the dorsal's free rear tip (L327-329):
  - STEEL, 0.03 thick, along the lobe's back-down side
  - it reaches ~0.05 past the blocks and carries one **V notch 0.045 deep at ~60% of the lobe length**
  - put `pts[0]` on the lobe axis at 50%, so the fan stays star-shaped (B.poly fans from pts[0])
  - let the fill run slightly concave between the root and the notch. That also gives this lobe its falcate trailing
    edge.
- (b) **The other trailing edges can stay straight.** At play distance the stacked steps read fine, and the dorsal
  already hooks.

### FIX 7 - Optional polish: jaw crescent and front teeth. L298-316
- From the front the lower jaw is a white box. Split it into a centre seg (x ±0.07) plus 2 side segs angled back 25°
  (the review-1 crescent), at the same z.
- When the jaw closes, upper teeth 1-3 per side sit within ~0.005 of the lower jaw's front and side faces. Move those
  three out by x +0.010.

### Your questions, briefly
- **(a)** Yes, add one more notch, in the caudal upper lobe via a trailing poly (fix 6). That makes 2.
- **(b)** Accept straight trailing edges except the new caudal fill.
- **(c)** **No, don't add density for the number.** 7.6k is fine; my 9-12k was an estimate, not a target. At 64 px the
  pet is already as busy as it can afford. After these fixes expect ~7.5-8.5k. The only tris worth spending are the
  notch fill (~60) and the crescent jaw (~70).
- **(d)** Keep the coral edge, but make it flush, thinner and less red (fix 3).

---------------------------------------------------------------------------------------------------------------------
## 3. Things I checked and that are fine (don't touch them)
- **Rest pose and rig:**
  - The dorsal fairing starts at the Chest pivot (y -0.19 vs -0.20), so the shear is ≤0.006 at ±12°.
  - Lame 6 overhanging Tail1 is fine.
  - The pelvics and the small fins on Tail1 are clear of the joint.
  - The pectoral fairing hides the root at mid-chord.
- **The lower teeth are buried 0.05 inside the upper jaw when the jaw is fully closed.** You can't see it and it isn't
  a checked pair. The rule that follows: never key the jaw past closed (see section 4).
- **The 0.6x in-game sim on grass reads well:**
  - a dark armoured hammerhead with glowing coral cracks, a white belly and steel fins
  - the armour does not merge into one black mass
  - nothing needs to be lighter

---------------------------------------------------------------------------------------------------------------------
## 4. Changes to the clip plan, now that the real geometry exists
These replace the matching lines in review 1, section 4. Everything else there stands, including the "no head
shakes, shark edition" rules and the pose limits.

1. **Jaw values are measured from CLOSED, and your rest is 10° open.**
   - Key `Jaw = plan angle - 10`. So closed = **-10**, roar gape 38 → key **28**, bite 34 → key **24**, and the
     idle jaw breath "10 → 16 → 10" → key **0 → 6 → 0**.
   - **Never key below -10.** Past closed, the lower teeth come out through the top of the upper jaw.
2. **act_hammerslam: the strike works only with the jaw CLOSED.** I checked it pivot by pivot with your joints:
   - The pose is Spine +22, Chest +10, Head +10 (Head vs Chest 10 ≤ 12) = **42°** nose-down at the hammer.
   - With the jaw closed, the hammer's leading-edge centre (y -1.16, z+0.025) is the lowest point. The chin plate is
     **0.037** higher, and the eye lobes about the same.
   - With the jaw left at its 10° rest, the margin is only **0.020**, so the jaw would scrape.
   - **Close the jaw (key -10) by f30** and hold it closed through the pin (f30-70). Then the bite opens it to key 24
     and snaps it back to -10 at f78.
3. **The strike is a pitch-over, not a dive.**
   - In that pose the hammer edge sits ~0.665 below the Spine pivot, so to touch the ground Spine z needs only
     about **+0.025** over rest.
   - The rear-up raises it to +0.10, and the strike drops it back while the head arcs down.
   - Solve it exactly with the `head_contact()` floor solve; don't hand-key it.
   - At contact the tail tip sits at ~1.69 world, under the 1.75 limit, so the tail counter-curl can stay small
     (Tail1-3 -4/-5/-6).
4. **The pectorals clear the ground by ~0.35 at the strike,** so "pectoral tips up 25 to clear the ground" is not
   needed. Keep a 10-15° brace lift for acting only.
5. **Move the `Slam` anchor** from (0, -1.03, z+0.0) to the leading-edge centre, **(0, -1.15, z+0.03)**. In the strike
   pose the old spot is ~0.08 above the ground, so the sand burst would spawn in the air.
6. **Gill pump:** no Gill bones were added, so the idle uses the jaw breath (point 1). That's fine. Don't add bones
   for it now.
7. **Roar pectoral drop:** 38° → **30°** unless the pose render shows the fin blade clear of the belly shell. Fin vs
   Chest is a parent/child pair, so nothing checks it automatically.
8. **Swim and idle:** no changes. The wave limits (relative yaw Spine ±2, Tail1 ±6, Tail2 ±9, Tail3 ±10, Tail4 ±9)
   suit the new joints (Tail1 0.30, Tail2 0.62, Tail3 0.90, Tail4 1.00). The graduated lames from fix 4 put lame 6 on
   Spine overhanging Tail1, which is fine at ±6°.

---------------------------------------------------------------------------------------------------------------------
## 5. What to send next (round 3 = mesh sign-off + first clips together)
Do fixes 1-6 (7 is optional), then render:
1. **The model sheet**, with the tq at 600, and **the close sheet**.
2. **The contact test pose:** Spine +22, Chest +10, Head +10, Jaw -10, with Spine z solved so the hammer touches
   0.005. Use a side and a tq view, and report the minimum z of the Jaw group, of Fin_L/R and of the eye lobes.
3. **The 64/128 icon strip** with Kappa / SeaTurtleWarrior / Kraken through `icon3.py` (the portrait raw at the normal
   portrait camera).
4. **Re-measure the value shares.** Targets:
   - side: coral family ≥9.5%, ARMOR 28-38%, BELLY ≥12%
   - tq and game: ARMOR ≤42%, game coral ≥8%
5. **Then go ahead with idle and swim, and send their pose sheets with the above.** I will sign off the mesh and those
   clips in one pass. Roar and act_hammerslam can follow in the round after.

Pass bar for the mesh in round 3:
- gills visible over the belly line on both sides
- zero floating parts in the close views
- no bead or rod read on any fin edge
- graduated lames with no tail clamps
- 2 notches in the silhouette
- the hammer front reads as one blade
- brow spikes visible from the game camera
