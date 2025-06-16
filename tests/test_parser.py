from __future__ import annotations

from textwrap import dedent

import pytest

from agent_docstrings.languages.python import parse_python_file
from agent_docstrings.languages.common import ClassInfo, SignatureInfo


@pytest.mark.parametrize(
    "source, expected_classes, expected_funcs",
    [
        (
            dedent(
                """
                class Foo:
                    def bar(self, x):
                        return x

                def baz(y):
                    return y
                """
            ),
            [
                ClassInfo(
                    name="Foo",
                    line=1,
                    methods=[SignatureInfo(signature="bar(x)", line=2)],
                    inner_classes=[],
                )
            ],
            [SignatureInfo(signature="baz(y)", line=5)],
        ),
    ],
)

def test_parse_python_file(source: str, expected_classes: list[ClassInfo], expected_funcs: list[SignatureInfo]) -> None:
    """Verifies that *parse_python_file* extracts classes and functions correctly."""
    classes, funcs = parse_python_file(source.splitlines())

    # * Compare structural information without caring about exact object identity.
    assert classes == expected_classes
    assert funcs == expected_funcs 