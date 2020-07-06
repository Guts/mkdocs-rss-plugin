#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from pathlib import Path

# 3rd party
from jinja2 import Environment, FileSystemLoader, select_autoescape
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

# package modules
from .__about__ import __title__, __version__
from .util import Util

# ############################################################################
# ########## Globals #############
# ################################

DEFAULT_TEMPLATE_FOLDER = Path(__file__).parent / "templates"
DEFAULT_TEMPLATE_FILENAME = DEFAULT_TEMPLATE_FOLDER / "rss.xml.jinja2"


# ############################################################################
# ########## Classes ###############
# ##################################
class GitRssPlugin(BasePlugin):
    config_scheme = (
        ("category", config_options.Type(str, default=None)),
        ("exclude_files", config_options.Type(list, default=[])),
        ("length", config_options.Type(int, default=20)),
        ("output_feed_filepath", config_options.Type(str, default="feed.xml")),
        ("template", config_options.Type(str, default=str(DEFAULT_TEMPLATE_FILENAME)),),
    )

    def __init__(self):
        self.util = Util()

    def on_config(self, config: config_options.Config) -> dict:
        """

        The config event is the first event called on build and
        is run immediately after the user configuration is loaded and validated.
        Any alterations to the config should be made here.
        https://www.mkdocs.org/user-guide/plugins/#on_config

        Args:
            config (dict): global configuration object

        Returns:
            dict: global configuration object
        """
        # start a feed dictionary using global config vars
        self.feed = {
            "author": config.get("author", None),
            "copyright": config.get("copyright", None),
            "description": config.get("site_description", None),
            "generator": "{} - v{}".format(__title__, __version__),
            "link": config.get("site_url", None),
            "repo_url": config.get("repo_url", config.get("site_url", None)),
            "title": config.get("site_name", None),
        }

        # check template dirs
        if not Path(self.config.get("template")).is_file():
            raise FileExistsError(self.config.get("template"))
        tpl_file = Path(self.config.get("template"))
        tpl_folder = Path(self.config.get("template")).parent

        # load Jinja environment
        env = Environment(
            loader=FileSystemLoader(tpl_folder), autoescape=select_autoescape(["xml"]),
        )

        template = env.get_template(tpl_file.name)

        with open(
            self.config.get("output_feed_filepath"), mode="w", encoding="UTF8"
        ) as fh:
            fh.write(template.render(feed=self.feed))

        return config
