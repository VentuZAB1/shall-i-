"""Turn the OBS recording of the in-game trailer into the upload-ready MP4 for Creator Hub > Videos.

    python finish_video.py "C:\\path\\to\\recording.mkv"            -> trailer\\final\\SLINGSHOT_trailer.mp4
    python finish_video.py recording.mkv --no-crop                  (keep the Roblox menu button corner)
    python finish_video.py recording.mkv --out D:\\other.mp4

What it does:
- cuts the black lead-in (the trailer's 2 s "start OBS" black) and keeps only 0.6 s of the black at the end;
- crops 1/12 off the top + left (the always-on Roblox menu button), keeping 16:9, and scales to 1920x1080;
- H.264 High, 60 fps max, peak 13.5 Mbps video (+192k audio, under the ~15 Mbps advice), AAC 192k 48 kHz stereo, +faststart;
- exactly ONE video + ONE audio stream, no metadata / chapters / cover image (an extra stream fails the upload);
- refuses to write anything longer than 59 s (Roblox's limit is 60 s).
Roblox rules checked 2026-10-15 on the live Videos page: .mp4/.mov, <= 100 MB, ~15 Mbps, <= 60 s,
640x360..1920x1080, 16:9, 3 uploads per month.
"""
import argparse
import os
import re
import subprocess
import sys

FFMPEG = r"C:\Users\ventu\AppData\Local\Programs\Python\Python312\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.join(os.path.dirname(HERE), "final", "SLINGSHOT_trailer.mp4")
MAX_LEN = 59.0
TAIL_BLACK = 0.6


def run(args):
    return subprocess.run([FFMPEG, "-hide_banner", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")


def duration_of(path):
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", run(["-i", path]).stderr)
    if not m:
        sys.exit("Can't read the video's length - is it a video file?")
    h, mi, s = m.groups()
    return int(h) * 3600 + int(mi) * 60 + float(s)


def black_parts(path):
    out = run(["-i", path, "-vf", "blackdetect=d=0.25:pix_th=0.08", "-an", "-f", "null", "-"]).stderr
    return [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", out)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--no-crop", action="store_true")
    a = ap.parse_args()
    if not os.path.exists(a.input):
        sys.exit("File not found: " + a.input)

    total = duration_of(a.input)
    blacks = black_parts(a.input)
    start = 0.0
    end = total
    # the lead-in: the black that starts at (or right after) the beginning of the recording
    for b0, b1 in blacks:
        if b0 <= 1.5:
            start = b1
            break
    # the outro: the last black that runs to the end
    for b0, b1 in reversed(blacks):
        if b1 >= total - 0.3 and b0 > start + 5:
            end = min(total, b0 + TAIL_BLACK)
            break
    length = end - start
    if length > MAX_LEN:
        sys.exit(f"The trailer part is {length:.1f} s - longer than Roblox's 60 s limit. Did the recording include extra gameplay?")
    if length < 5:
        sys.exit(f"Only {length:.1f} s left after cutting the black - check the recording.")

    vf = "fps=60"
    if not a.no_crop:
        vf += ",crop=iw*11/12:ih*11/12:iw/12:ih/12"
    vf += ",scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p"

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    args = ["-y", "-ss", f"{start:.3f}", "-i", a.input, "-t", f"{length:.3f}",
            "-map", "0:v:0", "-map", "0:a:0?",
            "-vf", vf,
            "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "17",
            "-maxrate", "13.5M", "-bufsize", "27M", "-g", "120",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-af", f"afade=t=out:st={max(0.0, length - 0.5):.3f}:d=0.5",
            "-map_metadata", "-1", "-map_chapters", "-1", "-dn", "-sn",
            "-movflags", "+faststart", a.out]
    r = run(args)
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + r.stderr[-2000:])

    info = run(["-i", a.out]).stderr
    streams = re.findall(r"Stream #0:\d+.*?: (Video|Audio|Data|Subtitle|Attachment)", info)
    size_mb = os.path.getsize(a.out) / 1e6
    out_len = duration_of(a.out)
    print(f"Cut {start:.2f} s of black at the start; kept {length:.2f} s.")
    print(f"Saved {a.out}")
    print(f"  {out_len:.2f} s, {size_mb:.1f} MB, streams: {', '.join(streams)}")
    ok = streams.count("Video") == 1 and len(streams) <= 2 and size_mb < 100 and out_len <= 60
    print("  Ready for Creator Hub > Videos" if ok else "  WARNING: check the streams / size / length above")


if __name__ == "__main__":
    main()
