#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

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

    def __init__(self, mkdocs_config: MkDocsConfig) -> None:
        """Integration instantiation.

        Args:
            mkdocs_config (MkDocsConfig): Mkdocs website configuration object.
        """
        # store Mkdocs config as attribute
        self.mkdocs_config = mkdocs_config

        self.IS_THEME_MATERIAL = self.is_mkdocs_theme_material()

    def is_mkdocs_theme_material(
        self, mkdocs_config: MkDocsConfig | None = None
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
