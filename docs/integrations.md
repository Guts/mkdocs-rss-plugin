---
title: Integrations
icon: octicons/plug-16
---

## Reference RSS feeds in HTML meta-tags

To facilitate the discovery of RSS feeds, it's recommended to add relevant meta-tags in `<head>` section in HTML pages.

### Automatically set with Material theme

If you're using the Material theme, everything is automagically set up (see [the related documentation page](https://squidfunk.github.io/mkdocs-material/setup/setting-up-a-blog/#rss)) :partying_face:.

### Manually

You need to customize the theme's template. Typically, in `main.html`:

```html
{% extends "base.html" %}

{% block extrahead %}
  <!-- RSS Feed -->
  <link rel="alternate" type="application/rss+xml" title="RSS feed of created content" href="{{ config.site_url }}feed_rss_created.xml">
  <link rel="alternate" type="application/rss+xml" title="RSS feed of updated content" href="{{ config.site_url }}feed_rss_updated.xml">
{% endblock %}
```
