# Roblox Developer & Official Guidance on Retention, Session Length, and Economy Balancing (Simulator / Tycoon / Collecting)

## 1. What D1/D7/D30 retention and session length count as "good" (official Roblox guidance + benchmarks)

### Takeaway
Roblox does not publish fixed "good" numbers. Creator Analytics shows your percentile against "similar experiences" or genre benchmarks, and Roblox says to focus first on D1 retention and average session time. The best independent benchmark (GameAnalytics 2026, 500+ titles with 1M+ MAU) puts the median game at roughly D1 10.3%, D7 1.6%, D30 0.5%, with a 9.8-minute session. Top-1% games reach roughly D1 22%, D7 9%, D30 4.7%, and 21-minute sessions.

### Cited Findings
- Roblox: D1 and average session time are "key metrics to focus on first" because they show whether new users enjoy the game and come back. D7 and D30 show whether players are progressing and returning long-term. Creators should aim for session time and D1 that match or beat their similar-game benchmarks. — [Roblox Creator Hub: Analytics / Get started](https://create.roblox.com/docs/production/analytics/get-started); [Analytics overview (GitHub mirror)](https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/index.md)
- Roblox diagnosis by metric:
  - Low D1 points to the core loop, the first-time experience, or performance. Onboarding should take "ideally in 5 minutes or less after entering your game."
  - Low D7 points to progression. Fixes are "clear user goals" and "Add content variety: A variety of content, such as new modes, inventory items, and social features."
  - D30 depends on updates and social mechanics. — [Roblox Creator Hub: Retention](https://create.roblox.com/docs/production/analytics/retention)
- A drop in D1/D7/D30 for a single cohort after a big influx of new users is described as "a typical and temporary outcome." — [Roblox Creator Hub: Retention](https://create.roblox.com/docs/production/analytics/retention)
- Benchmark tools added in October 2025:
  - Retention split by acquisition source, plus a toggle between the "similar experiences" and genre benchmark sets.
  - Users arriving from "Other" have much lower D1 than users from Home Recommendations, so a change in traffic mix can move your retention without any game change. — [DevForum announcement: Analytics retention by acquisition source & benchmark set](https://devforum.roblox.com/t/analytics-view-retention-by-acquisition-source-and-select-your-benchmark-set/4010157)
- Daily cohorts (tracked over 10 days) and weekly cohorts (tracked over 10 weeks) were added in 2025. Roblox says a falling DAU/MAU ratio means new players aren't forming daily habits, and suggests experience events or better engagement hooks. — [DevForum: Track new user retention by daily and weekly cohort](https://devforum.roblox.com/t/analytics-track-new-user-retention-by-daily-and-weekly-cohort/3817030)
- Discovery ranking (Recommended For You) is engagement-driven:
  - Signals include play-through rate, first-play bounce rate, and "7 day intentional co-play days per user."
  - Engagement and retention from users acquired through ads, friends, search and similar sources is NOT counted in the ranking stage. — [Roblox Creator Hub: Discovery](https://create.roblox.com/docs/discovery); [DevForum: Improved Recommended For You algorithm](https://devforum.roblox.com/t/boost-your-discovery-with-the-improved-recommended-for-you-algorithm-and-analytics-for-creators/3587441)
- GameAnalytics 2026 Roblox Benchmark Report (500+ titles with ≥1M MAU, Aug 2025–Jul 2026, 4.76B sessions), by percentile:

  | Metric | p25 | p50 | Higher percentiles |
  |---|---|---|---|
  | D1 retention | 8.4% | 10.3% | p99 22.2% |
  | D7 retention | 1.0% | 1.6% | p99 9.1% |
  | D30 retention | 0.3% | 0.5% | p99 4.7% |
  | Session length per game (min) | 7.3 | 9.8 | p75 12.0 / p90 14.7 / p95 16.6 / p99 21.1 |
  | Sessions per player per day | 1.34 | 1.56 | p75 2.07 / p90 3.22 / p99 8.30 |

  Monetization in the same sample: 3.80% of players paid anything. Per-game ARPPU was p50 $0.70, p90 $2.33, p99 $55.31. — [GameAnalytics 2026 Roblox Benchmark Report](https://www.gameanalytics.com/reports/2026-roblox-report)
- GameAnalytics 2025 report:
  - Short-session games (0–6 min) "struggle to survive": daily sessions rarely exceed one per user and D1 is below 10%.
  - Games with 7–18 minute sessions are healthy, but play frequency stays low.
  - Core users average 37 min per session versus under 2 min for casual users. — [GameAnalytics 2025 Roblox Benchmark Report](https://www.gameanalytics.com/reports/2025-roblox-report)
- Third-party targets (unverified methodology):
  - BLOXG (marketing agency): D1 20%+ is good, 30%+ is great, below 15% means FTUE problems, and D7 below 5% is a warning sign. — [BLOXG: Low retention](https://bloxg.com/problems/roblox-game-low-retention)
  - rolearn.dev for simulators: D1 35% good / 50% excellent, D7 18% good / 28% excellent. — [rolearn.dev: First week retention](https://rolearn.dev/guidance/first-week-retention-optimization/)
  - **Conflict:** these targets are 2–10x higher than GameAnalytics' measured p99 for D7. They probably use a different definition (for example rolling or "returned at any time" retention) or are aspirational. Treat them with caution.
- Real low-end example: a developer on the DevForum reported D1 4.24%, D7 0.58% and D30 0.15%. The dashboard placed this around the 2nd percentile. — [DevForum: Help with Retention](https://devforum.roblox.com/t/help-with-retention/3882323)
- Fantasy Forest (solo-dev pet/animal game) post-mortem:
  - D1 was at least 15%, at "Top 200" levels, but session time was "below Top 1000."
  - Adding new animals and a decoration mode raised session time from about 9 to about 13 minutes.
  - The game reached 2k CCU in 4 weeks after the developer stopped ads. Roughly 40k Robux of ads in week 1 had produced only about 40 CCU. — [DevForum: Fantasy Forest post-mortem](https://devforum.roblox.com/t/from-0-to-2000-players-in-4-weeks-fantasy-forest-launch-post-mortem/2044257)

### Inferences
- For a new simulator, a realistic early goal is D1 ≥ 10–15% (median to top quartile), sessions ≥ 12 minutes (p75), and D7 ≥ 3% (well above the 1.6% median). D7 is where progression and economy pacing show up.
- Because Recommended For You only scores Home-acquired users, progression and economy problems that hurt D7 directly hurt organic reach.

### Gaps
- No official Roblox numbers for "good" D1/D7/D30 or session length were found. The thresholds are only visible per-game in the dashboard.
- No genre-specific (simulator/tycoon) breakdown was found in the public GameAnalytics summaries.
- No RDC talk transcript with retention numbers was found in this pass.

## 2. Economy balancing: rebirth/upgrade cost curves, pacing tests, fixing over-fast economies

### Takeaway
DevForum consensus is that cost growth must be balanced against income-multiplier growth. Mining Simulator pairs a linear rebirth cost with a linear +1x multiplier so each rebirth takes roughly the same grind time. Pure exponential costs explode, and hybrid or decaying-rate curves are the common fix. Developers say total length matters less than constant new content. No well-documented Roblox simulator post-mortem about a wipe or reset was found.

### Cited Findings
- Mining Simulator uses linear scaling:
  - Rebirth cost is 10,000,000 × (n+1) coins.
  - Each rebirth adds +1x to a permanent ore-value multiplier (2x after the first).
  - Tools and backpacks cost (1 + rebirths)/2 × base price, so shop prices scale with income. — [Mining Simulator Wiki: Rebirth](https://mining-simulator.fandom.com/wiki/Rebirth)
- Geometric formula: C(r) = S·R^r, for example 100·1.5^r. One developer found that price·1.1^rebirths reaches about 10^400 at 10,000 rebirths, and lowering the rate to 5% didn't help. — [DevForum: Simulator Formulas](https://devforum.roblox.com/t/simulator-formulas/853976); [DevForum: Unlimited rebirths formula](https://devforum.roblox.com/t/unlimited-rebirths-formula/1848726)
- Workaround for very high rebirth counts: grow cost by a percentage, but halve that percentage at 100, 200, 400, 800... rebirths. — [DevForum: Unlimited rebirths formula](https://devforum.roblox.com/t/unlimited-rebirths-formula/1848726)
- A quadratic rebirth cost made late levels too easy in a coin game. The suggested fix was a hybrid polynomial × exponential curve, with a warning to cap it. — [DevForum: Good formula to calculate amount needed to rebirth](https://devforum.roblox.com/t/good-formula-to-calculate-amount-needed-to-rebirth/1047686)
- For "buy max" rebirth buttons, an arithmetic-series closed form (cost = 5000·n·(2c+n+1) when each rebirth costs (c+1)·10,000) avoids loops. — [DevForum: Rebirths math problem](https://devforum.roblox.com/t/rebirths-math-problem/768366)
- A DevForum reply recommends looking up incremental/idle-game balancing theory, because "simulators" are essentially incremental games. — [DevForum: Simulator Formulas](https://devforum.roblox.com/t/simulator-formulas/853976)
- Typical completion length cited by developers:
  - Tycoons take "1-10 hours to finish."
  - Simulators take "1-100 hours to finish (depending on rebirths, etc)."
  - Players leave "after 5-10 minutes" if each of 10 zones repeats the same roughly hour-long cycle. Advice: "Make the game long but add content in between." — [DevForum: How long should it take a player to complete your game?](https://devforum.roblox.com/t/how-long-should-it-take-a-player-to-complete-your-game/3859022)
- Roblox suggests using Experiments (A/B tests) to measure the causal impact of changes, and Configs to adjust in-game values in real time without republishing. This fits tuning economy constants live. — [Roblox Creator Hub: Analyze and experiment](https://create.roblox.com/docs/production/game-design/analytics-essentials)
- Roblox's Economy analytics records currency sources and sinks, but data can't be reset. Admin and test grants permanently pollute the charts, so one developer wrapped AnalyticsService to drop admin actions. — [DevForum: Allow way to reset economy analytics](https://devforum.roblox.com/t/allow-way-to-reset-economy-analytics/3305641)
- Wipes and resets:
  - Da Amazing Bunker Simulator had an accidental data wipe in May 2020. Players voted on compensation, everyone restarted with $10,000, and past suits and events were made available for a limited time. — [Da Amazing Bunker Simulator Wiki: Data Reset](https://da-amazing-bunker-simulator.fandom.com/wiki/Data_Reset)
  - General economy-reset design: resets can run on a timer (seasons) or be triggered by economy-health indicators. Without new sinks, inflation returns. — [Tau Labs: How to design economic resets](https://taulabs.substack.com/p/economic-resets-in-games)
  - Player reaction to a deliberate inflation wipe (non-Roblox SAES:RPG server): veteran players called it "disrespectful to labor" and predicted inactive players would quit. — [SAES:RPG forum: Economy reset](https://saesrpg.uk/forums/topic/35874-feature-economy-resetsolved/)
- Pet Simulator 99 (BIG Games):
  - It has a consistent Saturday update cadence, but each new top-tier pet drop has thrown valuations "in shambles."
  - The Golden/Rainbow/Shiny tiers (5:1 combines at 1.5x/3x/5x stats) act as a currency and pet sink: one Shiny needs 125 normal copies. — [RoWatcher: Pet Simulator 99 economy explained](https://rowatcher.com/news/pet-simulator-99-economy-explained-gems-enchants-and-the-true-cost-of-progress)

### Inferences
- Pick a target time-per-rebirth (or time-per-area) and solve the cost curve against the income curve. Cost growth should roughly track multiplier growth, plus a mild premium for later tiers. Don't hand-pick cost and multiplier separately.
- Fix an over-fast economy by adding new tiers, sinks and content rather than wiping. If you must reset, compensate players (exclusive items, starting boosts) and announce it in advance.

### Gaps
- No published "time-to-milestone spreadsheet" from a named top Roblox studio was found.
- No first-hand BIG Games, Gamer Robot or Pet Sim X economy-wipe post-mortem was found.
- No Roblox simulator case study of migrating saves to a rebalanced economy was found.

## 3. Update cadence, events, and limited-time content

### Takeaway
Roblox officially recommends small updates every 2–4 weeks and big feature updates every 2–3 months. The biggest 2025 hits (Grow a Garden, Steal a Brainrot, Pet Sim 99) ran weekly Saturday updates with live "admin abuse" events, which produced huge, recurring but short-lived CCU spikes.

### Cited Findings
- Official D30 guidance: "A common frequency is to release smaller updates on the existing mechanics every 2-4 weeks, and bigger updates of new features every 2-3 months." Roblox also suggests social features to keep users engaged "while waiting for new content." — [Roblox Creator Hub: Retention](https://create.roblox.com/docs/production/analytics/retention)
- Jandel (Janzen Madsen, Splitting Point) on Grow a Garden:
  - "We implemented a live service. We started weekly updates... We're known for doing weekly updates in games across Roblox."
  - He says the game grew from about 500 CCU (10–20k DAU) to about 100k CCU "within two weeks," hit 1M CCU in about a month, and peaked at 22.3M CCU. It reached roughly 30B plays in three to four months.
  - He credits the offline-growing "persistent world." — [GamesBeat interview with Janzen Madsen](https://gamesbeat.com/janzen-madsen-interview/)
- Grow a Garden retention mechanics:
  - Seeds rotate in and out of stock, and weekly exclusive items must be claimed while online.
  - Two dedicated event teams were set up in July 2025.
  - Admin weather events ran before each weekly update. — [Wikipedia: Grow a Garden](https://en.wikipedia.org/wiki/Grow_a_Garden)
- Over a 30-day window, Saturday (update day) peaks averaged about 8.1M CCU versus about 2.8M on other days. PocketGamer.biz noted the game "doesn't typically sustain its peaks for long," and CCU once fell to 7.6M within an hour. — [Max Power Gaming: Grow a Garden keeps driving Roblox to new heights](https://www.maxpowergaming.co/post/grow-a-garden-keeps-driving-roblox-to-new-heights) (secondary source citing PocketGamer.biz)
- Steal a Brainrot:
  - Admin Abuse events run Tuesday 6 PM ET and Saturday 3 PM ET, with new content on Saturdays.
  - FOMO framing: "Missing a Saturday update event means waiting another whole week." — [Eldorado: Steal a Brainrot admin abuse schedule](https://www.eldorado.gg/blog/steal-a-brainrot-admin-abuse-schedule-explained/)
  - A joint "admin war" on August 23, 2025 set records for both games: Grow a Garden ≥22.3M CCU and Steal a Brainrot >20M CCU. — [Wikipedia: Steal a Brainrot](https://en.wikipedia.org/wiki/Steal_a_Brainrot)
- Durability caveat: Jefferies (Sept 2026) said US and Canada DAU growth to a 26M peak in Q3 2025 came mostly from viral hits like Grow a Garden and Steal a Brainrot, "which lost players quickly." — [Benzinga: Jefferies downgrades Roblox](https://www.benzinga.com/trading-ideas/movers/26/09/62018983/jefferies-downgrades-roblox-sees-bookings-growth-well-below-wall-street-stock-falls)
- DevForum on why games die: players leave because "they have to see new content after a while." Pet Simulator X's weekly updates are cited as the fix. — [DevForum: Games failing out of nowhere](https://devforum.roblox.com/t/games-failing-out-of-nowhere-read-the-solution/1940195)
- Counterpoint: one developer added a weekly rewards track and other hooks and saw "no positive movement at all" a week later. Hooks alone don't fix a weak core loop. — [DevForum: Why aren't players coming back?](https://devforum.roblox.com/t/feedback-why-arent-players-coming-back/4858033)
- Roblox's older developer blog recommends time-delayed rewards, such as mystery boxes that pay out after a set time, as come-back hooks. — [Roblox Developer Medium: Player Retention, a first look](https://medium.com/roblox-developer/player-retention-a-first-look-at-how-to-get-players-coming-back-to-your-game-9ae68826f466)

### Inferences
- A practical cadence for a small team: a fixed weekly day for small drops (new egg or creature, limited item, event), plus a new area or element every 4–8 weeks. That sits between Roblox's 2–4 week advice and the weekly cadence of top games.
- Update spikes are big but brief. Lasting retention needs a progression layer that stays deep between spikes.

### Gaps
- No Roblox-published data quantifying the returning-player uplift per update for typical (non-viral) games was found.
- The Grow a Garden Saturday versus weekday CCU figures come from a secondary blog. The primary PocketGamer.biz article was not fetched.

## 4. Monetization balance: Robux multipliers, boosts, keeping free players progressing

### Takeaway
Roblox's docs separate durable items (passes: permanent power-ups) from consumables (developer products: temporary boosts and currency). They recommend free and premium season passes so non-payers still earn rewards, and spacing pass rewards relative to average session time. No official guidance on caps for paid multipliers was found. Community practice is to sell speed and convenience, keep free progression complete, and keep money from turning into PvP power.

### Cited Findings
- Passes are for one-time privileges like a "permanent power-up." Repeatable items ("potions, temporary power-ups, or in-game currency") should be developer products. — [Roblox Creator Hub: Passes](https://create.roblox.com/docs/production/monetization/passes)
- Monetization foundations:
  - Items are split into Durable and Consumable ("temporary boosts"), and into Expression (cosmetics, pets) versus Enhancement (speed, strength) items.
  - Roblox advises "both a free and premium pass," which "ensures that non-paying players can still earn rewards and enjoy your experience, while rewarding paying players with worthwhile bonuses."
  - It also says to "consider designing the distance between rewards on your season pass relative to the average session time." — [Roblox Creator Hub: Monetization foundations](https://create.roblox.com/docs/production/game-design/monetization-foundations)
- Market reference: War Simulator's "x2 Money!" pass costs 299 Robux. — [Rolimons: x2 Money! pass](https://www.rolimons.com/gamepass/10453218)
- DevForum design discussion:
  - A developer observed that "almost every game (mostly simulators) are pay to win" and wanted to avoid it.
  - Their compromise sold the pass effect as a pricey single-use potion for soft currency, while the Robux pass made it permanent. — [DevForum: Would this gamepass idea be pay to win?](https://devforum.roblox.com/t/would-this-gamepass-idea-be-pay-to-win/1710950)
- Common 2x-pass bug: watching the currency value and doubling it causes totals to double on every rejoin. Apply the multiplier at each payout instead. — [DevForum: 2x Points gamepass in simulator game](https://devforum.roblox.com/t/2x-points-gamepass-in-simulator-game/539544)
- Grow a Garden lets players spend Robux to speed plant growth, which is time-skip monetization layered on offline progress. — [Max Power Gaming: How Grow a Garden crushed records](https://www.maxpowergaming.co/post/how-grow-a-garden-crushed-fortnite-and-steam-records-on-roblox)
- Steal a Brainrot:
  - Free spins are time-gated (the reviewer was told "a free spin 1 hour and 27 minutes from now").
  - Robux buys spins and spin luck. The article criticizes these mechanics as exploiting kids' weak grasp of probability. — [Free Systems: The algorithm behind Steal a Brainrot](https://freesystems.substack.com/p/the-algorithm-behind-steal-a-brainrot)
- Pet Sim 99: a $400 exclusive bundle drew the sharpest criticism given its young audience. — [RoWatcher: PS99 economy](https://rowatcher.com/news/pet-simulator-99-economy-explained-gems-enchants-and-the-true-cost-of-progress)
- Real-money benchmark: only 3.80% of tracked players paid anything, with per-game ARPPU median $0.70. Monetization rests on a small minority, which argues for keeping the free path long and intact. — [GameAnalytics 2026 Roblox Benchmark Report](https://www.gameanalytics.com/reports/2026-roblox-report)
- Third-party guide advice:
  - Introduce paid offers only "after a first-session win, not on the landing screen."
  - Avoid "pay-to-win" feel, which "drives negative reviews and player churn."
  - Offer 3–5 passes at different price points (e.g. 49/149/499/999 Robux). — [obby.fun monetization guide](https://www.obby.fun/blog/roblox-monetization-guide); [bloxg monetization guide](https://bloxg.com/guides/roblox-monetization)

### Inferences
- About 96% of players never pay, so tune milestone timings for free players and treat paid multipliers as compressors on top. Check that a fully boosted player (all passes, potions and rebirth bonuses stacked) still can't clear new content faster than updates ship.
- A practical cap is to add Robux multipliers together rather than multiplying them, and to keep each paid boost's effect on the "time to next area" under about 2x.

### Gaps
- No official Roblox guidance or named-studio data was found on capping stacked paid multipliers, or on how paid boosts affect endgame depletion.
- No sourced conversion data specific to x2-money passes was found.

## 5. Social and competitive retention: leaderboards, stealing/raids, trading, friend boosts

### Takeaway
Roblox officially pushes social play for both retention and discovery. Tools include invite prompts, the referral system (ReferredByPlayerId) and parties/trading. "Intentional co-play days" is an explicit Recommended For You signal. The 2025 megahits used visible bases, stealing and trading to create status and loss-aversion loops.

### Cited Findings
- Roblox design guidance: social interaction "helps to grow your audience as users invite their friends" through "mechanics such as parties and trading." Social play "can also help with retention, as users can act as evergreen sources of content for each other." — [Roblox Creator Hub: Design for Roblox (social)](https://create.roblox.com/docs/production/game-design/social-roleplay)
- Friend referral system:
  - Player:GetJoinData().ReferredByPlayerId identifies the inviter, so both inviter and invitee can be rewarded.
  - Roblox suggests an in-game button tied to the friend-invite modal. — [Roblox Creator Hub: Friend referral system](https://create.roblox.com/docs/production/promotion/referral-system)
- Player invite prompts support multi-friend or single-friend invites, custom messages, and launch data such as routing the invitee to the inviter. — [Roblox Creator Hub: Player invite prompts](https://create.roblox.com/docs/production/promotion/invite-prompts)
- Recommended For You signal: "7 day intentional co-play days per user," counting join, invite or private-server play with friends but not matchmaking. — [DevForum: Improved Recommended For You algorithm](https://devforum.roblox.com/t/boost-your-discovery-with-the-improved-recommended-for-you-algorithm-and-analytics-for-creators/3587441)
- Steal a Brainrot and Grow a Garden:
  - Players can steal from each other, which drives loss aversion.
  - Players see each other's bases or gardens, and competition centers on "having the coolest garden with the rarest items." — [Free Systems: The algorithm behind Steal a Brainrot](https://freesystems.substack.com/p/the-algorithm-behind-steal-a-brainrot)
- Pet Simulator 99: trading is "the true backbone of the player economy," with values denominated in Diamonds. New top-tier drops destabilize those values. — [RoWatcher: PS99 economy](https://rowatcher.com/news/pet-simulator-99-economy-explained-gems-enchants-and-the-true-cost-of-progress)

### Inferences
- Showing off visible bases and pets to other players is one of the cheapest retention levers for a collecting game. Stealing or raids add urgency but need protection windows to avoid rage-quits. This is an inference: no source quantified churn from stealing.
- A "play with friends" money or luck bonus also feeds the co-play ranking signal.

### Gaps
- No sourced retention uplift numbers were found for leaderboards, friend boosts or group-join rewards specifically.
- No developer statement was found on how Steal a Brainrot balances stealing against base protection.

## 6. Common mistakes that kill simulator games

### Takeaway
The repeated failure modes are:
- A repetitive loop with no new content between milestones (low session time and D7).
- Exponential curves that hit absurd numbers or impassable walls.
- Inflation from new top-tier drops without sinks.
- Spending on ads before engagement metrics are healthy.
- Pay-to-win perception.
- Relying on viral spikes without depth.

### Cited Findings
- Repetitive zones: if each of 10 zones repeats the same cycle, players leave "after 5-10 minutes." Content must arrive "all the time." — [DevForum: How long should it take a player to complete your game?](https://devforum.roblox.com/t/how-long-should-it-take-a-player-to-complete-your-game/3859022)
- Exponential cost curves reaching about 10^400 make the game unplayable. Cap or decay the growth rate. — [DevForum: Unlimited rebirths formula](https://devforum.roblox.com/t/unlimited-rebirths-formula/1848726); [DevForum: Good formula to calculate amount needed to rebirth](https://devforum.roblox.com/t/good-formula-to-calculate-amount-needed-to-rebirth/1047686)
- Short sessions (0–6 min) correlate with D1 below 10% and negligible monetization. — [GameAnalytics 2025 Roblox Benchmark Report](https://www.gameanalytics.com/reports/2025-roblox-report)
- Ads before engagement: Fantasy Forest's developer previously had a farming simulator fail "after some ad spending." Their lesson: "Focus on improving your game's engagement metrics, and the algorithm will give you players!" — [DevForum: Fantasy Forest post-mortem](https://devforum.roblox.com/t/from-0-to-2000-players-in-4-weeks-fantasy-forest-launch-post-mortem/2044257)
- Inflation and devaluation in Pet Sim 99 after major drops: real-money black-market prices of about $5 per billion gems suggest the currency has lost value. — [RoWatcher: PS99 economy](https://rowatcher.com/news/pet-simulator-99-economy-explained-gems-enchants-and-the-true-cost-of-progress)
- Uneven pacing (fast early, empty endgame) is a recurring complaint in progression-heavy games generally. Example: Schedule I players say early levels go too fast and the endgame turns into routine chores. — [Steam: Schedule I "Progression is too fast"](https://steamcommunity.com/app/3164500/discussions/1/599657527485931585/) (non-Roblox)
- Players will always finish content faster than developers can make it, which is why Goat Simulator added player-made content via Workshop. — [Game Developer: Goat Simulator post-mortem](https://www.gamedeveloper.com/business/goat-simulator-post-mortem) (non-Roblox)
- Viral-only growth fades. Top 2025 hits "lost players quickly," per Jefferies. — [Benzinga: Jefferies on Roblox](https://www.benzinga.com/trading-ideas/movers/26/09/62018983/jefferies-downgrades-roblox-sees-bookings-growth-well-below-wall-street-stock-falls)

### Inferences
- For a multi-area simulator, the main defences against "finishing too fast" are:
  - An endless or prestige layer (rebirths with growing but capped multipliers).
  - Collection completion with rare items.
  - Sinks such as upgrades and fusions.
  - A steady drip of new areas and creatures, rather than slowing the early game. A slow early game would hurt D1.

### Gaps
- No quantitative study was found linking "time to finish" with churn for Roblox simulators.
- No BIG Games or Gamer Robot first-hand post-mortem on endgame or inflation mistakes was found.
