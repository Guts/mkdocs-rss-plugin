# MkDocs RSS plugin

[![PyPi version badge](https://badgen.net/pypi/v/mkdocs-rss-plugin)](https://pypi.org/project/mkdocs-rss-plugin/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-rss-plugin)](https://pypi.org/project/mkdocs-rss-plugin/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-rss-plugin)](https://pypi.org/project/mkdocs-rss-plugin/)

[![codecov](https://codecov.io/gh/Guts/mkdocs-rss-plugin/branch/master/graph/badge.svg?token=A0XPLKiwiW)](https://codecov.io/gh/Guts/mkdocs-rss-plugin)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![flake8](https://img.shields.io/badge/linter-flake8-green)](https://flake8.pycqa.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Guts/mkdocs-rss-plugin/master.svg)](https://results.pre-commit.ci/latest/github/Guts/mkdocs-rss-plugin/master)
[![📚 Documentation](https://github.com/Guts/mkdocs-rss-plugin/actions/workflows/documentation.yml/badge.svg)](https://github.com/Guts/mkdocs-rss-plugin/actions/workflows/documentation.yml)

A plugin for [MkDocs](https://www.mkdocs.org), the static site generator, which creates [RSS 2.0](https://wikipedia.org/wiki/RSS) feeds using the creation and modification dates from [git log](https://git-scm.com/docs/git-log) and page metadata ([YAML frontmatter](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data)).

## Usage

Minimal [`mkdocs.yml` configuration](https://www.mkdocs.org/user-guide/configuration/#project-information):

```yaml
site_description: required. Used as feed mandatory channel description.
site_name: required. Used as feed mandatory channel title and items source URL label.
site_url: required. Used to build feed items URLs.
```

Minimal plugin option:

```yaml
plugins:
  - rss
```

Full options:

```yaml
plugins:
  - rss:
      abstract_chars_count: 160  # -1 for full content
      comments_path: "#__comments"
      date_from_meta:
        as_creation: "date"
        as_update: false
        datetime_format: "%Y-%m-%d %H:%M"
      feed_ttl: 1440
      image: https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Feed-icon.svg/128px-Feed-icon.svg.png
      length: 20
      pretty_print: false
      match_path: ".*"
      url_parameters:
        utm_source: "documentation"
        utm_medium: "RSS"
        utm_campaign: "feed-syndication"
```

For further information, [see the user documentation](https://guts.github.io/mkdocs-rss-plugin/).

## Development

Clone the repository:

```bash
# install project as editable
python -m pip install -U -r requirements.txt

# install development dependencies
python -m pip install -U -r requirements/development.txt

# install git hooks
pre-commit install

# run tests
pytest

# install dependencies for documentation
python -m pip install -U -r requirements/documentation.txt
```

Then follow the [contribution guidelines](CONTRIBUTING.md).
