---
title: Configuration
date: 2020-12-31 14:20
description: Configuration steps and settings for MkDocs RSS plugin
image: "https://svgsilh.com/png-512/97849.png"
---

# Configuration

To produce a valid RSS feed, the plugin uses:

- some global settings from [MkDocs configuration](#mkdocs-configuration)
- some [specific settings](#plugin-options) to custom behavior or add some optional elements

## MkDocs configuration

| Setting | Expected level | Corresponding RSS element |
| :------ | :------------: | :------------------------ |
| [`site_description`](https://www.mkdocs.org/user-guide/configuration/#site_description) | **required** | mandatory channel element [`description`](https://www.w3schools.com/xml/rss_tag_title_link_description_channel.asp) |
| [`site_name`](https://www.mkdocs.org/user-guide/configuration/#site_name) | **required** | mandatory channel element [`title`](https://www.w3schools.com/xml/rss_tag_title_link_description_channel.asp) |
| [`site_url`](https://www.mkdocs.org/user-guide/configuration/#site_url) | **required** | mandatory channel element [`link`](https://www.w3schools.com/xml/rss_tag_title_link_description_channel.asp) |
| ---- | ---- | ---- |
| [`repo_url`](https://www.mkdocs.org/user-guide/configuration/#repo_url) | **recomended** | optional channel element [`docs`](https://www.w3schools.com/xml/rss_tag_docs.asp) |
| [`site_author`](https://www.mkdocs.org/user-guide/configuration/#site_author) | **recomended** | optional channel element [`managingEditor`](https://www.w3schools.com/xml/rss_tag_managingeditor.asp) |
| ---- | ---- | ---- |
| [`copyright`](https://www.mkdocs.org/user-guide/configuration/#copyright) | *optional* | optional channel element [`copyright`](https://www.w3schools.com/xml/rss_tag_copyright.asp) |
| [`locale` or `theme/locale` or `theme/language`](https://github.com/squidfunk/mkdocs-material/issues/1350#issuecomment-559095892) | *optional* | optional channel element [`language`](https://www.w3schools.com/xml/rss_tag_language.asp) |

### Automatic elements

| Variable / value | Corresponding RSS element |
| :---- | :------------------------ |
| MkDocs [build timestamp](https://github.com/mkdocs/mkdocs/blob/ff0b7260564e65b6547fd41753ec971e4237823b/mkdocs/utils/__init__.py#L83-L94) | optional channel elements [`lastBuildDate`](https://www.w3schools.com/xml/rss_tag_lastbuilddate.asp) and [`pubDate`](https://www.w3schools.com/xml/rss_tag_pubdate.asp) |
| MkDocs RSS plugin - v*1.0.0* | optional channel elements [`generator`](https://www.w3schools.com/xml/rss_tag_generator.asp) |

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
  <title>MkDocs RSS Plugin - Illustration</title>
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

Basically, the plugin aims to retrieve creation and update dates from git log. But sometimes, it does not match the content workflow as described in the following use cases.

So, it's possible to use the dates manually specified into the [page metadata] through the [YAML frontmatter](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data).

For example, in your pages, you can write the front-matter like this:

```markdown
---
title: "This page title is a perfect clickbait!"
authors: ["Julien M."]
date: "2020-12-28 10:20"
---

# This plugin will change your MkDocs life

Lorem ipsum

```

So in your `mkdocs.yml` you will have:

```yaml
plugins:
  - rss:
      date_from_meta:
        as_creation: "date"
        as_update: false
```

#### Options

`as_creation`: meta tag name to use as creation date. Default to False.
`as_update`: meta tag name to use as update date. Default to False.
`date_format`: datetime format. Default to "%Y-%m-%d %H:%M".

If False, it will use th git log.

#### Use cases

##### Contribution and publication workflow

- a writer create the article
- multiple authors will contribute to the article content
- after a few weeks, the article is published. But in the meantime, others articles have been published and trusting the git log it

##### Generated pages from sources

> TO DOC

<!-- Hyperinks references -->
[page metadata]: https://python-markdown.github.io/extensions/meta_data/
