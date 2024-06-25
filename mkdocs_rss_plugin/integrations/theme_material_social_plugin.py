#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import json
from hashlib import md5
from pathlib import Path
from typing import Optional

# 3rd party
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.pages import Page

# package
from mkdocs_rss_plugin.constants import MKDOCS_LOGGER_NAME

# conditional
try:
    from material import __version__ as material_version
except ImportError:
    material_version = None

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
    IS_INSIDERS: bool = False
    CARDS_MANIFEST: Optional[dict] = None

    def __init__(self, mkdocs_config: MkDocsConfig, switch_force: bool = True) -> None:
        """Integration instantiation.

        Args:
            mkdocs_config (MkDocsConfig): Mkdocs website configuration object.
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
            self.social_cards_assets_dir = self.get_social_cards_build_dir(
                mkdocs_config=mkdocs_config
            )
            self.social_cards_cache_dir = self.get_social_cards_cache_dir(
                mkdocs_config=mkdocs_config
            )
            if self.is_mkdocs_theme_material_insiders():
                self.load_cache_cards_manifest()

            # store some attributes used to compute social card hash
            self.site_name = mkdocs_config.site_name
            self.site_description = mkdocs_config.site_description or ""

    def is_mkdocs_theme_material(self, mkdocs_config: MkDocsConfig) -> bool:
        """Check if the theme set in mkdocs.yml is material or not.

        Args:
            mkdocs_config (MkDocsConfig): Mkdocs website configuration object.

        Returns:
            bool: True if the theme's name is 'material'. False if not.
        """
        self.IS_THEME_MATERIAL = mkdocs_config.theme.name == "material"
        return self.IS_THEME_MATERIAL

    def is_mkdocs_theme_material_insiders(self) -> Optional[bool]:
        """Check if the material theme is community or insiders edition.

        Returns:
            bool: True if the theme is Insiders edition. False if community. None if
                the Material theme is not installed.
        """
        if not self.IS_THEME_MATERIAL:
            return None

        if material_version is not None and "insiders" in material_version:
            logger.debug("Material theme edition INSIDERS")
            self.IS_INSIDERS = True
            return True
        else:
            logger.debug("Material theme edition COMMUNITY")
            self.IS_INSIDERS = False
            return False

    def is_social_plugin_enabled_mkdocs(self, mkdocs_config: MkDocsConfig) -> bool:
        """Check if social plugin is installed and enabled.

        Args:
            mkdocs_config (MkDocsConfig): Mkdocs website configuration object.

        Returns:
            bool: True if the theme material and the plugin social cards is enabled.
        """
        if not self.is_mkdocs_theme_material(mkdocs_config=mkdocs_config):
            logger.debug("Installed theme is not 'material'. Integration disabled.")
            return False

        if not mkdocs_config.plugins.get("material/social"):
            logger.debug("Material Social plugin not listed in configuration.")
            return False

        social_plugin_cfg = mkdocs_config.plugins.get("material/social")

        if not social_plugin_cfg.config.enabled:
            logger.debug("Material Social plugin is installed but disabled.")
            self.IS_SOCIAL_PLUGIN_ENABLED = False
            return False

        logger.debug("Material Social plugin is enabled in Mkdocs configuration.")
        self.IS_SOCIAL_PLUGIN_CARDS_ENABLED = True
        return True

    def is_social_plugin_and_cards_enabled_mkdocs(
        self, mkdocs_config: MkDocsConfig
    ) -> bool:
        """Check if social cards plugin is enabled.

        Args:
            mkdocs_config (MkDocsConfig): Mkdocs website configuration object.

        Returns:
            bool: True if the theme material and the plugin social cards is enabled.
        """
        if not self.is_social_plugin_enabled_mkdocs(mkdocs_config=mkdocs_config):
            return False

        social_plugin_cfg = mkdocs_config.plugins.get("material/social")

        if not social_plugin_cfg.config.cards:
            logger.debug(
                "Material Social plugin is installed, present but cards are disabled."
            )
            self.IS_SOCIAL_PLUGIN_CARDS_ENABLED = False
            return False

        logger.debug("Material Social cards are enabled in Mkdocs configuration.")
        self.IS_SOCIAL_PLUGIN_CARDS_ENABLED = True
        return True

    def is_social_plugin_enabled_page(
        self, mkdocs_page: Page, fallback_value: bool = True
    ) -> bool:
        """Check if the social plugin is enabled or disabled for a specific page. Plugin
            has to be enabled in Mkdocs configuration before.

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

    def load_cache_cards_manifest(self) -> Optional[dict]:
        """Load social cards manifest if the file exists.

        Returns:
            dict | None: manifest as dict or None if the file does not exist
        """
        cache_cards_manifest = Path(self.social_cards_cache_dir).joinpath(
            "manifest.json"
        )
        if not cache_cards_manifest.is_file():
            logger.debug(
                "Material Social Cards cache manifest file not found: "
                f"{cache_cards_manifest}"
            )
            return None

        with cache_cards_manifest.open(mode="r", encoding="UTF-8") as manifest:
            self.CARDS_MANIFEST = json.load(manifest)
        logger.debug(
            f"Material Social Cards cache manifest loaded from {cache_cards_manifest}"
        )

        return self.CARDS_MANIFEST

    def get_social_cards_build_dir(self, mkdocs_config: MkDocsConfig) -> Path:
        """Get Social Cards folder within Mkdocs site_dir.
        See: https://squidfunk.github.io/mkdocs-material/plugins/social/#config.cards_dir

        Args:
            mkdocs_config (MkDocsConfig): Mkdocs website configuration object.

        Returns:
            str: True if the theme material and the plugin social cards is enabled.
        """
        social_plugin_cfg = mkdocs_config.plugins.get("material/social")

        logger.debug(
            "Material Social cards folder in Mkdocs build directory: "
            f"{social_plugin_cfg.config.cards_dir}."
        )

        return Path(social_plugin_cfg.config.cards_dir).resolve()

    def get_social_cards_cache_dir(self, mkdocs_config: MkDocsConfig) -> Path:
        """Get Social Cards folder within Mkdocs site_dir.
        See: https://squidfunk.github.io/mkdocs-material/plugins/social/#config.cards_dir

        Args:
            mkdocs_config (MkDocsConfig): Mkdocs website configuration object.

        Returns:
            str: True if the theme material and the plugin social cards is enabled.
        """
        social_plugin_cfg = mkdocs_config.plugins.get("material/social")
        self.social_cards_cache_dir = Path(social_plugin_cfg.config.cache_dir).resolve()

        logger.debug(
            "Material Social cards cache folder: " f"{self.social_cards_cache_dir}."
        )

        return self.social_cards_cache_dir

    def get_social_card_build_path_for_page(
        self, mkdocs_page: Page, mkdocs_site_dir: Optional[str] = None
    ) -> Optional[Path]:
        """Get social card path in Mkdocs build dir for a specific page.

        Args:
            mkdocs_page (Page): Mkdocs page object.
            mkdocs_site_dir (Optional[str], optional): Mkdocs build site dir. If None, the
                'class.mkdocs_site_build_dir' is used. is Defaults to None.

        Returns:
            Path: path to the image once published
        """
        if mkdocs_site_dir is None and self.mkdocs_site_build_dir:
            mkdocs_site_dir = self.mkdocs_site_build_dir

        expected_built_card_path = Path(
            f"{mkdocs_site_dir}/{self.social_cards_assets_dir}/"
            f"{Path(mkdocs_page.file.src_uri).with_suffix('.png')}"
        )

        if expected_built_card_path.is_file():
            logger.debug(
                f"Social card file found in cache folder: {expected_built_card_path}"
            )
            return expected_built_card_path
        else:
            logger.debug(f"Not found: {expected_built_card_path}")
            return None

    def get_social_card_cache_path_for_page(self, mkdocs_page: Page) -> Optional[Path]:
        """Get social card path in social plugin cache folder for a specific page.

        Note:
            As we write this code (June 2024), the cache mechanism in Insiders edition
            has stores images directly with the corresponding Page's path and name and
            keep a correspondance matrix with hashes in a manifest.json;
            the cache mechanism in Community edition uses the hash as file names without
            any exposed matching criteria.

        Args:
            mkdocs_page (Page): Mkdocs page object.

        Returns:
            Path: path to the image in local cache folder if it exists
        """
        if self.IS_INSIDERS:
            expected_cached_card_path = self.social_cards_cache_dir.joinpath(
                f"assets/images/social/{Path(mkdocs_page.file.src_uri).with_suffix('.png')}"
            )
            if expected_cached_card_path.is_file():
                logger.debug(
                    f"Social card file found in cache folder: {expected_cached_card_path}"
                )
                return expected_cached_card_path
            else:
                logger.debug(f"Not found: {expected_cached_card_path}")

        else:
            if "description" in mkdocs_page.meta:
                description = mkdocs_page.meta["description"]
            else:
                description = self.site_description

            page_hash = md5(
                "".join(
                    [
                        self.site_name,
                        str(mkdocs_page.meta.get("title", mkdocs_page.title)),
                        description,
                    ]
                ).encode("utf-8")
            )
            expected_cached_card_path = self.social_cards_cache_dir.joinpath(
                f"{page_hash.hexdigest()}.png"
            )

        if expected_cached_card_path.is_file():
            logger.debug(
                f"Social card file found in cache folder: {expected_cached_card_path}"
            )
            return expected_cached_card_path
        else:
            logger.debug(f"Not found: {expected_cached_card_path}")
            return None

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
