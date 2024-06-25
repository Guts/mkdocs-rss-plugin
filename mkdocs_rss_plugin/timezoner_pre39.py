#! python3  # noqa: E265


"""
Manage timezones for pages date(time)s using pytz module.
Meant to be dropped when Python 3.8 reaches EOL.
"""

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from datetime import datetime

# 3rd party
import pytz
from mkdocs.plugins import get_plugin_logger

# package
from mkdocs_rss_plugin.constants import MKDOCS_LOGGER_NAME

# ############################################################################
# ########## Globals #############
# ################################


logger = get_plugin_logger(MKDOCS_LOGGER_NAME)


# ############################################################################
# ########## Functions ###########
# ################################


def set_datetime_zoneinfo(
    input_datetime: datetime, config_timezone: str = "UTC"
) -> datetime:
    """Apply timezone to a naive datetime.

    :param input_datetime: offset-naive datetime
    :type input_datetime: datetime
    :param config_timezone: name of timezone as registered in IANA database,
    defaults to "UTC". Example : Europe/Paris.
    :type config_timezone: str, optional

    :return: offset-aware datetime
    :rtype: datetime
    """
    if input_datetime.tzinfo:
        return input_datetime
    elif not config_timezone:
        return input_datetime.replace(tzinfo=pytz.utc)
    else:
        config_tz = pytz.timezone(config_timezone)
        return config_tz.localize(input_datetime)
