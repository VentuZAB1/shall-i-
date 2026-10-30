# SLINGSHOT economy v4: design

Date: 2026-10-05.

**Background:**
- Research: `reports/Roblox simulator economy progression.md`.
- Pacing model: `economy/pacing_model.py`. Every number below comes from that model and was re-checked with it. It simulates a free player: egg trips, waves, hatch times, treadmill training and shopping.

**Decisions:** the user answered "no preference" on 2026-10-05, so my recommendations apply:
1. Rebirth resets **Money and Speed**. Pets, eggs, slots, upgrades, treadmill tier, the Index and Robux items are always kept.
2. Robux "Double Speed" (stack up to x1024) becomes a **30-minute x2 Speed Potion**.
3. A fresh start for everyone. The game moves to a new save slot (`PlayerData_v2`), so old saves are kept but no longer loaded. The user's own save is the one item still to confirm: start fresh (recommended) or keep the old one.

## Goals (pacing for a free, engaged player, measured in time in a server)

| Milestone | Target | Model result (free) | Model result (x2 Money pass + x4 speed) |
|---|---|---|---|
| First rebirth | ~15 min | 15 min | 11 min |
| End of day 1 (3 h) | Fire, rebirth 6–7 | R7 at 3.4 h | R9 at 3 h |
| Celestial (rebirth 12) | ~11 h | 10.8 h | 6.1 h |
| Max rebirth (20) | ~60 h | 59.4 h | 32.9 h |
| Walk speed 250 (cap) | months (trophy) | ~900 treadmill h | ~230 treadmill h |

Each run takes about 1.22 times as long as the previous one: 15 min for R1, about 11 h for R20.

## Rebirth

- **Price** is the money for rebirth number `n`. **Needs a pet:** you must own (base or hotbar) a pet from that area of at least this KG. The pet is not used up.
- Each rebirth gives **+1 pet slot** and **+0.25x money and speed**.
  - Slots = 3 + rebirths, so 23 at R20.
  - Multiplier = 1 + 0.25 × rebirths, so x6 at R20.
  - Rebirths 1–5 still grow the base, with the same fence styles.
- **Resets:** Money to $0 and Speed to 10M (walk 48, the same as a new player).
- **Cap:** `MAX_REBIRTH = 20` at launch.
- **Raising the cap later:** rebirth 21 and up costs $14T × 1.5^(n−20) and needs a Celestial pet of at least 1M KG.

| n | Price | Needs a pet | n | Price | Needs a pet |
|---|---|---|---|---|---|
| 1 | $250K | Water (any) | 11 | $80B | Shadow 10K+ KG |
| 2 | $2M | Water (any) | 12 | $250B | Celestial (any) |
| 3 | $7M | Thunder (any) | 13 | $900B | Celestial 100+ KG |
| 4 | $50M | Thunder 100+ KG | 14 | $1.5T | Celestial 1K+ KG |
| 5 | $125M | Fire (any) | 15 | $2.25T | Celestial 5K+ KG |
| 6 | $500M | Fire 100+ KG | 16 | $3.5T | Celestial 10K+ KG |
| 7 | $2B | Fire 1K+ KG | 17 | $5T | Celestial 25K+ KG |
| 8 | $5B | Shadow (any) | 18 | $6.5T | Celestial 50K+ KG |
| 9 | $20B | Shadow 100+ KG | 19 | $9T | Celestial 100K+ KG |
| 10 | $50B | Shadow 1K+ KG | 20 | $14T | Celestial 1M+ KG (lucky egg) |

## Speed

- **Walk-speed curve:** unchanged. Areas are gated by how fast you can outrun their waves (walk 58 / 75 / 92 / 115 / 141). That needs Speed 16.5M / 114M / 1B / 10B / 110B.
- **Treadmill tiers** are kept forever. Each costs about 30% of the rebirth where its speed becomes necessary.

| Tier | Name on the sign | Speed/s (x1) | Money | Robux skip |
|---|---|---|---|---|
| 1 | x1 | 50K | free | – |
| 2 | x6 | 300K | $1M | 49 |
| 3 | x40 | 2M | $50M | 99 |
| 4 | x240 | 12M | $2.5B | 199 |
| 5 | x1.5K | 75M | $50B | 399 |
| 6 (new, gold) | x10K | 500M | $2T | 799 |

- **Speed gained per second** = tier rate × rebirth multiplier × (1 + Index bonus) × x2 Speed pass × x2 potion.
- **Robux speed** tops out at x4 (the pass plus the potion), down from x2048.
- **Speed Potion:** 129 R$, x2 for 30 min. Buying again adds 30 min, up to 4 h banked. The time is saved, so it carries over to new servers.

## Upgrade stall (bought once, kept forever)

- **Slingshot Power:** level L costs $25K × 1.95^(L−1), rounded to 2 significant digits.

  | Area reached | Level | That level's price | Total to get there |
  |---|---|---|---|
  | Water | 1 | $25K | $25K |
  | Thunder | 6 | $700K | $1.4M |
  | Fire | 11 | $20M | $41M |
  | Shadow | 17 | $1.1B | $2.3B |
  | Celestial | 22 | $31B | $64B |
  | Max | 25 | $230B | $474B |

  The ranges are unchanged.
- **Fast Grab:** $100K / $5M / $250M / $10B / $500B. Hold time 1.5 → 1.2 → 0.9 → 0.6 → 0.4 → 0.2 s.
- **Wave Shield:** 1 level, **$25B**. That is where "very expensive, like $1B" sits in the new economy, about the R9 price. The user can say if they want a different number.

## Index

- Claiming a completed area gives **+5% money and +5% speed forever** (attribute `IndexBonus`). The maximum is +30%.
- It no longer pays one-time cash or speed, which would be wiped by the next rebirth.

## Money multiplier (one shared formula, `ReplicatedStorage.Boosts`)

- Money = (1 + friend% / 100) × (1 + 0.25 × rebirths) × (1 + IndexBonus) × x2 Money pass.
- Speed = (1 + 0.25 × rebirths) × (1 + IndexBonus) × x2 Speed pass × x2 potion.
- Server and client displays (pet tags, Pets panel, HUD) all use these. Today the client displays leave out the Money pass.

## Unchanged

- Pet income: area base × KG^¼.
- Egg sizes and lucky eggs.
- Hatch times.
- Selling: a pet sells for 120 s of income, an egg for 60 s.
- Playtime gifts: already a share of your current income and speed.
- Friend boost.
- The x2 Money and x2 Speed passes, and the VIP and Growth passes.

## Long-term goals (only what's needed)

- **New leaderboards:** **MOST REBIRTHS** (attribute `Rebirths`) and **HEAVIEST PET** (attribute `BestKg`, the heaviest pet ever hatched, from the Index). They go on the hub's empty side walls, next to RICHEST PLAYERS and MOST TIME PLAYED.
- **Player list:** a `Rebirths` column in the in-game player list (leaderstats).
- **Rebirth page:** always shows the next goal: price, required pet ✔/✗, or MAX.
- **Saves:** `PlayerData_v2` and leaderboard stores `_v2`, so everyone starts fresh and old data is kept untouched.

## Out of scope (later, if data shows the need)

- Offline income.
- Weekly limited eggs/events.
- A MAX chat title.
- Trading.
- A second prestige layer.
