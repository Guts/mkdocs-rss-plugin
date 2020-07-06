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
    abs_path: Path
    created: datetime
    updated: datetime
    title: str
    description: str
    url_full: str
