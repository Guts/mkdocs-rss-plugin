#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

# package modules
from mkdocs_rss_plugin.__about__ import __title__, __version__

# ############################################################################
# ########## Classes ###############
# ##################################


@dataclass
class PageInformation:
    """Data type to set and get page information in order to produce the RSS feed."""

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


@dataclass
class RssFeedBase:
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
