# Task 8 Step 1b: hands-on red team (the controller, with computer-use + the Studio MCP)

The owner asked for this (2026-10-29): "also you do the testing use my computer if needed, to do trading and trying to
find a hole in the system."

## Setup
1. In Edit, check `workspace:GetAttribute("TestFreshSave") == true`. No other Play session may be running
   (`get_studio_state`).
2. Test tab: "Server & Clients", 2 players, Start. Three windows open: the server and Player1 / Player2 (vault note: each
   window gets an MCP id, and calls lag 10-25 s).
3. Run `list_roblox_studios`: note the ids of the server and of both clients.
4. On the server:
   - for both players: `TutorialDone = true`, `DataLoaded` checked;
   - give them pets (`ServerStorage.GivePet:Invoke(p, name, kg)`) and eggs (EggInventory / `ServerStorage.GiveEgg`),
     including mutations;
   - check PolicyService for the Studio test players (the node's policy cache). If it refuses in Studio, note it and use
     the Studio-only test switch, if one exists (never change live behaviour).
5. Write the conservation snapshot helper (server execute_luau). For each player it builds the multiset of
   pets (PetId, name, kg, mut) and eggs (kind, kg, mut) from BaseData / PetInventory / EggInventory and TradeEscrow, and
   records the totals.

## Real trades (clicking in the client windows)
- **A. Full trade:**
  1. P1: Trading tile -> P2 is ONLINE -> SEND.
  2. P2: the card -> ACCEPT.
  3. Both add 2-3 items (pets + an egg with a mutation).
  4. READY / READY -> Phase 2 -> ACCEPT / ACCEPT -> Done.
  5. Conservation: the items swapped, none lost, none doubled.
- **B. BACK** in Phase 2: both offers emptied, the items returned; then add again -> commit. Conservation.
- **C. CANCEL** in Phase 1 and in Phase 2. Conservation.
- **D. Close P2's window in Phase 2** (after escrow): P1 gets the cancel; P2's escrow is in the save; the next join
  recovers it. Conservation after re-checking the save (the server snapshot of TradeEscrow + the ledger record).
- **E. Spam-click** READY / ACCEPT / an item card: no double action, no error.
- **F. Full inventory:** give P2 150 pets, then a trade that would raise P2 over the cap -> "inventory is full" at
  READY.
- **G. Request spam:** the 4th pending request, the 30 s expiry, decline -> the 30 s pair cooldown.

## Forged remotes (Client datamodel execute_luau on P1's window)
Fire `ReplicatedStorage.Trade.Request/Action/Query:InvokeServer(...)` with:
- **an other player's pet id** (one of P2's PetIds) in `add`;
- **the same pet id 9 times**, and a 10th item;
- **odd values:** an egg ref with a kg P1 doesn't own, NaN / inf / negative / 1e308 kg, an unknown kind;
- **bad indexes:** `remove` with 0 / -1 / 10 / 1.5 / "1";
- **bad versions:** `ready` / `accept` with an old ver, a future ver, ver = 0, NaN, a string, a table;
- **early accept:** `accept` before the 5 s lock or before escrow;
- **a stolen request:** `respond` with P2's request id (a request meant for someone else), a forged id, or a table id;
- **bad chat:** 0, 7, NaN, a 100 KB string;
- **giant input:** `search` with a 100 KB string, control characters, and SQL/JSON-looking text;
- **the wrong remote:** ops sent to the wrong remote, unknown ops, no args, 50 extra args, a nested table 100 deep;
- **spam:** 500 calls in a loop (the limiter, and no thread pile-up: check the server's memory/thread count after).
- **Changes mid-trade:** in Phase 2 (after escrow), `add` / `remove` / `ready` from P1, which must be refused. Then sell or
  place the escrowed item (the Sell remote, the place remote), which must be refused because the item is out of the
  data.
- **Leaving mid-trade:** in the middle of commit, kill P1's client.
- After each group: the conservation snapshot plus the server console (no errors).

## Recording
- Every attempt goes in the ledger: attempt -> result -> blocked? (yes / HOLE).
- Every HOLE becomes a failing test (TradeSimTests.exploit or TradeUITests) and then a fix (Task 8 Step 2).
- At the end: the red End Session button. TestFreshSave stays true until Step 4.
