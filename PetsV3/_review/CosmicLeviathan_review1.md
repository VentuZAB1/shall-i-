# Cosmic Leviathan - review 1 (v1 MODEL GATE, 2026-10-14) - NOT APPROVED YET: v2 with M1-M8, all pre-tested

**Verdict: 6 / 10. A strong base, but 6 of the 13 checklist items fail.** Every fix below was built and measured
on a patched copy of your file. The full must-fix package is collision-free at all 7 limit poses. Expect v2 to pass
in one round.

**What is already secret-grade:**
- The Comet Crown: 55 gold px at 64 px, the biggest gold mass in the strip.
- The palette, executed exactly. It is the only magenta pet in the game.
- The swallowtail fluke: clean V, no knob.
- The segmented hull: no creases, slivers or ring folds.
- The rig: clean at rest and at every limit.

**What fails:**
- The dorsals read as **crayons** (dark stub + plum ring + blue cone).
- The wing-fin is a **dark plank + a bundle of 3 finger strips**, not a closed fan. The plum is hidden.
- The 3 nasal plates stand up as **battlements**. This is a bug.
- From the front, the nostril slits on the rostral shield read as **a second pair of angry eyes**, while the real eyes
  hide under the crown corners.
- The front is still an **egg with a cream bib**.
- The 64 px icon is the **smallest silhouette** in the strip, and its fins read as blue spikes.

**What I looked at:**
- `_model_sheet_600` and all 5 model views (zoomed 2-3x)
- `_face_close` and the 3 `close_*` renders
- `_icons_strip_64/128` and `_AB_64/128`
- `_flat_sheet`, `_shares`, `_limits_sheet` / `_limits.txt`, `_model_info.txt`
- the model sheets, icons and face sheets of BlackDragon, CelestialDragon, ThunderRex and AbyssalOrca
- `pets/CosmicLeviathan.py` lines 1-492 (the model). I ignored the new clip section below it.
- `curveloft.py` (band / at / surf) and `blockkit.py` (frame_from, build, HEAD_XF)
- `pose_try.py` and `icon3.py`

**How I tested:**
- A driver ran patched copies of your file with `petkit.ROOT` redirected to `%TEMP%\lev_rev\`. Nothing was written to
  the project except this file.
- The baseline copy reproduced your tris (12,876), H, pitch, lowest point and **every flat share to 0.1**.
- A `pose_try` clone with your 4 limits reproduced your **0 collisions** on the original. I used Head+Neck up as both
  Neck −12 / Head −18 and Head −30, and the fins through your `axis_euler` hinge (+28 = (−9.217, ∓9.006, ∓25.652),
  −20 = (8.506, ±3.574, ±17.501)).

**Evidence images** (all in `C:\Users\ventu\AppData\Local\Temp\lev_rev\`):

| file | shows |
|---|---|
| `REVIEW_v1_vs_Mpackage.png` | top row = your v1, bottom = the M package; side / tq / front / game |
| `REVIEW_Mpackage_face_fin.png` | the M-package face (front / side / tq) and the closed fan from above |
| `REVIEW_icons_64.png`, `REVIEW_icons_128.png` | v1 icon, M-package icon, then the 8 comparison pets |
| `fin_fluke_top.png` | v1 fin from above (plank + slot + fingers) and the fluke notch |
| `crown_check.png` | crown seating, low angles |
| `v1_side_dorsal.png` | the crayon dorsals, even after thinning |
| `v11_sheet.png` | the rear (S1) test |
| `v16_sheet.png` | the slim chest (S2) test |

- The patch set is `mkvar.py` (each patch is an exact text replacement on your file).
- `v14.py` is the full must-fix package as a runnable file. Copy what you need.

---------------------------------------------------------------------------------------------------------------------
## 1. §9 checklist (v1 as delivered)

| # | item | grade | evidence |
|---|---|---|---|
| 1 | S-silhouette | **PASS** | `model_side`: ∩ neck/head → ∪ trough → flattening tail; no banana. H 1.695 (1.70 ± 0.03 ✓), lowest 0.126 ✓, L:H 3.03/1.695 = 1.79 ✓, skull hw 0.21 vs N0 0.19 ✓. Note: the "?" is shallow, because the jaw bottom (~0.96) sits level with the chest top (0.98), so there is almost no visible neck. See S1. |
| 2 | Front view | **FAIL** | Fins to ±1.05 ✓, cheek fins ±0.40 ✓, BELLY 15.2 + BELLY_D 5.3 = 20.5 ≤ 22 ✓. But the cream oval is 63 % of the body width, fills the whole lower half and has a round egg outline, and the BELLY_D bars are too low-contrast to break it. It reads as a **penguin bib on an egg** (`front_zoom`). Fix M6. |
| 3 | Game camera | **FAIL** | ✓ the gold ring + blade; ✓ segmented plates with plum gaps; ✓ the fluke gradient. ✗ The wing-fins read as a dark ARMOR plank with 3 azure "icicle" fingers below it, and the plum field is a thin wedge hidden under the spar (`game_zoom`). ✗ The dorsals read as small blue crystal cones. Fixes M4 + M5. |
| 4 | 64 px icon | **FAIL** | ✓ crowned sea-serpent (it reads as a "crowned purple serpent-fish"); ✓ gold crown + blade, **55 gold px** (≥ 25). ✗ Periwinkle fins: at 64 px they are blue spikes along the back, and the near wing-fin is a dark sliver. ✗ Most striking of the Celestial row: frame fill **26 %**, the lowest of all 9 (SolarLion 40, Griffin 33, CelestialDragon 32, Cvetibara 43, Rex 43, Orca 30, Mantis 27, BlackDragon 28); bbox aspect 1.59, the widest. |
| 5 | BlackDragon / CelestialDragon A/B | **PASS** | `_AB_64`: a rearing finned serpent vs a low legged wave; bright magenta + ivory vs dark indigo-violet; azure fins vs violet crystals. Nothing like the CelestialDragon (blue legs, wings, white dots). |
| 6 | Shares | **PASS-WITH-DEVIATION** | Misses of 0.8-2.0 (your table). The M package changes them; the final ruling is in §3. GOLD exists only on the crown ✓. No role is above 45 % ✓. |
| 7 | Face close | **FAIL** | ✓ Lids form a scowl in side/tq; no glint; the underbite chin is 0.04 ahead; 2 tusks outside the lip; teeth ≥ 0.024 full width and offset; dark roof and floor. ✗ The **3 nasal plates stand 0.057 proud as square crests** (battlements in side/tq). ✗ From the front, the "\ /" nostril slits on the dark shield read as **angry eyes on a second face**. ✗ The real eyes hide under the crown's corner blocks from the front (yaw 25° = side-facing). |
| 8 | Fins | **FAIL** | ✓ no B.poly; ✓ tapered and bevelled; ✓ studded HIDE, smooth light colours; ✓ swallowtail with a clean V and no knob (`fin_fluke_top` right). ✗ **The fan is not closed:** from above (`fin_fluke_top` left) there is an open slot between the spar and P2 from ~40 % out, and P2-P4 are 3 near-parallel strips of almost equal length (0.80/0.72/0.62), so it reads as a rake. |
| 9 | Hull | **PASS** | n 2.6 ✓; studs visible on ARMOR/HIDE/BELLY at pitch 0.038 ✓; no crease, sliver or fold (side zoom) ✓; per-bone bands + mid-Chest/mid-Spine breaks ✓. SEG 20 instead of 24: accepted (tris). |
| 10 | Remix sweep | **FAIL** | ✗ Crayon dorsals with azure cones, plus the wing-fin fingers poking above the back in the side view, read as **Rex crystal shards**. ✗ The separate 0.026 AZURE trailing-edge bar reads as a detached glowing stick (Rex seam). Clean: no dots, crescents, violet, core gem, rings, beads, veins or sail; no gold outside the crown. |
| 11 | Hard rules | **PASS-WITH-DEVIATION** | No Neon ✓; tris 12,876, over the 12 k target but under the 15 k cap (accepted); crown seated with no gaps at low angles (`crown_check`) ✓; HIDE max channel 170 ✓; ARMOR lum 65.9 ✓; HEIGHT 10 to the horn tip ✓. Nasal crests are covered by M1. The nostril slits are 0.010 tall, under the 0.02 detail rule; covered by M2. |
| 12 | Rig at rest and the limits | **PASS** | Reproduced independently: 0 pairs at rest, Head+Neck +30 (both splits), yaw 22 + 8, flap +28 / −20, fluke-up; fluke root z 1.483 ≥ 1.35 ✓; all §7.5 anchors exist ✓. |
| 13 | Deliverables | **PASS** | All present. |

---------------------------------------------------------------------------------------------------------------------
## 2. Rulings on your deviations

**1. Wing-fins**

| change | ruling | reason / fix |
|---|---|---|
| Azimuths 32/44/55/66 | **APPROVED** as 32/43/54/65 | Fine-tuned in M5. |
| Lengths 0.86/0.80/0.72/0.62 | **REJECTED** → 0.86/0.80/0.70/0.58 | Near-equal lengths made a rake of fingers. A graded trailing edge is the fan read. |
| Dihedral 17/16/15/14 | **APPROVED**, against my own plan | Tested at 10/9/8/7: tq AZURE went 9.6 → 9.3 and nothing visible improved. Your dihedral also keeps the tips at z ≥ 0.6. |
| Splits HIDE 0-36 / DEEP 36-42 / AZURE 42-100 | **REJECTED** → HIDE 0-46 / DEEP 46-52 / AZURE 52-100 | With the knuckle, 0-36 % is a narrow wedge under the spar, so the plum never shows. M5 puts the lost azure back on the spar tip, so the tq AZURE family is unchanged (10.0). |
| Hub on the skin | **APPROVED** | |
| Root knuckle `panel(root=)` | **APPROVED** | Necessary. The wider M5 chords stay clean at +28 / −20. |
| Flap hinge on the P4 line (`fin_rot` / `axis_euler`) | **APPROVED** | Good engineering. Update `FIN_AXIS` to P4's new azimuth (65°, e 14°). |
| FinTip pivot (0.60, −0.25, 0.67) | **APPROVED** | Unchanged by M5: P1 keeps az 32, e 17, length 0.86. |
| Second hub capsule | **APPROVED** | |

**2. Dorsal tips moved back (sweep 45°): REJECTED.**
- On the 35-40° down-sloping chest, a world-space sweep turns into "upright" against the skin.
- Thickness 0.08 against a 0.06 tip chord makes cones.
- The horizontal colour rings complete the crayon.
- Thinning alone did not fix it (`v1_side_dorsal.png`). Rebuild per M4.

**3. Saddle**
- Gaps 0.06: **APPROVED.** Tested 0.045: game ARMOR rose to 44.2.
- Neck/Chest/Spine wrap to −0.15: **APPROVED.**
- Midline split: **APPROVED.** It is a checker from the game camera, but it carries the dorsals and holds game ARMOR
  ≤ 42. Do not widen it.
- Add the Tail1/Tail2 wrap (M7).

**4. Skull**
- Helmet down the cheeks, the nasal bridge and the rostral shield: **APPROVED.** The plain dark shield kills the pig
  snout.
- Nostril slits on the shield: **REJECTED** (second face). Use M2.
- Brow-lids instead of brow bars: **APPROVED.** The scowl reads in side/tq, and the Mantis goggles lesson applies.
- The eye position also has to change (M3).
- The nasal plates are a **bug**: `frame_from`'s local x is the surface normal, so the size (hw, 0.008, 0.032) stood
  each plate hw = 0.045 tall. Fix M1.

**5. Belly keel strips (Neck −0.80, Chest −0.88): APPROVED.** Add the plum scute gaps and lift the Spine/Tail belly
(M6).

**6. Gold trims: APPROVED.** tq GOLD 6.9 is accepted because the crown is the hero and the only gold. Do not trim
further.

**7. Throat-junction capsule: APPROVED, with proof required.** It masks real crossings, so in the clip round add one
close render of the throat at yaw 22 + 8 and at head-up 30, seen from below-side, showing no visible poke-through
(S5).

**8. Rest span 2.09 and fin tips at z ≥ 0.6: APPROVED.**

---------------------------------------------------------------------------------------------------------------------
## 3. Share misses: rulings

The M package (`v14.py`), measured with your own flat-ID method:

| view | ARMOR | HIDE | BELLY (+D) | AZURE fam | GOLD |
|---|---|---|---|---|---|
| side | 37.9 ✓ | **33.0** (+1.0) | 8.5 (+3.1) ✓ | 8.6 ✓ | 2.8 ✓ |
| tq | 34.1 ✓ | 30.3 ✓ | 7.0 (+3.2) ✓ | **10.0** (−2.0) | **6.9** (+0.9) |
| game | 41.2 ✓ (was 43.6) | **28.5** (+0.5) | 1.1 ✓ | 18.5 ✓ | 3.0 ✓ |
| front | 23.1 | 28.1 | 12.9 + 3.7 = 16.6 ✓ (was 20.5) | 14.4 | 7.9 |

**Rulings:**
- **Game ARMOR:** fixed by M5's lit spar tip (43.6 → 41.2).
- **HIDE side / game:** accepted with a ±1.5 tolerance. The plum on the fan is the gradient we want.
- **tq AZURE 10.0:** **accepted at ≥ 9.5.** It is structural. At the 20° tq camera the near fan is nearly edge-on, and
  every variant I built (dihedral 10-17, wider light fields, a higher camera) landed at 9.3-10.5. The game camera,
  where the pet lives, carries 18.5.
- **tq GOLD 6.9:** accepted up to 7.5 (crown = hero).

---------------------------------------------------------------------------------------------------------------------
## 4. MUST-FIX (v2). All are in `v14.py`; pivots and bones are unchanged; 0 pairs at the 7 limit poses

**M1 - Nasal plates flush** (bug):
- Change `B.add(p + nn * 0.012, (hw, 0.008, 0.032), ARMOR, ...)` to `B.add(p + nn * 0.004, (0.008, hw, 0.032), ARMOR, ...)`.
- Result: 0.012 proud, as the plan said.

**M2 - Nostrils off the shield, onto the snout sides.**
- Replace the 2 slits with
  `B.add((s_*0.099, -1.285, 1.142), (0.004, 0.014, 0.010), BLACK, "Head", studs=[], role="detail", R=Matrix.Rotation(math.radians(-s_*12), 3, "Z"), bevel=0.002)`.
- Keep the rostral shield plain.
- Result: no second face from the front, the nostrils read in profile, and the detail is ≥ 0.02.

**M3 - Eyes forward and down, clear of the crown.**
- Set `c0 = (s_*0.150, -1.035, 1.265)` and `n0 = (s_*cos42°, -sin42°, 0.20).normalized()`.
- The lids are unchanged.
- Result: the slit top is ≤ 1.31, under the crown bar bottom (1.335), and both eyes and lids read from the front
  (`REVIEW_Mpackage_face_fin.png`).

**M4 - Dorsals: falcate "spar + web" fins**, the same language as the wing-fan.
- Roots, tip height and back offset:
  - Dorsal1 (−0.50, −0.16), h 0.32, back 0.03
  - Dorsal2 (−0.07, 0.23), h 0.34, back 0.03
  - Dorsal3 (0.44, 0.66), h 0.25, back 0.03
- The tip is measured on the local axis between the skin normal and vertical, so the sweep is relative to the skin.
- Drop the separate AZURE trailing-edge bar.
- Resulting tips: D1 (0, 0.128, 1.016), D2 (0, 0.280, 0.911), D3 (0, 0.591, 0.843).
- No new pairs: Head|Dorsal1 and Fluke|Dorsal3 stay clean at the limits.

```python
for nm, (yf, yb), tip in (("Dorsal1", (-0.50, -0.16), (0.32, 0.03)),
                          ("Dorsal2", (-0.07, 0.23), (0.34, 0.03)),
                          ("Dorsal3", (0.44, 0.66), (0.25, 0.03))):
    Rf = Lf.surf(sy(yf), math.pi / 2) - Vector((0, 0, 0.03))
    Rb = Lf.surf(sy(yb), math.pi / 2) - Vector((0, 0, 0.03))
    _c, _T, _N, _w, _h = Lf.at(sy((yf + yb) / 2))
    U = (_N + Vector((0, 0, 1))).normalized()              # between skin normal and vertical
    Bk = (_T - U * _T.dot(U)).normalized()                 # backward, along the skin
    T = (Rf + Rb) / 2 + U * tip[0] + Bk * ((Rb - Rf).length / 2 + tip[1])   # tip trails the rear root
    def FE(h): return Rf.lerp(T, h) + (U * 0.035 - Bk * 0.015) * math.sin(math.pi * h)   # convex leading edge
    def BE(h): return Rb.lerp(T, h) - Bk * 0.035 * math.sin(math.pi * h)                  # CONCAVE trailing edge
    def PP(h, f): return FE(h).lerp(BE(h), f)
    for c, h0_, h1_, f0, f1, th0, th1 in ((ARMOR, 0.0, 0.36, 0.0, 0.40, 0.026, 0.021),      # dark leading spar
                                         (ARMOR, 0.36, 0.70, 0.0, 0.40, 0.021, 0.017),
                                         (ARMOR, 0.70, 0.95, 0.0, 0.40, 0.017, 0.013),
                                         (HIDE, 0.0, 0.32, 0.40, 1.0, 0.018, 0.015),        # plum web (studded)
                                         (DEEP, 0.32, 0.38, 0.40, 1.0, 0.015, 0.014),
                                         (AZURE, 0.38, 0.95, 0.40, 1.0, 0.014, 0.010)):     # lit trailing web
        fm = (f0 + f1) / 2
        m0, m1 = PP(h0_, fm), PP(h1_, fm)
        w0 = max(0.010, (PP(h0_, f1) - PP(h0_, f0)).length / 2)
        w1 = max(0.006, (PP(h1_, f1) - PP(h1_, f0)).length / 2)
        side = (PP(h0_, f1) - PP(h0_, f0)).normalized()
        kw = dict(studs=[], nostud=True, role="limb") if c in (DEEP, AZURE) else {}
        B.seg(m0 - (m1 - m0).normalized() * 0.008, m1 + (m1 - m0).normalized() * 0.006, w0, th0, c, nm,
              side=side, top=(w1 / w0, th1 / th0), **kw)
    # keep your STAR tip spike + ANCH[nm + "Tip"]
```

**M5 - Close the wing-fan, show the plum, light the spar tip.**
- Panels `(az, e, len, hc, off)`: (32, 17, 0.86, **0.07**, 0.008), (**43**, 16, 0.80, **0.15**, 0.004),
  (**54**, 15, **0.70**, **0.15**, 0.0), (**65**, 14, **0.58**, **0.13**, −0.004).
- P2-P4: `top_w=0.45` and splits **[0.46, 0.52]** (HIDE / DEEP / AZURE).
- P1 spar: colours `[ARMOR, ARMOR, DEEP, AZURE]`, bones `[Fin, FinTip, FinTip, FinTip]`, splits `[0.45, 0.62, 0.68]`.
- `FIN_AXIS` → az 65, e 14.
- Result: from above, a closed fan for ~80 % with 4 scalloped star points (`REVIEW_Mpackage_face_fin.png`, right), and
  plum → deep → azure → star from the game camera.
- Flaps +28 / −20 stay clean.

**M6 - Belly scutes.**
- Neck + Chest scute bars become **HIDE, ±0.017** (0.034 wide) instead of BELLY_D ±0.01.
- Spine/Tail1/Tail2 belly default `zhi −0.50 → −0.40`, with the bars following.
- Result: the front reads as a ladder of ivory ventral plates instead of a bib (front 20.5 → 16.6), and side BELLY is
  8.5.

**M7 - Tail1 / Tail2 saddle plates `zlo 0.12 → −0.05`.**
- This keeps side HIDE at 33.0 after M4/M5; without it, it is 35.7.

**M8 - Re-render all of §9.13 and re-run the 4 limits with `pose_try`.**
- Render the model views last.
- Add one top view of the fin (`top=0.15,0.25,1`) and the 128 px icon strip.

---------------------------------------------------------------------------------------------------------------------
## 5. SHOULD (S): decide BEFORE the clips; S1 and S2 move geometry under the rig

**S1 - Rear the "?" neck.** This is the plan's "massive crowned head at the top", and the owner's 2026-10-08 note
that heads are too small.
- `HEAD_XF = [((0, -0.80, 1.04), 1.0, ("Head", "Jaw", "Crown", "Horn", "Mouth", "Eye_L", "Eye_R"), (0, -0.02, 0.12))]`,
  using the kit's own facility, which moves the blocks and those joints.
- Stations: N0 (−0.88, 1.24), N1 (−0.78, 1.10), N2 (−0.65, 0.90). `NECKP` (0, −0.65, 0.90).
- `joints()`: shift the jaw-hinge and throat capsules by (0, −0.02, +0.12).
- Tested (`v11_sheet.png`):
  - The side view now reads as a rearing serpent and the front as a cobra column.
  - H 1.815, pitch 0.0407, shares unchanged, icon aspect 1.59 → 1.51.
- **Cost:** Jaw|Neck reaches 62-265 pairs at head-up and yaw. The steeper neck tilts the loft's front ring under the
  jaw, reaching y −1.0. Pulling N0 back to −0.83 did not cure it (96-246). It needs a neck-start solution, for example
  starting the loft at N1 with a collar cap.
- Worth it for the secret, but only if you solve it now. Otherwise skip it; v1's S passes.

**S2 - Slimmer chest.**
- Station C (−0.46, 0.66, **0.28, 0.29**) and M (−0.12, 0.43, **0.245, 0.25**).
- Result: less pot-belly in the tq/icon and a narrower front column (`v16_sheet.png`). Shares stay in range.
- **Cost:** Fin_L/R|Spine 6-8 pairs at flap −20 (the hub reseats inward). Fix by moving the hub 0.01 out or extending
  the knuckle capsule.

**S3 - Mandible plates:** they read as bolted rails in the side close. Seat them at `tab(JAWT, y)[1] + 0.002`,
thickness 0.004, with their bottom edge on the jaw's lower lip line.

**S4 - Eye STAR hot spot:** 0.013 × 0.006 → 0.009 × 0.005, so it is not a glint at close range.

**S5 - Throat proof render** (see ruling 7).

**Accepted without change:** 4 upper teeth + 3 lower fangs per side (plan: 6 + 4), cheek-fin ARMOR 0-38 %, and
tris ≤ 13 k.

---------------------------------------------------------------------------------------------------------------------
## 6. Your specific questions
- **Face:** v1 is not cute, but from the front it is a dark box with a second face, because the eyes sit under the
  crown. After M1-M3 it is a scowling armoured wedge with visible azure slits, tusks and an underbite.
- **Front:** v1 is a bowling pin with a bib. M6 turns it into a plated serpent column; S2 / S1 make it lean.
- **Game view:** in v1 the fan reads dark → azure fingers. After M5 it reads plum → deep → azure → star.
- **64 px:** I can name "crowned serpent" and "gold crown + blade" in v1, but not the periwinkle fins. After the M
  package the fins read as blue-lit fans at 128 px and as blue-tipped fins at 64 px.
  - Frame fill is structural for a long serpent: 26 %, in the BlackDragon (28) and Mantis (27) band.
  - At v2 I will grade item 4 on the 3 names and the hero, not on fill.
  - It already wins the row on colour and hero.

---------------------------------------------------------------------------------------------------------------------
## 7. GO / NO-GO for the clips (§7)

**NO-GO for final clips until v2 passes this gate.**
- You may keep drafting clip code. M1-M8 do not move a single pivot or bone:
  - the FinTip pivot stays on the spar at 45 %
  - the Dorsal joints are unchanged
  - `FIN_AXIS` moves 1°
- Do not render the act / roar sheets for review on v1 geometry.
- **If you take S1 or S2, do it before keying,** because they move the Head/Jaw/Neck pivots and the fin hub.
- v2 deliverables: §9.13 + the fin top view + the 128 px strip + the limits table. Re-grade items 2, 3, 4, 7, 8 and 10.
