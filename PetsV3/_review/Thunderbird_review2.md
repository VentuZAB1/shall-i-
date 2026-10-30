# Thunderbird - art director review 2 (2026-10-14) - REVISE (light): 9 codeable fixes, then the model is approved

**Score: 6.5/10 for a 5% pet** (v1: 4/10). The rebuild worked:
- From the side and in tq it is now a real eagle: a big keeled breast at 46°, the knee gone into the belly, short
  gold tarsi with hooked talons, the cloak fold laid along the flank, a white bolt-tipped fan, and kinked lightning on
  every tip.
- It owns its hue in the Storm egg.

What still holds it back is the view players see most, **the game camera from behind**:
- two full-length TEAL arm bars run down the back like rails
- the mantle is dark shingles on a teal field, which reads as rows of shark teeth
- the hands flare out at the bottom

There are also four face details and two deliverable gaps. Every fix below is small. I tested the big ones (fold,
saddle, arm split, face) on a temp copy of your spec.
- **Fold answer:** don't trade the breast. **The flight-muscle shoulder blocks are what the wing hits.** Delete them
  and the wing root goes back to +0.07, giving a narrower fold with 0 hits.

What I looked at:
- `pets/Thunderbird.py` v2 (all of it)
- `_model_sheet`, `_fold_sheet`, `_close_sheet`, all fold0_* and model_* singles at full size, plus 2-3x crops

My experiments: headless, run3 + a temp copy of your spec with switches. Outputs went only to
`C:\Users\ventu\AppData\Local\Temp\tb_review2\`, and no project file was touched.
- `fsearch.py`: fold grid with per-pair hits, envelope, and the wingtip→tail-tip distance measured from the Tail2 mesh
- `ptest.py`: transitions, bezier keys, every frame
- `flat_views.py`: an unlit vertex-colour render, used for **exact** palette shares
- `close.py`
- Sheets to open:
  - `cmp_varB.png`: as delivered vs the fixed back / fold, plus the spread pose and the raised V
  - `cmp_varD.png`: fold alternatives with all fixes
  - `cmp_face.png`: face before/after
  - `strip64_storm_egg.png`: the Storm-egg 64/128 px strip, v2 vs fixed vs a raised-V icon
  - `zoom1.png` / `zoom_fin.png`: rails, teeth, the edge-on tail, the withers fin

---------------------------------------------------------------------------------------------------------------------
## 1. The section-3 checklist, judged on v2 as delivered

| # | item | result | notes |
|---|---|---|---|
| 1 | Posture | **PASS** | Axis 46-52°. The breast is the forward mass. No femur shows. Visible leg ≈ 0.42 / 1.86 = 23%. |
| 2 | Front view | partial | Torso is OK and the "buttons" are gone. But the trousers are two boxy STORM blocks whose outer edge (~x 0.26) sticks out past the belly, and the tail fan seen edge-on makes a thin bar across the knees ("skewer", `zoom1.png`). |
| 3 | Fold | partial | 0 hits incl. Chest/Spine; all LIFT paths 0 hits; the arm lies along the flank. But the half-width is **0.667 / 0.566 (90%)**, and wingtip→tail tip is 0.257. |
| 4 | Game camera | **FAIL** | It reads as an eagle, but the full-length TEAL arm bars are the brightest thing on the back ("rails"), the mantle reads as dark shark teeth on teal, and both hands splay outward at the bottom. |
| 5 | 64 px | **PASS** | Clearly the teal one in the egg. White head, crest and beak read; the bolts are small yellow specks. |
| 6 | Palette | **PASS** | Largest single colour is 25.8% (table below). |
| 7 | Lightning | **PASS** | Every primary, tail and crest tip is a kinked BOLT→HOT. No dipped tips, no white secondary fringe. |
| 8 | Face | partial | The fused brow V reads from the front. Problems: (a) the eye is a yellow window in an even black frame with a near-full-height pupil (0.016 vs iris 0.0175 = 93%, breaks Lessons #7), which reads as spectacles; (b) the brow juts out as a pale visor in the side close-up; (c) the 0.13 hook spike points straight down and reads as an icicle from the front; (d) the crest reads as a **crown of 7 candles** from the front. |
| 9 | Tier | partial | Only the crest's crown read; everything else sits between the commons and Rex. |
| 10 | Deliverables | partial | `model_tq.png` is 200 px. `headless_closeup.py` calls `R3["model"](name, views=("tq",), res=200)` and overwrites it, so run the close-ups first or re-render. The 64 px strip is missing (mine is in temp). |

**Exact palette shares, fold pose = idle f0** (unlit vertex-colour renders, so no lighting error):

| view | STORM+PRI | TEAL+COV | WHITE | BOLT+HOT | GOLD | largest single |
|---|---|---|---|---|---|---|
| tq | 32.9 | 28.9 | 19.1 | 8.7 | 9.0 | STORM 23.6 |
| side | 44.7 | 24.0 | 11.6 | 13.9 | 4.8 | PRIMARY 25.8 |
| game | 29.3 | **31.2** | 23.3 | 15.1 | 0.9 | TEAL 24.7 |
| back | 35.0 | 28.5 | 17.1 | 17.7 | 1.3 | TEAL 19.6 |

The game view is TEAL-dominant because the rails and the teal mantle field show between the wings. That is the
opposite of the "dark top" structure. After fixes 1-3 (my test build), the game view goes to **STORM+PRI 44.0 /
TEAL+COV 16.1 / WHITE 22.5 / BOLT+HOT 16.4** (largest single: STORM 30.7). The back becomes a dark cloak with teal
shoulder patches, the bolts pop against it, and the teal stays on the breast, front and shoulders.

---------------------------------------------------------------------------------------------------------------------
## 2. Ranked fixes (all codeable; 1-3 are tested together)

### 1. Fold package: delete the shoulders, root back to +0.07, new FOLD (tested)
- **Delete the two flight-muscle blocks** (the `for s in (1, -1): B.add((s * 0.20, -0.10, 1.12), (0.10, 0.12, 0.11) …`
  loop in `model()`). In the fold they are hidden under the arm anyway, and per-pair counts show they are the
  Wing-vs-Chest blocker.
  - With them at WDX 0.10: none of the 72 grid candidates is collision-free; the closest ones hit Chest (77
    tri-pairs).
  - Without them at WDX 0.07: 12 of 72 are clean, and **the breast is untouched**.
- **WDX 0.15 → 0.07.**
- **FOLD = (86, 10, -80, 0).** Measured on the fixed body (saddle from fix 2 included):

| fold | half-width max / 90% | wing min z | wingtip end (y, z) | tail tip | wingtip→tail | hits |
|---|---|---|---|---|---|---|
| v2 FOLD (86,4,-95,-15) @ 0.15 | 0.667 / 0.566 | 0.142 | 1.336, 0.423 | 1.125, 0.278 | 0.257 | 0 |
| **new (86,10,-80,0) @ 0.07, no shoulders** | **0.549 / 0.461** | 0.326 | 1.365, 0.544 | 1.125, 0.278 | 0.359 | **0** |
| alt (92,16,-88,-15) @ 0.07 (measured before the saddle) | 0.588 / 0.511 | 0.182 | 1.371, 0.518 | | 0.344 | 0 |

- The new fold keeps the long eagle side silhouette, the wings hug the body from the game camera, and the hands stop
  flaring (`cmp_varD.png` row 1). I am **relaxing my wingtip-to-tail target from ±0.12 to "above or beside the fan,
  ≤ 0.40, never below it"**. The tighter options (tip +30) make the side view stubby, with the bolts bunched at the
  bottom (row 2).
- **The waypoints stay exactly as you have them:** LIFT1 (84,16,-80,-15), LIFT2 (70,24,-55,0), LIFT3 (50,20,-25,10),
  LIFT4 (35,8,-8,10), BREATH (80,26,-65,-10), RAISED_V (40,0,0,-10).
- I re-tested them from the new FOLD on the fixed body, **0 hits on all 8 paths** (bezier keys, every frame):
  1. fold→open
  2. flight bottom→brake→LIFT4..1→fold
  3. the raised-V roar loop with 2 beats
  4. the BREATH loop
  5. a 2-frame-spacing takeoff (fold→…→(30,0,0,0)→(-34,8,6,4))
  6. the stoop: **1-frame spacing** (30,0,0,0)→LIFT4..1→FOLD→LIFT1..3→raised V
  7. fold↔LIFT1
  8. V→LIFT3..1→fold
- Re-run your step-1 pass after the change anyway.

### 2. STORM dorsal saddle under the mantle (kills the shark teeth; tested)
The teeth come from contrast: dark shingles on a teal field. Put a dark field under them. Add these right after the
shingle code (exactly what I rendered):
```python
B.add(chest.world(Vector((0, 0.09, 0.0))), (0.25, 0.17, 0.25), STORM, "Chest", R=chest.R, bot=(0.62, 0.56),
      top=(0.92, 0.92), rnd=0.40)                      # dorsal saddle: chest back
B.add(low.world(Vector((0, 0.07, 0.0))), (0.185, 0.14, 0.16), STORM, "Spine", R=low.R, bot=(0.72, 0.66),
      top=(0.92, 0.9), rnd=0.38)                       # dorsal saddle: lower back
```
- The mantle shingles stay STORM, so they become tonal feather texture.
- The teal flanks and breast stay teal, because the saddle is narrower in x than the chest.
- From above in flight, a dark back between teal-covert wings reads as a raptor (`cmp_varB.png` row 3).

### 3. Arm bar: teal shoulder patch, storm to the wrist (removes the rails; tested)
Replace the single TEAL arm seg with:
```python
Wm = S0.lerp(W, 0.38)
B.seg(S0, Wm, 0.06, 0.09, TEAL, wb, side=nrm, ext=0.05, role="limb", top=(0.95, 0.95))
B.seg(Wm, W, 0.057, 0.085, STORM, wb, side=nrm, ext=0.01, role="limb", top=(0.85, 0.8))
```
- Then make the wrist knuckle block STORM too.
- Result: from behind, a short teal shoulder patch per side (a real raptor feature), not two rails.
- In flight, the leading edge goes light at the shoulder and dark toward the wrist, under the COVERT upper wing.

### 4. Face (prototyped; `cmp_face.png` bottom row)
- **Eye:**
  - Delete the pupil block.
  - Make the socket lid-heavy: centre `c + R @ (s*0.003, 0, 0.007*sc)`, half `(0.053*sc, 0.008, 0.026*sc)`.
  - The black then shows as a heavy upper lid plus a thin lower line: a narrow, angry raptor eye, not a framed window.
- **Brow:** move it back 0.014 in y (overhang ≤ 0.025), which I tested. Optionally also taper its front
  (top=(0.8,0.85), not tested). The side view should show a ridge, not a pale cap.
- **Hook:**
  - Spike 0.13 → **0.09**, dir (0,-0.25,-1) → **(0,-0.55,-1)**, start `HC + (0,-0.365,-0.05)`.
  - It continues the bill's curve instead of hanging like an icicle.
- **Crest (tier fix: no crown on a 5%):**
  - Back-row rise (30,36,33,27) → **(16,22,19,14)**; front row (42,46,40) → **(26,30,24)**.
  - x-spread factor 6.5 → **3.0**.
  - From the front only the tips peek over the head. From the side and the game camera it is a swept harpy crest,
    still the top of the head silhouette (`cmp_varD.png` front column).
  - **Check (see clips):** the lower crest sits closer to the nape.

### 5. The withers fin
- A thin dark plate stands edge-on at the withers, just behind the white cape (`zoom_fin.png`; it is in v2 and in my
  variant).
- Most likely it is the top mantle row (local z 0.20, x ±0.12) placed on the flat-face assumption over the chest's
  rounded top edge (Lessons #2).
- Seat it 0.02 lower, or drop the outer two of that row. Verify with a 2x crop of fold side and model side.

### 6. Trousers: rounder, narrower, ragged
- Shin seg hw 0.08 → **0.07** at the knee, flaring to **0.085** (not 1.25x).
- x stays ±0.16; rnd 0.45.
- Fringe: **7 spikes** all around the cuff, L 0.12-0.15, alternating STORM / PRIMARY.
- Target in the front view: the trouser outer edge stays inside the belly silhouette (≤ x 0.22), and the cuff reads
  as feathers, not a box edge.

### 7. Tail seen edge-on from the front
- Cup the fan: add `+0.10 * abs(a)` to each feather direction's z. The outer tips rise, so from the front the fan
  becomes a shallow V behind the legs instead of a flat bar at knee height.
- Re-check Tail2 vs WingTip at the new FOLD; the wingtips now ride 0.27 above the fan tip, so there is room.

### 8. Deliverables
- Re-render `model_tq` at 600 px (run `headless_closeup` before `headless_model`, or re-run the model render last).
- Add the 64 px strip, built from the idle f0 portrait.
- **Keep idle f0 (folded) as the Index portrait.** I tried the raised V as an icon pose: from the tq camera the wings
  go edge-on and the pet shrinks to a thin sliver at 64 px (`strip64_storm_egg.png`, last column).

### 9. Export hygiene
`WDX` and `TAIL_SPREAD` read `TB_DX` / `TB_TS` from the environment. Bake the final values as plain constants before the
export run, so a stray shell variable can't change the shipped mesh.

**Not blocking, accepted:**
- GOLD is 9-9.6% in tq, above my 4-7% target, because the beak and feet are bigger. It reads right.
- BOLT+HOT is 8.4-8.7% in tq; it is 15-20% from behind, where it matters.
- Side STORM+PRI is ~50% after the fixes. That is natural for a folded dark-winged eagle, and no single colour exceeds
  30%.

---------------------------------------------------------------------------------------------------------------------
## 3. Clip plan changes for this geometry
- **Constants:** FOLD = (86,10,-80,0). LIFT1-4, BREATH and RAISED_V are unchanged and all re-tested (above), including
  the 1-frame stoop/throw keys. No other wing pose needs to change.
- **Crest vs cape:**
  - The lowered crest lies nearer the nape.
  - In roar (Head -12, Neck -6) and the talonstrike scream, check that the crest doesn't cut the hackle cape or mantle.
  - Add ("Head","Neck") to `check_pairs()` (rest-pose contacts are ignored by `overlap_report`) and inspect those
    frames at 2x.
- **Legs (new joints):**
  - Add ("Shin_L","Spine") and ("Shin_R","Spine") so the trousers can't swing through the flank skirt in the walk
    or the stoop's FK throw.
  - Watch ground_min_z on the hallux talon (0.11, backward) at toe-off.
- **Fly pitch:**
  - The rest body already leans 46-52°, so FPITCH 40 now gives a near-horizontal body (good for an eagle).
  - Don't go above 40.
  - Retune FHEAD so the beak points forward and the head stays level (gyro head from review 1).
- **Tail:**
  - The fan is one bone at ±38°. In the stoop and the land, pitch it up (-12..-14) for the flare.
  - Re-check Tail2 vs WingTip on the stoop's FOLD/tuck frames with the tail pitched.
- **Strike anchor** (0,-0.23,0.02) matches the 0.18 reach in front of the toes. Keep it.
- Everything else in review 1 §4 stands:
  - idle without the 58° whip
  - walk with a gyro head and a rolling strut
  - takeoff and land through the waypoints
  - SKY SCREECH with the raised V and 2 beats
  - STOOP STRIKE

---------------------------------------------------------------------------------------------------------------------
## 4. Verdict for the coordinator
- **REVISE (light), 6.5/10 now.** About **8/10 once fixes 1-4 land**; my test build of 1-4 already looks the part
  from every camera.
- **Order:**
  1. Fixes 1-3 first. They change the rig geometry and the FOLD constant.
  2. Then start authoring the clips right away. The waypoints are final, so no need to wait for me.
  3. Fixes 4-9 can go in alongside.
- **Round 3, send together:**
  - fold sheet (incl. game cam)
  - model sheet with a 600 px tq
  - close sheet
  - 64 px strip
  - pose sheet of every clip
  - the collision/audit pass
- If fixes 1-8 match this brief, round 3 is the model approval plus the clip review in one pass.
