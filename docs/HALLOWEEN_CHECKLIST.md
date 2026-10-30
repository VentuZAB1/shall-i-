# Halloween hub - live checklist (2026-10-12)

## What is in the place (Studio, not yet published)
Everything new lives in `Workspace.HalloweenDecor`, with its motion in
`StarterPlayer.StarterPlayerScripts.HalloweenClient` (client-side only).

**Back wall**
- `GiantPumpkin`: the giant jack-o'-lantern behind the back wall. It watches each player; fire glows inside, with eye glows and smoke.
- Bat flock: 12 bats, spawned client-side into `HalloweenDecor.Bats`. Template `ReplicatedStorage.HalloweenBat`, animation clips `ReplicatedStorage.CreatureClips.Bat`.
- `Garlands`, `Webs`, `Vines`.

**Hub floor**
- `PumpkinEggs`: 12 clusters with candles and lights.

**Garden** (`Garden`, one folder per bed):

| Piece | Count |
|---|---|
| TPTree | 5 |
| DeadTree | 5 |
| HauntedTree | 3 |
| Bush_Thorn (cobweb + spider) | 7 |
| Bush_TP | 4 |
| Bush_Autumn | 3 |
| Bramble | 3 |
| Grave_A / B / C (where the rocks were) | 3 |
| DeadGrass | 64 |

**Spiders**
- `Spiders` holds 24 spiders: 4 on the wall, 7 on thorn bushes and 13 on the trees. They bob on silk threads.
- The threads are anchored to `SpiderAnchors`.

**Templates and backup**
- Imported templates: `ServerStorage.HalloweenTemplates`.
- The original garden pieces are in `ServerStorage.HalloweenGardenBackup`: 97 models, nothing deleted. Each model has
  an `OriginalParent` attribute.
- The 6 raised round beds (`Soil` + `Border` parts) were removed on the owner's request, so they're no longer
  "floating islands". They are in the backup too. The garden now stands on the hub floor.
- The yellow flowers and small stones stayed. They were lowered 0.95 to the floor and tagged with a `HalloweenDrop`
  attribute so the restore can lift them back.
- The 17 red toadstools ("Mushrooms") were removed from the hub on the owner's request. They are in the backup at their
  original height.

## To go live
1. In Studio: **File > Save to Roblox**, then **Publish**.
2. Creator Hub (or Studio's Game Settings): **Migrate to Latest Update**, so running servers pick it up.
3. Check on a phone once it is live. The garden adds roughly 750k triangles (Roblox reduces distant meshes
   automatically; the thin webs, paper and branches are set to Precise so they don't break up).

## After Halloween - put the normal hub back
Paste this in Studio's command bar (Edit mode), then Save + Publish:

```lua
-- restore the original garden (beds + pieces) and store the Halloween decor for next year
-- 1) the toadstools / flowers that stayed were lowered 0.95 when the raised beds were removed: lift them back
for _, m in workspace.Map.Hub.Decor.Gardens:GetDescendants() do
	local d = m:IsA("Model") and m:GetAttribute("HalloweenDrop")
	if d then
		m:PivotTo(m:GetPivot() + Vector3.new(0, d, 0))
		m:SetAttribute("HalloweenDrop", nil)
	end
end
for _, g in workspace.Map.Hub.Decor.Gardens:GetChildren() do g:SetAttribute("BedRemoved", nil) end
-- 2) everything in the backup (trees, bushes, rocks, grass, the Soil + Border bed parts) goes back where it was
local backup = game.ServerStorage:FindFirstChild("HalloweenGardenBackup")
if backup then
	for _, m in backup:GetDescendants() do
		local path = (m:IsA("Model") or m:IsA("BasePart")) and m:GetAttribute("OriginalParent")
		if path then
			local parent = game
			for name in path:gmatch("[^%.]+") do parent = parent and parent:FindFirstChild(name) end
			if parent then
				m:SetAttribute("OriginalParent", nil)
				m:SetAttribute("HalloweenKind", nil)
				m.Parent = parent
			end
		end
	end
end
local decor = workspace:FindFirstChild("HalloweenDecor")
if decor then decor.Parent = game.ServerStorage end -- HalloweenClient does nothing without it
```

## Tuning knobs
- **Head:** the `HalloweenClient` constants (YAW / PITCH, spring speeds).
- **Fire:** `GiantPumpkin.FireBed`. Keep the flame quads inside the shell; the 34x2x14 bed and the 16/24/20 sizes
  are what fixed the glow leaking under the head.
- **Bats:** `BAT_COUNT` (12) and the bank limit in the "bats" section of `HalloweenClient`.
- **Spiders:** the `BobAmp` / `BobPeriod` attributes on each spider model.
