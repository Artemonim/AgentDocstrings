"""
    Classes/Functions:
    - SignatureInfo (line 15):
    - ClassInfo (line 21):
    - CommentStyle (line 29):
      - Functions:
        - strip_existing_header(text: str, language: str) -> str (line 46)
"""
from __future__ import annotations

import re
from typing import List, Tuple, Dict, NamedTuple


class SignatureInfo(NamedTuple):
    """Stores information about a parsed function or method signature."""
    signature: str
    line: int


class ClassInfo(NamedTuple):
    """Stores information about a parsed class, including its methods."""
    name: str
    line: int
    methods: List[SignatureInfo]
    inner_classes: List["ClassInfo"]


class CommentStyle(NamedTuple):
    """Stores language-specific comment delimiters and formatting."""
    start: str
    end: str
    prefix: str  # e.g., ' * ' or '    '


COMMENT_STYLES: Dict[str, CommentStyle] = {
    "python": CommentStyle('"""', '"""', "    "),
    "kotlin": CommentStyle('/**', ' */', ' * '),
    "javascript": CommentStyle('/**', ' */', ' * '),
    "typescript": CommentStyle('/**', ' */', ' * '),
    "csharp": CommentStyle('/*', ' */', ' * '),
    "cpp": CommentStyle('/*', ' */', ' * '),
    "c": CommentStyle('/*', ' */', ' * '),
    "java": CommentStyle('/**', ' */', ' * '),
    "go": CommentStyle('/*', ' */', ' * '),
    "powershell": CommentStyle('<#', '#>', ' # '),
    "delphi": CommentStyle('(*', '*)', ' * '),
}


def strip_existing_header(text: str, language: str) -> str:
    """Remove a previously generated header from *text*.

    The search is intentionally limited to the very beginning of the file
    because *agent-docstrings* always inserts the header at the top.  A
    language-specific regular expression is used to locate and strip the
    first comment block that contains the marker string
    ``Classes/Functions:``.

    Args:
        text (str): Full contents of the source file.
        language (str): Canonical language name (e.g. ``"python"``) used
            to pick the correct comment delimiters from
            :data:`COMMENT_STYLES`.

    Returns:
        str: *text* without the existing header block. If no header is
        detected, *text* is returned unchanged.
    """
    style = COMMENT_STYLES[language]
    # For Python, the docstring is very specifically at the top.
    # For others, it's a block comment that could be anywhere, but we only care about the first one.
    if language == "python":
        pattern = rf'(?s)^"""[^\S\r\n]*Classes/Functions:.*?^"""[^\S\r\n]*\r?\n?'
    else:
        # Match /* or /** followed by a space and Classes/Functions:.
        pattern = rf'(?s)^{re.escape(style.start)}[^\S\r\n]*Classes/Functions:.*?{re.escape(style.end)}[^\S\r\n]*\r?\n?'
    return re.sub(pattern, "", text, count=1, flags=re.MULTILINE) 