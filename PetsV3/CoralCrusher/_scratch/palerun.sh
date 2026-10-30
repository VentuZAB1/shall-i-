#!/bin/bash
# flat renders + shares only (pale check)
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
"$BL" -b --factory-startup --python _tools/headless_pack.py -- CoralCrusher views=side,tq,game,back 2>&1 | grep -E "Error|Traceback"
python PermafrostTitan/_scratch/shares_all.py CoralCrusher side,tq,game,back > CoralCrusher/_scratch/shares_all_f85.json
python -c "
import json
d=json.load(open('CoralCrusher/_scratch/shares_all_f85.json'))
for v,x in d.items(): print(' ',v, {k:x[k] for k in x if k in ('BRONZE','BRONZE_D','SHELL_D','BELLY_PALE','ROSE','ROSE_D')})"
