#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# 3rd party
from mkdocs.config import config_options
from mkdocs.config.base import Config

# package
from mkdocs_rss_plugin.constants import DEFAULT_CACHE_FOLDER

# ############################################################################
# ########## Classes ###############
# ##################################


class _DateFromMeta(Config):
    """Sub configuration object for related date options."""

    # for as_creation and as_update
    as_creation = config_options.Type(str, default="git")
    as_update = config_options.Type(str, default="git")
    datetime_format = config_options.Type(str, default="%Y-%m-%d %H:%M")
    default_time = config_options.Type(str, default="00:00")
    default_timezone = config_options.Type(str, default="UTC")


class _FeedsFilenamesConfig(Config):
    """Sub configuration for feeds filenames."""

    json_created = config_options.Type(str, default="feed_json_created.json")
    json_updated = config_options.Type(str, default="feed_json_updated.json")
    rss_created = config_options.Type(str, default="feed_rss_created.xml")
    rss_updated = config_options.Type(str, default="feed_rss_updated.xml")


class RssPluginConfig(Config):
    """Configuration for RSS plugin for Mkdocs."""

    abstract_chars_count = config_options.Type(int, default=160)
    abstract_delimiter = config_options.Type(str, default="<!-- more -->")
    categories = config_options.Optional(
        config_options.ListOfItems(config_options.Type(str))
    )
    cache_dir = config_options.Type(str, default=f"{DEFAULT_CACHE_FOLDER.resolve()}")
    comments_path = config_options.Optional(config_options.Type(str))
    date_from_meta = config_options.SubConfig(_DateFromMeta)
    enabled = config_options.Type(bool, default=True)
    feeds_filenames = config_options.SubConfig(_FeedsFilenamesConfig)
    feed_description = config_options.Optional(config_options.Type(str))
    feed_title = config_options.Optional(config_options.Type(str))
    feed_ttl = config_options.Type(int, default=1440)
    image = config_options.Optional(config_options.Type(str))
    json_feed_enabled = config_options.Type(bool, default=True)
    length = config_options.Type(int, default=20)
    match_path = config_options.Type(str, default=".*")
    pretty_print = config_options.Type(bool, default=False)
    rss_feed_enabled = config_options.Type(bool, default=True)
    url_parameters = config_options.Optional(config_options.Type(dict))
    use_git = config_options.Type(bool, default=True)
    use_material_social_cards = config_options.Type(bool, default=True)
