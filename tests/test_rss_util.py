#! python3  # noqa E265

"""Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_rss_util

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
from pathlib import Path

# plugin target
from mkdocs_rss_plugin.util import Util


# #############################################################################
# ########## Classes ###############
# ##################################
class TestRssUtil(unittest.TestCase):
    """Test plugin tools."""

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
    def test_local_image_ok(self):
        """Test local image length calculation."""
        plg_utils = Util()
        img_length = plg_utils.get_local_image_length(
            page_path="docs/usage/index.md", path_to_append="rss_icon.svg"
        )
        self.assertIsInstance(img_length, int)

    def test_local_image_none(self):
        """Test local image length calculation on non-existing image."""
        plg_utils = Util()
        img_length = plg_utils.get_local_image_length(
            page_path="docs/usage/index.md", path_to_append="inexisting_image.svg"
        )
        self.assertIsNone(img_length)

    def test_remote_image_ok(self):
        """Test remote image length calculation."""
        plg_utils = Util()
        img_length = plg_utils.get_remote_image_length(image_url=self.feed_image)
        self.assertIsInstance(img_length, int)

    def test_remote_image_none(self):
        """Test remote image length calculation on unreachable image."""
        plg_utils = Util()
        img_length = plg_utils.get_remote_image_length(
            image_url="https://guts.github.io/mkdocs-rss-plugin/inexisting.svg"
        )
        self.assertIsNone(img_length)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
