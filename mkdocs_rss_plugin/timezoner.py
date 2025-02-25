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

    Args:
        input_datetime (datetime): offset-naive datetime
        config_timezone (str, optional): name of timezone as registered in IANA
            database. Defaults to "UTC". Example : Europe/Paris.

    Returns:
        datetime: offset-aware datetime
    """
    if input_datetime.tzinfo:
        return input_datetime
    elif not config_timezone:
        return input_datetime.replace(tzinfo=timezone.utc)
    else:
        config_tz = ZoneInfo(config_timezone)
        return input_datetime.replace(tzinfo=config_tz)
