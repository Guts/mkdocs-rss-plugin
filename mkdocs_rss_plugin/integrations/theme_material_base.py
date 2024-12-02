#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from typing import Optional

# 3rd party
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger

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


class IntegrationMaterialThemeBase:
    # attributes
    IS_THEME_MATERIAL: bool = False
    IS_INSIDERS: Optional[bool] = False

    def __init__(self, mkdocs_config: MkDocsConfig) -> None:
        """Integration instantiation.

        Args:
            mkdocs_config (MkDocsConfig): Mkdocs website configuration object.
        """
        # store Mkdocs config as attribute
        self.mkdocs_config = mkdocs_config

        self.IS_THEME_MATERIAL = self.is_mkdocs_theme_material()
        self.IS_INSIDERS = self.is_mkdocs_theme_material_insiders()

    def is_mkdocs_theme_material(
        self, mkdocs_config: Optional[MkDocsConfig] = None
    ) -> bool:
        """Check if the theme set in mkdocs.yml is material or not.

        Args:
            mkdocs_config (Optional[MkDocsConfig]): Mkdocs website configuration object.

        Returns:
            bool: True if the theme's name is 'material'. False if not.
        """
        if mkdocs_config is None and isinstance(self.mkdocs_config, MkDocsConfig):
            mkdocs_config: MkDocsConfig = self.mkdocs_config

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
