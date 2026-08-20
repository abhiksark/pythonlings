#!/usr/bin/env bash
set -euo pipefail

# Renders docs/assets/branding/pythonlings-banner-source.html into:
#   docs/assets/branding/pythonlings-banner.gif   (animated, 100 frames at 25fps)
#   docs/assets/branding/pythonlings-hero.png     (static, 2x, frame $hero_frame)
#
# Each frame is captured independently by passing ?f=<n> to the source, so the
# output depends only on the source file and not on capture timing.

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
branding_dir="$repo_root/docs/assets/branding"
source_html="$branding_dir/pythonlings-banner-source.html"
gif_out="$branding_dir/pythonlings-banner.gif"
png_out="$branding_dir/pythonlings-hero.png"

frames=100
fps=25
width=1280
height=520
hero_frame=20
jobs="${BANNER_JOBS:-6}"
# Flat colour and crisp type quantise cleanly undithered; the pass sweep is the
# one gradient in the frame, so a light ordered dither is worth its bytes.
# Ordered dithering is position-based and so stays identical across frames,
# which keeps static regions diffing away to nothing.
dither="${BANNER_DITHER:-bayer:bayer_scale=5}"
capture_timeout="${BANNER_CAPTURE_TIMEOUT:-45}"
capture_attempts=3

ffmpeg_bin="${FFMPEG_BIN:-ffmpeg}"
if ! command -v "$ffmpeg_bin" >/dev/null 2>&1; then
  cat >&2 <<'EOF'
ffmpeg is required to encode the banner GIF.

Install it with:
  brew install ffmpeg

To use a specific binary:
  FFMPEG_BIN=/path/to/ffmpeg scripts/generate_banner.sh
EOF
  exit 127
fi

chrome_bin="${CHROME_BIN:-}"
if [[ -z "$chrome_bin" ]]; then
  for candidate in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    google-chrome chromium chromium-browser; do
    if [[ -x "$candidate" ]] || command -v "$candidate" >/dev/null 2>&1; then
      chrome_bin="$candidate"
      break
    fi
  done
fi
if [[ -z "$chrome_bin" ]]; then
  cat >&2 <<'EOF'
A Chrome or Chromium binary is required to capture banner frames.

Install Google Chrome, or point at an existing binary:
  CHROME_BIN=/path/to/chrome scripts/generate_banner.sh
EOF
  exit 127
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 with Pillow is required to verify captured frames." >&2
  exit 127
fi

work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

export BANNER_CHROME="$chrome_bin"
export BANNER_URL="file://$source_html"
export BANNER_WORK="$work_dir"
export BANNER_SIZE="$width,$height"
export BANNER_TIMEOUT="$capture_timeout"
export BANNER_ATTEMPTS="$capture_attempts"

capture_frame() {
  local index="$1"
  local out attempt chrome_pid watchdog_pid
  printf -v out "%s/frame_%03d.png" "$BANNER_WORK" "$index"

  for ((attempt = 1; attempt <= BANNER_ATTEMPTS; attempt++)); do
    rm -f "$out"
    "$BANNER_CHROME" \
      --headless=new --hide-scrollbars --disable-gpu \
      --window-size="$BANNER_SIZE" --virtual-time-budget=10000 \
      --screenshot="$out" "$BANNER_URL?f=$index" >/dev/null 2>&1 &
    chrome_pid=$!

    ( sleep "$BANNER_TIMEOUT"; kill -9 "$chrome_pid" 2>/dev/null ) &
    watchdog_pid=$!

    wait "$chrome_pid" 2>/dev/null || true
    kill "$watchdog_pid" 2>/dev/null || true
    wait "$watchdog_pid" 2>/dev/null || true

    if [[ -s "$out" ]]; then
      return 0
    fi
    echo "  frame $index produced nothing on attempt $attempt; retrying" >&2
  done

  echo "failed to capture frame $index after $BANNER_ATTEMPTS attempts" >&2
  return 1
}
export -f capture_frame

echo "Capturing $frames frames at ${width}x${height} (${jobs} at a time)..."
seq 0 $((frames - 1)) | xargs -P "$jobs" -I {} bash -c 'capture_frame "$@"' _ {}

# The source pulls its webfont over the network, once per capture. If a frame
# renders before that font is ready it will differ from its neighbours in a
# region that is supposed to be identical in every frame, which shows up as
# type that flickers between fallback and JetBrains Mono. Fail loudly instead.
echo "Verifying frame consistency..."
python3 - "$work_dir" "$frames" <<'PYEOF'
import hashlib
import sys

from PIL import Image

work_dir, frames = sys.argv[1], int(sys.argv[2])
# The tagline never animates, so every frame must render it identically.
STATIC_REGION = (52, 388, 350, 451)

digests = {}
for index in range(frames):
    path = "%s/frame_%03d.png" % (work_dir, index)
    try:
        crop = Image.open(path).convert("RGB").crop(STATIC_REGION)
        digest = hashlib.sha256(crop.tobytes()).hexdigest()
    except Exception as exc:
        print("frame %d did not decode: %s" % (index, exc), file=sys.stderr)
        sys.exit(1)
    digests.setdefault(digest, []).append(index)

if len(digests) != 1:
    groups = sorted(digests.values(), key=len, reverse=True)
    print("Frames disagree in a region that never animates.", file=sys.stderr)
    print("This usually means the webfont had not loaded for some captures.", file=sys.stderr)
    for group in groups[1:]:
        print("  odd frames: %s" % group, file=sys.stderr)
    sys.exit(1)

print("  all %d frames agree on the static region" % frames)
PYEOF

echo "Encoding $gif_out..."
"$ffmpeg_bin" -v error -y -framerate "$fps" -i "$work_dir/frame_%03d.png" \
  -vf "palettegen=stats_mode=full" "$work_dir/palette.png"
"$ffmpeg_bin" -v error -y -framerate "$fps" -i "$work_dir/frame_%03d.png" \
  -i "$work_dir/palette.png" \
  -lavfi "paletteuse=dither=$dither:diff_mode=rectangle" \
  -loop 0 "$gif_out"

echo "Rendering $png_out from frame $hero_frame at 2x..."
"$chrome_bin" \
  --headless=new --hide-scrollbars --disable-gpu \
  --force-device-scale-factor=2 \
  --window-size="$width,$height" --virtual-time-budget=10000 \
  --screenshot="$png_out" "file://$source_html?f=$hero_frame" >/dev/null 2>&1 || true
if [[ ! -s "$png_out" ]]; then
  echo "failed to render $png_out" >&2
  exit 1
fi

python3 - "$gif_out" "$png_out" "$frames" "$fps" <<'PYEOF'
import os
import sys

from PIL import Image

gif_path, png_path, frames, fps = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])

gif = Image.open(gif_path)
assert gif.n_frames == frames, "expected %d frames, got %d" % (frames, gif.n_frames)
print("")
print("  %s  %dx%d  %d frames  %.2fs  %.0f KB" % (
    os.path.basename(gif_path), gif.size[0], gif.size[1], gif.n_frames,
    gif.n_frames / float(fps), os.path.getsize(gif_path) / 1024.0))

png = Image.open(png_path)
print("  %s  %dx%d  %.0f KB" % (
    os.path.basename(png_path), png.size[0], png.size[1],
    os.path.getsize(png_path) / 1024.0))
PYEOF
