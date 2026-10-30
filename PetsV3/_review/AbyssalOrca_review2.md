# Abyssal Orca - art director review 2 (2026-10-14) - MODEL: REVISE (targeted) / RIG: APPROVED, clips may start

**Score: 7/10 for a 1.5% SECRET (v1 was 2.5/10).** This is now clearly the DEEP SOVEREIGN, and it is one of ours: a
real orca torpedo with a hump and a narrow peduncle, a tall stepped blade dorsal, a white jaw and belly, a lens eye
patch under a fierce slit eye, and a crowned angler lantern. The lantern reads in every view and at 64 px. Do not
redesign anything.

Two things hold it back:
- **The inlays are not flush on the body's back half.** The saddle reads as a grey box on the back from the game
  camera, and the flank lobes stick out as white blades with stray shards.
- **The black/white pattern is too small for the 64 px icon.** In the tq view WHITE is only 15%.

Both trace back to one root cause in the hull loft (FIX 3). Fixes 1-5 below should take it to ~8.5.

**The rig is approved as built. No fix below moves a bone.** You can author swim / idle / roar now, in parallel.
Re-run collision and act_lure's clearances after the mesh fixes (section 4).

What I looked at:
- `pets/AbyssalOrca.py` v2 (428 lines)
- `_model_sheet`, `_close_sheet` and all 8 single renders at full size
- 3x enlarged crops of the saddle, lobe, fluke root and head (game / back / side / tq)
- my own 64 px slate cut-out strip with an outline, next to Thunder Rex, Hammerjaw, Kraken, Kappa and SeaTurtleWarrior, compared with the v1 strip
- the v1 review checklist

All temp files are outside the project; nothing but this verdict was written.

How I measured: the same pixel classifier as round 1, recalibrated for the brighter INK. Lit INK reaches max channel
~150 and lit SADDLE ~200-230 with B-R ≈ 60. White belly pixels tinted green by the ground bounce are counted back in
by filling holes in the silhouette. Figures are approximate, ±3%.

| view | INK | WHITE | SADDLE | JADE | GOLD |
|---|---|---|---|---|---|
| side | **61.7%** | 21.5% | 4.3% | 9.9% | 2.5% |
| tq | 57.6% | **15.5%** | 8.0% | 12.7% | 6.2% |
| game cam | 60.5% | 14.5% | 11.7% | 9.5% | 3.7% |
| back | 53.1% | 23.9% | 11.3% | 8.5% | 3.2% |
| front | 47.0% | 15.7% | 7.7% | 20.2% (orb) | 9.3% |

---------------------------------------------------------------------------------------------------------------------
## 1. Round-1 checklist - item by item

1. **Lineup - PASS.**
   - It is now the most distinctive Tide pet: the only black/white one, and the only one with a light source.
   - It is not a Hammerjaw variant: no plates, spike row or poly fins. It is not a Rex palette swap: jade beads and veins, no crystals or seams.
   - Rex is still the more saturated icon overall, which is fine because it is a different egg.
2. **64 px test - FAIL (narrow, 2 of 3).**
   - Orca: yes. The dorsal blade and flukes give the whale shape.
   - Lantern with gold: yes. A jade and gold blob that pops on the slate, the strongest read in the icon.
   - Black/white pattern: only partly. The white jaw line shows, but the eye patch is 1-2 px and the flank lobe is invisible.
   - FIX 4 addresses this.
3. **Value blocking - FAIL (narrow).**
   - Side: INK 61.7% (target ≤ 55%). tq: WHITE 15.5% (target ≥ 20%). These miss.
   - Game cam: INK 60.5% and WHITE+SADDLE 26%. Both pass.
   - Glare: the fins no longer glare, so that passes by inspection.
   - An orca is inherently ~60% black, so for v3 **I relax the gates to side INK ≤ 58% and tq WHITE ≥ 18%.** FIX 2 and FIX 4 get there.
4. **Accent - PASS.**
   - JADE is 8.5-12.7% in the side, tq, game and back views. Every bead steps GLOW→HOT, and the vein trunks have HOT cores.
   - GOLD is ≥ 1.5% in every view: 2.5-6.2%, and gold shows on the head top from the game camera.
   - The tq's 6.2% is above the 2-3% target. I accept it, because all of it is the hero piece.
5. **Silhouette - PASS.**
   - The dorsal tip is the top (H_MODEL 1.80). The orb centre sits at 64% of the height and its top at 73%.
   - L:H ≈ 1.78 by geometry. Max girth is at ~33% from the snout. The belly rises into the tail stock.
   - The peduncle is 0.13 wide and 0.19 tall. The dorsal is a 0.11 wedge at the root.
   - The "?" rod silhouette reads from the side.
6. **Face - PASS, with 2 polish notes.**
   - The slit eye sits under an angled INK_D brow, with the white lens flush behind and above it. The eye patch lens is the best-built inlay on the pet.
   - 7/6 interlocking teeth with an overbite, a dark mouth roof and floor, and no red specks.
   - Polish notes (FIX 8): the MOUTH floor shows through the chin as a dark-red dash (close_side, close_tq). In the front view, the brows stick out of the narrow rostrum as two small dark tabs.
7. **Fins - PASS.** There is no `B.poly` on the dorsal, pectorals or flukes. The dorsal steps read as f_63's stepped fin, with veins and serrations.
8. **Hard rules - FAIL.**
   - **Saddle:** about 0.025-0.03 proud at its corners and front edge, and built as two overlapping boxes ("a box in a box" from the game camera).
   - **Flank lobes:** these are poly fans that stand off the hull as white blades. A stray white shard points forward at each lobe's front sliver (side render crop at y ≈ -0.06, back render crop under the belly).
   - **Lobe bone:** each lobe sits on ONE bone, `bone(C.y)` with the shared fan centre ≈ y 0.15, so Spine. Its back third (y 0.26-0.38) is over Tail1, so it will float or sink as soon as the tail flexes. The brief asked for a split at Tail1.
   - Everything else passes: no Neon, 6.4k tris, INK lum 71, no detail under 0.02 except the eye pupil, beads seated with `surf_hit`.
9. **Rig - PASS.**
   - Bulb sits at the orb centre. Lure → Lure2 → Esca is a real pendulum chain.
   - Maw, Glow1-3, DorsalTip and FlukeL/R are present, and the Head pivot is at the throat.
   - The dorsal's trailing root is 0.12 ahead of the Tail1 pivot (≥ 0.10). The saddle is split at Tail1.
   - The check pairs include all the additions.
   - Two limits for animation are in section 4.
10. **Deliverables - PARTIAL.**
    - Present: model sheet, close sheet, game render.
    - Missing:
      - the tq is 520 px (not 600)
      - no icon strip from the icon pipeline
      - no pixel-share table (I made both myself for this round)

---------------------------------------------------------------------------------------------------------------------
## 2. Fixes, ranked by impact (all in `pets/AbyssalOrca.py`)

### FIX 1 - The saddle must be a flush chevron, not a grey box (game camera; checklist items 8 and 3). L272-273
The saddle is the biggest light shape players see from behind, and it reads as a seat or briefcase on the back. There
are three causes:
- **Wrong dimensions.** Its dims come from `hull()`, the piecewise-linear station table. But the real Spine hull seg
  runs straight from y -0.12 to hull(0.36), so at y 0.12-0.26 the real hull is ~0.02 narrower and lower than `hull()`
  says. With grow 0.008, the shell sits ~0.025 proud. FIX 3 removes this cause.
- **Sharper corners than the hull.** rnd 0.40 of its own ~0.15 half-height gives a ~0.06 radius, against the hull's
  ~0.09. Its upper corners stick out further than its sides.
- **Two visible end faces.** The Spine piece and the Tail1 piece overlap, and both end faces show.

Do this:
- After FIX 3, pass a matched rounding to every shell: `rnd = min(0.9, 0.40 * min(hw, hh) / min(w0, d0))`. Here
  (hw, hh) are the hull's dims at the shell's start and (w0, d0) are the shell's own start half-sizes. This applies
  to the saddle, the belly band (L245-246) and the new lobe shells.
- Build the saddle from 2 pieces with no visible joint:
  - **Spine piece:** y **0.10** → 0.26, end_w **0.90**. Its front face starts under the dorsal's trailing root (te ≈ 0.14), so it is hidden.
  - **Tail1 piece:** starts at y 0.25 (buried 0.01 inside the Spine piece), with `scale0` = the Spine piece's end size × 0.98, end_w **0.30** (the chevron point).
- Optional: SADDLE (150, 162, 194) → **(136, 146, 182)**, so it sits halfway between INK and WHITE instead of competing with the white.
- **Check:** in model_game and model_back the saddle outline has no step or lip, and it tapers to a point toward the tail.

### FIX 2 - Flank lobes as stepped, studded WHITE shells split at Tail1 (items 8 and 3). L250-263
Delete the `patch()` call for the lobes. Keep `patch()` for the eye lenses: they work, because the head side is
flatter and sits on one bone. In place of the lobes, build 5 WHITE loft shells (grow 0.008, zlo -1.0, matched rnd as
in FIX 1, ext1 0.02):

| y0 → y1 | bone | zhi | end_w |
|---|---|---|---|
| -0.04 → 0.08 | Spine | -0.45 | 1.0 |
| 0.08 → 0.18 | Spine | -0.25 | 1.0 |
| 0.18 → 0.26 | Spine | -0.05 | 1.0 |
| 0.26 → 0.36 | Tail1 | +0.10 | 0.92 |
| 0.36 → 0.42 | Tail1 | +0.12 | 0.55 (the tip sinks into the hull = the tongue's point) |

- From the side, the white boundary becomes a staircase rising toward the back to ~55% of the body height. This is
  the angular, voxel-style patch of f_63, it is studded like the hull, and it bends with the tail.
- It overlaps the belly band, which is fine (white on white).
- **Check:** no white shard anywhere on the flank or belly in model_side, model_back or model_game at full size, and
  the lobe tip follows Tail1 in a +16° tail pose.

### FIX 3 - Build the hull exactly on its stations (the root cause of FIX 1; also fixes the head shape). L191-199
Each hull seg runs straight from y0 to `hull(y1 + ext1)`, and `head_up` spans S0 → S2 in ONE seg. So the hull cuts
inside every station kink by up to ~0.02-0.03, and every `hull()`-based shell ends up proud. Three side effects:
- **The head is a wedge.** At the eye (y -1.06) the hull is ~0.168 wide instead of S1's 0.19, so the head is ~12%
  too narrow. That is why it reads like a dolphin or shark wedge instead of a blunt orca head.
- **The head has hard edges.** `head_up`'s bevel radius is set by its smallest half-size, so it carries the snout's
  ~0.025 radius all the way back: the hard ridge along the head's upper side in close_tq.
- **Visible joint creases.** Each seg has a different radius and taper in the overlaps, which gives creases in the
  side and back views (behind the eye patch, and at the chest/spine joint under the dorsal front).

Do this:
- Build **one seg per station pair** (S0-S1, S1-S2, ... S7-S8). Use exact station dims at both stations, and keep
  the upper-head band (zlo = MOUTH_F) for the two head segs.
- **Build each seg from its BIG end toward its small end**, so the bevel radius suits the big end; the kit's clamp
  rounds the small end.
- Bury the joints along the seg's OWN slope. With `slope = (end - start) / (y1 - y0)` for hw, hh and zc, extend the
  far end by 0.05: end dims = station dims + slope × 0.05. Do this instead of reading `hull()` past the station.
- Then `hull()` is the truth again, and every shell built from it (belly band, saddle, lobes, throat) is flush.
- **Optional melon:** add a station at **y -0.94: (0.235, 0.25, +0.01)** for a domed forehead, the orca's blunt
  melon. If you add it, raise ROD[0] and the coronet by +0.035 so they still sit on the skin. That moves the Lure joint
  by 0.035, which is harmless to the clips.

### FIX 4 - More white where the camera and the icon look (items 2 and 3). L265-270
- **Eye lens about 1.4x the area:** run it from y **-1.00 → -0.70**, with the centre line rising from Z0+0.03 to
  Z0+0.11 and half-heights **+0.065 above / -0.055 below** (now +0.055 / -0.045).
- Keep its lower front point ≥ 0.03 above the brow block. It is the 64 px orca read, so it must be ≥ 3x2 px on the icon.
- Together with FIX 2's rising lobe, this should give **side INK ≤ 58%, side WHITE ≥ 20% and tq WHITE ≥ 18%.**

### FIX 5 - Remove the knob at the fluke root; make a V notch. L330, L316-317
- Delete the "notch root fill" cube at (0, 0.97, z+0.03). In game and back views it reads as a bolt or knob between the flukes.
- End the hull in a point: last station (0.88, 0.05, 0.075) → **(0.94, 0.03, 0.045)**.
- Start the inner fluke segs at x **±0.015** (P[0] x 0.03 → 0.015), so the two inner trailing edges meet in a clean V notch.

### FIX 6 - The orb is a "jade bell pepper"; make it a drop of light. L292-300
Two rotated rounded squares, taller than wide, make 8 vertical rounded ribs: a ribbed barrel. That reads as a pepper
or pumpkin in every close-up, which is risky with the Halloween hub live.
- **Upper body:** **3 Z-only rotations (0 / 30 / 60°)** of a rounded GLOW block, hw 0.15, hz **0.11**, centred at
  ORB + (0, 0, 0.04), top 0.90. Z-only rotations give a smooth 12-sided body. The X-rotated copy is what made the
  cauliflower.
- **Lower cone:** the same 3 rotations, centred at ORB − (0, 0, 0.10), hz 0.065, **bot = (0.40, 0.40)**. The orb
  narrows downward into the drip.
- **Drip:** HOT spike at ORB − (0, 0, 0.165), **0.10 long, w 0.035** (now 0.08 / 0.03 and barely visible).
- Keep the 5 gold claws. Their tips already grip at ORB.z − 0.03, which is now the widest point.
- Silhouette: an inverted teardrop lure, not a barrel. Gold share stays the same.

### FIX 7 - Round lantern beads, not square tiles. `bead()` L120-129
- `rnd` is a fraction of the smallest half-size (0.012), so the domes stay square. They read as portholes or LED tiles in the close-ups and in the spine row.
- Add a second GLOW dome rotated 45° about the normal (`R @ Rz(45)`), which gives an octagonal lantern. Optionally do the same for the DEEP socket.

### FIX 8 - Polish (optional)
- **Chin dash:** make the MOUTH floor (L210) hw 0.12 → **0.09** and top 1.6 → **1.3**, or lower it 0.01 into the jaw, so it no longer shows through the chin.
- **Brow tabs:** seat the brow block at `n * 0.0` instead of `n * 0.006` (L166), and yaw it 8° more toward the face, so it stops reading as a tab in the front view.

### Where density actually helps (you asked; 6.4k now)
Spend it on FIX 7 (~+1.0k), FIX 6 (~+0.4k), FIX 3 + melon (~+0.3k) and FIX 1-2 shells (~+0.2k), for about **8.3k**.
Then stop. Every part you add from here becomes noise at game distance. This pet's richness comes from the pattern,
the lantern and the lights, which are all there. Do not add scars (Hammerjaw), barnacles (Kraken), spikes or extra
gold.

---------------------------------------------------------------------------------------------------------------------
## 3. Notes for clip authoring (rig approved; the review-1 section 4 tables still apply)

- **Animation references (owner rule):** pull 1-3 clips from animationreference.org before keying, e.g. a whale or
  dolphin fluke cycle, a jaw-clap or bite, an ambush strike. Note their key frames and cite them in the clip plan.
- **The jaw is MODELLED 8° open.** Every jaw angle in my tables is the TOTAL opening, so the key is total − 8 (jaw
  shut = −8; "jaw 44" = +36). Render the shut pose once: the upper teeth must close OUTSIDE the lower lip (overbite).
- **Chest vs Spine ≤ ±4°.** The dorsal root (y -0.36 → 0.14, on Dorsal → Spine) straddles the Chest hull ahead of the
  Spine pivot. Beyond 4° its front root lifts off the back or sinks into it by more than 0.02. Put the swim counter
  and the idle/act rolls on Spine.
- **Esca clearance (act_lure "dangle").**
  - The orb is now ~0.30 across, so my Lure +16 / Lure2 +20 may bring it too close to the snout.
  - Scale them until the orb hangs ≥ 0.04 clear of the rostrum and above the 8°-open jaw, and verify with the (Esca, Head) and (Esca, Jaw) pairs.
  - In the "lure up" beat, confirm the orb clears the dorsal leading edge (Esca, Dorsal).
- **Saddle and lobe shells at the Tail1 joint.** Keep the Tail1 pieces buried ≥ 0.01 under the Spine pieces, so a
  +16° tail-up flex does not open a gap at the joint.
- **The pectoral fold** ("lights out": back 20 / up 8) presses the paddles toward the belly band. Check (Fin_L/R,
  Chest) at that pose.
- Run `ground_lift()` (Kraken L214-240) in every clip. The pectoral tips are the lowest vertices in the rolls.

---------------------------------------------------------------------------------------------------------------------
## 4. v3 sign-off checks (short)

1. **Full-size model_game, model_back and model_side:**
   - the saddle is a flush chevron with no step or lip
   - no white blades or shards on the flanks or belly
   - no knob between the flukes; a V notch instead
   - no creases at the hull joints
   - the head reads blunt
2. **Shares (my method, ±3%):**
   - side: INK ≤ 58%, WHITE ≥ 20%
   - tq: WHITE ≥ 18%
   - game: WHITE+SADDLE ≥ 15%
   - GOLD ≥ 1.5% everywhere; JADE 8-14% (front excepted)
3. **64 px strip on slate from the icon pipeline:** the eye patch is ≥ 3x2 px, and you can name an orca, a gold-and-jade lantern and the black/white pattern.
4. **Close sheet:** the orb is a smooth teardrop with a visible drip, the beads are round, there is no chin dash and there are no brow tabs.
5. **Deliverables:** a 600 px tq, the pixel-share table, collision_free still true at rest, and the tri count (expect ~8.3k).

With fixes 1-5 the model is approved. Fixes 6-8 are strongly recommended, but I will not block on them.
