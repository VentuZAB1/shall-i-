# Builder rules for the SLINGSHOT trading build (read before touching Studio)

## Where things are
- The game is the owner's open Roblox Studio place. Studio MCP `studio_id` = `3bf21205-caff-490e-a927-3bd9f0097311`.
- Tools: `mcp__Roblox_Studio__execute_luau` (datamodel_type `Edit` / `Server` / `Client`), `script_read`, `script_grep`,
  `multi_edit`, `start_stop_play`, `get_studio_state`, `get_console_output`. Load deferred MCP tools with ToolSearch
  (`select:mcp__Roblox_Studio__execute_luau,...`) before the first call.
- Scripts live in the place (no files, no git). Write scripts by setting `.Source` from `execute_luau` (fine for new
  scripts), or with `multi_edit` for targeted edits to big existing scripts.
- Vault (game-agnostic know-how, read the notes your task touches): `V:\Obsidian\Roblox\` -> `04 Code/Save Data.md`,
  `04 Code/Remotes and Security.md`, `04 Code/Testing in Studio.md`, `08 Tools/Studio MCP Gotchas.md`,
  `05 Systems/Backpack Hotbar and Inventory.md`, `05 Systems/Eggs Hatching Pets.md`.

## Hard rules (owner, from real incidents)
- NEVER publish, never File > Save. The controller saves at the end.
- **Before EVERY Play test:** in Edit, check `workspace:GetAttribute("TestFreshSave") == true`; if not, set it to true
  first. Never Play without it: tests would edit the owner's REAL save. Leave it true when you finish (the controller
  turns it off at the very end).
- Never type in Studio's command bar, never click Studio dialogs, never set `Camera.CameraType` from Edit.
- Before changing an EXISTING script: if `ServerStorage._Backup_Trading.Before` doesn't already hold a copy, clone the
  script there first (`Disabled`/`Enabled = false`, all CollectionService tags removed).
- Long `execute_luau` work: chunk it and `task.wait()` between chunks (Studio freezes otherwise).
- Edit mode caches `require`: test modules require CLONES of what they test (see `ServerStorage.StreakTests` header),
  or run the live parts in Play.
- Play sessions: check `get_studio_state` first. If a Play session is already running that YOU didn't start, don't stop it;
  report NEEDS_CONTEXT. Stop the Play sessions you start when you're done.
- Studio store names: every trading DataStore / OrderedDataStore / MemoryStore map / Messaging topic ends in `_Studio`
  in Studio (`TradeConfig.stores()` once Task 2 exists).
- Follow the code style of the surrounding scripts: comment density, naming, `--!strict` only where the file has it.
  Short plain-English comments explaining WHY, like the existing scripts.

## Tests
- Test modules live in `ServerStorage.<Name>Tests` and return a report string `"<suite>: N pass / M fail"` plus one line
  per failing check (copy the `report()` / `runner()` pattern from `ServerStorage.PerfTests` / `StreakTests`).
- TDD: write the checks first, run them and see them FAIL (record that output), then implement, then run until they
  PASS (record that output). Paste both outputs into your report.

## Report contract
- Write your full report to the report file named in your dispatch: what you built (every script path you created or
  changed, and its backup path), the RED and GREEN test outputs, rulings you had to make, concerns.
- Your final reply: under 15 lines, with Status (DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT), a one-line test
  summary, concerns, and the report path.
- You do not dispatch subagents (no helpers, no reviewers). The controller reviews after you report.
