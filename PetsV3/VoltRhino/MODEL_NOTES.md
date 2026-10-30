# Volt Rhino - model notes (model gate, 2026-10-27)

File: `pets/VoltRhino.py` (model + rig + check_pairs, no clips yet).
Tris: 10,348. Size (Blender units) 0.88 x 3.15 x 1.57. HEIGHT 8.5 studs = bbox top (withers shield). PITCH 0.0414
(same world stud size as the Raiju).

## What I built
- Armoured Indian-style rhino. Body = one smooth `curveloft` barrel (split Chest | Spine) whose belly line rises
  0.62 -> 0.77 (no box belly).
- Dark iron armour laid over it as raised shells:
  - a shoulder shield (proud, overlaps the saddle);
  - a narrow saddle along the spine;
  - a rump plate.
- Two heavy fold rims cross the flanks (behind the shield, in front of the thigh).
- Lofted head held low, with a dark nasal ridge + nose plate over the muzzle.
- HERO: one big ivory horn (3 tapered segments, sweeping forward-up and curving upward; tip above the nose at
  z 1.43) with a volt-lime lightning zigzag down BOTH sides. A small ivory brow nub behind it.
- Volt bolts on both shoulder shields. Lime slit eyes (black socket, small lime-white hot centre) set side-front,
  front end low, under heavy dark brows.
- Cupped tube ears, pillar legs with dark elbow/knee folds, dark round foot pads with 3 black toenails, a short
  tail with a dark 4-spike tuft.
- Bones for VFX anchors: `Horn_Base`, `Horn_Tip`, `Shoulder_L/R`, `Mouth`, `Foot_FL`.

## Value shares (flat palette IDs, %)
| | IRON_D | IRON | PALE | HORN_IVORY | VOLT | BLACK |
|---|---|---|---|---|---|---|
| side | 45.9 | 40.2 | 5.1 | 3.0 | 2.4 | 2.4 |
| tq | 48.6 | 37.6 | 1.8 | 4.8 | 2.6 | 3.7 |
| game | 68.9 | 23.4 | 0.2 | 3.1 | 1.5 | 1.9 |

The plan's IRON_D >= 25 % gate passes (45.9 % side). In the game camera the back is darkest and the horn is the
brightest part.

## Deviations from the plan (and why)
- **HEIGHT**: 8.5 = the withers. The plan says "top of the lightning horn", but the plan's own proportions
  (horn 0.32H from the nose, head top 0.55H) can't reach H. The horn tip sits at 0.91 of the height.
- **Horn length**: 0.77 model units = 0.49H (plan 0.32H). Bigger so the High-tier hero reads at 64 px.
- **Palette**: tiny cool tint, IRON (172,178,190) / IRON_D (100,108,122). The plan has (176,180,186) / (104,110,120).
  Brightest channel stays >= 170. The tint keeps it out of "flat grey plastic" and ties it to the storm egg.
  Everything else is the plan's palette, plus EYE_HOT (238,255,168) for the small eye centre.
- **PALE**: 5 % side (plan 10 %). The belly strip follows the rising underside. A bigger pale area read as a white
  bib.
- **Body build**: lofted barrel + raised band shells instead of tapered boxes. The first box version read as
  stacked boxes with steps. The legs, head details, horn and tail are still blocks.
- **Act feasibility (for the clip gate)**: the horn tip is 1.23 from the throat pivot, 25 deg above horizontal.
  A 25 deg head pitch can't reach the snow. The horn tap will add a front-leg crouch + spine pitch, with the
  head pitch under the limits. I'll report the exact numbers at the clip gate.

## Self-critique
- The face reads as a rhino (no pig snout: nostrils on the sides, dark nose plate on the front).
- It is the lightest Thunder pet in the strip. That's intended: the plan wants grey, not blue.
- The rhino is simpler than the Wyvern; the horn + lime bolt is the High-tier signature.

## Round 2 (review 1 fixes, 2026-10-27)
Tris 12,452. Height unchanged (8.5 studs = withers, 1.57 units).

**MUST fixes**
- M1 palette: IRON (156,164,178), IRON_D (92,100,116).
- M2: the fold hoops are now tapered wedges. They run from the spine (proud 0.030) to a point at the belly line and
  ride on top of the armour.
- M3: every armour lower edge slopes (narrow1).
  - Shield: -0.26 front -> -0.12 rear.
  - Saddle: 0.34 front -> 0.22 rear.
  - Rump: -0.30 front -> -0.02 rear.
- M4: pale underside 8.1 % side.
  - The plain zhi -0.46 only gave 4.6-5.6 %. The side camera sits above the belly.
  - So the band tops are now at -0.24, with pointed tapered ends at the chest and rump.
  - Added a pale throat (neck underside), and the lower jaw is now PALE (Raiju-style).
  - The separate flat chin board was removed: it read as a white plate from below.
- M5: ears are dark IRON_D flaps with a black inner, 0.20 long, root z 1.18.
- M6: the horn is now ONE smooth superellipse tube (flat-ish sides), so there are no segment steps.
  - A HORN_SHADE root collar plus 2 thin growth rings (NICE).
  - HORN_IVORY (232,224,204).
  - Lime zig 0.060 wide x 0.013 thick, narrowed to the horn depth near the tip so it never fins out.
- M7: rump bolts (0.068 wide). Eye slits are (0.008, 0.018, 0.080) at a 22 deg tilt. VOLT is 3.6 % side, 3.2 % game.
- M8: nasal ridge grow 0.012. Brow is (0.040, 0.026, 0.096), moved 0.008 into the skull.

**NICE fixes:** VOLT (190,255,64); horn growth rings; IRON_D shin gaiters on the front legs.

**Value shares (%)**

| view | IRON_D | IRON | PALE | HORN_IVORY + HORN_SHADE | VOLT |
|---|---|---|---|---|---|
| side | 45.8 | 35.8 | 8.1 | 1.6 + 1.8 | 3.6 |
| game | 67.6 | 22.4 | 0.8 | 1.8 + 1.4 | 3.2 |

**Deliverables:** `_model_sheet.png`, `_close_sheet.png`, `_horn_sheet.png` (horn base and joints), `under.png`
(underside), `model_game.png` (600 px game camera), `flat_side`, `flat_tq`, `flat_game`, and the
`_icons_strip_64/128.png` strips (Volt first, then ThunderBull, Raiju, Thunderbird, ThunderRex).

## Round 3 (2026-10-27, after the round-2 verdict)
All round-2 MUST and NICE fixes are applied, plus the small mesh changes the clips needed. The list is in `CLIP_NOTES.md` under "Changes made for the clips". Fresh sheets: `renders/_model_sheet.png`, `renders/_close_sheet.png`, `renders/_icons_strip_64.png` / `_128.png`.

## Final 8.5 gate round (2026-10-28, `_review/VoltRhino_final85.md`)
Pet file: `pets/VoltRhino.py` 01:35. Pre-round backup: `_scratch/VoltRhino_r4_export.py`.
- **M2 back seams:** the rear fold (y 0.405) is gone; the fold wedge is 0.030 -> 0.014 thick. The back shows the shield
  edge and one fold; the saddle / rump plate edge is the only other line (`model_game`, `model_side`).
- **M3 chin:** the pale jaw is 0.14 / 0.055 -> 0.10 / 0.040 and 0.015 lower, so from below it reads as a thin pale strip
  running on from the throat, not a slab (`renders/_chin_sheet.png`). Found while checking: the MOUTH lip line (half width
  0.142) poked out as red dots at the snout corners once the chin narrowed; it is now 0.100, tapering to 0.08.
- **M4 eyes:** VOLT slit (0.009, 0.026, 0.092), BLACK socket (0.011, 0.040, 0.100) (`_close_sheet.png`).
- **M5 legs:** the numeric ask (hock 0.13 -> 0.105, pad 0.055 tall, rnd 0.60) was applied first, but the legs still read
  as stacked boxes, and rnd above 0.45 does nothing (`blockkit._resolve` caps edge rounding at 0.45 x the smallest half
  size). So every leg segment is now a studded superellipse loft (`ltube`, n 2.4, 20 segments) with the old blocks'
  extents: thigh, shin and the back hock (0.125 -> 0.105, flowing from the shin, no ledge). The pads are round pucks
  0.11 tall (`PAD`, was a 0.15 box). The elbow / knee fold wedges are shorter fore-aft (+-0.07) to sit on the round leg.
- **N1 / N2:** IRON_D (76, 84, 102), IRON (146, 154, 168).
- **T1 ridge:** three IRON_D spikes on the spine over the saddle (y -0.10 / 0.12 / 0.30, 0.10 / 0.11 / 0.09 tall, raked
  back, blunt tips, nostud). They are now the top of the model: bbox 1.5661 -> 1.6014. So HEIGHT 8.5 -> 8.69 and H_MODEL
  1.57 -> 1.605 (same ratio, PITCH 0.0414 unchanged): the withers stay at 8.5 studs and the body's world size is
  unchanged in game.
- **T2:** one volt bolt on each upper side of the saddle (the rump bolts' zig, width 0.068), seen by the game camera.
- **Numbers:** tris 14,572 (was 12,328; the leg lofts + ridge + bolts; cap 15k). Flat shares side / tq / game: IRON_D
  43.4 / 46.2 / 65.0 (gate >= 25 % side), IRON 36.8 / 36.7 / 23.0, PALE 8.3 / 2.3 / 0.9, VOLT 4.6 / 4.6 / 5.1.
- **M1 renders (01:33-01:37, from the 01:35 file; title bars carry the times):** `renders/_model_sheet.png` (tq, front,
  side, back, game 600 px, under), `_close_sheet.png`, `_chin_sheet.png`, `_flat_sheet.png` (`flat_side/tq/game.png`),
  `_icons_strip_64/128.png` (Volt, ThunderBull, Raiju, Thunderbird, ThunderRex, StormWyvern), `VoltRhino_icon.png`
  regenerated from the new `VoltRhino_portrait_raw.png`.

## Final gate round 2 (2026-10-28, `_review/VoltRhino_final85_r2.md`)
Pet file 04:06; backup of round 1 `_scratch/VoltRhino_f85r1.py`. Renders 04:07-04:09 (title bars carry the times);
export 04:09:10, portrait raw 04:09:11, icon + strips 04:09:13 (made from that final portrait, MM4).
- **MM1:** rump tuple `(0.40, 0.93, "Spine", 0.06, 0.06, 0.032)`: the rump starts where the saddle ends; one step on the
  back (`model_game`, `model_back`, `model_side`).
- **MM2 chin:** the chin seg (0.080 / 0.026) on the Jaw, raised (z 0.825 -> 0.762) so it is fully inside the head when
  closed and only drops into view when the jaw opens. The pale underside of the snout is now a narrow rounded strip along
  the head loft's bottom line (0.08 wide, ~0.015 proud, smooth, on the Head), continuing the throat strip: no flat face, no
  white tip (`renders/_chin_sheet.png`: below, side, and roar f28 with the jaw open; `under.png`). The suggested head-loft
  band was tried first: the head's studs poked through its thin shell in a ragged patch, so it was not kept.
- **MM3 eyes:** VOLT (0.009, 0.026, 0.110), BLACK (0.011, 0.040, 0.118) (`_close_sheet.png`, `_icons_strip_64.png`).
- **MM4:** icon re-made after the export (see times above). Foot / horn log at the taps from the current file:
  `_scratch/feet_taps_f85r2.txt`: all four soles z 0.000 at f30, f42, f54; ankles at rest height (front 0.22, back 0.30);
  Horn_Tip z 0.008 / 0.008 / 0.004.
- **T-a:** FLANK (126, 134, 150) on the barrel only (legs / head stay IRON). IRON_D 41.6 % side (gate >= 25 %).
- **T-b:** brow nub 0.21 -> 0.12. **T-f:** thigh lofts 12 segments: tris 14,248 (was 14,572).

## Final gate round 3 (2026-10-28 05:09, exported 05:11)
- MUST 1, chin:
  - The separate pale Jaw chin seg is deleted. The MOUTH interior on the Jaw stays, so the open jaw still shows dark mouth in `pclose_below_roar_28` and `pclose_side_roar_28`.
  - The snout strip now stops at y -1.52, about 0.1 short of the tip. It was rebuilt as a smooth superellipse loft (13 rings, 0.036 x 0.011) that tapers to points at both ends, so `under.png` and `closeb_cbelow` show a soft pale spindle with no flat face or straight hard edge.
  - The white sliver at the snout front in `closeb_cside2` was the flat lit IRON front cap of the head loft, not the strip. It is now covered by a domed IRON_D nose cap (4 superellipse rings, 0.004 proud). The front edge in `closeb_cside2` (y 200-300) peaks at (244,255,255) as a rim sheen on the dark cap; the r2 render had a solid 255 white line.
- MUST 2, eye: VOLT `(0.009, 0.036, 0.110)` in BLACK `(0.011, 0.048, 0.118)`. 8 lime pixels form a line at the eye in `_icons_strip_64.png` at 1:1. The icon and strips were re-made from the 05:11 portrait.
- Tris 14,532, collision_free true.

## Final gate round 4 polish (2026-10-28 06:08)
- T4: the MOUTH interior's front end tapers to 0.03 x 0.025 (top=(0.30, 0.50); it was 0.07 x 0.0375). It reads as a wedge in `pclose_below_roar_28`. JAW_MAX is still 14.
- Eye frame: the BLACK socket is now (0.011, 0.074, 0.156); the slit inside is unchanged. In the portrait, a black frame surrounds the slit. In `_icons_strip_64` at 1:1, 8 dark pixels border the 7-pixel lime line. The icon was re-made from the 06:1x portrait.
