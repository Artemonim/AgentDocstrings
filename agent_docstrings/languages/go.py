from __future__ import annotations
import re
from typing import List, Tuple

from .common import ClassInfo, SignatureInfo

# Go doesn't have classes. It has structs and methods on structs.
# This simplified parser will only look for top-level functions.
# e.g., func FunctionName(arg type) retType {
# e.g., func (s *MyStruct) MethodName(arg type) retType {
GO_FUNC_RE = re.compile(
    r"^\s*func(?:\s+\([^)]+\))?\s+(\w+)\s*\(([^)]*)\)"
)


def parse_go_file(
    lines: List[str],
) -> tuple[List[ClassInfo], List[SignatureInfo]]:
    """Parse *lines* and extract structural information for a Go file.

    This is a simplified parser focusing on top-level functions. It
    does not attempt to parse structs or interfaces.

    Args:
        lines (List[str]): Source code split into individual lines.

    Returns:
        Tuple[List[ClassInfo], List[SignatureInfo]]: Top-level functions.
        Classes will always be an empty list for Go.
    """
    classes: List[ClassInfo] = []  # Go doesn't have classes
    top_level_funcs: List[SignatureInfo] = []

    for line_num, line in enumerate(lines, 1):
        stripped_line = line.strip()
        if not stripped_line:
            continue

        func_match = GO_FUNC_RE.match(line)
        if func_match:
            signature = stripped_line.split("{")[0].strip()
            info = SignatureInfo(signature=signature, line=line_num)
            top_level_funcs.append(info)

    return classes, top_level_funcs 