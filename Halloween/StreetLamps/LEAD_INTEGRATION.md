# Lead's integration notes (not for the builder) - 2026-10-13

## The old lamps (to be moved to ServerStorage._Backup_StreetLamps)
- `Workspace.Map.Hub.Decor.PathLamps`: 30 loose parts (6 lamps x LampBase / LampPost / arm / cap / Neon Lantern).
- `Workspace.Map.Hub.MarketCorners.LeftMarket`: LampBase, LampPost, LampArm, LampCap, Lantern x2.
- No PointLights. No script references them.

## Spots (post centre x, z; ground y; the direction the old lantern hung, in xz)
| # | where | x | z | ground y | lantern dir (x, z) |
|---|---|---|---|---|---|
| 1 | path | 0.41 | 8.15 | 0 | (-0.99, -0.12) |
| 2 | path | -9.09 | -5.15 | 0 | (0.99, 0.12) |
| 3 | path | -58.34 | 8.70 | 0 | (-0.54, -0.84) |
| 4 | path | -37.86 | -17.40 | 0 | (0.54, 0.84) |
| 5 | path | 64.25 | -0.58 | 0 | (-0.54, 0.84) |
| 6 | path | 31.95 | -8.12 | 0 | (0.54, -0.84) |
| 7 | market deck | -71.51 | -47.44 | 0.6 | (-0.71, -0.71) |
| 8 | market deck | -105.46 | -13.50 | 0.6 | (-0.71, -0.71) |

## Studio setup to reuse (from HalloweenDecor.PumpkinEggs)
- Inside PointLight: Range 11, Brightness 1.2, Color ff963c, Shadows true, attribute `Flicker` = base brightness.
  HalloweenClient flickers it automatically (DescendantAdded, so it works with streaming).
- Glow ParticleEmitter: tex rbxassetid://121296816813830, Rate 4, Size 5.6, Lifetime 1-1.4, LightEmission 1, ZOffset -0.5.
- Candle Flame ParticleEmitter: tex rbxassetid://122285978725244, Grid8x8 flipbook, Size 1.2-1.6, LightEmission 0.35-1,
  ZOffset 0.05, attribute `Prime` (HalloweenClient emits the first frame right away).
- Every Halloween part: CanCollide / CanTouch / CanQuery false, CollisionFidelity Box, RenderFidelity Precise.
- Night boost: DayNightClient will raise the lamp lights (Range / brightness) while Night is on.
