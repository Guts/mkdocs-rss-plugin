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

The updated JSON feed can also be used inside your documentation site to render a
small "recently updated pages" index. This is useful for documentation portals or
digital gardens where readers may want to see what changed recently without using
a feed reader.

First, keep the updated JSON feed enabled and expose enough entries for the page:

```yaml title="mkdocs.yml"
plugins:
  - rss:
      length: 100
      match_path: "^(?!updates\\.md$)(?!.*(?:^|/)(README|index)\\.md$).+\\.md$"
      feeds_filenames:
        json_updated: feed_json_updated.json

extra_javascript:
  - javascripts/recent-updates.js

nav:
  - Recently updated: updates.md
```

The page can only show entries that are present in the generated JSON feed. Set
`length` to at least the maximum number of updates you want readers to browse.

Then create a page that contains the target container and optional direct feed
links:

```markdown title="docs/updates.md"
# Recently updated

<p class="updates-note">
  Sorted by Git last-modified time from the updated feed. Index pages and this
  page are excluded.
</p>

<p class="updates-feeds">
  <a href="../feed_json_updated.json">JSON feed</a>
</p>

<div data-recent-updates data-page-size="20">
  Loading updates...
</div>
```

Finally, add a small script that fetches the JSON feed and progressively renders
entries:

```javascript title="docs/javascripts/recent-updates.js"
(function () {
  var root = document.querySelector("[data-recent-updates]");

  if (!root) {
    return;
  }

  function feedUrl() {
    return new URL("../feed_json_updated.json", window.location.href).toString();
  }

  function itemDate(item) {
    return item.date_modified || item.date_published || item.date_created || "";
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
    var container = document.createElement("div");
    var text = "";

    container.innerHTML = item.content_html || item.summary || "";
    text = (container.textContent || "").replace(/\s+/g, " ").trim();

    return text.length > 160 ? text.slice(0, 160) + "..." : text;
  }

  function render(items) {
    var pageSize = parseInt(root.getAttribute("data-page-size") || "20", 10);
    var visibleCount = Math.min(pageSize, items.length);
    var list = document.createElement("ol");
    var button = document.createElement("button");

    function renderVisibleItems() {
      list.innerHTML = "";

      items.slice(0, visibleCount).forEach(function (item) {
        var entry = document.createElement("li");
        var link = document.createElement("a");
        var summary = document.createElement("p");
        var time = document.createElement("time");
        var date = itemDate(item);

        link.href = item.url || item.id || "#";
        link.textContent = item.title || link.href;
        summary.textContent = itemSummary(item);
        time.dateTime = date;
        time.textContent = formatDate(date);

        entry.appendChild(link);
        entry.appendChild(summary);
        entry.appendChild(time);
        list.appendChild(entry);
      });

      button.hidden = visibleCount >= items.length;
    }

    button.type = "button";
    button.textContent = "Show more updates";
    button.addEventListener("click", function () {
      visibleCount = Math.min(visibleCount + pageSize, items.length);
      renderVisibleItems();
    });

    root.replaceChildren(list, button);
    renderVisibleItems();
  }

  fetch(feedUrl(), { cache: "no-store" })
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

      render(items);
    })
    .catch(function () {
      root.textContent = "Unable to load recent updates.";
    });
})();
```

The example intentionally uses the updated feed (`feed_json_updated.json`) rather
than the created feed, because the page is meant to answer "what changed
recently?". You can adapt `match_path` to include only blog posts, release notes,
or any other section of your documentation.

This is a client-side enhancement. Readers without JavaScript can still use the
direct feed link, but the list itself is rendered in the browser.
