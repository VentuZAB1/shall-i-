# Overworld (cloud sea) — progress ledger (2026-10-22)

Owner ask: "put something in the overworld not only the animated sky, but also the bottom ... when players fly they see the overworld ... make it look pretty there too."
Coordinator: 3 options first, then the OWNER PICKED **A: soft stylized cloud sea a good distance below + a few distant floating islands**. B / C were never built.

## Rules in force
- Don't touch Sky / terrain Clouds / Atmosphere / Lighting / hub / runway.
- Publish-safe at all times: build in `ServerStorage._OverworldPreview`, put in workspace only while capturing, nothing new left in workspace between steps; final = `workspace.Overworld` (attr `_Overworld = true`), in the Revert module.
- Phone cost: few meshes, anchored, CanCollide / CanQuery / CanTouch false, CastShadow false. Toolbox: strip every script + tag.
- End in Edit, TestFreshSave false.

## Measurements (before)
- Nothing below the map (raycasts to y -350 hit nothing). Sky bottom = flat light blue.
- Map: hub x ±222, z -67..178 (floor y 0); runway x ±80, z -60..-2480 (areas every 400 studs), bottom y -18.
- StreamingEnabled = true → the overworld must be a **Persistent** model (like Map.Bounds) or far clouds stream out.
- Atmosphere Density 0.20 / Haze 0.10 (fades far things to light blue = soft horizon for free).
- MapGuard: raycast Include = workspace.Map only; VOID_Y = -60 (players below -60 go back to their last safe spot). FallenPartsDestroyHeight -500. Flights peak ~600 studs up.
- "Before" shots: `final/before_day_V1..V5`.

## Fixed views
- V1 flight over area 1: cam (25,150,-60) → (-40,-60,-620)
- V2 flight over area 3: cam (-40,300,-760) → (60,-80,-1350)
- V3 flight over area 6 (high): cam (20,520,-1750) → (-80,-140,-2600)
- V4 hub edge: cam (150,60,30) → (900,-220,120)
- V5 overview: cam (1100,950,900) → (0,-150,-1100)

## Asset research
- Cloud puff: the classic Roblox cloud mesh **1095708** + texture 1095709 (an official 2008 Roblox asset; soft white with a blue underside, matches the anime sky). **854 tris** (measured: Toolbox model 425604289 = 12 of them = 10,248 tris; cache LOD0 = 854). Made into a MeshPart with AssetService:CreateMeshPartAsync (RenderFidelity Automatic → auto-LOD 854 / 426 / 212 ...).
- Floating island: "Floating Island" by **Starblaze Games** (verified creator, 16519830532, no scripts). Full model 14,074 tris / 209 parts (incl. a SpawnLocation + a 166-block plaza). Kept only body (rock) + grass top + grass patch + some trees. Cache LOD0: trunk 320, leaves 646 per tree; body+grass+patch ≈ 1,480.
- Islets: "Floating Island [v2]" 11127736760 (2 MeshParts, 1,478 tris, untextured → recoloured to the Starblaze palette).
- Rejected: spam re-uploads of clouds/islands (several carried backdoor scripts: `CoreSkyboxSystem`, `DO NOT DELETE.Material` — stripped, not used).

- **2026-10-22: OVERWORLD CANCELLED BY THE OWNER** ("just forget the ground to have clouds etc, just test the needed things"). Nothing built was kept: `ServerStorage._OverworldPreview` (my test pieces only: the Toolbox candidates with their scripts stripped, the templates and a cloud-sea builder) was deleted. Nothing overworld-related is in workspace. Studio is idle in Edit with TestFreshSave false.
