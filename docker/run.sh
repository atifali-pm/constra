#!/usr/bin/env bash
# Convenience wrapper around `docker compose` for the Constra dev image.
#
# Usage:
#   docker/run.sh build              Build or rebuild the image.
#   docker/run.sh app                Launch the visual Constra main window.
#   docker/run.sh shell              Open an interactive shell in the container.
#   docker/run.sh test               Run the full test suite (headless).
#   docker/run.sh lint               Run ruff + black --check.
#   docker/run.sh fmt                Apply black formatting in-place.
#   docker/run.sh pdf                Regenerate docs/Constra-Vision.pdf.
#   docker/run.sh <anything else>    Run the given command inside the container.
#
# The first time you want to launch the visual app on a new host, run:
#
#   xhost +SI:localuser:$(whoami)
#
# to let the container's dev user draw on your X server.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/.." && pwd)"
cd "$REPO_ROOT"

# Use host UID/GID so files written from inside the container are owned
# by the host user. These are picked up by compose.yaml build args and
# by the --user flag at run time.
export HOST_UID="${HOST_UID:-$(id -u)}"
export HOST_GID="${HOST_GID:-$(id -g)}"

compose_run() {
    docker compose run --rm --user "$HOST_UID:$HOST_GID" constra "$@"
}

compose_run_headless() {
    docker compose run --rm --user "$HOST_UID:$HOST_GID" \
        -e QT_QPA_PLATFORM=offscreen constra "$@"
}

cmd="${1:-help}"
shift || true

case "$cmd" in
    build)
        docker compose build "$@"
        ;;
    app)
        compose_run python -m constra "$@"
        ;;
    shell|sh|bash)
        compose_run bash "$@"
        ;;
    test|pytest)
        compose_run_headless pytest "$@"
        ;;
    lint)
        compose_run_headless bash -c "ruff check . && black --check ."
        ;;
    fmt|format)
        compose_run_headless black .
        ;;
    pdf)
        compose_run_headless python scripts/build_vision_pdf.py "$@"
        ;;
    help|-h|--help)
        sed -n '2,20p' "$0"
        ;;
    *)
        # Fall through: run whatever the user passed.
        compose_run "$cmd" "$@"
        ;;
esac
