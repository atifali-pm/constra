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
├── docs/
│   ├── Constra-Vision.pdf       # generated vision document (source of truth for scope)
│   ├── petrel.md                # cleaned rewrite of the Petrel source note
│   ├── surfer.md                # cleaned rewrite of the Surfer source note
│   └── images/                  # figures referenced by the docs and PDF
├── scripts/
│   └── build_vision_pdf.py      # regenerates docs/Constra-Vision.pdf
├── Document No. 1 Petrel.docx   # original source note (kept for provenance)
├── Document No. 2 Surfer.docx   # original source note (kept for provenance)
├── LICENSE                      # MIT
└── README.md
```

## Regenerating the vision PDF

The PDF is checked in, but it is generated from the rewritten Markdown sources and the images in `docs/images/`. To rebuild it:

```bash
python3 -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install reportlab Pillow
python3 scripts/build_vision_pdf.py
```

The script writes `docs/Constra-Vision.pdf`.

## Current status

Pre-code. This repository currently holds only the vision document and its sources. Implementation work begins with the **M0 — Project bootstrap** milestone described in the vision PDF.

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
