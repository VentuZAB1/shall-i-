#!/bin/bash
# usage: mkgifs.sh <PetName>   -> encodes renders/gif/<clip>/*.png into renders/<Pet>_<clip>.gif via the skill encoder
ENC="/c/Users/ventu/.claude/skills/animate-roblox-characters/scripts/build_animation_preview.py"
D="/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV2/$1/renders"
for c in "$D"/gif/*/; do
  c=${c%/}; n=$(basename "$c"); cnt=$(ls "$c"/*.png | wc -l)
  fps=30; [ "$n" = "idle" ] && fps=15; [ "$n" = "roar" ] && fps=15
  python "$ENC" --frames-dir "$c" --glob "*.png" --output "$D/$1_$n.gif" --fps $fps 2>&1 | tail -1
done
