-- HUB GRIME ROLLOUT: FINAL layout tables (lead, 2026-10-14). Feed to rollout_engine.lua:
--   local engine = loadstring(game.ServerStorage._GrimeRolloutEngine.Source)()
--   engine("check" | "build", MOSS, WALLD, FLOOR)
-- "build" rebuilds Workspace.HalloweenDecor.Grime.Rollout (Walls + Floor). The owner-approved test patch stays as
-- Grime.Bay_B7 and is counted in the overlap checks. s = studs along a wall from its LEFT end as seen from the hub
-- (back wall: x = 119.55 - s). Bays and walls: see NOTES.md section 3 + lead notes in BUILD_NOTES.
--
-- POST-BUILD TWEAKS (re-apply after any rebuild):
--  1. Sun-facing moss tint (the sun comes from (-0.61, 0.75, 0.25), so DiagFrontR faces it and its moss went lime/hedge):
--     Texture.Color3 = (0.62, 0.72, 0.62) on FR1_Moss + FR2_Moss;
--     Decal.Color3   = (0.70, 0.78, 0.68) on sunlit floor moss: GL_Moss GR_Moss Mid_MossL C10_Moss C09_Moss TR_Moss FR1_FootMoss.
--     Every moss carrier has attribute SunLit (0..1) from a sun raycast.
--  2. Plaza_StainNE is G_Stain_A 8x8 at r 21.2, Transparency 0.3 (the G_Stain_B mud skid read as a pale hand print on cream).
--  (Moves for spiders are already in the tables below.)

local MOSS = { -- {id, wall, A/B, s0, s1, OffsetStudsU}  (W_Crack_C bays use offset 0)
	{"B9_Moss", "BackWall", "A", 3.75, 25.32, 6},
	{"B8_Moss", "BackWall", "B", 27.82, 51.88, 12},
	{"B6_Moss", "BackWall", "B", 80.95, 105.01, 18},
	{"B4_Moss", "BackWall", "B", 134.08, 158.14, 0},
	{"B3_Moss", "BackWall", "A", 160.64, 184.71, 12},
	{"B2_Moss", "BackWall", "A", 187.21, 211.27, 0},
	{"SL_Moss", "SideL", "B", 1.3, 25.25, 6},
	{"DL1_Moss", "DiagBackL", "B", 3.75, 25.95, 0},
	{"DL2_Moss", "DiagBackL", "A", 28.45, 53.15, 12},
	{"DR1_Moss", "DiagBackR", "B", 3.75, 25.95, 6},
	{"DR3_Moss", "DiagBackR", "A", 55.65, 77.85, 0},
	{"FL1_Moss", "DiagFrontL", "A", 3.75, 25.41, 12},
	{"FL3_Moss", "DiagFrontL", "B", 54.56, 78.56, 0},
	{"FR2_Moss", "DiagFrontR", "A", 81.22, 105.37, 6},
	{"FR1_Moss", "DiagFrontR", "B", 107.87, 129.55, 18},
	-- 2026-10-14 owner: moss at the bottom of EVERY wall -> the former bare bays:
	{"B1_Moss", "BackWall", "B", 213.77, 235.35, 12},
	{"B5_Moss", "BackWall", "A", 107.51, 131.58, 6},
	{"SR_Moss", "SideR", "A", 1.3, 25.25, 12}, -- sun-facing: tint 0.62/0.72/0.62
	{"DL3_Moss", "DiagBackL", "B", 55.65, 77.85, 18},
	{"DR2_Moss", "DiagBackR", "A", 28.45, 53.15, 18},
	{"FL2_Moss", "DiagFrontL", "B", 27.91, 52.06, 6},
	{"FR3_Moss", "DiagFrontR", "B", 6.67, 78.67, 0}, -- + FR3_EndL cap (W_MossBase_EndL) at s 0.67..6.67; sun tint
}
-- no bare bays any more (owner 2026-10-14)

local WALLD = { -- {id, wall, texture, s centre, bottom y above floor | "drip" (top = trim bottom + 0.35)}
	{"FL3_EndR", "DiagFrontL", "W_MossBase_EndR", 81.56, -0.375},
	{"B8_CrackA", "BackWall", "W_Crack_A", 41, 5.5}, -- moved off Spider4
	{"B6_CrackA", "BackWall", "W_Crack_A", 87, 5.5}, -- moved off Spider3
	{"B5_CrackB", "BackWall", "W_Crack_B", 125.58, 5.25}, -- raised when B5 got moss
	{"B5_Drip", "BackWall", "W_Drip_A", 111.62, "drip"},
	{"B4_CrackC", "BackWall", "W_Crack_C", 148.08, -0.375}, -- B low-moss slot (u 14)
	{"B2_CrackC", "BackWall", "W_Crack_C", 195.71, -0.375}, -- A low-moss slot (u 8.5)
	{"B1_Drip", "BackWall", "W_Drip_A", 217.45, "drip"}, -- B2 had Spider1 in the drip spot
	{"SR_Drip", "SideR", "W_Drip_A", 22.5, "drip"},
	{"DL1_CrackC", "DiagBackL", "W_Crack_C", 17.75, -0.375},
	{"DL2_DripSlime", "DiagBackL", "W_Drip_B", 32.56, "drip"},
	{"DR3_CrackC", "DiagBackR", "W_Crack_C", 64.15, -0.375},
	{"FL1_CrackB", "DiagFrontL", "W_Crack_B", 17.4, 5.25},
	{"FL3_CrackB", "DiagFrontL", "W_Crack_B", 102, 5.85}, -- above the market deck (0.6), between the stalls
	{"FL3_Drip", "DiagFrontL", "W_Drip_A", 82, "drip"}, -- next to a garland hook
	{"FR3_CrackA", "DiagFrontR", "W_Crack_A", 40.5, 5.5}, -- gap between SpeedBoard and HeaviestBoard
	{"FR3_DripSlime", "DiagFrontR", "W_Drip_B", 57, "drip"},
	{"FR1_CrackA", "DiagFrontR", "W_Crack_A", 114.87, 5.5},
}

local FLOOR = { -- wall-relative {wall, s, d} | absolute {x, z, yaw} | plaza {theta, r} | path {along, lat}
	{id = "B9_Moss", tex = "G_Moss_A", wall = "BackWall", s = 15, d = 2.75},
	{id = "B9_Stain", tex = "G_Stain_A", x = 98, z = 98.5, yaw = 15},
	{id = "B8_Moss", tex = "G_Moss_B", wall = "BackWall", s = 33.82, d = 2.26},
	{id = "B8_Crack", tex = "G_Crack_C", x = 90, z = 92, yaw = -20},
	{id = "B3_Moss", tex = "G_Moss_B", wall = "BackWall", s = 180.5, d = 2.26},
	{id = "B3_Stain", tex = "G_Stain_B", x = -62, z = 93, yaw = -20},
	{id = "B3_Slime", tex = "G_Slime_A", x = -50, z = 87, yaw = 15},
	{id = "B2_Moss", tex = "G_Moss_A", wall = "BackWall", s = 195.71, d = 2.75},
	{id = "B1_Stain", tex = "G_Stain_A", wall = "BackWall", s = 217.45, d = 5},
	{id = "GL_Moss", tex = "G_Moss_A", x = -53, z = 69, yaw = 10},
	{id = "GR_Crack", tex = "G_Crack_A", x = 38, z = 74, yaw = 60},
	{id = "GR_Moss", tex = "G_Moss_B", x = 41, z = 60, yaw = 90},
	{id = "GR2_Stain", tex = "G_Stain_A", x = 40, z = 28, yaw = 0},
	{id = "Plaza_CrackE", tex = "G_Crack_A", plaza = 0, r = 21.5, scale = 0.85, transp = 0.12},
	{id = "Plaza_CrackNW", tex = "G_Crack_C", plaza = 125, r = 21.5, scale = 0.85, transp = 0.12},
	{id = "Plaza_CrackSW", tex = "G_Crack_A", plaza = 215, r = 21.5, scale = 0.85, transp = 0.12},
	{id = "Plaza_StainNE", tex = "G_Stain_A", plaza = 45, r = 21.2, scale = 0.8, transp = 0.3},
	{id = "Plaza_SlimeW", tex = "G_Slime_A", plaza = 180, r = 21.5, scale = 0.85},
	{id = "Mid_Stain", tex = "G_Stain_B", x = 16, z = 1, yaw = 25},
	{id = "Mid_Crack", tex = "G_Crack_B", x = 20, z = -4, yaw = 10},
	{id = "Mid_MossL", tex = "G_Moss_A", x = -34, z = 3, yaw = 20, scale = 0.85},
	{id = "FR_Crack", tex = "G_Crack_B", x = 42, z = -48, yaw = 20},
	{id = "FR_Stain", tex = "G_Stain_A", x = 47, z = -38, yaw = 0},
	{id = "C10_Slime", tex = "G_Slime_A", x = 66, z = -22, yaw = 20},
	{id = "C10_Moss", tex = "G_Moss_A", x = 81, z = -28, yaw = -15},
	{id = "C10_Crack", tex = "G_Crack_C", x = 64, z = -42, yaw = -20},
	{id = "C09_Moss", tex = "G_Moss_B", x = -57, z = -29, yaw = 80},
	{id = "C09_Crack", tex = "G_Crack_A", x = -54, z = -42, yaw = -40},
	{id = "FLF_Crack", tex = "G_Crack_B", x = -36, z = -50, yaw = 15},
	{id = "FL3_FootMoss", tex = "G_Moss_B", wall = "DiagFrontL", s = 68, d = 2.26},
	{id = "FL3_FootStain", tex = "G_Stain_B", wall = "DiagFrontL", s = 60, d = 7},
	{id = "TR_Moss", tex = "G_Moss_A", x = 128, z = 6, yaw = 25},
	{id = "TR_Stain", tex = "G_Stain_A", x = 145, z = 18, yaw = 0},
	{id = "FL1_FootMoss", tex = "G_Moss_B", wall = "DiagFrontL", s = 14, d = 2.26},
	{id = "TL_Stain", tex = "G_Stain_B", x = -130, z = -8, yaw = 45},
	{id = "TL_Crack", tex = "G_Crack_C", x = -142, z = 2, yaw = -30},
	{id = "SL_FootMoss", tex = "G_Moss_A", wall = "SideL", s = 12, d = 2.75},
	{id = "FR1_FootMoss", tex = "G_Moss_B", wall = "DiagFrontR", s = 114.87, d = 2.26},
	{id = "P1_Stain", tex = "G_Stain_B", path = "Path_Base1", along = 20, lat = 0.9, scale = 0.85, transp = 0.3},
	{id = "P3_Crack", tex = "G_Crack_C", path = "Path_Base3", along = 4, lat = -0.9, scale = 0.85, transp = 0.12},
}
-- Rejected by the checks (kept out): floor decals at the diagonal back walls (inside Base1/Base3 slot + 4 margin),
-- in front of back bays B4-B6 (Base2 margin), GL_Crack / GL2_Moss (Base1/Base2 margin), TR_Crack (crack over moss).
