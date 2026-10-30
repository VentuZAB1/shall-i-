-- Night candidates for DayNightClient's NIGHT table (2026-10-13), built on top of the ORIGINAL lighting
-- (ServerStorage._Backup_Lighting1013.Before). Screenshots: night_options.jpg. The owner picks one; it replaces NIGHT.
local C = Color3.fromRGB
return {
	A_Moonlit = {
		[""] = {ClockTime = 0, Brightness = 2.4, Ambient = C(110, 115, 150), OutdoorAmbient = C(140, 145, 185), ExposureCompensation = 0.3, ColorShift_Top = C(200, 210, 255)},
		Atmosphere = {Density = 0.3, Haze = 1.2, Glare = 0, Color = C(110, 125, 190), Decay = C(60, 75, 145)},
		ColorCorrection = {Brightness = 0.03, Contrast = 0.15, Saturation = 0.25, TintColor = C(240, 244, 255)},
		Bloom = {Intensity = 0.6, Threshold = 1.1},
		SunRays = {Intensity = 0},
		Sky = {StarCount = 3000},
	},
	B_Dusk = {
		[""] = {ClockTime = 17.9, Brightness = 2, Ambient = C(120, 105, 130), OutdoorAmbient = C(160, 140, 165), ExposureCompensation = 0.2, ColorShift_Top = C(255, 200, 160)},
		Atmosphere = {Density = 0.32, Haze = 1.8, Glare = 0.4, Color = C(230, 175, 195), Decay = C(130, 95, 170)},
		ColorCorrection = {Brightness = 0.02, Contrast = 0.15, Saturation = 0.1, TintColor = C(255, 248, 248)},
		Bloom = {Intensity = 0.5, Threshold = 1.2},
		SunRays = {Intensity = 0.08},
		Sky = {StarCount = 800},
	},
	C_HalloweenNight = {
		[""] = {ClockTime = 0, Brightness = 2.2, Ambient = C(105, 98, 135), OutdoorAmbient = C(135, 125, 175), ExposureCompensation = 0.25, ColorShift_Top = C(195, 185, 255)},
		Atmosphere = {Density = 0.34, Haze = 1.6, Glare = 0, Color = C(125, 100, 175), Decay = C(75, 50, 125)},
		ColorCorrection = {Brightness = 0.03, Contrast = 0.15, Saturation = 0.25, TintColor = C(245, 240, 255)},
		Bloom = {Intensity = 0.7, Threshold = 1.0},
		SunRays = {Intensity = 0},
		Sky = {StarCount = 3000},
	},
}
