#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from pathlib import Path
from typing import Optional

# 3rd party
from mkdocs.config.config_options import Config
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.pages import Page

# package
from mkdocs_rss_plugin.constants import MKDOCS_LOGGER_NAME

# ############################################################################
# ########## Globals #############
# ################################

logger = get_plugin_logger(MKDOCS_LOGGER_NAME)

# ############################################################################
# ########## Logic ###############
# ################################


class IntegrationMaterialSocialCards:
    # attributes
    IS_ENABLED: bool = True
    IS_SOCIAL_PLUGIN_ENABLED: bool = True
    IS_SOCIAL_PLUGIN_CARDS_ENABLED: bool = True
    IS_THEME_MATERIAL: bool = False

    def __init__(self, mkdocs_config: Config, switch_force: bool = True) -> None:
        """Integration instanciation.

        Args:
            mkdocs_config (Config): Mkdocs website configuration object.
            switch_force (bool, optional): option to force integration disabling. Set
                it to False to disable it even if Social Cards are enabled in Mkdocs
                configuration. Defaults to True.
        """
        # check if the integration can be enabled or not
        self.IS_SOCIAL_PLUGIN_CARDS_ENABLED = (
            self.is_social_plugin_and_cards_enabled_mkdocs(mkdocs_config=mkdocs_config)
        )

        # if every conditions are True, enable the integration
        self.IS_ENABLED = all(
            [
                self.IS_THEME_MATERIAL,
                self.IS_SOCIAL_PLUGIN_ENABLED,
                self.IS_SOCIAL_PLUGIN_CARDS_ENABLED,
            ]
        )

        # except if the end-user wants to disable it
        if switch_force is False:
            self.IS_ENABLED = False
            logger.debug(
                "Integration with Social Cards (Material theme) is "
                "disabled in plugin's option in Mkdocs configuration."
            )

        # if enabled, save some config elements
        if self.IS_ENABLED:
            self.mkdocs_site_url = mkdocs_config.site_url
            self.mkdocs_site_build_dir = mkdocs_config.site_dir
            self.social_cards_assets_dir = self.get_social_cards_dir(
                mkdocs_config=mkdocs_config
            )

    def is_theme_material(self, mkdocs_config: Config) -> bool:
        """Check if the theme set in mkdocs.yml is material or not.

        Args:
            mkdocs_config (Config): Mkdocs website configuration object.

        Returns:
            bool: True if the theme's name is 'material'. False if not.
        """
        self.IS_THEME_MATERIAL = mkdocs_config.theme.name == "material"
        return self.IS_THEME_MATERIAL

    def is_social_plugin_enabled_mkdocs(self, mkdocs_config: Config) -> bool:
        """Check if social plugin is installed and enabled.

        Args:
            mkdocs_config (Config): Mkdocs website configuration object.

        Returns:
            bool: True if the theme material and the plugin social cards is enabled.
        """
        if not self.is_theme_material(mkdocs_config=mkdocs_config):
            logger.debug("Installed theme is not 'material'. Integration disabled.")
            return False

        if not mkdocs_config.plugins.get("material/social"):
            logger.debug("Social plugin not listed in configuration.")
            return False

        social_plugin_cfg = mkdocs_config.plugins.get("material/social")

        if not social_plugin_cfg.config.enabled:
            logger.debug("Social plugin is installed but disabled.")
            self.IS_SOCIAL_PLUGIN_ENABLED = False
            return False

        logger.debug("Social plugin is enabled in Mkdocs configuration.")
        self.IS_SOCIAL_PLUGIN_CARDS_ENABLED = True
        return True

    def is_social_plugin_and_cards_enabled_mkdocs(self, mkdocs_config: Config) -> bool:
        """Check if social cards plugin is enabled.

        Args:
            mkdocs_config (Config): Mkdocs website configuration object.

        Returns:
            bool: True if the theme material and the plugin social cards is enabled.
        """
        if not self.is_social_plugin_enabled_mkdocs(mkdocs_config=mkdocs_config):
            return False

        social_plugin_cfg = mkdocs_config.plugins.get("material/social")

        if not social_plugin_cfg.config.cards:
            logger.debug("Social plugin is installed, present but cards are disabled.")
            self.IS_SOCIAL_PLUGIN_CARDS_ENABLED = False
            return False

        logger.debug("Social cards are enabled in Mkdocs configuration.")
        self.IS_SOCIAL_PLUGIN_CARDS_ENABLED = True
        return True

    def is_social_plugin_enabled_page(
        self, mkdocs_page: Page, fallback_value: bool = True
    ) -> bool:
        """Check if the social plugin is enabled or disabled for a specific page. Plugin
            has to enabled in Mkdocs configuration before.

        Args:
            mkdocs_page (Page): Mkdocs page object.
            fallback_value (bool, optional): fallback value. It might be the
                'plugins.social.cards.enabled' option in Mkdocs config. Defaults to True.

        Returns:
            bool: True if the social cards are enabled for a page.
        """
        return mkdocs_page.meta.get("social", {"cards": fallback_value}).get(
            "cards", fallback_value
        )

    def get_social_cards_dir(self, mkdocs_config: Config) -> str:
        """Get Social Cards folder within Mkdocs site_dir.
        See: https://squidfunk.github.io/mkdocs-material/plugins/social/#config.cards_dir

        Args:
            mkdocs_config (Config): Mkdocs website configuration object.

        Returns:
            str: True if the theme material and the plugin social cards is enabled.
        """
        social_plugin_cfg = mkdocs_config.plugins.get("material/social")

        logger.debug(
            "Social cards folder in Mkdocs build directory: "
            f"{social_plugin_cfg.config.cards_dir}."
        )

        return social_plugin_cfg.config.cards_dir

    def get_social_card_build_path_for_page(
        self, mkdocs_page: Page, mkdocs_site_dir: Optional[str] = None
    ) -> Path:
        """Get social card URL for a specific page in documentation.

        Args:
            mkdocs_page (Page): Mkdocs page object.
            mkdocs_site_dir (Optional[str], optional): Mkdocs build site dir. If None, the
                'class.mkdocs_site_build_dir' is used. is Defaults to None.

        Returns:
            str: URL to the image once published
        """
        if mkdocs_site_dir is None and self.mkdocs_site_build_dir:
            mkdocs_site_dir = self.mkdocs_site_build_dir

        return Path(
            f"{mkdocs_site_dir}/{self.social_cards_assets_dir}/"
            f"{Path(mkdocs_page.file.src_uri).with_suffix('.png')}"
        )

    def get_social_card_url_for_page(
        self,
        mkdocs_page: Page,
        mkdocs_site_url: Optional[str] = None,
    ) -> str:
        """Get social card URL for a specific page in documentation.

        Args:
            mkdocs_page (Page): Mkdocs page object.
            mkdocs_site_url (Optional[str], optional): Mkdocs site URL. If None, the
                'class.mkdocs_site_url' is used. is Defaults to None.

        Returns:
            str: URL to the image once published
        """
        if mkdocs_site_url is None and self.mkdocs_site_url:
            mkdocs_site_url = self.mkdocs_site_url

        return f"{mkdocs_site_url}assets/images/social/{Path(mkdocs_page.file.src_uri).with_suffix('.png')}"
