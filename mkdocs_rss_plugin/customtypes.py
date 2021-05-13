#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from datetime import datetime
from pathlib import Path
from typing import NamedTuple


# ############################################################################
# ########## Classes ###############
# ##################################
class PageInformation(NamedTuple):
    """Data type to set and get page information in order to produce the RSS feed."""

    abs_path: Path = None
    authors: tuple = None
    created: datetime = None
    description: str = None
    guid: str = None
    image: str = None
    title: str = None
    updated: datetime = None
    url_comments: str = None
    url_full: str = None
