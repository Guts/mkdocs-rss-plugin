#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging

# 3rd party
from mkdocs.config.config_options import Config
from mkdocs.structure.pages import Page

# ############################################################################
# ########## Globals #############
# ################################

logger = logging.getLogger("mkdocs.mkdocs_rss_plugin")

# ############################################################################
# ########## Logic ###############
# ################################


def is_theme_material(mkdocs_config: Config) -> bool:
    """Check if the theme set in mkdocs.yml is material or not.

    Args:
        mkdocs_config (Config): Mkdocs website configuration object.

    Returns:
        bool: True if the theme's name is 'material'. False if not.
    """
    return mkdocs_config.theme.name == "material"


def is_social_plugin_enabled_mkdocs(mkdocs_config: Config) -> bool:
    """Check if social cards plugin is enabled.

    Args:
        mkdocs_config (Config): Mkdocs website configuration object.

    Returns:
        bool: True if the theme material and the plugin social cards is enabled.
    """
    if not is_theme_material(mkdocs_config=mkdocs_config):
        logger.debug(
            "[rss-plugin] Installed theme is not 'material'. Integration disabled."
        )
        return False

    if not mkdocs_config.plugins.get("material/social"):
        logger.debug("[rss-plugin] Social plugin not listed in configuration.")
        return False

    social_plugin_cfg = mkdocs_config.plugins.get("material/social")

    if not social_plugin_cfg.config.enabled or not social_plugin_cfg.config.cards:
        logger.debug(
            "[rss-plugin] Social plugin is installed, present but cards are disabled."
        )
        return False

    logger.debug("[rss-plugin] Social cards are enabled in Mkdocs configuration.")
    return True


def is_social_plugin_enabled_page(mkdocs_page: Page) -> bool:
    """Check if the social plugin is enabled or disabled for a specific page. Plugin
        has to enabled in Mkdocs configuration before.

    Args:
        mkdocs_page (Page): Mkdocs page object.

    Returns:
        bool: True if the social cards are enabled for a page.
    """
    if (
        "social" in mkdocs_page.meta
        and mkdocs_page.meta.get("social").get(
            "cards", is_social_plugin_enabled_mkdocs()
        )
        is True
    ):
        return True

    return False


def get_social_card_url_for_page(mkdocs_config: Config, mkdocs_page: Page) -> str:
    """Get social card URL for a specific page in documentation.

    Args:
        mkdocs_config (Config): Mkdocs website configuration object.
        mkdocs_page (Page): Mkdocs page object.

    Returns:
        str: URL to the image once published
    """
    return f"{mkdocs_config.site_url}assets/images/social{mkdocs_page.abs_url[:-1]}.png"
