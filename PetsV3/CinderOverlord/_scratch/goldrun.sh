#!/bin/bash
# re-run the pack + both icons and print the kit gold counter (portrait, game)
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
CMP=BlackDragon,MoltenBoar,LavaGolem,Cerberus,Ivonrath,InfernoPhoenix,ThunderRex,CosmicLeviathan
"$BL" -b --factory-startup --python _tools/headless_pack.py -- CinderOverlord views=side,tq,game,back 2>&1 | grep -E "Error|Traceback"
python _tools/pack_post.py CinderOverlord $CMP views=side,tq,game,back > CinderOverlord/_scratch/pack_post.json 2>&1
"$BL" -b --factory-startup --python _tools/game_raw.py -- CinderOverlord 2>&1 | grep -E "Error|Traceback"
python _tools/game_icon.py CinderOverlord $CMP > CinderOverlord/_scratch/game_icon_out.txt 2>&1
tail -1 CinderOverlord/_scratch/game_icon_out.txt | cut -c1-110
