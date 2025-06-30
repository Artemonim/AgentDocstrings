<!-- ain badges -->

[![PyPI version](https://badge.fury.io/py/agent-docstrings.svg)](https://badge.fury.io/py/agent-docstrings)
[![Python versions](https://img.shields.io/pypi/pyversions/agent-docstrings.svg)](https://pypi.org/project/agent-docstrings/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- GitHub stats -->

[![GitHub stars](https://img.shields.io/github/stars/Artemonim/AgentDocstrings.svg?style=social&label=Star)](https://github.com/Artemonim/AgentDocstrings)
[![GitHub forks](https://img.shields.io/github/forks/Artemonim/AgentDocstrings.svg?style=social&label=Fork)](https://github.com/Artemonim/AgentDocstrings)
[![Build Status](https://github.com/Artemonim/AgentDocstrings/workflows/Publish%20Python%20Package%20to%20PyPI/badge.svg)](https://github.com/Artemonim/AgentDocstrings/actions)

<!-- Code Quality -->

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Typed with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![codecov](https://codecov.io/gh/Artemonim/AgentDocstrings/branch/master/graph/badge.svg)](https://codecov.io/gh/Artemonim/AgentDocstrings)

# Agent Docstrings: Automatic Code Summaries

**Agent Docstrings** is a command-line tool that automatically generates and maintains a "Table of Contents" at the top of your source files. It scans for classes, functions, and methods, creating a summary that provides a high-level overview of the file's structure.

<video src="Doc/AgentDocstringsExample130.mp4" autoplay loop muted width="600"></video>

This is especially useful for AI-Agents: quickly understanding large files, navigating unfamiliar codebases, etc.

---

## Table of Contents

-   [Supported Languages](#supported-languages)
-   [Why Use Agent Docstrings?](#why-use-agent-docstrings)
-   [Features](#features)
-   [Examples](#examples)
-   [Platform Compatibility](#platform-compatibility)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Configuration](#configuration)
-   [Limitations and Nuances](#limitations-and-nuances)
-   [Integration with Development Workflow](#integration-with-development-workflow)
-   [Development](#development)
-   [Contributing](#contributing)
-   [License](#license)
-   [Changelog](#changelog)

---

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

## Why Use Agent Docstrings?

**Agent Docstrings** providing a scannable "Table of Contents" at the beginning of each file. This offers several key advantages:

-   **Faster Onboarding**: AI Agents can familiarize themselves with the codebase much faster. The generated docstring acts as a map to the file's contents.
-   **Improved Code Navigation**: AI get an immediate high-level overview of any file's structure without reading its entire content. Jump directly to the code it need.

## Features

-   **Multi-language support**: Works with a wide range of popular programming languages.
-   **Automatic discovery**: Recursively scans directories for source files to process.
-   **Smart filtering**: Automatically respects `.gitignore` files and allows for custom ignore (`.agent-docstrings-ignore`) and include (`.agent-docstrings-include`) files for fine-grained control.
-   **Incremental updates**: Designed to be fast, it only modifies files when changes to the code structure are detected.
-   **Robust Parsers**: Uses reliable AST (Abstract Syntax Tree) parsers for Python and Go, and intelligent regex-based parsing for other languages.
-   **CLI interface**: A simple and easy-to-use command-line tool for manual runs or CI/CD integration.
-   **Extensively Tested**: High reliability is ensured by a comprehensive suite of over 140 tests, covering everything from individual parsers (unit tests) to full command-line behavior (end-to-end tests).

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
    Table of content is automatically generated by Agent Docstrings v1.3.0

    Classes/Functions:
    - MathUtils (line 18):
      - add(a, b) (line 19)
      - Functions:
        - calculate_fibonacci(n) (line 13)
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

## Platform Compatibility

This tool is compatible with:

-   **Python**: 3.10, 3.11, 3.12, and 3.13
-   **Go**: >=1.22 (required only for building the Go parser during package development)

-   No dependency on external Python libraries at runtime

## Installation

### From PyPI (recommended)

```bash
pip install agent-docstrings
```

### From source

```bash
git clone https://github.com/Artemonim/agent-docstrings.git
cd agent-docstrings
pip install -e .
```

## Usage

### Processing paths

You can process one or more directories, files, or a mix of both.

Process a directory:

```bash
agent-docstrings src/
```

Process a single file:

```bash
agent-docstrings src/main.py
```

Process multiple paths:

```bash
agent-docstrings src/ tests/ lib/utils.py
```

### With verbose output

```bash
agent-docstrings src/ --verbose
```

### Using as a Python module

```python
from agent_docstrings.core import discover_and_process_files

# Process a mix of files and directories
discover_and_process_files(["src/", "lib/utils.py"], verbose=True)
```

## Configuration

### Gitignore Integration

The tool automatically reads and respects `.gitignore` files in your project directory and its parents. Files and directories ignored by git will also be ignored by the docstring generator.

### Blacklist (Ignore files)

You can create a gitignore-like `.agent-docstrings-ignore` file in your project root to specify files and directories to ignore:

### Whitelist (Only process specific files)

You can create a gitignore-like `.agent-docstrings-include` file to only process specific files:

```
# Only process main source code
src/*.py
lib/*.py
agent_docstrings/*.py
```

**Note**: If a whitelist file exists and is not empty, ONLY files matching the whitelist patterns will be processed.

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
