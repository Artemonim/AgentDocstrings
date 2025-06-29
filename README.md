# Agent Docstrings Generator

A command-line tool to auto-generate and update file-level docstrings summarizing classes and functions. Useful for maintaining a high-level overview of your files, especially in projects with code generated or modified by AI assistants.

## Why?

When working in Cursor and similar IDEs, Agents often start reading files from the beginning. And regarding Cursor's behavior during the script's creation, in normal mode, the model reads 250 lines of code per call, and in MAX mode, 750 lines. However, I have projects with files over 1000 lines of code, which are not very appropriate to divide into smaller files. And anyway, Agent still have to call reading tools for each individual file.

At the same time, the Agent can choose from which line to read the file. It can navigate and surf within your repository. The script literally provides the Agent with the table of contents of the current file, so that immediately after the first read, the Agent understands the entire structure and can read the file from a specific line, rather than trying to get to it (while also potentially making mistakes along the way).

In addition to the advantage of quick navigation, the initial docstring also serves as a method to reduce context window usage. For example, if a required method in a 900-line file is on line 856, the Agent will only read lines 1-250 and 856-900, instead of sequentially going to the desired forty lines and filling its context with unnecessary code.

## Features

-   **Multi-language support**: Python, Java, Kotlin, Go, PowerShell, Delphi, C, C++, C#, JavaScript, TypeScript
-   **Automatic discovery**: Recursively scans directories for source files
-   **Smart filtering**: Respects `.gitignore` files and custom blacklist/whitelist configurations
-   **Incremental updates**: Only modifies files when changes are detected
-   **Type annotations**: Full type hint support for Python 3.8+
-   **CLI interface**: Easy-to-use command-line tool

## Python Version Compatibility

This tool is compatible with **Python 3.8, 3.9, 3.10, 3.11, 3.12, and 3.13**.

### Key compatibility features:

-   Uses `typing.Union` instead of `|` syntax for Python 3.8/3.9 compatibility
-   Uses `typing.Tuple` instead of built-in `tuple` for type hints
-   Compatible with `from __future__ import annotations`
-   No dependency on external libraries

## Installation

### From PyPI (recommended)

```bash
pip install agent-docstrings
```

### From source

```bash
git clone https://github.com/yourname/agent-docstrings.git
cd agent-docstrings
pip install -e .
```

## Usage

### Basic usage

```bash
agent-docstrings src/
```

### With verbose output

```bash
agent-docstrings src/ --verbose
```

### Process multiple directories

```bash
agent-docstrings src/ tests/ lib/
```

### Using as a Python module

```python
from agent_docstrings.core import discover_and_process_files

# Process directories
discover_and_process_files(["src/", "lib/"], verbose=True)
```

## Configuration

### Blacklist (Ignore files)

Create a `.agent-docstrings-ignore` file in your project root to specify files and directories to ignore:

```
# Test directories
tests/
test_*.py

# Build and cache directories
__pycache__/
*.pyc
build/
dist/
*.egg-info/

# IDE files
.vscode/
.idea/

# Documentation
docs/
README.md
```

### Whitelist (Only process specific files)

Create a `.agent-docstrings-include` file to only process specific files:

```
# Only process main source code
src/*.py
lib/*.py
agent_docstrings/*.py
```

**Note**: If a whitelist file exists and is not empty, ONLY files matching the whitelist patterns will be processed.

### Gitignore Integration

The tool automatically reads and respects `.gitignore` files in your project directory and its parents. Files and directories ignored by git will also be ignored by the docstring generator.

## Limitations and Nuances

It is important to understand the nuances of this tool to use it effectively. The quality and method of code parsing vary significantly by language.

-   **Table of Contents, Not Full Documentation**: The generator does not create detailed, explanatory docstrings. Instead, it generates a file-level comment block that acts as a "Table of Contents" listing the functions and classes found in the file. This provides a quick overview of the file's structure.

-   **Language-Dependent Parsing Quality**: The reliability of the parser is highly dependent on the target language.

    -   **Robust AST-Based Parsing (Python, Go)**: For Python and Go, the tool uses native Abstract Syntax Tree (AST) parsers. This approach is highly accurate and robustly handles complex syntax, multiline definitions, and unconventional formatting.

    -   **Regex-Based Parsing (Other Languages)**: For other languages (C++, C#, Java, JavaScript, TypeScript, Kotlin, PowerShell, Delphi), the generator relies on regular expressions and simplified scope analysis (brace counting). This method is inherently more fragile and may fail or produce incorrect results with:
        -   **Multiline Definitions**: Function or class signatures that span multiple lines.
        -   **Complex Syntax**: Advanced language features like C++ templates, decorators on separate lines, or complex default parameter values.
        -   **Unconventional Formatting**: Code that does not follow common formatting standards.
        -   **Scope Confusion**: The brace-counting mechanism can be easily confused by comments or strings containing `{` or `}` characters, leading to incorrect structure detection.

-   **In-Place File Modification**: The tool modifies files directly. It is designed to correctly remove its own previously generated headers, but it might struggle with files that have very complex, pre-existing header comments, potentially leading to incorrect placement of the new header.

## Supported Languages

| Language   | File Extensions                     | Features                       |
| ---------- | ----------------------------------- | ------------------------------ |
| Python     | `.py`                               | Classes, functions, methods    |
| Java       | `.java`                             | Classes, methods               |
| Kotlin     | `.kt`                               | Classes, functions             |
| Go         | `.go`                               | Functions, methods             |
| PowerShell | `.ps1`, `.psm1`                     | Functions                      |
| Delphi     | `.pas`                              | Classes, procedures, functions |
| C          | `.c`, `.h`                          | Functions                      |
| C++        | `.cpp`, `.hpp`, `.cc`, `.cxx`, `.h` | Functions, classes             |
| C#         | `.cs`                               | Classes, methods               |
| JavaScript | `.js`, `.jsx`                       | Functions, classes             |
| TypeScript | `.ts`, `.tsx`                       | Functions, classes             |

## Examples

### Python Example

Before:

```python
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

class MathUtils:
    def add(self, a, b):
        return a + b
```

After:

```python
"""
    --- AUTO-GENERATED DOCSTRING ---
    This docstring is automatically generated by Agent Docstrings.
    Do not modify this block directly.

    Classes/Functions:
      - MathUtils (line 8):
        - add(a, b) (line 9)
      - Functions:
        - calculate_fibonacci(n) (line 1)
    --- END AUTO-GENERATED DOCSTRING ---
"""
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

class MathUtils:
    def add(self, a, b):
        return a + b
```

## Integration with Development Workflow

### Pre-commit Hook

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
    - repo: local
      hooks:
          - id: agent-docstrings
            name: Generate docstrings
            entry: agent-docstrings
            language: system
            files: \.(py|java|kt|go|ps1|psm1|pas|js|jsx|ts|tsx|cs|cpp|cxx|cc|hpp|h|c)$
            pass_filenames: false
            args: [src/]
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Generate docstrings
  run: |
      pip install agent-docstrings
      agent-docstrings src/
      # Check if any files were modified
      git diff --exit-code || (echo "Docstrings need updating" && exit 1)
```

## Development

### Setting up development environment

```bash
git clone https://github.com/Artemonim/agent-docstrings.git
cd agent-docstrings
pip install -e .[dev]
```

### Running tests

```bash
pytest tests/ -v
```

### Code formatting

```bash
black agent_docstrings/
```

### Type checking

```bash
mypy agent_docstrings/
```

### Version Bumping

This project uses [bump-my-version](https://github.com/callowayproject/bump-my-version) for version management. To create a new version, use the following commands after installing the development dependencies (`pip install -e .[dev]`):

-   **Patch release (e.g., 1.0.1 -> 1.0.2):**
    ```bash
    bump-my-version patch
    ```
-   **Minor release (e.g., 1.0.2 -> 1.1.0):**
    ```bash
    bump-my-version minor
    ```
-   **Major release (e.g., 1.1.0 -> 2.0.0):**
    ```bash
    bump-my-version major
    ```

The tool is configured in `pyproject.toml` to automatically update the version string in `agent_docstrings/__init__.py`, `pyproject.toml`, and `CHANGELOG.md`.

**Note**: Per project configuration, this tool only modifies the files. You will need to commit and tag the changes manually after bumping the version.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

## Support

-   **Issues**: [GitHub Issues](https://github.com/Artemonim/agent-docstrings/issues)
-   **Documentation**: [GitHub README](https://github.com/Artemonim/agent-docstrings#readme)
-   **Source Code**: [GitHub Repository](https://github.com/Artemonim/agent-docstrings)
