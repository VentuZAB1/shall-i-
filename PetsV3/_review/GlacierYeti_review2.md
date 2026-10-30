# Glacier Yeti - model gate review 2 (2026-10-27) - APPROVED WITH FIXES (model)

**Score: 7/10 for a 14 % big tier** (round 1 was 5/10). Ship at 8/10 or better.

All seven round-1 MUSTs and the NICE items landed. The fists no longer read as faces, the accent shows, the face reads fierce without a grin, the hump no longer shows a white cap, and the chest has form. The creature is now a fierce, heavy ice-armoured ape rather than a blocky robot.

Two side-profile problems are left, and they are the same kind of misread the owner has rejected before (a white bib and white teeth). Both are small and codeable. Fix them in the mesh before export. I will re-check them in the clip-gate side renders. No further full model round is needed if they land as written below.

## What I looked at

- Code: `pets/GlacierYeti.py` (palette L16-22; pectoral and abdominal masses L114-129; crust and rim icicles L194-199; shelf 2 on the upper arm L207-212; arms L180-186; legs and feet L214-226).
- Builder notes: `GlacierYeti/MODEL_NOTES.md` "Round 2" section, including the value table.
- Renders (round 2): `_model_sheet.png` (incl. `model_lowfront`), `_close_sheet.png` (front, side, tq), `_chest_sheet.png` (incl. `chest_front`, `chest_lowfront`, `chest_lowtq`, `chest_side`), `under.png`, `model_side.png`, `model_back.png`, `model_game.png`, `flat_game.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, and the combined strip `VoltRhino/_scratch/_all_strips_r2.png`.
- Not re-counted: the value shares. There is no PIL in the Python install I can reach, so I used the builder's table. The AURORA share is also visible by eye in `flat_game.png` and the side render.

Measured: 5,832 tris (cap 15k). HEIGHT 9.0 studs (1.63 Blender units). Side shares (builder): POLAR_NAVY 50.3, NAVY_D 13.3, PLATE_ICE 16.1, AURORA 3.4, BROW 13.5, BLACK 3.1, IVORY 0.3. Game shares: AURORA 4.4.

## Round-1 MUST check

| # | Item | Result |
|---|---|---|
| M1 | Fists: plates on top edge, no seam, smooth BROW front | PASS. No face read. The fists are still cube-like (NICE 3). |
| M2 | Arms tapered (upper 0.17 to 0.14; forearm 0.15 to 0.10) | PASS on spec. The arm still reads as a parallel sleeve (NICE 4). |
| M3 | Legs: thigh 0.19 to 0.15; calf bulge; shin 0.14 to 0.10; wedge feet, 3 toes | PASS. The legs read as thick, jointed legs. The feet read as wedges with toe nubs. |
| M4 | Chest form: 2 pectoral masses + 1 abdominal mass | PASS, with a note. The pecs read as pads with hard seams (NICE 2). The abdominal block is fine in profile. |
| M5 | Navy muzzle, 0.10 fangs | PASS. The face is fierce, with no grin or bib in the front view. |
| M6 | AURORA seams 0.040 round each crust rim (3.4 % side, 4.4 % game) | PASS. The green rim reads on the front shoulders at 128 px and in the game render. Only a faint edge at 64 px. |
| M7 | Hump sheet lowered and tilted, no white cap above the skull | PASS. Nothing shows above the skull in the front or close-up views. |

## NICE check

- Brow wings narrowed: PASS. The V no longer reads as a visor.
- Skull 0.22 wide: PASS. The head reads as a head.
- NAVY_D on the belly, pelvis, shins and calves: PASS in the side view. It is subtle, which is fine.
- Crust rim icicles trimmed to 2 per crust: PASS, with a side-view problem (MUST 2).

---

## Remaining MUST (in priority order)

1. **A pale slab on the upper arm reads as a white bib on the chest in profile.** This is shelf 2 (`pets/GlacierYeti.py` L207-212). In `model_side.png` it is the pale plate with a green bottom edge at about x 220-335, y 220-295, lying over the chest front. The cause: the slab's normal points straight out along x (`(s*cos20, 0, sin20)`), so from the side camera it is seen face-on, and its centre (about y -0.26) sits in front of the chest line (about y -0.33 at that height). It was already there in round 1, and I missed it then.
   - Shift `Ua` back in y by +0.08, and move it down the arm from 0.42 to 0.50 of the shoulder-to-elbow length.
   - Shorten the outline's y extent by about 25 % so its front edge stays behind the chest line (y greater than about -0.22).
   - Keep the outward normal and the lower-edge seam.
   - Target: no pale plate over the chest front in the side view.

2. **Front rim icicle reads as a second set of white teeth in profile.** The crust's front icicle is `j = 0` (L196-199): its direction is `(s*0.20, -0.15, -1)`, which points down and forward, straight at the snout in profile (`model_side.png` at about x 270-330, y 170-215). That is the two-fang read the owner dislikes.
   - Either delete the front icicle, or change its direction to `(s*0.45, +0.05, -1)`. That points it outward and slightly back, with no forward component.
   - Keep the back icicle (`j = 1`).
   - Target: no white point below the crust's front edge in the side view.

## NICE (do these too)

1. **Pectoral masses look like stuck-on pads.** Sink them: reduce `out` from 0.024 to about 0.010 (L118-119) and raise `rnd` from 0.50 to about 0.60, so they blend into the chest. Keep the abdominal block.
2. **Fists are still cubes with a white lid.** Taper the claw-side face of the fist so it reads as a knuckle wedge, for example by lowering the front-bottom corner by about 0.03 (L185). Keep the BROW front smooth.
3. **Arms read as a parallel sleeve.** Add a bicep block at the middle of the upper arm (about 0.15 half-width, `rnd` 0.6) and keep the wrist at about 0.62 of the elbow width (currently 0.67).
4. **Tris are at 5,832.** There is room for the NICE items and for the MUST fixes without going near the 15k cap.

## Pass / fail checklist (model gate, round 2)

| Check | Result |
|---|---|
| 64 px silhouette: a hunched ape/yeti reads | PASS |
| 128 px strip: pale shoulders, dark head, accent rim visible | PASS |
| Upper face fierce (slits, brow, no round eyes, no glint, no smile) | PASS |
| Muzzle and fangs: no grin, no bib in the front view | PASS |
| No white bib or teeth in the side view | FAIL (MUST 1, MUST 2) |
| Real anatomy, tapered limbs | PASS (arms still sleeve-like, NICE 3) |
| Fists and feet are not faces or boxes | PARTIAL (NICE 2) |
| No box belly; belly line rises in side view | PASS |
| Pectoral form in front view | PASS (NICE 1) |
| Dark body + ONE accent (no pale underside, accepted) | PASS (AURORA 3.4 %, visible) |
| Body colour rule: brightest channel 170 or more | PASS (196) |
| Studs everywhere, details smooth | PASS |
| No glow, no Neon | PASS |
| Tris 15k or under | PASS (5,832) |
| Floating, poking or intersecting parts (visible parts) | PASS (the hump sheet is fixed) |
| Parts visible from below | PASS (`under.png`: no gaps or floating parts; feet and claws sit flat) |
| Tier fit: big, below Roc, Titan and Absolute Zero, heavier than the Mammoth | PASS |
| Distinctness: no sibling copy | PASS (the strip shows it is not LavaGolem or Mammoth; the blue reads close to Raiju and ThunderBull in hue, cross-egg, accepted) |
| Clip gate | not judged this round |

## Notes for the clip gate

- Re-check the side view after MUST 1 and 2 (send `model_side.png` and a 3/4 side).
- The game camera (about 5 studs up, FOV 70) is the real judge of colour. Re-check the body colour once it is in Studio, since Roblox darkens about 0.6x. The Blender preview reads lavender-periwinkle, which is expected before darkening.
- The hump sheets now sit lower and tilted. Check that the clip poses (especially the skid and roar) do not push a sheet through the head.
