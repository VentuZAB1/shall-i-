#!/bin/bash
# save_dl.sh <CreatureName>: copy everything downloaded since ~/.dl_marker into claude_design/<CreatureName>/
D="/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/claude_design/$1"
mkdir -p "$D"
cd ~/Downloads && find . -maxdepth 1 -type f -newer ~/.dl_marker ! -name "*.tmp" -exec cp {} "$D/" \;
ls "$D"
