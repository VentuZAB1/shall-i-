#!/bin/bash
# usage: rend.sh <Name> <closeup x,y,z> <dist>   (closeup first, model views last; then both sheets)
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3/"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
if [ -n "$2" ]; then
  "$BL" -b --factory-startup --python _tools/headless_closeup.py -- $1 $2 $3 600 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback|line [0-9]" | head -8
  python sheet3.py $1 close_ 3 > /dev/null
fi
"$BL" -b --factory-startup --python _tools/headless_model.py -- $1 tq,front,side,back 600 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback|line [0-9]" | sed 's/"files": \[[^]]*\], //' | head -8
python sheet3.py $1 model_ 2 > /dev/null
