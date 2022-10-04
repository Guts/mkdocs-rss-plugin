#! python3  # noqa: E265


"""
    Manage timezones for pages date(time)s using zoneinfo module, added in Python 3.9.

"""

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
from datetime import datetime
from functools import lru_cache

# ############################################################################
# ########## Globals #############
# ################################


logger = logging.getLogger("mkdocs.mkdocs_rss_plugin")


# ############################################################################
# ########## Functions ###########
# ################################


@lru_cache(typed=True)
def set_datetime_zoneinfo(
    input_datetime: datetime, config_timezone: str = None
) -> datetime:
    """_summary_

    :param input_datetime: _description_
    :type input_datetime: datetime
    :param config_timezone: _description_
    :type config_timezone: str
    :return: _description_
    :rtype: datetime
    """
    pass
