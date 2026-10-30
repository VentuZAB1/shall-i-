# Bramble Badger - model gate review 2 (2026-10-27) - APPROVED WITH FIXES (model)

**Score: 7/10** for a 40 % starter (ship target 8/10).

Round 1 was 6/10. Almost every item landed, and most landed as specified. The head now reads as a white badger face with black
edge bands, the palette is balanced, the belly has its tuck, and the mantle is a shoulder cape. One stuck-on part is left, and
it is a small, quick fix. Send one close-up after that fix, not a full round. Then the clip gate can start.

## What I looked at

- `BrambleBadger/MODEL_NOTES.md` (builder deviations), `BrambleBadger/renders/_shares.json`.
- Round-2 renders: `_model_sheet.png`, `_close_sheet.png`, `close_side.png`, `close_front.png`, `game_view.png`,
  `flat_side.png`, `flat_game.png`, `_icons_strip_64.png`, `_icons_strip_128.png`.
- Source: `pets/BrambleBadger.py` (209 lines), read in full.
- Comparisons: `ForestStag`, `VenomBasilisk` and `MossbackTortoise` model sheets, and `_ALL_FIERCE_progress.png` (round 1).
- Brief: `_review/GLACIER_REVIEWER_BRIEF.md`. Style: `Creature Style.md`, `Model Review Checklist.md`.

Units: HEIGHT is now 0.58 model units (6.5 studs, thorn-crest top). The body was lowered 0.03 (`DZ`).
Tris 4,668 (cap 15k).

## Review 1 items - status

| # | Item | Status | Evidence |
|---|---|---|---|
| M1 | Stripes thinned, white centre at least 0.12, FACE (255,252,244), bigger cheek ruff | MET, one deviation accepted | Bands hug the skull edge (`edge_band`, lines 56-65, 90-91). White centre 0.17 at the back, about 0.12 at the front. The band's outer edge is at x 0.153, not 0.13 (see accepted deviations). Cheek ruff line 108. |
| M2 | Palette: BELLY_D (104,88,80), MANTLE (136,130,146), AMBER (255,176,64), THORN_D (96,56,28) | MET | Lines 18-23. In game the belly is no longer near-black. |
| M3 | Grey/dark split at z 0.30, belly tuck 0.04 | MET | Skirt bottom 0.22 at the chest, 0.26 at the waist and rump (lines 79-81). |
| M4 | Mantle as a shoulder cape, sloped back edge, y -0.48 to -0.26 | MET | Lines 73-76. MANTLE 14.4 % of the side view. |
| M5 | Eyes forward in the band, slit, hot centre, brow | MET, yaw deviation accepted | Lines 92-106. Eyes ~33 deg forward on a stronger wedge. In the three-quarter close-up (`close_tq`) the slit reads well. |
| M6 | Snout shortened to -0.92, nose -0.935, jaw -0.88, mouth -0.80, fangs -0.865 | MET | Lines 86-88, 116-119. |
| M7 | Ear rims flush on the ear front face | MET | Lines 109-114: rim 0.004 thick, on the ear's front face. |
| N1 | Front claws 0.050 | MET | Line 160. |
| N2 | Thorns at or below 0.058 | MET | Lines 35-37, spike width 0.056. |
| N3 | Whole body 0.03 lower | PARTLY | `DZ` applied to the body group (lines 38, 134-139). The head top still sits about 0.03 above the back arch (see N-1). |
| N4 | Tail stub seated in the rump, shorter band | MET | Lines 132-133. Looks seated in `model_side`. |

## Deviations: accepted

1. **Stripe outer edge at x 0.153 (not 0.13).** The builder is right. A band at 0.13 sits inside the skull wall at the
   eye, so it never shows from the side. The band now hugs the skull's top edge and reads as the badger's band. The white
   centre is 0.17 at the back and about 0.12 at the front, which beats my number. Accepted.
2. **Eye yaw about 33 deg forward on a stronger wedge (not my s*35).** My yaw sign was wrong: `s*35` would have turned the
   eyes backward, as the builder says. In `close_tq` the slit faces the camera. Accepted.

## The pick: BELLY_D 25 % (side) - neither change

The builder offered two levers: thinner legs, or a grey/dark split below z 0.30.

**My pick: neither. Accept BELLY_D as built.** Reasons:

- **The brief judges game colours, not the side view.** In the game-camera palette (`_shares.json`, `game`) BELLY_D is 14.4 %,
  just under the 15 % floor. The side-view 25 % is inflated by the four legs seen in profile. The game camera does not show
  them that way.
- **Thinner legs cost the stout read.** The plan says "short and stout". The legs are already 8 % slimmer. A further cut turns
  the badger lean, closer to a dog or ferret.
- **A lower split removes the dark skirt, which is the badger read.** The real animal has a black belly and black legs over a
  grey back. Lowering the split below z 0.30 greys the belly, reverses the M3 tuck, and pushes the pet toward the "grey plastic
  toy" risk the owner has rejected before.

If the lead still wants the side-view number, pick thinner legs before the split. That is the lesser loss.

Other shares: GREY 37.8 (target 35-40), MANTLE 14.4 (11-14), BLACK 6.3 (6-8), IVORY 0.6 (under 1). FACE 8.5 is under
11-13 (see N-2). AMBER is 5.4 in the side view (target 6-7), but 12.6 in the game view, so the accent reads strong in game
colours. THORN_D 1.3 is under 2-3, but the bases are tiny. Both accepted.

---

## MUST (one item)

**M-1. The brow ridge and the eye socket stand off the skull side like stuck-on tiles.** (lines 95, 99-106)
- Built: the socket is centred at `W+0.010` (line 95), so its outer face is about 0.02 out from the skull wall. The brow is
  placed at `p + nrm*0.010` with a half thickness of 0.012 (line 105), so its outer face is about 0.03 out from the wall.
  `close_side.png` shows a grey tile sitting on the band, with a black box behind the amber slit. It reads as bolted on, which
  is the "stuck-on" look the Creature Style rejects.
- Direction:
  - Line 95: move the eye anchor from `W+0.010` to `W-0.002`. The socket's outer face then sits about 0.008 out, not 0.02.
  - Line 105: remove the `+ nrm*0.010` from the brow, so the brow centre sits on the wall. Its outer face then sits about
    0.010 out, not 0.03. Keep the heavy brow read.
  - The slit at `p + nrm*0.011` (line 101) stays as it is. It then sits about 0.013 out, proud of the band, so the eye still reads.
- Check: a close-up from the side and the three-quarter, showing the brow and the socket flush with the band.
- Do not change the eye yaw or the band widths.

---

## NICE

**N-1. Head still rides about 0.03 above the back arch.** Skull line 85 z 0.43 -> 0.41 (both ends). Snout line 86 z 0.392
and 0.366 -> 0.372 and 0.346 (on the snout, not the skull). Ear line 111 z 0.52 -> 0.50. Rig `Head` joint line 172 and `Jaw`
joint line 173: z -0.02 each. The bands and eye follow the skull, so they move too. Head top then sits level with the back arch.

**N-2. FACE 8.5 %, under the 11-13 target.** The white is already clear in the front view and at 64 px. A small lift is enough:
the cheek ruff (line 108) centre z 0.385 -> 0.370, half z 0.060 -> 0.070. That adds about two points. Optional: the chin
(line 116) radius 0.075 -> 0.085.

**N-3. Haunch block rides the hind leg.** Lines 152-153 put a GREY block on the `Leg_B*` bone. It will swing with the hind leg
in the walk and can poke out from the body. This does not matter at the model gate. Carry it to the clip gate: parent it to
`Spine`, or drop it to the rest pose and check `collision_free`.

**N-4. (Optional) The back is one flat grey.** From the game camera the back reads as one light tone, and the stud skin plus
the mantle cape are the only breaks. The plan calls for this, so it is not a fail. If the owner calls it a plastic toy, a
slightly darker flank band (for example GREY_D (150,146,156)) on the lower flank would add depth.

---

## Pass / fail checklist

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Reads as a badger at 64 px | PASS | Clear white face, black bands, grey body, amber row, dark legs. |
| 2 | Reads at 128 px | PASS | |
| 3 | Distinct from every Grass pet (Stag, Mossback, Treant, Basilisk, Mantis) | PASS | White face is unique in the Grass egg. |
| 4 | Fierce, not cute | PASS (after M-1) | Black bands, brow and amber slits read grumpy. Eyes are clear in three-quarter views. |
| 5 | Box belly / plastic slabs | PASS | Dark skirt tucks up 0.04 from chest to waist. |
| 6 | Palette follows the plan (inversion accepted) | PASS, with the accepted BELLY_D deviation | |
| 7 | Dark body / pale back / one accent (value shares) | PASS, with notes | GREY 37.8, MANTLE 14.4, BLACK 6.3. BELLY_D accepted. FACE 8.5 (N-2). |
| 8 | Accent strong enough in game colours | PASS | AMBER 12.6 % in the game view. |
| 9 | Proportions: head | PASS | Head 0.38 units after the snout cut, as I recommended. |
| 10 | Proportions: legs | PASS, with note | Ground-to-belly about 33 % of HEIGHT (plan 22 %). Reads stocky enough in `model_side`. |
| 11 | Floating, poking or intersecting parts | FAIL | M-1: brow and socket stand off the skull. |
| 12 | Parts visible from below | NOT CHECKED | Needs a low-camera render. Add to the next round. |
| 13 | Studs | PASS | Body, legs, white face and chin studded. Bands, eyes, thorns, claws and nose smooth. |
| 14 | Game colours | PASS | Belly not near-black. Face white reads (153,151,146). Amber reads. |
| 15 | Tris | PASS | 4,668 (cap 15k). |
| 16 | Collision and ground | NOT CHECKED | Clip gate. Watch N-3. |

## Next step

1. Builder applies M-1 (lines 95 and 105) and sends `close_side.png`, `close_front.png` and `close_tq.png`, plus one
   low-camera render (item 12). No full model round.
2. N-1 and N-2 are optional for this gate, but they are quick. Do them if they do not disturb M-1.
3. Once M-1 is confirmed, the badger is cleared for the clip gate. The haunch block (N-3) is carried into that gate.
