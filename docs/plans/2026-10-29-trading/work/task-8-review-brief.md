# Task 8 whole-system security review: the shared brief

The SLINGSHOT cross-server trading system is fully built (Tasks 0-7). This is the last code review before the owner
publishes. The owner's bar is "no holes": no duplicated, lost or stolen pets/eggs, and no stuck or unrecoverable items,
through any client exploit, disconnect, crash, server switch, lag, service error or timing.

## How to read the code (read-only)
- Use the Roblox Studio MCP: load `mcp__Roblox_Studio__script_read`, `mcp__Roblox_Studio__script_grep` and
  `mcp__Roblox_Studio__execute_luau` via ToolSearch. The studio_id is `3bf21205-caff-490e-a927-3bd9f0097311`.
- Use execute_luau ONLY for read-only listing (e.g. finding a script's full path), in the Edit datamodel. Never write,
  never run Play, never edit.
- Changed scripts have their pre-trading copies in `ServerStorage._Backup_Trading.Before`. Diff the live script against
  its backup to see what trading changed.

## The authority
- The spec: `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\specs\2026-10-29-trading-design.md`. Read it fully,
  especially section 5 (invariants 1-6) and the section 6 exploit table.
- The ledger with every ruling: `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\plans\2026-10-29-trading\progress.md`.
  Grep it for "Ruling:". A ruling is a decision, but you MAY say a ruling is unsafe, with evidence.
- Reports (the builders' claims, UNVERIFIED): `...\2026-10-29-trading\work\task-1-report.md` through `task-7-report.md`.
- Earlier reviews (don't simply repeat them; check their fixes held): `work\task-*-review*.md`,
  `work\task-6-redteam.md`.

## Every script trading created or changed
**Server, new:**
- `ServerScriptService.SaveLock`: the version-checked save, the write queue, takeover, gift intent/receipts.
- `ReplicatedStorage.TradeConfig`.
- `ServerScriptService.TradeCore`: the pure rules.
- `ServerScriptService.TradePresence` + `TradePresenceServer`: presence, search, busy locks.
- `ServerScriptService.TradeNode`: part A (requests, sessions, phases, bus) + part B (escrow, record, settle, recovery,
  leave / teleport / shutdown / SaveLost).
- `ServerScriptService.TradeServer`: remotes, hooks, BindToClose.

**Server, changed (each has a backup):**
- `ServerScriptService.PlayerData`: the SaveLock load/write, the TradeRecoveryHook, SaveLost.
- `ServerScriptService.BaseHatchery`: the TradeItems take/give/count/describe wrapper, and SkipHatch.
- `Receipts`, `ShopServer`: the gift intent flow.
- `AdminServer`: saves before the soft-restart.
- `ServerScriptService.AutoReconnectServer`: TradeCancelFor before the seal.

**Client, new:** `StarterPlayer.StarterPlayerScripts.TradeClient`.

**Client, changed (each has a backup):**
- `StarterGui.MainMenu.MenuController`;
- `ServerStorage.AdminUI.AdminClient`;
- `PetsEggsUI`, `SellClient`, `UpgradeClientLegacy`, `WeatherClient`: the modal lock only.

**Tests / Studio-only:**
- `ServerStorage.SaveLockTests`, `TradeCoreTests`, `TradeItemsTests`, `TradePresenceTests`, `TradeSimTests`,
  `TradeUITests`, `TradeUIPreview`;
- the Studio-only seams `_fault`, `crashAt`, `TradeServerDebug`, `TradePreview`. Check each one is unreachable live.

## Output
Write to the file your dispatch names. For each finding give:
- the title;
- the severity (Critical / Important / Minor);
- CONFIRMED (you traced the exact lines) or PLAUSIBLE (it depends on an unverified service behaviour);
- the attack or failure steps, with script:line;
- the impact;
- the fix.

Then list the attacks / failure paths you checked that ARE blocked, one line each with the blocking line. Never pad: a
short honest list beats a long speculative one.
