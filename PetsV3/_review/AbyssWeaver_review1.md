# Abyss Weaver v1 - MODEL GATE review 1 (2026-10-14)

## 1. Verdict: APPROVED WITH FIXES - 7.5 / 10 as delivered, about 8.5 with the 3 fixes below

This is the strongest first model of the new-secrets round. It follows the brief closely: the numbers, shares, rig and
limit poses all reproduce exactly (my rebuild gives 11,852 tris and the same share table to 0.1). It reads as a fierce
crowned widow-queen, not a Halloween prop. It has the only 8-legged silhouette in the game, and two gold heroes cover
both cameras.

Three things hold it back, and all three are fixed and tested on a temp copy:
1. From the portrait camera the V-brows hide the two main eyes almost completely, so the icon loses its "burning eyes".
2. The rift (a straight white line in a closed gold almond) reads as a cat's eye from the top. It also carries an
   anatomical-shape risk in a kids' game.
3. The belly band's 4-ring chords let the wine hull poke through it: a red diamond on the white band in the side view.

No full re-gate is needed. Apply FIX 1-3 verbatim and put these in the clip-round pack for confirmation: the
portrait-direction face close-up, the rift close-up (game + top), the side view, and the 64/128 strip.

**How I tested:** a temp copy `C:\Users\ventu\AppData\Local\Temp\weaver_rev2\spec\AbyssWeaverR.py`, with variant
flags in env `WFIX`; `eye3,crack,band,bandb` = all fixes. Built with `weaver_rev2\drv.py`, with petkit ROOT redirected
to `weaver_rev2\out`. Limit poses ran through a redirected copy of pose_try (`weaver_rev2\pose_try_r.py`). Evidence is
in `weaver_rev2\out\`:

| file | shows |
|---|---|
| `c_face2.png` | rows: base, eye2 (with HOT spot), eye3 (final), all from the portrait direction |
| `c_rift.png`, `c_rift2.png` | rift variants (see Q1) |
| `c_belly.png` | the band poke-through |
| `c_roar.png`, `c_roar3.png` | the roar leg-1 yaw tests |
| `c_final.png` | the final face + rift close-ups |
| `s_void_128.png`, `s_secrets_128.png` | icon strips |

Nothing in the project was touched except this file.

## 2. Section 8 checklist (v1 as delivered)
| # | item | result | reason |
|---|---|---|---|
| 1 | silhouette | PASS | H 1.10 at the pair-2 thorn tips. Bounds x +-1.06, y -1.148..1.24, z -0.005..1.10, all within 0.05 of section 3. Long egg abdomen rising to a point; 4 leg segments. |
| 2 | front view | PASS | crown over the 8 eyes; V-brows; 4-eye frown row; two separate daggers (tips 0.05 apart); the rift's gold front shows over the crown; leg "A" |
| 3 | game camera | FAIL (minor) -> FIX 2 | Rift faces the camera; crown ring ahead; wine seams, red knees and orchid thorns all round. But the straight HOT line in the almond reads as a gem highlight or eye, not a tear. Belly band: only a 1-2 px flank sliver (FIX 3 trims it). |
| 4 | 64 px strip | PASS | Crowned spider + gold crown + gold-framed glowing slit all nameable. Gold 48 / 83 with the brief's counter (section 4 of this review). The most striking of the Void row. |
| 5 | cute traps | PASS | No ball, stilts, white leg rings, U fangs, rear grin or plush. Trap 1 is absent only because the eyes are hidden; FIX 1 shows the eyes without a glint. |
| 6 | A/B pairs | PASS | Weaver vs Mantis: low and wide vs upright, plum vs jade. Weaver vs Kraken: straight jointed legs vs curls, plum-black vs red. |
| 7 | shares | PASS | three hairlines accepted (section 4); gold only on the crown + rift |
| 8 | face close | FAIL -> FIX 1 | Pupils at 70 %, no glint, crown seated, gem flush, chelicera gap 0.024, palps outside: all fine. But from the PORTRAIT direction the brow is a 0.055-deep visor over a 0.024-tall lens: only a sliver of orchid shows, and it also covers the crown's front bar. |
| 9 | rift close-up | FAIL -> FIX 2 | 14 segments, no candy stripes (the stair-steps suit the block style). Lips 0.09 wide with a GOLD_D edge; 3-prong settings. But it reads as a slit-pupil eye from the top (Q1). |
| 10 | legs | PASS | Right colours; one thorn per knee; spines 0.013; hips 0.136-0.140 apart; leg 1 about 0.08 from the turret. Claw tips at -0.005 accepted (inside the -0.02 ground rule). |
| 11 | hard rules | FAIL (minor) -> FIX 3 | No Neon; 11,852 tris; studs on the right roles; no B.poly; th 0.26; ARMOR lum 67; HEIGHT 8; RIG quad. But the wine hull pokes through the SILK band. |
| 12 | rig limits | PASS | All 6 poses at 0 hits, reproduced; also 0 on the fixed geometry, plus the new roar s35. |
| 13 | deliverables | PASS | complete |

Tri groups: abdomen 4.5 k (about 3.8 k budget) and face 1.4 k (0.9 k budget) run over. The legs and head run under,
and the total stays below 12 k. Accepted.

## 3. Deviations and Q1
- **W1 APPROVED.** N = 14 shows no stripes. The half-resolution GOLD_D strips are fine.
- **W2 APPROVED.** The E3 seat on the turret's tapered side is correct.
- **W3 OVERRULED IN PART.** The recolour and the 70 % pupil are right. The brow geometry is wrong at this scale: it was
  tuned for ThunderRex's head at sc 1.3, and at sc 0.9 on a 0.24-wide turret it buries the lens. The HOT spot goes:
  at a readable lens size it reads as a cartoon glint (cute trap 1; tested, see `c_face2.png` row 2). Replace it with
  FIX 1. The Studio EyeGlow VFX will carry the "burning".
- **W4 APPROVED.** The sign reading is right: fem + leans OUT, shin/foot + OPEN the knee about t, R mirrored. Palps
  pitch +5 replaces the brief's -15. A required addition for the front read is in section 6.
- **W5 APPROVED, except the band arc.** Gaps 0.04 and the thorn ORCHID at 0.022 stay. The band goes back to the
  brief's 205-335 deg inside FIX 3: the thicker 6-ring band keeps side SILK at 3.3.
- **W6 APPROVED** (inner spinnerets, circlet strips, the Rift anchor lifted 0.02, the SILK sternum).
- **Q1: yes, it reads as a cat's eye.** From the top: a closed gold almond, an orchid iris stepping evenly inward, and
  a straight central slit. With the pink layers and gold lips, the same top view is also a shape players will meme on.
  - **Keep the HOT seam** (it is the light), but make it a meandering CRACK with two short side fractures, and give
    the orchid body a torn, irregular edge (FIX 2). Eyes never branch.
  - **Keep the closed lip frame.** I tested opening the lip ends (lips t 0.07-0.93): it looks broken and unfinished.
  - **No regular zig-zag.** Tested: it reads as a lightning bolt, the Thunder pets' motif.
  - Verified: tq / game / top / rear now read as a cracked crystal of void-light in a gold setting, and the game-cam
    icon reads as a gold-framed cracked gem.

## 4. Hairline shares and gold
- **tq dark 70.2, tq SILK 0.9: accepted, and fixed anyway.** With FIX 1-3 they measure 69.9 and 1.2.
- **tq BLACK 5.2: accepted.** It is a counter artefact. Exact BLACK geometry is only 0.21 % of tq (0.25 % of front);
  the other 4.7 % is anti-aliased edges against the black flat-render background.
- **Final shares (FIX 1-3), side / tq / game / front:**

  | role | side | tq | game | front |
  |---|---|---|---|---|
  | dark | 64.1 | 69.9 | 71.8 | 67.3 |
  | VELVET | 21.8 | 12.1 | 9.0 | 14.5 |
  | SILK | 3.3 | 1.2 | 1.0 | 0.6 |
  | glow | 1.8 | 3.7 | 5.0 | 3.5 |
  | GOLD | 4.1 | 7.0 | 9.0 | 7.5 |

  Everything is in range except tq BLACK (artefact). Top role 43.8 %.
- **Gold: PASS.** The two counters differ:
  - the builder's: hue 0.08-0.16, s > .5, v > .45
  - the brief's (my `icons.py` from the mock round): hue 0.09-0.17, s > .45, v > .55

  | counter | v1 (portrait / game) | mock F | with FIX 1-3 |
  |---|---|---|---|
  | builder's | 44 / 68 | 49 / 62 | 45 / 67 |
  | brief's | 48 / 83 | 60 / 80 | 47 / 83 |

  The gate is the brief's counter: >= 45 / >= 60 passes. Report both numbers from now on. The 12 px the portrait gives
  away against the mock are mostly the crown's front bar hidden behind the brows (FIX 1 brings some back).

## 5. Fixes (exact code; ranked; all tested together on the temp copy)
Result with all three: 11,956 tris; H 1.10; bounds unchanged; idle f0 and all 7 limit poses `collision_free`.

### FIX 1 (must): the main eyes must read from the portrait camera (W3)
In `main_eye`, replace everything after `kw = dict(R=R, studs=[], role="detail")` with:
```python
    B.add(c, (0.052 * sc, 0.008, 0.028 * sc), BLACK, bone, bevel=0.004, **kw)                  # socket (was 0.025)
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0165 * sc), ORCHID, bone, bevel=0.003, **kw)     # lens (was 0.0135)
    B.add(c + n * 0.011 + R @ Vector((-s * 0.004, 0, 0)), (0.006 * sc, 0.004, 0.0115 * sc), BLACK, bone,
          bevel=0.002, **kw)                                                                  # slit pupil, 70 %
    Rb = Euler((0, math.radians(-s * 22), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, 0.040 * sc)) + n * 0.010, (0.074 * sc, 0.022, 0.026 * sc), ARMOR_D, bone, R=Rb,
          role="detail", bevel=0.010)                                                         # V-brow (was +0.036 / n 0.024 / 0.034 / 0.028)
```
- The HOT spot block is deleted.
- The brow now covers about 10 % of the lens from the front and about 30 % from the portrait camera.
- Verified: narrowed, lidded orchid reptile eyes; the V still meets at the midline; no glint; the crown's front bar
  is visible again.

### FIX 2 (must): the rift becomes a torn crack, not an eye (Q1)
Replace the 3-layer loop (`for col, wf, lift, cap in (...)` with its inner `for i in range(N)`) with the block below.
The lips, inner strips and settings stay as they are.
```python
    JAG = [0.55, 0.62, 0.72, 0.58, 0.66, 0.80, 0.62, 0.70, 0.82, 0.64, 0.56, 0.70, 0.60, 0.55]   # torn orchid edge
    ZZ = [0.0, 0.20, 0.42, 0.16, -0.28, -0.48, -0.20, 0.18, 0.46, 0.30, -0.06, -0.36, -0.22, 0.06, 0.0]  # crack path
    for i in range(N):
        t0, t1 = i / N, (i + 1) / N
        ua, ub = U0 + (U1 - U0) * t0, U0 + (U1 - U0) * t1
        nm = abd_nrm((ua + ub) / 2, 0)
        B.bar(abd_top(ua, 0, 0.010), abd_top(ub, 0, 0.010), nm, 2 * max(0.010, wt((t0 + t1) / 2)), 0.006, DEEP,
              "Abd", studs=[], nostud=True, role="detail", bevel=0.003)                      # void field (unchanged)
        B.bar(abd_top(ua, 0, 0.016), abd_top(ub, 0, 0.016), nm, 2 * max(0.010, JAG[i] * wt((t0 + t1) / 2)), 0.006,
              ORCHID, "Abd", studs=[], nostud=True, role="detail", bevel=0.003)              # glow body, torn edge
    pts = []
    for i in range(N + 1):                                    # HOT: a meandering crack (S + jitter), not a pupil
        t = i / N
        u = U0 + (U1 - U0) * t
        hw, _ = abd_interp(u)
        pts.append((abd_top(u, ZZ[i] * 0.45 * wt(t) / hw, 0.021), u))
    for (a, ua), (b, ub) in zip(pts, pts[1:]):
        d = (b - a).normalized()
        B.bar(a - d * 0.010, b + d * 0.010, abd_nrm((ua + ub) / 2, 0), 0.026, 0.004, HOT, "Abd", studs=[],
              nostud=True, role="detail", bevel=0.002)
    for i, side, du in ((5, -1, 0.05), (9, 1, -0.05)):       # 2 short side fractures (an eye never branches)
        a, ua = pts[i]
        ub = ua + du
        hw, _ = abd_interp(ub)
        b = abd_top(ub, (ZZ[i] * 0.45 + side * 0.42) * wt((ub - U0) / (U1 - U0)) / hw, 0.021)
        B.bar(a, b, abd_nrm((ua + ub) / 2, 0), 0.016, 0.004, HOT, "Abd", studs=[], nostud=True, role="detail",
              bevel=0.002)
```
- Cost: +24 tris (the two fractures).
- Glow shares are unchanged (tq 3.7, game 5.0). Gold is unchanged.
- Do NOT use a regular +-alternating zig-zag (Thunder bolt) and do NOT open the lip ends (both tested).

### FIX 3 (must, small): belly band poke-through
- Give `shell()` a ring count: signature `def shell(u0, u1, a0, a1, color, off=0.022, thick=0.03, seg=10, nr=4):`,
  loop `for i in range(nr):` with `u = u0 + (u1 - u0) * i / (nr - 1.0)`.
- The band call becomes: `shell(0.14, 0.64, 205, 335, SILK, off=0.014, thick=0.02, seg=12, nr=6)`.
- Cost: +104 tris.
- Effects: the red diamond is gone (`c_belly.png`), the game-view flank sliver gets thinner, and side SILK 3.3,
  tq SILK 1.2, game VELVET 9.0 all land in range.
- The plates (off 0.022) were checked: no poke-through.

### Optional (no gate)
- From the game cam, the wine rear tip and the two SILK-tipped spinnerets read faintly as a little mouth with fangs.
  If the owner notices it, make the big spinneret tips SILK_D (172, 160, 186). Otherwise leave it: the silk VFX comes
  from there.

## 6. For the CLIP phase (brief section 6), from this round
1. **Roar FK (W4):**
   - `leg_raise(i, side, fem, shin, foot)` = `cm.key_axis(t, +fem)` for the femur, `(t, -shin)` for the shin,
     `(t, -foot)` for the foot.
   - t = (-sin a, cos a, 0) on L, mirrored on R.
   - Keep the brief's (15, 80, 20) / (5, 40, 10). Palps: **spread 28, pitch +5** (not -15: the palp roots cut the
     leg-1 femurs).
2. **Roar front read (NEW, required):**
   - **Problem:** raised in their own -54 deg plane, legs 1 end at x +-0.98, a flat sideways "T" from the front. That
     is the Kappa arms-wide read section 1.2 bans.
   - **Fix:** add a forward yaw to the SHIN only. Pass `extra=Quaternion((0, 0, 1), math.radians(-35 * k))` on
     Shin1_L (+35 on R) in `key_axis`, with k = the shin's current opening / 80 so it eases in with the raise. At the
     peak this equals `k.key` Shin1_L (-52.82, -75.56, -73.3).
   - **Tested** (pose `s35`): 0 tri pairs with all section 5.5 pairs + 5.6 capsules (on v1 and on the fixed geometry).
     The ankles move to (+-0.48, -1.59, 1.31) and the front view becomes a raised "V" framing the crowned face
     (`c_roar3.png`).
   - **Raise the leg-1 raised-ankle limit to 1.32**, or open the shin 76 instead of 80 if 1.25 must hold.
   - **Do NOT yaw the femur:** Leg1 yaw -15 / -25 gives 17-28 Leg1|Palp tri pairs, because the femur sweeps the palp
     femur at rest (0.12-0.21, -0.68..-0.52, 0.29-0.42). Leaning it out further is worse (39-43).
   - **Optional:** Leg2 shin yaw -15 brings legs 2 slightly forward too (0 hits).
3. From the side the raised legs 1 still read as forward "lances". Check the side pose at f22 together with the front;
   the front "V" is the priority.
4. Keep the tested rules as written: the LEG-1 rule, the ABDOMEN LEVEL rule (Pedicel +6 / Abd +8 in the roar), the
   RIFT FACING rule (rear-down presents). L3 PRESENT with L4 at (1.02, 0.70, 0.45) and L4 CAST stay at 0 on the fixed
   geometry.
5. VFX note for section 7: the mesh eyes no longer carry a HOT spot. The EyeGlow anchor's 8-eye glow and the `flare`
   flash provide the burning look. The Rift glow should follow the crack (the anchor at u 0.47 is unchanged).
6. Report gold with the brief's counter (hue 0.09-0.17, s > .45, v > .55), and BLACK shares excluding
   background-adjacent pixels.

## Summary
**APPROVED WITH FIXES, 7.5/10 (about 8.5 after the fixes).** It's a fierce, unmistakable spider-queen. It beats every
Void sibling at 64 px and holds its own next to Rex / Orca / Leviathan / Hammerjaw / Basilisk / Thunderbird.

Must-do before the clips (exact code above, all tested together: 11,956 tris, every limit pose at 0):
- **FIX 1:** smaller, higher brow; taller lens; no HOT spot. The main eyes must show from the portrait camera.
- **FIX 2:** the rift's HOT line becomes a meandering crack with 2 fractures and a torn orchid edge. It kills the
  cat's-eye and anatomical reads; the lip frame stays closed.
- **FIX 3:** 6-ring band at 0.014, arc 205-335. Fixes the hull poke-through and the remaining share hairlines.

Clip phase:
- W4 is approved (palps +5).
- Add a Shin1 forward yaw of 35 deg to the roar so legs 1 read as a raised "V", not the banned sideways "T". Never yaw
  the femur.
- Raise the leg-1 raised-ankle limit to 1.32.
