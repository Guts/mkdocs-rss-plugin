#! python3  # noqa E265

"""Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_config

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
from pathlib import Path

# plugin target
from mkdocs_rss_plugin.plugin import GitRssPlugin


# #############################################################################
# ########## Classes ###############
# ##################################
class TestConfig(unittest.TestCase):
    """Test plugin configuration."""

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
    def test_plugin_config_defaults(self):
        # default reference
        expected = {
            "abstract_chars_count": 160,
            "category": None,
            "date_from_meta": None,
            "feed_ttl": 1440,
            "image": None,
            "length": 20,
            "pretty_print": False,
            "match_path": ".*",
        }

        # load
        plugin = GitRssPlugin()
        errors, warnings = plugin.load_config({})
        self.assertEqual(plugin.config, expected)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_plugin_config_image(self):
        # reference
        expected = {
            "abstract_chars_count": 160,
            "category": None,
            "date_from_meta": None,
            "feed_ttl": 1440,
            "image": self.feed_image,
            "length": 20,
            "pretty_print": False,
            "match_path": ".*",
        }

        # custom config
        custom_cfg = {"image": self.feed_image}

        # load
        plugin = GitRssPlugin()
        errors, warnings = plugin.load_config(custom_cfg)
        self.assertEqual(plugin.config, expected)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
