"""Generate SLINGSHOT creatures with the Meshy API (preview -> refine) from MESHY_PROMPTS.md.

API key: put it alone in meshy/meshy_key.txt (or set MESHY_API_KEY).
Output: ~/Downloads/Meshy/<Name>.glb, <Name>.fbx, <Name>.png (alpha thumbnail), same as the manual ones.

  python meshy_run.py list                  # creatures in order, with done/pending
  python meshy_run.py run "Thunderbird" 3   # start at Thunderbird, 3 creatures in parallel, to the end
  python meshy_run.py one "Phoenix"         # a single creature
  python meshy_run.py balance
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.expanduser("~"), "Downloads", "Meshy")
LOG = os.path.join(HERE, "meshy_tasks.json")
API = "https://api.meshy.ai/openapi"
BIG = {"Kraken", "Storm Wyvern", "Inferno Drake", "Void Dragon", "Abyss Behemoth",
       "Celestial Dragon", "Lava Golem", "Thunderbird", "Phoenix", "Griffin"}


def key():
    k = os.environ.get("MESHY_API_KEY")
    p = os.path.join(HERE, "meshy_key.txt")
    if not k and os.path.exists(p):
        k = open(p, encoding="utf-8").read().strip()
    if not k:
        sys.exit("No API key: put it in meshy/meshy_key.txt")
    return k


def call(method, path, body=None, tries=4):
    for i in range(tries):
        req = urllib.request.Request(
            API + path, method=method,
            headers={"Authorization": "Bearer " + key(), "Content-Type": "application/json"},
            data=json.dumps(body).encode() if body is not None else None)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                time.sleep(20 * (i + 1))
                continue
            raise RuntimeError(f"HTTP {e.code} {method} {path}: {msg}")
        except urllib.error.URLError:
            if i < tries - 1:
                time.sleep(20)
                continue
            raise


def creatures():
    s = open(os.path.join(HERE, "MESHY_PROMPTS.md"), encoding="utf-8").read()
    out = []
    for m in re.finditer(r"### (.+?)\n```\n(.*?)\n```\n\*\*Texture \(Refine box\):\*\*\n```\n(.*?)\n```", s, re.S):
        out.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))
    return out


def load_log():
    return json.load(open(LOG)) if os.path.exists(LOG) else {}


def save_log(name, **kv):
    d = load_log()
    d.setdefault(name, {}).update(kv)
    json.dump(d, open(LOG, "w"), indent=2)


def wait(tid, name, stage):
    last = -1
    while True:
        t = call("GET", f"/v2/text-to-3d/{tid}")
        if t.get("progress") != last:
            last = t.get("progress")
            print(f"[{name}] {stage} {t['status']} {last}%", flush=True)
        if t["status"] in ("SUCCEEDED", "FAILED", "CANCELED"):
            return t
        time.sleep(15)


def fetch(url, dest):
    with urllib.request.urlopen(url, timeout=600) as r, open(dest, "wb") as f:
        f.write(r.read())


def make(name, prompt, texture):
    os.makedirs(OUT, exist_ok=True)
    if os.path.exists(os.path.join(OUT, name + ".glb")):
        print(f"[{name}] already in Downloads/Meshy, skipping")
        return name, "skipped"
    try:
        entry = load_log().get(name, {})
        pid = entry.get("preview")
        if not pid:
            pid = call("POST", "/v2/text-to-3d", {
                "mode": "preview", "prompt": prompt[:800], "ai_model": "latest",
                "model_type": "standard", "geometry_resolution": "standard",
                "should_remesh": True, "topology": "triangle",
                "target_polycount": 15000 if name in BIG else 10000,
                "pose_mode": "", "moderation": False, "auto_size": False,
                "target_formats": ["glb", "fbx"], "alpha_thumbnail": True,
            })["result"]
            save_log(name, preview=pid)
        t = wait(pid, name, "preview")
        if t["status"] != "SUCCEEDED":
            save_log(name, preview=None, error=t.get("task_error"))
            return name, f"preview {t['status']}"
        rid = entry.get("refine")
        if not rid:
            rid = call("POST", "/v2/text-to-3d", {
                "mode": "refine", "preview_task_id": pid, "ai_model": "latest",
                "texture_prompt": texture[:800], "enable_pbr": True,
                "texture_resolution": "2k", "moderation": False, "auto_size": False,
                "target_formats": ["glb", "fbx"], "alpha_thumbnail": True,
            })["result"]
            save_log(name, refine=rid)
        t = wait(rid, name, "refine")
        if t["status"] != "SUCCEEDED":
            save_log(name, refine=None, error=t.get("task_error"))
            return name, f"refine {t['status']}"
        urls = t.get("model_urls") or {}
        for fmt in ("fbx", "glb"):  # glb last: its presence marks the creature done
            if urls.get(fmt):
                fetch(urls[fmt], os.path.join(OUT, f"{name}.{fmt}.part"))
        for fmt in ("fbx", "glb"):
            part = os.path.join(OUT, f"{name}.{fmt}.part")
            if os.path.exists(part):
                os.replace(part, os.path.join(OUT, f"{name}.{fmt}"))
        thumb = t.get("alpha_thumbnail_url") or t.get("thumbnail_url")
        if thumb:
            fetch(thumb, os.path.join(OUT, f"{name}.png"))
        save_log(name, done=True)
        print(f"[{name}] DONE -> Downloads/Meshy/{name}.glb/.fbx/.png", flush=True)
        return name, "done"
    except Exception as e:
        print(f"[{name}] ERROR {e}", flush=True)
        return name, f"error: {e}"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd, cs = sys.argv[1], creatures()
    if cmd == "list":
        for n, _, _ in cs:
            print(("done   " if os.path.exists(os.path.join(OUT, n + ".glb")) else "pending"), n)
    elif cmd == "balance":
        print(call("GET", "/v1/balance"))
    elif cmd == "one":
        c = next(c for c in cs if c[0] == sys.argv[2])
        print(make(*c))
    elif cmd == "run":
        names = [c[0] for c in cs]
        start = names.index(sys.argv[2]) if len(sys.argv) > 2 else 0
        par = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        with ThreadPoolExecutor(par) as ex:
            results = list(ex.map(lambda c: make(*c), cs[start:]))
        print("\nSUMMARY")
        for n, r in results:
            print(f"  {n}: {r}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
