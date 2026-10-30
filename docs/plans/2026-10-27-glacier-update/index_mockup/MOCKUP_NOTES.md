# Index mockup for the Glacier update (2026-10-28), v2

**Owner rule:** "you can make the pets index to be on two rows if needed, no need to make it this small".

This mockup is the live Index in Studio, re-laid out on the client only (nothing saved; Play was stopped after the capture). The new pets' portraits were pasted in with `compose.py`, because they aren't uploaded yet.

**Files:**
- `INDEX_MOCKUP_v2.png`: the mockup
- `capture_glacier_tab_v2.jpg`: the raw capture
- `compose.py`: the paste script

**Note:** the Studio viewport was only 744 px wide. On a PC the window is about 1.7x bigger.

## Layout (IndexPage scale coords; to build in S2 after the owner approves)

**Window:**
- MenuController LAYOUT Index aspect 1.75 → **1.42**, so the page is taller.
- Header 0.18 of the face (was 0.2247). Title, Icon and Close are scaled ×0.8 in y.
- Body size (0.9226, 0.775) at y 0.5775.

**Tabs:**
- 7 tabs, size (0.125, 0.112).
- y = 0.062 + (i-1) × 0.122. The selected tab gets +0.008 x.

**Header:** (0.545, 0.14) at (0.415, 0.075).

**Cards: 2 rows × 3.**
- w = (0.545 - 0.008 - 2 × 0.011) / 3 = 0.1717; h = 0.28.
- x = 0.1425 + 0.004 + w/2 + col × (w + 0.011).
- y = 0.16 + h/2 + row × (h + 0.012).
- Inside each card:

  | element | position / size |
  |---|---|
  | Name | y 0.10, h 0.13 |
  | badge | y 0.215 |
  | View | (0.94, 0.56) at y 0.54 |
  | Chance pill | (0.5, 0.13) at y 0.885 |

- **Portrait crop:** crop the new portraits to their bounding box before upload. The old 512 px squares have big margins and would look tiny in the shorter cards; re-crop the old ones too if they look small.

**Badges and colours:**
- **SECRET:** gold card + pink SECRET badge (as now).
- **MYTHIC:** the Check-UI Day-7 RAINBOW spectrum on the card (rotation 45) and on the badge, with the text "MYTHIC".
- Glacier colours: (200, 240, 255) → (60, 120, 220).

**Rules (owner decisions):**
- The mythic is a BONUS card: it counts in x/6, but the area claim needs only the non-mythic cards.
- `areaComplete` skips `c.mythic`.
- Every egg gets 6 cards.
- The Fire, Celestial and Glacier tabs each show one MYTHIC card: Cinder Overlord, Eclipse Seraph and Frostcrown Dragon.

**Unchanged:** the reward strip, the bottom bar and the inspect panel.

## Full-screen captures (the owner made Studio full screen; viewport 1519 × 753)
- **v3:** `INDEX_MOCKUP_v3_fullscreen.png`. Today's window size (Size 0.6458 × 0.8148) with the aspect changed to 1.42. The window is 704 × 496 px, and each card is about 108 × 100 px.
- **v4:** `INDEX_MOCKUP_v4_bigger.png`. A BIGGER window, about 1.4× the cards of v3. Each card is about 155 × 128 px, and the window is 1001 × 646.
  - Window: Size (0.9, 0.93), aspect 1.55.
  - Header: 0.15 of the face; Title, Icon and Close y × (0.15 / 0.2247).
  - Body: (0.9226, 0.815) at y 0.5625.
  - Caveat: the book icon touches the top-left topbar buttons. Use a height of about 0.9, or nudge the window down 0.01.

## OWNER RULING (2026-10-28): ONE layout on every device
- The owner said: "cant' we make the UI same as pc? wtf", then "We cannot change the whole layout to be different on the devices."
- The phone uses the SAME layout as PC (v8), scaled to the screen. The separate phone arrangement (phone v1 / v2: tab strip, horizontal cards, inspect sheet) is DROPPED. Ignore review 4 MUST 6 and any phone-layout items.
- Phone check: `INDEX_PHONE_v3_samepc.png` is the v8 window cloned into an 844x390 canvas at 0.94 height (577 x 366 px). Any phone tweaks must stay inside this layout (text minimums only).
- **Latest PC:** `INDEX_MOCKUP_v8.png`. Review 4 scored it 8.5.
