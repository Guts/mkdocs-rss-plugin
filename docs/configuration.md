---
title: Configuration
description: Configuration steps for MkDocs RSS plugin
---

# Configuration

## MkDocs configuration

### Required

- [`site_description`](https://www.mkdocs.org/user-guide/configuration/#site_description): used for RSS 2.0 mandatory channel element `description`
- [`site_name`](https://www.mkdocs.org/user-guide/configuration/#site_name): used for RSS 2.0 mandatory channel element `title`
- [`site_url`](https://www.mkdocs.org/user-guide/configuration/#site_url): used for RSS 2.0 mandatory channel element `link` value

### Recomended

- [`site_author`](https://www.mkdocs.org/user-guide/configuration/#site_author)
- [`repo_url`](https://www.mkdocs.org/user-guide/configuration/#repo_url)

### Optional

- [`copyright`](https://www.mkdocs.org/user-guide/configuration/#site_url): used as RSS 2.0 optional `copyright` value

----

## Plugin options

Sample:

```yml
plugins:
  - mkdocs-rss-plugin:
      abstract_chars_count: 150
      feed_ttl: 1440
      length: 20
```

### Feed length

`length`: number of pages to include in feed items (entries).

Default: `20`

### Item description length

`abstract_chars_count`: number of characters to use as item description.

Default: `150`

### Feed TTL

`feed_ttl`: to be inserted as channel `ttl` element. See: [W3C RSS 2.0 documentation](https://validator.w3.org/feed/docs/rss2.html#ltttlgtSubelementOfLtchannelgt).

Unity: minutes
Default: 1440 (= 1 day)

----
