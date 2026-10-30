# Review: tutorial steps 9-10 + phone Speed offer (2026-10-15)

**Verdict: CHANGES NEEDED.** Visuals are clean and on-style. Two server bugs let steps 9-10 finish themselves.

1. **Step 10 finishes itself on rejoin, with a free potion.** Where: `TutorialServer.watchExtra`, the LEVELS watcher. `seen` is read at PlayerAdded (0). `PlayerData.load` then sets SlingLevel (1 or more after step 8) and DataLoaded in one run. With Deferred signals, the handler runs after DataLoaded is true, so it counts the saved level as a purchase: TutorialExtra 2 → 0, plus the potion. Hits everyone who left during "Earn" and all OnboardStep-11 players.
   **Fix:** in `UpgradeServer`, fire `ServerStorage.UpgradeBought` (BindableEvent) after `levelUp` in the money branch (line 89) and in the Robux receipt when it succeeds (line 55). Never fire it from the FreeSling branch. In TutorialServer: `if TutorialExtra == 2 then set 0; GivePotion end`. Delete the LEVELS loop.

2. **Using the treadmill before step 8 skips steps 9-10.** Where: `watchExtra.tryRun`. New players start with TutorialExtra 1, and `tryRun` never checks how far they are. Your own treadmill mounts you on contact, which is likely while the first egg grows. After 5 s TutorialExtra becomes 2, and the FREE step-8 level then pays the reward. The player gets the old finish text and no reward row.
   **Fix:** in `tryRun` and the delayed check, also require `TutorialDone == true and not (FreeSling == true and SlingLevel == 0)`. Connect `tryRun` to FreeSling changes. Analytics already gates this way (`GATED_FROM`).

3. **Players who come back mid-tutorial never get 9-10.** Where: `PlayerData.load`, the TutorialExtra rule. Old saves stopped at steps 1-8 get 0. That is the biggest drop group.
   **Fix:** `isNew` → 1 (0 on TEST_FRESH); `data.TutorialDone == false or data.FreeSling == true or ob == 10` → 1; `ob == 11` → 2; otherwise 0.

4. **Step 10 can be impossible.** Where: `TutorialClient.nextUpgrade` / `extraStep`. At Rebirth 0, Sling Lv4 and every Fast Grab level need a rebirth. A player who already owns Sling Lv3 gets `nextUpgrade() == nil`: "Press the green button" on a REBIRTH 1 lock, with no arrow, until they rebirth.
   **Fix:** when TutorialExtra becomes 2 (and on load at 2), if they can't buy any money level at their rebirths, set 0 and give the potion. Also: `UpgradeClient.tutorialBuy` only points at Sling, but the title can say FAST GRAB. Point it at the row `nextUpgrade` picks.

5. **"Earn" can dead-end and gives nothing to do.** Where: `TutorialClient.extraStep`. With 0 pets placed (the 600 s hatch fallback, or pets moved to the hotbar), money never goes up. With one Grass pet it is a 1-2 minute wait with no arrow, and the sub line is the longest in the tutorial.
   **Fix:** with `#pets == 0`, show "Hatch a PET to earn $!" with target `PAD`. Otherwise use target `PAD` and the sub "$420 / $1.3K - grab more EGGS!".

**Checked, OK:** the client can't move steps or get the potion (server-set attributes); no double reward; getting off or dying cancels the 5 s timer; Auto Reconnect re-mounts count; rebirths keep levels; `finish()` closes the window cleanly; the phone offer sits above `RightTiles`.
