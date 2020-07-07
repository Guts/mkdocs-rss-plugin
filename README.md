# MkDocs RSS plugin

!!! warning

  Under active developement. Very early version.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Use [git log](https://git-scm.com/docs/git-log) to generates RSS 2.0 feeds:

- `feed_rss_created.xml`: using latest **created** pages
- `feed_rss_updated.xml`: using latest **updated** pages

## Installation

> TO DOC

----

## MkDocs configuration

### Required

- [`site_description`](https://www.mkdocs.org/user-guide/configuration/#site_description): used for RSS 2.0 mandatory channel element `description`
- [`site_name`](https://www.mkdocs.org/user-guide/configuration/#site_name): used for RSS 2.0 mandatory channel element `title`
- [`site_url`](https://www.mkdocs.org/user-guide/configuration/#site_url): used for RSS 2.0 mandatory channel element `link` value

### Recomended

- [`site_author`](https://www.mkdocs.org/user-guide/configuration/#site_author)
- [`repo_url`](https://www.mkdocs.org/user-guide/configuration/#repo_url)

### Optional

- [`copyright`](https://www.mkdocs.org/user-guide/configuration/#site_url): used as RSS 2.0 optional `copyright` value

----

## Plugin options

> TO DOC

### Feed TTL

`feed_ttl`: to be inserted as channel `ttl` element. See: [W3C RSS 2.0 documentation](https://validator.w3.org/feed/docs/rss2.html#ltttlgtSubelementOfLtchannelgt).

Unity: minutes
Default: 1440 (= 1 day)

----

## Credits

Inspired from [Tim Vink git-based plugins](https://github.com/timvink?tab=repositories&q=mkdocs-git&type=&language=).

Using magic from:

- [GitPython](https://gitpython.readthedocs.io/)
- [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)
