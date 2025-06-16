"""Shared pytest configuration and fixtures for Agent Docstrings tests."""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Iterator

import pytest


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """Returns the absolute path to the *fixtures* directory used in tests."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture()
def sample_python_file(tmp_path: Path) -> Iterator[Path]:
    """Creates a simple temporary Python file and yields its path.

    The temporary file is removed automatically when the test finishes.
    """
    code = textwrap.dedent(
        """
        class Foo:
            def bar(self, x):
                return x

        def baz(y):
            return y * 2
        """
    ).lstrip()

    file_path = tmp_path / "sample.py"
    file_path.write_text(code, encoding="utf-8")
    yield file_path 