#!/usr/bin/env bash
# Optional dependency setup for the video/reverse-animation workflow.
# Installs Bun packages and Playwright Chromium; run only after the user approves.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"
if [[ "${HARNES_ALLOW_REANIMATE_INSTALL:-}" != "1" ]]; then
  echo "Refusing to install. After explicit user approval, re-run with HARNES_ALLOW_REANIMATE_INSTALL=1." >&2
  echo "This downloads Bun packages, Playwright Chromium, and a static FFmpeg binary (hundreds of MB)." >&2
  exit 2
fi
if ! command -v bun >/dev/null; then
  echo "Bun is required (upstream supports Bun 1.1+); install it separately after user approval." >&2
  exit 1
fi
if [[ ! -d node_modules/playwright || ! -x node_modules/ffmpeg-static/ffmpeg ]]; then
  bun install --frozen-lockfile --silent
fi
if ! bun -e 'const {chromium}=await import("playwright"); const b=await chromium.launch(); await b.close(); console.log("chromium ok")' 2>/dev/null; then
  echo "Chromium missing for this Playwright version, installing it..."
  ./node_modules/.bin/playwright install chromium
fi
node_modules/ffmpeg-static/ffmpeg -hide_banner -version | head -1
echo "ready: $HERE"
