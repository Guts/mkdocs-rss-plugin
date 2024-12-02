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
import tempfile
import unittest
from logging import DEBUG, getLogger
from pathlib import Path
from traceback import format_exception

# 3rd party
import feedparser
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
    def test_plugin_config_social_cards_enabled_but_integration_disabled(self):
        # default reference
        cfg_mkdocs = load_config(
            str(
                Path(
                    "tests/fixtures/mkdocs_items_material_blog_enabled_but_integration_disabled.yml"
                ).resolve()
            )
        )

        integration_social_cards = IntegrationMaterialBlog(
            mkdocs_config=cfg_mkdocs,
            switch_force=cfg_mkdocs.plugins.get("rss").config.use_material_blog,
        )
        self.assertTrue(integration_social_cards.IS_THEME_MATERIAL)
        self.assertTrue(integration_social_cards.IS_BLOG_PLUGIN_ENABLED)
        self.assertFalse(integration_social_cards.IS_ENABLED)

    def test_plugin_config_blog_enabled(self):
        # default reference
        cfg_mkdocs = load_config(
            str(Path("tests/fixtures/mkdocs_items_material_blog_enabled.yml").resolve())
        )

        integration_social_cards = IntegrationMaterialBlog(mkdocs_config=cfg_mkdocs)
        self.assertTrue(integration_social_cards.IS_THEME_MATERIAL)
        self.assertTrue(integration_social_cards.IS_BLOG_PLUGIN_ENABLED)
        self.assertTrue(integration_social_cards.IS_ENABLED)

    def test_simple_build(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path(
                    "tests/fixtures/mkdocs_items_material_blog_enabled.yml"
                ),
                output_path=tmpdirname,
                strict=False,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            self.assertEqual(feed_parsed.bozo, 0)

            # updated items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_updated.xml")
            self.assertEqual(feed_parsed.bozo, 0)

        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path(
                    "tests/fixtures/mkdocs_items_material_blog_enabled_but_integration_disabled.yml"
                ),
                output_path=tmpdirname,
                strict=False,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            self.assertEqual(feed_parsed.bozo, 0)

            # updated items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_updated.xml")
            self.assertEqual(feed_parsed.bozo, 0)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
