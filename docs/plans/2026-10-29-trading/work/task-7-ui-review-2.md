# Task 7 UI review 2: trading screens after fix round 1 (fresh reviewer)

**Result: 7 of 16 screens pass (8.5 or higher). Lowest 7.6 (09 and 10, tied). Average 8.4. 9 screens go back to the builder.**

Reviewed: `ui/00` to `ui/15` against `ref_shop`, `ref_rebirth`, `ref_index`, the rules in `task-7-ui-review-1.md`, the "UI fix round 1" list in `task-7-report.md`, and the controller rulings in the brief.

Scoring: (a) the reference look, (b) clarity, (c) layout, (d) the phone at about 0.63. Each overall score is the mean of the four, to one decimal.

**Limits of this review**
- **(d) is provisional.** `ui/` still has no 733x392 or 0.63-scale capture. Phone numbers come from the builder's measured phone sizes in `task-7-report.md`. Design px is taken as roughly capture px (the trade window is about 890 px wide); phone = design px x 0.63. Confirm in the Device emulator before the ship gate.
- Owner sign-off is not scored here (controller ruling).

## Scores

| Screen | a look | b clarity | c layout | d phone | Score | Reason |
|---|---|---|---|---|---|---|
| 00 HUD: Trading tile + ADMIN | 9.5 | 9.0 | 9.0 | 8.5 | **9.0** | Same tile grid as the approved refs; Trading and ADMIN take their slots; labels read |
| 01 Trading, Players | 9.0 | 9.0 | 8.5 | 8.5 | **8.8** | Check-UI header with the big icon, bright tabs, ONLINE / AWAY and SEND clear; footer is mostly empty |
| 02 Players, SEND greyed | 9.0 | 8.5 | 8.5 | 8.0 | **8.5** | Reason moved above the list (ruling met); padlock on each greyed SEND. Borderline pass |
| 03 History | 9.0 | 8.0 | 8.5 | 8.5 | **8.5** | Clean GAVE / GOT rows; mini cards are picture-only and "+3" does not say what it hides. Borderline pass |
| 04 Request card (1) | 9.0 | 9.5 | 8.5 | 9.0 | **9.0** | Read in one glance; big ACCEPT / DECLINE; weather row present, card sits 8 px above it |
| 05 Request stack (3) | 9.0 | 9.0 | 8.5 | 8.5 | **8.8** | Clean stack with 8 px gaps; its right edge differs from the single card (polish, below) |
| 06 Phase 1, empty offers | 9.5 | 8.0 | 9.0 | 7.0 | **8.4** | Hint line and "Ends in" pill work; inventory KG and $/s are 6-8 phone px |
| 07 Phase 1, 9+9, READY locked | 9.5 | 7.5 | 8.5 | 7.0 | **8.1** | Tick now off the text; offer and inventory labels small; chat log lines about 8 px |
| 08 Phase 1, EGGS, READY pressed | 9.5 | 8.0 | 8.5 | 7.0 | **8.3** | Pressed READY reads as done; "Waiting for @builderman..." is visibly smaller than "2.9s Left" in 07 |
| 09 Phase 2, securing | 9.0 | 7.0 | 8.0 | 6.5 | **7.6** | Name, KG and $/s share one 10-11 px line on about 40 px rows; KG and $/s run close with no divider |
| 10 Phase 2, ACCEPT countdown | 9.0 | 7.5 | 7.5 | 6.5 | **7.6** | Same rows as 09; 3-4 items leave a third to a half of each panel empty |
| 11 Phase 2, waiting for B | 9.0 | 8.0 | 8.0 | 7.5 | **8.1** | ACCEPTED ribbon now fits the header; wait line fits; bubble on YOU GIVE only; rows as in 09 |
| 12 Returning items + toast | 9.0 | 8.0 | 8.5 | 8.0 | **8.4** | Overlay clear; subtitle wraps mid-rule; the window-open toast is gold on tan with no plate |
| 13 Done, trade complete | 9.5 | 8.5 | 8.0 | 7.5 | **8.4** | Totals and net line added; YOU GAVE panel is mostly empty under one row of cards; net figure small |
| 14 Refusal toast, "Max 9 items" | 9.0 | 8.5 | 8.0 | 7.5 | **8.3** | Plate sits on the offer's bottom edge with a red 2 px stroke; it hides the Your Offer $/s total |
| 15 No-window toast, "declined" | 9.0 | 8.5 | 9.0 | 8.0 | **8.6** | GiftToast spot, plate-less per the ruling; gold on tan still readable |

Mean of the 16 scores: 8.4. Lowest: 09 and 10 at 7.6. Under 8.5: 06, 07, 08, 09, 10, 11, 12, 13, 14. Passing: 00, 01, 02, 03, 04, 05, 15.

## Fixes for screens under 8.5

Layout only. No text floor, no phone-only arrangement, no 2-column inventory. Sizes are design px.

### Shared fix A: Phase 1 card labels (06, 07, 08, 13)
The inventory cards are about 70 px wide, with KG, mutation and $/s packed into one block at 8-9 px.
1. Widen the inventory column from about 230 to about 290 px. Take 30 px from each offer column (216 to 186; the 3x3 cells stay about 58 px). Chat stays at 168. The total still fits the 882 px window.
2. Inventory card about 92 px wide (3 across, 4 px gutters). Picture on top (about 40 px), mutation as a small pill on the picture's top-left corner, then KG and $/s each on its own line at 11 px (was about 8.5).
3. Use the same card layout for the 9 offer cells.

### 06 Phase 1, empty offers (8.4)
1. Apply shared fix A.
2. Keep the hint line and the "Ends in" pill as built.

### 07 Phase 1, 9+9, READY locked (8.1)
1. Apply shared fix A to inventory and offer cards.
2. Keep the offered tick in the picture's top-right corner, never over a text line.
3. Chat log (Phase 1 keeps it): raise lines from about 8 px to 11 px with 14 px leading, and show the last 6 lines instead of 8. Spec section 3 needs a note for 6 lines.

### 08 Phase 1, EGGS tab, READY pressed (8.3)
1. Apply shared fix A to the egg cards (KG line at 11 px).
2. Set "Waiting for @builderman..." to the same 14 px gold as "2.9s Left" in 07. It must fit the READY button's width (about 218 px). If it does not fit on one line, wrap it to two lines or drop the trailing dots. Do not shrink it below the "2.9s Left" size.

### Shared fix B: Phase 2 rows (09, 10, 11)
The builder's one-line rows hit their width limit (report concern 1). Use two-line rows in the same panels and window size.
1. Row pitch 46 px (about 40 px now). Five rows show per side and the list scrolls. Picture 30 px (about 20 px now).
2. Line 1: name at 16 px, one size for every row (set by the longest name, "Black Eastern Dragon"). Mutation as a coloured pill at the right end of line 1, 10 px ("METEOR + UFO" fits one line in an about 80 px pill).
3. Line 2: exact KG at 13 px in a fixed 120 px column, then $/s at 13 px in a fixed 90 px column, both left-aligned. The columns line up down the list.
4. Unchanged: panel widths (about 365 px), the summary line, ACCEPT 70 / BACK 30, and the chat column.
Check: the name at 16 px (about 190 px) plus the pill (about 80 px) is about 270 px, inside the about 317 px text area.
Phone: a 46 px row is about 29 phone px. Names become about 10 phone px and numbers about 8 phone px (now 7-8 for both). Still small, but the row height is what the layout allows without a floor.

### 09 Phase 2, securing (7.6)
1. Apply shared fix B.

### 10 Phase 2, ACCEPT countdown (7.6)
1. Apply shared fix B.
2. Dead space: 3-4 items leave a third to a half of each panel empty. Do not pad it. Reserve a 36 px bubble strip at the foot of each list in every Phase 2 state (the strip 11 already uses). It stays empty when no one speaks and holds the bubble when a line arrives. Row size does not change with the item count.
3. Keep "ACCEPT (2.9s)" with its padlock as built.

### 11 Phase 2, waiting for B (8.1)
1. Apply shared fix B.
2. Give YOU GET the same bubble strip as YOU GIVE, so both panels share a foot. Set the bubble text to 13 px to match line 2.
3. Keep as built: the ACCEPTED ribbon inside the header, the "Waiting for @builderman..." line, and BACK at 30 %.

### 12 Returning items + toast (8.4)
1. The subtitle "Add them again when they're back" wraps mid-rule ("when / they're back"). Break it on purpose at 14 px: "Add them again" on one line and "when they're back" on the next, both centred over the grid.
2. The toast under the open window is gold on the tan floor, the weakest contrast in the set after 15. The no-plate ruling covers toasts with no window. This toast has a window open, so the controller should rule on it: keep it plate-less (no change), or give it the offer-refusal plate (dark slate, 2 px gold stroke) in the same spot. I scored it on legibility either way.

### 13 Done, trade complete (8.4)
1. YOU GAVE has 3 cards on one row and about 60 % of its panel empty. Enlarge the receipt cards from about 84 to about 100 px (still 3 per row) and centre each side's card block vertically in its panel instead of top-aligning it.
2. "Net -$42.1M/s" is the outcome figure. Set it at 16 px (now about 12), keep red / lime, and centre it over OK.
3. Card labels: apply shared fix A (KG and $/s on their own lines at 11 px).
Keep the sunburst, the gold title and the header totals.

### 14 Refusal toast, "Max 9 items" (8.3)
1. The plate covers the whole Your Offer total row, so the $/s total disappears while the refusal shows. Make the plate only as wide as its text (about 120 px for "Max 9 items" at 14 px) and place it at the left of the total row. The $/s total stays on the right of the same row.
2. Keep the dark slate plate, the 2 px red stroke and the server's wording.

## Across the set
- **G1. The phone is still provisional.** No 733x392 capture is in `ui/`. Capture 06, 07, 09 and 13 in the Device emulator before the ship gate.
- **G2. Phase 1 card labels (06, 07, 08, 13).** Shared fix A is layout only and is the largest single gain in the set.
- **G3. Phase 2 rows (09, 10, 11).** Shared fix B: two-line rows at the same window size. One line of text cannot reach a readable size in a 40 px row.
- **G4. Empty list space (10, 11, 13).** Fill it with the bubble strip, not with padding. Centre the receipt cards on 13.
- **G5. Plate ruling for window-open toasts (12).** Needs the controller's call. The no-plate ruling holds for 15.
- **G6. Anchor jump (04 and 05).** The single request card's right edge is at the boost row (about 1505 px); the stack's is at the tile column (about 1430 px). The cards move about 75 px when the second request arrives. This is not a fail, but it is layout (polish below).

## Keep as it is
- Check-UI signature: the checker header with the big icon, the red 3D X, GothamBlack white with a black stroke, slate panels, bright 3D buttons.
- The one red reason line above the list (02), with the padlock on each greyed SEND.
- Locked = padlock and dark; done = check and silver.
- ACCEPT 70 / BACK 30; the Phase 2 summary line with "|" separators and the red / lime net.
- Phase 2 has no chat log; chat shows as bubbles only.
- READY! and ACCEPTED ribbons sit inside the header bars.
- The offer-refusal plate (14) and the plate-less no-window toast (15).
- The request card (04) and stack (05) styling.

## Optional polish (screens that pass)
- 02: give the red reason line its own 8 px band above the first row; enlarge the padlock to about 24 px.
- 03: "+3" to "+3 more", or mutation pips on the mini cards. Not required.
- 04 and 05: pick one anchor for every count. Suggest the tile column's left edge (about 1430 px) for both, so the cards do not jump when the second request arrives.
