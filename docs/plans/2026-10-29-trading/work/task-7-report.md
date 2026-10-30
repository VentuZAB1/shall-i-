# Task 7 report, PART 1: the real TradeClient screens from fake payloads + screenshots (review gate next)

**Status: DONE_WITH_CONCERNS (part 1 only).** Every screen in the dispatch list is built in the real
`TradeClient`, drawn from fake view payloads through a Studio-only preview entry point, and captured into `ui/`
(16 screen files + the 3 reference windows). The Trading tile and the Admin button move are in, and their backups were
already in place. The screens are **not wired to the live remotes yet**. `act` / `respond` are no-ops, and the 4 named UI
tests and the modal lock come in part 2, after the review gate. The concerns are below: Phase 2 row text is small on a
phone, there were no owner reference shots for the trade window, and one deviation from the CheckUIIcons-first rule.

Builder: Opus, 2026-10-30. Studio `3bf21205-caff-490e-a927-3bd9f0097311`.
- **Play sessions:** I started and stopped every one myself (11), and checked `TestFreshSave == true` in Edit right
  before each. TestFreshSave is left `true`. Studio is in Edit, with no Play running.
- **Save / publish:** never. No server trade script was touched.
- **Studio rules:** I never used the command bar or a dialog, and never set CameraType.
- **Leftovers:** the preview copies in ReplicatedStorage (`TradeUIPreview`, `_TradeFake`) were made inside Play
  sessions only. None of them exists in Edit (checked).

## Scripts
| Path | Change | Backup |
|---|---|---|
| `StarterPlayer.StarterPlayerScripts.TradeClient` (LocalScript, **new**) | 61,864 chars, 1,409 lines. Every trading screen: Trade page, request cards, trade window (Phase 1 / Phase 2 / Done / Returning), toasts, plus `script.TradePreview` (Studio only) | n/a (new) |
| `StarterGui.MainMenu.MenuController` | +1,758 chars: the Trading tile (a clone of the Index tile, made at runtime, only when `TradeConfig.ENABLED`), page id `Trade` (PAGES, HEADER_THEME "Amber", title "Trading"), `CHROME.Trade = CHROME.Index`, LAYOUT `Trade` = the Index window, and `wideOnPhone` (the Index's phone "size B" also for Trade). Nothing else was touched | `ServerStorage._Backup_Trading.Before.MenuController` (Task 0; I checked it byte-identical to the pre-edit source, Enabled = false, 0 tags) |
| `ServerStorage.AdminUI.AdminClient` | +1,294 chars: `placeButton` only (and the header comment). The button keeps its look and its admin-only copy path (AdminServer gives the ScreenGui to admins only) | `ServerStorage._Backup_Trading.Before.AdminClient` (Task 0; byte-identical check, Enabled = false, 0 tags) |
| `ServerStorage.TradeUIPreview` (ModuleScript, **new**) | the FAKE payloads (inventory, views, chat, rows, history, done) in the exact Task 5/6 push shapes. Studio test data only; nothing live requires it | n/a (new) |

No CollectionService tags on any of them. SellClient, PetsEggsUI and the Upgrade prompt are untouched (the modal lock
is part 2).

### The preview entry point (decision 14)
`player.PlayerScripts.TradeClient.TradePreview:Invoke(op, data)` exists only when `RunService:IsStudio()`. It draws
through the SAME functions the live pushes will use (`renderTrade`, `renderDone`, `addRequest`, `removeRequest`,
`showToast`, `renderMenu`). The ops are:
- `inventory` {pets, eggs}
- `tab` "Pets"/"Eggs"
- `trade` view
- `done` push
- `request` push
- `requestGone` {id}
- `toast` {text, error?}
- `returning` seconds
- `menu` {tab, rows, why, history, search, note}
- `freeze` bool: holds the countdowns still for a screenshot
- `close`
- `measure`: the phone-size numbers below, as JSON

How to drive it, in a Play session (TestFreshSave):
- Server: `game.ServerStorage.TradeUIPreview:Clone().Parent = game.ReplicatedStorage`
- Client: `local F = require(game.ReplicatedStorage.TradeUIPreview)`, then
  `TradePreview:Invoke("trade", F.view({mine = F.mineFull, theirs = F.theirsFull, readyIn = 2.9, chat = F.chat()}))`

## Screen files (`docs/plans/2026-10-29-trading/ui/`, 1519 x 753 Studio Play captures)
| File | What |
|---|---|
| `00_hud_trading_tile_admin.png` | the HUD: the Trading tile (row 3 under Rebirth) and the ADMIN button moved below Rebirth + Index |
| `01_menu_players.png` | Trading menu, PLAYERS tab: search, 2 ONLINE rows (SEND lime) + 2 AWAY rows (SEND greyed "AWAY"), INVITE FRIENDS |
| `02_menu_players_send_greyed_reason.png` | the same with the list's `why` ("Finish the tutorial first"): every SEND greyed, the reason line in red |
| `03_menu_history.png` | HISTORY tab: @name, "2 h ago", GAVE / GOT small item cards, "+3" overflow, "nothing" |
| `04_request_card_1.png` | 1 request card, bottom-right above the weather / boost icon row: headshot, @name, "wants to trade!", ACCEPT / DECLINE, 30 s bar |
| `05_request_cards_3_stacked.png` | 3 cards, newest on top, each with its own bar (29 / 19 / 9 s left), left of the Eggs/Pets/Potions tiles |
| `06_phase1_empty.png` | Phase 1, empty offers: your PETS (inventory), 0/9 + 0/9, $0/s, READY, CANCEL, the chat hint, the 6 phrases, the trade timer |
| `07_phase1_full_9x9_ready_countdown.png` | Phase 1, 9 + 9 with mutations (UFO / METEOR / METEOR+1), totals, offered items ticked in your inventory, READY locked (lock icon) + "2.9s Left", "syncing...", 5 chat lines |
| `08_phase1_you_ready_eggs_tab.png` | extra: EGGS tab, you pressed READY (READY! ribbon, silver button, "Waiting for @builderman...") |
| `09_phase2_securing_items.png` | Phase 2, 9 + 9 read-only rows (picture, name, mutation in words or "None", the exact KG like 152,340.5 KG, $/s), "You give 5 pets + 4 eggs - You get 6 pets + 3 eggs -$38.3M/s", ACCEPT = "Securing items..." (locked), BACK |
| `10_phase2_accept_countdown.png` | Phase 2, both secured: "ACCEPT (2.9s)" locked |
| `11_phase2_waiting_for_B.png` | Phase 2 after you accepted: ACCEPTED ribbon, "Waiting for @builderman..." |
| `12_returning_items_after_back_with_toast.png` | after BACK: both offers empty, "Returning items..." over your inventory, READY "4.2s Left", toast "@builderman went back - add your items again" under the window |
| `13_done_trade_complete.png` | Done: "Trade complete!" (gold gradient, turning sunburst), YOU GAVE / YOU GOT cards, OK |
| `14_toast_refusal_under_window.png` | a refusal toast ("Max 9 items", red) below the open window |
| `15_toast_no_window.png` | a toast with no window ("@builderman declined", gold, y 0.83 like GiftToast) |
| `ref_shop.png`, `ref_rebirth.png`, `ref_index.png` | the 3 existing windows, captured in the same session (the look reference) |

Fake data: names are public Roblox test accounts (builderman 156, Shedletsky 261, Roblox 1). The two AWAY rows use
uid 2 / 3 ("John_Doe" / "Jane_Doe"), so their headshots are real but generic.

## Which BrickUI / Check-UI helpers each screen uses
- **Trading tile:** a clone of the Studio-built Index tile, restyled by MenuController's existing `B.restyle` pass (it
  gets `CUIGradient`, `B.damier`, `B.innerHighlight` and the pink palette from `B.palette`). Clicks go through the
  existing `hookBrick`, and it opens through the existing `openWindow`.
- **Admin button:** unchanged (AdminClient's `button()` = `B.brick` amber). In the tile row its label box is 0.86 x
  0.3, because a square box made TextScaled wrap "ADMIN".
- **Trade page (menu):**
  - window chrome: MenuController's (`B.setHeaderTheme(header, "Amber")`, `B.closeButton`, the Index's slim CHROME);
  - tabs PLAYERS / HISTORY and SEND / INVITE FRIENDS: `B.brick` 3D buttons (lime / silver / off / cyan);
  - player rows: the Settings-row recipe (`B.corner`, `B.pxStroke`, `B.damier`, `B.innerHighlight`);
  - text and images: `B.text` / `B.image`;
  - search box: AdminClient's text-field style (`B.RECESS`, highlight stroke).
- **Request card:**
  - the card: `B.brick` with `role = "window"` (slate canvas + #181E22 border);
  - ACCEPT / DECLINE: `B.brick` lime / red;
  - the 30 s bar: the skill's progress-bar colours (§3.3 trough, orange-to-gold fill);
  - headshot ring: `B.corner` 0.5 + `B.pxStroke`.
- **Trade window:**
  - frame and chrome: `B.brick` window (slate #3B5866, 3.5 px #181E22), `B.header(..., "Amber")` with the big icon
    over the corner (the Check-UI signature), `B.closeButton`;
  - panels: recessed `B.CARD` + `B.CARD_HIGHLIGHT` (MenuController's Body card);
  - buttons: every one is `B.brick` (READY / ACCEPT / OK lime, CANCEL red, BACK amber, phrases cyan, tabs lime / silver,
    strips cyan / purple / amber);
  - item cards: the same brick recipe (bevel + gradient + `B.damier` + `B.innerHighlight`) tinted by area like the
    Index (secret gold, mythic rainbow);
  - the READY! / ACCEPTED ribbon: the Day 7 "SECRET!" ribbon idea;
  - Done: `B.SUNBURST` turning at 20 deg/s, and the title in the Day 7 "SECRET PET!" gold gradient.
- **Toasts:** `B.text` like GiftToast (gold; red for refusals).
- All text is GothamBlack with a black outline (`B.text`). Every button is centre-anchored with a ButtonScale pop
  (1.05 / 0.94).

## The tile icon
**CheckUIIcons Main/Trade "Trade 1st Outline", `rbxassetid://91526512763195`.** It's the green-and-orange two-arrow swap,
with the thick dark outline the other tiles' icons have. I compared all four Trade variants and the Friend icons
side by side on the slate background in Play: "1st Outline" matches the tiles best (the plain "1st" has no outline).
No emoji fallback was needed. The same id is the trade window's header icon and the Trade page icon.

The other icons are all "_Outline" variants:
- Magnifying Glass `113888173779365` (search);
- Chat `119814753932933`;
- Clock `77081812380832` (the trade timer);
- Add Player `73659702190059` (INVITE FRIENDS);
- Lock `99673707827333` (READY / ACCEPT while locked);
- plus the game's own Check / Paw / Egg / Money icons.

**Deviation from the vault rule:** the vault's Icons note says the owner's icon pack is the first choice, and that pack
has a `Trade.png` (`Downloads\Verctor-...\Verctor\Trade.png`, never uploaded). I followed decision 5 (CheckUIIcons)
instead. If the owner prefers the pack's look, uploading `Trade.png` and swapping one id (`TRADE_ICON` in
MenuController and in TradeClient) is a 2-line change.

## Phone sizes at 733 x 392 (decision 15)
**Method.** Measured in code (`TradePreview:Invoke("measure")`). Every visible label's `TextBounds.Y` and every
button's `AbsoluteSize` on the 1519 x 753 Play screen, times the ratio that screen has to a 733 x 392 phone. It's
computed for both top-bar heights (58 px, and 36 px on older clients).

**The scales:**
- trade window: 0.538 / 0.574 of its 1060 x 576 design px (PC 1080p: 1.05);
- Trade page: the Index's phone size B (ratio 0.554 / 0.594 to this screen);
- request cards: deviceScale x 1.3 on phones.

This is an approximation: TextScaled rounds to whole sizes. The controller's Device-emulator pass is the real check.

**Tap targets (phone px, 58 px top bar; the 36 px bar is 2-4 px bigger). All >= 42.**
| Screen | Element | Size |
|---|---|---|
| Trade window | [X] | 46 x 46 (invisible hit area; the visible X stays the Check-UI 54 design px = 29 px) |
| | PETS / EGGS tabs | 69 x 42 |
| | inventory item | 46 x 46 (hit area = card + its gap) |
| | offer card (remove) | 46 x 47 |
| | READY / CANCEL | 140 x 42 |
| | the 6 phrases | 49 x 42 |
| | ACCEPT / BACK | 218 x 42 |
| | OK (Done) | 140 x 42 |
| Request card | ACCEPT / DECLINE | 74 x 42 |
| Trade page | PLAYERS / HISTORY | 102 x 42 |
| | SEND / AWAY | 99 x 42 |
| | INVITE FRIENDS | 142 x 42 |

**Text heights (phone px, 58 px bar / 36 px bar).**
| Screen | Smallest | Labels under 9 px | Which |
|---|---|---|---|
| Trade page, Players | 12.2 / 13.1 | 0 | names 20.5, SEND 21.6, ONLINE / AWAY 13.9, INVITE FRIENDS 12.2 |
| Trade page, History | 12.2 / 13.1 | 0 | names 20.5, GAVE / GOT 14-15, "2 h ago" 12.7, "+3" 13.9 (the mini cards carry no mutation tag, see ruling 11) |
| Request card | 15.6 / 15.6 | 0 | |
| Phase 1, full 9 + 9 | 5.8 / 6.2 | 45 of 100 / 30 of 100 | the compact card labels: KG 6.5-8.4, mutation tag 7.1, "METEOR+1" 5.8, $/s 8.4 (>= 9 with the 36 px bar), chat lines 7.8-8.4. Buttons, titles, totals and the countdown are all >= 10 |
| Phase 2, full 9 + 9 | 6.5 / 6.9 | 67 of 87 / 18 of 87 | the read-only rows: names 6.5-8.4 (the longest, "Black Eastern Dragon", 6.5), exact KG 8.4, $/s 6.5-8.4, mutation words 7.8-8.4. The summary line, ACCEPT / BACK and the totals are >= 10 |
| Done | 7.8 / 8.3 | 2 | the 2 card mutation tags |

Per decision 3, I added no text floors (the compact card labels are the Check-UI look, as on the Index / Sell cards).
The Phase 2 numbers are concern 1.

## Rulings I made (please confirm at the gate)
1. **Tile and Admin placement.**
   - The Trading tile is a 5th tile in a third row, in Rebirth's column (the menu's 2-column grid kept).
   - The ADMIN button sits in the free right spot of that row, tile-sized: below Rebirth + Index, admins only, as before.
   - Why not a wide bar under 3 rows: it would reach toward the money / speed pills on short screens.
   - With the kill switch off (no tile), the old wide bar goes under the Rebirth / Index row.
   - The tile is pink (the Check-UI "feature" palette), so it differs from the 4 existing tiles and the amber ADMIN.
2. **The Trade menu is a MenuController page** (`Body.TradePage`, page id `Trade`, the Trading tile).
   - It reuses the Index's window, its slim chrome and its phone size B, so it is one window at a time, with the 58 % cap
     and the wider-on-phones rule for free.
   - Header theme: Amber.
3. **The trade window is its own ScreenGui `TradeUI`** (DisplayOrder 25, ResetOnSpawn = false), not a menu page: it's
   modal and must survive respawns.
   - Fit: the window fit rule. 58 % of the width on a PC; on a short phone screen (viewport Y < 520) 97 % of the width,
     with the full height; always centred.
   - Opening it fires MainMenu `CloseWindow` + `WindowOpened` (the Sell / Admin / side panels close) and hides the
     hotbar. The full modal lock is part 2.
4. **Request cards** (`TradeRequests` ScreenGui):
   - Anchored on `PlayerGui.WeatherTiles.Row`: their bottom is 8 px above the row's top, their right edge is the row's
     right edge.
   - When the stack would overlap the right-hand Eggs / Pets / Potions tiles, it moves left of them.
   - Size: x0.85 deviceScale on PC, x1.3 on phones.
   - They never reach the hotbar, the Drop button or the bottom-left pills.
5. **Toasts** (`TradeToast` ScreenGui, DisplayOrder 31):
   - with no window: y 0.83, like GiftToast;
   - with the trade window open: centred in the space under it, or over its bottom edge when there's no room (phones);
   - refusals red, everything else gold.
6. **The exact KG** is the shortest decimal that reads back as the same number (else `%.17g`), with thousands commas
   ("152,340.5 KG").
   - Phase 2 mutation words: "UFO + METEOR" in their colours, or "None".
   - Small cards show the first mutation + "+N" ("METEOR+1"), so two tags never overlap.
7. **"Returning items..."** covers your inventory for up to 3 s after a view goes from confirm / commit back to select.
   It clears 0.3 s after your PetInventory / EggInventory / BaseData attribute changes (the items are back). The offers
   show empty (BACK empties them); nothing is shown as missing.
8. **The window's [X]** = CANCEL during a trade (spec 3: "Closing the window [X] or CANCEL ends the trade"). On Done it
   just closes, like OK.
9. **The button states:**
   - READY:
     - locked: off colour, lock icon, "2.9s Left" under it;
     - ready: lime;
     - pressed: silver "READY!", plus "Waiting for @B..." under it.
   - Under CANCEL: "syncing..." (`view.syncing`) or "@B is ready!".
   - ACCEPT:
     - "Securing items..." while either side's `secured` is false;
     - then "ACCEPT (2.9s)" while locked;
     - then "ACCEPT";
     - after you press: "Waiting for @B...";
     - in phase commit: "Completing...".
   - The chat phrases grey out outside select / confirm.
10. **Invisible tap areas** (`Hit` TextButtons) on the window's [X] (1.6x) and on item cards (1.08x). They reach 42 px
    on phones without making the Check-UI art bigger.
11. **History mini cards show only the picture.** A mutation tag there would be about 4 px on a phone. The History row
    is a summary, and the exact items are in the trade itself.
12. **The countdowns** count down from the push's seconds-left on the client clock (`os.clock()` minus the arrival
    time). The `freeze` preview op holds them still for screenshots; it exists in Studio only.

## Things I could not match / concerns
1. **Phase 2 row text on a phone is small:** 6.5-8.4 px at 733 x 392 with the 58 px bar.
   - This is the anti-scam view (exact KG, mutation words).
   - On a PC it's 11-14 px, and with the 36 px bar most rows reach 9 px or more.
   - Following decision 3, I didn't add a text floor.
   - If the reviewer or the emulator pass says it's too small, the cheapest in-layout fix is to give the rows the chat
     column's width in Phase 2 (hide the chat while confirming), which makes the rows about 25 % bigger. The spec keeps
     chat in Phase 2, so I didn't.
2. **No owner reference screenshots.** The spec says the trade window is "built from the owner's screenshots", but I
   found none in `docs/`, so I built it from the spec text. The arrangement is the spec's: inventory left, offers centre,
   chat right.
3. **The icon pack vs CheckUIIcons** for the tile icon (see "The tile icon").
4. **Part 1 is not wired.**
   - `act()` / `respond()` are empty functions.
   - The Trade page shows nothing in a live session until part 2 calls `list`.
   - There are no Query `state` rebuilds yet, and no modal-lock changes in MenuController / PetsEggsUI / SellClient /
     the Upgrade prompt yet.
   - Don't publish between part 1 and part 2. The tile would open an empty page.
5. **Studio's capture viewport is 1519 x 753** (wider than 16:9). On a 1920 x 1080 player screen the trade window is
   1.05x its design size (1114 x 636 px, 58 % wide), and the Trade page is the Index window.
6. **The request card reads "@A" + "wants to trade!"** on two lines (the spec's "@A wants to trade"), to keep the name
   big at card size.

## Part 2 (after the gate)
Wire the remotes (Request / Action / Query / Push) to these same render functions:
- the toasts carry the server's reasons exactly as sent;
- Query `state` at start and after a respawn;
- `list` / `search` / `history`;
- SEND / respond / outgoing.

Then the modal lock (MenuController pages + WindowOpened / CloseWindow, PetsEggsUI panels, SellClient, the Upgrade
prompt; backups first), the 4 named tests RED then GREEN (`menu_regression`, `trade_window_modal`,
`rebuild_after_respawn`, `request_card_stack`) and the final screenshots.

---

# UI fix round 1 (2026-10-30)

**Status: DONE_WITH_CONCERNS (still part 1, no live wiring).** Every fix in `task-7-ui-review-1.md` "Fixes for screens
under 8.5" is applied, as the controller's rulings set them. Every screen was captured again under the same file name;
the 3 refs are unchanged. Phase 2 phone text is still under 9 px (concern 1).

- Only `StarterPlayer.StarterPlayerScripts.TradeClient` changed: 73,454 chars, 1,667 lines.
- Not touched: MenuController, AdminClient, `TradeUIPreview` and the server scripts. No new backups were needed
  (TradeClient is new).
- **Play sessions:** I started and stopped every one myself (7 this round), and checked `TestFreshSave == true` in Edit
  right before each. It's left `true`.
- **Save / publish:** never.
- **Leftovers:** none in Edit. The preview copies and the 2 stand-in boost icons existed only inside Play sessions.

## Housekeeping: the Luau local limit
The new pieces pushed the script past Luau's 200-locals-per-function limit ("Out of local registers"), so I
restructured it without changing any behaviour:
- the icon ids moved into one `ICON` table, and the Phase 2 numbers into `R2`;
- the Trade page, the messages and the request cards are each built inside their own function;
- a few build-only locals are now scoped.

It is at 189 top-level locals now. `loadstring` compiles it clean, and every Play session logged no errors.

## What changed, per screen
| Screen | Review item | Change |
|---|---|---|
| 02 | 1 | The reason line ("Finish the tutorial first") is now directly above the list, full width, in the same red. The list starts under it. The footer holds INVITE FRIENDS only. |
| 02 | 2 | Every greyed SEND has the padlock (`99673707827333`, the same as READY / ACCEPT) and keeps the word SEND. AWAY rows still read "AWAY" with no lock. |
| 02 | 3 | No per-button reason words (controller ruling). |
| 06 | 1 | While both offers are empty: "Tap a pet or egg on the left to offer it." centred over Your Offer, white GothamBlack, the size of "2.9s Left". It hides once anything is offered. |
| 06 | 2 | The timer pill reads "Ends in 2:59". It shows whichever of the idle 3 min / total 10 min ends first (the view's `endsIn`), so "Ends in" is the true caption, not "Idle". |
| 06 | 3 | REJECTED by the controller: 3 columns everywhere. |
| 07 | 1-2 | The in-offer tick is now a 24-design-px green check on the card's top-right corner (the grid got top padding for it). Only the picture dims. KG, mutation and $/s stay full brightness. |
| 07 | 3 | "syncing..." is now white with a black stroke, the same style as "2.9s Left". |
| 08 | 1 | Pressed READY stays silver with the lime check. "Waiting for @builderman..." is now in the gold state style (like "2.9s Left"). |
| 08 | 2 | READY! / ACCEPTED ribbons sit fully inside the panel's coloured strip, unrotated, at its right end. The title shortens while a ribbon shows. |
| 09 | 1 | Phase 2 rows are fixed columns (420 design px row): picture 36, name 140, mutation 60 (wraps "METEOR + UFO" to 2 lines), KG 92 right-aligned, an 8 px gutter, then $/s 58 left-aligned. |
| 09 | 2 | One text size per column, set by its longest entry on either side (`fitRows2`, measured with TextService). Every name is the same size; the numbers keep their own columns. |
| 09 | 3 | Rows are 44 design px (36 px at this screen, 46 px at 1080p). Six show per side and the list scrolls (ScrollingFrame + UIListLayout). Pictures 36 design px (30 px here). |
| 09 | 4 | Summary: "You give 5 pets + 4 eggs  \|  You get 6 pets + 3 eggs  \|  Net -$38.3M/s". The separators are grey "\|", and the net is red / lime. |
| 09 | 5 | ACCEPT is about 70 % of the row (618 of 890 design px), BACK about 30 % (262). Colours kept. |
| 09 | 6 | Phase 2 chat is ONE column: 6 phrases in a 132 design px panel (`Chat2`). The two lists grew from 405 to 440 px each. Every device gets the same layout. |
| 09 | 6, note | No log fits next to six 42 px phone taps. A NEW chat line in Phase 2 shows for 4 s as a bubble (slate plate, amber stroke, chat icon) on the speaker's list: "@Santrinio: Deal?" in 11. |
| 10 | 1-3 | Covered by 09. "ACCEPT (2.9s)" stays locked with its padlock. |
| 11 | 1 | Covered by 09-5. |
| 11 | 2 | ACCEPT is wider now, so "Waiting for @builderman..." no longer touches its edge. |
| 12 | 1 | "Add them again when they're back" is on its own lines under the title, white, at the size of "4.2s Left" (cap = 24 design px, the 30 px box's size). |
| 12 | 2 | The toast below the window stays plate-less: see 15 / G4. |
| 13 | 1 | Panel headers carry their totals ("YOU GAVE $79.9M/s", "YOU GOT $37.8M/s"). "Net -$42.1M/s" sits above OK, red if negative, lime if positive. |
| 13 | 2 | No dead space: cards start 10 px under the strip. Both panels are as tall as the bigger side's card rows. OK sits right under the net line, and the whole block is centred. |
| 13 | 3 | Sunburst and gold title kept. |
| 14 | 1-2 | Offer refusals (`showToast(text, color, "offer")`, used for add / remove in part 2) show at the bottom edge of Your Offer, over its total row, on a dark slate plate (`B.RECESS`) with a 2 px red stroke. Red text, the server's words exactly. |
| 15 / G4 | | I checked the game's existing toasts: GiftToast (ShopClientLegacy), InventoryToast (InventoryClient), ShieldToast (UpgradeClientLegacy). All three are plate-less GothamBlack with a black outline. The trade toasts already match them (GiftToast's spot y 0.83, gold; refusals red like InventoryToast), so they stay plate-less. |
| G4, window open | | Non-offer toasts below an open window keep the plate-less style (decision 6; GiftToast does the same under the Shop). Only on a screen with no room below the window (phones) do they go on the slate plate over the offers' bottom edge. |
| G3 | | 04 and 05 were captured again with the weather / boost row present: two stand-in icons (clones of AdminBannerClient's Money x2 / Lucky chips, preview only; the server clears boosts it didn't start). The single card sits 8 px above the row with its right edge on the row's. The 3-card stack moves left of the Eggs / Pets / Potions column. |

**Not changed:**
- the "Keep as it is" list;
- the optional polish for passing screens (the 05 stack's fixed right edge, the 03 mutation pips).

## Screen files (overwritten, same names)
00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14 and 15 are all re-captured. `ref_shop`, `ref_rebirth` and
`ref_index` are untouched.
- 00 / 01 / 03 changed only by the current camera.
- 14 now shows the in-window red plate under Your Offer; the file name is kept.

## Phone scale after the fixes (733 x 392, top bar 58 px / 36 px)
**Phase 2 rows (09, 9 + 9 items):**

| Column | Phone px (58 / 36 px bar) | Notes |
|---|---|---|
| name | 7.1 / 7.6 | one size for every row; was 6.5-8.4 mixed |
| mutation | 7.8 / 8.3 | per line; "METEOR + UFO" is 2 lines |
| exact KG | 7.8 / 8.3 | |
| $/s | 7.1 / 7.6 | |
| row height | 23.3 / 24.9 | was ~19; PC 36 here, 46 at 1080p |
| picture | 19 | was ~17 |

- Phase 2 labels under 7 px: 0 (was 2). Under 9 px: 63 of 81 (was 67 of 87); the rows are uniform now, not mixed.

**Other screens:**
- **Phase 1 empty / full:** unchanged at 5.8 min. The compact card labels ("METEOR+1" 5.8, KG 6.5-8.4) follow decision 3,
  with 3 columns (ruling on 06-3).
- **Done:** min 7.8. **Trade page with the reason line:** min 12.2.
- **Request cards:** min 15.6.

**Tap targets:** all >= 42 px.
- New in Phase 2: the one-column phrases are 70 x 43 (hit area = the whole 79 px pitch), ACCEPT 332 x 42, BACK 141 x 42.
- The padlocked SEND is 99 x 42.

## Concerns
1. **Phase 2 row text is still 7-8 px on the 58 px-bar phone.** The binding limit is width: the name column must fit
   "Black Eastern Dragon" on one line (one name size, review 09-2).
   - The next in-layout options are a 2-line name column (bigger text, busier rows) or a narrower $/s column (the
     longest value is "$78.2M/s").
   - Both are owner / reviewer calls, and the Device-emulator pass is the real check.
2. **The Phase 2 chat log is gone.** The one column holds only the six phrases (ruling 09-6). New lines show as a 4 s
   bubble on the speaker's list, which the spec ("the last 8 lines are shown") would need a note for. Phase 1 keeps the
   8-line log.
3. **Preview-only stand-ins** in 04 / 05: the two boost icons are clones placed by the capture script. Live, the row is
   filled by AdminBannerClient / WeatherTilesClient.

---

# UI fix round 2

Scope: only the items in the round 2 brief (08, 09/10/11, 12, 13, 14). The controller rulings are untouched:
- The Phase 1 card text (06/07) is unchanged.
- Toasts while a window is open stay plate-less, below the window.
- 3 columns everywhere.

**Recaptured** (same names, `ui/`): `08`, `09`, `10`, `11`, `12`, `13`, `14`, plus the new `14b`. The other screens did not change.
- After the anti-scam fix (below), `10` and `14` were captured again.
- `10` now shows full 9 + 9 lists with a fresh chat line.
- `14` now shows a long refusal, and the new `14b` shows a short one.

## Changes per screen

**09 / 10 / 11, Phase 2 rows: now two-line.**
- **Rows:** 54 design px tall with 6 px gaps. The list is 294 tall, which shows 5 rows; longer lists scroll. The picture is 44 px.
- **Line 1:** picture plus the name, up to 20 design px. Each row has its own `UITextSizeConstraint`, so a long name shrinks only in its own row. The name is the largest text in the row.
- **Line 2:** `152,340.5 KG · UFO · $78.2M/s`, up to 16 design px. The dots are grey, the mutation uses its own colour, and $/s is green. Eggs show only KG and the mutation.
- **Bubble strip:** a 4 s chat bubble (420 x 36, text up to 17) shows only in EMPTY space under the speaker's last row. 11 shows both bubbles on short lists. A full list gets no bubble at all; see the anti-scam fix below, and 10.
- **Kept:** the `|` summary line, ACCEPT 70 / BACK 30, and the one-column phrases.

**08:** "Waiting for @builderman..." now uses the same text cap as "2.9s Left".
- While only you are ready, its box spans 530 px under READY, so it fits on one line.
- Both are 24 px at this screen (15.5 phone px). The box goes back to 260 when the state changes; it is tracked by the attribute `Wide`.

**12:** the subtitle sits in its own box and is broken on purpose, "Add them again" / "when they're back". It is centred, about 19 px here (12.3 phone px), and never wraps mid-phrase.

**13:**
- Receipt cards grow up to 110 px, sized to fit the rows needed.
- Each side's block is centred vertically, so YOU GAVE with 3 cards sits level with the middle of YOU GET's block instead of top-aligned.
- The Net figure's box is 500 x 40. It is 33 px here (21.4 phone px), red or lime, centred over OK.

**14 / 14b:** the refusal plate never covers the Your Offer $/s total and is never shrunk into a short box. This was updated by the anti-scam fix below.
- **Short text, fits beside the total:** if the text fits beside the total on one line at the full 20 design px, the plate sits at the left of the total row. It is only as wide as its text, and the total moves to the row's right end while it shows.
- **Anything longer:**
  - The plate sits right ABOVE the total row, over the bottom edge of the offer grid.
  - It is as wide as its text, up to the row's full 246 px; past that it becomes two lines, 62 px tall.
  - The total stays in view under it.
- **Captures:**
  - 14: "One of your items is no longer available", the longest offer refusal the server sends. It shows on 2 lines at 16 px here (about 10.4 phone px; before this fix it was about 6.5).
  - 14b: "Max 9 items" on 1 line, with the total `$80.4M/s` fully visible under it.
- Kept: the slate plate, the 2 px red stroke and the server's wording.

## Phone-scale sizes, Phase 2 rows (measured, `measure` op)

Columns are the measured text heights on a phone with a 58 px / 36 px top bar (trade ratios 0.647 / 0.691).

| element | 58 / 36 bar | round 1 | here (1920-wide Studio) |
|---|---|---|---|
| name (line 1) | 10.4 / 11.1 | 7.1 / 7.6 | 16 (20.2 at 1080p) |
| info: KG · mutation · $/s (line 2) | 8.4 / 9.0 | 7.1-7.8 / 7.6-8.3 | 13 (16.4 at 1080p) |
| row height | 28.5 / 30.4 | 23.3 / 24.9 | 44 |
| picture | 23.2 / 24.8 | 19 | 35.9 |

- Phase 2 has 52 text labels.
  - On the 58 px bar the smallest is 8.4; 18 are under 9 (all of them info lines) and 0 are under 7.
  - On the 36 px bar the smallest is 9.0 and 0 are under 9.
- The smallest tap target is 42 / 44 px.
- Other round 2 screens:
  - 08 "Waiting for": 15.5
  - 12 subtitle: 12.3
  - 13 Net: 21.4

## Anti-scam fix (coordinator, 2026-10-30): nothing may cover a Phase 2 row or the "| Net" line

Chat allows 1 line per 1.5 s and a bubble stays 4 s, so a bubble over row 5 could hide that item for the whole ACCEPT window.

**Chat bubble:**
- It shows only in empty list space under the speaker's last row.
  - The rule is in design px: rows x (54 + 6) - 6 + a 6 px margin must fit above the bubble's top, at 256 of the 294 px list.
  - The real rows round down, never up.
- So 0 to 4 rows get the bubble. 5 or more rows (the list is full or scrolls) get no bubble at all.
- Instead, the phrase in the right column gets a name tag on its top edge for 4 s: `@builderman`, or `You` in the chat colours, with a matching 2 px stroke and a small pop. Capture 10 shows "Deal?" tagged `@builderman` over a full 9 + 9 trade with every row clear.
- The tag is a Frame / TextLabel, so taps still reach the phrase's hit area.
- A line that is not one of the six phrases is dropped.

**Other overlays in Phase 2:**
- **Toast with no room under the window (phones):** it used to go on a plate over the bottom of both lists, which covered the rows. It now goes on the plate over the header's title.
- **A plate-less toast from before the window opened:** for example, at the 0.83 spot. While Phase 2 shows, every frame hides it if it touches the window (`guardToast`).
- **Refusal plate:** Phase 1 only (it needs Your Offer on screen), and every plate hides on a phase change.
- **"Securing items...":** this is the ACCEPT button's own label, not an overlay. "Returning items..." lives inside the Phase 1 inventory and is hidden in Phase 2.
- **The game's own UI:** `TradeUI.DisplayOrder` went from 25 to 130 (its toast from 31 to 131). That puts the window over:
  - the menu (3);
  - the stall windows (20);
  - the Shop / Upgrade toasts (30), the tutorial (40) and the streak celebration (45);
  - InventoryUI / InventoryToast (115 / 116);
  - the hotbar (Backpack 120, which is also hidden while trading).

  Request cards (24) stay under the window. Only the weather cutscenes (190 / 200) still draw over it; see concern 3.

**Verified in Play:**
- 98 cases: 0 / 1 / 3 / 4 / 5 / 9 / 9 rows on each side, with either player speaking.
  - 56 bubbles were shown, all in lists with 4 rows or fewer; there were 42 name tags.
  - 416 plate-vs-row and plate-vs-summary rectangle checks found 0 overlaps.
- A toast shown before Phase 2 opened was hidden once Phase 2 was on screen.
- Long refusal: 2 lines at 16 px; the total's text is never touched.

## Studio
- **Play sessions:** 4 this round:
  - captures;
  - the `measure` check;
  - the anti-scam test, stopped so I could edit;
  - the final tests plus the 10 / 14 / 14b captures.

  I started and stopped every one, and checked `TestFreshSave == true` in Edit before each. Studio is back in Edit with TestFreshSave true, and the preview copy is gone.
- I did not save, publish or change any server trade script.
- `TradeClient` compiles clean, and no Play logged an error.
- **Preview-only fix:** `measure` now cuts label text in a UTF-8-safe way, so the "·" in the info line no longer breaks the JSON.

## Concerns (round 2)
1. **The info line is 8.4 px on the 58 px-bar phone** (9.0 on the 36 px bar). The name reaches 10.4 / 11.1. The next step up is a taller row, which means 4 visible rows instead of 5. That is a reviewer call.
2. **The phrase name tag is small.** The label box is 16 px tall here, and an 11-letter name shrinks to fit the 112 px tag (about 7 phone px). The phrase itself stays at full size. A reviewer may want it bigger; the bubble is the main path on short lists.
3. **Weather cutscenes (DisplayOrder 190 / 200) still draw over the trade window.** Trades are cross-server, so a player who is alone on their server could get one mid-trade.
   - It is not partner-controlled, and a full-screen cutscene hides ACCEPT too.
   - Even so, part 2's modal lock should hold or skip weather cutscenes while a trade is open.
4. **Phone sizes come from `measure`, not a Device-emulator capture.** The 733x392 emulator pass is still the real check (review G1).

---

# UI fix round 3

Scope: the coordinator's round 3 list, built on `task-7-ui-review-3.md`. The rulings are unchanged:
- compact Phase 1 card labels;
- 3 columns everywhere;
- plate-less toasts while a window is open;
- nothing over the Phase 2 rows or the Net line.

**Recaptured** (same names, `ui/`): `07`, `08`, `09`, `10`, `11`, `13`, `14`, `14b`. `10` shows full 9 + 9 lists with a fresh "Deal?" from @builderman.

**Units (review G2).** Sizes are in design px unless marked.
- "Here" is this 1519-wide Studio view, where the window draws at 0.834 x design.
- The phone figures are the `measure` op's 733x392 numbers.
- Round 2's "54" (design), "44" (here) and "28.5" (phone) were the same row. This round's row is 68 design = 56 here = 36.2 phone.

## Changes per screen

**07:**
- "syncing..." uses the same box, the same cap and the same black outline as "2.9s Left", in pure white (#FFFFFF).
  - Both now sit in a 260 x 52 box under their own button and share one size: 26 design px, 21 here, 13.6 / 14.5 phone.
  - "2.9s Left" went down from 24 here to 21 so that 08's two-line wait matches it.
- **Trade chat:**
  - The lines now stack from the TOP of the log.
  - They take the biggest size, 15-20 design px, at which the shown lines fit. 07's five lines get 17 px, up from about 13.
  - A long line wraps onto a second line instead of shrinking.
  - The log keeps up to 8 lines; at 15 px the oldest drop off when it is full.

**08:**
- "Waiting for" / "@builderman..." sits under READY only, in the same box as 07's "2.9s Left". It never spans under CANCEL.
- It is broken on purpose onto two lines at the same 26 px size: 13.6 phone px per line. The round 2 "Wide" box is removed.

**09 / 10 / 11, Phase 2 rows: taller, 4 per side.**
- **Row geometry:** rows are 68 design px with 6 px gaps (4 x 68 + 3 x 6 = 290 of the 294 px list). The picture is 56 px.
- **Text:** the name goes up to 24 px and the info line up to 19 px. Each row keeps its own text-size constraint. The longest info line, "152,340.5 KG · METEOR + UFO · $78.2M/s", still fits the 340 px column at 19.
- **Scrolling:** a list longer than 4 rows scrolls. Its bar is 10 design px wide, white, on a dark track that shows only while the list scrolls.
- **Bubble:** the bubble text now matches the info line, up to 19 px. The anti-scam rule is unchanged; at 68 px rows it allows a bubble only for 0-3 rows, and 4 or more rows get the name tag.
  - 11's YOU GET has 4 items, so @builderman's line is now a tag on "Deal?". YOU GIVE's 3 rows still get the bubble.
- **Name tag:**
  - It spans the phrase column's full width (128 of 132), so it never comes near a row.
  - Its text goes up to 18 px. "@builderman" renders at 14 here, the same as the phrase text (9.1 phone px each).

**13:**
- Each header reads `YOU GAVE · 2 pets + 1 egg · $79.9M/s`: the title in white, the counts in gold and the $/s in green. Both headers share one size, the largest that fits both (up to 22).
- The cards sit 12 px under the header.
- Each panel is as tall as its own cards: YOU GAVE is 1 row and YOU GOT is 2.
- Both panels are as wide as the wider header or card row, with no empty sides, and the pair is centred.
- Net and OK sit under the taller panel. Kept: the sunburst, the gold title and the Net line (21.4 phone px).

**14 / 14b:**
- All in-window plates now use the window header, over the title text only: offer refusals, and toasts with no room under the window.
  - That is 552 x 48 design at x 132-684, which never reaches the "Ends in" pill (at 696) or the X.
  - It shows one line at up to 22 px, or two lines when it must. It keeps the slate fill, the 2 px red stroke and the exact server wording.
- 14 shows "One of your items is no longer available" on one line, at 18 here and 11.6 phone. 14b shows "Max 9 items".
- No offer cell, total or inventory card is covered; this was checked with rectangles in Play.
- The old above/beside-the-total plate and its branch are removed (review 3, item 14b-4).

**Also fixed:** plate text caps (bubbles and the header plate) were taken from the window's AbsoluteSize. During the open bounce that size shrinks the cap. They now use the window's fitted size.

## Phone-scale sizes, Phase 2 (measured, `measure` op, 58 / 36 px top bar)

| element | round 3 | round 2 | here (design) |
|---|---|---|---|
| name (line 1) | 12.3 / 13.1 | 10.4 / 11.1 | 19 (24) |
| info: KG · mutation · $/s (line 2) | 9.7 / 10.4 | 8.4 / 9.0 | 15 (19) |
| row height | 36.2 / 38.7 | 28.5 / 30.4 | 56 (68) |
| picture | 29.8 / 31.9 | 23.2 / 24.8 | 46 (56) |
| name tag | 9.1 / 9.7 | about 7 | 14 (up to 18) |
| chat bubble text | 9.7 / 10.4 | about 8.4 | 15 (19) |
| summary line | 13.6 / 14.5 | 13.6 / 14.5 | unchanged |

- **Phase 2 labels:** 53.
  - On the 58 px bar the smallest is 9.1 and none are under 9 (round 2: 18 under 9).
  - On the 36 px bar the smallest is 9.7.
- **Tap targets:** the smallest is 42 / 44 px.
- **Other round 3 screens (phone):**
  - 07 / 08 status lines: 13.6 / 14.5.
  - 07 chat log: 8.4-9.1 per line (was about 7).
  - 13 headers: 11.0-11.6 / 11.7-12.4.
  - 13 Net: 21.4 / 22.8.
  - 14 header plate: 11.6 / 12.4.

## Verified in Play
- **Anti-scam re-run** (review G4): 98 cases, with 0 / 1 / 2 / 3 / 4 / 9 / 9 rows per side and either player speaking.
  - Bubbles: 14 each at 0, 1, 2 and 3 rows.
  - Name tags: 14 at 4 rows and 28 at 9 rows.
  - 882 rectangle checks (bubble, header plate or name tag against every visible row and the summary line) found 0 overlaps.
- **14 / 14b header plate:** it does not cover the timer pill, Your Offer, the other player's offer or the inventory. The plate's right edge is at 887 px and the timer's left edge at 897 px.
- **Status line:** "Waiting for @builderman..." sits at the same x (571-787) as READY.

## Studio
- **Play sessions:** 4 this round:
  - 07, stopped to tune the chat size;
  - 07-13, stopped to fit the Done panels;
  - 13 / 14 / 14b plus the tests and `measure`, stopped to fix the plate cap;
  - an 11 recapture.

  I started and stopped every one, and checked `TestFreshSave == true` in Edit before each. Studio is back in Edit with TestFreshSave true, and the preview copy is gone.
- I did not save, publish or change any server trade script. `TradeClient` compiles clean, and no Play logged an error.

## Concerns (round 3)
1. **The chat log's size changes with its content** (20 px with a few lines, down to 15 px with eight), so the text shrinks a little as chat fills. A wrapped line can leave a short word on its own second line ("Offer" in 07).
2. **The header plate hides the partner's name for its 3 s.** Review 3 accepts this, and the name is also in the Players list and the panel titles.
3. **The 13 headers are 11-12 phone px.** The longest header, "5 pets + 4 eggs · $80.4M/s", sets the size both share. The panels grow to at most 480 px each so they stay inside the window.
4. **Weather cutscenes still draw over the window** (round 2, concern 3). This is for part 2's modal lock.
5. **The phone is still provisional:** all phone sizes come from `measure`, not a Device-emulator capture (review G1).

---

# Part 2: live wiring, modal lock, respawn, tests

**Status: DONE_WITH_CONCERNS.** The concerns are listed at the end; none of them is a failing test.

| Suite | Result |
|---|---|
| `TradeUITests` | 5 pass / 0 fail, three GREEN runs in a row (RED was 0 / 5) |
| `TradeSimTests.partA` (re-run) | 28 pass / 0 fail |
| `TradeSimTests.partB` (re-run) | 24 pass / 0 fail |

- No server trade script changed: TradeNode, TradeServer, TradeCore and TradePresence are untouched.
- No existing script was changed without a backup.

## 1. Review 4 polish
- **(a) Phase 1 chat log:** one fixed size, 15 design px with 18 px leading (12 px here). The lines still stack from the top, a long line still wraps instead of shrinking, and the oldest drop off once the box is full. The 15-20 px auto-fit is gone.
- **(b) The status line** under CANCEL now reads "Syncing offer..." (was "syncing..."). Its style is unchanged: white, black outline, the same box and size as "2.9s Left".
- **(c) The in-window plate is sized to its text:**
  - Width = text width at 22 px + 28, at least 280 and at most 552.
  - It is centred on the title's centre (x 408), so it stays inside x 132-684 and never reaches the "Ends in" pill (696) or the X.
  - Long text still takes the full span, on two lines if needed.
  - **Builder's addition: the title text hides while the plate shows.** It comes back when the plate goes; this was checked in Play.
    - Without it, "Max 9 items" showed fragments of "Trading with @builderman" on both sides.
    - This needs the reviewer's confirmation.
- **Recaptured** (same names, `ui/`): `07`, `08`, `14b`.

## 2. Scripts changed
Every existing script was cloned into `ServerStorage._Backup_Trading.Before` first: `Enabled = false`, tags stripped, one backup per script.

| Script | Size now | Backup | Change |
|---|---|---|---|
| `StarterPlayerScripts.TradeClient` | 96,446 | (own, Task 7) | the polish; the server wiring; the lock attribute; the rebuild; the Studio-only test API |
| `StarterGui.MainMenu.MenuController` | 33,269 | `.Before.MenuController` (from part 1) | `openWindow` refuses while `TradeWindowOpen` is set and fires `TradeUI.Locked` (the reason toast) |
| `StarterPlayerScripts.PetsEggsUI` | 30,766 | `.Before.PetsEggsUI` (new) | `setOpen(name)` refuses to OPEN a panel while trading; closing still works |
| `StarterPlayerScripts.SellClient` | 19,327 | `.Before.SellClient` (new) | `setOpen(true)` refuses while trading. The ring loop waits, so stepping in during a trade opens the Sell window once the trade is over |
| `StarterPlayerScripts.UpgradeClientLegacy` | 21,768 | `.Before.UpgradeClientLegacy` (new) | the same as SellClient, for the Upgrade stall |
| `StarterPlayerScripts.WeatherClient` | 6,003 | `.Before.WeatherClient` (new) | `onCutscene` skips with `WeatherCutsceneSkip = "trading"` while trading (client side only) |
| `ServerStorage.TradeSimTests` | 157,751 | `.Before.TradeSimTests` (new) | test harness only: the push recorder also calls `H.tap` when set, and `T.harness = harness` is exported. partA / partB are unchanged in behaviour (re-run green) |
| `ServerStorage.TradeUITests` | 33,257 (new) | - | the 5 UI tests |

## 3. Wiring map (TradeClient -> `ReplicatedStorage.Trade`)
Every button calls `Client.<op>` in its own thread. `Client.<op>` sends the op with the Remote API's exact types and waits.

**Rules every call follows:**
- **Nothing changes on screen until the server's next view.** The client trusts nothing it shows.
- **No double sends.** A call is never sent twice while it is still out: the same key is ignored, and the in-flight check covers the paths through the same key.
- **Refusals are shown with their exact text:** on the header plate when the window is open, otherwise as a toast.
- **No list toast for "Slow down":** a list / history refresh refused with "Slow down" keeps the rows already shown. Every other refusal is shown.

| UI | Client function | Remote op (types) | In-flight key |
|---|---|---|---|
| Players row SEND | `send(uid)` | Request `"send", uid` (a whole number); the reply sets the outgoing state | `send` |
| Players row CANCEL (your pending request) | `cancelRequest(id)` | Request `"cancelRequest", reqId` | `cancelRequest` |
| Request card ACCEPT / DECLINE | `respond(id, yes)` | Request `"respond", reqId, boolean` | `respond:<id>` |
| Inventory card | `tapItem(it)` -> `add(ref)` / `remove(i)` | Action `"add", {t="pet", id}` or `{t="egg", kind, kg = the exact KG from your EggInventory, mutKey?}` | `offer` (one offer change at a time) |
| Your offer card | `remove(i)` | Action `"remove", i` (whole number 1..9, into the latest view's `mine`) | `offer` |
| READY / ACCEPT | `ready()` / `accept()` | Action `"ready"` / `"accept"`, the whole `ver` of the latest view | `ready` / `accept` |
| BACK / CANCEL / [X] | `back()` / `cancel()` | Action `"back"` / `"cancel"` | `back` / `cancel` |
| The six phrases | `chat(n)` | Action `"chat"`, n (whole number 1..6) | `chat` |
| The Trade page shows (tile / window visible) | `list()` | Query `"list"`: rows + `why` (the reason line) | `list` |
| Search (no local match, valid username, 0.6 s after typing) | `search(text)` | Query `"search"`: rows, or the exact reason as the list note | `search` |
| HISTORY tab | `history()` | Query `"history"` | `history` |
| Start + every respawn | `rebuild()` | Query `"state"`: the window from `trade`, the cards from `requests` (only the server's list stays), and `outgoing` | `state` |
| INVITE FRIENDS | (unchanged) | `SocialService:CanSendGameInviteAsync` then `PromptGameInvite`, both in pcall | - |
| Done OK | `closeDone()` | none: the trade is already over | - |

**Pushes:**
- `trade` -> renderTrade (countdowns are seconds left from arrival). A closed view closes the window and toasts `why`.
- `done` -> the Done screen ("completed"). A "cancelled" Done closes the window and toasts `why`, but only if the closed view hasn't just said the same thing (8 s), then shows "Your items are back" if `returned` is set.
- `request` / `requestGone` -> the cards.
- `outgoing` / `outgoingGone` -> the row state: REQUEST SENT in gold, plus CANCEL.
- `toast` -> the text exactly as sent.

**Returning items...** shows after BACK or a refused Phase 2 (confirm -> select) until the items come back.

**Studio-only test API** (`if STUDIO then`; none of it exists live):
- **Preview ops:** `transport` (a test copy of the remotes), `press` (the same `Client.<op>` the button calls), `pressItem` (an inventory card's tap), `items`, `snapshot`, `hide` (the window off the screen with no server call).
- **Swapping the remotes:** `Client.useFolder` is defined only in Studio.

## 4. Modal lock coverage (decision 8)
TradeClient sets the local player attribute `TradeWindowOpen` when the window opens and clears it when it closes. The window has DisplayOrder 130, above every game GUI except the weather cutscenes.

| Surface | While a trade window is open |
|---|---|
| MenuController pages: every tile, the top bar's Settings, any `OpenPage` (Shop, Gift, Rebirth, Index, Trade, Settings) | refused; the header plate says "Finish your trade first" |
| PetsEggsUI side panels (Pets / Eggs / Potions, `OpenPanel`) | refused (same reason); closing still works |
| Walk-in Sell window | doesn't open; it opens after the trade if you're still in the ring |
| Upgrade stall window | the same as Sell |
| Weather cutscenes (UFO / Meteor) | skipped (`WeatherCutsceneSkip = "trading"`); the weather server is untouched |
| CloseWindow / WindowOpened from any script | never close the trade window; only the trade closes it (a closed view, Done OK) |
| Hotbar | hidden (part 1) |
| FreeGift / Welcome Back / Starter Pack / InventoryUI | not locked; they draw UNDER the window (DisplayOrder at most 116, against 130) |

## 5. Respawn (decision 9)
- TradeUI, TradeRequests and TradeToast use `ResetOnSpawn = false`, and MainMenu was already `ResetOnSpawn = false`.
- `Client.rebuild()` runs at start and 0.5 s after every CharacterAdded. It asks Query `"state"` and draws exactly what the server has, so dying never ends or hides a trade.

## 6. Tests (`ServerStorage.TradeUITests`)
**How they run.** The UI lives on the client, so the tests do too.
- **Server half:** `serverUp(player)` builds TradeSimTests' two simulated servers:
  - node A = the real test player + A2-A4;
  - node B = the virtual peers B and C.

  It adds `ReplicatedStorage.TradeSimUI`, a copy of `Request` / `Action` / `Query` / `Push` wired to node A exactly as TradeServer wires the default node. It also adds a `Bot` remote: the virtual players' ops, the item multiset, the server's copy of the last push, and a respawn.
- **The trade clock follows real time** during the run, so the client's 5 s countdowns and the server's locks agree.
- **Client half:** `client(verbose)` points TradeClient at the copy (`transport`) and drives it ONLY through the functions its buttons call.
- `serverDown()` runs the harness teardown.
- **Limit:** scripts can't click. `VirtualInputManager` answers "lacking capability RobloxScript". So tiles and ADMIN are checked by a hit-test, plus the same open function their click runs.

| Test | What it proves |
|---|---|
| `menu_regression` | With no trade open:<br>- every tile (Shop, Gift, Rebirth, Index, Trade) is on screen, and the topmost input-taking object at its centre is the tile;<br>- its page opens through `openWindow` and closes, and so does Settings;<br>- ADMIN is reachable, under Index, in the Trading tile's row;<br>- the Pets / Eggs / Potions panels open and close;<br>- the Sell and Upgrade walk-ins open in their rings and close outside |
| `trade_window_modal` | With a trade window open:<br>- none of the 6 pages opens, and the reason shows;<br>- no panel opens;<br>- Sell / Upgrade stay shut in their rings;<br>- a UFO cutscene start (this client's copy of the attributes) is skipped, "trading";<br>- CloseWindow / WindowOpened leave it open;<br>- a closed view closes it and frees the lock, and the Shop opens again |
| `rebuild_after_respawn` | A live trade with B: B's request accepted on the card, one item each.<br>- The window is taken off the screen with no server call, then a real respawn (`LoadCharacter`).<br>- A `state` call rebuilds the same trade: same ver, same offers, and the view equals the server's apart from the countdowns.<br>- The trade is still open on the server |
| `request_card_stack` | A2 and A3 (your server) and B (the other server) send:<br>- 3 cards, newest on top, one column, no overlap, a running 30 s bar each, above the weather row;<br>- A4's 4th request is refused "@... has too many requests";<br>- DECLINE removes that card and B gets `outgoingGone` "declined";<br>- ACCEPT opens the trade with A3 and the last card goes |
| `ui_trade_end_to_end` | SEND (and the outgoing state), then B accepts on node B. Then:<br>- a pet and an egg from the inventory cards, with the egg's KG exact in the view;<br>- a remove from the offer card, then the egg again;<br>- a chat phrase;<br>- READY pressed twice while its call is out = **one** call;<br>- B READY -> Phase 2 with both escrows saved;<br>- **BACK** -> both offers empty, "Returning items..." shown, the pet back;<br>- round 2 -> ACCEPT ("Waiting for @SimPeerB...") -> B ACCEPT -> the Done screen (2 gave, 1 got);<br>- **conservation:** the item multiset of both players before == after, and no pet id twice;<br>- the client's last view and its Done push == the server's (deep compare);<br>- OK closes it and frees the lock |

**RED** (on the client with its wiring switched off: no remote calls, no pushes, no lock, no test API; the other scripts were not changed yet):
```
TradeUI: 0 pass / 5 fail
FAIL menu_regression [Shop tile is covered by Players.Santrinio.PlayerGui.BackpackGui.Backpack]
FAIL trade_window_modal [no modal lock (TradeWindowOpen)]
FAIL rebuild_after_respawn [TradeClient has no test API (snapshot)]
FAIL request_card_stack [TradeClient has no test API (snapshot)]
FAIL ui_trade_end_to_end [TradeClient has no test API (press)]
```
- **`menu_regression`'s RED was a test bug, not a menu bug.** Satchel's full-screen Backpack frame is transparent and takes no input. The hit-test now takes the topmost object that takes input (a button or Active).
- **The first GREEN run was 4/5.** `request_card_stack` measured the newest card during its 0.25 s pop-in tween, so the test now waits for all three cards to be full size.

**GREEN** (final code; the same result in three runs in a row):
```
TradeUI: 5 pass / 0 fail
ok   menu_regression [41 asserts, 2.8 s]
ok   trade_window_modal [22 asserts, 6.4 s]
ok   rebuild_after_respawn [14 asserts, 4.7 s]
ok   request_card_stack [20 asserts, 4.0 s]
ok   ui_trade_end_to_end [40 asserts, 28.4 s]
```
The server calls the end-to-end test made (counted on the copied remotes):

| Op | Calls |
|---|---|
| Action.add | 5 |
| Action.remove | 1 |
| Action.chat | 1 |
| Action.ready | 2 (one per round, despite the double presses) |
| Action.back | 1 |
| Action.accept | 1 |
| Request.send | 1 |

**Server suites re-run afterwards** (the same Play session, the UI test harness torn down first):
```
TradeSim partA: 28 pass / 0 fail
TradeSim partB: 24 pass / 0 fail   (sync retries 0; the counters show only the faults the tests inject)
```

**Ad-hoc checks** (sim transport):
- The Trade page asks for its list when it shows: rows @SimPeerB, @SimPeerC, @SimSendA2-A4, with no reason line.
- History returns `[]`.
- Typing "Roblox" (no local match) sends one `search` after the pause, and the list note reads the server's exact "@Roblox isn't online".
- An exact search for a virtual peer ("SimPeerB") answers "isn't online". This is server behaviour: TradePresence looks up real usernames.

## 7. Studio
- **Play sessions:** 5. I started and stopped every one, and checked `TestFreshSave == true` in Edit before each:
  - an API probe;
  - RED;
  - GREEN 4/5;
  - GREEN 5/5 x2, the ad-hoc checks and the 07 / 08 / 14b captures;
  - the 14b recapture, a GREEN 5/5 run, partA and partB.
- Studio is back in Edit with TestFreshSave true.
- Nothing is left over: the temporary stash `_T7Work` is deleted, and the test folders exist only while a test runs.
- No save, no publish.
- **Console:** no TradeClient or TradeUITests error. The run showed:
  - one transient `DataStoreService: InternalServerError` on `TradeSeen_v1_Studio` (Roblox's side);
  - partB's own expected lines: a test takeover of the TestFreshSave save key, and the injected TradeItems fault.

## 8. Concerns
1. **Tile and ADMIN clicks aren't simulated.** Scripts can't send input. The tests prove that nothing covers each tile, that the button takes input, and that its open function works. A real-click check of the tiles and ADMIN belongs in the controller's Device-emulator pass.
2. **New client texts** need an owner / reviewer look:
   - "Finish your trade first" (a locked tile or panel; spec: "a disabled button always shows why");
   - "REQUEST SENT" + CANCEL on the row of your pending request;
   - "Try again in a moment" (the server's own phrase) when a remote call itself fails.
3. **The header plate now hides the title text while it shows** (builder's call, section 1c).
4. **Walk-in windows wait.** Standing in the Sell / Upgrade ring when a trade ends opens that window right after OK. This is the normal walk-in behaviour, deferred.
5. **Weather cutscenes are skipped, not postponed,** for a trading player. They are 8 s arrivals; postponing one would replay a stale arrival.
6. **Still provisional:** the phone sizes (review G1) and the owner's look at the new states.

# Code fix round 1 (2026-10-30)
Source: `work/task-7-code-review.md` (0 Critical / 3 Important / 10 Minor). The work was TDD: a failing test first in
`ServerStorage.TradeUITests`, then the fix. No screen's look changed; the phone pass stands.

## 1. Scripts changed
| Script | What | Backup |
|---|---|---|
| `StarterPlayerScripts.TradeClient` | I-1, I-2, I-3, M-1..M-4, M-6, M-8..M-10, inventory rules, a rebuild race (section 3), test-API ops | new in Task 7 |
| `StarterGui.MainMenu.MenuController` | M-5: line 30 `ENABLED == true` -> `ENABLED ~= false` | `_Backup_Trading.Before.MenuController` (Part 1) |
| `ServerScriptService.TradeCore` | M-5: `newSession` refused when `not C.ENABLED` -> `C.ENABLED == false` | **new:** `_Backup_Trading.Before.TradeCore` |
| `ServerStorage.TradeUITests` | 7 new tests, `rebuild_after_respawn` rewritten, new Bot ops | new in Task 7 |

**The server script change, stated clearly.** TradeCore is a server trade script. Before the fix, `TradeConfig.ENABLED = nil`
let TradeNode and TradePresence run (they use `~= false`) while TradeCore refused every new session ("Trading is off").
Today's config has `ENABLED = true`, so the bug was latent. The coordinator asked for one rule everywhere.
- The test: `kill_switch` calls `TradeCore.newSession` with `ENABLED = nil`.
  - RED: `nil -> false "Trading is off"`.
  - GREEN: the session starts, and `false` still refuses.
- `TradeCoreTests.pure` was re-run in Edit: 32 pass / 0 fail.
- TradePresence (line 720) already behaved as `~= false`, so it is unchanged.

## 2. The fixes (TradeClient line numbers are the new 2,256-line script)
- **I-1, closed views (`renderTrade` 1286).**
  - A closed view (done or cancel) is never kept as the live `view`. The window closes and `TradeWindowOpen` goes at
    once, unless the Done screen is the one showing.
  - A cancel's `why` shows as a toast.
  - The Done push then opens the Done screen by itself, with the open pop.
  - If no Done push arrives within 6 s (counted by `Client.dones`), the closed view's `why` ("Trade complete!") shows as a green toast.
- **I-2, "the trade doesn't exist" (`inTrade` 1953).**
  - Any in-window op refused with "You're not trading" or "Trade is over" clears `view`, closes the window, frees the lock
    and toasts the exact text. Those ops are add, remove, ready, accept, back, cancel and chat.
  - It then runs `Client.rebuild()` (Query "state"), so a trade that does exist comes back.
- **I-3, request cards (`requestOver` 1938).** A refused ACCEPT or DECLINE removes the card only for a final reason:
  - "That request has expired";
  - "You're already trading";
  - "@B is already trading";
  - "@B isn't online right now" / "@B left the game" (the sender left);
  - "Trade cancelled" (the server sends it only after it has already used up the request).

  Every other reason keeps the card and shows the toast, including "Wait Ns", "Slow down", "Try again in a moment",
  "Reconnecting...", "Syncing... try again" and "Your items are still loading". The card still runs out on its own bar.
- **M-1.** A search refused "Slow down" no longer becomes the list's note. The same name is asked once more after
  `TradeConfig.SEARCH_GAP` (2 s), if the text hasn't changed. Without that retry, the 0.6 s type-pause would lose searches.
- **M-2.** The prices come from the server wherever it sends them:
  - The Phase 1 and Phase 2 totals were already `view.total` / `summary.diff`.
  - The Done screen now uses the server's `total.mine` / `total.theirs` when the last view was this trade's closed done
    view with the same cards.
  - **Display-only sums that remain:**
    - the Done screen's fallback sum of the cards' server-sent `ps`, used when the last view doesn't match (the Done push carries no totals);
    - the inventory cards' $/s (`CreatureConfig.petIncome`).

    Neither is ever sent back. The server re-prices every item from its own data.
- **M-3, timeouts (`call` 1880).**
  - Every call has `Client.TIMEOUT = 10` s. On timeout it frees its in-flight key (a per-call token, so a late finish
    can't free a newer call's key) and returns "Try again in a moment". The late answer is dropped; the pushes still tell the truth.
  - A respawn clears every in-flight key (`CharacterAdded` 2084).
- **M-4.** The sent row captures its request id when it is built (`sentId` 1675).
- **M-5.** One rule everywhere: `ENABLED ~= false` (MenuController, TradeCore; TradeNode and TradePresence already used it).
- **M-6, ACCEPT gate (`tick` 1519).** It now matches the server exactly.
  - `TradeCore.accept` refuses only when YOUR side isn't escrowed (`escrowedNow(s, side)`). The commit (`toCommit`) is
    the step that needs both.
  - So ACCEPT unlocks on `secured.you`, and "Securing items..." shows only while your own escrow is pending.
- **M-8.** The Trade page waits for MainMenu in its own thread (`task.spawn` 1572).
  - The server wiring, the pushes, the rebuild and the Heartbeat are all set up without waiting for MainMenu.
  - Until the page is built, stand-in `Menu.*` functions (1558) keep your outgoing request, and the page applies it once it exists.
- **M-9.** `respond` and `cancelRequest` refuse any id that isn't a non-empty string before calling the server (`goodId` 1927).
- **M-10, hotbar (`setHotbar` 982).** The hotbar is hidden with a `TradeHotbarHidden` flag, the same pattern as the
  walk-ins' `WalkInHotbarHidden`. On close it comes back only if the trade hid it. A hotbar that another system had
  turned off stays off.
- **Rebuild re-parents the screens.** It puts TradeUI, TradeRequests and TradeToast back into PlayerGui if they are
  missing. All three already use `ResetOnSpawn = false`.

## 3. A race the new tests found (fixed)
`not_trading_resyncs` caught a stale rebuild:
1. A `state` answer is already on its way.
2. A newer view opens the window.
3. The old answer arrives and closes that window.

Live, the server's ordering makes this unlikely, but the fix is cheap. `renderTrade` counts views (`Client.views` 1289),
and a rebuild whose call started before the latest view leaves the window alone (2022-2025). Request cards and the
outgoing request still sync.

## 4. "Unverified": the inventory equals what TradeItems accepts
The server's rules (`BaseHatchery` TradeItems `describe` 1178-1202, `usable` 507-509; `TradeCore.petSig` / `eggSig` / `validKg`):
- **Pets:**
  - all of BaseData.pets (placed on the base) + PetInventory (hotbar / stored); there is no equipped or placed exclusion;
  - the id must be there exactly once;
  - the creature needs a CreatureConfig entry AND a model in `RS.CreatureModels`;
  - the id, name and KG must make a `petSig`: no "|", the KG a finite number > 0 (a string KG fails on the server).
- **Eggs:**
  - unplaced eggs only: EggInventory. Placed eggs live in `BaseData.eggs` and were never listed;
  - the kind needs a template in `ServerStorage.Assets.Eggs`. The client can't see ServerStorage, so it uses `EGG_AREA`,
    which lists the same seven kinds; the test checks one egg of every server template kind;
  - `entryKg` must be > 0.

**Four differences were found, and the client now matches** (`myItems` 1061): it listed duplicated ids, pets with no
model, pets with a bad KG or a "|" in the id, and eggs of unknown kinds or with KG <= 0.

The RED run listed exactly these extra cards: `pet|e_dup` x2, `e_neg`, `e_str`, `e_zero`, `e|pipe`, `FakeEgg|5|`, `TideEgg|-2|` and `TideEgg|0|`.

## 5. Tests (`ServerStorage.TradeUITests`, 12 tests)
New Bot ops:
- `inject` (a refusal on the copy of the remotes before node A sees it);
- `stall` (a call that doesn't come back);
- `mute` (lost pushes);
- `kill` (a real death);
- `enabled` / `newSession` (the kill switch);
- `describe` / `describeAttrs` / `edgeAttrs` (TradeItems' describe on the player, or on a virtual holder with edge-case items).

New TradePreview ops: `itemKeys`, `timeout`, `enabled`, and `note` in the snapshot. The preview `trade` / `done` ops now
go through `Client.onPush`, the push handler.

**Harness note.** Code run from the MCP has its own `require` cache: its TradeConfig is a different table from the
game's (proved with a probe script). So the kill switch is changed in the game's VM:
- on the server, through a Play-only fixture Script (`ServerScriptService._TradeUIKillSwitch`), which `serverDown` removes;
- on the client, through TradePreview `enabled`.

| Test | Covers | RED (before the fix) |
|---|---|---|
| hotbar_state | M-10 | a hidden hotbar came back on close |
| closed_view_closes | I-1 (done + cancel, Done push after, no push at all) | "the closed done view left the window true / lock true / a live view true" |
| accept_gate | M-6 | "Securing items..." with your escrow saved |
| kill_switch | M-5 / M-7: ENABLED false = no tile (a fresh MainMenu copy runs MenuController), the real remotes refuse list / history / state / send ("Trading is off"), nil = tile + newSession | "ENABLED = nil hid the Trading tile"; server newSession(nil) "Trading is off" |
| rebuild_after_respawn | M-7: ResetOnSpawn = false on all three screens; a REAL death with the window open (same ScreenGui, state re-read); the screens removed from PlayerGui + a second death -> rebuilt, view == the server's | "the screens weren't rebuilt after the respawn" |
| request_refusals | I-3 (6 transient reasons keep the card + toast; 5 final reasons drop it, rebuild brings it back), M-9, M-1, M-3 | "\"Wait 3s\" took the card away" |
| not_trading_resyncs | I-2: a real trade ended with its pushes muted, then READY; then stale windows for cancel / BACK / ACCEPT / add / remove / chat | "ready: the window / lock stayed" |
| inventory_matches_server | "unverified": edge set + the player's own items == describe; every listed card added and removed in a live trade | 9 extra cards (section 4) |

The five Part 2 tests still pass: menu_regression, trade_window_modal, request_card_stack, ui_trade_end_to_end and the
rewritten rebuild_after_respawn.

**Results.**
- After the fixes: 11 / 12, which found the race in section 3. After that fix: 12 / 12 three runs in a row.
  - A full run takes about 95 s.
  - e2e: 40 asserts / 29.4 s; rebuild: 20 asserts / 11.6 s; refusals: 44 asserts / 5.6 s; resync: 19 asserts / 13.7 s; inventory: 29 asserts / 10.5 s.
- Then, in the same session with the UI harness torn down:
  ```
  TradeSim partA: 28 pass / 0 fail
  TradeSim partB: 24 pass / 0 fail
  TradeCore (Edit, pure): 32 pass / 0 fail
  ```

## 6. Studio
- **Play sessions:** 4, each started and stopped by me, with `TestFreshSave == true` checked in Edit before each:
  - RED (12 tests);
  - RED kill_switch after the harness fix;
  - GREEN 11 / 12, plus a re-run of the failing test;
  - GREEN 12 / 12 x3, partA and partB.
- Studio is back in Edit with TestFreshSave true.
- No leftovers: the fixture Script, `_KillSwitchMenu`, `TradeSimUI` and the RS test copy exist only during Play.
- No save, no publish.
- **Console:** only the expected lines: partB's save takeover and its injected TradeItems describe fault.

## 7. Concerns (code fix round 1)
1. **The completed-trade transition changed.** The closed done view now closes the window, and the Done push reopens it
   with the open pop and sound. Before, the stale Phase 2 screen stayed until the Done screen replaced it. The screens
   look the same; the controller may want to watch this once on the phone.
2. **New client texts:**
   - "You're not trading" as a toast when a stale window closes (the server's own text);
   - "Trade complete!" (the server's `why`) as a green toast when no Done push arrives within 6 s.
3. **"Trade cancelled" counts as final for a request card.** This goes beyond the coordinator's list: the server sends it
   only after it has already used up the request.
4. **Search's "Slow down" triggers one automatic retry** after 2 s (section 2, M-1). This is new behaviour.
5. **M-8 has no automated test.** It would need a MainMenu that arrives late. It was checked by structure: the page
   builder is a `task.spawn`, and stand-ins keep your request.
6. **Clearing in-flight keys on respawn** lets a call that is still out be pressed again. The server's own rules (the ver
   check, one call at a time, the limiter) make the second one harmless.
7. **The kill_switch tile check briefly runs a second MenuController** in a hidden copy of MainMenu (about 0.1 s; Studio
   test only). BrickUI keeps that copy's viewport callback until the session ends.

# Final fix round (2026-10-30)
Sources: `work/task-7-code-rereview-1.md` (new issue 1 Important, new issues 2 and 4 Minor) and `work/task-7-ui-review-5.md`
(F3 bottom margin, F5 status copy). The work was TDD where it could be tested. Only TradeClient and TradeUITests changed;
no server script was touched. ENABLED stays `~= false` (the coordinator's ruling).

## 1. Fixes (TradeClient, now 2,297 lines)
1. **A late Done push never closes or covers a newer trade's window** (`renderDone` 1406).
   - When a view that isn't closed is on screen (`view ~= nil`), the push belongs to an older trade. The server always
     sends a trade's closed view before its Done push, and the closed view drops `view`.
   - In that case the push's outcome is only a toast: its `why`, deduped against the closed view's toast within 8 s, plus
     "Your items are back" if it returned items. The live window is left alone.
   - It also starts a `rebuild`, so the server's state settles the window. If the closed view of the open trade was ever
     lost, that rebuild closes the stale window.
   - Views carry no trade id, so "a live view is open" is the test, as the coordinator allowed.
2. **The GONE toast no longer replaces a closed view's reason** (`inTrade` 1988). "You're not trading" / "Trade is over"
   only toasts when this call is what closes the window. A window the closed view already closed keeps that view's own
   toast.
3. **`EGG_AREA` is derived** (76) from `CreatureConfig.Areas`, the shared table the server's hatchery checks
   (`BaseHatchery`: `if not CreatureConfig.Areas[kind] then return false, "Unknown egg"`). It was a hand-copied list.
   - TradeItems' `describe` checks the server-only egg templates (`ServerStorage.Assets.Eggs`), which the client can't
     see. A test now asserts that the client's egg kinds equal those templates exactly, so neither side can drift silently.
4. **The phone fit keeps 8 px off the bottom edge** (`tradeScale` 1006, `Client.fitBox` 1011).
   - On a phone, the fit now holds back 18 px of height instead of 8. The layout is unchanged.
   - Across every landscape phone screen 733 / 812 / 874 / 932 wide and 280-484 tall, taking the worst case of the pixel
     rounding: the window ends at least 9 px above the bottom edge, and the header icon starts at least 8 px under the top
     (before: 4 px and 3 px).
   - The window is about 3 % smaller on a phone (at 874 x 344: scale 0.554 -> 0.538).
   - The PC fit is unchanged.
5. **The PC 07 status line says what it waits for** (1532). It now reads "Syncing offers / with @builderman...": two
   lines, the same form as 08's "Waiting for / @builderman...", in the white "2.9s Left" style and box. "Offers" is
   plural because `syncing` covers a change on its way from either side.

## 2. Tests (`ServerStorage.TradeUITests`, 15 tests)
New Bot ops: `hold(kind)` / `held()` / `release()` (a push held back on its way to the client: a late push) and
`eggTemplates`. New TradePreview ops: `fitAt` (Client.fitBox on any screen size) and `eggKinds`.

| Test | Covers | RED (before the fix) |
|---|---|---|
| late_done_push (new) | 1: trade A with B is cancelled while its Done push is held; trade B with C opens; A's push is released. B's window stays open, locked and on B's trade, and a chat press still works. Then an older *completed* Done push doesn't cover it either | "A's late Done push hit B's window: open false, lock nil" |
| not_trading_resyncs (extended) | 2: a closed view's reason stays after a late "You're not trading" | "the closed view's reason was replaced by: You're not trading" |
| inventory_matches_server (extended) | 3: client egg kinds == the server's egg templates | (none: the copied list matched; this guards against drift) |
| phone_fit (new) | 4: 820 phone screen sizes leave 8 px or more at the bottom and the top; the real window on this screen too | "741 of 820 phone screens leave under 8 px, e.g. 733x280: bottom 5, top 3" |
| sync_status (new) | 5: the line under CANCEL while syncing | "the sync line: Syncing offer..." |

**Results** (one Play session):
- TradeUITests: 15 pass / 0 fail, twice.
  - late_done_push: 12 asserts / 9.1 s; not_trading_resyncs: 21 asserts / 14.7 s; inventory: 30 asserts / 11.8 s; e2e: 40 asserts / 29.2 s.
- Then:
  ```
  TradeSim partA: 28 pass / 0 fail
  TradeSim partB: 24 pass / 0 fail
  ```

## 3. Capture
`ui/07_phase1_full_9x9_ready_countdown.png` was captured again (1519 x 753, same payload: 9 + 9, READY locked "2.9s
Left", 5 chat lines, syncing). Under CANCEL it now reads "Syncing offers / with @builderman...". Nothing else on the
screen changed.

## 4. Studio
- **Play sessions:** 2, each started and stopped by me, with `TestFreshSave == true` checked in Edit before each:
  - RED (the 4 new / extended tests);
  - GREEN: 15 / 15 twice, the 07 capture, partA and partB.
- Studio is back in Edit with TestFreshSave true. No leftovers, no save, no publish.
- **Console:**
  - partB's expected lines (the save takeover and the injected describe fault);
  - six `MemoryStoreService: InternalError` lines (HashMap.Get on `TradeSessions_v1_Studio`, HashMap.Update on
    `TradeBusy_v1_Studio`). These are Roblox-side Studio service errors from the real server node's background work. No
    test failed, and the node's own retry handles them.

## 5. Concerns (final fix round)
1. **The late-push rule relies on the server's order:** a trade's closed view always comes before its Done push
   (TradeNode `endLocal` 927-936, and the settle push after it). If that ever changed, a Done push for the open trade
   would become a toast plus a rebuild instead of the Done screen. The rebuild still closes that window.
2. **Phone scale is 3 % smaller** for the 8 px margin. The phone captures (`phone_07` / `10` / `13` / `lock`) were not
   retaken; only a Device-emulator pass can, and that is the controller's.
3. **The phone window width and the other review-5 phone items** (F1 menu centring, F2 the HUD tile lift, the F3 width
   cap, F4 chat size, F6 info line) were not in this round's list and are unchanged.
