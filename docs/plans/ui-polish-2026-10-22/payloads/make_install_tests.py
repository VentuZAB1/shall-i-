# make_install_tests.py: install_tests.lua = one execute_luau (Edit) that writes the polish test modules into
# ServerStorage.UIPolishTests (source hash-checked against the files on disk).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_apply import fnv, lua_str
HERE = os.path.dirname(os.path.abspath(__file__))
PLANS = os.path.dirname(os.path.dirname(HERE))
files = [("checkui_contain", os.path.join(PLANS, "tests-2026-10-21", "checkui_contain.lua")),
         ("polish_client", os.path.join(os.path.dirname(HERE), "polish_client.lua")),
         ("polish_server", os.path.join(os.path.dirname(HERE), "polish_server.lua"))]
out = ['-- install_tests.lua (2026-10-22 UI polish): ServerStorage.UIPolishTests.<module>, hash-checked',
       'local SS = game:GetService("ServerStorage")',
       'local function fnv(s) local h = 2166136261 for i = 1, #s do h = bit32.bxor(h, string.byte(s, i)) h = ((h % 256) * 16777216 + h * 403) % 4294967296 end return h end',
       'local f = SS:FindFirstChild("UIPolishTests") or Instance.new("Folder") f.Name = "UIPolishTests" f.Parent = SS',
       'local res = {}',
       'local function put(name, src, h) if fnv(src) ~= h then table.insert(res, name .. ": HASH MISMATCH") return end local m = f:FindFirstChild(name) or Instance.new("ModuleScript") m.Name = name m.Source = src m.Parent = f table.insert(res, name .. ": ok " .. #src .. " b") end']
for name, path in files:
    src = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    out.append(f'put("{name}", {lua_str(src)}, {fnv(src.encode("utf-8"))})')
out.append('return table.concat(res, "\n")')
open(os.path.join(HERE, "install_tests.lua"), "w", encoding="ascii", newline="\n").write("\n".join(out) + "\n")
print(os.path.getsize(os.path.join(HERE, "install_tests.lua")))
