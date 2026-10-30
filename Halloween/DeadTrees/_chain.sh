#!/bin/bash
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/Halloween/DeadTrees"
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
for k in haunted dead; do
  t=$k; [ $k = haunted ] && t=h
  for st in build bake render export; do
    echo "START $k $st $(date +%T)"
    "$B" -b --factory-startup --python trees.py -- $k $st > log_${st}_$t.txt 2>&1
    echo "END $k $st rc=$? $(date +%T)"
    if grep -q "Traceback" log_${st}_$t.txt; then echo "ERROR in $k $st"; grep -A30 Traceback log_${st}_$t.txt | head -40; fi
  done
done
echo CHAIN_END
