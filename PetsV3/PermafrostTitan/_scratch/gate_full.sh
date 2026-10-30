#!/bin/bash
# usage: gate_full.sh <Name> <closeup x,y,z> <dist> <cmp list for strips>  = gate_all + game-cam icon + gold counter + strict shares
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3/"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
bash PermafrostTitan/_scratch/gate_all.sh $1 $2 $3 $4 | tail -1
"$BL" -b --factory-startup --python PermafrostTitan/_scratch/gameraw_model.py -- $1 2>&1 | grep -E "Error|Traceback"
python _tools/game_icon.py $1 $4 > $1/_scratch/game_icon.json
python PermafrostTitan/_scratch/shares.py $1 > $1/_scratch/shares_strict.json
cat $1/_scratch/game_icon.json | python -c "import json,sys; d=json.load(sys.stdin); print({k:v for k,v in d.items() if 'gold' in k.lower()})"
cat $1/_scratch/shares_strict.json
cat $1/_scratch/model_result.txt
