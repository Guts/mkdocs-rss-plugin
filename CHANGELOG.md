# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- ----

## [Unreleased]

### Added

### Changed

### Removed -->

----

## 0.10.0

### Added

- option to use dates from page metadata (YAML front-matter) instead of git log. See [#14](https://github.com/Guts/mkdocs-rss-plugin/pull/14) and [related documentation section](https://guts.github.io/mkdocs-rss-plugin/configuration/#dates-overriding)
- Python 3.9 is enabled in CI and referenced in PyPi tags

### Changed

- the default length for description has been changed from 150 to 160 to fit maximum recommendation

----

## 0.9.0

### Improved

- enable auto-escape on feed and item titles, using the Jinja e filter - see #19
- improve consistency for missing attributes in mkdocs.yml, returning almost always a None value

----

## 0.8.0

### Added

- RSS compliance: image length is now present into enclosure tags - See #9
- User documentation:
  - clarify how item elements are computed
  - add how to edit HTML templates meta-tags to reference feeds
- API reference documentation generated from source code and published through Read The Docs

----

## 0.7.2

### Fixed

- wrong items order in updated feed

----

## 0.7.1

### Fixed

- feed for updated content is broken - #15

----

## 0.7.0

### Added

- plugin: add the `language` tag to the channel
- tooling:
  - add first unit tests and code coverage
  - add Github Action to perform tests
  - check docker build using mkdocs-material

### Changed

- docs: switch Feedly images from HTTP to HTTPS

----

## 0.6.1

### Fixed

- remove print from plugin code

----

## 0.6.0

### Added

- plugin: add tag `guid` to the feed's items (using the page URL)

### Changed

- docs: minor improvments

----

## 0.5.0

### Added

- plugin: handle channel `image` and items (entries) `enclosure`

### Changed

- plugin: refactoring to build feed entry through a method
