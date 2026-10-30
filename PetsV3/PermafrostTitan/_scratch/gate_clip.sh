#!/bin/bash
# usage: gate_clip.sh <Name> <closeup x,y,z> <dist> <cmp list>   (pets WITH clips: portrait / game raw = idle f0)
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3/"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
N=$1
"$BL" -b --factory-startup --python _tools/headless_closeup.py -- $N $2 $3 700 2>&1 | grep -E "Error|Traceback"
python sheet3.py $N close_ 3 > /dev/null
"$BL" -b --factory-startup --python _tools/headless_pack.py -- $N 2>&1 | grep -E "Error|Traceback"
python _tools/pack_post.py $N $4 > $N/_scratch/pack_post.json
"$BL" -b --factory-startup --python PermafrostTitan/_scratch/gamelook.py -- $N 2>&1 | grep -E "Error|Traceback"
"$BL" -b --factory-startup --python _tools/game_raw.py -- $N 2>&1 | grep -E "Error|Traceback"
python _tools/game_icon.py $N $4 > $N/_scratch/game_icon.json
python PermafrostTitan/_scratch/shares.py $N > $N/_scratch/shares_strict.json
"$BL" -b --factory-startup --python _tools/headless_model.py -- $N tq,front,side,back 600 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback" | sed 's/"files": \[[^]]*\], //' > $N/_scratch/model_result.txt
python sheet3.py $N model_ 2 > /dev/null
python -c "import json; d=json.load(open('$N/_scratch/game_icon.json')); print('$N', {k: v for k, v in d.items() if 'gold' in k})"
cat $N/_scratch/shares_strict.json; echo; cat $N/_scratch/model_result.txt
