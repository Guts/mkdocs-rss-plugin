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

# 3rd party
from mkdocs.config.base import Config

# plugin target
from mkdocs_rss_plugin.config import RssPluginConfig
from mkdocs_rss_plugin.plugin import GitRssPlugin

# test suite
from tests.base import BaseTest


# #############################################################################
# ########## Classes ###############
# ##################################
class TestConfig(BaseTest):
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
            "abstract_delimiter": "<!-- more -->",
            "categories": None,
            "comments_path": None,
            "date_from_meta": None,
            "enabled": True,
            "feed_ttl": 1440,
            "image": None,
            "json_feed_enabled": True,
            "length": 20,
            "match_path": ".*",
            "pretty_print": False,
            "rss_feed_enabled": True,
            "url_parameters": None,
            "use_git": True,
            "use_material_social_cards": True,
        }

        # load
        plugin = GitRssPlugin()
        errors, warnings = plugin.load_config({})
        self.assertIsInstance(plugin.config, RssPluginConfig)
        self.assertIsInstance(plugin.config, Config)
        self.assertEqual(plugin.config, expected)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_plugin_config_image(self):
        # reference
        expected = {
            "abstract_chars_count": 160,
            "abstract_delimiter": "<!-- more -->",
            "categories": None,
            "comments_path": None,
            "date_from_meta": None,
            "enabled": True,
            "feed_ttl": 1440,
            "image": self.feed_image,
            "json_feed_enabled": True,
            "length": 20,
            "match_path": ".*",
            "pretty_print": False,
            "rss_feed_enabled": True,
            "url_parameters": None,
            "use_git": True,
            "use_material_social_cards": True,
        }

        # custom config
        custom_cfg = {"image": self.feed_image}

        # load
        plugin = GitRssPlugin()
        errors, warnings = plugin.load_config(custom_cfg)
        self.assertIsInstance(plugin.config, RssPluginConfig)
        self.assertIsInstance(plugin.config, Config)
        self.assertEqual(plugin.config, expected)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_plugin_config_through_mkdocs(self):
        for config_filepath in self.config_files:
            plg_cfg = self.get_plugin_config_from_mkdocs(config_filepath, "rss")
            print(config_filepath)
            self.assertIsInstance(plg_cfg, Config)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
