# Contributing Guidelines

First off, thanks for considering to contribute to this project!

These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Git hooks

We use git hooks through [pre-commit](https://pre-commit.com/) to enforce and automatically check some "rules". Please install it before to push any commit.

See the relevant configuration file: `.pre-commit-config.yaml`.

## Code Style

Make sure your code *roughly* follows [PEP-8](https://www.python.org/dev/peps/pep-0008/) and keeps things consistent with the rest of the code:

- docstrings: [sphinx-style](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html#the-sphinx-docstring-format) is used to write technical documentation.
- formatting: [black](https://black.readthedocs.io/) is used to automatically format the code without debate.
- sorted imports: [isort](https://pycqa.github.io/isort/) is used to sort imports
- static analysis: [flake8](https://flake8.pycqa.org/en/latest/) is used to catch some dizziness and keep the source code healthy.

## Pulls requests

Pull requests are really welcome since you take the time to push or modify tests related to the code you edit or create.

----

## IDE

Feel free to use the IDE you love. Here come configurations for some popular IDEs to fit those guidelines.

### Visual Studio Code

```jsonc
{
    // Editor
    "files.associations": {
        "./requirements/*.txt": "pip-requirements"
    },
    // Python
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        },
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.guides.bracketPairs": "active",
        "editor.rulers": [
            88
        ],
        "editor.wordWrapColumn": 88,
    },
    "flake8.args": [
        "--config=setup.cfg",
        "--verbose"
    ],
    "isort.args": [
        "--profile",
        "black"
    ],
    "isort.check": true,
    // extensions
    "autoDocstring.guessTypes": true,
    "autoDocstring.docstringFormat": "google",
    "autoDocstring.generateDocstringOnEnter": false,
}
```
