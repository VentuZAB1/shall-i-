# SLINGSHOT: Rebirth v6 + Tutorial Rebirth step + 7-Day Login Streak (design)

Date: 2026-10-21. Owner request, verbatim:
> "Start with everything, lower all rebirthing making the higher amounts harder to reach, but for the newbies from 0 to
> 10th to be slithly easy. Add to the tutorial the rebirth, like highlighting it, when its ready (of course it has to be
> apart of the tutorial) so they know. Start with everything, but the 7-day login streak, has to be massive, including
> the 7th day."

**Why:** the live funnel (last 7 days, 10-21) shows 60% of new players buy their first money upgrade but only **10.8% ever
rebirth** (1,045 → 114). There is no daily reason to come back (D1 retention is the #1 algorithm signal).

**Success:** more players reach Rebirth 1 (goal: 25%+ of joins), more reach R2-R10, R11-R20 lasts longer, and players
come back the next day for their streak. We read this from the Onboarding, Rebirth ladder and the new Streak funnel.

Not in this batch: Next Goal bar + daily quests, Starter Pack, icon/thumbnail, hub for 6-8 bases (each its own task).

---

## 1. Rebirth ladder v6 (RS.RebirthConfig.LADDER)

Pet requirements from R2 are the same as v5. R1 has **no pet requirement** (money only).

| R | v5 cost | **v6 cost** | Pet requirement (unchanged from R2) |
|---|---|---|---|
| 1 | $40K + Water pet | **$25K, money only** | none |
| 2 | $2M | **$1.2M** | Water pet |
| 3 | $5.5M | **$4M** | Thunder pet |
| 4 | $25M | **$18M** | Thunder 100 kg |
| 5 | $125M | **$90M** | Fire pet |
| 6 | $800M | **$550M** | Fire 100 kg |
| 7 | $1.8B | **$1.3B** | Fire 1K kg |
| 8 | $4B | **$3B** | Shadow pet |
| 9 | $20B | **$15B** | Shadow 100 kg |
| 10 | $50B | **$38B** | Shadow 1K kg |
| 11 | $80B | **$120B** | Shadow 10K kg |
| 12 | $250B | **$400B** | Celestial pet |
| 13 | $900B | **$1.5T** | Celestial 100 kg |
| 14 | $1.5T | **$2.6T** | Celestial 1K kg |
| 15 | $2.25T | **$4T** | Celestial 5K kg |
| 16 | $3.5T | **$6.5T** | Celestial 10K kg |
| 17 | $5T | **$9.5T** | Celestial 25K kg |
| 18 | $6.5T | **$13T** | Celestial 50K kg |
| 19 | $9T | **$19T** | Celestial 100K kg |
| 20 | $14T | **$32T** | Celestial 1M kg |

Simulation (`economy/v6_rebirth.py`, 20 seeds, v5 player model): time to R10 **6.1 h → about 5 h**, time to R20
**59 h → about 95 h**. R2 is set to $1.2M (not $1.5M) so the R2 run is no longer than in v5.

Code changes:
- `RebirthConfig.LADDER[1]` gets no pet requirement; `petMeets(pets, nil)` returns **true** (today it returns false).
  `requirementText(nil)` returns "" and the Rebirth page **hides the pet need card** when there is no requirement.
- Skip-Rebirth (Robux) and the Rebirth "!" badge already read the ladder, so they follow automatically.
- Players who are already past a rebirth keep it. Nobody loses anything.

## 2. "REBIRTH READY!" moment (every rebirth, outside the tutorial)

When a player first meets both the money and the pet requirement of their next rebirth:
- A big Check-UI floating banner at the top centre: **"REBIRTH READY!"** (purple Rebirth theme, GothamBlack, black
  stroke, pop-in + gentle pulse) with the sub line **"+1 PET SLOT  •  x1.25 MONEY"** (the real numbers of that rebirth
  from RebirthConfig). It stays 4 s, then slides away.
- The left **Rebirth tile** pulses and keeps its "!" badge until the page is opened.
- Once per rebirth level per session (a client-side "shown for level N" value). Tapping it opens the Rebirth page.
  Never while a window is open (it waits
  until the window closes), never during the intro, never while the tutorial owns the screen (step 11 does it instead).
- Sound: a sound that is already in the SFX library (no new upload).

## 3. Tutorial step 11: first REBIRTH (part of the tutorial)

Today the tutorial ends after step 10 (first money upgrade) with TUTORIAL COMPLETE + 1 Money potion. Now:

- `TutorialExtra = 3` is a new stage = "rebirth next". TOTAL steps 10 → **11**.
- Server (TutorialServer): when UpgradeBought fires in stage 2 → stage **3** (or straight to done if Rebirths ≥ 1).
  When Rebirths goes up in stage 3 → stage 0 + the reward (moved here from step 10). Stuck guard: if a stage-3 player
  already has Rebirths ≥ 1 on load → done.
- Client (TutorialClient), step 11 has three states:
  1. **Not enough money:** "Earn $25K to REBIRTH!" with the live sub line "$x / $25K - grab more EGGS!" (same as the
     step 10 earn state: arrow to the slingshot pad while in the hub, "Hatch a PET to earn $!" if no pets).
  2. **Ready:** "REBIRTH is READY!" with the guide arrow on the left **Rebirth tile** (the tile glows too).
  3. **Rebirth page open:** "Press REBIRTH!" with the arrow on the green REBIRTH button; after the first press the
     button already says "TAP AGAIN!", and the tutorial line says "Tap AGAIN to confirm!".
- Finish screen after the rebirth: **TUTORIAL COMPLETE!** + reward row "+1 x2 MONEY POTION!" + "Next: reach the WATER
  area!" (the existing finish card, moved from step 10).
- PlayerData load rule: OnboardStep 12 (first money upgrade done) and Rebirths 0 → `TutorialExtra = 3`. Returners
  who already rebirthed get 0. Studio `TestTutorial` still starts at step 1.

## 4. 7-Day Login Streak (inside the Gift window)

### Where
- The **Gift tile stays the only tile** (no 5th left tile). The Gift window gets two tabs at the top: **DAILY** |
  **PLAYTIME**. PLAYTIME is the current 12 Playtime Rewards, unchanged. DAILY is the streak.
- The window opens on DAILY when today's reward is waiting, otherwise on PLAYTIME.
- The tile's "!" badge shows when **either** tab has something to claim.
- **Auto-open once per day** on join, when today's reward is waiting: after the Welcome Back (offline) window closes.
  Not while the intro or the tutorial is running (TutorialDone false or TutorialExtra ≠ 0); the badge still shows.

### Rules
- Days are **UTC calendar days** (server `os.time()`), so "come back tomorrow" means after 00:00 UTC.
  The DAILY tab shows a live countdown: "Next reward in 07:41:12".
- Claim today's reward → streak day +1. Claiming on the next UTC day continues the streak.
- **Missing a whole day resets the streak to Day 1** (the tab says "Streak lost - back to Day 1!" once).
  Owner approved the full reset (2026-10-21).
- After Day 7 the cycle starts again at Day 1 (week 2, 3, ...). **Every** Day 7 gives the secret pet, so a daily player
  gets one secret per week (owner approved, 2026-10-21).
- Saved fields (PlayerData FIELDS): `StreakDay = 0` (last claimed day 1-7, 0 = never), `StreakLast = 0` (UTC day number
  `os.time() // 86400` of the last claim).
- Server-authoritative RemoteFunction `Streak.Claim()`: DataLoaded check, busy lock, re-checks the day, gives the reward,
  and only then advances the streak (a failed give, for example "Pets full!", does not use up the day).

### Rewards ("massive"), money/speed scale with the player like Playtime Rewards (PlaytimeConfig.amount)

| Day | Card | Reward |
|---|---|---|
| 1 | cyan | **15 min of income** + 1 Money Potion |
| 2 | cyan | 1 Hatch Potion + 1 Speed Potion + **+20% Speed** |
| 3 | cyan | **30 min of income** + 2 Money Potions |
| 4 | purple | **BIG EGG**: the egg of your furthest area at that area's max normal KG (Grass 30K ... Celestial 500K) |
| 5 | magenta | **3 Money + 3 Hatch + 3 Speed Potions** |
| 6 | amber | **1 hour of income** + **+50% Speed** |
| 7 | **rainbow, double-size card** | **MEGA DAY:** a guaranteed **SECRET pet** of your furthest area at half that area's max KG (Grass 15K ... Celestial 250K) **+ 5 of every potion + 2 hours of income** |

- Day 7 is the hero card: rainbow gradient, sunburst behind the secret pet's portrait, "SECRET!" ribbon, slow shine
  sweep, and a full-screen celebration on claim: dark backdrop, turning sunburst, the pet portrait popping in,
  "SECRET PET!" in rainbow, the reward list (no particle confetti: the VFX rule says world VFX come from Blender).
- The secret pet goes into the hotbar/inventory and the Creature Index like Playtime's pet (GivePet).
- The egg goes into EggInventory through a new `ServerStorage.GiveEgg` bindable in BaseHatchery (same code path as the
  Studio `HatcheryGive` helper, minus the debug global).

### Look (Check-UI Daily Rewards archetype)
- Lime header "DAILY REWARDS", 2-tier divider, damier fade, 3D [X] close; the tab buttons follow the iconless button
  standard (active = lime, inactive = silver).
- 7 cards: Days 1-3 cyan, 4 purple, 5 magenta, 6 amber, 7 rainbow (spans two cards). Each card: "DAY N", reward icon
  (cash stacks / potion icons / egg / pet portrait), reward text, and its state: **CLAIM** (lime, pulsing) /
  **CLAIMED** (silver + check) / **LOCKED** (dark, "Tomorrow" on the next card).
- Phone: the same window scales with the Check-UI UIScale rule; cards wrap 4 + 3.

### Analytics
- New funnel **"Daily Streak"**: steps Day 1 ... Day 7 claimed (per cycle), plus Money economy events for the cash.

## 5. Testing (Studio, TestFreshSave = true before every Play)

- Rebirth: R1 with $25K and no Water pet works; R2 still needs a Water pet; the need card is hidden for R1; costs match
  the table; the banner shows once, waits for an open window, never shows in the tutorial.
- Tutorial: a fresh save goes 1 → 11; step 11 states 1-3 appear in order; the reward is given once, after the rebirth;
  rejoin in stage 3 resumes step 11; a stage-3 save with Rebirths 1 finishes at once.
- Streak: a Studio day-offset switch (`StreakDebugDay` attribute) fakes days. Check: Day 1 → 7, the double claim
  on the same day fails, a missed day resets, the cycle after Day 7, pets full keeps the day, auto-open only once per
  day and never during the tutorial/intro, the tab badge, and phone layout screenshots.
- A reviewer subagent checks the finished work (security of the remotes, DataStore fields, UI against Check-UI).

The owner Saves + Publishes. Never published by me.
