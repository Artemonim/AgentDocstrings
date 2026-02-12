# Roadmap to Plugin-Based Architecture

## Objective

Define and implement a plugin-based architecture for language-specific logic to improve modularity, scalability, and maintainability of the docstring generator.

## Goals

- Extract language-specific responsibilities (parsing, comment styles, header handling) into separate plugins.
- Simplify `core.py` to function as a pure orchestrator using a standardized plugin interface.
- Maintain shared data structures (`ClassInfo`, `SignatureInfo`) and common utilities in `common.py`.
- Improve testability by allowing isolated testing of each language plugin.

## Phases

### Phase 1: Define Plugin Interface

- Introduce `LanguagePlugin` interface in `common.py` with methods:
  - `get_comment_style() -> CommentStyle`
  - `parse(lines: List[str]) -> Tuple[List[ClassInfo], List[SignatureInfo]]`
  - `get_preserved_header_end_line(lines: List[str]) -> int`
  - `remove_agent_docstring(text: str) -> str`
- Document interface contract and update developer guide.

### Phase 2: Implement Language Plugins

- Create plugin classes for each supported language:
  - Python, Go, Java, Kotlin, JavaScript, TypeScript, C#, C/C++, PowerShell, Delphi.
- Move existing language-specific logic from `core.py` and `common.py` into respective plugin implementations.
- Register each plugin in a `LANG_PLUGINS` registry keyed by file extension.

### Phase 3: Refactor Core Orchestrator

- Replace `EXT_TO_LANG` and `LANG_PARSERS` maps with the new plugin registry.
- Update `process_file()` to load and invoke plugin methods exclusively.
- Remove all `if language == ...` branches from `core.py` and `common.py`.

### Phase 4: Update Common Utilities

- Retain shared data types (`ClassInfo`, `SignatureInfo`) in `common.py`.
- Optionally move default comment-style configurations into plugins or keep shared defaults.
- Ensure `common.py` only defines interfaces and general-purpose helpers.

### Phase 5: Testing & Validation

- Develop unit tests for each plugin method in isolation.
- Update existing core and integration tests to use the plugin-based workflow.
- Validate end-to-end functionality across all supported languages.

### Phase 6: Documentation & Release

- Update `README.md` and project documentation with new architecture overview.
- Add a migration guide for contributors and users.
- Tag a beta release for community feedback, then finalize and publish.

## Estimated Timeline

- **Q3 2025:** Complete Phases 1–3 (interface definition, plugin implementation, core refactor).
- **Q4 2025:** Complete Phases 4–6 (utilities update, testing, documentation, release). 