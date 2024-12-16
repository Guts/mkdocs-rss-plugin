#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from functools import lru_cache
from pathlib import Path
from typing import Optional

# 3rd party
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.pages import Page

# package
from mkdocs_rss_plugin.constants import MKDOCS_LOGGER_NAME
from mkdocs_rss_plugin.integrations.theme_material_base import (
    IntegrationMaterialThemeBase,
)

# conditional
try:
    from material import __version__ as material_version
    from material.plugins.blog.plugin import BlogPlugin

except ImportError:
    material_version = None


# ############################################################################
# ########## Globals #############
# ################################

logger = get_plugin_logger(MKDOCS_LOGGER_NAME)

# ############################################################################
# ########## Logic ###############
# ################################


class IntegrationMaterialBlog(IntegrationMaterialThemeBase):
    # attributes
    IS_ENABLED: bool = True
    IS_BLOG_PLUGIN_ENABLED: bool = True

    def __init__(self, mkdocs_config: MkDocsConfig, switch_force: bool = True) -> None:
        """Integration instantiation.

        Args:
            mkdocs_config (MkDocsConfig): Mkdocs website configuration object.
            switch_force (bool, optional): option to force integration disabling. Set
                it to False to disable it even if Social Cards are enabled in Mkdocs
                configuration. Defaults to True.
        """
        # check if the integration can be enabled or not
        self.IS_BLOG_PLUGIN_ENABLED = self.is_blog_plugin_enabled_mkdocs(
            mkdocs_config=mkdocs_config
        )
        # if every conditions are True, enable the integration
        self.IS_ENABLED = all([self.IS_THEME_MATERIAL, self.IS_BLOG_PLUGIN_ENABLED])

        # except if the end-user wants to disable it
        if switch_force is False:
            self.IS_ENABLED = False
            logger.debug(
                "Integration with Blog (Material theme) is "
                "disabled in plugin's option in Mkdocs configuration."
            )

    def is_blog_plugin_enabled_mkdocs(
        self, mkdocs_config: Optional[MkDocsConfig]
    ) -> bool:
        """Check if blog plugin is installed and enabled.

        Args:
            mkdocs_config (Optional[MkDocsConfig]): Mkdocs website configuration object.

        Returns:
            bool: True if the theme material and the plugin blog is enabled.
        """
        if mkdocs_config is None and isinstance(self.mkdocs_config, MkDocsConfig):
            mkdocs_config = self.mkdocs_config

        if not self.is_mkdocs_theme_material(mkdocs_config=mkdocs_config):
            logger.debug("Installed theme is not 'material'. Integration disabled.")
            return False

        if not mkdocs_config.plugins.get("material/blog"):
            logger.debug("Material blog plugin is not listed in configuration.")
            self.IS_BLOG_PLUGIN_ENABLED = False
            return False

        self.blog_plugin_cfg: BlogPlugin | None = mkdocs_config.plugins.get(
            "material/blog"
        )

        if not self.blog_plugin_cfg.config.enabled:
            logger.debug("Material blog plugin is installed but disabled.")
            self.IS_BLOG_PLUGIN_ENABLED = False
            return False

        logger.debug("Material blog plugin is enabled in Mkdocs configuration.")
        self.IS_BLOG_PLUGIN_ENABLED = True
        return True

    @lru_cache
    def author_name_from_id(self, author_id: str) -> str:
        """Return author name from author_id used in Material blog plugin (.authors.yml).

        Args:
            author_id (str): author key in .authors.yml

        Returns:
            str: author name or passed author_id if not found within .authors.yml
        """
        if (
            self.blog_plugin_cfg.config.authors
            and isinstance(self.blog_plugin_cfg, BlogPlugin)
            and hasattr(self.blog_plugin_cfg, "authors")
            and isinstance(self.blog_plugin_cfg.authors, dict)
        ):
            if author_id in self.blog_plugin_cfg.authors:
                author_metadata = self.blog_plugin_cfg.authors.get(author_id)
                if "email" in self.blog_plugin_cfg.authors.get(author_id):
                    return f"{author_metadata.get('email')} ({author_metadata.get('name')})"
                else:
                    return author_metadata.get("name")
            else:
                logger.error(
                    f"Author ID '{author_id}' is not part of known authors: "
                    f"{self.blog_plugin_cfg.authors}. Returning author_id."
                )
                return author_id

    def is_page_a_blog_post(self, mkdocs_page: Page) -> bool:
        """Identifies if the given page is part of Material Blog.

        Args:
            mkdocs_page (Page): page to identify

        Returns:
            bool: True if the given page is a Material Blog post.
        """
        return Path(mkdocs_page.file.src_uri).is_relative_to(
            self.blog_plugin_cfg.config.blog_dir
        )
