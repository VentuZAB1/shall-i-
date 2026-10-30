-- settings_save_server.lua (2026-10-21, RIS run A): the Settings save round trip. SERVER datamodel of a TestFreshSave
-- Play session, right after the client's _G.SettingsTests("save", combo). Writes the player's save now
-- (ServerStorage.SavePlayerNow, the same write as autosave / leave), reads the STORED save back uncached
-- (ServerStorage.PlayerDataDebug "read") and compares its Settings field, key by key, with the player's attribute.
-- Refuses unless workspace TestFreshSave == true (the session key is studiotest_<TestSaveTag>_<userId>, never the real one).
local HttpService = game:GetService("HttpService")
local SS = game:GetService("ServerStorage")
if workspace:GetAttribute("TestFreshSave") ~= true then return "save: 0 pass / 1 fail\nFAIL refusing: TestFreshSave is not true" end
local p = game.Players:GetPlayers()[1]
if not p then return "save: 0 pass / 1 fail\nFAIL no player" end
local pass, fail, lines = 0, 0, {}
local function check(name, ok, detail)
	if ok then pass += 1 else fail += 1 end
	table.insert(lines, (ok and "ok   " or "FAIL ") .. name .. (detail ~= nil and (" [" .. tostring(detail) .. "]") or ""))
end
local attr = p:GetAttribute("Settings")
local okSave = SS.SavePlayerNow:Invoke(p)
check("SavePlayerNow wrote the save", okSave == true, okSave)
local stored = SS.PlayerDataDebug:Invoke("read", p)
check("the stored save has a Settings field", type(stored) == "table" and type(stored.Settings) == "string", stored and stored.Settings)
local a = HttpService:JSONDecode(attr or "{}")
local s = (type(stored) == "table" and type(stored.Settings) == "string") and HttpService:JSONDecode(stored.Settings) or {}
for _, key in {"music", "sfx", "night", "musicVol", "track"} do
	check(("%s: stored %s = attribute %s"):format(key, tostring(s[key]), tostring(a[key])), s[key] == a[key])
end
table.insert(lines, "     session key studiotest_" .. tostring(workspace:GetAttribute("TestSaveTag")) .. "_" .. p.UserId .. "; stored Settings " .. tostring(type(stored) == "table" and stored.Settings))
return ("save (server round trip): %d pass / %d fail\n%s"):format(pass, fail, table.concat(lines, "\n"))
