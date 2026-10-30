# Abyss Weaver - CLIP review (review 2, 2026-10-14)

## Verdict: CLIPS APPROVED WITH 2 MUST-FIXES - 8 / 10 as delivered, about 9 with the fixes below

The clips follow the brief closely, and the hard gate holds. I reproduced it on a temp copy:
- `collision_free` at step 1 on all 4 clips, with every section 5.5 pair and 5.6 capsule
- linear 0; idle and walk loops exact; walk slide 0 and foot_z_var 0; idle planted drift 0
- ground -0.0054 on every clip; events as reported; 11,956 tris

What the gate can't see is *motion quality*. I sampled the world position of 18 key points on every frame of every
clip (`motion.py`: mid-move speed dips = hitches, one-frame speed spikes = pops). That found two must-fixes:
1. **Roar thrum / rasp are square waves.** The abdomen holds 2 frames, then jumps 4 deg in one frame, every 3 frames
   from f23 to f53. The spinneret moves 0.079 per frame (about 0.6 studs), then 0, 0: a 10 Hz judder, not a thrum. The
   palps do the same at 0.049 per frame.
2. **The act's cast is a soft double-pump, not "tell -> snap -> hard stop".** `curve()` smoothsteps every segment, so
   the f77 in-between key has zero velocity. Spinneret speed f74-80: 0.072, 0.149, 0.127, 0.126, 0.148, 0.073. The
   whip pumps twice and eases *into* f80.

The fixes for both, plus three polish items (C1-C5), were tested together in one temp build; optional C6 was tested
with C1-C4 in a second. In both, every clip stays collision-free, linear 0, loops exact, ground -0.0054. No re-review is needed if they are applied verbatim. Return the motion numbers
in section 4 with the export round.

Temp test files are in `C:\Users\ventu\AppData\Local\Temp\weaver_rev3\`:
- the spec copy is `spec\AbyssWeaverC.py`; env `WFIX` flags select fixes: `thrum,flare,swing,cast,land` = C1-C5,
  `draw2` = C6
- `drv3.py` builds and runs the audit, step-1 collisions, ground check and per-frame sampling; `motion.py` runs the
  hitch/pop analysis
- in `out\`: `c0_motion.json` (as delivered) and `c3_motion.json` (fixed); `act_grid.png`, `roar_grid.png`,
  `c_land.png`, `c_draw_game.png`

## 1. Does the pack confirm FIX 1-3? YES
- **FIX 1:** `_face_close` from the portrait direction shows narrowed, lidded orchid eyes with slit pupils, a V-brow
  and no glint. The crown's front band is visible again, and the eyes read on the 128 portrait icon.
- **FIX 2:** `_rift_close` (tq / game / top) shows a meandering crack with 2 fractures and a torn orchid edge in the
  closed gold frame. It reads as a cracked crystal of light, not an eye.
- **FIX 3:** the side view shows a clean band (no red diamond).
- **Shares:** all in range. tq dark 69.9, tq SILK 1.1, game VELVET 9.2. BLACK is correctly labelled as an edge
  artefact.
- **Gold:** I re-counted your new icons with my own script and get **56 / 86 with the brief's counter** (gate
  >= 45 / >= 60). The builder's counter gives 46 / 73; your 45 is anti-aliasing noise.
  - My temp build had measured 47 / 83. The likely cause is that your portrait now uses the real idle f0: the
    abdomen is about 0.9 deg rear-up, which tips the rift toward the camera.
- **Tris:** 11,956, matching my temp build.

## 2. Per-clip verdicts
| clip | verdict | notes |
|---|---|---|
| idle "STILL HUNTER" | **APPROVED as is** | No pops. Loop-seam speeds match (spinneret 0.0041 / 0.0044 per frame). One-way listen turn with the head leading by 2 f. Taps solved every frame; fang flex, rasp and pump as briefed. |
| walk "SCUTTLE" | **APPROVED as is** | Slide 0, foot_z_var 0, exact loop. The 4 abdomen speed dips per cycle are bob/yaw turnarounds (0.001-0.009 per frame), not hitches. |
| roar "FANG FLARE" | **APPROVED WITH FIXES** C1 (must), C4 + C5 (should) | The s35 front "V" reads; from the game cam it's a big threat silhouette. Side "lances" accepted. The 34-frame body freeze (f20-53) is accepted: a still spider is a real threat behaviour, and the rasp, thrum, tremble and stab keep it alive. A "moving hold" would push the leg-1 ankle past 1.32. |
| act_riftweave "RIFT WEAVE" | **APPROVED WITH FIXES** C2 (must), C3 (should), C6 (optional) | **PRESENT works:** the rift-normal dot game-camera rises from 0.557 at rest to 0.766-0.798 at f24-74, about 40 % more projected area (target >= 70 % of rest). Events on the beats. The R4 draw reads from the game cam; the L4 draws barely do (C6). |

## 3. Clip deviations
- **W1 APPROVED.** Palps lift -6 in the crouch. The brief's +12 "tuck" drove the tips 0.053 into the ground.
- **W2 APPROVED.** Flare palps at pitch +12 with a +-7 rasp, inside the femur-clear +5..+19 band. With C1 the rasp
  becomes a sine of the same amplitude; re-verified collision-free.
- **W3 APPROVED.** FK starts at f14 / f16. The handoff is clean: the leg-1 ankle moves only 0.022 on f13 -> 14.
- **W4 APPROVED.** The raise and land values are right, the s35 shin yaw eases in with the opening, and the peak is
  (0.479, -1.594, 1.305). The leg-1 landing gets C5.
- **W5 APPROVED.** The fang stab is 65 -> 53 -> 65. "+12" on a -Z bone swings the tip back, which is a spider's real
  strike, and it respects the 70 limit.
- **Events `pulse1` / `pulse2` APPROVED.** When the owner wires `CreatureVFX`, both must trigger the Rift swell (the
  brief's `pulse`).

## 4. Fixes (exact code; all tested together)
### C1 (MUST, roar): continuous thrum and rasp
In `roar()`, replace the two step-function lines:
```python
        thrum = 2 * math.sin(2 * math.pi * (f - 24) / 6.0) if 24 <= f <= 54 else 0      # +-2 every 3 f, continuous
        ...
        rasp = 7 * math.sin(2 * math.pi * (f - 26) / 4.0) if 26 <= f <= 50 else 0       # +-7, period 4 f
```
- Both start and end on 0, so there's no pop at f24/f54 or f26/f50.
- Measured: the spinneret peak drops from 0.079 to 0.034 per frame, the abdomen tip from 0.063 to 0.027, and the
  palp tip from 0.049 to 0.041. The detector flags no pops.
- Keep the leg-1 shin tremble as is (keys every 3 f, Bezier: already smooth).

### C2 (MUST, act): the cast snaps and stops hard (ref #5)
Let `curve()` take an optional 3rd item, `"in"` = accelerate into that key:
```python
def curve(keys, f):
    """smoothstep through (frame, value[, ease]) keys; a 3rd item "in" on a key = accelerate INTO it (u * u: a snap
    with a hard stop on that key)"""
    for k0, k1 in zip(keys, keys[1:]):
        (f0, v0), (f1, v1) = k0[:2], k1[:2]
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            e = u * u if (len(k1) > 2 and k1[2] == "in") else u * u * (3 - 2 * u)
            return v0 + (v1 - v0) * e
    return keys[-1][1] if f > keys[-1][0] else keys[0][1]
```
In `act_riftweave()`. This includes C3: the `(18, 0)` key is gone.
```python
    pc = [(0, 0), (12, 3), (24, -6), (74, -6), (80, 2, "in"), (96, 0), (120, 0)]
    ped = [(0, 0), (12, 0), (24, -4), (74, -4), (80, 2, "in"), (100, 0), (120, 0)]
    abd = [(0, 0), (12, 8), (24, -8), (74, -8), (80, 10, "in"), (92, -2), (100, 0), (120, 0)]
```
- Measured spinneret speed f74-80: **0.020, 0.059, 0.096, 0.134, 0.173, 0.215, then 0.008**. That is one
  accelerating whip and a dead stop on the `cast` frame; the settle (smoothstep from f80) is the recoil.
- The f77 in-between is no longer needed: keys are every frame and the swing is 18 deg over 6 f. The brief's > 60 deg
  rule doesn't apply.

### C3 (should, act; already inside C2): one continuous wind-up -> PRESENT swing
- Removing `(18, 0)` turns the double hump (0.068 / 0.047 / 0.068) into one bell peaking at 0.075.
- PRESENT and the rift facing are unchanged.

### C4 (should, roar): one-segment fang flare
```python
    unf = [(0, 0), (18, 0), (24, 65), (38, 65), (40, 53), (44, 65), (54, 65), (62, 0), (72, 0)]
```
- This drops `(22, 45)`, its zero-velocity dip at f22. Measured: a single bell peaking at 0.0755 per frame at f21.

### C5 (should, roar): legs 1 come DOWN onto their spots
**Problem:** at f64 the leg-1 ankle is still 0.31 in front of its spot with the claw about 0.08 up. In f64 -> 66 it
travels 0.21, then 0.11, skimming just above the ground: a scrape-in.

**Fix:** add after the three `plant8` calls, before `k.finish()`:
```python
    k.bake_bezier_now()
    for leg in ("Leg1_L", "Leg1_R"):                 # land from above: f64 over the spot, f65 just above, f66 planted
        foot = k.legs2[leg]["foot"]
        spot = k.J[foot].copy()
        bpy.context.scene.frame_set(64)
        fk64 = k.arm.matrix_world @ k.arm.pose.bones[foot].head
        for f, P in ((64, spot.lerp(fk64, 0.25) + Vector((0, 0, 0.10))), (65, spot + Vector((0, 0, 0.03)))):
            bpy.context.scene.frame_set(f)
            ankle_to(k, leg, f, P)
```
**Measured, horizontal offset / ankle z per frame:**

| frame | offset | ankle z |
|---|---|---|
| f63 | 0.349 | 0.343 |
| f64 | 0.078 | 0.220 |
| f65 | 0.000 | 0.130 |
| f66 | planted | |

- The landing is now vertical and collision-free.
- The knee fold now spreads over f63 / f64 (0.099 and 0.092 per frame) instead of one 0.085 spike at f65 (`c_land.png`).

### C6 (optional, act): draw target more OUT + UP, less BACK
- **What I saw:** from the kit's game camera (+x side, high behind) the two L4 draws barely read. Out-back-up points
  at the lens: "back" and "up" cancel on screen, so the leg looks planted. The R4 draw reads well.
- **Raising z alone (0.58) does not help** (tested).
- **What was tested:** `T = Vector((s * 1.10, 0.55, 0.58))`. Collision-free, reach about 0.71, inside the leg-4 limit
  0.60. It pushes the claw further out and the silk beam becomes more lateral.
- **Expect only a small gain.** The draw's real read is the motion plus the Spinneret -> Silk beam VFX, so do this
  only if the owner says the draws don't read in Studio.

## 5. Not changed (checked)
- The walk palp phase, the idle body turn absorbed by the planted legs, act pumps / spinner flicks / pedicel-away
  yaw, the FK -> IK handoffs at f13/14 and f15/16: all measured smooth.
- The optional Leg2 shin yaw and SILK_D spinneret tips stay optional.

## Summary
**Clips APPROVED WITH FIXES, 8/10, about 9 after C1-C5.** The pack confirms FIX 1-3 (eyes, crack, band); shares are
all in range; gold is 56 / 86 by the brief's counter.

Must-do:
- **C1:** roar thrum and rasp become sines. The square waves judder the abdomen 0.6 studs every 3rd frame.
- **C2:** `curve()` gets an `"in"` ease, and the act's cast keys become `(80, …, "in")` without the f77 key, for a real
  snap and a hard stop at the `cast` event.

Should-do:
- C3 (inside C2): one wind-up -> PRESENT swing.
- C4: one-segment fang flare.
- C5: legs 1 land from above.

Optional:
- C6: a more lateral silk-draw target.

C1-C5 were tested together in one build, and C6 with C1-C4 in another. Both builds were collision-free at step 1,
with linear 0, loops exact and ground -0.0054.
W1-W5 are all approved. Ready for export once C1-C2 (ideally C1-C5) are in.
