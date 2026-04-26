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
            "Constra: Vision and Initial Scope",
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
            "Geoscience software for engineers",
            styles["cover_subtitle"],
        )
    )
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph("Vision and Initial Scope", styles["cover_subtitle"]))
    story.append(Spacer(1, 4 * cm))
    story.append(
        Paragraph(
            f"Draft v0.3 &middot; {date.today().isoformat()}<br/>"
            "Working name: <b>Constra</b> (subject to change)",
            styles["cover_meta"],
        )
    )
    story.append(PageBreak())

    # -------- Executive Summary --------
    story.append(Paragraph("1. Executive Summary", styles["h1"]))
    story.append(
        Paragraph(
            "Constra is desktop software for engineering geologists and engineering "
            "geophysicists. It pulls together the data an engineering project actually "
            "runs on (boreholes, in-situ tests, surface geophysics, topography, CAD "
            "plans) into one project file, in one coordinate system. Map, section, "
            "and 3D views all read from the same data, so the well or the section "
            "the user picks in one view is the same well or section in the other two.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Oil and gas has had this kind of software for decades. Petrel, by "
            "Schlumberger, is the obvious example, and it does its job well. "
            "Engineering has nothing comparable. Engineering geologists draw "
            "cross-sections in CAD, plot logs in Surfer or Excel, manage spatial "
            "layers in a separate GIS package, and keep tabular records in "
            "spreadsheets. Pieces drift out of sync. Figures stop matching the data "
            "they came from. Constra is built to replace that fragmented stack with "
            "one project.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Petrel and Surfer appear in this document as reference points, not as "
            "rivals. Petrel shows what an integrated workspace can do for the "
            "geologist who uses it every day. Surfer shows where the ceiling sits "
            "for tools that only plot. Constra is for a different industry, one "
            "that today has neither.",
            styles["body"],
        )
    )
    story.append(PageBreak())

    # -------- Background: Petrel --------
    story.append(Paragraph("2. Reference Point: Petrel", styles["h1"]))
    story.append(
        Paragraph(
            "Petrel is Schlumberger's interpretation platform for the oil and gas "
            "industry. Inside that industry it is the standard tool, and it works "
            "well. It is reproduced here for one reason: it shows what an "
            "integrated workspace can do for the geologist who lives inside it. "
            "Engineering needs something with the same shape, just built around "
            "engineering data.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Petrel handles seismic data, well logs, geological surfaces, and "
            "reservoir models in one project. The user works in 2D maps, vertical "
            "sections, and 3D scenes, and everything stays in sync. Click a well "
            "in the map and the same well lights up in the section and the 3D scene.",
            styles["body"],
        )
    )

    story.append(Paragraph("2.1 Map View", styles["h2"]))
    story.append(
        Paragraph(
            "The Map View shows everything in its real-world location. Satellite "
            "imagery, seismic line tracks, well heads, and cultural features (roads, "
            "buildings) layer up in the same window.",
            styles["body"],
        )
    )
    story.append(
        figure(
            os.path.join(IMAGES_DIR, "01-petrel-map-view-satellite.png"),
            "Figure 1. Satellite basemap in Petrel's Map View. The image of the "
            "project area sits at the bottom of the layer stack and gives every "
            "other layer its geographic context.",
            styles,
        )
    )
    story.append(
        figure(
            os.path.join(IMAGES_DIR, "02-petrel-map-seismic-wells.png"),
            "Figure 2. Seismic lines and well locations on the same map. The "
            "interpreter can see which line passes nearest to which well and open "
            "that line directly from the map.",
            styles,
        )
    )

    story.append(Paragraph("2.2 Section View", styles["h2"]))
    story.append(
        Paragraph(
            "The Section View is for data that lives on a vertical slice through "
            "the ground: 2D seismic lines, well logs, horizons, and faults. Click "
            "a line on the map and it opens here as a vertical section, ready to "
            "interpret.",
            styles["body"],
        )
    )
    story.append(
        figure(
            os.path.join(IMAGES_DIR, "03-petrel-section-view-seismic.png"),
            "Figure 3. A 2D seismic line displayed as a vertical section in Petrel.",
            styles,
        )
    )
    story.append(
        Paragraph(
            "<b>Map View and Section View are linked.</b> Pick a horizon in the "
            "section and the same pick shows up on the map. Move a crosshair on the "
            "map and the section follows. The same is true for every other data "
            "type in the project.",
            styles["callout"],
        )
    )

    story.append(Paragraph("2.3 3D View", styles["h2"]))
    story.append(
        Paragraph(
            "The 3D View shows the same data in three dimensions. It is linked to "
            "the Map and Section views, so a selection made anywhere appears in all "
            "three.",
            styles["body"],
        )
    )
    story.append(
        figure(
            os.path.join(IMAGES_DIR, "04-petrel-3d-seismic-lines.png"),
            "Figure 4. Several 2D seismic lines drawn together in 3D. The "
            "geologist sees how the subsurface looks along the different "
            "acquisition directions at once.",
            styles,
        )
    )
    story.append(
        figure(
            os.path.join(IMAGES_DIR, "05-petrel-3d-reservoir-well.png"),
            "Figure 5. A reservoir model in 3D with a well trajectory through it. "
            "The well path against the body is visible at a glance.",
            styles,
        )
    )

    story.append(Paragraph("2.4 Coordinate System", styles["h2"]))
    story.append(
        Paragraph(
            "Petrel works in real-world coordinates: latitude/longitude or "
            "Easting/Northing. Reprojection is handled by the software, not by the "
            "user. Two datasets in different systems land in the right place "
            "without manual intervention. This is what makes the cross-view "
            "interactivity actually useful: the well in the map is the same well "
            "in the section and the same well in 3D, because all three views read "
            "from the same coordinate frame. Constra needs the same property for "
            "engineering data.",
            styles["body"],
        )
    )
    story.append(PageBreak())

    # -------- Background: Surfer --------
    story.append(Paragraph("3. Reference Point: Surfer", styles["h1"]))
    story.append(
        Paragraph(
            "Surfer (Golden Software) is a plotting and contouring package widely "
            "used in geoscience. It is included here as a different sort of "
            "reference. Petrel shows what a workspace can be. Surfer shows what "
            "plotting tools cannot do for someone who needs more than a finished "
            "figure. Surfer is good at what it does. It just is not a workspace, "
            "and a workspace is what engineering needs.",
            styles["body"],
        )
    )

    story.append(Paragraph("3.1 No dedicated views", styles["h2"]))
    story.append(
        Paragraph(
            "Surfer does not have separate Map, Section, and 3D views that share "
            "state. Maps and sections both end up in the same generic plot window. "
            "There is no shared canvas, no automatic basemap, no cross-view "
            "synchronisation. Every figure is built by hand, and every figure is "
            "its own thing.",
            styles["body"],
        )
    )

    story.append(Paragraph("3.2 No project-level coordinate frame", styles["h2"]))
    story.append(
        Paragraph(
            "Surfer does not put every dataset into a shared coordinate system. It "
            "plots data against whatever values are in the file, and it is up to "
            "the user to make sure those values agree across files. If two datasets "
            "are in different coordinate systems, the user notices that, not the "
            "software.",
            styles["body"],
        )
    )

    story.append(Paragraph("3.3 Manual workflow", styles["h2"]))
    story.append(
        Paragraph(
            "Every layer, every object, every label has to be added by hand. That "
            "is fine for a one-off figure. It is not fine when many datasets have "
            "to stay consistent, when the underlying data changes regularly, or "
            "when the interpreter needs to switch between map, section, and 3D in "
            "the course of a working day.",
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
            "The two products above are reference points, not rivals. The oil and "
            "gas industry has its workspace. Everyone, engineers included, has "
            "plotting tools. Engineering itself has no equivalent of either kind. "
            "The table below shows where each capability stands, in each industry, "
            "today.",
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
            cell("<b>Petrel<br/>(oil and gas)</b>"),
            cell("<b>Surfer<br/>(generic plotting)</b>"),
            cell("<b>Engineering<br/>geoscience today</b>"),
        ],
        [
            cell("Industry-specific integrated workspace"),
            cell("Yes"),
            cell("n/a"),
            cell("Nothing widely available"),
        ],
        [
            cell("Single project, shared coordinate frame"),
            cell("Yes"),
            cell("No"),
            cell("Nothing widely available"),
        ],
        [
            cell("Real-world coordinates, automatic reprojection"),
            cell("Yes"),
            cell("No"),
            cell("Handled per tool, per file"),
        ],
        [
            cell("Linked Map, Section, and 3D views"),
            cell("Yes"),
            cell("No"),
            cell("Nothing widely available"),
        ],
        [
            cell("Multiple simultaneous cross-sections"),
            cell("Yes"),
            cell("No"),
            cell("Manual in CAD"),
        ],
        [
            cell("Native readers for the industry's primary data"),
            cell("Yes (oil and gas formats)"),
            cell("n/a"),
            cell("Fragmented across single-purpose tools"),
        ],
        [
            cell("Cross-view selection"),
            cell("Yes"),
            cell("No"),
            cell("Nothing widely available"),
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
            "Constra is the rightmost column.",
            styles["callout"],
        )
    )
    story.append(PageBreak())

    # -------- Problem & target user --------
    story.append(Paragraph("5. The Problem and Who Constra Is For", styles["h1"]))
    story.append(Paragraph("5.1 The problem", styles["h2"]))
    story.append(
        Paragraph(
            "An engineering project (a tunnel, a dam, a road cutting, a foundation, "
            "a slope) generates a lot of geological and geophysical data. "
            "Boreholes. In-situ tests like CPT and SPT. Surface geophysics: "
            "refraction, MASW, GPR, ERT. Topographic and bathymetric surveys. CAD "
            "plans. The engineer's own interpreted cross-sections.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Today that data is spread across separate tools. CAD for plans and "
            "sections. Surfer or similar for graphs. A GIS package for spatial "
            "layers. Excel for the tabular records that hold everything else. "
            "Nothing pulls these into one project the way Petrel does in oil and "
            "gas, and nothing keeps them in one coordinate system with linked map, "
            "section, and 3D views.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Constra exists to be that one thing.",
            styles["callout"],
        )
    )

    story.append(Paragraph("5.2 Who Constra is for", styles["h2"]))
    story.append(
        Paragraph(
            "Constra is for the engineering geologist and the engineering "
            "geophysicist. The practitioner who interprets the near surface and "
            "then has to communicate that interpretation to civil designers, "
            "contractors, regulators, and clients. The fields of practice this "
            "covers:",
            styles["body"],
        )
    )
    story.extend(
        bullet_list(
            [
                "Geotechnical site investigation.",
                "Civil and construction engineering: foundations, slopes, dams, "
                "tunnels, roads, bridges, embankments.",
                "Mining engineering and exploration outside oil and gas.",
                "Environmental engineering and engineering hydrogeology.",
            ],
            styles,
        )
    )
    story.append(
        Paragraph(
            "What ties these together: the practitioner works in real-world "
            "coordinates, has several data types in every project, and has to "
            "produce interpreted outputs (cross-sections, maps, 3D models) that "
            "other people use to make engineering decisions.",
            styles["body"],
        )
    )

    story.append(Paragraph("5.3 What Constra is not", styles["h2"]))
    story.extend(
        bullet_list(
            [
                "<b>Not a numerical solver.</b> Constra interprets and visualises. "
                "It does not run finite-element analyses, slope-stability "
                "calculations, groundwater models, or seismic processing pipelines. "
                "It produces interpreted outputs that those tools can read in.",
                "<b>Not a web app, at least not yet.</b> v0.1 is a Windows desktop "
                "application. The stack we picked could go elsewhere later, but "
                "the first release does not promise that.",
                "<b>Not a collaboration platform.</b> v0.1 is one practitioner "
                "working on one project at a time. Multi-user editing, cloud sync, "
                "and shared review come later.",
            ],
            styles,
        )
    )
    story.append(PageBreak())

    # -------- Initial release scope --------
    story.append(Paragraph("6. Initial Release Scope (v0.1)", styles["h1"]))
    story.append(
        Paragraph(
            "Constra is meant to be a real working tool, not a stripped-down proof "
            "of concept. The v0.1 scope below is what the first release has to do "
            "to be useful on an actual engineering project. Everything else can "
            "wait.",
            styles["body"],
        )
    )

    story.append(Paragraph("6.1 In scope for v0.1", styles["h2"]))
    story.extend(
        bullet_list(
            [
                "<b>A project.</b> A Constra project is a folder. Inside it: the "
                "project's data sources, its coordinate reference system, and a "
                "small metadata file.",
                "<b>Map View.</b> A 2D canvas drawing every dataset at its real "
                "location. Pan, zoom, layers on or off. The user draws "
                "cross-section corridors here (straight lines or polylines) for "
                "the Section View to follow.",
                "<b>Section View.</b> Vertical sections, several open at once, "
                "one per corridor on the map. Each section shows whatever data "
                "the corridor crosses (boreholes, in-situ test traces, surface "
                "geophysics) at the right depth and at the right distance along "
                "the line.",
                "<b>3D View.</b> The same data in 3D. Linked to the Map and "
                "Section views by a shared selection.",
                "<b>Data import.</b> Built-in readers for the formats engineering "
                "teams actually use. The final v0.1 list is still being decided. "
                "Current candidates: borehole records (AGS), in-situ tests (CPT, "
                "SPT), surface geophysics (refraction, MASW, GPR, ERT), DEM and "
                "DTM rasters (GeoTIFF, ASCII grid), GIS layers (shapefile, "
                "GeoJSON), CAD plans (DXF). SEG-Y is not on the list. Engineering "
                "geophysics is mostly not SEG-Y.",
                "<b>Coordinates.</b> Each project has one CRS, set when the "
                "project is created. Anything loaded into the project gets "
                "reprojected into that CRS by PROJ.",
                "<b>Cross-view selection.</b> Click a borehole, a station, or a "
                "feature in any view, and the same thing lights up in the other "
                "two.",
                "<b>Windows installer.</b> One MSI or exe for Windows 10/11, "
                "published on GitHub Releases.",
            ],
            styles,
        )
    )

    story.append(Paragraph("6.2 Deferred past v0.1", styles["h2"]))
    story.append(
        Paragraph(
            "The list below is what fits the engineering use case but is not in "
            "the first release. Things that belong to oil and gas (reservoir "
            "modelling, horizon picking on 3D seismic, SEG-Y attribute generation) "
            "are not deferred. They are simply not in scope.",
            styles["body"],
        )
    )
    story.extend(
        bullet_list(
            [
                "Editing or writing back to source files. v0.1 only reads.",
                "Multiple users on one project. Cloud sync. Shared review.",
                "Mac and Linux installers. The stack supports both, but v0.1 "
                "will not produce or support them.",
                "A Python scripting or plugin API.",
                "Web or SaaS deployment.",
                "Automatic report generation (PDF or DOCX export of interpreted "
                "sections and maps).",
            ],
            styles,
        )
    )
    story.append(PageBreak())

    # -------- Tech stack --------
    story.append(Paragraph("7. Technology Choice", styles["h1"]))
    story.append(Paragraph("7.1 Stack", styles["h2"]))
    story.extend(
        bullet_list(
            [
                "<b>Language:</b> Python 3.10 or newer.",
                "<b>GUI:</b> PySide6 (Qt 6).",
                "<b>3D and visualisation:</b> VTK, optionally through PyVista.",
                "<b>Coordinate systems:</b> pyproj, the Python binding for PROJ.",
                "<b>Raster I/O:</b> rasterio, for GeoTIFF and ASCII grid.",
                "<b>Vector I/O:</b> pyogrio or Fiona for shapefile and GeoJSON; "
                "geopandas for in-memory work.",
                "<b>CAD:</b> ezdxf for DXF.",
                "<b>Engineering parsers:</b> chosen during M1. Likely python-ags4 "
                "for AGS borehole data, plus dedicated or custom readers for CPT, "
                "refraction, MASW, GPR, ERT.",
                "<b>Windows packaging:</b> PyInstaller.",
                "<b>Tests:</b> pytest with pytest-qt.",
                "<b>Lint and format:</b> ruff, black.",
            ],
            styles,
        )
    )

    story.append(Paragraph("7.2 Why this stack", styles["h2"]))
    story.append(
        Paragraph(
            "Python with Qt and VTK is what ParaView and 3D Slicer are built on. "
            "Both are successful scientific visualisation applications, and both "
            "are open source. The hard parts of Constra's roadmap (large raster "
            "display, 3D scene management, coordinate reprojection, vector and "
            "CAD interop) all have established Python libraries.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Engineering-specific parsers, where they need to be written, are "
            "easier to write in Python than in anything else. Speed of iteration "
            "matters more right now than raw performance: getting the interaction "
            "model right is harder than making it fast. If a piece of the "
            "application later turns out to be a bottleneck, that piece can be "
            "rewritten in C++ or Rust without changing the rest.",
            styles["body"],
        )
    )

    story.append(Paragraph("7.3 Platform", styles["h2"]))
    story.append(
        Paragraph(
            "v0.1 ships on Windows 10 and 11, because that is where engineering "
            "practitioners work. The stack itself is cross-platform, so Linux and "
            "macOS builds should be straightforward once the Windows build is "
            "solid. Neither is committed for v0.1.",
            styles["body"],
        )
    )
    story.append(PageBreak())

    # -------- Initial tasks --------
    story.append(Paragraph("8. Roadmap", styles["h1"]))
    story.append(
        Paragraph(
            "Work is organised into milestones. Each milestone ends in a runnable "
            "application that does a little more than the one before it.",
            styles["body"],
        )
    )

    milestones = [
        (
            "M0: Project bootstrap (complete)",
            [
                "Public GitHub repo at github.com/atifali-pm/constra. MIT licence, "
                "README, and .gitignore in place.",
                "Python project skeleton: pyproject.toml, src layout, dev and docs " "extras.",
                "Ruff, black, pytest, and pytest-qt configured. GitHub Actions CI "
                "runs them on Python 3.10, 3.11, and 3.12.",
                "A PySide6 main window that launches, displays a placeholder, and "
                "closes cleanly.",
                "Docker development image with X11 forwarding so the app can be "
                "run visually on a Linux host.",
            ],
        ),
        (
            "M1: Project container, CRS, and engineering-format selection",
            [
                "Define the on-disk project format: a folder plus a project.toml.",
                "Implement project create, open, save.",
                "Per-project CRS, set at project creation by EPSG code, stored in "
                "the project file.",
                "Wire pyproj so any loaded dataset is reprojected into the project "
                "CRS on the way in.",
                "Decide the v0.1 list of engineering data formats. Pick or write "
                "the parser for each.",
            ],
        ),
        (
            "M2: Map View",
            [
                "Build the Map View widget (Qt Graphics View, or VTK in 2D mode).",
                "Load a DEM or DTM raster (GeoTIFF, ASCII grid) and draw it in " "the project CRS.",
                "Load a shapefile or GeoJSON vector layer.",
                "Load a CSV of point data, for example borehole heads, and label " "each point.",
                "Load a DXF plan via ezdxf and render it as a layer.",
                "Pan, zoom, layer visibility, and a side panel listing the layers.",
                "A tool that draws cross-section corridors (straight or polyline) "
                "on the map. The Section View will follow these corridors in M3.",
            ],
        ),
        (
            "M3: Section View (multiple sections)",
            [
                "Build the Section View widget. Several sections can be open at "
                "once, one per corridor.",
                "For each section, project the data the corridor crosses "
                "(boreholes, in-situ test traces, surface geophysics) into "
                "(distance, depth) and render it.",
                "Configurable colour map, gain, vertical exaggeration, and depth " "scale.",
                "Link Section View to Map View. Selecting a corridor, a feature, "
                "or a borehole in one view highlights it in the other.",
            ],
        ),
        (
            "M4: 3D View",
            [
                "Build the 3D View widget on VTK or PyVista.",
                "Render the basemap, boreholes, surface geophysics traces, and "
                "section corridors in 3D.",
                "Make the 3D View share the same selection model as the Map View "
                "and the Section View.",
            ],
        ),
        (
            "M5: Native engineering data and the first installer",
            [
                "Implement the engineering-format parsers picked in M1: AGS "
                "borehole data, CPT/SPT, surface geophysics formats.",
                "Display borehole logs next to the section view.",
                "Package the application for Windows with PyInstaller.",
                "Publish a signed Windows installer to GitHub Releases.",
            ],
        ),
    ]

    for title, items in milestones:
        story.append(Paragraph(title, styles["h2"]))
        story.extend(bullet_list(items, styles))

    story.append(Spacer(1, 6 * mm))
    story.append(
        Paragraph(
            "When M5 ships, Constra v0.1 is a real workspace: one project, one "
            "coordinate system, linked Map, Section, and 3D views, and built-in "
            "readers for the data engineers actually use. It is the first usable "
            "release of the project, and what every later release is built on.",
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
        title="Constra: Vision and Initial Scope",
        author="Constra project",
        subject="Vision document, reference points, initial release scope, roadmap",
    )
    story = build_story(styles)
    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
