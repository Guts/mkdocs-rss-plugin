#! python3  # noqa: E265

"""Test that title and description don't contain double-encoded HTML entities.

MkDocs pre-escapes content, so Jinja's |e filter should not double-encode.

Usage from the repo root folder:

    python -m unittest tests.test_double_encoded_entities

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


class TestDoubleEncodedEntities(BaseTest):
    """Test that HTML entities are not double-encoded in RSS feed."""

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
