# Plan review: Redesigned Hub (A HORSESHOE)

Reviewer: plan reviewer (Opus), 2026-10-21. Read-only review.
Reviewed: `docs/plans/2026-10-21-redesigned-hub.md` against the binding spec `docs/specs/2026-10-21-redesigned-hub-design.md`,
the layout files in `docs/plans/hub-2026-10-21/`, the memory notes, and the owner's Studio.

How I checked it:
- Re-ran `tools/hub_layout.py` on a copy: ALL PASS (49 lines). Re-ran `tools/fence_parts.py`: 284 / 347 / 658 / 811 / 883 / 564 fence+floor parts at R0-R5.
- Edit-mode, read-only Luau (`execute_luau` in Edit only): a scan of all 188 non-backup scripts for `Hub` lookups and hub-area
  Vector3/CFrame literals, the tag census, the old hub's colours, the board/stall/treadmill-tier extents, the gate-door reach on
  the live Base2, and the Halloween garden inventory. While another agent was in Play, I only used `script_read`/`script_grep`
  and the 2026-10-15 code snapshot in `Desktop/ROBLOX PLAYBOOK/slingshot-code`. I never started or stopped Play.

---

## Verdict: APPROVE WITH CHANGES

The architecture is right. It uses off-map staging with no tags, `_SwapTags`/`_RemovedTags`, the same names so that only 4 scripts change, one
generated layout module, a Python checker plus an in-Studio validator that checks rules rather than decor positions, and a `fitEggs` that
mirrors the existing, tested `rebase()`. I confirmed the "no change" claims in the code (see "What's good").

The 14 MUST items below are mostly tests and validator checks that would fail by design. They also include one real
Trailer bug, one visual bug (the owner-card backing), one runtime layout clash (high-tier treadmills vs upgrade signs) and
three "looks" gaps against the owner's own sketch and playbook. All can be fixed inside the plan. None of them changes the
architecture.

---

## MUST changes

1. **Trailer hatch spot (Task 8): stop using `Plot:GetBoundingBox()`.**
   - The problem: `Trailer.lua` ~569-575 sets `hatchPos` from `plot:GetBoundingBox()`. The new `Plot.Look.SlotBed` (60 x 90) and the sign parts
     are inside `Plot`, so the box centre becomes the Slot centre. At R0 that is 25 studs behind the fenced floor's centre, outside
     the back fence. S6 (hatch) and S11 (big-number orbit) would play on the unclaimed land.
   - The fix: `local floor = base.Plot.Floor; hatchPos = (floor.CFrame * CFrame.new(0, floor.Size.Y / 2, 0)).Position`.
   - Add to the Task 8 string test: `plot:GetBoundingBox()` no longer appears in the Source.
   - Add to T10.10: `BaseConfig.inside(floor, hatchPos, 0)` is true.

2. **Owner name sign (Task 1): the planned `SignBoard`/`SignFrame` will cut the owner card in half.**
   - The problem: `OwnerSign.Card` is a camera-facing BillboardGui (17 x 14 studs, `AlwaysOnTop = false`, bobbed ±0.35 by BaseSignFloat). A
     fixed board 0.6 behind it is depth-tested against the turning card. At any view angle above ~4° off the board's normal,
     one half of the card goes behind the board and disappears.
   - The fix: keep the card as it is. Replace `SignBoard` + `SignFrame` with a low sign that stays under the card's lowest edge
     (floorT + 11 - 7 - 0.35 = 4.15):
     - `SignPostL` / `SignPostR`: (0.8, 3.2, 0.8) at `root * (∓7, floorT + 1.6, hz - 1.0)`.
     - `SignPlank`: (15, 1.0, 0.4) at `root * (0, floorT + 2.6, hz - 1.0)`, Color (58, 36, 24).
     - `SignTrim`: (15.4, 0.3, 0.5) at `root * (0, floorT + 3.25, hz - 1.0)`, Color = accent.
     - All tops are ≤ floorT + 3.4.
   - Update the `Look` name list in the Task 1 test.
   - Do NOT convert the card to a SurfaceGui now. It would need changes to BaseSignFloat (`StudsOffset`, `rect()`), Trailer `hideCards`/`hideBases`
     (BillboardGui only) and `BaseManager.setSign`. A card inside `Look` would also be destroyed on every rebuild.

3. **The gate door hangs outside the Slot. Fix 3 assertions.**
   - The problem: BaseBuilder opens `Fence.GateDoor` 74° outward. Measured on the live Base2, the door reaches z = -43.27 in Slot space, while the
     Slot front edge is at -40. That is 3.27 beyond the edge. So these assertions fail at every r: Task 1 Step 1 ("every Plot BasePart
     except SlotBed inside the Slot ±0.5"), Task 4 Step 4 and T10.3.
   - The fix: exclude `Fence.GateDoor` from those checks, or allow up to 3.5 of overhang on the front (local -Z) side only.

4. **Treadmill tiers: re-check the layout with the biggest tier.**
   - The problem: the checker and validator use the Tier 1 footprint (9.1 x 16.1). TreadmillServer swaps in tiers 2-11 at the same pivot.
     Measured in pivot space, Tier 11 spans x ±7.4, y -0.6..15.8, z -11.1..+9.2. That is 9.2 toward the plot and 11.1 toward the plaza.
     Tiers 5-11 are all about 14.2-14.8 wide.
   - The result with Tier 11:
     - Plots 3/4: `UpgradeSign_B3/B4` (R 24.5..28.5, F 5.4..6.6) overlaps the treadmill (R up to 25.4, F 5.1..25.4) by about 0.9.
     - Plots 1/2/5/6: only 0.6 of clearance, below the checker's own 1.5 rule.
   - The fix:
     - Put the Tier 11 box (asymmetric along F) into `hub_layout.py`, re-run it, and move the signs. For example, SIGN_S = 30 for all plots;
       for 3/4, nudge the corner boards so the sign still clears them.
     - Regenerate `HubLayout.lua`.
     - Validator check 12 must place every `ServerStorage.Assets.Treadmills` template's extents at each `PLOTS[N].treadmill`
       pivot and run the overlap and walking-line rules on them.

5. **Validator checks 7 and 8 need exact exceptions. Otherwise Task 3 and the live check can never pass.**
   - Check 7: "No CanCollide part ... intersects INTRO_ZONE" catches the plaza medallion. It is 51.8 wide with a top at about 0.3, centred
     at (0, 20), so it covers z -5.9..45.9. It also catches the SpawnLocation edge at z 12. Define the rule as: fail when a part's top is
     more than 0.8 above y 0. Floor-like parts with top ≤ 0.8 pass whether or not they collide. The Slingshot and LaunchPlatform stay
     as exceptions.
   - Check 8 in `"live"` mode: the main lines from ENTRY (0.5, -56) to plots 2, 3, 4 and 5 cross the LaunchPlatform. ENTRY to plot 2
     passes x -8.8 at z -45, which is the left fork post. Add `Slingshot`, `LaunchPlatform` and anything under `Map.Runway` to the
     check 8 exceptions. Without this, Task 9 Step 3 ("live" = 0 failures) is impossible, and a builder may "fix" it by moving fixed parts.

6. **T9.4 tag census: count only workspace copies, and never strip template tags.**
   - The problem: it fails on legitimate tags as written.
     - `AdminTreadmill` has 51 copies outside workspace: `Assets.Treadmills`, `_TreadmillLabKit`, `AdminUI.Trailer.Assets` and old
       backups. No script reads this tag.
     - `LaunchGate` has 2 copies in `_Backup_HubLayout.ScoreBridge`.
   - The fix:
     - Per tag, count only `IsDescendantOf(workspace)`: Base 6, Treadmill 6, AdminTreadmill 6, Slingshot 1, LaunchPad 1, LaunchGate 1.
     - Assert 0 tags under `_Backup_Hub.*`, `_Backup_HubV2` and `HubV2Kit`.
     - Add to the plan: never strip tags from `ServerStorage.Assets.*` or `AdminUI.Trailer.Assets`. They are clone sources.

7. **T10.7 walker: use pathfinding instead of straight lines.**
   - The problem: straight `Humanoid:MoveTo` over all 110 ordered pairs fails by design. For example, plot 1's spawn spot (-114, -30) to plot 2's (-82, 42) runs
     straight through the Upgrade stall counter (pivot (-104.4, -7.0)). Plot 5 to plot 6 runs through the Sell stall.
   - The fix:
     - Walk every pair with PathfindingService: `CreatePath` + `ComputeAsync`, then MoveTo each waypoint. Fail on `NoPath` or on a waypoint
       not reached within 3 s.
     - Keep straight MoveTo only for the checker's lines: ENTRY and the gate edges to each spawn spot, and each spawn spot to its own
       treadmill exit.

8. **T10.4: unequip the pets before the egg-capacity test.**
   - The problem: at R20 the 23 equipped pets use all 23 pet slots. `HatcheryDebug "place"` calls the validated `place()`, so every placement
     returns "Pet slots full", never "No room".
   - The fix: unequip all pets first (`HatcheryDebug "unequip", player, petId` for each pet), then place 100,000-KG StormEggs until "No room",
     then re-equip.

9. **Edge walls: nobody may stand on them, and fix the T10.6 expectation.**
   - The problem:
     - The bounds column sits 2..6 studs outside the floor, and MapGuard's `inWall` adds a 1-stud margin. So "outside" starts 1 stud past
       the floor edge.
     - The 4-stud wall (0..2 outside) is jumpable. A player on its inner half is fine; on its outer half they are teleported back. That is
       rubber-banding.
     - T10.6's "on the wall top centre: moved within 0.6 s" sits exactly on the boundary (`|p| < 3` is false), so it fails or flickers.
   - The fix:
     - Add a `WallCap` to every edge wall: invisible, CanCollide true, CanQuery/CanTouch false, CastShadow false, 2 thick, from the wall
       top to y 12, in `Hub.EdgeWalls` (not in `Map.Bounds`).
     - T10.6 then asserts that a jump at each wall never lands on top of it, and keeps "1.5 inside the edge = not moved".

10. **The performance check must include pets.**
    - The problem: spec §5.5 asks for "the cost of 6 grown plots with pets". Task 11's `fill` + `grow(i, 4)` gives fake owners with no pets.
    - The fix:
      - Add a Studio-only `BaseDebug "pets", baseId, n`. It creates n `Pet_<id>` Configurations in `BaseContent.Base<N>.Pets` with the
        attributes `spawnPet` sets: Creature, KG, Scale, Motion, From/To/T0/Dur/State, Owner = the fake id. PetAnimator then builds and
        animates them.
      - Measure 6 plots at R4 with 23 pets each, from two spots:
        - the plaza centre, where all 6 plots are inside PetAnimator's `ANIMATE_RANGE = 220`, so up to 138 animated rigs (today's maximum is 69);
        - plot 1's spawn spot.
      - Record the animated-pet count next to frame time and memory.

11. **Rollback must be one real step. Do not restore BaseHatchery.**
    - (a) Write `HubV2Kit.Swap` and `HubV2Kit.Rollback` as one ModuleScript function each. Each is idempotent, checks its own steps, and stops at
      the first failure.
      - Rehearse in Edit before any publish: Swap → `Validate(live)` → Rollback → `GetTagged("Base")` = 3, all in workspace, and the old
        hub intact → Swap again.
      - Record both results in the ledger.
    - (b) Rollback step 6 must say: do NOT restore BaseHatchery.
      - Eggs saved on the new 90-long plots can sit up to z ±(45 - 4 - r) from the floor centre. Only `fitEggs` pulls them back inside the
        old 80-long plots.
      - Restoring the old BaseManager and BaseBuilder is fine. Keeping the new versions is also fine.

12. **Plaza ground colour: decide it with the owner at Task 3, before anything is built on it.**
    - The problem: the owner's chosen sketch (`A_horseshoe.png`) and `planned_layout.png` both show a cream plaza. Task 3 builds it green
      (128, 170, 96).
      - That is the same colour family as the plot `FloorTop` (80, 165, 62) and `SlotBed` (110, 150, 82): green plots on green slots on a
        green field. Most servers will show mostly R0 40x40 plots, since only about 11% of players ever reached R1 before v6.
      - It also breaks the playbook's "colour-code areas".
    - The fix:
      - At Task 3 Step 4, shoot two top-downs and let the owner pick:
        - (A) green as planned;
        - (B), recommended: plaza = the old path/plaza cream "Brick yellow" (222, 205, 170), Plastic + Studs, with the existing
          "Burlap" (198, 176, 140) and "Red flip/flop" (150, 118, 88) as edge and medallion trims.
      - Plots stay grass either way. `SlotBed` gets a clearly different "unclaimed" tone.
      - Write the chosen RGBs into the plan before Task 4.

13. **Permanent decor and lights that survive the end of October.**
    - The problem: Owner action 4 deletes `HalloweenDecor`, and with it all 8 lamps. What is left over about 36,000 sq studs of plaza:
      2 round trees, 2 blossoms, 2 rocks, 4 benches, the gate beds, the alley bed and the medallion.
      - Night mode would go dark (there are no lights at all).
      - It breaks the playbook's "keep it dense".
    - The fix: add a permanent layer in `Hub.Decor`:
      - (a) `Lamps`: 8 permanent lamp posts at `LAMP_SPOTS`. For example, the StreetLamp `Post` + `Cage` with a warm PointLight that carries
        `NightBrightness` / `NightRange`. The Halloween layer only adds the pumpkin head and web on top.
      - (b) Tree, bush and rock clusters from `ServerStorage.HalloweenGardenBackup`: 6 TreeRound, 6 Blossom, Bush/BushSmall, Rock and the
        grass tufts. No Mushrooms (the owner removed them). Place them in the wedges between the walking lines, the 4 dead corners and
        behind the boards and stalls.
      - Add a checker rule: no plaza circle of radius 25 is free of decor, except on walking lines, rings, the medallion and the spawn.

14. **Halloween layer: re-place the free-standing HQ garden (spec §1 says "re-placed").**
    - The problem: the plan says only the wall-bound items are dropped. It also silently drops the owner-requested HQ garden from 2026-10-12
      (two review rounds): 5 TPTree, 5 DeadTree, 3 HauntedTree, 7 Bush_Thorn, 4 Bush_TP, 3 Bush_Autumn, 3 Bramble and 64 DeadGrass.
      - All of these are free-standing.
      - All of them have templates in `ServerStorage.HalloweenTemplates`: `Halloween_TPTree`, `Halloween_DeadTree`, `Halloween_HauntedTree`,
        `Halloween_Bush_Autumn`, `Halloween_TPBush`, `Halloween_Bramble`, `Halloween_Bush_Thorn`, `Halloween_DeadGrass_A/B`.
      - Task 6 under-lists that folder. It also holds garlands, webs, pumpkin eggs, candles and a bat.
    - The fix:
      - Re-place the garden pieces in `HalloweenV2`: the wedges, the alley and around the boards, with fronts toward the plaza. Hang a few of
        the 20 garden spiders on the trees again.
      - Keep the owner rule: CanCollide/CanTouch/CanQuery false, Box collision.
      - Then list exactly what is dropped: Garlands, Vines, WallBats (4,620 instances; dropping them is a performance win) and wall grime.

---

## SHOULD changes

1. **`fitEggs`:**
   - Share one helper with `rebase()` (same loop; old CF = current floor CF).
   - Use two passes:
     - Pass 1 keeps every egg that is already inside and clear of the others. A valid egg must never move.
     - Pass 2 places only the misfits with `findSpot` against all the kept eggs.
   - When `findSpot` returns nil, fall back to `BaseConfig.clampInside` + `warn`, not `or world` (which leaves the egg outside the fence).
   - Add a T2.3b case: Rebirths 5 (60 x 90), 6 eggs at the old 64-wide limit x = ±(28 - r). Expect all of them inside, and the untouched
     records byte-equal.
2. **T2.3:** give the injected second egg record its own id (8-char GUID), plus kind, kg and `readyAt = os.time() + 600`. Otherwise
   `Egg_<id>` and `grow[id]` collide.
3. **T10.2 (seventh player):** assert that `BaseData` and `EggInventory` stay byte-identical for 10 s. Then restore the base owner, or end the
   Play session, before the next test.
4. **Staging hygiene:**
   - Keep at most the 2 newest `Stage*` snapshots. Each is a full HubV2 clone, and ServerStorage loads on every live server.
   - Delete all of them after the owner's live check.
   - Tell the owner not to Publish while `Map.HubV2` exists, because it would ship to live servers (Leaderboards also draws the staging
     boards). Or park it in ServerStorage between build sessions. It has no tags or scripts, so that is safe.
5. **Version checkpoints:** before Task 9, ask the owner to Save, and write the place version into the ledger. Publish only after Task 11.
6. **Performance:**
   - Run a first measurement in staging before the swap: the staging plots rebuilt at R4 by BaseBuilder, with the camera over the
     staging plaza.
   - The picket cap saves about 15% (11 → 9 parts per section), not 25%.
   - A free, invisible saving: one `Collider` per fence line instead of one per section, about 65 fewer parts per plot at R4.
7. **Streaming:**
   - Set `ModelStreamingMode = Atomic` on each `UpgradeSign_B<N>` and each board model.
   - In `BaseManager.spawnAtBase`, call `pcall(player.RequestStreamAroundAsync, player, spot)` before `PivotTo`. The spawn (0, 20) is
     about 125 studs from plot 1/6's spawn spots.
8. **Trailer S8 camera:**
   - The problem: it is offset along the treadmill's RightVector.
     - Plot 6: it lands at (99.7, 5.6, -64), outside the floor edge.
     - Plot 4: it lands at (74, 5, 55.7), inside the TimeBoard footprint.
   - The fix: flip the side toward the plaza, using the sign of R·(plaza centre - treadmill). In T10.10, check the S6, S8 and S11 freeze
     frames for plots 1, 4 and 6.
9. **`BaseDebug "fill"`:** also turn on the 6 owner cards (a placeholder name and a real headshot id). The screenshots then show a full server, and
   BaseSignFloat's overlap logic gets exercised.
10. **Validator check 15:** also assert that each board's screen faces the plaza: `pivot.LookVector · ((0, 20) - pivot) > 0.5`. I verified that
    the live boards' pivot LookVector equals the screen normal (Face Front).
11. **Cheap seasonal accents that need no walls:**
    - Corner and torn webs on the stall roofs, the board frames and the lamp cages.
    - One `Halloween_Garland_Long` strung between the Speed and Heaviest boards over the Free Gift. Their inner edges are about 19.6 apart,
      which makes a gateway.
12. **`SlotBed`:** make it 0.2 thick (top at y 0.2, still under `FloorTop`). A 0.1 gap over the ground z-fights at 150+ studs on mobile GPUs.
13. **`Runway_L_1` / `R_1`:** keep the original Y size and position from `_OrigSize` / `_OrigCFrame`, and change only the Z extents. Don't
    hard-code y 540 / 1000.
14. **Owner edit freeze:** from Task 3 until the swap, the owner should not hand-edit `Map.Hub` / `HalloweenDecor`. Those edits go to the backup at
    the swap.
15. **TestFreshSave wording:**
    - Replace "require true" with: "if false, set it true in Edit, read it back, then Play; set it false after the session's last Play".
    - Never flip it while another agent's Play session is running.
16. **Values to write down, so the builder doesn't guess:**
    - Edge-wall `TopTrim` = Storm blue (69, 95, 132).
    - Walls (96, 132, 170).
    - Old medallion bbox centre (0, 0.155, -33.5), so the translation delta is (0, 0, 53.5).

---

## What's good

- **Layout:**
  - It matches the owner's U. Gaps at 60 x 90 are 12 / 20.9 / 20 / 20.9 / 12. Gate to slingshot is 122.4-129.5 (rule ≤ 140), with
    fairness 1.058.
  - The launch zone and intro corridor are kept clear. The stalls sit in side pockets off every walking line, and the rings clear the
    lines by 12.4 / 12.4 / 14.2.
  - The 130-deep plaza is correct. The spec's "185 x 180" and "≤ ~140" can't both hold with the slingshot on the front edge; a 180-deep
    plaza puts the back gates about 180-220 away. The plaza is wide, not cramped (180-244 wide).
- **The "only 4 scripts change" claim holds.** My scan of all 188 non-backup scripts found hub coordinates only in IntroCutscene, the Trailer
  and two dev tools.
  - IntroCutscene: I checked every shot. START, HOP_FROM and FINISH and all hub cameras stay inside x -12..24, z -40..12. They look
    into the plaza or the runway, and the occluder fade covers `Hub.Decor`, `MarketCorners` and `HalloweenDecor`.
  - Everything else finds hub items by name, tag or attribute, and handles streaming: TreadmillServer/Client, TreadmillSignClient,
    ShopClient, TutorialClient, OfflineClient, HatchClient, Upgrade/SellClient, FreeGiftServer/Client, Leaderboards (attribute scan),
    LeaderboardScroll (re-scans every 2 s), MapGuard (Bounds + recursive "Spawn"), VipClient/MapGuard rooms (runway), SlingshotServer
    (GateZ, workspace tag), EggSpawner (GateZ + 2), WaveServer, WeatherServer (runway AreaZones), AutoReconnect (MountTreadmill), and
    PetPlace/EggPlace (`Plot.Floor` plane).
- **Data path:**
  - `fitEggs` is the existing `rebase()` with old = new floor. That is tested code: it changes only x/z, leaving mutations, `readyAt`
    and pets untouched. Pets have no saved positions; they clamp with `clampInside`.
  - PlayerData sets `Rebirths` before `DataLoaded`, so BaseManager's rebuild runs before `loadBase` under deferred signals, and the
    refit uses the grown floor.
  - A 7th player never reaches `loadBase`, so their BaseData is never written.
- **The tags and the staging spawn:**
  - The tag rules (none in staging, `_SwapTags`, `_RemovedTags`, a census) directly address the 2026-10-21 launch bug.
  - `Spawn_V2` stays disabled, which accounts for MapGuard's `FindFirstChild("Spawn", true)`.
- **Things the planner caught:**
  - The spec's "64 x 120" is really 64 x 80 in Studio.
  - The `Runway_L_1` / `R_1` columns reach 11 studs into the new plaza.
- **Process:** TDD steps, a ledger, stage snapshots, script backups, one builder at a time, no command bar, no CameraType changes, and the owner
  publishes. The staging area (x 1740..2260, z -125..295) is empty; I checked.

---

## Owner's calls

1. **Plaza surface:** cream paving (like the approved sketch and today's paths) or green (as planned). See MUST 12.
2. **Walk length:** new walks are 122-130 studs; today they are 61 (Base2) to about 100 (Base1/3). The plan picked equal walks.
   - Pulling plots 1/6 in to x ±105 would make theirs about 107, but fairness would drop to 1.21.
   - If you want it tighter overall, the middle plaza (180 wide) could lose about 20-30 studs.
3. **Low 4-stud walls:** your playbook says "walls ≥10 tall, skyline backdrop"; the spec picked low walls with the open cloud sea. You could add a
   permanent backdrop behind plots 3/4, at the end of the alley where the giant pumpkin stands in October (a big statue, tree or rock
   arch), so the back of the hub isn't empty after Halloween.
4. **Stalls:** Upgrade on the left and Sell on the right, as in your sketch. That means plots 4-6 walk about 200+ studs to the Upgrade stall, and
   tutorial steps 8/10 send them there.
5. **Halloween wall items:** dropping the garlands, vines, 84 wall bats and wall grime is fine by me. They only live until Oct 31, and the bats
   alone are 4,620 instances. MUST 14 keeps the free-standing garden.
6. **After October:** the style of the permanent lamps (MUST 13).
7. **Server size 6** in Creator Hub. Studio reports `Players.MaxPlayers = 60` in Edit; check the live setting. If it really is 60 today, the
   3-plot servers already overfill.
8. **Plot fill order:** "lowest free BaseId first" puts solo/duo servers on the left side only (Base1, Base2). A symmetric order such as 1, 6,
   2, 5, 3, 4 would balance the hub.
