# Visual review: HATCH NIGHT Starter Pack popup + Shop (2026-10-21)

Reviewer: visual reviewer, read-only. I made no game changes and ran no Play. In Edit I only read the source with `script_read` / `script_grep` (`ShopClient`, `StarterPackClient`, `BrickUI.Hatch`) so the fixes below can cite real lines.

**What I looked at:**
- All 37 build shots in `hatch-night-build/popup_shop/`.
- The mockups in `style-2026-10-21/popup_shop/` and `qa_report.txt`.
- The plan, its review, the builder's ledger (`progress.md`) and the spec.
- The Gift window shots and its visual review.
- My own PIL crops and measurements, saved in `hatch-night-build/popup_shop/review/` (`z_*.png`).

**Scale used for measurements:**
- Shop shots: window s = 1.2041 (ledger).
- Popup: 1.178. The pink band is 872 px for 740 logical, the same as the mockup's 871 px.

## Verdict: **FIX THEN SHIP**

**Close to the mockups overall.**
- The popup matches `popup_pc.png` element for element in all 5 states.
- The Shop matches `shop_*_pc.png` in layout, rail, section headers, cards and gold CTAs.
- Rebirth, Index and Settings are unchanged. The Gift window is unchanged too: the gift snapshot AFTER equals BEFORE.

**Owner's hard rules:**

| Rule | Result |
|---|---|
| Timers have no background | Pass: popup ENDS IN and the Shop card's "LEFT" |
| Shop stays big on PC | Pass: 891 x 566 now, 906 x 566 before (`shop_before_after.jpg`) |
| Egg odds visible before any purchase | Pass: the Shop card's BUY only opens the popup |
| Only the main action pulses | Pass: only the popup BUY and the Shop Starter BUY have `pulseAmp`, and they are never on screen together |
| Nothing rotated hangs over an edge | Pass |
| Nothing hovers over text | Pass |

**What stops sign-off:** two "cramped / basic" items of exactly the kind the owner complains about.

---

## MUST

### 1. Potion pack titles overfill their box and outshout the price
- **Shots:** `shop_potions.jpg`, `shop_refusal.jpg`, `shop_phone_potions.jpg`; crop `review/z_potion_titles.png`.
- **What's wrong:**
  - The titles read "MONEY POTION", "HATCH POTION" and "SPEED POTION" at 22.
  - Measured ink width is 186 px, which is 154 logical, in the 174 Title box. That is **91 % of box minus stroke**. The rule is 83 %.
  - They are the widest and loudest text in the Shop. The price "25" below them looks smaller: same cap height, a third of the width.
  - Plan 4.7 and `shop_potions_pc.png` say the title is the short potion name: MONEY, HATCH, SPEED.
- **Change:** `ShopClient` line 361: `string.upper(kind and kind.name or pk.potion)` becomes **`string.upper(pk.potion)`**. The fill drops to about 45 %.
- **Test:** the containment `textFits` check let a 91 % line pass. Tighten it to the plan's 83 % of (box - 2 x stroke) for every `H.text`, not only `H.fit` labels. Then re-run S2.

### 2. The gift picker is a tall, mostly empty panel (your note: yes, it should fit its content)
- **Shot:** `shop_gift.jpg`; crop `review/z_gift_row.png`.
- **What's wrong:**
  - With 1 player, the 420 x 386 Box uses 76 logical of its 307-tall list. About 70 % of the panel is empty navy.
  - SLINGSHOT servers usually hold 1-3 players, so 0-2 rows is the normal case, not an edge case.
  - It reads as unfinished: the owner's "basic".
- **Change (`ShopClient`):** add `fitPicker(n)` and call it at the end of `buildPicker` (after line 748).
  - Size:
    - `rowsH = math.min(307, 8 + 68 * math.max(n, 1))`
    - `Hb = 79 + rowsH`, where 79 = list top 66 + bottom pad 8 + depth 5
    - Results: n = 0 or 1 -> **155**, 2 -> **223**, 3 -> **291**, 4 -> **359**, 5 or more -> **386** (scrolls, as now).
  - Box position: centred in the page body, at `(160, 66 + (386 - Hb) / 2)`.
  - Resize the shellCard parts (built at h = 386, line 431):
    - holder / Dim / Badges / Sink height = `Hb`;
    - Side / Face / HoverFx / Icons height = `Hb - 5` (Side keeps y 5);
    - Pop centre `(210, (Hb - 5) / 2)`, height `Hb - 5`;
    - `pPlayers.Size = (404, rowsH)`.
  - Empty state: move `Empty1` from y 160 to **80** and `Empty2` from 184 to **104** (line 473 and the next line), so they sit inside the 155 box.
- **Test:** re-run S6 at 1 row and at 8 fake rows, and add a 0-row run, at native and 0.7106. The Close X and every row must be inside the Box. `PickerConns` must stay 0 after close.

---

## SHOULD

### 3. Restricted popup: a dead band above and below the 2 reward rows (your note: confirmed)
- **Shots:** `popup_restricted.jpg` vs `popup.jpg`; crop `review/z_restricted.png`.
- **What's wrong:**
  - It matches the mockup (`popup_restricted_pc.png` has the same gaps), but the frame is built for 3 rows + odds and shows 2 rows.
  - There are 87 logical px of nothing between the teeth (62) and PotionRow (149), and 95 px between CashRow's bottom (289) and the buttons (384).
  - The hero sits at centre y 220 instead of 196, so it reads low.
- **Change (preferred):** cut the 96 px odds band out of the restricted window's height; the width stays the same.
  - Face 463 -> **367**; holder 470 -> **374**. Keep fitWindow's scale s; the holder size becomes `(740 s, 374 s)`.
  - Buttons y 384 -> **288**.
  - Rows: PotionRow y 149 -> **101**, CashRow y 223 -> **175** (`StarterPackClient` lines 282-283).
  - Hero centre (155, 220) -> **(155, 184)** (line 273).
  - Clearances: PotionSpeed 103..167 sits 8 px under the ENDS IN stroke (95); the potions' bottom 267 sits 21 px above the buttons.
  - `refreshPopup()` must call `refit()`. B23 flips the policy while the popup is open, and the window must grow back to 470 live when the odds return.
- **Fallback (only if `windowChrome` cannot take a height):** keep 740 x 470 and use 2 big rows:
  - rows 412 x 140 at y **70 / 222**;
  - icon 96 at (12, 22);
  - Line1 @28 at (124, 36, 276, 28);
  - Line2 @20 at (124, 72, 276, 22).
- **Test:** re-run P2 at native and 0.7106, B16, and B23.

### 4. Tier-1 treadmill: the lone $10K button breaks the right edge of the buttons
- **Shot:** `shop_bottom.jpg`; crop `review/z_tread_eggs_align.png`.
- **What's wrong:**
  - Every new player sees this state (`TreadmillRobuxHidden = {[2] = true}`).
  - The lime button is 112 wide at x 452. Every other wide card's button is 160 at x 404. On screen the left edges are 1022 px vs 965 px.
- **Change:**
  - Add `moneyWide = H.priceButton(f, "MoneyWide", 404, 32, 160, 54, {d = 4, r = 12, glyph = 30, size = 28, pal = "lime"})`. Wire it to `handlers.TreadMoney`.
  - When `hideRobux`, show `moneyWide` and hide `money`. Write the "$" word into whichever is visible.
  - Delete the position move at line 842.

### 5. Treadmill MAX: "MAX" twice and a floating label
- **Shot:** `shop_states_bottom.jpg`; crop `review/z_tread_max.png`.
- **What's wrong:**
  - The card shows "x1 MAX" and also "MAX LEVEL" floating in the empty button area.
  - Double Speed's MAX uses a silver pill (`shop_states.jpg`).
- **Change:**
  - Hide `MaxText` (line 389).
  - When maxed, show `moneyWide` (item 4) with `setWord("MAX", "silver")` and `face.Active = false`, exactly like Double.
  - Keep the gold "xN MAX" in Now.

### 6. Make the price the biggest text on the small cards (boosts + packs)
- **Shots:** `zoom_boosts_best_value.png`, `zoom_packs_best_value.png`.
- **What's wrong:** the Title (@22: "+101M", "3 POTIONS", "MONEY") ties the price (@22). Plan D9 and the acceptance test say the price is the biggest text on every card.
- **Change:**
  - Boost and pack `Title` TextSize 22 -> **20**, box unchanged (6, 88/90, 174, 22).
  - Don't raise the price instead: 24 + stroke in the 29-tall face is cramped.

### 7. The x2 MONEY pass card reads grey, like a disabled card
- **Shot:** `shop_top.jpg`.
- **What's wrong:**
  - The 15 % gold tint (line 277, `H.CARD.top:Lerp(tint, 0.15)`) neutralises the violet.
  - The Money face samples (82, 70, 120), saturation 0.42. Growth is (83, 56, 135), saturation 0.59, and VIP is 0.62.
- **Change:** no face tint for `Money2x`: grad top = `H.CARD.top`. Raise its Glow to 0.3 transparency (from 0.4) so the gold identity comes from the glow.

---

## NICE

8. **ENDS IN (your note):** the placement matches the mockup.
   - Centre x: 155.0 logical vs the mockup's 154.6. Top y: about 79 vs 76 from the band top.
   - It looks smaller because GothamBlack caps are about 17 % shorter than the mockup font: 15 px vs 18 px. Every label shows the same shrink (row titles 15 vs 18), so this is not a bug.
   - For more urgency: `EndsIn` @**24** at (10, 67, 290, 24). That is 62 % fill, and the stroked bottom 94 stays 5.7 px above the Cash sticker (99.7).
9. **Thanks state (`popup_thanks.jpg`):** NO THANKS is hidden, so OWNED! sits right-aligned with an empty left third. Span it across **(10, 384, 720, 60)** for the 1.6 s it shows.
10. **OFFER ENDED (`popup_error.jpg`):** the button says OFFER ENDED while the timer still reads 29:33. For that one refusal, hide `EndsIn` while it shows.
11. **Popup header icon:** the STAR burst's red sparks almost vanish on the magenta band (`review/z_popup_header.png`). Give it the ink drop shadow the stickers use, or use the plain gold star from the mockup.

**Not this build (already reported by the builder):**
- The left HUD is a different size across sessions, e.g. `gift_after.jpg` vs `shop_top.jpg`.
- Cause: the Check-UI deviceScale start-up race.
- Keep it on the bug list.

---

## What's good
- The popup is a faithful, juicy match.
  - The magenta band and teeth, the hero sticker stack with rays and glow, three clean reward chips, the readable 5-cell odds strip (secret silhouette + gold "?"), and the fat gold BUY.
  - All 5 states (normal, urgent red timer, refusal, thanks, restricted) behave as planned.
- The Shop reads premium.
  - The in-window rail with a lime pill, section headers with a colour code, frameless stickers with soft glows, and gold price buttons everywhere.
  - Contained BEST VALUE tags, OWNED / MAX silver pills, and refusal words that fit.
- The phone layouts at 0.7106 hold up (`popup_phone.jpg`, `shop_phone_*.jpg`).
- Engineering is solid.
  - Tests are green, there are no leaks, and the refresh costs about 0.1 ms.
  - Untouched windows were proved byte-identical, and the legacy fallback was kept.
