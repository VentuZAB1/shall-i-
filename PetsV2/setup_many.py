# python setup_many.py A B C -> one Luau chunk that sets up several imported models (and moves loose clip modules)
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(here, "studio_setup.lua"), encoding="utf-8").read()
body = tpl.split("local CFG = __CFG__", 1)[1]
cfgs = []
for n in sys.argv[1:]:
    m = json.load(open(os.path.join(here, n, n + "_meta.json")))
    cfgs.append('{name = "%s", display = "%s", height = %s, motion = "%s", rig = "%s", stride = %.5f, walk_len = %.4f, glow = {%s}, light = 1.2}' % (
        m["name"], m["display"], m["height"], m["motion"], m["rig"], m["stride"] or 0, m["walk_len"] or 1,
        ", ".join('"%s"' % g for g in m["glow"])))
out = ["local RS = game.ReplicatedStorage", "local results = {}",
       "local function clipFolders()", "	local t = {}",
       "	for _, s in {game.ServerStorage, workspace} do for _, f in s:GetChildren() do",
       "		if f.Name == \"PetsV2Clips\" then table.insert(t, f) end end end", "	return t", "end",
       "local function setup(CFG)"]
out.append(body.replace("\nreturn string.format(", "\nreturn string.format("))
out.append("end")
out.append("for _, CFG in {" + ", ".join(cfgs) + "} do")
out.append("\tlocal ok, r = pcall(setup, CFG)")
out.append("\ttable.insert(results, ok and r or (CFG.name .. ' ERROR ' .. tostring(r)))")
out.append("end")
out.append("-- loose clip modules for pets whose model was already set up (clip-only updates)")
out.append("for _, f in clipFolders() do")
out.append("\tif f.Name == 'PetsV2Clips' then")
out.append("\t\tfor _, mod in f:GetChildren() do")
out.append("\t\t\tlocal old = RS.CreatureClips:FindFirstChild(mod.Name)")
out.append("\t\t\tif old then old:Destroy() end")
out.append("\t\t\tmod.Parent = RS.CreatureClips")
out.append("\t\t\ttable.insert(results, 'clips updated: ' .. mod.Name)")
out.append("\t\tend")
out.append("\t\tf:Destroy()")
out.append("\tend")
out.append("end")
out.append("return table.concat(results, '\\n')")
src = "\n".join(out)
src = src.replace("local RS = game.ReplicatedStorage\n", "", 1) if src.count("local RS = game.ReplicatedStorage") > 1 else src
print(src)
