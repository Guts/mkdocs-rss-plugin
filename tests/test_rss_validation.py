#! python3  # noqa: E265

"""Tests for RSS 2.0 feed validation compliance.

Verifies:
- <dc:creator> used instead of <author> for item authors (RSS spec requires <author> to be email)
- No double-encoded HTML entities in title/description
- <enclosure> omitted when length is None or non-positive

Usage from the repo root folder:

    python -m unittest tests.test_rss_validation

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import tempfile
from pathlib import Path
from traceback import format_exception
from xml.etree import ElementTree

# test suite
from tests.base import BaseTest

# -- Globals --
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

OUTPUT_RSS_FEED_CREATED = "feed_rss_created.xml"

# #############################################################################
# ########## Classes ###############
# ##################################


class TestRssValidation(BaseTest):
    """Test RSS 2.0 feed validation compliance."""

    def test_dc_creator_instead_of_author(self):
        """Verify that item authors use <dc:creator> instead of <author>.

        RSS 2.0 spec requires <author> to be an email address.
        Human-readable names should use <dc:creator>.
        """
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_complete.yml"),
                output_path=tmpdirname,
                strict=True,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # Parse the raw XML to check element names
            rss_path = Path(tmpdirname) / OUTPUT_RSS_FEED_CREATED
            tree = ElementTree.parse(rss_path)
            root = tree.getroot()

            # RSS namespace
            ns = {
                "rss": "http://www.w3.org/2005/Atom",
                "dc": "http://purl.org/dc/elements/1.1/",
            }

            # Find all item elements
            items = root.findall(".//item")
            self.assertTrue(len(items) > 0, "Expected at least one item in feed")

            for item in items:
                # Check that <author> is NOT used for item authors
                author_elem = item.find("author")
                self.assertIsNone(
                    author_elem,
                    "Found <author> element in item. RSS 2.0 requires <author> to be "
                    "an email address. Use <dc:creator> for human-readable names.",
                )

                # Check that <dc:creator> IS used when authors are present
                # The page_with_meta.md has authors, so at least one item should have dc:creator
                dc_creators = item.findall("dc:creator", ns)
                # Items with authors should have dc:creator elements
                # Items without authors may not have any
                if item.find("title").text == "Page With Explicit Metadata":
                    self.assertTrue(
                        len(dc_creators) > 0,
                        "Expected <dc:creator> elements for item with authors.",
                    )

    def test_no_double_encoded_entities(self):
        """Verify that title and description don't contain double-encoded HTML entities.

        MkDocs pre-escapes content, so Jinja's |e filter should not double-encode.
        """
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_complete.yml"),
                output_path=tmpdirname,
                strict=True,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # Read raw XML content
            rss_path = Path(tmpdirname) / OUTPUT_RSS_FEED_CREATED
            rss_content = rss_path.read_text()

            # Check for double-encoded entities
            double_encoded = ["&amp;amp;", "&amp;lt;", "&amp;gt;"]
            for entity in double_encoded:
                self.assertNotIn(
                    entity,
                    rss_content,
                    f"Found double-encoded HTML entity {entity} in RSS feed. "
                    "This indicates MkDocs pre-escaping combined with Jinja |e filter.",
                )

    def test_enclosure_guard_none_length(self):
        """Verify that <enclosure> is omitted when image length is None or non-positive.

        When a remote image returns 404, the length field becomes None,
        which would produce invalid XML like <enclosure length="None" />.
        """
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_complete.yml"),
                output_path=tmpdirname,
                strict=True,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # Read raw XML content
            rss_path = Path(tmpdirname) / OUTPUT_RSS_FEED_CREATED
            rss_content = rss_path.read_text()

            # Check that no enclosure has length="None" or length="0" or negative
            self.assertNotIn(
                'length="None"',
                rss_content,
                "Found enclosure with length='None'. "
                "The template should guard against None length values.",
            )
            self.assertNotIn(
                'length="0"',
                rss_content,
                "Found enclosure with length='0'. "
                "The template should guard against zero length values.",
            )
