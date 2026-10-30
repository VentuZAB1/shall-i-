# SLINGSHOT - Analytics + Shop changes review (2026-10-13)

Read-only review of the Studio place (Edit datamodel). Nothing was edited and Play was never started.
What I compared: every changed script against `ServerStorage._Backup_Analytics.Before` (a line diff of all 13 scripts),
plus the full source of `Analytics`, `AnalyticsServer`, `ShopServer`, `Receipts`, `Money`, `UpgradeServer`,
`RebirthServer`, `SellServer` and `PlaytimeServer`, and the parts of `TutorialClient`, `ShopClient`,
`MainMenu.MenuController`, `BaseHatchery`, `EggSpawner`, `MapGuard` and `SlingshotServer` that matter here.

Line numbers below are for the current scripts.

---

## Findings

### CRITICAL

1. **CRITICAL - ShopServer L200-202 (with ShopConfig L66-68): every treadmill Robux product only gives +1 tier, whichever tier it was for.**
   `Receipts.on(id, function(player) return grantTier(player) end)` never looks at `tier`. A client can call
   `MarketplaceService:PromptProductPurchase` on any product id from a LocalScript or an executor. So a player can buy
   the 25 R$ tier-2 product ten times and climb from x1 to x20 for 250 R$. The real price is 4,975 R$, the same as the
   Diamond Rainbow pass, so this also makes the new treadmill passes pointless. The hole has existed since tiers 7-11
   were added. Today's 500-1250 R$ products for tiers 7-11 make it the most valuable exploit in the game.
   **Fix:** register each product with its own tier. The receipt should raise the player to that tier:
   ```lua
   for tier, id in ShopConfig.TreadmillProducts do
       Receipts.on(id, function(player)
           local cur = player:GetAttribute("TreadmillTier") or 1
           if tier > cur then player:SetAttribute("TreadmillTier", math.min(tier, MAX_TIER)) end
           return true -- a stale or lower product closes the receipt without a grant (warn/log it)
       end)
   end
   ```
   Honest players can double-click Buy. To stop that costing them, refuse a second `treadmillRobux` prompt while one
   is pending (`pendingTier[player]`, cleared on `PromptProductPurchaseFinished`).

### IMPORTANT

2. **IMPORTANT - ShopServer L199 (Double Speed) and UpgradeServer L50-54 (Robux upgrade bands): the same exploit, older code.**
   The receipt of any Double Speed step gives +1 boost. ShopConfig even says so: "The receipt of ANY step gives +1".
   The receipt of any upgrade band gives +1 level. Buying the cheapest one again and again costs:
   - x1024 speed: 10 x 10 R$ = 100 R$ instead of 1,125 R$.
   - Slingshot Power 25: 25 x 8 R$ = 200 R$ instead of 690 R$.

   **Fix:** in each handler, check that the product is the player's current next step or band. For Double Speed that
   is `ShopConfig.doubleSpeedStep(SpeedBoosts).id == productId`. For upgrades it is
   `ShopConfig.upgradeProduct(kind, level + 1).id == band.id`. If it doesn't match, close the receipt with no grant
   and log it. Allow one step of lag for the double-click race described in item 1.

3. **IMPORTANT - ShopServer L101-111 `isOwner`: race and cached failure can give the group owner every treadmill pass.**
   - **Race:** `ownerId = game.CreatorId` (the group id) is set before `GetGroupInfoAsync` yields. Any other
     `applyTreadmillPasses` call during that yield compares the UserId against the group id and decides "not owner".
     For example, the owner and a friend loading together at server start.
   - **Cached failure:** if the pcall fails, `ownerId = 0` is cached for the life of the server.
   - **Result:** either way the owner is raised to tier 11 (x20). That is saved and tops TOP SPEED, which is exactly
     what this code is meant to prevent. The `info.Owner.Id` path itself is correct: in Edit it returned 1809064431,
     the Studio user.

   **Fix:** resolve the owner once at script start in a `task.spawn` with retries, into a local such as
   `ownerResolved`. Have `applyTreadmillPasses` skip, and retry later, while the owner is unresolved. Never compare
   against `game.CreatorId` when `CreatorType == Group`, and never cache a failed lookup.
   Also check the premise in a live server: does the group owner really own group-created passes? If not, this code
   is harmless but unnecessary.

4. **IMPORTANT - TutorialClient L449 + AnalyticsServer L69: "Egg Hatched" (onboarding 9) is logged when the egg is placed.**
   The client shows `n = 8` as soon as the first egg is placed and starts growing (TutorialClient L387). The free
   upgrade step is also `n = 8` (L362/L365), so the only step change that fires `tutorial 8` is the placement one. AnalyticsServer
   maps 8 to 9, so step 9 fires before the hatch. Placed to Hatched will read close to 100%, and a real hatch
   drop-off becomes invisible.
   **Fix:** map client 8 to onboarding 8, or ignore client 8 entirely. The server already logs 8 (BaseHatchery L273)
   and 9 (BaseHatchery L308) from real events.

5. **IMPORTANT - ShopClient L659-661 + MenuController L145-151 / L178-181: closing the Shop with X never sends "closed", and reopening never sends "opened".**
   - `closeWindow()` only sets `win.Visible = false`. `ShopPage.Visible` stays true, so no `shop=false` is sent.
   - On reopen, `openWindow` sets `ShopPage.Visible = true`, but it already is, so no Changed signal and no new
     "Opened" step.
   - The server therefore treats the Shop as open until a different menu page is opened.
   - Meanwhile every prompt (VIP Door, Upgrades, Rebirth, Hatchery, Playtime, Speed Offer) is relabelled
     `Surface - Shop` and also logs Shop "Clicked Buy".
   - Treadmill-sign money buys count as Shop purchases.
   - Shop opens are under-counted.

   **Fix (client):** send `page.Visible and win.Visible`, listening to both signals and sending only when the
   combined value changes. Alternatively, make `closeWindow` also hide the custom page.
   **Fix (server):** expire an "open" Shop session after about 5 min with no Shop activity.

6. **IMPORTANT - AnalyticsServer L19-28 + Analytics L70-96: onboarding steps 11-13 only work in one session, so the funnel will show a fake cliff.**
   - The onboarding state is in memory and is only created when `TutorialDone ~= true or FreeSling == true`.
   - A player who finishes the tutorial in session 1 and does their first treadmill run, money upgrade or rebirth in
     a later session never logs 11-13. First Rebirth almost always happens in a later session.
   - Steps 11-13 are also independent milestones, not a sequence. Whichever one is skipped gets auto-completed by
     Roblox; for example, a rebirth before any money upgrade fills in "First Money Upgrade".

   **Fix:** save the highest onboarding step, e.g. a PlayerData field `OnboardStep`. Start the tracker whenever it is
   below 13, and seed `s.last` from it. Or end the Onboarding funnel at step 10 and track Treadmill / Money Upgrade /
   Rebirth as their own first-time milestones (the existing ladders already cover Rebirth and Treadmill).

7. **IMPORTANT - Analytics L131, L148-149, L161-162, L169-170, L188, L195, L201: custom fields are only sent on step 1.**
   - "Purchased" (Robux Purchase), "Clicked Buy"/"Purchased" (Shop) and "Grabbed Egg"/"Banked" (Egg Run) go out with
     no fields.
   - A breakdown by Item, Surface, Sling Lv or rebirth bucket then cannot show conversion per value, because the later
     steps carry no value. Per-item purchase conversion is the main reason the Robux Purchase funnel exists.
   - The rebirth bucket also changes slot: CustomField01 in Shop, CustomField03 in Robux Purchase, Egg Run and
     Money.

   **Fix:** keep the fields with the session (`p.f = {item, surface, bucket}`, `run[player] = {id, f}`) and pass the
   same fields on every step of that session. Always put the rebirth bucket in CustomField03.

8. **IMPORTANT - Analytics `prompted` + every prompt remote: one client can use up the whole server's analytics budget.**
   - Each remote call that prompts now logs 1-2 AnalyticsService requests.
   - `Playtime.SkipAll` (PlaytimeServer L82-91) has no busy lock, no DataLoaded check and no rate limit.
   - `Shop.Buy`, `Upgrades.Buy` ("robux"), `RebirthRequest("skip")` and `Hatchery.SkipEgg` only lock for the duration
     of the call, and a prompt returns immediately.
   - An invoke loop produces thousands of events per minute. That blows the 120 + 20 x CCU per-minute budget, so
     every player's events in that server are throttled and dropped. Repeated "Prompted" sessions also inflate the
     funnel.

   **Fix:**
   - (a) In `A.prompted`, if the same player and id were prompted less than about 10 s ago, reuse that session and
     send nothing.
   - (b) Cap prompt logging at about 6 per minute per player.
   - (c) Add a global token bucket in `send()` with capacity of about 100 + 15 x `#Players:GetPlayers()` per minute.
     When it is low, drop Egg Run and ladder events first.
   - (d) Give `SkipAll` the same busy and DataLoaded guard as the other remotes.

   Normal play fits the budget: about 4 events per full egg run, roughly 8-16 per minute for an active runner. That is
   more than the header's "~10 per player per minute at most", but under budget.

9. **IMPORTANT - Analytics L20-21, L99-113: a broken Analytics module now stops purchases and income.**
   - Money and Receipts `require` Analytics when they load.
   - Analytics' top-level code runs outside the pcall wrapper: the `WaitForChild` calls and the loops over
     `ShopConfig.Passes`, `DoubleSpeedSteps`, `TreadmillProducts`, `PotionPacks`, `SpeedPacks` and `UpgradeProducts`.
   - If a config table is renamed, `require` errors and ProcessReceipt is never set (every purchase stays unprocessed)
     and `Money.Earn` breaks.
   - If `CreatureConfig` is renamed, they wait forever.

   **Fix:** wrap L99-113 in a `pcall` with `or {}` on each table, as L108 already does. In Money and Receipts, load
   Analytics with
   `local ok, A = pcall(require, ...)` and fall back to a no-op stub when it fails.

### MINOR

10. **MINOR - Analytics L228-233 `moneyIn`: no `valid(player)` check or "has left" check.**
    An income, sell or playtime call after `A.playerLeft` creates `income[player]` again. That can come from a
    PlayerRemoving handler connected after AnalyticsServer's, or a late tick. The 5-minute loop only walks
    `GetPlayers()`, so the entry is never flushed or cleared: a small leak and lost income data.
    **Fix:** keep a weak-keyed `left` set filled in `playerLeft` and return early for it. Or make all per-player tables
    weak-keyed with `setmetatable({}, {__mode = "k"})`.

11. **MINOR - Analytics L193 / L196 / AnalyticsServer L26-27: wasted or misleading Egg Run and ladder events.**
    - A grab with no launch creates a new Egg Run session whose step 2 auto-completes "Launched", inflating Launched.
    - Area Ladder is re-sent on every grab even though its session id is fixed, about 25% of all Egg Run traffic.
    - Both ladders are re-sent on every join.

    **Fix:** skip Egg Run steps when `run[player]` is nil. Keep `maxArea[player]` and send only a new higher area.
    Send each ladder value once per server.

12. **MINOR - Analytics L139-150: "Prompted" is over-counted.**
    It is logged even when Roblox silently ignores the prompt because another one is already open. Every extra click
    replaces `prompts[player][id]` with a new GUID, so conversion looks lower than it is. With 10+ abandoned sessions,
    a slow-arriving purchase can fall outside the 10 tracked session ids.
    **Fix:** the reuse-within-60 s rule from item 8.

13. **MINOR - Analytics L119-122: the 60 s "closedAt" grace in `shopSession` is dead code.**
    Every caller also checks `s.open`. **Fix:** remove it, or use it on purpose so a money buy or receipt within 60 s
    of closing still counts toward that Shop session.

14. **MINOR - TutorialClient L449: tutorial events go back and forth and share the 30/min UI budget with the Shop.**
    The client fires on every step change, including going backwards:
    - 1/2/3 on repeated launches without an egg.
    - 5/6 crossing the base fence.
    - 6/7 when equipping and unequipping the egg.

    The server ignores the repeats, but they use up the 30-per-minute UI budget that the Shop open/close events also
    use, and a dropped "close" leaves the Shop stuck open.
    **Fix:** on the client, only send when `s.n` is higher than the highest step already sent.

15. **MINOR - AnalyticsServer L74-77 and ShopServer L112-150: gamepasses bought on the Store page are never seen in game.**
    - The comment says the hook catches passes "bought in game or on the Store page".
      `PromptGamePassPurchaseFinished` never fires for Store-page purchases, so the Store-only treadmill passes never
      reach the Robux Purchase funnel.
    - A treadmill pass bought on the website while in game is only applied after a rejoin, because
      `applyTreadmillPasses` only runs on DataLoaded.
    - A pass for a lower tier than the player already has does nothing. The Store descriptions should say
      "at least x12" and so on.
    - A client can prompt any pass id, including other games' passes, which then logs as Item `<id>` / Other.

    **Fix:**
    - Correct the comment.
    - Re-check treadmill passes when the treadmill sign or Shop opens, or every few minutes.
    - In `A.purchased`, ignore ids that are not in `itemName`.
    - In ShopServer L142-150, confirm with `UserOwnsGamePassAsync` before `raiseTier`, as defence in depth.

16. **MINOR - Analytics L49: Studio never calls AnalyticsService, so argument errors would only show live.**
    **Fix:** in debug mode also call the real API (Roblox discards Studio events), or test once in a private published
    server and read the server log.

17. **MINOR - Economy accuracy.**
    - The income flush uses the balance at flush time as `endingBalance` (Analytics L223/L239). That is fine for
      averages but not exact per event.
    - The Rebirth sink (RebirthServer L71) puts the rebirth cost and the forfeited balance under one SKU.
    - AdminServer L363 money grants are not tracked.
    - Amounts reach 1e14 or more. Check on the first live day that the Economy totals look sane; if they are clamped,
      log in $M.

    **Fix:** split the SKU into "Rebirth Cost" / "Rebirth Reset", and add an "Admin" source SKU or exclude the owner.

18. **MINOR - ShopServer L185-195 `giftAllowed`: the shape of the `GetUsersPriceLevelsAsync` result is unconfirmed.**
    The call is server-only and errored in Edit. The code expects an array of `{UserId, PriceLevel}`. If the real
    field names differ, every live gift is refused with "Can't gift": the check fails closed, which is safe but would
    silently remove gifting.
    **Fix:** run one Server-mode test that prints the result, and `warn` when the shape is unexpected.

19. **MINOR - Analytics L254-262 wrapper loop: correct, with one nit.**
    - Assigning to existing keys while iterating is allowed.
    - Internal `A.x` calls resolve to the wrapped versions.
    - Luau `pcall` can yield.
    - Return values are kept, up to 2.
    - The `A.itemName`, `AREAS` and `ONBOARDING` tables are skipped.

    Nit: a failing hook warns on every call. `moneyIn` runs every second per player, so one error would flood the
    output.
    **Fix:** warn once per key per server, or at most once per minute.

20. **MINOR (pre-existing) - Receipts L12/L32: `granted` only exists in this server's memory.**
    If a server crashes after a grant but before Roblox records PurchaseGranted, the retried receipt can be granted
    again in another server, and logged as Purchased twice.
    **Fix:** store processed PurchaseIds in the player's save, which is Roblox's recommended ProcessReceipt pattern.

---

## Checked and correct (no action needed)
- Method names and argument order:
  - `LogFunnelStepEvent(player, funnel, sessionId, step, stepName, fields)`
  - `LogOnboardingFunnelStepEvent(player, step, stepName)`
  - `LogEconomyEvent(player, FlowType, "Money", amount, endingBalance, txType.Name, sku, fields)`
- Enums exist (`TimedReward`, `Gameplay`, `Shop`, `Source`, `Sink`, `CustomField01..03`). Field keys use `.Name`.
  Transaction types are passed as `.Name` strings.
- 6 recurring funnels + onboarding is within the 10-funnel limit. Largest step count is 21 (Rebirth Ladder), within
  the 100-step limit. Ladder session ids are fixed (`<userId>-RebirthLadder`), per-run sessions use GUIDs.
- Custom-field combinations stay far below 8,000. Economy uses 3 transaction types and about 20 SKUs.
- `Analytics.UI` remote: types checked, NaN and inf rejected (`value % 1 == 0`), budget counted before validation,
  `budget` cleared on leave. A spoofer can only distort their own Shop/onboarding rows.
- Per-player tables (`onboard`, `prompts`, `shop`, `run`, `income`, `budget`, `pendingGift`, `busy`) are cleared on
  PlayerRemoving, apart from the late-write case in item 10.
- The `ladder:gsub(...)` inside the `..` expression keeps only its first return value, so the session id is correct.
- `CreatureConfig.Areas[kind].area` is a number from 1 to 6, so `A.AREAS[area]` works.
- `GetGroupInfoAsync(...).Owner.Id` is the right path.
- ShopConfig: treadmill pass prices equal the sum of the product ladder (1275/1925/2725/3725/4975). Fallback prices
  are only used for display. The live price comes from `GetProductInfo`.

---
## Resolution (2026-10-13, orchestrator). Fixes were Play-tested with TestFreshSave + AnalyticsDebug.
1. **FIXED (critical exploit).** Each treadmill product only buys its own tier: TreadmillTier must be below that tier,
   otherwise the receipt stays unprocessed.
   - Tested: tier-2 product at tier 2 → refused; tier-11 product at tier 2 → +1 only.
2. **FIXED.**
   - Double Speed step i only grants while SpeedBoosts < i.
   - An upgrade band only grants while level < band.upTo.
   - Tested: step 1 bought twice → second refused; Sling band 1 at Lv5 → refused.
3. **FIXED.** The owner lookup retries with back-off and never caches a failure; passes wait until the owner is known,
   then are re-applied to everyone. Also fixed a startup ordering bug (task.wait before use).
4. **FIXED.** Client tutorial steps are accepted for 2..7 only. Placing (8) and hatching (9) are server-logged.
5. **FIXED.**
   - ShopClient reports whether the Shop is really on screen (page + every window above it + ScreenGui.Enabled).
   - The server ends an "open" after 15 min.
   - Only Shop-capable surfaces become "Shop"; tested: an Upgrades prompt after closing with X stays "Upgrades".
6. **FIXED.** The highest onboarding step is saved (PlayerData.OnboardStep), and later sessions continue it.
7. **FIXED.** Custom fields are stored per session and sent on every step; the rebirth bucket is always CustomField03.
8. **FIXED.**
   - Budget in send(): at most 100 + 15 × players events a minute per server and 40 per player.
   - Prompted is de-duplicated per id for 15 s.
   - Tested: 50 prompts in a minute → 10 dropped.
9. **FIXED.** The module's setup is pcall-protected; Money + Receipts require it with pcall and fall back to a stub.
10. **FIXED.** moneyIn ignores players who have left.
11. **FIXED.** No Egg Run step without a launch; the Area Ladder and the other ladders are de-duplicated per session.
12. **FIXED** (see 8).
13. **FIXED.** The grace period was replaced by the open-state + timeout model.
14. **FIXED.** The client sends tutorial steps forward only; the UI limit is 40 a minute.
15. **DOCUMENTED.**
    - Store-page purchases apply on the next join; this is normal for Store passes.
    - Analytics only sees in-game purchases.
    - The comment was fixed.
16. **NOTED.** Verify live with Creator Hub > Analytics > Funnels/Economy > "View Events" right after publishing.
17. **PARTLY.** The rebirth sink is now "Rebirth Reset"; the income balance is the one at flush time (accepted); admin
    grants are not tracked (on purpose).
18. **CONFIRMED.** In a Studio Play server, GetUsersPriceLevelsAsync returned {UserId, PriceLevel = 1000} entries.
19. **OK.**
20. **FIXED (2026-10-13, later the same day).** Roblox's recommended pattern:
    - The purchase id goes into the player's own save (new PlayerData field `ReceiptIds`, the latest 50), in the same
      snapshot as what they bought.
    - Their data is saved at once (`ServerStorage.SavePlayerNow`). Only after a successful save is Roblox told
      `PurchaseGranted`; a failed save answers `NotProcessedYet`, and Roblox's retry only acknowledges it.
    - A purchase id that is being processed is locked, so two calls for one purchase can't both grant.
    - Play-tested on a throwaway save (TestFreshSave), through `ServerStorage.TestProcessReceipt` (Studio only):
      - grant + save took 0.75 s; the DataStore then held both the id and the grant;
      - the same id again: acknowledged, not granted;
      - two calls at once: one granted, the other NotProcessedYet, granted once;
      - save down: NotProcessedYet with the grant remembered; the retry with the save back: acknowledged, no second
        grant;
      - an unknown product: NotProcessedYet;
      - 0 warnings or errors.
    - Backup: `ServerStorage._Backup_ReceiptIds.Before`.
