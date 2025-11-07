---
icon: material/code-block-tags
title: Contribution guide
tags:
    - contribution
    - development
---

First off, thanks for considering to contribute to this project!

These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Development

Once you cloned the repository:

```sh
# install project as editable
python -m pip install -e .

# including development dependencies
python -m pip install -e .[dev]

# including documentation dependencies
python -m pip install -e .[docs]

# including testing dependencies
python -m pip install -e .[test]

# all inclusive
python -m pip install -e .[dev,docs,test]

# install git hooks
pre-commit install
```

Then follow the [contribution guidelines](#guidelines).

### Run the tests

```sh
# install development dependencies
python -m pip install -e .[test]

# run tests
pytest
```

### Build the documentation

```sh
# install dependencies for documentation
python -m pip install -e .[docs]

# build the documentation
mkdocs build
```

### Release workflow

1. Fill the `CHANGELOG.md`
1. Change the version number in `__about__.py`
1. Apply a git tag with the relevant version: `git tag -a 0.3.0 {git commit hash} -m "New awesome feature"`
1. Push tag to main branch: `git push origin 0.3.0`

----

## Guidelines

### Git hooks

We use git hooks through [pre-commit](https://pre-commit.com/) to enforce and automatically check some "rules". Please install it before to push any commit.

See the relevant configuration file: `.pre-commit-config.yaml`.

### Code Style

Make sure your code *roughly* follows [PEP-8](https://www.python.org/dev/peps/pep-0008/) and keeps things consistent with the rest of the code:

- docstrings: [google-style](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html) is used to technically describe what code does or not.
- formatting: [black](https://black.readthedocs.io/) is used to automatically format the code without debate.
- sorted imports: [isort](https://pycqa.github.io/isort/) is used to sort imports
- static analysis: [flake8](https://flake8.pycqa.org/en/latest/) is used to catch some dizziness and keep the source code healthy.

### Pulls requests

Pull requests are really welcome since you take the time to push or modify tests related to the code you edit or create.

----

## IDE proposed settings

Feel free to use the IDE you love. Here come configurations for some popular IDEs to fit those guidelines.

### Visual Studio Code

```jsonc
{
    // JSON
    "[json]": {
        "editor.bracketPairColorization.enabled": true,
        "editor.defaultFormatter": "vscode.json-language-features",
        "editor.formatOnSave": true,
        "editor.guides.bracketPairs": "active"
    },
    "json.format.enable": true,
    "json.schemaDownload.enable": true,
    // Markdown
    "markdown.updateLinksOnFileMove.enabled": "prompt",
    "markdown.updateLinksOnFileMove.enableForDirectories": true,
    "markdown.validate.enabled": true,
    "markdown.validate.fileLinks.markdownFragmentLinks": "warning",
    "markdown.validate.fragmentLinks.enabled": "warning",
    "[markdown]": {
        "editor.bracketPairColorization.enabled": true,
        "editor.formatOnSave": true,
        "editor.guides.bracketPairs": "active",
        "files.trimTrailingWhitespace": false
    },
    // Python
    "python.analysis.autoFormatStrings": true,
    "python.analysis.autoImportCompletions": true,
    "python.analysis.typeCheckingMode": "basic",
    "python.terminal.activateEnvInCurrentTerminal": true,
    "python.terminal.activateEnvironment": true,
    "python.testing.unittestEnabled": true,
    "python.testing.pytestEnabled": true,  
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        },
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.guides.bracketPairs": "active",
        "editor.rulers": [
            88
        ],
        "editor.wordWrapColumn": 88,
    },
    // YAML
    "[yaml]": {
        "editor.autoIndent": "keep",
        "editor.formatOnSave": true,
        "editor.insertSpaces": true,
        "editor.tabSize": 2,
        "diffEditor.ignoreTrimWhitespace": false,
        "editor.quickSuggestions": {
            "other": true,
            "comments": false,
            "strings": true
        }
    },
    // extensions
    "autoDocstring.guessTypes": true,
    "autoDocstring.docstringFormat": "google-notypes",
    "autoDocstring.generateDocstringOnEnter": false,
    "flake8.args": [
        "--verbose"
    ],
    "isort.args": [
        "--profile",
        "black"
    ],
    "isort.check": true,
    "yaml.customTags": [
        "!ENV scalar",
        "!ENV sequence",
        "!relative scalar",
        "tag:yaml.org,2002:python/name:material.extensions.emoji.to_svg",
        "tag:yaml.org,2002:python/name:material.extensions.emoji.twemoji",
        "tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format"
    ]
}
```
