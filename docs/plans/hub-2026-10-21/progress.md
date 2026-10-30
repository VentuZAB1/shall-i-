# Redesigned hub - builder progress ledger (2026-10-21)

Inputs: spec `docs/specs/2026-10-21-redesigned-hub-design.md`, plan `docs/plans/2026-10-21-redesigned-hub.md`,
review `docs/plans/2026-10-21-redesigned-hub.review.md` (APPROVE WITH CHANGES: MUST 1-14 applied, SHOULDs unless noted).
Owner calls (decided, "do as recommended"): cream plaza; equal walks (122-130); permanent backdrop at the alley end;
Upgrade left / Sell right; Halloween wall items dropped (garlands, vines, wall bats, wall grime); permanent lamps + garden
trees after October; server size 6 set by the owner at publish; plot fill order 1, 6, 2, 5, 3, 4.

Paths used by this builder (the parent's brief overrides the plan's paths):
- ledger: this file; screenshots: `docs/plans/hub-2026-10-21/build/`.
- script backups: `ServerStorage._Backup_Hub.Before.Scripts` (brief: "back up every script you edit into
  ServerStorage._Backup_Hub.Before"); stage snapshots: `ServerStorage._Backup_HubV2.Stage*` (max 2 kept, SHOULD 4).

Resume recipe: read this file top to bottom; the last "Task N done" line is the checkpoint. Studio objects:
`ServerStorage.HubV2Kit` (Layout, Validate, BuilderTest, Templates, Swap, Rollback), `workspace.Map.HubV2` (staging).

## Rulings (deviations from the plan)

- Ruling: layout tool changed for MUST 4 - treadmill box = envelope of all 11 tiers (R +-7.35, F -9.25..+11.64, measured
  in Studio from `ServerStorage.Assets.Treadmills`), TREAD_S 18 -> 16, SIGN_S -> 27 for all 6 plots, sign footprint
  4.04 x 1.2 (the B3 clone). Why: with TREAD_S 18 a sign 1.5 clear of Tier 11 would sit past z -60 at plots 1/6 (off the
  ground); 16/27 keeps sign-treadmill 1.63 and sign-RichestBoard 3.38 with no board move. ALL PASS. Cost if wrong: the
  treadmill sits 2 studs nearer its gate (still 8.65+ clear of the gate line). Backups `tools/*.bak_planner`.
- Ruling: treadmill pivot y 0.6 -> 0.65 and sign pivot y 3.2 -> 3.18 in the generated layout. Why: the live treadmills
  sit at y 0.65 (every tier's min y is -0.65, so the base is flush with y 0); the B3 sign pivot is 3.18 above its foot.
  Cost if wrong: none (0.05 stud).

## Task log
- Ruling: MUST 13b permanent garden added to the layout tool (`GARDEN`, 14 clusters: TreeRound x6 incl. the 2 corner
  trees, Blossom x6 incl. the 2 back trees, bushes) + the checker rule 11 "density" (every plaza point off the lines /
  rings / medallion / spawn / launch + intro zones, 8+ from a plot, 4+ from the edge has PERMANENT decor within 25;
  seasonal beds don't count) -> 0 bare points; and `BACKDROP` (owner call 3: floating garden island + giant tree at
  (0, 194) beyond the back wall). Stall deck bushes may stand 0.5 from their own counter. 51 PASS / ALL PASS.
  Why: MUST 13 + owner call 3. Cost if wrong: a few decor spots to nudge (owner may hand-edit).
- Task 0 done (2026-10-21): hub_layout.py ALL PASS (51), HubLayout.lua regenerated and pushed to
  `ServerStorage.HubV2Kit.Layout` (len 19320, checksum 25215609 = local file; #PLOTS 6, P1 look +X, gate check 0.0000).
  Grep: hub literals only in Trailer (Task 8), dev tools (_GrimeRolloutEngine, AutoReconnectTests fallback, lab kits);
  Weather* use runway area centres; IntroCutscene kept clear by the layout. Nothing new for Task 8.
  BASELINE Edit: ws BaseParts 4637 / instances 10936 / Map.Hub parts 2015 / HalloweenDecor inst 6004 (= planning).
  Tags ws/all: Base 3/3, Treadmill 3/3, AdminTreadmill 3/54, Slingshot 1/1, LaunchPad 1/1, LaunchGate 1/3.
  BASELINE Play client, shot cam (0,40,-80)->(0,0,40): Studio unfocused = 15 fps cap (66.7 ms RenderStepped dt, not
  usable), so the perf metric is Stats: renderCPU 4.71 ms/frame, heartbeat 0.72 ms, 1,011,719 tris, 273 draw calls,
  mem 2366 MB, primitives 3827, client instances 69774.
  Suites: Edit AutoReconnectTests.unit 83/0, RebirthV6Tests.pure 45/0, StreakTests.pure 24/0, StarterPackTests.pure
  38/0; Play TutorialV11Tests.live 13/0, RebirthV6Tests.live 5/0, StreakTests.live 20/0, StarterPackTests.live 33/0;
  AutoReconnectTests.server (AutoReconnectTest session) 78/1 (pre-existing FAIL "teleportErrors: retry gap counts
  from the failure (no/rate)"). TestFreshSave set false after; AutoReconnectTest reset to nil.
- Task 1 done: BaseBuilder Look. Backup `_Backup_Hub.Before.Scripts.BaseBuilder`. `HubV2Kit.BuilderTest` (Edit):
  before = 31 pass / 12 fail (Floor visible, no Look) -> after = 103 pass / 0 fail. Parts R0..R5 = 295 / 358 / 669 /
  822 / 894 / 575 (= the review's fence_parts + 11 Look parts). MUST 2 applied (SignPostL/R + SignPlank + SignTrim,
  every top <= floorT + 3.4, asserted); MUST 3 applied (GateDoor may hang 3.5 past the Slot front, asserted);
  SHOULD 12 applied (SlotBed 0.2 thick, top y 0.2). Backward check: in Play the OLD hub's 3 bases were rebuilt by
  BaseManager with the new code: Base2 Look = 11 parts, Floor.Transparency 1, old Max 64x80 -> R5 64x80 (no error).
  The Edit-time Base2 plot was rebuilt once for the check and then restored to its original clone.
- Ruling: SlotBed colour = sage (150, 172, 112), "unclaimed land" between the cream plaza and the grass FloorTop
  (review MUST 12: a clearly different tone). Cost if wrong: one Color3 in BaseBuilder.C.slotBed.
- BLOCKER (screenshots): Studio's 3D viewport renders WHITE in every screen_capture (Edit with camera params, Edit
  current view, and Play client with a RenderStepped shot camera): Studio is not in front, and computer-use access to
  Studio was denied, so it can't be brought forward. Ruling: keep retrying screen_capture at each stage; in the
  meantime use an in-Studio raycast renderer (`HubV2Kit.Render`, a WorldModel copy in ServerStorage) whose
  palette/RLE output is decoded to PNG locally. Cost: renders are flat-shaded approximations (MeshParts = their
  collision box), not real Studio screenshots; the owner should take real ones.
- Task 2 done: backups `_Backup_Hub.Before.Scripts.{BaseManager, BaseHatchery}`. `ServerStorage.HubV2Tests` T2.1-T2.3b
  (Play, TestFreshSave, old hub): before = 3 pass / 11 fail -> after = 22 pass / 0 fail; 0 game warnings/errors in the
  log. BaseManager: or 60 / or 90; FILL_ORDER 1, 6, 2, 5, 3, 4 (owner call 8; TestBaseId first in Studio);
  sortedBases counts only bases in workspace; spawnAtBase RequestStreamAroundAsync before PivotTo (SHOULD 7);
  BaseDebug fill/grow/release/releaseAll/state/reassign/pets (fill lights the 6 owner cards, SHOULD 9; pets = MUST 10
  via HatcheryDebug "fakePets" -> real spawnPet wander loops). BaseHatchery: refitEggs = ONE two-pass helper shared
  by rebase + fitEggs (SHOULD 1: valid eggs never move, misfits -> findSpot, nil -> clampInside + warn); loadBase calls
  fitEggs; HatcheryDebug "reload". SHOULD 2 (twin record own GUID/kind/kg/readyAt) in T2.3; T2.3b = SHOULD 1 case.
- Ruling: T2.3b compares the untouched records field by field (x, z, kg, kind, readyAt exact) instead of JSON bytes:
  HttpService:JSONEncode key order is not stable between tables, so byte-equality failed with identical values.
- Ruling: BaseManager.sortedBases filters IsDescendantOf(workspace) (not in the plan): the 2026-10-21 launch-bug rule
  for server GetTagged lookups. Cost if wrong: none (live bases are always in workspace).
- Task 3 done: `workspace.Map.HubV2` (Model, WorldPivot (2000,0,0), attribute _Staging) with Ground (3 tiles, CREAM
  (222,205,170) Plastic + Studs = owner call 1 / MUST 12 option B), EdgeWalls Edge1..13 (96,132,170) + TopTrim Storm
  blue (69,95,132) + WallCap (invisible, collides, y 4..12, MUST 9), BoundsV2 Hub_E1..13 (Persistent), _StageRef
  proxies, Decor.Plaza (medallion clone moved (0,0,53.5), SHOULD 16; its cream discs + Burlap rings + Red flip/flop
  border = option B trims), Spawn_V2 (disabled). `HubV2Kit.Validate` written (checks 1-17 + 18 Halloween + 19
  WallCaps + 20 bounds + 21 MUST 13 density; MUST 5 exceptions). Empty HubV2: 97 failures in 4,10-16,19-21, no Lua
  error. After the build: 24 failures, only checks 4 / 12 / 13 / 14 / 15 (plots, treadmills, signs, stalls, boards
  not built) + 21 (no decor yet) - as planned. Snapshot `_Backup_HubV2.Stage3_Ground`.
  Shots (HubV2Kit.Render, decoded with tools/decode_render.py): build/stage3_topdown_cream.png (built) and
  build/stage3_topdown_green_option.png (the green alternative, render-only recolour) for the owner.
- Ruling: `HubV2Kit.Render` = raycast renderer (WorldModel copy in ServerStorage, destroyed after each use); its
  output goes through >99k-char tool results, which the harness saves to files; tools/decode_latest.py decodes them.
- Task 4 done: HubV2.Bases.Base1..6 (Model; BaseId, MaxWidth 60, MaxLength 90, Owner 0, _SwapTags "Base"; new Slot at
  the layout; OwnerSign clone with the card off; Plot by the NEW BaseBuilder at R0 + accent(N)), Treadmills
  Treadmill_B1..6 (Tier 1 clone, tags -> _SwapTags Treadmill / AdminTreadmill on Conveyor, BaseId N), UpgradeSigns
  UpgradeSign_B1..6 (B3 clone, ClickDetector removed, Atomic). Validator: before = 4/12/13 fail; after = only 14, 15
  (stalls, boards) + 21 (decor) fail. Check 12 includes MUST 4: the envelope of all 11 Assets.Treadmills templates at
  every pivot clears plots, signs, everything visible and the other plots' lines. Growth preview R0..R5 x 6 plots:
  0 fails (all Plot parts inside the Slot +-0.5, GateDoor <= 3.5 past the front); min plot gap R0..R5 = 32 / 28 /
  24 / 20 / 16 / 12. Validator at R5: only 14/15/21. Shot build/stage4_r5_topdown.png; rebuilt at R0; snapshot
  `_Backup_HubV2.Stage4_Plots` (Stage3 + Stage4 kept).
- Task 5 done: Stalls (clones, tags stripped, _OrigPos/_OrigRadius removed), MarketCorners LeftMarket/RightMarket
  (24 x 24 Deck + 24.8 x 24.8 DeckTrim, live colours/studs, trim -0.05 below like the live deck), 4 Leaderboards
  (clones, legacy GlobalLeaderboard/TimeLeaderboard tags stripped, Atomic = SHOULD 7, live pivot y 10.25), FreeGift
  (Chest + FreeGiftZone + PadRing moved together by the plan's T; chest at (0,1.5,56) facing -Z; zone on the Fill).
  Validator: before = 14/15 fail; after = 0 failures except check 21 (density: no permanent decor yet, Task 6).
  Stall bases checked on their decks (0 low corners off the deck). Shots: build/stage5_topdown.png,
  build/stage5_{UpgradeStall,SellStall,FreeGift,RichestBoard,SpeedBoard,HeaviestBoard,TimeBoard}.png and
  build/stage5_closeups_sheet.png. Snapshot `Stage5_Plaza` (kept: Stage4, Stage5).
- Ruling: each stall is placed so that its walk-in ZONE lands exactly on the layout ring (0.000 off), keeping the
  stall's own counter-to-ring arrangement. The planner's STALL_RING_F 4.53 is right for the Sell stall but the
  Upgrade stall's ring sits 5.64 in front of its plinth, so its model pivot is 1.11 behind the layout pivot.
  Why: the ring/zone is what players use and what the line checks measure. Cost if wrong: none (deck still covers it).
- Ruling: close-up shots taken at 5 studs eye height (avatar eye level, as in the Halloween reviews), not the plan's
  1.7 (that is knee height in studs). Renders: MeshParts/boards are their collision boxes, GUIs are not drawn.
- Task 6 done: Templates (0 scripts, 0 tags): TreeRound, Blossom, Rock, Bush, BushSmall, GrassA/B/C, Sprout, Flowers
  (from HalloweenGardenBackup + the hub's yellow flowers; pivot = ground point, trunk/rock colliders), Bench = Toolbox
  23153972 "Park Bench" (Roblox) vetted in _Quarantine (0 scripts, 14 BaseParts, 3 Seats -> Parts, 1 tag + attrs
  stripped, one BenchCollider), Lamp (MUST 13a). Candidate 9717664338 REJECTED (54 BaseParts > 30); _Quarantine empty.
  Permanent decor (Hub.Decor): Trees (4) + Benches (4) per DECOR, Garden (14 clusters, MUST 13b), GateBeds (6: soil +
  0.6 stone border (collides) + plants), AlleyBed (8 x 80, low plants + rocks only), Lamps (8 permanent lamps), Backdrop
  (owner call 3: floating studded garden island at (0,194) with a 1.7x TreeRound + 2 Blossoms + rocks/bushes; top
  y ~29.5, under the October pumpkin's chin). Seasonal HalloweenV2: GiantPumpkin (Pivot (0,64,230), Persistent),
  StreetLamps 1..8 = only Pumpkin + Web + WebSilk over the permanent lamps (pumpkins turned 90-degree steps to face
  (0,20), dot 1.00), PumpkinEggs (6 clusters on gate beds 1/3/4/6 + alley; pieces hanging off a bed settled to what is
  under them), Garden (MUST 14: 12 spots = 10 live trees (TPTree 4, DeadTree 4, HauntedTree 2) + 22 bushes/graves
  (3 Halloween beds with Grave A/B/C) + 57 dead grass; 18 tree/bush spiders moved with their trees + new anchors;
  Spider5..8 on lamps 5-8), SpiderAnchors. Validator 0 failures (incl. 18 Halloween no-collide, 21 density);
  float check 247 props: 0 floating/sunk after sinking the Bush template 0.7 (its tilted lumps' box bottom was low).
  Counts: HubV2 BaseParts 2803 / instances 3923; HalloweenV2 instances 802 (old HalloweenDecor 6004).
  Shots: build/stage6_topdown.png, stage6_plot{1..6}_eye.png, stage6_plaza_to_plot{1..6}.png, stage6_alley.png,
  sheets stage6_plot_eyes_sheet.png / stage6_plaza_to_plots_sheet.png. Snapshot Stage6_Decor (kept: 5, 6).
  NOT re-placed (left in the backup at the swap): Garlands, wall Webs, Vines, WallBats, Grime (owner call 5) + from
  the HQ garden 1 TPTree, 1 DeadTree, 1 HauntedTree, 1 Bush_Autumn, 7 DeadGrass_A and 2 spiders on those trees (no
  free spot off the walking lines; the alley stays low).
- Ruling (lamps, owner call 6): the "old non-Halloween style" in _Backup_StreetLamps.Old.PathLamps = the 9-stud neon
  posts the owner called "small ugly ones" on 2026-10-13, so the permanent lamp = the hub's current lamp without its
  Halloween parts (Post + Cage + GroundLight) + a warm neon bulb (review MUST 13a). Its lights shine at the night
  values all day (bulb 2.2/14, ground light 2/18) because HalloweenClient only boosts lights in HalloweenDecor (no
  script change). Cost if wrong: swap the 8 Hub.Decor.Lamps models; the old posts are in the backup.
- Ruling: layout nudges after the in-Studio checks (tool ALL PASS again, Layout re-synced, checksum = file):
  lamp 2 (27.5,-12) -> (29,-6) (its cage hung 0.1 into the intro zone), corner trees x +-90 -> +-88 and rocks
  (+-83,-56.5) -> (+-82,-57) (canopies were inside the Tier-11 treadmill envelope of plots 1/6), BACKDROP tree scale
  2.5 -> 1.7 (the October pumpkin head's front reaches z ~175 above y ~36).
- Ruling: Render now keeps hull-collision MeshParts as meshes (trees/bushes look right); Box-fidelity meshes (all the
  Halloween ones, lamp posts, the giant pumpkin) still draw as grey boxes.
- Task 8 done: Trailer backed up (`_Backup_Hub.Before.Scripts.Trailer`, Assets not duplicated), local copy kept as
  `trailer/studio/Trailer.lua.bak_2026-10-21_prehub` (Studio == local before: 66595 chars, checksum 279415498).
  Failing check before: V(0, 0, -33), "Treadmill_B2", V(0, lerp(18, 58, u), 169), plot:GetBoundingBox() all present.
  Edits: S6 hatchPos = own Plot.Floor top centre (MUST 1) + hatchFront = own Slot LookVector (fallback (0,0,20) - c);
  S8 = own Treadmill_B<BaseId> (else B1, fallback = layout B1 pivot) filmed from its plaza side (SHOULD 8 treadSide);
  S10 = the plan's exact PUMPKIN_AT-relative code, PUMPKIN_AT read once per play (else (0,64,230)); header line.
  After: compiles, all 4 old strings gone, PUMPKIN_AT defined once; local file rewritten from Studio and equal
  (68254 chars, checksum 107994584; SHA-256 of the local file e5abbd46...). Runtime check = T10.10.
- Ruling: "SHA-256 == local" verified as length + polynomial checksum (Luau has no SHA-256); same guarantee for a copy.
- SHOULD 6 pre-swap perf (Play, TestFreshSave true -> false after; old hub live + HubV2 staging with its 6 plots
  rebuilt at R4 in the server only; same shot cam moved +2000 X): renderCPU 4.89 ms (base 4.71), heartbeat 0.14 ms
  (0.72), mem 2515 MB (2366), primitives 6878 (3827), client instances 71902 (69774). Tris 1,011,719 and 273 draw
  calls are EXACTLY the baseline numbers, so with Studio unfocused the scene is not rendered and SceneTriangleCount /
  SceneDrawcallCount are frozen: they are NOT a valid metric here (same for MUST 10 in Task 11). Valid: memory,
  primitives, instances, heartbeat; render cost needs a focused Studio or a live check (owner to-do).
- Task 7 done: Haiku visual reviewer -> build/STAGE_REVIEW.md "PASS WITH FIXES" (U order, walks, stalls, chest,
  alley-low OK). Each item checked in Studio before acting:
  - Ruling: MUST "element-colour trim per plot" NOT applied - spec section 1 row "Plot look": "Basic, all 6 the
    same (owner): no element themes", element plots are listed as out of scope (skins later). A_horseshoe's colours
    were the sketch's area labels. Cost if wrong: one colour per plot in Look.Trim* (5 parts each), 10 min.
  - Ruling: MUST "giant pumpkin ~110-135 studs, scale to 30" NOT applied - it is the owner's live October head
    cloned unchanged (live: 107.8 x 85.6 x 109.2, bottom y 27.6, pivot (0,64,169); staged: same size, same bottom
    y 27.6, pivot (0,64,230) per plan). The planned_layout 30-stud circle is a symbol, and the grey "box" is the
    renderer drawing its Box-fidelity MeshParts as boxes. Cost if wrong: one ScaleTo on the model.
  - Ruling: MUST "pumpkin base hovering" NOT applied - it floats by design in the live hub too (same bottom y 27.6
    over the ground, invisible FireBed); its chin clears the Backdrop island (top y 29.5 at z <= 214, head
    bottom there is higher; checked at the 1.7x ruling).
  - NICE stalls ~100 studs from spawn: skipped - stall spots are the reviewed layout (corner decks, Upgrade left /
    Sell right, owner call 4) and each has its sign + neon ring.
  - NICE spread Speed/Heaviest boards: tried in the layout tool - x +-21/24 cross the walk lines to plots 3/4, z 66-70
    hits gate beds 3/4 (FAIL); current (+-18, 63) is the only passing spot. Chest keeps 6.6 studs each side.
  - NICE board height: skipped - the 4 boards are the live models cloned unchanged (spec: re-place, not redesign).
  - NICE "yellow/black hazard band": it is plot fence caps (Fence/Cap x39 yellow on dark posts = BaseBuilder's
    existing per-base fence accent), not tape; unchanged.
  - NICE alley-bed gap: skipped - the alley is open +-30 studs above y 2.9 for its whole length (raycast grid
    z 80..170), the bed is the plan's 0.8-tall median "pumpkin lane" (PUMPKIN_ALLEY sits on it).
  Validator unchanged (0 failures). No geometry changed, so no Stage7 snapshot (Stage5/Stage6 kept).
- Task 9 done: SWAPPED 2026-10-21 14:58 UTC (Map.Hub attrs HubVersion V2 / SwappedAt). Pre-swap gates (Edit, no
  Play): Validate stage 0 failures, BuilderTest 103/0, Trailer len 68254 checksum 107994584 = local, Layout 20993 /
  675429612 = local; old Map.Hub children diff = only Floor/FloorSides/Walls/Spawn (+ Slingshot/LaunchPlatform,
  carried) not in V2, as planned. `HubV2Kit.Swap` (one step): a-i all ok (13 old tags -> _RemovedTags, 18 _SwapTags
  added, Slingshot + LaunchPlatform CFrames exact + tags kept, Runway_L_1/R_1 end at z -60), Validate(Map.Hub, live)
  = 0 failures, T9.4 census Base 6 / Treadmill 6 / AdminTreadmill 6 / Slingshot 1 / LaunchPad 1 / LaunchGate 1 in
  workspace, 0 tags under _Backup_Hub.* / _Backup_HubV2 / HubV2Kit.
  REHEARSAL (MUST 11): `HubV2Kit.Rollback` (one step) -> ok; census Base 3 / Treadmill 3 / AdminTreadmill 3 / 1 / 1 / 1,
  old Spawn live, runway bounds back to 1217 long, ws BaseParts 4637 / instances 10936 / Map.Hub parts 2015 /
  HalloweenDecor 6004 = EXACTLY the Task 0 baseline. Swap again (from _Backup_Hub.After) -> all ok, Validate live 0,
  census 6/6/6/1/1/1. Live: ws BaseParts 4884 / instances 6650; one SpawnLocation (Map.Hub.Spawn, enabled).
  Fix: Swap now destroys the emptied bounds folder in both paths (After.Bounds was left empty); re-run = "already
  swapped: only validating" ok. _Backup_Hub.Before = Scripts (4, BaseManager/BaseHatchery disabled), Hub_Old,
  HalloweenDecor, Bounds (7). Shot: build/swap_live_topdown.png (pumpkin tinted orange in the render).
- Task 10 session 1 (TestFreshSave true -> Play -> false after; player Santrinio got BaseId 1 = FILL_ORDER first):
  - Fix in HubV2Tests: the T10 sections called check(ok, "what") but the runner took check("what", ok), so a T10
    check could never fail. The runner now accepts both orders (string first = T2 style). All T10 results below are
    from the fixed runner.
  - T10.12 Play suites FIRST (before my tests touch the save): TutorialV11Tests.live 13/0, RebirthV6Tests.live 5/0,
    StreakTests.live 20/0, StarterPackTests.live 33/0 (= baseline).
  - T10.1 5/5, T10.2 5/5 (reassign 0, respawn at (-2.7, 3.2, 22.8), BaseData + EggInventory identical 10 s, base
    given back), T10.3 12/12 (R0..R5 sizes = Layout.SIZES, colliders in Slot +-0.5, OwnerSign <= 1 of the back fence
    centre, no Look part over another base) + pairwise floor gaps at R5: B1-B2 12.0, B2-B3 20.9, B3-B4 20.0, B4-B5
    20.9, B5-B6 12.0 (min 12.0 >= 10). Shots build/live_r5_topdown.png, live_r5_pair12_a/b.png.
  - T10.4 2/2 (R20 floor 60 x 90, 23 CelestialDragon 1,000,000 KG given) + client equipBest (23 pets) + T10.4b 3/3
    (23 pets inside the fence for 20 s at 2 samples/s; MUST 8 unequip-all, then 12 x 100,000-KG StormEggs fit,
    stopped by "Too close to another egg"; expected >= 12).
  - T10.6 (client): 13 edges x {1.5 inside: not moved 2 s; jump at the wall (v 18 out + 52 up): peak y 9.7, lands
    1.3-1.9 inside, never on top (WallCap); 2 studs outside the Hub_E column at y 10: MapGuard puts it back in
    0.12-0.43 s} = 13/13 PASS; (+-70, 3, -55) not moved 2 s = 2/2. (First run: E3 "moved 200" = MapGuard's late
    correction from the previous edge's outside step; re-run with 1 s settle between edges: 13/13, E3 standing
    still checked alone for 2.5 s: 0.0 moved.)
  - T10.11: Upgrade / Sell / Free Gift windows open inside each ring and close 8 studs out (3/3); 4 boards drew
    Row01; FREE! SignAnchor 0.05 from the chest (XZ); night via the Settings attribute (TIME switch data path):
    Lighting NightMode true, 16/16 permanent lamp lights at NightBrightness, HalloweenDecor lights 21/21 on;
    Settings restored.
  - T10.10 trailer (owner account, TrailerDebugT freezes): S6 12.6 / 13.8 look passes 0.02 from own floor centre
    + 3, camera on the plaza side (dot 0.97) and inside the own fence, BaseConfig.inside(floor, hatchPos, 0) true,
    no hub part in the way; S8 19.5 looks 0.20 from own Treadmill_B1 (+4), camera (-101.2, 9.65, -31) over the
    plaza; S10 25.5 / 27.0 frames on the glide, 61 samples of the glide path: 0 parts within 1.5 studs of the lens,
    nothing between lens and pumpkin; S12 31.0 slingshot (927,553) + pumpkin (643,280) on screen, unblocked.
    GiantPumpkin.Pivot part found at (0,64,230) = PUMPKIN_AT. Trailer ends cleanly (CameraType Custom).
  - T10.7 walker (client, input sunk, WalkSpeed 52.8): 110 ordered pairs with PathfindingService + 24 straight
    checker lines (ENTRY / GateL / GateR -> 6 spawn spots from where the line leaves the pad (+2), spot -> own
    treadmill exit): straight 24/24; path 97/110 first pass. The 13 misses re-run twice each with the Free Gift
    point moved from the zone centre (= inside the chest, a test error) to the ring front (0, 50): 11/13 pass 2/2.
    The last 2 are pathfinding artefacts, not blocked lines: FreeGift > S3 plans THROUGH the Speed board's 0.8-thick
    screen (navmesh voxels miss it; the walker stops in the board's front pocket, free to walk out), FreeGift > S4
    plans a jump over the 3-tall chest. Both walked fine around (board: via (-30, 56); chest: via (12, 52)).
    Notes: no leg mounted the own treadmill or loaded the sling.
  - Task 11 Step 1 / MUST 10 measured here (same session, fill + grow(i, 4) x6 + BaseDebug pets 23 on the 5 fake
    plots + the player's own 11 equipped = 126 pet rigs):
    - Static world at 6 x R4: Map 8,253 + HalloweenDecor 224 = 8,477 BaseParts (budget <= 11,000: PASS); Map 9,854 +
      HalloweenDecor 803 instances ~ 10,660 (budget <= 10,936 + 3,000: PASS). Whole server workspace incl. 2,190
      runway ZoneEggs, base eggs/pets 708 and the avatar: 11,397 BaseParts / 14,350 instances.
    - Client (Task 0 camera): renderCPU 3.99 ms (base 4.71), heartbeat 0.90 ms (0.72), primitives 9,747 (3,827),
      client instances 77,606 (69,774). Plaza centre (0,25,20): 4.22 ms / 0.88 ms, 126 of 126 pets animated
      (<= 220); plot 1 spawn: 4.12 ms / 0.73 ms, 71 animated. Frame dt stays 66.7 ms (unfocused Studio = 15 fps
      cap) and tris/draw calls are frozen, so these render numbers are indicative only.
    - Memory: same-session delta from "all plots R0, no pets" (2,720 MB) to "6 x R4 + 126 pets" (2,744 MB) = +25 MB
      (budget +60: PASS). The absolute Studio number (2,7xx vs Task 0's 2,366) is the whole Studio process after many
      Play sessions + the backups now in ServerStorage (Hub_Old, old HalloweenDecor 6,004 inst, 2 stage snapshots);
      not comparable - owner to read the live Developer Console instead.
    - Ruling: no picket cap (plan Step 2) - every measurable budget passes; the cap would only cut ~15% fence parts.
- Renderer: Box-fidelity MeshParts now draw as a 0.9 pole (tall thin: lamp posts) or a ball of their smallest size
  (Halloween trees, the pumpkin head) instead of grey slabs; Render.clear() after every use (0 _RenderWorld left).
- T10.12 Edit suites: AutoReconnectTests.unit 83/0, RebirthV6Tests.pure 45/0, StreakTests.pure 24/0,
  StarterPackTests.pure 38/0. AutoReconnectTests.server (own session, workspace AutoReconnectTest true -> nil after)
  78/1, the same pre-existing FAIL "teleportErrors: retry gap counts from the failure (no/rate)" = baseline.
- T10.9 intro (session TestBaseId 1, TestIntro + TestTutorial true): IntroDebugT freezes 0.5 / 2.0 / 2.8 / 3.5 /
  T.gate 18.81 / T.outro - 0.3 = 26.26: lens -> puppet clear of every plot, board, stall, deck, treadmill and sign
  (6/6); shot 1: the slingshot covers 57% of the screen height (8/8 corners in front); FINISH takeover: root at
  (-6, 2.94, -21.8), y steady 2 s (drift 0.00), standing on Plastic (no fall).
- T10.5 + T10.8, one session per TestBaseId 1..6 (TestTutorial true, TestFreshSave true -> false after each):
  - Streaming from the spawn spot (0.0 from the layout spawnSpot on 2-6; plot 1 = after the intro): 6 belts + 6
    floors + 4 board SurfaceGuis in 0.4 s, 6/6 sessions.
  - Tutorial targets (client TutorialGuide.Target, 0.00 off in every case): step 5 = own Plot.Floor + (0,2,0),
    step 6 in the base, step 8 "Your egg is growing" on the egg, step 8 FREE upgrade = UpgradeZone + (0,2,0) and
    "Press FREE" inside the stall (plots 2-6; FreeSling set true before the hatch because TestFreshSave saves start
    false - on plot 1 the flow went straight to step 9 as designed for such saves), free Sling buy (Lv1), step 9 =
    own Treadmill_B<id>.Belt + (0,3,0), "Keep RUNNING!", TutorialExtra 1 -> 2 after 5 s, step 10 =
    UpgradeZone + (0,2,0) (Money 1e12). 6/6 plots.
  - T10.5 server section 10/10 on every plot (MountTreadmill true, TreadmillRun = Treadmill_B<id>, Speed rises,
    tier 2 at the same pivot (0.00) tagged with BaseId, re-mounted, sign NowName x2). Jump-off (the TreadmillClient
    exit replayed from the client: Exit remote + step 7.5 behind the belt): lands 0.00 from Layout treadExit, y 3.4,
    not moved by MapGuard for 2 s, 6/6. (A real Space press cannot be sent without driving Studio input.)
  - Console (last session): 0 server warnings/errors, client only the TopbarPlus "new version" note.
- Task 10 done: T10.1 5/5, T10.2 5/5, T10.3 12/12 + gaps, T10.4 5/5, T10.5 6 x 10/10 + 6 jump-offs + 6 streaming,
  T10.6 15/15, T10.7 134 legs (24/24 straight, 108/110 path + 2 pathfinding artefacts walked around), T10.8 6 x 7,
  T10.9 8/8, T10.10 6 frames + glide, T10.11 3 windows + boards + sign + night, T10.12 = baseline (Play 13/5/20/33
  pass, Edit 83/45/24/38, AutoReconnect server 78/1 pre-existing). TestFreshSave false after every session.
- Ruling: studiotest_ save keys NOT deleted (plan Step final) - deleting DataStore keys is permanent data removal,
  left to the owner; the keys are only read by Studio fresh-save sessions, so they are harmless. Recipe in the
  owner checklist. Cost if wrong: a few unused keys in PlayerData_v3.
- Task 11: final shots in a Play session (fill + mixed rebirths B1..B6 = own/R1/R3/R2/R0/R4, 5 x (6 + 3R) fake pets +
  the player's own, rendered on the CLIENT so LocalPets show; temp copy of Render in ReplicatedStorage, deleted
  after): build/final_topdown_day.png, final_topdown_night.png, final_full_server.png, final_plot{1..6}_eye.png
  (sheet final_plot_eyes_sheet.png), final_plaza_to_plot{1..6}.png (sheet final_plaza_to_plots_sheet.png),
  final_plaza_day.png, final_plaza_night.png, final_from_slingshot.png (sheet final_plaza_sheet.png).
  Earlier live shots: swap_live_topdown.png, live_r5_topdown.png, live_r5_pair12_a/b.png.
- Owner checklist written: docs/HUB_V2_OWNER_CHECKLIST.md. Memory: slingshot-redesigned-hub.md rewritten with the
  build outcome + MEMORY.md index line updated.
  Ruling: the plan named a new note `roblox-redesigned-hub.md`; the topic already had `slingshot-redesigned-hub.md`
  (indexed), so that note was updated instead of adding a duplicate.
- End state: Studio in Edit; TestFreshSave false, TestStarterPack true, TestTutorial false, TestIntro false,
  TestBaseId / AutoReconnectTest unset; Swap re-run = validate-only OK (Validate live 0, census 6/6/6/1/1/1, 0 tags
  in backups/kit); no Map.HubV2, _RenderWorld, _SwapHold or temp modules left; _Backup_HubV2 keeps Stage5_Plaza +
  Stage6_Decor (delete after the owner's live check, SHOULD 4).
- Task 11 final visual review (fresh Haiku reviewer): build/FINAL_REVIEW.md "PASS WITH FIXES" - U order, open walks,
  stalls / chest / boards visible, plaza lit at night, density OK.
  - Its one MUST ("dark grey curved band over the top of final_from_slingshot.png") checked in Studio: a box-ray
    test from that camera hits `Map.Hub.Slingshot.LivePouch` at 0 studs - the camera sat inside the slingshot
    pouch's box. A camera-placement artefact of the render, not a hub part over the exit. No change.
  - NICE skipped, with reasons: (a) plot 3/4 gates + alley mouth outside the lamp pools at night - night is an opt-in
    setting (Day default) and the 8 lamp spots come from the checked layout (LAMP_SPOTS); more lamps = a layout
    change for the owner to ask for; (b) plots read as trees / fence edges from the plaza - basic identical plots
    are the owner's decision; (c) gate posts / boards near spawn spots 3 and 4 - BaseBuilder's gate posts are
    unchanged and the boards cannot move (Task 7 layout tries all fail); (d) stalls small at the far corners -
    stall decks are the reviewed layout (owner call 4).
- Task 11 done. Skipped SHOULDs (reasons): SHOULD 5 (owner away; no Save/version possible from here - Studio's
  PlaceVersion reads 0); SHOULD 6 "one Collider per fence line" (every budget passes; would change BaseBuilder's
  collider layout that T10.3 checks); SHOULD 11 (the garland conflicts with owner call 5; stall-roof / board-frame
  corner webs not added because their placement can't be checked visually here - the 8 lamp cages keep their webs);
  SHOULD 14 (owner away: no hand edits to freeze).
