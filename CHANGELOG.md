# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features

-   Additional language support: Swift, Perl, Curl, Fortran, Visual Basic, R, PHP, Lua, Bash, SQL
-   Configuration file format validation
-   Switching to the Abstract Syntax Tree (AST)

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

### Technical Features

-   Uses `from __future__ import annotations` for forward compatibility
-   Compatible with `typing.Union` and `typing.Tuple` for Python 3.8/3.9
-   No external dependencies - built on Python standard library only
-   Comprehensive test suite with pytest
-   Full type checking support with mypy
-   Code formatting with black
-   Proper packaging for PyPI distribution

### Configuration

-   `.agent-docstrings-ignore`: Specify files and patterns to exclude
-   `.agent-docstrings-include`: Specify files and patterns to include (whitelist mode)
-   Automatic integration with existing `.gitignore` files
-   Support for glob patterns in configuration files

### Documentation

-   Comprehensive README with usage examples
-   Integration guides for pre-commit hooks and CI/CD
-   Development setup instructions
-   API documentation for programmatic usage

## Version History

-   **1.0.1** - Parser and docstring handling improvements
-   **1.0.0** - Initial stable release with multi-language support and filtering system
-   **0.4.0** - (internal)
-   **0.3.0** - (internal)
-   **0.2.0** - (internal)
-   **0.1.0** - Initial development version (internal)
