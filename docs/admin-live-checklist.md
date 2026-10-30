# Admin menu - live test checklist (after you save + publish)

Some parts only work on real Roblox servers (not in Studio): messages between servers, the restart and bans.
Open the game twice so you get TWO servers (e.g. you on PC + a friend or alt account in another server,
or join, then use "Join a different server").

1. **ADMIN button** - only on your screen, above the Shop tile. Friends/alts must NOT see it.
2. **Announce** - ANNOUNCE tab, type a message, SEND TO ALL. Both servers show
   "Santrinio [verified tick]: your message" at the top for ~7 s.
3. **Admin Abuse** - ADMIN ABUSE tab, e.g. MONEY x2 for 15m -> ON. In BOTH servers everyone sees
   "Santrinio [verified tick]: activated x2 MONEY for 15 min!" at the top for 5 s with a power-up sound, and the cash icon
   appears bottom right with its timer under it ("14:59") and an "x2" badge. Hover it (PC) / tap it (phone) ->
   "x2 MONEY - Everyone earns x2 money".
   Start SPEED x3 for 15m too -> its own icon with its own timer.
   (2026-10-12: boosts and weathers share ONE row with no "ADMIN ABUSE" label, in the order you started them: the newest
   at the right end. Stop one and start it again -> it comes back at the right end.) Speed only boosts FREE speed: with x2 Robux speed
   your HUD shows x4 (x2 + 2), not x6. OFF stops just that one; STOP ALL stops all.
4. **New server joins a running boost** - while a boost runs, join a brand-new server: the icon is there too.
5. **Give** - PLAYERS tab, type the other account's username: GIVE money / a pet / a potion. The result line says
   "Gave ..." even when they are in the other server. A name nobody has -> "... is not online in any server".
6. **Kick** - kick the alt with a reason -> it leaves with "Kicked by an admin: <reason>".
7. **Ban / Unban** - ban the ALT for 1H -> it gets kicked and can't rejoin; UNBAN -> it can join again.
   (Banning yourself is blocked.)
8. **No Waves + fun** - ADMIN ABUSE tab: NO WAVES 15m -> ON: waves stop in every server (running ones vanish) and a teal
   shield icon shows the time. SPAWN lucky eggs (extra big eggs on the runway) and START a wave still work.
   **Everything in ADMIN ABUSE hits ALL servers** (2026-10-11): with a friend in another server, SPAWN eggs / START a
   wave / WEATHER START -> they get it too (reply says "in every server").
   **Weather (2026-10-12):** pick one or more (they turn blue) -> START turns them on everywhere. One already running
   stays as it is; nothing is replaced; 2+ at once = no cutscenes. STOP ends the picked ones, or ALL of them when
   none is picked (the button then reads STOP ALL). A server that opens during them joins all of them with the time
   left. **HOURLY WEATHER:** 1H / 6H / 24H -> PAUSE stops the automatic hourly weather in every server for that long
   ("PAUSED h:mm:ss"); RESUME turns it back on early.
9. **Restart** - only when you really want it: SERVER tab, message, RESTART ALL SERVERS, then press again within 3 s.
   Every server shows "SERVER RESTART IN 30", then everyone is moved to fresh servers. Check your money/pets are
   still there after. Then restart a SECOND time: everyone must move again.
   Good to know: players in a VIP server end up in public servers after a restart. Rarely, someone sent back can land
   in an old server that hasn't restarted yet. They stay there on the old version until they rejoin.

If something fails, the result line at the bottom of the menu says why. Every admin action is also saved in the
DataStore `AdminLog_v1` (last 100).
