# SLINGSHOT phone FPS audit (2026-10-27): read-only

Auditor: Claude (Opus), read-only. Studio stayed in Edit and nothing was written, played or edited. Every number below
comes from `execute_luau` reads in Edit, the pre-swap backup `ServerStorage._Backup_Hub.Before`, the
`_Backup_HubMakeover.Before` / `_Backup_RunwayDecor.Before` backups, script source, or memory notes.

The trigger: the Creator Hub shows average client FPS **28, down 24% this week** (~37 before). Most players are on phones.

---

## 0. The short version

**The decor is not what got heavier this week. The number of players per server did.**

- Static hub geometry went DOWN by two thirds.
  - Hub + HalloweenDecor source triangles: **1.92M -> 0.66M**.
  - PBR SurfaceAppearances: **410 -> 150**.
  - The runway lost ~4,100 decor parts (10-21 cleanup).
- What went UP:
  - **Plots: 3 -> 6.** The live server size was 3 and the V2 hub is built for 6.
  - Each phone now draws and animates up to **2x avatars, pets, plot eggs, pet tags and treadmills**.
  - The horseshoe puts **all 6 plots inside the 220-stud pet "animate" range** from anywhere in the hub.
- Second suspect, outside the map: **the player mix changed**. DAU went 72 -> 306 in 5 days, ~91% of new players come
  from ads, and these are probably lower-end phones. A device-mix shift alone can move an average FPS by this much.
  **Check it first** (section 6, owner check 1). It is free.

The zero-visual cuts (section 5A) make each extra player and pet cheaper: culling off-screen pets and tags, throttling
flicker writes, turning off the daytime-invisible finial lights. Estimated gain: **+3 to +6 FPS** on a mid phone in a
full 6-player hub. The visible cuts (5B) are for the owner to judge.

---

## 1. What this week changed (before = `_Backup_Hub.Before`, the live state up to 10-21)

| Item | Before | Now | Change | FPS effect |
|---|---|---|---|---|
| Plots / players per server | 3 bases, server size 3 | 6 bases, server size 6 | **x2** | **worse** |
| Hub + Halloween parts | 2,008 + 535 = 2,543 | 2,489 + 273 = 2,762 | +9% | ~0 |
| Hub + Halloween source triangles (EditableMesh face count) | ~1.92M | ~0.66M | **-66%** | better |
| Runway parts | ~6,175 | 2,073 | -4,100 (10-21 cleanup) | better |
| PBR SurfaceAppearances in hub decor | 410 | 150 | -63% | better |
| Local lights in hub | 29 | **43** | **+14** (lanterns 8 PL + 8 Spot, finials 8 PL; -8 old lamp spots, -2 pumpkin eggs) | worse |
| Shadow-casting local lights | 14 | 13 | -1 | same (but more movers near them, see cause 3) |
| Grime decal/texture carriers | 89 | **118** | +29 (82 are tiled Textures now) | slightly worse |
| Leaderboard SurfaceGuis | 4 | 8 (double-sided) | +4 | slightly worse (memory) |
| Treadmills / upgrade signs | 3 / 3 | 6 / 6 | x2 | slightly worse |
| Post effects | DoF **ON**, SunRays 0.08, Bloom 0.4 | DoF **OFF**, SunRays 0.05, Bloom 0.4 | DoF removed | better |
| Terrain Clouds, cloud-sea client (SkyEnvironment) | on since 09-29 / 10-07 | same | none | same |
| New UI loops (Starter Pack HUD, Streak, REBIRTH READY, tutorial step 11) | none | 6 RenderStepped loops | all gated on Visible/Enabled | ~0 |
| Audience | DAU 72 (10-22) | DAU 306 (10-27), 3,706 of 4,079 new users from ads | mix shift | **worse (unverified)** |

---

## 2. Cost table per folder / system (now)

"Tris" = source mesh face count read through `AssetService:CreateEditableMeshAsync`. Toolbox / leaderboard meshes
refused permission. Shadow = CastShadow on a visible part. Phone cost is my estimate.

| Folder / system | Parts | MeshParts (unique) | Tris | Unions | Decals+Tex (unique) | SurfaceGui / Billboard | Lights (shadowed) | Particles / Beams | Shadow casters | Phone cost |
|---|---|---|---|---|---|---|---|---|---|---|
| Map.Hub.Bases (6 plots, static) | 1,782 | 0 | - | 0 | 0 | 0 / 6 owner cards | 0 | 0 | 0 | Low (static blocks); the runtime load is in the rows "pets / eggs / avatars" |
| Map.Hub.Walls (13 runs, 42 pillars) | 202 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | Low |
| Map.Hub.Decor (Lanterns 40, Ground 81, Plaza 5) | 126 | 8 (1) | 25K | 0 | 0 | 0 | **16 (0)**: 8 PL R14 B2.2 + 8 Spot R18 B2, on all day | 0 | 8 | Medium |
| Map.Hub.Treadmills | 114 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | Low (+ belt script, cause 4) |
| Map.Hub.Stalls | 165 | 0 | - | 6 | 0 | 6 / 0 | 0 | 0 | 2 | Low |
| Map.Hub.Leaderboards (4 + 4 _Back) | 28 | 28 (6) | n/a | 0 | 0 | 8 at 477x647 px | 0 | 0 | 8 | Low-Medium (2.5M GUI px) |
| Map.Hub.UpgradeSigns | 24 | 0 | - | 0 | 0 | 6 at 619x379 px (164 px/stud) | 0 | 0 | 0 | Low |
| Map.Hub.FreeGift | 33 | 0 | - | 3 | 0 | 0 / 1 | 0 | 1 (5/s) | 28 | Low |
| Map.Hub.Slingshot | 5 | 5 | 17K | 0 | 0 | 0 | 0 | 2 beams | - | Low |
| HD.WallDecor: Finials 38 / Garlands 36 / Bats 12 / Hands 4 / Webs 4 | 94 | 94 (10) | **353K** (finials 133K) | 0 | 0 | 0 | 8 (0): finials B0.3 R10 | 0 | 0 | Medium (86 PBR SA; 46 Precise = no LOD) |
| HD.GateDecor (12 candle clusters) | 24 | 24 (2) | 79K | 0 | 0 | 0 | 0 | 0 | 0 | Low-Medium (24 PBR SA) |
| HD.Grime (moss / cracks / drips / floor) | 118 | 0 | - | 0 | **118 (14)**: 82 tiled Textures, 36 Decals, ~7,900 studs² of alpha | 0 | 0 | 0 | 0 | Medium (118 separate alpha draws) |
| HD.StreetLamps (pumpkin heads) | 8 | 8 (1) | 28K | 0 | 0 | 0 | **8 (8)**: R11, Flicker 1.4, brightness written every frame | 16 (~34/s) | 8 | **Medium-High** |
| HD.PumpkinEggs (5 wall clusters) | 16 | 16 (6) | 73K | 0 | 0 | 0 | **10 (5)**: all flicker every frame | 25 (~25/s) | 16 | Medium |
| HD.GiantPumpkin (watching head) | 8 | 6 (6) | 52K | 0 | 0 | 0 | 1 (0): **R70** (engine max 60), B6, flickers + moves every frame | 8 (~72/s) | 3 | Medium (BulkMoveTo every frame) |
| HD.Spiders | 4 | 4 (1) | 28K | 0 | 0 | 0 | 0 | 4 beams | 0 | Low |
| Map.Runway (6 areas) | 2,073 | 1,152 (26) | n/a (Toolbox) | 0 | 0 | 72 VIP door guis, on Transparency 1 parts | 0 | 14 Fire | **469** | Medium on the runway (1,070 Precise meshes), ~0 in the hub (streamed / culled) |
| Map.Bounds | 18 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | none (invisible, CanQuery off) |
| SkyEnvironment (client) | 18 cells of 2048x2048 | 0 | - | - | 18 tiled cloud Textures (2 layers), offsets at 20 Hz | - | - | - | 0 | Medium (2 big alpha layers when looking out; the upper layer is already skipped at quality <= 3) |
| Lighting | - | - | - | - | - | - | - | - | - | Medium, pre-existing: GlobalShadows, Future (owner-set), Bloom size 26, SunRays 0.05, ColorCorrection, Atmosphere 0.2, Terrain Clouds 0.52; DoF now OFF |
| **Runtime: pets** (`workspace.LocalPets`, client) | 3 + rebirths per plot (~126 at 6 x R4) | 1 skinned mesh each, ~25 bones | - | - | - | 1 PetTag billboard each | 0-1 | 0-4 tier emitters + 1-3 aura emitters (100K+ KG) | **all cast** | **HIGH**: Lua bone blending each frame, skinning, shadow pass |
| **Runtime: plot eggs** | 6-20 slots per plot, ~58 parts per egg model | - | - | - | - | timers | 0 | - | 0 | Medium (x2 plots) |
| **Runtime: avatars** | 6 (was 3) | - | - | - | - | name tags | - | - | cast | Medium-High (layered clothing, humanoids) |
| Runtime: flying bats (HalloweenClient) | 12 skinned | 12 | - | - | - | - | - | - | - | Low-Medium (bones every frame within 450 studs = the whole hub) |
| ServerStorage backups (`_Backup_*`, `HubV2Kit`, ...) | ~20K+ | - | - | - | - | - | - | - | - | **none** (ServerStorage never replicates to clients) |

Other checks:
- Unanchored parts in Map / HalloweenDecor: 0.
- Unions: 9 in total (stalls, chest), so union triangle cost is negligible.
- Static particles in the whole workspace: 139 particles/s in total. Low.
- Highlights: 0.

---

## 3. Client scripts that run every frame (relevant ones)

| Script | What runs every frame | Scales with | Notes |
|---|---|---|---|
| `StarterPlayerScripts.PetAnimator` (RenderStepped) | `model:PivotTo` for **every** pet, always; `CreatureAnimator:step` (bones) + VFX for every pet within `ANIMATE_RANGE = 220` | pets | No off-screen check. From the plaza all 6 plots are within 220 (plots at 60-170 studs). |
| `ReplicatedStorage.CreatureAnimator:step` | ~25 bones x 1-3 layers of CFrame lerps + Bone.Transform writes; **new `target` / `layers` / per-layer tables every call** | pets | Benchmark (math only, no Transform writes, this PC): **0.6 ms for 63 pets, 1.1 ms for 126**. Phones are several times slower. Transform writes, PivotTo and GPU skinning come on top. |
| `StarterPlayerScripts.BaseSignFloat` (RenderStepped) | for **every** PetTag in the server: 2 `WorldToViewportPoint`, 2+ new tables, then a `table.sort` with a closure | pets | PetTag `MaxDistance = 120`, but tags beyond 120 are still processed. |
| `StarterPlayerScripts.HalloweenClient` | Heartbeat: Brightness write on 14 flicker lights within 220 (the whole hub), 4 spiders PivotTo. RenderStepped: giant pumpkin BulkMoveTo (moves its R70 light). Heartbeat: 12 bats BulkMoveTo + bones | fixed | Pre-existing (10-12), but cheap to throttle. |
| `StarterPlayerScripts.TreadmillClient` (2 x RenderStepped) | belt texture offsets + **chevron CFrame writes for all treadmills, idle or not** | plots (3 -> 6) | No distance / screen check. |
| `StarterPlayerScripts.LeaderboardScroll` | 8 boards within 260 studs: CanvasPosition only on change; the scroll bar Size/Position is re-set each frame | boards (4 -> 8) | Low. |
| `SkyEnvironment` | grid re-place on cell change, texture offsets at 20 Hz | fixed | Low (already throttled). |
| UI: StarterPackHud / StarterPackClient / StreakClient / RebirthClientLegacy / PlaytimeClient / TutorialClient / Offline / FreeGift / Upgrade | sunburst rotations, bobs, pulses | - | **All gated** on `gui.Enabled` / `Visible` / `running`, so nothing animates while a window is closed. Low. |
| WaveClient, EggClient, SlingshotVisuals, SpeedFeel, SpeedUI | runway / own-player work | - | Not changed this week. |

---

## 4. Top 5 likely causes, ranked

### 1. Twice the players per server, and every plot is in view and in animate range (HIGH)
Evidence:
- The old hub had **3 bases**; memory says the live server size was 3. The V2 hub (live this week) has **6 bases** and
  the spec asks for server size 6.
- Base pivots: plots sit at (+/-165,-30), (+/-133,42), (+/-40,121). **All 6 are within 220 studs of the spawn (0,52)**,
  so `PetAnimator` bone-animates every pet on every plot and keeps every pet VFX emitter on.
- Pets: one skinned mesh each, ~25 bones, CastShadow ON (shadow pass). Each also carries a PetTag billboard and 0-4 tier
  emitters, plus 1-3 aura emitters at 100K+ KG (the 1M+ "haze" is large translucent smoke).
- The memory budget test for the hub used 6 x R4 = **126 pets**. Ad players are mostly R0-R1, so a typical full
  server has ~25-40 pets. Either way it is 2x what 3 plots produced.
- 2x avatars (humanoids, layered clothing), 2x plot eggs (~58-part models, 6-20 slots per plot), 2x treadmills.
- Benchmark: the blend math alone doubles from 0.6 to 1.1 ms on this PC (63 -> 126 pets) before Transform writes,
  PivotTo and skinning. On a phone at 28 FPS (35.7 ms per frame), the pet pipeline plausibly costs **5-12 ms per frame**
  in a full late-game server.

### 2. Player and device mix shifted to ad traffic (HIGH, not verified)
Evidence:
- DAU 72 (10-22) -> 306 (10-27). 3,706 of 4,079 new users in 56 days came from Sponsored Ads (PLAYS objective since
  ~10-22).
- Ad audiences skew to cheaper phones, and many phones are capped at 30 FPS. An average of 28 is exactly what a mostly
  30-capped crowd produces.
- A pure mix shift lowers the AVERAGE with no change in per-device performance.
- This could be most of the -24%. Verify it before spending effort (section 6).

### 3. More local lights in the plaza, and shadowed pumpkin lights rewritten every frame with more movers near them (MEDIUM-HIGH)
Evidence:
- **43 local lights** (was 29), clustered in the hub.
  - New this week: 16 lantern lights (PointLight R14 B2.2 + SpotLight R18 B2, on all day) and 8 finial lights (B0.3,
    effectively invisible by day).
- **13 lights have Shadows = true** (8 street-lamp pumpkins, 5 wall pumpkin eggs).
  - All 13 flicker: `HalloweenClient` writes `Brightness` on every Heartbeat for every flicker light within 220 studs,
    which is all of them.
- Cost on phones by lighting tier:
  - Future-capable phones: a shadowed point light has to re-render its shadow when things move inside its range.
    Avatars and pets near the street lamps doubled with cause 1.
  - Lower phones (voxel fallback): per-frame light changes keep the lighting update busy.
- The GiantPumpkin `FireLight` is set to Range 70 (the engine caps it at 60). It is B6, flickers, and moves every frame
  with the head. It is pre-existing, but it is the single biggest light.

### 4. Per-frame Lua that ignores the camera and grows with pets / plots (MEDIUM)
Evidence (section 3):
- `PetAnimator` animates pets behind the camera. The horseshoe surrounds the plaza, so roughly half the plots are
  behind you at any moment.
- `PetAnimator` also PivotTo's every pet every frame, even resting ones.
- `BaseSignFloat` processes all pet tags every frame, including the ones beyond their own 120-stud MaxDistance.
- `CreatureAnimator` allocates ~3+ tables per pet per frame, which means GC hitches on phones.
- `TreadmillClient` moves the chevrons of all 6 treadmills every frame.
- These costs are not new, but every one of them doubled with cause 1. They are also the easiest wins, because culling
  is invisible.

### 5. Alpha layers and PBR decor on the walls (MEDIUM-LOW)
Evidence:
- **118 grime carriers**, each its own alpha-blended decal/texture draw (not instanced). They cover ~7,900 studs² of
  wall and floor, which fills much of the screen from the plaza. Mobile GPUs pay for every blended pixel.
- Up from 89 last week, and 82 of them are now tiled Textures.
- 110 PBR SurfaceAppearance meshes on the new wall/gate decor. 46 are `RenderFidelity = Precise` (no LOD), including
  38 finials at 3,500 tris each.
- Context: total decor triangles and PBR count both DROPPED this week (section 1). This is a "could be cheaper" item,
  not the cause of the drop.

Ruled out:
- Total part/triangle count (down).
- Post-processing (DoF was turned off this week: cheaper).
- Static particles (139/s).
- UI loops (gated).
- Unanchored parts (0).
- Backups (ServerStorage).
- Terrain Clouds and the cloud sea (unchanged since 09-29 / 10-07).

---

## 5. Cuts

### 5A. Zero visual change: can be applied right away (back up first per the vault rules)

| # | Cut | Where | Visible | Expected gain (mid phone, full 6-player hub) |
|---|---|---|---|---|
| Z1 | **Skip bones + VFX for pets outside the camera view** (WorldToViewportPoint with a ~30% margin + pet height; resume on entry, the motion is time-based so nothing jumps). Also skip `PivotTo` for off-screen pets. | `PetAnimator.updatePet` | none | **-2 to -6 ms** (~40-60% of pet CPU; half the plots are behind the camera) = **+2 to +4 FPS** |
| Z2 | **BaseSignFloat: only tags that are Enabled, within 120 studs (their MaxDistance) and on screen**; run the overlap pass at 15-20 Hz; reuse the tables (no per-frame allocation, no closure sort). | `BaseSignFloat` | none (tags beyond 120 are not drawn anyway) | -0.5 to -2 ms |
| Z3 | **CreatureAnimator: reuse `target` / `layers` / layer tables** per animator instead of allocating per step. | `CreatureAnimator:step` | none | fewer GC hitches (smoother frame times; 0.2-1 ms average) |
| Z4 | **Finial PointLights (8 x B0.3) enabled only when `Lighting.NightMode` is on**: HalloweenClient already tracks night, so add `l.Enabled = isNight` for the Finial lights. | `HalloweenClient` (Finials have NightBrightness 1.6 / NightRange 14) | none by day (0.3 under a 2.4 sun is invisible); night unchanged | 8 fewer lights in the plaza for every Day player (most players) |
| Z5 | **Flicker writes at ~20 Hz** instead of every Heartbeat, and only for lights within ~120 studs. Same noise, sampled less often. | `HalloweenClient` Heartbeat | none (a 7 Hz shiver still reads at 20 Hz) | ~3x fewer light updates: matters most on voxel-fallback phones, ~0.3-1 ms |
| Z6 | **Flying bats: bones only when on screen** (BulkMoveTo still runs, so they keep their path). | `HalloweenClient` bats loop | none | -0.2 to -0.5 ms |
| Z7 | **TreadmillClient: skip slats / chevrons of treadmills that are off screen or > 150 studs** (offsets are time-accumulated, so no jump). | `TreadmillClient` (both loops) | none | -0.1 to -0.4 ms |
| Z8 | **CanTouch = false on pure-decor parts** with no Touched listener: leaderboard meshes (24), stall body parts (keep the walk-in zones), chest body parts (keep `FreeGiftZone`). Walls keep CanQuery (the camera uses it). | `Map.Hub.Leaderboards / Stalls / FreeGift` | none | tiny (physics broadphase) |

**Total for Z1-Z8: about -3.5 to -10 ms per frame = roughly +3 to +6 FPS** from 28 at a full late-game 6-player hub.
The gain is smaller in light servers. This is an estimate from the benchmark and the script structure; it is not a
phone measurement.

### 5B. Visible cuts: the owner judges (screenshots before/after; lighting rule: ask first)

| # | Cut | Visible | Expected gain |
|---|---|---|---|
| V1 | **Shadows = false on the 13 pumpkin lights** (8 street lamps, 5 wall pumpkin eggs). | none by day; **slight at night**: the carved-face light pattern becomes a round glow | **Medium on Future-capable phones** (no shadow re-renders when players / pets walk by): -1 to -4 ms |
| V2 | Lantern lights by day: SpotLight `GroundLight` off by day (keep the Neon bulb + PointLight), or both at half range by day; full at night. | slight by day (softer warm pools on walls) | 8-16 fewer lights by day: -0.5 to -2 ms |
| V3 | GiantPumpkin `FireLight`: Range 70 -> 40-45 (60 is the real cap) and/or a gentler flicker at 20 Hz. | slight (owner check on the pumpkin glow) | -0.3 to -1 ms |
| V4 | Far pets: bones at half rate beyond ~90 studs; `CastShadow = false` for pets beyond ~70 studs (hysteresis). | slight (distant pets a bit less smooth, no tiny far shadows) | -1 to -3 ms in full servers |
| V5 | Grime by quality: hide `HalloweenDecor.Grime` when the saved graphics quality is <= 3 (the same switch `SkyEnvironment` already uses for its upper cloud layer). | **clear for low-quality phones only**; no change on PC or high quality | -118 alpha draws on the weakest phones |
| V6 | Decor `RenderFidelity` Precise -> Automatic: 38 finials, 4 hands, 4 webs, 8 lantern cages, 4 spiders (and the 1,070 Precise runway meshes). | none up close, slight at range | -0.5 to -1.5 ms GPU at range (mostly the runway) |
| V7 | SunRays off (Intensity is already only 0.05); Bloom Size 26 -> 16. | slight (only toward the sun / on bright edges) | one full-screen pass less + a cheaper blur: -0.5 to -1.5 ms on phones |
| V8 | Pet aura "haze" (1M+ KG, large translucent smoke) at half Rate on touch devices. | slight | overdraw in late-game servers |
| V9 | Streaming (owner sets in Workspace Properties; the plugin can't read these): `StreamOutBehavior = Opportunistic`, `StreamingTargetRadius` ~512. The hub is compact (< 400 studs), so the hub is unaffected; far runway areas leave phone memory. | slight (far areas stream in when you get closer) | phone memory, fewer memory-pressure stalls; little hub FPS |

Not recommended:
- CastShadow off on all decor. The hub is already nearly shadow-free (Hub 49, HalloweenDecor 27 casters). The 469
  runway casters are natural props the owner wants grounded (10-13 rule).
- Removing grime that "sits behind other decor". The rollout engine already kept carriers clear of plots, boards,
  stalls, lamps and pillars, and I found no hidden carriers. Merging would mean re-baking textures, which is a visible
  risk.

---

## 6. Owner checks (things I can't read from the Studio plugin)

1. **Creator Hub > Analytics > Performance: filter client FPS by platform / OS / device**, this week vs last.
   - If phone FPS on its own is flat and only the mix moved toward phones, the map isn't the cause (cause 2).
   - If phone FPS itself dropped from ~10-23 (publish), causes 1/3/4 are confirmed.
2. **Creator Hub > Places > Server size**: confirm it is 6 now (it was 3).
3. **Workspace Properties > StreamingTargetRadius / StreamingMinRadius / StreamOutBehavior**: these are not readable
   from the MCP plugin. Note the values for V9.
4. **On a real phone:** Roblox app > Settings > Micro Profiler ON, then open the shown address on the PC. Alternatively,
   Developer Console (`/console`) > ScriptProfiler, in a full hub. This confirms PetAnimator / BaseSignFloat /
   HalloweenClient times before and after Z1-Z7.
   - Studio's own FPS / draw-call counters are frozen when Studio is unfocused (memory gotcha), so don't use them.

## 7. Method notes
- Counts: workspace descendant walks per folder; pre-week numbers from `_Backup_Hub.Before` (Hub_Old + HalloweenDecor),
  `_Backup_HubMakeover.Before.Removed` and `_Backup_RunwayDecor.Before`.
- Triangles: `AssetService:CreateEditableMeshAsync` + `#GetFaces()`, in memory and destroyed. Toolbox runway meshes and
  leaderboard meshes refused permission (shown as n/a).
- Benchmark: pure Luau CFrame-lerp loop shaped like `CreatureAnimator:step` (25 bones x 2 layers), no instances; best of
  20 runs.
- Nothing was created in, changed in or removed from the place. Studio was left in Edit. TestFreshSave was false
  throughout and was not touched.
