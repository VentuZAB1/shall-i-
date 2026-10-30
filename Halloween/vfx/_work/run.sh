#!/bin/bash
# usage: run.sh <key...>   renders via vfx.py and prints the stats
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/Halloween"
LOG="vfx/_work/log_$(echo "$@" | tr ' ' '_').txt"
timeout 1800 "/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b --factory-startup --python vfx.py -- "$@" > "$LOG" 2>&1
grep -E "VFX_DONE|rror|Traceback|line [0-9]+" "$LOG" | grep -v "^Fra" | head -30
