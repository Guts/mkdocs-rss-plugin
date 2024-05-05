# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- ----

## [Unreleased]

### Added

### Changed

### Removed

-->

## 1.12.2 - 2024-04-30

### Bugs fixes 🐛

* Fix: abstract limit by @tiosgz and @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/268>

### Tooling 🔧

* ci: fix missing Codecov token by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/269>

### Documentation 📖

* Update docs on locale configuration by @YDX-2147483647 in <https://github.com/Guts/mkdocs-rss-plugin/pull/256>

## 1.12.1 - 2024-02-14

### Bugs fixes 🐛

* fix: stripped time from meta date as  datetime by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/248>

### Documentation 📖

* docs: fix indentation of nested lists by @YDX-2147483647 in <https://github.com/Guts/mkdocs-rss-plugin/pull/242>

## 1.12.0 - 2024-01-13

### Features and enhancements 🎉

* Implement JSON Feed output by @notpushkin and @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/177>

### Documentation 📖

* docs: add how to make JSON Feeds discoverable by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/240>

### Other Changes

* tests: check JSON feed validity by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/239>

### New Contributors

* @notpushkin made their first contribution in <https://github.com/Guts/mkdocs-rss-plugin/pull/177>

## 1.11.1 - 2024-01-11

### Features and enhancements 🎉

* fix #229 allow date.created to get creation date by @copdips in <https://github.com/Guts/mkdocs-rss-plugin/pull/237>

### New Contributors

* @copdips made their first contribution in <https://github.com/Guts/mkdocs-rss-plugin/pull/237>

## 1.11.0 - 2023-12-19

### Features and enhancements 🎉

* improvement: if social card not found, try to retrieve length from remote URL by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/225>

### Tooling 🔧

* ci: add a link between release and discussion by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/224>
* docs: explicitly enable plugins with env vars by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/227>

### Documentation 📖

* docs: add API autodocumentation with mkdocstrings by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/226>

## 1.10.0 - 2023-12-17

### Features and enhancements 🎉

* Feature: support material social cards plugin by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/217>
* feature:  use plugin logger as recomended by Mkdocs (road to Mkdocs>=1.4) by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/221>
* quality: add tests against social cards integration by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/222>

### Tooling 🔧

* ci: set PyPi environment by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/215>

### Documentation 📖

* docs: switch to Material theme and revamp sections by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/216>
* docs: add missing git_use option by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/218>
* Documentation: fix anchors in JSON schema by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/220>

## 1.9.0 - 2023-12-07

### Bugs fixes 🐛

* fix: deprecation of Theme._vars by using config attributes by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/212> thanks to the excellent work of @alexvoss on <https://github.com/Guts/mkdocs-rss-plugin/issues/205> and <https://github.com/Guts/mkdocs-rss-plugin/pull/206>

### Features and enhancements 🎉

* Road to Mkdocs >= 1.4: plugin's configuration by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/195>
* Road to Mkdocs 1.4: use  config attributes by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/211>
* Project: split dev and test dependencies by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/213>
* refacto: move global variables to constants module and rename customtypes into models by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/210>

### Tooling 🔧

* packaging: add Python 3.12 as supported version by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/214>

## 1.8.0 - 2023-07-24

### Bugs fixes 🐛

* Fix tests config by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/196>

### Features and enhancements 🎉

* Add option to enable/disable git use. by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/187>

## 1.7.0 - 2023-05-28

### Bugs fixes 🐛

* Fix tests: restore missing `__init__.py` file to make tests a subpackage by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/190>

### Features and enhancements 🎉

* Comply language codes with RSS Spec by @YDX-2147483647 in <https://github.com/Guts/mkdocs-rss-plugin/pull/178>

### Tooling 🔧

* Documentation: housekeeping dependencies and CI by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/175>

### Documentation 📖

* Doc: typo & tips by @YDX-2147483647 in <https://github.com/Guts/mkdocs-rss-plugin/pull/179>

### Other Changes

* Improve: strip image URL to avoid common errors by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/180>
* Dev tooling: extend git hooks by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/189>

## 1.6.0 - 2023-02-21

### Bugs fixes 🐛

* Improve: handle missing site url by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/150>
* Upgrade git hooks to fix fail because of isort by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/170>

### Features and enhancements 🎉

* Tests: more use cases, better coverage by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/152>
* Handle abstract_chars_count set to 0 by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/172>
* Add new option abstract_delimiter by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/173>

### Tooling 🔧

* Add Python 3.11 to supported versions by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/157>
* Just a little refresh on CI workflows by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/158>
* CI : disable fail fast on tests matrix to get all Python versions results by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/159>
* CI: sse GA to deploy to GH Pages instead of ghp-import by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/171>
* Remove Python 3.7 support by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/174>

## 1.5.0 - 2022-10-13

### Added

* Feature: ignore pages with draft:true in meta by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/149>

### Changed

* Require tzdata only on Windows by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/148>

## 1.4.1 - 2022-10-07

### Changed

* Set Mkdocs upper cap to major version by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/146> to comply with the discussion opened by @oprypin in #137

## 1.4.0 - 2022-10-07

### Added

* Feature: add default_time option by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/145>

### Changed

* Minor improvements: clean unused imports, lines length and use fstrings in logging by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/143>
* Improvement: more granular fallback to build timestamp by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/144>

## 1.3.0 - 2022-10-07

### Added

* Feature: add option to set default timezone by @Guts in <https://github.com/Guts/mkdocs-rss-plugin/pull/142>

## 1.2.0 - 2022-10-03

### Changed

* compatibility with Mkdocs 1.4
* dependencies update

## 1.1.0 - 2022-04-27

### Changed

* switched license to MIT. (See #117)

## 1.0.0 - 2022-03-31

First stable release according to semver.  
So, no feature in this release, just focusing on quality and code cleanliness.

### Added

* Unit tests to reach a 80% coverage score

### Changed

* Supported Mkdocs versions range increased to `mkdocs>=1.1,<1.4`

### Fixed

* Minor bugs fixes
* Minor documentation improvements

----

## 0.21.0 - 2022-02-10

### Added

* JSON Schema for configuration validation
* compatible with Python 3.10

----

## 0.20.1 - 2022-02-08

### Fixed

* Error when using "enabled: false" together with "match_path" (see #104 - PR #107). Reported by @prcr, fixed by @dcode. Thanks to them!

----

## 0.20.0 - 2022-01-06

### Added

* option to enable/disable the plugin, for example through an environment variable (default: enabled). See: PR #103, [related doc section](https://guts.github.io/mkdocs-rss-plugin/configuration/#disabling-the-plugin)

### Changed

* CI: Python version used to build and publish package is now 3.9

### Removed

* support for Python 3.6 (EOL)

----

## 0.19.1 - 2021-10-04

### Fixed

* Fix #95: introduced logic did not handle case where categories meta keys are not defined

----

## 0.19.0 - 2021-10-02

### Added

* new option to include [RSS `<category>` item element](https://www.w3schools.com/xml/rss_tag_category_item.asp) using page metadata (YAML frontmatter). It's customizable to get custom meta keys for keywords/tags. PR [#4](https://github.com/Guts/mkdocs-rss-plugin/pull/4)

----

## 0.18.0 - 2021-09-20

### Added

* option to get the full page content into thread. Contributed by [liang2kl](https://github.com/liang2kl) with [PR 88](https://github.com/Guts/mkdocs-rss-plugin/pull/88). See the [related documentation section](https://guts.github.io/mkdocs-rss-plugin/configuration/#item-description-length).

### Changed

* documentation on ReadTheDocs has been removed to reduce confusion and dependencies. [PR #89](https://github.com/Guts/mkdocs-rss-plugin/pull/89).

----

## 0.17.0 - 2021-06-14

### Changed

* bump MkDocs maximal version

### Fixed

* improve DockerFile used to test, fixing it after Material removed some dependencies

----

## 0.16.1

### Fixed

* remove a print statement

----

## 0.16.0

### Added

* add option to handle the [RSS item comments element](https://www.w3schools.com/XML/rss_tag_comments.asp) through item URL path (see [documentation](https://guts.github.io/mkdocs-rss-plugin/configuration/#item-comments-path))

### Changed

* ignore `urllib.error.URLError` exception to avoid build crashes typically when network is offline

----

## 0.15.0

### Added

* ability to define URL parameters on items URLs (see [documentation](https://guts.github.io/mkdocs-rss-plugin/configuration/#url-parameters))
* complete unit tests and display code coverage badge (using codecov.io)

### Changed

* homogenization of docstrings on the sphinx format (as stipulated in the contribution guidelines)

----

## 0.14.0

### Fixed

* fix `match_path` option by skipping the pages that aren't included. See [PR #49](https://github.com/Guts/mkdocs-rss-plugin/pull/49). Contributed by [Paulo Ribeiro](https://github.com/pauloribeiro-codacy/).

### Added

* add isort to development toolbelt

----

## 0.13.0

### Added

* if `page.meta.description` is not set, the `abstract_chars_count` first characters from markdown content are now converted into HTML.
* add `match_path` option which should be a regex pattern matching the path to your files within the docs_dir. See [issue #34](https://github.com/Guts/mkdocs-rss-plugin/issues/34) and the related [PR #43](https://github.com/Guts/mkdocs-rss-plugin/pull/43). Contributed by [Ryan Morshead](https://github.com/rmorshea/).

----

## 0.12.0

### Added

* add support to `page.meta.authors` or `page.meta.author` to populate feed items author tag. See [issue #34](https://github.com/Guts/mkdocs-rss-plugin/issues/34).

----

## 0.11.0

### Added

* option to prettify the output, disabling minify. See [issue #18](https://github.com/Guts/mkdocs-rss-plugin/issues/18), [PR #33](https://github.com/Guts/mkdocs-rss-plugin/pull/33) and [related documentation section](https://guts.github.io/mkdocs-rss-plugin/configuration/#prettified-output)

### Changed

* By default, the output file is now minified.

----

## 0.10.0

### Added

* option to use dates from page metadata (YAML front-matter) instead of git log. See [#14](https://github.com/Guts/mkdocs-rss-plugin/pull/14) and [related documentation section](https://guts.github.io/mkdocs-rss-plugin/configuration/#dates-overriding)
* Python 3.9 is enabled in CI and referenced in PyPi tags

### Changed

* the default length for description has been changed from 150 to 160 to fit maximum recommendation

----

## 0.9.0

### Improved

* enable auto-escape on feed and item titles, using the Jinja e filter - see #19
* improve consistency for missing attributes in mkdocs.yml, returning almost always a None value

----

## 0.8.0

### Added

* RSS compliance: image length is now present into enclosure tags - See #9
* User documentation:
  * clarify how item elements are computed
  * add how to edit HTML templates meta-tags to reference feeds
* API reference documentation generated from source code and published through Read The Docs

----

## 0.7.2

### Fixed

* wrong items order in updated feed

----

## 0.7.1

### Fixed

* feed for updated content is broken - #15

----

## 0.7.0

### Added

* plugin: add the `language` tag to the channel
* tooling:
  * add first unit tests and code coverage
  * add Github Action to perform tests
  * check docker build using mkdocs-material

### Changed

* docs: switch Feedly images from HTTP to HTTPS

----

## 0.6.1

### Fixed

* remove print from plugin code

----

## 0.6.0

### Added

* plugin: add tag `guid` to the feed's items (using the page URL)

### Changed

* docs: minor improvements

----

## 0.5.0

### Added

* plugin: handle channel `image` and items (entries) `enclosure`

### Changed

* plugin: refactoring to build feed entry through a method
