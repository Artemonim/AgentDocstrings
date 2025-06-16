# Agent Docstrings

A command-line tool to auto-generate and update file-level docstrings summarizing classes and functions. Useful for maintaining a high-level overview of your files, especially in projects with code generated or modified by AI assistants.

Supports Python, Kotlin, JavaScript, TypeScript, C#, and C++.

## Why?

When working with AI assistants, code can be generated or refactored quickly. While the logic might be sound, the high-level documentation, like module or file-level summaries, often gets overlooked. This tool automates the creation and maintenance of these summaries.

It scans your source files, identifies classes, methods, and functions, and generates a formatted block comment at the top of the file, including the line numbers where each definition appears.

## Installation

The tool is packaged for PyPI. You can install it using `pip`:

```bash
pip install agent-docstrings
```

_Note: You will need to replace this with the actual package name once published._

## Usage

Run the tool from your terminal, providing a list of directories you want to process. It will recursively scan for supported file types in those directories.

```bash
agent-docstrings path/to/your/project/src another/path/to/process
```

### Supported Languages

| Language   | Extensions                          | Comment Style      |
| ---------- | ----------------------------------- | ------------------ |
| Python     | `.py`                               | Triple-quote `"""` |
| Kotlin     | `.kt`                               | KDoc `/** */`      |
| JavaScript | `.js`, `.jsx`                       | JSDoc `/** */`     |
| TypeScript | `.ts`, `.tsx`                       | TSDoc `/** */`     |
| C#         | `.cs`                               | Block `/* */`      |
| C++        | `.cpp`, `.cxx`, `.cc`, `.hpp`, `.h` | Block `/* */`      |

## Contributing

This is an open-source project. Contributions are welcome! Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
