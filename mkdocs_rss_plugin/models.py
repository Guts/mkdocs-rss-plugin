#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard
from datetime import datetime
from pathlib import Path
from typing import NamedTuple, Optional


# ############################################################################
# ########## Classes ###############
# ##################################
class PageInformation(NamedTuple):
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
