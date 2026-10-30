# HATCH NIGHT Rebirth + Index + Settings: build ledger (2026-10-21)

Plan: `docs/plans/2026-10-21-hatch-night-rebirth-index-settings.md`. Review: `....review.md` (APPROVE WITH CHANGES: MUST 1-5 +
SHOULD 1-16). Split into 3 runs (review SHOULD 15): **run A = shared groundwork + SETTINGS** (this section), run B = Index,
run C = Rebirth + wrap-up.
Owner's calls (decided, "do as recommended"): windows as big as today on PC; Settings band steel-lilac + the top-bar gear;
MUSIC ON lime; keep the old Settings page as a disabled fallback 7 days live; same layout + content, only the look changes.
Studio: 0663e976-4faf-4dca-bf0c-91120a8d1353, viewport 1519x753.

## Run A (groundwork + Settings)

### Tasks

- [x] **Task 0** (pre-flight + BEFORE evidence). Studio in Edit; the fix-round ledger ends "End state: Edit" and every
  file it names is in place (BrickUI 606 lines with the viewport fix, Hatch 960, MenuController 501). TestFreshSave read
  false at the start (fix-round end state) -> set true, read back true (review SHOULD 14).
  - Anchor drift vs the plan: none that matters. `PAGES.Settings` (MenuController line 122) has no `icon` yet;
    `local body = panel:WaitForChild("Body")` is line 325, the Settings block runs to the end (line 501); `H.pageCap` is
    the Shop-only body at Hatch 850-853; `H.arrow` (937-945) has no `k`; `H.text` has no `opts.fill`.
  - R measured (Play, Check-UI windows, 0.9 s after open, MainMenu 1519 x 695): Rebirth 548.6 x 438.9 -> **0.6315**,
    Index 859.8 x 491.3 -> **0.7069**, Settings 570.5 x 438.9 -> **0.6315** (= the plan's values). Shop 891 x 565.9, Gift
    872.3 x 554.0 (HATCH, unchanged).
  - `H.bindCanvasScale` hidden-page guard present (Hatch line 642).
  - BEFORE evidence (fresh session): `tests-2026-10-21/hatch_gift_before_ris.txt` (181-group list, FNV 4b73c224),
    `hatch_shop_before_ris.txt` (ALL d31e8fb0, 146 groups, stable after 2 dumps), `hatch_chrome_before_v3.txt` (Menu right
    173.88, SpeedUI.Holder (14.28, 537.93 263.89 x 145.46); 51 lines per window; Settings line 44 = `Window.Face.Icon`,
    Image empty). Shots `hatch-night-build/ris/settings/settings_before.jpg`, `ris/rebirth_before.jpg`, `ris/index_before.jpg`.
  - Ruling: the gift BEFORE list differs from the popup/Shop AFTER file (ae122c90) in the 15 PLAYTIME PlaytimeView groups
    only (PlayBar, SkipAll, Slot1-12, Warning); DAILY and all chrome groups are identical - why: nothing was changed
    between the two runs, so it is session data in the playtime slots; the user asked to re-capture the baseline first,
    this run compares against its own BEFORE - cost if wrong: none for this run (if PLAYTIME also moves between two of
    MY sessions, the AFTER check says so and is judged on DAILY + chrome + a same-session re-run).
  - Ruling: test sources are mirrored as ModuleScripts in `ServerStorage.HatchRISTests` (a folder with a `Note`
    attribute; never required by the game). Each Play session the Server copies the folder to ReplicatedStorage (runtime
    only) and the client runner requires a clone - why: the same file is not re-pasted into every session, and later runs
    can reuse it - cost if wrong: the folder ships in the place file like `ServerStorage.StreakTests` does (inert). Every
    mirror is checked against the local file (same CR-stripped FNV).
  - The 3D world renders white in captures (Studio unfocused); the GUI is fine.
- [x] **Task 1** backups: `ServerStorage._Backup_HatchNight.Before` + `MenuController_preRIS`, `BrickUI_preRIS` (with
  `Hatch`), `IndexClient_preRIS`, `RebirthClient_preRIS`; LocalScripts Enabled false; sources byte-identical to the
  live ones (5/5: MenuController, BrickUI, Hatch, IndexClient, RebirthClient); 0 tags in the folder; folder attributes
  `WasEnabled_preRIS`, `HowToRestore_preRIS`.
  - Ruling: `IndexClientLegacy` / `RebirthClientLegacy` are NOT created in this run - why: the user's rule for run A
    ("don't touch RebirthClient, the Index scripts"); a byte copy made now could go stale before runs B / C rewrite those
    scripts; each later run makes its own copy from the live script at its start (and checks it equals its `_preRIS`
    backup) - cost if wrong: none (the copies only matter once the new scripts exist).
- [x] **Task 2** tests first (RED). Local files in `docs/plans/tests-2026-10-21/`, each mirrored to
  `ServerStorage.HatchRISTests.<name>` (same CR-stripped FNV checked for every file):
  - `hatch_pure.lua` + block RIS (R1-R9; R6 also checks MUST 1 HatchHug + SHOULD 3 `arrow = false`; R9 = MUST 1 `opts.fill`).
    RED run (Edit): **pass 108 fail 22**; the 22 fails are all R1-R7 / R9 lines; the 93 older checks pass (= the fix
    round's 93/93; 108 = 93 + 15 new checks that already hold: R8 canvas guard, R4 1050 / 844 rows, R5 default arrow,
    R2 Gift / override, R3 Shop / Gift).
  - `hatch_containment.lua` **v3**: `_G.HatchRISCfg(name, opts)` (all 3 pages; probes = every shown GuiButton's centre),
    checks `nowNext` + `barFill`, `cfg.noOnTop` (review SHOULD 9 forced big-PC runs). textFill stays a FAIL off Gift.
  - `settings_client.lua` (open, toggles, volume, song, reopen, respawn (SHOULD 7), save, legacy) + `settings_save_server.lua`
    (Server: SavePlayerNow + the stored save read back uncached, key by key).
  - `hatch_shop_snapshot.lua` (new; SHOULD 11: dumps until 2 dumps 1 s apart are identical), `hatch_ris_perf.lua` (idle,
    canvasguard, cost, counts, leaks; Index / Rebirth sections say "skipped (Check-UI)" until runs B / C), `hatch_assets.lua`
    (+ the 7.4 ids).
  - Ruling: `index_client.lua`, `rebirth_page_client.lua` and the `streak_client.lua` section-5 change are NOT written in
    run A - why: they test scripts this run must not touch; runs B / C write them RED first, as TDD wants - cost if wrong: none.
  - Ruling: SettingsClient exposes the song names as a Studio-only page attribute `TestTracks` and the test reads it - why:
    requiring `SFX` from the test VM could run its side effects a second time - cost if wrong: none (Studio only).
- [x] **Task 3** BrickUI.Hatch additions (7.1) with the Task 0 R values: `H.text opts.fill` (MUST 1, sets HatchFill before the
  first fit), `H.PAGE_CAP_R` + table-driven `H.pageCap`, `H.arrow(..., k)`, `H.BAND.Rebirth / Index / Settings` +
  `H.PAGE_BAND`, `H.nowNext` (HatchHug on Now / Next = MUST 1; `o.arrow = false` = SHOULD 3), `H.progressBar` (trough attribute
  `HatchBar`, Text with fill 0.83). GREEN: `hatch_pure` **pass 147 fail 0** (Edit).
  - Diff vs `BrickUI_preRIS.Hatch` (960 -> 1072 lines): old lines changed = `H.pageCap`'s `if page == "Shop"` line (-> 2
    lines over `H.PAGE_CAP_R`), `H.arrow`'s signature, its `H.frame` line (18 * k, 22 * k) and its 4 segment lines (* k);
    inserted: 1 line in `H.text` (`if opts.fill ...`), the `H.PAGE_CAP_R` line + 2 comment lines, `k = k or 1` + 1 comment
    line; the rest is the new section at the end. Everything else byte-identical.
  - Ruling: the arrow's `H.frame` line changes too (not only the signature + 4 segments the diff rule lists) - why: the box
    must scale with k (R5 13.5 x 16.5) - cost if wrong: none (k = 1 gives 18 x 22 exactly; R5 compares every segment of
    the default arrow with the pre-RIS arrow: identical).
  - Ruling: `H.nowNext`'s frame is 4 px bigger than (x, y, w, size + 2) on every side, the parts sit 4 px in - why: Now is
    left-aligned at the row's x, so its 2.5 px text stroke would poke out of a frame that starts there (containment
    textWidth) - cost if wrong: none (R6 checks the glyphs start exactly at the row's x).
  - Ruling: R5 compared `7 x 0.75 = 5.25` exactly and failed: UDim offsets are integers (5.25 is stored as 5), the check now
    compares against `UDim2.fromOffset(0, 5.25)` - why: a test bug, not a helper bug - cost if wrong: none.
  - PAUSED here 2026-10-21 by the coordinator (the owner is hand-editing the map): Studio left in Edit, no Play running,
    TestFreshSave false; nothing calls the new helpers yet (no PAGE_SKIN change), so the place is safe to save as is.

### Review items (run A view)

Applied in run A (shared groundwork + Settings):
- MUST 1 (83 % rule): `H.text opts.fill` (sets HatchFill before the first fit) + `H.nowNext` HatchHug on Now / Next +
  `H.progressBar` Text fill 0.83 (hatch_pure R6 / R7 / R9); SettingsClient builds every label through `txt()` (fill 0.83)
  and sets HatchFill 0.83 on the 3 Toggle labels.
- MUST 4 (test switches): SettingsPage honours HatchTestHover (`H.setTestHover`); it has no breathing button (plan D14), so
  HatchTestPulse has nothing to drive there (the containment pulse pass = a second layout pass).
- SHOULD 3 (`nowNext` `o.arrow = false`): in the helper + R6. SHOULD 7 (Settings respawn check): settings_client `respawn`.
- SHOULD 9 (big-PC scale): SET1 at a forced HatchTestScale 1.37 (`noOnTop`). SHOULD 10 (Gift + Shop snapshots and G1 / S1
  right after Task 3). SHOULD 11 (shop snapshot waits for the prices). SHOULD 13 (the identical-source count; see Task 1).
  SHOULD 14 (TestFreshSave false + the legacy switches cleared at the end of the run). SHOULD 15 (this split).

Deferred to run B (Index):
- MUST 1 page part: Index labels via a fill-0.83 `txt()`; HatchFill 0.83 on the CLAIM / CLAIM ALL gloss labels.
- MUST 2: the selection Ring on all 5 cards in `Card.Face` at ZIndex 1 (after Glow), only its Visible toggles; Badges empty.
- MUST 4 page part: IndexPage HatchTestHover + `btn.pulse(t, page HatchTestPulse)` in its RenderStepped.
- SHOULD 5 (inspect stat L box (8, 4, 92, 16)), SHOULD 6 (claim refusal `{tostring(msg or ""):upper(), "TRY AGAIN"}` + a
  `busy` flag), SHOULD 9 (IDX1 forced 1.45), SHOULD 12 (claimall asserts Potion_Money / Potion_Hatch +2), SHOULD 16 (known
  cards: 15 % `area.colors[1]` tint). `IndexClientLegacy` byte copy + `index_client.lua` (RED first).

Deferred to run C (Rebirth + wrap-up):
- MUST 1 page part (REBIRTH gloss label HatchFill 0.83; Head / reward Line use `H.nowNext`), MUST 3 (step-11: the
  top-anchored `hatchFit` clearance measured from `TutorialUI.Guide`, in Task 6 itself; the `tutorial` check measures
  Guide at native / 1.0982 / 0.7106), MUST 4 page part (RebirthPage HatchTestHover + `btn.pulse(t, fixed)`), MUST 5 (one
  REBIRTH width 476, holder centre x 492 not ready / 370 ready or MAX).
- SHOULD 1 (6.7 contract: `refresh`, `ownedPets`, `B` / `RS` / `TweenService` / `RunService` / `RebirthConfig` names), SHOULD 2
  (token loop `if dirty or os.clock() < confirmUntil + 0.6`), SHOULD 4 (Rays centre-anchored at (86, 124), burst capped at
  132), SHOULD 8 (refusal setup with a qualifying pet), SHOULD 9 (REB1 forced 1.37), SHOULD 16 (reward cards: 15 % tile
  colour tint, Glow 0.4). `RebirthClientLegacy` byte copy, `rebirth_page_client.lua`, `streak_client.lua` section 5,
  Task 7 cross-checks for Index / Rebirth, Task 9 memory updates.

### Resumed 2026-10-22 (coordinator RESUME; the hub + Lighting were changed by another builder meanwhile, out of scope)
- [x] **SHOULD 10** (right after Task 3, fresh session, RIS helpers live): G1 Gift Daily native **0 fails / 1677 checks**,
  G1 Playtime native **0 / 2019**, S1 Shop top native **0 / 2837** (textFill 62/62); only the 4 known Gift notes (x5 86 %,
  PLAYED 85 %, SKIP ALL 99 %, 48 95 %). Gift snapshot: DAILY + every chrome group = BEFORE; the 181-group list = **ae122c90**
  (= the popup/Shop build's BEFORE and AFTER files) and it is stable inside the session (2 runs). Shop snapshot: ALL
  **985d5a8c** (Task 0 BEFORE: d31e8fb0); only `Rail.Label1-5`, `GiftPicker.Box` and `Scroll.List` differ.
  - A/B to settle it (owner rule: never guess): the pre-RIS Hatch was put back for ONE fresh session (the RIS Hatch parked in
    `_Backup_HatchNight.Before`, restored right after, `hatch_pure` 147/147 again): gift **ae122c90**, shop **985d5a8c** -
    identical to the RIS-helper session. So the helpers change nothing in Gift or Shop.
  - Ruling: the Task 0 session's Gift PLAYTIME groups (4b73c224) and Shop list (d31e8fb0) were a different session state
    (both from the same session; every later session, with the old or the new Hatch, gives ae122c90 / 985d5a8c) - why: the
    A/B proves the code is not the cause - cost if wrong: none for Gift / Shop (the A/B is the stronger proof). The
    BEFORE baselines for the end of the run are now **gift ae122c90** (= `hatch_gift_after.txt` of the popup/Shop build) and
    **shop 985d5a8c** (`hatch_shop_before_ris.txt`, re-captured with the pre-RIS code); the Task 0 lists stay in the files
    as history. Chrome: UI only, no 3D world; kept (the coordinator's re-capture note is about 3D-world baselines).
- [x] **Task 2 RED (Play)**: `_G.SettingsTests("open")` = **1 pass / 9 fail** on the Check-UI page (title SHOP-left-over /
  tooth / icon / AR 1.30 / CanvasScale / HatchCanvas / rows / header), no script errors.
- [x] Chrome baseline re-checked before Task 4 (fresh session, unchanged code): Shop / Rebirth / Index / Settings section
  hashes 225c112d / d9c86590 / d45e6ce0 / 890e9b10 = `hatch_chrome_before_v3.txt` exactly.
- [x] **Task 4 SETTINGS** (one sitting, Edit): `StarterPlayerScripts.SettingsClient` (new, 330 lines; draft
  `AppData/Local/Temp/ris/SettingsClient.lua`), MenuController (`PAGES.Settings.icon` = the gear + the 2-line guard after
  `local body = panel:WaitForChild("Body")` with its 2 comment lines; nothing else), BrickUI `PAGE_SKIN.Settings = "Hatch"`.
  - Session 1 (fresh, TestFreshSave true): settings_client open **10/0**, toggles **13/0** (server-written value flips and
    back; MusicGroup 0 / SFXGroup 0 follow; DayNightClient NightMode + ClockTime 0 -> 13.5 back), volume 8/1 (the 1 = a
    test bug, below), song **9/0** (RACE TO FINISH 77 % at 18), reopen **4/0** (closed: refresh count frozen; a change while
    closed = 1 refresh on reopen), respawn **4/0** (Server kills the character; still 1 HATCH page, opens), save round trip
    **both directions 7/0** (`{"music":false,"sfx":false,"night":true,"musicVol":0.3,"track":4}` then the defaults:
    SavePlayerNow + the stored save read back uncached = the attribute, key by key; key studiotest_<tag>_<userId>).
  - Containment SET2 (all off, NIGHT, 0 %, RACE TO FINISH) native + 0.7106: **0 fails** (1008 / 1006 checks). SET1
    (defaults, 100 %) native / 0.7106 / 0.6787 / 1.0982 / forced 1.37: **1 fail each**, the same one: `corner VolBar.Fill.Gloss`.
  - Bug found + fixed (TDD): the progress bar's gloss strip was full width with a 0.45-height corner, so its square-ish
    right end poked past the fill pill's rounded end (exactly "corners aren't even in the box"). New hatch_pure R7 check
    (gloss ends inside the pill at the smallest and the full fill width) FAILED first (147/1), then `H.progressBar` makes the
    strip a pill (corner round) inset `ga` = 6 at h 36 (computed from the pill + strip radii, any h): **148/0**.
  - Ruling: settings_client volume "52.2" compared a fractional offset; UDim offsets are integers (52) - test bug, now
    compared with `UDim2.fromOffset(52.2, 0)` - cost if wrong: none.
  - Perf (session 1): idle 3 s = SettingsRefreshN / HatchPerfSettings frozen; canvasguard 0 hidden-page writes (Settings /
    Shop / Gift x3 each); refresh avg 0.186 ms, max 0.476 ms (20 refreshes); counts SettingsPage 131 GuiObjects / 262
    instances / 41 UIStrokes (Check-UI pages, for runs B / C: Index 210 / 566 / 139, Rebirth 78 / 211 / 47); leaks 30 cycles
    131 -> 131 / 262 -> 262, Window 3707 -> 3707, LuaHeap -85.6 MB.
  - Ruling: the 0.3 ms Settings refresh target is judged on the AVERAGE (as the Shop's "refresh avg 0.091 ms"), the max
    is reported - why: one 0.48 ms sample in a ring of 30 at Studio's unfocused 60 fps is jitter (a refresh is 3 cached
    fits + 1 JSON decode) - cost if wrong: a 0.2 ms spike on a click, never per frame (no loop).
  - Logs: client + server, 0 non-CorePackages warnings / errors.
  - Shots so far (`hatch-night-build/ris/settings/`): settings_before, settings_off_night_vol0, settings_on_vol70_allsongs,
    settings_vol100_song1_sandcastles, settings_song2_beachparty, settings_song3_adventure, settings_night_song4_racetofinish
    (the fill-visible ones are re-shot after the gloss fix).
  - Session 2 (after the gloss fix): open **10/0**, volume **9/0**; containment SET1 native / 0.7106 / 0.6787 / 1.0982 /
    forced 1.37 (noOnTop) **0 fails each** (1014-1017 checks: barFill 1/1, corner 47/47, textFill 18/18, hitFirst 18/18);
    extra SET3 volume 10 % (the smallest, a circle) and 70 %: **0 fails**. Perf re-run: refresh avg 0.192 ms (max 0.339);
    leaks 90 cycles flat (LuaHeap 979.0 -> 980.8 -> 980.6 -> 983.2 MB every 10: GC noise). Results:
    `tests-2026-10-21/hatch_ris_perf_results.txt`.
  - Shots `hatch-night-build/ris/settings/`: settings_on_vol70_allsongs, settings_off_night_vol0, settings_vol100_song1_
    sandcastles, settings_song2_beachparty, settings_song3_adventure, settings_night_song4_racetofinish, settings_phone_scale
    (+ _full; HatchTestScale 0.7106, 524 x 333), settings_before_after, settings_legacy_fallback; zooms: zoom_header_gear,
    zoom_volume_0_off / 70 / 100, zoom_song_racetofinish, zoom_toggles_night, zoom_corner_bottom_left / top_right,
    zoom_phone_controls.
  - Legacy session (Edit TestSettingsLegacy = true, cleared after): `legacy` **4/0** (the Check-UI page in ~1 s, no
    HatchCanvas, Check-UI header, label = the saved value) + a REAL mouse click on the Check-UI MUSIC toggle flipped
    `music` to false (label OFF) and a second click back. Chrome legacy (`hatch_chrome_after_v3_legacy.txt`): Rebirth +
    Index = BEFORE; Settings = BEFORE except line 44 `Window.Face.Icon` (the gear) - as planned.
  - Ruling: the legacy run's Shop chrome section differs in 4 lines of the HIDDEN Check-UI header (size 0.22 vs 0.23) -
    why: MenuController resizes that header only on Check-UI opens and this session opened the Check-UI Settings first;
    history, not a change - cost if wrong: none (the normal-mode fresh-session AFTER checks the Shop section).

### Final checks (run A, 2026-10-22; every Play session started from Edit with TestFreshSave set + read back true,
### stopped by me, then set false + read back)
- [x] hatch_pure (Edit) **148/0**; StreakTests pure **24/24**; StarterPackTests pure **38/38**.
- [x] Session A (fresh, normal mode): gift snapshot 181-group list **ae122c90** = BEFORE (`hatch_gift_after_ris.txt`;
  the 2 PLAYTIME chrome groups that differ from DAILY are the window title + its shadow, as in BEFORE); shop snapshot ALL
  **985d5a8c** = BASELINE, stable after 2 dumps (`hatch_shop_after_ris.txt`); chrome (`hatch_chrome_after_v3.txt`) Shop
  **225c112d**, Rebirth **d9c86590**, Index **d45e6ce0** = BEFORE line for line; Settings 6c1a39a8 (26 of 51 lines differ:
  the Check-UI chrome hidden + the HATCH title / icon / close, as planned; 3 of them now equal the Hatch Shop's lines).
  This also closes the legacy-run Shop-header ruling: normal mode = BEFORE. hatch_assets **68 / ok 68 / failed 0**.
  shop_client (open **15/0**, layout **15/0** (slot hidden), reopen **4/0**, analytics **4/0**, canvasguard **2/0**, + new
  canvasguard_settings **1/0**: 0 hidden-ShopPage CanvasScale writes over 3 Settings open / close). StarterPackTests live
  **33/33**.
  - Ruling: shop_client ran as the file's prelude + those sections pasted verbatim (plus the 1 new check), not the whole
    file - why: the other sections need Server steps / their own sessions and cover Shop code this run did not touch (the
    snapshot ALL hash proves the Shop tree unchanged) - cost if wrong: a Shop behaviour change outside the tree (none: no
    Shop script was edited).
- [x] Session B (fresh): streak_client v2 **48/0** (run first, auto-open), StreakTests live **20/20**, settings_client open
  **10/0** + reopen **4/0** after the streak work. `ServerStorage.HatchRISTests.streak_client` = a copy of
  `StreakTests.CLIENT_SRC` (11055 chars, FNV 0cc17b20 = streak_client.lua) so the client can require it (test folder, inert).
- [x] Logs, both sessions: server 0 errors / 0 warnings; client 0 errors, only the TopbarPlus version notice and the
  CorePackages UIBlox FoundationProvider warnings (Roblox internals).
- [x] End state: Edit, no Play; TestFreshSave **false** (read back), TestSettingsLegacy nil, HatchBand nil, HatchTestScale
  nil, TestStarterPack **true**; RS.HatchRISTests absent in Edit; SettingsClient enabled; PAGE_SKIN = Gift / Shop / Settings
  Hatch; backups `MenuController_preRIS` / `IndexClient_preRIS` / `RebirthClient_preRIS` disabled, 0 tags, `BrickUI_preRIS`
  0 tags. Not published, not saved by me (owner: Save + Publish when happy; the Check-UI Settings fallback stays in
  MenuController for the 7 live days).
- Unverified: a real phone (only HatchTestScale 0.7106 emulation); the owner's eye on the steel-lilac band + gear.
- [x] **Visual review (Settings): orchestrator, SHIP** (2026-10-22; before/after + phone shots reviewed: matches the mockup,
  clean, no overlaps, corners inside the window). Run A closed.

## Run B (Index) - started 2026-10-22 in the same session (coordinator: same plan / review / hard rules; only Studio writer)
- [x] **B0 pre-flight**: Edit, no Play; `IndexClient` Source == `IndexClient_preRIS` (22558 chars, 0 tags).
  `StarterPlayerScripts.IndexClientLegacy` = byte copy (same Source), Enabled false, 0 tags, attribute `Note`.
  Before shots: `hatch-night-build/ris/index/index_before_fresh.jpg` (Task 0) + `index_before_idx2.jpg` (IDX2 data, local).
- [x] **B1 tests first (RED)**: `tests-2026-10-21/index_client.lua` (open, tabs, cards, names, secret, inspect, again, tile,
  claim, claimall, refusal, lifecycle1/2, legacy; mirrored as `HatchRISTests.index_client`, FNV f30484b8) +
  `hatch_ris_perf.lua` cost section for Index (tab sweep x6 + 5 cards, avg <= 2 ms; mirror FNV 6b4c6828).
  RED (fresh session): `open` **0 / 6** on the Check-UI page (no HatchCanvas, AR 1.75), no script errors.
  - Ruling: the coordinator's "tile badge on the left menu" does not exist today (the Index tile has no badge; only the
    Gift tile's Badge and RebirthClient's HUD "!"). IndexClient adds one: a copy of the Gift tile's red "!" Badge on
    `Menu.Index.Face`, shown while any area reward is claimable (= the rail Dots), updated only when IndexData changes (no
    loop, no pulse), behind `TILE_BADGE = true` - why: the coordinator asked to prove it works and it repeats the in-window
    "!" rule on the HUD like the Gift / Rebirth tiles - cost if wrong: one line (`TILE_BADGE = false`).
- [x] **Task 5 INDEX** (one sitting, Edit): `IndexClient` rewritten (28247 chars, FNV 30d473ba; draft
  `AppData/Local/Temp/ris/IndexClient.lua`, compiled with loadstring before writing) + BrickUI `PAGE_SKIN.Index = "Hatch"`
  (the 1 line; nothing else in BrickUI). Switches at the top: `SHOW_CARD_NAMES = false` (owner's call 5; Studio
  `workspace.TestCardNames` overrides it for tests), `TILE_BADGE = true`.
  - Ruling: cards are 66 wide every 75 (plan: 66.8 every 74.8) - why: UDim offsets are integers (66.8 -> 66, x 208.8 -> 208
    gave uneven 8 / 9 gaps); 5 x 66 + 4 x 9 = 366 = the AreaHead / Reward width exactly - cost if wrong: none (0.8 px).
  - Ruling: inspect stat L box (8, 4, 94, 16), not SHOULD 5's 92 - why: measured "HATCHED" @16 = 73 px = 84 % of 92 - 5
    (the review's 82 % estimate was low); 94 gives 82 % and still ends 2 px before V (104) - cost if wrong: none.
  - Ruling: the SECRET! tag and the bonus chip widths come from the measured copy at the 83 % rule (TAG_W from "SECRET!",
    BONUS_W from the widest "x%.1f" of all 30 creatures: "x3.9" @16 is 84 % of the plan's 42 box) - cost if wrong: none.
  - Ruling: SHOW_CARD_NAMES = true draws a name strip (2, 4, 62, 12) at 10 down to 7 (first word if the full name does
    not fit) and hides the secret star (the gold face still marks it) - why: a 66-wide card cannot hold a name at the
    16 minimum (MOSSBACK @14 = 125 %); true = the old tiny names, the owner's choice - cost if wrong: only when flipped.
  - Session 1 (fresh): index_client open **14/0**, tabs **7/0**, cards **3/0**, names 3/1 (RED: "BLACK / EASTERN DRAGON"),
    secret **10/0**, inspect **9/0**, again **2/0**, tile **6/0**; Server "complete area 1" -> claim **13/0** (claimed[1] = 2,
    IndexBonus +0.05, Potion_Money / Potion_Hatch +1 each, CLAIMED! silver Active false, Star1, tile badge off, 2nd press
    sends nothing); areas 2 + 3 -> claimall **5/0** (+0.10, potions +2 each = SHOULD 12); area 4 -> refusal **5/0**
    ("NOTHING TO CLAIM" red 1.3 s, an empty message -> "TRY AGAIN" = SHOULD 6); lifecycle1 -> Server PetIndex.record (a
    hatch) + area 5 -> lifecycle2 **5/0** (closed: IndexRefreshN 43 -> 43, IndexLoop false, tile badge follows; reopen:
    exactly 1 refresh, Dot5, CLAIM ALL (2)). Logs: 0 errors / 0 warnings.
  - Fix (TDD): the 2-line name split now picks the space that makes the WIDER line narrowest (tie -> the later space):
    BLACK EASTERN / DRAGON (141 px), MOSSBACK / TORTOISE, SEA TURTLE / WARRIOR, NIGHTMARE / STALLION ... -> names **4/0**.
  - Containment session 2 (before the fixes below): IDX1 native / 0.7106 / 0.6787 / 1.0982 **0 fails**; RED where real:
    IDX1 forced 1.45: 5 corner fails (the 4 reward-chip icons + the book: their box corners outside the round pill / recess
    ends - within tolerance at 1.18, not at 1.45); IDX2 / IDX3 / IDX4 native: Bonus IconShadow corner + `Total.ClaimAll`
    contain (the 1.04 hover grew it 1.5 px past the recess's right end).
  - Fixes: chip icons (8, 3, 22), book (10, 4, 28), bonus icon (8, 2, 16) (box + shadow inside the round ends);
    CLAIM ALL `hoverScale = 1` (the gloss brightens instead: Gift / Shop rule for tight holders). IndexClient 28740 chars,
    FNV 94cbafb8 (= the draft).
  - Containment session 3 (all **0 fails**): IDX1 native / 0.7106 / 0.6787 / 1.0982 (1505-1507 checks; hitFirst 26/26,
    textFill 45/45, drawOrder 5/5) + forced 1.45 (noOnTop, review SHOULD 9); IDX2 native / 0.7106 (barFill 2/2, 1600-1602);
    IDX3 (secret Card 5, CLAIM! breathing, pulse pass 1.03) native / 0.7106 / forced 1.45; IDX4 all 30 found at 12.5M KG,
    6 tabs x cards 3 / 2 / 5 = 18 runs, 29826 checks, 0 fails.
  - Other windows (session 2, fresh, before any IndexData change): gift 181-group list **ae122c90** = BEFORE; shop ALL
    **985d5a8c** = BASELINE; chrome Shop **225c112d**, Rebirth **d9c86590**, Settings **6c1a39a8** = run A AFTER (unchanged);
    Index 782558c8 (the HATCH skin, as planned). hatch_assets 68 / failed 0. Edit: hatch_pure **148/0**, StreakTests pure
    **24/24**, StarterPackTests pure **38/38**.
  - Perf (`hatch_ris_perf_results.txt`, run B section): idle = IndexRefreshN + HatchPerfIndex frozen; canvasguard 0 writes
    on every hidden page (Settings / Index / Shop / Gift x3); Index refresh avg **0.905 ms** (target <= 2 ms; max 1.99 ms);
    IndexPage 268 GuiObjects / 493 instances / 99 UIStrokes; 30 open / close cycles (6 tabs + 5 cards each) flat, LuaHeap
    -9.2 MB.
  - Shots `hatch-night-build/ris/index/`: index_empty_fresh, index_tab1_grass_card_selected, index_tab2_water_claimed,
    index_tab3_thunder_claim_available, index_tab4_fire, index_tab5_shadow_secret_unlocked, index_tab6_celestial,
    index_secret_locked, index_claim_all_6, index_full_all_claimed, index_phone_scale (+ _full; 0.7106, 524 x 333),
    index_before_after (+ index_before_idx2 / index_after_idx2, same data), index_before_fresh; zooms: card_row_selected,
    secret_card_and_inspect, rail, reward_claim, reward_claimed, total_claim_all, inspect_two_line_name, tile_badge,
    corner_bottom_left, corner_top_right, phone_cards.
  - Regression (fresh session, streak_client first): streak_client v2 **48/0**, StreakTests live **20/20**, StarterPackTests
    live **33/33**, shop_client open **15/0**, reopen **4/0**, analytics **4/0**, canvasguard **2/0** + canvasguard_index **1/0**
    (0 hidden-ShopPage writes over 3 Index open / close), settings_client open **10/0** + reopen **4/0**. Logs: client +
    server 0 errors / 0 warnings (only TopbarPlus + CorePackages UIBlox notices).
  - Legacy session (Edit TestIndexLegacy = true, cleared after): `legacy` **3/0** (IndexClientLegacy enabled at once, exactly
    1 IndexPage, no HatchCanvas, Check-UI chrome on open); chrome legacy: Index **d45e6ce0** = BEFORE v3 line for line,
    Rebirth d9c86590, Settings 6c1a39a8; no tile badge in the fallback (the old script). Shot `index_legacy_fallback.jpg`.
    The Shop section (22c4ae18) is the run A legacy ruling again (hidden Check-UI header history after a Check-UI open).
  - Owner switch check (Edit TestCardNames = true, cleared after): names on the 5 cards (MOSSBACK @8, FOREST STAG @7,
    TREANT @10, ??? @10, THORNBLADE @7; first word when the full name does not fit), containment **0 fails / 1556**.
    Shot `index_option_SHOW_CARD_NAMES_true.jpg`. Default stays false.
  - Deferred to run C (Rebirth + wrap-up), unchanged: review MUST 1 / 3 / 4 / 5 Rebirth parts, SHOULD 1 / 2 / 4 / 8 / 9 (REB1
    1.37) / 16 (Rebirth tint), `RebirthClientLegacy`, `rebirth_page_client.lua`, `streak_client.lua` section 5 (still
    expects Rebirth on Check-UI), Task 7 Rebirth cross-checks, Task 9 memory updates (`roblox-index.md`: the HATCH layout,
    SHOW_CARD_NAMES / TILE_BADGE switches, TestPress / TestClaimFail / TestCardNames / TestIndexLegacy hooks).
  - Unverified: a real phone (HatchTestScale 0.7106 only); real mouse clicks on the rail / cards / CLAIM (TestPress drives
    the same handlers; the hit-first probes prove each button is the top one at its centre).
  - End state run B: Edit, no Play; TestFreshSave **false** (read back); TestIndexLegacy, TestSettingsLegacy, TestCardNames,
    HatchBand nil; TestStarterPack true; IndexClient enabled (28740, FNV 94cbafb8); IndexClientLegacy disabled, 0 tags,
    = IndexClient_preRIS; PAGE_SKIN Gift / Shop / Settings / Index = Hatch; not saved, not published.
- [x] **Card-bar fix** (coordinator review of index_before_after / index_tab5): the flat dark pill under each card's art
  (the plan's card `Pedestal`, 50 x 10) read as an empty name slot. Removed on the cards in BOTH modes; the art grows
  58 -> 60 and centres in the freed space (Portrait (3, 30, 60), Glow (3, 26, 60, 68), Q (3, 46, 60)); a 60 box tilted
  -6 deg on hover is 65.9 wide, inside the 66 face. The inspect panel's flat bar became a soft ink ground shadow
  (`H.glow` (41, 138, 140, 24), INK, 0.2) for the same reason. IndexClient 28854 chars, FNV 1e093868 (= the draft).
  - Re-run (fresh session): open **14/0**, names **4/0**, secret **10/0**; containment IDX1 native / 0.7106 / 0.6787 / 1.0982 /
    1.45 (noOnTop), IDX2 native / 0.7106, IDX3 native / 0.7106 / 1.45 (noOnTop), IDX4 18 runs (29448 checks): **0 fails**.
    (One IDX3 1.45 run without noOnTop failed onTop on SpeedUI: the known forced-scale ruling, not a layout fault.)
  - SHOW_CARD_NAMES = true session (TestCardNames, cleared after): names strip + art still clear, containment native
    **0 / 1535** and 0.7106 **0 / 1533**; shot `index_option_SHOW_CARD_NAMES_true.jpg` re-taken.
  - Shots: `index_tab1_cardbar_fix.jpg`, `zoom_cardbar_before_after.png`, `zoom_card_row_after_fix.png`.
- [x] **Visual review (Index): orchestrator, SHIP after card-bar fix.** TILE_BADGE = true kept as the default (the
  coordinator tells the owner about the switch). Run B closed; end state Edit, TestFreshSave false, switches cleared.

## Run C (Rebirth + wrap-up) - started 2026-10-22 in the same session (coordinator: same plan / review / hard rules)
- [x] **C0 pre-flight**: Edit, no Play. `RebirthClient` Source == `RebirthClient_preRIS` (33751 chars, 0 tags). Run-C snapshots
  in `_Backup_HatchNight.Before`: `MenuController_preRISc` (disabled) + `BrickUI_preRISc` (with Hatch), both == live, 0 tags;
  folder attribute `HowToRestore_preRISc`. `StarterPlayerScripts.RebirthClientLegacy` = byte copy of today's RebirthClient,
  Enabled false, 0 tags, attribute `Note`.
- [x] **C1 tests first (RED)**: `hatch_pure.lua` R10 `H.tutorialFit` (31335 B, FNV b7d53c28); `streak_client.lua` section 5
  now expects the HATCH Rebirth (10919 B, FNV 0bfe0ce0); NEW `rebirth_page_client.lua` (open, states, lifecycle, tutorial,
  confirm, refusal, refusalpet, skipdry, skipreceipt1/2, legacy; 21314 B, FNV fa860906); `hatch_ris_perf.lua` Rebirth cost
  section + probe HatchPerfRebirthRefresh (10759 B, FNV 01415cc4). All mirrored to `HatchRISTests` (same FNV).
  RED: hatch_pure 148 / 1 (R10: tutorialFit nil); `open` **0 / 6** on the Check-UI page (no HatchCanvas, AR 1.25).
- [x] **Task 6 REBIRTH** (one sitting, Edit, each write compiled with loadstring first):
  - `BrickUI.Hatch` + `H.tutorialFit(s, cx, cy, guiH, topClear)` (additive, before `return H`; 50599 -> 51225 chars).
  - `MenuController` (25099 chars): `tutorialTop()` above hatchFit (TutorialExtra 3 + TutorialUI enabled + Guide visible ->
    the bottom of Title / Sub / Pips, converted screen -> MainMenu space, + 6) and 2 lines after the HatchTestScale line
    (`if openName == "Rebirth" ...: H.tutorialFit`). Nothing else.
  - `RebirthClient` rewritten: 38078 chars, FNV 0cc52270; PAGE region = draft `AppData/Local/Temp/ris/RebirthPage_region.lua`
    (26664 B, FNV 8f0a586e). BrickUI line `PAGE_SKIN ... Index = "Hatch", Rebirth = "Hatch"` written in the same call.
  - **HUD diff vs `_preRIS` (LCS, 251 -> 249 lines)**: exactly plan 6.6: pre 656 / 657 / 659 (B.image arrow, aspect
    constraint, ZIndex) -> new 786 (`H.image(page, "TutorialArrow", TUT_ARROW, ARROW_X, ARROW_Y, 48, 48, 10, true)`); pre 686 ->
    new 814 (`UDim2.fromOffset(ARROW_X + bob * 12, ARROW_Y)`). **Byte-identical**: canRebirth() (422 chars), the tile badge
    makeBadge / updateBadge (1837), the REBIRTH READY banner (4756), the cached canRebirth poll + badge pulse (639).
  - Ruling: SKIP and REBIRTH use `hoverScale = 1` (the gloss brightens) - why: they sit 8 px apart; a 1.04 hover on the
    476-wide REBIRTH reaches x 739.5 and overlaps SKIP's 1.04 hover (Gift / Shop / CLAIM ALL rule for tight holders); the
    ready breathing (1.00-1.04, Skip hidden) is unchanged - cost if wrong: one opt per button.
  - Ruling: the pet portrait (Ring.Pet) gets a round UICorner - why: a square Fit image's box corners leave the round ring
    (corner check) - cost: none (it reads as a round portrait in the ring).
  - Ruling: the TAP AGAIN! window also gets a one-shot `task.delay(2.6)` refresh (as today) on top of SHOULD 2's loop rule -
    why: the loop ticks every 0.5 s from the open, so the label could stay up to 0.5 s past the 2.5 s; one delayed call,
    not a loop - cost: none.
  - Built as planned: violet band, coin (gloss pill (12, 6, 60, 30) + TopHL (30, 4, 24) inside the circle), rays
    centre-anchored at (86, 124), 12 deg/s only on screen, burst 132 (SHOULD 4); 2 lines; GetLabel + lines 14 px clear;
    4 dark reward cards, face top tinted 15 % + glow 0.4 (SHOULD 16); pet + money chips (money centred at x 192 on R1);
    SKIP gold priceButton (live price); REBIRTH 476 x 60 always, centre 492 / 370 (MUST 5); shine every 1.85 s; MAX silver,
    Active false; refusals 1.3 s with the 83 % variants (MUST 1); HatchTestPulse / HatchTestHover wired (MUST 4); dry-run
    SKIP (TestSkip refuses + warns without TestDryRun; no real prompt ever); probes RebirthLoop / RebirthRefreshN /
    HatchPerfRebirth / HatchPerfRebirthRefresh. Closed: no RenderStepped, no loop, Money only marks dirty (D8 / D9).
- [x] **MUST 3 measured** (the review's guide estimates were low: it subtracted the inset, but both guis use the same space,
  and the Pips row is the lowest text): Studio 1519x753: guide Pips bottom **142.6** gui px -> clear 148.6 -> s 1.18 ->
  **1.1486** (window top 70 -> 148, -2.7 %); computed 1050x620 (guide x1.0): Pips bottom 120.4 -> s 1.0982 -> **0.914** (16 px
  text -> 14.6); computed 844x390 phone (guide 0.629 x 0.8): Pips bottom 61.5 -> s 0.7106 -> **0.58** (16 px text -> 9.3 pt;
  the review expected 0.67 / 10.7 pt). Phone-proportion emulation in Studio (guide WindowScale 0.503 x 695/346, window
  height-limited) measured s **0.590**. R10 keeps the review's rows (pure function test).
  - **Owner's call (new)**: accept the smaller step-11 Rebirth window on phones (one tutorial step, ~9 pt text), or the
    review's alternative: the guide slides away / shrinks in step 11 (TutorialClient, out of scope; not built).
- [x] Session 1 (fresh): `rebirth_client.lua` **13/0** (first); open **12/0**, states **18/0**, lifecycle **5/0** (closed:
  RebirthLoop false, HatchPerfRebirth + RebirthRefreshN frozen; reopen exactly 1 refresh), tutorial **10/0** (guide above the
  window at native / 1.0982 / 0.7106; arrow 38 px right of the 1.04 face), confirm **8/0**, refusal **2/0** (Server gave a
  Water pet first: SHOULD 8), refusalpet **2/0**, skipdry **5/0**, skipreceipt **3/0**.
  - Flows (TestFreshSave save): confirm = 2 presses -> server Rebirths 0 -> 1, Money 25000 -> 0, Speed 1234 -> 0,
    SpeedMultiplier 2 -> 2.25, Boosts.money 2.5, pet slots 3 -> 4, Base1 Plot.Floor 40 x 40 -> **44 x 50** (Width / Length,
    base Rebirths 1); coin 2, flash seen. TestReceipt(3716712457) -> Rebirths 1 -> 2, coin pop 1.25. No real Robux prompt.
  - Containment (0 fails each): REB1 native / 0.7106 / 0.6787 / 1.0982 + forced 1.37 (noOnTop, SHOULD 9) (1400-1403
    checks); REB2 step 11 + pulse 1.04 native (s 1.1468) / 0.7106; REB3 native / 0.7106; REB4 TAP AGAIN! native; REB5 MAX
    native / 0.7106; REB6 held refusals ("NEED MORE $!" @26, "TEST SAVE ONLY" @23) native / 0.7106; REB7 R19 "$9.99T / $32T"
    + CELESTIAL PET NEEDS 1M+ KG native. (REB3's first run: 3 fails = the tutorial finish screen on top + the window caught
    mid-tween right after REB2's TutorialExtra 3 -> 0 in the same step; harness artifact, re-run 0.)
  - Ruling: the Starter Pack popup (TestStarterPack true; it auto-opens on local tutorial attribute changes) is closed
    locally (`StarterPackUI.Enabled = false`, what its own close does) before each containment run / shot.
- [x] Session 2 (fresh): gift 181 groups **ae122c90** (=); shop ALL **985d5a8c** (=); hatch_assets 68 / failed 0;
  shop_client open **15/0**, reopen **4/0**, analytics **4/0** (Rebirth after the Shop = exactly one false), canvasguard
  **2/0**; settings_client open **10/0**, reopen **4/0**; index_client open **14/0** (13/1 first: the pill was left on tab 6 by
  the perf leaks sweep; Tab_1, then 14/0). Perf (`hatch_ris_perf_results.txt`, run C section): idle all frozen +
  RebirthLoop false; canvasguard 0 writes x5 openers; Rebirth ready RenderStepped avg **0.0087 ms** (<= 0.05), refresh avg
  **0.125 ms** (<= 0.3; steady ~0.07, the 1.6 ms max is the first refresh at load); RebirthPage 152 GuiObjects / 265
  instances / 48 UIStrokes; 30 cycles flat, LuaHeap -15.5 MB.
  - Chrome: Shop **225c112d** (=), Rebirth a67275d8 (the HATCH skin, planned), Index 60d834c0 / Settings 5435f5b8.
    Ruling: Index / Settings differ from run B only because no Check-UI page opens before them any more (the hidden Check-UI
    header / title keep their first values). Proof, legacy session (Rebirth on Check-UI again = run B's order): Rebirth
    **d9c86590** = BEFORE v3, Index **782558c8**, Settings **6c1a39a8** = run B exactly; Shop 22c4ae18 = the run A / B
    legacy ruling.
- [x] Session 3 (fresh): streak_client v2 **48/0** (first), StreakTests live **20/20**, StarterPackTests live **33/33**,
  RebirthV6Tests live **5/5**. Edit: hatch_pure **161/0**, StreakTests pure 24, StarterPackTests pure 38, RebirthV6Tests pure 45.
- [x] Legacy session (TestRebirthLegacy, cleared after): `legacy` **4/0** (RebirthClientLegacy enabled at once, exactly 1
  RebirthPage without HatchCanvas, exactly 1 RebirthReadyUI + RebirthTutorialUI = the HUD ran once, Check-UI chrome).
- [x] Logs, every session: 0 errors; warnings only the Roblox UIBlox / TopbarPlus notices, the expected TestSkip refusal
  (skipdry) and the legacy takeover line.
- [x] Shots `hatch-night-build/ris/rebirth/`: rebirth_need_r0_pc, rebirth_need_pet_pc, rebirth_ready_pc, rebirth_confirm_pc,
  rebirth_max_r20_pc, rebirth_refusal_skip_dryrun_pc (SKIP + REBIRTH refusals held), rebirth_tutorial_step11_pc,
  rebirth_tutorial_step11_phone_emulated, rebirth_phone_scale (+ _full, 0.7106), rebirth_before_after, rebirth_legacy_fallback;
  zooms: coin_title, reward_cards, needs_chips, buttons_skip_price, ready_button_pet_portrait, tutorial_arrow,
  max_coin_rewards, phone_needs_buttons, corner_bottom_left, corner_top_right.
- Unverified: a real phone (HatchTestScale 0.7106 + the step-11 emulation only); real mouse clicks (TestPress / TestSkip
  drive the same handlers; hit-first probes pass); the owner's eye. Left for the coordinator: Task 9 memory updates.
- End state run C: Edit, no Play; TestFreshSave **false** (read back); TestSettingsLegacy / TestIndexLegacy /
  TestRebirthLegacy / TestCardNames / HatchBand nil; MainMenu HatchTestScale nil; TestStarterPack true; RS.HatchRISTests
  absent in Edit; RebirthClient enabled (38078, FNV 0cc52270), RebirthClientLegacy disabled; PAGE_SKIN Gift / Shop /
  Settings / Index / Rebirth = Hatch. Not saved, not published.
