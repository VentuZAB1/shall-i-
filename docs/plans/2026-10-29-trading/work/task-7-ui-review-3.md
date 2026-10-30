# Task 7 UI review 3: trading screens after fix round 2 (fresh reviewer)

**Result: 2 of 10 screens pass (8.5 or higher), both on the line (06 and 12). Lowest 7.8 (14). Average 8.3. 8 screens go back to the builder.**

Reviewed: `ui/06` to `ui/14b` (10 screens) against `ref_shop`, `ref_rebirth`, `ref_index`, the controller rulings in the brief, `task-7-ui-review-2.md`, and the "UI fix round 2" section of `task-7-report.md`. Screens 00-05 and 15 are not re-scored.

Scoring: (a) the reference look, (b) clarity, (c) layout, (d) the phone at about 0.63. Each overall score is the mean of the four, to one decimal.

**Limits of this review**
- **(d) is provisional.** `ui/` still has no 733x392 or 0.63-scale capture. Phone numbers come from the builder's `measure` table (Phase 2 name 10.4-11.1 phone px, info line 8.4-9.0, smallest tap target 42-44 px) and the 0.63 scale. Capture 06, 07, 09, 13 and 14 in the Device emulator before the ship gate (G1).
- **Phase 1 card labels (06/07) are exempt** by the controller ruling. They are not scored down or raised. The Phase 1 chat log is a different element and is scored.
- Design px is taken as roughly capture px, as in review 2 (phone = design px x 0.63).

## Scores

| Screen | a look | b clarity | c layout | d phone | Score | Reason |
|---|---|---|---|---|---|---|
| 06 Phase 1, empty offers | 9.0 | 8.5 | 8.5 | 8.0 | **8.5** | Clean three-column window; hint sits inside the empty grid; "Ends in" is captioned. Passes on the line |
| 07 Phase 1, 9+9, READY locked | 9.0 | 8.0 | 8.5 | 8.0 | **8.4** | "syncing..." under CANCEL is dim grey on slate; the chat log is five small lines with about 55 px of empty box above them |
| 08 Phase 1, EGGS, READY pressed | 9.0 | 8.5 | 8.0 | 8.0 | **8.4** | "Waiting for" is readable at 24 px, but it spans under READY and CANCEL while 07's "2.9s Left" sits under READY; same chat log as 07 |
| 09 Phase 2, securing | 9.0 | 8.5 | 8.5 | 7.5 | **8.4** | Two-line rows fix the old merged line. The info line (KG, mutation, $/s) is still about 8-9 phone px on five-row lists |
| 10 Phase 2, ACCEPT countdown | 9.0 | 8.0 | 8.5 | 7.5 | **8.3** | Same rows as 09. The "@builderman" name tag is small: its 112 px box shrinks the name |
| 11 Phase 2, waiting for B | 9.0 | 8.5 | 8.5 | 7.5 | **8.4** | ACCEPTED ribbon and waiting line read well; bubbles sit in empty list space only (correct); same row size as 09 |
| 12 Returning items + toast | 9.0 | 8.5 | 8.5 | 8.0 | **8.5** | Subtitle breaks on purpose; the plate-less toast under the window is legible on its black stroke. Passes on the line |
| 13 Done, trade complete | 9.0 | 8.5 | 8.0 | 8.0 | **8.4** | Totals and red net line work. Each panel is about 200 px tall with an 82 px card block in the middle: about 58 px empty above and below |
| 14 Refusal, long text | 8.5 | 7.5 | 7.5 | 7.5 | **7.8** | The plate sits on the bottom row of Your Offer and hides the three items under it while the refusal shows |
| 14b Refusal, "Max 9 items" | 8.5 | 8.5 | 7.5 | 8.0 | **8.1** | Short text reads well, but the plate covers the labels of two bottom-row offer cells. The capture puts it above the total, not beside it as the round 2 report says |

Mean of the 10 scores: 8.3. Lowest: 14 at 7.8. Passing: 06 and 12 (both 8.5). Under 8.5: 07, 08, 09, 10, 11, 13, 14, 14b.

## Shared fixes

Layout only. No text floor, no phone-only arrangement. Sizes are design px and are set by the box they sit in.

### Shared fix A: Phase 1 chat log (07, 08)
The chat log is not a card label, so the card-label ruling does not cover it. The card labels stay as approved.
1. The box has about 55 px of empty space above its five lines. Use it: seven lines at about 13 px with 17 px leading, bottom-anchored. Wrap a long line onto a second line rather than clip it. The column is 168 px wide.
2. Phase 1 only. Phase 2 has no chat log (ruling).

### Shared fix B: Phase 2 rows (09, 10, 11)
The info line is the anti-scam content: exact KG, mutation and $/s. At five rows it is 8.4-9.0 phone px, and the row height is what limits it.
1. Show **four rows per side** instead of five. Make each row about 62 design px tall with 6 px gaps. Four rows take 266 px of the 294 px list. Both lists scroll through all nine items. The summary line keeps the counts, so nothing is hidden.
2. Name up to 20 px. Info line up to 16 px (KG, mutation colour, $/s green, as built). Picture about 44 px. Each row keeps its own text size constraint.
   - Phone check: 62 px is about 39 phone px per row; the info line at 16 px is about 10 phone px; the name at 20 px is about 12.6 phone px. This is layout, not a floor. The row sets the size.
3. **Row height needs confirming first.** The round 2 report says 54 design px in its body, 44 "here" in its `measure` table, and the capture rows look about 46 px. Confirm which is live, then set the 62 px rows from that base.
4. **Bubble rule.** The round 2 rule was written for 54 px rows. At 62 px, a bubble fits with 0-3 rows, and 4 or more rows get the name tag on the phrase instead. Keep the rule and re-run the 0 / 1 / 3 / 4 Play cases.
5. Keep as built: panel widths, the `|` summary line, ACCEPT 70 / BACK 30, the phrase column.

## Per-screen fixes (screens under 8.5)

### 07 Phase 1, 9+9, READY locked (8.4)
1. "syncing..." under CANCEL is dim grey. Use the same gold style with black stroke as "2.9s Left". This item from review 1 is still open.
2. Shared fix A (chat log).

### 08 Phase 1, EGGS tab, READY pressed (8.4)
1. "Waiting for @builderman..." runs under READY and CANCEL (about x 643-943), while READY is about x 571-788. Give the status line the same anchor as 07's "2.9s Left", so the label does not jump when READY is pressed. Either centre both under the READY / CANCEL pair, or give both one left edge. Keep the 24 px size.
2. Shared fix A (chat log).

### 09 Phase 2, securing (8.4)
1. Shared fix B.

### 10 Phase 2, ACCEPT countdown (8.3)
1. Shared fix B.
2. The "@builderman" name tag sits on the top edge of "Deal?" in a 112 px box, so the name shrinks to fit. Make the tag wide enough for the whole name at about 14 px (about 130 px). Keep it on the phrase's top edge in the right column. It must never reach a row or the Net line.

### 11 Phase 2, waiting for B (8.4)
1. Shared fix B. YOU GET has four items, so under fix B its bubble becomes a name tag on the phrase. That is the rule working as written.
2. Bubble text: match the info line at 16 px (it is about 13 px now). Keep the bubble in the foot strip below the last row.

### 13 Done, trade complete (8.4)
1. **Dead space.** Each panel is about 200 px tall, and the card block is about 82 px in the middle, so about 58 px sits empty above and below. Keep the window size (the same as Phase 2). Move each card block up to the top of its panel, about 12 px under the header. Under the cards, add one line at 16 px: "2 pets + 1 egg" for YOU GAVE and "3 pets + 1 egg" for YOU GET. These are the same counts as the Phase 2 summary, so the panel gains real information rather than padding.
2. Keep the sunburst, the gold title, the header totals, and the Net line over OK (red / lime, 21 px).

### 14 Refusal, long text (7.8) and 14b Refusal, "Max 9 items" (8.1)
**Shared fix C: the refusal plate moves to the window header title.** The plate now covers offer row 3: 14 hides the whole row, and 14b hides the labels of two cells. A player cannot see the items it hides while it shows.
1. Put the in-window refusal plate on the gold header, centred over the title "Trading with @builderman". Use one line at 16 px. The long text (about 340 px) fits inside the 448 px title span. Keep the dark slate plate, the 2 px red stroke and the server's wording.
2. It must not cover the "Ends in" pill or the X. Covering the partner's name for a few seconds is fine. The Phase 2 no-room toast already uses the header title this way.
3. Result: no offer cell is covered, and the total row is never touched.
4. 14b: the capture shows "Max 9 items" above the total, not at its left as the round 2 report describes. Check which branch runs. The header placement makes the branch moot.

## Across the set
- **G1. The phone is still provisional.** Capture 06, 07, 09, 13 and 14 at 733x392 in the Device emulator before the ship gate.
- **G2. Row heights disagree in the round 2 report** (54 in the body, 44 in the `measure` table). Fix B depends on which one is live.
- **G3. Fix B is a controller call only if it is contested.** It is a layout choice under the no-text-floor ruling: four taller rows instead of five. If the controller keeps five rows, the info line stays at about 9 phone px and 09 / 10 / 11 stay near 8.4.
- **G4. The bubble and name-tag rule** was written for 54 px rows. Re-run the 0 / 1 / 3 / 4 Play cases after fix B.

## Keep as it is
- Check-UI signature: the gold trade header with the big icon, the red X, GothamBlack with black stroke, slate panels, bright 3D buttons.
- Phase 1 card labels in 06 and 07 (approved by ruling; not raised here).
- Phase 2: ACCEPT 70 / BACK 30; the summary line with `|` separators; Net in red / lime; ACCEPTED and READY! ribbons inside the header bars; the "Waiting for" line in 11.
- Name tag on the phrase and bubbles only in empty list space (10, 11). No chat over a row or the Net line.
- 12: the plate-less toast under the window (ruling) and the broken subtitle.
- 14 / 14b: the plate styling (dark slate, red stroke). Only its position changes.

## Optional polish (screens that pass)
- 06: enlarge the empty-state hint in the empty 3x3 grid to about 18 px over three lines. It is the only instruction on the screen.
- 12: no change needed.
