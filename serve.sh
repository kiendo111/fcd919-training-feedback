#!/usr/bin/env bash
# Preview the report locally. The page fetches data/*.csv, which the browser blocks over
# file://, so it has to be served over http://localhost. (In production GitHub Pages serves it.)
#
# Usage:  ./serve.sh        (Ctrl-C to stop; set PORT=xxxx to change the port)
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${PORT:-8899}"
echo "serving $DIR at http://localhost:$PORT/  (Ctrl-C to stop)"
xdg-open "http://localhost:$PORT/" >/dev/null 2>&1 || echo "(open http://localhost:$PORT/ manually)"
exec python3 -m http.server "$PORT" --directory "$DIR"
