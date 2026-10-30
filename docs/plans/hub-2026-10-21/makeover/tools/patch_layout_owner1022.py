"""One-shot patch of ../../tools/hub_layout.py (2026-10-22): the OWNER moved the treadmills + upgrade signs of plots 1 and 6
in Studio. Their exact positions become per-plot overrides (the owner's placement is the truth, not the formula).
Original kept in tools/bak/hub_layout.py.pre_owner1022."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "..", "tools", "hub_layout.py")
BAK = os.path.join(HERE, "bak", "hub_layout.py.pre_owner1022")
if not os.path.exists(BAK):
    shutil.copyfile(P, BAK)
s = open(P, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    if new in s:
        return                                # already applied
    n = s.count(old)
    assert n == count, (old[:70], n)
    s = s.replace(old, new)


rep('''EXIT_BEHIND = 7.5                       # TreadmillClient: jump off = 7.5 behind the belt (towards the plot)''',
    '''EXIT_BEHIND = 7.5                       # TreadmillClient: jump off = 7.5 behind the belt (towards the plot)
# (2026-10-22, OWNER edit in Studio) plots 1 / 6: treadmill + upgrade sign moved to the plaza side of the gate, beside the
# plot (same facings as the formula). Exact owner values, deliberately NOT mirrored (103.65 vs 105.65, 109.91 vs 113.91).
OWNER_TREAD = {1: (-103.6503, -14.5395), 6: (105.6504, -14.5395)}
OWNER_SIGN = {1: (-109.9084, -4.8940), 6: (113.9084, -4.8940)}''')
rep('''    tread = add(add(G, F, TREAD_F), R, s * TREAD_S)
    sign = add(add(G, F, SIGN_F), R, s * SIGN_S[pid])''',
    '''    tread = OWNER_TREAD.get(pid) or add(add(G, F, TREAD_F), R, s * TREAD_S)
    sign = OWNER_SIGN.get(pid) or add(add(G, F, SIGN_F), R, s * SIGN_S[pid])''')
open(P, "w", encoding="utf-8").write(s)
print("patched", P)

# rule 5: the owner's own treadmill + sign pair (plots 1 / 6) stands 0.3 from the BIGGEST-tier envelope (Tier 11 is 14.7
# wide; today's Tier 1 is 9.1): accepted as placed, the pair must just not overlap
s = open(P, encoding="utf-8").read()
old = '''            need = 1.5 if owner_of(a) and owner_of(a) == owner_of(b) else 3.0'''
new = '''            need = 1.5 if owner_of(a) and owner_of(a) == owner_of(b) else 3.0
            if owner_of(a) and owner_of(a) == owner_of(b) and owner_of(a) in OWNER_TREAD:
                need = 0.0                    # (2026-10-22) owner-placed pair (plots 1 / 6): no overlap is enough'''
if old in s and "owner-placed pair (plots 1 / 6)" not in s:
    s = s.replace(old, new)
    open(P, "w", encoding="utf-8").write(s)
    print("rule 5 patched")
