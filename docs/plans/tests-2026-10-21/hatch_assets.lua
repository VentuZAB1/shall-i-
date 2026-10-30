-- hatch_assets.lua (2026-10-21, plan 8.5): every image the HATCH NIGHT Gift window uses loads. Client datamodel (Play).
-- PreloadAsync over BrickUI.Hatch.ICON, the potion icons, StreakConfig.EGG_ICONS, every IndexConfig.PORTRAITS value and
-- the header bat (ReplicatedStorage.HatchUIAssets.Bat: its mesh + SurfaceAppearance). Expected: failed 0.
local RS = game:GetService("ReplicatedStorage")
local CP = game:GetService("ContentProvider")
local H = require(RS.BrickUI).Hatch
local ids, seen, label = {}, {}, {}
local function add(id, what)
	if type(id) ~= "string" or id == "" or seen[id] then return end
	seen[id] = true
	label[id] = what
	table.insert(ids, id)
end
for k, v in H.ICON do add(v, "ICON." .. k) end
for k, v in require(RS.PotionConfig).byKey do add(v.icon, "potion " .. k) end
for k, v in require(RS.StreakConfig).EGG_ICONS do add(v, "egg " .. k) end
for k, v in require(RS.IndexConfig).PORTRAITS do add(v, "portrait " .. k) end
-- (popup/Shop plan 7.8) the Shop + Starter Pack popup images
add("rbxassetid://109535585247625", "robuxWhite")
add("rbxassetid://93906069548754", "Reward_Star (Featured / popup icon)")
add("rbxassetid://104087244878251", "treadmill icon")
add("rbxassetid://135711525932647", "egg icon (Eggs card)")
add("rbxassetid://80829076123513", "speed icon")
add("rbxassetid://88694661500877", "cash")
add(require(RS.PotionConfig).TILE_ICON, "PotionConfig.TILE_ICON")
for _, ps in require(RS.ShopConfig).Passes do add(ps.icon, "pass " .. ps.key) end
for k, c in require(RS.SpeedBoostCards).CARDS do add(c.art, "boost art " .. k) end
-- (RIS plan 7.4 / 8.8) the Settings / Index / Rebirth images (eggs, portraits, potions, cash, shoe, star, check, glow and
-- rays are already in the lists above)
add("rbxassetid://98060718033874", "Settings header gear (BackpackButton's)")
add("rbxassetid://122195701390652", "Index book")
add("rbxassetid://107611738765467", "Rebirth paw (PET SLOT)")
add("rbxassetid://131090032079108", "Rebirth house (BASE SIZE)")
add("rbxassetid://71044264112125", "red X (need not met)")
add("rbxassetid://93838363576146", "tutorial arrow")
add("rbxassetid://131724750673548", "cash (Rebirth / Index)")
-- (UWF plan 7.3 / 8.8, 2026-10-22) the Free Gift / Welcome Back / Upgrades images (gift, cash, boost, tutorial arrow,
-- lock, check, rays, glow, star, robux and the potions are already in the lists above)
add("rbxassetid://137195579182647", "Free Gift group icon")
add("rbxassetid://108186731829732", "Free Gift heart (THUMB_EMOJI false)")
add("rbxassetid://84334196742101", "Upgrades Sling rocket")
add("rbxassetid://104553006398763", "Upgrades Grab bolt")
add("rbxassetid://131653504755402", "Upgrades Shield heart")
-- (2026-10-21 gotcha) PreloadAsync with plain "rbxassetid://" STRINGS reported Failure for every image, even ones on
-- screen: preload through throwaway ImageLabels instead (the callback still reports per content id)
local status = {}
local list = {}
for _, id in ids do local im = Instance.new("ImageLabel") im.Image = id table.insert(list, im) end
local bat = RS:FindFirstChild("HatchUIAssets") and RS.HatchUIAssets:FindFirstChild("Bat")
if bat then table.insert(list, bat) end
CP:PreloadAsync(list, function(id, st) status[id] = st end)
local ok, failed, lines, extra = 0, 0, {}, 0
for id, st in status do
	if not label[id] then extra += 1 end
	if st == Enum.AssetFetchStatus.Success then ok += 1 else failed += 1 table.insert(lines, ("FAIL %s %s (%s)"):format(label[id] or "bat part", id, tostring(st))) end
end
local missing = 0
for _, id in ids do if status[id] == nil then missing += 1 table.insert(lines, "NO STATUS " .. label[id] .. " " .. id) end end
for _, im in list do if im:IsA("ImageLabel") then im:Destroy() end end
return ("assets %d (image ids %d + %d bat contents), ok %d, failed %d, no-status %d, clock %s\n%s"):format(ok + failed, #ids, extra, ok, failed, missing,
	tostring(status[H.ICON.clock]), table.concat(lines, "\n"))
