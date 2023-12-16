---
title: Configuration
authors:
  - dev@ingeoveritas.com (Julien Moura)
date: 2020-12-31 14:20
description: Configuration steps and settings for MkDocs RSS plugin
icon: material/book-cog
image: https://svgsilh.com/png-512/97849.png
tags:
  - settings
  - options
  - plugin
---

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
| [`repo_url`](https://www.mkdocs.org/user-guide/configuration/#repo_url) | **recommended** | [`docs`](https://www.w3schools.com/xml/rss_tag_docs.asp) |
| [`site_author`](https://www.mkdocs.org/user-guide/configuration/#site_author) | **recommended** | [`managingEditor`](https://www.w3schools.com/xml/rss_tag_managingeditor.asp) |
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
| [`page.meta.description`](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) if present, else extract headlines from the content. See below the [item_description_length option](#item-description-length). | **required** | [`description`](https://www.w3schools.com/xml/rss_tag_title_link_description_item.asp) |
| creation or last update datetime according git log. Can be overridden by dates in page.meta. If not, then it uses [MkDocs build date](https://github.com/mkdocs/mkdocs/blob/master/mkdocs/utils/__init__.py#L111-L118) | **recommended** | [`pubDate`](https://www.w3schools.com/xml/rss_tag_pubdate_item.asp) |
| [`page.meta.image`](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) | *optional* | item element [`enclosure`](https://www.w3schools.com/xml/rss_tag_enclosure.asp). Some HTTP requests can be performed to retrieve remote images length. |
| [`page.meta.authors`](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) or `page.meta.author`. Accepted value types: `str` `list`, `tuple`. <br />To comply with the standard, the page writer is responsible to fill this field following this syntax: `john@doe.com (John Doe)` ([read this SO](https://stackoverflow.com/a/6079731/2556577)). | *optional* | [`author`](https://www.w3schools.com/XML/rss_tag_author.asp) |
| [`page.meta.tags`](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) or any tags value (for example `page.meta.categories`...). Accepted value types: `str` `list`. | *optional* | [`category`](https://www.w3schools.com/xml/rss_tag_category_item.asp) |

### Item image (enclosure)

To add an image to a feed item as [enclosure](https://www.w3schools.com/xml/rss_tag_enclosure.asp), the page writer is responsible to fill the `page.meta.image`. The plugin tries to retrieve the image length and mime-type to complete the enclosure tag.

Accepted keys:

- `image`: preferred
- `illustration`: alternative to make it easier to comply with some themes

Accepted values:

- remote image URL: must be reachable from the build environment.
- relative path to the image: the plugin adds the `site_url` to the path to ensure that image will be reachable by external feed readers once the site is published.

#### Examples

##### Local image

`mkdocs.yml` :

```yaml
site_url: https://blog.mydomain.com
```

Page:

```markdown
---
[...]
image: "featured_images.png"
---

# Page h1 title

Some page text.
```

Output:

```xml
<item>
  [...]
  <title>Page h1 title</title>
  <enclosure url="https://blog.mydomain.com/featured_images.png" type="image/png" length="219753"/>
  [...]
</item>
```

##### Remote image

```markdown
---
[...]
image: "http://example.com/image.jpg"
---

# Page h1 title

Some page text.
```

Output:

```xml
<item>
  [...]
  <title>Page h1 title</title>
  <enclosure url="http://example.com/image.jpg" type="image/jpg" length="19753"/>
  [...]
</item>
```

----

## Plugin options

For a sample see [homepage](./index.md#quickstart).

### `enabled`: enabling/disabling the plugin

You can use the `enabled` option to optionally disable this plugin. A possible use case is local development where you might want faster build times. It's recommended to use this option with an environment variable together with a default fallback (introduced in `mkdocs` v1.2.1, see [docs](https://www.mkdocs.org/user-guide/configuration/#environment-variables)). Example:

```yaml
plugins:
  - rss:
      enabled: !ENV [MKDOCS_ENABLE_RSS_PLUGIN, True]
```

Which enables you to disable the plugin locally using:

```bash
export MKDOCS_ENABLE_RSS_PLUGIN=false
mkdocs serve
```

### `image`: set the channel image

`image`: URL to image to use as feed illustration.

Default: `None`.

#### Example

```yaml
plugins:
  - rss:
      image: https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Feed-icon.svg/128px-Feed-icon.svg.png
```

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

### `comments_path`: item comments path

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

### `length`: number of items to include in feed

`length`: number of pages to include as feed items (entries).

Default: `20`

### `feed_ttl`: feed's cache time

`feed_ttl`: number of minutes to be cached. Inserted as channel `ttl` element. See: [W3C RSS 2.0 documentation](https://www.w3schools.com/xml/rss_tag_ttl.asp).

Default: `1440` (= 1 day)

Output:

```xml
<ttl>1440</ttl>
```

### `abstract_chars_count`: item description length

To fill each [item description element](https://www.w3schools.com/xml/rss_tag_title_link_description_item.asp):

- If this value is set to `-1`, then the articles' full HTML content will be filled into the description element.
- be careful: if set to `0` and there is no description, the feed's compliance is broken (an item must have a description)
- Otherwise, the plugin first tries to retrieve the value of the keyword `description` from the [page metadata].
- If the value is non-negative and no `description` meta is found, then the plugin retrieves the first number of characters of the page content defined by this setting. Retrieved content is the raw markdown converted roughly into HTML.

`abstract_chars_count`: number of characters to use as item description.

Default: `150`

----

#### `abstract_delimiter`: abstract delimiter

Used to fill each [item description element](https://www.w3schools.com/xml/rss_tag_title_link_description_item.asp):

- If this value is set to `-1`, then the full HTML content will be filled into the description element.
- Otherwise, the plugin first tries to retrieve the value of the key `description` from the page metadata.
- If the value is non-negative and no `description` meta is found, then the plugin retrieves the first number of characters of the page content defined by this setting. Retrieved content is the raw markdown converted rougthly into HTML (i.e. without extension, etc.).

`abstract_delimiter`: string to mark .

Default: `<!-- more -->`

----

### `categories`: item categories

`categories`: list of page metadata values to use as [RSS item categories](https://www.w3schools.com/xml/rss_tag_category_item.asp).

Default: `None`.

#### Example

In configuration:

```yaml
- rss:
    categories:
      - tags        # will look into page.meta.tags
      - categories  # will also look into page.meta.categories
```

In page 1:

```markdown
---
title: "Lorem Ipsum 1"
tags:
  - tag x
  - tag Y
---

[...]
```

In page 2

```markdown
---
title: "Page 2"
categories: ["Release notes", "test"]
---

[...]
```

Output:

```xml
  [...]
  <item>
    <title>Lorem Ipsum 1</title>
    <category>tag x</category>
    <category>tag Y</category>
    [...]
  </item>
  <item>
    <title>Page 2</title>
    <category>Release notes</category>
    <category>test</category>
    [...]
  </item>
  [...]
```

----

### `date_from_meta`: override dates from git log with page.meta

Basically, the plugin aims to retrieve creation and update dates from git log. But sometimes, it does not match the content workflow: markdown generated from sources, .

So, it's possible to use the dates manually specified into the [page metadata] through the [YAML frontmatter](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data).

- `as_creation`: meta tag name to use as creation date. Default to `False`.
- `as_update`: meta tag name to use as update date. Default to `False`.
- `datetime_format`: datetime format. Default to `"%Y-%m-%d %H:%M"`.
- `default_timezone`: timezone to use by default to make aware datetimes. Default to `UTC`. Introduced in version 1.3.0 with [PR 142](https://github.com/Guts/mkdocs-rss-plugin/pull/142).
- `default_time`: time to use if page contains only a date. Useful to avoid the 'midnight syndrome' or have to specify hour in every single page. Default to `None`. 24h-clock format is expected: `%H:%M`. Example: `"14:20"`. Introduced in version 1.4.0 with [PR 145](https://github.com/Guts/mkdocs-rss-plugin/pull/145).

#### Example

For example, in your `best_article.md` created in 2019, you can write the front-matter like this:

```markdown
---
title: "This page title is a perfect clickbait!"
authors:
  - "Julien M."
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
        default_timezone: Europe/Paris
```

At the end, into the RSS you will get:

```xml
<item>
  <title>This page title is a perfect clickbait!</title>
  <link>https://website.com/articles/best_article/</link>
  <pubDate>Thu, 22 Oct 2020 17:18:00 +0200</pubDate>
  [...]

</item>
```

!!! note "Timezone dependencies"
    The timezones data depends on the Python version used to build:
        - for Python >= 3.9, it uses the standard library and ships [tzdata](https://pypi.org/project/tzdata/) only on Windows which do not provide such data
        - for Python < 3.9, [pytz](https://pypi.org/project/pytz/) is shipped.

### `pretty_print`: prettified XML

By default, the output file is minified, using Jinja2 strip options and manual work. It's possible to disable it and prettify the output using `pretty_print: true`.

```yaml
plugins:
  - rss:
      pretty_print: true
```

Default: `False`.

### `match_path`: filter pages to include in feed

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

### `url_parameters`: additional URL parameters

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

### `use_git`: enable/disable git log

If `false`, the plugin does not try use the git log nor does not check if this is a valid git repository and use informations exclusively from `page.meta` (YAML frontmatter).

Useful if you build your documentation in an environment where you can't easily install git.

Default: `true`.

### `use_material_social_cards`: enable/disable integration with Material Social Cards plugin

If `false`, the integration with Social Cards is disabled.

Default: `true`.

> See [the related section in integrations page](./integrations.md#social-cards-plugin-from-material-theme).

<!-- Hyperlinks reference -->
[page metadata]: https://python-markdown.github.io/extensions/meta_data/
