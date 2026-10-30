# Thornblade Mantis - art director review 2 (2026-10-14) - APPROVE WITH FIXES

**Score: 7.5/10 for a 2% SECRET (v1: 5/10).** With must-fixes M1-M4 applied, expect about 8.5.

This is now a real secret. From the game camera it reads as an armoured royal mantis:
- a dark thorny shield
- a big gold crown with ruby eyes
- gold knee spines
- a gold-trimmed leaf with ruby stigmas

In the portrait it reads as a crowned executioner holding two gold scythes. It is the most colourful, most premium pet
in the Grass egg, and at 128 px it holds its own next to Thunder Rex and the Basilisk. Do not redesign anything.

**What is left is finish quality, all in code:**
- the gold and ruby are studded
- the ruby "thorns" read as maroon dice
- the eyes are maroon from behind
- the pupils sit on the outer side (wall-eyed)

I tested every must-fix below in a temp copy of the file. The numbers are verified, not guessed. My renders are in
`C:\Users\ventu\AppData\Local\Temp\mantis_rev\v2\out\`:
- `orig_*` = your v2
- `fix2_*` = v2 + M1-M4
- `cmp_tq_game.png`
- `fix2_hind_under_w.png`
- `v2_strip_128.png`

**No new full model round is needed.** Send one updated model sheet, close sheet and arm close-up together with the
clip pose sheet.

What I looked at:
- `pets/ThornbladeMantis.py` (v2d)
- all sheets, single renders and icon strips
- my own transparent re-builds: tq, game, side, front, back, head front/tq/game, arm tq/front, and the hindwings from
  above and below with the tegmina hidden
- my 64/128 slate strips: v2, v2+fixes, Basilisk, Rex

Measurements:
- **Your flat palette-ID:** game ARMOR 46 / HIDE 30 / ruby 4.5; side BELLY 7.8. These pass review-1 targets 2 and 3.
- **My shaded classifier** (BELLY inflated by speculars): game ARMOR 33 / HIDE 35. That is v1's 27 / 51 turned
  around, so it agrees with yours.
- **Crown:** about 5% of pet pixels on its own in tq and game (target ≥ 3%), so it is the largest single gold mass.
  Total GOLD in tq is about 16%, mostly the two scythes. That is acceptable, since they are hero #2.
- 11.5k tris. Bounds top 1.612 = the crown tip.

---------------------------------------------------------------------------------------------------------------------
## 1. Review-1 checklist (section 4)

| # | item | result |
|---|---|---|
| 1 | 64 px slate icon | **PASS.** I can name a mantis, a gold crown and ruby eyes. The crown is the largest gold mass, and there is no white blob. It has less body mass than the Basilisk and Rex; that is mantis anatomy, and the gold/ruby make up for it |
| 2 | Game camera | **PASS with M3.** Shield, thorns, crown, back gem and knee spines all read. ARMOR/HIDE/RUBY targets met. **But from behind the eyes are mostly RUBY_D maroon** (the rim ellipsoid sits behind the body), and the ruby thorn tips on the shield are specks |
| 3 | Side view | **PASS.** Three bands; the mint sternite stripe reads; no picket fence |
| 4 | Face close sheet | **PARTIAL.** No mask; the domes rise above the head line; the V-brow lids the eyes; antennae clear of the brows. **Fail:** the pupils sit on the outer side, so the eyes look wall-eyed or derpy; the deep crescent on the inner side reads as a "tyre" from the front; the mouth plate reads as a pale tag |
| 5 | Arms | **PARTIAL.** Dark femurs, a 0.08-deep gold crescent, gold knee spines, no jade slabs. **Fail:** the ruby saw reads as clusters of maroon DICE, not thorns (`ruby_gem` at 0.05-0.075 is mostly a fat RUBY_D box) |
| 6 | Silhouette | **PASS.** The crown tip is the top (1.612); HEIGHT 10 studs measures to it |
| 7 | Rig | **PARTIAL.** Antenna_L fixed. `check_pairs()` is unchanged; the review-1 §3.2 pairs and the VFX anchors are still missing (M5) |
| 8 | Hard rules | **FAIL (easy).** All the gold and ruby made with `B.spike` / `B.add` without `nostud=True` get the stud skin: the cone is visibly studded (a party hat from the side). Only the crescents and the shield ruby tips are smooth. Otherwise: no Neon, 11.5k tris, nothing floating |
| 9 | Deliverables | **PARTIAL.** `renders/model_tq.png` was overwritten at **200 px** again (by headless_closeup); re-render it at 600. The hidden-tegmina render is missing, so I made it: **W1 passes**, and the ruby eye-spots read from above and below |

---------------------------------------------------------------------------------------------------------------------
## 2. MUST-FIX before clips (all tested)

### M1 - Smooth gold and ruby (hard rule; the biggest quality win per line)
Add `nostud=True` to:
- **crown:** band, cone, both side prongs, GOLD_D keel, gold back plate
- **knee spine** `B.spike(F1 + ...)`
- **gold tibia** `B.seg(F1, T1, ...)` and the **hook** spike
- **all three spikes inside `ruby_gem`** (replaced in M2)

The crescents and the shield ruby tips already have it. After this, the cone reads as a polished gold spire, not a
studded party hat.

### M2 - The ruby saw must read as THORNS, not dice
In `ruby_gem` the RUBY_D base runs the full length, is 0.55× wide and only tapers to 0.7. It swallows the ruby body,
so each gem is a maroon cube with a pink dot. Replace it with a short socket, a long slender ruby body and a hot point.
That is roughly a 3:1 thorn that shows the DEEP→MID→HOT steps:

```python
def ruby_gem(B, c, n, size, bone):
    """thorn: short deep socket -> long slender ruby body -> hot point"""
    n = Vector(n).normalized()
    c = Vector(c)
    B.spike(c - n * 0.01, n, size * 0.40, size * 0.34, RUBY_D, bone, top=(0.75, 0.75), nostud=True)
    B.spike(c + n * size * 0.22, n, size * 0.88, size * 0.30, RUBY, bone, top=(0.10, 0.10), nostud=True)
    B.spike(c + n * size * 0.80, n, size * 0.36, size * 0.13, RUBY_HOT, bone, top=(0.08, 0.08), nostud=True)
```

- Tested result: red crystal thorns with pink points; ruby stays at ≥ 4% in the game view and 5.7% in tq.
- Optional: outer-row sizes 0.075/0.05 → 0.085/0.06 to win back some red mass. Check the tips stay off the tibia.

### M3 - Eyes: ruby from every side, pupils looking FORWARD (L216-221)
- From behind (the game camera) the eyes are RUBY_D, because the deep rim is the bigger ellipsoid and the body is
  pushed forward.
- The pupil direction `(-s*0.12, -0.98, 0)` is in the eye's yawed frame, so in world space it points 0.19 OUTWARD.
  That gives the wall-eyed look.
- Make the RUBY body the big ellipsoid and tuck the deep rim back and low, so it reads as a shadow crescent:

```python
ellipsoid(B, e + Re @ Vector((-s * 0.004, 0.014, -0.012)), (0.066, 0.064, 0.084), RUBY_D, "Head", Re, n=24, rings=14)
eb, axb = e + Vector((s * 0.006, -0.008, 0.006)), (0.069, 0.067, 0.089)                       # ruby body (bigger)
...
ellipsoid(B, on_surf(eb, axb, Re, (-s * 0.5, -0.86, -0.16), 0.95), (0.009, 0.012, 0.032), BLACK, "Head", Re,
          n=12, rings=6)                                                                       # pupil: inner-front
```

**Tested:**
- Game camera: red domes with a deep crescent at the back-bottom.
- tq / front: the pupils sit at the inner-front, half under the brow lid, so the stare converges forward. That reads as
  a glare.
- The pupil at n=12, rings=6 saves about 0.8k tris.

Keep the RUBY_HOT glint OUT. You were right that it read as cute.

### M4 - Crown jewels: flush diamond inlays, not cubes
The 0.06 front gem and the 0.045 back gem (also `ruby_gem`) read as a red button in front and a maroon cube on the back
of the head. Use a flush 45° diamond, deep frame → ruby → hot glint (Ivonrath's rotated red gem, scaled up):

```python
def gem_inlay(B, c, n, size, bone):
    n = Vector(n).normalized()
    x = Vector((0, 0, 1)).cross(n).normalized()
    z = n.cross(x).normalized()
    Rr = Matrix((x, n, z)).transposed() @ Matrix.Rotation(math.radians(45), 3, "Y")
    kw = dict(R=Rr, studs=[], nostud=True, role="detail")
    B.add(c, (size, 0.008, size), RUBY_D, bone, bevel=0.004, **kw)
    B.add(c + n * 0.006, (size * 0.72, 0.007, size * 0.72), RUBY, bone, bevel=0.003, **kw)
    B.add(c + n * 0.011 + (x + z) * size * 0.25, (size * 0.16, 0.004, size * 0.16), RUBY_HOT, bone, bevel=0.002, **kw)

gem_inlay(B, HC + Vector((0, -0.064, 0.12)), (0, -1, 0), 0.034, "Head")    # front
gem_inlay(B, HC + Vector((0, 0.076, 0.115)), (0, 1, 0), 0.026, "Head")     # back (game camera)
```

### M5 - Rig prep (before keying anything)
1. **Add these posed-check pairs** to `check_pairs()` (review-1 §3.2):
   - (Head, Chest)
   - (Elytra_L/R, Chest)
   - (Wing_L/R, Chest)
   - (Fore_L/R, Chest)
   - (Fore_L/R, Leg_FL/FR)
   - (Blade_L/R, Leg_FL/FR)
   - (Antenna_L/R, Blade_L/R)
   - (Antenna_L/R, Fore_L/R)
   - (Elytra_L, Wing_R)
   - (Elytra_R, Wing_L)
2. **VFX anchor bones:**
   - `Crown` at the cone tip (0, -0.437, 1.61), on Head
   - `EyeSpot_L/R` at `X(leaf(s, 0.55, 0.45), ...) - (0, 0, 0.026)`, on Wing_L/R
   - `BladeTip_L/R` at the claw tip, on Blade_L/R
   - Keep `Strike`, but move it after keying to the strike-2 X-cross point (about (0, -0.95, 0.75)), on Chest.
3. **Mandible_L/R: not needed.** The mandibles are invisible from the game camera, and a Jaw pitch clack reads well
   enough. Skip them.

### M6 - Deliverables
Re-render `model_tq.png` at 600, and keep a tegmina-hidden top + bottom render in `renders/` for the roar check.

---------------------------------------------------------------------------------------------------------------------
## 3. Should-fix (cheap, do them with M1-M4)

| # | change | why |
|---|---|---|
| S1 | Mouth plate (L198) BELLY_D → **ARMOR** (or delete it) | It reads as a pale tag on the chin. Tested: ARMOR reads as a dark clypeus |
| S2 | Shield thorn ruby tips: start at **0.5 L**, length **0.6 L**, w 0.014 → **0.02** | From the game camera they are specks, and that view sells "Thornblade" |
| S3 | Antenna roots `ANT0.x` 0.03 → **0.055** | They cover the sides of the front gem; this frames it instead |
| S4 | Hindwing eye-spot centre `leaf(s, 0.55, 0.45)` → **(0.55, 0.40)** | The black outer disc pokes about 0.01 past the wing's outer edge (visible from below) |
| S5 (optional) | Two GOLD_D ring bands on the cone at 35% and 65% of its height (0.008 proud) | Turns the plain cone into an ornamental spire from the side |

---------------------------------------------------------------------------------------------------------------------
## 4. CLIP BRIEF (final; replaces review-1 §3 where they differ)

**Owner rule first:**
- Pull 1-3 reference clips from animationreference.org (a mantis strike, an insect or deimatic threat display, a
  predator stalk), note the key poses and frames, and cite them in the clip docstrings.
- Feet stay planted (`plant_frames`) in idle, roar and thornstrike.

### Pose limits
| joint | limit |
|---|---|
| Neck | ≤ 8° |
| Head + Neck pitch | up ≤ 30°; down ≤ 20° (≤ 15° while yaw is over 15°) |
| Head yaw | ±25° |
| Head roll (tilt) | ≤ 15°. One tilt + hold + return. **Never alternating L/R = no head shakes** |
| Chest vs Spine | pitch -10° (lower) .. +12° (rear), yaw ±8°, roll ±4°. The shield meets the tegmina root past +12° |
| **Arm rule (new, geometry v2)** | The knee spine sits just under the eye dome. **Whenever Arm pitch-up > 5°, Arm yaw-out must be ≥ 12°**, so the knee x stays ≥ 0.27 while its z > 1.05. Pitching the arm up with no yaw drives the knee spine into the eye (computed: knee z 1.11 at x 0.21 for +20°). Lead with the yaw, ≥ 2 f before the pitch |

### idle (~120 f, loop)
- **Leaf-sway:** Spine roll ±3° and x ±0.015, 40 f period. The head counter-rotates so the gaze stays level (the
  predator head-lock).
- **One predatory tilt:** roll 12° in 5 f, hold 25 f, back in 8 f.
- **One groom:** Blade_L rises to the mouth (≥ 0.02 clearance), with Jaw chomps ×2.
- **Antenna flicks:** alternating, ±12°, 3 f.

### walk
- Gait: diagonal pairs (F_L+B_R / F_R+B_L), duty about 0.6, slide 0.
- Blades held folded, with a 2° counter-swing.
- Chest counter-yaws against Spine; the head stays world-stable with a small lag; the abdomen lags 2-3 f.
- Keep a low leaf-rock layer for the jerky mantis walk.

### roar - deimatic display (90 f)
| f | beat | keys |
|---|---|---|
| 0-10 | crouch | Spine z -0.04, pitch +4; Chest -6; Head -6; Fore +8 (tuck); antennae back -25 |
| 10-20 | rear | Spine z +0.035, pitch -10; Chest +12; Neck +6; Head +12 (sum 18) |
| 14-26 | fan | Elytra f14→24: pitch +65, roll out +40 (V). Wing f16→26: pitch +80, roll out +15 (2 f lag). Tail1/2/3 curl up -8/-12/-16 |
| 16-26 | arms spread | **Arm yaw out 30 from f16; pitch up 20 only from f18** (arm rule). Femurs raised; Blade open 75; Jaw open 18. **`display` f24** |
| 26-60 | hold | Wing roll shiver ±3/3 f; Jaw clacks f34/f44 (`clack`); Blade pumps 75→60→75 at f38-42 and f50-54; Spine rock ±2; antenna twitches |
| 60-76 | fold | Wing 80→0 over f60-70 FIRST, then Elytra 65→0 over f64-74 (they close over the hindwings); blades fold f60-72; Chest 0 by f76 |
| 76-90 | settle | Spine z -0.01 overshoot at f84 → rest |

**Check frame f30** in tq, front and game:
- both eye-spots whole (front: the top discs; game: the underside discs)
- both gold tibiae open
- the crown above the wings
- no clipping

### act_thornstrike - "THORN STRIKE" (100 f; there is no blade act in the roster)
| f | beat | keys |
|---|---|---|
| 0-14 | lock-on + peering | Chest -8; Head -8 (locked); Spine x +0.025 (f4) → -0.025 (f9) → 0 (f14); antennae forward. `lockon` f6 |
| 14-24 | cock + tell | **Arm yaw out 12 (from f14), pitch up 8 (from f16)**; Fore leans back -10; Blade folds -10 tighter; Spine z -0.03, y +0.02; Chest -10. **Hold f20-24** |
| 24-27 | STRIKE 1 | Arm → pitch -45 (forward-down), yaw back to 0; Fore extends -50; Blade OPEN 85 at f25, CLOSED 10 at f27; Spine y -0.07, pitch +6. `strike1` f25 |
| 27-33 | recoil | Arm -10 (half-cocked), small overshoot |
| 33-36 | STRIKE 2: X-cross | Arms sweep in-down, yaw in ±18. L leads by 1 f and passes 0.05 higher (Arm pitch offset 6°); Blade open-snap; Spine y -0.09. `strike2` f34 |
| 36-50 | executioner hold | Blades crossed low in an X, tibiae closed; ONE head roll of 12°; Jaw 15. `finish` f36 |
| 50-72 | retract + groom | Prayer pose by f60. Head -8; Blade_L to the mouth (≥ 0.02); Jaw chomps f64/f69 (`groom` f64) |
| 72-100 | settle | Head roll back; antenna twitch at f80; Spine z micro-dip; rest |

- Hard stops on f25 / f27 / f34. The 4 f tell before each snap is what makes a 2 f strike readable.
- Reach ≤ 0.6 in front of HC (about 3.8 studs at x1).

**Return:**
- a pose sheet: roar f10 / f24 / f30 / f50, thornstrike f20 / f25 / f34 / f40 / f66, idle tilt hold, walk contact
- `collision_free` with the extended pairs; slide 0; loops closed
- the M1-M4 model sheet, close sheet and arm close-up
