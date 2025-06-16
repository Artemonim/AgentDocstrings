from __future__ import annotations

import sys
from pathlib import Path

import pytest

import agent_docstrings.cli as cli


def test_cli_processes_directory(sample_python_file: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """Ensures the CLI finishes without errors when given a valid directory."""
    # * Override *sys.argv* so that ``cli.main`` believes it is executed via the
    # * console entry-point. The first element is conventionally the program
    # * name.
    monkeypatch.setattr(sys, "argv", ["agent-docstrings", str(sample_python_file.parent)])

    # * ``cli.main`` normally calls :pyfunc:`sys.exit` on failure. If an
    # * unexpected *SystemExit* is raised, the test will fail automatically.
    cli.main()

    captured = capsys.readouterr()
    # * The program prints *"Done."* upon successful completion.
    assert "Done." in captured.out 