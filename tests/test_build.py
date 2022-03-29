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

# logging
from logging import DEBUG, getLogger
from pathlib import Path
from traceback import format_exception

# 3rd party
import feedparser

# test suite
from tests.base import BaseTest

logger = getLogger(__name__)
logger.setLevel(DEBUG)

# #############################################################################
# ########## Classes ###############
# ##################################


class TestBuildRss(BaseTest):
    """Test MkDocs build with RSS plugin."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.config_files = sorted(Path("tests/fixtures/").glob("**/*.yml"))
        cls.feed_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Feed-icon.svg/128px-Feed-icon.svg.png"

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
    def test_simple_build(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            run_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("mkdocs.yml"),
                output_path=tmpdirname,
            )
            self.assertEqual(run_result.exit_code, 0)
            self.assertIsNone(run_result.exception)

    def test_simple_build_disabled(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            run_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_disabled.yml"),
                output_path=tmpdirname,
            )
            if run_result.exception is not None:
                e = run_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(run_result.exit_code, 0)
            self.assertIsNone(run_result.exception)

    def test_simple_build_feed_length(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            run_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path(
                    "tests/fixtures/mkdocs_feed_length_custom.yml"
                ),
                output_path=tmpdirname,
            )
            if run_result.exception is not None:
                e = run_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(run_result.exit_code, 0)
            self.assertIsNone(run_result.exception)

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            self.assertEqual(feed_parsed.bozo, 0)

            # updated items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_updated.xml")
            self.assertEqual(feed_parsed.bozo, 0)

            self.assertEqual(len(feed_parsed.entries), 3)

    def test_rss_feed_validation(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("mkdocs.yml"),
                output_path=tmpdirname,
            )

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            self.assertEqual(feed_parsed.bozo, 0)

            # updated items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_updated.xml")
            self.assertEqual(feed_parsed.bozo, 0)

            # some feed characteristics
            self.assertEqual(feed_parsed.version, "rss20")


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
