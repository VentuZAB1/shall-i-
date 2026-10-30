# Bramble Badger - model gate notes, round 2 (builder A, 2026-10-27)

File: `pets/BrambleBadger.py` (lead draft kept in `_scratch/BrambleBadger_v1_lead.py`). Answers `_review/BrambleBadger_review1.md`.
Tris 4,668. Size 0.52 W x 1.54 L x 0.58 H units; HEIGHT 6.5 studs = the thorn crest top. TH 0.23, PITCH 0.024.
Rig builds (27 bones, head pivot at the throat (0, -0.56, 0.34)).

## Review 1 items
- **M1 bands**: a new `edge_band()` hugs the skull's top-side edge, 0.07 wide on the top face and 0.08 down the side
  wall. It is rounded like the skull edge (rnd 0.45) and 0.003 proud. A second band runs down the snout to the nose.
  - The white centre is 0.17 at the back of the skull and ~0.12 at its front. BLACK is 6.3 % of the side.
  - FACE is (255,252,244). The cheek ruff is (0.05, 0.145, 0.06) at x 0.125, longer so the white runs back toward the
    ear.
  - Deviation: the band's outer edge is at x 0.153, not 0.13 or less. A band kept at 0.13 or less sits inside the
    skull wall and doesn't show from the side. The reviewer's hw / hd numbers were read as back / front widths; they
    are width and depth.
- **M2 palette**: done as given. AMBER_HOT stays.
- **M3 belly**: the grey / dark split is at z 0.30. The skirt rises from 0.22 (chest) to 0.26 (waist and rump), a tuck
  of 0.04. All of this is before N3 lowers the body 0.03.
- **M4 mantle**: covers only y -0.48..-0.26, 0.006 proud of the grey (a cape lip). The back edge is sloped
  (top_shift 0.035). A grey shoulder block and the grey spine start at -0.26. MANTLE is 14.4 % of the side, neck
  included.
- **M5 eyes**: the slit sits in the band near the front of the skull, about 33 deg forward. That is the wedge wall
  angle + 22 deg. Socket, slit, hot centre and brow are all rotated about the skull's up axis.
  - The skull is a stronger wedge (x taper 0.66) so the wall faces forward. The eye is at x about 0.11, on the band
    surface; x 0.100 is inside the head.
  - The draft yaw `s*10` turned the eyes 10 deg backward, and `s*35` would have turned them further back.
- **M6 snout**: done as given. The snout ends at -0.92, the nose at -0.935, the jaw at -0.88, the mouth at -0.80, the
  fangs at -0.865, and the growl anchor at -0.91.
- **M7 ear rims**: a flush 0.008-thick rim along the top of the ear's front face.
- **N1**: the front claws are 0.050. **N2**: the thorns are 0.058 or less (widened to 0.056 for the AMBER share).
  **N3**: the body is 0.03 lower (`DZ` + `LEGS`). **N4**: the tail stub is seated in the rump on the centre line,
  with a shorter band.
- **Extras**:
  - The legs are ~8 % slimmer.
  - A flush grey haunch block carries the body grey over the thigh top (BELLY_D 28 -> 25 %). A more proud version read
    as a knob and was removed.
  - The chin is white (FACE).
  - The anchors are renamed to the plan's names: FX_DirtPuff_FL/FR/BL/BR [Foot_*], FX_DustGrowl [Head, at the mouth],
    FX_LeafDust [Spine, at the crest].

## Value shares (side, flat palette) vs review 1 targets
| Colour | build | target |
|---|---|---|
| GREY | 37.8 | 35-40 |
| MANTLE | 14.4 | 11-14 |
| BELLY_D | **25.1** | 15-22 |
| FACE | **8.5** | 11-13 |
| AMBER (+HOT 0.2) | 5.4 | 6-7 (game view 12.6) |
| THORN_D | 1.3 | 2-3 |
| BLACK | 6.3 | 6-8 |
| IVORY | 0.6 | under 1 |
Light (GREY + FACE + IVORY) is 46.9 % and dark (MANTLE + BELLY_D + BLACK) is 45.8 %. Review 1 measured 24.7 / 69.8.

## Open
- **BELLY_D 25 %** is the stout legs (the plan: "short and stout"). The next levers are thinner legs (less stout) or a
  grey line lower than 0.30 (against M3). The reviewer should pick one.
- **FACE 8.5 %**: the bands cover the upper head sides. The white shows on the top centre, cheeks, snout and chin.

## Round 2 fixes (review 2, 2026-10-27)
Tris 4,956.
- **M-1**: the eye anchor is at `W-0.002` and the brow has no `+nrm*0.010` offset. Socket and brow now sit in the band; the slit stays proud.
- **N-1**: the head is 0.02 lower: skull, snout, nose, jaw, mouth, fangs, ears, the neck end, and the Head / Jaw / Ear / FX_DustGrowl joints + hinge.
- **N-2**: the cheek ruff is at z 0.352 with half z 0.070, and the chin half-width is 0.085. FACE went from 8.5 to 9.5 side.
- **N-3**: the haunch block is on `Spine`.
- **Evidence**: `renders/close_side.png`, `close_tq.png`, `close_front.png`, and the low camera `renders/low_below.png` (the underside is the dark skirt; nothing floats).
- **Shares, side**: GREY 37.7, MANTLE 14.1, BELLY_D 24.4, FACE 9.5, AMBER 5.5 (+0.2), THORN_D 1.3, BLACK 6.2. **Game**: GREY 54.0, BELLY_D 14.4, AMBER 12.8.

## Round 3: final 8.5 gate fixes (`_review/BrambleBadger_final85.md`), 2026-10-28
- **M1, hind thigh:** top (0.95, 0.95), rnd 0.45, and the thigh is narrower (half-width 0.072 → 0.060, depth 0.088 → 0.080) and starts 0.045 lower, under the body line. Rounding alone still left a corner poking out beside the now-flush haunch; with these changes nothing peaks above the skirt (`renders/_body_f85.png`).
- **M2, rump knob:** the haunch fur block has no x offset and a half-x of 0.050, so it sits flush with the rear block.
- **M3, back seams:** the rear block is top (0.95, 0.95) and rnd 0.50, so the back runs as one level line to the tail stub.
- **T1, flank band:** GREY_D (150,146,156), 0.035 tall (z 0.315-0.350), y -0.26..0.27, 0.003 proud, rounded and smooth, on both flanks. It sits between the grey back and the dark skirt. GREY_D is 4.1 % side / 2.1 % game.
- **T2, crest:** the middle five thorns are 0.072 and the two flanking ones 0.064; thorn width is 0.064. It reads as a bold amber crest, not a hedgehog (the thorns stay swept back, flat and few), so I kept the full step.
- **Shares, game:** GREY 50.4, MANTLE 9.4, BELLY_D 15.4, GREY_D 2.1, AMBER 14.7 (+0.5 AMBER_HOT). Tris 5,004.

## Round 4: 8.5 gate round 2 (`_review/BrambleBadger_final85_r2.md`), 2026-10-28
- **MM1:** the hind thigh half-width is 0.048 (was 0.060). No corner sits proud at the hip.
- **MM2 + T2 (a seam was left after MM2, so I merged the blocks):** the spine seg, the rear block and the back arch are now ONE grey body. `body_hull()` lofts a studded closed Tube of superellipse rings (top half exponent 3.5, lower half 6.0, so the flank stays full down to the skirt and the legs stay covered).
  - The top line `hull_top(y)` is 0.540 at the shoulders, rises to the old arch height 0.553 over the middle, and drops to 0.535 over the rump, which rounds off at y 0.40-0.465.
  - The thorns from y -0.15 back sit on the hull top (`hull_top - 0.006`); their rig joints follow.
  - There are no seams on the back or flank (`renders/_body_r2.png`, `_model_sheet.png`).
  - The DZ shift now moves Tube rings (the Lynx review 1 lesson).
- **T1:** the flank band is an open-arc strip that hugs the hull flank (0.003 proud), z 0.3085-0.3565 (half-height 0.024), y -0.25..0.38. GREY_D is 6.8 % side / 2.8 % game.
- **MM3:** `renders/low_below.png` is re-rendered from low front-left (camera z ≈ 0.15) and shows the belly, skirt and legs. Nothing floats.
- **Tris 6,832** (the hull rings). Game shares: GREY 48.6, MANTLE 9.5, BELLY_D 14.6, GREY_D 2.8, AMBER 16.4.


## Round 5: 8.5 gate round 3 (`_review/BrambleBadger_final85_r3.md`), 2026-10-28
- **T1, shoulder hump:**
  - The mantle centre z is 0.44 (was 0.42) and half z 0.135 (was 0.12), so it rises above the back line as a hump.
  - The first two THORNS are 0.035 higher (z 0.550 / 0.570) and sit on the nape and the hump.
  - The taller mantle first touched the head in act_burrow f5-68 (Head|Chest). Its top face now tapers to (0.86, 0.66) and is shifted 0.050 back (`top_shift`), so the hump's front slopes away from the dipping head. The badger is collision_free in every clip.
- **Shares:**
  - side: GREY 30.6, MANTLE 14.1, BELLY_D 22.9, GREY_D 6.4, FACE 9.2, AMBER 8.1;
  - game: GREY 48.0, MANTLE 10.2, BELLY_D 14.4, AMBER 16.9 (+0.4 AMBER_HOT).
- Tris 6,832; height 0.62.
- Evidence: `renders/_model_sheet.png`, `renders/_idle_close_r3.png`, `_scratch/r3/_neck_check.png`.


## Round 6: 8.5 gate round 4 (`_review/BrambleBadger_final85_r4.md`), 2026-10-28
- **N5, mantle rear edge:**
  - rnd 0.50 (blockkit caps it at 0.45 of the smallest half-size);
  - the mantle is tilted **-10 deg** (nose up, rear down: `MANTLE_TILT`), so its rear top edge rolls down toward the hull instead of standing as a wall;
  - centre y -0.364 (was -0.37), to keep the head clearance with the raised front.
  - Compared at 0 / -5 / -10 from the game camera; -10 softened the step most. `renders/game_view.png`, `_model_sheet.png`.
- **M2 clearance fix:** the FACE cheek ruffs are 0.018 shorter at the rear (centre y -0.649, half y 0.136; the front end is unchanged). The head vs mantle clearance is now >= 0.0105 in every clip (see CLIP_NOTES round 4).
- **Shares:**
  - side: GREY 30.4, MANTLE 14.5, BELLY_D 23.0, FACE 9.0, AMBER 8.3;
  - game: GREY 47.6, MANTLE 10.4, BELLY_D 14.4, AMBER 17.1 (+0.4 hot).
- Tris 6,544 (was 6,832, after the ruff + mantle changes); height 0.62.


## Round 7: 8.5 gate round 6 (`_review/BrambleBadger_final85_r6.md`), 2026-10-28
- **The nape slab is gone.** The neck is one dark BELLY_D column between the head and the cape (see CLIP_NOTES r6); thorn 1 sits on it (y -0.455, z 0.505).
- **Waist tuck:** 0.02 at y 0.08 (`hull_hx`), and the waist skirt follows it (`BADGER_WAIST` test switch).
- **Shares:**
  - side: GREY 30.3, MANTLE 10.3, BELLY_D 26.3, FACE 9.6, AMBER 8.3;
  - game: GREY 46.8, MANTLE 8.3, BELLY_D 15.6, AMBER 16.6 (+0.5 hot).
- Tris 6,356.
- Fresh model / icon renders: `renders/_model_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `game_view.png`, `low_below.png` (08:20).
