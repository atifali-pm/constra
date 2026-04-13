"""Smoke tests for the M0 bootstrap main window."""

from __future__ import annotations

from constra import __version__
from constra.app import MainWindow


def test_main_window_title(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert __version__ in window.windowTitle()
    assert window.windowTitle().startswith("Constra")


def test_main_window_has_central_widget(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.centralWidget() is not None


def test_main_window_shows_and_hides(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    qtbot.waitExposed(window)
    assert window.isVisible()
    window.close()
    assert not window.isVisible()
