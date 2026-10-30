# usage: bash <pet>/_r.sh <Name> [views] [res]  -> renders model views + sheet, prints the compact result
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
cd "C:/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
"$BL" -b --factory-startup --python _tools/headless_model.py -- "$1" "${2:-tq,front,side,back}" "${3:-600}" 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback|line [0-9]+, in" | python -c "
import sys, json
t = sys.stdin.read()
if 'HEADLESS_RESULT' in t:
    d = json.loads(t.split('HEADLESS_RESULT ', 1)[1].splitlines()[0]); d.pop('files', None); print(d)
else:
    print(t[-1500:])"
python sheet3.py "$1" model_ 2 > /dev/null
