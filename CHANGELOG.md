# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

## [Unreleased]

### Planned Features

-   Additional language support: Swift, Perl, Curl, Fortran, Visual Basic, R, PHP, Lua, Bash, SQL
-   Configuration file format validation
-   Switching to the Abstract Syntax Tree (AST)

---

## Version History

-   **1.0.0** - Initial stable release with multi-language support and filtering system
-   **0.4.0** - (internal)
-   **0.3.0** - (internal)
-   **0.2.0** - (internal)
-   **0.1.0** - Initial development version (internal)
