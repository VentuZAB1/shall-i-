#!/bin/bash
# grab.sh NAME : copy the newest Studio capture into work/caps/NAME.jpg
SRC="C:/Users/ventu/.claude/projects/C--Users-ventu-OneDrive-Desktop-SLINGSHOT-Creatures-PetsV3/16a9c627-061b-4963-bb36-7b966755070e/tool-results"
DST="C:/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/docs/plans/thumbnails-2026-10-22/work/caps"
mkdir -p "$DST"
f=$(ls -t "$SRC"/mcp-Roblox_Studio-blob-*.jpg | head -1)
cp "$f" "$DST/$1.jpg" && echo "$1 <- $(basename $f)"
