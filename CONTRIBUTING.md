# Contributing Guidelines

First off, thanks for considering to contribute to this project! :tada::+1:

These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Git hooks

We use git hooks through [pre-commit](https://pre-commit.com/) to enforce and automatically check some "rules". Please install it before to push any commit.

See the relevant configuration file: `.pre-commit-config.yaml`.

## Code Style

Make sure your code *roughly* follows [PEP-8](https://www.python.org/dev/peps/pep-0008/) and keeps things consistent with the rest of the code:

- docstrings: [sphinx-style](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html#the-sphinx-docstring-format) is used to write technical documentation.
- formatting: [black](https://black.readthedocs.io/) is used to automatically format the code without debate.
- sorted imports: [isort](https://pycqa.github.io/isort/) is used to sort imports
- static analisis: [flake8](https://flake8.pycqa.org/en/latest/) is used to catch some dizziness and keep the source code healthy.

----

## IDE

Feel free to use the IDE you love. Here come configurations for some popular IDEs to fit those guidelines.

### Visual Studio Code

```jsonc
{
    "python.pythonPath": ".venv/bin/python",
    // Editor
    "editor.rulers": [
        88
    ],
    "editor.wordWrapColumn": 88,
    "files.associations": {
        "./requirements/*.txt": "pip-requirements"
    },
    // Formatter
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": [
        "--target-version=py38"
    ],
    // Linter
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--config=setup.cfg",
        "--verbose"
    ],
    "python.linting.pylintEnabled": false,
    // Git
    "git.enableCommitSigning": true,
    // Extensions
    "autoDocstring.docstringFormat": "sphinx"
}
```
