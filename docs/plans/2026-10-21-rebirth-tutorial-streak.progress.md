# SDD ledger — plan: Desktop/SLINGSHOT Creatures/docs/plans/2026-10-21-rebirth-tutorial-streak.md

Setup: Ruling: no git worktree / sdd scripts — Studio is the source of truth and the git root is the home folder (plan Global Constraints); this file is the ledger, backups in ServerStorage._Backup_RebirthStreak.Before are the "commits" — cost if wrong: none (no git history to lose).

Pre-flight (shared interfaces):
- T1 -> T2: requirement(r) may be nil; T2 canRebirth/banner use petMeets(nil)=true + cost(r). Consistent.
- T1 -> T3: cost(0)=25000 drives step-11 copy "Earn $25K". Consistent.
- T2 -> T3: RebirthPage attr Confirming, TestPress, TileArrow/TutorialArrow; T3 client checks use TestPress. Consistent.
- T4 -> T5: attributes StreakToday/Claimable/Next/Lost/Through/Area/Pet/Egg + RS.Streak.Claim + StreakConfig fields. Consistent.
- T4 -> T5: StreakDebug "set"/"claim" used by T5 step 6. Consistent.
Task 1: Ruling: plan's "require(module:Clone())" fails for modules that use script.Parent (RebirthConfig needs CreatureConfig) — tests use T.fresh(): clone parented next to the original as <Name>_TestCopy, required, destroyed — cost if wrong: none (test helper only).
Task 1: Ruling: sim Expected "v6 R2 run <= v5 R2 run" missed (13.0 m vs 12.5 m at $1.2M; 12.7 m even at $1.1M) — the R2 run is dominated by hunting the first Water pet (moved from R1 to R2), not by price, so kept the spec's $1.2M — cost if wrong: R2 ~30 s slower than v5 in the model; total to R2 still 0.4 h.
Task 1: complete (RebirthV6Tests.pure 45/45 RED(23 fail)->GREEN; live 5/5 RED(RebirthDebug missing)->GREEN; client R0 page: NeedPet hidden, NeedMoney x0.5, no RebirthClient errors; sim R10 5.0 h, R20 96.4 h)
Task 2: Ruling: TileArrow sits UNDER the Rebirth tile pointing up (plan: right of the tile pointing left) — the menu is 2 tiles wide, so "right of Rebirth" covered the Index tile (screenshot tilearrow) — cost if wrong: a position tweak.
Task 2: Ruling: page TutorialArrow points LEFT at the REBIRTH button from its right, size 0.1 (plan: over the button) — over the button it covered the money bar text (screenshot pagearrow) — cost if wrong: a position tweak.
Task 2: Ruling: spec "the tile glows too" = the existing pulsing green "!" badge + the bobbing arrow; no extra glow layer (the tile Face already has its Check-UI UIStroke, a second stroke wouldn't render) — cost if wrong: one small visual addition.
Task 2: Ruling: client checks set attributes LOCALLY on the LocalPlayer (only this client's UI sees them) instead of server+client round trips; kept in docs/plans/tests-2026-10-21/rebirth_client.lua — cost if wrong: none (UI-only logic).
Task 2: complete (client checks RED "RebirthReadyUI not found" -> GREEN 11/11, then after the arrow moves 10/10 incl. R3-level banner sub x1.75, Confirming via TestPress; screenshots banner2, tilearrow2, pagearrow2)
Task 3: Ruling: the tutorial text normally slides off-screen while ANY menu window is open; in step 11 it now stays up while the Rebirth page is open (above the window) — otherwise "Press REBIRTH!" / "Tap AGAIN to confirm!" from the plan's copy table could never be seen — cost if wrong: the pips row touches the window's top edge (see minor below).
Task 3: Ruling: step 11 shows the "Earn" state whenever money < cost, even with the Rebirth page open (plan's table only listed page states for "ready") — cost if wrong: none.
Task 3: minor (deferred): with the Rebirth page open in step 11 the tutorial's pip row overlaps the window's top edge/icon by a few px at 1519x753 (screenshot step11_confirm).
Task 3: complete (TutorialV11Tests.live RED 2/11 -> GREEN 13/13, re-run 13/13 after the client work; client states Earn $25K / $1K / $25K + 11 pips, REBIRTH is READY! + TileArrow, Press REBIRTH! + page arrow, Tap AGAIN to confirm!, real rebirth via TestPress x2 -> TUTORIAL COMPLETE + reward row + Next: reach the WATER area!, window closed, Potion_Money 1; fresh TestTutorial run: step 1 "Walk to the SLINGSHOT!" with 11 pips)
Task 4: Ruling: wrote StreakTests.live BEFORE StreakServer/GiveEgg (plan order had implement step 6 before the live test in step 7) — TDD needs the RED first — cost if wrong: none.
Task 4: complete (StreakTests.pure RED "StreakConfig not found" -> GREEN 24/24; StreakTests.live RED "StreakServer not running" -> GREEN 20/20 incl. rollover, same-day refusal, egg_full + pet_full keep the day, Day 4 egg at EGG_KG, missed-day reset, Day 7 secret at SECRET_KG + 5/5/5 potions + 2 h cash, new week; AnalyticsDebug prints "[Analytics] funnel Daily Streak 1 Day 1"; console: no StreakServer warnings)
Task 5: Ruling: locked cards read "LOCKED" (plan: "DAY n") — the SPEC says CLAIM / CLAIMED / LOCKED ("Tomorrow" on the next card); test updated — cost if wrong: one string.
Task 5: Ruling: Day 2 copy is 2 lines ("+1 Hatch & Speed Potion", "+X Speed") and Day 5 "+3 of EVERY" / "POTION!" (plan listed 3 / 1 lines) — the 0.235-wide cards only fit 2 readable lines — cost if wrong: copy tweak.
Task 5: Ruling: the Day 7 card's lock cover is lighter (0.72 vs 0.45) so the rainbow + secret pet stay bright while locked (spec: hero card) — cost if wrong: none.
Task 5: Ruling: cards are taller (0.425, rows at 0.11/0.565) than the plan's 0.4 — the second reward line hid behind the button (screenshot daily1) — cost if wrong: none.
Task 5: Ruling: Studio-only DailyView.Card<d>.TestPress BindableEvent (same pattern as RebirthPage.TestPress) so tests press the real button handler — cost if wrong: none (Studio only).
Task 5: PENDING (owner): phone screenshot — needs the owner to switch Studio's device emulator to a phone (I may not click Studio dialogs).
Task 5: complete (client checks RED "Tabs not found / no auto-open" -> GREEN 7/7 + 7/7, final run 14/14 incl. TestPress claim toast, countdown, reopen picks PLAYTIME; Day 3 + Day 7 visuals and StreakCelebrate (pet portrait + "Thornblade Mantis 15K KG + 5 of every potion + $72K"); console clean; screenshots daily2, daily_claimed, playtime_tab, daily_day3, day7_celebrate)
Task 6: Ruling: no export to docs/plans/review-2026-10-21 — the reviewer (general-purpose agent, Haiku per the owner's reviewer rule) reads the scripts straight from Studio with read-only tools (script_read/grep), told never to execute or edit — cost if wrong: none (same sources, no stale copies).
Final review: general-purpose agent (Haiku, owner's reviewer rule), read-only from Studio — 1 Important + 8 Minor.
Final: fixed tutorial card not re-syncing on RebirthPage.Visible / TutorialExtra (Shop -> Rebirth hid "Press REBIRTH!", Rebirth -> Gift left it over the window) — client check shop/rebirth/gift guide Y RED(-0.3 on Rebirth) -> GREEN(-0.3 / 0.015 / -0.3).
Final: fixed (re-graded Minor -> Important: new players finish the tutorial 10+ min in, so they would NEVER get the Day 1 auto-open) StreakClient auto-open gave up after 120 s — tutorial-blocked 130 s check RED("never") -> GREEN("opened", tab Daily).
Final: fixed (re-graded Minor -> Important: returners get Welcome Back on almost every join, the banner fired hidden under it and was used up) REBIRTH READY banner ignored OfflineUI / UpgradeUI — Welcome Back check RED(shown during) -> GREEN(hidden during, shown after close).
Final: suite after the fix pass: RebirthV6 pure 45/45 + live 5/5, TutorialV11 live 13/13, Streak pure 24/24 + live 20/20, streak client 14/14, rebirth client 13/13, step-11 end-to-end (READY -> Press -> Tap AGAIN -> TUTORIAL COMPLETE).
Final: Ruling: banner sub says "x1.25 MONEY & SPEED" (spec: "x1.25 MONEY") — a rebirth multiplies both, so the longer line is the true one — cost if wrong: one string.
Final: Ruling: reviewer #7 (active tab keeps a silver bevel) — not a defect: BrickUI's followColour/paintFace recolours the Depth bevel with the face (screenshot daily2 shows the lime tab's dark-lime bevel) — cost if wrong: a bevel colour.
Final: minor (deferred): StreakServer claim — GivePet/GiveEgg/GivePotion/Analytics calls not wrapped in one pcall; a throwing BindableFunction would leave busy[player] set for the session (no throw path found).
Final: minor (deferred): TutorialServer.done() sets stage 0 before GivePotion and ignores its result — a failed give loses the step-11 potion silently.
Final: minor (deferred): RebirthClient runs canRebirth() (2 JSON decodes) every frame while TutorialExtra == 3 and no window is open.
Final: minor (deferred): steps 8-11 aren't sent as tutorial steps to the Onboarding funnel (pre-existing for 8-10; "First Rebirth" is still logged as onboarding step 13).
Final: minor (deferred): auto-open never re-fires after a mid-session UTC midnight (badge + tab dot still light).
Cleanup: TestFreshSave=false, TestTutorial=false, AnalyticsDebug=nil, StreakDayOffset=nil, IncomingReplicationLag=0; 10 backups in ServerStorage._Backup_RebirthStreak.Before, all disabled, 0 tags.
