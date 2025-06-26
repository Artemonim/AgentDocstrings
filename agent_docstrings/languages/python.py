from __future__ import annotations
import re
from typing import List, Tuple, Union, Optional

from .common import ClassInfo, SignatureInfo

PY_CLASS_RE = re.compile(r"^class\s+(\w+)")
PY_FUNC_RE = re.compile(r"^(\s*)(async\s+)?def\s+(_?_?[\w]+_?_?)\(([^)]*)\)(?:\s*->\s*([^:]+))?:")


def parse_python_file(
    lines: List[str],
) -> Tuple[List[ClassInfo], List[SignatureInfo]]:
    """Parse Python source and extract class/function definitions.

    Args:
        lines (List[str]): Python source code split into lines.

    Returns:
        Tuple[List[ClassInfo], List[SignatureInfo]]: Collection of classes
        (with their methods) and a list of module-level functions.
    """
    classes: List[ClassInfo] = []
    top_level_funcs: List[SignatureInfo] = []
    
    current_class_info: Optional[ClassInfo] = None
    
    for line_num, line in enumerate(lines, 1):
        class_match = PY_CLASS_RE.match(line)
        if class_match:
            class_name = class_match.group(1)
            current_class_info = ClassInfo(name=class_name, line=line_num, methods=[], inner_classes=[])
            classes.append(current_class_info)
            continue

        func_match = PY_FUNC_RE.match(line)
        if func_match:
            indent, async_keyword, name, params, rtype = func_match.groups()
            # Basic handling for dunder methods, excluding __init__ from method lists for cleaner summaries
            if name == "__init__":
                continue
            
            sig_params = params.replace('self, ', '').replace('self', '')
            signature = f"{name}({sig_params})"
            if rtype:
                signature += f" -> {rtype.strip()}"
            
            info = SignatureInfo(signature=signature, line=line_num)
            
            if indent and current_class_info:
                # This simple logic doesn't support nested classes.
                # It assumes any indented function belongs to the most recent class.
                current_class_info.methods.append(info)
            elif not indent:
                top_level_funcs.append(info)
                current_class_info = None # A top-level function resets the class context
                
    return classes, top_level_funcs 