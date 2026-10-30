"""Turn a local Lua/Luau source file into a tab-free, copy-safe execute_luau snippet that writes it into a Studio
ModuleScript and returns length + checksum (h = (h * 31 + byte) % 2147483647) for verification.
Usage: python make_push_lua.py <source file> <studio path, e.g. game.ServerStorage.HubV2Kit.Layout> <out file>"""
import sys

BS = chr(92)
src_path, target, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src_path, "rb").read().decode("utf-8").replace("\r\n", "\n")
h = 0
for b in s.encode("utf-8"):
    h = (h * 31 + b) % 2147483647
lines = s.split("\n")
out = ["local L = {"]
for ln in lines:
    esc = ln.replace(BS, BS + BS).replace('"', BS + '"').replace("\t", BS + "t")
    out.append('"' + esc + '",')
out.append("}")
out.append('local src = table.concat(L, "' + BS + 'n")')
out.append("local m = " + target)
out.append("m.Source = src")
out.append("local h = 0 for i = 1, #src do h = (h * 31 + string.byte(src, i)) % 2147483647 end")
out.append('return #src .. " " .. h .. " (local ' + str(len(s.encode("utf-8"))) + " " + str(h) + ')"')
open(out_path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print(out_path, len(s.encode("utf-8")), h)
