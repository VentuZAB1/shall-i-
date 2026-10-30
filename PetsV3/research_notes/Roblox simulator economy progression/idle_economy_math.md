# Mathematics of Incremental / Idle / Simulator Economies and Prestige (Rebirth) Systems

Note on sources: the original blog.kongregate.com URLs for "The Math of Idle Games" now return 404; the series is live at kongregate.com/en/pages/... and gamedeveloper.com. Some findings came through search-result summaries rather than full-page fetches; those are flagged. Numeric tables marked "(computed)" were calculated by me from the cited formulas with Python, not taken from a source.

## Q1. Cost growth, production growth, walls, bulk-buy (Pecorella "Math of Idle Games" I-II)

### Takeaway
The core model is exponential cost (base * r^owned, r typically 1.07-1.15) against linear/polynomial production (base * owned * multipliers). Exponential always overtakes polynomial, which creates the "wall" that milestone multipliers temporarily push back and prestige ultimately resolves. Closed-form bulk-buy and max-affordable formulas exist for pure geometric costs.

### Cited Findings
- Series background: three parts by Anthony Pecorella (Kongregate), based on his MIGS 2016 talk; Part I 4 Oct 2016, Part II 28 Oct 2016, Part III Jan/Feb 2017; spreadsheet models at kon.gg/idle-math-spreadsheets — [Kongregate, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i); [Game Developer, Part I](https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i)
- Cost formula: `cost_next = cost_base * rate_growth^owned` — [Kongregate, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i)
- Production formula: `production_total = (production_base * owned) * multipliers` (linear in owned) — [Kongregate, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i)
- AdVenture Capitalist Lemonade Stand: rate_growth = 1.07, cost_base = 4 (actually 3.738), production_base = 1.67/sec; at 10 owned next cost = 7.87 — [Kongregate, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i)
- Most games use a growth rate of 1.07-1.15 per unit; Cookie Clicker uses 1.15 — via search summary of [Game Developer, Part I](https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i)
- AdCap per-business cost rates (secondary compilation): Lemonade 1.07, Newspaper 1.15, Car Wash 1.14, Pizza 1.13, Donut 1.12, Shrimp Boat 1.11, Hockey 1.10, Movie Studio 1.09, Bank 1.08, Oil 1.07 — [IdleFramework research doc (GitHub)](https://github.com/ac2522/IdleFramework/blob/main/IDLE_GAME_MECHANICS_RESEARCH.md) (secondary source, not verified against game data)
- Eric Guan example: cost x1.15 per level vs production x1.1 per level (both exponential, cost faster) — [Eric Guan, Idle Game Design Principles](https://ericguan.substack.com/p/idle-game-design-principles)
- Why walls happen: "exponential growth (anything of the form n^x, for n > 1) will eventually catch and far exceed any polynomial growth (x^k)" regardless of constants — [Kongregate, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i)
- Early in a run production exceeds costs, eventually costs become prohibitive; multipliers' purpose is to (temporarily) get production closer to or ahead of costs; AdCap shows bursts of rapid purchases at 300/400/500 owned when multipliers kick in — via search summary of [Game Developer, Part I](https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i)
- AdCap milestone multipliers: owning 25 and 50 Lemonade Stands each gives a stacking x2 — [Kongregate, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i)
- Bulk cost of n units when k owned: `cost = b * r^k * (r^n - 1)/(r - 1)` — [Kongregate, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i)
- Max affordable with currency c: `max = floor( log_r( c*(r-1)/(b*r^k) + 1 ) )` — [Kongregate, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i); these only work for simple exponential cost without shifting costs/exponents — via search summary of [Game Developer, Part I](https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i)
- Generator balancing: optimal play buys the best income:cost ratio at each opportunity; if the newest generator always dominates, older generators become irrelevant and decisions vanish; varying milestone-multiplier thresholds per generator shifts which generator is priority — [Kongregate, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i)
- Part II (generator-of-generators, Antimatter-Dimensions style): with n tiers each producing the tier below, currency grows like x^n/n!; series 1, x, x^2/2, x^3/6 ... approaches e^x but never reaches it, so exponential costs still win. Derivative Clicker example cost: 5 * 1.1^n — [Kongregate, Part II](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-ii)
- Roblox DevForum rebirth-cost patterns: geometric `C(r) = S * R^r` (e.g. 100 * 1.5^r, or 100 * 2^r); devs report pure exponential becomes impossible at high rebirth counts and suggest squaring (polynomial) or adding limits; Mining Simulator uses linear 10,000,000*(n+1) coins; arithmetic-series closed form for buying many rebirths — [DevForum: Simulator Rebirth Formula](https://devforum.roblox.com/t/simulator-rebirth-formula/3162074); [DevForum: Simulator Formulas](https://devforum.roblox.com/t/simulator-formulas/853976); [DevForum: Rebirths math problem](https://devforum.roblox.com/t/rebirths-math-problem/768366); [Mining Simulator wiki: Rebirth](https://mining-simulator.fandom.com/wiki/Rebirth)

### Inferences
- (computed) Cost multiplier after k purchases, and units per x2 / x10 cost:

| r | r^10 | r^25 | r^50 | r^100 | units per x2 cost | units per x10 cost |
|---|---|---|---|---|---|---|
| 1.07 | 2.0 | 5.4 | 29.5 | 868 | 10.2 | 34.0 |
| 1.10 | 2.6 | 10.8 | 117 | 13,781 | 7.3 | 24.2 |
| 1.15 | 4.0 | 32.9 | 1,084 | 1.17M | 5.0 | 16.5 |

  Rule: units per doubling of cost = ln2 / ln r. A designer can pick r from "how many buys until the price doubles" (1.07 = ~10 buys, 1.15 = ~5).
- (computed) Time-to-next-purchase approx = cost_next / income = b*r^k / (p*k*m). With AdCap Lemonade constants (b=4, r=1.07, p=1.67) and x2 at 25/50/100: k=10 -> 0.5 s; k=25 -> 0.26 s (just after x2); k=99 -> 4.9 s; k=100 -> 2.6 s; k=150 -> 51 s; k=200 -> ~1,127 s (~19 min). This is the sawtooth/wall shape: each milestone halves the wait, but r^k/k explodes past ~100-150 units. (Single-generator illustration only; real games add more generators and upgrades.)
- Recommendation for a simulator: per-item/upgrade costs r = 1.07-1.15 (lower r for higher-tier items as AdCap does); use milestone multipliers (x2 every 25 levels, bigger at 100s) to create "bursts"; rebirth cost should be geometric with modest R (1.5-2x per rebirth) or polynomial (n^2) if players can reach very high rebirth counts.
- For a simulator where income scales with a stat (e.g. KG), the same logic applies: if stat gain per action is polynomial and cost per stat point exponential, the wall is guaranteed; place rebirth roughly where wait between meaningful purchases exceeds a few minutes.

### Gaps
- Part II full article text beyond the fetched summary (e.g., any specific numeric pacing tables) not obtained. The per-business AdCap rates come from a secondary GitHub compilation, not the game files.

## Q2. Prestige formulas, why roots, multiplier per prestige, reset timing

### Takeaway
Prestige currency is almost always a fractional power (sqrt, cube root, ~1/7) of lifetime, max, or current-run earnings. The exponent sets how much more you must earn to double prestige currency: sqrt -> 4x, cube root -> 8x, ^0.14 -> ~128x. Common player rule: reset when the pending gain is about +50% to +200% of current prestige currency (often "when it doubles").

### Cited Findings
- AdVenture Capitalist: `angels = 150 * sqrt(c_L / 1e15)` (lifetime earnings) — [Kongregate, Part III](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-iii); floor applied, Mars uses 1e14 divisor; each angel +2% to all profits, multiplier = 1 + 0.02*angels — [IdleFramework research doc](https://github.com/ac2522/IdleFramework/blob/main/IDLE_GAME_MECHANICS_RESEARCH.md) (secondary)
- Cookie Clicker: `p = cbrt(c_L / 1e12)` (lifetime cookies) — [Kongregate, Part III](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-iii); level N needs N^3 trillion cookies; 1e12 -> 1, 1e15 -> 10, 1e18 -> 100, 1e21 -> 1,000, 1e24 -> 10,000; +1% CpS per prestige level once "Legacy" is bought (1,000 levels = x10 production); recommended first-ascension target 365 levels (~48.6 quintillion cookies) — via search summary of [Cookie Clicker Wiki: Ascension guide](https://cookieclicker.wiki.gg/wiki/Ascension_guide) and [Heavenly Chips (Fandom)](https://cookieclicker.fandom.com/wiki/Heavenly_Chips)
- Realm Grinder (max currency): `p = (sqrt(1 + 8*c_M/1e12) - 1)/2`, derived from c_M = 1e12 * p(p+1)/2; resetting at the same point yields literally no more currency — [Kongregate, Part III](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-iii)
- Egg, Inc. (current run): `dp = (c_R / 1e6)^0.14`, ~1/7 exponent, requires ~128x earnings to double, nudging toward active play and reducing time dependency — [Kongregate, Part III](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-iii)
- Clicker Heroes bases prestige on number of upgrades purchased; since upgrade costs are exponential this effectively "takes a log" of growth — [Kongregate, Part III](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-iii)
- Sqrt systems need 4x earnings to double prestige currency; cube root ~8x — [Kongregate, Part III](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-iii)
- With lifetime-based sqrt you can reset at the same point and still gain, but diminishingly; doubling takes ~3x-4x more earnings than the previous run — via search summary of [Game Developer, Part III](https://www.gamedeveloper.com/design/the-math-of-idle-games-part-iii)
- Pecorella advises "bumpy" loops with slow and fast parts; balancing requires spreadsheet models plus iteration — [Kongregate, Part III](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-iii)
- Reset rule of thumb: players typically prestige when gaining "+50% to +200%" prestige currency; use fractional exponents/logs to scale back growth; prestige cycles can be designed to accelerate, decelerate (risk tedium without meta-prestige), or vary — [Pecorella, Quest for Progress, GDC Europe 2016 (SlideShare)](https://www.slideshare.net/slideshow/quest-for-progress-gdc-europe-2016/65405507)
- Reset heuristic "prestige when pending gains >= current prestige currency (doubling)" — [IdleFramework research doc](https://github.com/ac2522/IdleFramework/blob/main/IDLE_GAME_MECHANICS_RESEARCH.md) (secondary)
- Antimatter Dimensions (post-Break-Infinity): `IP = floor(IPmult * 10^(log10(highest AM)/308 - 0.75))`; divisor 308 lowered by upgrades (307.8, then 285 via Time Study 111); every x1e308 antimatter = x10 IP; ~1.78 IP at exactly 1.8e308 — via search summary of [Antimatter Dimensions Wiki: Infinity](https://antimatterdimensions.wiki.gg/wiki/Infinity). This is an extremely flat (log-of-log-scale) layer formula.
- Prestige in Part I is framed as letting "the player get farther through the cost curve before falling behind" each cycle — [Kongregate, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i)
- Idle Breakout example combining lifetime and progress: `Points = floor(sqrt(lifetimeCoins/10,000) * (1 + bestLevel*0.05))` — via search summary citing [playbrain.games Idle Breakout tips](https://playbrain.games/blog/idle-breakout-tips-strategy-guide) (secondary, not fetched)

### Inferences
- (computed) AdCap angels and resulting multiplier (1 + 0.02*angels):

| Lifetime earnings | Angels | Profit multiplier |
|---|---|---|
| 1e15 | 150 | x4.0 |
| 4e15 | 300 | x7.0 |
| 1e16 | 474 | x10.5 |
| 1e18 | 4,743 | x95.9 |
| 1e21 | 150,000 | x3,001 |

  So the first prestige is designed to land at x4; each 100x lifetime earnings -> 10x angels -> ~10x multiplier. Because the bonus is linear in angels and angels are sqrt in earnings, net bonus ~ earnings^0.5: production after prestige grows sub-linearly in what you already earned, which keeps runs from trivializing.
- General template: `prestige = floor(C * (E / D)^e)`, bonus = `1 + k*prestige` (additive per unit). Choose D = earnings at the intended first-reset point, C so first reset gives a round count, and e by desired "earn Nx to double": N = 2^(1/e) (e=0.5 -> 4x, e=1/3 -> 8x, e=0.14 -> ~141x by formula; Pecorella quotes ~128x for ~1/7).
- Choose the input: lifetime/max earnings (AdCap, Cookie Clicker, Realm Grinder) forces "go further than before" for big gains; current-run earnings (Egg Inc) lets repeated same-depth resets pay the same, making short loops viable. For a Roblox money-rebirth with a fixed price (as in many simulators), the rebirth is effectively a fixed-step milestone rather than a root formula; the multiplier per rebirth then needs to be additive (e.g. +0.5x per rebirth) to avoid runaway.
- Target multiplier for the next run: a first reset worth ~x2-x4 total production matches AdCap's designed first reset (x4) and Pecorella's +50%-200% heuristic (x1.5-x3 currency).

### Gaps
- No primary source found giving canonical "first prestige at X hours, later at Y" for AdCap/Cookie Clicker; see Q3 for anecdotal ranges. The claim "a well-tuned prestige gives a 2x-4x speedup on the second run" appeared only in search-engine summaries of studio blogs (game-ace / gridinc) and was not verified on a fetched page.
- Realm Grinder/Cookie Clicker per-unit bonus details beyond what is above were not verified first-hand.

## Q3. Pacing targets (first upgrade, purchase intervals, session length, new layers)

### Takeaway
Hard data is scarce; the strongest guidance is qualitative from Pecorella (early game must feel quick; each run must get noticeably farther) plus practitioner targets: first purchase under ~60 s, first automation ~3 min, and first-session engagement 15-60 min with play frequency decaying from hourly to weekly. First-prestige times vary from ~10-30 min (small/jam games) to an evening or more (large idle games), with later runs much faster.

### Cited Findings
- Pecorella's two pacing questions: will early progress be quick ("an important feeling of growth of power"), and will they get noticeably farther than last time — [Quest for Progress (SlideShare)](https://www.slideshare.net/slideshow/quest-for-progress-gdc-europe-2016/65405507)
- First play session 15-60 minutes of active play; engagement decays, check-ins drop from hourly to weekly; example production caps staged at 20 min / 5 h / 2 days to match decaying engagement — [Eric Guan, Idle Game Design Principles](https://ericguan.substack.com/p/idle-game-design-principles)
- "Just-noticeable difference": players perceive multiplicative changes (e.g. x1.2) consistently, so scale on exponential steps — [Eric Guan](https://ericguan.substack.com/p/idle-game-design-principles)
- Practitioner targets for small idle games: first upgrade within 60 s, first automation within 3 min, first prestige within 10-15 min, phase transitions every 3-5 min of active play — via search summary of [DEV: I Built 7 Idle Games in 30 Days](https://dev.to/aguier/i-built-7-idle-games-in-30-days-what-i-learned-about-incremental-design-5d3f) (small 30-minute games; not fetched)
- Player-reported first-prestige times: 18 h first then ~1.5 h second (itch.io); Revolution Idle first Infinity ~16 h, later best 17 min (Steam) — via search summary of [itch.io post](https://itch.io/post/15616223) and [Revolution Idle Steam discussion](https://steamcommunity.com/app/2763740/discussions/0/6955341154010347761) (anecdotal)
- Player guide: first prestige may take an evening, later ones a day or a week, by design — via search summary of [onirealms prestige guide](http://onirealms.com/guides/prestige-rebirth-ascension-explained/) (secondary)
- Egg Inc. had a 2-hour offline earning limit, which Pecorella considered detrimental to retention — [Quest for Progress (SlideShare)](https://www.slideshare.net/slideshow/quest-for-progress-gdc-europe-2016/65405507)
- Offline caps commonly 2-24 h — via search summary of [game-ace idle game development](https://game-ace.com/blog/idle-game-development/) (secondary)
- Player complaints map to pacing failures: first upgrade takes too long; mid-game waits keep lengthening while "next purchases don't make much difference"; or prestige tree becomes too quick — via search summary of itch.io feedback threads (e.g. [itch.io post](https://itch.io/post/15330988))
- AdCap shows purchase bursts at 300/400/500 owned due to milestone multipliers — via search summary of [Game Developer, Part I](https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i)

### Inferences
- "Log-time" pacing: if each meaningful unlock costs roughly a constant factor (e.g. x2-x3) more time than the previous, unlock n arrives at time ~ T0 * g^n, i.e. the number of unlocks grows with log(time). That matches decaying engagement (Eric Guan) and keeps each unlock feeling equally significant on a multiplicative scale (JND).
- Suggested Roblox-simulator targets (synthesis, not sourced as a standard): first purchase 5-30 s; purchases every 10-60 s in first 10 min; first area/major unlock 3-5 min; first rebirth 15-45 min of active play (Roblox sessions are shorter than PC idle); rebirth 2-5 at 30-90 min each; introduce a new layer/system when the time per rebirth would exceed ~2-3 sessions.
- Each rebirth should make the early part of the run "visibly faster" (Pecorella's "quick early progress") — e.g. reaching the previous wall in 25-50% of the prior time.

### Gaps
- No rigorous public dataset of time-to-first-prestige across commercial idle games. No r/incremental_games thread was retrieved. Roblox-specific session-length data not found in this research pass.

## Q4. Multiplier stacking, runaway, soft caps, diminishing returns

### Takeaway
Use "additive within a category, multiplicative across categories": Final = Base * (1+sumA) * (1+sumB) * .... This bounds growth from any single bonus type while allowing exponential late-game via new categories. Soft caps switch to a weaker growth curve past a threshold, continuously.

### Cited Findings
- Typical idle-RPG rule: bonuses stack additively within the same category and multiplicatively across categories, to prevent uncontrolled scaling and create decisions — via search summary of [missionszanx: How Multipliers Stack in Idle RPGs](https://missionszanx.com/guides/how-multipliers-stack-in-idle-rpgs) (secondary)
- Example math: +20% and +30% additive = x1.50; multiplicative = x1.56; three +10% multiplicative = x1.331 vs x1.30 additive — same source
- Paradox (Stellaris): modifiers additive within class, multiplicative across classes — [Paradox forum](https://forum.paradoxplaza.com/forum/threads/additive-bonuses-vs-multiplicative-bonuses.1144836/); Diablo 3 bonuses of same type add before multiplying — [Blue Tracker D3](https://www.bluetracker.gg/diablo3/topic/us-en/25426-what-is-additivemultiplicative-damage-a-modern-dhs-perspective/); Diablo 4 "damage buckets": a bonus in an already huge additive pool adds little relative gain — [expcarry D4 damage buckets](https://expcarry.com/diablo-4-damage-buckets-multipliers-additive-build-scaling) (all via search summary)
- Idle production stacking template: `final = base * product(multiplicative_upgrades) * (1 + sum(percentage_upgrades)) * (1 + prestige_bonus) + sum(additive)` — [IdleFramework research doc](https://github.com/ac2522/IdleFramework/blob/main/IDLE_GAME_MECHANICS_RESEARCH.md)
- Prestige bonuses themselves are additive per unit in reference games: AdCap +2%/angel, Cookie Clicker +1%/level — [IdleFramework](https://github.com/ac2522/IdleFramework/blob/main/IDLE_GAME_MECHANICS_RESEARCH.md); [Cookie Clicker Wiki](https://cookieclicker.wiki.gg/wiki/Ascension_guide)
- Soft-cap example: effect 1.004^x * 2 up to 95, then (190x - 9025)^0.5 above 95 (continuous at the cap, switches exponential to sqrt growth) — via search summary of [TV Tropes: Diminishing Returns for Balance](https://tvtropes.org/pmwiki/pmwiki.php/Main/DiminishingReturnsForBalance)
- Prestige formulas are themselves the main diminishing-return device (very flat curves; e.g. Egg Inc ^0.14) — [Kongregate, Part III](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-iii)
- Stacked boosts can explode: Idle Miner Tycoon permanent x2 cash, x2 idle (x4 idle combined), timed 50x adds to existing for 87x, with ad boost 174x — via search summary of [Idle Miner Tycoon wiki: Boosts](https://idleminertycoon.fandom.com/wiki/Boosts)

### Inferences
- Recommended structure for a simulator: 3-5 named multiplicative buckets max (e.g. Rebirth, Pets, Gamepass, Upgrades, Event); inside each bucket sum bonuses. Total theoretical multiplier = product of bucket maxima; design the content curve against that product for whales and against ~the free-player product for everyone else.
- Generic soft-cap formulas (standard math, continuous at threshold T):
  - Power soft cap: `x <= T: x; x > T: T * (x/T)^s` with s in 0.3-0.5.
  - Log soft cap: `x > T: T * (1 + ln(x/T))`.
  - Hyperbolic diminishing (bounded to max M): `bonus = M * x/(x + K)` (half of M at x = K).
- Power-law stat-to-income (e.g. income ~ KG^(1/4), as the user's economy already uses) is itself a strong diminishing-return curve: 16x more KG gives 2x income.

### Gaps
- No primary Kongregate source explicitly prescribing soft-cap constants; the constants above are generic math, not sourced recommendations.

## Q5. Big number display and when to rescale

### Takeaway
Short-scale suffixes (K, M, B, T, Qa, Qi, Sx, Sp, Oc, No, Dc...) or letter suffixes (aa, ab...) read as milestones and are standard; scientific notation is preferred by many players at extreme magnitudes, so offer it as an option. Each new digit/suffix is a reward moment.

### Cited Findings
- Three common systems: full short-scale names, compact suffixes (K, M, B, T, Qa, Qi, Sx...), alphabetic (K, M, B, T, aa, ab...); each step x1,000, display 1-3 digits before suffix; after Qi: Sx, Sp, Oc, No, Dc, Ud, Dd, Td... — via search summary of [simpleidle: Big Number Notation](https://www.simpleidle.com/learn/big-number-notation-explained) and [bloxcontrol Roblox abbreviations](https://bloxcontrol.com/guides/roblox-number-abbreviations-k-m-b-t-qa-qi-explained/)
- InnoGames chose letter notation (K, M, B, T, AA, AB, AC) over scientific/engineering after talking to game design — [InnoGames blog: Dealing with huge numbers in idle games](https://blog.innogames.com/dealing-with-huge-numbers-in-idle-games/) (via search summary)
- AdVenture Capitalist uses names up to Centillion (1e303) and shows infinity past the float limit — via search summary; Antimatter Dimensions' 1.8e308 "Infinity" is the double-precision limit — [Antimatter Dimensions Wiki](https://antimatterdimensions.wiki.gg/wiki/Infinity)
- Players: lettered notation gets unwieldy, 1e100 easier to parse; long-scale languages confuse "billion" — via search summary of Steam discussions (e.g. [Unnamed Space Idle](https://steamcommunity.com/app/2471100/discussions/0/600765572565761276/))
- Psychology: new digits/suffixes act as visual milestones; numbers going up reduce loss aversion; reinvestment loop — via search summary of [Dinogame: Psychology of Idle Games](https://dinogame.gg/blog/psychology-of-idle-games/) and [FictionTalk](https://fictiontalk.com/2021/08/25/the-psychology-of-idle-games-why-humans-like-big-numbers/) (secondary, low authority)

### Inferences
- Roblox Luau numbers are doubles (max ~1.8e308, integers exact only to 2^53 ~ 9e15); plan currency to stay below ~1e300 or switch to a mantissa/exponent representation. DataStore saves of doubles are fine for display-precision economies.
- Rescale (introduce a new currency or layer that converts the old one at a fixed ratio) when the displayed suffix outruns the player's ability to read it, or when costs would need more than ~3 suffix steps per area; a new area/element is a natural rescale point.

### Gaps
- No rigorous study found that quantifies engagement effect of suffix vs scientific notation.

## Q6. Monetization interplay: paid multipliers and caps

### Takeaway
Paid permanent multipliers (x2 etc.) stack multiplicatively with free progression and can collapse pacing for payers; reference games sell x2-x4 permanent boosts and much larger timed boosts. No source gives a hard rule; the safe practice is to size paid boosts relative to one prestige step and scale rewards to current income.

### Cited Findings
- Idle Miner Tycoon: permanent x2 cash (all mines), separate x2 idle cash (x4 idle if both), timed boosts stack additively with permanent ones (50x + existing -> 87x, x2 with ad -> 174x) — via search summary of [Idle Miner Tycoon wiki: Boosts](https://idleminertycoon.fandom.com/wiki/Boosts)
- Common paid items: instant currency as % of current income, time-warps granting hours of income, permanent multiplier persisting through prestige, instant prestige, gacha — via search summary of [Incremental game (Wikipedia)](https://en.wikipedia.org/wiki/Incremental_game) and genre articles
- Size rewards to current income, not fixed amounts (fixed reward valuable at hour 1 is worthless by day 10) — via search summary of [game-ace idle development](https://game-ace.com/blog/idle-game-development/) / [applixir monetization guide](https://www.applixir.com/blog/the-ultimate-guide-to-game-monetization-models-and-metrics/)
- Rewarded ads typically 30-40% of idle game revenue; Frozen City est. 15-20% — via search summary of [Naavik: Frozen City deconstruction](https://naavik.co/deep-dives/frozen-city-deconstruction/)
- Industry figures: ~62% IAP / 38% ads; payers 2.6x LTV — [IdleFramework research doc](https://github.com/ac2522/IdleFramework/blob/main/IDLE_GAME_MECHANICS_RESEARCH.md) (secondary, original source unclear)
- GDC survey cited: 70% of idle players "core", 20% "hardcore", top motivators Completion and Power — via search summary (original GDC talk not fetched)
- Pecorella GDC 2015 "The Mechanics and Monetization of Self-Playing Games" exists on GDC Vault (not fetched) — via search summary of [Game Developer author page](https://www.gamedeveloper.com/author/anthony-pecorella)

### Inferences
- Treat a paid permanent x2 as roughly equal to one early prestige/rebirth step (AdCap's designed first reset is x4). Recommended caps (synthesis): permanent paid multipliers combined <= x2-x4 on the main currency; timed boosts x2-x3 for 15-60 min; never sell large multipliers (x10, x1024) on the core currency, because with costs at r^k a x1024 multiplier equals ln(1024)/ln(r) free purchases (= ~102 units at r=1.07, ~50 at r=1.15) or 5 doublings of sqrt-prestige earnings, which skips whole areas.
- Put paid multipliers in their own bucket (multiplicative once) rather than letting each pass multiply every other bucket, and design area costs against free_curve * paid_bucket_max so payers move faster but still hit each wall.
- Prefer selling time (time-warps scaled to current income, extra slots, convenience) over raw multipliers, since time-skips are self-limiting relative to the cost curve while multipliers compound.

### Gaps
- No primary source found stating a numeric cap on paid boosts relative to free progression; recommendations above are inferences. Robux-specific (Roblox) gamepass multiplier norms (e.g. x2 money gamepass prevalence) were not researched in this pass.
