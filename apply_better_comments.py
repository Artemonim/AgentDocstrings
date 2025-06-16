"""A script that inserts or refreshes file-level headers summarizing classes and functions for multiple languages.

Supported languages/extensions and comment styles:
  - Python  (.py)   → module docstring (triple quotes)
  - Kotlin  (.kt)   → KDoc block comment
  - JavaScript (.js, .jsx) → JSDoc block comment
  - TypeScript (.ts, .tsx) → TSDoc block comment (same as JSDoc)
  - C#      (.cs)   → C-style block comment (/* */)
  - C++     (.cpp, .hpp, .h, .cc, .cxx) → C-style block comment (/* */)

Typical usage:
    $ python apply_better_comments.py path1 path2 ...
If no paths are supplied, the current working directory is scanned recursively.

The script is intentionally dependency-free (only stdlib) to simplify
symlink-based reuse across projects.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict


# region ────────────────────────────────────── Helpers
class _ClassNode:
    """Represents a class and its nested structure."""

    def __init__(self, name: str, line: int) -> None:
        self.name: str = name
        self.line: int = line
        self.methods: List[Tuple[str, int]] = []  # (signature, line)
        self.inner: List["_ClassNode"] = []

    def dump(self, dst: List[str], indent: int = 1) -> None:
        prefix = " " * indent
        dst.append(f" *{prefix}- {self.name} (line {self.line}):")
        for sig, ln in self.methods:
            dst.append(f" *{prefix}  - {sig} (line {ln})")
        for child in self.inner:
            child.dump(dst, indent + 2)


# endregion


# region ────────────────────────────────────── Language specific builders
PY_CLASS_RE = re.compile(r"^class\s+(\w+)")
PY_FUNC_RE = re.compile(r"^(\s*)def\s+(\w+)\(([^)]*)\)(?:\s*->\s*([^:]+))?:")

CSHARP_CLASS_RE = re.compile(r"^\s*(?:public|private|protected|internal|sealed|static|partial|abstract)?\s*class\s+(\w+)")
CSHARP_METHOD_RE = re.compile(
    r"^\s*(?:public|private|protected|internal|static|async|override|virtual|sealed|partial)\s+([\w<>\[\],]+)\s+(\w+)\s*\(([^)]*)\)")

KOTLIN_CLASS_RE = re.compile(r"^\s*(?:public|protected|private|internal)?\s*class\s+(\w+)")
KOTLIN_FUN_RE = re.compile(
    r"^\s*(?:public|protected|private|internal)?\s*fun\s+(\w+)\s*\(([^)]*)\)\s*(?::\s*([^ {]+))?")

JS_CLASS_RE = re.compile(r"^\s*class\s+(\w+)")
JS_METHOD_RE = re.compile(r"^\s*(?:async\s+)?(\w+)\s*\(([^)]*)\)\s*{")
JS_FUNC_RE = re.compile(r"^\s*(?:export\s+)?function\s+(\w+)\s*\(([^)]*)\)")

CPP_CLASS_RE = re.compile(r"^\s*class\s+(\w+)")
CPP_METHOD_RE = re.compile(r"^\s*(?:virtual\s+)?(?:[\w:<>]+\s+)+?(\w+)\s*\(([^)]*)\)\s*(?:const)?\s*(?:=\s*0)?\s*[;{]")
CPP_FUNC_RE = re.compile(r"^\s*(?:inline\s+)?(?:static\s+)?(?:[\w:<>]+\s+)+?(\w+)\s*\(([^)]*)\)\s*[;{]")


class CommentStyle:
    """Stores language-specific comment delimiters."""

    def __init__(self, start: str, end: str) -> None:
        self.start = start
        self.end = end

    def wrap(self, body: List[str]) -> str:
        return "\n".join([self.start] + body + [self.end])


COMMENT_STYLES = {
    "python": CommentStyle('"""', '"""'),
    "kotlin": CommentStyle('/**', ' */'),
    "javascript": CommentStyle('/**', ' */'),
    "typescript": CommentStyle('/**', ' */'),
    "csharp": CommentStyle('/*', ' */'),
    "cpp": CommentStyle('/*', ' */'),
}


# endregion


# region ────────────────────────────────────── Core logic

def _strip_existing_header(text: str, language: str) -> str:
    """Removes an existing header inserted by this tool if present."""
    cs = COMMENT_STYLES[language]
    if language == "python":
        pattern = rf"(?s)^{re.escape(cs.start)}.*?{re.escape(cs.end)}\s*"
    else:
        pattern = rf"(?s)^{re.escape(cs.start)}.*?{re.escape(cs.end)}\s*"
    return re.sub(pattern, "", text, count=1)


def _build_generic_header(
    lines: List[str],
    class_re: re.Pattern[str],
    method_re: re.Pattern[str] | None,
    func_re: re.Pattern[str] | None,
) -> List[str]:
    header: List[str] = [" * Classes/Functions:"]

    brace_balance = 0
    class_stack: List[Tuple[_ClassNode, int]] = []  # node, brace_level at declaration
    top_level_funcs: List[Tuple[str, int]] = []
    nodes: Dict[str, _ClassNode] = {}

    for ln, raw in enumerate(lines, 1):
        # Check for class
        cm = class_re.match(raw)
        if cm:
            cls_name = cm.group(1)
            node = _ClassNode(cls_name, ln)
            nodes[cls_name] = node
            parent = class_stack[-1][0] if class_stack else None
            if parent:
                parent.inner.append(node)
            # update brace balance BEFORE pushing
            brace_balance += raw.count("{") - raw.count("}")
            class_stack.append((node, brace_balance))
            continue

        # Update brace balance and pop exited classes
        brace_balance += raw.count("{") - raw.count("}")
        while class_stack and brace_balance <= class_stack[-1][1]:
            class_stack.pop()

        # Method detection
        if method_re:
            mm = method_re.match(raw)
            if mm:
                if class_stack:
                    method_name = mm.group(1) if class_re is CSHARP_METHOD_RE else None  # placeholder
                sig = raw.strip()
                receiver = class_stack[-1][0] if class_stack else None
                if receiver:
                    receiver.methods.append((sig, ln))
                else:
                    top_level_funcs.append((sig, ln))
                continue

        # Top-level function detection
        if func_re:
            fm = func_re.match(raw)
            if fm and not class_stack:
                sig_line = raw.strip()
                top_level_funcs.append((sig_line, ln))

    # Dump
    roots = [n for n in nodes.values() if all(n is not child for parent in nodes.values() for child in parent.inner)]
    for n in roots:
        n.dump(header)
    if top_level_funcs:
        header.append(" *   - Functions:")
        for sig, ln in top_level_funcs:
            header.append(f" *     - {sig} (line {ln})")
    return header


# language-specific builders --------------------------------------------------

def build_python_header(lines: List[str]) -> str:
    hdr_lines = ["Classes/Functions:"]

    current_cls = None
    current_cls_line = None
    class_methods: Dict[str, List[Tuple[str, int]]] = {}
    class_lines: Dict[str, int] = {}
    top_funcs: List[Tuple[str, int]] = []

    for ln, line in enumerate(lines, 1):
        cm = PY_CLASS_RE.match(line)
        if cm:
            current_cls = cm.group(1)
            current_cls_line = ln
            class_lines[current_cls] = ln
            class_methods[current_cls] = []
            continue
        fm = PY_FUNC_RE.match(line)
        if fm:
            indent, name, params, rtype = fm.groups()
            sig = f"{name}({params})"
            if rtype:
                sig += f" -> {rtype.strip()}"
            if indent and current_cls:
                class_methods[current_cls].append((sig, ln))
            elif not indent:
                top_funcs.append((sig, ln))

    for cls, mlist in class_methods.items():
        hdr_lines.append(f"    - {cls} (line {class_lines[cls]}):")
        for sig, ln in mlist:
            hdr_lines.append(f"      - {sig} (line {ln})")
    for sig, ln in top_funcs:
        hdr_lines.append(f"    - {sig} (line {ln})")

    cs = COMMENT_STYLES["python"]
    return cs.wrap(hdr_lines)


def build_kotlin_header(lines: List[str]) -> str:
    header = [" * Classes/Functions:"]
    brace_balance = 0
    class_stack: List[Tuple[_ClassNode, int]] = []
    nodes: Dict[str, _ClassNode] = {}
    top_level_functions: List[Tuple[str, int]] = []

    for ln, line in enumerate(lines, 1):
        cm = KOTLIN_CLASS_RE.match(line)
        if cm:
            cls = cm.group(1)
            node = _ClassNode(cls, ln)
            nodes[cls] = node
            parent = class_stack[-1][0] if class_stack else None
            if parent:
                parent.inner.append(node)
            brace_balance += line.count("{") - line.count("}")
            class_stack.append((node, brace_balance))
            continue

        brace_balance += line.count("{") - line.count("}")
        while class_stack and brace_balance <= class_stack[-1][1]:
            class_stack.pop()

        fm = KOTLIN_FUN_RE.match(line)
        if fm:
            name = fm.group(1)
            params = fm.group(2)
            rtype = fm.group(3) or ""
            sig = f"fun {name}({params})"
            if rtype:
                sig += f": {rtype}"
            if class_stack:
                class_stack[-1][0].methods.append((sig, ln))
            else:
                top_level_functions.append((sig, ln))

    # find roots
    roots = [n for n in nodes.values() if all(n is not child for parent in nodes.values() for child in parent.inner)]
    for n in roots:
        n.dump(header)
    if top_level_functions:
        header.append(" *   - Functions:")
        for sig, ln in top_level_functions:
            header.append(f" *     - {sig} (line {ln})")

    cs = COMMENT_STYLES["kotlin"]
    return cs.wrap(header)


GENERIC_CONFIGS = {
    "javascript": {
        "class_re": JS_CLASS_RE,
        "method_re": JS_METHOD_RE,
        "func_re": JS_FUNC_RE,
    },
    "typescript": {
        "class_re": JS_CLASS_RE,
        "method_re": JS_METHOD_RE,
        "func_re": JS_FUNC_RE,
    },
    "csharp": {
        "class_re": CSHARP_CLASS_RE,
        "method_re": CSHARP_METHOD_RE,
        "func_re": None,
    },
    "cpp": {
        "class_re": CPP_CLASS_RE,
        "method_re": CPP_METHOD_RE,
        "func_re": CPP_FUNC_RE,
    },
}


def build_generic_language_header(lines: List[str], language: str) -> str:
    cfg = GENERIC_CONFIGS[language]
    hdr_body = _build_generic_header(
        lines,
        cfg["class_re"],
        cfg["method_re"],
        cfg["func_re"],
    )
    cs = COMMENT_STYLES[language]
    return cs.wrap(hdr_body)


# endregion


# region ────────────────────────────────────── File processing

def process_file(path: Path, verbose: bool = False) -> None:
    """Inserts or refreshes a header in *path* based on its language."""
    ext = path.suffix.lower()
    language = None
    if ext == ".py":
        language = "python"
    elif ext == ".kt":
        language = "kotlin"
    elif ext in {".js", ".jsx"}:
        language = "javascript"
    elif ext in {".ts", ".tsx"}:
        language = "typescript"
    elif ext == ".cs":
        language = "csharp"
    elif ext in {".cpp", ".cxx", ".cc", ".hpp", ".h"}:
        language = "cpp"
    if language is None:
        return  # Unsupported

    text = path.read_text(encoding="utf-8", errors="ignore")
    text_no_hdr = _strip_existing_header(text, language)
    lines = text_no_hdr.splitlines(keepends=False)

    if language == "python":
        header = build_python_header(lines)
    elif language == "kotlin":
        header = build_kotlin_header(lines)
    else:
        header = build_generic_language_header(lines, language)

    new_content = f"{header}\n" + "\n".join(lines) + "\n"
    path.write_text(new_content, encoding="utf-8")
    if verbose:
        print(f"Processed {language.capitalize()}: {path}")


# endregion


# region ────────────────────────────────────── CLI

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Apply Better Comments file-level headers across multiple languages.")
    p.add_argument("paths", nargs="*", help="Files or directories to process. If omitted, the current directory is used.")
    p.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    targets = [Path(p) for p in args.paths] if args.paths else [Path.cwd()]

    for target in targets:
        if target.is_file():
            process_file(target, args.verbose)
        else:
            for root, _, files in os.walk(target):
                # Skip virtual-envs or git folders to speed things up
                skip_dirs = {".git", "__pycache__", ".venv", "node_modules", "build", "dist"}
                if any(nd in Path(root).parts for nd in skip_dirs):
                    continue
                for f in files:
                    process_file(Path(root) / f, args.verbose)


if __name__ == "__main__":
    main() 