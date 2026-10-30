# Glacier update: ECONOMY PLAN (numbers only, nothing built)

2026-10-27. Spec: `docs/plans/2026-10-22-new-pets-glacier-area.md`. Owner decisions: keep the 12 names, area 7 =
FROSTFALL GLACIER + Glacier Egg, rebirths up to R25, no 2nd slingshot, odds down to 0.1%.
Everything "today" was read from Studio (read-only) on 2026-10-27. Nothing in Studio was changed.

Sims: `PetsV3/economy/glacier_sim.py` (+ `glacier_spread.py`). Output: `glacier_sim_output.txt` (next to this file).
The sim is one greedy FREE player with every live formula (rarity bonus, v7 hatch, 11 treadmills, offline 10%, sling
v5 + 10-27 changes). "Dedicated" = 3 h of play a day, offline the rest (eggs keep hatching). It plays like a fast bot:
real players are about 2-3x slower in the first hour (water_wall_sim calibration), so read the numbers as
today-vs-new, not as exact hours.

---

## 1. Area 7 position

Same 400-stud pattern as areas 1-6 (each area's floor, AreaZone and trench line up like this today).

| Thing | Today (Celestial end) | Glacier |
|---|---|---|
| Floor | Celestial z -2060 .. -2460 | **z -2460 .. -2860** |
| AreaZone centre / size Z | -2260 / 400 | **-2660 / 400** (x 0, size X 120) |
| Trench (Gap.HideZone) centre | -2260 (11 long) | **-2660** (11 long) |
| `Map.Bounds.Runway_End` centre z | -2470 (size 162 x 1000 x 22) | **-2870** (same size) |
| Side bounds | `Runway_L_2` / `R_2`: x -70 / 70, z -1872.5, size 22 x 1000 x 1217 (ends at -2481) | **add `Runway_L_3` / `Runway_R_3`**: x -70 / 70, y 540, **z -2670**, size **22 x 1000 x 422** (z -2459 .. -2881) |
| `WaveConfig.StartZ` | -2500 | **-2900** (40 past the floor end, like today) |
| `UpgradeConfig` AREAS | ends at `{name = "Celestial", z = -2060}` | add **`{name = "Glacier", z = -2460}`** |

- The runway folder must be named exactly **`Area7_Glacier`** with attributes `Area = 7`, `AreaName = "Glacier"`,
  `Emoji = "🧊"`, tagged `Area` (+ `TextColor`) for the AreaTitle banner. UFO/Meteor clients find zones by
  `("Area%d_%s"):format(area, AREA_NAMES[area])`.
- `MapGuard` has no numbers in it: it reads `Map.Bounds` parts, so moving/adding the Bounds parts is enough.
- WeatherServer, EggSpawner and the `CurrentArea` loop build their areas from the Runway folders (AreaZone + `Area`
  attribute), so they pick up area 7 automatically.

## 2. Slingshot Power for Glacier

**Formula: keep the same straight line, just let it run past 25.** The slope stays `(2300 - 370.3) / 25 = 77.2`
studs per level by keeping the old divisor 25 under a new name. Checked in Studio: Lv0-25 give exactly today's
range. Price, lock and range for Lv0-25 don't change.

Paste into `ReplicatedStorage.UpgradeConfig`:

```lua
-- line 22-25
local AREAS = {
	{name = "Grass", z = -60}, {name = "Water", z = -460}, {name = "Thunder", z = -860},
	{name = "Fire", z = -1260}, {name = "Shadow", z = -1660}, {name = "Celestial", z = -2060},
	{name = "Glacier", z = -2460},
}
-- line 48-57
U.SLING_MAX = 30 -- 2026-10-27 Glacier: Lv26-30 continue the SAME straight line (77.2 studs a level)
U.SLING_SLOPE_LEVELS = 25 -- the slope stays (MAX_RANGE - BASE_RANGE) / 25, so Lv0-25 keep exactly today's range
U.SLING_BASE_RANGE = rangeOf(SlingConfig.MaxSpeed) -- ~370 studs: the end of Grass
U.SLING_MAX_RANGE = 2300 -- the range at Lv25 (Lv30 = 2686)
-- (SLING_EARLY_RANGE line 53 unchanged)
function U.slingRange(level)
	local l = math.clamp(level, 0, U.SLING_MAX)
	return U.SLING_BASE_RANGE + (U.SLING_MAX_RANGE - U.SLING_BASE_RANGE) * l / U.SLING_SLOPE_LEVELS + (U.SLING_EARLY_RANGE[l] or 0)
end
-- line 87
U.SLING_REBIRTH = {0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 7, 7, 7, 9, 9, 11, 11, 13, 13, 16, 20, 20, 22, 22}
```

`slingCost` needs **no change**: its $25K x 1.95^(L-1) curve already continues past 25. Also update the header comment
(lines 1-14): "30 levels ... Glacier Lv27 at R20 (R21)".

| Level | Range | Full-power landing z | Lands in | Price (formula) | Money lock | Flight |
|---|---|---|---|---|---|---|
| 24 (today) | 2223 | -2268 | Celestial | $120B | R13 | 7.6 s |
| 25 (today) | 2300 | -2345 | Celestial | $230B | R13 | 7.7 s |
| **26** | 2377 | -2422 | Celestial (38 studs before the gate) | **$450B** | **R16** | 7.8 s |
| **27** | 2454 | -2499 | **Glacier** (+39) | **$870B** | **R20** | 7.9 s |
| **28** | 2532 | -2577 | Glacier | **$1.7T** | **R20** | 8.1 s |
| **29** | 2609 | -2654 | Glacier (at the trench) | **$3.3T** | **R22** | 8.2 s |
| **30** | 2686 | -2731 | Glacier | **$6.4T** | **R22** | 8.3 s |

- **Glacier opens at Lv27, money lock R20, one rebirth before R21 (the first rebirth that needs a Glacier pet).**
  That's today's rule (Water Lv1 R0, Thunder Lv6 R2, Fire Lv11 R4, Shadow Lv17 R7, Celestial Lv22 R11) and the
  "every ~5 levels" step (22 -> 27).
- Lv26 at R16 gives R16-R19 players something to buy (today nothing in the Sling line after R13).
- At R20 the player earns ~$533M/s (sim). Lv26 = 14 min of that income, Lv27 = 27 min, Lv30 = 3.3 h. That's cheap
  next to R21 ($40T), but so are the other area doors (Thunder Lv6 = 1.5% of R3). It's fine because the real gate is
  the R20 lock.
- Launch speed at Lv30 = 457 (Lv25 = 423). `SlingshotServer` takes `SlingMaxSpeed` with no cap, and `UpgradeServer`
  line 36 clamps to `U.SLING_MAX`. Test one Lv30 flight: streaming/landing, flight about 8.3 s.
- **Robux +1 LV: a new band is needed.** Today `ShopConfig.UpgradeProducts.Sling` stops at `{upTo = 25, price = 50}`
  (line 110) and `upgradeProduct("Sling", 26)` returns nil, so Lv26+ can't be bought with Robux.
  **Needs the owner's OK + a new developer product (do NOT create it):** `{upTo = 30, id = <new>, price = 65}`.
  The price follows the band steps 8 / 15 / 25 / 40 / 50.

## 3. Rebirths R21-R25

The rules stay the same: money + a pet, +1 pet slot and +0.25x money/speed each. The base is already at max size from R5.
Costs were tuned with `glacier_sim.py --tune`, so each run takes about as long as R20's run (+8-15% a step), then rounded.
The x3 jump at R22 matches the pattern at every new area (R12 -> R13 x3.75, R8 -> R9 x5): the first pet of a new
area is cheap, and the next rebirth jumps once that area's income arrives.

| R | Cost | Needs | Pet slots | Money/Speed | Run after the update (sim, play h) |
|---|---|---|---|---|---|
| 15 (today) | $4T | Celestial 5K+ KG | 18 | x4.75 | 4.4 |
| 16 (today) | $6.5T | Celestial 10K+ KG | 19 | x5.0 | 6.4 |
| 17 (today) | $9.5T | Celestial 25K+ KG | 20 | x5.25 | 6.0 |
| 18 (today) | $13T | Celestial 50K+ KG | 21 | x5.5 | 6.4 |
| 19 (today) | $19T | Celestial 100K+ KG | 22 | x5.75 | 8.5 |
| 20 (today) | $32T | Celestial 1M+ KG | 23 | x6.0 | 15.0 |
| **21** | **$40T** | **Glacier pet** | 24 | x6.25 | 12.2 |
| **22** | **$130T** | **Glacier 1K+ KG** | 25 | x6.5 | 14.0 |
| **23** | **$230T** | **Glacier 10K+ KG** | 26 | x6.75 | 18.0 |
| **24** | **$350T** | **Glacier 100K+ KG** | 27 | x7.0 | 18.0 |
| **25** | **$500T** | **Glacier 1M+ KG** | 28 | x7.25 | 22.5 (P90 24) |

Paste into `ReplicatedStorage.RebirthConfig`:

```lua
RebirthConfig.MAX_REBIRTH = 25 -- line 22
RebirthConfig.AREA_NAMES = {"Grass", "Water", "Thunder", "Fire", "Shadow", "Celestial", "Glacier"} -- line 26
-- append after line 51 ({cost = 32000000000000, area = 6, kg = 1000000},):
	{cost = 40000000000000, area = 7, kg = 1}, -- R21 (Glacier opens at R20: Slingshot Lv27)
	{cost = 130000000000000, area = 7, kg = 1000},
	{cost = 230000000000000, area = 7, kg = 10000},
	{cost = 350000000000000, area = 7, kg = 100000},
	{cost = 500000000000000, area = 7, kg = 1000000}, -- R25: a lucky 1M+ KG Glacier egg (~1 in 258 eggs, 36 h hatch)
```

Also update the header comments (lines 7-9, 28-30). `petMeets`, `requirementText` and `isMax` work for area 7 as they
are. **R25 = 28 pets on a 60 x 90 plot:** `HubV2Tests` line 358-360 only checks 23 (R20). Add a 28-pet check
because big pets may crowd.

## 4. The Glacier Egg

| Number | Today (Celestial) | Glacier (proposed) | Where |
|---|---|---|---|
| `AREA_INCOME` | $55K | **$300K** | `CreatureConfig` line 160 |
| `AREA_HATCH` | 1 | **2** | `CreatureConfig` line 107 |
| `KG_MAX` | 500K | **800K** | `EggSpawner` line 36 |
| `KG_SKEW` | 2.2 | **2.0** | `EggSpawner` line 37 |
| `KG_LUCKY_ODDS` (1 in N) | 250 | **180** | `EggSpawner` line 38 |
| `KG_LUCKY_MAX` | 5M | **10M** (= AdminLogic.KG_MAX, the luck cap) | `EggSpawner` line 39 |

Each of these continues the step between the areas before it (x1.6, -0.2, x0.72, x2). One Glacier egg: 1K+ KG 1 in 3,
10K+ 1 in 6, 100K+ 1 in 12, **1M+ 1 in 258** (Celestial 1 in 703, Shadow ~1 in 2,000), 2.5M+ 1 in 1,039.

**AREA_INCOME $300K checked:** the average money of a picked egg (best of 4) goes up x6.6 from Celestial to Glacier.
Earlier steps: Fire to Shadow x6.6, Shadow to Celestial x6.0. So the x5.5 base step lands right in line.

**Hatch times** (`max(10, 32400 x AREA_HATCH x (KG/200K)^0.43)`, real clock, keeps going offline):

| KG | 1 | 100 | 1K | 10K | 100K | 200K | 1M | 2.5M | 10M |
|---|---|---|---|---|---|---|---|---|---|
| Celestial (today) | 3 min | 21 min | 55 min | 2.5 h | 6.7 h | 9 h | 18 h | 27 h | 48 h |
| **Glacier** | 6 min | 41 min | 1.8 h | 5 h | 13.4 h | 18 h | **36 h** | 53 h | **97 h** |

(If 97 h for a 10M egg feels too much: `AREA_HATCH[7] = 1.5` gives 1M 27 h, 10M 73 h. Owner's choice.)

**The 6 pets** (money bonus = `max(1, (50/odds)^0.35)`, raw $/s before rebirth/Index/pass boosts):

| Pet | Odds | Bonus | 1 KG | 1K KG | 100K KG | 1M KG | Sell (1 KG pet, 120 s) |
|---|---|---|---|---|---|---|---|
| Frostfang Lynx | 50% | x1.00 | $300K | $1.69M | $5.33M | $9.49M | $36M |
| Ice Mammoth | 26% | x1.26 | $377K | $2.12M | $6.71M | $11.9M | $45M |
| Glacier Yeti | 14% | x1.56 | $468K | $2.63M | $8.33M | $14.8M | $56M |
| Blizzard Roc | 7.4% | x1.95 | $586K | $3.29M | $10.4M | $18.5M | $70M |
| Permafrost Titan (secret) | 2.5% | x2.85 | $856K | $4.81M | $15.2M | $27.1M | $103M |
| Frostcrown Dragon (mythic) | 0.1% | x8.80 | $2.64M | $14.9M | $47M | $83.5M | $317M |

Sum = 100. Heavy eggs are luckier: the 0.1% Dragon is 0.19% at 1K KG, 0.23% at 100K and 0.26% at 10M.
**Egg sell value** (60 s of Frostfang Lynx at the egg's KG, `SellConfig` automatic): 1 KG $18M, 1K $101M,
100K $320M, 1M $569M, 10M $1.01B.

## 5. +1 pet per existing area

All 7 new tables **sum to 100** (checked). New pets marked *. `chance` and `rarityMult` are worked out from the odds
when the game loads, so every owned pet's bonus updates by itself.

| Area | Pet | Odds today -> new | Money bonus today -> new | Owned pets' $/s |
|---|---|---|---|---|
| Grass | Bramble Badger* | new 40% | x1.08 | - |
| | Mossback Tortoise | 52 -> 30 | x1.00 -> x1.20 | **+20%** |
| | Forest Stag | 28 -> 16 | x1.22 -> x1.49 | **+22%** |
| | Treant | 13 -> 8.5 | x1.60 -> x1.86 | **+16%** |
| | Venom Basilisk | 5 -> 3.5 | x2.24 -> x2.54 | **+13%** |
| | Thornblade Mantis (secret) | 2 -> 2 | x3.09 | 0 |
| Water | Kappa | 53 -> 45 | x1.00 -> x1.04 | +4% |
| | Sea Turtle Warrior | 27 -> 25 | x1.24 -> x1.27 | +3% |
| | Coral Crusher* | new 15% | x1.52 | - |
| | Kraken | 13 -> 9 | x1.60 -> x1.82 | **+14%** |
| | Hammerjaw Shark | 5.5 -> 4.5 | x2.17 -> x2.32 | +7% |
| | Abyssal Orca (secret) | 1.5 -> 1.5 | x3.41 | 0 |
| Thunder | Raiju | 54 -> 50 | x1.00 | 0 |
| | Thunder Bull | 26 -> 25 | x1.26 -> x1.27 | +1% |
| | Storm Wyvern | 14 -> 14 | x1.56 | 0 |
| | Volt Rhino* | new 6% | x2.10 | - |
| | Thunderbird | 5 -> 4 | x2.24 -> x2.42 | +8% |
| | Thunder Rex (secret) | 1 -> 1 | x3.93 | 0 |
| Fire | Molten Boar | 54 -> 53.5 | x1.00 | 0 |
| | Lava Golem / Cerberus / Ivonrath / Inferno Phoenix | same | same | 0 |
| | Cinder Overlord* | new 0.5% | x5.01 | - |
| Shadow | Shade Panther | 54 -> 50 | x1.00 | 0 |
| | Nightmare Stallion | 27 -> 25 | x1.24 -> x1.27 | +3% |
| | Wraith Hound* | new 10% | x1.76 | - |
| | Black Eastern Dragon | 13.5 -> 9.5 | x1.58 -> x1.79 | **+13%** |
| | Pharaoh Asparuh / Abyss Weaver | same | same | 0 |
| Celestial | Solar Lion | 55 -> 54.9 | x1.00 | 0 |
| | Griffin / Celestial Dragon / Cvetibara / Cosmic Leviathan | same | same | 0 |
| | Eclipse Seraph* | new 0.1% | x8.80 | - |

- **Direction confirmed:** lower odds give a HIGHER bonus. **No owned pet loses money.** Every existing pet stays the
  same or goes up (0 to +22%).
- **Is it a problem? No.** The average bonus of a 1 KG egg goes up: Grass +7.5%, Water +7.3%, Thunder +5.1%,
  Shadow +6.1%, Fire +1.6%, Celestial +0.6%. That's a small boost to the early game, where we want it easy.
  Egg sell values go up +8% in Grass (the 1st creature is now the x1.08 Badger) and +4% in Water. The rest are unchanged.
- **Side effects to know:**
  - The list order moves. Grass pets all shift +1, Kraken and Black Dragon move from 3rd to 4th. That changes the
    Index card order and the heavy-egg luck. Inferno Phoenix and Cosmic Leviathan become 5th of 6: at 10M KG their
    luck is x3.4 instead of x4.
  - Players will see the old starter pets' % drop (e.g. Mossback Tortoise 52% -> 30%).
  - The CreatureConfig comment "minimum 1 %" (line 11-12) must say 0.1%.
- **Index cost (owner decision).** To claim an area you must find every pet in it. Median eggs needed (best-of-4
  eggs): Fire 25 -> **82**, Celestial 40 -> **322**, Glacier **326**. Grass/Water/Thunder/Shadow stay at 31-43.
  In the sim most free players never claim Fire/Celestial/Glacier, which makes R20 about +2.5 h slower (69 -> 71.5 h).
  The upside: the version bump lets veterans claim every area again (up to +35% money AND speed for a full
  collector). Options: (a) keep it, a long collection goal; (b) mythic cards don't block the claim.

## 6. Waves in Glacier

**Today waves are NOT per area.** `WaveServer` rolls one shared rhythm (Normal 55, Medium 90, Fast 140, Hyper 230
announced, Jump 120, Swinging 70) from `WaveConfig.StartZ` (-2500) to the gate. The sim's "walk speed per area" is
how fast you must be to farm an area safely (outrun the waves that pass you): Water 58, Thunder 75, Fire 92,
Shadow 115, Celestial **141** (just faster than Fast 140).

- Moving `StartZ` to -2900 doesn't make areas 1-6 harder. The spawn rhythm is the same, so the same number of waves a
  minute pass every spot. Each wave just reaches the hub later (Normal +7.3 s, Fast +2.9 s).
- **Recommended: a Glacier-only `BLIZZARD WAVE` at 155 studs/s.** That's a small +11% step over Fast 140, still far
  under Hyper 230. It rolls only from -2900 to the Glacier gate (-2460) and breaks there, so areas 1-6 are unchanged.
  It runs on its own timer, every 18-30 s, and never joins the shared rhythm.

| | Walk needed | Speed needed | Treadmill time at that point (sim median) |
|---|---|---|---|
| Celestial (today) | 141 | 750M | ~3 min at R20 (x14, Speed x6.3) |
| **Glacier, Blizzard 155** | **156** | **3.17B** | **12 min at R20** (x14) / 17 min on x10 / 9 min at R24 (x16, x7.35) |
| Glacier, Blizzard 160 (harder) | 161 | 5.12B | 19 min at R20 / 27 min on x10 |
| No new wave | 141 | 750M | Glacier is only longer, not harder |

Speed resets every rebirth, so the 12 min is paid again each R21-R25 run. That's the reason for 155 over 160.

Code shape for the integrator (`WaveConfig`):

```lua
StartZ = -2900, -- line 5: far end of Glacier (its floor ends at -2860)
-- in Config.Types:
Blizzard = { -- Glacier only (2026-10-27): never in the shared rhythm (Weight 0), own loop in WaveServer
	Name = "BLIZZARD WAVE", Speed = 155, Height = 53, Length = 75, Weight = 0,
	StartZ = -2900, EndZ = -2460, -- rolls through Glacier and breaks at the Glacier gate
	Accent = Color3.fromRGB(190, 235, 255), Spray = 2,
},
-- line 60-62 / 102-104: per-type start and end
function Config.FrontZ(t, start, now) return (t.StartZ or Config.StartZ) + t.Speed * (now - start) end
function Config.TravelTime(t) return ((t.EndZ or Config.EndZ) - (t.StartZ or Config.StartZ)) / t.Speed end
```

Also: `WaveServer.pickType` (lines 40-52) must skip `Weight == 0`. A roll of exactly 0 could otherwise pick it.
Add one more loop with an 18-30 s gap that obeys `noWaves()` and the pause. In the hit check (lines 193, 196),
`Config.EndZ` becomes `t.EndZ or Config.EndZ`. `WaveClient` lines 419-422 and 462 need the same per-type end.
It also needs a `WaveModels.Blizzard` model (AREA7 plan).

## 7. Pacing

Dedicated free player, 3 h/day + offline hatching (`glacier_sim.py`, 24 seeds, medians; P90 from 40 seeds).

| Milestone | Today: play h (day) | Glacier update: play h (day) |
|---|---|---|
| First Water / Fire / Shadow egg | 0.1 / 1.2 / 3.6 h | same |
| First Celestial egg | 12.1 h (day 4) | 12.2 h (day 4) |
| Sling Lv26 (R16) | - | 36 h (day 12) |
| R20 | **69 h (day 23)** | 71.5 h (day 23.5) |
| Sling Lv27 + **first Glacier egg** | - | **72 h (day 23.6)**, P90 78 h |
| R21 | - | 84 h (day 27.6) |
| Sling Lv30 | - | 99 h (day 32.5) |
| Treadmill x16 / x18 | never | 87 h / 104 h |
| **R25** | - | **154 h (day 51)**, P90 168 h |
| Income at the end | $592M/s at R20 | $4.2B/s at R25 |

Playing with no breaks (`--continuous`), long hatches eat play time: today's R20 takes 144 h, the update's R20
152 h and R25 353 h.

**Flags:**
- **Not trivially fast:** every R21-R25 run is 12-22 h of play, the same size as R20's run (13-15 h). No Glacier rebirth
  can be done the day it opens without the money.
- **Not impossibly slow:** the worst run (R25, a 1M+ Glacier egg = about 65 trips + a 36 h hatch) is 22.5 h, P90 24 h.
  Offline hatching covers the 36 h overnight.
- Glacier is late content: the first Glacier egg comes at ~72 h of play (day 24 at 3 h/day). Very few of today's
  players will see it. The 6 "+1" pets are what everyone gets.
- Treadmill x20 ($200T) is still never bought by a free player before R25. It stays a Robux / after-max goal, as today.
- A maxed R20 player who saved money can buy Lv26-27 at once ($1.3T) and may hit R21 on day one. That's fine.
- Skip Hatch is 13 R$ for any egg, so on 36-97 h Glacier eggs it becomes a much bigger deal (no change proposed).

## 8. Systems inventory (every place that knows "6 areas" or needs a Glacier entry)

| Script : line | Today | Change |
|---|---|---|
| `RS.UpgradeConfig` 1-14, 22-25, 48-57, 87 | 6 AREAS, SLING_MAX 25, locks to Lv25 | see section 2 |
| `RS.RebirthConfig` 7-9, 22, 26, 28-52 | MAX 20, 6 AREA_NAMES, LADDER to R20 | see section 3 |
| `RS.CreatureConfig` 11-13 | `c(name, display, motion, odds, secret)`, "minimum 1 %" | add a 6th arg `mythic`; comment 0.1% |
| `RS.CreatureConfig` 15-56 | 6 eggs x 5 pets | new 6-pet lists + `GlacierEgg = {area = 7, list = {...}}` (odds from section 4/5). Flag **Cinder Overlord, Eclipse Seraph, Frostcrown Dragon `secret = true, mythic = true`**; Permafrost Titan `secret = true`. Internal names e.g. `BrambleBadger`, `CoralCrusher`, `VoltRhino`, `CinderOverlord`, `WraithHound`, `EclipseSeraph`, `FrostfangLynx`, `IceMammoth` (the old unused model's name), `GlacierYeti`, `BlizzardRoc`, `PermafrostTitan`, `FrostcrownDragon`; motion per pet plan |
| `RS.CreatureConfig` 78-80 | byName record | add `mythic = cr.mythic` |
| `RS.CreatureConfig` 107 / 160 | AREA_HATCH / AREA_INCOME 6 values | add `2` / `300000` |
| `SSS.EggSpawner` 36-39 | KG tables x6 | add 800000 / 2.0 / 180 / 10000000 |
| `SSS.EggSpawner` 73-80 + `ServerStorage.Assets.Eggs` | ICONS x6, egg templates with `Area` attr | `GlacierEgg` icon + a `GlacierEgg` template with `Area = 7` |
| `RS.WaveConfig` 5, 26-53, 60-62, 102-104 | StartZ -2500, shared types | StartZ -2900 + Blizzard (section 6) |
| `SSS.WaveServer` 40-52, 101-136, 193-196 | one rhythm, Config.EndZ | skip Weight 0, Blizzard loop, per-type EndZ |
| `SPS.WaveClient` 419-422, 462 | Config.EndZ | per-type EndZ |
| `workspace.Map.Bounds` | Runway_End -2470, L/R_1..2 | Runway_End -2870, add L_3 / R_3 (section 1) |
| `workspace.Map.Runway` | Area1..6 | `Area7_Glacier` (section 1) |
| `RS.StreakConfig` 27-28 | EGG_KG / SECRET_KG x6 | add **800000** / **400000** (Day 7 = Permafrost Titan 400K = $21.5M/s raw) |
| `RS.StreakConfig` 30-37 | EGG_ICONS x6 | add GlacierEgg |
| `RS.StreakConfig` 76 | `info.secret` (pairs order is random!) | **`info.secret and not info.mythic`**, or Day 7 could hand out a 0.1-0.5% pet |
| `RS.PlaytimeConfig` 52 | `not info.secret` | OK as is **only if** mythics are also `secret = true` (else the 2 h gift = the area's last pet = a mythic) |
| `RS.StarterPackConfig` 15-17, 56 | Magma/Shadow egg, `secret` silhouette | no change (mythics flagged secret show as silhouettes); popup now lists 6 lines (`StarterPackClient` 269 sizes by count, check visually) |
| `SSS.ChatAnnounce` 24, 69-86 | secrets always announced, huge 1M+ | mythics already always announced (secret). Optional: a `★ MYTHIC!` line, priority 4 (visible text = owner OK) |
| `RS.IndexConfig` 15-22 | 6 areas, versions 2/2/2/3/3/3 | versions **3/3/3/4/4/4** + `{area = 7, egg = "GlacierEgg", name = "Glacier", version = 1, colors = {icy pair}, reward = {pct = 0.05, potions = {Money = 1, Hatch = 1}}}` |
| `RS.IndexConfig` ~100-138 | PORTRAITS | 12 new portraits |
| `SPS.IndexClientLegacy` 2-8, 130, 172-180 | 6 tabs, `for slot = 1, 5`, CARD_W 0.174, "x/21" | 7 tabs, 6 cards, 42 total. **Visible UI: mockup + owner OK first** |
| `RS.CreatureVFX` 69-102, 142-161 | per-pet particles, ELEMENT map, AURA x6 | add 12 pets + a Glacier aura. **Unknown names fall back to the Celestial gold aura (line 161)** |
| `RS.PetEventFX` | per-pet entries | only for new pets with clip events |
| `SPS.HatchClient` 25-31 | SHELL colours x6 (falls back to WoodEgg) | add GlacierEgg |
| `SPS.PetsEggsUI` 36-43 | EGG_ICONS x6 | add GlacierEgg |
| `SPS.InventoryClient` 22-39 | EGG_ICONS, EGG_AREA, AREA_COLOR x6 | add GlacierEgg = 7 + an icy colour |
| `SPS.SellClient` 35-43 | EGG_ICONS, EGG_AREA, AREA_COLOR x6 | same as InventoryClient |
| `SSS.Analytics` 34 | A.AREAS x6 | add "Glacier" (Area Ladder step 7) |
| `SSS.Analytics` 80 | buckets up to "R16-20" | `r <= 20 and "R16-20" or "R21-25"` |
| `RS.WeatherConfig` 10 | AREAS = 6 | **owner pick:** 7 (weathers visit Glacier, 1/7 of the time in an almost empty area) or keep 6 at launch |
| `RS.ShopConfig` 109-110 | Sling bands to upTo 25 | `{upTo = 30, id = <new>, price = 65}`, **owner OK, never create** |
| `SPS.AdminBannerClient` 171-175, UFO/MeteorClient | read RebirthConfig.AREA_NAMES | automatic once "Glacier" is added |
| `SSS.MapGuard`, `SellConfig`, `UpgradeServer`, `RebirthServer`, `RebirthClientLegacy`, `TutorialClient` 479-481, `IntroCutscene` (END_Z = gate) | - | no change (read the configs) |
| Tests: `RebirthV6Tests` 7-10, `StreakTests` 53-59, `WeatherTests` 67, `HatchRISTests.index_client` 113-114 / 211, `HubV2Tests` 358-360 | copies of 20 rebirths, 6 areas, 5 cards, 23 pets | update to 25 / 7 / 6 / 28 |

## Where this differs from AREA7_PLAN.md (use these numbers)

| Item | AREA7_PLAN | This plan (sim-checked) |
|---|---|---|
| Lv26-30 range | 2300 + 75 x (L - 25) | the same 77.2-stud line (Lv27 opens Glacier either way) |
| SLING_REBIRTH 26-30 | 16, 20, 21, 22, 23 | **16, 20, 20, 22, 22** (pairs, like Celestial). It must have all 30 entries: `rebirthNeeded` returns 0 for a missing level |
| AREA_HATCH[7] | 1.5 | **2.0** (1.5 is option 6 below) |
| AREA_INCOME[7] | 302500 | **300000** |
| Side bounds | stretch L_2 / R_2 to 1617 long | add L_3 / R_3. Either works |
| Waves | StartZ -2900, any speed change = global | StartZ -2900 + a **Glacier-only** Blizzard (no global change) |

## Owner decisions needed

1. **R21-R25 ladder** above ($40T / $130T / $230T / $350T / $500T, Glacier 1 / 1K / 10K / 100K / 1M KG), so R25 takes
   ~154 h of play (~day 51 at 3 h/day).
2. **Robux +1 LV band for Lv26-30** (new product, 65 R$ suggested). Without it, Robux can't skip the Glacier lock.
3. **Glacier wave:** Blizzard 155 (recommended), 160 (harder), or none.
4. **Index + mythics:** mythics block the area claim (Celestial/Glacier ~320 eggs), or they are bonus cards.
5. **Weather in Glacier** (WeatherConfig.AREAS 7) or not.
6. `AREA_HATCH[7]` 2.0 (1M = 36 h, recommended) or 1.5 (27 h).
7. Optional `★ MYTHIC!` chat line (visible text).
