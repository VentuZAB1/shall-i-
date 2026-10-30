# Overnight report: 2026-10-21 night → 2026-10-22 morning

Everything below was done in your open Studio. **Nothing is saved or published.**
Studio was left in Edit, TestFreshSave is false, and TestStarterPack is true (Studio-only).

## 1. Lighting: "too bright", toned down
- Changed: Brightness 3 → 2.4, Exposure 0.15 → -0.05, Saturation 0.30 → 0.05, Contrast 0.17, Bloom 0.55 → 0.4, ambients down.
- **The animated sky, clouds and atmosphere are untouched.**
- Undo: the old values are in `ServerStorage._LightingPreview.Live_VIVID_before_SOFT`. The new values are recorded in `Live_SOFT_2026_10_21`.

## 2. Hub makeover (your rules: big walls, decor only on walls/ground, no trees/bushes/seats)
- **Big walls on every side:** 22.4 tall, with slate pillars, warm sandstone caps, an orange band and a pumpkin on every pillar. Two tall towers frame the runway mouth, which stays fully open.
- **Pumpkin hands:** the VineGrip vine "hands" are back on the back wall under the giant pumpkin.
- **On the walls:** 12 pumpkin garlands, 3 small bat flocks (static, no lag), 4 corner webs, and 8 lanterns. The lanterns are the night-boost lamps, so the night boost still works. There are also 8 soft night lights on the long walls.
- **On the ground:**
  - warm tan paving with subtle lanes
  - kerbs around the plots
  - lawn-green plot beds
  - 5 pumpkin piles at the wall feet
  - small candle and pumpkin piles at the 6 plot gates
- **Removed (into backup, not deleted):** every tree, bush, flower bed and bench, the floating island, the Halloween garden and the lamp posts.
- **Your example placements, fixed properly:**
  - **Shops:** mirrored exactly and facing the plaza.
  - **Leaderboards:** the 4 boards ring the chest, and each now has a screen on BOTH sides.
  - **Free Gift:** the zone and the FREE! sign moved onto the chest. They were left at the old spot, so claiming at the chest didn't work.
  - **Spawn:** moved off the chest.
- **Parts:** 4,737 of the 11,000 budget.
- **Play-tested:** walls (no escape, no stuck spots), placements, stall windows, the Free Gift claim, the boards, night lights, tutorial arrows on plots 1 and 6, a slingshot launch, the trailer view and the intro cameras.
- **Full hub test suite:** 110/0, green in 2 separate fresh sessions and a 3rd rerun. Fixing the test order uncovered one real test bug: a teleport dragged a welded treadmill. The tests now handle that.
- **Undo, one step:** `require(game.ServerStorage["_Backup_HubMakeover.Before"].Revert:Clone())()` in Edit.
- **Your call:** your 2 front leaderboards show in the background of 3 intro-cutscene shots. They block nothing, so I left them. If you don't like it, move those two boards out a little.
- **Docs and shots:** `docs/plans/hub-2026-10-21/makeover/` (FINAL.md, `shots/fix_*` = final, `after_*` = first build, `before_*`).

## 3. HATCH NIGHT UI, now on 8 windows
- Done: the Gift window, the Starter Pack popup, the Shop, Settings, Index, Rebirth, Free Gift, Welcome Back and Upgrades.
- Every window keeps its old layout; only the look changed.
- Each one keeps its old script as a **switched-off backup for 7 days live** (`*Legacy`).
- Closed windows do no work, and none of them leak.
- All test suites pass.

**Decisions I made with your "do as recommended" (each one is easy to flip):**

| Window | What I did | How to change it |
|---|---|---|
| Left menu on PC | It now looks smaller. A startup bug was often giving PCs the phone size (1.3x); it's fixed, so PC gets its real size. | Tell me if you want the bigger size on purpose (one number). |
| Index | Creature names show only in the right panel. | `SHOW_CARD_NAMES = true` at the top of IndexClient |
| Index | NEW red "!" on the Index button when a reward is waiting. | `TILE_BADGE = false` |
| Welcome Back | CLAIM x5 is gold, like every Robux button. | A switch at the top of the script brings back the rainbow. |
| Upgrades | A button you can't afford is dark, not red. | A switch at the top of the script |
| Upgrades | During tutorial step 10, the +1 LV Robux button is hidden so new players don't mis-tap. | A switch at the top of the script |
| Free Gift / Welcome Back / Upgrades | The hotbar hides while the window is open; it was covering the CLAIM buttons. | — |

**Open question:**
- **Tutorial on phones.** During tutorial steps 8, 10 and 11, the Upgrades and Rebirth windows move down and shrink so they fit under the tutorial text. On small phones the text gets small (about 9 pt).
- **My recommendation:** hide the tutorial's top text while that window is open; the arrow alone is enough. This is a small tutorial change. Say yes and I'll do it.

**Shots:**
- Popup and Shop: `docs/plans/hatch-night-build/popup_shop/` (with `v2/`)
- Settings, Index, Rebirth: `ris/{settings,index,rebirth}/`
- Free Gift, Welcome Back, Upgrades: `uwf/{freegift,welcome,upgrades}/`

## 4. Your to-do list
1. **Look around in Studio:** the hub, day and night (Settings → Time), and the 8 windows.
2. **Creator Hub:** set the **server size to 6**. Live is still 3, so the 6 plots won't fill.
3. **Save, Publish, then Migrate to Latest Update.**
4. **Live check:**
   - you spawn at your own gate
   - the treadmill works
   - the stalls work
   - the Free Gift claim works at the chest
   - F9 memory looks normal
5. **Phone check (2 min):** open the Shop on your oldest phone with the MicroProfiler. If opening it stutters, there is a flag `SNAP_SHOP_ON_TOUCH` that turns the open animation off on phones.
6. **Later:**
   - Delete the `*Legacy` scripts after 7 days live.
   - Delete the `_Backup_HubV2` snapshots.
   - Keep `_Backup_Hub.Before` and `_Backup_HubMakeover.Before` until you're sure.

## 5. Next, when you say go
- **HATCH NIGHT:** the main HUD, then the Admin menu (last).
- **Waiting on your yes:** Next Goal bar + Daily Quests (spec ready), and the Starter Pack "LAST CHANCE" comeback.
