# Task 7 UI review 5: trading screens after fix round 4 (fresh reviewer)

**Result: 6 of 11 pass (8.5 or higher). Lowest 8.1 (phone_07, Phase 1 on the phone). Average 8.5 (8.47 over 11).**
Under 8.5: phone_00 (8.4), phone_01 (8.2), phone_07 (8.1), phone_10 (8.4), phone_lock (8.2).
On the line at 8.5: PC 07 and phone_13.

Reviewed: PC `07`, `08`, `14b`; phone `00`, `01`, `05`, `07`, `10`, `13`, `lock_shop_tap_blocked`, `admin_button_opens_panel`.
Read against `ref_shop`, `ref_rebirth`, `ref_index`, the controller rulings in the brief and `task-7-ui-review-4.md`.

## Method
- Each score is the mean of (a) look, (b) clarity, (c) layout, (d) readability, to one decimal.
- (d) is judged at each capture's own size. PC captures are read at PC size. Phone captures are read at phone size.
- Phone geometry comes from pixel checks on each capture (window edges, jump-ring edges, screen bottom), not only from the round 3 `measure` numbers. Positions below are in that capture's own pixels.
- The phone captures are the Device-emulator screenshots (iPhone 17 Pro, landscape) the brief asked for.

## Review 4 fixes
1. **Chat at a fixed size: done.** The 15 design px auto-fit is gone. On the phone, though, 15 px is now about 8.6 phone px, the smallest decision text in Phase 1 (see F4).
2. **"syncing..." says what it waits for: not met.** "Syncing offer..." says what is happening, not what the player waits for (see F5).
3. **Refusal plate sized to its text: done.** 14b passes at 8.7.

## Scores

| Image | a look | b clarity | c layout | d readability | Score | Reason |
|---|---|---|---|---|---|---|
| PC 07 Phase 1, 9+9, READY locked | 9.0 | 8.0 | 8.5 | 8.5 | **8.5** | Chat is fixed and legible at PC size. "Syncing offer..." still does not say what it waits for. On the line |
| PC 08 Phase 1, EGGS, READY pressed | 9.0 | 8.5 | 8.5 | 8.5 | **8.6** | "Waiting for @builderman..." under READY is clear and centred |
| PC 14b Refusal, "Max 9 items" | 8.8 | 8.6 | 8.8 | 8.5 | **8.7** | Plate sized to its text, centred on the title, clear of the timer and the X |
| phone_00 HUD tiles, Daily Rewards open | 9.0 | 8.5 | 7.5 | 8.5 | **8.4** | The Trading and ADMIN bottoms touch the thumbstick ring: ring top about y 595, tile bottoms about y 600 |
| phone_01 Trading menu, live click | 8.8 | 8.5 | 7.0 | 8.5 | **8.2** | Menu is centred at x 627, but the screen centre is 572. Its right edge (974) covers the left 60 % of the jump ring (915-995) |
| phone_05 request cards x3 | 9.0 | 9.0 | 9.0 | 8.8 | **9.0** | Clear of the top bar, the Eggs/Pets/Potions column and the jump ring. Name text about 15.6 phone px |
| phone_07 Phase 1, 9+9 | 9.0 | 8.0 | 8.0 | 7.5 | **8.1** | Window bottom 4 px above the screen bottom. Right edge 5-7 px from the jump ring. Chat about 8.6 phone px |
| phone_10 Phase 2, ACCEPT countdown | 9.0 | 8.5 | 8.0 | 8.0 | **8.4** | Same window edges as 07. Info line at 9.7-10.4 phone px is the smallest decision text. Net line and rows are clear |
| phone_13 Done | 9.0 | 8.5 | 8.0 | 8.5 | **8.5** | Headers at 11-12 phone px. Window bottom 3-4 px above the screen bottom. On the line |
| phone_lock Phase 1, "Finish your trade first" | 8.8 | 8.5 | 8.0 | 7.5 | **8.2** | The plate reads clearly and clears the timer and the X. Same window edges and chat size as phone_07 |
| phone_admin Admin panel opens | 8.5 | 8.5 | 9.0 | 8.2 | **8.6** | Panel is centred and clear of the ADMIN tile, top bar, jump ring and thumbstick. Minor: in the preview row the checkbox touches the colon (pre-existing). Hotbar overlap excluded by ruling |

Passing: PC 07 (8.5), PC 08, PC 14b, phone_05, phone_13 (8.5), phone_admin.
Under 8.5: phone_00, phone_01, phone_07, phone_10, phone_lock.

## Fixes (screens under 8.5)

### F1. phone_01 Trading menu (8.2)
- Centre the menu on the screen. It sits 55 px right of centre (centre 627 against 572). The Daily Rewards window in phone_00 is centred at 572.
- Cap its width at the trade window's width (about 671 px, 63 % of the screen). Today it is 693 px. Then its right edge stays left of the jump ring at x 915.

### F2. phone_00 HUD (8.4)
- Lift the whole tile grid (Shop to ADMIN) by about 20 capture px, about 14 phone px. About 55 px of free space sits between the Friends pill and the Shop tile.
- That clears the thumbstick ring with about 20 px to spare. Same grid on PC, so one layout.

### F3. Trade window edges on the phone (phone_07, phone_10, phone_lock, phone_13)
- The window starts 20 px below the top bar but ends only 3-4 px above the screen's bottom edge. Lift the window about 8 px, so the top and bottom gaps are both about 12 px.
- The window is 63 % of the screen width on the phone, so its right edge sits 5-7 px from the jump ring. Narrow the phone window to the 58 % cap (about 620 px). The PC window is already at that cap (1060 design px), so only the phone changes. That gives about 30 px of clearance to the ring.
- The inner layout (offers, phrase column, summary line) must still fit at the narrower width. Check it in Play.

### F4. Phase 1 chat log (phone_07, phone_lock; PC 07 and 08)
- 15 design px is about 8.6 phone px, the smallest decision text on the Phase 1 phone screens. Set the log to one fixed size of 17 design px with 20 px leading. Keep the stacking from the top and the oldest-line drop. Check in Play that the 8-line log still fits.
- Phase 1 only. Phase 2 has no chat log (ruling).

### F5. Status copy under CANCEL (PC 07; phone_07 and phone_lock if the line shows)
- Change "Syncing offer..." to name the subject, in the same tone as 08: for example "Syncing your offer to @builderman...".
- Keep the white, black-outline style and the box of "2.9s Left".
- This is the review 4 ask and it is not met yet.

### F6. Phase 2 info line (phone_10, 8.4)
- The info line at 9.7-10.4 phone px is the last size limit on Phase 2. Take the picture from 56 to about 46 design px, as review 4 suggested.
- Let the info line grow from 19 to about 21 design px. Check in Play that the longest line ("152,340.5 KG · METEOR + UFO · $78.2M/s") stays on one line.
- Keep the 68 px rows, the 4-row list, the summary line and no chat in Phase 2.

Fixes F2, F3 and F6 are shared with the PC layout (one layout on every device). F1 applies to any menu window on the phone.

## Keep as it is
- The Check-UI signature: gold header with the big icon, red X, GothamBlack with stroke, slate panels, 3D buttons.
- The Phase 1 compact card labels (approved; not scored).
- Phase 2: no chat, Net line and rows clear, ACCEPT 70 / BACK 30.
- 14b: the header plate is sized to its text, centred, and clear of the timer and the X.
- 05: the request cards clear the Eggs/Pets/Potions column and the jump ring.
- The Admin panel fits. The preview-row checkbox is pre-existing and needs no trading change.

## Open questions
- phone_07 shows nothing under CANCEL, while PC 07 shows "Syncing offer...". Please confirm the sync status also shows on the phone when an offer is syncing. The capture alone does not say whether this is a state or a bug.
- The hotbar drawn over the Admin panel is excluded, as the ruling says.
