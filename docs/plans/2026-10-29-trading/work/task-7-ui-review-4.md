# Task 7 UI review 4: trading screens after fix round 3 (fresh reviewer)

**Result: 5 of 8 screens pass (8.5 or higher). Lowest 8.4 (07, 08, 14b). Average 8.49. Three screens go back to the builder: 07, 08 and 14b.**

Reviewed: `ui/07`, `08`, `09`, `10`, `11`, `13`, `14` and `14b` (the Phase 1, Phase 2, Done and refusal screens). Read against `ref_shop`, `ref_rebirth` and `ref_index`, the controller rulings in the brief, `task-7-ui-review-3.md` and the "UI fix round 3" section of `task-7-report.md`. Screens 00-06, 12 and 15 are not scored here.

Scoring: (a) the reference look, (b) clarity, (c) layout, (d) the phone. Each screen score is the mean of the four, to one decimal. (d) comes only from the measured sizes in the round 3 report.

**Limits of this review**
- **(d) is provisional.** The measured sizes come from the `measure` op on the 58 px top bar. The 36 px bar gives slightly larger numbers, so it would not lower any (d) score. The 733x392 Device-emulator capture (review G1) still decides the final (d).
- **Phase 1 card labels are exempt** by ruling. The Phase 1 chat log and the status lines are not card labels, so they are scored.
- **(d) reasoning for Phase 2.** The layout holds at 0.63: every tap is 42 px or more, and the round 3 check found 0 overlaps in 882 rectangle tests. The binding phone sizes are the info line (9.7-10.4 px) and the name tag and bubble (9.1-9.7 px). Under the no-floor ruling I did not score these as a size problem. They are scored as a layout limit, because the 68 design px row and the 294 design px list set them. Phase 2 (d) is therefore 8.0, not lower.

## Scores

| Screen | a look | b clarity | c layout | d phone | Score | Reason |
|---|---|---|---|---|---|---|
| 07 Phase 1, 9+9, READY locked | 9.0 | 8.0 | 8.5 | 8.2 | **8.4** | Chat log text changes size as lines fill (17 px at 5 lines, down to 15 px at 8). "syncing..." does not say what it waits for |
| 08 Phase 1, EGGS, READY pressed | 9.0 | 8.0 | 8.5 | 8.2 | **8.4** | Same chat log as 07. The two-line "Waiting for" status under READY is right and is centred |
| 09 Phase 2, securing | 9.0 | 8.5 | 8.5 | 8.0 | **8.5** | Four taller rows with a scrollbar. Info line (KG, mutation, $/s) is the smallest decision text on the screen |
| 10 Phase 2, ACCEPT countdown | 9.0 | 8.5 | 8.5 | 8.0 | **8.5** | Same rows as 09. The name tag sits on the top edge of "Deal?" as the rule requires; its text is 14 px where it could reach 18 |
| 11 Phase 2, waiting for B | 9.0 | 8.5 | 8.5 | 8.0 | **8.5** | ACCEPTED ribbon and the "Waiting for" line read well. The bubble sits in empty list space under the 3 YOU GIVE rows (correct) |
| 13 Done, trade complete | 9.0 | 8.7 | 8.5 | 8.2 | **8.6** | Dead space is gone. Headers carry the counts and $/s. Panels are unequal heights, which is acceptable |
| 14 Refusal, long text | 8.8 | 8.5 | 8.8 | 8.2 | **8.6** | The plate sits on the header title only. No offer cell, total or timer is covered (plate right edge 887, timer left edge 897) |
| 14b Refusal, "Max 9 items" | 8.8 | 8.5 | 8.0 | 8.2 | **8.4** | Same plate, always the full 552 design px wide. Two words sit in an empty dark bar |

Mean of the 8 scores: 8.49. Lowest: 8.4 (07, 08, 14b). Passing: 09, 10, 11, 13, 14. Under 8.5: 07, 08, 14b.

Screens 09, 10 and 11 pass only on the line. The owner's floor is 8.5 and the aim is 9+, so the optional fixes below are worth doing.

## Shared fix A: Phase 1 chat log (07, 08)

The chat log is not a card label, so the card-label ruling does not cover it.

1. Use one fixed size for every state: 15 design px, with 18 px leading. The round 3 log already fits 8 lines at 15 px. Remove the 15-20 px auto-fit, so the text does not change size as lines arrive.
2. Keep the top-stacked order, the wrap of long lines onto a second line, and the rule that the oldest line drops at 8.
3. Expected result: (b) goes to 8.5 and the screen to about 8.6. The phone numbers stay as they are (8.4-9.1 px).
4. Phase 1 only. Phase 2 has no chat log (ruling).

## Per-screen fixes (screens under 8.5)

### 07 Phase 1, 9+9, READY locked (8.4)
1. Shared fix A (chat log).
2. Optional copy fix, not scored: "syncing..." under CANCEL names no subject. Say what it waits for, in the same tone as 08's "Waiting for @builderman...". The style (white with black stroke, same box as "2.9s Left") is right and should stay.

### 08 Phase 1, EGGS tab, READY pressed (8.4)
1. Shared fix A (chat log).
2. Nothing else. The status line under READY is centred, and the READY! pill in the header is clear.

### 14b Refusal, "Max 9 items" (8.4)
1. **Size the in-window plate to its text.** The plate now always spans the full 552 design px of the title span, so "Max 9 items" sits in a wide empty dark bar. Give it a minimum width of about 280 design px and a width that follows the text plus padding, capped at 552. Keep it centred on the title's centre, at the header's vertical centre, with the same slate fill and 2 px red stroke. Keep it inside x 132-684, so it never reaches the timer pill (x 696) or the X.
2. Keep the long-text case as built: 14 uses the full span and wraps to two lines if it must.
3. Expected result: (c) goes to about 8.5-8.8 and the screen to about 8.6.

## Optional fixes (screens at 8.5, to reach 9)

These are not required for the bar. They are the only remaining levers.

**09, 10, 11: the info line is the last (d) limit.**
- The info line is the anti-scam content and sits at 9.7-10.4 phone px. The row is 68 design px and the list is 294. Test a wider text column: take the picture from 56 design px to about 46, so the longest entry, "152,340.5 KG · METEOR + UFO · $78.2M/s", has room at 21 design px. Keep 68 px rows and the same 4-row list. Confirm with a Play check that the longest entry does not wrap or reach the picture.
- Keep it on one line. Do not split the info line into two lines unless the row height is raised, because the list cannot take it.

**10, 11: the name tag is small.**
- The tag text is 14 design px, limited by the 128 px box. Let the tag use the full phrase width (132 px) with minimal padding, so "@builderman" can reach 18 px.
- It stays on the top edge of the phrase, never over a row or the Net line (security ruling).

**13 (optional, keep as is).** Unequal panel heights fit the card counts. Equal heights would add empty space, which the round 2 review asked to remove. Keep.

## Keep as it is
- The Check-UI signature: the gold trade header with the big icon, the red X, GothamBlack with black stroke, slate panels, and bright 3D buttons.
- Phase 1 card labels in 06, 07 and 08 (approved; not scored).
- Phase 2: ACCEPT 70 / BACK 30, the summary line with `|` separators, Net in red and lime, the ACCEPTED and READY! ribbons, and the "Waiting for" line in 11.
- Bubbles appear only in empty list space (11). Name tags sit on the phrase (10, 11). No chat over a row or the Net line.
- 14 and 14b: the plate is on the header title only, and its style (dark slate, red stroke) stays. Only its width changes in 14b.
- 13: the sunburst, the gold title, the header counts with $/s, the Net line (21.4 phone px) over OK.

## Across the set
- **G1. The phone is still provisional.** Capture 07, 09, 13 and 14 at 733x392 in the Device emulator before the ship gate.
- **G2. The row-height numbers now agree** (68 design, 56 here, 36.2 phone). The round 2 disagreement is closed.
- **G3. Fix A and fix 14b are the only changes needed to clear the bar.** After them, 07, 08 and 14b should land around 8.6. If the owner wants 9+ on Phase 2, the optional info-line and name-tag fixes are the route.
