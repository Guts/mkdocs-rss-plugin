---
title: The MkDocs RSS Plugin
authors: ["dev@ingeoveritas.com (Julien Moura)", "vinktim@gmail.com (Tim Vink)"]
date: 2020-07-06
description: "MkDocs RSS plugin: generate RSS feeds for your static website using git log."
image: "rss_icon.svg"
---

--8<-- "README.md"

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

## Example

As examples, here come the feeds generated for this documentation:

- [feed_rss_created.xml](feed_rss_created.xml) for  latest **created** pages: [W3C validator](https://validator.w3.org/feed/check.cgi?url=https%3A//guts.github.io/mkdocs-rss-plugin/feed_rss_created.xml)
- [feed_rss_updated.xml](feed_rss_updated.xml) for latest **updated** pages: [W3C validator](https://validator.w3.org/feed/check.cgi?url=https%3A//guts.github.io/mkdocs-rss-plugin/feed_rss_updated.xml)

Or it could be displayed as a Feedly follow button:

[![Feedly button](https://s3.feedly.com/img/follows/feedly-follow-rectangle-flat-big_2x.png "Follow us on Feedly"){: width=130 height= 50 loading=lazy }](https://feedly.com/i/subscription/feed%2Fhttps%3A%2F%2Fguts.github.io%2Fmkdocs-rss-plugin%2Ffeed_rss_created.xml)

## Credits

![RSS logo](rss_icon.svg "RSS icon - Wikimedia"){: align=right }

Plugin logic is inspired from [Tim Vink git-based plugins](https://github.com/timvink?tab=repositories&q=mkdocs-git&type=&language=) and main parts of Git stuff are nearly copied/pasted.

Using magic from:

- [GitPython](https://gitpython.readthedocs.io/)
- [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)

Documentation theme [United from mkdocs-bootswatch](https://mkdocs.github.io/mkdocs-bootswatch/#united) as a tribute to the classic RSS color scheme: orange and white.
