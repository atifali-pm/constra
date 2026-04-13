"""Constra application entry point.

This is the M0 bootstrap main window: a minimal PySide6 QMainWindow that
launches, displays a placeholder message, and closes cleanly. It exists so
the project skeleton, packaging, tests, and CI can all be proven before any
real geoscience functionality is built on top.
"""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

from constra import __version__

WINDOW_TITLE = f"Constra {__version__}"
PLACEHOLDER_TEXT = (
    "Constra\n\n"
    "Integrated desktop environment for geoscience interpretation.\n\n"
    "This is the M0 bootstrap window.\n"
    "Map View, Section View, and 3D View will land in later milestones."
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(900, 600)

        label = QLabel(PLACEHOLDER_TEXT)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        self.setCentralWidget(label)


def main() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
