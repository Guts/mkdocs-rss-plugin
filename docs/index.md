---
title: The MkDocs RSS Plugin
description: "MkDocs RSS plugin: generate RSS feeds for your static website using git logq" 
---

# MkDocs RSS Plugin

Plugin for [MkDocs](https://www.mkdocs.org) using [git log](https://git-scm.com/docs/git-log) to generates two [RSS 2.0](https://wikipedia.org/wiki/RSS) feeds:

- [feed_rss_created.xml](feed_rss_created.xml) for  latest **created** pages
- [feed_rss_updated.xml](feed_rss_updated.xml) for latest **updated** pages

## Quickstart

Installation:

```bash
pip install mkdocs-rss-plugin
```

Then in your `mkdocs.yml`:

```yml
plugins:
  - rss
```

## Credits

Plugin logic is inspired from [Tim Vink git-based plugins](https://github.com/timvink?tab=repositories&q=mkdocs-git&type=&language=) and main Git stuff is nearly copied/pasted.

Using magic from:

- [GitPython](https://gitpython.readthedocs.io/)
- [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)

Documentation theme [United from mkdocs-bootswatch](http://mkdocs.github.io/mkdocs-bootswatch/#united) as a tribute to the classic RSS color scheme: orange and white.
