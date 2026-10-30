#!/usr/bin/env bash
# usage: bash FrostfangLynx/_scratch/gate_full.sh <Name> <Cmp1,...> <x,y,z face target> <dist> <x,y,z body centre> <game dist> [<x,y,z low target> <low dist>]
# Full model-gate render set in the right order: pack (portrait, flat shares, icon strips) -> face close-ups ->
# game view -> model views LAST (headless_closeup re-renders model_tq at 200 px).  cwd = PetsV3
cd "C:/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
N="$1"; C="$2"; T="$3"; D="$4"
"$BL" -b --factory-startup --python _tools/headless_pack.py -- "$N" 2>&1 | grep -E "Error|Traceback" -A3
python _tools/pack_post.py "$N" "$C" > "$N/renders/_shares.json"
python -c "import json; d=json.load(open('$N/renders/_shares.json'))['shares_pct']; [print(v, d[v]) for v in d]"
"$BL" -b --factory-startup --python _tools/headless_closeup.py -- "$N" "$T" "$D" 600 2>&1 | grep -E "Error|Traceback" -A3
python sheet3.py "$N" close_ 3 > /dev/null
# game camera (high behind, like the in-game follow cam) -> renders/game_view.png (not part of the model_ sheet)
"$BL" -b --factory-startup --python _tools/headless_closeup.py -- "$N" "$5" "$6" 600 "view=0.45,1.0,0.85" game_ 2>&1 | grep -E "Error|Traceback" -A3
if [ -n "$7" ]; then   # optional low camera (under-view: belly, socks, tail underside) -> renders/low_below.png
  "$BL" -b --factory-startup --python _tools/headless_closeup.py -- "$N" "$7" "$8" 600 "below=0.55,-0.80,-0.14" low_ 2>&1 | grep -E "Error|Traceback" -A3
fi
"$BL" -b --factory-startup --python _tools/headless_model.py -- "$N" tq,front,side,back 600 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback" -A3 | sed -E 's/"files": \[[^]]*\], //'
python sheet3.py "$N" model_ 2 > /dev/null
