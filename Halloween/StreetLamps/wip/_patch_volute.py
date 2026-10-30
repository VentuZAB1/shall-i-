p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\StreetLamps\lamp.py"
s = open(p, encoding="utf-8").read()
old_head = '''def volute_curve(cv, n=900):
    """Log-spiral scroll nested in the bend; the centre / start radius are solved so that the outer coil touches the
    crook's inner side near the pole and under the arc."""
    P, Rloc, s = crook_path3d(cv)'''
new_head = '''VOLUTE_CACHE = os.path.join(OUT, "volute_cache.json")


def volute_curve(cv, n=900):
    """Log-spiral scroll nested in the bend; the centre / start radius are solved so that the outer coil touches the
    crook's inner side near the pole (cached in volute_cache.json)."""
    A_tot, r_end, beta0 = np.radians(600.0), 0.12, np.radians(186.0)
    key = json.dumps(CROOK, sort_keys=True)
    if os.path.exists(VOLUTE_CACHE):
        with open(VOLUTE_CACHE) as fh:
            cache = json.load(fh)
        if cache.get("key") == key:
            Cy, Cz, rho0 = cache["Cy"], cache["Cz"], cache["rho0"]
            k = math.log(rho0 / r_end) / A_tot
            al = np.linspace(0, A_tot, n)
            rho = rho0 * np.exp(-k * al)
            return dict(y=Cy + rho * np.cos(beta0 - al), z=Cz + rho * np.sin(beta0 - al), C=(Cy, Cz), rho0=rho0,
                        gaps=tuple(cache["gaps"]), rho=rho, al=al)
    P, Rloc, s = crook_path3d(cv)'''
assert old_head in s
s = s.replace(old_head, new_head)
old_tail = '''    _, Cy, Cz, rho0, gmin, g0, gmid = best
    k = math.log(rho0 / r_end) / A_tot'''
new_tail = '''    _, Cy, Cz, rho0, gmin, g0, gmid = best
    with open(VOLUTE_CACHE, "w") as fh:
        json.dump(dict(key=key, Cy=float(Cy), Cz=float(Cz), rho0=float(rho0),
                       gaps=[round(gmin, 4), round(g0, 4), round(gmid, 4)]), fh)
    k = math.log(rho0 / r_end) / A_tot'''
assert old_tail in s
s = s.replace(old_tail, new_tail)
open(p, "w", encoding="utf-8").write(s)
print("patched")
