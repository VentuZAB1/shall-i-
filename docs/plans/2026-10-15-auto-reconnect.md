# Auto Reconnect (AFK players keep farming) — plan 2026-10-15

## Goal
Roblox kicks a player after 20 min with no input. Any player who has been idle for 15:00 gets teleported into a fresh session first. If the server saw them on their own treadmill when it sent them, they land back on it and keep gaining Speed. Everyone else rejoins at their base as normal. From 0:30 of idle time a bottom-right label counts down: "Auto Reconnect: 14:30" … "0:00". It's white GothamBlack with a thick black outline and no box, like the reference.

## Interpretation (the reviewer may adjust)
- The idle clock is real time with no input, the same thing Roblox's kick measures. The label appears at 0:30 and the reconnect fires at 15:00.
- Any input (key, mouse button, mouse move or wheel, touch, gamepad button, thumbstick past 0.25, chat typing) hides the label and resets the clock. Character movement never counts as input, because the treadmill, waves, bats and respawns all move the character.
- "Back on the treadmill" is decided by the SERVER from `TreadmillRun ~= nil` at seal time (TreadmillServer `mount` l.141 only sets it on the owner's own treadmill). That flag is stored in the player's SAVE. The client never supplies it.
- Teleport target is **any public server** (`TeleportAsync(game.PlaceId, {player}, options)`), not the same JobId. In a solo server, rejoining the same instance would fail because the server shuts down when its last player leaves, and the player would be stranded on an error screen. The data design works for every destination, including the same server.

## Existing code it builds on
- **TreadmillServer**
  - CHECK_INTERVAL 0.1 (l.20), GAIN_INTERVAL 0.1 (l.21), STAND_OFFSET -1 (l.25).
  - `mount` welds the root to the Belt and sets `TreadmillRun` (l.127-142). `dismount` is at l.145-152 and the Exit remote at l.154.
  - The zone loop mounts only the owner and only when `SlingPhase == "None"` (l.244-275).
  - `placeTier` re-mounts riders when the tier model is swapped (l.176-204). Gain is paid on Heartbeat (l.282-292).
- **TreadmillClient:** walk animation on `TreadmillRun` (l.290-292). JumpRequest fires Exit (l.299-318).
- **BaseManager:** `assign` gives the lowest free base on PlayerAdded (l.58-71). `spawnAtBase` is deferred on CharacterAdded (l.91-96). The treadmill is `Treadmill_B<BaseId>`.
- **PlayerData**
  - FIELDS at l.18-53. `save` is a blind UpdateAsync overwrite (l.132-150).
  - SavePlayerNow (l.154-157), leave-save (l.164-170), AddGiftedPass (l.180-205), autosave every 60 s (l.207-214), BindToClose (l.216-229).
  - No session lock. RESTART_LOBBY (l.86).
- **AdminServer soft restart:** `sendToLobby` + `TeleportInitFailed` handling (l.161-211, l.696-728). It has NO race guard; it relies on the lobby hop taking a few seconds. We reuse its patterns (pcall TeleportAsync, retry, IS_LOBBY) but add a real handoff.
- **Receipts:** grants first, then SavePlayerNow, and returns NotProcessedYet if that save fails.
- **OfflineConfig:** MIN_SECONDS = 300, so reconnects never open Welcome Back. Unclaimed OfflinePending still re-shows it, which is fine.
- **PlaytimeServer:** progress is per session (l.36-41). A reconnect would reset it, so it gets carried (step 4).
- **TutorialClient** (l.10-11) re-derives the step from real state, so a rejoin mid-tutorial is safe.

## Architecture
**New**
- `ReplicatedStorage.AutoReconnectConfig` (ModuleScript). Constants SHOW_AFTER 30, LIMIT 900, HARD_CEILING 1110 (18:30), RETRY_GAP 60, CARRY_MAX_AGE 300. Pure functions, all unit-tested:
  - `clock(secondsLeft)` returns "14:38".
  - `isActivity(input)` excludes Accelerometer, Gyro, Focus, and thumbsticks/triggers under 0.25.
  - `blockReason(state)`
  - `validateRequest(...)`
  - `parseJoin(td)`
  - `matchCarry(carryJson, handoff, now)`
  - `place(viewport, rowRect, avoidRects, labelSize)`
- `ServerScriptService.AutoReconnectServer` (Script). Creates `RS.AutoReconnect` (Folder) with:
  - `Request` (RemoteFunction, client→server, arg idleSeconds).
  - `Status` (RemoteEvent, server→client "failed").
  - Folder attributes `Enabled`, `Limit` and `ShowAfter`, so the client and server use the same timings.
- `StarterPlayerScripts.AutoReconnectClient` (LocalScript): idle clock, label, request.
- `ServerStorage.AutoReconnectTests` (ModuleScript).

**Changed**
- **PlayerData**
  - New FIELD `ReconnectCarry = ""`.
  - Per-player `inflight` save counter and a `sealed` set.
  - `ServerStorage.SealForReconnect(player) -> ok`: seals, waits until in-flight saves = 0 (max 15 s), then does the final write. `ServerStorage.UnsealPlayer(player)` restores normal saving.
  - The leave-save is skipped for sealed players.
  - AddGiftedPass returns false for a sealed userId, so the buyer's receipt is retried later.
  - Reconnect-aware load (step 5).
- **TreadmillServer:** `ServerStorage.MountTreadmill(player) -> ok`. It checks owner, alive, `SlingPhase == "None"` and not already mounted, clears `mustLeave`, then calls the existing `mount`.
- **Receipts.process:** also returns NotProcessedYet while `player:GetAttribute("Reconnecting")`.
- **AdminServer:**
  - `applyGlobal.restart` sets workspace `RestartPending` and clears it with `restarting`.
  - `sendToLobby` skips players with `Reconnecting`, so a teleport already in flight can't fail the 50-player group.
- **Analytics:** a small `A.custom(player, name, value, field01)` wrapper. One event, "AutoReconnect", on arrival with field "Treadmill" / "TreadmillFailed" / "Hub". It shows how much AFK farming happens.

`Enabled`:
- Live public servers: on.
- Restart lobby: off.
- Private (VIP) servers: off (Q1).
- Studio: off unless workspace `AutoReconnectTest == true` (then LIMIT 25 s, SHOW_AFTER 3 s, RETRY_GAP 5 s).

## Data-safety design (handoff instead of session locking)
1. **Request (old server).** Client invokes `Request(idle)`. The server refuses unless all of these hold:
   - Enabled, and `RestartPending` is not set.
   - Rate limit: 1 call per 10 s, and not already busy.
   - `DataLoaded == true`.
   - `idle` is a finite number ≥ LIMIT-5.
   - The server-side session age (time since PlayerAdded here) is ≥ LIMIT-30. This alone caps reconnects (and their DataStore writes) at one per ~14.5 min per player.
   - Server-seen activity is ≥ LIMIT-30 old: a Treadmill `Exit` remote (jumped off) or `SlingPhase` turning "Aiming".
   - SlingPhase is not Loading/Flying/Landed. If it is, the reply is `"wait"`.
2. **Carry.** handoff = `HttpService:GenerateGUID(false)`. Set `ReconnectCarry` = JSON `{id, at = os.time(), tm = TreadmillRun ~= nil, pt = seconds played this session, pc = PlaytimeClaimed}`. Set `Reconnecting = true`.
3. **Seal + final save.** `SealForReconnect`:
   - `loaded[player] = nil`: autosave, BindToClose and SavePlayerNow skip them, and Receipts hold.
   - Wait for in-flight saves, then write the snapshot.
   - If the write fails: unseal, clear `Reconnecting`/`ReconnectCarry`, reply false. The client retries after RETRY_GAP.
   - The final save finishes **before** TeleportAsync. After it, the old server never writes this player again. That removes both classic races: the new server loading before the leave-save lands, and a late leave-save overwriting the new server.
4. **Teleport.**
   - TeleportData = `{autoReconnect = 1, handoff = id}` only. It travels through the client, so it never carries values.
   - pcall TeleportAsync up to 3 tries (0 s / 3 s / 8 s).
   - `TeleportInitFailed` (filtered to our pending players) uses the same retry budget. When it's exhausted: UnsealPlayer, clear the attributes, `Status:FireClient("failed")`.
   - Watchdog: if the player is still here 60 s after an accepted call, treat it as failed.
   - PlayerRemoving for a sealed player: no leave-save. Any seconds of income after the snapshot are lost (accepted).
5. **Load (new server, PlayerData.load).** If `GetJoinData().SourcePlaceId == game.PlaceId` and `parseJoin(td)` yields a handoff:
   - Read with `DataStoreGetOptions.UseCache = false`.
   - If the stored carry id ≠ handoff, re-read up to 3× at 1.5 s, then continue with what's there.
   - A forged handoff only costs ≤ 5 s of waiting.
6. **Arrival (AutoReconnectServer).** After `DataLoaded`:
   - `matchCarry` must pass: the SAVED carry id = TeleportData handoff, and age < 300 s. Otherwise nothing is applied.
   - Playtime: `PlaytimeStart = now - pt - gap`, `PlaytimeClaimed = pc` (pattern-checked).
   - If `tm`:
     - Wait for `BaseId > 0`, the treadmill's `Tier == TreadmillTier` (≤ 5 s), and a live character ≥ 1.5 s old. This lets BaseManager's deferred `spawnAtBase` and BaseSpawnCamera finish first, so a PivotTo can't drag the welded belt.
     - Then call `MountTreadmill`, up to 3 tries over 15 s.
   - Clear `ReconnectCarry = ""` and log the Analytics event.

## Failure cases
| Case | Result |
|---|---|
| Final save fails | No teleport, unsealed, retry in 60 s; after 18:30 we stop, so Roblox kicks at 20:00 (today's behaviour) |
| All teleports fail / watchdog | Unsealed, normal saves resume, client hides the label and retries once more |
| Player closes the game mid-teleport | The final save already holds their data |
| Purchase during the handoff | Held (NotProcessedYet) → Roblox retries in the next server; ReceiptIds stop double grants |
| Gift to a sealed player | AddGiftedPass false → retried |
| No free base / tier swap / server running old code | Spawns normally, event "TreadmillFailed" |
| Admin soft restart running | Requests refused; restart skips `Reconnecting` players |

## Idle states (client; the server re-checks what it can)
The clock keeps counting in **every** state, because Roblox's 20-min kick doesn't pause either. A state only HIDES the label and/or DEFERS the request. Past HARD_CEILING (18:30) the request goes out anyway, since a reconnect beats a kick.

| State (detection) | Label | At 15:00 |
|---|---|---|
| Own treadmill (`TreadmillRun`) | shows | reconnect → back on treadmill |
| Hub / base / standing | shows | reconnect → base spawn |
| Runway (`SlingState == "Out"`); waves/bat may hit them (not input) | shows | reconnect (a carried egg is lost, as with a kick) |
| Sitting in the pouch (`SlingPhase` Aiming) | shows | reconnect |
| Launch/flight (`SlingPhase` Loading/Flying/Landed, ends ≤ 20 s, SlingshotServer l.173-179) | shows | defer until it ends |
| Intro (`IntroPlaying`), hatch cinematic (`InHatchCinematic`), any cutscene (`CurrentCamera.CameraType == Scriptable`, covers weather cutscenes) | hidden | defer until it ends |
| Tutorial (`TutorialDone == false`) | shows | reconnect (the step is re-derived on rejoin) |
| Menu window / Welcome Back / Robux prompt open | shows | reconnect (receipts retry) |
| Dead / respawning (no live Humanoid) | shows | defer until alive |

Extra activity sources:
- `GuiService.MenuOpened/MenuClosed` and `MarketplaceService` purchase-finished events.
- `Player.Idled(t)` acts as a floor: `lastInput = min(lastInput, now - t)`, so our clock never runs behind Roblox's.

## UI spec (Check-UI)
- **ScreenGui** `AutoReconnect`: ResetOnSpawn false, IgnoreGuiInset false, DisplayOrder 4 (above PetsEggsUI 2 / MainMenu 3; weather tips at 5 and toasts at 20-30 draw over it).
- **TextLabel** `Label`:
  - Text white, GothamBlack.
  - TextSize 22 at the Check-UI baseline 1050×620; Size (0,300,0,28).
  - AnchorPoint (1,1), TextXAlignment Right, no background.
- **UIStroke:** black, Thickness 2.6, LineJoinMode Round.
- **UIScale** `WindowScale` with k = clamp(min(vx/1050, vy/620), 0.52, 1.18), the same as WeatherTilesClient l.135. That gives ≈26 px text on desktop and ≈14 px on an 844×390 phone.
- **Show/hide:** fades in over 0.2 s, hides instantly on input. At 0:00 the text becomes "Reconnecting...".
- **Placement** (`place()`, re-run on viewport change and every 0.5 s while visible):
  - Right edge = the right edge of `PlayerGui.WeatherTiles.Row`.
  - Bottom = the row's top − 6·k. The row is always S+TH tall (WeatherTilesClient l.153), even with no icons, so the label sits above the weather/Admin-Abuse icons and their timers and never jumps when icons come and go.
  - On touch screens the row is already left of the jump button (l.140-148), so the label never covers the jump button either.
  - Then, if the rect intersects `BackpackGui` Hotbar or `PetsEggsUI.RightTiles`, raise it above that rect's top. This matters on phones, where the centred hotbar can reach the label's x range.
- **Measured in Studio this session (1519×753):**
  - Row right edge x 1503, top y 592. Hotbar x 432-1087 / y 625-695. RightTiles y 235-460.
  - Label ≈ x 1150-1503, y 553-586: clear of all of them.
  - GiftToast (y 556-598, x ≤ 1291) can briefly overlap; it's transient and draws on top.

## Studio test plan
**Setup**
- HARD RULE: `TestFreshSave == true` before every Play.
- Coordinate Play with the other agent.
- workspace `AutoReconnectTest = true`.

**Studio-only hooks**
- Client: LocalPlayer attribute `AutoReconnectIdleDebug = n` sets idle to n s. `AutoReconnectFakeInput` calls `markActive()`. These avoid the owner's mouse resetting real waits.
- Server: `ServerStorage.AutoReconnectDebug:Invoke(player, op, ...)`:
  - In Studio, TeleportAsync is replaced by a stub that records the options.
  - `"fail"` simulates exhausted retries.
  - `"arrive", td` runs the arrival handler.
  - `"state"` returns sealed / pending / handoff / writes count.

**Tests**
1. **Unit (AutoReconnectTests, Server):**
   - `clock` (870 → "14:30", 0 → "0:00").
   - `isActivity` (Accelerometer, Gyro and a 0.1 thumbstick ignored; MouseMovement and Touch count).
   - `blockReason` table.
   - `validateRequest` (NaN, inf, string, short session, recent Exit, rate limit).
   - `parseJoin` (non-table, long strings, wrong SourcePlaceId).
   - `matchCarry` (match, wrong id, stale).
   - `place()` at 1920×1080, 1366×768, 1519×753 and 844×390-touch with sample rects: no overlaps.
2. **Label:** idle 4 → visible "0:21"; FakeInput → hidden; `IntroPlaying` / `InHatchCinematic` / Scriptable camera → hidden and no request at LIMIT; clear the state → request.
3. **Seal path (treadmill):**
   - Mount, then idle to LIMIT.
   - `Reconnecting == true` and SavePlayerNow returns false.
   - The test-key read (UseCache=false) shows `ReconnectCarry.id ==` the stub handoff, `tm == true`, Speed equals the attribute at seal.
   - Stub TeleportData is exactly `{autoReconnect=1, handoff}`.
   - Repeat on the hub: `tm == false`.
4. **Fail:** `"fail"` → unsealed (SavePlayerNow true), attributes cleared, client hides, retries after RETRY_GAP.
5. **Arrival:** `"arrive"` with the matching carry → `TreadmillRun == "Treadmill_B"..BaseId` within 5 s, Speed rising, Playtime restored, carry cleared. Hub carry → not mounted. Wrong id or stale carry → nothing applied.
6. **Receipts:** `TestProcessReceipt` while Reconnecting → "NotProcessedYet"; after unseal → "PurchaseGranted".
7. **Security:**
   - Client `Request:InvokeServer(1)`, `("x")`, `(0/0)` → refused.
   - 20 rapid calls → one seal at most (writes count).
   - SlingPhase "Flying" → "wait".
8. **Screenshots:** Client screen_capture with a weather icon running + hotbar; phone sizes via the offline preview (roblox-ui-offline-preview.md).
9. **Regression:** Admin/Weather test suites; normal autosave/leave unchanged.

**Live test (owner, after publish; the teleport can't run in Studio)**
- Stand on the treadmill and touch nothing for 15 min.
- Expect: label at 0:30 showing 14:30, teleport at 15:00, back on the treadmill, Speed rising, pets/money intact.
- Repeat idling on the hub: back at base.

## Backups
Before any edit, `ServerStorage._Backup_AutoReconnect.Before` gets clones of PlayerData, TreadmillServer, Receipts, AdminServer and Analytics. Restore = swap the clones back and delete the 3 new scripts and the module. The owner must Save + Publish afterwards.

## Open questions for the owner
1. Private (VIP) servers: leave auto-reconnect off there (default), or move idle players to a public server?
2. Carry Playtime-reward progress across reconnects (default yes)? Otherwise AFK players never reach the 20-120 min gifts.

## Review (2026-10-15)

**Verdict: APPROVED WITH CHANGES.**

I checked the plan against the live Studio source: PlayerData, TreadmillServer, BaseManager, Receipts, ShopServer, AdminServer, BaseHatchery, PlaytimeServer, WeatherTilesClient and TreadmillClient. The plan's line refs are correct. The core order is right: seal → drain in-flight saves → final write → teleport → no leave-save. The gaps are in the failure/unseal paths and one harmful gift change. The builder applies every Required item below; where it conflicts with the plan above, the review wins.

### Required changes
1. **Key the seal state by Player instance, not UserId.** Use `sealed[player]` and `inflight[player]`, and clear both in PlayerRemoving. A same-server rejoin creates a new Player object, and it must save normally.
2. **Drain rule.** `inflight` wraps the whole of `save()`, from the snapshot to the last retry. The seal sets `loaded[player] = nil` before any yield. If `inflight` isn't 0 within 15 s, abort with no final write and handle it as "final save failed".
3. **Never unseal after an accepted TeleportAsync.**
   - On TeleportInitFailed, retry up to 2 more times while still sealed.
   - When retries are exhausted, or the 60 s watchdog fires, call `player:Kick("Auto Reconnect failed - your progress is saved, please rejoin!")`.
   - Unseal only in two cases: the final write failed, or every TeleportAsync call errored synchronously. Even then, unseal only if the player is still in Players after a 5 s grace.
   - Why:
     - The plan's retry waits can unseal a player who has already left. That puts `loaded[player] = true` back, and the autosave loop (which only checks `loaded`) then writes stale data over their new server every 60 s. That's a rollback.
     - A client that can make its own teleport fail could keep good post-seal results (such as hatch rolls) and throw away bad ones.
4. **Leaving during a seal.**
   - PlayerRemoving keeps `leaving[userId] = true` until the seal's write finishes, so AddGiftedPass's gone-path write lands after it.
   - If the seal aborted or failed and the player is gone, do one plain write (the leave-save that was skipped). Never re-add them to `loaded`.
   - BindToClose also waits for seal writes still in progress.
   - AutoReconnectServer refuses new requests once the server is closing.
5. **Drop "AddGiftedPass returns false for sealed"; it's harmful.**
   - ShopServer clears `pendingGift` (l.231) before calling giveGift. So the retried receipt reaches the fallback at l.235 and gives the pass to the BUYER.
   - Leave AddGiftedPass unchanged.
   - Instead, ShopServer `kind == "gift"` (l.290-302) refuses a target that has `Reconnecting` set ("They're reconnecting - try again in a moment"). It also stamps `GiftAt = os.time()` on both buyer and target.
   - AutoReconnectServer answers "wait" while either player has a `GiftAt` under 120 s old.
6. **Drop the reconnect-aware load in PlayerData** (TD parsing and the 3× re-read).
   - The final write commits before the teleport starts, so re-reading can't change anything.
   - Instead, pass `DataStoreGetOptions.UseCache = false` on every load.
   - The handoff match stays only in AutoReconnectServer's arrival handler. After DataLoaded it always sets `ReconnectCarry = ""`, whether or not the carry matched.
7. **Guards after the seal** (anything done in this window would be silently lost):
   - BaseHatchery refuses to hatch while `Reconnecting` is set (prompt l.248, skipNow l.728).
   - AdminServer `loading(p)` (l.356) returns true while `Reconnecting` is set.
   - Keep the Receipts guard, placed before any grant next to the DataLoaded check.
   - Add ShopServer and BaseHatchery to `_Backup_AutoReconnect.Before`.
8. **Server-side budget.**
   - After any attempt, the server allows no new seal for RETRY_GAP. Cap failed attempts at 3 per server session.
   - `Request` validates, starts the seal/teleport in `task.spawn`, and returns at once with "started", "wait" or "no".
9. **Idle input.**
   - Count InputBegan/InputChanged/InputEnded **regardless of gameProcessedEvent**: GUI clicks and chat typing are gameProcessed.
   - Filter thumbsticks and triggers on `Position` magnitude ≥ 0.25.
   - Player.Idled is client-only, which is fine as planned.
10. **MountTreadmill.**
    - Treat a nil `SlingPhase` as "None" (new joins have none).
    - Return `mounted[player] ~= nil`.
    - Compare against `math.clamp(TreadmillTier, 1, MAX_TIER)`.
    - Keep the wait for spawnAtBase (character ≥ 1.5 s old).
11. **Add a Studio-only PlayerData debug hook**: delay the next save by n s, fail the next write, and keep a write log with snapshot times. Use it to prove:
    - a save already in flight at seal time lands before the final write, and nothing lands after it;
    - a failed final write unseals the player (SavePlayerNow returns true);
    - a removal simulated mid-seal never unseals;
    - a stubbed post-accept failure takes the kick path.

### Optional suggestions
- Drop the server-seen activity gate (Exit/Aiming). The session-age gate already caps writes, and a client that lies only reconnects itself.
- Drop the wait for the tier to match. `placeTier` already re-mounts riders when the tier model is swapped.
- Build the Analytics event last, and cut it if anything slips. Reconnects will also appear as leave/join in the session funnels.
- Set LIMIT = 899 to match the owner's "14:59" (the label then runs 14:29 → 0:00).
- In `place()`, test overlaps using the label's TextBounds, not the 300 px box.
- The RestartPending refusal is optional. The `sendToLobby` skip is the part that's needed.

### Live tests for the owner (after publish)
1. **Treadmill:** note Speed and Money, then idle. After the reconnect you should be back on the treadmill with Speed rising and pets/eggs intact.
2. **Two cycles back to back (about 35 min with no input):** this proves Roblox's 20-min idle kick resets across the teleport, which the whole feature depends on.
3. **Hub idle:** you land back at your base.
4. **Phone lying still:** gyro noise must not reset the clock, and the label must not cover the jump button or the hotbar.
5. **Manual rejoin afterwards:** the data matches.
6. **VIP server:** no label appears.

### Open-question defaults
- **Q1 (VIP servers): off.** Disable whenever `game.PrivateServerId ~= ""`. Moving players to a public server breaks what they paid for, and a VIP server with one player shuts down when they leave. Today's 20-min kick stays there.
- **Q2 (Playtime carry): yes.** The values come from the server-written save. Cap `pt` at the last slot's minutes + 5, and pattern-check `pc` against `^,[%d,]*$`. Without the carry, every reconnect resets the gift timer, which looks like a bug to players.
