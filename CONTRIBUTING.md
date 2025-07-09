# Contributing to AgentDocstringsGenerator

First off, thank you for considering contributing to AgentDocstringsGenerator! It's people like you that make this such a great tool.

This document provides guidelines for contributing to the project. Please feel free to propose changes to this document in a pull request.

## Table of Contents

-   [How Can I Contribute?](#how-can-i-contribute)
    -   [Reporting Bugs](#reporting-bugs)
    -   [Suggesting Enhancements](#suggesting-enhancements)
    -   [Pull Requests](#pull-requests)
-   [Development Workflow](#development-workflow)
    -   [Branching Model](#branching-model)
    -   [Development Steps](#development-steps)
    -   [Updating the Changelog](#updating-the-changelog)
-   [Release Process (for maintainers)](#release-process-for-maintainers)
-   [Styleguides](#styleguides)

## How Can I Contribute?

We value community contributions and appreciate your help. Please be respectful in all your interactions.

### Reporting Bugs

If you find a bug, please ensure it hasn't already been reported by searching on GitHub under [Issues](https://github.com/Artemonim/AgentDocstrings/issues). If you can't find an open issue addressing the problem, please open a new one. Include a clear title, a detailed description, and a code sample or test case that demonstrates the issue.

### Suggesting Enhancements

If you have an idea for an enhancement, please open an issue to discuss it first. This allows us to coordinate our efforts and ensure the proposed changes align with the project's goals.

### Pull Requests

We welcome pull requests. Please follow these steps to have your contribution considered:

1. Follow the [Development Workflow](#development-workflow).
2. Ensure that your code adheres to the [Styleguides](#styleguides).
3. Make sure all tests pass.
4. Fill out the pull request template provided.

## Development Workflow

This project uses a GitFlow-like branching model.

### Branching Model

-   **`master`**: This branch contains the latest stable release. Direct pushes are not allowed.
-   **`dev`**: This is the main development branch. All feature branches should be created from `dev`, and all pull requests should be submitted to `dev`.
-   **`feature/*`**: For new features. Branched from `dev`. Example: `feature/new-parser`.
-   **`fix/*`**: For bug fixes. Branched from `dev`. Example: `fix/off-by-one-error`.
-   **`release/*`**: For preparing new releases. Branched from `dev`. Merged into `master`.

### Development Steps

1.  **Fork** the repository on GitHub.
2.  **Clone** your fork locally: `git clone https://github.com/YOUR_USERNAME/AgentDocstrings.git`
3.  **Set up the environment**:
    ```bash
    cd AgentDocstrings
    pip install -e .[dev]
    ```
4.  **Create a new branch** from `dev`:
    ```bash
    git checkout dev
    git pull origin dev
    git checkout -b feature/your-amazing-feature
    ```
5.  **Make your changes**. Write clean, readable code.
6.  **Add or update tests** for your changes in the `tests/` directory.
7.  **Run tests** to ensure everything is working correctly: `python -m pytest`
8.  **Update the Changelog** `NextRelease` section.
9.  **Commit** your changes. Use a clear and descriptive commit message.
10. **Push** your branch to your fork on GitHub: `git push origin feature/your-amazing-feature`
11. **Open a Pull Request** to the `dev` branch of the main repository.

### Updating the Changelog

For every change that affects the user, you must add an entry to the `CHANGELOG.md` file under the `[NextRelease]` section. Follow the format of existing entries. If your pull request resolves an existing issue, please link it in the changelog entry `(fixes #123)` or `(closes #456)`).

Example:

```markdown
## [NextRelease]

### Fixed

-   **My Awesome Fix**: A brief description of what you've fixed (fixes #78).
```

## Release Process (for maintainers)

The release process is partially automated.

1.  Create a release branch from `dev`: `git checkout -b release/x.y.z` (e.g., `release/1.4.0`).
2.  Update the version using `bump-my-version`:
    ```bash
    # For a patch, minor, or major release
    bump-my-version bump patch/minor/major
    ```
    This command will update the version in `pyproject.toml` and update the `CHANGELOG.md`, replacing `[NextRelease]` with the new version tag.
3.  Commit the version bump: `git commit -am "chore: release v.x.y.z"`
4.  Push the release branch: `git push origin release/x.y.z`
5.  Open a Pull Request from the `release/x.y.z` branch to `master`.
6.  Once the PR is merged into `master`, the `release-automation` workflow will automatically:
    -   Create a Git tag (e.g., `v1.4.0`).
    -   Create a GitHub Release with the notes from `CHANGELOG.md`.
    -   Create a Pull Request to merge `master` back into `dev`.
7.  The `release.yml` workflow will then automatically publish the package to PyPI upon the creation of the GitHub Release.

## Styleguides

Please follow the coding style of the project to maintain consistency.

-   **Python**: [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html), formatted with `black`.
-   **Comments**: Use [Better Comments](https://marketplace.visualstudio.com/items?itemName=aaron-bond.better-comments) style.
-   **Docstrings**: Use Google Style Docstrings.
