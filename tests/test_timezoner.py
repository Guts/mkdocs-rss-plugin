#! python3  # noqa E265

"""Usage from the repo root folder:

.. code-block:: python

    # for whole test
    python -m unittest tests.test_timezoner

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
from datetime import datetime

# plugin target
from mkdocs_rss_plugin.util import set_datetime_zoneinfo


# #############################################################################
# ########## Classes ###############
# ##################################
class TestTimezoner(unittest.TestCase):
    """Test timezone handler."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.fmt_date = "%Y-%m-%d"
        cls.fmt_datetime_aware = "%Y-%m-%d %H:%M:%S%z"
        cls.fmt_datetime_naive = "%Y-%m-%d %H:%M"

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
    def test_tz_dates(self):
        """Test timezone set for dates."""

        test_date_summer = datetime.strptime("2022-07-14", self.fmt_date)
        test_date_winter = datetime.strptime("2022-12-25", self.fmt_date)

        self.assertEqual(
            set_datetime_zoneinfo(test_date_summer),
            datetime.strptime("2022-07-14 00:00:00+00:00", self.fmt_datetime_aware),
        )
        self.assertEqual(
            set_datetime_zoneinfo(test_date_winter),
            datetime.strptime("2022-12-25 00:00:00+00:00", self.fmt_datetime_aware),
        )

    def test_tz_datetimes_naive(self):
        """Test timezone set for naive datetimes."""

        test_datetime_summer_naive = datetime.strptime(
            "2022-07-14 12:00", self.fmt_datetime_naive
        )
        test_datetime_winter_naive = datetime.strptime(
            "2022-12-25 22:00", self.fmt_datetime_naive
        )

        # without timezone = UTC
        self.assertEqual(
            set_datetime_zoneinfo(test_datetime_summer_naive),
            datetime.strptime("2022-07-14 12:00:00+00:00", self.fmt_datetime_aware),
        )
        self.assertEqual(
            set_datetime_zoneinfo(test_datetime_winter_naive),
            datetime.strptime("2022-12-25 22:00:00+00:00", self.fmt_datetime_aware),
        )

        # with timezone
        self.assertEqual(
            set_datetime_zoneinfo(test_datetime_summer_naive, "Europe/Paris"),
            datetime.strptime("2022-07-14 12:00:00+02:00", self.fmt_datetime_aware),
        )
        self.assertEqual(
            set_datetime_zoneinfo(test_datetime_winter_naive, "Europe/Paris"),
            datetime.strptime("2022-12-25 22:00:00+01:00", self.fmt_datetime_aware),
        )

    def test_tz_datetimes_aware(self):
        """Test timezone set for aware datetimes."""

        test_datetime_summer_aware = datetime.strptime(
            "2022-07-14 12:00:00+0400", self.fmt_datetime_aware
        )
        test_datetime_winter_aware = datetime.strptime(
            "2022-12-25 22:00:00-0800", self.fmt_datetime_aware
        )

        # without timezone = UTC
        self.assertEqual(
            set_datetime_zoneinfo(test_datetime_summer_aware),
            datetime.strptime("2022-07-14 12:00:00+04:00", self.fmt_datetime_aware),
        )
        self.assertEqual(
            set_datetime_zoneinfo(test_datetime_winter_aware),
            datetime.strptime("2022-12-25 22:00:00-08:00", self.fmt_datetime_aware),
        )

        # with timezone
        self.assertEqual(
            set_datetime_zoneinfo(test_datetime_summer_aware, "Europe/Paris"),
            datetime.strptime("2022-07-14 12:00:00+04:00", self.fmt_datetime_aware),
        )
        self.assertEqual(
            set_datetime_zoneinfo(test_datetime_winter_aware, "Europe/Paris"),
            datetime.strptime("2022-12-25 22:00:00-08:00", self.fmt_datetime_aware),
        )


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
