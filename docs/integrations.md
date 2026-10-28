---
title: Integrations
icon: octicons/plug-16
---

Since version 1.19, the plugin supports both [Material for Mkdocs](https://squidfunk.github.io/mkdocs-material/) (which is in maintenance mode since Nov 11, 2025 and until November 2026) and its fork [MaterialX](https://jaywhj.github.io/mkdocs-materialx/).

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

----

## Display a recent updates page from the JSON feed

The updated JSON feed can also be used inside your documentation site to render a small "recently updated pages" index. This is useful for documentation portals or digital gardens where readers may want to see what changed recently without using a feed reader.

First, keep the updated JSON feed enabled and expose enough entries for the page:

```yaml title="mkdocs.yml"
plugins:
  - rss:
      length: 20
      match_path: '^(?!updates\.md$).*\.md$'
      feeds_filenames:
        json_updated: feed_json_updated.json

theme:
  name: material
  custom_dir: docs/theme/overrides

extra_javascript:
  - javascripts/recent-updates.js

nav:
  - Recently updated: updates.md
```

Merge these entries into your existing configuration, including any existing theme overrides. Add the `Recently updated` entry to your existing `nav`; copying this `nav` block as-is replaces the whole site navigation with a single entry.

The page shows all entries in the generated updated JSON feed, up to the configured `length`. This example excludes only `updates.md`; adapt `match_path` to select the content you want to include, such as `'blog/posts/.*'` for blog posts.

Then create the page and select a custom template:

```markdown title="docs/updates.md"
---
template: updates.html
---

# Recently updated

Sorted by last update date from the updated feed. This page is excluded.
```

Add the template below to your theme override directory. The `url` filter resolves the feed path for both values of `use_directory_urls` and for sites hosted under a subpath. Keep the filename in sync with `feeds_filenames.json_updated` if you change it.

```jinja title="docs/theme/overrides/updates.html"
{% extends "main.html" %}

{% block content %}
  {{ super() }}
  <p><a id="updates-feed" href="{{ 'feed_json_updated.json' | url }}">JSON feed</a></p>
  <div data-recent-updates aria-live="polite">Loading updates...</div>
  <noscript><p>Enable JavaScript to display the list, or use the JSON feed link.</p></noscript>
{% endblock %}
```

Finally, add a script that fetches the JSON feed and renders its entries in feed order. It subscribes to [Material's page lifecycle](https://squidfunk.github.io/mkdocs-material/customization/#additional-javascript) so it also runs after instant navigation:

```javascript title="docs/javascripts/recent-updates.js"
(function () {
  function initUpdates() {
    var root = document.querySelector("[data-recent-updates]");

    if (!root) {
      return;
    }

    fetch(document.getElementById("updates-feed").href, { cache: "no-store" })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Unable to load updates feed");
        }

        return response.json();
      })
      .then(function (feed) {
        var items = Array.isArray(feed.items) ? feed.items : [];

        if (!items.length) {
          root.textContent = "No recent updates found.";
          return;
        }

        var list = document.createElement("ol");

        items.forEach(function (item) {
          var entry = document.createElement("li");
          var link = document.createElement("a");
          var summary = document.createElement("p");
          var time = document.createElement("time");
          var date = item.date_modified || item.date_published || "";

          link.href = item.url;
          link.textContent = item.title || item.url;
          summary.textContent = itemSummary(item);
          time.dateTime = date;
          time.textContent = formatDate(date);

          entry.appendChild(link);
          entry.appendChild(summary);
          entry.appendChild(time);
          list.appendChild(entry);
        });

        root.replaceChildren(list);
      })
      .catch(function () {
        root.textContent = "Unable to load recent updates.";
      });
  }

  function formatDate(value) {
    var date = new Date(value);

    if (Number.isNaN(date.getTime())) {
      return value;
    }

    return date.toLocaleString(undefined, {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  function itemSummary(item) {
    var template = document.createElement("template");

    template.innerHTML = item.content_html || "";
    var text = (template.content.textContent || "").replace(/\s+/g, " ").trim();

    return text.length > 160 ? text.slice(0, 160) + "..." : text;
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(initUpdates);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initUpdates);
  } else {
    initUpdates();
  }
})();
```

The example uses the updated feed (`feed_json_updated.json`) to answer "what changed recently?". Dates come from Git or page metadata according to your [`date_from_meta` configuration](configuration.md#date_from_meta).

This is a client-side enhancement. Readers without JavaScript can still use the direct feed link, but the list itself is rendered in the browser.
