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
    return [Paragraph(f"•&nbsp;&nbsp;{item}", styles["bullet"]) for item in items]


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
            "An integrated geoscience workspace for engineering and construction",
            styles["cover_subtitle"],
        )
    )
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph("Vision &amp; Initial Scope", styles["cover_subtitle"]))
    story.append(Spacer(1, 4 * cm))
    story.append(
        Paragraph(
            f"Draft v0.2 &middot; {date.today().isoformat()}<br/>"
            "Working name: <b>Constra</b> (subject to change)",
            styles["cover_meta"],
        )
    )
    story.append(PageBreak())

    # -------- Executive Summary --------
    story.append(Paragraph("1. Executive Summary", styles["h1"]))
    story.append(
        Paragraph(
            "Constra is a desktop application for <b>engineering geoscience</b> — the daily "
            "working environment for engineering geologists and engineering geophysicists "
            "in geotechnical site investigation, civil and construction engineering, "
            "mining engineering, and environmental / engineering hydrogeology. It is built "
            "around three linked views — Map, Section, and 3D — that share a single "
            "real-world coordinate frame, so the boreholes, in-situ tests, near-surface "
            "geophysics, topographic data, and CAD-derived plans that drive an engineering "
            "project all live together in one project.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "The oil &amp; gas industry has had this kind of integrated, coordinate-aware "
            "workspace for decades — Petrel, by Schlumberger, is the canonical example "
            "and a genuinely outstanding product within its domain. Engineering "
            "geoscience has had no equivalent. Practitioners assemble cross-sections by "
            "hand in CAD, plot data in generic tools, and stitch results together across "
            "half a dozen single-purpose applications, with all the workflow friction "
            "and silent inconsistency that implies. Constra exists to close that gap — "
            "to give the engineering practitioner the same kind of integrated workspace "
            "that the oil industry has long enjoyed, but built specifically around "
            "engineering data, engineering coordinate systems, and the engineering "
            "interpretation workflow.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Petrel and Surfer appear in this document only as <i>exemplars</i>. Petrel "
            "illustrates what an integrated, multi-view, coordinate-aware workspace looks "
            "like when one is purpose-built for an industry. Surfer illustrates the limits "
            "of generic plotting tools that lack a project model. Neither is a competitor "
            "to Constra: Constra serves a different industry — one that currently has "
            "nothing of either kind purpose-built for it.",
            styles["body"],
        )
    )
    story.append(PageBreak())

    # -------- Background: Petrel --------
    story.append(Paragraph("2. Exemplar — Petrel", styles["h1"]))
    story.append(
        Paragraph(
            "Petrel is a flagship interpretation platform built by Schlumberger for the "
            "oil &amp; gas industry. It is shown here only as an exemplar — a legendary "
            "product within its industry, used to illustrate what an integrated, "
            "coordinate-aware geoscience workspace looks like when one is purpose-built "
            "for a domain. Petrel does not serve engineering, and Constra is not a "
            "Petrel alternative; the two products live in different industries. The "
            "figures that follow are reproduced so that the reader can see, concretely, "
            "what the engineering equivalent — Constra — should feel like in use.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Within its own industry, Petrel integrates geophysical, geological, "
            "hydrogeological, and reservoir data into a single interactive environment "
            "where multiple data types can be combined and visualised together. Data is "
            "displayed in both 2D and 3D, and every view stays in sync with the others.",
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
            "Figure 2 — Seismic lines overlaid with well locations. The Map View shows "
            "the geometry of acquired 2D seismic lines together with well locations, so "
            "an interpreter can pick which line to open next based on where the wells are.",
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
            "unified. Constra targets the same property for engineering data.",
            styles["body"],
        )
    )
    story.append(PageBreak())

    # -------- Background: Surfer --------
    story.append(Paragraph("3. Exemplar — Surfer", styles["h1"]))
    story.append(
        Paragraph(
            "Surfer (by Golden Software) is a widely used plotting and contouring "
            "package for spatial data. It is shown here as an exemplar of a different "
            "category — a generic plotting tool, not an industry-specific workspace — "
            "to illustrate where the integration limit sits when a tool is not built "
            "around a project model. Surfer is good at what it does; the point is simply "
            "that what it does is not what an engineering practitioner needs as a daily "
            "working environment.",
            styles["body"],
        )
    )

    story.append(Paragraph("3.1 No dedicated views", styles["h2"]))
    story.append(
        Paragraph(
            "Surfer does not provide separate Map, Section, and 3D views that share "
            "state. All output — whether conceptually a map or a vertical section — is "
            "drawn into the same generic plot window. There is no shared geographic "
            "canvas, no automatic basemap layer, and no cross-view synchronisation. "
            "Each figure is a standalone artefact constructed by hand.",
            styles["body"],
        )
    )

    story.append(Paragraph("3.2 No project-level coordinate frame", styles["h2"]))
    story.append(
        Paragraph(
            "Surfer does not place datasets into a shared real-world projected coordinate "
            "frame. Data is plotted against whatever coordinate values are supplied in "
            "the input file, and the user is responsible for ensuring those values are "
            "consistent across datasets. There is no built-in projection engine that "
            "unifies every dataset into a single geographic reference.",
            styles["body"],
        )
    )

    story.append(Paragraph("3.3 Manual workflow", styles["h2"]))
    story.append(
        Paragraph(
            "Every dataset, every object, every label is added to the plot by the user. "
            "This is acceptable when producing a single figure, but it scales poorly "
            "when many datasets must be kept consistent, when data is updated frequently, "
            "or when an interpreter needs to move fluidly between map, section, and 3D "
            "perspectives of the same subsurface model.",
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

    # -------- Comparison: where things stand for engineering --------
    story.append(Paragraph("4. The Engineering-Geoscience Gap", styles["h1"]))
    story.append(
        Paragraph(
            "The point of contrasting these two exemplars is not to compare them with "
            "each other, but to show what the engineering practitioner has access to "
            "today. The oil &amp; gas industry has Petrel; everyone, including "
            "engineering teams, has Surfer-class plotting tools; engineering geoscience "
            "has no widely available integrated workspace of its own. The table below "
            "makes that gap explicit.",
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
        [
            cell("<b>Capability</b>"),
            cell("<b>Petrel<br/>(oil &amp; gas)</b>"),
            cell("<b>Surfer<br/>(generic plotting)</b>"),
            cell("<b>Engineering<br/>geoscience today</b>"),
        ],
        [
            cell("Industry-specific integrated workspace"),
            cell("Yes"),
            cell("—"),
            cell("None widely available"),
        ],
        [
            cell("Single project / shared coordinate frame"),
            cell("Yes"),
            cell("No"),
            cell("None widely available"),
        ],
        [
            cell("Real-world coordinates, automatic reprojection"),
            cell("Yes"),
            cell("No"),
            cell("Handled per-tool, per-file"),
        ],
        [
            cell("Linked Map / Section / 3D views"),
            cell("Yes"),
            cell("No"),
            cell("None widely available"),
        ],
        [
            cell("Multiple simultaneous cross-sections"),
            cell("Yes"),
            cell("No"),
            cell("Manual in CAD"),
        ],
        [
            cell("Native readers for the industry's primary data"),
            cell("Yes (oil &amp; gas formats)"),
            cell("—"),
            cell("Fragmented across single-purpose tools"),
        ],
        [
            cell("Cross-view selection / propagation"),
            cell("Yes"),
            cell("No"),
            cell("None widely available"),
        ],
    ]

    col_widths = [
        CONTENT_WIDTH * 0.32,
        CONTENT_WIDTH * 0.20,
        CONTENT_WIDTH * 0.22,
        CONTENT_WIDTH * 0.26,
    ]
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
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "Constra is built to fill the rightmost column.",
            styles["callout"],
        )
    )
    story.append(PageBreak())

    # -------- Problem & target user --------
    story.append(Paragraph("5. Problem Statement &amp; Target User", styles["h1"]))
    story.append(Paragraph("5.1 The problem", styles["h2"]))
    story.append(
        Paragraph(
            "Engineering projects — foundations, slopes, tunnels, dams, roads, mining "
            "works, environmental sites — generate large quantities of geological and "
            "geophysical data: borehole logs, in-situ tests (CPT, SPT, and others), "
            "near-surface geophysics surveys (refraction, MASW, GPR, ERT), topographic "
            "and bathymetric data, CAD-derived plans, and the engineer's own interpreted "
            "cross-sections. Today this data is handled across a fragmented toolchain — "
            "a CAD package for plans and sections, a plotting tool for graphs, a GIS for "
            "spatial layers, and Excel for tabular records. There is no integrated "
            "workspace, comparable to what oil &amp; gas has in Petrel, that brings "
            "these data into one project, in one coordinate system, with linked Map, "
            "Section, and 3D views.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Constra exists to be that workspace.",
            styles["callout"],
        )
    )

    story.append(Paragraph("5.2 Who Constra is for", styles["h2"]))
    story.append(
        Paragraph(
            "Constra is built specifically for the <b>engineering geologist</b> and the "
            "<b>engineering geophysicist</b> — the practitioner who produces interpreted "
            "geological and geophysical models of the near surface and has to communicate "
            "them to civil designers, contractors, regulators, and clients. The primary "
            "domains of practice are:",
            styles["body"],
        )
    )
    story.extend(
        bullet_list(
            [
                "Geotechnical site investigation.",
                "Civil and construction engineering — foundations, slopes, dams, "
                "tunnels, roads, bridges, embankments.",
                "Mining engineering and exploration that does not fit the oil &amp; gas "
                "paradigm.",
                "Environmental engineering and engineering hydrogeology.",
            ],
            styles,
        )
    )
    story.append(
        Paragraph(
            "The shared characteristic across all four is that the practitioner is "
            "working in real-world coordinates, with multiple data types per project, "
            "producing interpreted outputs (cross-sections, maps, 3D models) that other "
            "engineers and stakeholders consume.",
            styles["body"],
        )
    )

    story.append(Paragraph("5.3 What Constra is not", styles["h2"]))
    story.extend(
        bullet_list(
            [
                "<b>Not a numerical solver.</b> Constra is an interpretation and "
                "visualisation environment — it does not run finite-element analyses, "
                "slope-stability calculations, groundwater flow models, or seismic "
                "processing pipelines. It produces and displays interpreted models that "
                "those tools can consume.",
                "<b>Not (yet) a web application.</b> v0.1 is a desktop application for "
                "Windows. The chosen technology stack does not preclude a future web or "
                "cross-platform release, but neither is committed at v0.1.",
                "<b>Not a multi-user collaboration platform.</b> A single practitioner "
                "working on a single project is the v0.1 case. Multi-user editing, "
                "cloud sync, and shared review are explicitly future work.",
            ],
            styles,
        )
    )
    story.append(PageBreak())

    # -------- Initial release scope --------
    story.append(Paragraph("6. Initial Release Scope (v0.1)", styles["h1"]))
    story.append(
        Paragraph(
            "Constra is meant to be a sophisticated, ambitious tool — the engineering "
            "industry's equivalent of a Petrel-class workspace, not a minimalist "
            "proof-of-concept. The v0.1 scope below is the first coherent release "
            "subset: enough to be genuinely useful on a real engineering project, while "
            "leaving room for everything else to follow.",
            styles["body"],
        )
    )

    story.append(Paragraph("6.1 In scope for v0.1", styles["h2"]))
    story.extend(
        bullet_list(
            [
                "<b>Project container.</b> A Constra project is a folder holding data "
                "sources plus a project-level coordinate reference system (CRS) and "
                "project metadata.",
                "<b>Map View.</b> 2D canvas that renders all datasets in their "
                "real-world projected coordinates, with pan, zoom, and layer visibility "
                "controls. The user can lay out <b>multiple cross-section corridors</b> "
                "(straight or polyline) on the map for use by the Section View.",
                "<b>Section View.</b> Vertical-section workspace supporting <b>multiple "
                "sections open simultaneously</b>, each linked to a corridor defined "
                "on the map. Each section displays the data that intersects its "
                "corridor — boreholes, in-situ test traces, near-surface geophysics "
                "data — in correct relative depth and along-corridor distance.",
                "<b>3D View.</b> A 3D scene rendering all loaded datasets in space, "
                "linked to the same selection model as Map View and Section View.",
                "<b>Engineering data import.</b> Native readers for the data formats "
                "primary to engineering geoscience workflows. The exact format set for "
                "v0.1 is being finalised; current candidates include borehole records "
                "(e.g. AGS), in-situ test data (CPT, SPT), near-surface geophysics "
                "(refraction, MASW, GPR, ERT), DEM/DTM rasters (GeoTIFF, ASCII grid), "
                "vector GIS layers (shapefile, GeoJSON), and CAD plans (DXF). "
                "<b>SEG-Y is not a v0.1 priority</b> — engineering geophysics is "
                "largely non-SEG-Y.",
                "<b>Coordinate system support.</b> Per-project CRS via PROJ (pyproj), "
                "with on-the-fly reprojection of every loaded dataset into the project "
                "frame.",
                "<b>Cross-view selection.</b> Selecting a borehole, station, or feature "
                "in any view highlights it in every other view.",
                "<b>Windows installer.</b> A one-click MSI or exe for Windows 10/11, "
                "produced as a GitHub release artefact.",
            ],
            styles,
        )
    )

    story.append(Paragraph("6.2 Deferred past v0.1", styles["h2"]))
    story.append(
        Paragraph(
            "The list below contains items that fit Constra's industry but are not "
            "scheduled for the first release. Oil &amp; gas-specific features (reservoir "
            "modelling, horizon picking on 3D seismic volumes, SEG-Y attribute "
            "generation) are not on this list — they belong to a different industry and "
            "are simply out of scope.",
            styles["body"],
        )
    )
    story.extend(
        bullet_list(
            [
                "Edit / write-back of imported data files (v0.1 is read-only).",
                "Multi-user collaboration, cloud sync, and shared project review.",
                "Mac and Linux installers (the chosen stack supports them; v0.1 simply "
                "does not commit to producing or supporting them).",
                "Python scripting / plugin API for user extensions.",
                "Web or SaaS deployment.",
                "Automated report generation (PDF / DOCX export of interpreted "
                "sections and maps).",
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
                "<b>Language:</b> Python 3.10+",
                "<b>GUI framework:</b> PySide6 (Qt 6 bindings, LGPL)",
                "<b>3D and scientific visualisation:</b> VTK (the library behind "
                "ParaView and 3D Slicer), optionally via PyVista for ergonomics",
                "<b>Coordinate systems:</b> pyproj (bindings to PROJ)",
                "<b>Raster I/O:</b> rasterio (GeoTIFF, ASCII grid, etc.)",
                "<b>Vector I/O:</b> pyogrio or Fiona for shapefile / GeoJSON; "
                "geopandas for in-memory manipulation",
                "<b>CAD I/O:</b> ezdxf for DXF (a primary engineering interchange " "format)",
                "<b>Engineering-format parsers:</b> selection finalised during M1 "
                "planning — likely python-ags4 for AGS borehole data, plus dedicated "
                "or custom readers for CPT, refraction, MASW, GPR, ERT.",
                "<b>Packaging for Windows:</b> PyInstaller, producing a standalone " "installer",
                "<b>Testing:</b> pytest with pytest-qt for GUI tests",
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
            "3D scene management, coordinate reprojection, vector and CAD interop — "
            "already has a mature, well-maintained Python library. Where engineering-"
            "specific parsers are needed, Python is also the easiest ecosystem to add "
            "them in. Iteration speed matters at this stage, when getting the "
            "interaction model right is more important than micro-optimised performance; "
            "performance-critical components can later be moved to C++ or Rust without "
            "changing the user-facing application.",
            styles["body"],
        )
    )

    story.append(Paragraph("7.3 Platform strategy", styles["h2"]))
    story.append(
        Paragraph(
            "v0.1 targets <b>Windows 10/11</b> only, because that is where engineering "
            "practitioners work day-to-day. Because the chosen stack is cross-platform "
            "by construction, Linux and macOS builds are expected to come essentially "
            "for free once the Windows build is stable — but they are not a v0.1 "
            "commitment.",
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
            "M0 — Project bootstrap (complete)",
            [
                "Public GitHub repository at github.com/atifali-pm/constra, with MIT "
                "licence, README, and .gitignore.",
                "Python project skeleton (pyproject.toml, src/ layout, dev / docs " "extras).",
                "Ruff + black + pytest + pytest-qt configured, plus GitHub Actions "
                "CI on Python 3.10 / 3.11 / 3.12.",
                "Hello-world PySide6 main window that launches and closes cleanly.",
                "Docker development image with X11 forwarding for visual runs on " "Linux hosts.",
            ],
        ),
        (
            "M1 — Project container, CRS, and engineering-format selection",
            [
                "Define the on-disk Constra project format (project folder + " "project.toml).",
                "Implement project create / open / save.",
                "Project-level CRS setting (pick EPSG code at project creation, "
                "stored in the project file).",
                "Wire pyproj for on-the-fly reprojection of any loaded dataset into "
                "the project CRS.",
                "Finalise the v0.1 set of engineering data formats and pick / write "
                "the parsers.",
            ],
        ),
        (
            "M2 — Map View",
            [
                "Build the Map View widget (Qt Graphics View or a VTK 2D render " "window).",
                "Load a DEM / DTM raster (GeoTIFF, ASCII grid) and display it "
                "reprojected into the project CRS.",
                "Load a shapefile / GeoJSON vector layer and overlay it.",
                "Load a CSV of point data (e.g. borehole heads) and plot each point "
                "with a label.",
                "Load a DXF plan via ezdxf and render it as a layer.",
                "Pan / zoom / layer-visibility controls and a layer panel.",
                "Tool to draw <b>multiple cross-section corridors</b> on the map for "
                "use by the Section View.",
            ],
        ),
        (
            "M3 — Section View (multiple sections)",
            [
                "Build the Section View widget supporting <b>multiple sections open "
                "concurrently</b>, one per defined corridor.",
                "For each section, project the data that intersects the corridor "
                "(boreholes, in-situ test traces, near-surface geophysics) into "
                "(distance, depth) coordinates and render it.",
                "Configurable colour map, gain, vertical exaggeration, and depth " "scale.",
                "Link Section View to Map View — selecting a section corridor, "
                "feature, or borehole in one view highlights it in the other.",
            ],
        ),
        (
            "M4 — 3D View",
            [
                "Build the 3D View widget using VTK / PyVista.",
                "Render the basemap, boreholes, near-surface geophysics traces, and "
                "section corridors in 3D space.",
                "Wire cross-view selection so the 3D View shares a selection model "
                "with the Map View and Section View.",
            ],
        ),
        (
            "M5 — Native engineering data and the first installer",
            [
                "Implement the engineering-format parsers chosen in M1 (e.g. AGS "
                "borehole data, CPT/SPT, near-surface geophysics formats).",
                "Display borehole logs alongside the section view.",
                "Package the application for Windows with PyInstaller.",
                "Publish a signed Windows installer as a GitHub release artefact.",
            ],
        ),
    ]

    for title, items in milestones:
        story.append(Paragraph(title, styles["h2"]))
        story.extend(bullet_list(items, styles))

    story.append(Spacer(1, 6 * mm))
    story.append(
        Paragraph(
            "Shipping M5 means Constra v0.1 is a real engineering-geoscience workspace: "
            "project-scoped, coordinate-aware, with linked Map / Section / 3D views and "
            "native readers for the data engineers actually use. It is not a tiny proof "
            "of concept — it is the first usable release of an ambitious tool, and the "
            "foundation everything else is built on.",
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
        subject="Vision document, background, initial release scope, task list",
    )
    story = build_story(styles)
    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
