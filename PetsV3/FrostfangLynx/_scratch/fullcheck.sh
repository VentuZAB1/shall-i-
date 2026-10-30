#!/usr/bin/env bash
# usage: bash FrostfangLynx/_scratch/fullcheck.sh <Name> [picks] -> step-1 audit / collisions / ground summary
cd "C:/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
"$BL" -b --factory-startup --python _tools/headless_full.py -- "$1" "${2:--}" 1 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback" -A8 | python -c "
import sys, json
for line in sys.stdin:
    if line.startswith('HEADLESS_RESULT'):
        d = json.loads(line[len('HEADLESS_RESULT '):])
        open(r'$1/_scratch/fullcheck.json', 'w').write(json.dumps(d, default=str))
        print('audit', json.dumps(d['audit']))
        print('clips', d['clips'], 'events', d['events'])
        print('ground', d['ground_min_z'])
        print('collision_free', d['collision_free'], json.dumps(d['collisions'])[:2500])
        print('tris', d['tris_body'], 'stride', d['stride'])
    elif 'Blender' not in line and line.strip():
        print(line.rstrip())
"
