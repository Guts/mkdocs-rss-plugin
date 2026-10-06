#! python3  # noqa: E265

"""Test that <enclosure> is omitted when image length is None or non-positive.

When a remote image returns 404, the length field becomes None,
which would produce invalid XML like <enclosure length="None" />.

Usage from the repo root folder:

    python -m unittest tests.test_enclosure_guard

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import tempfile
from pathlib import Path
from traceback import format_exception

# test suite
from tests.base import BaseTest

# -- Globals --
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

OUTPUT_RSS_FEED_CREATED = "feed_rss_created.xml"

# #############################################################################
# ########## Classes ###############
# ##################################


class TestEnclosureGuard(BaseTest):
    """Test that <enclosure> is properly guarded against invalid length values."""

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
