# Abyss Weaver v1 - builder report for the MODEL GATE (2026-10-14)

Spec: `pets/AbyssWeaver.py` (model + rig + anchors + check_pairs + joints + a v0 idle STUB holding rest with all 8 legs
planted, so headless_pack measures at idle f0). Built to `_review/AbyssWeaver_plan_review.md`; structure from your mock,
every number from the brief. Clips come after this gate (brief section 6, references first).

## Numbers
- tris **11,852** (<= 12k): ceph 672 · head (turret, 8 eyes, brows, crown, gem) 1,276 · face (chelicerae, fangs, palps)
  1,400 · abdomen (hull, plates, band, spines, rift, settings, spinnerets) 4,504 · legs 4,000
- H **1.10** (pair-2 knee-thorn tips) · bounds x +-1.06, y -1.148 .. +1.24, z -0.005 .. 1.10 · pitch 0.0308 · TH 0.26
- lowest -0.005 (claw tips) · idle f0 `collision_free: true` (all section 5.5 pairs + 5.6 capsules)

## Checklist evidence (brief section 8)
| item | evidence |
|---|---|
| 1 silhouette | `_model_sheet_600.png` (bind = rest: tq / front / back / side / game), `_model_tq_600.png` |
| 2 front | same sheet + `_face_close.png` |
| 3 game camera | sheet game view; `_rift_close.png` game |
| 4 64 px strip | `_icons2_strip_64.png` / `_128.png` = [portrait icon, GAME-CAM icon, ShadePanther, NightmareStallion, BlackDragon, PharaohAsparuh, ThornbladeMantis, Kraken]; also `_icons_strip_64/128.png` (portrait only) |
| 4 gold px @64 | **44 portrait / 68 game** (HSV hue 0.08-0.16, s > .5, v > .45; `_tools/game_icon.py`). Your mock F scores 49 / 62 with the same count (W/B/C: 49-53 / 67-75), so my counter is not your counter; same-method the build is within 5 of the mock |
| 5 cute traps | sheet + face close |
| 6 A/B | `_AB_ThornbladeMantis_64/128.png`, `_AB_Kraken_64/128.png` |
| 7 shares | `_shares.txt` (table below), `_flat_sheet.png` |
| 8 face close (700 px) | `_face_close.png` front / side / tq. The pure side is blocked by legs 1-2 (unavoidable on a spider); the "side" here is (1, -0.55, 0.3) and still mostly leg |
| 9 rift close-up | `_rift_close.png` tq / game / top (700 px) |
| 12 rig limits | `_limits_sheet.png` (tq + game): **0 hits on all 6** (table below) |

## Shares (flat palette-ID, idle f0) vs section 2.3
| view | ARMOR | ARMOR_D | dark | VELVET | SILK | glow | GOLD | BLACK |
|---|---|---|---|---|---|---|---|---|
| side | 27.9 ok | 36.4 ok | 64.3 ok | 21.6 ok | 3.5 ok | 1.7 ok | 4.1 ok | 4.8 ok |
| tq | 25.9 ok | 44.3 ok | **70.2** (<= 70) | 12.3 ok | **0.9** (1-3) | 3.6 ok | 6.9 ok | **5.2** (<= 5) |
| game | 39.9 ok | 31.9 ok | 71.8 ok | 9.0 ok | 0.9 ok | 5.0 ok | 9.0 ok | 4.3 ok |
| front | 23.7 ok | 44.1 ok | 67.8 ok | 14.5 ok | 0.6 ok | 3.3 ok | 7.3 ok | 5.7 ok |
No role > 45 % (top 44.3). Three tq misses by <= 0.2. BLACK includes anti-aliased edges against the flat render's black
background (same method as your mock numbers).

## Limit poses (static, step 1, section 5.5 pairs + 5.6 capsules) - all 0 hits, lowest -0.005 (claws)
| pose | keys |
|---|---|
| L1 rest | - |
| L2 roar peak (6.3 f22) | Spine -14 nose-up, Root z +0.06, Pedicel +6, Abd +8; legs 3-4 planted; leg 1 FK fem +15 / shin +80 / foot +20, leg 2 FK +5 / +40 / +10 (about the leg-plane axis, see W4); Chel yaw out 12 pitch -18; Fang unfold 65; palps spread 28, **pitch +5** (W4). Ankles: leg 1 **(0.978, -1.437, 1.223)**, leg 2 (1.404, -0.73, 0.664) |
| L3 act PRESENT + L4 draw (6.4 f34) | Root z +0.06, Spine -6, Pedicel -4, Abd -8; L4 ankle at **(1.02, 0.70, 0.45)** exactly (raised-ankle helper, toe +30); the other 7 legs planted |
| L4 act CAST peak | Abd +10, Pedicel +2, Spine +2, Root y +0.03 z +0.06, Fang unfold 35; all planted |
| L5 Spine yaw +10 | all planted |
| L6 Head yaw 10 + pitch 8 | all planted |

## Deviations / decisions (please approve or overrule)
- **W1 tri trims:** rift layers and lips at N = **14** (your minimum; 18 put the build at 12.6k); the GOLD_D lip inner
  strips at half resolution (7 per side, they are thin and flat). Blocks under a 0.004 bevel stay 12 tris.
- **W2 every small part `surf_hit`-seated:** the fovea + 6 radial grooves on the carapace tube, all 8 eyes on the turret /
  clypeus. The E3 top-side eyes land at the turret side surface x ~0.10 (at z 0.645 the turret's 0.80 top taper puts its
  side at 0.10, so your mock's x 0.122 floated ~0.02 off it).
- **W3 main eyes:** ThunderRex `fierce_eye` at sc 0.9 / yaw 18 / tilt 20, recoloured; the pupil half-height is
  0.0095 x sc (= 70 % of the lens, the recipe's was 100 %); the brow sits at +0.036 x sc (was 0.044) so it lids the top
  ~30 % and the two brows meet in a V at the midline.
- **W4 roar FK sign + palps:** your values only work with fem + = leaning OUT (right-hand about t) and shin / foot + =
  OPENING the knee (left-hand about t): that reading puts the ankles exactly where the brief says (z ~1.2 in front of and
  outside the face; leg 2 ~0.65). The other three readings fold the shin under the body or raise the ankle to 1.75.
  With palps pitch -15 the palp roots cut the leg-1 femurs (16-17 tri pairs, rest-space x 0.14-0.21, y -0.68..-0.52,
  z 0.29-0.42); palps **pitch +5** (spread still 28 >= Chel + 12) is 0. Clip-phase helper: `leg_raise(i, side, fem,
  shin, foot)` = key_axis(t, +fem) / (t, -shin) / (t, -foot), R mirrored.
- **W5 shares:** all plate gaps at 0.04 (P1 0.05-0.16, P2 0.20-0.40, P3 0.44-0.64, P4 0.68-0.99); belly band alpha
  200-340 (was 205-335 in the brief); knee-thorn ORCHID width 0.019 -> 0.022.
- **W6 my own calls where the brief was silent:** the 2 small inner spinnerets at the big pair's base + (-s 0.02, -0.01,
  -0.03) along (+-0.12, 0.85, -0.5), L 0.06 w 0.022, SILK tips; the circlet GOLD_D inner strips as thin bars on the 4
  inner faces; the `Rift` anchor at the hull top u 0.47 lifted 0.02 (tail = the surface normal); the sternum is SILK
  (mock had SILK_D).
- **Q1 for you, the rift read:** from the top (and partly the game cam) the almond lip frame with the thin HOT seam could
  read as a cat's eye with a slit pupil. The seam is per your table (0.12 w, <= 0.018). If you see it, say whether to drop
  the seam, break the lip frame at the ends, or keep.

## Tools added this round
`_tools/game_raw.py` (idle f0 from the game camera, transparent) + `_tools/game_icon.py` (game-cam icon, 2-icon strip,
gold px count); `pose_try` now takes `plant=Leg3_L,...` (only those legs, 8-leg specs via `plant8`) and
`ankle=Leg4_L:x,y,z[:toe]` (the raised-ankle helper); `headless_closeup` takes custom views + an output prefix.
