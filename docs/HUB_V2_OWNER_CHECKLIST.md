# Redesigned hub (HUB V2) - owner checklist

The hub was swapped in Studio on 2026-10-21 at 14:58 UTC. All play tests passed. Details are in
`docs/plans/hub-2026-10-21/progress.md` and the pictures are in `docs/plans/hub-2026-10-21/build/` (`final_*.png`).
Nothing has been published yet.

## Before you publish

1. **Creator Hub** > SLINGSHOT > start place > Places / Settings > **Server size (Max players) = 6**.
   - Studio can't set this.
   - The live servers are still size 3, so players 4-6 would have no plot.
2. Optional: walk the hub in Studio Play. `TestFreshSave` is currently **false**, so Play uses your real save.
   - Set it to true first if you want a throwaway save.
3. **Save, then Publish, then Migrate to Latest Update.**
   - `Map.HubV2` (the staging copy) no longer exists, so publishing is safe now.
   - Do not publish a place file that still has `Map.HubV2`: it would ship a second hub.
   - Returning players' eggs are moved onto the new plots automatically when they join.

## Live check (after the publish)

- Join and check that you spawn at your plot's gate.
- Walk to your treadmill (it sits next to your gate), then to the Upgrade stall (left) and the Sell stall (right).
- With friends: up to 6 plots fill in this order: 1, 6, 2, 5, 3, 4.
- Developer Console (F9) > Memory: compare with an old server. The Studio numbers weren't comparable.

## Rollback (if something is wrong live)

- Ask Claude for "hub rollback", then Save + Publish.
- It is one tested step: `require(game.ServerStorage.HubV2Kit.Rollback:Clone())()` in Edit.
  - It puts the old hub, the old Halloween decor and the old bounds back from `ServerStorage._Backup_Hub.Before`.
  - It parks the new hub in `_Backup_Hub.After`.
  - `HubV2Kit.Swap` brings the new hub back again.
- The scripts stay new: BaseBuilder, BaseManager and Trailer also work on the old hub.
- **Never** restore the old BaseHatchery. Eggs saved on the new 90-long plots would end up outside the old fences.

## After October

- Delete `workspace.HalloweenDecor`. That removes the giant pumpkin, the pumpkin heads on the lamps, the spiders,
  the pumpkin eggs and the Halloween garden.
- The permanent lamps, trees, bushes and the backdrop island live in `Map.Hub.Decor` and stay.
- The old garlands, wall webs, vines, wall bats and grime were not re-placed. They are kept in
  `ServerStorage._Backup_Hub.Before.HalloweenDecor`.

## Cleanup (once the live hub is confirmed)

- `ServerStorage._Backup_HubV2`: 2 staging snapshots (Stage5_Plaza, Stage6_Decor). Delete them; they load on every
  server.
- `ServerStorage._Backup_Hub.Before`: the old hub, its Halloween decor, its 7 bounds columns and the 4 old scripts.
  Keep it until you're sure you won't roll back, then delete it.
- `ServerStorage.HubV2Kit` (Layout, Validate, Swap, Rollback, SwapLib, Render, Templates, BuilderTest) and
  `ServerStorage.HubV2Tests` are Studio tools with no tags and no running scripts. Keep them for future hub edits.
- The Studio test runs left throwaway `studiotest_*` save keys. Only Studio test sessions use them; they are harmless.
  Delete them only if you want a tidy DataStore, and never delete keys without that prefix.

## Editing the hub by hand

- Decor can be moved freely.
- Keep the walking lines clear: from the slingshot gate to each plot gate, and around the stall rings and the chest.
- Don't move plots, treadmills, upgrade signs, stalls, boards, the Free Gift, the Spawn or the edge walls without
  the layout tool: `docs/plans/hub-2026-10-21/tools/hub_layout.py` -> `make_layout_lua.py` -> `HubV2Kit.Layout`.
- `HubV2Kit.Validate(workspace.Map.Hub, Vector3.zero, "live")` lists anything that breaks a rule (0 = good).
