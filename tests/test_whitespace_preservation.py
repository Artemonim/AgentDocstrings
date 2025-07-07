"""
Tests to ensure that the docstring generator preserves important whitespace.
"""
from textwrap import dedent

def test_blank_lines_are_preserved(source_processor) -> None:
    """
    Verifies that blank lines between functions and classes are not removed.
    """
    initial_content = dedent('''
        class FirstClass:
            pass


        def top_level_function():
            pass

    ''').strip()
    
    result_content, _, _ = source_processor("whitespace_test.py", initial_content)
    
    # After processing, there should still be a blank line between the class and function
    # The docstring generation will add its own lines, so we can't do a direct
    # line-by-line comparison, but we can check for the pattern.
    expected_pattern = "class FirstClass:\n    pass\n\n\ndef top_level_function():"
    
    # We normalize the result content by removing the docstring to make the test reliable
    from agent_docstrings.languages.common import remove_agent_docstring
    cleaned_result = remove_agent_docstring(result_content, 'python')
    
    # The cleaned result should have the preserved blank lines.
    # Note: The exact number of newlines might differ slightly based on how the
    # docstring is inserted, so we check for at least two newlines.
    assert "pass\n\n\ndef" in cleaned_result, \
        f"Expected blank lines to be preserved. Cleaned result:\n{cleaned_result}"

def test_trailing_whitespace_is_preserved(source_processor) -> None:
    """
    Verifies that trailing newlines at the end of a file are not removed.
    """
    initial_content = dedent('''
        class FirstClass:
            pass
    ''') + "\\n\\n"  # Add trailing newlines that dedent would strip

    result_content, _, _ = source_processor("whitespace_test.py", initial_content)
    
    from agent_docstrings.languages.common import remove_agent_docstring
    cleaned_result = remove_agent_docstring(result_content, 'python')
    
    assert cleaned_result.endswith("\\n\\n"), \
        f"Expected trailing newlines to be preserved. Cleaned result ends with: {repr(cleaned_result[-5:])}" 