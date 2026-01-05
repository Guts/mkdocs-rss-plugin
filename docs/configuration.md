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
| [`theme/locale` (or `theme/language` for Material theme)](https://github.com/squidfunk/mkdocs-material/issues/1350#issuecomment-559095892) | *optional* | [`language`](https://www.w3schools.com/xml/rss_tag_language.asp) |

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
| [`page.meta.description`](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data) if present, else extract headlines from the content. See below the [item_description_length option](#abstract_chars_count). | **required** | [`description`](https://www.w3schools.com/xml/rss_tag_title_link_description_item.asp) |
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

### :material-toggle-switch: `enabled`: enabling/disabling the plugin { #enabled }

You can use the `enabled` option to optionally disable this plugin. A possible use case is local development where you might want faster build times. It's recommended to use this option with an environment variable together with a default fallback (introduced in `mkdocs` v1.2.1, see [docs](https://www.mkdocs.org/user-guide/configuration/#environment-variables)). Example:

```yaml
plugins:
  - rss:
      enabled: !ENV [MKDOCS_ENABLE_RSS_PLUGIN, True]
```

Which allows you to disable the plugin locally using:

```bash
export MKDOCS_ENABLE_RSS_PLUGIN=false
mkdocs serve
```

----

### :simple-json: `json_feed_enabled`: enabling/disabling export to JSON Feed { #json_feed_enabled }

Set it to `false` if you want to only export to RSS.

Default: `true`.

----

### :material-rss: `rss_feed_enabled`: enabling/disabling export to RSS { #rss_feed_enabled }

Set it to `false` if you want to only export to JSON feed.

Default: `true`.

----

### :material-more: `abstract_chars_count`: item description length { #abstract_chars_count }

Used, in combination with `abstract_delimiter`, to determine each [item description element](https://www.w3schools.com/xml/rss_tag_title_link_description_item.asp):

- If this value is set to `-1`, then the articles' full HTML content will be filled into the description element.
- If you want to customize the description per each Markdown page, refer to the example below.
- Otherwise, the plugin first tries to retrieve the value of the keyword `description` from the [page metadata].
- If that fails and `abstract_delimiter` is found in the page, the article content up to (but not including) the delimiter is used.
- If the above has failed, then the plugin retrieves the first number of characters of the page content defined by this setting. Retrieved content is the raw markdown converted roughly into HTML.

Be careful: if set to `0` and there is no description, the feed's compliance is broken (an item must have a description).

#### Override feed description per page

To customize the value of the RSS description per each page and override the value of `site_description` and `plugins.rss.feed_description`, you can modify the value per each page as you see in the example below:

```markdown
---
date: 2024-06-24
description: >-
  This is the SEO description.
rss:
  feed_description: >-
    And I want to have customized RSS description.
---
```

`abstract_chars_count`: number of characters to use as item description.

Default: `150`

----

### :material-pen-minus: `abstract_delimiter`: abstract delimiter { #abstract_delimiter }

Please see `abstract_chars_count` for how this setting is used. A value of `""` (the empty string) disables this step.

`abstract_delimiter`: string to mark where the description ends.

Default: `<!-- more -->`

----

### :material-recycle: `cache_dir`: folder where to store plugin's cached files { #cache_dir }

The plugin implements a caching mechanism, ensuring that a remote media is only get once during its life-cycle on remote HTTP server (using [Cache Control](https://pypi.org/project/CacheControl/) under the hood). It is normally not necessary to specify this setting, except for when you want to change the path within your root directory where HTTP body and metadata files are cached.

If you want to change it, use:

``` yaml
plugins:
  - rss:
      cache_dir: my/custom/dir
```

It's strongly recommended to add the path to your `.gitignore` file in the root of your project:

``` title=".gitignore"
.cache
```

Default: `.cache/plugins/rss`.

----

### :material-tag-multiple: `categories`: item categories { #categories }

`categories`: list of page metadata values to use as [RSS item categories](https://www.w3schools.com/xml/rss_tag_category_item.asp).

Default: `None`.

#### Example { #categories_example }

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

### :material-comment-bookmark-outline: `comments_path`: item comments path { #comments_path }

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

----

### :material-calendar-start: `date_from_meta`: override dates from git log with page.meta { #date_from_meta }

Basically, the plugin aims to retrieve creation and update dates from git log. But sometimes, it does not match the content workflow: markdown generated from sources, .

So, it's possible to use the dates manually specified into the [page metadata] through the [YAML frontmatter](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data).

- `as_creation`: meta tag name (or a dot-separated tag name) to use as creation date. Default to `False`.
- `as_update`: meta tag name (or a dot-separated tag name) to use as update date. Default to `False`.
- `datetime_format`: datetime format. Default to `"%Y-%m-%d %H:%M"`.
- `default_timezone`: timezone to use by default to make aware datetimes. Default to `UTC`. Introduced in version 1.3.0 with [PR 142](https://github.com/Guts/mkdocs-rss-plugin/pull/142).
- `default_time`: time to use if page contains only a date. Useful to avoid the 'midnight syndrome' or have to specify hour in every single page. Default to `None`. 24h-clock format is expected: `%H:%M`. Example: `"14:20"`. Introduced in version 1.4.0 with [PR 145](https://github.com/Guts/mkdocs-rss-plugin/pull/145).

#### Example { #date_from_meta_example }

For example, in your `best_article.md` created in 2019, you can write the front-matter like this:

=== "tag name: `date`"

    ```markdown hl_lines="5"
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

    ```yaml hl_lines="4-5"
    plugins:
      - rss:
          date_from_meta:
            as_creation: "date"
            as_update: "git"
            datetime_format: "%Y-%m-%d %H:%M"
            default_timezone: Europe/Paris
    ```

=== "dot-separated tag name: `date.created`"

    ```markdown hl_lines="6"
    ---
    title: "This page title is a perfect clickbait!"
    authors:
      - "Julien M."
    date:
      created: "2020-10-22 17:18"
    ---

    # This plugin will change your MkDocs life

    Lorem ipsum [...]
    ```

    So in your `mkdocs.yml` you will have:

    ```yaml hl_lines="4-5"
    plugins:
      - rss:
          date_from_meta:
            as_creation: "date.created"
            as_update: "git"
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
    The timezones data relies on the standard library and ships [tzdata](https://pypi.org/project/tzdata/) only on Windows which do not provide such data.

----

### :material-subtitles: `feed_description`: override site description { #description }

This option allows you to override the default MkDocs site description for the description tag in this feed.
This is useful if you have multiple instances of this plugin for multiple feeds. (For example, one feed
for the blog, and a second for documentation updates.)

This setting is optional. If you do not include it, the default site description will be used.

```yaml
plugins:
  - rss:
      feed_description: The best blog from the best site
```

Default: Use the default MkDocs `site_description:`.

----

### :material-format-title: `feed_title`: override site title { #title }

This option allows you to override the default MkDocs site name for the title tag in this feed.
This is useful if you have multiple instances of this plugin for multiple feeds. (For example, one feed
for the blog, and a second for documentation updates.)

This setting is optional. If you do not include it, the default site name will be used.

```yaml
plugins:
  - rss:
      feed_title: My awesome blog feed
```

Default: Use the default MkDocs `site_name:`.

----

### :material-clock-end: `feed_ttl`: feed's cache time { #feed_ttl }

`feed_ttl`: number of minutes to be cached. Inserted as channel `ttl` element. See: [W3C RSS 2.0 documentation](https://www.w3schools.com/xml/rss_tag_ttl.asp).

Default: `1440` (= 1 day)

Output:

```xml
<ttl>1440</ttl>
```

----

### :material-alphabet-latin: `feeds_filenames`: customize the output feed URL { #feeds_filenames }

> Since version 1.13.0.

Customize every feed filenames generated by the plugin:

```yaml title="mkdocs.yml with custom RSS and JSON feeds names."
plugins:
  - rss:
      feeds_filenames:
        json_created: feed.json
        json_updated: feed-updated.json
        rss_created: rss.xml
        rss_updated: rss-updated.xml
```

Default:

- JSON feed for **created** items: `feed_json_created.json`
- JSON feed for **updated** items: `feed_json_updated.json`
- RSS feed for **created** items: `feed_rss_created.json`
- RSS feed for **updated** items: `feed_rss_updated.json`

----

### :material-image-outline: `image`: set the channel image { #image }

`image`: URL to image to use as feed illustration.

Default: `None`.

#### Example

```yaml
plugins:
  - rss:
      image: https://github.com/Guts/mkdocs-rss-plugin/blob/main/docs/assets/logo_rss_plugin_mkdocs.png?raw=true
```

Output:

```xml
<image>
  <url>
    https://github.com/Guts/mkdocs-rss-plugin/blob/main/docs/assets/logo_rss_plugin_mkdocs.png?raw=true
  </url>
  <title>MkDocs RSS Plugin</title>
  <link>https://guts.github.io/mkdocs-rss-plugin/</link>
</image>
```

----

### :material-counter:  `length`: number of items to include in feed { #length }

`length`: number of pages to include as feed items (entries).

Default: `20`

----

### :material-regex: `match_path`: filter pages to include in feed { #match_path }

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

----

### :material-format-indent-increase: `pretty_print`: prettified XML { #pretty_print }

By default, the output file is minified, using Jinja2 strip options and manual work. It's possible to disable it and prettify the output using `pretty_print: true`.

```yaml
plugins:
  - rss:
      pretty_print: true
```

Default: `False`.

----

### :material-track-light: `url_parameters`: additional URL parameters { #url_parameters }

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

### :material-git: `use_git`: enable/disable git log { #use_git }

If `false`, the plugin does not try use the git log nor does not check if this is a valid git repository and use informations exclusively from `page.meta` (YAML frontmatter).

Useful if you build your documentation in an environment where you can't easily install git.

Default: `true`.

----

### :material-newspaper-variant-outline: `use_material_blog`: enable/disable integration with Material Blog plugin { #use_material_blog }

If `false`, the integration with the Blog plugin is disabled.

Default: `true`.

> See [the related section in integrations page](./integrations.md#blog-plugin-from-material-theme).

----

### :material-cards: `use_material_social_cards`: enable/disable integration with Material Social Cards plugin { #use_material_social_cards }

If `false`, the integration with Social Cards is disabled.

Default: `true`.

> See [the related section in integrations page](./integrations.md#social-cards-plugin-from-material-theme).

<!-- Hyperlinks reference -->
[page metadata]: https://python-markdown.github.io/extensions/meta_data/
