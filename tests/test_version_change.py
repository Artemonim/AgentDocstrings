"""
Tests to ensure that files are not reprocessed when only the version has changed.
"""
import shutil
from pathlib import Path

from agent_docstrings.core import process_file
from agent_docstrings import __version__


def test_no_change_on_version_mismatch(tmp_path: Path):
    """
    Verify that reprocessing a file with only a version difference
    in the docstring does not result in a file modification.
    """
    # 1. Create a temporary python file
    source_content = (
        "def func_one():\n"
        "    pass\n"
        "\n"
        "class MyClass:\n"
        "    def method_one(self):\n"
        "        pass\n"
    )
    py_file = tmp_path / "test_version.py"
    py_file.write_text(source_content, encoding="utf-8")

    # 2. Process it once to generate the initial docstring
    process_file(py_file)
    content_after_first_run = py_file.read_text(encoding="utf-8")
    assert __version__ in content_after_first_run

    # 3. Manually change the version in the header to an old one
    old_version_content = content_after_first_run.replace(
        f"v{__version__}", "v0.0.1"
    )
    py_file.write_text(old_version_content, encoding="utf-8")

    # 4. Process the file again
    process_file(py_file)
    content_after_second_run = py_file.read_text(encoding="utf-8")

    # 5. Assert the file content has NOT changed
    assert content_after_second_run == old_version_content
    assert f"v{__version__}" not in content_after_second_run
    assert "v0.0.1" in content_after_second_run

    # 6. Now, modify the structure of the file
    new_source_content = (
        source_content + "\n\ndef func_two():\n    pass\n"
    )

    # Add the old docstring back to simulate a real-world scenario
    # where an old file is being updated.
    # Get the docstring from the first run, but with the old version
    docstring_end_index = content_after_first_run.rfind('"""') + 3
    docstring_from_first_run = content_after_first_run[:docstring_end_index]

    old_version_docstring = docstring_from_first_run.replace(f"v{__version__}", "v0.0.1")

    # Combine the old docstring with the NEW code
    content_with_new_code_old_doc = old_version_docstring + "\n" + new_source_content
    py_file.write_text(content_with_new_code_old_doc, encoding="utf-8")

    # 7. Process it again
    process_file(py_file)
    content_after_third_run = py_file.read_text(encoding="utf-8")

    # 8. Assert the file HAS been updated with the new structure and version
    assert content_after_third_run != content_with_new_code_old_doc
    assert f"v{__version__}" in content_after_third_run
    assert "v0.0.1" not in content_after_third_run
    assert "func_two" in content_after_third_run 