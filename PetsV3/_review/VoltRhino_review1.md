# Volt Rhino - model gate review 1 (2026-10-27) - REVISE (model)

**Score: 6/10 for a 6 % High** (ship bar about 8). Silhouette, the lime-horn hero and the distinctness all work. The body
finish does not yet read as fierce or finished: the light flanks, the hoop folds, the flat-cut armour edges, the thin pale
underside and the cold horn read as a toy. Every fix below is a code-level change in `pets/VoltRhino.py`. No new concept.
With M1-M8 applied I expect about 8/10.

**Verdict: REVISE.** One more model round (send the list at the end), then the clip gate.

## What I looked at
- `pets/VoltRhino.py` (244 lines, line references below)
- `VoltRhino/MODEL_NOTES.md`, `_review/VoltRhino_plan.md` (v2), `GLACIER_CONCEPTS.md`, `GLACIER_PLAN_REVIEW.md` section 2.9
- format and strictness: `VenomBasilisk_review2.md`, `ThornbladeMantis_review2.md`
- Obsidian `Creature Style.md`, `Model Review Checklist.md`; `FIERCE_GUIDE.md`
- Volt Rhino renders: `_model_sheet`, `_close_sheet`, `_icons_strip_64`, `_icons_strip_128`, `flat_side`, `flat_tq`,
  `flat_game`, `model_side`, `model_front`, `model_game`, `model_tq`, `VoltRhino_icon.png` (portrait)
- comparison: Raiju, ThunderBull, ThunderRex, Thunderbird, StormWyvern `_model_sheet.png`; `_ALL_FIERCE_progress.png`
- sibling palettes (code): Raiju FUR (80,102,182) / BOLT (255,202,36); ThunderBull BODY (98,108,178) / EYE cyan;
  Thunderbird BOLT (255,234,56); ThunderRex BELLY (176,196,240) / CYAN; StormWyvern BODY (96,90,166)

Not checked (missing): an underside view, a back view at icon angle, a clip. Game-camera colours are the owner's rule
(about 0.6x in game), not a measured Roblox render.

---------------------------------------------------------------------------------------------------------------------
## 1. The lead's question: the game-colour read

**Partly yes.** The grey is not the whole problem. The split is:

- **The back is fine.** IRON_D is the darkest mass (46 % of the side view, 69 % of the game camera, `flat_game`). In game
  the back reads as dark slate. Gate 2 of the plan passes.
- **The flanks and legs are the risk.** IRON (172,178,190) is a light, low-chroma lavender grey (S about 0.07). It covers
  40 % of the side view. Roblox's ~0.6x puts it around (103,107,114) in game: a mid-light flat grey.
- **Five things make it read as a toy, and colour is only one of them:**
  1. flat, low-chroma flank grey with no value range inside it;
  2. the stud dots show as white bubble-wrap on light grey (`_close_sheet` panels 1 and 3);
  3. the two fold rims (lines 106-107) are full loft rings from the belly to the top: they read as tank hoops in
     `model_side` and `model_game`;
  4. the armour bands are cut flat at the bottom (saddle zlo 0.28 at line 103, rump zlo -0.16 at line 104), so the flank
     reads as stacked boxes (the light rectangle mid-flank in `flat_side`);
  5. the horn is a smooth cold white blade with a visible step at each segment joint (`_close_sheet` panels 2 and 3), and
     the pale underside is only 5.1 % (plan 10 %), so nothing breaks up the grey.
- **Distinctness is a real asset.** It is the only neutral body in the Thunder egg (`_icons_strip_64`). Do not turn it blue
  to match the siblings. Keep the chroma low (S 0.14 or less) so it stays iron, and widen the value range instead.

**What makes it feel finished and fierce (answer in short):** a darker, slightly steel-cool flank; a back that is clearly the
darkest; tapered armour edges and fold wedges instead of rings and cut steps; a real pale underside band; a brighter, warmer
horn with a seam collar; and more lime on the rump and the eyes.

---------------------------------------------------------------------------------------------------------------------
## 2. MUST (prioritised, all in `pets/VoltRhino.py`)

### M1. Iron, not plastic: darker, steel-cool palette (lines 16-17)
- `IRON (172,178,190)` -> **(156,164,178)**: flanks, legs, head. Hue 218, S 0.12. The brightest channel is 178, so it keeps
  the guide's brightest-channel rule (170 or more). This is the lead's "darker iron", inside the luminance clause.
- `IRON_D (100,108,122)` -> **(92,100,116)**: back, shield, folds, brows, feet. Hue 220, S 0.21. The back stays the
  darkest mass in game (about (55,60,70) at 0.6x).
- `PALE` stays (222,224,228), see M4. `HORN_IVORY` changes, see M6.
- Re-check the value shares after the change: IRON_D at least 25 % of the side view (plan gate).
- Expected game flank: about (94,98,107) at 0.6x, down from about (103,107,114).

### M2. Fold rims: tapered wedges, not hoops (lines 106-107)
- The two fold bands are full rings from the belly line up over the back (`Lb.band(... zlo=zl, grow=0.050)`). Replace each
  with a tapered wedge: `B.seg` from the spine down to a point at the belly line, `rnd=0.30`, IRON_D, same y positions.
- Proud depth `grow 0.050` -> **0.030** model units (about 0.16 studs). Thinner in y: 0.07 stays.
- The wedge catches the light on its top face and goes dark underneath: this is the "stronger fold shading" the lead asked
  for, without a painted line.

### M3. Armour edges: no flat horizontal cuts (lines 102, 103, 104)
- The three IRON_D bands end in flat horizontal bottoms: shield zlo -0.22 (L102), saddle zlo 0.28 (L103), rump zlo -0.16
  (L104). Each one reads as a box step on the flank (`model_side`, `flat_side`).
- Slope every lower edge: the rump plate from about **-0.30 at the front to -0.02 at the rear**; the saddle from about 0.34
  front to 0.22 rear. If `Lb.band` cannot slope, replace each band with 2-3 short `B.seg` wedges that taper to a point.
- The shield keeps its proud overlap. Its lower front edge may stay at -0.22.

### M4. Pale underside: 5.1 % -> 8-10 % (lines 99-100)
- Raise the top of both PALE bands from `zhi=-0.54` to **-0.46**. The strip then climbs the lower flank and ends in a point
  at the elbow. Keep the belly taper, so it does not turn into a bib.
- Reject the deviation in MODEL_NOTES ("a bigger pale area read as a white bib"). The bib risk starts above about 12 %; 8-10 %
  tapers fine. Target the side-view PALE share at 8-10 %.

### M5. Ears: from headphone cups to dark ear flaps (lines 148-153)
- From the front (`_close_sheet` panel 1, `model_front`) the ears are white-rimmed rectangular cups. They read as headphones.
- Outer spike length 0.27 -> **0.20** (line 151); root z 1.24 -> **1.18** (line 149).
- Outer shell colour IRON -> **IRON_D**; inner spike IRON_D -> **BLACK** (nostud). Dark ears match the fierce brow and
  remove the white rim.

### M6. Horn finish: from cold white blade to ivory horn (lines 19, 156-159, 170)
- The base and both segment joints show a visible step (`_close_sheet` panels 2-3). Add a **HORN_SHADE (205,198,180)** collar
  ring 0.014 thick at `b0` and at `h1`, `nostud`. The collar covers the seam and adds form.
- `HORN_IVORY (240,236,222)` -> **(232,224,204)** (line 19). A warmer ivory stops it reading as cold white plastic in the game
  camera. It stays the brightest large shape on the model.
- The lime zig on the horn: width 0.050 -> **0.060** and thickness 0.010 -> **0.013** (line 170), so the lightning survives at
  64 px. Keep the 3 zigzag segments; no kink.

### M7. More lime: VOLT 2.4 % -> about 4 % (plan)
- Add **one lime zig per rump flank**, the same `zig()` call pattern as the shoulder bolts (lines 110-115), width 0.060, on the
  rump plate after M3.
- Eye slits, line 139: `(0.007, 0.016, 0.070)` -> **(0.008, 0.018, 0.080)**. Line 138: tilt 16 deg -> **22 deg** (fiercer slant).
- Target VOLT at 3.5-4.5 % of the side view.

### M8. Face finish: nasal ridge and brow (lines 121, 145)
- The nasal ridge band `grow=0.022` (line 121) reads as a dark pipe across the snout (`_close_sheet` panel 2). Set `grow` to
  **0.012** so it blends into the nose.
- The brow capsule `(0.034, 0.034, 0.112)` (line 145) reads as a stuck-on bar. Make it **(0.040, 0.026, 0.096)** and move it
  0.008 toward the skull, so it is an overhang and not a pipe.

---------------------------------------------------------------------------------------------------------------------
## 3. NICE (do these too)

- **Accent hue.** VOLT (210,255,80) is hue 75. It is 22 deg from the Thunderbird BOLT (255,234,56, hue 54), the plan's
  accepted cross-egg pair, and 30 deg from Raiju's BOLT (255,202,36, hue 45). A greener lime **(190,255,64)** (hue 80) puts
  it 27 deg from the Thunderbird and reads more "electric". The accent is accepted; this is polish.
- **Horn growth rings.** Two HORN_SHADE ridges on the upper horn (0.008 thick) add a real rhino-horn read.
- **Fore shin gaiter.** A short IRON_D band on the front shins (near lines 184-187) adds a fierce dark leg accent.
- **Shield bolts** (lines 110-115): good, keep.

---------------------------------------------------------------------------------------------------------------------
## 4. Deviations from the plan (accept or reject)

| Deviation (MODEL_NOTES) | Ruling |
|---|---|
| HEIGHT 8.5 measured at the withers, not the horn tip | ACCEPT. Horn tip sits at 0.91 H, so the plan's own numbers could not reach H. |
| Horn 0.49 H (plan 0.32 H) | ACCEPT. It is the hero and it reads in the 64 px strip. Keep it. |
| Cooler palette tint | ACCEPT the idea. M1 supersedes the numbers. |
| PALE 5.1 % (plan 10 %) | REJECT. M4 raises it to 8-10 %. |
| Lofted barrel + raised shells instead of boxes | ACCEPT. Better than the first box build. M2 and M3 remove the remaining box and ring cues. |
| EYE_HOT centre, nostud on horn and toenails | ACCEPT. |

---------------------------------------------------------------------------------------------------------------------
## 5. Pass / fail checklist

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Tris at or under 15k | PASS | 10,348 |
| 2 | Silhouette at 64 px; species reads at once | PASS | Rhino + horn; the lightest silhouette in its strip |
| 3 | Hero (lime horn) reads at 64 px | PASS | Widen the zig (M6) to keep it |
| 4 | Fierce, not cute | PARTIAL | Eyes and brows fierce; ears and round head soften it (M5, M8) |
| 5 | Not a grey plastic toy | FAIL | M1-M4, M6 |
| 6 | Dark back + pale underside + ONE accent | PARTIAL | Back PASS; underside FAIL at 5.1 %; accent PASS but thin |
| 7 | Palette shares (plan) | PASS / FAIL | IRON_D 45.9 % (gate 25) PASS; PALE 5.1 % (plan 10) FAIL; VOLT 2.4 % (plan 4) FAIL; HORN PASS |
| 8 | Accent strong in game colours | PARTIAL | Horn and shoulder bolts read; rump and eye slits small (M7) |
| 9 | Distinct from siblings (accent, act) | PASS | Only neutral body in the egg; accent 22 deg from Thunderbird BOLT (accepted) |
| 10 | Stud skin off horn, inlays, toenails, eyes | PASS | `nostud` used on horn, zigs, toenails, eyes |
| 11 | No glow, no Neon | PASS | Light and colour only |
| 12 | Floating, poking, intersecting parts | PARTIAL | Ears, brow capsule, nasal band, horn base step (M5, M6, M8) |
| 13 | Visible from below | NOT CHECKED | Need an underside render (belly strip, chin, horn underside) |
| 14 | Deliverables complete | PARTIAL | Missing: underside, back at icon angle, 600 px game-camera render |

---------------------------------------------------------------------------------------------------------------------
## 6. Round-2 deliverables (send all at once)

1. `pets/VoltRhino.py` with M1-M8 applied and NICE items you choose to take.
2. `_model_sheet.png` (5 views) and `_close_sheet.png` (face, horn base, ears).
3. `_icons_strip_64.png` and `_icons_strip_128.png`: Volt Rhino FIRST, then ThunderBull, Raiju, Thunderbird, ThunderRex.
4. `flat_side`, `flat_tq`, `flat_game` with the new value shares (side: IRON_D >= 25 %, PALE 8-10 %, VOLT 3.5-4.5 %).
5. An underside render and a 600 px game-camera render.
6. A horn close-up (base and joints).

Gate for the clip stage: the 64 px strip reads as steel, not grey plastic; the back is the darkest mass in game; the underside
is pale; the horn reads at 64 px. Do not start the clips before this passes.
