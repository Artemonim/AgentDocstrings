# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features

-   Additional language support: Swift, Perl, Curl, Fortran, Visual Basic, R, PHP, Lua, Bash, SQL
-   Configuration file format validation
-   Switching to the Abstract Syntax Tree (AST)
-   [And more...](https://github.com/Artemonim/AgentDocstrings/issues)

## [NextRelease]

### Header

-   **subtitle**: describtion

## [1.3.5]

### Added

-   **Placeholder-Based Line Numbering**: Implemented a new placeholder system (`OFFSET_PLACEHOLDER`) for calculating line numbers in generated headers. This ensures deterministic line numbering by first generating headers with placeholders, then calculating the actual offset based on the final header size, and finally replacing placeholders with accurate line numbers.

### Fixed

-   **Deterministic Line Numbering**: Completely reworked the line number calculation algorithm to ensure consistent and accurate line numbers across multiple runs. The new approach uses a two-pass system that measures rather than guesses header sizes, ensuring deterministic results.
-   **Docstring Merging Logic**: Improved the logic for merging manual docstrings with auto-generated content. Manual content is now properly preserved and formatted without adding unnecessary newlines or reformatting.
-   **Multi-Pass Docstring Removal**: Enhanced the `remove_agent_docstring` function to handle complex scenarios where multiple agent-generated docstrings might be present, preventing duplication issues on repeated runs.
-   **Whitespace Normalization**: Added proper whitespace handling in content comparison to prevent unnecessary file modifications when only minor whitespace differences exist.
-   **Manual Content Extraction**: Improved the extraction of manual docstring content by properly handling the inner content within triple quotes, preserving original formatting and indentation.

### Testing

-   **New Test Cases**: Added comprehensive test cases for placeholder usage, short manual docstring handling, and merged multiline docstring preservation to ensure the new algorithms work correctly across various scenarios.

## [1.3.4]

### Fixed

-   **Deterministic Processing**: Fixed a critical bug that caused line numbers in the table of contents to change on every run. This was due to inconsistent newline handling after removing an existing agent docstring. The process is now fully idempotent.
-   **Robust Docstring Removal**: Improved the detection logic to correctly find and remove all agent-generated docstrings, even when located in the middle of a file or when multiple (erroneous) docstrings were present. This prevents docstring duplication on repeated runs.
-   **Manual Docstring Preservation**: Ensured that manual docstrings are no longer reformatted or modified unless they are being merged with an agent-generated table of contents.
-   **Version-Only Change Skipping**: Fixed a bug where files were being unnecessarily modified when only the version number in the auto-generated header differed, while the actual content structure remained unchanged. The tool now performs normalized content comparison that ignores version differences, preventing unnecessary file modifications after Agent Docstrings version updates.

### Documentation

-   **Contribution Guide**: Added a new `CONTRIBUTING.md` file with detailed guidelines for development workflow and the release process.
-   **README Update**: Updated `README.md` to link to the new contribution guide and reflect the automated release process.

### CI/CD

-   **Release Automation**: Added a new `release-automation.yml` workflow that automatically creates Git tags, GitHub Releases, and back-merge PRs when release branches are merged to master.
-   **CI Optimization**: Optimized the main CI pipeline by removing redundant test runs on master branch pushes and adding caching for pip dependencies and Go modules to speed up workflow execution.
-   **Workflow Efficiency**: Changed CI triggers to run on pushes to `dev` instead of `master`, eliminating duplicate test runs while maintaining comprehensive coverage.
-   **Version Check Precision**: Improved the version bump detection in CI to specifically check version changes in `pyproject.toml` and `agent_docstrings/__init__.py`, preventing false positives from other file modifications.

## [1.3.3]

### Fixed

-   **Python Docstring Cleaning**: Improved the `remove_agent_docstring` function to better handle Python docstrings by preserving manual content while removing auto-generated table of contents. The function now correctly identifies and removes only the auto-generated content while maintaining the structure of existing manual docstrings. (fixes #11)
-   **C-Style Comment Handling**: Enhanced the docstring removal logic for C-style languages (Kotlin, Java, Go, etc.) to be more flexible with comment formatting variations, ensuring proper detection and removal of auto-generated content across different comment styles.

## [1.3.2]

### Fixed

-   **Kotlin Header Preservation**: Fixed a bug where multi-line block comments (`/** ... */`) in Kotlin files were not correctly preserved, leading to malformed docstrings. The header parsing logic now correctly identifies and preserves these comment blocks. (Fixes #9)

## [1.3.1]

### Added

-   **Python Single-Line Docstrings**: Implemented support for identifying and merging the generated table of contents with existing single-line Python docstrings (`"""docstring"""`).

### Fixed

-   **Python Docstring Generation**: Fixed a critical bug where repeatedly processing a Python file with a manual docstring would cause content duplication. The logic has been reworked to ensure correct placement of the generated table of contents relative to `from __future__ import` statements and existing docstrings.

### CI/CD

-   **CI dev**: The CI pipeline now runs on the `dev` branch, with Codecov reports limited to `master`.
-   **Version check**: Added a new check to prevent accidental version bumps in feature branches.

## [1.3.0] - 2025-06-30

### Added

-   **Process Individual Files**: The CLI now accepts both directory and individual file paths, allowing for more granular control over which files are processed.
-   **Expanded Keywords**: Added a comprehensive list of keywords to `pyproject.toml` to significantly improve package discoverability on PyPI and search engines.
-   **Beta Features Flag**: Introduced a `--beta` command-line flag to enable experimental features that are under development.

### Changed

-   **Header Text Update**: Changed the auto-generated header to "Table of content is automatically generated by Agent Docstrings {version}".
-   **Streamlined Header Format**: The format of the generated "Table of Contents" has been improved. Top-level functions and classes are now presented in a single, chronologically sorted list, removing the nested "Functions" section for a cleaner, more intuitive layout.
-   **Deterministic Sorting**: All discovered items (classes, methods, functions) are now strictly sorted by their line number in the source file, ensuring a consistent and predictable output every time.
-   **CLI Argument Renaming**: The `DIRECTORY` argument in the CLI has been renamed to `PATH` to accurately reflect its new capability to handle both files and directories.
-   **Header Version Updates**: The tool will now update the header if the generator version has changed, even if the code structure remains the same, ensuring docstrings always reflect the version of the tool that generated them.
-   **Repository URLs**: Updated project URLs in `pyproject.toml` to point to the correct `AgentDocstrings` repository name.

### Fixed

-   **Error Handling for Inaccessible Directories**: Fixed a crash (`PermissionError`) that occurred when scanning directories with restricted read permissions. The application will now skip such directories and print a warning, preventing unintended modifications to files that might have been excluded by an unreadable `.gitignore` or other configuration files.
-   **Deleting empty lines**: Detected and fixed the removal of empty lines at the end of processed files
-   **Language-Specific Indentation**: Fixed the indentation in the generated 'Table of Contents' to respect common style conventions for each language (e.g., 4 spaces for Python, 2 for JavaScript).

### Build

-   **Python Version Support**: Updated the minimum required Python version from 3.8 to 3.10 to align with modern dependencies and language features. Project metadata (`pyproject.toml`) and CI configurations have been updated accordingly.

### CI/CD

-   **Continuous Integration Workflow**: Added a new GitHub Actions workflow (`ci.yml`) to automatically run tests on all pushes and pull requests to the `master` branch. The workflow tests against multiple Python versions (3.10-3.13) and includes matrix testing for beta features.

### Documentation

-   **Complete README Overhaul**: The `README.md` has been completely rewritten to be more comprehensive, professional, and user-friendly. It now includes a clear project mission, a detailed table of contents, expanded sections on features and usage, new examples, and platform compatibility information.
-   **Pull Request Template**: Added a `PULL_REQUEST_TEMPLATE.md` to standardize contributions.
-   **Demo Video**: Included a new video in the `README.md` to demonstrate the tool's functionality.

## [1.2.1] - 2025-06-30

### Added

-   **Python Docstring Merging**: Implemented a feature to merge the auto-generated header with existing manual module-level docstrings in Python files, preserving user-written content.

### Changed

-   **Test Suite Refactoring**: Significantly refactored the test suite by introducing a `source_processor` fixture. This simplifies test code, removes boilerplate for file creation, and improves readability across all test files.

### Documentation

-   Updated the repository URL in `README.md`.
-   Reorganized `README.md` for better readability by moving the "Supported Languages" section to the top.

## [1.2.0] - 2025-06-29

### Added

-   **Generator Versioning**: The tool's version is now embedded in the generated docstring for easier tracking and debugging.
-   **Header Preservation**: Implemented intelligent detection to preserve file headers (e.g., shebangs, encoding declarations, Go package definitions, leading comments/imports) across all supported languages.
-   **Expanded Language Support**: Added initial processing support and type mappings for Java, PowerShell, Delphi, and C.
-   **Enhanced Testing**: Introduced new test suites for determinism, header preservation, and line number accuracy to ensure core feature reliability.
-   **Initial release of `agent-docstrings`**

### Changed

-   **Python Parser Overhaul**: Replaced the fragile regex-based Python parser with a robust implementation using Python's native Abstract Syntax Tree (`ast`) module. This provides highly accurate parsing of complex function signatures, decorators, type hints, and nested class structures.
-   **Line Numbering Accuracy**: Completely reworked the line number calculation to account for preserved file headers and the size of the injected docstring, ensuring the table of contents is always accurate.

### Fixed

-   **`__future__` Import Placement**: Corrected a critical bug where `from __future__ import` statements were incorrectly moved below the generated docstring, breaking Python file syntax.
-   **Docstring Management**: Hardened the logic for identifying and removing agent-generated docstrings by using more specific start/end markers, preventing accidental modification of user-written docstrings.
-   **Generic Parser**: Improved the generic parser for C-style languages, resolving a known bug that affected brace counting and failed C# file parsing.

## [1.1.0] - 2025-06-29

### AST-parsing

-   **Go Language**:
    -   Implemented a new, high-precision AST parser using Go's native `go/parser` and `go/ast` libraries. This significantly improves the accuracy of identifying functions, methods, and types in `.go` files compared to previous methods.
    -   Added a `build_goparser.ps1` script to automate the compilation of the Go parser into an executable.
    -   Integrated the new parser into the main Python application, replacing the old logic for Go file analysis.

## [1.0.1] - 2025-06-27

### Fixed

-   **Parser improvements**:
    -   Correctly identifies functions with `async def`.
    -   Better handling of functions with decorators.
-   **Docstring placement**:
    -   Ensures auto-generated docstrings are placed after shebang (`#!`) and encoding (`# -*- coding: utf-8 -*-`) lines.
-   **Unified docstring handling**:
    -   Intelligently integrates auto-generated docstrings into existing manual docstrings.
    -   Replaces content of existing auto-generated docstrings while preserving manual additions.

## [1.0.0] - 2025-06-27

### Added

-   **Multi-language support**: Python, Java, Kotlin, Go, PowerShell, Delphi, C++, C#, JavaScript, TypeScript
-   **Smart file filtering system**:
    -   Automatic `.gitignore` parsing and respect
    -   Custom blacklist support via `.agent-docstrings-ignore` files
    -   Custom whitelist support via `.agent-docstrings-include` files
-   **Python version compatibility**: Full support for Python 3.8, 3.9, 3.10, 3.11, 3.12, and 3.13
-   **Type annotations**: Complete type hint support using `typing` module for backward compatibility
-   **CLI interface**: Easy-to-use command-line tool with verbose output option
-   **Programmatic API**: Import and use in other Python projects
-   **Safe operation**: Only modifies auto-generated docstring blocks, preserves existing documentation
-   **Incremental updates**: Only processes files when changes are detected
