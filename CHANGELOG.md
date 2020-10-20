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
