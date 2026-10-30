# Task 7: controller decisions and carries (binding; the brief is the requirements, the spec is the authority)

## The look (owner rules from real incidents: read them as hard rules)
1. **The look is SLINGSHOT's existing Check-UI windows.** The owner approved them as art.
   - Build the NEW trading screens to match: copy the structure and the helpers of the existing windows (MenuController
     pages, `ReplicatedStorage.BrickUI` with `STYLE = "CheckUI"`: `B.header`, `B.closeButton`, `B.restyle`, `B.fonts`,
     `B.palette`, the 3D buttons).
   - Read the skill file first: `C:\Users\ventu\.claude\skills\check-ui-clean-roblox\SKILL.md`. It is THE UI standard
     (owner rule).
   - Look at the Shop, Rebirth, Index and Sell windows in the place before drawing anything.
2. **Never restyle an existing window.** Existing UI changes only for:
   - the Trading tile;
   - the Admin button move (`AdminClient.placeButton`: below the Rebirth and Index tiles; still visible only to the
     whitelisted admins, as today);
   - the modal lock.
   - Back up every existing script first (BUILDER_RULES).
3. **No metric-driven restyles.** Don't add text-floor, contrast or "icon inside the header" fixes that break the
   Check-UI signature. The owner rejected exactly that once ("ON EVERY TAB THIS IS UGLY").
   - The big header icon overlapping the corner, the compact card labels and the white text with a black stroke ARE the
     look.
4. **One layout on every device:** a phone is the PC layout scaled. Never a separate phone arrangement.
   - The window fit rule: cap at about 58 % of the screen width, wider on short phone screens. That is the Shop's fix;
     reuse its fitScale / responsive scale.
   - Tap targets ≥ 42 px at the phone scale.
5. **The Trading tile** is "🤝 Trading" in the left menu tiles. Use an icon from the CheckUIIcons registry that matches
   the other tiles' icon style (search for handshake / trade). Fall back to the 🤝 emoji only if nothing fits, and say
   so in the report.
6. **Screen zones:** the request card sits bottom-right (up to 3 stacked, a 30 s bar each).
   - It must not cover the weather icon row (also bottom-right), the hotbar, the Drop button or the HUD pills. Check what
     is there in the place and stack above it.
   - Toasts shown while a window is open go BELOW the window (y ~0.83).
7. **No notifications, no quest bar.** Sounds come from the SFX library (there is no "Win" sound: use HatchWin / Step).

## Behaviour
8. **The modal lock:** while a trade window is open, nothing else may open over it or close it:
   - MenuController pages and the WindowOpened / CloseWindow events;
   - the PetsEggsUI side panels;
   - the walk-in Sell window (SellClient);
   - the Upgrade stall prompt (it opens the Shop).
   - The trade window closes only through the trade itself (cancel / done). `menu_regression` checks that every
     existing tile, the Admin button and every window still open and close normally when no trade is open.
9. **Respawn:** every death deletes PlayerGui children unless they are ScreenGuis with `ResetOnSpawn = false`. Use
   ResetOnSpawn = false or get-or-create, and rebuild from the Query `"state"` op after a respawn and at start
   (`rebuild_after_respawn`).
10. **Remotes and payloads** are as in `work/task-5-report.md`:
    - the "Remote API" table (exact op names and STRICT types: `respond` = boolean, `ready`/`accept` = the whole `ver`
      from the latest view, `remove` = an index 1..9 into `mine`, `chat` = 1..6);
    - the "Push payload schema";
    - the Done / finished-trade Push kind in `work/task-6-report.md` (Task 6 adds it).
    - Countdowns arrive as seconds LEFT: count them down on the client clock from when the push arrived.
    - Show the refusal reasons as toasts, exactly as sent.
11. **What can be offered** comes from `work/task-3-report.md` (which pets: base + hotbar Tools, unplaced eggs;
    equipped / placed rules). Egg refs send the exact `kg` from the client's own EggInventory.
12. **Players list rows:**
    - a headshot (`rbxthumb://type=AvatarHeadShot&id=<uid>&w=150&h=150`), @name, and ONLINE / AWAY;
    - SEND, greyed with the reason when you can't trade (the list's `why`, and AWAY rows);
    - Invite Friends = `SocialService:PromptGameInvite` (guarded with pcall + `CanSendGameInviteAsync`).
    - History tab = the `history` op entries.
13. **The phrases** come from `TradeConfig.PHRASES`, in that order (Add More, L Trade, Last Offer, Deal?, Fair Trade, No
    Thanks). Never re-typed.

## Process (rulings in the ledger)
14. **Mockups = the REAL TradeClient screens.**
    - Render them in a Play session from FAKE view payloads, through a preview entry point that only works in Studio
      (`RunService:IsStudio()`) and is driven from your test code.
    - Capture every screen with `screen_capture` into `docs/plans/2026-10-29-trading/ui/`:
      - the Trading menu: Players and History;
      - the request card stack;
      - Phase 1, empty and full (9 + 9);
      - Phase 2 with "Securing items..." and with ACCEPT counting down;
      - Done;
      - a toast.
    - In the same Play session, capture 3 EXISTING windows as the look reference for the reviewer: the Shop, the
      Rebirth page and the Index. Save them as `ui/ref_shop.png`, `ui/ref_rebirth.png` and `ui/ref_index.png`.
    - Then STOP and report. The controller has each screen reviewed (it must score ≥ 8.5). Only after that do you wire
      the screens to the live remotes and finish the tests.
15. **Phone sizes:** measure the text and tap-target sizes at the phone scale in code (AbsoluteSize × the scale a
    733×392 viewport would give) and list them in the report. The controller does the real Device-emulator pass with
    computer-use afterwards.
16. **Tests:** `menu_regression`, `trade_window_modal`, `rebuild_after_respawn`, `request_card_stack`. RED first, then
    GREEN. The TestFreshSave rule applies to every Play.

## Carries from Task 6
17. After BACK or a cancelled Phase 2, the escrowed items are out of the inventory for about 1 s while they come back.
    Show them as "Returning items...", never as missing.
18. **The finished-trade Push:** the "Done Push" section of `work/task-6-report.md` is the exact schema. The Done
    screen shows "Trade complete!" with what you gave and what you got. A cancel shows its reason as a toast and closes
    the window.
19. **READY can now refuse with "Wait Ns"** (each player gets at most 6 Phase 2 entries per 5 min). Show it like every
    other refusal: a toast. If the view carries the seconds, add a countdown on READY too.
20. **"Your last trade is still finishing"** (an older escrow is still settling) is a normal refusal. Show it as a
    toast.
