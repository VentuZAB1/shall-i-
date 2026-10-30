# Make Every Rebirth Cost Time, Not Just Money

SLINGSHOT for Pets runs too fast for three reasons. A rebirth resets nothing. Rebirth prices grow by a fixed x4 that has no link to income. Paid speed boosts multiply by x1024, which buries every free source of speed. The hit games this note looks at handle the same problem the same way. Steal a Brainrot (SaB), Escape Tsunami for Brainrots (ETFB), Pet Simulator 99 (PS99) and the classic speed simulators all wipe the main currency or stat on rebirth. All of them keep the collection. Each gives a small, mostly additive bonus per rebirth. Most also block late rebirths behind owning a specific rare unit, so money alone cannot buy them. A cap on rebirths is raised in weekly updates, so nobody ever "finishes".

The fix proposed here is about a dozen changes, not a new game. Rebirth resets **Money and Speed** and keeps pets, slots and upgrades. The rebirth bonus becomes **+0.25x money and speed** plus +1 slot. There are **20 rebirths at launch**, each needing money plus a pet from the right area. Prices are taken from a target *play-time* per rebirth that rises about **x1.22** each time: roughly 15 minutes for Rebirth 1 and 11 hours for Rebirth 20. Robux speed is capped at **x4 total**. On this plan an engaged player reaches Fire on day 1, Celestial after about 11 hours of play, and max rebirth after about 60 hours. KG hunting, the Index, leaderboards and weekly content carry the game past that.

Every number below comes from a model, not from playtests. Tune them with live analytics, and wipe the tester saves before launch.

## The recommended redesign: tables you can paste into config

**What rebirth resets and what it keeps.** Rebirth resets **Money to $0 and Speed to 10M**, which is walkspeed 48. It keeps:

- all pets, eggs and Index progress
- pet slots and treadmill tiers
- the Upgrade-stall levels (Slingshot Power, Fast Grab, Wave Shield)
- Robux purchases

ETFB, the closest competitor to our tsunami loop, does the same: it resets Speed and keeps brainrots and the base ([AllThingsHow](https://allthings.how/how-rebirth-works-in-escape-tsunami-for-brainrots-all-20-levels/)). Kept pets keep paying from the first second of the next run, so each run gets back to the last wall quickly. That is the "visibly faster each run" feeling Pecorella calls essential ([Quest for Progress, GDC 2016](https://www.slideshare.net/slideshow/quest-for-progress-gdc-europe-2016/65405507)).

**Core formulas** (r = rebirths owned):

```
Pet slots        = 3 + r                         (max 23 at R20)
Rebirth mult     = 1 + 0.25 * r                  (applies to money AND speed gain)
Money/s per pet  = AREA_INCOME[area] * KG^0.25   (unchanged: 8 / 50 / 300 / 1.8K / 10K / 55K)
Total money/s    = sum(pets) * RebirthMult * FriendMult(<=1.5) * MoneyPass(x2) * [timed potion x2]
Speed gain/s     = TreadmillTierGain * RebirthMult * SpeedPass(x2) * [timed Speed Potion x2]   (Robux cap x4)
Rebirth cost r   = table below; beyond R20: Cost(r) = $400B * 1.35^(r-20)
Slingshot Lv L   = $1K * 2^(L-2)                  (L = 2..25; doubles each level; all 25 ~ $16.8B)
Walkspeed        = keep the current log curve (10M->48, 100M->74, 1B->92, 1T->165, 1Qa->240, cap 250)
```

**Rebirth ladder.** Each rebirth needs the money and a qualifying pet (in the base or in storage). "Top X%" means the pet's KG is in the top X% of that area's normal egg rolls. Set the KG cut-offs from your real KG distribution. Target time is active or in-server play time for a free player with no passes.

| R | Cost | Pet required | Gets | Target time for this rebirth | Cumulative play |
|---|---|---|---|---|---|
| 1 | $100K | any Water pet | +1 slot, x1.25, base grows | 15 min | 0.25 h |
| 2 | $250K | any Water pet | +1 slot, x1.5, base grows | 18 min | 0.6 h |
| 3 | $2.5M | any Thunder pet | +1 slot, x1.75, base grows | 22 min | 0.9 h |
| 4 | $5M | Thunder, top 50% KG | +1 slot, x2.0, base grows | 27 min | 1.4 h |
| 5 | $50M | any Fire pet | +1 slot, x2.25, base max + fence style | 33 min | 1.9 h |
| 6 | $85M | Fire, top 50% | +1 slot, x2.5 | 40 min | 2.6 h |
| 7 | $125M | Fire, top 20% | +1 slot, x2.75 | 50 min | 3.4 h |
| 8 | $1.2B | any Shadow pet | +1 slot, x3.0 | 1.0 h | 4.4 h |
| 9 | $1.75B | Shadow, top 50% | +1 slot, x3.25 | 1.2 h | 5.7 h |
| 10 | $2.5B | Shadow, top 20% | +1 slot, x3.5, milestone cosmetic | 1.5 h | 7.2 h |
| 11 | $3.5B | Shadow, top 5% | +1 slot, x3.75 | 1.8 h | 9.0 h |
| 12 | $33B | any Celestial pet | +1 slot, x4.0 | 2.2 h | 11 h |
| 13 | $45B | Celestial, top 50% | +1 slot, x4.25 | 2.7 h | 14 h |
| 14 | $65B | Celestial, top 50% | +1 slot, x4.5 | 3.3 h | 17 h |
| 15 | $90B | Celestial, top 20% | +1 slot, x4.75, milestone cosmetic | 4.0 h | 21 h |
| 16 | $120B | Celestial, top 20% | +1 slot, x5.0 | 4.9 h | 26 h |
| 17 | $160B | Celestial, top 5% | +1 slot, x5.25 | 6.0 h | 32 h |
| 18 | $220B | Celestial, top 5% | +1 slot, x5.5 | 7.3 h | 40 h |
| 19 | $300B | Celestial, top 1% | +1 slot, x5.75 | 9.0 h | 49 h |
| 20 | $400B | lucky Celestial >= 1M KG | +1 slot, x6.0, "Max" title | 11 h | 60 h |

**Upgrades and speed.** Slingshot Power stays at 25 levels. The new curve puts each area at these cumulative prices:

| Level | Area reached | Price of that level | Total spent so far |
|---|---|---|---|
| 5 | Water | $8K | $15K |
| 10 | Thunder | $256K | $511K |
| 15 | Fire | $8.2M | $16M |
| 20 | Shadow | $262M | $524M |
| 25 | Celestial | $8.4B | $16.8B |

Fast Grab becomes $20K / $500K / $15M / $500M / $15B. Wave Shield moves to $2B. All three are bought once and kept, so they compete with rebirth for each run's money. That is a real decision for the player, which Pecorella says the cost curve should create ([Kongregate, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i)).

Treadmills become six tiers. Each tier costs **x100** the previous one and gains **x6** the speed. Tiers are kept through rebirth, and the old Robux tier skips stay.

| Tier | Price | Speed/s (x1) |
|---|---|---|
| T1 | free | 50K |
| T2 | $25K | 250K |
| T3 | $2.5M | 1.5M |
| T4 | $250M | 10M |
| T5 | $25B | 60M |
| T6 (post-R20 goal) | $2.5T | 400M |

Comfortable walkspeed targets per area, read off the current log curve:

| Area | Walkspeed | Speed needed |
|---|---|---|
| Grass | 48 | 10M (start) |
| Water | 60 | 3e7 |
| Thunder | 75 | 1.1e8 |
| Fire | 95 | 1.3e9 |
| Shadow | 120 | 1.4e10 |
| Celestial | 150 | 2.4e11 |
| Endgame | 200 | 2.5e13 |
| Cap | 250 | 2.5e15 |

Speed resets each run, so re-training is the "replay". In the model it takes about **7 minutes** to re-reach Water on run 1, about **9 minutes** to re-reach Shadow at R7 on T4, and about **15-18 minutes** to re-reach Celestial on T5 at R11-R16. Walkspeed 200 takes about **3 hours** on T6 at R20. The 250 cap takes roughly **290 treadmill-hours** for a free player (about 72 with x4 Robux). That makes it a deliberate, months-long trophy.

**Robux.** Keep the **x2 Money pass** and the **x2 Speed pass**. Turn the 10-stack "Double Speed" product into a **consumable 30-minute x2 Speed Potion that does not stack with itself**. Roblox's own docs say permanent power-ups belong in passes and temporary boosts in developer products ([Roblox Creator Hub: Passes](https://create.roblox.com/docs/production/monetization/passes)). Total paid speed is then **at most x4**, down from x2048.

**Additions, in priority order:**

1. The rebirth-gate check (one function).
2. `MAX_REBIRTH = 20`, raised by 3-5 in later updates.
3. Capped offline earnings, about 25% rate for up to 6 hours.
4. Two leaderboards: heaviest pet (KG) and rebirths.
5. A weekly limited egg or event on a fixed day.

Leave out second prestige layers, rebirth shops, mutations and trading until the data shows a need.

## Why the current economy collapses in about a day

**Rebirth is a free power-up, not a trade-off.** Nothing resets, so the best play is always to buy the next rebirth the instant you can afford it. The player gives up nothing and never replays anything. Every reference game makes rebirth cost something:

- SaB resets cash, brainrots and gear and keeps multiplier, slots and lock time ([U7BUY](https://www.u7buy.com/blog/steal-a-brainrot-rebirth-guide/)).
- PS99 resets coins and area progress and keeps pets ([GINX](https://www.ginx.tv/en/roblox/pet-simulator-99-rebirth)).
- Muscle Legends wipes **100% of Strength and Durability and 50% of Agility** ([ML wiki](https://muscle-legends.fandom.com/wiki/Rebirths)).
- Mining Simulator wipes coins, tools and backpacks ([Mining Simulator wiki](https://mining-simulator.fandom.com/wiki/Rebirth)).

Our rebirth is really a purchasable slot. Slots compound with ever-bigger pets, so income runs away. That is how the test account reached $1.7T.

**The x4 cost curve is not tied to anything.** It does not follow the income curve, which jumps about **x6 per area** and up to **x13-x20** more from a lucky high-KG pet. A 1M KG Celestial pet at $1.7M/s pays for the current R10 ($65.5B) in about 11 hours on its own, and a base can hold 12 of them. Two DevForum points apply. Developers report that pure exponential rebirth prices "explode" and need taming ([DevForum: Unlimited rebirths formula](https://devforum.roblox.com/t/unlimited-rebirths-formula/1848726)). The common advice is to pick a target time per rebirth and solve the price from expected income, rather than choosing price and reward separately. Our current prices are a fixed geometric series, so they turn trivial whenever income jumps faster than x4 per rebirth, which happens at every new area and every lucky pet.

**Speed is effectively Robux-only.** Free speed tops out at 16K/s. At that rate, the 1B speed needed for walkspeed 92 takes about 17 hours of treadmill time. The 2.4e11 needed for a walkspeed-150 Celestial run takes months. Ten stacked x2 purchases plus the pass (x2048) bring the same climb down to minutes. The rebirth speed bonus is *added* (+0.15 per rebirth) on top of a *multiplied* Robux stack, so free progress counts for close to nothing.

The research notes found no Roblox data on capping stacked paid boosts. The general rule from idle-game design is to keep permanent paid multipliers combined at about **x2-x4**. Sources here are the Kongregate idle-math series, which shows how a big multiplier skips a large part of an exponential cost curve, and the stacking practice of Idle Miner Tycoon ([Kongregate, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i)). Since only **3.8% of Roblox players pay anything** ([GameAnalytics 2026](https://www.gameanalytics.com/reports/2026-roblox-report)), the pacing has to work for the free path. Paid boosts should compress that path, not replace it.

**The content ceiling is too low and too cheap.** All six areas unlock through Slingshot Power for about $2B in total. At Celestial income that is minutes, so area discovery is used up on day 1. After that, nothing is left to chase except more rebirths, and those have no cap and no gate. The Index rewards are fixed amounts ($10K-$120M, 1M-600M speed). A fixed reward that matters in hour 1 is worth nothing by day 10, which is why genre guides tell you to scale rewards to current income ([Kongregate, Part III](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-iii)).

## How the hits pace progression: two gates, small bonuses, a moving ceiling

**Steal a Brainrot** prices rebirths in cash, but the real wall is a named brainrot. R1 costs only **$500K** but needs Trippi Troppi plus Gangster Footera. Costs climb to **$125B at R10** and **$30Qa at R19**. The multiplier rises from x0.5 to x19, and each rebirth adds one base slot, from 10 to a maximum of 28 ([Eldorado rebirth guide](https://www.eldorado.gg/blog/steal-a-brainrot-rebirth-guide/)). Players describe sitting on enough cash "for days waiting on the belt" for R13's unit. R16 needs the first Secret, and R19's cash alone takes "several days" even with a full base ([U7BUY](https://www.u7buy.com/blog/steal-a-brainrot-rebirth-guide/); [U7BUY R19](https://www.u7buy.com/blog/steal-a-brainrot-rebirth-19/)).

When players complained, the developers **halved the early and mid cash costs** (R1 from $1M to $500K, R15 from $500T to $100T). They kept the unit gates ([U7BUY](https://www.u7buy.com/blog/steal-a-brainrot-rebirth-guide/)). The lesson: a cheap early game plus a random, collection-based gate later spreads progress over weeks without making day 1 feel stingy. Our version is the area plus KG-percentile requirement.

**Escape Tsunami for Brainrots** is closest to our loop and gates rebirth on Speed. R1 needs **40 Speed**, and each later rebirth needs +10 more and gives +0.5x money, up to 230 Speed and x11 at R20. Speed resets on rebirth ([AllThingsHow](https://allthings.how/how-rebirth-works-in-escape-tsunami-for-brainrots-all-20-levels/)). Speed levels cost **1.17x** the previous one ([AllThingsHow caps](https://allthings.how/every-max-level-cap-in-escape-tsunami-for-brainrots-explained/)). So each rebirth costs about 1.17^10, or **about 4.8x, more cash than the last** while paying only +0.5x. That is a deliberately worsening exchange rate.

Late ETFB rebirths add income-per-second and rare-unit requirements. R24 needs **$100Qn/s plus a Divine in base**, and R25 needs **three Divines** ([Game Rant](https://gamerant.com/roblox-escape-tsunami-for-brainrots-how-rebirth-fast-all-levels/)). The rebirth cap went from 25 to 26 to 27 and then to 29 as top players caught up ([Game8](https://game8.co/games/Roblox/archives/580777)). Zones are distance bands tied to Speed thresholds, with trenches as wave shelters ([games.gg](https://games.gg/roblox/guides/escape-tsunami-for-brainrots-zones-guide/)). This is our geometry exactly, which is why speed should reset and stay meaningful.

**Steal an Egg** uses Speed as the area key. Thresholds grow **about 4-40x per biome**, from Lake at 900 to Angels & Demons at 20B, and guides advise being about 20% above the minimum because big eggs slow you down ([Eldorado](https://www.eldorado.gg/blog/steal-an-egg/steal-an-egg-biomes-and-speed-requirements/); [timesaver.gg](https://timesaver.gg/blog/steal-an-egg-how-to-get-speed-fast)). Pet income runs from **$1/s to billions per second** across those biomes ([games.gg](https://games.gg/roblox/guides/steal-an-egg-all-eggs-pets-and-income-rates/)). Sources disagree on whether it has a rebirth system at all, which suggests speed-gated areas can carry a game on their own.

**PS99 and the classic simulators** show what a rebirth usually pays. PS99 puts rebirth statues at fixed zones (25/50/75/99...), caps rebirths at 9, and gives **+75% pet strength plus a feature unlock** such as teleport, auto-hatch or pet teams ([HoldToReset](https://holdtoreset.com/pet-simulator-99-rebirth-system-explained/); [Game Rant](https://gamerant.com/pet-sim-simulator-99-rebirth-statues/)). Other per-rebirth bonuses:

- Mining Simulator: +1x
- Horse Race: +10%
- Muscle Legends: +5%

Muscle Legends notes that "rebirth multipliers barely seem to have an effect at some point" once pets dominate ([ML wiki](https://muscle-legends.fandom.com/wiki/How_Rebirthing_Works)). Horse Race shows the late-game shape: costs double per rebirth early and settle near **x1.19 per rebirth** late, while each rebirth still adds only +10% ([Horse Race wiki](https://horse-race.fandom.com/wiki/Rebirth)).

These games share a pattern. **Rebirth is the slow floor and pets are the fast ceiling.** That is why our +0.25x per rebirth is enough: the x6-per-area pet jumps do the heavy lifting.

## Why these numbers: costs, speed and time

**Rebirth costs come from time, not from a ratio.** Each price in the table is:

```
Cost(r) = 0.6 * T(r) * ExpectedIncome(r)
T(r)    = 15 min * 1.22^(r-1)
ExpectedIncome(r) = (r+2 slots) * typical pet $/s of the area the gate requires * (1 + 0.25(r-1))
```

The 0.6 allows for ramp-up time and for money spent on Slingshot, Fast Grab and treadmills during the run. Typical pet incomes are the current $70 / $470 / $3.2K / $20K / $130K per second by area.

The price ratio is therefore uneven on purpose. It jumps about **x10 when a new area becomes required**, because income also jumps about x6 there. In between, it is about **x1.3-x1.7**, while play time rises a steady 1.22x. A rule of thumb from incremental design supports this "log-time" pacing: if every milestone takes a constant factor longer than the last, each still feels equally significant, and the schedule matches how engagement decays from hourly check-ins to weekly ones ([Eric Guan](https://ericguan.substack.com/p/idle-game-design-principles)).

The first rebirth raises income by about **x1.67**: 4/3 from the extra slot times 1.25 from the multiplier. That sits inside Pecorella's guideline that players prestige when the gain is **+50% to +200%** ([Quest for Progress](https://www.slideshare.net/slideshow/quest-for-progress-gdc-europe-2016/65405507)). Mining Simulator's linear model shows the same principle from another angle: it pairs a +1x reward with a cost of 10M x (n+1) so each rebirth takes about the same grind ([Mining Simulator wiki](https://mining-simulator.fandom.com/wiki/Rebirth)). Past R20, use $400B x 1.35^(r-20) plus rising KG gates. Never let a pure exponential run unchecked, because DevForum developers report it reaching absurd values like 10^400 at high counts ([DevForum](https://devforum.roblox.com/t/unlimited-rebirths-formula/1848726)).

**Speed and upgrades should scale by tier, not by Robux.** The new treadmill ladder (x100 price for x6 gain) mirrors the geometric zone thresholds that are standard in the genre. Muscle Legends rocks go from 5K to 150K to 1M to 25M, roughly 3-10x per zone ([ML wiki: Rocks](https://muscle-legends.fandom.com/wiki/Rocks)). Steal an Egg's biomes grow about 4-40x. The +0.25x speed per rebirth then makes each replay faster: the climb back to Celestial falls from about 18 minutes at R11 to about 13 minutes at R16. That matches the guidance that each run should reach the previous wall in a fraction of the previous time.

Keep the log walkspeed curve. Big displayed numbers are fun, and real walkspeed has to be bounded because physics and readability break at high speeds. Legends of Speed lets players turn their own speed down, and Tapping Legends caps WalkSpeed upgrades at +32 ([LoS wiki](https://legends-of-speed.fandom.com/wiki/Legends_Highway); [Tapping Legends wiki](https://tapping-legends.fandom.com/wiki/Rebirth_Shop)).

Slingshot Power doubling each level ($1K x 2^(L-2)) puts Water at about 5 minutes, Thunder before R3, Fire before R5, Shadow before R8 and Celestial at about R11-R12. Because money resets, the $8.4B Lv25 purchase competes directly with R10-R11. That makes reaching Celestial the defining mid-game decision.

**Realistic timeline.** For an engaged free player (2-4 hours a day):

| When | Where they should be |
|---|---|
| First 60 s | first egg hatched |
| ~1-2 min | first Slingshot upgrade |
| ~5 min | Water unlocked |
| ~15-20 min | Rebirth 1 |
| Day 1 (3-4 h) | Fire, R6-R7 |
| Week 1 (~15 h) | Celestial, R12-R13 |
| ~60 h (weeks 3-6) | R20 |

A median Roblox player plays about **1.5 sessions of about 10 minutes a day** ([GameAnalytics 2026](https://www.gameanalytics.com/reports/2026-roblox-report)) and will take months for the same path. That is fine: they always have a next area or rebirth within reach. Payers with x2 Money and friend boosts move about 3x faster, but they still hit every pet gate. Simulator developers commonly put total length at **"1-100 hours"** and warn that what really keeps players is a steady stream of new content, not length alone ([DevForum](https://devforum.roblox.com/t/how-long-should-it-take-a-player-to-complete-your-game/3859022)).

The model rests on two assumptions to verify in playtests: a pet earning typical area income, and the KG distribution behind the percentile gates. Log time-per-rebirth and income-at-rebirth, then adjust the constants live with Roblox Configs and Experiments ([Roblox Creator Hub](https://create.roblox.com/docs/production/game-design/analytics-essentials)).

## Stopping day-one completion and giving players months of goals

**Three locks stop day-one completion.** The first is the reset, which forces a replay. The second is the pet gate. Overnight AFK income cannot buy a rebirth that needs a top-5% Celestial pet, which only active egg-grabbing can produce. This is the same role SaB's named units play ([U7BUY](https://www.u7buy.com/blog/steal-a-brainrot-rebirth-guide/)). The third is a hard **MAX_REBIRTH of 20**, raised 3-5 at a time as top players arrive, the way SaB added R14, R18 and R19 and ETFB went from 25 to 29 ([Eldorado update log](https://www.eldorado.gg/blog/steal-a-brainrot-update-log/)).

Do not slow the first hour to compensate. Roblox says low D1 points to the core loop and onboarding (ideally five minutes or less), while low D7 points to progression and unclear goals ([Roblox Creator Hub: Retention](https://create.roblox.com/docs/production/analytics/retention)). The early game must stay generous. SaB cut its early rebirth prices for exactly this reason.

**Long-term goals should reuse what already exists.** The KG^0.25 curve with 5M-KG lucky Celestials is already a months-long chase, because 16x the KG gives only 2x the income. A "heaviest pet" leaderboard turns that into status at almost no cost. Showing off bases and pets is one of the cheapest retention levers in the stealing and garden hits ([Free Systems](https://freesystems.substack.com/p/the-algorithm-behind-steal-a-brainrot)).

Turn Index area rewards into **permanent +% bonuses** (for example +3% money per completed area page) so they survive rebirths and stay meaningful. Add **capped offline income**. SaB caps offline cash at 5 hours ([Fandom](https://stealabrainrot.fandom.com/wiki/Offline_Cash)). Adopt Me's Pet Pen lets pets gain only one level before you must visit ([Adopt Me](https://www.playadopt.me/news/pet-pen-and-pet-releaser-features-notes)). Both reward checking in a few times a day rather than staying online.

Give rebirths 5/10/15/20 a visible milestone, such as a fence or base style or a title, in the PS99 tradition of feature and cosmetic unlocks. Then release on a fixed weekly day: a new creature, a limited egg, or an event. All the top games (SaB, Grow a Garden, BGSI, Adopt Me) update weekly. Roblox's own minimum advice is small updates every 2-4 weeks and big ones every 2-3 months ([Roblox Creator Hub: Retention](https://create.roblox.com/docs/production/analytics/retention)).

Hooks are not a cure-all. One developer added a weekly rewards track and saw "no positive movement at all" ([DevForum](https://devforum.roblox.com/t/feedback-why-arent-players-coming-back/4858033)). The progression spine has to come first. Analysts also noted that the 2025 viral hits "lost players quickly" once the novelty faded ([Benzinga/Jefferies](https://www.benzinga.com/trading-ideas/movers/26/09/62018983/jefferies-downgrades-roblox-sees-bookings-growth-well-below-wall-street-stock-falls)).

**Big numbers stay manageable.** Under this plan, money peaks around **$400B at R20 and $2.5T for T6**, and Speed tops out at **2.5e15**. Both are below the **~9e15 limit up to which Luau numbers hold exact integers**, so no BigNum library is needed. The existing K/M/B/T/Qa formatter is enough. If later worlds push past that, rename the currency per world, as PS99 does with Coins, then Gold Bars, then Platinum ([PS99 wiki](https://pet-simulator.fandom.com/wiki/Currencies_(Pet_Simulator_99))).

Because only testers have data, do the **full wipe now** and give testers a "Founder" badge. An unexpected wipe after launch is the case that angers players ([SAES:RPG forum](https://saesrpg.uk/forums/topic/35874-feature-economy-resetsolved/)).

## Conclusion

The real change is in how prices are set: in **minutes of play** rather than in dollars. Once each rebirth is priced as "about 1.22x longer than the last" and matched to the income the player has at that point, the jumps between areas, the lucky-KG pets and the Robux passes stop breaking pacing. Each becomes a known compressor on a time budget, and the pet gates catch any compressor that is too strong. The research also points somewhere less obvious. In every successful game, the thing that holds players for weeks is **scarcity they cannot buy**: a named brainrot, a Divine unit, a top-1% KG roll. Raw cost gives the other lever, a long grind, but scarcity is what makes the grind matter. SLINGSHOT already has the ingredient in its KG system. The redesign makes KG the gate rather than a shortcut.

The open risk is calibration. The cost table assumes typical pet incomes and a KG distribution that have not been measured in live play. Ship it with telemetry on time-per-rebirth, set the KG percentiles from real egg rolls, and expect to change the constants (not the structure) in the first two weeks.
