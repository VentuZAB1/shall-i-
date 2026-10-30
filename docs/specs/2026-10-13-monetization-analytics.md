# SLINGSHOT: treadmill Robux items, 50% price cut, regional pricing, analytics funnels (2026-10-13)

## The owner's request
- "Use the extension you have from chrome to create gamepasses for the new treadmills."
- "Make all current prices 50% cheaper, turn regional pricing as well."
- "Setup Funnels for our game, so we can keep track of everything."

## What the owner picked
- **Treadmill Robux items, both kinds for x12-x20:**
  - Developer products power the purple +1 button: 500 / 650 / 800 / 1,000 / 1,250 R$.
  - Store gamepasses at the full ladder value: 1,275 / 1,925 / 2,725 / 3,725 / 4,975 R$.
- **The 50% cut:** Robux items only. In-game $ prices are unchanged.
- **Funnels:** all 7 funnels, plus economy events.

## 1. Treadmill Robux items
| Tier | +1 product | R$ | Store pass | R$ |
|---|---|---|---|---|
| x12 | Treadmill Upgrade: Tier 7 (3718239330) | 500 | Emerald Treadmill (2028962292) | 1,275 |
| x14 | Tier 8 (3718239363) | 650 | Frost Treadmill (2029538285) | 1,925 |
| x16 | Tier 9 (3718239372) | 800 | Galaxy Treadmill (2030678290) | 2,725 |
| x18 | Tier 10 (3718239379) | 1,000 | Inferno Treadmill (2028824306) | 3,725 |
| x20 | Tier 11 (3718239391) | 1,250 | Diamond Rainbow Treadmill (2029790295) | 4,975 |

- **Pass price:** the sum of every +1 product up to that tier, so buying a pass never undercuts the ladder.
- **What a pass does** (`ShopServer`): owning one sets `TreadmillTier` to at least that tier.
  - Checked when your data loads and granted at once when the pass is bought.
  - The tier is saved, and TreadmillServer swaps the model.
- **The game's owner is skipped.** Creators own every pass they make, so the owner's real save would jump to x20 and
  top the TOP SPEED board.
  - Studio switch: workspace `TestTreadmillPasses = true` applies passes to the owner too.
- **x12-x20 now show the purple Robux button** on the sign and in the Shop. `TreadmillRobuxHidden` only hides x2.
- **New icons:** every treadmill product (x2-x20) and pass now uses a render of the real model.
  - The old x2-x10 icons still said x6 / x40 / x240 / x1.5K / x10K.
  - Files: `Desktop/SLINGSHOT Icons/products/make_treadmill_cards.py` and `matte.py`.

## 2. Prices: 50% off + regional pricing
- **The cut:** every existing Robux item is halved, rounded to whole Robux (49 → 25, 99 → 50, 749 → 375 …).
  - That's 42 developer products and 4 passes.
  - `ShopConfig` fallback prices match. The UI always shows the live price from `GetProductInfo`.
- **Regional pricing** (Roblox calls it "managed pricing") is ON for all 47 developer products and all 9 passes.
  - Roblox adjusts the price per region, from at most 70% off up to the default price.
  - Roblox's two requirements for developer products are met:
    1. The UI shows live prices. ShopClient, TreadmillSignClient, UpgradeClient, RebirthClient, PlaytimeClient,
       SpeedOfferClient and SpeedBoostCards already used `GetProductInfo`.
    2. Gifts are regulated. `ShopServer.giftAllowed` asks `GetUsersPriceLevelsAsync` every time, and a pass gift is
       allowed only when the buyer's price level is at least the receiver's. Otherwise the button says "CAN'T GIFT".
       If Roblox can't answer, the gift is refused live.
- **Checked:** all 47 products on Creator Hub were compared with ShopConfig, with 0 mismatches.

## 3. Analytics funnels (Creator Hub > Analytics)
Events only reach Roblox from the **published** game, never from Studio. To check in Studio, set workspace
`AnalyticsDebug = true` and every event prints to Output.

| # | Funnel | Steps | Session |
|---|---|---|---|
| 1 | Onboarding (one-time, new players) | 1 Joined → 2 Walked To Slingshot → 3 Launched → 4 Grabbed Egg → 5 Back In Hub → 6 At Base → 7 Egg Selected → 8 Egg Placed → 9 Egg Hatched → 10 Free Upgrade → 11 First Treadmill Run → 12 First Money Upgrade → 13 First Rebirth | — |
| 2 | Robux Purchase | 1 Prompted → 2 Purchased | one GUID per prompt |
| 3 | Shop | 1 Opened → 2 Clicked Buy → 3 Purchased | one GUID per opening |
| 4 | Egg Run | 1 Launched → 2 Grabbed Egg → 3 Banked | one GUID per launch |
| 5 | Rebirth Ladder | 1 Start → 2 Rebirth 1 … 21 Rebirth 20 | `<userId>-RebirthLadder` |
| 6 | Treadmill Ladder | 1 x1 … 11 x20 | `<userId>-TreadmillLadder` |
| 7 | Area Ladder | 1 Grass … 6 Celestial (the farthest area where you grabbed an egg) | `<userId>-AreaLadder` |

- **Custom fields** (breakdowns on the first step):
  - Robux Purchase: `Item - …`, `Surface - Shop / Treadmill Sign / Upgrades / Rebirth / Hatchery / Playtime / Speed Offer / Gift / Potions / Speed Pack / VIP Door / Other`, `Rebirth - R0 … R16-20`.
  - Egg Run: `Sling Lv - n`, `Rebirth - …`.
  - Shop: `Rebirth - …`.
- **Onboarding rules:**
  - Only players whose tutorial isn't done (or whose free upgrade is still waiting) are counted.
  - Steps 11-13 wait until step 10 is done, so using the treadmill before the tutorial can't skip tutorial steps.
- **Economy ("Money"):**
  - Income (Pets / Sell / Playtime) is added up and sent every 5 minutes and when the player leaves.
  - Each spend is sent at once: Upgrade Sling / Grab / Shield, Treadmill Tier n, and Rebirth (the money a rebirth wipes).
- **Code:**
  - `ServerScriptService.Analytics` (module) holds every AnalyticsService call.
  - `ServerScriptService.AnalyticsServer` watches attributes, the client UI remote, pass purchases, and runs the flush.
  - `ReplicatedStorage.Analytics.UI` is the client → server RemoteEvent: Shop window open/close and the tutorial
    step. It is validated and limited to 30 events a minute per player.
- **Budget:** about 10 events per player per minute at most. Roblox allows 120 + 20 × CCU per minute.
- **Dashboard:** after publishing, the Funnels page unlocks once events arrive. Add each funnel as a tab there (up to
  10). Economy is on the Economy page, and "View Events" shows recent events live.

## Independent code review (`docs/reviews/2026-10-13-analytics-review.md`): fixes
- **EXPLOIT closed** (older than this job, but cheaper now): a client can prompt any developer product itself, and
  every treadmill / Double Speed / upgrade product used to give "+1".
  - Buying the cheapest one again and again reached x20 for ~250 R$, x1024 speed for ~100 R$, or Slingshot Lv25.
  - Now each product only buys its own step: treadmill tier N needs tier < N; Double Speed step i needs boosts < i;
    an upgrade band needs level < upTo. A wrong receipt stays unprocessed.
- **Owner lookup:** retried, never cached when it fails.
- **Shop open:** means really on screen; an "open" ends after 15 min; only Shop surfaces count as Shop.
- **Onboarding:** the highest step is saved (`PlayerData.OnboardStep`), so later sessions continue the funnel.
- **Custom fields:** sent on every step.
- **Event budget:** 100 + 15 × players a minute per server, 40 per player; prompts de-duplicated.
- **Safety:** Analytics can never break Money / Receipts (pcall require + stub).
- **Receipts made crash-safe (pre-existing issue, fixed the same day):** the purchase id is saved in the player's
  data together with what they bought (PlayerData `ReceiptIds`), the save runs at once, and only then is Roblox told
  the purchase is granted. A purchase can no longer be granted twice or lost to a server crash.

## Tested in Studio (Play, TestFreshSave, AnalyticsDebug)
- Exploit checks through the real receipt handlers:
  - tier-2 product twice → the 2nd is refused;
  - tier-11 product at tier 2 → +1 only;
  - Double Speed step 1 twice → the 2nd is refused;
  - Sling band 1 at Lv5 → refused.
- Treadmill pass grant (switch `TestTreadmillPasses`) → straight to x20 in one step.
- The real Shop window: open → "Opened"; closing with X → an Upgrades prompt afterwards stays "Upgrades".
- Budget: 50 prompts a minute for one player → 10 dropped.
- Onboarding: Joined, Launched, Grabbed Egg; Treadmill Run held back until Free Upgrade.
- Shop: Opened → Clicked Buy → Purchased. Robux Purchase: Prompted (item + surface) → Purchased.
- Egg Run: Launched → Grabbed. Area, Rebirth and Treadmill ladders.
- Economy: pet income (with boosts), Sell, Upgrade spend.
- The owner skip: the test save stayed at x1. Before the fix it jumped to x20.
- No errors or warnings on the server or client.
- Backup: `ServerStorage._Backup_Analytics.Before` (13 scripts).
