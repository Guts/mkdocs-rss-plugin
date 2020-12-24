---
title: Configuration
date: 2020-12-31 14:20
description: Configuration steps and settings for MkDocs RSS plugin
image: "https://svgsilh.com/png-512/97849.png"
---

# Configuration

To produce a valid RSS feed, the plugin uses:

- some global settings from [MkDocs configuration](#mkdocs-configuration)
- some [page attributes](#page-attributes)
- some [specific settings](#plugin-options) to custom behavior or add some optional elements

## MkDocs configuration

| Setting | Expected level | Corresponding RSS element |
| :------ | :------------: | :------------------------ |
| [`site_description`](https://www.mkdocs.org/user-guide/configuration/#site_description) | **required** | [`description`](https://www.w3schools.com/xml/rss_tag_title_link_description_channel.asp) |
| [`site_name`](https://www.mkdocs.org/user-guide/configuration/#site_name) | **required** | [`title`](https://www.w3schools.com/xml/rss_tag_title_link_description_channel.asp) and also as [`source` URL label](https://www.w3schools.com/xml/rss_tag_source.asp) for each feed item |
| [`site_url`](https://www.mkdocs.org/user-guide/configuration/#site_url) | **required** | [`link`](https://www.w3schools.com/xml/rss_tag_title_link_description_channel.asp) |
| ---- | ---- | ---- |
| [`repo_url`](https://www.mkdocs.org/user-guide/configuration/#repo_url) | **recomended** | [`docs`](https://www.w3schools.com/xml/rss_tag_docs.asp) |
| [`site_author`](https://www.mkdocs.org/user-guide/configuration/#site_author) | **recomended** | [`managingEditor`](https://www.w3schools.com/xml/rss_tag_managingeditor.asp) |
| ---- | ---- | ---- |
| [`copyright`](https://www.mkdocs.org/user-guide/configuration/#copyright) | *optional* | [`copyright`](https://www.w3schools.com/xml/rss_tag_copyright.asp) |
| [`locale` or `theme/locale` or `theme/language`](https://github.com/squidfunk/mkdocs-material/issues/1350#issuecomment-559095892) | *optional* | [`language`](https://www.w3schools.com/xml/rss_tag_language.asp) |

### Automatic elements

| Variable / value | Corresponding RSS element |
| :---- | :------------------------ |
| MkDocs [build timestamp](https://github.com/mkdocs/mkdocs/blob/ff0b7260564e65b6547fd41753ec971e4237823b/mkdocs/utils/__init__.py#L83-L94) | optional channel elements [`lastBuildDate`](https://www.w3schools.com/xml/rss_tag_lastbuilddate.asp) and [`pubDate`](https://www.w3schools.com/xml/rss_tag_pubdate.asp) |
| MkDocs RSS plugin - v*1.0.0* | optional channel elements [`generator`](https://www.w3schools.com/xml/rss_tag_generator.asp) |

----

## Page attributes

Basically, each page is an item element in the RSS feed.

| Attribute | Expected level | Corresponding RSS element |
| :------ | :------------: | :------------------------ |
| [`page.canonical_url`](https://github.com/mkdocs/mkdocs/blob/master/mkdocs/structure/pages.py#L97-L105) | **required** and *optional* | mandatory item element [`link`](https://www.w3schools.com/xml/rss_tag_title_link_description_item.asp) and also used as [`guid`](https://www.w3schools.com/xml/rss_tag_guid.asp) |
| [`page.meta.title`](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) | **required** | [`title`](https://www.w3schools.com/xml/rss_tag_title_link_description_item.asp) |
| [`page.meta.description`](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) if present, else extract headlines from the content. See below the [item_description_length option](http://localhost:8000/configuration/#item-description-length). | **required** | [`description`](https://www.w3schools.com/xml/rss_tag_title_link_description_item.asp) |
| creation or last update datetime according git log. If not possible, then use [MkDcos build date](https://github.com/mkdocs/mkdocs/blob/master/mkdocs/utils/__init__.py#L111-L118) | **recomended** | [`pubDate`](https://www.w3schools.com/xml/rss_tag_pubdate_item.asp) |
| [`page.meta.image`](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) | *optional* | item element [`enclosure`](https://www.w3schools.com/xml/rss_tag_enclosure.asp). Some HTTP requests can be performed to retrieve remote images length. |

----

## Plugin options

Sample:

```yaml
plugins:
  - rss:
      abstract_chars_count: 150
      feed_ttl: 1440
      image: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Feed-icon.svg/128px-Feed-icon.svg.png'
      length: 20
```

### Channel image

`image`: URL to image to use as feed illustration.

Default: `None`.

Output:

```xml
<image>
  <url>
    https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Feed-icon.svg/128px-Feed-icon.svg.png
  </url>
  <title>MkDocs RSS Plugin</title>
  <link>https://guts.github.io/mkdocs-rss-plugin/</link>
</image>
```

### Feed length

`length`: number of pages to include as feed items (entries).

Default: `20`

### Feed TTL

`feed_ttl`: number of minutes to be cached. Inserted as channel `ttl` element. See: [W3C RSS 2.0 documentation](https://www.w3schools.com/xml/rss_tag_ttl.asp).

Default: `1440` (= 1 day)

Output:

```xml
<ttl>1440</ttl>
```

### Item description length

To fill each [item description element](https://www.w3schools.com/xml/rss_tag_title_link_description_item.asp), the plugin first tries to retrieve the value of the keyword `description` from the [page metadata].

If the page has no meta, then the plugin retrieves the first number of characters of the page content defined by this setting. Retrieved content is raw markdown.

`abstract_chars_count`: number of characters to use as item description.

Default: `150`

### Dates overriding

Basically, the plugin aims to retrieve creation and update dates from git log. But sometimes, it does not match the content workflow: markdown generated from sources, .

So, it's possible to use the dates manually specified into the [page metadata] through the [YAML frontmatter](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data).

- `as_creation`: meta tag name to use as creation date. Default to False.
- `as_update`: meta tag name to use as update date. Default to False.
- `datetime_format`: datetime format. Default to "%Y-%m-%d %H:%M".

#### Example

For example, in your `best_article.md` created in 2019, you can write the front-matter like this:

```markdown
---
title: "This page title is a perfect clickbait!"
authors: ["Julien M."]
date: "2020-10-22 17:18"
---

# This plugin will change your MkDocs life

Lorem ipsum [...]
```

So in your `mkdocs.yml` you will have:

```yaml
plugins:
  - rss:
      date_from_meta:
        as_creation: "date"
        as_update: false
        datetime_format: "%Y-%m-%d %H:%M"
```

At the end, into the RSS you will get:

```xml
<item>
  <title>This page title is a perfect clickbait!</title>
  <link>https://website.com/articles/best_article/</link>
  <pubDate>Thu, 22 Oct 2020 17:18:00 -0000</pubDate>
  [...]

</item>
```

----

## Integration

### Reference RSS feeds in HTML meta-tags

To facilitate the discovery of RSS feeds, it's recomended to add relevant meta-tags into the pages `<head>`, through template customization in `main.html` :

```html
{% extends "base.html" %}

{% block extrahead %}
  <!-- RSS Feed -->
  <link rel="alternate" type="application/rss+xml" title="RSS feed of created content" href="/feed_rss_created.xml">
  <link rel="alternate" type="application/rss+xml" title="RSS feed of updated content" href="/feed_rss_updated.xml">
{% endblock %}
```

<!-- Hyperlinks reference -->
[page metadata]: https://python-markdown.github.io/extensions/meta_data/
