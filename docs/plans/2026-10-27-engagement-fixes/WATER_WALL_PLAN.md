# Water wall plan (engagement fix 2): PLAN + MOCKUP ONLY

Date: 2026-10-27.

**Status (later on 2026-10-27):**
- **A + B BUILT in Studio** after the owner said "about the other things, yes add it". Not published.
- **The banner was "too big":** the owner said "maybe like a small text or do not add it". A small-text mockup followed; the owner then said "skip it". The banner is DROPPED.

**What was built:**
- `ReplicatedStorage.UpgradeConfig`:
  - `SLING_EARLY_COST = {[2] = 600, [3] = 1500}`
  - `SLING_EARLY_RANGE = {30, 35, 30, 15}`, added in `slingRange`
- Backup: `ServerStorage._Backup_EngagementFix1027.Before.UpgradeConfig`.
- Tests: `ServerStorage.WaterWallTests` (pure). It failed 7/19 before the change and passed 19/19 after it.
- Play test with TestFreshSave:
  - Lv2 bought for $600 ($599 = "Not enough money"); Lv3 for $1,500.
  - Lv4 at R0 = "Need Rebirth 1".
  - SlingMaxSpeed Lv1 188.7, Lv2 205.1, Lv3 218.4 (was 182.4 at Lv1).
  - EggAssistTests still pass, pure 19/19 and live 3/3.
  - The console was clean.
Sim: `economy/water_wall_sim.py` (output: `water_wall_sim_output.txt`, same folder as this plan). It uses the flight model in `economy/egg_run_probe.py`.

## 1. What the game does today

**World:** the slingshot fires from z -45. Water starts at z -460, which is ~415 studs from the slingshot and ~424 from where the rider lets go. Thunder starts at z -860.

**Slingshot Power** (UpgradeConfig: range 370 + 77.2 studs per level; Lv4+ needs Rebirth 1). Water% is the chance a launch lands in Water. Near-miss% is the chance it lands 105 studs or less short (the banner range). Both use "learned" aim, about the 6th launch.

| Level | Price | Range | A perfect shot lands at | Water% | Near-miss% |
|---|---|---|---|---|---|
| Lv0 | – | 370 | z -394 (Grass) | 0% | 19% |
| Lv1 | free in the tutorial | 448 | z -471 (11 studs into Water) | **2%** | **50%** |
| Lv2 | $1.3K | 525 | z -548 | 30% | 41% |
| Lv3 | $3.4K | 602 | z -624 | 52% | 30% |
| Lv4 | $8.8K, R1 | 679 | z -702 | 66% | 22% |
| Lv5 | $23K, R1 | 756 | z -779 | 76% | 16% |

**Money in the first 10 minutes:**
- A Grass pet earns 20 × KG^0.25 × rarity, a median of ~$33/s.
- With 3 slots, a player has ~$100-150/s by minutes 5-8. Water pets earn ~6× that.
- By the end of the tutorial (~5 min), about half of new players already have the $4.7K for Lv2 + Lv3.

**Today's minute-to-Water.** The sim is calibrated to the live funnel × the first-session quit curve. The calibrated pace gives the free upgrade at 4.7 min, the first money upgrade at 5.5 min and a Water ladder of 36%. Live: ~4.2 / ~4.9 min and 33%.
- **First Water egg: median 8.6 min after joining. 25% of players get there by 6.5 min, 75% by 12.4 min.** Only 56% have one by minute 10.
- First Rebirth: 11.7 min. Rebirth 2: 32 min.

**What the numbers say:**
- The *median* is already inside the 8-12 min target. The wall is the slow half: those players need 3+ egg runs, and every run takes ~2 min at real-player pace.
- Meanwhile, 56% of new players are gone by minute 5 and 80% by minute 10.
- The free Lv1 reaches Water on only ~2% of shots, but it falls just short on 50%.
- **Cash is not the main gate.** Making Lv2 + Lv3 cheaper moves Lv3 from minute 7.4 to 5.7, but the first Water egg only moves from 8.6 to 8.5. Aim precision plus the run length are the gate.

## 2. Proposal: three small steps (no world moves, waves untouched)

| | Change | Today | Proposed |
|---|---|---|---|
| **A** | Slingshot Power **Lv2 / Lv3 price** (`UpgradeConfig.slingCost`, Lv4+ unchanged) | $1.3K / $3.4K | **$600 / $1.5K** |
| **B** | **Early range** bonus for Lv1-4 (`UpgradeConfig.slingRange` + {30, 35, 30, 15} studs; Lv5+ unchanged, so Thunder still opens at Lv6) | 448 / 525 / 602 / 679 | **478 / 560 / 632 / 694** |
| **Banner** | Near-miss top banner (section 3) | – | "WATER IS ONLY 12 STUDS AWAY!" |

Effect of B on Water% per launch:
- Lv1: 2% → **13%**
- Lv2: 30% → **41%**
- Lv3: 52% → **58%**
- Lv4: 66% → 69%

Notes:
- Robux "+1 LV" bands, rebirth locks, the late-game curve and the Water / Thunder positions all stay as they are.
- The tutorial step 10 text ("Earn $600 for an UPGRADE!") picks up the new price by itself.

### Before / after milestones

Median minutes since joining, 400 simulated new players each:

| Setup | Lv3 bought | First Water landing | First Water egg (25-75%) | Water egg by 10 min | Rebirth 1 | Rebirth 2 | Water ladder* |
|---|---|---|---|---|---|---|---|
| **Today** (fix 1 built) | 7.4 | 8.6 | 8.6 (6.5-12.4) | 56% | 11.7 | 32.4 | 36% |
| A only (cheaper Lv2-3) | 5.7 | 8.5 | 8.5 (6.4-11.7) | 61% | 10.7 | 32.1 | 38% |
| B only (early range) | 7.5 | 8.4 | 8.4 (6.3-10.8) | 64% | 11.0 | 31.7 | 39% |
| A + B | 5.7 | 8.3 | 8.3 (6.4-10.7) | 67% | 10.7 | 31.5 | 40% |
| **A + B + banner (recommended)** | 5.7 | 8.2 | 8.3 (**6.3-10.4**) | **72%** | **10.7** | **31.0** | **42%** |

\* Water ladder = the share of Grass egg grabbers who also get a Water egg, weighted by the live quit curve. The live value today is 33%.

- **Recommended: A + B + banner.**
  - The average new player gets Water at ~8 min; 3 in 4 are there by 10.4 min (today: 12.4).
  - The Water ladder rises ~36% → ~42%, about +17% relative. Rebirth 1 comes a minute earlier.
- Optional C: a fix-1 assist egg on a player's FIRST Water landing. It adds +1 point by 10 min and reuses the fix-1 code.

**Caveats:**
- Aim skill and real-player pace are fitted to the funnel, so trust the differences more than the absolute minutes.
- The sim's Rebirth 1 (11.7 min) is earlier than the funnel suggests (~15 min).
- The banner's effect is an ASSUMPTION: after a near miss, the next shot's power error is 30% smaller. Check it with the NearMiss analytics event after launch.

## 3. Near-miss banner (mockup only; the owner judges it)

**Mockups:**
- `near_miss_banner_mockup.png`: the moment of landing, with the game's existing "Grass 🌿" area strip on screen at the same time.
- `near_miss_banner_mockup_no_area_title.png`
- `near_miss_banner_mockup_zoom.png`: 2× zoom of the banner.
- Script: `make_near_miss_mockup.py`.

**Backdrop:** a real Studio Edit capture of the Grass runway with the HUD visible (`lighting-2026-10-21/6_vivid_cumulus_runway.jpg`).
- Today's `screen_capture` came back white 4 times, because Studio was not in front and my request to bring it forward was declined.
- The HUD in today's capture is identical to the HUD in this backdrop.
- The banner is drawn in Montserrat Black, the GothamBlack look-alike Roblox ships in Studio's content/fonts. In game it is real GothamBlack.

**Look** (the same Check-UI floating text as the owner-approved REBIRTH READY! banner):
- One line, centred at y 0.22, just under the area strip.
- Chunky GothamBlack with a 3.5 px black outline × device scale.
- White text, with the area name in its own area colour (Water blue 60,200,255) and the distance in tutorial amber #FFD000.
- No panel, no icon, no floating world sign.
- It pops in (Back, 0.45 s) and stays ~3 s.

**Rules (when built):**
- Shown once per launch, at touchdown, when the landing is short of the next area's start by at most 25% of the distance to it. That is about 105 studs for Water.
- Distance = studs short, rounded up ("1 STUD" singular).
- Only for an area the player has never reached (Index found-list).
- Never during the tutorial run, never over an open window, never while another top banner is popping.
- Client-only. No gameplay effect and no Robux link. It is a free launch, not a paid roll, so the vault's "near-miss on paid rolls" warning doesn't apply.
- Analytics: a custom event "NearMiss" (field 01 = area) so its effect can be measured.
- Frequency check: at Lv1, half of all launches are near misses, so new players will see it often for a few minutes. That is the point, but the owner may want it once per session per area instead. That is a one-line switch.

**Build plan (after a yes):**
- A small `NearMissClient` LocalScript next to SlingshotClient. It reads the landing from the client's own flight (the Landed moment) and the area starts from the `AreaZone` parts.
- ScreenGui `NearMissUI`, DisplayOrder 6, IgnoreGuiInset.
- Phone check in the emulator: at device scale ~0.63 the line is ~60% of the screen width.

## 4. Files
- Sim: `economy/water_wall_sim.py` (calibrated defaults, `python water_wall_sim.py 400`).
- Flight model: `economy/egg_run_probe.py`.
- Output: `docs/plans/2026-10-27-engagement-fixes/water_wall_sim_output.txt`.
- Mockups: `docs/plans/2026-10-27-engagement-fixes/near_miss_banner_mockup*.png`.
- Nothing about fix 2 was changed in Studio.
