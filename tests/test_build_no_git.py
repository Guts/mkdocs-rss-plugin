#! python3  # noqa E265

"""Usage from the repo root folder:

.. code-block:: python

    # for whole test
    python -m unittest tests.test_build_no_git
    # for specific test
    python -m unittest tests.test_build_no_git.TestBuildRssNoGit.test_not_git_repo_without_option
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

# test suite
from tests.base import BaseTest

logger = getLogger(__name__)
logger.setLevel(DEBUG)

# #############################################################################
# ########## Classes ###############
# ##################################


class TestBuildRssNoGit(BaseTest):
    """Test MkDocs build with RSS plugin but without git."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        pass

    def setUp(self):
        """Executed before each test."""
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # # In case of some tests failure, ensure that everything is cleaned up
        # temp_page = Path("tests/fixtures/docs/temp_page_not_in_git_log.md")
        # # if temp_page.exists():
        # #     temp_page.unlink()

        git_dir = Path("_git")
        if git_dir.exists():
            git_dir.replace(git_dir.with_name(".git"))

    # -- TESTS ---------------------------------------------------------
    def test_not_git_repo(self):
        # temporarily rename the git folder to fake a non-git repo
        git_dir = Path(".git")
        git_dir_tmp = git_dir.with_name("_git")
        git_dir.replace(git_dir_tmp)

        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_complete_no_git.yml"),
                output_path=tmpdirname,
                strict=True,
            )

            self.assertIsNone(cli_result.exception)
            self.assertEqual(cli_result.exit_code, 0, cli_result)

        # restore name
        git_dir_tmp.replace(git_dir)

    def test_not_git_repo_without_option(self):
        # temporarily rename the git folder to fake a non-git repo
        git_dir = Path(".git")
        git_dir_tmp = git_dir.with_name("_git")
        git_dir.replace(git_dir_tmp)

        with tempfile.TemporaryDirectory() as tmpdirname:
            cli_result = self.build_docs_setup(
                testproject_path="docs",
                mkdocs_yml_filepath=Path("tests/fixtures/mkdocs_complete.yml"),
                output_path=tmpdirname,
                strict=True,
            )

            self.assertIsNotNone(cli_result.exception)
            self.assertEqual(
                cli_result.exit_code,
                1,
                format_exception(
                    type(cli_result.exception),
                    cli_result.exception,
                    cli_result.exception.__traceback__,
                ),
            )

        # restore name
        git_dir_tmp.replace(git_dir)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
