# SLINGSHOT: REDESIGNED HUB (design)

Date: 2026-10-21. Owner-approved choices are marked (owner).

**Why:** the owner wants a totally different hub that holds 6 players instead of 3: "I want a totally different hub, but
still to be close to the slingshot / shops etc, but still to hold 6 players / plots inside of it... How we say it, its
REDESIGNED HUB. Maybe paths are not needed, do whatever to make it better looking. If needed, take models from
toolbox." Six players per server also means more co-play, which the algorithm rewards (playbook).

**Today:**
- Map.Hub has 3 bases: Base1 (-106,6,42), Base2 (-6,6,54), Base3 (106,6,42). They grow with rebirths up to 64x120 (BaseManager / BaseBuilder, attributes MaxWidth / MaxLength).
- One shared Slingshot (0,15,-43) with its LaunchPlatform, and the runway going -Z.
- Treadmills and UpgradeSigns for each base, plus Stalls (Upgrade, Sell, with neon pad rings), Leaderboards (in-place), MarketCorners, Decor, FreeGift (owner-placed chest), Floor / FloorSides / Walls, and Spawn.
- HalloweenDecor in workspace.

---

## 1. Decisions

| Topic | Decision |
|---|---|
| Players per server | 6 (owner). The owner sets the server size in Creator Hub (Places > Server size); it can't be set from Studio. |
| Scope | A whole new hub layout, not an extension (owner). |
| Fixed | The runway, the Slingshot and the LaunchPlatform keep their exact positions: every area, egg spawner and the slingshot flight are built along the runway. |
| Layout | **A HORSESHOE** (owner): 6 plots in a U around one central plaza, open toward the slingshot / runway. Sketch: `docs/plans/hub-2026-10-21/A_horseshoe.png`. |
| Plot size | Plots still grow with rebirths, capped at **60 x 90** studs (was 64 x 120) (owner). |
| Plot look | **Basic, all 6 the same** (owner): no element themes. Later the owner will add unlockable PLOT SKINS; build the plots skin-ready (§3), but no skin system now. |
| Paths | None needed: the plaza is one open floor (owner). |
| Toolbox | Allowed for props (owner). Every model must have its scripts, tags and junk stripped before use: both sky models inserted on 2026-10-21 hid backdoor scripts. |
| Halloween | Re-placed on the new hub as a seasonal layer (one folder), easy to remove after October. |

## 2. Layout (horseshoe)

- **Plaza:** one open floor right behind the slingshot (about 185 x 180 studs), between the plots.
  - Front, nearest the slingshot: the Upgrade stall and the Sell stall, with their neon pad rings.
  - Middle: Spawn.
  - Back: the leaderboards (4 in-place boards) and the Free Gift chest with its FREE! sign and pad ring.
  - Also: MarketCorners, and decor (trees, lamps, benches) that never blocks walking lines.
- **Plots:** 2 along the left side, 2 across the back, 2 along the right side.
  - Each plot's gate faces the plaza.
  - Its treadmill and upgrade sign sit at the plaza-side corner by the gate.
  - Plots are at least 10 studs apart; nothing overlaps at max size.
- **Walk distance:** from any plot gate to the slingshot about 140 studs or less, and every plot is about the same distance (fairness).
- **Edges:** low walls or edge decor around the hub, with the map bounds / MapGuard updated. The world still floats over the SkyEnvironment cloud sea under the new anime sky.
- **Exact coordinates:** chosen by the planner from these rules and checked in a top-down render.

## 3. The plot (basic, skin-ready)

- **Look:** a clean floor (grass top + trim), the existing rebirth fence styles (they still upgrade with rebirths), a gate, a name sign with the owner's name, a treadmill, an upgrade sign.
- **Skin-ready:** every purely visual part of a plot lives in one folder `Look`: the floor top, trim, the sign's backing and decor anchors. A future skin system then swaps only `Look`.
- **Gameplay parts stay outside `Look`:** the egg placement area, pet bounds, treadmill and gate.
- No skin data, UI or purchase now (YAGNI).

## 4. Systems to update

Each one must work in all 6 plots:
- **BaseManager / BaseBuilder:** 6 bases, the max size 60 x 90, growth per rebirth (RebirthConfig.baseSize), and free/assign/release on join/leave.
- **Treadmills:** one per plot (TreadmillServer tier swaps, the AutoReconnect re-mount).
- **UpgradeSigns:** one per plot (the treadmill sign UI).
- **Stalls:** Upgrade and Sell stalls and pad rings, moved to the plaza.
- **Leaderboards:** in-place boards moved.
- **Free Gift:** the chest moved into the plaza, with its FREE! sign and pad ring.
- **Spawn:** the new players' spawn, plus the respawn on their own plot (BaseSpawnCamera).
- **Map bounds:** Walls, Map.Bounds and MapGuard; the VIP rooms (VipDoor) if they sit in the hub.
- **IntroCutscene:** its hard-coded world coordinates (puppet avatar, camera path).
- **Trailer:** its hard-coded camera path.
- **Tutorial:** the arrows/targets (stalls, treadmill, own plot, slingshot).
- **"On your base" line:** OfflineClient's "You earn $X/Day" line (uses the plot floor).
- **Weather:** the UFO/Meteor targets near the hub, if any.
- **HalloweenDecor:** the lamps (night boost), grime, spiders, garlands.
- **Thumbnail stage:** strip tags on any copies (the 2026-10-21 rule).

## 5. Build approach (safe)

- **Build in a staging model:** the new hub is built as `Map.HubV2`, away from the live hub. When it's done and tested, it is swapped in.
- **Rollback:** the old `Map.Hub` (+ HalloweenDecor) is moved whole into `ServerStorage._Backup_Hub.Before` for a one-step rollback.
- **Pipeline:** the owner's Opus pipeline:
  1. planner: exact layout + an audit of every system in §4, with the file/line changes
  2. plan reviewer
  3. builder in stages: plaza → plots → props/decor → re-pointing → swap
  4. visual reviewer (top-down + player-height shots)
  5. performance check: part/instance count, the cost of 6 grown plots with pets, low-end phones
- **Studio:** one builder in Studio at a time. It starts after the HATCH NIGHT Gift window build.
- **Owner's hand edits:** the owner may hand-edit the map afterwards. The tests must not depend on exact decor.

## 6. Testing

Studio, TestFreshSave sessions only:
- **6 bases:** hand out and free 6 bases. Use a debug hook to assign test plots, since a 6-client local server needs the owner's Studio UI.
- **Growth:** every plot grows R0 → R5 to 60 x 90 with no overlaps or fence clipping.
- **Pets:** a late-game pet count (20+ pets at max KG size) fits and wanders inside the plot.
- **Each plot:** the treadmill run / tier swap / AutoReconnect re-mount, and the upgrade sign.
- **Tutorial:** start to finish in every plot; the intro cutscene plays right.
- **Hub:** the stalls, the Free Gift chest, the leaderboards, and the map bounds (no escape, no stuck spots).
- **Screenshots:** top-down, player-height from each plot, and night mode.
- **Performance:** frame time and part count vs today.

## Out of scope (later)

- Plot skins (unlockable), element-themed plots, new monetization in the hub.
