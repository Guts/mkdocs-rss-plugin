# MkDocs RSS plugin

[![PyPi version badge](https://badgen.net/pypi/v/mkdocs-rss-plugin)](https://pypi.org/project/mkdocs-rss-plugin/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-rss-plugin)](https://pypi.org/project/mkdocs-rss-plugin/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-rss-plugin)](https://pypi.org/project/mkdocs-rss-plugin/)

[![codecov](https://codecov.io/gh/Guts/mkdocs-rss-plugin/branch/main/graph/badge.svg?token=A0XPLKiwiW)](https://codecov.io/gh/Guts/mkdocs-rss-plugin)
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
      abstract_delimiter: <!-- more -->
      categories:
        - tags
      comments_path: "#__comments"
      date_from_meta:
        as_creation: "date"
        as_update: false
        datetime_format: "%Y-%m-%d %H:%M"
        default_timezone: Europe/Paris
        default_time: "09:30"
      enabled: true
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

Following initiative from the author of Material for MkDocs, this plugin provides its own JSON schema to validate configuration: [source](https://github.com/Guts/mkdocs-rss-plugin/blob/main/docs/schema.json) - [documentation](https://guts.github.io/mkdocs-rss-plugin/schema.json).

## Development

Clone the repository. If you are not a collaborator then first [fork it
on GitHub](https://github.com/Guts/mkdocs-rss-plugin/fork) and clone
your fork. Change into the directory that contains the code, then:

```bash
# install development dependencies
python -m pip install -U -r requirements/development.txt
# alternatively: pip install -e .[dev]

# install project as editable
python -m pip install -e .

# install git hooks
pre-commit install

# run tests
pytest

# install dependencies for documentation
python -m pip install -U -r requirements/documentation.txt
# alternatively: pip install -e .[doc]
```

Then follow the [contribution guidelines](https://github.com/Guts/mkdocs-rss-plugin/blob/main/CONTRIBUTING.md)

## Release workflow

1. Fill the `CHANGELOG.md`
1. Change the version number in `__about__.py`
1. Apply a git tag with the relevant version: `git tag -a 0.3.0 {git commit hash} -m "New awesome feature"`
1. Push tag to main branch: `git push origin 0.3.0`
