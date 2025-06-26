from __future__ import annotations
import re
from typing import List

from .common import ClassInfo, SignatureInfo

# Regexes are intentionally kept simple to capture common cases.
# They may not capture all edge cases of the language syntax.
CSHARP_CLASS_RE = re.compile(
    r"^\s*(?:public|private|protected|internal|sealed|static|partial|abstract)?\s*class\s+(\w+)"
)
CSHARP_METHOD_RE = re.compile(
    r"^\s*(?:public|private|protected|internal|static|async|override|virtual|sealed|partial)\s+[\w<>\[\],]+\s+(\w+)\s*\(([^)]*)\)"
)

JS_CLASS_RE = re.compile(r"^\s*(?:export\s+)?class\s+(\w+)")
JS_FUNC_RE = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)")

CPP_CLASS_RE = re.compile(r"^\s*class\s+(\w+)")
# This is a simplified regex for C++ methods and functions.
# It won't handle complex templates or return types perfectly.
CPP_FUNC_RE = re.compile(r"^\s*(?:virtual\s|inline\s|static\s)?[\w:<>~,*\s]+\s+([\w:]+)\(([^)]*)\)\s*(?:const)?\s*(?:=\s*0)?\s*[;{]")


def parse_generic_file(
    lines: List[str],
    lang: str,
) -> tuple[List[ClassInfo], List[SignatureInfo]]:
    """Parse *lines* and extract structural information for a C-style language.

    Args:
        lines (List[str]): Source code split into individual lines.
        lang (str): Canonical language identifier. Supported values are
            ``"javascript"``, ``"typescript"``, ``"csharp"`` and ``"cpp"``.

    Returns:
        Tuple[List[ClassInfo], List[SignatureInfo]]: Two parallel
        collections where the first element contains a potentially nested
        class hierarchy and the second lists top-level functions.
    """
    if lang in ("javascript", "typescript"):
        class_re, func_re = JS_CLASS_RE, JS_FUNC_RE
    elif lang == "csharp":
        class_re, func_re = CSHARP_CLASS_RE, CSHARP_METHOD_RE
    elif lang == "cpp":
        class_re, func_re = CPP_CLASS_RE, CPP_FUNC_RE
    else:
        return [], []

    classes: List[ClassInfo] = []
    top_level_funcs: List[SignatureInfo] = []
    class_stack: List[ClassInfo] = []
    brace_balance: int = 0
    brace_stack: List[int] = []

    for line_num, line in enumerate(lines, 1):
        stripped_line = line.strip()
        if not stripped_line:
            continue

        # Store balance before this line is processed
        pre_line_brace_balance = brace_balance

        # Very basic brace counting to track class scope.
        open_braces = line.count("{")
        close_braces = line.count("}")
        brace_balance += open_braces - close_braces

        if class_stack and brace_balance > 0:
            if brace_balance == brace_stack[-1]:
                # Exiting a class scope
                if open_braces == 0 and close_braces > 0:
                    brace_balance -= close_braces
                    if brace_balance < brace_stack[-1]:
                       class_stack.pop()
                       brace_stack.pop()
                    continue

        class_match = class_re.match(line)
        if class_match:
            class_name = class_match.group(1)
            new_class = ClassInfo(name=class_name, line=line_num, methods=[], inner_classes=[])
            if class_stack:
                class_stack[-1].inner_classes.append(new_class)
            else:
                classes.append(new_class)
            class_stack.append(new_class)
            if "{" in line:
                brace_stack.append(brace_balance)
            continue

        # Only look for functions at the top-level (not inside another block)
        if pre_line_brace_balance == 0:
            func_match = func_re.match(line)
            if func_match:
                # Simplified signature extraction
                signature = stripped_line.split("{")[0].strip()
                info = SignatureInfo(signature=signature, line=line_num)
                if class_stack:
                    # This is a very rough approximation and might misclassify methods
                    # as belonging to outer classes in complex nested scenarios.
                    class_stack[-1].methods.append(info)
                else:
                    top_level_funcs.append(info)

    return classes, top_level_funcs 