#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import json
from copy import deepcopy
from datetime import datetime
from email.utils import formatdate
from pathlib import Path
from re import compile as re_compile
from typing import List, Literal, Optional

# 3rd party
from jinja2 import Environment, FileSystemLoader, select_autoescape
from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, event_priority, get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs.utils import get_build_timestamp

# package modules
from mkdocs_rss_plugin.__about__ import __title__, __uri__, __version__
from mkdocs_rss_plugin.config import RssPluginConfig
from mkdocs_rss_plugin.constants import (
    DEFAULT_TEMPLATE_FILENAME,
    DEFAULT_TEMPLATE_FOLDER,
    MKDOCS_LOGGER_NAME,
)
from mkdocs_rss_plugin.integrations.theme_material_social_plugin import (
    IntegrationMaterialSocialCards,
)
from mkdocs_rss_plugin.models import PageInformation
from mkdocs_rss_plugin.util import Util

# ############################################################################
# ########## Globals #############
# ################################


logger = get_plugin_logger(MKDOCS_LOGGER_NAME)


# ############################################################################
# ########## Classes ###############
# ##################################


class GitRssPlugin(BasePlugin[RssPluginConfig]):
    """Main class for MkDocs plugin."""

    # allow to set the plugin multiple times in the same mkdocs config
    supports_multiple_instances = True

    def __init__(self, *args, **kwargs):
        """Instantiation."""
        # pages storage
        super().__init__(*args, **kwargs)

        self.cmd_is_serve: bool = False

    def on_startup(
        self, *, command: Literal["build", "gh-deploy", "serve"], dirty: bool
    ) -> None:
        """The `startup` event runs once at the very beginning of an `mkdocs` invocation.
        Note that for initializing variables, the __init__ method is still preferred.
        For initializing per-build variables (and whenever in doubt), use the
        on_config event.

        See: https://www.mkdocs.org/user-guide/plugins/#on_startup

        Args:
            command: the command that MkDocs was invoked with, e.g. "serve" for `mkdocs serve`.
            dirty: whether `--dirty` flag was passed.
        """
        # flag used command to disable some actions if serve is used
        self.cmd_is_serve = command == "serve"

        self.pages_to_filter: List[PageInformation] = []
        # prepare output feeds
        self.feed_created: dict = {}
        self.feed_updated: dict = {}

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        """The config event is the first event called on build and
        is run immediately after the user configuration is loaded and validated.
        Any alterations to the config should be made here.

        See: https://www.mkdocs.org/user-guide/plugins/#on_config

        Args:
            config (config_options.Config): global configuration object

        Raises:
            FileExistsError: if the template for the RSS feed is not found
            PluginError: if the 'date_from_meta.default_time' format does not comply

        Returns:
            MkDocsConfig: global configuration object
        """
        # Skip if disabled
        if not self.config.enabled:
            return config

        # Fail if any export option is enabled
        if not any([self.config.json_feed_enabled, self.config.rss_feed_enabled]):
            logger.error(
                "At least one export option has to be enabled. Plugin is disabled."
            )
            self.config.enabled = False
            return config

        # cache dir
        self.cache_dir = Path(self.config.cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Caching HTTP requests to: {self.cache_dir.resolve()}")

        # integrations - check if theme is Material and if social cards are enabled
        self.integration_material_social_cards = IntegrationMaterialSocialCards(
            mkdocs_config=config,
            switch_force=self.config.use_material_social_cards,
        )

        # instantiate plugin tooling
        self.util = Util(
            cache_dir=self.cache_dir,
            use_git=self.config.use_git,
            integration_material_social_cards=self.integration_material_social_cards,
            mkdocs_command_is_on_serve=self.cmd_is_serve,
        )

        # check template dirs
        if not Path(DEFAULT_TEMPLATE_FILENAME).is_file():
            raise FileExistsError(DEFAULT_TEMPLATE_FILENAME)
        self.tpl_file = Path(DEFAULT_TEMPLATE_FILENAME)
        self.tpl_folder = DEFAULT_TEMPLATE_FOLDER

        # start a feed dictionary using global config vars
        base_feed = {
            "author": config.site_author or None,
            "buildDate": formatdate(get_build_timestamp()),
            "copyright": config.copyright,
            "description": (
                self.config.feed_description
                if self.config.feed_description
                else config.site_description
            ),
            "entries": [],
            "generator": f"{__title__} - v{__version__}",
            "html_url": self.util.get_site_url(mkdocs_config=config),
            "language": self.util.guess_locale(mkdocs_config=config),
            "pubDate": formatdate(get_build_timestamp()),
            "repo_url": config.repo_url,
            "title": (
                self.config.feed_title if self.config.feed_title else config.site_name
            ),
            "ttl": self.config.feed_ttl,
        }

        # feed image
        if self.config.image:
            base_feed["logo_url"] = self.config.image

        # pattern to match pages included in output
        self.match_path_pattern = re_compile(self.config.match_path)

        # date handling
        if (
            self.config.date_from_meta.as_creation == "git"
            and self.config.date_from_meta.as_update == "git"
        ):
            logger.debug("Dates will be retrieved from git log.")
        elif any(
            [
                isinstance(self.config.date_from_meta.as_creation, bool),
                isinstance(self.config.date_from_meta.as_update, bool),
            ]
        ):
            deprecation_msg = (
                "Since version 1.13, using a boolean for "
                "'date_from_meta.as_creation' and 'date_from_meta.as_update' is "
                "deprecated. Please update your "
                "`rss` plugin settings in your Mkdocs configuration "
                f"({config.config_file_path}) by using a str or removing the value if "
                "you were using `False`., "
            )
            logger.warning(DeprecationWarning(deprecation_msg))
            self.config.date_from_meta.as_creation = (
                self.config.date_from_meta.as_update
            ) = "git"

        # check if default time complies with expected format
        try:
            self.config.date_from_meta.default_time = datetime.strptime(
                self.config.date_from_meta.default_time, "%H:%M"
            )
        except (TypeError, ValueError) as err:
            logger.warning(
                "Config error: `date_from_meta.default_time` value "
                f"'{self.config.date_from_meta.default_time}' format doesn't match the "
                f"expected format %H:%M. Fallback to the default value. Trace: {err}"
            )
            self.config.date_from_meta.default_time = datetime.strptime(
                "00:00", "%H:%M"
            )

        if self.config.use_git:
            logger.debug(
                "Dates will be retrieved FIRSTLY from page meta (yaml "
                "frontmatter). The git log will be used as fallback."
            )
        else:
            logger.debug(
                "Dates will be retrieved ONLY from page meta (yaml "
                "frontmatter). The build date will be used as fallback, without any "
                "call to Git."
            )

        # create 2 final dicts
        self.feed_created = deepcopy(base_feed)
        self.feed_updated = deepcopy(base_feed)

        # final feed url
        if base_feed.get("html_url"):
            # concatenate both URLs
            self.feed_created["rss_url"] = (
                base_feed.get("html_url") + self.config.feeds_filenames.rss_created
            )
            self.feed_updated["rss_url"] = (
                base_feed.get("html_url") + self.config.feeds_filenames.rss_updated
            )
            self.feed_created["json_url"] = (
                base_feed.get("html_url") + self.config.feeds_filenames.json_created
            )
            self.feed_updated["json_url"] = (
                base_feed.get("html_url") + self.config.feeds_filenames.json_updated
            )
        else:
            logger.error(
                "The variable `site_url` is not set in the MkDocs "
                "configuration file whereas a URL is mandatory to publish. "
                "See: https://validator.w3.org/feed/docs/rss2.html#requiredChannelElements"
            )
            self.feed_created["rss_url"] = self.feed_updated["json_url"] = (
                self.feed_updated["rss_url"]
            ) = self.feed_updated["json_url"] = None

        # ending event
        return config

    @event_priority(priority=-75)
    def on_page_content(
        self, html: str, page: Page, config: MkDocsConfig, files: Files
    ) -> Optional[str]:
        """The page_content event is called after the Markdown text is rendered to HTML
            (but before being passed to a template) and can be used to alter the HTML
            body of the page.

        See: https://www.mkdocs.org/user-guide/plugins/#on_page_content

        Args:
            html (str): HTML rendered from Markdown source as string
            page (Page): `mkdocs.structure.pages.Page` instance
            config (MkDocsConfig): global configuration object
            files (Files): global files collection

        Returns:
            Optional[str]: HTML rendered from Markdown source as string
        """
        # Skip if disabled
        if not self.config.enabled:
            return

        # skip pages that don't match the config var match_path
        if not self.match_path_pattern.match(page.file.src_path):
            return

        # skip pages with draft=true
        if page.meta.get("draft", False) is True:
            logger.debug(f"Page {page.title} ignored because it's a draft")
            return

        # retrieve dates from git log
        page_dates = self.util.get_file_dates(
            in_page=page,
            source_date_creation=self.config.date_from_meta.as_creation,
            source_date_update=self.config.date_from_meta.as_update,
            meta_datetime_format=self.config.date_from_meta.datetime_format,
            meta_default_timezone=self.config.date_from_meta.default_timezone,
            meta_default_time=self.config.date_from_meta.default_time,
        )

        # handle custom URL parameters
        if self.config.url_parameters:
            page_url_full = self.util.build_url(
                base_url=page.canonical_url,
                path="",
                args_dict=self.config.url_parameters,
            )
        else:
            page_url_full = page.canonical_url

        # handle URL comment path
        if self.config.comments_path:
            page_url_comments = self.util.build_url(
                base_url=page.canonical_url,
                path=self.config.comments_path,
            )
        else:
            page_url_comments = None

        # append to list to be filtered later
        self.pages_to_filter.append(
            PageInformation(
                abs_path=Path(page.file.abs_src_path),
                authors=self.util.get_authors_from_meta(in_page=page),
                categories=self.util.get_categories_from_meta(
                    in_page=page, categories_labels=self.config.categories
                ),
                created=page_dates[0],
                description=self.util.get_description_or_abstract(
                    in_page=page,
                    chars_count=self.config.abstract_chars_count,
                    abstract_delimiter=self.config.abstract_delimiter,
                ),
                guid=page.canonical_url,
                image=self.util.get_image(
                    in_page=page,
                    # below let it as old dict get method to handle custom fallback value
                    base_url=config.get("site_url", __uri__),
                ),
                title=page.title,
                updated=page_dates[1],
                url_comments=page_url_comments,
                url_full=page_url_full,
            )
        )

    def on_post_build(self, config: config_options.Config) -> None:
        """The post_build event does not alter any variables. Use this event to call
            post-build scripts.

        See:
            <https://www.mkdocs.org/user-guide/plugins/#on_post_build>

        Args:
            config (config_options.Config): global configuration object
        """
        # Skip if disabled
        if not self.config.enabled:
            return

        # pretty print or not
        pretty_print = self.config.pretty_print

        # output filepaths
        out_feed_created = Path(config.site_dir).joinpath(
            self.config.feeds_filenames.rss_created
        )
        out_feed_updated = Path(config.site_dir).joinpath(
            self.config.feeds_filenames.rss_updated
        )
        out_json_created = Path(config.site_dir).joinpath(
            self.config.feeds_filenames.json_created
        )
        out_json_updated = Path(config.site_dir).joinpath(
            self.config.feeds_filenames.json_updated
        )

        # created items
        self.feed_created.get("entries").extend(
            self.util.filter_pages(
                pages=self.pages_to_filter,
                attribute="created",
                length=self.config.length,
            )
        )

        # updated items
        self.feed_updated.get("entries").extend(
            self.util.filter_pages(
                pages=self.pages_to_filter,
                attribute="updated",
                length=self.config.length,
            )
        )

        # RSS
        if self.config.rss_feed_enabled:
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

        # JSON FEED
        if self.config.json_feed_enabled:
            with out_json_created.open(mode="w", encoding="UTF8") as fp:
                json.dump(
                    self.util.feed_to_json(self.feed_created),
                    fp,
                    indent=4 if self.config.pretty_print else None,
                )

            with out_json_updated.open(mode="w", encoding="UTF8") as fp:
                json.dump(
                    self.util.feed_to_json(self.feed_updated, updated=True),
                    fp,
                    indent=4 if self.config.pretty_print else None,
                )
