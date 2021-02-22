# MkDocs RSS plugin

[![PyPi version badge](https://badgen.net/pypi/v/mkdocs-rss-plugin)](https://pypi.org/project/mkdocs-rss-plugin/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-rss-plugin)](https://pypi.org/project/mkdocs-rss-plugin/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-rss-plugin)](https://pypi.org/project/mkdocs-rss-plugin/)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Documentation Status](https://readthedocs.org/projects/mkdocs-rss-plugin/badge/?version=latest)](https://mkdocs-rss-plugin.readthedocs.io/en/latest/?badge=latest)

A plugin for [MkDocs](https://www.mkdocs.org), the static site generator, which creates [RSS 2.0](https://wikipedia.org/wiki/RSS) feeds using the creation and modification dates from [git log](https://git-scm.com/docs/git-log).

## Usage

Typical `mkdocs.yml`:

```yaml
plugins:
  - rss:
      abstract_chars_count: 160
      date_from_meta:
        as_creation: "date"
        as_update: false
        datetime_format: "%Y-%m-%d %H:%M"
      feed_ttl: 1440
      image: https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Feed-icon.svg/128px-Feed-icon.svg.png
      length: 20
      pretty_print: false
      match_path: ".*"
```

For further information, [see the user documentation](https://guts.github.io/mkdocs-rss-plugin/).

## Development

For further information, [see the technical documentation](https://mkdocs-rss-plugin.readthedocs.io/).
