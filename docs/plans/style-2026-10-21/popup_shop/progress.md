# HATCH NIGHT popup + Shop: build ledger (2026-10-21)

Plan: `docs/plans/2026-10-21-hatch-night-popup-shop.md`. Review: `....review.md` (APPROVE WITH CHANGES: MUST 1-11 + SHOULDs).
Owner's calls (decided, "do as recommended"): magenta band all year; left rail inside the window; frameless sticker boost
art (old ids kept in `BOOST_ART`); full 740x470 popup; BUY breathing on (1.00..1.02); keep `ShopClientLegacy` 7 days live.
Studio: 0663e976-4faf-4dca-bf0c-91120a8d1353, viewport 1519x753.

## Tasks

- [x] **Task 0** (pre-flight + BEFORE evidence). Edit, TestFreshSave read back true, Play.
  - Test tools (Server DataModel, Play only): `ServerStorage.TestReceipt` BindableFunction `:Invoke(player, productId)`;
    `ServerStorage.TestProcessReceipt` BindableFunction `:Invoke(player, productId, purchaseId)`; `ServerStorage.StarterDebug`
    BindableFunction `:Invoke(op, player, value)`, ops reset / endsAt / restricted / seen / grant / buy (buy = REAL prompt
    while the offer is live: never used). `ServerStorage.StarterPackTests` ModuleScript (exists in Edit). None of the
    three runtime tools exist in Edit (checked).
  - MUST 1.3: today's Check-UI Shop at 1519x753 = win 906.1 x 566.3 in mm 1519 x 695 -> **H ratio 0.8148** (= LAYOUT 2.0 x
    BaseSize 0.4074, exact). Above 0.80, so R = 0.8148.
  - `hatch_chrome_before_v2.txt` (v2 filter, fresh session; header: Menu right 221.76, SpeedUI.Holder (14.28,537.93
    263.89x145.46)); 51 lines per section.
  - `hatch_gift_before.txt`: group hashes, 2 identical runs in one session.
  - `hatch-night-build/popup_shop/shop_before.jpg`, `popup_before.jpg` (StarterDebug reset + Rebirths 1, Magma egg, area 4
    "Fire"). The 3D world renders white (Studio unfocused); the GUI is fine.
  - Ruling: `hatch_gift_snapshot.lua` freezes PLAYTIME by setting the player's `PlaytimeStart` LOCALLY to now-5 s during the
    dump (restored after), and skips the hidden PlaytimeView's descendants in the DAILY dump - why: those carry the
    state the view last showed (run 1 vs run 2 differed only there), so they are history, not layout - cost if wrong: a
    PlaytimeView change only visible while the DAILY tab is shown would be missed (the PLAYTIME section still covers
    the whole view).
  - Ruling: the gift snapshot saves one hash per path group (4 levels) instead of one per line - why: 2 x 1494 lines,
    and a differing group still points at the subtree to inspect - cost if wrong: none for detection (any changed line
    changes its group hash).
  - Ruling: chrome snapshot v2 PRE "Shop" opens the Hatch Shop, then the next window straight over it (no close) for
    each of Rebirth / Index / Settings - why: that is the skin-switch path; the v1 "PRE then loop" would have closed the
    Shop by re-opening it - cost if wrong: none (an extra path).
- [x] **Task 1** backups + legacy. `ServerStorage._Backup_HatchNight.Before`: `ShopClient_prePopupShop`,
  `StarterPackClient_prePopupShop`, `MenuController_prePopupShop` (all Enabled false), `BrickUI_prePopupShop` (+ `Hatch`);
  sources byte-identical to the live ones, 0 tags left in the folder; folder attributes `WasEnabled_prePopupShop`,
  `HowToRestore_prePopupShop`. `StarterPlayerScripts.ShopClientLegacy`: byte copy of today's ShopClient, Enabled false,
  tags stripped, the note in attribute `Note` (MUST 10.5).
- [x] **Task 2** BrickUI.Hatch extensions (6.2) + hatch_pure.lua RED (9 fails on the new checks) then GREEN (79/81 then
  the 2 below fixed; final full run in Task 6). Scroll probe (7.2, Play, UIScale 0.5): (a) AbsoluteCanvasSize.Y 500
  (scales); (b) max CanvasPosition.Y 450 = screen px, so **K = s** (CanvasPosition = logical y x CanvasScale; the build
  uses K = Scroll.AbsoluteSize.Y / 386 at use time); (c) AbsoluteWindowSize 95.5 of 100 px = the 8 px bar scales (4 px +
  rounding): no ScrollBarThickness rebinding needed; (d) inner child at CanvasPosition 100 sits at -90 px (= 10 - 100):
  consistent with K = s. Stroke scaling not re-measured (the Gift probe proved it).
  - In-engine GothamBlack width table (TextService, 58 strings incl. every 4.12 / QA top-5 string): max copy fill 80 %
    ("TREADMILL"@16 in the 114 rail label), 79 % "EVERY EGG IN YOUR BASE"@16 and "KEPT ON REBIRTH"@16, 78 % "HATCH ALL
    EGGS"@24, 77 % "BEST VALUE"@16, 74 % "29.4%"@20. Refusal words only: "ALREADY OWNED"@18 in 166 = 96 %, "NEED MORE
    $!"@16 in 112 = 99 % (see the Word-box ruling). In-engine "1499"@26 = 55 px (the review estimated 68).
  - Ruling: `priceButton.setWord` lays the Word in an 8 px-padded box (w - 16), like the price group - why: otherwise
    "NEED MORE $!" fills a 112 treadmill button to 99 % (cramped, the owner's complaint); with the padding the MUST 5
    short variant "NEED $!" is chosen there and the full words stay on the 166+ buttons - cost if wrong: none (a variant).
  - Ruling: MUST 4's pure check expected "1499" to step below 26, but in-engine it is 55 px wide and fits at 26 (G 93 <=
    96); the check now asserts G <= 96 + centred for "1499" and a real step-down on "99999" (26 -> 20, G 93) - why: the
    review's width came from the wider mockup font - cost if wrong: none (the rule G <= w - 16 is what is enforced).
  - Ruling: `H.arrow` points nudged 1 px in, (4,4)-(14,11)-(4,18) instead of (3,3)-(14,11)-(3,19) - why: the 7 px ink bar
    ends of the plan's points reach x -0.47 / y -0.86, outside the 18 x 22 box (a containment fail at 1.2x) - cost if
    wrong: the chevron is 2 px shorter.
  - Ruling: `H.sectionHeader` icon at y 1 (plan 2) and the Title box `min(200, tw + 8)` (plan 200) - why: the +3 ink shadow
    of a 26 px sticker at y 2 ends at 31, past the 30 px header; a 200 box would run under the line - cost if wrong: the
    icon sits 1 px higher.
  - Ruling: the transient option (MUST 6) keeps the button in `H.buttons` while it lives and removes it on
    `holder.Destroying` (the review's 2nd option, opt-in via `opts.transient`) - why: picker rows still get the test hover
    pass; nothing leaks - cost if wrong: none.
- [x] **Task 3** `BrickUI.PAGE_SKIN = {Gift = "Hatch", Shop = "Hatch"}`; MenuController: `hatch.setTheme(H.bandTheme(name))`
  and `H.fitWindow(..., H.pageCap and H.pageCap(openName, gs.Y))`. Play (1519x753): Rebirth 548.6x438.9, Index
  859.8x491.3, Settings 570.5x438.9 = the BEFORE sizes, HatchBack hidden; Shop = night shell, title SHOP, tooth
  (220,0,100), bats hidden, window 891 x 566 (s 1.2041; old Check-UI Shop 906 x 566).
  - Ruling: MenuController changes 4 lines, not 2: `local openName` moved above `hatchFit` (one line added there, the old
    declaration line replaced by a comment) - why: `hatchFit` is defined BEFORE `local openName`, so the review's
    `H.pageCap(openName, gs.Y)` would read a nil GLOBAL and the Shop would never get its big cap - cost if wrong: none
    (the same local, declared earlier; every other use is below both lines).
- [x] **Task 4** ShopClient rewrite (6.4; 1005 lines; draft `AppData/Local/Temp/hn/ShopClient.lua`). Rail + scroll list,
  Starter slot, passes / Double / 3 boosts / 6 packs / Treadmill / Eggs, gift picker, toasts, dry-run buy path
  (TestDryRun / TestLastBuy / TestDryRunResult / TestDryRunHold), pressed-tab rule, event-driven open/close, fallback.
  - Ruling: `List.StarterSlot` is the whole content margin box (0, 0, 584, 136) and StarterPackClient puts the card at
    (4, 4) 576 x 128 with HatchPad 4 (the plan: slot 576 x 128 at (4, 4)) - why: the card's 2.5 px outline stuck out of
    an invisible 576 x 128 parent (2 containment fails per run); the card itself did not move - cost if wrong: none.
  - Ruling: Treadmill at MAX shows `NowName .. " MAX"` (gold) + MAX LEVEL, no buttons - the plan's Double wording reused.
  - Ruling: `ScrollTo` (PetsEggsUI GET MORE) counts as a pressed tab - why: MUST 8's clamped-scroll rule then keeps the
    Pill on the asked section - cost if wrong: none.
  - Ruling: boosts / packs art y 30, title y 88, sub y 110 (review SHOULD 19, the sub clears the button at hover).
  - Ruling: SHOULD 1 applied as glows 0.4 (wide cards) / 0.45 (small cards) and a 15 % pass-colour tint on the pass faces.
  - Ruling (found in Task 6): the `HatchButtons` probe is written on `task.defer` - why: picker rows leave `H.buttons` in
    their `Destroying` handler, which runs deferred, so the immediate probe counted the rows just destroyed (51 -> 59
    after 10 rebuilds, a false MUST 6 fail); deferred: 50 -> 50 - cost if wrong: none (Studio-only probe).
- [x] **Task 5** StarterPackClient rebuild (6.5; draft `.../hn/StarterPackClient.lua`): 740 x 470 HATCH NIGHT popup, no
  bats, magenta band, hero / 3 reward rows / odds strip / NO THANKS + gold BUY (pre BUY, breathing 1.00..1.02), one
  RenderStepped + a ticker only while shown, expiry timer, the Shop card in the slot (its BUY only opens the popup).
- [x] **Task 6** tests (all green; numbers):
  - hatch_pure.lua (Edit): **82/82**.
  - Containment v2, every run **0 fails**: S1 top native / 0.7106 / 0.6787 / 1.0982 (2775 / 2773 checks); S2 y 0 / 504 /
    866 / 1280(=1248) / 1248 at native + 0.7106 (2847-2971 checks each); S3 owned/MAX/MAX LEVEL y 0 / 504 / 1248; S4
    tier 1 + 4 held refusals (NEED $! / NEED MORE $! x2 / OFFER ENDED) at TREADMILL + POTIONS, native + 0.7106; S5 1499
    override + huge income (titles +562Qi / +4.5Sx) top + SPEED, native + 0.6787; S6 picker 1 row and + 8 fake 20-char
    rows, native + 0.7106 (3081-3811 checks); P1 native / 0.7106 / 0.6787 / 1.1702 (679); P2 restricted native + 0.7106
    (518); P3 last hour, refusal held x2, thanks held (614-679); P4 odds 6 / 7 at native + 0.6787 (696 / 713); G1 Gift
    Daily + Playtime native + 0.7106 (1675-2027).
  - shop_client.lua: open 15/15, layout hidden 15/15 + shown 15/15, prices 16/16 (GamePass for passes, Product elsewhere;
    the Asset lookup of Grow All returns nil = MUST 3's point), buys 19/19 (every B2 path + MUST 11 refusal without dry
    run + owned VIP sends nothing), refusal 7/7, treadmoney (REAL, Money 0 < $10K) 3/3, scroll hidden 11/11 + shown
    11/11 (MUST 8 Tab_TREADMILL -> TREADMILL), reopen 4/4 (MUST 2), gift 11/11 incl. MUST 6 + MUST 7, toasts got 5/5,
    sent 5/5, granted 5/5, states 6/6, nosign 2/2 (SHOULD 3), analytics 4/4, respawn (7.3 check 8) ok, legacy session
    8/8 (MUST 10.3), B24 (the offer ends while the Shop is open) 6/6.
  - starter_popup_client.lua: auto-popup (opened 3.05 s after the reset, once in 24 s), open 28/28, close paths by real
    MCP mouse clicks (CloseHit, NoThanks, Backdrop each close; clicks on PotionRow / Odds do not) 4/4, inside 7/7, seen
    2/2, timer normal 8/8 + urgent 8/8, buy 7/7, odds (a)-(g) at 5 / 6 / 7 cells 21/21, restricted 5/5, thanks 4/4,
    owned 5/5, expiry 3/3, B23 (the policy flips while open: odds hide and come back live) ok.
  - Perf (hatch_shop_perf_results.txt): idle counters flat (twice); Shop refresh avg 0.10 ms / max 0.16 ms per 0.3 s tick;
    popup RenderStepped work avg 0.012 ms / max 0.049 ms; 30 leak cycles flat (ShopPage 599 GuiObjects / 1096
    instances, StarterPackUI 175 / 254, HatchButtons 49, PickerConns 0, LuaHeap +0.3 MB).
  - hatch_assets.lua: 62 assets, failed 0. Snapshots: gift AFTER = BEFORE (181-group list FNV ae122c90 in both); chrome
    Rebirth / Index / Settings: see the ruling below. Regression: StarterPackTests pure 38/38 + live 33/33 (its 3 "buy"
    calls are all in refused states: not started / ended / owned); StreakTests pure 24/24 + live 20/20; streak_client v2
    48/48; starter_hud_client layout 28/28, placement 10/10, states 34/34, hover 12/12, content 11/11, expiry 3/3. Logs:
    0 errors (client + server) in every session; the only warnings are the MUST 11 refusals the tests provoke.
  - Ruling: chrome snapshot BEFORE vs AFTER, Rebirth / Index / Settings: 43 of 51 lines identical; the other 8 (window /
    depth / body / close strokes, header divider + highlight heights) differ ONLY by `BrickUI.deviceScale()` at
    MenuController start: BEFORE was captured with 0.52 (strokes 1.82 / 0.78 / 0.62 / 1.46, dividers 2 px, highlight
    1 px), AFTER with 1.18 (4.13 / 1.77 / 1.42 / 3.3, 4 px, 2 px). Proved by re-hashing the AFTER lines with the 0.52
    values: all 24 match BEFORE. PRE Gift / PRE Shop runs = the fresh run for all three windows. The Menu right edge
    (221.76 BEFORE, 173.88 AFTER) moved too - why: a pre-existing start-up race (Check-UI styles once at start with the
    camera ViewportSize; in the Task 0 session it was not ready yet), not this build (the MenuController restyle lines
    are untouched; the legacy session read 4.13 at load) - cost if wrong: a real Check-UI change hidden in those 8 lines
    (none: every one was re-derived). BEFORE could not be re-captured (the code is already changed). Reported to the
    owner as a separate bug.
  - Ruling: containment v2.1 (test only): with the gift picker open, only the picker buttons are hit-probed (its shade is
    modal by design), and TextTruncate labels skip textFits and use their box as their width (MUST 7 names end in
    "..."). Without these, S6 showed 20 / 44 "fails" that were the design.
  - Ruling: streak_client.lua section 5 now opens Rebirth instead of the Shop as the "other window keeps Check-UI" check -
    why: the Shop is a HATCH NIGHT page now - cost if wrong: none (the Shop is covered by shop_client.lua).
    `ServerStorage.StreakTests.CLIENT_SRC` (a stored copy) was NOT updated (test module, out of scope).
  - Ruling: shop_client legacy check "PAGE_SKIN.Shop cleared" removed - why: execute_luau runs in its own Lua VM, so its
    require(BrickUI) is another table; the effect (Check-UI chrome on the legacy Shop) is checked instead.
  - Ruling: the forced HatchTestScale 1.45 Shop run fails onTop (SpeedUI x2) because the test switch centres the window
    over the left HUD; not a real layout (real scales come from fitWindow with the HUD clearance). Not in the plan matrix.
  - Ruling: frame times in the perf file are the Studio unfocused 15 fps throttle (66.7 ms) for every state; the targets
    are judged on the probes (refresh / RenderStepped work).
  - Not run: starter_hud_client envelope / motion / flicker / overlaps / timer - why: they exercise StarterPackHud alone
    (untouched, out of scope); the sections that touch the popup / Shop (states, hover, content, expiry) were run.
- [x] **Task 7** screenshots `docs/plans/hatch-night-build/popup_shop/`: popup, popup_restricted, popup_urgent,
  popup_error, popup_thanks, popup_phone (0.7106, cropped x2; full frame popup_phone_full); shop_top, shop_speed,
  shop_potions, shop_bottom, shop_gift, shop_states (+ shop_states_bottom), shop_refusal, shop_phone_top,
  shop_phone_potions; gift_after, rebirth_after, index_after, settings_after; shop_before_after, popup_before_after;
  zooms: zoom_price_groups_passes, zoom_price_double, zoom_boosts_best_value, zoom_packs_best_value, zoom_rail_pill,
  zoom_treadmill_money, zoom_popup_odds, zoom_popup_buy, zoom_refusal_words. Passes were set false LOCALLY for the gold
  prices (the owner account owns all 4) and restored. Treadmill MAX shots show "x1 MAX" because the tier was faked
  locally (the sign still says x1); a real tier 11 reads the sign name. The plan 7.10 Haiku visual review is left to
  the coordinator.

## Review items

- MUST 1-11: all applied (MUST 1 pageCap 0.8148 -> s 1.2041 at 1519x753; MUST 2 one on-screen signal, reopen test;
  MUST 3 InfoType per lookup; MUST 4/5 price step-down + short refusal; MUST 6 transient buttons, flat; MUST 7 names
  truncated, toasts min 18 + cut names; MUST 8 pressed tab wins; MUST 9 no StarterDebug "buy" while live (only the
  suite refused-state calls); MUST 10 legacy fallback, its own session; MUST 11 dry-run switch on every Robux key).
- SHOULDs applied: 1-21, 25, 26 (B21-B26 all tested), 22 (HUD edges recorded; they differed - see the ruling), 23 (Tasks
  3-5 in one sitting; nothing saved / published).
- SHOULD skipped: 24 (phone-emulator MicroProfiler glance) - why: it needs Studio UI driving (device emulator +
  MicroProfiler), which the rules forbid; the per-tick probes stand in for it.
- 6.2 diff rule (BrickUI.Hatch vs `BrickUI_prePopupShop.Hatch`): 793 -> 940 lines; 66 old lines changed, all signature
  extensions or re-indents of default paths: glossButton pulse line (amp/period fields), recess / chip signatures +
  corner radius lines, shellCard Hit block (wrapped in `if not opts.noHit`), its gradient line (opts.grad), setToday
  restore line, the hover handlers (wrapped in `if not opts.noHover`), bandTheme signature, windowChrome signature + the
  bats block (wrapped in `if opts.bats ~= false`), the bats loop `want` line, setTheme bats line. Default behaviour
  proved identical by the gift snapshot (AFTER = BEFORE) and G1 containment. BrickUI: 1 line (PAGE_SKIN). MenuController:
  3 old lines (fitWindow call, the moved `local openName`, setTheme).

## Fix round (2026-10-21): visual review FIX THEN SHIP + perf review OK TO SHIP, one pass

Backups first (`ServerStorage._Backup_HatchNight.Before`, disabled, 0 tags): `BrickUI_preViewportFix` (with its Hatch),
`MenuController_preViewportFix`, `ShopClient_preFixRound`, `StarterPackClient_preFixRound`; restore note = BrickUI attribute
`HowToRestore_preViewportFix`. Studio is the source of truth: the drafts in `AppData/Local/Temp/hn` (ShopClient.lua,
StarterPackClient.lua) are pre-fix-round and were NOT synced.

### Done
- [x] **MUST 1** pack titles = `string.upper(pk.potion)`: MONEY / HATCH / SPEED.
  - Test first: containment v2.2 adds `textFill` = every non-Gift line's glyphs <= 83 % of (box - 2 x stroke). Watched
    it fail on the old copy: `H.fit(title, "MONEY POTION")` -> `FAIL textFill ... 'MONEY POTION' 87%` (textFill 66/67);
    the fixed Shop: 67/67.
  - Ruling: boxes that hug their text by design carry `HatchHug` and are exempt (Price, Pre, Now / Next, section
    titles); the price-button Word and the toasts carry `HatchFill 0.83` (H.fit room x 0.83) - why: a hug box is 100 %
    by construction - cost if wrong: a hug label could crowd its neighbour (textClear / textWidth still check that).
  - Ruling: the Gift window is frozen, so its lines over 83 % are NOTES, not fails: Card7 Chip1 'x5' 86 %, PlayBar
    'PLAYED' 85 %, SkipAll 'SKIP ALL' 99 %, SkipAll Price '48' 95 %. For a later Gift pass (owner / coordinator call).
  - Found by the new rule and fixed: the popup odds `Pct` at 6 / 7 cells (HatchTestOdds) filled 88-100 %. `Pct` now has
    HatchFill 0.83 and, for 6+ cells only, its box runs to the cell edge -> 6 cells 19-20, 7 cells 16-18; the real
    5-cell strip keeps 20 in the old box. Residual: a 7-cell string wider than "29.4%" at 16 could still pass 83 %
    (7 cells is the stress switch, no egg has 7 lines today).
- [x] **MUST 2** gift picker fits its content: `fitPicker(n)`, box 79 + min(307, 8 + 68 n), centred in the body
  (y 66 + (386 - box) / 2), inner parts resized, Empty1 / Empty2 at y 80 / 104. PickerBoxH 155 / 155 / 291 / 386 / 386
  for 0 / 1 / 3 / 6 / 8 rows.
- [x] **SHOULD 3** restricted popup = 374 tall (`chrome.setHeight`), face / canvas 367, buttons at 288 (centre 318), rows
  101 / 175, hero (155, 184); re-laid out live when the policy flips while open (B23, both directions, 0.00 s).
- [x] **SHOULD 4** tier 1 (no Robux skip): one wide lime `MoneyWide` 160 x 54 in the Robux slot (404); Money / Robux hidden.
- [x] **SHOULD 5** MAX: `MaxText` never shown; `MoneyWide` = silver MAX, not Active (a press is blocked); Now keeps the
  gold "xN MAX".
- [x] **SHOULD 6** boost + pack titles 20 (the price stays 22). Ruling: box (6, 89, 174, 20) instead of the review's
  (6, 88/90, 174, 22) - why: H.text sizes the text from the box height; same centre y 99 - cost if wrong: none.
- [x] **SHOULD 7** x2 MONEY card: plain `H.CARD.top` face (no gold tint), glow 0.3.
- [x] **I-1** the Starter card's BUY pulses only while the card is in the scroll's visible box (RenderStepped off
  otherwise; CanvasPosition re-checks).
  - Bug found by the new cardpulse test and fixed: the first version read `AbsolutePosition`, which right after a
    Shop open or a scroll step is still the previous layout's -> after a reopen the card stayed still at the top
    (cardpulse 3/8). Now the in-view test reads CanvasPosition / K in the List's logical px. cardpulse 11/11.
- [x] **I-2** the refresh is 6 parts (passes, double, boosts, packs, treadmill, eggs), each in its own pcall, one warning
  per part per session; `robux()` returns the fallback for a nil / 0 id. Studio switch `ShopPage TestBreakSection = i`.
- [x] **I-4** `bindCanvasScale` returns while the page is hidden and re-binds when it shows.
- [x] **I-3** = the owner's real-phone MicroProfiler check (not done here). The reviewer's no-tween-on-phone snippet is in
  MenuController behind `SNAP_SHOP_ON_TOUCH = false` (a flag, default off: no behaviour change).
- [x] **Item 7** (start-up viewport race): BrickUI (client) waits for a real viewport (>= 100 x 100) before the first
  deviceScale read, capped at 5 s; `deviceScale()` returns 1 (not 0.52) while the viewport is not ready; strokes, tiles
  and headers are tracked and re-applied on every ViewportSize change (`BrickUI.onViewport`, `trackStroke`); MenuController
  re-applies the menu scale on a viewport change. Studio switch `workspace TestViewport1x1 = n` (seconds of a fake 1x1).
  - Ruling: not-ready = 1, not 0.52 - why: a 1x1 viewport is not a phone; 1 is the Check-UI baseline and the real
    scale follows on the first ViewportSize change - cost if wrong: a phone shows baseline strokes for a frame or two.
  - Side evidence: the build's old shots show the 1.3x phone menu on PC (`v2/ba_treadmill_tier1.jpg`, left tiles).
- [x] **5** `ServerStorage.StreakTests.CLIENT_SRC` synced with streak_client.lua (section 5 = Rebirth; 11055 chars, same FNV).

### Skipped / deferred
- NICE (skipped, listed): 8 EndsIn @24; 9 OWNED! spanning (10, 384, 720, 60) in the thanks state; 10 hide EndsIn while
  OFFER ENDED shows; 11 the header star's drop shadow / plain gold star.
- MINOR (deferred, not fixed): M-1 price prefetch + retry; M-2 Shop build time unmeasured; M-3 no image preload; M-4 nine
  GetProductInfo caches; M-5 the popup's Open event after unbounded waits; M-6 the leak probe without the Signals tag;
  M-7 a lighter refresh.

### Tests (fix round; every session started from Edit with TestFreshSave read back true, stopped, set false)
- hatch_pure.lua (Edit): **93/93** (82 + 11: HatchFill, HatchHug, setHeight, BrickUI viewport helpers).
- Containment v2.2, every run **0 fails**: S1 top native / 0.7106 / 0.6787 / 1.0982 (2950-2952 checks, textFill 67/67);
  S2 y 0 / 504 / 866 / 1280(=1248) / 1248 native + 0.7106; S3 owned / MAX x 6; S4 tier 1 + held refusals x 4 (MoneyWide
  NEED MORE $!); S5 override 1499 native + 0.6787 SPEED; S6 picker 0 / 1 / 3 / 6 / 8 rows native + 0.7106 (3095-3877);
  P1 native / 0.7106 / 0.6787 / 1.1702 (697); P2 restricted native / 0.7106 / after the live flip (527); P3 last hour,
  refusal held x 2, thanks held; P4 odds 6 / 7 at native / 0.7106 / 0.6787 (715 / 733; 2 / 6 textFill fails before
  the Pct fix); G1 Gift Daily + Playtime native + 0.7106 (1675-2039, the 4 notes above).
- shop_client.lua: open 15, layout 15, prices 22 (+ the 6 pack titles), buys 19, refusal 7, treadmoney 3 (REAL press,
  Money $0 < $10K), override 15/15 on-screen prices, scroll 11, reopen 4, states 7, nosign 2, analytics 4, gift 11,
  pickerfit 32 at native + 32 at 0.7106, canvasguard 2, breaksection 7, toasts got / sent / granted 6 each (a 20-char
  name takes the cut variant at 82 %).
  - Ruling: the override check counts only prices really on screen and not the Starter card's (StarterPackClient's live
    price) - why: at tier 1 the hidden 112 buttons keep `Price.Visible = true` under a hidden holder - cost if wrong: none.
- starter_popup_client.lua: open 31/31, inside 7, buy 7, timer normal 8 + urgent 8, odds 5 / 6 / 7 cells 7 each,
  restricted 20, relayout 18 + 18 (B23), cardpulse 11 (after the fix), thanks 4, owned 5, expiry 3, auto 3.
  - Unverified: session A's first `open` run failed 2 checks: the card's BUY opened the popup and it closed ~0.1 s
    later (CanvasScale caught at 0.935 of the Holder = the close tween). Not reproduced in 4 reruns over 2 sessions; no
    code path closes it on its own; consistent with a click landing on the Backdrop during the run.
- StarterPackTests pure 38/38 + live 33/33; StreakTests pure 24/24 + live 20/20; streak_client 48/48 (fresh session D).
- Gift window unchanged: fresh session B, hatch_gift_snapshot 181-group list FNV **ae122c90** = BEFORE = build AFTER.
  (Session A's run differed only in reward values that scale with progress - Day 2 / 6 cards, Playtime slots 2 / 4 / 8 -
  because it was no longer a fresh save.)
- Perf (`hatch_shop_perf_results.txt`, fix-round section): closed = 0 work (twice); refresh avg 0.091 ms; popup work avg
  0.012 ms; 30 open / close cycles flat (ShopPage 609 / 1117, StarterPackUI 175 / 254, HatchButtons 50, PickerConns 0,
  LuaHeap -17.8 MB).
- Item 7 (`item7_results.txt`, `item7_snapA.txt`): sessions A and B give identical Shop / Rebirth / Index / Settings
  chrome hashes (A = the build's 1.18 AFTER file, line for line) and identical numbers: deviceScale 1.18, Face stroke
  4.13, menu tile stroke 3.07, menu UIScale none, menu right 173.88. Menu 97 / 99 lines equal; the 2 others are the
  Claim "!" badge's pulse (volatile). Forced `TestViewport1x1 = 20`: at t 10.5 s the UI read 1 (menu 1.30, strokes
  2.60 / 3.50, never 0.52); at t 20.9 s all re-applied (menu 1.00, 3.07 / 4.13) and the chrome hashes matched A and B.
- Logs: 0 errors; only the warnings the tests provoke (MUST 11 refusals, TestBreakSection).
- Test files updated: hatch_containment.lua v2.2, shop_client.lua, starter_popup_client.lua, hatch_pure.lua,
  hatch_chrome_snapshot.lua (`_G.HATCH_SNAP_MENU`), item7_proof.lua (new).

### Screenshots `hatch-night-build/popup_shop/v2/`
shop_potions, shop_gift_0_empty / _1 / _3 / _6, popup_restricted, shop_treadmill_tier1, shop_treadmill_max, shop_top,
shop_speed, rebirth_after, index_after, settings_after; before / after pairs `ba_*.jpg` (potions, gift 1 / 3 / 6,
restricted, treadmill tier 1 + MAX, top, speed, rebirth, index, settings).

### End state
Edit; TestFreshSave false; TestShopLegacy nil; TestViewport1x1 nil; TestGiftSelf nil; TestStarterPack true; nothing
published; backups disabled with 0 tags.
