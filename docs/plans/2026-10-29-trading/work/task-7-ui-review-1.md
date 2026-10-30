# Task 7 UI review 1: trading screens (fresh reviewer)

**Result: 5 of 16 screens pass (8.5 or higher). Lowest 7.5 (09). Average 8.3. 11 screens go back to the builder.**

Reviewed: `ui/00` to `ui/15` against the three look references (`ref_shop`, `ref_rebirth`, `ref_index`), spec section 4 (what each screen is for) and the owner's hard rules. I zoomed into 00, 05, 07, 09, 11, 12 and 13 to check the small labels.

Scoring: (a) the reference look, (b) clarity (can a player tell what is happening and what to press), (c) layout (alignment, spacing, nothing clipped or overlapping), (d) phone at about 0.63. Each overall score is the mean of the four, to one decimal.

**Limits of this review**
- **(d) is provisional.** `ui/` has no 733x392 or 0.63-scale capture. The phone view is judged from the builder's own code measurements in `task-7-report.md` (text heights and tap sizes). Confirm in the Device emulator before the ship gate (G1).
- The weather / boost row is not in any capture, so the request-card anchor cannot be checked from these shots (G3).
- No owner mockup of the trade window exists (report concern 2). This review does not replace owner approval (G6).

## Scores

| Screen | a look | b clarity | c layout | d phone | Score | Reason |
|---|---|---|---|---|---|---|
| 00 HUD: Trading tile + ADMIN | 9.5 | 9.0 | 9.0 | 8.5 | **9.0** | Trading tile fits the 2-column grid in Rebirth's column; ADMIN takes the free slot cleanly; labels read at zoom |
| 01 Trading, Players | 9.5 | 9.0 | 8.5 | 8.5 | **8.9** | Check-UI header with the big icon, bright tabs, clear ONLINE / AWAY and SEND / AWAY; INVITE FRIENDS bottom-right |
| 02 Players, SEND greyed with reason | 9.0 | 7.0 | 8.5 | 7.5 | **8.0** | The reason line sits in the footer, far from the greyed SEND buttons, which do not say why |
| 03 History | 9.5 | 8.5 | 8.0 | 8.5 | **8.6** | Clean receipt rows, GAVE / GOT readable; item cards are picture-only and small, "+3" hides what it is |
| 04 Request card (1) | 9.0 | 9.5 | 8.5 | 9.0 | **9.0** | Reads in one glance; bright ACCEPT / DECLINE; bar; right edge lines up with the tile column |
| 05 Request stack (3) | 9.0 | 9.0 | 8.5 | 8.5 | **8.8** | Each card has its own bar, newest on top, clean 8 px gaps; the stack jumps about 75 px left when the second request arrives |
| 06 Phase 1, empty offers | 9.5 | 8.0 | 9.0 | 7.0 | **8.4** | Clean three-column window; nothing says "tap an item"; the 2:59 timer has no caption; phone card labels small |
| 07 Phase 1, 9+9, READY locked | 9.5 | 7.5 | 8.5 | 7.0 | **8.1** | The tick on each offered card covers its mutation tag; "syncing..." is the weakest label |
| 08 Phase 1, EGGS tab, READY pressed | 9.5 | 8.0 | 8.5 | 7.0 | **8.3** | Pressed READY is silver with a check, close to the disabled look; the "Waiting for" line is small grey; READY! ribbon crosses the header stroke |
| 09 Phase 2, securing | 9.0 | 7.0 | 7.5 | 6.5 | **7.5** | Anti-scam content is all there, but KG and $/s run together, names are squeezed, rows are small, and BACK is the brightest button |
| 10 Phase 2, ACCEPT countdown | 9.0 | 7.5 | 8.0 | 6.5 | **7.8** | Same row and BACK problems as 09; the lists hold 2-4 rows and are mostly empty |
| 11 Phase 2, waiting for B | 9.0 | 8.0 | 8.5 | 7.5 | **8.3** | ACCEPTED ribbon and waiting line read well; BACK is the only big live button, and it empties both offers |
| 12 Returning items + toast | 9.0 | 8.0 | 8.5 | 7.5 | **8.3** | "Returning items..." is clear; the rule under it ("add them again") is about 8 px; toast has no plate |
| 13 Done, trade complete | 9.5 | 8.0 | 7.5 | 7.5 | **8.1** | On-brand, but the receipt has no totals and both panels have dead space above the cards |
| 14 Refusal toast, "Max 9 items" | 8.5 | 7.5 | 8.0 | 7.0 | **7.8** | Red text on the floor, no plate, placed under the whole window, away from the offer it refers to |
| 15 No-window toast, "declined" | 9.0 | 8.5 | 8.5 | 7.5 | **8.4** | Clear and in the GiftToast spot; gold on the tan path has weak contrast with no plate |

Mean of the 16 scores: 8.3. Lowest: 09 at 7.5. Under 8.5: 02, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15. Passing: 00, 01, 03, 04, 05.

## Fixes for screens under 8.5

Each fix is one change. Where a fix is shared, it is written out once (under the first screen that needs it) and referenced after that.

### 02 Players, SEND greyed (8.0)
1. Move the reason line ("Finish the tutorial first") out of the footer. Put it full width, in the same red, directly under the search row and above the list. The footer keeps INVITE FRIENDS only.
2. Give each greyed SEND a small lock icon (the same lock `99673707827333` used on READY), and keep the word SEND. Right now a greyed SEND and an AWAY button differ only by their label.
3. Spec section 2 says "a disabled button always shows why". The line above the list may not meet that literally. Ask the owner: keep the line above the list, or add a short reason word to each greyed button (for example "TUTORIAL").

### 06 Phase 1, empty offers (8.4)
1. Empty-state hint: while both offers are empty, show one line centred over the empty "Your Offer" grid: "Tap a pet or egg on the left to offer it." White GothamBlack with black stroke, about 14 px at PC. Hide it once the first item is offered.
2. Caption the 2:59 pill with what runs out, for example "Idle 2:59" if this is the 3-minute idle timer from spec section 4.
3. Phone: do not add a text floor. If the emulator shows the inventory KG and $/s as unreadable, change the inventory grid from 3 columns to 2. Cards get about 50 % wider and their labels grow with them; the list scrolls more. Keep the 3x3 offer grids as they are.

### 07 Phase 1, 9+9, READY locked (8.1)
1. Move the offered tick off the card's content. Put a 14-16 px green tick in the card's top-right corner, or use a dim "IN OFFER" strip along the bottom edge. Five ticked pet cards (152K, 64.1K, 36.4K, 18.4K, 7.6K) have the tick over their mutation tag now.
2. On ticked cards, dim the picture only. KG, mutation word and $/s stay at full brightness.
3. "syncing..." under CANCEL is dim grey on slate. Use the same white label with black stroke as "2.9s Left".

### 08 Phase 1, EGGS tab, READY pressed (8.3)
1. Keep the spec's silver for pressed READY, but make its status read as waiting, not disabled. Put "Waiting for @builderman..." in the same yellow state style as "2.9s Left" (see 07 item 3 for the style). Keep the lime check.
2. The READY! ribbon crosses the top stroke of the "Your Offer" header. Move it so it sits fully inside the header bar.

### 09 Phase 2, securing (7.5)
This is the anti-scam screen. Its fixes also apply to 10 and 11.
1. **KG and $/s run together.** "152,340.5 KG$78.2M/s", "18,440 KG$20.6K/s", and on most rows on both sides. Split each row into fixed columns: name, mutation, KG (right-aligned), $/s (left-aligned), with a 6-8 px gutter between KG and $/s.
2. **Names are squeezed.** "Black Eastern Dragon" is drawn at about 70 % of the size of "Frostcrown Dragon". Give the name column more of the row. Take the width from gaps and the picture, not from the numbers. Use one name size for all rows, set by the longest name.
3. **Rows are too small.** Rows are about 27 px at PC, so the KG and $/s text is about 10 px at PC and 6.5-8.4 px on the phone (report). Width alone will not fix this, because the height limits the text too. Make rows about 36-40 px and show six per side with the list scrolling. The summary line already states the counts, so nothing is hidden. Grow the pictures with the row (from about 12-13 px to 18-20 px).
4. **The summary line reads as a minus sign.** "You give 5 pets + 4 eggs - You get 6 pets + 3 eggs -$38.3M/s". Change the separators to "You give 5 pets + 4 eggs  |  You get 6 pets + 3 eggs  |  Net -$38.3M/s".
5. **BACK is the brightest control, and it is as wide as ACCEPT**, while ACCEPT is locked. Make BACK about 30 % of the button row and ACCEPT about 70 %. Keep both colours. Once ACCEPT unlocks, it is the main action.
6. **The lists need width.** Phase 2 only needs the six phrases, so show them in one column and narrow Trade Chat in Phase 2. Give the freed width to the lists. (Hiding chat in Phase 2 also works, but spec section 3 would need a note.)

### 10 Phase 2, ACCEPT countdown (7.8)
1. Apply 09 items 1, 3, 4 and 5 (KG / $/s gutter, taller rows, summary separators, narrow BACK).
2. The lists hold 2-4 rows and leave about 60 % of each panel empty. Taller rows fix most of this. Do not pad the panels with filler.
3. Keep "ACCEPT (2.9s)" locked with its padlock. It reads correctly.

### 11 Phase 2, waiting for B (8.3)
1. Apply 09 item 5. BACK is the only live control while you wait, and it empties both offers. Make it the narrow one.
2. "Waiting for @builderman..." runs to the button's right edge. Let the text scale down with the button, or drop the trailing dots, so the name never touches the edge.

### 12 Returning items + toast (8.3)
1. "Add them again when they're back" is about 8 px at PC and carries the rule (you cannot add items yet). Raise it to the size of "4.2s Left" (about 14 px at PC) and set it on its own line under the title.
2. The toast under the window has no plate. See G4.

### 13 Done (8.1)
1. Add totals to the panel headers the way Phase 2 does: "YOU GAVE $80.4M/s" and "YOU GOT $42M/s". Add one net line above OK: "Net -$38.3M/s", red if negative, lime if positive. This is the receipt, so the numbers belong here.
2. Dead space: about 70 px of empty slate sits above the cards in both panels. Move the card rows up under the header (about 10 px gap), shorten both panels to the card height, and move OK up beneath them.
3. Keep the sunburst and the gold title as they are.

### 14 Refusal toast (7.8)
1. Put the toast on a dark slate plate with a 2 px red stroke, in the same family as the request card. Then the red text does not depend on the floor's colour.
2. Show offer refusals at the bottom edge of the offer panel they came from, not under the whole window. Keep the server's wording exactly as sent (report part 2 rule).

### 15 No-window toast (8.4)
1. Add the same plate as 14, unless the owner confirms GiftToast is plate-less and approved as it is. Gold on the tan path has the weakest contrast in the set. This is an owner call (G4).

## Wrong on every screen, or across the set

- **G1. The phone is unverified.** No phone-scale capture exists in `ui/`, and the report calls the Device-emulator pass "the real check". Every (d) score here is provisional. Capture 00, 01, 04, 06, 09 and 13 in the Device emulator before the gate.
- **G2. Phone text is small across the trade window.** Phase 1 has 45 of 100 labels under 9 px, and Phase 2 has 67 of 87 (report). I did not ask for a text floor, because the owner's rule rules that out. The fixes above change layout only where the information decides a trade (the Phase 2 rows, the tick on Phase 1 cards). Spec section 9 still says "text floors" on phones, which contradicts the owner's rule. Update section 9 so no builder chases a floor.
- **G3. Anchors cannot be verified.** The weather / boost row is missing from every capture. In 04 and 05 there is empty space under the request cards, so the 8 px gap above the row and the move to the left of the tiles cannot be checked. Get a capture with the row present.
- **G4. Toasts have no plate.** They sit on the 3D world (sky, grass, sand). The black stroke holds them up, but gold and red on tan is the weakest contrast (15, 14). Owner decision: if GiftToast has no plate, say so and I will score the toasts on that basis.
- **G5. The grey family is crowded.** Greyed SEND, AWAY, locked READY, pressed READY (silver), locked ACCEPT, Securing and Waiting are all grey. The padlock (locked) against the check (done) coding works in the window. Greyed SEND and AWAY differ only by label (see 02 item 2).
- **G6. Owner sign-off is still needed.** Spec section 9 says the menu and the trade window are shown to the owner before they are built. The builder has no owner mockup for the window. Get the owner's yes on these screens before they go in.

## Keep as it is (do not change)
- Check-UI signature: the header with the big icon over the corner, the bevelled red X, GothamBlack with black stroke, the slate windows.
- Locked = padlock and dark; done = check and silver.
- Explicit "None" for no mutation; the exact KG with commas; the Phase 2 totals and the difference line.
- The three-column window layout (inventory, offers, chat), and the request card.

## Optional polish (screens that pass)
- 03: a mutation pip on the mini cards, or a "+3 more" tap target. Not required.
- 05: keep the stack's right edge fixed to the tile column's left edge at every count, so the cards do not jump when the second request arrives (also G3).
