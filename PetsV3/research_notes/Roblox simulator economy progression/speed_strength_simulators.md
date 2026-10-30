# Roblox speed/strength/clicker simulators: progression and rebirth economies

Method note: Fandom page URLs return HTTP 402 to the fetch tool, so wiki content was read as raw wikitext through the MediaWiki API (`<wiki>.fandom.com/api.php?action=query&prop=revisions...`). The citations below link the human-readable wiki page. Fandom wikis are community-edited and often lag behind live game balance. Treat their numbers as "documented at some point" rather than "current live values". Revision timestamps seen: LoS Rebirth page edited 2026-03-17, Ultimate Upgrades 2026-04-09, ML Rebirths 2026-08-27, ML "How Rebirthing Works" 2023-04-11.

## 1. Rebirth cost formulas: linear, polynomial or exponential? (values at rebirth 1/10/100/1000)

### Takeaway
The big "classic" sims use surprisingly simple linear rebirth costs: Legends of Speed adds +25 levels per rebirth and Muscle Legends adds +5K strength per rebirth. They stay endless because the stat curve behind each level or rep grows faster than the requirement. Newer or smaller sims use explicit exponential cost tables (Horse Race: about x2 per rebirth early, decaying to about x1.19 per rebirth late) or roughly quadratic ones (Speed Run Simulator, about n^2). Mining Simulator 1 is linear in coins, but every price in the game scales with the rebirth count as well.

### Cited Findings
**Legends of Speed (Scriptbloxian Studios): linear in *levels***
- The rebirth requirement starts at level 50 and rises by 25 levels per rebirth (50, 75, 100...). Each rebirth gives gems, +1 rebirth (+2 with the x2 Rebirths gamepass), a stacking "x1 multiplier" and a new max level. Required level = 50 + 25·n, where n is the number of rebirths already done. That gives level 50 for rebirth 1, 275 for rebirth 10, 2,525 for rebirth 100 and 25,025 for rebirth 1,000 (computed from the stated rule). — [LoS wiki: Rebirth](https://legends-of-speed.fandom.com/wiki/Rebirth)
- The "Divine Rebirth" ultimate makes rebirths cost 10% fewer levels per tier, up to 5 tiers. — [LoS wiki: Ultimate Upgrades](https://legends-of-speed.fandom.com/wiki/Ultimate_Upgrades)
- The steps-per-level XP curve is not documented. The wiki only says that steps act as EXP and that reaching step goals levels you up. — [LoS wiki: Steps](https://legends-of-speed.fandom.com/wiki/Steps)

**Muscle Legends (Scriptbloxian Studios): linear in strength**
- Rebirth cost = 10,000 + 5,000·x strength, where x is the current rebirth count. Gems earned = 5,000·x. — [ML wiki: How Rebirthing Works](https://muscle-legends.fandom.com/wiki/How_Rebirthing_Works)
- Rebirth 1 costs 10K strength and gives 10K gems. The gem reward rises 5K per rebirth (rebirth 10 gives 55K). "Rebirth strength requirement increases 5k strength every rebirth." — [ML wiki: Rebirths](https://muscle-legends.fandom.com/wiki/Rebirths)
- Computed from the formula: about 10K for rebirth 1, 55–60K for rebirth 10, about 505K for rebirth 100 and about 5.0M for rebirth 1,000. Elite players still report rebirth counts of 78.1K and 1.7M, using scripted auto-rebirth overnight. Linear costs let rebirth counts explode once per-rep gains are large. — [ML wiki: Beginners Guide](https://muscle-legends.fandom.com/wiki/Beginners_Guide(how_you_should_start_the_game))

**Speed Run Simulator: roughly quadratic**
- Rebirth prices in Speed: #1 = 1,000; #2 = 2,948; #3 = 6,702; #5 = 20,500; #10 = 98,453; #20 = 480,228; #30 = 1,215,582; #36 = 1,845,911; #39 = 2.21M. Rebirth 48 unlocks everything. — [Speed Run Simulator wiki: Rebirths](https://speed-run-simulator.fandom.com/wiki/Rebirths)
- (My own fit of that table: cost ≈ 1000·n^k with k rising from 1.56 at n=2 to 2.1 at n=36, so roughly quadratic.)

**Horse Race (comparable Roblox training sim, trophies): exponential with a decaying ratio, the best full table found**
- Costs are 500, 1K, 2K, 4K, 8K, 16K, 32K, 64K, 130K and 260K for rebirths 1–10 (doubling each time). Later costs: 94M at #20, 11B at #30, 1.7T at #50, 10T at #60, 1Qa at #86, 12Qa at #100, 1Qi at #125, 86Qi at #150 and 1Sx at #164. — [Horse Race wiki: Rebirth](https://horse-race.fandom.com/wiki/Rebirth)
- The boost is +10% training power per rebirth, cumulative and additive (100% at #10, 500% at #50, 1000% at #100). The table shows the boost frozen at 1200% for #120–150, which may be a cap or a wiki error. — same source
- (My own calculation: the per-rebirth cost ratio is x2.0 for #1–10, about x1.80 for #10–20, about x1.39 for #20–50, and about x1.19 for #50–100 and #100–150. Late-game cost grows about 19% per rebirth while the reward is only +10 percentage points, additive.)

**Mining Simulator 1: linear, but the whole economy rescales**
- Rebirth price = 10,000,000·(n+1) coins. Tools and backpacks cost (1+n)/2 × base; eggs and crates cost (1+n) × base. Each rebirth adds +1x to a permanent ore-value multiplier (2x after the first). — [Mining Simulator wiki: Rebirth](https://mining-simulator.fandom.com/wiki/Rebirth)

**Mining Simulator 2**
- The first rebirth costs 400,000,000 coins. The "Cheap Rebirths" gem enchant cuts that by up to 75%. Multi Rebirth (up to 5 at once) costs 10x the coins for 2 rebirths, 20x for 3, 30x for 4 and 40x for 5. The wiki itself flags that cost growth after the first rebirth is undocumented. — [Mining Simulator wiki: Rebirths (MS2)](https://mining-simulator.fandom.com/wiki/Rebirths_(MS2))

**Tapping Legends: linear per-rebirth price, sold in bulk**
- Clicks needed = x·(50·y), where x is the number of rebirths bought and y is the current rebirth count. Bulk buttons go +1, +5, +25, +50, +150, +500, +2.5K, ... up to +10NvD (about 1e31+) rebirths. — [Tapping Legends wiki: Rebirths](https://tapping-legends.fandom.com/wiki/Rebirths)

**Clicker Simulator**
- The first rebirth costs 800 clicks according to the wiki. — [Clicker Simulator Info wiki: Rebirths](https://clicker-simulator-info.fandom.com/wiki/Rebirths)
- AllThings.How says the first rebirth costs 750 clicks. Higher islands sell higher-tier rebirth buttons that convert clicks to rebirths at better rates. — [AllThings.How](https://allthings.how/roblox-clicker-simulator-how-to-play-from-first-click-to-first-rebirth/)
- You can buy up to 10 rebirths at a time and the cost rises each rebirth. The Unlimited Rebirths pass (R$799) removes the batch cap and Auto Rebirth (R$299) automates it. — [Pro Game Guides](https://progameguides.com/roblox/how-to-get-more-rebirths-in-clicker-simulator/)

**Race Clicker**
- Rebirth costs Wins. No cost table was found. — [The Helpful Gamer](https://thehelpfulgamer.com/how-to-rebirth-in-race-clicker-on-roblox)

**DevForum convention**
- Developers recommend a geometric cost, C(r) = S·R^r. Example: 100·1.5^r, so each rebirth costs 50% more. — [DevForum: Simulator Rebirth Formula](https://devforum.roblox.com/t/simulator-rebirth-formula/3162074)

### Inferences
- There are two design schools. (a) Linear rebirth cost with stat gains that grow super-linearly through pets, gyms and multipliers: LoS, ML, Tapping Legends, MS1. Rebirth counts become huge (ML players at 1.7M), so rebirths turn into a currency spent in shops. (b) Exponential cost with a decaying ratio: Horse Race starts at x2 and settles around x1.2. Rebirth counts stay in the low hundreds and the numbers climb through Qa, Qi and Sx.
- Horse Race's decaying-ratio curve shows a common practical pattern. Steep doubling early means the first rebirths come quickly. Later the ratio flattens to about x1.2 because players' income multipliers also grow geometrically.

### Gaps
- No official Race Clicker rebirth cost table was found. NamuWiki returned 403.
- The Legends of Speed steps-per-level curve is undocumented.
- The Mining Simulator 2 rebirth cost after the first rebirth is undocumented.
- The Clicker Simulator cost formula is undocumented.
- No Strongman Simulator or Weight Lifting Simulator rebirth formula was found. Only user Q&A sites came up, and they conflict.

## 2. What each rebirth gives, and what resets

### Takeaway
Rebirth almost always wipes the main stat or currency and keeps pets, trails, cosmetics and unlocked areas. In exchange it grants a small additive multiplier: +1x per rebirth (LoS, MS1, Clicker Sim), +5% (ML) or +10% (Horse Race, Race Clicker). Many games also pay a secondary currency (gems or tokens) that feeds a persistent rebirth shop.

### Cited Findings
- **Legends of Speed:** gems, +1 rebirth, x1 stacking multiplier and a new max level. Pets and trails are kept. Rebirthing is optional. The level resets, so city access must be re-earned. — [LoS wiki: Rebirth](https://legends-of-speed.fandom.com/wiki/Rebirth); [LoS wiki: Cities](https://legends-of-speed.fandom.com/wiki/Cities)
- **LoS, steps:** the step counter resets on rebirth, but rebirths permanently raise the base step multiplier. — [LoS wiki: Steps](https://legends-of-speed.fandom.com/wiki/Steps)
- **Muscle Legends, what you lose:** 100% of Strength, 100% of Durability and 50% of Agility.
- **Muscle Legends, what you gain:** +5% strength, durability and agility (stacking) plus gems.
- **Muscle Legends, what you keep:** Karma, pets, consumables, auras and unlocked gyms.
- Source for the three ML bullets above: [ML wiki: Rebirths](https://muscle-legends.fandom.com/wiki/Rebirths)
- **ML caveat:** the rebirth boost applies only to equipment gains, not to pet stats. For example, with 35 rebirths a 10-strength dumbbell rep becomes 10·2.75 + pet strength. As a result, "rebirth multipliers barely seem to have an effect at some point". — [ML wiki: How Rebirthing Works](https://muscle-legends.fandom.com/wiki/How_Rebirthing_Works)
- **ML, 20 rebirths:** about 2x stats. — [ML wiki: Beginners Guide](https://muscle-legends.fandom.com/wiki/Beginners_Guide(how_you_should_start_the_game))
- **Clicker Simulator:** each rebirth adds +1x clicks (100/s becomes 200/s after 1 rebirth) and gives 10 gems. Gems buy bigger rebirth buttons and rebirth pets. — [Clicker Simulator Info wiki: Rebirths](https://clicker-simulator-info.fandom.com/wiki/Rebirths)
- **Clicker Simulator, what resets:** the click total resets; pets, quest progress and islands are kept. — [AllThings.How](https://allthings.how/roblox-clicker-simulator-how-to-play-from-first-click-to-first-rebirth/)
- **Race Clicker:** +10% wins and acceleration per rebirth; current wins are lost; trading unlocks after the first rebirth. — [The Helpful Gamer](https://thehelpfulgamer.com/how-to-rebirth-in-race-clicker-on-roblox)
- **Race Clicker at rebirth 60:** +900% acceleration and +2400% wins. Rebirths can also be spent in a "Rebirth Coin Shop", but guides advise holding 60. — [Item Level Gaming](https://itemlevel.net/race-clicker-ultimate-hatching-guide-wins-grinding-guide/)
- **Race Clicker, conflicting claim:** a 2026 guide says about 15–20% effective speed per rebirth. It is low-reliability. — [Earnaldo](https://earnaldo.com/blog/race-clicker-free-robux-guide)
- **Speed Run Simulator:** +1 Speed-Per-Click per rebirth plus a new trail. Speed is lost; pets and trails are kept. — [Speed Run Simulator wiki](https://speed-run-simulator.fandom.com/wiki/Rebirths)
- **Mining Simulator 1:** +1x ore value and 20 Rebirth Tokens (40 with the 2x Tokens pass). Coins, tools and backpacks are lost; Robux and token items are kept. — [MS wiki: Rebirth](https://mining-simulator.fandom.com/wiki/Rebirth); [MS wiki: Rebirth Tokens](https://mining-simulator.fandom.com/wiki/Rebirth_Tokens)
- **Mining Simulator 2:** "rebirth Coin Multiplier increases by 10x" (exact wording; ambiguous whether this is +10x or ×10) and 150 gems. Skins at rebirths 1, 5 and 10; achievements at 1, 5, 15, 35, 100 and 350. — [MS wiki: Rebirths (MS2)](https://mining-simulator.fandom.com/wiki/Rebirths_(MS2))
- **Horse Race:** +10% training power (cumulative). Power resets; trophies, worlds and treadmills are kept. The leaderboard keeps the highest power. — [Horse Race wiki: Rebirth](https://horse-race.fandom.com/wiki/Rebirth)
- **Tapping Legends:** diamonds per rebirth, spent in the Rebirth Shop.
  - +1 Pet Storage, up to 470 times
  - +1 WalkSpeed, up to 32 times
  - "+1.01 Click Bonus" (+1% click multiplier), up to 5000 times
  - +5 Pet Storage, up to 10 times
  - Auto Clicker, once
  - Source: [Tapping Legends wiki: Rebirth Shop](https://tapping-legends.fandom.com/wiki/Rebirth_Shop)

### Inferences
- The typical per-rebirth reward is small and additive: +5% to +10%, or +1x on a base of 1. Big power growth comes from multiplicative sources (pets, trails, gamepasses) that survive rebirth. Rebirth is the slow floor; pets are the fast ceiling.
- Additive boosts give diminishing relative returns. Going from rebirth 100 to 101 in Horse Race is +10 points on 1000%, under 1% better. Games counter this with rebirth shops and bulk rebirth buttons, and by gating areas on rebirth count.

### Gaps
- The Legends of Speed per-rebirth step multiplier (+1x?) is not precisely documented.
- Whether the Mining Simulator 2 "10x" is additive or multiplicative is unclear.

## 3. How stats map to actual walk speed and gameplay (caps, diminishing returns)

### Takeaway
Hard data is thin. In Legends of Speed, level drives speed and jump power roughly proportionally, about 4 speed per level from one data point. Players can and must lower their speed in settings because high speeds are unplayable. The raw stat keeps growing while the effective WalkSpeed is user-clamped.

### Cited Findings
- **LoS, speed scaling:** as level rises, max speed and jump rise proportionally. — [LoS wiki: Steps](https://legends-of-speed.fandom.com/wiki/Steps)
- **LoS, Speed Desert chasm:** crossing requires at least level 139, or 564 speed and 675 jump power. — [LoS wiki: Speed Desert](https://legends-of-speed.fandom.com/wiki/Speed_Desert)
- **LoS, Legends Highway:** recommended speed is 300–500 and jump power 200. Players who are "too fast" can change these in the settings menu. — [LoS wiki: Legends Highway](https://legends-of-speed.fandom.com/wiki/Legends_Highway)
- **Muscle Legends, Agility:** Agility is speed, Strength is damage and Durability is health. At 60 rebirths a player makes about 50 strength per rep without pets, and the best jungle pets give 2.5K stats. — [ML wiki: Beginners Guide](https://muscle-legends.fandom.com/wiki/Beginners_Guide(how_you_should_start_the_game))
- **ML treadmills:** +1 Agility every 2 seconds, gated by agility thresholds of 0/20/100/250/600/1,000/1,500/2,000/3,000/3,500. — [ML wiki: Treadmills](https://muscle-legends.fandom.com/wiki/Treadmills)
- **Race Clicker:** speed depends on the clicks made during the pre-race countdown and on wins. — [The Helpful Gamer](https://thehelpfulgamer.com/how-to-rebirth-in-race-clicker-on-roblox)
- **+1 Speed Keyboard Escape:** speed per step = (Base Step Speed + Button Upgrades) × Rebirth Multiplier × Trail Multiplier × Aura Multiplier. Trails and auras do not reset on rebirth. This comes from a fan wiki of uncertain reliability. — [1keyboardescape.wiki](https://www.1keyboardescape.wiki/guide/1-Speed-Keyboard-Escape-guide)
- **Tapping Legends:** WalkSpeed is a separate rebirth-shop upgrade capped at +32 (32 purchases). Movement speed is decoupled from the clicks stat. — [Tapping Legends wiki: Rebirth Shop](https://tapping-legends.fandom.com/wiki/Rebirth_Shop)

### Inferences
- Common pattern: the stat number (speed, strength) is effectively a score and currency that grows without bound. Actual Humanoid WalkSpeed is either a small, capped derivative (Tapping Legends +32 cap) or user-adjustable (LoS settings), because physics breaks at very high WalkSpeed.

### Gaps
- No source gave an exact stat→WalkSpeed function or log-scale mapping for any of these games. The LoS "about 4 speed per level" figure comes from one data point.

## 4. Treadmill / training-zone gating: requirements per zone and gain ratios

### Takeaway
Zones are gated either by rebirth count (Muscle Legends gyms, LoS worlds, MS1 zones), by a level or stat threshold (LoS caves, ML equipment), or both (Speed Run Simulator: rebirths plus speed). The thresholds usually rise geometrically: ML rocks go from 5K to 150K to 400K to 750K to 1M to 5M to 10M to 25M durability. Clicker Simulator egg prices rise roughly x15–x80 per island.

### Cited Findings
**Muscle Legends gyms (by rebirths)**

| Gym | Rebirths required | Stage |
|---|---|---|
| Tiny Island | under 1,000 strength | starter |
| Frost | 1 | early |
| Mythical | 5 | early |
| Muscle King | 5 | early |
| Eternal | 15 | early |
| Legends | 30 | mid |
| Jungle | 60 | late |
| Industrial | 150 | late |

— [ML wiki: Gyms](https://muscle-legends.fandom.com/wiki/Gyms)

**Muscle Legends rocks (by durability)**

| Rock | Durability required |
|---|---|
| Tiny | 0 |
| Punching | 10 |
| Large | 100 |
| Golden | 5K |
| Frozen | 150K |
| Mythical | 400K |
| Eternal | 750K |
| Legends | 1M |
| Muscle King | 5M |
| Jungle | 10M |
| Industrial | 25M |

— [ML wiki: Rocks](https://muscle-legends.fandom.com/wiki/Rocks)

- **ML treadmill anomaly:** a 1,000-agility main-island treadmill outperforms the later Legend Beach and Frost Gym treadmills, so zone gain ratios are not strictly monotonic. — [ML wiki: Treadmills](https://muscle-legends.fandom.com/wiki/Treadmills)

**Legends of Speed worlds and courses**
- Grass Course: level 5 (+500 steps)
- Frost Course: level 15 (+1,000)
- Mysterious Cave / Snow City: level 25
- Parkour Challenge: level 35 (+2,000)
- Magma City: 1 rebirth plus the Inferno Cave course
- Speed Desert: 5 rebirths
- Electro Cave / Legends Highway: 10 rebirths
- Outer Space: 50 races won
- Pirate Course: 50 rebirths
- Source: [LoS wiki: Worlds](https://legends-of-speed.fandom.com/wiki/Worlds)

**Legends of Speed per-zone rewards**
- Snow City hoop: 850 steps. — [Snow City](https://legends-of-speed.fandom.com/wiki/Snow_City)
- Outer Space hoops: 800–1,000 steps. — [Outer Space](https://legends-of-speed.fandom.com/wiki/Outer_Space)
- Crystal (egg) prices: Snow 4K gems, Space 15K and 25K, Desert 40K and 50K, Electro Legends 100K.
- Orbs give more stats in each newly unlocked city. — [LoS wiki: Cities](https://legends-of-speed.fandom.com/wiki/Cities)

**Speed Run Simulator areas (rebirths + speed)**

| Area | Requirement |
|---|---|
| Desert | 2 rebirths + 15K speed |
| Snow | 4 rebirths + 40K speed |
| Volcano | 6 rebirths + 60K speed |
| Graveyard | 9 rebirths + 115K speed |
| SpongeBob | 23 rebirths + 700K speed |
| Adventure Time | 28 rebirths + 1.25M speed |
| Jungle | 33 rebirths + 2M speed |
| Castle | 45 rebirths + 5M speed |

— [Speed Run Simulator wiki: Rebirths](https://speed-run-simulator.fandom.com/wiki/Rebirths)

**Mining Simulator 1 zones (by rebirths)**
- Candy Land 1, Dino Land 2, Atlantis 5, The Beach 10, Crystal Cavern 20, Magic Forest 45, Lava World 60. — [MS wiki: Rebirth](https://mining-simulator.fandom.com/wiki/Rebirth)

**Race Clicker worlds (older data)**
- Home World: 0 rebirths. Space World: 2 rebirths, 2x multiplier. Ocean World: 4 rebirths, 5x multiplier. The game now has more worlds. — via search summary of [NamuWiki: Race Clicker](https://en.namu.wiki/w/Race%20Clicker) (page itself returned 403, so unverified)

**Tapping Simulator Gauntlet World (cumulative damage gates)**
- Areas unlock at 5K, 100K, 1M, 25M, 100M, 200M, 500M, 750M, 1B and 100B damage. — [Tapping Simulator wiki: Worlds](https://tapping-simulator-roblox.fandom.com/wiki/Worlds)

**Clicker Simulator World 1 egg prices by island (clicks)**

| Island egg | Price |
|---|---|
| Basic | 250 |
| Earth | 2.5K |
| Sun God | 1.5M |
| Frozen Arctic | 25M |
| Lava Dragon | 2B |
| Treasure | 65B |
| Space Guardian | 3.75T |
| Treeland | 100T |
| Ice Cream | 1.9Qa |
| Atlantis | 62Qa |
| Tropical | 1.1Sx |
| Bee | 60Sx |
| Galaxy | 5Sp |

- World 2 (Tech) starts at 1 No (Tech Egg) and reaches 606 Sd. World 3 (Time) goes from 90 St to 15 N and beyond. — [Clicker Simulator Info wiki: Worlds](https://clicker-simulator-info.fandom.com/wiki/Worlds)
- (My own calculation: consecutive island ratios are roughly x10 to x80, median about x30. The 62Qa → 1.1Sx jump of about x17,700 looks like a wiki typo, perhaps 62 Qi.)

**Strongman Simulator**
- About 23+ areas listed (Back Alley → ... → Sewer). A Rolimons listing mentions "Area 29". A late area reportedly needs "2Qa and 50M Strength". This is low-reliability, via search summaries of NamuWiki, Rolimons and TikTok. — [NamuWiki: Strongman Simulator](https://en.namu.wiki/w/Strongman%20Simulator)

### Inferences
- A rough design ratio across these games: each new zone needs about 3–10x the previous stat threshold in early zones (ML rocks: 5K → 150K → 400K → 750K → 1M) and pays about 1.5–3x more per action. Rebirth-gated zones space out as 1, 5, 15, 30, 60, 150 (ML) or 1, 2, 5, 10, 20, 45, 60 (MS1), roughly doubling.

### Gaps
- Direct per-zone gain ratios (stat per rep per zone) were not found in structured form for any game.

## 5. Typical time to milestones

### Takeaway
There is very little reliable time data. Most numbers are anecdotal or come from low-quality SEO guides.

### Cited Findings
- **Muscle Legends:** the first rebirth comes at 10K strength in the early session, and "20 rebirths gives about 2x stats". Glitching targets of 14,580 or 18,980 rebirths "take about a couple days". A player went from 78.1K to 1.7M rebirths using a rebirth script plus eight paid packs. Casual players can stop at about 60 rebirths. — [ML wiki: Beginners Guide](https://muscle-legends.fandom.com/wiki/Beginners_Guide(how_you_should_start_the_game))
- **Legends of Speed:** with evolved pets, reaching the rebirth level drops from about 20 minutes to about 30 seconds. This comes from a search summary and the original guide was not verified. — via [SuperCheats LoS guide](https://www.supercheats.com/legends-of-speed-codes-tips)
- **+1 Speed Keyboard Escape:** low-reliability SEO fan wiki.

| Phase | Rebirths | Wins | Time |
|---|---|---|---|
| Early | 0–5 | 1–50K | 1–3 h |
| Mid | 5–15 | 50K–10M | 5–15 h |
| Late | 15–30 | 10M–1B | 20–50 h |
| Endgame | 30–50 | 1B–100T | 75–200+ h |

— [plus1speedkeyboardescape.wiki](https://plus1speedkeyboardescape.wiki/progression/1-speed-keyboard-escape-100-trillion-wins)

- **+1 Speed Evolve:** the first rebirth and World 2 gate come around level 25. World 3 needs rebirth 50–100+. The site notes that exact numbers shift with patches. — [speedevolve.wiki](https://speedevolve.wiki/guides/world-progression/)
- **Race Clicker, YouTube:** one video title cites "1.84 Trillion per race at rebirth 60", which indicates the wins scale by mid-game (title only). — [YouTube](https://www.youtube.com/watch?v=st2b381r-Ys)

### Inferences
- The pattern is a first rebirth within the first session (about 5–20 min) and the first area unlocks within 1–3 hours. "Final world" or endgame targets are set at tens to hundreds of hours, and rebirth automation (passes, scripts) is assumed at the top end.

### Gaps
- No developer-published retention or time-to-milestone data was found. The time figures above are anecdotal, or come from SEO sites that may be AI-generated.

## 6. Keeping it endless: prestige layers, rebirth shops, events, leaderboards, number scales

### Takeaway
Every game studied uses rebirths as a spendable currency (shops), bulk or auto rebirth (often monetized), and cosmetic rank ladders that run into the quintillions. Several add a second prestige layer (Tapping Simulator's Super Rebirth, LoS's Ultimate/MEGA upgrades bought with rebirths). Number suffixes run through K, M, B, T, Qa, Qi, Sx, Sp, Oc, No, Dc and on to UnD, DD, TD ... NvD.

### Cited Findings
**Legends of Speed Ultimate Upgrades (cost in rebirths, linear arithmetic per level)**
- Total to max everything: 69,625 rebirths.
- Rebirth pets (10 each): 14,700, 22,000 and 27,500 rebirths to max.
- Game upgrades, 3,700 rebirths total:
  - x2 Trails, 10 levels, 25 → 1,375 total
  - +1 Pet Slot ×3, 900 total
  - +10 item capacity
  - +1 daily spin
  - x2 chest rewards
  - x2 quest rewards
- Enhancements, 1,725 rebirths total:
  - Step Booster: +10% per level, 5 levels, 150 total
  - Ethereal Orbs: +10% spawn chance of x10 orbs
  - Demon Hoops: +100% hoop rewards
  - Divine Rebirth: −10% rebirth level cost
- Source: [LoS wiki: Ultimate Upgrades](https://legends-of-speed.fandom.com/wiki/Ultimate_Upgrades)

**Tapping Simulator Super Rebirth (second prestige layer)**
- Requires 5B regular rebirths. Gives a permanent 2x on regular rebirths. — [Tapping Simulator wiki: Super Rebirth](https://tapping-simulator-roblox.fandom.com/wiki/Super_Rebirth)
- Rank ladder: Shiny (1), Sparkling (2), ... Omega (6–999), then a new title every 1,000 super rebirths up to Lit at 27,000+. — same source; [Ranks](https://tapping-simulator-roblox.fandom.com/wiki/Ranks)
- Super Rebirth Shop, paid in Super Tokens. — [Super Rebirth Shop](https://tapping-simulator-roblox.fandom.com/wiki/Super_Rebirth_Shop)
  - Pizza Party: ÷10 egg prices per level, 10 levels
  - Way of the Ninja: multiplies rebirths, 30 levels
  - The Hive: keep one pet per level through a super rebirth
  - Tap, Rebirth, Repeat: 1,000 levels, 33B tokens total
  - Bad Luck Protection: 100 levels, 252B
  - Super Homerunner: auto super rebirth
  - Gauntlet World: unlocks for 10 Super Tokens

**Rebirth token shops**
- Mining Simulator 1: tokens buy permanent tools, backpacks and cosmetics. Tokens can also be bought with Robux (10 R$ = 20 tokens ... 2,750 R$ = 8,000). — [MS wiki: Rebirth Tokens](https://mining-simulator.fandom.com/wiki/Rebirth_Tokens)

**Monetized rebirth automation**
- LoS: x2 Rebirths pass; Unlimited Levels lets players multi-rebirth. — [LoS wiki: Rebirth](https://legends-of-speed.fandom.com/wiki/Rebirth)
- Clicker Simulator: Unlimited Rebirths R$799, Auto Rebirth R$299. — [Pro Game Guides](https://progameguides.com/roblox/how-to-get-more-rebirths-in-clicker-simulator/)
- MS2: Multi Rebirth enchant. — [MS wiki: Rebirths (MS2)](https://mining-simulator.fandom.com/wiki/Rebirths_(MS2))

**Cosmetic rank ladders**
- Muscle Legends strength ranks:
  - Rookie ranks: 0 / 100 / 500 / 1.5K / ... / 25K (Muscle Legend)
  - Elite ranks: 100K (House Lifter), 10M, 50M, 100M, 250M, 1B (Multiverse Elite), 5B, 15B, 40B, 100B, 250B, 500B, 1T (World Ender), 5T, 25T, 75T, 500T, 1Qa, 5Qa, 15Qa, 50Qa, 250Qa (True Legend)
  - Source: [ML wiki: Ranks](https://muscle-legends.fandom.com/wiki/Ranks)
- LoS racing ranks by races won: 1, 5, 10, 20, 30, 50, 80, 120, 200, then elite at 350, 700, 1,250, 2,000, 3,000 and 5,000. — [LoS wiki: Racing Ranks](https://legends-of-speed.fandom.com/wiki/Racing_Ranks)

**Number scale reached**
- Tapping Legends bulk rebirth buttons go up to "+10NvD" (novemdecillion). — [Tapping Legends wiki: Rebirths](https://tapping-legends.fandom.com/wiki/Rebirths)
- Clicker Simulator egg prices reach Sp, No, Dc, Ud, Td, Qad, Sd, St, O and N within three worlds. — [Clicker Simulator Info wiki: Worlds](https://clicker-simulator-info.fandom.com/wiki/Worlds)
- Horse Race reaches Sx by rebirth 164. — [Horse Race wiki](https://horse-race.fandom.com/wiki/Rebirth)

**Events and leaderboards**
- "+1 Speed Every Second" runs global leaderboards and timed X2 Speed events. Premium players get +50% speed per second. — [Roblox game page](https://www.roblox.com/games/11623553646/Roblox-but-every-second-you-get-1-Speed) (via search summary)
- Horse Race leaderboards keep the highest power even after a rebirth reset. — [Horse Race wiki](https://horse-race.fandom.com/wiki/Rebirth)
- Clicker Simulator ships a constant stream of event eggs ("100M Event Egg" ... "465M Event Egg"). — [Clicker Simulator Info wiki page list](https://clicker-simulator-info.fandom.com/wiki/Worlds)

### Inferences
- Endlessness is built from layered sinks: rebirths → rebirth shop (rebirths spent as currency) → super-rebirth or ultimate tier → cosmetic rank ladders with thresholds spaced roughly 2–5x apart up to quintillions. Bulk-rebirth and auto-rebirth features become necessary, and monetizable, once counts reach the thousands.
- For a Luau implementation, values beyond about 1e15 need a suffix formatter (K, M, B, T, Qa, Qi, Sx, Sp, Oc, No, Dc, ...). Values beyond about 1e308 would need a BigNum. None of the documented games appear to exceed about 1e60 (NvD is about 1e60 on the short scale).

### Gaps
- No current (2024–2026) official changelogs with balance numbers were found.
- No data was found on seasonal-event economics, such as event-currency to multiplier conversion.
- The Race Clicker world multipliers beyond Ocean World are unknown.
