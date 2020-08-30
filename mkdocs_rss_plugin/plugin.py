#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
import re
from copy import deepcopy
from email.utils import formatdate
from pathlib import Path

# 3rd party
from jinja2 import Environment, FileSystemLoader, select_autoescape
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
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
DEFAULT_TEMPLATE_RSS = DEFAULT_TEMPLATE_FOLDER / "rss.xml.jinja2"
DEFAULT_TEMPLATE_TAG = DEFAULT_TEMPLATE_FOLDER / "tag_latest_created.html.jinja2"
OUTPUT_FEED_CREATED = "feed_rss_created.xml"
OUTPUT_FEED_UPDATED = "feed_rss_updated.xml"


# ############################################################################
# ########## Classes ###############
# ##################################
class GitRssPlugin(BasePlugin):
    config_scheme = (
        ("abstract_chars_count", config_options.Type(int, default=150)),
        ("category", config_options.Type(str, default=None)),
        ("feed_ttl", config_options.Type(int, default=1440)),
        ("image", config_options.Type(str, default=None)),
        ("length", config_options.Type(int, default=20)),
    )

    def __init__(self):
        # tooling
        self.util = Util()
        # pages storage
        self.pages_to_filter = []
        # prepare output feeds
        self.feed_created = dict
        self.feed_updated = dict
        # tag dict
        self.tag_created = list
        self.tag_updated = list

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
        # check template dirs
        if not Path(DEFAULT_TEMPLATE_RSS).is_file():
            raise FileExistsError(DEFAULT_TEMPLATE_RSS)
        self.tpl_file = Path(DEFAULT_TEMPLATE_RSS)
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
            "html_url": config.get("site_url", __uri__),
            "pubDate": formatdate(get_build_timestamp()),
            "repo_url": config.get("repo_url", config.get("site_url", None)),
            "title": config.get("site_name", None),
            "ttl": self.config.get("feed_ttl", None),
        }

        # feed image
        if self.config.get("image"):
            base_feed["logo_url"] = self.config.get("image")

        # create 2 final dicts
        self.feed_created = deepcopy(base_feed)
        self.feed_updated = deepcopy(base_feed)

        # final feed url
        if config.get("site_url"):
            # handle trailing slash
            if not config.get("site_url").endswith("/"):
                site_url_base = config.get("site_url") + "/"
            else:
                site_url_base = config.get("site_url")

            # concatenate both URLs
            self.feed_created["rss_url"] = site_url_base + OUTPUT_FEED_CREATED
            self.feed_updated["rss_url"] = site_url_base + OUTPUT_FEED_UPDATED
        else:
            logging.warning(
                "[rss-plugin] The variable `site_url` is not set in the MkDocs "
                "configuration file whereas a URL is mandatory to publish. "
                "See: https://validator.w3.org/feed/docs/rss2.html#requiredChannelElements"
            )

        # ending event
        return config

    def on_page_content(
        self, html: str, page: Page, config, files: Files, **kwargs
    ) -> str:
        """
        Replace jinja tag {{ git_latest_created }} in HTML.

        The page_content event is called after the Markdown text is
        rendered to HTML (but before being passed to a template) and
        can be used to alter the HTML body of the page.

        https://www.mkdocs.org/user-guide/plugins/#on_page_content

        We replace the authors list in this event in order to be able
        to replace it with arbitrary HTML content (which might otherwise
        end up in styled HTML in a code block).

        Args:
            html: the processed HTML of the page
            page: mkdocs.nav.Page instance
            config: global configuration object
            site_navigation: global navigation object

        Returns:
            str: HTML text of page as string
        """
        list_pattern = re.compile(
            r"\{\{\s*git_latest_created\s*\}\}", flags=re.IGNORECASE
        )
        dico_files = {}

        if list_pattern.search(html):
            for i in files:
                if i.is_documentation_page():
                    self.tag_created.append(PageInformation(
                        abs_path=Path(i.abs_src_path),
                        category=self.util.get_category(in_page=page),
                        created=page_dates[0],
                        updated=page_dates[1],
                        title=page.title,
                        description=self.util.get_description_or_abstract(
                        in_page=page, chars_count=self.config.get("abstract_chars_count")),
                        url_full=page.canonical_url,
                    ))
        
                    dico_files[i.name] = (i.src_path, i.url, self.util.get_file_dates(i.abs_src_path))
            print(dir(i), i.src_path)
            print(dico_files)

            # # created items
            # self.tag_created = self.util.filter_pages(
            #     pages=self.pages_to_filter,
            #     attribute="created",
            #     length=self.config.get("length", 20),
            # )

            # jinja2 environment
            # env = Environment(
            #     loader=FileSystemLoader(self.tpl_folder),
            #     autoescape=select_autoescape(["html", "xml"]),
            # )

            # template = env.get_template(DEFAULT_TEMPLATE_TAG.name)
            # html = list_pattern.sub(template.render(entries=self.tag_created), html)

            # return html

    def on_page_markdown(
        self, markdown: str, page: Page, config: config_options.Config, files
    ) -> str:
        """The page_markdown event is called after the page's markdown is loaded
        from file and can be used to alter the Markdown source text.
        The meta-data has been stripped off and is available as page.meta
        at this point.

        https://www.mkdocs.org/user-guide/plugins/#on_page_markdown

        Args:
            markdown (str): Markdown source text of page as string
            page: mkdocs.nav.Page instance
            config: global configuration object
            site_navigation: global navigation object

        Returns:
            str: Markdown source text of page as string
        """
        # retrieve dates from git log
        page_dates = self.util.get_file_dates(path=page.file.abs_src_path)

        # append to list to be filtered later
        self.pages_to_filter.append(
            PageInformation(
                abs_path=Path(page.file.abs_src_path),
                category=self.util.get_category(in_page=page),
                created=page_dates[0],
                updated=page_dates[1],
                title=page.title,
                description=self.util.get_description_or_abstract(
                    in_page=page, chars_count=self.config.get("abstract_chars_count")
                ),
                url_full=page.canonical_url,
            )
        )

    def on_post_build(self, config: config_options.Config) -> dict:
        """The post_build event does not alter any variables. \
        Use this event to call post-build scripts. \
        See: <https://www.mkdocs.org/user-guide/plugins/#on_post_build>

        Args:
            config (dict): global configuration object

        Returns:
            dict: global configuration object
        """
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
        self.feed_created.get("entries").extend(
            self.util.filter_pages(
                pages=self.pages_to_filter,
                attribute="updated",
                length=self.config.get("length", 20),
            )
        )
        # load Jinja environment
        env = Environment(
            loader=FileSystemLoader(self.tpl_folder),
            autoescape=select_autoescape(["html", "xml"]),
        )

        template = env.get_template(self.tpl_file.name)

        # write feeds to files
        with out_feed_created.open(mode="w", encoding="UTF8") as fifeed_created:
            fifeed_created.write(template.render(feed=self.feed_created))

        with out_feed_updated.open(mode="w", encoding="UTF8") as fifeed_updated:
            fifeed_updated.write(template.render(feed=self.feed_updated))
