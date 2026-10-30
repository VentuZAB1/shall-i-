import sys
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\StreetLamps")
import lamp
from lamp import *
CFG["fast"] = True
fresh(4)
cv = crook_design(); H = head_stack(cv)
pk = build_pumpkin(False)
env = pumpkin_envelope()
zc = 13.36
S2, Q = strap_profile(env, 12.40 - zc, 0.265, H["ring_z"] - zc - 0.01, 0.51)
print("strap pts", len(S2))
P = np.array([[r, 0, z] for r, z in S2])
Rl = polyline_curv_radius(P, k=6)
idx = adaptive_samples(P, Rl, sag=0.003, max_len=0.28)
print("rings", len(idx), "Rmin", Rl.min(), "R at idx", np.round(Rl[idx], 2))
