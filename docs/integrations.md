---
title: Integrations
icon: octicons/plug-16
---

## Blog plugin (from Material theme)

Since version 1.17, the plugin integrates with the [Blog plugin (shipped with Material theme)](https://squidfunk.github.io/mkdocs-material/plugins/blog/) (see also [the tutorial about blog + RSS  plugins](https://squidfunk.github.io/mkdocs-material/tutorials/blogs/engage/)).

In some cases, the RSS plugin needs to work with the Material Blog:

- for blog posts, the structure of the path to social cards is depending on blog configuration
- retrieve the author's name from the `.authors.yml` file
- optionnaly retrieve the author's email from the `.authors.yml` file

If you don't want this integration, you can disable it with the option: `use_material_blog=false`.

> See [related section in settings](./configuration.md#use_material_blog).

### Example of blog authors with email

```yaml title="docs/blog/.authors.yml"
authors:
  alexvoss:
    name: Alex Voss
    description: Weltenwanderer
    avatar: https://github.com/alexvoss.png
  guts:
    avatar: https://cdn.geotribu.fr/img/internal/contributeurs/jmou.jfif
    description: GIS Watchman
    name: Julien Moura
    url: https://github.com/guts/
    email: joe@biden.com
```

This given Markdown post:

```markdown title="blog/posts/demo.md"
---
authors:
  - alexvoss
  - guts
date: 2024-12-02
categories:
  - tutorial
---

# Demonstration blog post

[...]
```

Will be rendered as:

```xml title="/build/site/feed_rss_created.xml"
[...]
        <item>
            <title>Demonstration blog post</title>
            <author>Alex Voss</author>
            <author>Julien Moura (joe@biden.com)</author>
[...]
```

----

## Social Cards plugin (from Material theme)

Since version 1.10, the plugin integrates with the [Social Cards plugin (shipped with Material theme)](https://squidfunk.github.io/mkdocs-material/setup/setting-up-social-cards/) (see also [the full plugin documentation here](https://squidfunk.github.io/mkdocs-material/plugins/social/)).

Here's how the RSS plugin prioritizes the image to be used in the feed:

1. an image (local path or URL) is defined in the page's YAML header of the page with the key `image`. Typically: `image: path_or_url_to_image.webp`.
1. an image (local path or URL) is defined in the page's YAML header with the key `illustration`. Typically: `illustration: path_or_url_to_image.webp`.
1. if neither is defined, but both the social plugin and the cards option are enabled, then the social card image is used.

If you don't want this integration, you can disable it with the option: `use_material_social_cards=false`.

> See [related section in settings](./configuration.md#use_material_social_cards).

----

## Reference RSS feeds in HTML meta-tags

To facilitate the discovery of RSS feeds, it's recommended to add relevant meta-tags in `<head>` section in HTML pages.

### Automatically set with Material theme

If you're using the Material theme, everything is automagically set up (see [the related documentation page](https://squidfunk.github.io/mkdocs-material/setup/setting-up-a-blog/#rss)) :partying_face:.

### Manually { #feed-discovery-manual-rss }

You need to customize the theme's template. Typically, in `main.html`:

```html
{% extends "base.html" %}

{% block extrahead %}
  <!-- RSS Feed -->
  <link rel="alternate" type="application/rss+xml" title="RSS feed of created content" href="{{ config.site_url }}feed_rss_created.xml">
  <link rel="alternate" type="application/rss+xml" title="RSS feed of updated content" href="{{ config.site_url }}feed_rss_updated.xml">
{% endblock %}
```

----

## Reference JSON feeds in HTML meta-tags

To facilitate the discovery of JSON feeds, it's [recommended](https://www.jsonfeed.org/version/1.1/#discovery-a-name-discovery-a) to add relevant meta-tags in `<head>` section in HTML pages.

### Manually { #feed-discovery-manual-json }

You need to customize the theme's template. Firstly, you need to declare the folder where you store your template overrides:

```yaml title="mkdocs.yml"
[...]
theme:
  name: material
  custom_dir: docs/theme/overrides
[...]
```

Then add a `main.html` inside:

```jinja title="docs/theme/overrides/main.html"
{% extends "base.html" %}

{% block extrahead %}
{# JSON Feed #}
{% if "rss" in config.plugins %}
<link
  rel="alternate"
  type="application/feed+json"
  title="JSON feed" href="{{ 'feed_json_created.json' | url }}"
  />
<link
  rel="alternate"
  type="application/feed+json"
  title="JSON feed of updated content"
  href="{{ 'feed_json_updated.json' | url }}" />
{% endif %}
{% endblock %}
```

If your `main.html` is getting too large, or if you like to modularize anything with more than 3 lines, you can also put this configuration in a separated `partials` file:

```jinja title="content/theme/partials/json_feed.html.jinja2"
{# JSON Feed #}
{% if "rss" in config.plugins %}
<link
  rel="alternate"
  type="application/feed+json"
  title="JSON feed" href="{{ 'feed_json_created.json' | url }}"
  />
<link
  rel="alternate"
  type="application/feed+json"
  title="JSON feed of updated content"
  href="{{ 'feed_json_updated.json' | url }}" />
{% endif %}
```

And include it in `main.html`:

```jinja title="docs/theme/overrides/main.html"
{% include "partials/json_feed.html.jinja2" %}
```
