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
        # In case of some tests failure, ensure that everything is cleaned up
        # temp_page = Path("tests/fixtures/docs/temp_page_not_in_git_log.md")
        # if temp_page.exists():
        #     temp_page.unlink()

        git_dir = Path("_git")
        if git_dir.exists():
            git_dir.replace(git_dir.with_name(".git"))

    # -- TESTS ---------------------------------------------------------
    def test_simple_build(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_simple.yml"),
                output_path=tmpdirname,
                strict=False,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

    def test_simple_build_minimal(self):
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

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            for feed_item in feed_parsed.entries:
                # mandatory properties
                self.assertTrue("description" in feed_item)
                self.assertTrue("guid" in feed_item)
                self.assertTrue("link" in feed_item)
                self.assertTrue("published" in feed_item)
                self.assertTrue("source" in feed_item)
                self.assertTrue("title" in feed_item)
                # optional - following should not be present in the feed by default
                self.assertTrue("category" not in feed_item)
                self.assertTrue("comments" not in feed_item)
                self.assertTrue("enclosure" not in feed_item)

                if feed_item.title in ("Test page with meta",):
                    self.assertTrue("author" in feed_item)

    def test_simple_build_complete(self):
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

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            for feed_item in feed_parsed.entries:
                # mandatory properties
                self.assertTrue("description" in feed_item)
                self.assertTrue("guid" in feed_item)
                self.assertTrue("link" in feed_item)
                self.assertTrue("published" in feed_item)
                self.assertTrue("source" in feed_item)
                self.assertTrue("title" in feed_item)

                # optional - following should not be present in the feed by default
                if (
                    "without_meta" in feed_item.title
                    or feed_item.title == "Test home page"
                ):
                    self.assertTrue("category" not in feed_item)
                    self.assertTrue("comments" in feed_item)
                elif "with_meta" in feed_item.title:
                    self.assertTrue("author" in feed_item)
                    self.assertTrue("category" in feed_item)
                    self.assertTrue("enclosure" in feed_item)
                else:
                    pass

    def test_simple_build_disabled(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_disabled.yml"),
                output_path=tmpdirname,
            )
            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

    def test_simple_build_item_dates(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_dates_overridden.yml"),
                output_path=tmpdirname,
            )
            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

    def test_simple_build_feed_length(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path(
                    "tests/fixtures/mkdocs_feed_length_custom.yml"
                ),
                output_path=tmpdirname,
            )
            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            self.assertEqual(len(feed_parsed.entries), 3)

            # updated items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_updated.xml")
            self.assertEqual(len(feed_parsed.entries), 3)

    def test_simple_build_feed_ttl(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_feed_ttl_custom.yml"),
                output_path=tmpdirname,
            )
            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            self.assertNotEqual(feed_parsed.feed.ttl, "1440")
            self.assertEqual(feed_parsed.feed.ttl, "90")

            # updated items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_updated.xml")
            self.assertNotEqual(feed_parsed.feed.ttl, "1440")
            self.assertEqual(feed_parsed.feed.ttl, "90")

    def test_simple_build_item_categories_enabled(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_item_categories.yml"),
                output_path=tmpdirname,
                strict=True,
            )
            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")

            for feed_item in feed_parsed.entries:
                if feed_item.title in ("Test page with meta",):
                    self.assertTrue("category" in feed_item)

    def test_simple_build_item_comments_enabled(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_item_comments.yml"),
                output_path=tmpdirname,
                strict=True,
            )
            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            self.assertEqual(feed_parsed.bozo, 0)

            for feed_item in feed_parsed.entries:
                self.assertTrue("comments" in feed_item)

    def test_simple_build_item_comments_disabled(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_item_no_comments.yml"),
                output_path=tmpdirname,
                strict=True,
            )
            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            self.assertEqual(feed_parsed.bozo, 0)

            for feed_item in feed_parsed.entries:
                self.assertTrue("comments" not in feed_item)

    def test_simple_build_item_length_unlimited(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path(
                    "tests/fixtures/mkdocs_item_length_unlimited.yml"
                ),
                output_path=tmpdirname,
                strict=True,
            )
            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            self.assertEqual(feed_parsed.bozo, 0)

            for feed_item in feed_parsed.entries:
                if feed_item.title not in (
                    "Page without meta with short text",
                    "Blog sample",
                ):
                    self.assertGreaterEqual(
                        len(feed_item.description), 150, feed_item.title
                    )

    def test_simple_build_lang_with_territory(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path(
                    "tests/fixtures/mkdocs_lang_with_territory.yml"
                ),
                output_path=tmpdirname,
                strict=True,
            )

            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # created items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            self.assertEqual(feed_parsed.feed.get("language"), "en-US")

            # updated items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_updated.xml")
            self.assertEqual(feed_parsed.feed.get("language"), "en-US")

    def test_simple_build_pretty_print_enabled(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path(
                    "tests/fixtures/mkdocs_pretty_print_enabled.yml"
                ),
                output_path=tmpdirname,
            )
            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # created items
            with Path(Path(tmpdirname) / "feed_rss_created.xml").open("r") as f:
                self.assertGreater(len(f.readlines()), 0)

            # updated items
            with Path(Path(tmpdirname) / "feed_rss_updated.xml").open("r") as f:
                self.assertGreater(len(f.readlines()), 0)

    def test_simple_build_pretty_print_disabled(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path(
                    "tests/fixtures/mkdocs_pretty_print_disabled.yml"
                ),
                output_path=tmpdirname,
            )
            if cli_result.exception is not None:
                e = cli_result.exception
                logger.debug(format_exception(type(e), e, e.__traceback__))

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

            # created items
            with Path(Path(tmpdirname) / "feed_rss_created.xml").open("r") as f:
                self.assertEqual(len(f.readlines()), 1)

            # updated items
            with Path(Path(tmpdirname) / "feed_rss_updated.xml").open("r") as f:
                self.assertEqual(len(f.readlines()), 1)

    def test_rss_feed_validation(self):
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
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_created.xml")
            self.assertEqual(feed_parsed.bozo, 0)

            # updated items
            feed_parsed = feedparser.parse(Path(tmpdirname) / "feed_rss_updated.xml")
            self.assertEqual(feed_parsed.bozo, 0)

            # some feed characteristics
            self.assertEqual(feed_parsed.version, "rss20")

    def test_config_no_site_url(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path(
                    "tests/fixtures/mkdocs_minimal_no_site_url.yml"
                ),
                output_path=tmpdirname,
                strict=True,
            )

            # cli should returns an error code (1)
            self.assertEqual(cli_result.exit_code, 1)
            self.assertIsNotNone(cli_result.exception)

    def test_bad_config(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_bad_config.yml"),
                output_path=tmpdirname,
                strict=True,
            )

            # cli should returns an error code (1)
            self.assertEqual(cli_result.exit_code, 1)
            self.assertIsNotNone(cli_result.exception)

    def test_bad_date_format(self):
        # add a new page without tracking it
        md_str = """---\ndate: 13 April 2022\n---\n\n# This page is dynamically created for test purposes\n\nHi!\n
        """
        temp_page = Path("tests/fixtures/docs/temp_page_not_in_git_log.md")
        if temp_page.exists():
            temp_page.unlink()
        temp_page.write_text(md_str)

        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("mkdocs.yml"),
                output_path=tmpdirname,
                strict=True,
            )

            # cli should returns an error code (1)
            self.assertEqual(cli_result.exit_code, 1)
            self.assertIsNotNone(cli_result.exception)

        # rm page
        temp_page.unlink()

    def test_not_in_git_log(self):
        # add a new page without tracking it
        md_str = """# This page is dynamically created for test purposes\n\nHi!\n
        """
        temp_page = Path("tests/fixtures/docs/temp_page_not_in_git_log.md")
        if temp_page.exists():
            temp_page.unlink()
        temp_page.write_text(md_str)

        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_complete.yml"),
                output_path=tmpdirname,
                strict=True,
            )

            self.assertEqual(cli_result.exit_code, 0)
            self.assertIsNone(cli_result.exception)

        # rm page
        temp_page.unlink()

    def test_not_git_repo(self):
        # temporarily rename the git folder to fake a non-git repo
        git_dir = Path(".git")
        git_dir_tmp = git_dir.with_name("_git")
        git_dir.replace(git_dir_tmp)

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

            self.assertEqual(cli_result.exit_code, 1)
            self.assertIsNotNone(cli_result.exception)

        # restore name
        git_dir_tmp.replace(git_dir)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
