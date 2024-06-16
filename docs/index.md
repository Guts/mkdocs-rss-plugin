---
title: The MkDocs RSS Plugin
authors:
  - dev@ingeoveritas.com (Julien Moura)
  - vinktim@gmail.com (Tim Vink)
date: 2020-07-06
description: "MkDocs RSS plugin: generate RSS and JSON feeds for your static website using git log ad YAML frontmatter (markdown pages'metadata header)."
image: "assets/rss_icon.svg"
tags:
  - JSON Feed
  - Mkdocs
  - plugin
  - RSS
---

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

A plugin for [MkDocs](https://www.mkdocs.org), the static site generator, which creates [RSS 2.0](https://wikipedia.org/wiki/RSS) and [JSON Feed 1.1](https://www.jsonfeed.org/version/1.1/) feeds using the creation and modification dates from [git log](https://git-scm.com/docs/git-log) and page metadata ([YAML frontmatter](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data)).

## Quickstart

Installation:

<!-- termynal: {"prompt_literal_start": [">"], title: Terminal} -->

```sh
> pip install mkdocs-rss-plugin
---> 100%
RSS plugin for Mkdocs installed! Add 'rss' to your 'plugins' section in mkdocs.yml
```

Then in your `mkdocs.yml`:

```yaml
site_description: required. Used as feed mandatory channel description.
site_name: required. Used as feed mandatory channel title and items source URL label.
site_url: required. Used to build feed items URLs.

plugins:
  - rss
```

----

## Example

As examples, here are the feeds generated for this documentation:

- [feed_rss_created.xml](feed_rss_created.xml) and [feed_json_created.json](feed_json_created.json) for  latest **created** pages: [W3C validator](https://validator.w3.org/feed/check.cgi?url=https%3A//guts.github.io/mkdocs-rss-plugin/feed_rss_created.xml)
- [feed_rss_updated.xml](feed_rss_updated.xml) and [feed_json_updated.json](feed_json_updated.json) for latest **updated** pages: [W3C validator](https://validator.w3.org/feed/check.cgi?url=https%3A//guts.github.io/mkdocs-rss-plugin/feed_rss_updated.xml)

Or it could be displayed as a RSS or Feedly follow button:

[![RSS logo](assets/rss_icon.svg "Subscribe to our RSS"){: width=130  loading=lazy }](https://guts.github.io/mkdocs-rss-plugin/feed_rss_created.xml)
[![Feedly button](https://s3.feedly.com/img/follows/feedly-follow-rectangle-flat-big_2x.png "Follow us on Feedly"){: width=130 loading=lazy }](https://feedly.com/i/subscription/feed%2Fhttps%3A%2F%2Fguts.github.io%2Fmkdocs-rss-plugin%2Ffeed_rss_created.xml)
{: align=middle }

For JSON Feed, you can use the icon:

[![JSON Feed icon](https://raw.githubusercontent.com/manton/JSONFeed/master/graphics/icon.png){: width=130 loading=lazy }](https://guts.github.io/mkdocs-rss-plugin/feed_json_created.json)
{: align=middle }

!!! tip
    See how to make your [RSS](integrations.md#reference-rss-feeds-in-html-meta-tags) and [JSON](integrations.md#reference-json-feeds-in-html-meta-tags) discoverable.

----

## Credits

![RSS logo](assets/rss_icon.svg "RSS icon - Wikimedia"){: align=right }

- Plugin logic is inspired from [Tim Vink git-based plugins](https://github.com/timvink?tab=repositories&q=mkdocs-git&type=&language=) and main parts of Git stuff are nearly copied/pasted.
- Using magic mainly from:
  - [GitPython](https://gitpython.readthedocs.io/)
  - [Jinja2](https://jinja.palletsprojects.com/)
- Documentation colors are a tribute to the classic RSS color scheme: orange and white.
- Logo generated with DALL·E.
