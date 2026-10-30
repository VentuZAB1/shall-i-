# SLINGSHOT: Next Goal bar + Daily Quests (design)

Date: 2026-10-21. The owner asked to "continue with everything" from the recommendation list, after the rebirth v6 / step 11 /
login streak batch (docs/specs/2026-10-21-rebirth-tutorial-streak-design.md).

**Why:** after the tutorial, players don't know what to do next. A rebirth is 20-60 minutes away, and nothing points at
the steps in between. Daily quests give 3 short goals every day (D1/D7 retention and play days). The Next Goal bar always
shows the ONE next big goal.

Not in this batch: the Starter Pack (it needs a new Robux product, see the end), the hub for 6-8 bases, and the icon /
thumbnail.

---

## 1. Next Goal bar (always on screen)

- A slim Check-UI bar at the **top centre** with the label "NEXT GOAL", one goal line, a progress trough
  (orange-to-gold fill) and the numbers. Example: `NEXT GOAL  Rebirth 1  [=====-----]  $12K / $25K`.
- **Hidden while:** the tutorial runs, the intro plays, any window is open, or a cutscene camera is on. It stays clear of
  the REBIRTH READY banner and the area-name banner (it slides under them while they show).
- **Tapping it** opens the matching place: the Rebirth page; or, for a slingshot goal, it shows the trail arrow to the
  Upgrade stall for 10 s.
- **The goal is picked from real state (client only, nothing saved), first match wins:**
  1. The next rebirth needs a pet the player doesn't own, and their slingshot can't reach that area yet:
     "Upgrade SLINGSHOT to Lv N to reach WATER" with $have / $price of the next level.
  2. The next rebirth needs a pet the player doesn't own: "Hatch a WATER pet" (no bar; tick when done).
  3. Otherwise: "Rebirth N" with $have / $cost.
  4. At MAX rebirth: "Max rebirth! Fill the INDEX" with found / total creatures.

## 2. Daily Quests (a 3rd tab in the Gift window: DAILY | QUESTS | PLAYTIME)

- **3 quests per UTC day,** picked by the server for each player from a pool (no two of the same kind). The amounts
  scale with the player (the area they reached and their income), so a quest takes about 5-10 minutes of normal play.
- **Pool:**

| Quest | Counted by (server) | Amount |
|---|---|---|
| Launch from the slingshot N times | SlingPhase -> Flying | 8 / 12 / 15 |
| Grab N eggs | CarryingEgg set | 5 / 8 |
| Bank N eggs (bring them home) | EggSpawner banked | 3 / 5 |
| Hatch N eggs | BaseHatchery hatch | 2 / 4 |
| Run on your treadmill for N minutes | TreadmillRun seconds | 3 / 5 |
| Earn $X | Money.Earn | 20 minutes of the player's income |
| Buy an upgrade | UpgradeBought | 1 (only offered if one can be bought) |

- **Rewards:**
  - Each quest: **10 minutes of income + 1 potion** (Money / Hatch / Speed in turn).
  - All 3 done: a **BONUS** chest of **+1 of every potion + 30 minutes of income**.
  - Each reward is claimed with its own CLAIM button (the same look as the streak cards).
- **Saved:** PlayerData `Quests` (JSON `{day, list = {{kind, goal, have, claimed}}, bonus}`). On a new UTC day the server
  writes a new set.
- **Badge:** the Gift tile "!" and the QUESTS tab dot light when a quest or the bonus is waiting.
- **Look:** 3 wide rows (icon, quest text, progress bar "3 / 8", reward, CLAIM / CLAIMED), then a BONUS row under them.
  Check-UI, phone-safe. The tab opens on QUESTS only when something is claimable and today's streak is already claimed.
- **Analytics:** a "Daily Quests" funnel: Quest 1 done, 2 done, 3 done, Bonus claimed.

## 3. Testing

The same as the streak: StreakDayOffset also moves the quest day, plus a Studio-only QuestDebug (set progress, complete,
new day). Pure tests for picking and scaling quests; live tests for each counter, claims, the bonus, a new day and
rejoin. Client checks and screenshots, including a phone shot if the owner switches the emulator. TestFreshSave before
every Play. Then a reviewer agent.

## Later: Starter Pack (needs the owner)

A one-time **49 R$ STARTER PACK**: 5 of every potion + 1 hour of income + a BIG EGG of the next area. It shows once as an
offer after Rebirth 1, and as a card in the Shop. It needs a new Developer Product in the group's Creator Hub (Monetization),
and I only create it with the owner's OK.
