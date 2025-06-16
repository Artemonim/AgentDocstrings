from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from agent_docstrings.core import process_file


def test_process_file_inserts_header(tmp_path: Path) -> None:
    """Ensures :pyfunc:`process_file` adds a header to a Python source file."""
    file_content = dedent(
        """
        class Greeter:
            def hello(self, name):
                print(f"Hello, {name}!")
        """
    ).lstrip()

    src_file = tmp_path / "greet.py"
    src_file.write_text(file_content, encoding="utf-8")

    # * Execute processing.
    process_file(src_file, verbose=False)

    new_content = src_file.read_text(encoding="utf-8")
    assert new_content.startswith('"""')  # * The generated docstring should be at the top.
    assert "Greeter" in new_content 