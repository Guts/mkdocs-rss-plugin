#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################


# standard
from collections.abc import MutableMapping
from dataclasses import dataclass, field
from datetime import datetime
from email.utils import format_datetime
from pathlib import Path
from typing import Any, Literal, Optional

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

    dest_uri: str
    src_uri: str
    title: Optional[str] = None
    meta: Optional[MutableMapping[str, Any]] = None

    @classmethod
    def from_page(cls, page: Page) -> "MkdocsPageSubset":
        """Create a PageSubset from a Mkdocs page.

        Args:
            page: MkDocs Page object
        """
        return cls(
            meta=page.meta,
            title=page.title,
            src_uri=page.file.src_uri,
            dest_uri=page.file.dest_uri,
        )


@dataclass
class PageInformation:
    """Object describing a page information gathered from Mkdocs and used as feed's item."""

    abs_path: Optional[Path] = None
    categories: Optional[list] = None
    authors: Optional[tuple] = None
    created: Optional[datetime] = None
    description: Optional[str] = None
    guid: Optional[str] = None
    image: Optional[str] = None
    title: Optional[str] = None
    updated: Optional[datetime] = None
    url_comments: Optional[str] = None
    url_full: Optional[str] = None
    _mkdocs_page_ref: Optional[MkdocsPageSubset] = field(
        default=None, repr=False, compare=False
    )

    def as_rss_item(self, date_type: Literal["created", "updated"]) -> dict:
        """Return the object as a dictionary formatted for RSS item."""
        pub_date: datetime = getattr(self, date_type)
        return {
            "authors": self.authors,
            "categories": self.categories,
            "comments_url": self.url_comments,
            "description": self.description,
            "guid": self.guid,
            "image": self.image,
            "link": self.url_full,
            "pubDate": format_datetime(dt=pub_date),
            "pubDate3339": pub_date.isoformat("T"),
            "title": self.title,
        }


@dataclass
class RssFeedBase:
    """Object describing a feed."""

    author: Optional[str] = None
    buildDate: Optional[str] = None
    copyright: Optional[str] = None
    description: Optional[str] = None
    entries: list[PageInformation] = field(default_factory=list)
    generator: str = f"{__title__} - v{__version__}"
    html_url: Optional[str] = None
    json_url: Optional[str] = None
    language: Optional[str] = None
    logo_url: Optional[str] = None
    pubDate: Optional[str] = None
    repo_url: Optional[str] = None
    rss_url: Optional[str] = None
    title: Optional[str] = None
    ttl: Optional[int] = None
