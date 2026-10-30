# Venom Basilisk - review 3b (2026-10-14) - SIGNED OFF

**Venom Basilisk is approved and ready to ship.** Model 8/10 for a 5% rare; all four clips are approved.

What I checked:
- The diff of `pets/VenomBasilisk.py` against `_tools/rex_versions/VenomBasilisk_r3clips.py`. It contains only:
  - the four roar Frill values (f20 -30, f24 -32, f52 -32, hold loop -32 ± 1.5), exactly as specified
  - the act_dash jaw-crack keys
  - the comment fix

  The mesh code is unchanged, so the model stays frozen at the approved state.
- `_r3_roar_game.png` and `_r3_roar_front.png`.

Findings:
- **Roar, from the game camera** (f20/24/40): the fan now faces up and back toward the follow camera as a full violet
  fan behind the head on all three frames. Before, it was an edge-on sliver. This matches my in-memory test
  (facing ~0.42, about the same as rest).
- **Roar, from the front** (f20/24/40): the fan frames the raised head as a crown. It clears the horns, the tongue is
  out at f24/f40, and I see no Frill/Head cut.
- **act_dash tongue flicks** (f7, f100): the jaw cracks 3° on f6-9 and f99-102 and closes after the tongue returns.
  The timing matches the idle (tongue out at f7/f100, back by f10/f103, jaw shut at f11/f104).
- **Checks:** `collision_free` true (0 pairs), linear 0, idle and walk loops exact, walk slide 0, ground_min_z
  ≥ -0.006 on all clips, stride 0.48 unchanged.

Not taken: the optional pale under-shell raise. That is fine; the belly reads.

**Owner to-do (as for all pets):**
- Studio import as creator ZAB Studio.
- VFX Studio effects driven by the events: `roar` (f22), `launch` (f20), `stomp` (f55), `frill_flash` (f58, Frill)
  and `venom_drip` (f60, Venom anchor).
- Save + Publish.
