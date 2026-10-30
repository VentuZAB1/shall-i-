# python mkrbxmx.py out.rbxmx Name1 Name2 ...  -> one Folder "PetsV2Clips" holding ModuleScript <Name> = <Name>/<Name>.lua
# (Studio: right-click a service > Insert from File... ; then move the modules into ReplicatedStorage.CreatureClips)
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
out, names = sys.argv[1], sys.argv[2:]


def cdata(s):
    return "<![CDATA[" + s.replace("]]>", "]]]]><![CDATA[>") + "]]>"


items = []
for i, n in enumerate(names, 1):
    src = open(os.path.join(here, n, n + ".lua"), encoding="utf-8").read()
    items.append('<Item class="ModuleScript" referent="RBX%d"><Properties><string name="Name">%s</string>'
                 '<ProtectedString name="Source">%s</ProtectedString></Properties></Item>' % (i, n, cdata(src)))
xml = ('<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
       'xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">'
       '<Item class="Folder" referent="RBX0"><Properties><string name="Name">PetsV2Clips</string></Properties>'
       + "".join(items) + '</Item></roblox>')
open(out, "w", encoding="utf-8").write(xml)
print(out, len(xml), "bytes,", len(names), "modules")
