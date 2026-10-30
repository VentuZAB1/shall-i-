## C. Kaiju No. 8 - heavy creature weight (lead's site cuts, added 2026-10-27 after the clip gate)
Found on the site's free tag page `/tags/kaiju-no-8` (6 clips; no clip credit spent). I stepped the frames on the
Sakugabooru source posts (the same mp4 the site player streams) as canvas contact sheets in the browser. Nothing was
downloaded. Anime frames are at 23.976 fps; the 30-fps equivalent is x1.25.
- **#257646** (Sakugabooru tags `proro`, `kaiju no. 8`, `3d background`, `cgi`, `creatures`, `fighting`; Source #07). It is
  a CGI fight cut, not the Yuya Takahashi cut the lead's note names.
- **#254909** (tags `yuya takahashi`, `artist unknown`, `kaiju no. 8`, `character acting`, `creatures`; Source #01,
  CAD/AD Tetsuya Nishio). This is the site's "Kaiju No. 8: Character Acting & Creature Animation (#01 ... Yuya Takahashi)".

| # | observation | time / frames (24 fps) |
|---|---|---|
| K8a | **Landing into a hold.** Close-up: the feet and hand hit the street with a dust burst. Wide shot: the kaiju sits in a low three-point crouch, settles ~3 frames, then holds visually still for ~1.5 s (36 frames = ~45 f at 30 fps). Only the dust moves. | #257646 8.25-8.45 s (f198-203) impact; f204-207 settle; f207-243 hold (8.6-10.1 s) |
| K8b | **Tuck, lift, lock.** The head is bowed (horns forward, eyes down) and held ~4 frames. It lifts to level in ~4-5 frames (= ~6 f at 30 fps), the eyes lock on the camera, and then it holds still for ~0.9 s. The glowing lines carry the hold. | #257646 f243-247 tuck, f247-251 lift, f251-272 hold (10.14-11.34 s) |
| K8c | **Weight by stillness.** After the transformation the kaiju looks at its raised fist almost motionless for ~5 s (only small fist turns). The head turns from profile to the camera slowly, over ~3.3 s. No snaps: the size reads through slow, minimal motion and the glow. | #254909 15.8-21.3 s (fist), 24.6-28.0 s (head turn) |

**Fit:** these cuts fit the roar hold and the kneel hold. They do not show a rise: #257646 cuts out of the crouch, so K3
(Plate 356) stays the source for the rise itself.
- **roar:** K8b matches the beat order: tuck f0-10, lift f10-22, a still hold f22-50 (28 f = 0.93 s, K8b ~0.9 s), with
  the core pulses carrying the hold (K8c). My lift takes 12 f, which is slower than K8b's ~6 f. I kept the slower lift
  for the giant's mass (#9). If the reviewer wants more snap, the lift can go to f10-17 without other changes.
- **act_kneelrise:** K8a backs a still kneel hold (f18-50 = 1.07 s; only a 0.006 BU breath and the core pulses). The
  landing currently eases in (smoothstep into f18). An optional polish from K8a is a 3-frame settle after the knee lands
  (overshoot ~0.01 down at f20, back by f23). It is not applied yet: the clips under review stay unchanged.
- **idle:** K8c supports the low-motion idle (hip yaw +/-3 deg, 1-deg breaths, the head level).
