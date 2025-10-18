#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# for class autoref typing
from __future__ import annotations

# standard
from collections.abc import MutableMapping
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# 3rd party
from mkdocs.structure.pages import Page

# package modules
from mkdocs_rss_plugin.__about__ import __title__, __version__

# ############################################################################
# ########## Classes ###############
# ##################################


@dataclass
class MkdocsPageSubset:
    """Minimal subset of a Mkdocs Page with only necessary attributes for plugin needs."""

    abs_src_path: str
    dest_uri: str
    src_uri: str
    title: str | None = None
    meta: MutableMapping[str, Any] | None = None

    @classmethod
    def from_page(cls, page: Page) -> MkdocsPageSubset:
        """Create a PageSubset from a Mkdocs page.

        Args:
            page: MkDocs Page object
        """
        return cls(
            abs_src_path=page.file.abs_src_path,
            meta=page.meta,
            title=page.title,
            src_uri=page.file.src_uri,
            dest_uri=page.file.dest_uri,
        )


@dataclass
class PageInformation:
    """Object describing a page information gathered from Mkdocs and used as feed's item."""

    abs_path: Path | None = None
    categories: list | None = None
    authors: tuple | None = None
    comments_url: str | None = None
    created: datetime | None = None
    description: str | None = None
    guid: str | None = None
    image: tuple[str, str, int] | None = None
    link: str | None = None
    pub_date: str | None = None
    title: str | None = None
    updated: datetime | None = None
    # private
    _mkdocs_page_ref: MkdocsPageSubset | None = field(
        default=None, repr=False, compare=False
    )


@dataclass
class RssFeedBase:
    """Object describing a feed."""

    author: str | None = None
    buildDate: str | None = None
    copyright: str | None = None
    description: str | None = None
    entries: list[PageInformation] = field(default_factory=list)
    generator: str = f"{__title__} - v{__version__}"
    html_url: str | None = None
    json_url: str | None = None
    language: str | None = None
    logo_url: str | None = None
    pubDate: str | None = None
    repo_url: str | None = None
    rss_url: str | None = None
    title: str | None = None
    ttl: int | None = None
