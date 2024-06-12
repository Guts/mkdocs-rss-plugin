#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard
from datetime import datetime
from pathlib import Path
from typing import NamedTuple


# ############################################################################
# ########## Classes ###############
# ##################################
class PageInformation(NamedTuple):
    """Data type to set and get page information in order to produce the RSS feed."""

    abs_path: Path | None = None
    categories: list | None = None
    authors: tuple | None = None
    created: datetime | None = None
    description: str | None = None
    guid: str | None = None
    image: str | None = None
    title: str | None = None
    updated: datetime | None = None
    url_comments: str | None = None
    url_full: str | None = None
