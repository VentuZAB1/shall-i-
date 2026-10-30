# Frostfang Lynx - model gate notes (builder A, 2026-10-27)

File: `pets/FrostfangLynx.py` (lead draft kept in `_scratch/FrostfangLynx_v1_lead.py`).
Tris 6,416. Size 0.46 W x 1.58 L x 1.19 H units; HEIGHT 7.0 studs = the ice-tuft tips. TH 0.384, PITCH 0.034.
Rig builds (32 bones, head pivot at the throat (0, -0.535, 0.82)).

## What I built (fixes to the lead's draft)
- **Head x1.28 about the throat** (`HJ`, `HEAD_S`, ShadePanther pattern). Every head part moves: skull, cheeks, muzzle,
  eyes, brows, fangs, jaw, the beard ruff, ears, tufts. Rig joints Jaw / Ear / FX_IceDust go through `hs()` too.
- **Shoulders**: the upper foreleg is a rounded (rnd 0.45) tapered block set 0.008 inward, with an elbow tuft and
  spots on it, so the flat slab face is gone. The thighs are rounded the same way.
- **Anti-stilt**: the whole body / head / tail sit 0.03 lower (`DZ`, legs shortened via `LEGS`). Forearms, shins and
  socks are ~12 % thicker. Snowshoe paws are 0.076 x 0.088.
- **Rosettes**: organic flush Poly blobs (irregular 7-8-gons) and 3-crescent rosettes on the chest, waist, hips, neck
  and all upper legs and shins. **Rosettes alone = 20.3 % of the side view** (BACK_SHADE 28.9 % with spots, 8.6 %
  without; the `LYNX_NOSPOTS=1` env switch renders without them).
- **Saddle**: flush studded Tube inlays on the three torso tops, plus a dark nape scruff. A raised slab saddle read as
  shiny metal plates, and a cape wrapping the edges read as boxes on the back.
- **Face**: V brows lie over the eye tops as lids; the vertical pupils are enlarged. The lynx beard is a snow sideburn
  block with a fan of 4 chunky points flaring sideways. Muzzle with two puffy whisker pads.
- **Ears**: an ICE frost cap on each ear tip plus 2 thin ice pencils. Cones read as horns, and with the chin tuft they
  read as a goat at 64 px. The chin tuft is removed.

## Value shares (flat palette)
| | side | tq | game |
|---|---|---|---|
| WARM_SILVER | 49.7 | 40.6 | 47.2 |
| BACK_SHADE (rosettes 20.3 side) | 28.9 | 24.7 | 33.4 |
| SNOW | 13.6 | 24.9 | 11.4 |
| ICE / ICE_CLAW | 0.7 / 0.9 | 1.4 / 2.0 | 1.0 / 0.0 |
| BLACK | 3.6 | 3.3 | 4.8 |
MOUTH ~1.3 and TEETH ~1.3 are anti-alias edge pixels (nearest-colour match), not real surfaces.

## Deviations from the plan
- **ICE is 0.7 % of the side view** (plan 5 %). ICE is only on the eye slits, ear caps and tuft pencils; reaching 5 %
  would need horn-sized tufts, which read as a goat. The tufts read at 64 / 128 px.
- **SNOW is 13.6 % side / 24.9 % tq** (plan 20 %). The underside is mostly hidden from a level side camera.
- **Ground to elbow is ~0.26H** (plan 0.42H). The plan's numbers conflict (withers 0.62H with the elbow at 0.42H leaves
  no chest), and the lead flagged the stilt look.
- **One Claw bone per forepaw** (`Claw_FL` / `Claw_FR`) carries all 4 claws, not one bone per claw. The act flexes them
  together.
- **`FX_IceDust_L/R` are parented to `Ear_L/R`** (the plan says `Tuft_*`). The tufts are rigid on the ears, so they
  have no separate bone.
- VFX anchors: FX_IceSpark_L/R [Claw_F*], FX_IceDust_L/R [Ear_*], FX_SnowPuff_FL/FR [Foot_F*], FX_SnowFlick [Tail3].

## Round 2 (review 1 fixes, 2026-10-27)
Tris 6,400. Size 0.42 x 1.46 x 1.16 units.
- **M1 bug**: the DZ loop now moves Tube saddles with `Tube.map`, which updates `rings`, `pts` and `c`. The saddle sits flush; see `renders/crop_rump_side.png`.
- **M2 bobtail**: `TAILP` is 0.19 long and keeps the black tip. `FX_SnowFlick` moves with it.
- **M3 ICE is 2.6 % side / 2.2 % game / 4.5 % tq** (it was 0.7 / 1.0 / 1.4):
  - claws are ICE;
  - each ruff spike is a 55 % SNOW base with a 45 % ICE tip (45 rather than 40 to clear 2.5 %);
  - the frost fangs are ICE_CLAW, 0.066 long;
  - the iris is 0.034 x 0.012 and the socket 0.040 x 0.018.
  - TEETH is removed from the palette (unused).
- **M4 pupil**: forward to y -0.720, 0.026 tall; the brow is 0.004 higher. The slit is visible from the front; see `renders/crop_eyes_front.png`.
- **M5 ears**: the base is 0.088 wide and the pencils 0.045 / 0.040.
- **NICE**:
  - the front sock is 0.035 tall;
  - the lowest spot on each shin is removed;
  - the underline rises 0.015 toward the hind legs (tuck end, waist bottom, snow strip);
  - the mid ruff spikes are 0.088 / 0.078 and the top one 0.066.
  - The saddle stays as 3 inlays: flush after M1, the seams follow the torso block steps.
- **Shares, side**: WARM 50.1, BACK 28.6 (rosettes 20.8 = 28.6 - 7.8 no-spot), SNOW 13.1, ICE 2.6, ICE_CLAW 1.0, BLACK 3.3.
- **Under-view**: `renders/low_below.png`.

## Round 3 (review 2 fixes, 2026-10-27)
Tris 6,356.
- **M1**: the flat studded chest bib is deleted. The neck's snow throat seg (rnd 0.45) now runs down to the chest front, and the two chest-ruff points sit on the chest. See `renders/crop_front_throat.png` and `low_below.png`.
- **NICE 1**: the pupil is centred on the iris (x 0.051, z 0.937).
- **NICE 4**: the waist underline is a further 0.01 higher (tuck end 0.560, waist bottom, snow strip).
- **NICE 3** (one saddle band): not done. The flush inlays follow the three torso block tops, which sit at different heights.
- Shares are unchanged: ICE 2.6 side / 2.2 game; rosettes 20.8 %.

## Round 4 (clip review 3, 2026-10-27)
- **M1, throat:** the snow throat seg is thinner (half-width 0.045, half-depth 0.040), with four SNOW fur tufts. Renders, newer than the source: `renders/crop_front_throat.png`, `crop_tq_throat.png`, `low_below.png`.
- **M2, claws:** one bone per front claw (`Claw_FL1-4`, `Claw_FR1-4`, children of `Claw_FL` / `Claw_FR`). The geometry is unchanged.
- **Ruff_L / Ruff_R:** the cheek-ruff hinges added for the roar (round 1 of the clips).
- Tris 6,404, 42 bones.

## Round 5: final 8.5 gate fixes (`_review/FrostfangLynx_final85.md`), 2026-10-28
- **M1, one dorsal band:** the three saddle inlays are gone. `dorsal_band()` lofts one studded BACK_SHADE Tube (half-width 0.050, ends tapered to 0.040) over the union of the rib, waist and hip tops, from the nape scruff to the tail root.
  - The top line is smoothed (a running max, then a mean) so the band bridges the small steps between the blocks as one line. The bottom is buried 0.034 deep.
  - It is split Chest / Spine with an overlap at y 0.016-0.032.
  - The nape scruff is narrowed (half-width 0.090 → 0.068) so it flows into the band.
  - See `renders/game_view.png`.
- **M2, paws:** the paw blocks and the hind foot segs are coat colour, with a thin SNOW sole plate (0.012 thick, smooth). The front socks are kept. Game SNOW is 3.8 % (was ~10 %).
- **M3, frost accent:**
  - the fangs are ICE (ICE_CLAW is retired);
  - the chest-ruff points and the throat tufts get ICE tips (the throat tufts keep soft, rounded tips);
  - the cheek ruff is 60 % ICE (was 45 %);
  - the elbow tufts get a small ICE tip;
  - there is no ICE added on the ears.
  - Result: **ICE is 3.5 % game / 4.7 % side** (was 2.2 % game).
- **Underside:** the flat snow under-chest slab is a rounded seg now, so there is no plank between the forelegs from the front.
- **T1, rosettes:** each rosette is a broken, irregular ring of 5 blobs around an open coat-coloured centre. A regular 6-blob ring read as a cog. One spot is dropped per flank block (rib, waist, hips). The rosette share stays **21.0 % of the side view**, with SPOT_K 1.24 and bigger ring blobs (debug render `_scratch/spots_debug_side2.png`).
- **T2, coat (lead ruling, the builder's pick): FROST-SILVER (168,176,188), with BACK_SHADE (100,106,122).**
  - The comparison renders are in `_scratch/coat/`: `_coat_strips128.png`, `_coat_strips64x2.png`, `_coat_game.png`, and the share JSONs.
  - **warm (190,172,150):** reads beige, as the reviewer said.
  - **sand (170,156,138):** reads as an ordinary forest / desert lynx. The cyan pops on it, but it does not say "frost".
  - **frost:** reads at once as a snow lynx at 64 and 128 px, and sits in the Glacier family next to the Ice Mammoth, Glacier Yeti and Permafrost Titan. It stays distinct from them: silver against their cyan, blue and violet. The cool slate rosettes are crisper on it than the warm spots were.
  - The fierce read comes from the face (black sockets, slit eyes, heavy V brows, ICE fangs), which is unchanged.
  - The brightest channel is 188 (rule ≥ ~170). The coat can be switched with `LYNX_COAT=warm|sand|frost`.
- **Shares, game:** coat 58.3, BACK_SHADE 29.5, SNOW 3.8, ICE 3.5, BLACK 4.0. Side: ICE 4.7, SNOW 6.4.
- **Tris 7,772** (cap 15k).

## Round 6: 8.5 gate round 2 (`_review/FrostfangLynx_final85_r2.md`; the model passed 8.5), TO 9+ items, 2026-10-28
- **T1, rosettes as rings:** 5 uneven blobs at radius 0.98-1.14 r (the open centre is bigger than before), filled with a lighter coat tone ROSE_C (204,210,222), which sits 0.0022 proud so the ring blobs (0.003) overlap it cleanly.
  - The uneven spacing (±14 deg) and sizes stop the regular 6-blob ring reading as a cog from the game camera.
  - The spot share is 21.3 % of the side view (`renders/_rosette_r2.png`, `_rosette_check.png`).
- **T2, chest:** the throat tufts are plain soft SNOW; only the outer chest-ruff pair keeps ICE tips.
- **T3, socks:** the front shin socks are 0.020 tall (was 0.035).
- **C1 model part:** the claws are 0.095 long with a 0.017 half-width. The base is at z 0.042, direction (0,-1,-0.42), so the rest tips stay at +0.005.
- **Shares, game:** coat 57.8, BACK_SHADE 29.3, SNOW 4.0, **ICE 4.0**. Side ICE 5.3. Tris 8,396.
