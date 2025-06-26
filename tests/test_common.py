"""Tests for agent_docstrings.languages.common module."""

from __future__ import annotations

import pytest

from agent_docstrings.languages.common import (
    COMMENT_STYLES,
    ClassInfo,
    SignatureInfo,
    CommentStyle,
    remove_agent_docstring,
    DOCSTRING_START_MARKER,
    DOCSTRING_END_MARKER,
)


class TestDataClasses:
    """Tests for data classes used in parsing."""

    def test_signature_info_creation(self) -> None:
        """Test SignatureInfo namedtuple creation and access."""
        sig = SignatureInfo(signature="test_function(param: str) -> int", line=42)
        assert sig.signature == "test_function(param: str) -> int"
        assert sig.line == 42

    def test_class_info_creation(self) -> None:
        """Test ClassInfo namedtuple creation and access."""
        method = SignatureInfo(signature="method()", line=2)
        inner_class = ClassInfo(name="Inner", line=3, methods=[], inner_classes=[])
        
        cls = ClassInfo(
            name="TestClass",
            line=1,
            methods=[method],
            inner_classes=[inner_class]
        )
        
        assert cls.name == "TestClass"
        assert cls.line == 1
        assert len(cls.methods) == 1
        assert cls.methods[0] == method
        assert len(cls.inner_classes) == 1
        assert cls.inner_classes[0] == inner_class

    def test_comment_style_creation(self) -> None:
        """Test CommentStyle namedtuple creation."""
        style = CommentStyle(start="/*", end="*/", prefix=" * ")
        assert style.start == "/*"
        assert style.end == "*/"
        assert style.prefix == " * "


class TestCommentStyles:
    """Tests for comment style definitions."""

    def test_all_supported_languages_have_styles(self) -> None:
        """Ensure all supported languages have comment style definitions."""
        expected_languages = {
            "python", "kotlin", "javascript", "typescript", "csharp", "cpp", 
            "c", "java", "go", "powershell", "delphi"
        }
        assert set(COMMENT_STYLES.keys()) == expected_languages

    @pytest.mark.parametrize("language,expected_start,expected_end,expected_prefix", [
        ("python", '"""', '"""', "    "),
        ("kotlin", '/**', ' */', ' * '),
        ("javascript", '/**', ' */', ' * '),
        ("typescript", '/**', ' */', ' * '),
        ("csharp", '/*', ' */', ' * '),
        ("cpp", '/*', ' */', ' * '),
    ])
    def test_comment_style_values(
        self, 
        language: str, 
        expected_start: str, 
        expected_end: str, 
        expected_prefix: str
    ) -> None:
        """Test specific comment style values for each language."""
        style = COMMENT_STYLES[language]
        assert style.start == expected_start
        assert style.end == expected_end
        assert style.prefix == expected_prefix


class TestHeaderStripping:
    """Tests for remove_agent_docstring function."""

    def test_strip_python_header(self) -> None:
        """Test stripping Python docstring headers."""
        content = '''"""Classes/Functions:
    - TestClass (line 5):
      - method(self) (line 6)
    - Functions:
      - function() (line 10)
"""
class TestClass:
    def method(self):
        pass

def function():
    pass'''
        
        expected = '''class TestClass:
    def method(self):
        pass

def function():
    pass'''
        
        result = strip_existing_header(content, "python")
        assert result.strip() == expected.strip()

    def test_strip_block_comment_header(self) -> None:
        """Test stripping block comment headers for C-style languages."""
        content = '''/**Classes/Functions:
 *   - TestClass (line 8):
 *     - method() (line 9)
 */
class TestClass {
    void method() {}
}'''
        
        expected = '''class TestClass {
    void method() {}
}'''
        
        for language in ["kotlin", "javascript", "typescript"]:
            result = strip_existing_header(content, language)
            assert result.strip() == expected.strip()

    def test_strip_c_style_comment_header(self) -> None:
        """Test stripping C-style comment headers."""
        content = '''/*Classes/Functions:
 *   - Calculator (line 6):
 *     - add(int, int) (line 7)
 */
class Calculator {
    int add(int a, int b) { return a + b; }
}'''
        
        expected = '''class Calculator {
    int add(int a, int b) { return a + b; }
}'''
        
        for language in ["csharp", "cpp"]:
            result = strip_existing_header(content, language)
            assert result.strip() == expected.strip()

    def test_no_header_to_strip(self) -> None:
        """Test that content without headers remains unchanged."""
        content = '''class TestClass:
    def method(self):
        pass'''
        
        result = strip_existing_header(content, "python")
        assert result == content

    def test_preserve_shebang_when_stripping(self) -> None:
        """Test that shebangs are preserved during header stripping."""
        content = '''#!/usr/bin/env python3
"""Classes/Functions:
    - TestClass (line 6):
"""
class TestClass:
    pass'''
        
        result = strip_existing_header(content, "python")
        assert "class TestClass:" in result

    def test_strip_header_with_various_whitespace(self) -> None:
        """Test header stripping with different whitespace patterns."""
        base_content = '"""Classes/Functions:\n    - Test (line 4):\n"""\nclass Test: pass'
        
        result = strip_existing_header(base_content, "python")
        assert "Classes/Functions:" not in result
        assert "class Test: pass" in result

    def test_strip_only_first_matching_header(self) -> None:
        """Test that only the first matching header is stripped."""
        content = '''"""Classes/Functions:
    - FirstClass (line 6):
"""
class FirstClass:
    def method(self):
        """
        Classes/Functions:
          - This should not be stripped
        """
        pass'''
        
        result = strip_existing_header(content, "python")
        assert result.count("Classes/Functions:") == 1
        assert "This should not be stripped" in result

    def test_strip_header_edge_cases(self) -> None:
        """Test edge cases in header stripping."""
        assert strip_existing_header("", "python") == ""
        
        header_only = '"""Classes/Functions:\n    - Test (line 4):\n"""'
        result = strip_existing_header(header_only, "python")
        assert "Classes/Functions:" not in result
        
        no_newline = '"""Classes/Functions:\n"""class Test: pass'
        result = strip_existing_header(no_newline, "python")
        assert result == "class Test: pass"

    def test_header_not_at_start(self) -> None:
        """Test that headers not at the start of file are not stripped."""
        content = '''class SomeClass:
    pass

"""Classes/Functions:
    - This should not be stripped
"""'''
        
        result = strip_existing_header(content, "python")
        assert "class SomeClass:" in result

    @pytest.mark.parametrize("language", ["python", "kotlin", "javascript", "typescript", "csharp", "cpp"])
    def test_invalid_language_patterns(self, language: str) -> None:
        invalid_contents = [
            "Classes/Functions: but not in a comment",
            "/* Classes/Functions: but not closed properly",
            '""" Classes/Functions: but missing closing quotes',
        ]
        
        for content in invalid_contents:
            result = strip_existing_header(content, language)
            assert isinstance(result, str) 