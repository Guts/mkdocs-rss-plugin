#! python3  # noqa: E265


"""
    Manage timezones for pages date(time)s using zoneinfo module, added in Python 3.9.

"""

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# 3rd party
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
        return input_datetime.replace(tzinfo=timezone.utc)
    else:
        config_tz = ZoneInfo(config_timezone)
        return input_datetime.replace(tzinfo=config_tz)
