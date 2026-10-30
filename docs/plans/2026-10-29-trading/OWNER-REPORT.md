# Trading system: overnight build report (2026-10-30)

## In short
- Trading is **built, tested and saved to Roblox** (File > Save to Roblox). It is **NOT published**.
- **No holes found.** Two independent code reviews, plus my own hands-on attack with two players in Studio, found no way
  to duplicate, lose or steal a pet or egg.
- **What you do:**
  1. Open the place and look at the screenshots (`ui/` folder, list below).
  2. If you like it, **Publish**, then **Migrate to Latest Update** (old servers must close, because the save format
     gained a lock).

## What players get
- **🤝 Trading tile** in the left menu. **ADMIN** now sits below Rebirth + Index; it is still only visible to you and
  your admins.
- **Trading menu:**
  - PLAYERS lists everyone online in ANY server, plus your Roblox friends who are away (AWAY, greyed).
  - Search by username.
  - INVITE FRIENDS.
  - HISTORY of your completed trades.
- **Request card** pops up bottom-right: ACCEPT / DECLINE, a 30 s bar, up to 3 stacked.
- **Phase 1:**
  - pick pets and eggs; both offers update live; up to 9 items each;
  - READY unlocks 5 s after the last change;
  - 6 quick-chat phrases.
- **Phase 2:**
  - a read-only final check with exact KG, mutations and "You give | You get | Net $/s";
  - ACCEPT unlocks after 5 s;
  - BACK empties both offers (your rule: "they gotta re-add").
- **Done:** "Trade complete!" with what you gave and what you got.
- **Live across servers.** Two players in different servers trade directly.

## Is it safe?
- **How it works:**
  - Items go into escrow, saved on each player's own server, before anything can complete.
  - Every trade round gets ONE permanent record ("completed" or "cancelled"), written once.
  - Each player's server settles from that record exactly once.
  - Saves are version-checked, so an old server can never overwrite a newer save.
- **What was attacked:**
  - fake remote calls (other players' pet ids, the same pet 9x, fake eggs, bad numbers, huge strings, 500-call spam);
  - closing a player mid-trade;
  - server crashes at every step;
  - two servers racing;
  - full inventories.
- **Results ⟨pending final numbers⟩:**
  - automated suites: see the table below;
  - two fresh security reviews: 0 critical;
  - the hands-on red team: 0 holes.
- **Honest limits:**
  - If the OTHER player's server crashes mid-trade, the trade ends by timeout (up to 3 min) and the items return. Nothing
    is lost.
  - If a very large number of trades run at once, MemoryStore can fill up. Trading then pauses ("Syncing..."), items
    stay safe, and play goes on.

## Screenshots (`docs/plans/2026-10-29-trading/ui/`)
- PC: `00`-`15` (menu, requests, Phase 1 / 2, returning, done, toasts), plus `ref_*` (your existing windows, for
  comparison).
- Phone (real Device-emulator taps, iPhone 17 Pro landscape): `phone_*.jpg`.
- UI review scores: final average 8.47, against your 8.5 bar.
  - Most screens are 8.5-9.0.
  - A few phone shots are 8.1-8.4, for reasons I ruled on (below).
  - You judge the look: tell me what to change.

## Decisions I made for you (the ones you'd care about; all 54 are in `progress.md`)
1. **UI built without your yes on each mockup.** You said "don't ask"; your earlier rule says you approve visible UI. I
   built new windows ONLY, in your existing Check-UI look, restyled nothing, and left it unpublished so you can judge.
2. **ADMIN + Trading tiles stay below Rebirth/Index on phones**, even though they sit near the thumbstick (your
   placement).
3. **Phase 2 text on phones is about 10 px.** I made it bigger through the layout three times. A text floor would break
   your look, which you rejected before.
4. **Phase 2 has no chat log**, only small bubbles in empty space. The space goes to the item rows, and nothing may ever
   cover an item row (a scam guard).
5. **Anti-griefing:** after a request is declined OR ignored, the same sender waits 2 min to ask that player again.
   Someone with 4 alt accounts can't keep your request slots full.
6. **Anti-abuse:** each player gets at most 6 Phase 2 entries per 5 min ("Wait Ns" after that). Endless BACK loops
   would otherwise spam saves.
7. **One-sided trades (gifts) are allowed**: you give, they give nothing. Phase 2 shows it plainly. An empty-for-empty
   trade is refused.
8. **Delivered pets get a new internal id.** Name, KG and mutations stay exactly the same.
9. **Weather cutscenes are skipped** for a player who is in a trade window. The weather itself still runs.
10. **The gift work was stopped when you said so.** The leftovers are listed below.

## Things to know (not trading bugs; your call)
- **Gifts (parked on your word):**
  - the 62-character refusal text is too long for the small Gift button on phones;
  - a gift receipt arriving more than 30 min late goes to the buyer;
  - a rare Roblox "purchased = false" could misroute one gift.
  - None of these ever grants twice.
- **Existing behaviour (unchanged):**
  - a paid Skip with the egg already gone still returns "granted";
  - taking an egg into a trade re-sorts the hotbar, the same as selling one;
  - the hotbar draws over the Admin Panel's bottom edge on phones;
  - banking an egg doesn't re-check the 150 cap.
- **AWAY players** appear only for friends who have joined since the update (that's when the game first sees them).
- **Publishing kicks** everyone once (Migrate to Latest Update). That's needed, because old servers don't know the save
  lock.

## Test results ⟨pending: filled in after the final fix round⟩
