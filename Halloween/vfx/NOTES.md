# SLINGSHOT Halloween - VFX textures (rendered in Blender) - NOTES

All textures are rendered by `Halloween\vfx.py` in headless Blender 5.2 (Cycles CPU + OSL shaders in `vfx\osl\`).
Straight (un-premultiplied) alpha, sRGB, 8-bit RGBA PNG. The colour is defined everywhere (dilated into transparent
pixels), so filtered or mip-mapped edges never go dark. Every frame/image reaches alpha 0 at least 3 px before its edge,
so flipbook frames never bleed into each other.

Rebuild: `blender.exe -b --factory-startup --python Halloween\vfx.py -- all` (about 5 min), then
`python Halloween\vfx\make_sheet.py`. Review sheet: `vfx_contact_sheet.png` (over dark and sky-blue sRGB 140,170,205,
each with normal blending (LightEmission 0) and additive blending (LightEmission 1), plus the candle loop-seam check).

## Files

| File | Size | Layout | Use |
|---|---|---|---|
| `CandleFlame_8x8.png` | 1024 x 1024 | 8x8 = 64 frames of 128 px, row-major from the top-left | FlipbookLayout **Grid8x8**, FlipbookMode **Loop** |
| `FireTongue_8x8.png` | 1024 x 1024 | 8x8 = 64 frames of 128 px | Grid8x8, **OneShot** |
| `SmokeWisp_4x4.png` | 1024 x 1024 | 4x4 = 16 frames of 256 px | **Grid4x4**, **OneShot** |
| `Glow.png` | 256 x 256 | single | FlipbookLayout None |
| `Ember.png` | 64 x 64 | single | None |
| `Mist.png` | 512 x 512 | single | None (optional low ground mist) |

Sources: `..\vfx.py`, `osl\common.h`, `osl\candle.osl`, `osl\tongue.osl`, `osl\smoke_vol.osl`, `osl\glow.osl`,
`osl\ember.osl`, `osl\mist_vol.osl` (`smoke.osl` and `mist.osl` are older 2D versions, not used). `make_sheet.py`
builds the review sheet. `_work\` holds intermediate EXRs, logs and test previews (safe to delete).

### What is in each texture
- **CandleFlame**: a tall teardrop (round full belly low down, convex sides, pointed tip), white-yellow core low in the
  belly, orange body, a thin red edge, a faint blue rim at the very base. Gentle sway = a slow bend travelling up the
  flame. The loop has one strong flicker (frames 22-26: it stretches, thins, wiggles and a small tongue pinches off the
  tip and burns out) and one weak flicker (around frame 51). Every time function is periodic, so the loop is seamless:
  mean frame-to-frame change 0.00120, frame 63 -> frame 0 change 0.00090 (smaller than an average step).
  In the frame: the flame bottom is 8.6 % of the frame above the frame's bottom edge; the normal tip is 24 % below the
  top edge (67 % of the frame tall); a flicker reaches 4 % below the top. Width about 22 % of the frame, centred.
- **FireTongue**: one-shot. f0-8 born (a small bright bulb), f8-32 licks upward (whipping S-shaped tongue, torn licking
  tips, white-yellow inner core, bright ribbons and darker folds), f34-50 its waist is eaten through and the top breaks
  away and keeps rising, f50-63 the pieces cool to red, tear into wisps and burn out. The root fades out softly (raggedly)
  so many overlapping tongues merge into one fire bed. Root about 5 % above the frame's bottom edge, about 31 % of the
  frame wide, centred.
- **SmokeWisp**: a lit volumetric dark-grey puff (real self-shadowing, lit from the upper left): it rises a little in
  the frame, rolls/curls (vortex-ring flanks), grows, thins into wisps and fades (last frame faint). About 50 % of the
  frame wide, centred. Colour roughly sRGB 35-150 grey.
- **Glow**: warm radial glow: white-yellow hot centre -> amber -> orange, Gaussian core + soft tail, alpha 0 at 95 % of
  the radius. Bright part = the inner ~30 % of the image.
- **Ember**: a solid white-yellow core (radius about 25 % of the image) in an orange glow.
- **Mist**: a soft, wide, translucent pale-lavender mist bank (max alpha 0.77).

## Roblox setup (all emitters)

- Upload the PNGs as Images under the group **ZAB Studio** (the place is group-owned); `Texture = rbxassetid://<id>`.
- `Color` stays **white** (the colour is in the texture). `LightInfluence = 0` for every fire/glow/ember emitter (they
  are light sources), `WindAffectsDrag = false`.
- **OneShot** plays the whole flipbook exactly once over each particle's lifetime (`FlipbookFramerate` is ignored), so
  the texture's timing scales with `Lifetime`.
- Flames use `Orientation = FacingCameraWorldUp` (they stay upright when the camera looks down); glow, embers and smoke
  use `FacingCamera`.
- **About LightEmission in daylight**: additive blending can only brighten, so over the bright daytime sky every
  additive flame turns pale cream/pink (see the sky + additive rows of the sheet). Inside the head and in the egg
  interiors the background is dark, so LightEmission 1 is right there. For the small candle flames that are seen against
  bright walls and sky, use a lower LightEmission (0.35) so they keep their orange colour. `Brightness` 1.2-2 adds
  punch (and bloom if the place has a Bloom effect).
- Roblox does not interpolate flipbook frames: the candle and the tongue have 64 small steps (smooth); the smoke has
  16 gradual steps and relies on the particle's own rise, growth and rotation for the motion.

Sequences below are written as `(time, value[, envelope])`.

### 1. Candle flame (pumpkin-egg candles, hub candles)
Attachment: on the wick tip, moved **up by 0.414 x Size** (the flame's bottom sits at 8.6 % of the frame).

| Property | Value |
|---|---|
| Texture | CandleFlame_8x8 |
| FlipbookLayout / Mode | Grid8x8 / Loop |
| FlipbookFramerate | 24 (one loop = 2.67 s) |
| FlipbookStartRandom | false |
| Size | constant **1.5 x the wanted flame height** (e.g. 1.2 for a 0.8-stud flame; 1.6 inside a 7-stud egg) |
| Lifetime | 3.07 (= 64/24 + 0.4) |
| Rate | 0.375 (= 24/64: one particle per loop) |
| Speed / SpreadAngle / Acceleration / Drag | 0 / (0,0) / (0,0,0) / 0 |
| LockedToPart | true |
| Rotation / RotSpeed | 0 / 0 |
| Transparency | (0, 1) (0.13, 0) (0.87, 0) (1, 1) |
| LightEmission | 0.35 in daylight (1 inside a dark egg is fine) |
| LightInfluence / Brightness | 0 / 1.5 |
| Orientation / ZOffset | FacingCameraWorldUp / 0.05 |

Why these numbers: a new particle is born exactly one loop after the previous one, so both show the same frame while
they cross-fade (no ghost double flame) and the flame is continuous. Call `emitter:Emit(1)` once when the candle is
enabled (so it does not wait one period for the first flame). Stop all candles flickering in sync: enable each
emitter after a random `task.delay(math.random() * 2.6, ...)`, or give each candle its own fps in 21-27 with
`Rate = fps/64` and `Lifetime = 64/fps + 0.4`.
Optional halo: a second emitter with Glow, Size 2.5 x flame height, Transparency 0.65, Rate 4, Lifetime 1,
LightEmission 1, LockedToPart true. PointLight: Color (255,150,60), Range 8-10, Brightness 1-1.5.

### 2. The giant head's inner fire (head ~110 studs wide)
Emitter: an invisible, non-colliding, anchored Part (Transparency 1) as the fire bed on the floor of the head
interior, about **60 x 2 x 36** studs (X x Y x Z), `Shape = Box`, `ShapeStyle = Volume`, `EmissionDirection = Top`.
The Part must move with the head (weld it to the head) so the fire stays inside when the head turns.

| Property | FireTongues | FireBedGlow (2nd emitter, same Part) |
|---|---|---|
| Texture | FireTongue_8x8 | Glow |
| FlipbookLayout / Mode | Grid8x8 / OneShot | None |
| Size | (0, 24, 6) (0.5, 34, 7) (1, 30, 7) | (0, 50, 10) (1, 60, 10) |
| Lifetime | 1.1 - 1.6 | 0.8 - 1.2 |
| Rate | 36 (about 50 tongues alive) | 6 |
| Speed | 8 - 14 | 2 - 4 |
| SpreadAngle | (12, 12) | (5, 5) |
| Acceleration / Drag | (0, 10, 0) / 0.5 | (0, 0, 0) / 0 |
| Rotation / RotSpeed | -8 - 8 / 0 | 0 - 360 / -10 - 10 |
| Transparency | (0, 0.4) (0.12, 0.05) (1, 0.15) | (0, 1) (0.3, 0.6) (0.7, 0.6) (1, 1) |
| LightEmission / LightInfluence | 0.85 / 0 | 1 / 0 |
| Brightness | 1.3 | 1.2 |
| Orientation | FacingCameraWorldUp | FacingCamera |
| LockedToPart | false (true if the tongues should swing with the head) | true |

Tongues rise about 25 studs on their own plus their in-frame rise, so with 24-34-stud particles the flames reach
50-60 studs above the floor, i.e. up past the eyes. Raise Size/Speed if the eyes need more fire. A flickering
PointLight (Range 60-80, Color (255,140,50)) in the middle completes it.

### 3. Embers rising out of the head
Emitter: the same fire-bed Part (a third emitter). Particles are not blocked by the shell, so embers rise through the
interior (seen in the holes) and come out above the head top.

| Property | Value |
|---|---|
| Texture | Ember |
| Size | (0, 1.0, 0.4) (0.7, 0.8, 0.3) (1, 0) |
| Lifetime | 3 - 5 |
| Rate | 14 |
| Speed | 18 - 28 |
| SpreadAngle | (25, 25) |
| Acceleration / Drag | (2, 4, 0) (a slight drift) / 0.6 |
| Rotation / RotSpeed | 0 / 0 |
| Transparency | (0, 0) (0.3, 0.25) (0.5, 0) (0.75, 0.3) (1, 1) (twinkle) |
| LightEmission / LightInfluence / Brightness | 1 / 0 / 2 |
| Orientation / Squash | VelocityParallel / 0.5 (short streaks along the motion) |

### 4. Eye glow behind each eye socket (~25-stud sockets)
Attachment: inside the head, centred on each socket, about 8 studs behind the opening and **behind the slit pupil**
(the pupil is opaque geometry, so it stays dark in front of the glow). Two emitters per eye on the same Attachment:

| Property | EyeGlowCore | EyeGlowFill |
|---|---|---|
| Texture | Glow | Glow |
| Size | (0, 32) (0.5, 38) (1, 32) | (0, 66) (0.5, 72) (1, 66) |
| Lifetime | 1.2 - 1.6 | 1.6 - 2.0 |
| Rate | 4 | 2.5 |
| Speed / Acceleration | 0 / 0 | 0 / 0 |
| Rotation / RotSpeed | 0 - 360 / -10 - 10 | 0 - 360 / -6 - 6 |
| Transparency | (0, 1) (0.25, 0.35) (0.75, 0.35) (1, 1) | (0, 1) (0.3, 0.55) (0.7, 0.55) (1, 1) |
| LightEmission / LightInfluence / Brightness | 1 / 0 / 1.5 | 1 / 0 / 1.2 |
| LockedToPart | true | true |
| ZOffset | -8 | -10 |

The fill makes the whole socket glow, the core gives the hot centre; overlapping particles that fade in and out give a
slow living shimmer. The negative ZOffset pushes the camera-facing quads away from the camera so they never poke
through the shell around the socket when the head is seen from the side.

### 5. Glow inside each 7-stud pumpkin egg
Attachment: the egg's inside-light point (see the egg builder's NOTES), plus the candle flame of section 1 (Size ~1.6)
and a PointLight (Color (255,150,60), Range 10-12, Brightness 1.2).

| Property | Value |
|---|---|
| Texture | Glow |
| Size | (0, 5.6, 0.4) (0.5, 6.6, 0.4) (1, 5.6, 0.4) |
| Lifetime | 1.0 - 1.4 |
| Rate | 4 |
| Speed / Acceleration | 0 / 0 |
| Rotation / RotSpeed | 0 - 360 / -10 - 10 |
| Transparency | (0, 1) (0.3, 0.4) (0.7, 0.4) (1, 1) |
| LightEmission / LightInfluence / Brightness | 1 / 0 / 1.2 |
| LockedToPart / ZOffset | true / -0.5 |

### 6. Smoke from the head's top
Emitter: an Attachment (or a small invisible Part) at the head's top around the stem, `Shape = Disc` radius ~8 if a
Part is used. The puff fills about half of the frame, so the visible puff is about 0.5 x Size.

| Property | Value |
|---|---|
| Texture | SmokeWisp_4x4 |
| FlipbookLayout / Mode | Grid4x4 / OneShot |
| Size | (0, 12, 3) (0.5, 24, 4) (1, 36, 5) |
| Lifetime | 4.5 - 6 |
| Rate | 3 |
| Speed | 6 - 10 |
| SpreadAngle | (10, 10) |
| Acceleration / Drag | (1.5, 2, 0) (drift with the wind direction you like) / 0.3 |
| Rotation / RotSpeed | 0 - 360 / -10 - 10 |
| Transparency | (0, 1) (0.12, 0.25) (1, 0.45) (the texture fades itself at the end) |
| LightEmission / LightInfluence / Brightness | 0 / 0.5 / 1 |
| Orientation | FacingCamera |
| LockedToPart | false (it should trail behind when the head turns) |

The texture already contains its own lighting (lit upper left, darker underside); LightInfluence 0.5 lets the hub's
sun shade it a little more without turning it black in shadow.

### Optional: low ground mist
Texture Mist, Size (0, 18) (1, 26), Lifetime 6 - 9, Rate 1.5, Speed 0.5 - 1.5, SpreadAngle (180, 0) from a flat Part,
Transparency (0, 1) (0.3, 0.6) (0.7, 0.6) (1, 1), LightEmission 0, LightInfluence 0.7, Rotation 0 - 360, RotSpeed -3 - 3.

## Known limitations
- Over a bright daytime sky, additive (LightEmission 1) flames read as pale cream, not orange; that is how additive
  blending works. Keep the candles at LightEmission ~0.35 where the sky is behind them.
- The FireTongue is one design reused by every particle; the variety comes from Size/Speed/Rotation ranges and the
  overlapping lifetimes. If repetition shows, render a second variant (change `seed` in `osl\tongue.osl`, e.g. 5.9)
  and alternate two emitters.
- The smoke has only 16 frames (as requested); at 4.5-6 s lifetime that is ~3 frames/s, hidden by the particle motion.
- The Rate-based single-flame candle relies on Roblox emitting at a steady interval; if a cross-fade ever shows a ghost
  flame, drive it from a script instead (`Rate = 0`, `Emit(1)` every 64/fps s).
