# Hammerjaw Shark - art director review 3 (2026-10-14) - MESH APPROVED, CLIPS APPROVED (with one act fix)

**Mesh: APPROVE, 8/10 for a 5.5% pet** (v1 4/10, v2 7/10).
- Every review-2 fix landed, and all the round-3 pass-bar items pass.
- It clearly outclasses the Tide commons and reads as one of our family.
- **The mesh is locked.** Don't touch it unless the owner asks.

**Clips:**
- **idle: APPROVED.**
- **swim: APPROVED.**
- **roar: APPROVED,** with two should-fixes for the game camera.
- **act_hammerslam: APPROVED once one small timing fix lands.** The strike decelerates into the floor, so the slam
  lands soft (section 3).

**No new model or clip review is needed.** Send only the strike numbers and stills listed in section 5. I'll sign off
from those.

What I looked at:
- v3 `pets/HammerjawShark.py`, including the round-3 collision changes
- `_model_sheet` (600 px), `_close_sheet` and all model renders at full size
- `_icons_strip_64/128` (enlarged 4x)
- `_pose_side_sheet`, `_pose_tq_sheet` and 12 single pose frames
- the `flat_*` ID renders
- `_review/ANIM_REFERENCES_1014.md`

I re-measured the value shares myself in two ways (table below).

| view | ARMOR | STEEL | BELLY | coral family | target | result |
|---|---|---|---|---|---|---|
| side (flat ID, my count) | 28.7% | 35.3% | 12.4% | **11.9%** | ARMOR 28-38, BELLY ≥12, coral ≥9.5 | PASS |
| tq (flat ID) | **41.5%** | 27.9% | 4.0% | 16.7% | ARMOR ≤42 | PASS |
| game (flat ID) | **38.4%** | 32.9% | 4.8% | **13.1%** | ARMOR ≤42, coral ≥8 | PASS |
| side (shaded, review-2 method) | 28.5% | 43.2% | 13.2% | 8.5% | cross-check | - |

**A note on method.**
- My flat-ID count matches yours to ±0.1, so from now on the **flat-ID (nearest palette, unlit) count is the
  official measure.**
- My shaded classifier undercounts coral by ~3.5 points. Shaded CORAL_D and the shadow sides of the fin edges fall
  outside its coral band.
- The shaded number barely moved since round 2 (8.3 → 8.5). So the round-2 "coral fail" was mostly a measuring
  artifact. Under the flat method, v2 was probably already around 11-12%. That was my error, not yours.

---------------------------------------------------------------------------------------------------------------------
## 1. Mesh - round-3 pass bar, item by item

1. **Gills visible over the belly line on both sides - PASS.** All 5 MOUTH slits and coral flaps cross onto the white
   shell (close_side, model_side). The v1 read is back, and stronger now that it sits on white.
2. **Zero floating parts - PASS.**
   - The lame keels and the head keel are now seated strips. The "suitcase handle" is gone in close_front.
   - The 3 scars sit parallel on lame 2 and hug the plate.
3. **No bead or rod read on any fin edge - PASS.**
   - From the front, the dorsal edge is now a thin coral line on a steel blade.
   - The pectoral and caudal edges are flush and run CORAL → HOT without chevrons.
4. **Graduated lames, no tail clamps - PASS.**
   - The lames run big to small (0.22 → 0.11), and the coral heat fades to CORAL_D at the last seam. The back now
     reads as armour speeding up toward the tail instead of 14 equal stripes.
   - The tail saddles plus the lone peduncle keel removed the hose clamps and the "+" cross.
5. **2 notches in the silhouette - PASS.** One on the dorsal free tip, and one in the new caudal trailing fill, which
   reads clearly in model_side.
6. **The hammer front reads as one blade - PASS (narrow).**
   - In close_front the lead edge still shows two soft creases at the notch. At play distance and at 64 px it reads
     as one studded blade.
   - Not worth another pass.
7. **Brow spikes visible from the game camera - PASS.** The two coral horn tips frame the T in model_game and in the
   tq.

**The other round-1 items still pass:**
- lineup and family fit
- L:H: 2.02 in the render; the new caudal position adds 0.04 of length, which is fine
- the hard rules: studs, no glow, 8k-range tris, H_MODEL
- the face

**64 px (your icon3 strip) - PASS, 2 of 3.**
- Hammer T: yes.
- Coral-seamed armour: yes.
- Teeth: **no.** The portrait camera looks down onto the helm, so the jaw is hidden.
- At 128 px the coral eye slit shows on the near lobe.
- **Optional, for the coordinator's portrait step only:** lower the portrait camera ~8° for this pet so the tooth row
  shows under the hammer. This is the same kind of per-pet tweak as Rex's crown camera. Do not change the mesh for it.

**Round-3 collision changes - all accepted.**
- The shorter pectoral root, the Spine hull starting at -0.20 (still a 0.08 telescope), the throat ending at the jaw
  hinge, the caudal moved back 0.04 and the head jaw-hinge ignore line (the Rex precedent) are all invisible at play
  distance.
- None of them costs a read.

**Contact test - PASS.**
- At f33: hammer 0.005; jaw 0.0495 (0.045 clear, better than my 0.037 estimate); eye lobes 0.064; fins 0.270.
- The same holds pinned at yaw 20 (f54).
- This closes rig item H.

---------------------------------------------------------------------------------------------------------------------
## 2. idle (120 f) and swim (32 f) - APPROVED, no changes

**idle:**
- The build matches the PATROL HOVER spec: the bob, the 3° hunting pitch, the 40% wave, the fin trim swap with
  flutter, the two jaw breaths and the teeth flash.
- The **single** banked glance: the head's world yaw reaches 10° through Chest 4 + Head 6, and Head vs Chest stays
  ±6.
- Outside the glance I compute the head world yaw at ±0.16°. Your ≤ ±0.8 is a safe bound.
- No head shake.

**swim:**
- I summed your relative yaws as phasors (Spine 2 / T1 6 / T2 9 / T3 10 / T4 9, 0.12 cycle lag per bone) with your
  joint spacing:
  - **tail-tip lateral excursion ≈ ±0.24** (target ±0.25)
  - caudal world angle ≈ ±23°
  - head world yaw ±1° opposite the spine (recoil, not a sweep)
- The front two-thirds stay rigid. The pectorals plane and never flap. The thrust pulses at 2x.
- It reads "shark" from the tq stills, and it is a different motion from the Kraken's jet swim.
- The ±0.5° head nod and the ±1.5° jaw flutter are below visibility. Harmless; leave them.

---------------------------------------------------------------------------------------------------------------------
## 3. act_hammerslam (104 f) - APPROVED after ONE timing fix

**What is good:**
- The beat structure is exactly the STINGRAY PIN: spot, rear-up with a 4-frame hang, pitch-over, pin, a 20° pivot
  around the pinned point, a lift and ONE bite, and a glide back to rest.
- The solver holding both min z and the Slam anchor's x/y is the right construction.
- The side f33 still is the strongest silhouette the pet has: a steep diagonal, the hammer flat on the floor, the tail
  high.
- The jaw stays shut through the strike and pin, and the bite opens at 0.08 above the floor.
- All limits hold: Chest vs Spine 12 at the overshoot, Head vs Chest 10.
- No head shake.

**MUST-FIX: the strike decelerates into the floor, so the slam lands soft.**
- The cause: keys are auto-clamped beziers, and on **Spine pitch and Head pitch f33 is a plateau** (22 at f33 and
  f35; 10 at f33 and f35). So their handles go flat at f33.
- With the f24-28 hang also flat, f28 → f33 becomes a smoothstep: about 10 / 35 / 65 / 90 / 100%. **The last frame
  before contact covers only ~10% of the drop.** The hammer is set down, not slammed.
- (Chest isn't affected; its overshoot to 12 at f35 keeps it moving.)
- The fix: make the head arrive at speed and stop on impact. Key Spine pitch, Chest pitch, Head pitch and Spine z at:

  | f | share of the f28 → f33 move |
  |---|---|
  | 28 | 0% (hang, as now) |
  | 30 | 35% |
  | 32 | 75% |
  | 33 | 100% (contact) |
  | 34 | 104% (Spine 23, Head 10.5; the solver lifts the body, so it reads as the body compressing into the pin) |
  | 36 | 100% |

  - Keep Chest's existing 12 at f35.
  - **Criterion:** the hammer's last frame (f32 → f33) covers **≥25%** of its f28 → f33 drop, measured from the
    Head-group min z.
  - `head_contact` still owns f33-70, so the floor and the pin are unaffected. Do check that ground_min_z stays
    ≥ -0.02 on f30-32.

**Should-fix (same pass, tiny): a 2-frame bite snap.**
- Today the bite is 24 at f74 → -10 at f78. -10 is a minimum, so that curve also eases into closure.
- Hold 24 to **f76**, then snap to -10 at **f78**. The `bite` event stays on f78.

**Optional, for the Studio VFX:** add events `press1` at f46 and `press2` at f58, so the VFX pass can put sand puffs
under the hammer on the two press pulses.

---------------------------------------------------------------------------------------------------------------------
## 4. roar (66 f) - APPROVED, two should-fixes for the game camera
**What is good:**
- It follows my THREAT DISPLAY table: the gather, the hump, the snout up, the pectoral drop (30, as I asked), the
  late gape (it matches your Sea Beasts note), the buzz, the tail-tip shiver, the snap, and the overshoot settle.
- There is no roll and no head yaw.
- From the tq the gape reads well: the teeth show under the hammer.

**The problem:** from the game camera (high behind) the jaw is invisible. The rest of the display is subtle by design.
- The head swings 18° (from +8 at f10 to -10 at f20) and the pectorals drop 40°.
- Then the 26-frame hold is static apart from a small tail flicker.
- The display was my spec, so this is on me.

Two cheap amplifications, both inside the limits:
1. **A bigger crouch-and-pop.** Spine z f10 -0.05 → **-0.07**, and f20 -0.02 → **+0.02**. That makes a 0.09 pop
   instead of 0.03, which reads from above as the shark puffing up.
2. **A tail-only lateral C-curl through the hold.** This is the "lateral bending" of the real agonistic display, and
   your Petrov note: the tail goes the other way.
   - Tail1-4 relative yaw **+4 / +6 / +6 / +4** at f20, held to f46, back to 0 by f58. That is about 20°
     cumulative, swept to one side.
   - Keep the current shiver on top of it (Tail3 ±4, Tail4 ±8). Raise Tail4 to ±10 if it still looks small.
   - The head stays fixed (yaw 0), so the no-head-shake rule holds.
   - From above, a flexed body is the clearest "threat" silhouette available.

Also make the **jaw snap a 2-frame snap**: hold 28 to **f48**, -10 at f50. That is the same reason as the bite: -10
is a minimum, so the current f46 → f50 curve eases into closure.

---------------------------------------------------------------------------------------------------------------------
## 5. To finish
1. **The act strike keys** (section 3, must-fix) and the 2-frame bite snap.
2. Recommended: the two roar amplifications and the 2-frame jaw snap (section 4).
3. Re-run step 1:
   - 0 collisions
   - audit linear 0
   - ground_min_z ≥ -0.02 (watch the act at f30-32 and the roar pop at f20)
   - loops closed
4. **Send me, and nothing else:**
   - the act's Head-group min z for f28-36 (one number per frame)
   - pose_side stills at act f31, f32, f33
   - if you did the roar changes, pose_game stills at roar f10 and f30
   - I'll sign off from those
5. Then the final export (step 1 + export to `C:\cdimp`).

**Owner to-do (as for all pets):**
- Studio import of `C:\cdimp\HammerjawShark.fbx` as creator **ZAB Studio**.
- **VFX Studio** effects on the anchors (owner rule: no hand-made particles):
  - `Slam`: a sand burst plus a shock ring on `slam`, and dust on `pin`/`press1`/`press2`
  - `Mouth`: bubbles on the idle jaw breaths, a bubble burst on `roar`, a snap puff on `snap` and `bite`
  - `Wake`: a bubble trail in swim
  - `DorsalTip`: a spray streak in swim
- Remember the ~0.6x in-game darkening. The coral seams are the only warm colour on the pet, so they will carry it.
- Save + Publish.

---------------------------------------------------------------------------------------------------------------------
## 6. Final sign-off on the clip fixes (round 3b) - APPROVE

**Hammerjaw Shark is signed off and ready to export:** mesh 8/10 for a 5.5% pet, all four clips approved.

What I checked:
- the builder's per-frame Head-group and Jaw-group min z for f28-36
- `_r3_side_strike.png` (act f31-34)
- `_r3_game_roar.png` (roar f10/20/30 from the game camera)
- the re-run report: 0 collisions at step 1, audit linear 0, loops closed, ground_min_z act 0.005 / roar 0.164

**act_hammerslam strike - APPROVED.**
- The total drop is 0.839 (0.844 at f28 → 0.005 at f33). The last frame (f32 → f33) covers 0.243, **29%** (the
  criterion was ≥25%).
- In the stills, f32 still hangs halfway and f33 is on the floor. It now arrives at speed and stops on impact, and
  f34 reads as the body compressing into the pin.
- **70% at f32 instead of my 75% was the right call.** Your measurement showed 75% gave only 23.9%.
- The floor-only solve on f29-32 and the pin solve on f33-70 hold the hammer at 0.005 through f33-36.
- The jaw stays ≥0.0495 through the strike.
- **The 2-frame bite snap** (24 held to f76, -10 at f78) is approved.
- *Optional polish, not blocking:* the per-frame drop runs 0.095 / 0.181 / **0.132** / 0.188 / 0.243. That is a
  one-frame slowdown at f30 → f31.
  - Lowering the f30 key from 35% to ~28-30% would make the drop speed up on every frame.
  - In a 5-frame strike the eye reads hang → whoosh → impact, so leave it unless you're in the file anyway.

**roar - APPROVED.**
- From the game camera the display now reads:
  - f10: tail straight, crouched
  - f20 and f30: the tail is curled to one side with the shiver on top, the pectorals are dropped, and the head is
    fixed
- The crouch-and-pop (-0.07 → +0.02) and the 2-frame jaw snap (28 held to f48, -10 at f50) are in.
- No head yaw anywhere. ground_min_z 0.164.

**Portrait camera:** leave it as it is. 2 of 3 at 64 px passes, and a per-pet override of the shared `camera_for("tq")`
isn't worth it for the teeth.

**Next:**
1. Final step-1 run and export to `C:\cdimp`.
2. Then the owner to-do list in section 5 (Studio import as ZAB Studio, VFX Studio effects on the anchors, Save +
   Publish).
