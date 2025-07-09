import re
from agent_docstrings.core import _format_header, OFFSET_PLACEHOLDER
from agent_docstrings.languages.common import ClassInfo, SignatureInfo

def test_placeholder_usage_in_header():
    # Create dummy ClassInfo and SignatureInfo
    class_info = ClassInfo(name="MyClass", line=5, methods=[], inner_classes=[])
    sig_info = SignatureInfo(signature="my_function()", line=10)
    # Generate placeholder header
    header = _format_header([class_info], [sig_info], "python", 0, None, placeholder=True)
    # Check that placeholder for line numbers exists
    assert f"{OFFSET_PLACEHOLDER}+5" in header
    assert f"{OFFSET_PLACEHOLDER}+10" in header 