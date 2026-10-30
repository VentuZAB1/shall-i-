# SLINGSHOT Admin Menu - design (2026-10-10)

## Goal
An owner-only admin menu inside SLINGSHOT ("Slingshot for Eggs", place 97952972919986) so the owner can talk to and
manage the whole live game from inside it: global announcements, "Admin Abuse" boost events, player tools and
server tools. Success = the owner opens the menu with one button, every command works on every live server,
no other player can ever trigger a command, and every player sees announcements/events clearly.

## Decisions (owner, 2026-10-10)
| Topic | Decision |
|---|---|
| Admins | Only Santrinio, UserId 1809064431 (one config list, more can be added later) |
| Commands v1 | Global announcement, Admin Abuse events, player tools, server tools (all four) |
| Announcement look | Big Check-UI banner at the top of the screen, ~8 s, sound |
| Open the menu | Small ADMIN button on the owner's HUD only |
| Event boosts | Money x2/x3/x5, Speed x2/x3/x5, Lucky egg rain, Faster hatching x2/x3 |
| Player tools reach | Players online in ANY server (by username); ban also works offline |
| Shutdown | Soft restart: countdown banner, then everyone moves to fresh servers |
| New servers during an event | Join the running event until it ends |
| Approach | Custom system (no HD Admin / Adonis: third-party code, backdoor risk, wrong style) |

## Architecture
```
Owner client                     Owner's server                         Every server (incl. owner's)
AdminClient (menu) --Remote--> AdminServer: check UserId, validate, --MessagingService "Admin"--> AdminServer: apply
                                rate-limit, filter text, log            (banner/event/kick/give/restart)
                                MemoryStore "AdminEvent" (event state)  <- new servers read it on start
All clients: AdminBanner (announcement banner + event timer pill), driven by replicated attributes/remote events
```

### Units
1. **`ReplicatedStorage.AdminConfig`** (ModuleScript): `ADMINS = {[1809064431] = true}`, allowed values
   (multipliers {2,3,5}, hatch {2,3}, durations 5..120 min, text max 200 chars, give limits), topic names.
2. **`ServerScriptService.AdminServer`** (Script): the only place commands run.
   - `ReplicatedStorage.Admin.Command` RemoteFunction. Every call: `ADMINS[player.UserId]` or reject; validate types,
     ranges and whitelists; 1 command / second rate limit; returns {ok, message}.
   - Gives the menu UI only to admins (clones `ServerStorage.AdminUI` into the admin's PlayerGui on spawn).
   - Cross-server: `MessagingService` topic `Admin` carries {kind, args, from, id}; every server (the sender too)
     applies it on receive. Replies for player commands come back on topic `AdminReply` -> shown in the menu.
   - Event state: `MemoryStoreService` hash map `AdminEvent` key `current` = {boosts, endsAt}, expiry = endsAt.
     Each server reads it on start and on each `Admin` event message, then sets workspace attributes
     `Event_Money`, `Event_Speed`, `Event_Hatch`, `Event_LuckyRain`, `Event_EndsAt` (0/1 when off). Ends by itself.
   - Audit log: DataStore `AdminLog_v1`, last 100 entries {time, admin, kind, args, result}.
3. **Game hooks** (small edits in existing systems, each reads the workspace attributes):
   - `ReplicatedStorage.Boosts`: money x Event_Money, speed x Event_Speed (shown everywhere money/speed is shown).
   - `ServerScriptService.BaseHatchery`: hatch time / Event_Hatch.
   - `ServerScriptService.EggSpawner`: lucky odds divided by ~10 while Event_LuckyRain (still capped per area).
4. **`StarterGui.AdminBanner` + `StarterPlayerScripts.AdminBannerClient`** (all players): top banner for
   announcements and restart countdown; event pill "ADMIN ABUSE  x2 MONEY  14:59" placed in a free HUD zone.
5. **`ServerStorage.AdminUI` + its LocalScript** (owner only): Check-UI window (528x415, silver Settings-style
   header "ADMIN"), 4 tabs:
   - **Announce**: text box (200 chars), Send. Shows the filtered result.
   - **Events**: toggles + multiplier pickers for the 4 boosts, duration, Start / Stop event.
   - **Players**: username box; Give money (amount), Give pet (creature + KG), Give potion (type + count), Kick
     (reason), Ban (duration: 1 h / 1 d / 7 d / forever, reason, alts on/off), Unban. Reply line ("done" / "not online").
   - **Server**: Soft restart all servers (countdown 30 s, message), Spawn lucky eggs, Start a wave (both in every server since 2026-10-11, moved to the ADMIN ABUSE tab).
   - The ADMIN HUD button is created by the same script (only exists for admins).

### Commands in detail
- **Announce**: server filters with `TextService:FilterStringAsync(text, ownerId, PublicChat)` ->
  `GetNonChatStringForBroadcastAsync`; publishes the FILTERED text; every server fires the banner to all clients.
- **Event start/stop**: write MemoryStore, publish; servers apply attributes. Stop = clear + publish.
- **Give money / pet / potion**: publish with target username; the server that has the player applies it with
  `Money.Earn`-style add (no boosts: raw amount), `ServerStorage.GivePet`, `ServerStorage.GivePotion`; replies.
- **Kick**: the server that has the player kicks with the reason; replies.
- **Ban / Unban**: `Players:BanAsync` / `UnbanAsync` (ApplyToUniverse, duration, display + private reason, alts
  option) run on the owner's server - works offline and kicks the player from any server.
- **Soft restart**: publish; every server shows a 30 s countdown, then teleports its players to a reserved
  server that sends them straight back to the place (fresh servers on the latest version). New servers started
  in the last 60 s ignore it.
- **Lucky eggs / wave**: calls into EggSpawner / WaveServer (small BindableFunctions). Since 2026-10-11 they run in
  EVERY server, like an announcement (owner: "it has to be ALL SERVERS ... its admin abuse for a point").
- **Weather** (added with the weather system; ALL servers since 2026-10-11): START replaces whatever weather runs on each
  server and is stored (MemoryStore `AdminEvent` key `weather` = {id, type, endsAt} / {id, stopped}). Servers that open
  during it, or missed the message, join it with the time left (`AdminLogic.weatherSync`, re-checked every 60 s), so
  every server ends it together. STOP stops it everywhere; a late stop only ends the admin weather, never a scheduled one.
  Messages from other servers are checked again with the same rules (`AdminLogic.recheck`).

## Error handling
- Every MessagingService / MemoryStore / DataStore / filter / ban call is in pcall with a retry for publish;
  failures come back to the menu as a red reply line, never a silent drop.
- Filter failure -> announcement is NOT sent (never show unfiltered text).
- Event attributes are cleared when endsAt passes even if no stop message arrives.
- Non-admin calls are rejected and logged (UserId) - nothing else happens.

## Testing
- Studio play (TestFreshSave = true): every command on the local server, filter result, event attributes and
  boosts (money/speed numbers, hatch time, lucky odds), banner + pill on screen, menu tabs, mobile-size layout.
- 2-player Server & Clients test: give/kick on the other player; the second player has no menu, no button, and a
  forged Remote call from that client is rejected.
- Live (after publish, owner): two servers open -> announcement, event, give/kick across servers, soft restart.
  Checklist handed to the owner.

## Out of scope (v1)
Editing offline players' saves, extra admins/moderator ranks, fly/noclip/teleport commands, scheduled events.
