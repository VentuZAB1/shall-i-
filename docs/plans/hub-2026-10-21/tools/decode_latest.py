"""python decode_latest.py N [OUT_DIR]: decode the N newest saved execute_luau outputs (HubV2Kit.Render chunks)."""
import glob, os, subprocess, sys
D = r"C:/Users/ventu/.claude/projects/C--Users-ventu-OneDrive-Desktop-SLINGSHOT-Creatures-PetsV3/16a9c627-061b-4963-bb36-7b966755070e/tool-results"
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build")
files = sorted(glob.glob(os.path.join(D, "mcp-Roblox_Studio-execute_luau-*.txt")), key=os.path.getmtime)[-n:]
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "decode_render.py"), out] + files, check=True)
