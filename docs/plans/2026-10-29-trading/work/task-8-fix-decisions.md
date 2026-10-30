# Task 8 Steps 2-3: the fix list (controller rulings, binding)

The sources are the two whole-system reviews (`work/task-8-review-A.md`, `work/task-8-review-B.md`) and the controller's
hands-on red team (ledger, "Step 1b"). No dupe/loss/steal path was found. These are the fixes to make, each test-first
where testable (a failing check, then the fix, then green).

## FIX (Important)
1. **Request-slot griefing (B I-1).**
   - The pair cooldown applies after a DECLINE and also after a request EXPIRES or is dropped unanswered. It becomes
     `TradeConfig.PAIR_COOLDOWN = 120` s (decline used 30 s).
   - Keep the 3-pending cap per receiver and every sender limit.
   - Effect: one alt can target the same victim at most every ~2.5 min, so keeping 3 slots full needs ~12 alts instead
     of 4.
   - Test `request_slot_griefing`: 4 senders, staggered, can't keep the victim's slots full past the first wave, and a
     5th real sender gets through within 60 s.
   - Spec §6 "Request-bombing" row: update the text to say what the code does.
2. **Refused calls cost MemoryStore writes (B I-2).**
   - (a) The node refuses, from its OWN current copy and with NO UpdateAsync, anything that copy already proves
     refused: wrong phase, a ver behind the copy, the READY/ACCEPT lock still running on this node's clock, offers
     locked, the per-trade change cap reached. The UpdateAsync stays the authority for everything else.
   - (b) READY / ACCEPT / BACK / CANCEL: 1 call per second per player, each (state stays on the shared button limiter).
   - (c) A per-trade write budget for both nodes' writes on that trade: about 40 session writes per minute, values in
     TradeConfig. Over budget, the call answers "Slow down" with no service call.
   - Test `refused_calls_free`: 50 refused READY/ACCEPT/add calls in the lock window cost 0 UpdateAsync (count them
     through the env memory adapter).
   - Re-run `budget`.

## FIX (Minor, all cheap)
3. **A-M1:** the AdminServer soft restart (`saveBeforeLobby`) calls `ServerStorage.TradeCancelFor` for every player
   BEFORE its save, exactly like AutoReconnect. Back up AdminServer first if needed.
4. **A-M2:** settleStep's writes after `give` (TradeEscrow / SettledRounds / TradeHistory) must be all-or-nothing with
   the give.
   - Pre-check the three encoded lengths BEFORE give (refuse the settle if any is over a safe limit, e.g. 150 KB).
   - Restore on a throw like writeAll.
   - A failed settle must leave everything as it was.
   - Test via a Studio fault seam.
5. **A-M3:** the 30 s check's `verdict` counts "missing" as abort only after a second read at least POLL s later, the
   same rule as isSessionLive.
6. **A-M4:** in the expired-confirm case, move the session first (cancel it), then write "aborted" (rule 4 order).
   recoverEntry: when the cancel write failed, re-read. Write "aborted" only if the session is over / missing /
   another round.
7. **A-M5 = B M-5 (H1 reversed):** gate the BaseHatchery `_G` helpers (HatcheryGive / PlaceAt / HatchAll / Rebase / Force
   / Validate) behind `RunService:IsStudio()`.
   - FIRST grep every script for live callers. If any non-test live code calls one, leave that one and report it.
8. **B M-1:** don't clear the per-player limiter on leave. Sweep expired entries on a timer instead, so the table stays
   bounded. The decline/expiry pair cooldowns survive a rejoin on that node.
9. **B M-2 (partly reverses the Task 5 I1 ruling, see the ledger):** isSessionLive treats an EXPIRED session as NOT live
   after a second read at least POLL s later. An expired session can't commit (toCommit's precheck), and escrow settles
   from its record, so a dead server no longer holds both players' busy locks for 15 min. Test.
10. **B M-4 (= Task 6 N2):** when writeAll's restore itself throws, warn loudly and block trading for that player for the
    rest of the session (a flag checked by ownRules and take/give). Test via the fault seam.
11. **UI-1 (hands-on):** the trade window on a tall/narrow PC window (557x723) got the 58 % width rule (scale 0.30), and
    its size differed between two opens in the same viewport.
    - Use the 97 % width rule whenever the screen is portrait-ish (gx / gy < 1.3), not only when height < 520.
    - Find and fix why two opens gave different sizes (fitTrade must use the CURRENT TradeUI AbsoluteSize at every
      open).
    - Extend the `phone_fit` test with 557x723 and two opens.
12. **Wording:** the TradePresence warning "friends failed (trading pauses, play goes on)" becomes "friends list failed
    (AWAY friends hidden, trading and play go on)", or similar, because only the AWAY list pauses.

## ACCEPTED (no change; the controller's rulings are in the ledger)
- **A-M6:** an undecodable TradeEscrow keeps the player playing and blocks trading. The raw string stays in the save for
  an admin repair. Failing the whole load would lock a player out of the game.
- **B M-3:** a RecoveryPending flag isn't needed. enterEscrow's older-entry wait and the SettledRounds gate already
  hold.

## Step 3: the full suite, after the fixes
Run and report every suite, each with pass/fail counts:
- SaveLockTests (pure + live);
- TradeCoreTests;
- TradeItemsTests;
- TradePresenceTests (pure + live);
- TradeSimTests partA / partB / crash / exploit / budget;
- TradeUITests;
- AutoReconnectTests (server + unit);
- the existing StreakTests / StarterPackTests live parts (regression);
- AdminServerTests (AdminServer is touched by fix 3).

Any failure gets fixed (with a test), or reported with its cause if it's pre-existing and unrelated to trading.
