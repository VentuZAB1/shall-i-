# Early-game economy v5 + egg placement: plan (2026-10-12)

**Spec:** `docs/specs/2026-10-12-early-economy-placement-design.md`. The owner approved it and said "Start doing it",
so I'm running it inline.
**Backup:** `ServerStorage._Backup_EconomyV5.Before` holds clones of every script before any change.
**Test rule:** `TestFreshSave = true` before every Play; set it back to false after the last Play.

## Task 1: Speed starts at 0
- **SpeedStat:** add `OFFSET = 10_000_000`; `WalkSpeed(s)` uses `log10(1 + s + OFFSET)`. Update the curve comments.
- **RebirthConfig:** `START_SPEED = 0`.
- **PlayerData:** field `Speed = 0`, plus a new `SpeedZero = true` field. A loaded save without `SpeedZero` gets
  `Speed = max(0, Speed - 10M)` once, then `SpeedZero = true`. This runs after the `SpeedScale` migration.
- **Leaderboards:** TOP SPEED store `TopSpeed_v3` → `TopSpeed_v4`.
- **PlaytimeConfig.amount:** the speed gift = `(speed + OFFSET) * pct`. `MIN_SPEED` is no longer needed.
- **Test:** walk(0) = 48 = old walk(10M); the migration math; rebirth → 0.

## Task 2: Economy v5 numbers
- **CreatureConfig.AREA_INCOME:** `{20, 120, 300, 1800, 10000, 55000}`.
- **UpgradeConfig.slingCost(L):** `nice(min(500 * 2.6^(L-1), 25000 * 1.95^(L-1)))`.
- **ShopConfig.TreadmillMoney[2] = 10000, [3] = 2000000.** Hide the T2 Robux skip: ShopClient and TreadmillSignClient
  skip the Robux button for T2.
- **RebirthConfig.LADDER costs:** R1 40K, R3 5.5M, R4 25M, R6 800M, R7 1.8B, R8 4B.
- **Test:** the config values match the spec tables; the UI shows the new prices.

## Task 3: Egg placement
- **BaseConfig.findSpot(floor, pos, r, eggs, spacingFn):** returns `pos` if valid, otherwise the nearest valid spot
  inside the inner rect (ring search, 1-stud steps, up to the rect size), otherwise nil. Shared by client and server.
- **EggPlaceClient:**
  - PC: the mouse ray hits the floor plane (not just the floor part), so clicks near or over the fence still count;
    the spot goes through `clampInside` + `findSpot`.
  - Phone: `TouchTapInWorld` gives the real tap position; a tap on the plot (plane hit inside the base + 6-stud
    margin) places through `findSpot`.
  - The hint shows the real pet slots.
- **BaseHatchery.PlaceEgg:** run the same `findSpot` before validate, so a slightly-off spot is moved, not refused.
- **Test:** findSpot unit checks (edge, corner, crowded, full); a server PlaceEgg near the fence succeeds; phone
  emulator tap.

## Task 4: Play verification + docs
- **Play test** (TestFreshSave on):
  - fresh player: Speed 0 and walk 48;
  - prices in the Upgrade window, the treadmill sign and the Rebirth page;
  - placing near the fence on PC;
  - the phone emulator.
- **Memory and docs:**
  - memory: economy-v5 notes;
  - update the economy-v4 and upgrade-stall memories;
  - the owner must Save + Publish + Migrate.
