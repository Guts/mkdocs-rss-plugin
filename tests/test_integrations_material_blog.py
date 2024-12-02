#! python3  # noqa E265

"""Usage from the repo root folder:

.. code-block:: python

    # for whole test
    python -m unittest tests.test_build

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
from logging import DEBUG, getLogger
from pathlib import Path

# 3rd party
from mkdocs.config import load_config

# package
from mkdocs_rss_plugin.integrations.theme_material_blog_plugin import (
    IntegrationMaterialBlog,
)

# test suite
from tests.base import BaseTest

# #############################################################################
# ########## Classes ###############
# ##################################

logger = getLogger(__name__)
logger.setLevel(DEBUG)


class TestRssPluginIntegrationsMaterialBlog(BaseTest):
    """Test integration of Material Blog plugin with RSS plugin."""

    # -- TESTS ---------------------------------------------------------
    def test_plugin_config_blog_enabled(self):
        # default reference
        cfg_mkdocs = load_config(
            str(Path("tests/fixtures/mkdocs_items_material_blog_enabled.yml").resolve())
        )

        integration_social_cards = IntegrationMaterialBlog(mkdocs_config=cfg_mkdocs)
        self.assertTrue(integration_social_cards.IS_THEME_MATERIAL)
        self.assertTrue(integration_social_cards.IS_BLOG_PLUGIN_ENABLED)
        self.assertTrue(integration_social_cards.IS_ENABLED)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
