#! python3  # noqa E265

"""Usage from the repo root folder:

.. code-block:: python

    # for whole test
    python -m unittest tests.test_atom

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import tempfile
import unittest
from pathlib import Path
from traceback import format_exception

# 3rd party
import feedparser

# test suite
from tests.base import BaseTest

# -- Globals --
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

OUTPUT_ATOM_FEED_CREATED = "feed_atom_created.xml"
OUTPUT_ATOM_FEED_UPDATED = "feed_atom_updated.xml"


# #############################################################################
# ########## Classes ###############
# ##################################


class TestBuildAtom(BaseTest):
    """Test MkDocs build with Atom feed generation."""

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
    def test_simple_build_atom(self):
        """Test that Atom feeds are generated correctly."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_minimal.yml"),
                output_path=tmpdirname,
                strict=True,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # Check that Atom feeds were created
            self.assertTrue(
                Path(tmpdirname).joinpath(OUTPUT_ATOM_FEED_CREATED).exists()
            )
            self.assertTrue(
                Path(tmpdirname).joinpath(OUTPUT_ATOM_FEED_UPDATED).exists()
            )

    def test_atom_feed_validation(self):
        """Test that generated Atom feeds are valid."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_complete.yml"),
                output_path=tmpdirname,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / OUTPUT_ATOM_FEED_CREATED)
            self.assertEqual(feed_parsed.bozo, 0, "Feed should parse without errors")
            self.assertEqual(feed_parsed.version, "atom10", "Should be Atom 1.0 feed")

            # updated items
            feed_parsed = feedparser.parse(Path(tmpdirname) / OUTPUT_ATOM_FEED_UPDATED)
            self.assertEqual(feed_parsed.bozo, 0, "Feed should parse without errors")
            self.assertEqual(feed_parsed.version, "atom10", "Should be Atom 1.0 feed")

    def test_atom_feed_content(self):
        """Test that Atom feed contains correct elements."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_complete.yml"),
                output_path=tmpdirname,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # Parse the feed
            feed_parsed = feedparser.parse(Path(tmpdirname) / OUTPUT_ATOM_FEED_CREATED)

            # Check feed-level elements
            self.assertTrue(hasattr(feed_parsed.feed, "title"))
            self.assertTrue(hasattr(feed_parsed.feed, "subtitle"))
            self.assertTrue(hasattr(feed_parsed.feed, "updated"))
            self.assertTrue(hasattr(feed_parsed.feed, "id"))

            # Check entries
            for feed_item in feed_parsed.entries:
                # Mandatory properties
                self.assertTrue("title" in feed_item)
                self.assertTrue("id" in feed_item)
                self.assertTrue("updated" in feed_item)
                self.assertTrue("published" in feed_item)
                self.assertTrue("summary" in feed_item)

                # Links
                self.assertTrue("links" in feed_item)
                self.assertGreater(len(feed_item.links), 0)

    def test_atom_feed_dates_rfc3339(self):
        """Test that Atom feed dates are in RFC 3339 format (ISO 8601 with timezone)."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_complete.yml"),
                output_path=tmpdirname,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # Parse the feed
            feed_parsed = feedparser.parse(Path(tmpdirname) / OUTPUT_ATOM_FEED_CREATED)

            # Check feed updated date contains timezone
            self.assertIn(
                "+",
                feed_parsed.feed.updated,
                "Feed updated date should contain timezone offset",
            )

            # Check entry dates contain timezone
            for feed_item in feed_parsed.entries:
                self.assertIn(
                    "+",
                    feed_item.updated,
                    f"Entry '{feed_item.title}' updated date should contain timezone",
                )
                self.assertIn(
                    "+",
                    feed_item.published,
                    f"Entry '{feed_item.title}' published date should contain timezone",
                )

    def test_atom_feed_disabled(self):
        """Test that Atom feeds are not generated when disabled."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_atom_disabled.yml"),
                output_path=tmpdirname,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # Check that Atom feeds were NOT created
            self.assertFalse(
                Path(tmpdirname).joinpath(OUTPUT_ATOM_FEED_CREATED).exists()
            )
            self.assertFalse(
                Path(tmpdirname).joinpath(OUTPUT_ATOM_FEED_UPDATED).exists()
            )

    def test_atom_feed_full_content(self):
        """Test Atom feed with full content (abstract_chars_count: -1)."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path(
                    "tests/fixtures/mkdocs_item_length_unlimited.yml"
                ),
                output_path=tmpdirname,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # Parse the feed
            feed_parsed = feedparser.parse(Path(tmpdirname) / OUTPUT_ATOM_FEED_CREATED)

            # Check that entries have content element
            for feed_item in feed_parsed.entries:
                if feed_item.title not in (
                    "Page without meta with short text",
                    "Blog sample",
                    "Blog",
                ):
                    # Should have content element with full HTML
                    self.assertTrue(
                        "content" in feed_item,
                        f"Entry '{feed_item.title}' should have content element",
                    )
                    if "content" in feed_item:
                        self.assertGreater(
                            len(feed_item.content[0].value),
                            150,
                            f"Entry '{feed_item.title}' content should be longer than summary",
                        )

    def test_atom_feed_language(self):
        """Test that Atom feed has xml:lang attribute."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path(
                    "tests/fixtures/mkdocs_locale_with_territory.yml"
                ),
                output_path=tmpdirname,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # Read the raw XML to check for xml:lang attribute
            atom_file = Path(tmpdirname) / OUTPUT_ATOM_FEED_CREATED
            with atom_file.open("r", encoding="utf-8") as f:
                xml_content = f.read()

            # Check that xml:lang attribute is present
            self.assertIn('xml:lang="en-US"', xml_content)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
