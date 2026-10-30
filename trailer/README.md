# SLINGSHOT FOR EGGS: in-game trailer

It plays inside your game (owner only), so you record it at full resolution with OBS. About 34 s of picture, then you
upload one MP4.

## 1. Save + publish (Studio)

**File > Save**, then **File > Publish to Roblox**. That ships:
- the trailer
- the admin button
- the pumpkin fix
- the hub floor fix (`Map.Hub.Floor` was unanchored, so it fell out of the world and the hub showed the cloud sea; this was probably live too)

## 2. Record (in the real Roblox game, not Studio)

1. Join your game in a quiet server (a private server is best). Other players are hidden during the trailer anyway.
2. Roblox **Esc > Settings**:
   - **Graphics Quality** manual, all the way up
   - **Volume** up
   - **Fullscreen** (F11) on a 1920x1080 screen
3. OBS settings:
   - Settings > Video: Base and Output **1920x1080**, **60 FPS**.
   - Source: **Game Capture** (or Window Capture) of Roblox, with **Capture Cursor OFF**.
   - Audio: Desktop Audio only (mute your mic).
   - Recording format **mp4** or **mkv** (both are fine).
4. Turn off Discord or Windows pop-ups (Do Not Disturb).
5. In the game: **ADMIN > SERVER > PLAY TRAILER**.
   - The screen goes **black for about 2 s**: press **Start Recording** in OBS now.
   - Don't touch the mouse or keyboard while it plays (Backspace stops it).
   - It ends on the title card, fades to black, then your normal screen comes back. **Stop Recording** then.

## 3. Finish the file (one command)

```
python "C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\trailer\tools\finish_video.py" "C:\path\to\your\recording.mkv"
```

This writes `trailer\final\SLINGSHOT_trailer.mp4`:
- the black lead-in is cut
- the top-left corner is cropped by 1/12, because Roblox always shows its menu button there
- 1920x1080, 60 fps, H.264 + AAC
- exactly 1 video + 1 audio stream, no cover image (an extra stream makes Roblox's upload fail)

Add `--no-crop` to keep the full frame. Or just tell Claude where the recording is.

## 4. Upload (you do this; Claude doesn't upload)

1. Go to https://create.roblox.com/dashboard/creations and open **[🎃] Slingshot for Eggs**.
2. Left menu: **Configurations > Places**, then click the place **[🎃] Slingshot for Eggs**.
3. Left menu: **Videos**, then **Upload Video**, then pick `SLINGSHOT_trailer.mp4`.
4. Wait for moderation. Once approved it shows first on the experience page media gallery and can show on Home
   (not on Xbox, PlayStation or VR).

## Roblox rules it meets (checked 2026-10-15)

From the live Videos page:
- .mp4 / .mov, at most **100 MB** and **60 s**, about 15 Mbps
- 640x360 to 1920x1080, **16:9**
- one video slot, **3 uploads per month** (a failed or rejected upload still uses one, so upload the finished file once)

From the Creator Docs video guidelines:
- Real in-game content and camera work only: every model, wave, weather, pet and UI style in the trailer is from the game.
- No voice-over, no lyrics: the music is "Race To Finish" (APM, Roblox catalog, already in the game's playlist).
- No subjective claims ("BEST", "#1", "FREE"): the captions only say what you do in the game.

## What's in Studio

- `ServerStorage.AdminUI.Trailer` (ModuleScript) + `Trailer.Assets` (Storm egg, Celestial egg, x20 treadmill). Only admins get AdminUI, so only you can run it.
- `AdminUI.AdminClient`: SERVER tab has a new TRAILER section with the PLAY TRAILER button. The restart section moved up.
- `StarterPlayerScripts.HalloweenClient`: while the trailer plays, the giant pumpkin looks straight ahead instead of at your hidden character.
- `Map.Hub.Floor.Anchored = true`.
- Backups: `ServerStorage._Backup_Trailer.Before` (AdminClient, HalloweenClient).
- Studio review switch: player attribute `TrailerDebugT = n` freezes the trailer at second n (Studio only).

The local copy of the script is `studio\Trailer.lua`; old versions are in `studio\history`.
