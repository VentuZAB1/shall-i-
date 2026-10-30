# HubGrime - run the Blender preview renders, then apply the Roblox-like veil exactly once to the new frames.
#   python gen\render_previews.py [shots] [extra blender args...]
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_veil  # noqa: E402

shots = sys.argv[1] if len(sys.argv) > 1 else "all"
extra = sys.argv[2:]
log = os.path.join(HERE, "logs", "render_previews.txt")
t0 = time.time()
with open(log, "w") as f:
    subprocess.run([BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "gen", "mock_preview.py"), "--",
                    "--shots", shots] + extra, stdout=f, stderr=subprocess.STDOUT, timeout=3000)
made = [ln.split("RENDERED ", 1)[1].strip() for ln in open(log) if ln.startswith("RENDERED ")]
for p in made:
    post_veil.veil(p)
print(f"{len(made)} frames rendered + veiled in {time.time() - t0:.0f}s (log: {log})")
