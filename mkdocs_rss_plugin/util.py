#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
from collections.abc import Iterable
from datetime import date, datetime
from email.utils import format_datetime
from mimetypes import guess_type
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urlparse, urlunparse

# 3rd party
import markdown
from git import GitCommandError, GitCommandNotFound, InvalidGitRepositoryError, Repo
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.pages import Page
from mkdocs.utils import get_build_datetime
from requests import Session
from requests.exceptions import HTTPError

# package
from mkdocs_rss_plugin.constants import MKDOCS_LOGGER_NAME, REMOTE_REQUEST_HEADERS
from mkdocs_rss_plugin.git_manager.ci import CiHandler
from mkdocs_rss_plugin.integrations.theme_material_social_plugin import (
    IntegrationMaterialSocialCards,
)
from mkdocs_rss_plugin.timezoner import set_datetime_zoneinfo

# ############################################################################
# ########## Globals #############
# ################################

logger = get_plugin_logger(MKDOCS_LOGGER_NAME)

# ############################################################################
# ########## Classes #############
# ################################


class Util:
    """Plugin logic."""

    git_is_valid: bool = False

    def __init__(
        self,
        path: str = ".",
        use_git: bool = True,
        integration_material_social_cards: None | (
            IntegrationMaterialSocialCards
        ) = None,
    ):
        """Class hosting the plugin logic.

        Args:
            path (str, optional): path to the git repository to use. Defaults to ".".
            use_git (bool, optional): flag to use git under the hood or not. Defaults to True.
            integration_material_social_cards (bool, optional): option to enable
                integration with Social Cards plugin from Material theme. Defaults to True.
        """
        if use_git:
            logger.debug("Git use is enabled.")
            try:
                git_repo = Repo(path, search_parent_directories=True)
                self.repo = git_repo.git
                self.git_is_valid = True
            except InvalidGitRepositoryError as err:
                logger.warning(
                    f"Path '{path}' is not a valid git directory. "
                    "Only page.meta (YAML frontmatter will be used). "
                    "To disable this warning, set 'use_git: false' in plugin options. "
                    f"Trace: {err}"
                )
                self.git_is_valid = False
                use_git = False
            except Exception as err:
                logger.warning(
                    f"Unrecognized git issue. "
                    "Only page.meta (YAML frontmatter will be used). "
                    "To disable this warning, set 'use_git: false' in plugin options. "
                    f"Trace: {err}"
                )
                self.git_is_valid = False
                use_git = False

            # Checks if user is running builds on CI and raise appropriate warnings
            if self.git_is_valid:
                CiHandler(git_repo.git).raise_ci_warnings()
        else:
            self.git_is_valid = False
            logger.debug(
                "Git use is disabled. "
                "Only page.meta (YAML frontmatter will be used). "
            )

        # save git enable/disable status
        self.use_git = use_git

        # save integrations
        self.social_cards = integration_material_social_cards

        # http/s session
        self.req_session = Session()
        self.req_session.headers.update(REMOTE_REQUEST_HEADERS)

    def build_url(self, base_url: str, path: str, args_dict: dict | None = None) -> str:
        """Build URL using base URL, cumulating existing and passed path, \
        then adding URL arguments.

        :param base_url: base URL with existing path to use
        :type base_url: str
        :param path: URL path to cumulate with existing
        :type path: str
        :param args_dict: URL arguments to add, defaults to None
        :type args_dict: dict, optional

        :return: complete and valid URL
        :rtype: str
        """
        if not base_url:
            logger.error(
                "Base url not set, probably because 'site_url' is not set "
                "in Mkdocs configuration file. Using an empty string instead."
            )
            base_url = ""

        # Returns a list in the structure of urlparse.ParseResult
        url_parts = list(urlparse(base_url))
        url_parts[2] += path
        if args_dict:
            url_parts[4] = urlencode(args_dict)
        return urlunparse(url_parts)

    def get_value_from_dot_key(self, data: dict, dot_key: str | bool) -> Any:
        """
        Retrieves a value from a dictionary using a dot notation key.

        :param data: The dictionary from which to retrieve the value.
        :type data: dict
        :param dot_key: The key in dot notation to specify the path in the dictionary.
        :type dot_key: Union[str, bool]

        :return: The value retrieved from the dictionary, or None if the key
        does not exist.
        :rtype: Any
        """
        if not isinstance(dot_key, str):
            return data.get(dot_key)
        for key in dot_key.split("."):
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data

    def get_file_dates(
        self,
        in_page: Page,
        source_date_creation: str,
        source_date_update: str,
        meta_datetime_format: str,
        meta_default_timezone: str,
        meta_default_time: datetime,
    ) -> tuple[datetime, datetime]:
        """Extract creation and update dates from page metadata (yaml frontmatter) or
        git log for given file.

        :param in_page: input page to work with
        :type in_page: Page
        :param source_date_creation: which source to use (git or meta tag) for creation
        date, defaults to "git"
        :type source_date_creation: str, optional
        :param source_date_update: which source to use (git or meta tag) for update
        date, defaults to "git"
        :type source_date_update: str, optional
        :param meta_datetime_format: datetime string format, defaults to "%Y-%m-%d %H:%M"
        :type meta_datetime_format: str, optional
        :param meta_default_timezone: timezone to use, defaults to "UTC"
        :type meta_default_timezone: str, optional
        :param meta_default_time: time to set if not specified, defaults to None
        :type meta_default_time: datetime, optional

        :return: tuple of timestamps (creation date, last commit date)
        :rtype: Tuple[datetime, datetime]
        """
        logger.debug(f"Extracting dates for {in_page.file.src_uri}")
        # empty vars
        dt_created = dt_updated = None
        if meta_default_time is None:
            meta_default_time = self.meta_default_time = datetime.min

        # if enabled, try to retrieve dates from page metadata
        if not self.use_git or (
            source_date_creation != "git"
            and self.get_value_from_dot_key(in_page.meta, source_date_creation)
        ):
            dt_created = self.get_date_from_meta(
                date_metatag_value=self.get_value_from_dot_key(
                    in_page.meta, source_date_creation
                ),
                meta_datetime_format=meta_datetime_format,
                meta_datetime_timezone=meta_default_timezone,
                meta_default_time=meta_default_time,
            )
            if isinstance(dt_created, str):
                logger.info(
                    f"Creation date of {in_page.file.abs_src_path} is an "
                    f"a character string: {dt_created} ({type(dt_created)})"
                )

            elif dt_created is None:
                logger.info(
                    f"Creation date of {in_page.file.abs_src_path} has not "
                    "been recognized."
                )

        if not self.use_git or (
            source_date_update != "git"
            and self.get_value_from_dot_key(in_page.meta, source_date_update)
        ):
            dt_updated = self.get_date_from_meta(
                date_metatag_value=self.get_value_from_dot_key(
                    in_page.meta, source_date_update
                ),
                meta_datetime_format=meta_datetime_format,
                meta_datetime_timezone=meta_default_timezone,
                meta_default_time=meta_default_time,
            )

            if isinstance(dt_updated, str):
                logger.debug(
                    f"Update date of {in_page.file.abs_src_path} is a "
                    f"character string: {dt_updated} ({type(dt_updated)})"
                )

            elif dt_updated is None:
                logger.debug(
                    f"Update date of {in_page.file.abs_src_path} is an "
                    f"unrecognized type: {dt_updated} ({type(dt_updated)})"
                )

        # explore git log
        if self.git_is_valid:
            try:
                # only if dates have not been retrieved from page meta
                if not dt_created:
                    dt_created = self.repo.log(
                        in_page.file.abs_src_path,
                        n=1,
                        date="short",
                        format="%at",
                        diff_filter="AR",
                    )
                if not dt_updated:
                    dt_updated = self.repo.log(
                        in_page.file.abs_src_path,
                        n=1,
                        date="short",
                        format="%at",
                    )
            except GitCommandError as err:
                logging.warning(
                    f"Unable to read git logs of '{in_page.file.abs_src_path}'. "
                    "Is git log readable? Falling back to build date. "
                    "To disable this warning, set 'use_git: false' in plugin options. "
                    f"Trace: {err}"
                )
            except GitCommandNotFound as err:
                logging.error(
                    "Unable to perform command 'git log'. Is git installed? "
                    "Falling back to build date. "
                    "To disable this warning, set 'use_git: false' in plugin options. "
                    f"Trace: {err}"
                )
                self.git_is_valid = 0
            # convert timestamps into datetimes
            if isinstance(dt_created, (str, float, int)) and dt_created:
                dt_created = set_datetime_zoneinfo(
                    datetime.fromtimestamp(float(dt_created)), meta_default_timezone
                )
            if isinstance(dt_updated, (str, float, int)) and dt_updated:
                dt_updated = set_datetime_zoneinfo(
                    datetime.fromtimestamp(float(dt_updated)), meta_default_timezone
                )

        # results
        if all([dt_created, dt_updated]):
            return (
                dt_created,
                dt_updated,
            )
        elif dt_created:
            log_msg = (
                "Updated date could not be retrieved for page: "
                f"{in_page.file.abs_src_path}. Fallback to build date."
            )
            if self.use_git:
                log_msg += "Maybe it has never been committed yet?"
            logger.debug(log_msg)
            return (
                dt_created,
                get_build_datetime(),
            )
        elif dt_updated:
            log_msg = (
                "Creation date could not be retrieved for page: "
                f"{in_page.file.abs_src_path}. Fallback to build date."
            )
            if self.use_git:
                log_msg += "Maybe it has never been committed yet?"
            logger.debug(log_msg)
            return (
                get_build_datetime(),
                dt_updated,
            )
        else:
            logger.info(
                f"Dates could not be retrieved for page: {in_page.file.abs_src_path}."
            )
            return (
                get_build_datetime(),
                get_build_datetime(),
            )

    def get_authors_from_meta(self, in_page: Page) -> tuple[str] | None:
        """Returns authors from page meta. It handles 'author' and 'authors' for keys, \
        str and iterable as values types.

        :param in_page: page to look into
        :type in_page: Page

        :return: tuple of authors names
        :rtype: Tuple[str] or None
        """
        # identify the key
        if "author" in in_page.meta:
            if isinstance(in_page.meta.get("author"), str):
                return (in_page.meta.get("author"),)
            elif isinstance(in_page.meta.get("author"), (list, tuple)):
                return tuple(in_page.meta.get("author"))
            else:
                logging.warning(
                    "Type of author value in page.meta "
                    f"({in_page.file.abs_src_path}) is not valid. "
                    "It should be str, list or tuple, "
                    f"not: {type(in_page.meta.get('author'))}."
                )
                return None
        elif "authors" in in_page.meta:
            if isinstance(in_page.meta.get("authors"), str):
                return (in_page.meta.get("authors"),)
            elif isinstance(in_page.meta.get("authors"), (list, tuple)):
                return tuple(in_page.meta.get("authors"))
            else:
                logging.warning(
                    "Type of authors value in page.meta (%s) is not valid. "
                    "It should be str, list or tuple, not: %s."
                    % in_page.file.abs_src_path,
                    type(in_page.meta.get("authors")),
                )
                return None

    def get_categories_from_meta(
        self, in_page: Page, categories_labels: Iterable
    ) -> list | None:
        """Returns category from page meta.

        :param in_page: input page to parse
        :type in_page: Page
        :param categories_labels: meta tags to look into
        :type categories_labels: Iterable

        :return: found categories
        :rtype: list
        """
        if not categories_labels:
            return None

        output_categories = []
        for category_label in categories_labels:
            if category_label in in_page.meta:
                if isinstance(in_page.meta.get(category_label), (list, tuple)):
                    output_categories.extend(in_page.meta.get(category_label))
                elif isinstance(in_page.meta.get(category_label), str):
                    output_categories.append(in_page.meta.get(category_label))
            else:
                continue
        return sorted(output_categories)

    def get_date_from_meta(
        self,
        date_metatag_value: str,
        meta_datetime_format: str,
        meta_datetime_timezone: str,
        meta_default_time: datetime,
    ) -> datetime:
        """Get date from page.meta handling str with associated datetime format and \
            date already transformed by MkDocs.

        :param date_metatag_value: value of page.meta.{tag_for_date}
        :type date_metatag_value: str
        :param meta_datetime_format: expected format of datetime
        :type meta_datetime_format: str
        :param meta_datetime_timezone: timezone to use
        :type meta_datetime_timezone: str
        :param meta_default_time: time to set if not specified
        :type meta_default_time: datetime

        :return: datetime
        :rtype: datetime
        """
        out_date = None
        try:
            if isinstance(date_metatag_value, str):
                out_date = datetime.strptime(date_metatag_value, meta_datetime_format)
            # datetime being a subclass of date, the following elif order matters
            # see: https://stackoverflow.com/a/68743663/2556577
            elif isinstance(date_metatag_value, datetime):
                # if datetime, use it directly
                out_date = date_metatag_value
            elif isinstance(date_metatag_value, date):
                out_date = datetime.combine(
                    date=date_metatag_value, time=meta_default_time.time()
                )
            else:
                logger.debug(
                    f"Incompatible date type: {type(date_metatag_value)}. It must be: "
                    "date, datetime or str (complying with defined strftime format)."
                )
                return out_date
        except ValueError as err:
            logger.error(
                f"Incompatible date found: {date_metatag_value=} "
                f"{type(date_metatag_value)}. Trace: {err}"
            )
            return out_date
        except Exception as err:
            logger.error(
                f"Unable to retrieve creation date: {date_metatag_value=} "
                f"{type(date_metatag_value)}. Trace: {err}"
            )
            return out_date

        if not out_date.tzinfo:
            out_date = set_datetime_zoneinfo(out_date, meta_datetime_timezone)

        return out_date

    def get_description_or_abstract(
        self, in_page: Page, chars_count: int = 160, abstract_delimiter: str = None
    ) -> str:
        """Returns description from page meta. If it doesn't exist, use the \
        page content up to {abstract_delimiter} or the {chars_count} first \
        characters from page content (in markdown).

        :param Page in_page: page to look at
        :param int chars_count: if page.meta.description is not set, number of chars \
        of the content to use. Defaults to: 160 - optional
        :param str abstract_delimiter: description delimiter, defaults to None

        :return: page description to use
        :rtype: str
        """

        description = in_page.meta.get("description")

        # If the full page is wanted (unlimited chars count)
        if chars_count == -1 and (in_page.content or in_page.markdown):
            if in_page.content:
                return in_page.content
            else:
                return markdown.markdown(in_page.markdown, output_format="html5")
        # If the description is explicitly given
        elif description:
            return description
        # If the abstract is cut by the delimiter
        elif (
            abstract_delimiter
            and (
                excerpt_separator_position := in_page.markdown.find(abstract_delimiter)
            )
            > -1
        ):
            return markdown.markdown(
                in_page.markdown[:excerpt_separator_position],
                output_format="html5",
            )
        # Use first chars_count from the markdown
        elif chars_count > 0 and in_page.markdown:
            if len(in_page.markdown) <= chars_count:
                return markdown.markdown(in_page.markdown, output_format="html5")
            else:
                return markdown.markdown(
                    f"{in_page.markdown[: chars_count - 3]}...",
                    output_format="html5",
                )
        # No explicit description and no (or empty) abstract found
        else:
            logger.warning(
                f"No description generated from metadata or content of the page {in_page.file.src_uri}, "
                "therefore the feed won't be compliant, "
                "because an item must have a description."
            )
            return ""

    def get_image(self, in_page: Page, base_url: str) -> tuple[str, str, int] | None:
        """Get page's image from page meta or social cards and returns properties.

        Args:
            in_page (Page): page to parse
            base_url (str): website URL to resolve absolute URLs for images referenced
                with local path.

        Returns:
            Optional[Tuple[str, str, int]]: (image url, mime type, image length) or None if
                there is no image set
        """
        if in_page.meta.get("image"):
            img_url = in_page.meta.get("image").strip()
            logger.debug(
                f"Image found ({img_url}) in page.meta.image for page: "
                f"{in_page.file.src_uri}"
            )
        elif in_page.meta.get("illustration"):
            img_url = in_page.meta.get("illustration").strip()
            logger.debug(
                f"Image found ({img_url}) in page.meta.illustration for page: "
                f"{in_page.file.src_uri}"
            )
        elif (
            isinstance(self.social_cards, IntegrationMaterialSocialCards)
            and self.social_cards.IS_ENABLED
            and self.social_cards.IS_SOCIAL_PLUGIN_CARDS_ENABLED
            and self.social_cards.is_social_plugin_enabled_page(
                mkdocs_page=in_page,
                fallback_value=self.social_cards.IS_SOCIAL_PLUGIN_CARDS_ENABLED,
            )
        ):

            img_url = self.social_cards.get_social_card_url_for_page(
                mkdocs_page=in_page
            )
            if img_local_cache_path := self.social_cards.get_social_card_cache_path_for_page(
                mkdocs_page=in_page
            ):
                img_length = img_local_cache_path.stat().st_size
                img_type = guess_type(url=img_local_cache_path, strict=False)[0]
            elif img_local_build_path := self.social_cards.get_social_card_build_path_for_page(
                mkdocs_page=in_page
            ):
                img_length = img_local_build_path.stat().st_size
                img_type = guess_type(url=img_local_build_path, strict=False)[0]
            else:
                logger.debug(
                    "Social card still not exists locally. Trying to "
                    f"retrieve length from remote image: {img_url}. "
                    "Note that would work only if the social card image has been "
                    "already published before the build."
                )
                img_length = self.get_remote_image_length(image_url=img_url)
                img_type = guess_type(url=img_url, strict=False)[0]

            return (
                img_url,
                img_type,
                img_length,
            )

        else:
            return None

        # guess mimetype
        mime_type = guess_type(url=img_url, strict=False)[0]

        # if path, resolve absolute url
        if not img_url.startswith("http"):
            img_length = self.get_local_image_length(
                page_path=in_page.file.abs_src_path, path_to_append=img_url
            )
            img_url = self.build_url(base_url=base_url, path=img_url)
        else:
            img_length = self.get_remote_image_length(image_url=img_url)

        # return final tuple
        return (img_url, mime_type, img_length)

    def get_local_image_length(self, page_path: str, path_to_append: str) -> int | None:
        """Calculates local image size in octets.

        Args:
            page_path (str): source path to the Mkdocs page
            path_to_append (str): path to append

        Returns:
            int: size in octets
        """
        image_path = Path(page_path).parent / Path(path_to_append)
        if not image_path.is_file():
            logger.debug(f"{image_path} not found")
            return None

        return image_path.stat().st_size

    def get_remote_image_length(
        self,
        image_url: str,
        http_method: str = "HEAD",
        attempt: int = 0,
        ssl_verify: bool = True,
    ) -> int | None:
        """Retrieve length for remote images (starting with 'http').

        Firstly, it tries to perform a HEAD request and get the length from the headers. \
        If it fails, it tries again with a GET and disabling SSL verification.

        Args:
            image_url (str): image URL
            http_method (str, optional): HTTP method to use for the request.
                Defaults to "HEAD".
            attempt (int, optional): request tries counter. Defaults to 0.
            ssl_verify (bool, optional): option to perform SSL verification or not.
                Defaults to True.

        Returns:
            int | None: image length as int or None
        """
        # first, try HEAD request to avoid downloading the image
        try:
            attempt += 1
            req_response = self.req_session.request(
                method=http_method, url=image_url, verify=ssl_verify
            )
            req_response.raise_for_status()
            img_length = req_response.headers.get("content-length")
        except HTTPError as err:
            logger.debug(
                f"Remote image could not been reached: {image_url}. "
                f"Trying again with GET and disabling SSL verification. Attempt: {attempt}. "
                f"Trace: {err}"
            )
            if attempt < 2:
                return self.get_remote_image_length(
                    image_url, http_method="GET", attempt=attempt, ssl_verify=False
                )
            else:
                logger.info(
                    f"Remote image is not reachable: {image_url} after "
                    f"{attempt} attempts. Trace: {err}"
                )
                return None

        return int(img_length)

    @staticmethod
    def get_site_url(mkdocs_config: MkDocsConfig) -> str | None:
        """Extract site URL from MkDocs configuration and enforce the behavior to ensure \
        returning a str with length > 0 or None. If exists, it adds an ending slash.

        :param mkdocs_config: configuration object
        :type mkdocs_config: Config

        :return: site url
        :rtype: str or None
        """
        # this method exists because the following line returns an empty string instead of \
        # None (because the key alwayus exists)
        defined_site_url = mkdocs_config.site_url

        # cases
        if defined_site_url is None or not len(defined_site_url):
            # in case of mkdocs's behavior change
            site_url = None
        else:
            site_url = defined_site_url
            # handle trailing slash
            if not site_url.endswith("/"):
                site_url = site_url + "/"

        return site_url

    def guess_locale(self, mkdocs_config: MkDocsConfig) -> str | None:
        """Extract language code from MkDocs or Theme configuration.

        :param mkdocs_config: configuration object
        :type mkdocs_config: Config

        :return: language code
        :rtype: str or None
        """
        # MkDocs locale settings - might be added in future mkdocs versions
        # see: https://github.com/timvink/mkdocs-git-revision-date-localized-plugin/issues/24
        if mkdocs_config.get("locale"):
            logger.warning(
                DeprecationWarning(
                    "Mkdocs does not support locale option at the "
                    "configuration root but under theme sub-configuration. It won't be "
                    "supported anymore by the plugin in the next version."
                )
            )
            return mkdocs_config.get("locale")

        # Some themes implement a locale or a language settings
        if "theme" in mkdocs_config:
            if (
                self.social_cards.IS_THEME_MATERIAL
                and "language" in mkdocs_config.theme
            ):
                # TODO: remove custom behavior when Material theme switches to locale
                # see: https://github.com/squidfunk/mkdocs-material/discussions/6453
                logger.debug(
                    "Language detected in Material theme "
                    f"('{mkdocs_config.theme.name}') settings: "
                    f"{mkdocs_config.theme.get('language')}"
                )
                return mkdocs_config.theme.get("language")

            elif "locale" in mkdocs_config.theme:
                locale = mkdocs_config.theme.locale
                logger.debug(
                    "Locale detected in theme "
                    f"('{mkdocs_config.theme.name}') settings: {locale=}"
                )
                return (
                    f"{locale.language}-{locale.territory}"
                    if locale.territory
                    else f"{locale.language}"
                )
            else:
                logger.debug(
                    "Nor locale or language detected in theme settings "
                    f"('{mkdocs_config.theme.name}')."
                )

        return None

    @staticmethod
    def filter_pages(pages: list, attribute: str, length: int) -> list:
        """Filter and return pages into a friendly RSS structure.

        :param pages: pages to filter
        :type pages: list
        :param attribute: page attribute as filter variable
        :type attribute: str
        :param length: max number of pages to return
        :type length: int

        :return: list of filtered pages
        :rtype: list
        """
        filtered_pages = []
        for page in sorted(
            pages, key=lambda page: getattr(page, attribute), reverse=True
        )[:length]:
            pub_date: datetime = getattr(page, attribute)
            filtered_pages.append(
                {
                    "authors": page.authors,
                    "categories": page.categories,
                    "comments_url": page.url_comments,
                    "description": page.description,
                    "guid": page.guid,
                    "image": page.image,
                    "link": page.url_full,
                    "pubDate": format_datetime(dt=pub_date),
                    "pubDate3339": pub_date.isoformat("T"),
                    "title": page.title,
                }
            )

        return filtered_pages

    @staticmethod
    def feed_to_json(feed: dict, *, updated: bool = False) -> dict:
        """Format internal feed representation as a JSON Feed compliant dict.

        :param feed: internal feed structure, i. e.
            GitRssPlugin.feed_created/feed_updated value
        :type feed: dict
        :param updated: True if this is a feed_updated
        :type updated: bool

        :return: dict that can be passed to json.dump
        :rtype: dict
        """
        entry_date_key = "date_modified" if updated else "date_published"

        return {
            "version": "https://jsonfeed.org/version/1",
            "title": feed.get("title"),
            "home_page_url": feed.get("html_url"),
            "feed_url": feed.get("json_url"),
            "description": feed.get("description"),
            "icon": feed.get("logo_url"),
            "authors": (
                [{"name": feed.get("author")}] if feed.get("author") is not None else []
            ),
            "language": str(feed.get("language")),
            "items": [
                {
                    "id": item.get("guid"),
                    "url": item.get("link"),
                    "title": item.get("title"),
                    "content_html": item.get("description"),
                    "image": (item.get("image") or (None,))[0],
                    entry_date_key: item.get("pubDate3339"),
                    "authors": [{"name": name} for name in (item.get("authors") or ())],
                    "tags": item.get("categories"),
                }
                for item in feed.get("entries", ())
            ],
        }
