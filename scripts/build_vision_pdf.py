"""Generate docs/Constra-Vision.pdf from the rewritten source documents.

Run from the repository root:
    python3 scripts/build_vision_pdf.py
"""

from __future__ import annotations

import os
from datetime import date

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(REPO_ROOT, "docs", "images")
OUTPUT_PATH = os.path.join(REPO_ROOT, "docs", "Constra-Vision.pdf")

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = RIGHT_MARGIN = 2 * cm
TOP_MARGIN = BOTTOM_MARGIN = 2 * cm
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

NAVY = colors.HexColor("#0B3D91")
SLATE = colors.HexColor("#334155")
LIGHT = colors.HexColor("#E2E8F0")
ACCENT = colors.HexColor("#B45309")


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=40,
            leading=48,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=16,
            leading=22,
            textColor=SLATE,
            alignment=TA_CENTER,
            spaceAfter=24,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=11,
            leading=14,
            textColor=SLATE,
            alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=26,
            textColor=NAVY,
            spaceBefore=6,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=NAVY,
            spaceBefore=12,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=15,
            textColor=SLATE,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=colors.black,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=colors.black,
            leftIndent=14,
            bulletIndent=2,
            spaceAfter=3,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["Italic"],
            fontName="Helvetica-Oblique",
            fontSize=9.5,
            leading=12,
            textColor=SLATE,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=14,
        ),
        "callout": ParagraphStyle(
            "callout",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=10.5,
            leading=15,
            textColor=ACCENT,
            leftIndent=10,
            rightIndent=10,
            spaceBefore=6,
            spaceAfter=10,
        ),
    }


def scaled_image(path: str, max_width: float, max_height: float) -> Image:
    """Return a reportlab Image scaled to fit within the given bounds."""
    with PILImage.open(path) as im:
        iw, ih = im.size
    ratio = min(max_width / iw, max_height / ih)
    return Image(path, width=iw * ratio, height=ih * ratio)


def figure(path: str, caption: str, styles, max_h: float = 10 * cm) -> KeepTogether:
    img = scaled_image(path, CONTENT_WIDTH, max_h)
    cap = Paragraph(caption, styles["caption"])
    return KeepTogether([img, Spacer(1, 2 * mm), cap])


def bullet_list(items: list[str], styles) -> list:
    return [Paragraph(f"\u2022&nbsp;&nbsp;{item}", styles["bullet"]) for item in items]


def _header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(SLATE)
    if doc.page > 1:
        canvas.drawString(
            LEFT_MARGIN,
            1.1 * cm,
            "Constra — Vision & Initial Scope",
        )
        canvas.drawRightString(
            PAGE_WIDTH - RIGHT_MARGIN,
            1.1 * cm,
            f"Page {doc.page}",
        )
    canvas.restoreState()


def build_story(styles) -> list:
    story: list = []

    # -------- Cover --------
    story.append(Spacer(1, 5 * cm))
    story.append(Paragraph("CONSTRA", styles["cover_title"]))
    story.append(
        Paragraph(
            "An integrated desktop environment for geoscience interpretation",
            styles["cover_subtitle"],
        )
    )
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph("Vision &amp; Initial Scope", styles["cover_subtitle"]))
    story.append(Spacer(1, 4 * cm))
    story.append(
        Paragraph(
            f"Draft v0.1 &middot; {date.today().isoformat()}<br/>"
            "Working name: <b>Constra</b> (subject to change)",
            styles["cover_meta"],
        )
    )
    story.append(PageBreak())

    # -------- Executive Summary --------
    story.append(Paragraph("1. Executive Summary", styles["h1"]))
    story.append(
        Paragraph(
            "Constra is a new cross-platform desktop application for geoscience "
            "interpretation. It starts from a simple observation: the tools geoscientists "
            "use today fall into two camps. On one side sit large, integrated commercial "
            "platforms such as <b>Petrel</b> that combine satellite imagery, 2D seismic, "
            "well data, and 3D reservoir models into a single interactive workspace in "
            "real-world coordinates. On the other side sit general-purpose plotting tools "
            "such as <b>Surfer</b> that are capable but manual, figure-oriented, and not "
            "designed to hold a whole project in a shared coordinate frame.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Constra aims at the underserved middle: the power of an integrated, "
            "coordinate-aware, multi-view workspace, delivered as an open, accessible "
            "desktop tool that a single geoscientist, a student, or a small consultancy "
            "can actually install and use.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "This document captures the two source notes that motivated the project "
            "(summaries of Petrel and Surfer), distils them into a comparison, and then "
            "lays out the problem statement, target user, MVP scope, technology choice, "
            "and the initial backlog of tasks needed to stand the project up.",
            styles["body"],
        )
    )
    story.append(PageBreak())

    # -------- Background: Petrel --------
    story.append(Paragraph("2. Background — Petrel", styles["h1"]))
    story.append(
        Paragraph(
            "Petrel is a leading oil and gas industry interpretation platform. It "
            "integrates geophysical, geological, hydrogeological, and reservoir data "
            "into a single interactive environment where multiple data types can be "
            "combined and visualised together. Data can be displayed in both 2D and 3D, "
            "and every view stays in sync with the others.",
            styles["body"],
        )
    )

    story.append(Paragraph("2.1 Map View", styles["h2"]))
    story.append(
        Paragraph(
            "All datasets are displayed in their true geographic location inside a "
            "shared Map View. Satellite imagery, seismic line locations, well locations, "
            "and cultural features (roads, buildings, infrastructure) can all be layered "
            "in the same window.",
            styles["body"],
        )
    )
    story.append(
        figure(
            os.path.join(IMAGES_DIR, "01-petrel-map-view-satellite.png"),
            "Figure 1 — Satellite basemap in Petrel's Map View. A satellite image of the "
            "project area is loaded as the bottom layer of the map, providing real-world "
            "geographic context for everything placed on top of it.",
            styles,
        )
    )
    story.append(
        figure(
            os.path.join(IMAGES_DIR, "02-petrel-map-seismic-wells.png"),
            "Figure 2 — Seismic lines overlaid with well locations. The same Map View "
            "now also shows the geometry of acquired 2D seismic lines together with "
            "well locations, so an interpreter can pick which line to open next based "
            "on where the wells are.",
            styles,
        )
    )

    story.append(Paragraph("2.2 Section View", styles["h2"]))
    story.append(
        Paragraph(
            "The Section View is used to display data that is naturally viewed as a "
            "vertical slice through the earth — 2D seismic lines, well logs, horizons, "
            "and faults. Selecting a line on the map opens it here as a vertical section, "
            "ready for interpretation.",
            styles["body"],
        )
    )
    story.append(
        figure(
            os.path.join(IMAGES_DIR, "03-petrel-section-view-seismic.png"),
            "Figure 3 — 2D seismic line displayed as a vertical section in Petrel.",
            styles,
        )
    )
    story.append(
        Paragraph(
            "<b>Key behaviour.</b> Map View and Section View are fully interactive. "
            "An action taken in one view — selecting a line, picking a horizon, moving a "
            "crosshair — is immediately reflected in the other. The same is true for "
            "every other data type loaded into the project.",
            styles["callout"],
        )
    )

    story.append(Paragraph("2.3 3D View", styles["h2"]))
    story.append(
        Paragraph(
            "In addition to 2D, all data can be viewed, interpreted, and displayed in a "
            "3D View, which is also synchronised with the Map View and Section View.",
            styles["body"],
        )
    )
    story.append(
        figure(
            os.path.join(IMAGES_DIR, "04-petrel-3d-seismic-lines.png"),
            "Figure 4 — 3D view of seismic lines in Petrel. Multiple 2D seismic lines "
            "are rendered together in three-dimensional space, making it easier to see "
            "how the subsurface looks along intersecting acquisition directions.",
            styles,
        )
    )
    story.append(
        figure(
            os.path.join(IMAGES_DIR, "05-petrel-3d-reservoir-well.png"),
            "Figure 5 — 3D view of reservoir data with a well. A reservoir model is "
            "visualised in 3D alongside a well trajectory, so the relationship between "
            "the well path and the reservoir body can be assessed directly.",
            styles,
        )
    )

    story.append(Paragraph("2.4 Coordinate System", styles["h2"]))
    story.append(
        Paragraph(
            "Petrel works natively in real-world coordinates, both geographic "
            "(latitude/longitude) and projected (Easting/Northing). Every dataset is "
            "placed in its true location, and projections are handled by the software "
            "rather than by the user. This is what makes the cross-view interactivity "
            "meaningful: a well clicked in the Map View is the <i>same</i> well in the "
            "Section View and the 3D View, because the underlying coordinate system is "
            "unified.",
            styles["body"],
        )
    )
    story.append(PageBreak())

    # -------- Background: Surfer --------
    story.append(Paragraph("3. Background — Surfer", styles["h1"]))
    story.append(
        Paragraph(
            "Surfer (by Golden Software) is a plotting and contouring package widely "
            "used for displaying spatial data. It is capable software and well suited "
            "to producing individual map and section figures, but it was not designed "
            "as an integrated interpretation environment in the way Petrel was.",
            styles["body"],
        )
    )

    story.append(Paragraph("3.1 Map and Section Views", styles["h2"]))
    story.append(
        Paragraph(
            "Surfer does not provide dedicated Map and Section views that are separate "
            "from each other. All output — whether conceptually a map or a vertical "
            "section — is drawn into the same generic plot window. There is no shared "
            "geographic canvas, no automatic basemap layer, and no cross-view "
            "synchronisation. Each figure is a standalone artefact constructed by hand.",
            styles["body"],
        )
    )

    story.append(Paragraph("3.2 3D View", styles["h2"]))
    story.append(
        Paragraph(
            "Surfer offers 3D surface and wireframe plots, but these are again "
            "standalone outputs rather than a synchronised 3D workspace. A 3D plot does "
            "not share state with any 2D map or section that the user has open.",
            styles["body"],
        )
    )

    story.append(Paragraph("3.3 Coordinate System", styles["h2"]))
    story.append(
        Paragraph(
            "Surfer does not natively place datasets into a shared real-world projected "
            "coordinate frame the way Petrel does. Data is plotted against whatever "
            "coordinate values are supplied in the input file, and the user is "
            "responsible for ensuring those values are consistent across datasets. "
            "There is no built-in projection engine that unifies every dataset into a "
            "single geographic reference.",
            styles["body"],
        )
    )

    story.append(Paragraph("3.4 Workflow", styles["h2"]))
    story.append(
        Paragraph(
            "Surfer's workflow is predominantly manual. Every dataset, every object, "
            "every label is added to the plot by the user. This is acceptable when "
            "producing a single figure, but it scales poorly when many datasets must "
            "be kept consistent, when data is updated frequently, or when an interpreter "
            "needs to move fluidly between map, section, and 3D perspectives of the "
            "same subsurface model.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Product page: <link href='https://www.goldensoftware.com/products/surfer' "
            "color='#0B3D91'>https://www.goldensoftware.com/products/surfer</link>",
            styles["body"],
        )
    )
    story.append(PageBreak())

    # -------- Comparison table --------
    story.append(Paragraph("4. Side-by-Side Comparison", styles["h1"]))
    story.append(
        Paragraph(
            "The table below distils the two backgrounds into the capabilities that "
            "matter most for an integrated interpretation workflow.",
            styles["body"],
        )
    )

    def cell(text: str, style_key: str = "body") -> Paragraph:
        s = ParagraphStyle(
            f"cell_{style_key}",
            parent=styles[style_key],
            fontSize=9.5,
            leading=12,
            alignment=TA_LEFT,
            spaceAfter=0,
        )
        return Paragraph(text, s)

    data = [
        [cell("<b>Capability</b>"), cell("<b>Petrel</b>"), cell("<b>Surfer</b>")],
        [
            cell("Dedicated Map View"),
            cell("Yes — shared geographic canvas"),
            cell("No — generic plot window"),
        ],
        [
            cell("Dedicated Section View"),
            cell("Yes — vertical slice, linked to map"),
            cell("No — another plot in the same window"),
        ],
        [
            cell("Dedicated 3D View"),
            cell("Yes — synchronised 3D workspace"),
            cell("Standalone 3D plots only"),
        ],
        [
            cell("Cross-view interactivity"),
            cell("Yes — actions propagate across views"),
            cell("No — figures are independent"),
        ],
        [
            cell("Real-world coordinates (lat/long, E/N)"),
            cell("Native; projections handled automatically"),
            cell("Not native; user manages coordinate consistency"),
        ],
        [
            cell("Data integration model"),
            cell("Unified project containing all datasets"),
            cell("Per-figure, assembled manually"),
        ],
        [
            cell("Typical audience"),
            cell("Large operators, well-funded teams"),
            cell("Anyone producing geoscience figures"),
        ],
        [
            cell("Accessibility / cost"),
            cell("Enterprise-priced commercial license"),
            cell("Commercial license, far more affordable"),
        ],
    ]

    col_widths = [CONTENT_WIDTH * 0.26, CONTENT_WIDTH * 0.37, CONTENT_WIDTH * 0.37]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, SLATE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
            ]
        )
    )
    story.append(table)
    story.append(PageBreak())

    # -------- Problem & target user --------
    story.append(Paragraph("5. Problem Statement & Target User", styles["h1"]))
    story.append(Paragraph("5.1 The gap", styles["h2"]))
    story.append(
        Paragraph(
            "A geoscientist who wants to work on subsurface data today faces a choice "
            "between two extremes. Commercial integrated platforms such as Petrel "
            "deliver an excellent multi-view, coordinate-aware workflow, but are priced "
            "for large operators and tied to heavy enterprise licensing. General plotting "
            "tools such as Surfer are affordable but produce isolated figures rather than "
            "a living, linked interpretation environment. There is no widely available, "
            "lightweight desktop tool that offers the <i>workflow</i> benefits of the "
            "integrated model (shared coordinate frame, linked views, data-type awareness) "
            "without the enterprise baggage.",
            styles["body"],
        )
    )

    story.append(Paragraph("5.2 Who Constra is for", styles["h2"]))
    story.extend(
        bullet_list(
            [
                "Independent geoscientists and small consultancies who cannot justify "
                "a Petrel license but need more than a plotting tool.",
                "University students and researchers learning interpretation workflows "
                "on real data.",
                "Adjacent disciplines (shallow geothermal, mineral exploration, "
                "hydrogeology, near-surface geophysics) whose data looks like oil and "
                "gas data but whose budgets do not.",
                "Anyone who wants to load a GeoTIFF basemap, drop well locations on it, "
                "open a seismic section linked to those wells, and view the whole thing "
                "in 3D — without a week of manual plot construction.",
            ],
            styles,
        )
    )

    story.append(Paragraph("5.3 What Constra is explicitly not", styles["h2"]))
    story.extend(
        bullet_list(
            [
                "Not a full Petrel replacement. Petrel is a multi-decade, multi-hundred-"
                "person platform; Constra will not match its feature breadth and should "
                "not try to.",
                "Not a reservoir simulator. Constra is an interpretation and "
                "visualisation environment, not a numerical solver.",
                "Not a web application (initially). The first release is a desktop app.",
            ],
            styles,
        )
    )
    story.append(PageBreak())

    # -------- MVP scope --------
    story.append(Paragraph("6. MVP Scope", styles["h1"]))
    story.append(
        Paragraph(
            "The MVP has to be small enough to ship and sharp enough to prove the core "
            "thesis: <b>shared coordinate frame, linked views, real geoscience data.</b> "
            "Everything below is in scope for v0.1. Everything else is deferred.",
            styles["body"],
        )
    )

    story.append(Paragraph("6.1 In scope for v0.1", styles["h2"]))
    story.extend(
        bullet_list(
            [
                "<b>Project container.</b> A Constra project is a folder that holds "
                "datasets plus a project-level coordinate reference system (CRS).",
                "<b>Map View.</b> 2D canvas that renders all datasets in their real-world "
                "projected coordinates, with pan, zoom, and layer visibility controls.",
                "<b>Section View.</b> Dedicated window for displaying one vertical "
                "section at a time, linked to the Map View.",
                "<b>3D View.</b> A minimal 3D scene showing the same datasets in space, "
                "linked to the Map View's selection.",
                "<b>Data formats, read-only for MVP:</b> GeoTIFF (raster basemap); "
                "shapefile and GeoJSON (vector features); CSV (point data such as well "
                "heads); LAS (well logs, 1D); SEG-Y (2D post-stack seismic).",
                "<b>Coordinate system support.</b> Per-project CRS, with on-the-fly "
                "reprojection of loaded datasets via PROJ (pyproj).",
                "<b>Cross-view selection.</b> Selecting a well on the map highlights it "
                "in the section view and the 3D view.",
                "<b>Windows installer.</b> A one-click MSI or exe for Windows 10/11.",
            ],
            styles,
        )
    )

    story.append(Paragraph("6.2 Deferred past v0.1", styles["h2"]))
    story.extend(
        bullet_list(
            [
                "Horizon picking, fault interpretation, attribute generation.",
                "3D reservoir grids and property modelling.",
                "Write support for any file format (v0.1 is read-only).",
                "Collaboration, cloud sync, multi-user projects.",
                "Mac and Linux installers (possible later; Windows is the priority).",
                "Python scripting / plugin API (likely v0.3 or later).",
            ],
            styles,
        )
    )
    story.append(PageBreak())

    # -------- Tech stack --------
    story.append(Paragraph("7. Technology Choice", styles["h1"]))
    story.append(Paragraph("7.1 Chosen stack", styles["h2"]))
    story.extend(
        bullet_list(
            [
                "<b>Language:</b> Python 3.11+",
                "<b>GUI framework:</b> PySide6 (Qt 6 bindings, LGPL)",
                "<b>3D and scientific visualisation:</b> VTK (the library behind "
                "ParaView and 3D Slicer), optionally via PyVista for ergonomics",
                "<b>Coordinate systems:</b> pyproj (bindings to PROJ)",
                "<b>Raster I/O:</b> rasterio (GeoTIFF, etc.)",
                "<b>Vector I/O:</b> pyogrio or Fiona for shapefile/GeoJSON; geopandas "
                "for in-memory manipulation",
                "<b>Seismic I/O:</b> segyio for SEG-Y",
                "<b>Well log I/O:</b> lasio for LAS",
                "<b>Packaging for Windows:</b> PyInstaller or briefcase, producing a "
                "standalone installer",
                "<b>Testing:</b> pytest, with pytest-qt for GUI tests",
                "<b>Linting / formatting:</b> ruff, black",
            ],
            styles,
        )
    )

    story.append(Paragraph("7.2 Why this stack", styles["h2"]))
    story.append(
        Paragraph(
            "This is the same toolchain that underpins ParaView and 3D Slicer, two of "
            "the most successful open-source scientific visualisation applications in "
            "existence. Every hard problem on Constra's roadmap — large raster display, "
            "3D scene management, coordinate reprojection, seismic parsing, well log "
            "parsing — already has a mature, well-maintained Python library. Python "
            "also keeps iteration speed high, which matters enormously at v0.1 when "
            "the biggest risk is <i>building the wrong product</i>, not <i>building it "
            "too slowly</i>. A future port of performance-critical pieces to C++ or Rust "
            "remains possible; starting there would simply slow the project down before "
            "the core product ideas have been tested.",
            styles["body"],
        )
    )

    story.append(Paragraph("7.3 Platform strategy", styles["h2"]))
    story.append(
        Paragraph(
            "v0.1 targets <b>Windows 10/11</b> only, because that is where the target "
            "users already run Petrel and Surfer. Because the chosen stack is "
            "cross-platform by construction, Linux and macOS builds are expected to "
            "come essentially for free once the Windows build is stable — but they are "
            "not a v0.1 commitment.",
            styles["body"],
        )
    )
    story.append(PageBreak())

    # -------- Initial tasks --------
    story.append(Paragraph("8. Initial Task List", styles["h1"]))
    story.append(
        Paragraph(
            "The backlog below is organised into milestones. Each milestone is meant "
            "to end in a runnable application that does a little bit more than the "
            "previous one.",
            styles["body"],
        )
    )

    milestones = [
        (
            "M0 — Project bootstrap",
            [
                "Create GitHub repository (public) and add MIT license, README, "
                ".gitignore.",
                "Set up Python project skeleton (pyproject.toml, src/ layout, virtual "
                "environment instructions).",
                "Add ruff + black + pytest + pytest-qt and a minimal CI workflow "
                "(GitHub Actions) that runs them on push.",
                "Add a hello-world PySide6 main window that launches and closes cleanly.",
            ],
        ),
        (
            "M1 — Project container and CRS",
            [
                "Define the on-disk Constra project format (project folder + "
                "project.json or project.toml).",
                "Implement project create / open / save.",
                "Implement a project-level CRS setting (pick EPSG code at project "
                "creation, stored in project file).",
                "Wire pyproj for on-the-fly reprojection of any loaded dataset into "
                "the project CRS.",
            ],
        ),
        (
            "M2 — Map View",
            [
                "Build the Map View widget (Qt Graphics View or a VTK 2D render window).",
                "Load a GeoTIFF via rasterio and display it reprojected into the "
                "project CRS.",
                "Load a shapefile/GeoJSON via pyogrio and overlay it.",
                "Load a CSV of point data (e.g. well heads) and plot each point with "
                "a label.",
                "Add pan / zoom / layer visibility controls and a simple layer panel.",
            ],
        ),
        (
            "M3 — Section View",
            [
                "Build the Section View widget.",
                "Implement a SEG-Y reader (segyio) that loads one 2D post-stack line.",
                "Display the seismic section with configurable colour map and gain.",
                "Link Section View to Map View: clicking a line on the map opens it "
                "in the section view.",
            ],
        ),
        (
            "M4 — 3D View",
            [
                "Build the 3D View widget using VTK / PyVista.",
                "Render the loaded basemap, well heads, and seismic line in 3D space.",
                "Link 3D View selection to Map View and Section View (shared selection "
                "model).",
            ],
        ),
        (
            "M5 — Well logs and first installer",
            [
                "Load LAS files with lasio and display logs in a small embedded log "
                "track beside the Section View.",
                "Package the app for Windows with PyInstaller (or briefcase).",
                "Produce a signed installer and publish it as a GitHub release "
                "artifact.",
            ],
        ),
    ]

    for title, items in milestones:
        story.append(Paragraph(title, styles["h2"]))
        story.extend(bullet_list(items, styles))

    story.append(Spacer(1, 6 * mm))
    story.append(
        Paragraph(
            "Shipping M5 means Constra v0.1 is a real application: it can open a "
            "GeoTIFF basemap, plot wells on it in real-world coordinates, open a linked "
            "SEG-Y seismic line in a section view with its well logs alongside, and "
            "show the whole scene in 3D — installable from a single Windows installer. "
            "That is the smallest possible product that proves the thesis.",
            styles["body"],
        )
    )

    return story


def main() -> None:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    styles = make_styles()
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title="Constra — Vision & Initial Scope",
        author="Constra project",
        subject="Vision document, background, MVP scope, initial task list",
    )
    story = build_story(styles)
    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
