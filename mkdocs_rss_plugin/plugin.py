#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
from copy import deepcopy
from email.utils import formatdate
from pathlib import Path
from re import compile

# 3rd party
from jinja2 import Environment, FileSystemLoader, select_autoescape
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.utils import get_build_timestamp

# package modules
from .__about__ import __title__, __uri__, __version__
from .customtypes import PageInformation
from .util import Util

# ############################################################################
# ########## Globals #############
# ################################

DEFAULT_TEMPLATE_FOLDER = Path(__file__).parent / "templates"
DEFAULT_TEMPLATE_FILENAME = DEFAULT_TEMPLATE_FOLDER / "rss.xml.jinja2"
OUTPUT_FEED_CREATED = "feed_rss_created.xml"
OUTPUT_FEED_UPDATED = "feed_rss_updated.xml"

logger = logging.getLogger("mkdocs.mkdocs_rss_plugin")


# ############################################################################
# ########## Classes ###############
# ##################################


class GitRssPlugin(BasePlugin):
    """Main class for MkDocs plugin."""

    config_scheme = (
        ("abstract_chars_count", config_options.Type(int, default=160)),
        ("category", config_options.Type(str, default=None)),
        ("comments_path", config_options.Type(str, default=None)),
        ("date_from_meta", config_options.Type(dict, default=None)),
        ("feed_ttl", config_options.Type(int, default=1440)),
        ("image", config_options.Type(str, default=None)),
        ("length", config_options.Type(int, default=20)),
        ("match_path", config_options.Type(str, default=".*")),
        ("pretty_print", config_options.Type(bool, default=False)),
        ("url_parameters", config_options.Type(dict, default=None)),
    )

    def __init__(self):
        """Instanciation."""
        # tooling
        self.util = Util()
        # dates source
        self.src_date_created = self.src_date_updated = "git"
        self.meta_datetime_format = None
        # pages storage
        self.pages_to_filter = []
        # prepare output feeds
        self.feed_created = dict
        self.feed_updated = dict

    def on_config(self, config: config_options.Config) -> dict:
        """The config event is the first event called on build and
        is run immediately after the user configuration is loaded and validated.
        Any alterations to the config should be made here.
        https://www.mkdocs.org/user-guide/plugins/#on_config

        :param config: global configuration object
        :type config: config_options.Config

        :raises FileExistsError: if the template for the RSS feed is not found

        :return: plugin configuration object
        :rtype: dict
        """
        # check template dirs
        if not Path(DEFAULT_TEMPLATE_FILENAME).is_file():
            raise FileExistsError(DEFAULT_TEMPLATE_FILENAME)
        self.tpl_file = Path(DEFAULT_TEMPLATE_FILENAME)
        self.tpl_folder = DEFAULT_TEMPLATE_FOLDER

        # start a feed dictionary using global config vars
        base_feed = {
            "author": config.get("site_author", None),
            "buildDate": formatdate(get_build_timestamp()),
            "category": self.config.get("category", None),
            "copyright": config.get("copyright", None),
            "description": config.get("site_description", None),
            "entries": [],
            "generator": "{} - v{}".format(__title__, __version__),
            "html_url": self.util.get_site_url(config),
            "language": self.util.guess_locale(config),
            "pubDate": formatdate(get_build_timestamp()),
            "repo_url": config.get("repo_url", config.get("site_url", None)),
            "title": config.get("site_name", None),
            "ttl": self.config.get("feed_ttl", None),
        }

        # feed image
        if self.config.get("image"):
            base_feed["logo_url"] = self.config.get("image")

        # pattern to match pages included in output
        self.match_path_pattern = compile(self.config.get("match_path"))

        # date handling
        if self.config.get("date_from_meta") is not None:
            self.src_date_created = self.config.get("date_from_meta").get(
                "as_creation", False
            )
            self.src_date_updated = self.config.get("date_from_meta").get(
                "as_update", False
            )
            self.meta_datetime_format = self.config.get("date_from_meta").get(
                "datetime_format", "%Y-%m-%d %H:%M"
            )
            logger.debug(
                "[rss-plugin] Dates will be retrieved from page meta (yaml "
                "frontmatter). The git log will be used as fallback."
            )
        else:
            logger.debug("[rss-plugin] Dates will be retrieved from git log.")

        # create 2 final dicts
        self.feed_created = deepcopy(base_feed)
        self.feed_updated = deepcopy(base_feed)

        # final feed url
        if base_feed.get("html_url"):
            # concatenate both URLs
            self.feed_created["rss_url"] = (
                base_feed.get("html_url") + OUTPUT_FEED_CREATED
            )
            self.feed_updated["rss_url"] = (
                base_feed.get("html_url") + OUTPUT_FEED_UPDATED
            )
        else:
            logging.warning(
                "[rss-plugin] The variable `site_url` is not set in the MkDocs "
                "configuration file whereas a URL is mandatory to publish. "
                "See: https://validator.w3.org/feed/docs/rss2.html#requiredChannelElements"
            )
            self.feed_created["rss_url"] = self.feed_updated["rss_url"] = None

        # ending event
        return config

    def on_page_markdown(
        self, markdown: str, page: Page, config: config_options.Config, files
    ) -> str:
        """The page_markdown event is called after the page's markdown is loaded
        from file and can be used to alter the Markdown source text.
        The meta- data has been stripped off and is available as page.meta
        at this point.

        https://www.mkdocs.org/user-guide/plugins/#on_page_markdown

        :param markdown: Markdown source text of page as strin
        :type markdown: str
        :param page: mkdocs.nav.Page instance
        :type page: Page
        :param config: global configuration object
        :type config: config_options.Config
        :param files: global navigation object
        :type files: [type]

        :return: Markdown source text of page as strin
        :rtype: str
        """
        # skip pages that don't match the config var match_path
        if not self.match_path_pattern.match(page.file.src_path):
            return

        # retrieve dates from git log
        page_dates = self.util.get_file_dates(
            in_page=page,
            source_date_creation=self.src_date_created,
            source_date_update=self.src_date_updated,
            meta_datetime_format=self.meta_datetime_format,
        )

        # handle custom URL parameters
        if self.config.get("url_parameters"):
            page_url_full = self.util.build_url(
                base_url=page.canonical_url,
                path="",
                args_dict=self.config.get("url_parameters"),
            )
        else:
            page_url_full = page.canonical_url

        # handle URL comment path
        if self.config.get("comments_path"):
            page_url_comments = self.util.build_url(
                base_url=page.canonical_url,
                path=self.config.get("comments_path"),
            )
        else:
            page_url_comments = None

        # append to list to be filtered later
        self.pages_to_filter.append(
            PageInformation(
                abs_path=Path(page.file.abs_src_path),
                authors=self.util.get_authors_from_meta(in_page=page),
                created=page_dates[0],
                description=self.util.get_description_or_abstract(
                    in_page=page, chars_count=self.config.get("abstract_chars_count")
                ),
                guid=page.canonical_url,
                image=self.util.get_image(
                    in_page=page, base_url=config.get("site_url", __uri__)
                ),
                title=page.title,
                updated=page_dates[1],
                url_comments=page_url_comments,
                url_full=page_url_full,
            )
        )

    def on_post_build(self, config: config_options.Config) -> dict:
        """The post_build event does not alter any variables. \
        Use this event to call post-build scripts. \
        See: <https://www.mkdocs.org/user-guide/plugins/#on_post_build>

        :param config: global configuration object
        :type config: config_options.Config
        :return: global configuration object
        :rtype: dict
        """
        # pretty print or not
        pretty_print = self.config.get("pretty_print", False)

        # output filepaths
        out_feed_created = Path(config.get("site_dir")) / OUTPUT_FEED_CREATED
        out_feed_updated = Path(config.get("site_dir")) / OUTPUT_FEED_UPDATED

        # created items
        self.feed_created.get("entries").extend(
            self.util.filter_pages(
                pages=self.pages_to_filter,
                attribute="created",
                length=self.config.get("length", 20),
            )
        )

        # updated items
        self.feed_updated.get("entries").extend(
            self.util.filter_pages(
                pages=self.pages_to_filter,
                attribute="updated",
                length=self.config.get("length", 20),
            )
        )

        # write feeds according to the pretty print option
        if pretty_print:
            # load Jinja environment and template
            env = Environment(
                autoescape=select_autoescape(["html", "xml"]),
                loader=FileSystemLoader(self.tpl_folder),
            )

            template = env.get_template(self.tpl_file.name)

            # write feeds to files
            with out_feed_created.open(mode="w", encoding="UTF8") as fifeed_created:
                fifeed_created.write(template.render(feed=self.feed_created))

            with out_feed_updated.open(mode="w", encoding="UTF8") as fifeed_updated:
                fifeed_updated.write(template.render(feed=self.feed_updated))

        else:
            # load Jinja environment and template
            env = Environment(
                autoescape=select_autoescape(["html", "xml"]),
                loader=FileSystemLoader(self.tpl_folder),
                lstrip_blocks=True,
                trim_blocks=True,
            )
            template = env.get_template(self.tpl_file.name)

            # write feeds to files stripping out spaces and new lines
            with out_feed_created.open(mode="w", encoding="UTF8") as fifeed_created:
                prev_char = ""
                for char in template.render(feed=self.feed_created):
                    if char == "\n":
                        continue
                    if char == " " and prev_char == " ":
                        prev_char = char
                        continue
                    prev_char = char
                    fifeed_created.write(char)

            with out_feed_updated.open(mode="w", encoding="UTF8") as fifeed_updated:
                for char in template.render(feed=self.feed_updated):
                    if char == "\n":
                        prev_char = char
                        continue
                    if char == " " and prev_char == " ":
                        prev_char = char
                        continue
                    prev_char = char
                    fifeed_updated.write(char)
