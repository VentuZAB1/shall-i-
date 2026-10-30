# Inferno Phoenix v1 - MODEL GATE review 1 (2026-10-14)

## 1. Verdict: APPROVED WITH FIXES. Score 7.5 / 10 now, about 8.5 once F1-F4 are in.

**What works:**
- The head is fierce at every size: a black hood, a fused V brow, lid-heavy fire eyes and a gold hook.
- The gold circlet with five fire plumes is the model top and reads from the game camera as a burning crown.
- The fire language is consistent: every fire part is a curved, stepped tongue, all curling the same way.
- It is clearly the strongest icon of the Magma row, and it holds its own next to Rex, Orca and Mantis.
- The rig is clean. I re-ran every test myself and got 0 hits on all of them.

**What is wrong:**
1. **Hero 2 does not reach the portrait.** In the tq / icon view the three streamers hide behind the near folded wing, so only one tip shows. "Long burning tail plumes" cannot be named at 64 px.
2. **The game-camera nape is blotchy.** It shows scattered dark tiles on a red neck. The LAVA hem is buried under the dorsal saddle: there are 0 LAVA pixels at the neck in `flat_game`.
3. **The inner talons of the two feet meet at the midline.** The tips are at x ≈ ±0.003, so the feet look pigeon-toed from the front. On the long-streamer build this already produced a `Foot_L|Foot_R` hit in the roar pose.
4. **The streamers miss two numbers.** The troughs sit at 0.087 (brief ≥ 0.10), and the tongues kink 13-15° up from the vanes, so they are not collinear.
5. **The beak has a hump.** The hook segment starts 0.03 above the bill's top line, so from the side it reads as a stepped "toucan" beak.

I tested every fix on a temp copy and verified each one (§5). Apply F1-F4. Then regenerate the pack (fold sheet, icon strips, A/B, shares, limit sheet, `path_test` JSON) and hand it in at the START of the clip review. You do not need a separate model round unless your numbers differ from mine.

**How I worked:** I copied the spec and tools to `C:\Users\ventu\AppData\Local\Temp\phx_rev\`. The tools load specs from `phx_rev\specs` and render to `phx_rev\out`. My harness reproduced your share table exactly. Nothing in the project was written except this file.

**Evidence (all in `phx_rev\`):**
- `cmp_final.png`: v1 vs the fixed build, tq / side / game
- `icons_final.png`: 64 / 128 strips
- `nape_g4.png`: v1 vs 3 cape variants, game camera
- `toes.png`
- `beak_cmp.png`
- `cmp_roar.png`, `roar_game_zoom.png`
- `specs\PhxF2.py` = v1 + F1 + F2 + F3; `specs\PhxB.py` = F4

## 2. Section 9 checklist

| # | item | result | reason |
|---|---|---|---|
| 1 | side silhouette | **PASS, except the troughs** | Chest 40°. Head front 0.37 ahead of the breast front (beak y −0.815 vs keel ≈ −0.45). The S is mild but present. Belly bottom 0.492 → visible leg 24.2 %. H_MODEL 2.034, the crest is the top in bind and at f0. Streamer troughs measured **0.087** (the diamond vane's lower corner) vs ≥ 0.10 → F1. |
| 2 | front | PASS | Shield torso. The PALE tongue reads as ONE upward flame (12.0 %). Trousers inset, scarlet tarsi, the crest fans as a crown. The pigeon-toed talons are fixed by F2. |
| 3 | game camera | **FAIL (one sub-item)** | The cloak, fire hem, fire primaries over 3 fire streamers, gold ring + plumes and w90 0.349 all pass, with no rails, teeth or backpack. **The ember cape with its LAVA hem does not show**: the hem row sits at z ≈ 1.22, under the dorsal saddle's top-back edge (z ≈ 1.35), and the nape reads as dark blotches → F3. |
| 4 | icon / strip | **FAIL (one sub-item)** | "Fire bird" and "flame crest with a gold ring" pass, it is the most striking Magma icon, and the crest is not cropped. **"Long burning tail plumes" is not readable**: the portrait silhouette is 289 × 376 px with the plumes hidden → F1. |
| 5 | A/B | PASS | **Thunderbird:** they share the pose class (cloak fold), but value, S-neck, rising crest, scarlet feet and tongue shape all separate them. **Ivonrath:** bird vs dragon, vermilion + black vs uniform crimson; no family confusion at 64 px. |
| 6 | shares | PASS **with accepted tolerances** | §4 |
| 7 | face close | PASS, with F4 polish | The V brow is fused, the eyes are lid-heavy with no pupil, the malar stripes are flush, the circlet is seated, and the cere, mandible and tooth are present. The hook hump is fixed by F4. |
| 8 | crest | PASS | 5 plumes, 4 smooth steps each, +11° same-way curl, roots 0.10 / 0.09 / 0.08, 2:1 diamond section; not a corona from any view. |
| 9 | wings + fold | PASS | Δ applied; fold_search accepted (D1); same-sign tongues; secondaries EMBER→LAVA; primaries LAVA→FLAME→HOT. |
| 10 | streamers | **PASS, except collinearity** | Round knuckles, shafts 0.09, vanes 3.8:1, diamond section; wing clearance measured **0.152** (≥ 0.06). But the tongue bends up from the vane (C 10°→24°, L 13°→28°), so it is not collinear, and in the roar rattle it would pass 85° → F1. |
| 11 | remix sweep | PASS | No seams, bolts, fan, disc, points, horns, membranes, back blades, crescents, violet, pupil or gold feet. |
| 12 | hard rules | PASS | 11,604 tris; BASALT lum 73.4; HEIGHT 10; no `environ`; no Neon. Sub-0.02 details (nostrils, gape lines, eye hot spot) are the approved Thunderbird recipe: accepted. H_MODEL constant 2.05 vs measured 2.034 → F5 (optional). |
| 13 | rig + limits | PASS | Re-run by me on v1: 0 hits at rest, all 6 limit poses and all 10 paths. Limit 5 is substituted by the airborne rising frame (D8 note below). All anchors exist. |
| 14 | deliverables | PASS | Next time attach the raw `PATH_RESULT` line, not just "0 hits". |

## 3. Deviations

- **D1 FOLD (86,6,−80,10): APPROVED.** It beats every acceptance number. With F1 the wingtip → C-vane-start distance becomes 0.366 (≤ 0.45). Re-run fold_search with `FOLD_TAIL=1.24,0.15` for the record.
- **D2 crest C 0.52 / inner 0.40: APPROVED.** The brief's 2.07 estimate ignored the back-curl, and 2.034 is in tolerance.
- **D3 vane 0.10 wide: APPROVED.** The brief's 0.20 max width broke its own ≥ 3.5:1 rule on a 0.37 vane. With F1 the vanes are 0.47 / 0.45 long, so they become 4.7:1 / 4.5:1.
- **D4 PALE tongue on the keel + throat tip: APPROVED.** The front reads as one rising flame.
- **D5 cape / arm bar: PARTLY OVERRULED.**
  - The arm bar (EMBER only on its inner 22 %) is approved.
  - The BASALT Neck cape with its EMBER + LAVA hem on the t 0.30 row is overruled: that row is buried under the dorsal saddle, and the 7 BASALT Neck2 tiles read as blotches from the game camera.
  - Replace both with F3: a clean dark hood tail plus ONE burning collar row above the mantle.
- **D6 x-separated roots (0.095), shafts hw 0.045: APPROVED.**
- **D7 pyre Spine z −0.05: APPROVED, and generalised** to every planted crouch (see §6.1).
- **D8 rising-frame legs (50, roll −15, −30, 66): APPROVED.** I re-verified them with the F1 streamers.
- **D9 fly tuck THI 60 / roll −18 / SHI −40 / FOO 70: APPROVED.** After F1 + F2 the fan L −8 / R +8 is still 0 hits at both wave extremes, so keep it.
- **Limit 5 substitution: APPROVED.** X1 −24 on the ground is geometrically impossible: the troughs rest at 0.10, and X1 −8 already puts the vane at −0.05. The ground drop floor is the pyre value X1 −4 / X2 −4 / X3 −2 (tested clean). X1 −24 is only legal airborne.

## 4. Share misses: all ACCEPTED as tolerances (no colour changes)

| miss | decision | why |
|---|---|---|
| side PALE 1.7 | accept, structural | The tongue faces forward. Front (12.0) and tq (5.7) carry it. Do NOT add pale flank stripes: that is the penguin read. |
| tq EMBER 33.4 | accept (ceiling 35) | tq looks straight at the neck column and breast flank. Darkening the neck sides would push side BASALT (already 44) toward 48: side and tq conflict on this posture. The Ivonrath A/B passes on value and form. |
| side BASALT 44.2 | accept | The folded cloak IS the side view. After F1 it is 42.2, inside the target. |
| game EMBER 23.2 | accept | +1.2. After F3 it is 23.4. |
| front EMBER 40.2 | accept | After the fixes it is 39.8, inside the target. |

**After F1 + F2 + F3** (my flat-ID run of `PhxF2`):

| view | BASALT + D | EMBER | PALE | FIRE | GOLD |
|---|---|---|---|---|---|
| side | 42.2 | 23.8 | 1.7 | **24.0** | 3.0 |
| tq | 35.3 | 32.7 | 5.7 | 15.1 | 4.6 |
| game | 45.6 | 23.4 | 1.4 | 20.4 | 2.7 |
| front | 24.3 | 39.8 | 12.0 | 8.4 | 4.9 |

Side FIRE 24.0 (+2) is accepted: it is the longer fire vanes, i.e. the hero.

## 5. Fixes (exact; all tested on the temp copy)

### F1 - MUST: longer, fanned streamers with collinear tongues and troughs ≥ 0.10
Replace the `STREAM` dict. `STREAM_START` is unchanged; the blocks, joints and capsules all derive from it.
```python
STREAM = {"C": [(0, 0.38, 0.60), (0, 0.80, 0.31), (0, 1.24, 0.15), (0, 1.70, 0.265), (0, 1.91, 0.32)],
          "L": [(0.095, 0.37, 0.53), (0.14, 0.73, 0.27), (0.25, 1.13, 0.155), (0.38, 1.55, 0.265), (0.435, 1.735, 0.315)]}
```
- **Lengths:** C 1.39 → 1.64, sides 1.22 → 1.50.
- **Geometry:** the side tips fan to x ±0.435; vane → tongue is collinear (< 1°); vanes rise 14° (C) / 15° (L). Update the vane comment to 4.7 : 1.
- **Verified:**
  - 0 hits on L1-L4 (planted), L5 rise, L6 fly (both extremes, with fan ±8, 0 and inward 4), roar ×4 and all 10 paths
  - wing ↔ streamer clearance at FOLD **0.124**; streamer min z **0.102**; spine min z 0.492; tris 11,428 (with F2 + F3)
  - bind bounds 2.97 × 2.74 × 2.07
- **Icon:** the near plume now sweeps out bottom-right past the hem, so the crest-top-left / plume-bottom-right composition asked for in the brief (§6.7) exists. The portrait still has width to spare (289 of 376 px), so the bird does not shrink in its tile.
- **Side / game:** a long, elegant three-plume train that fans in the game view (`cmp_final.png`).

### F2 - MUST: toe splay (the brief's §4.8 said 18°; v1 used 34° on both side toes, and the inner talons met at x ≈ 0)
Replace the toe loop header in `model()`. The talon and hook lines below it stay unchanged; they use `tb` and `d`.
```python
        for dx, spl in ((-0.040, -14.0), (0.0, 0.0), (0.045, 20.0)):          # inner / middle / outer, mirrored
            d = Vector((s * math.sin(math.radians(spl)), -math.cos(math.radians(spl)), 0))
            tb = T + Vector((s * dx, 0, 0)) + d * 0.10 + Vector((0, 0, -0.005))
            B.seg(T + Vector((s * dx * 0.5, -0.02, 0.0)), tb, 0.026, 0.024, EMBER, "Foot_" + side, role="limb")
```
Verified: the inner talon tips now sit at x ≈ ±0.055 (gap 0.11). The latent `Foot_L|Foot_R` hit is gone. The front reads as a three-forward raptor foot (`toes.png`).

### F3 - MUST (checklist 3): a clean hood tail plus a visible burning collar
Replace the two `neck_cape` calls:
```python
    neck_cape(B, n2a, n2b, 0.13, [(0.80, (-0.065, 0.0, 0.065), False), (0.45, (-0.065, 0.0, 0.065), False)],
              "Neck2", col=BASALT)                         # a clean dark hood tail down the nape
    neck_cape(B, n1a, n1b, 0.15, [(0.90, (-0.11, -0.04, 0.04, 0.11), True)],
              "Neck", hem=True, col=EMBER, last_col=EMBER)     # one burning collar row (EMBER + LAVA tips) above the mantle
```
- **Verified:** the game camera now shows a tidy dark hood tail ending in LAVA-tipped collar points just above the mantle (`nape_g4.png`, panel 4).
- **Tested and rejected:** (C1) raising your hem to t 0.64 left the blotches and showed one tip; (C2) an all-EMBER cape gave a clean red neck but no visible hem.
- **Effect:** shares move ≤ 0.5. It is also −10 blocks.

### F4 - SHOULD (face polish): a continuous culmen
```python
    B.seg(HC + Vector((0, -0.25, -0.024)), HC + Vector((0, -0.325, -0.058)), 0.040, 0.036, GOLD, "Head",
          top=(0.8, 0.8), role="limb", nostud=True)                                                   # hook segment
    B.spike(HC + Vector((0, -0.322, -0.054)), (0, -0.45, -1), 0.07, 0.032, BLACK, "Head", top=(0.15, 0.2))  # hook tip
```
Verified in close-ups (`beak_cmp.png`): the bill top flows into the hook, and the black tip continues the curve. Re-run the Jaw pairs at Jaw 34.

### F5 - OPTIONAL: `H_MODEL = 2.034` (measured)
This gives PITCH 0.0456 instead of 0.0460.

## 6. What the CLIP phase must take from this round

1. **Planted crouch cap: Spine z ≥ −0.05 whenever the feet are planted.** The knee is buried in the lower body, so a deeper crouch drives the trouser tops into the Spine.
   - This applies to the act pyre (−0.13), the act wind-up (−0.14) and the **takeoff crouch (−0.12)**: all go to −0.05, or re-test.
   - The pyre "sinking" comes from Spine pitch +9, Chest +3, the bow (Neck / Neck2 / Head +12 / +12 / +20), Crest −10 and the PYRE wings.
2. **Ground floor for the streamers: X1 ≥ −4, X2 ≥ −4, X3 ≥ −2 on any ground frame.**
   - pyre settle −6 → −4
   - land overshoot −6 → −3
   - roar release −6 → −4
   - idle drift: bias it upward (X1 0…+3, not ±1.5)
   - walk: X1 baseline +4 (the fanned L tip dips 0.03 more under the 4° roll)
   - sample `ground_min_z` on every frame
3. **Airborne hang with F1.** X1 −24 at the rising frame (z 0.46) clears the ground by only 0.015. Use **X1 −18 / X2 −6 / X3 +4** (0.134 clear, 0 hits, D8 legs).
   - In act beat 1 (z 0.14) keep X1 ≥ −6 until z ≥ 0.30.
   - At the takeoff launch, cap the drag at X1 −12 unless every frame clears −0.02.
4. **Roar train: hold the wings at LIFT1 (84,16,−80,−15) during the train, NOT BREATH.**
   - With BREATH the cloak covers most of the raised plumes from the side / tq and half of them from the game camera.
   - With LIFT1 the three tongues stand clear in front of the wing on the game camera (`roar_game_zoom.png`).
   - Keep the brief's streamer keys X1 +56 / X2 +24 / X3 −14. With F1 that puts the vane at 80° (rattle ±5 → 75-85) and the C tip at z 1.79, y 1.29, 0.33 under CrestTip (2.12). Tested 0 hits; LIFT2 and BREATH are also clean if the owner prefers the gesture.
   - The new target replaces "C vane top 1.45-1.62": **C tongue tip ≤ 1.85 and ≥ 0.25 below CrestTip; y ≥ 0.95.**
   - In tq the raised plumes must still read as rising from the TAIL behind the wing hem, not as a row of standing back blades (Black Dragon). Check the tq pose sheet at f20.
5. **Fly:** D9 legs plus the fan L −8 / R +8 are clean on the fixed model at both wave extremes. FPITCH, gyro and stroke as in the brief.
6. Everything else in brief §7 stands: look-back 44° tested clean, Crest +14 tested clean, references before keying.

## Summary
- **Verdict:** APPROVED WITH FIXES, 7.5/10 (≈ 8.5 after the fixes). A fierce, well-built fire raptor with a clean rig, and the best icon of the Magma row.
- **Must do:**
  - **F1:** longer, fanned, collinear streamers with troughs ≥ 0.10, so the tail hero reaches the portrait
  - **F2:** toe splay −14 / 0 / +20, which separates the talons
  - **F3:** hood-tail cape plus one burning collar row visible from the game camera
- **Should do:** F4 (continuous beak culmen).
- **Deviations:** D1-D4 and D6-D9 approved; D5 partly overruled (by F3).
- **Share misses:** all accepted as tolerances.
- **Clip phase:** planted crouch ≥ −0.05 everywhere (takeoff included); ground streamer floor X1 −4; airborne hang X1 −18; roar train held at LIFT1, not BREATH.
