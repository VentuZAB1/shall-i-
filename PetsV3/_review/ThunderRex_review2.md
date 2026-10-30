# Thunder Rex - art director review 2 (2026-10-14) - REVISE (targeted)

**Score: 7/10 for a 1% SECRET (v1 was 3/10).** This is now clearly one of our pets, and it is the best-built pet in
the Storm egg. The ridge, the horns, the armour with seams, the face, the legs and the saturation all work. Do not
redesign any of it. Three checklist items still fail, all narrowly, and for two reasons:
- **The hero piece doesn't read.** The gold crown is 0.1-0.3% of the pixels, so it disappears at 64 px and from the
  game camera.
- **The top half isn't "storm-black".** HIDE covers more area than ARMOR, so it reads "blue dino with dark patches".

Fixes 1-3 below should take it to roughly 8.5-9. Section 3 lists five rig/mesh fixes (A-E) to make before anyone
animates it.

What I looked at: `_model_sheet`, `_close_sheet`, all 8 single renders, `_strip_64/128`, v1 sheet, `pets/ThunderRex.py`,
Ivonrath/Raiju/CelestialDragon close and model sheets, `_icons_sheet.png`, f_70/f_71. I also made my own slate cut-out
icon test at 64/128 px with the same outline style as `_icons_sheet`.

How I measured: I classified the pet pixels by colour in each render (the background removed). The figures are
approximate, ±3%.

| view | ARMOR | HIDE | BELLY | crystal (DEEP+CYAN+HOT) | GOLD | body sat. median |
|---|---|---|---|---|---|---|
| side | 29% | **47%** | **4%** | 20% | 0.2% | 0.53 |
| back 3/4 | 24% | 44% | 10% | 22% | 0.1% | 0.50 |
| game cam | 29% | 42% | 5% | 23% | 0.2% | 0.50 |
| front | 12% | 66% | 9% | 12% | 0.3% | 0.51 |

---------------------------------------------------------------------------------------------------------------------
## 1. Checklist (round 1) - item by item

1. **Lineup - FAIL (narrow).** It is no longer a Raiju/ThunderBull remix: the crystal ridge, the armour and the rex
   silhouette are all its own. But it is not *clearly* the most striking. At 64 px the eye goes to SolarLion (gold
   mane), Ivonrath (red) and Raiju (yellow bolts) first. The Rex's only complementary accent is the gold, and there is
   almost none of it. Cyan on blue is low contrast. Fixes 1 and 2 address this.
2. **64 px test - FAIL (2 of 3).** T-rex: yes (biped, open jaws). Glowing ridge: yes (the pale cyan cluster reads on
   the slate). Crown: **no**. On my slate cut-out the crown is 1-2 yellow pixels. The prongs are cyan/white, so they
   merge into the horn tips and the ridge. The ARMOR does not merge with the slate, so no ARMOR change is needed for
   this item.
3. **Value blocking - FAIL (narrow).** Saturation is fixed: median 0.50-0.53, up from 0.32. But it shows two bands
   plus crystals, not three:
   - HIDE is 47% in the side view, over the 45% cap.
   - ARMOR is 24-29%; the target was 35-40%.
   - The silver underside is 4% in the side view.
   - Why: the tail shells are *narrower* than the tail hide (x half hw\*0.92 vs hw). From the side the tail is all
     HIDE with a thin dark top line.
4. **Accent - PASS.** Crystals are 20-23% of the side, back and game views (the target was ≥15%). Every big shard
   steps DEEP→CYAN→HOT. The zig-zag stickers are gone, and the cracks grow out of the seams.
5. **Silhouette - PASS.**
   - The horn tips are the highest point (z ≈ 2.017); the centre crown prong reaches ≈ 1.96.
   - The ridge peaks at 0.42 over the shoulders.
   - Chest hw 0.29. The W fan reads from behind.
   - Length:height is 1.75 by geometry (3.53/2.02) and 1.65 in the side render. That is at the limit, so **don't
     add any length.**
6. **Face - PASS.**
   - Front: the eyes sit ≈0.055 above the snout top, under a proper V brow. The nostrils are only at the snout tip.
     The eyes match Ivonrath's `fierce_eye` read.
   - Side: 2 big fangs per side, irregular teeth, no plank lip.
   - Not blocking: the lip line is a straight slope, not a stepped snarl. The nasal plate (hw 0.065, half the snout)
     reads as a dark "tie" from the front.
7. **Legs - PASS.** Shin hw 0.115. Dark ARMOR socks and feet, claws 0.10-0.115. The stance is a mild A (hips ±0.24,
   toes ±0.355). Boxy from the front, but no stilts.
8. **Hard rules - PASS.**
   - Crystals, gold, teeth and claws are smooth; armour, hide and belly are studded.
   - No Neon. 8.1k tris.
   - The head is ~21% of the length.
   - The shards are seated with `surf_hit` sockets, so nothing floats.
   - The only part under 0.02 is the pupil copied from `fierce_eye`. That is the family construction, so it's
     accepted.
9. **Family fit - PASS.** It uses the fierce_eye, V brow and fang construction. PITCH uses the Raiju formula
   (0.0453 → the same world stud). HIDE's brightest channel is 200 (≥170).
10. **Deliverables - PASS, with 2 notes.**
    - `_strip_64/128` use the opaque light-ground crops. On those the pale crystal tips vanish into the background,
      and the real Index cards are outlined cut-outs on slate (`_icons_sheet.png`). Next round, test with the icon
      pipeline.
    - `model_tq.png` was overwritten at 200 px by `_tools/headless_closeup.py` (L11 renders tq at res=200). The
      600 px tq now exists only inside `_model_sheet.png`. Re-render it before any portrait or icon step that reads
      it.

The HEIGHT of 10 studs to the crown tips is approved: a secret should stand taller than Raiju (8) and StormWyvern
(8.5).

---------------------------------------------------------------------------------------------------------------------
## 2. Remaining fixes, ordered by impact (all in `pets/ThunderRex.py`)

### FIX 1 - Make the crown GOLD (the hero piece; fixes checklist items 1 and 2). L271-288
Ivonrath's crown reads because its prongs are gold (`pets/Ivonrath.py` crown: every prong FLAME). Ours are cyan, so
they disappear into the horns.
- **Prong bodies → GOLD.** Change the colour of every `B.seg` prong part (kinked L280-281, straight L284) from CYAN to
  GOLD. Keep the HOT tip spikes (L282, L286). The result is gold lightning-bolt prongs with white-hot tips, and the
  horns (ARMOR→CYAN→HOT) now separate from the crown by colour.
- **Prong heights** 0.10/0.15/0.21/0.15/0.10 → **0.12/0.18/0.24/0.18/0.12**. Seg widths 0.022-0.024 → **0.028**.
  This keeps the centre tip at ≈2.01, just under the horn tips, so H_MODEL stays 2.02.
- **Band** (L271): (0.155, 0.05, 0.03) → **(0.165, 0.055, 0.045)**.
- **Close the circlet so the game camera sees gold.** Today you see one orange line from behind.
  - Add 2 GOLD side bars along the skull-cap edges, just outside the horn roots:
    `B.seg((s*0.165,-0.93,1.735), (s*0.155,-0.665,1.745), 0.022, 0.03, GOLD, "Head", studs=[], nostud=True, role="limb")`.
  - Add a GOLD back plate (0.10, 0.02, 0.035) at (0, -0.655, 1.74), with a CYAN gem facing +y, a copy of the L287
    gem at y -0.632.
- **Target:** GOLD **1.5-2%** of the pet pixels in the tq and game views (now 0.1-0.3%). The crown should be a
  visible yellow mark at 64 px on slate.

### FIX 2 - Give the pet a storm-black top (fixes checklist items 3 and 1)
Aim for ARMOR ≥35% and HIDE ≤40% in the side and game views. Keep HIDE on the head and snout sides, the neck sides,
the arms, the lower flanks and the lower tail sides.
- **Tail shells (L329-330), the biggest lever:**
  - x half `hw*0.92` → **`hw*1.06`**, so the shell sits proud of the hide and its sides show. That covers the upper
    ~65% of the tail side instead of a thin top line.
  - Keep the offset (`-dn*hw*0.42`) and depth (`hw*0.62`).
  - Joint bands (L333): `hw*1.13, hw*1.05` → **`hw*1.16, hw*1.10`**, so the cyan rings stay proud of the wider
    shells.
- **Torso shells (L196-197):** `za` 0.02 / 0.0 / 0.02 → **-0.07 / -0.09 / -0.06**. The shells then cover ~2/3 of the
  flank. The jagged teeth (L201) and the seam bands (L206-207) follow automatically, because they are built from `za`.
  While you're there, use **3 teeth per shell side** instead of 2: ly at 0.2/0.5/0.8 of the span, lengths
  0.10/0.07/0.09, hy 0.045 → 0.05. Two teeth read as a "saddle bag", not as jagged armour.
- **Skull cap (L223):** (0.15, 0.15, 0.03) at z 1.73 → **(0.165, 0.165, 0.05) at z 1.715**. The dark crown of the
  head then sets off the gold band, the brows and the cyan eyes.

### FIX 3 - Make the tail end and tail ridge read from the game camera (how players actually see it)
- **Thunder-blade (L340-346):** the blade is 0.024-0.028 thick in x, so from behind it is an edge-on sliver.
  - Make all 3 blade segs **0.040** in x, and the HOT tip spike w 0.022 → **0.03**.
  - Add the 2 side shards from the brief, at b1:
    `shard(B, b1, (s*0.55, 0.45, 0.70), 0.15, 0.05, "Tail4", socket=False)` for s = ±1.
  - From above, the tail then ends in a 3-prong bolt burst. Do not lengthen the blade (see the L:H note in item 5).
- **Side shard pairs on Tail1 and Tail2.** The brief said side rows "from the neck to Tail2"; today they stop at the
  hips (`centre[2:8]`), and from the game camera the tail shards read as small pegs. Add pairs for `centre[8]` (y 0.58)
  and `centre[9]` (y 0.92) with the same splay code at **0.6×** the centre length. That is ~16 parts and ~1k tris,
  still well under 15k. The W fan then runs down into the tail.

### FIX 4 - Show the silver underside in profile (checklist item 3; target ≥7% in the side view)
- **Tail belly (L327-328):** x half `hw*0.6` → **`hw*1.0`**, depth `hw*0.22` → **`hw*0.26`**, offset `dn*hw*0.82` →
  **`dn*hw*0.80`**. It then spans -0.54..-1.06 hw, so a silver stripe runs under the dark shells along the whole tail.
- **Belly scute strip (L169):** depth 0.03 → **0.05**, and lower both ends by 0.025 (z 0.875/0.81 → 0.85/0.785). Move
  the BELLY_D gap bars (L172) down with it. Its sides then show as a silver keel line under the chest in profile.

### FIX 5 - Show the whole chest core under the jaw (the Index portrait is the 3/4 front). L176-193
Today the jaw and throat hide the top half of the core. You see a gold "V-neck" over a silver bib, not a diamond.
- Move the core to `fpt(rib, 0, -0.07, off=0.03)` (from local z 0.0).
- Move the keel to local z **-0.19** (from -0.13) and set its hz 0.11 → **0.09**.
- The full ARMOR socket, gold rim, cyan diamond and HOT centre then show below the jaw line in the tq render. The Core
  anchor follows automatically through `CORE`.

**Optional polish, only if time allows:**
- Nasal plate (L227): hw 0.065 → 0.045, or split it into the 3 armour bumps from the brief.
- Lip: step the upper-tooth root line down 0.02 over the back half (y > -1.10) for a snarl.

---------------------------------------------------------------------------------------------------------------------
## 3. Things that will break or look wrong once animated

Fix A-E in the model/rig before animating, then follow the pose limits at the end.

**A. Neck shard 1 vs the skull: will collide on any roar or look-up. Must fix.**
- Centre shard 1 (y -0.585, Neck bone) sits ~0.06 behind the skull's top-back corner (y ≈ -0.65, z 1.76).
- The Head pivots low, at the throat (0, -0.64, 1.40). At only **12-15° head pitch-up**, that corner swings into the
  shard. At 15° it reaches y ≈ -0.557, z 1.75, inside the shard (y -0.57..-0.49 at that height).
- `check_pairs` will not catch it, because Head-vs-Neck is not a pair.
- Fix:
  - **Delete centre shard 1.** The horns cover that spot from every view.
  - **Re-parent shard 2 (y -0.47) from "Neck" to "Chest".** It sits only 0.07 in front of the Neck pivot, so its
    root drifts ≤0.03 at ±8° of neck pitch. On the Neck bone, by contrast, its tip swings ~0.13 back through the big
    Chest shard (y -0.335) on a 15° neck raise; their roots already overlap by ~0.02 at rest.
- After the fix, the skull clears shard 2 by ~0.04 at Head +30°.

**B. Jaw-hinge horns vs the first side-row shards when the head turns. Must fix.**
- The Q horn tip is at (±0.35, -0.48, 1.58). At a **20-25° head yaw**, the horn swinging inward reaches
  ≈(0.25, -0.35, 1.58), on top of the side shard at y -0.335 (its tip is at x ≈0.22, z ≈1.6).
- Fix: re-aim `Q[2]` (L266) to **(s\*0.37, -0.56, 1.55)**. That is more sideways and 0.08 shorter backward, and it
  still widens the head from above. After the fix there is ~0.05 clearance at 25-30° yaw.

**C. The mouth interior will be blue studs when the jaw opens. Must fix.**
- The roof of the mouth is the studded HIDE underside of the snout (Head bone). The MOUTH strip (L241) is only on the
  Jaw. Every roar will show a blue Lego roof.
- Add a MOUTH roof plate:
  `B.seg((0,-0.94,1.385), (0,-1.24,1.31), 0.10, 0.012, MOUTH, "Head", studs=[], role="detail")`.
- Add the brief's small **CYAN throat block** at (0, -0.86, 1.36), size (0.06, 0.02, 0.04), Head bone, so the open
  mouth reads as "charged".
- The jaw itself can open freely to ~35°. Nothing blocks the hinge, because the jaw muscles sit beside the jaw, not
  behind it.

**D. VFX anchors that are in the wrong place.**
- Ridge1-3 (L391-393) are not at the shard tips. Ridge2 is at mid-height of a shard, and Ridge3 (y 0.25, Spine) is
  over the hips, not on one of the three tallest shards. Lightning arcs between them would start inside the crystals.
- Fix: in `model()`, record the HOT-tip positions of the centre shards at y -0.335 / -0.20 / -0.065 (base + d·L,
  including the kink offset) into a module list, the same way `CORE` is done. Use those for Ridge1-3, all parented
  to **Chest**.
- `Breath` (0, -1.20, 1.36) is inside the snout (the snout bottom there is z ≈1.32). Move it to **(0, -1.26, 1.31)**,
  in the mouth gap at the front.

**E. Fangs already clip into the lower jaw.**
- The big upper fangs sit at x ±0.112, w 0.022, so they span x 0.09-0.134. The lower jaw's side there is at x
  ≈0.10-0.11, so the fangs are already inside its side walls, and every bite-close drives them deeper.
- Fix: move the upper teeth to **x ±0.13** (L237) so they hang outside the lower lip. This is the classic overbite,
  and it is clean at any jaw angle.
- Minor, same area: the front lower tooth (x 0.098 + tilt) pokes out of the narrowing snout side at the nose. Pull
  it in to x 0.085.

**Pose limits for the animator** (horns, crown and ridge stay clean inside these):
- **Head pitch-up ≤ +30° total (Head + Neck).** At 35-40° the big horn tips drop to z ≈1.69-1.74 at y ≈ -0.08,
  within ~0.03-0.07 of the side shard tips at y -0.20. Head pitch-down ≤ -20°. Head yaw ≤ ±30° once fix B is in.
- **Neck ≤ ±8°.** Do the big roar lift with the **Spine** (the root, +10-12°), so the chest and hips move as one and
  the ridge does not grind.
- **Chest vs Spine ≤ ±5°.** The ridge is a continuous crystal comb whose roots overlap by design (shards at y 0.07 on
  Chest and 0.21 on Spine almost touch). Small relative rotation is invisible; large rotation makes crystals cut
  through each other.
- **Walk:**
  - Keep foot plantar-flex ≤ 40° at toe-off, or re-aim the ankle spur (L315) from (0, 1, 0.25) to (0, 1, -0.2).
    Beyond that, the spur rotates into the back of the shin.
  - Keep hip extension ≤ ~20°. At rest the inner upper thigh already overlaps Tail1. It is hide on hide and hard to
    see, but add (`Tail1`, `Leg_L/R`) to the posed collision check rather than to the rest check.
  - Expected and fine: the cyan knee band slides into the thigh on deep knee bends.
- **Tail sway:** no issues. The tail shards and blade are on their own bones, far from the legs.

---------------------------------------------------------------------------------------------------------------------
## 4. v3 sign-off checks (short)
1. GOLD 1.5-2% in the tq and game views, and the crown visible at 64 px on a **slate cut-out with outline** (the
   icon pipeline), not the opaque crop.
2. ARMOR ≥35% and HIDE ≤40% in the side and game views. BELLY ≥7% in the side view.
3. From the game camera: a 3-prong tail burst and side shards on Tail1-2.
4. Pose renders:
   - roar: Spine +10°, Neck +8°, Head +22°, Jaw 35°
   - look-left and look-right: Head yaw ±25°
   - walk toe-off frame
   No crystal, horn or skull clipping, and a dark mouth interior with a cyan throat.
5. Re-render `model_tq.png` at 600 px.
