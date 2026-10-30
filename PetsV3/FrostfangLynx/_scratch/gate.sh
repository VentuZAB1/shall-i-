#!/usr/bin/env bash
# usage: bash FrostfangLynx/_scratch/gate.sh <Name> <Cmp1,Cmp2,...> [skip_pack]
# pack (portrait + flat shares + icon strips) then model views LAST (sheet).  cwd = PetsV3
cd "C:/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
N="$1"; C="$2"
if [ -z "$3" ]; then
  "$BL" -b --factory-startup --python _tools/headless_pack.py -- "$N" 2>&1 | grep -E "Error|Traceback" -A3
  python _tools/pack_post.py "$N" "$C" | python -c "import sys,json; d=json.load(sys.stdin)['shares_pct']; [print(v, d[v]) for v in d]"
fi
"$BL" -b --factory-startup --python _tools/headless_model.py -- "$N" tq,front,side,back 600 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback" -A3 | sed -E 's/"files": \[[^]]*\], //'
python sheet3.py "$N" model_ 2 > /dev/null
