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
    abs_path: Path = None
    created: datetime = None
    updated: datetime = None
    title: str = None
    description: str = None
    image: str = None
    url_full: str = None
