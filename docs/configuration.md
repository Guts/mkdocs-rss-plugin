---
title: Configuration
description: Configuration steps and settings for MkDocs RSS plugin
---

# Configuration

To produce a valid RSS feed, the plugin uses:

- some global settings from [MkDocs configuration](#mkdocs-configuration)
- some [specific settings](##plugin-options) to custom behavior or add some optional elements

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
      length: 20
```

### Feed length

`length`: number of pages to include as feed items (entries).

Default: `20`

### Feed TTL

`feed_ttl`: number of minutes to be cached. Inserted as channel `ttl` element. See: [W3C RSS 2.0 documentation](https://www.w3schools.com/xml/rss_tag_ttl.asp).

Default: `1440` (= 1 day)

### Item description length

To fill each [item description element](https://www.w3schools.com/xml/rss_tag_title_link_description_item.asp), the plugin first tries to retrieve the value of the keyword `description` from the [page metadata](https://python-markdown.github.io/extensions/meta_data/).

If the page has no meta, then the plugin retrieves the first number of characters of the page content defined by this setting. Retrieved content is raw markdown.

`abstract_chars_count`: number of characters to use as item description.

Default: `150`


----
