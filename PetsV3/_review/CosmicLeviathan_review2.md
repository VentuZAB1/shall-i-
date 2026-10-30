# Cosmic Leviathan - review 2 (v2 MODEL gate + CLIPS round 1, 2026-10-14)

## Verdict
**MODEL: APPROVED, 8 / 10.** All 13 §9 items pass (3 with an accepted deviation).

**CLIPS: idle and roar APPROVED; swim and act_sounding need one fix each.**
- The 3 fixes (C1-C3) are exact code lines.
- I applied all three to a temp copy and ran the full `headless_clips` gate: **collision_free true, linear 0, both
  loops closed, ground minimums unchanged or better.**
- **Apply C1-C3 verbatim, re-run `headless_clips`, and go to export. No review 3 is needed** unless you change anything
  beyond C1-C3.

**What I checked:**
- your §9.13 set, `_throat_proof`, `_act_sounding_v2`, `_clips_v2`, the clip code (lines 503-727)
- a diff of lines 1-499 against my `v14.py`: identical apart from S2 / S3 / S4, the hub +0.01 and `FIN_AXIS` 65°
- my own clip renders of the frames your sheets skip (swim extremes f0 / f16; act f40-f80; idle f32-f52; roar f12-f40)
- per-frame bone samples
- a re-run of the whole clip gate with `petkit.ROOT` redirected to temp. It reproduced yours exactly: collision_free,
  idle 0.107 @106, swim 0.130 @17, roar 0.100 @12, act 0.114 @66 Jaw.

Nothing was written to the project except this file. The evidence is in `C:\Users\ventu\AppData\Local\Temp\lev_rev2\`:
- `chk_*.png` (my v2 frames)
- `fl_cmp.png` (4 fluke-up curls)
- `fixed_clips.png` (C2 + C3 applied)
- `lev_clipfix.py` (your file with C1-C3)

---------------------------------------------------------------------------------------------------------------------
## 1. MODEL gate: §9 re-grade (v2)

| # | item | grade | evidence |
|---|---|---|---|
| 1 | S-silhouette | PASS | Unchanged S; lowest 0.137 (0.12-0.16 ✓); H 1.695; L:H 1.79. S1 not taken: accepted. |
| 2 | Front | **PASS** | `model_front`: a plated serpent column. 4 plum-gapped ivory scutes, no bib. Fins to ±1.04, cheek fins ±0.40. BELLY 12.2 + 4.2 = 16.4 ≤ 22. The slimmer chest (S2) narrows the egg. |
| 3 | Game camera | **PASS** | `model_game`: both fans read plum → deep → azure → 4 star points. Gold ring + blade. Segmented plates with plum gaps. The dorsals read as small swept fins, not cones. |
| 4 | 64 px icon | **PASS-WITH-DEVIATION** | I can name: crowned sea-serpent ✓; gold crown + blade, **51 gold px** ✓; blue-lit fins ✓ (the near fan shows plum → azure even at 64 px). Frame fill is 24.9 %, accepted as structural for a long serpent (ruled in review 1). It wins the Celestial row on colour and hero. |
| 5 | A/B | PASS | `_AB_64/128`: clearly not the BlackDragon (low, legged, indigo, violet crystals, pearl) and not the CelestialDragon. |
| 6 | Shares | **PASS** | See the table below. |
| 7 | Face | **PASS** | `_face_close`: nasal plates flush; nostrils on the snout sides; the plain obsidian shield ends the second face; both azure slits + V-lids read from the front; tusks outside the lip; dark roof and floor; smaller hot spot (no glint). |
| 8 | Fins | **PASS** | `model_top`: closed fan with 4 clean points; swallowtail clean; no z-fighting seen. |
| 9 | Hull | PASS | No creases, slivers or folds after S2. |
| 10 | Remix sweep | **PASS** | No crayons, crystal cones or detached seams. Gold only on the crown. |
| 11 | Hard rules | PASS-WITH-DEVIATION | Tris 12,856 (target 12 k, cap 15 k; accepted). Everything else ✓. |
| 12 | Rig at rest + limits | PASS | Your pose_try: 0 pairs at rest and at all 4 limits, fluke root 1.483. My review-1 reconstruction gives the same. |
| 13 | Deliverables | PASS | Complete. The **S5 throat proof is clean**: no poke-through at idle f32 / f52 or roar f27, in side, front and tq. |

**Shares (v2):**

| view | ARMOR | HIDE | BELLY (+D) | AZURE fam | GOLD |
|---|---|---|---|---|---|
| side | 38.3 ✓ | 32.4 (+0.4, within ±1.5) | 8.3 ✓ | 8.7 ✓ | 2.8 ✓ |
| tq | 33.8 ✓ | 29.5 ✓ | 6.5 ✓ | 11.2 (≥ 9.5 accepted) | 7.2 (≤ 7.5 accepted) |
| game | 41.0 ✓ | 27.8 ✓ | 1.0 ✓ | 19.1 ✓ | 3.0 ✓ |
| front | 22.6 | 26.3 | 12.2 + 4.2 ✓ | 16.6 | 8.1 |

Max role 41.0 ✓.

**Why 8 and not higher:**
- The icon silhouette is still a long low "crowned serpent-fish" (fill 24.9 %, the smallest in the strip).
- The "?" neck is shallow because S1 was skipped.
- From the side at rest, the far fan's 4 azure points peek over the back just behind Dorsal1.

None of these blocks the gate.

**Optional polish, only if you ever reopen the model:** S1 with a neck-start fix (see review 1). Do not touch the fan
now: `FIN_AXIS` and the clips depend on it.

---------------------------------------------------------------------------------------------------------------------
## 2. Deviation rulings (clips)

**No sweep-back, played as a down-fold instead: APPROVED.**
- It is geometry, not a choice. The closed fan I asked for (M5) puts P4 along the flank, so any yaw-back sweeps it
  through the body. Your 8° = 106-119 pairs is consistent with the hinge layout.
- The down-fold reads correctly:
  - roar gather (Fin −12 / FinTip −8): the fins brace under the body
  - plunge (Fin −10 / FinTip −10): the fins pressed along the flanks, streamlined (`chk_act`)
- The roar snap keeps the forward sweep (back −10): good.

**Swim stroke +26 / −18 (up-biased): APPROVED.** It respects the −20 limit and matches ref 8 (the banshee's high-V
upstroke).

---------------------------------------------------------------------------------------------------------------------
## 3. Clips

### idle "SKY DRIFT" (120 loop): APPROVED, with C1
✓ heave ±0.03 ×2; ✓ fins breathe ±8 with FinTip 4 f late; ✓ tail micro-wave; ✓ crown-glint beat + `glow` f78; ✓ fluke
flick with overshoot; ✓ no belly roll; ✓ loop closed.

**C1 - the look-back is a 4-frame snap.**
- Your keys run (36, +1) → (40, 0) → (48, −1). That swings Head + Neck through 24° in f36-40: 6°/f on average and
  about 9°/f at the smoothstep peak.
- That breaks the plan's "never faster than ~40° per 8 f" and reads as a twitch (`chk_idle`, f36 → f40).
- One continuous turn:

```python
look = [(0, 0), (20, 0), (30, 1), (38, 1), (50, -1), (58, -1), (66, 0), (120, 0)]
```

- Result: 48° over 12 f (4°/f average), ending at f66, still before the glint beat at f70.

### swim "MANTA FLIGHT" (36 loop): FIX C2 (one line)
✓ downstroke 45 %; ✓ Fin +26 / −18 with FinTip ±16 lagging 4 f; ✓ body wave ±2 / 4 / 7 / 10 / 14 with 0.08 lag;
✓ fluke ±10; ✓ head stabilised (Spine + Neck + Head pitch sums to 0); ✓ dorsals rigid; ✓ loop closed.

**C2 - the heave is in the wrong phase (bug).**
- `z = 0.02 − 0.02·cos(2π(ph − 0.5))` peaks at ph 0, the **top of the upstroke**.
- Sampled: Spine z is 0.4615 at f0 (fin end z 1.113, the highest) and 0.4215 at f16 (fin end 0.617, the lowest), so
  the body rises and falls WITH the fins. It reads as the fins hanging off a bobbing body: no lift.
- The plan (and the Orca, `0.0075 − 0.0275·cos 2πph`) peaks at the end of the downstroke. Change to:

```python
body(k, f, z=0.02 - 0.02 * math.cos(2 * math.pi * (ph - 0.05)), spine=sp, chest=0.0, neck=-0.4 * sp,
     head=-0.6 * sp, jaw=JAW_OPEN)
```

- Result: the body peaks at ph 0.55 (just after the bottom, ≈ f18) and is lowest just after the top (≈ f2).
- Tested: collision-free, loop closed, ground min 0.143 @2 (was 0.130).

### roar "RIPPLE ROAR" (66): APPROVED
✓ gather (Root −0.05, chin tucked, tail cocked −8 / −10 / −12); ✓ ripple Fluke → Neck reaching the head at f22;
✓ jaw opens a beat after the lift (f24 → 40 at f27, ref 3); ✓ fins snap to +22 / forward 10 with dorsals erect;
✓ `roar` f26; ✓ hold with buzz, quiver and shiver; ✓ release with overshoot; ✓ no rear-up and no chin-to-sky (head
up 16° only); ✓ Root y fixed.

`chk_roar` f27: a proper gape with a dark mouth, and from the game camera the spread fans read as a threat display.

**Optional S-R1 - buzz aliasing.**
- The jaw buzz uses a 3-frame period but is keyed every 2 frames in f32-50. The pattern comes out irregular
  (+ + − + + − …).
- Key every frame there: `frames = sorted(set(list(range(0, n + 1, 2)) + list(range(10, 51))))`.
- That costs nothing and makes the buzz even.

### act_sounding "COMET SOUNDING" (120): FIX C3 (the curl values were MY plan's error)
✓ Every beat, frame and event follows §7.1: ignite f12, plunge f28, starfall f48 / f60, splash f78, glow f96.
✓ The head → tail wave runs at 3 f lag on the plunge and 2 f lag on the resurface. ✓ Head + Neck ≤ 12° up. ✓ Snout
≥ 0.10 (0.114). ✓ Ends exactly at rest.

**C3 - the fluke-up over-curls into a scorpion hook.**
- My §7.1 values (Spine 22 + Tail 14 / 20 / 24 / 22 + Fluke 18 = 120°) rotate the fluke past vertical.
- Sampled f40-70: the fluke tips sit at y 0.374, **forward** of the fluke root (y 0.589), hanging over Dorsal3.
- From the side it is a shrimp / scorpion curl (`chk_act`) and edges toward the CelestialDragon's over-the-back tail
  arc. A sounding whale's fluke **towers behind**.
- I tested 4 curls (`fl_cmp.png`). Use set C (98° in total; the fluke stands vertical, tips over the root at y 0.582
  vs 0.615, fluke root z **1.501**, 0 pairs):

```python
"t1": [(0, 0), (14, -4), (22, -4), (34, 16), (70, 16), (80, -6), (92, 0), (120, 0)],
"t2": [(0, 0), (14, -6), (22, -6), (36, 20), (70, 20), (80, -8), (94, 0), (120, 0)],     # unchanged
"t3": [(0, 0), (14, -6), (22, -6), (38, 16), (70, 16), (80, -10), (96, 0), (120, 0)],
"t4": [(0, 0), (22, 0), (40, 10), (70, 10), (80, -8), (98, 0), (120, 0)],
"fl": [(0, 0), (22, 0), (40, 4), (70, 4), (80, -6), (100, 0), (120, 0)],
"t4y": [(0, 0), (40, 0), (46, 8), (58, -8), (68, 0), (120, 0)],     # swings +-6 -> +-8: readable from the game cam
"flr": [(0, 0), (40, 0), (46, 6), (58, -6), (68, 0), (120, 0)],     # +-4 -> +-6
```

- The slip, resurface, head, fins and events are unchanged.
- Tested in the full clip gate: collision-free, linear 0, ground min 0.114 @66 (unchanged).
- `fixed_clips.png`: the tq now shows a whale's swallowtail standing tall behind the arched back, and the game camera
  sees it swing.

---------------------------------------------------------------------------------------------------------------------
## 4. Next steps
1. Apply **C1, C2 and C3** exactly as written. My `lev_clipfix.py` is your current file with exactly these lines
   changed.
2. Re-run `headless_clips` and confirm: collision_free true, linear 0, loops closed, ground min idle ≈ 0.107,
   swim ≈ 0.143, roar ≈ 0.100, act ≈ 0.114.
3. Re-render `_act_sounding` (f12 / 30 / 50 / 58 / 78 / 96) and the swim pair f0 / f16 for the record.
4. Go to export (`headless_pack` portrait + bake). Add the `CosmicLeviathan` VFX preset (§8) only when the owner wires
   it.
5. The owner imports, saves and publishes. Never publish from here.
