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
from mkdocs_rss_plugin.integrations.theme_material_base import (
    IntegrationMaterialThemeBase,
)

# test suite
from tests.base import BaseTest

# #############################################################################
# ########## Classes ###############
# ##################################

logger = getLogger(__name__)
logger.setLevel(DEBUG)


class TestRssPluginIntegrationsMaterialThem(BaseTest):
    """Test integration of Material theme."""

    # -- TESTS ---------------------------------------------------------
    def test_plugin_config_theme_material(self):
        # default reference
        cfg_mkdocs = load_config(
            str(Path("tests/fixtures/mkdocs_language_specific_material.yml").resolve())
        )

        integration_social_cards = IntegrationMaterialThemeBase(
            mkdocs_config=cfg_mkdocs
        )
        self.assertTrue(integration_social_cards.IS_THEME_MATERIAL)

    def test_plugin_config_theme_not_material(self):
        # default reference
        cfg_mkdocs = load_config(
            str(Path("tests/fixtures/mkdocs_complete.yml").resolve())
        )

        integration_social_cards = IntegrationMaterialThemeBase(
            mkdocs_config=cfg_mkdocs
        )
        self.assertFalse(integration_social_cards.IS_THEME_MATERIAL)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
