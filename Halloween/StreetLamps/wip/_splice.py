import json
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\StreetLamps\lamp.py"
s = open(p, encoding="utf-8").read()
steps = open(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\StreetLamps\wip\_steps.py", encoding="utf-8").read()
a = s.index('if __name__ == "__main__":')
s = s[:a] + steps + s[a:]
s = s.replace('''    step = argv[0] if argv else "preview"
    if step == "preview":
        r = step_preview()
    log("done", step)''', '''    step = argv[0] if argv else "preview"
    if step == "preview":
        step_preview()
    elif step == "build":
        step_build()
    elif step == "bake":
        step_bake({"post": "Post", "cage": "Cage", "pumpkin": "Pumpkin"}[argv[1]])
    elif step == "web":
        step_web()
    elif step == "export":
        step_export()
    elif step == "verify":
        step_verify()
    elif step == "calib":
        step_calib()
    elif step == "review":
        step_review(argv[1] if len(argv) > 1 else "all")
    log("done", step)''')
open(p, "w", encoding="utf-8").write(s)
print("spliced")
