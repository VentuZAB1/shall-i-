# Wraith Hound - model gate notes (builder A, 2026-10-27)

File: `pets/WraithHound.py` (new; built on the Raiju / ShadePanther kit).
Tris 6,820. Size 0.45 W x 2.37 L (tail included) x 1.26 H units; HEIGHT 8.0 studs = the mane top (the ear tips are
~1.25). TH 0.43, PITCH 0.034. Rig builds (42 bones, head pivot at the throat (0, -0.76, 0.95)).

## What I built
- **Body**: a lean deep-chested hound. Ribcage with a bottom taper, sloped tuck, narrow waist, hips; long legs with
  rounded upper blocks, slim lower legs and narrow paws with 4 black claws.
  - Lavender-ash studded hide (170,160,206).
  - MIST: muzzle, jowls, throat, chest front, belly layer, tuck strip, and mist socks + paws (ghost mist pooling at the
    feet).
- **Saddle**: `upper()` cuts the top layer off each torso block (chest, waist, hips) and grows it 0.006, so the soot
  follows the body shape with a clean fur line along the flank instead of a plate on top. The split is ~0.09 below
  each block's centre.
  - **Saddle alone = 18.8 % of the side view**, measured with the `WH_SADDLEDBG=1` debug colour (18.9 % in the game
    view).
  - A version with soot caps carried over the shoulders and haunches reached 21.4 %, but the caps read as dark
    pauldrons from the front. Kept in `_scratch/WraithHound_legcaps.py`.
- **Mane**: 3 rows (Mane1 [Neck] at the nape, Mane2 [Chest] at the withers and tallest, Mane3 [Spine] on the back)
  plus a soot ridge along the neck.
  - Each row: a tall centre wisp and a back wisp on the row bone, and a side wisp and an outer-low wisp on each of
    `ManeN_L` / `ManeN_R` (for the cloak fan-out).
  - A wisp is a fat rounded soot root rising steeply and bending back into a tapering tail that ends in an indigo
    point (smooth). The tails lie over the next row's roots, so the crest reads as one streaming mass. Blocks only.
- **Head**: a long flat wedge. Dark crown, lean cheeks, long snout, mist muzzle fitted to the snout taper, black nose,
  ivory fangs, mist jaw.
  - Eyes: black socket, rim, hot blue slit tilted 18 deg, under a heavy soot V brow. (A small black pupil block exists in the code, but it does not show in any render; it is not claimed as a feature.)
  - Tall soot ears with lavender fronts, pinned back 12 deg.
- **Tail**: long and low, 4 segments (a lavender root and 3 soot), bushiest mid-tail, with a soft rounded soot tuft.

## Value shares (flat palette)
| | side | tq | game |
|---|---|---|---|
| ASH_LAV | 32.3 | 35.2 | 24.8 |
| SOOT (saddle 18.8 side) | 48.7 | 40.2 | 57.8 |
| MIST | 9.8 | 16.0 | 5.6 |
| INDIGO | 4.1 | 3.3 | 7.3 |
| BLACK | 3.0 | 3.3 | 2.6 |
INDIGO_L (the eye rims) is too thin to register at 400 px; it shows in the close-ups. MOUTH ~2 % is anti-alias edge
pixels.

## Deviations from the plan
- **SOOT is 48.7 % and ASH_LAV 32.3 % of the side** (plan 26 / 40). The plan's shares can't hold a saddle of 18 % or
  more (review MUST 2) plus a mane that reaches 1.0H, ears and a 0.70H soot-tipped tail. The MUST wins. The body still
  reads lavender: head, neck, lower flanks and legs.
- **The mane is swept wisps** (soot root, indigo point), not round puffs. Round puff columns read as bony fingers, then
  as caterpillar hooks.
- **Mist socks and mist paws** were added to bring MIST toward 12 %. The plan only says "inside legs", which a side
  camera can't see.
- **Proportions**: withers ~0.72H, ground to elbow ~0.33H, body ~1.1 units (~0.87H). The plan's numbers (withers 0.56H,
  elbow 0.42H, chest 0.34H) can't all hold at once; I kept a believable lean hound with the mane as the top.
- VFX anchors: FX_SmokeWisp_1..3 [Mane1..3, at the centre wisp tips], FX_IndigoWisp_L/R [Head, at the eyes; no Eye
  bones], FX_SmokePuff_FL/FR [Foot_F*], FX_SmokeTrail [Tail4], FX_Fog [Chest].
- The env switches `WH_NOMANE` and `WH_SADDLEDBG` exist only for share tests.

## Round 2 (review 1 fixes, 2026-10-27)
Tris 6,820. HEIGHT 8.5 (NICE 6). The top is the ear tips now that the mane streams back.
- **M0 waiver**: the saddle is 10-14 %. Measured with `WH_SADDLEDBG`: **11.7 % side**, 14.0 % game, 6.8 % tq.
- **M1**: `upper()` cuts at 0.043 / 0.024 / 0.030 (rib, waist, hips), so the soot is the top ~40 % of each block.
- **M2**: Tail1 and Tail2 are lavender; Tail3 and the tuft are soot.
- **M3**: the wisp d0 vectors are now centre (0, 0.85, 0.55), back (0, 0.95, 0.42) and side (s 0.55, 0.85, 0.60). The mane streams back as a plume (~33 deg).
- **M4**: INDIGO is (112,120,240) and INDIGO_L (176,184,255).
- **NICE**:
  - the front sock covers 18 % of the shin;
  - the chest plate half-width is 0.090;
  - the upper muzzle is ASH_LAV (MIST only on the jaw and jowls);
  - the fangs are 0.075 long;
  - the eyes are bigger (slit 0.038 x 0.012, rim 0.043 x 0.014, socket 0.048 x 0.020);
  - the waist centre is at z 0.775;
  - the under-view is `renders/low_below.png`.
- **Shares** against the review gates (SOOT 38 % or less, ASH + MIST 48 % or more):

| | side | tq | game |
|---|---|---|---|
| ASH_LAV | 46.5 | 47.0 | 37.4 |
| MIST | 8.4 | 12.7 | 5.3 |
| SOOT | 35.5 | 31.2 | 45.2 |
| INDIGO | 4.4 | 3.5 | 7.2 |

ASH + MIST is 54.9 side.

## Round 3 (review 2 fixes, 2026-10-27)
- **MUST 1**: the wisp tail lengths are centre 0.36·sc, back 0.28·sc and side 0.28·sc. The rows overlap into one swept plume; see `renders/crop_mane_side.png`, `crop_mane_front.png` and `_icons_strip_128.png`.
- **MUST 2**: HEIGHT 9.0 (ties NightmareStallion) and the comment is fixed. ground_min_z is checked at the clip gate.
- **NICE**:
  - the chest plate is rnd 0.50 and the tuck strip rnd 0.45;
  - the eye slit is 0.042 wide, the rim 0.047, the socket 0.052, and INDIGO_L is brighter (200,206,255);
  - the jowls are 20 % smaller.
- **Saddle**: 11.3 % side / 12.6 % game / 6.1 % tq. The debug renders are `renders/saddle_debug_side.png` and `saddle_debug_game.png` (magenta = saddle), and the numbers are in `_scratch/saddle_share.txt`.
- **Shares, side**: ASH_LAV 45.2, MIST 7.9, SOOT 36.4, INDIGO 5.4, BLACK 2.8. ASH + MIST is 53.1.

## Round 4 (clip review 3 model items, 2026-10-27)
- **M2, one plume:** the Mane2 and Mane3 roots are +0.03. The side wisps rise more steeply (d1 z 0.42, L0 0.19·sc). The back wisp and outer-low wisp tips are SOOT. Renders: `renders/crop_mane_side.png`, `crop_mane_front.png`, `_icons_strip_128.png`.
- **NICE 3:** the side wisp rest splay is d0 x 0.55 → 0.40, so there are no "wings" from the front.
- **NICE 5:** the chest plate half-depth is 0.046 and the belly tuck strip 0.042 (`low_below.png`).
- **Shares, side:** ASH_LAV 44.4, MIST 8.3, SOOT 38.7, INDIGO 3.5 (game 6.1), BLACK 2.8. Tris 6,820.
- **Saddle share denominator** (asked for in review 3): `_scratch/saddle_share.py` counts the magenta pixels of the flat (unlit, flat-colour) render `renders/flat_<view>.png` from `WH_SADDLEDBG=1`. It divides them by all non-background pixels of that render, where the background is near-black (max channel < 6). The saddle is unchanged since round 3 (11.3 % side / 12.6 % game).

## Round 5: final 8.5 gate fixes (`_review/WraithHound_final85.md`), 2026-10-28
- **M1, ghost read (a deviation from the plan's soot mane):** the mane roots and middles are WISP_ROOT (128,124,166), a mid-slate. The tips stay SOOT or INDIGO, and the outer-low wisps stay all SOOT.
  - The mane now reads as smoke rising off a lavender back, not as a solid soot crest that swallowed the ghost read (game SOOT was 47.7 %).
  - Tail1-3 are lavender, with the soot tuft on Tail4 only. Tail4's back overlap is shortened (ext 0.015) so the soot no longer pokes through Tail3.
  - **Game: SOOT 27.1 % (≤ 40), ASH_LAV 41.1 % (≥ 40)**, WISP_ROOT 17.0.
- **M2, one plume:** only Mane2's centre wisp keeps an indigo point, and its tail is 0.44 · sc (was 0.36). The Mane1 / Mane3 centre points are soot.
- **M3, eyes at 64 px:** the slit is 0.018 tall (was 0.012) and the rim 0.020 (was 0.014). The socket is unchanged.
- **TO 9+ #2:** the chest plate is ASH_LAV (no white bib), narrowed to 0.075. The MIST throat and belly strip are kept.
- **TO 9+ #1 (Mane1 / Mane3 side tips soot): NOT done.**
  - After M2 the game INDIGO was 4.7 %, under the 5 % floor, and soot side tips would cut it further.
  - Instead the indigo tips are longer (the tip segment is 50 % of the wisp tail on indigo-tipped wisps).
  - **Game INDIGO is 5.2 %.**
  - From the side the blue reads as one swept band (`renders/crop_mane_side.png`).
- **Shares, side:** ASH_LAV 47.0, MIST 7.0, SOOT 23.8, WISP_ROOT 14.2, INDIGO 3.1. Tris 6,820.

## Round 6: 8.5 gate round 2 (`_review/WraithHound_final85_r2.md`; the clips passed 8.5), 2026-10-28
- **M1:** the indigo tips are fatter (tip-width factor 0.85, was 0.62) and longer (0.58 of the wisp tail).
- **M2:** the eye sockets are 0.028 tall (was 0.020); the width is unchanged, so nothing pokes out.
- **TO 9+, all done:**
  - the saddle `upper()` calls use rnd_t 0.45, for rounder tops in the game view;
  - the Mane1 / Mane3 side tips are SOOT, so the only blue is Mane2 (centre + sides): one line;
  - the MIST throat strip is rounded (rnd 0.45, slight taper), so there is no bib from the front;
  - the cloak rows are staggered (lift 6 / 4 / 2 deg).
- **Accent check:** game INDIGO is **5.3 %** (≥ 5) with the soot side tips. ASH_LAV 41.1, SOOT 28.4, WISP_ROOT 15.5. Side INDIGO 3.1. Tris 6,820.
- Renders: `_icons_strip_64.png`, `_icons_strip_128.png`, `game_view.png`, `crop_mane_side.png`, `crop_mane_front.png`, `_fan_front_back_r2.png`.

## Round 7: 9+ polish after the pass (`_review/WraithHound_final85_r3.md`, model 8.5 / clips 8.5), 2026-10-28
- **Eye at icon size:** the slit is 0.022 tall (was 0.018) and the rim 0.024. The socket stays 0.028.
- **Accent:** the Mane2 side tips are fatter (tip width 1.0); the centre tip stays at 0.85. The blue is still one line on Mane2 only. **Game INDIGO is 5.9 %** (was 5.3).
- **ASH_LAV (158,148,198), kept.** Compared against (170,160,206) in `_scratch/lav/_lav_compare.png` (game view, 128 and 64 px). It still reads clearly lavender, with a little more definition against the white socks and the indigo. Game ASH_LAV is 40.7 % (≥ 40). Brightest channel 198.
- The backup before this round is `_scratch/WraithHound_pass85.py`. Tris 6,820, unchanged.


## Round 8: 9+ round (`_review/WraithHound_final85_r4.md`; model and clips already pass 8.5), 2026-10-28
Measured on `renders/_icons_strip_64.png` / `_128.png` with `_scratch/iconmeasure.py`. "Indigo" = b - r > 70 and b > 120, which reproduces round 4's counts on the 01:47 strips (3 / 13).
- **1. Eye at 64 px:**
  - the slit is a saturated hot blue, EYE_HOT (70,90,255);
  - the rim INDIGO_L is (110,125,255), saturated (was (200,206,255), which the icon light washed to white);
  - slit 0.046 x 0.025, rim 0.049 x 0.027, socket 0.050 x 0.030, all grown downward by 0.002 so the brow keeps the top.
  - Eye box (strip x 16-30, y 24-36): **7 indigo px at 64 px** (was 3; target >= 6) and **21 at 128 px** (was 13; target >= 16).
  - A first try with a brighter, paler (150,160,255) fill counted 3 / 8: the icon lighting whitens it. Saturation, not brightness, is what survives.
- **2. Icon luminance:**
  - ASH_LAV is (122,112,164) (was 158,148,198);
  - MIST is (200,200,218) (was 226,226,236);
  - WISP_ROOT is (102,98,138), so it stays below the body.
  - Wraith icon cell mean Y drops by **7.3** (90.6 -> 83.3 on my cell metric, which reads 7.3 below round 4's for the same strip). That is about **97.9 -> 90.6 on round 4's scale**, below the white-gold sphinx (slot 5).
  - Game shares: ASH_LAV **41.3 %** (floor 40), SOOT 28.3, WISP_ROOT 14.8, INDIGO 5.2.
  - The game view still reads lavender, a deeper dusk lavender (`_scratch/_game_cmp_r8.png`: new left, pass85 right).
- **Front crest:** with tip width 1.0, the Mane2 side tips read as two chunky blue blocks flanking the crest in `model_front.png`. Per the coordinator, Mane2 `tipw` is back to 0.85.
  - Whole-icon indigo is 67 px at 64 / 248 at 128.
- Skipped on purpose: splitting the Mane2 tips (the risk of front "wings"). I also dropped the pupil claim from these notes.
- Tris 6,820. Evidence: `renders/close_front.png`, `_close_sheet.png`, `_model_sheet.png`, `game_view.png`, `_icons_strip_64.png` / `_128.png`.


## Round 9 (`_review/WraithHound_final85_r5.md`: model 8.5, clips 8.7), 2026-10-28
- **Eye socket regression:** the black socket is half-x **0.054** (r8 had 0.050). The close-up shows the black frame round the blue rim again (`renders/close_front.png`).
  - Eye box: **6 indigo px at 64 px** (floor 6) and **21 at 128** (floor 16).
  - collision_free true; tris 6,820.
- No colour change while the owner looks at `_scratch/_game_cmp_r8.png`.
