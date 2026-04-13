# Constra

An integrated desktop environment for geoscience interpretation.

> **Working name.** "Constra" is a placeholder; the project name is expected to change before a public release.

## What is it?

Constra is a new cross-platform desktop application for geoscience interpretation, aimed at the gap between heavyweight commercial platforms (e.g. Petrel) and general-purpose plotting tools (e.g. Surfer). It is designed around three linked views — **Map View**, **Section View**, and **3D View** — that share a single real-world coordinate frame, so the same well, seismic line, or horizon appears in the right place in every view.

The full motivation, background, comparison with existing tools, MVP scope, technology choice, and initial backlog live in the vision document:

- **[docs/Constra-Vision.pdf](docs/Constra-Vision.pdf)** — read this first.

## Repository layout

```
constra/
├── src/constra/                 # application source (PySide6 entry point)
├── tests/                       # pytest-qt test suite
├── docker/
│   ├── Dockerfile               # Python 3.12 + Qt 6 dev image
│   └── run.sh                   # convenience wrapper around `docker compose`
├── compose.yaml                 # dev service with X11, source mount, GPU passthrough
├── docs/
│   ├── Constra-Vision.pdf       # generated vision document (source of truth for scope)
│   ├── petrel.md                # cleaned rewrite of the Petrel source note
│   ├── surfer.md                # cleaned rewrite of the Surfer source note
│   └── images/                  # figures referenced by the docs and PDF
├── scripts/
│   └── build_vision_pdf.py      # regenerates docs/Constra-Vision.pdf
├── .github/workflows/ci.yml     # ruff + black + pytest on 3.10 / 3.11 / 3.12
├── pyproject.toml               # project metadata, dependencies, tool config
├── Document No. 1 Petrel.docx   # original source note (kept for provenance)
├── Document No. 2 Surfer.docx   # original source note (kept for provenance)
├── LICENSE                      # MIT
└── README.md
```

## Development environment (Docker)

The canonical development environment is a Docker image defined in [docker/Dockerfile](docker/Dockerfile) and wired up via [compose.yaml](compose.yaml). It installs Python 3.12, the full Qt 6 runtime, and the project in editable mode, and runs as a non-root user whose UID matches your host so files created inside the container stay owned by you on the host.

A small wrapper script [docker/run.sh](docker/run.sh) handles the common flows.

### First-time setup (Linux host with X11)

```bash
docker/run.sh build                   # build the image (~1 GB, once)
xhost +SI:localuser:$(whoami)         # allow the container to draw on your X server
```

`xhost` only needs to be re-run if you reboot or log out. If you are on a Wayland-only host, run your X server's Xwayland fallback first, or replace this with a VNC-based setup (not yet wired in).

### Everyday commands

```bash
docker/run.sh app             # launch the visual Constra main window (uses your X server)
docker/run.sh test            # headless test suite (QT_QPA_PLATFORM=offscreen)
docker/run.sh lint            # ruff check + black --check
docker/run.sh fmt             # apply black formatting in place
docker/run.sh pdf             # regenerate docs/Constra-Vision.pdf
docker/run.sh shell           # interactive bash inside the container
docker/run.sh <anything>      # run any command inside the container
```

The source tree is bind-mounted at `/app`, so host-side edits are picked up immediately — no rebuild needed unless you change dependencies or the Dockerfile.

### Rebuilding after dependency changes

Whenever `pyproject.toml` gains or loses a dependency, rebuild the image so the baked-in install is up to date:

```bash
docker/run.sh build
```

### Running without Docker

Docker is not mandatory. If you prefer a local Python environment, the project installs like any standard package:

```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
python -m constra
```

On Debian/Ubuntu you may need `sudo apt install python3-venv libgl1 libegl1 libxkbcommon0 libxcb-cursor0 libdbus-1-3 libfontconfig1` for PySide6 to launch.

## Current status

**M0 — Project bootstrap complete.** The repository holds the vision document, the rewritten source notes, a minimal PySide6 main window, a pytest-qt smoke test suite, GitHub Actions CI on Python 3.10/3.11/3.12, and a Docker-based development environment with X11 passthrough for visual runs. Next milestone is **M1 — Project container and CRS** (see section 8 of the vision PDF).

## Planned technology stack

- **Language:** Python 3.11+
- **GUI framework:** PySide6 (Qt 6)
- **Scientific visualisation:** VTK (optionally via PyVista)
- **Coordinate systems:** pyproj (PROJ)
- **Raster / vector I/O:** rasterio, pyogrio, geopandas
- **Seismic I/O:** segyio
- **Well log I/O:** lasio
- **Packaging:** PyInstaller (Windows installer for v0.1)

Rationale for each choice is in section 7 of the vision PDF.

## Platform

v0.1 targets **Windows 10/11**. The chosen stack is cross-platform, so Linux and macOS builds are expected to come essentially for free once the Windows build is stable, but they are not a v0.1 commitment.

## License

[MIT](LICENSE)
