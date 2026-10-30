# Frostcrown Dragon - animation references (owner rule: references before keying), clip round 2, 2026-10-28

Method (lead ruling, review 4): for each clip I started from an animationreference.org TAG page, picked the site item,
and stepped the frames on that item's Sakugabooru source with canvas contact sheets (seek + draw; times in seconds;
our clips run at 30 fps, so frames = s x 30). I mapped each item to its post by the preview md5 on the tag page and
Sakugabooru's `post.json?tags=md5:`. **This used no site opens** (the counter stayed at 3/25).

- **HTTYD attempt (round 1):** `/tags/how-to-train-your-dragon`, "Flying With The Dragon Rider (HTTYD2)". The site
  open froze the Chrome tab, and no frames were read. I did not try it again.
- **HTTYD attempt 2 (round 3, review 5 TO 9+):** the tag's 10 items are YouTube clips or site-hosted HLS streams (no
  Sakugabooru post to step). I opened one site-hosted item, "How to Train Your Dragon" (`/video/PvGMeNA9bK8xXXQRNYAC`).
  The tab froze again (scripts and screenshots timed out), so I closed it. No frames were read and HTTYD is not used.
- **Round 1's Maid Dragon posts #31258 / #29750 did NOT come from a site tag.** I searched `/tags/dragon` (5 pages,
  mostly Dragon Ball), `/tags/flying` (all pages) and `/tags/kobayashi-san-chi-no-maid-dragon` (9 items), and neither
  post is on the site. I had found them by searching Sakugabooru directly, so they are dropped as primary references.

| # | site tag page -> site item title | Sakugabooru post | used for | frames read |
|---|---|---|---|---|
| H1 | `/tags/flying` (page 2), also `/tags/the-boy-and-the-heron` -> "Akihiko Yamashita: Character Acting & Creature Animation (BD - Animals)" | #260630 (*The Boy and the Heron*) | land, takeoff, act press, idle hold | LAND 12.6-17.0 s: 12.6-13.0 glide with wings spread, legs hanging; 13.4-13.8 the legs reach forward, the wings rise high behind (brake), body upright; **touch ~14.1 s**; 14.2-16.6 runs out the landing as the wings come down to half; 16.2-17.0 the body sinks and the wings fold. Flare to touch ~0.9 s (27 f). TAKEOFF 97.0-99.0 s: 97.0 wings half-open at the sides; 97.5 the wings rise high (gather); **98.0 push**, the legs leave as the downstroke starts; 98.5 the downstroke bottom; 99.0 airborne, wings spread, legs dangling. HEAD PRESS 44.0-51.6 s: 45.3 the head and neck lower and the body hunches; 46.5-49.1 hold low (~2.5 s) with small shudders; 50.4-51.6 rise. |
| E1 | `/tags/flying` (page 4) -> "Flying: Character Acting & Creature Animation (BD - Takeshi Honda)" | #236985 (*Tales from Earthsea*, dragons over the sea) | takeoff, land flare | TAKEOFF 13.6-14.8 s: 13.6-14.0 the dragon breaks from the sea; **14.4 the wings open full and the forelegs reach** (the launch, ~0.4 s / 12 f after the break); 14.8 it passes over, legs trailing. FLARE 36.8-38.8 s: the dragon rears upright in a hover, wings spread wide, forelegs reaching with open claws, head up. This is the brake pose before contact. |
| M1 | `/tags/flying` (page 4), also `/tags/kobayashi-san-chi-no-maid-dragon` -> "Flying: Creature Animation & VFX & Effects (NCOP (BD) - Kobayashi-San Chi No Maid Dragon S)" | #174482 | fly (body, legs) | 4.75-7.0 s: a black western dragon in level flight. The body is level, the neck long and forward, the legs tucked under the belly (forepaws folded), and the tail trails straight. |
| C1 | `/tags/walk-cycle` (page 4), also `/tags/the-cat-returns` -> "Animals: Character Acting & Creature Animation (BD - Crowd)" | #256671 (*The Cat Returns*, Shinji Otsuka) | walk gait | 16.79-17.71 s, a cat walking in side view: the near hind leg steps (~17.0), then the near foreleg (~17.2), then the far hind (~17.4), then the far fore (~17.6). That is a LATERAL-SEQUENCE walk, ~0.2 s between footfalls and a ~0.8 s cycle. The head and back stay level and the tail is carried. |
| W0 | `/tags/wolfs-rain` -> "Animals: Character Acting & Creature Animation (#30 - Wolfs Rain)" | #174333 (Yutaka Nakamura) | roar hold, act jaw | The mouth opens over ~15 f, then HOLDS with the head still. |
| D3 | ANIM_REFERENCES_1014 #8 (site study), *Avatar* banshee flight | - | fly stroke | One stroke ~0.8-0.9 s (FLY_N 28). High V at the top, ~25 below level at the bottom. The body barely bobs, the head stays level, and the tail streams. |
| D5 | ANIM_REFERENCES_1014 #3 (site study), *Sea Beasts* heavy-head roar | - | roar | The jaw opens fully ~0.4 s (12 f) after the head lift starts (the jaw lags the head). |

## How each reference maps to the clips (30 fps)
- **idle "frost hum" (120 f loop):** H1's stillness (holds with only small moves). Slow breath, wings HALF and back,
  fins tick 2 deg together (f32, f92), slow head sway (yaw +-8, long holds). Event `frostpuff` f80.
- **walk (40 f loop):** C1's lateral sequence (hind then fore on the same side: LH, LF, RH, RF) with a level head and
  back. Our heavy dragon stretches the cat's ~0.8 s cycle to 1.33 s (10 f between footfalls). The gait is matched
  (`cm.quad_walk(..., gait="walk")` is lateral sequence).
- **fly (28 f loop):** D3 stroke timing plus M1's body. Body near level (pitch 10), neck long and forward, head level,
  front paws tucked, hind legs trailing, tail streaming.
- **takeoff (28 f):** H1 97.0-99.0 + E1 13.6-14.8. f0-10 crouch while the wings rise to the stroke top (H1 97.5
  gather). **`launch` f11** = the push and the first downstroke (H1 98.0, E1 14.4). f12-15 the downstroke is split into
  in-betweens (review 4 N2). f19 the wings recover upward with the legs trailing (H1 99.0), into the flight cycle at f22.
- **land (28 f):** H1 12.6-17.0 + E1 36.8-38.8. f0 glide (H1 12.6). f7-12 flare upright with the wings braking and
  the legs reaching (H1 13.4-13.8, E1 36.8). **`touch` f16** (H1 ~14.1). f16-28 absorb (-0.05) while the wings come
  down and fold (H1 14.2-17.0), ending in the ground rest pose.
- **roar "crystal chime" (66 f):** D5 + W0. Head up 15 and wings to SPREAD (f0-14). The jaw lags the head (f14-26).
  The fins stand up 15 together. Event `roar` f24. Hold with the fin buzz (W0, f28-52), then close.
- **act_stillfreeze (110 f, signature):** H1 44.0-51.6 for the HEAD PRESS: the head and neck go down (H1 45.3 ->
  ours f22-34) and HOLD low (H1 46.5-49.1, ~2.5 s -> ours f34-58), then rise (H1 50.4 -> ours f58-80). The jaw opens
  over ~15 f and holds (W0). New peak (review 4 MUST 2): the wings flare open f30-44 and hold SPREAD f44-58 through the
  frost burst (`frost` f50). This is the H1 threat-display idea (wings spread around a still, locked head) on the
  press. The fins rise 30 at f16-22 (`click` f16).
