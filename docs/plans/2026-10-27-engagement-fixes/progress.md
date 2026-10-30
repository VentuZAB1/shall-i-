# Engagement fixes 2026-10-27 - progress ledger

Builder: Claude (Opus). Owner said "start". Fix 1 = BUILD (first egg runs always succeed). Fix 2 = PLAN + MOCKUP only.

## Log
- [x] Read vault (START HERE, 01 Rules, area notes) + game memory.
- [x] Fix 1: investigate root cause of 19.5% no-egg launches
- [x] Fix 1: backups -> ServerStorage._Backup_EngagementFix1027.Before
- [x] Fix 1: build
- [x] Fix 1: unit tests + TestFreshSave Play test (first 3 launches, Lv0/Lv1)
- [x] Fix 2: measure + Python sim
- [x] Fix 2: proposal + milestone table
- [x] Fix 2: banner mockup
- [x] Fix 2: WATER_WALL_PLAN.md
- [x] End: Studio in Edit, TestFreshSave false (verified)

## Fix 1 - root cause (probe: economy/egg_run_probe.py, real formulas from the Studio scripts)
- Every launch flies straight down the middle line (x = 0.5). Eggs never spawn within |x| < 7.7 (CENTER_X keep-out for the creature spots) and spread to |x| 42 over the whole area.
- 6 Grass eggs over ~360 studs of floor: the nearest egg to a Lv0/Lv1 landing is a median 36 studs away (90th pct 70-80); only ~1% of landings are already inside an egg's prompt reach (8 + 3 x size).
- Waves pass any runway spot every 9.7 s on average (WaveServer rhythm). Look around (~1 s) + walk + 1.5 s hold = ~3.1 s median before the grab -> ~28% of launches get a wave before the egg is in hand. Launch 1 is safe (tutorial hides server waves until the grab); launches 2-3 are the first time a new player meets real waves.
- Low-power shots do NOT land in the hub (min ~z -64..-90). Bat hits only drop CARRIED eggs (they hit Banked, not Grabbed). Inventory cap 150 irrelevant for new players.
- Eggs in Grass's first ~50 studs past the gate (z -70..-110) are almost never near a landing (nobody walks out; you can only fly in).

## Fix 1 - built (Studio, Edit) - backups in ServerStorage._Backup_EngagementFix1027.Before (7 scripts, disabled, untagged)
- NEW ReplicatedStorage.EggAssist (pure: predict / releasePoint / spot + numbers RUNS 3, REACH 16, HOLD 0.9, RESERVE 10 s, GRACE 2.5 s, SESSION_CAP 6)
- EggSpawner: assist on launch (watches SlingStart): predicts the landing (client flight loop), reserves an egg already in reach or pops a normal area egg 7 studs ahead / 9 to the side; carry() refuses other players while ReservedFor; a grab in an assisted run uses one up (EggAssist -1). Assist eggs are "extra" (no slot refill). Grass: 7 eggs + none before z -110. Studio hook ServerStorage.EggAssistDebug.
- PlayerData: field EggAssist (new saves + mid-tutorial saves 3, veterans 0).
- WaveServer + WaveClient: LandGraceUntil = no knock-out for 2.5 s after an assisted landing.
- EggClient: prompt off for others while ReservedFor. UpgradeClientLegacy: 0.9 s hold on your own reserved egg.
- Analytics: Egg Run field 02 = "Assist - Yes/No".
- NEW ServerStorage.EggAssistTests (pure + live).

## Fix 1 - tests (Play, TestFreshSave session 1793058343)
- pure 19/19 (Edit + Play), live 3/3 (EggAssist = 3 on a new save, Grass 7 eggs, none before z -110).
- Prediction vs real client landing: -274.627 vs -274.625, -334.144 vs -334.154, -278.615 vs -278.78 (< 0.2 stud).
- Launch 1 Lv0: egg 11.9 studs away, reach 16, hold 0.9 -> grabbed 1.2 s after touchdown, banked, EggAssist 3 -> 2.
- Launch 2 Lv1: 11.8 studs, grabbed 1.2 s after touchdown, banked, 2 -> 1.
- Launch 3 Lv1: 12.2 studs, grabbed 1.4 s after touchdown (0.35 s reaction), banked, 1 -> 0.
- Launch 4 Lv1: no assist (0 reserved eggs, Analytics "Assist - No").
- Runs where the harness was too slow (tool latency > 5 s) died to a wave AFTER the grace and kept their assist (by design); session cap counted 5 and was reset for the test.
- Reserved for someone else: server carry() refused, client prompt Enabled false -> cleared -> true.
- Wave grace: an Ultrakill wave passed through the player during LandGraceUntil, no knock-out.
- Console clean (only TopbarPlus version notice).
- Tutorial check (Play, TestTutorial + TestFreshSave): launch 1 -> guide "Grab an EGG!" and the assist egg IS the nearest egg (11 studs) -> grabbed -> "Run back to SAFETY!" (server waves still hidden, tutorial waves only) -> banked -> "Go back to YOUR BASE!"; onboarding funnel 1-5 normal. Console clean.
- After the tests: Studio in Edit, TestTutorial false, AnalyticsDebug cleared, TestFreshSave FALSE (set 2026-10-27 after the last Play).

## Fix 2 - plan + mockup (nothing built in Studio)
- Sim economy/water_wall_sim.py, calibrated to the onboarding funnel x first-session quit curve (pace x3 + 20 s idle per run, aim error 0.35 -> 0.20 s): free upgrade 4.7 min, Lv2 5.5, Water ladder 36% (live 33%).
- Today: first Water egg median 8.6 min (25-75% 6.5-12.4), 56% by 10 min, R1 11.7, R2 32.4. Lv1 (free) reaches Water on 2% of shots but falls <=105 studs short on 50%.
- Cash is not the gate (cheaper Lv2-3 alone: 8.6 -> 8.5 min). Proposal A+B+banner: Lv2 $600 / Lv3 $1.5K, range +30/+35/+30/+15 for Lv1-4 -> median 8.3 (6.3-10.4), 72% by 10 min, ladder ~42%, R1 10.7, R2 31.0.
- Mockups: near_miss_banner_mockup.png (+ _no_area_title, _zoom), make_near_miss_mockup.py. Backdrop = the 10-21 Edit capture (today's screen_capture was white x4, Studio not in front; computer-use focus request declined).
- WATER_WALL_PLAN.md written. Waiting for the owner.

## Fix 2 - owner answer + build (2026-10-27, later)
- **Owner:** "WATER IS ONLY XX STUDS AWAY is too big, maybe like a small text or do not add it, about the other things, yes add it."
- **A + B BUILT** (UpgradeConfig SLING_EARLY_COST + SLING_EARLY_RANGE).
  - Backup in `_Backup_EngagementFix1027.Before.UpgradeConfig`.
  - WaterWallTests: RED 12/19 -> GREEN 19/19.
- **Play test (TestFreshSave):**
  - Lv2 $600 OK ($599 refused); Lv3 $1,500 OK; Lv4 needs R1.
  - Speeds 188.7 / 205.1 / 218.4.
  - EggAssistTests 19/19 + 3/3. Console clean.
  - TestFreshSave back to false.
- **Banner:** small-text mockup `near_miss_small_mockup.png` (+ `_zoom`), script `make_near_miss_small.py`. The owner said "skip it": DROPPED.

## Owner to do
- Save + Publish (fix 1). Fix 2: approve or change the numbers + the banner look before anything is built.
