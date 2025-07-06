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