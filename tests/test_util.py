#! python3  # noqa E265

"""Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_base

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import unittest

# mkdocs
from mkdocs.structure.pages import Page

# plugin target
from mkdocs_rss_plugin.util import Util


# #############################################################################
# ########## Classes ###############
# ##################################
class TestUtil(unittest.TestCase):
    """Test plugin utils."""

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
        pass

    # -- TESTS ---------------------------------------------------------
    def description(self):
        pass


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
