#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from pathlib import Path

# package
from mkdocs_rss_plugin import __about__

# ############################################################################
# ########## Globals #############
# ################################

DEFAULT_CACHE_FOLDER: Path = Path(".cache/plugins/rss")
DEFAULT_TEMPLATE_FOLDER: Path = Path(__file__).parent / "templates"
DEFAULT_TEMPLATE_FILENAME: Path = DEFAULT_TEMPLATE_FOLDER / "rss.xml.jinja2"
MKDOCS_LOGGER_NAME: str = "[RSS-plugin]"
REMOTE_REQUEST_HEADERS: dict[str, str] = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": f"{__about__.__title__}/{__about__.__version__}",
}
