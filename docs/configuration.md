---
title: Configuration
author: "Julien Moura"
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
| creation or last update datetime according git log. Can be overridden by dates in page.meta. If not, then it uses [MkDcos build date](https://github.com/mkdocs/mkdocs/blob/master/mkdocs/utils/__init__.py#L111-L118) | **recomended** | [`pubDate`](https://www.w3schools.com/xml/rss_tag_pubdate_item.asp) |
| [`page.meta.image`](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) | *optional* | item element [`enclosure`](https://www.w3schools.com/xml/rss_tag_enclosure.asp). Some HTTP requests can be performed to retrieve remote images length. |
| [`page.meta.authors`](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) or `page.meta.author`. Accepted value types: `str` `list`, `tuple`. <br />To comply with the standard, the page writer is responsible to fill this field following this syntax: `john@doe.com (John Doe)` ([read this SO](https://stackoverflow.com/a/6079731/2556577)). | *optional* | [`author`](https://www.w3schools.com/XML/rss_tag_author.asp) |

----

## Plugin options

For a sample see [homepage](/#usage).

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

### Item comments path

`comments_path`: path to add to each item URL pointing.

Default: `None`.

For example, if you're using Material for Mkdocs with comment integration (Disqus or Isso), the comment block is under the div id `__comments`, so you can set: `comments_path: "#__comments"` and the output will be:

```xml
<item>
  <title>This page title is a perfect clickbait!</title>
  <link>https://website.com/articles/best_article/</link>
  <comments>https://website.com/articles/best_article/#__comments</comments>
  [...]

</item>
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

To fill each [item description element](https://www.w3schools.com/xml/rss_tag_title_link_description_item.asp):

- If this value is set to `-1`, then the articles' full HTML content will be filled into the description element.
- Otherwise, the plugin first tries to retrieve the value of the keyword `description` from the [page metadata].
- If the value is non-negative and no `description` meta is found, then the plugin retrieves the first number of characters of the page content defined by this setting. Retrieved content is the raw markdown converted rougthly into HTML.

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

### Prettified output

By default, the output file is minified, using Jinja2 strip options and manual work. It's possible to disable it and prettify the output using `pretty_print: true`.

```yaml
plugins:
  - rss:
      pretty_print: true
```

Default: `False`.

### Filter pages

This adds a `match_path` option which should be a regex pattern matching the path to your files within the `docs_dir`. For example if you had a blog under `docs/blog` where `docs_dir` is `docs` you might use:

```yaml
plugins:
  - rss:
      match_path: "blog/.*"
```

Since `match_path` gives you all the power of regular expressions you can have more complex patterns to include multiple directories. For example, to include all pages under both `release-notes` and `articles`:

```yaml
plugins:
  - rss:
      match_path: "(release-notes|articles)/.*"
```

Default: `.*`.

### URL parameters

This option allows you to add parameters to the URLs of the RSS feed items. It works as a dictionary of keys/values that is passed to [Python *urllib.parse.urlencode*](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode).  
One possible use case is the addition of [Urchin Tracking Module (UTM) parameters](https://en.wikipedia.org/wiki/UTM_parameters):

```yaml
plugins:
  - rss:
      url_parameters:
        utm_source: "documentation"
        utm_medium: "RSS"
        utm_campaign: "feed-syndication"
```

Will result in:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<rss>
    [...]
    <item>
      [...]
      <link>https://guts.github.io/mkdocs-rss-plugin/?utm_source=documentation&amp;utm_medium=RSS&amp;utm_campaign=feed-syndication</link>
      [...]
    </item>
    [...]
  </channel>
</rss>
```

Default: `None`.

----

## Integration

### Reference RSS feeds in HTML meta-tags

To facilitate the discovery of RSS feeds, it's recomended to add relevant meta-tags into the pages `<head>`, through template customization in `main.html` :

```html
{% extends "base.html" %}

{% block extrahead %}
  <!-- RSS Feed -->
  <link rel="alternate" type="application/rss+xml" title="RSS feed of created content" href="{{ config.site_url }}feed_rss_created.xml">
  <link rel="alternate" type="application/rss+xml" title="RSS feed of updated content" href="{{ config.site_url }}feed_rss_updated.xml">
{% endblock %}
```

<!-- Hyperlinks reference -->
[page metadata]: https://python-markdown.github.io/extensions/meta_data/
