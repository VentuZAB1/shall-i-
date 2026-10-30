# Weather: several at once, admin auto-pause, stacked mutations, weather tiles (design, 2026-10-12)

**Owner's request (2026-10-12):**
> "In Admin Panel, to be able to activate several mutation events, but if i turn more than 1, it disables all
> cutscenes, they just turn on. Make it also for possible pets have 2 or more (if we make more events in future) events
> on them, with multiplying it 1.5 * 1.5 = 2.25 and so on addons on money multipliers. Make it also stop the automatic
> event that starts every hour, for all servers etc."

Then: "make the UI cooler... horizontal [at the] bottom right".

**Answers the owner picked:**
- Several weathers pick their areas at random, and overlap is allowed.
- The hourly auto weather pauses for a chosen time (like the boosts).
- The HUD shows square icon tiles in a row at the bottom right.

Builds on `2026-10-10-weather-ufo-design.md`, `2026-10-10-weather-meteor-design.md` and
`2026-10-10-admin-menu-design.md`. Everything not named here stays as it is.

## 1. Several weathers at once (WeatherServer)
- WeatherServer keeps a **set of running weathers** (at most one of each type) instead of one.
  - Each has its own area, its own stays (30-90 s, `WeatherLogic.planStays`), its own moves and its own end time.
  - Each picks its next area with `Logic.nextArea` on its own; two weathers may be in the same area.
- **Server attributes:**
  - `Weather` = the running types, comma-joined and sorted ("" / "UFO" / "Meteor,UFO"). One weather reads as before.
  - Per type: `WeatherArea_<T>` (0 = off), `WeatherEnds_<T>`, and `WeatherCutsceneAt_<T>` (stamped only when that
    weather plays a cutscene).
  - The single `WeatherArea` / `WeatherEnds` / `WeatherCutsceneAt` attributes go away; every consumer moves to the
    per-type ones.
- **Bindables:**
  - `WeatherStart:Invoke(type?, area?, seconds?, quiet?)` keeps its returns. `quiet` = no cutscene.
  - `WeatherStop:Invoke(type?)`: nil stops all; returns true when something stopped.
  - `WeatherMove(area, type?)` (Studio only) is unchanged for one weather.
- **The hourly schedule** never starts a weather while any is running. Any start pushes the next one an hour on
  (unchanged rule).
- **The weather modules (UFO, Meteor) do not change.** They already own their own folders and take their area from
  `ctx` / `moveTo`.

## 2. The cutscene rule
- A weather plays its arrival cutscene (and freezes the waves for it) **only if no other weather is running when it
  starts and it is the only one being started.**
- **No cutscene** when:
  - the owner starts 2+ together;
  - the owner adds one while another runs;
  - an admin weather is joined late while another runs.
- In those cases it just turns on: the announcement bar ("UFO INVASION started in ..."), its tile and its effects.
- **Clients** play a type's cutscene when its `WeatherCutsceneAt_<T>` changes (same skip rules as now: slingshot,
  tutorial, hatch).

## 3. Admin panel: WEATHER row (all servers, as before)
- **Selection:** the weather chips become multi-select toggles.
- **START** turns on the selected weathers in every server. One already running there is left alone; nothing is
  replaced any more (the 2026-10-11 "replace" rule ends).
  - When the press starts 2+, or one is already running on a server, the new ones start quiet there (section 2).
- **STOP** turns off the selected weathers in every server, or all of them when none is selected.
- **The stored record** for late servers becomes `{id, weathers = {[T] = endsAt}}` or `{id, stopped = {T...} | "all"}`.
  - `AdminLogic.weatherSync` returns the weathers to start (each with its time left) or to stop.
  - A late stop still only ends admin weathers, never a scheduled one.
- **New row, AUTO WEATHER:** chips `[1h] [6h] [24h]` + `PAUSE` and `RESUME`.
  - PAUSE stops the hourly weather in every server for that long. It is stored (MemoryStore `AdminEvent`, key
    `autoWeather` = `{offUntil}`), so new servers respect it. Every server re-reads it each minute and on the message.
  - It resumes by itself when the time is up; RESUME ends it early.
  - Paused, the scheduler simply waits. Admin weathers still work.
  - The row shows "AUTO WEATHER: ON" or "PAUSED 5:41:12".
- **Workspace attribute:** `WeatherAutoOffUntil` (os.time, 0 = on).

## 4. HUD: weather tiles (bottom right)
- **The tiles:**
  - One **square tile per running weather**, side by side in a horizontal row in the bottom-right corner; a new one
    slides in from the right.
  - Each tile shows its icon (saucer / meteor render), a **countdown ring** around the icon that empties as the time
    runs out, and the time ("4:12", red under 1:00).
  - Built to the Check-UI rules (solid canvas, dark outline stroke, GothamBlack + outline, UIScale responsive), with
    the weather's colour (`hex`) as the accent.
- **Hover (PC) or tap (phone)** shows the existing tip label (title + what it does).
- **Placement:**
  - On touch screens the row sits left of the jump button.
  - The Admin Abuse boost column keeps its place under Eggs/Pets/Potions and shrinks to fit above the row.
  - The weather pill leaves that column.
- **Storm tint:** standing in an area with a weather gives that weather's tint; with two in your area, the one that
  arrived last.

## 5. Stacked mutations (rule unchanged, now covered by tests)
- **The rules (already in place):**
  - An egg collects each different mutation once (`Mutations.add` / `has`).
  - `Mutations.mult` multiplies them: UFO + Meteor = x2.25, and a future third x1.5 type = x3.375.
  - The pet tag shows every tag.
  - Pet pay = base income x the mutations product, through `Money.Earn` x `Boosts.money` (friends x rebirth x Index x
    Money pass x Money potion x Money boost).
- **New tests:**
  - An egg beamed (UFO) and then struck (Meteor) carries "Meteor,UFO" and earns x2.25.
  - A third pretend type multiplies to x3.375.
  - Its pay through `Money.Earn` is base x 2.25 x the player's money multiplier.

## Error handling
- A start that fails half-way is undone for that weather only (today's `safeStart`, per type).
- STOP of a type that isn't running is a no-op.
- The auto-pause record: unreadable = treat as ON (the hourly weather keeps working), retried every minute.

## Testing
- **WeatherTests (Edit):**
  - the `Weather` list encode / decode;
  - the cutscene rule (`Logic.cutsceneFor(runningCount, startingCount)`);
  - `weatherSync` with several weathers and with stops;
  - the auto-pause logic (`Logic.autoOn(offUntil, now)`).
- **WeatherServerTests (Play, TestFreshSave):**
  - UFO and Meteor at once: both run, each has its own area and end, no cutscene stamps, waves not frozen;
  - one alone: a cutscene;
  - stop one: the other keeps running;
  - stop all;
  - the hourly scheduler does nothing while paused and while any runs;
  - the stacked-mutation egg (x2.25) and the money chain.
- **AdminServerTests:**
  - multi-select START in every server (message + record);
  - STOP selected;
  - late join with two weathers;
  - PAUSE / RESUME stored and applied.
- **Visual:**
  - two weathers at once in Play, no cutscene;
  - the tile row on PC and in the phone emulator;
  - the admin row.
