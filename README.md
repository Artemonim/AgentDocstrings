# Agent Docstrings

A command-line tool to auto-generate and update file-level docstrings summarizing classes and functions. Useful for maintaining a high-level overview of your files, especially in projects with code generated or modified by AI assistants.

Supports Python, Kotlin, JavaScript, TypeScript, C#, and C++.

## Why?

When working in Cursor and similar IDEs, Agents often start reading files from the beginning. And regarding Cursor's behavior during the script's creation, in normal mode, the model reads 250 lines of code per call, and in MAX mode, 750 lines. However, I have projects with files over 1000 lines of code, which are not very appropriate to divide into smaller files. And anyway, Agent still have to call reading tools for each individual file.

At the same time, the Agent can choose from which line to read the file. It can navigate and surf within your repository. The script literally provides the Agent with the table of contents of the current file, so that immediately after the first read, the Agent understands the entire structure and can read the file from a specific line, rather than trying to get to it (while also potentially making mistakes along the way).

In addition to the advantage of quick navigation, the initial docstring also serves as a method to reduce context window usage. For example, if a required method in a 900-line file is on line 856, the Agent will only read lines 1-250 and 856-900, instead of sequentially going to the desired forty lines and filling its context with unnecessary code.

## Installation

The tool ~~is~~ _will be_ packaged for PyPI. You can install it using `pip`:

```bash
pip install agent-docstrings
```

_=== TODO: Replace this with the actual package name once published. ===_

## Usage

_I run this tool automatically within code quality check scripts. I plan to publish them in the near future._

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
