#! python3  # noqa E265

"""Test build without Material theme installed.

Usage from the repo root folder:

.. code-block:: python

    # for whole test
    python -m unittest tests.test_build_without_material
    # for specific test
    python -m unittest tests.test_build_without_material.TestBuildWithoutMaterial.test_build_without_material_theme
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# 3rd party
import feedparser

# test suite
from tests.base import BaseTest

# #############################################################################
# ########## Globals ###############
# ##################################

OUTPUT_RSS_FEED_CREATED = "feed_rss_created.xml"
OUTPUT_RSS_FEED_UPDATED = "feed_rss_updated.xml"
OUTPUT_JSON_FEED_CREATED = "feed_json_created.json"
OUTPUT_JSON_FEED_UPDATED = "feed_json_updated.json"


# #############################################################################
# ########## Classes ###############
# ##################################


class TestBuildWithoutMaterial(BaseTest):
    """Test MkDocs build with RSS plugin when Material theme is not available."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.feed_image = "https://github.com/Guts/mkdocs-rss-plugin/blob/main/docs/assets/logo_rss_plugin_mkdocs.png?raw=true"

    def setUp(self):
        """Executed before each test."""
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        pass

    # -- TESTS ---------------------------------------------------------
    def test_build_without_material_theme(self):
        """Test that the plugin works correctly when Material theme is not installed.

        This test simulates the absence of the Material theme by temporarily
        blocking its import, ensuring the RSS plugin gracefully handles the missing
        dependency.
        """
        # Mock the material module to simulate it not being installed
        with patch.dict(sys.modules, {"material": None}):
            # Also need to mock the submodules
            with patch.dict(
                sys.modules,
                {
                    "material.plugins": None,
                    "material.plugins.blog": None,
                    "material.plugins.blog.plugin": None,
                    "material.plugins.blog.structure": None,
                },
            ):
                with tempfile.TemporaryDirectory() as tmpdirname:
                    cli_result = self.build_docs_setup(
                        testproject_path="docs",
                        mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_minimal.yml"),
                        output_path=tmpdirname,
                        strict=True,
                    )

                    if cli_result.exception is not None:
                        e = cli_result.exception
                        return e

                    self.assertEqual(cli_result.exit_code, 0)
                    self.assertIsNone(cli_result.exception)

                    # Verify RSS feeds were created
                    self.assertTrue(
                        Path(tmpdirname).joinpath(OUTPUT_RSS_FEED_CREATED).exists()
                    )
                    self.assertTrue(
                        Path(tmpdirname).joinpath(OUTPUT_RSS_FEED_UPDATED).exists()
                    )

                    # Verify feeds are valid
                    feed_created = feedparser.parse(
                        Path(tmpdirname) / OUTPUT_RSS_FEED_CREATED
                    )
                    self.assertEqual(feed_created.bozo, 0)

                    feed_updated = feedparser.parse(
                        Path(tmpdirname) / OUTPUT_RSS_FEED_UPDATED
                    )
                    self.assertEqual(feed_updated.bozo, 0)

    def test_build_with_material_config_but_theme_not_installed(self):
        """Test build with Material-specific config when the theme is not installed.

        This test uses a configuration file that references Material theme features
        (like blog plugin) but simulates the theme not being installed. The plugin
        should handle this gracefully without crashing.
        """
        with patch.dict(sys.modules, {"material": None}):
            with patch.dict(
                sys.modules,
                {
                    "material.plugins": None,
                    "material.plugins.blog": None,
                    "material.plugins.blog.plugin": None,
                    "material.plugins.blog.structure": None,
                },
            ):
                with tempfile.TemporaryDirectory() as tmpdirname:
                    # Use a config that would normally use Material features
                    cli_result = self.build_docs_setup(
                        testproject_path="docs",
                        mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_complete.yml"),
                        output_path=tmpdirname,
                        strict=False,  # Don't fail on warnings
                    )

                    if cli_result.exception is not None:
                        e = cli_result.exception
                        return e

                    # Build should succeed even without Material
                    self.assertEqual(cli_result.exit_code, 0)
                    self.assertIsNone(cli_result.exception)

                    # Verify feeds were created and are valid
                    feed_created = feedparser.parse(
                        Path(tmpdirname) / OUTPUT_RSS_FEED_CREATED
                    )
                    self.assertEqual(feed_created.bozo, 0)
                    self.assertGreater(len(feed_created.entries), 0)

    def test_page_processing_without_material(self):
        """Test that page processing works correctly without Material theme.

        Ensures that pages are processed correctly and their metadata is extracted
        even when Material-specific features are not available.
        """
        with patch.dict(sys.modules, {"material": None}):
            with patch.dict(
                sys.modules,
                {
                    "material.plugins": None,
                    "material.plugins.blog": None,
                    "material.plugins.blog.plugin": None,
                    "material.plugins.blog.structure": None,
                },
            ):
                with tempfile.TemporaryDirectory() as tmpdirname:
                    # Use complete config which includes pages with authors
                    cli_result = self.build_docs_setup(
                        testproject_path="docs",
                        mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_complete.yml"),
                        output_path=tmpdirname,
                        strict=False,  # Material theme not available
                    )

                    self.assertEqual(cli_result.exit_code, 0)
                    self.assertIsNone(cli_result.exception)

                    # Parse the created feed
                    feed_parsed = feedparser.parse(
                        Path(tmpdirname) / OUTPUT_RSS_FEED_CREATED
                    )

                    # Verify feed has entries
                    self.assertGreater(
                        len(feed_parsed.entries),
                        0,
                        "Feed should contain at least one entry",
                    )

                    # Verify entries have required fields
                    for entry in feed_parsed.entries:
                        self.assertIn(
                            "title",
                            entry,
                            f"Entry '{entry.get('title', 'UNKNOWN')}' missing title",
                        )
                        self.assertIn(
                            "link", entry, f"Entry '{entry.title}' missing link"
                        )
                        self.assertIn(
                            "description",
                            entry,
                            f"Entry '{entry.title}' missing description",
                        )
                        self.assertIn(
                            "published",
                            entry,
                            f"Entry '{entry.title}' missing published date",
                        )

                    # Look for the specific page with complete metadata
                    page_with_complete_meta = next(
                        (
                            e
                            for e in feed_parsed.entries
                            if e.title == "Page with complete meta"
                        ),
                        None,
                    )

                    # This page should exist and have author metadata
                    self.assertIsNotNone(
                        page_with_complete_meta,
                        "Page 'Page with complete meta' should be in the feed. "
                        f"Available pages: {', '.join([e.title for e in feed_parsed.entries])}",
                    )

                    self.assertIn(
                        "author",
                        page_with_complete_meta,
                        "Page 'Page with complete meta' should have author metadata",
                    )
                    self.assertIsNotNone(
                        page_with_complete_meta.description,
                        "Page 'Page with complete meta' should have a description",
                    )


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
