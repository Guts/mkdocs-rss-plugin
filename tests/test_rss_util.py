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

# 3rd party
from validator_collection import checkers

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
        cls.plg_utils = Util()

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
    def test_build_url(self):
        """Test URL builder."""
        # without URL parameters
        item_url = self.plg_utils.build_url(
            base_url="https://guts.github.io/mkdocs-rss-plugin/", path="changelog"
        )
        self.assertTrue(checkers.is_url(item_url))

        # with URL parameters
        item_url = self.plg_utils.build_url(
            base_url="https://guts.github.io/mkdocs-rss-plugin/",
            path="changelog",
            args_dict={"utm_source": "test_rss"},
        )
        print(item_url)
        self.assertTrue(checkers.is_url(item_url))

    def test_local_image_ok(self):
        """Test local image length calculation."""
        img_length = self.plg_utils.get_local_image_length(
            page_path="docs/index.md", path_to_append="assets/rss_icon.svg"
        )
        self.assertIsInstance(img_length, int)

    def test_local_image_none(self):
        """Test local image length calculation on non-existing image."""
        img_length = self.plg_utils.get_local_image_length(
            page_path="docs/index.md", path_to_append="inexisting_image.svg"
        )
        self.assertIsNone(img_length)

    def test_remote_image_ok(self):
        """Test remote image length calculation."""
        img_length = self.plg_utils.get_remote_image_length(image_url=self.feed_image)
        self.assertIsInstance(img_length, int)

    def test_remote_image_none(self):
        """Test remote image length calculation on unreachable image."""
        img_length = self.plg_utils.get_remote_image_length(
            image_url="https://guts.github.io/mkdocs-rss-plugin/inexisting.svg"
        )
        self.assertIsNone(img_length)

    def test_get_value_from_dot_key(self):
        param_list = [
            {
                "meta": {"date": "2021-09-01"},
                "value_location": "date",
                "value": "2021-09-01",
            },
            {
                "meta": {"date": {"created": "2021-09-01"}},
                "value_location": "date.created",
                "value": "2021-09-01",
            },
            {
                "meta": {"date": "2021-09-01"},
                "value_location": "date.created",
                "value": None,
            },
            {
                "meta": {True: "bool_as_key"},
                "value_location": True,
                "value": "bool_as_key",
            },
            {
                "meta": {"date": "2021-09-01"},
                "value_location": True,
                "value": None,
            },
        ]
        for param in param_list:
            with self.subTest(param=param):
                result = self.plg_utils.get_value_from_dot_key(
                    param["meta"], param["value_location"]
                )
                self.assertEqual(result, param["value"])


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
