# SLINGSHOT: early-game economy v5 + egg placement (design, 2026-10-12)

## Owner's request (verbatim)
- **Speed:** Start at 0 instead of 10M. Keep the same progression feeling and ensure speed progression remains balanced.
- **Money / Upgrades:** Grass and Water pets generate only $1–$1K for new players, while plot upgrades cost around $1M.
  Rebalance prices so beginners can afford upgrades quickly.
- **Pet Placement (Mobile & PC):** Make placement inside the player's base intuitive. On mobile, players should be able
  to tap their base/plot to place an egg without having to aim precisely. On PC, fix the placement detection near
  fences so players can place eggs on valid grass even when standing close to the fence.
- Rebalance the early-game economy and review the entire progression to ensure it remains fair and satisfying later in
  the game.

## Owner's answers (2026-10-12)
- **Speed feel:** the same as now. 0 walks like today's 10M.
- **Money:** cheaper early prices plus a Grass/Water income buff, with the ladder re-tuned by the simulator.
- **Old saves:** subtract 10M once, and the TOP SPEED board restarts.
- **Placement:** exactly as written in the request. It is not an aiming system.

## 1. Speed starts at 0
- `SpeedStat.WalkSpeed(speed)` reads `speed + 10M` (constant `SpeedStat.OFFSET = 10_000_000`) on the existing curve.
  So Speed 0 = walk 48, the same as the old start, and every treadmill second feels identical.
- **New saves** and **every rebirth** set Speed to 0 (`RebirthConfig.START_SPEED = 0`; the PlayerData default is 0).
- **Old saves:** a one-time migration, `Speed = max(0, Speed − 10M)`, guarded by a save flag, so it never runs twice.
- **Board:** the TOP SPEED leaderboard gets a new OrderedDataStore key, so old and new numbers aren't mixed.
- **Percent-based speed rewards** (playtime gifts) use `Speed + OFFSET`, so they stay the same size.
- Any other hard-coded 10M speed value in scripts moves to the new scale.

## 2. Economy v5: the early game is cheaper, the late game is unchanged
Simulated with `SLINGSHOT Creatures/economy/v5_model.py`, which builds on the v4 `pacing_model.py`. The simulated
player is a free, engaged player who gets the tutorial's free Slingshot Lv1.

| Item | v4 | v5 |
|---|---|---|
| Pet income base (`CreatureConfig.AREA_INCOME`) Grass / Water | 8 / 50 | **20 / 120** (Thunder+ unchanged) |
| Slingshot price of level L | $25K × 1.95^(L−1) | **min($500 × 2.6^(L−1), v4)**, rounded to 2 significant figures |
| Treadmill T2 (x6) / T3 (x40) | $1M / $50M | **$10K / $2M** (T4–T6 unchanged) |
| Rebirth R1 / R3 / R4 | $250K / $7M / $50M | **$40K / $5.5M / $25M** |
| Rebirth R6 / R7 / R8 | $500M / $2B / $5B | **$800M / $1.8B / $4B** |
| Rebirth R2, R5, R9–R20 | | unchanged |

The new slingshot curve meets v4 at Lv15 (~$290M); Lv15 onward is unchanged:

| Level | Price | Level | Price | Level | Price |
|---|---|---|---|---|---|
| 1 | $500 (free in tutorial) | 6 | $59K | 11 | $7.1M |
| 2 | $1.3K | 7 | $150K | 12 | $18M |
| 3 | $3.4K | 8 | $400K | 13 | $48M |
| 4 | $8.8K | 9 | $1M | 14 | $120M |
| 5 | $23K | 10 | $2.7M | 15+ | v4 |

Rebirth locks, Fast Grab, Wave Shield, pet requirements, KG odds and hatch times are unchanged.

**Expected pacing (simulator median):**
- Purchases at about 4–5 min (Sling Lv2, Lv3, Treadmill x6), then R1 at about 8 min, Sling Lv4–5, and Grab Lv1 at
  about 10 min.
- Runs grow smoothly, 8 → 10 → 14 → 16 → 23 → 30 … min.
- R12 at about 10 h; R20 at about 59 h, the same as v4.

**Side effects:**
- Selling and playtime cash are based on income, so they rise for Grass and Water.
- The 49 R$ Robux skip for Treadmill x6 isn't worth buying at $10K, so that one Robux button is hidden. The other
  Robux prices are unchanged.

## 3. Egg placement
- **Shared rule (server and client):** a placement spot that is too close to the fence or to another egg moves to the
  nearest free spot inside the base, instead of being rejected. "Pet slots full" or "No room" appear only when they are
  really true.
- **Phone:** holding an egg, a tap on your plot places the egg there (or at the nearest free spot). The tap position
  comes from the tap itself, not from the last touch, which can be the joystick.
- **PC:** clicking grass inside your fence near the fence places the egg, even when standing right next to the fence.
- **Hint:** the slot count shows the real pet slots (3 + rebirths), not the area-based number it shows now.
- **Server:** `BaseHatchery.PlaceEgg` applies the same rule, so a slightly-off spot gets moved, not refused.
- **No ghost preview.** The owner said no earlier, and it stays no.

## 4. Testing
- Studio tests on test saves only: `TestFreshSave = true` before every Play, false after.
- **Speed:** walk speed at 0 = 48; the migration subtracts 10M exactly once; rebirth sets 0; the board key is new.
- **Prices:** UpgradeConfig, ShopConfig, RebirthConfig and CreatureConfig match the tables.
- **Placement:** spots at the fence edge are moved inside; a full base says so; the server accepts the moved spot.
- **Phone:** a tap test in the device emulator.
- The simulator files live in `economy/` for future re-tuning.

## 5. Follow-ups (same day, owner-approved)
### Eggs after the base grows (bug fix)
A rebirth that grows the base rebuilt the floor while egg records stayed relative to the old floor, so eggs jumped after
a rejoin and the server's spacing check disagreed with what players saw.
- **BaseHatchery `rebase(base)`:** runs on the base's Width/Length change. It keeps every egg at its world spot and
  rewrites its record (and its live grow entry) to the new floor, using findSpot only if needed.
- **Pets** now wander inside the current floor.
- **Tested:** the base grew 40x40 to 50x56; the models moved 0.02 studs; records match exactly; a new egg placed next
  to an old one is accepted.

### Treadmills +2 per upgrade (v6)
The owner asked for "1x > 2x > 4x > 6x > 8x > 10x", with more tiers to come.

| Tier | x1 | x2 | x4 | x6 | x8 | x10 |
|---|---|---|---|---|---|---|
| Rate (50K x mult) | 50K | 100K | 200K | 300K | 400K | 500K |
| Price | free | $10K | $2M | $100M | $1.5B | $80B |

The Robux skips are unchanged; the x2 skip is hidden.

The walk curve is the same up to Thunder (walk 75 at 100M). After that it is compressed: Fire / Shadow / Celestial need
200M / 360M / 750M Speed instead of ~1B / 10B / 100B.

Simulated (`economy/tread_v6.py`):
- Run times are unchanged within noise; R20 is about 57 h.
- Tiers are bought at about 6 min, 40 min, 1.5 h, 3.4 h and 8.7 h.

**Future tiers** are x12, x14 ...: one price row in `ShopConfig.TreadmillMoney` / `TreadmillRates` / Robux tables, plus
one template in `ServerStorage.Assets.Treadmills` (attributes Tier, TierName, SpeedPerSecond). Price each new tier at
about 25-50x the previous one.

**Tested:** all 5 upgrades are bought through the real remote; sign names and rates are correct; the hub model is
swapped to the tier's template.

### Hatch times v7 (owner: further down the runway and bigger KG = way longer)
- `CreatureConfig.hatchSeconds(kg, eggKind) = max(10, 32400 × AREA_HATCH[area] × (kg / 200K)^0.43)`.
- `AREA_HATCH = {0.02, 0.04, 0.1, 0.25, 0.5, 1}`, from Grass to Celestial.
- Results:
  - Celestial: 200K = 9 h, 1M = 18 h.
  - Shadow 1M = 9 h.
  - Water 10K = 6 min.
  - Grass 1 KG = 10 s.
- The Growth ×2 pass halves these.
- Eggs already placed keep their timers.
- Simulator: `economy/hatch_v7.py`.

### Treadmills x12–x20 (owner: "make 5 more ... see bigger differences"; "subagents, reviewers, approved plans")
| Tier | x12 | x14 | x16 | x18 | x20 |
|---|---|---|---|---|---|
| Rate | 600K | 700K | 800K | 900K | 1M |
| Price (money only) | $2T | $8T | $25T | $75T | $200T |
| Theme | Emerald | Frost | Galaxy | Inferno | Diamond Rainbow |
| Top (studs) | 10.0 | 12.8 | 14.4 | 14.9 | 15.8 |
| Visible / animated parts | 68 / 22 | 88 / 27 | 93 / 40 | 106 / 40 | 109 / 41 |

- **Process:**
  - The brief is `Treadmills/TREADMILL_BRIEF.md`.
  - 5 builder agents wrote plans. One plan reviewer approved them and set the height ladder (`PLAN_REVIEW.md`).
  - The builders built in a Studio lab, checked by an automatic validator.
  - Each tier had its own visual reviewer (`T*/REVIEW.md`), then a fix round.
  - A final lineup reviewer gave SHIP (`LINEUP_REVIEW.md`).
- **Style:** the same LEGO brick style as tiers 1–6 (Plastic + Studs/Inlet/Universal/Weld) and the same chassis. All new decor is non-colliding.
- **Hard limits (all five pass):**
  - The upgrade sign, the path lamp and the runner zone stay clear.
  - The runner camera corridor and the owner's exit walkway behind the belt stay clear.
  - The "+X / sec" label stays on a dark screen face.
- **Shop:** `ShopConfig` gained the rows for tiers 7–11. `TreadmillRobuxHidden[7..11] = true`; no Robux product exists for these tiers.
- **TreadmillClient:**
  - The walk animation speed goes up to tier 11.
  - Flames, sparkles, runes and wings switch the fx loop on by themselves.
  - Runes chase in number order.
  - Belt chevrons move with the arrow texture.
- **Tested in Play (TestFreshSave):**
  - Bought x2 → x20 through the real remote. Prices are right, the hub model swaps, sign names and rates are right, and the 11th buy returns "Max".
  - Label "+2M" (with the 2× pass).
  - Idle and running animation move.
  - Speed rises about 1.95M/s when mounted, which is 1M × 2.
  - A new Celestial 200K egg got 4.5 h, which is 9 h halved by Growth ×2.
  - No warnings or errors.
- **Lab kit:** `ServerStorage._TreadmillLabKit` + `_TreadLabTools`. To reuse for future tiers, parent the kit to Workspace and rename it `_TreadmillLab`.
- **Backup:** `ServerStorage._Backup_Treadmills11`.
