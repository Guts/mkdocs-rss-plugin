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
from importlib import metadata

_pkg_metadata = metadata.metadata("mkdocs-rss-plugin") or {}

try:
    from ._version import version as __version__
except ImportError:
    __version__ = _pkg_metadata.get("Version", "0.0.0-dev0")


# ############################################################################
# ########## Globals #############
# ################################


__author__: str = _pkg_metadata.get("Author-email", "Julien Moura (In Geo Veritas)")
__copyright__ = f"2020 - {date.today().year}, {__author__}"
__email__ = "dev@ingeoveritas.com"
__license__: str = _pkg_metadata.get("License-Expression", "MIT")
__summary__ = (
    "MkDocs plugin which generates a static RSS feed using git log and page.meta."
)
__title__ = "MkDocs RSS plugin"
__title_clean__ = "".join(e for e in __title__ if e.isalnum())
__uri__ = "https://github.com/Guts/mkdocs-rss-plugin/"

__version_clean__: str = __version__.split(".dev")[0].split("+")[0]
__version_info__ = tuple(
    [
        int(num) if num.isdigit() else num
        for num in __version__.replace("-", ".", 1).split(".")
    ]
)


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
