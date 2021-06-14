#! python3  # noqa: E265

"""
    Metadata about the package to easily retrieve informations about it.

    See: https://packaging.python.org/guides/single-sourcing-package-version/
"""

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from datetime import date

# ############################################################################
# ########## Globals #############
# ################################
__all__ = [
    "__author__",
    "__copyright__",
    "__email__",
    "__license__",
    "__summary__",
    "__title__",
    "__title_clean__",
    "__uri__",
    "__version__",
    "__version_info__",
]

__author__ = "Julien Moura"
__copyright__ = "2020 - {0}, {1}".format(date.today().year, __author__)
__email__ = "dev@ingeoveritas.com"
__license__ = "GNU General Public License v3.0"
__summary__ = (
    "MkDocs plugin which generates a static RSS feed using git log and page.meta."
)
__title__ = "MkDocs RSS plugin"
__title_clean__ = "".join(e for e in __title__ if e.isalnum())
__uri__ = "https://github.com/Guts/mkdocs-rss-plugin/"

__version__ = "0.17.0"
__version_info__ = tuple(
    [
        int(num) if num.isdigit() else num
        for num in __version__.replace("-", ".", 1).split(".")
    ]
)
