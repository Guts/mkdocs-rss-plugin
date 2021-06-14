#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
import ssl
from datetime import date, datetime
from email.utils import formatdate
from mimetypes import guess_type
from pathlib import Path
from typing import Tuple
from urllib import request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse, urlunparse

# 3rd party
import markdown
from git import GitCommandError, GitCommandNotFound, InvalidGitRepositoryError, Repo
from mkdocs.config.config_options import Config
from mkdocs.structure.pages import Page
from mkdocs.utils import get_build_timestamp

# package
from mkdocs_rss_plugin import __about__
from mkdocs_rss_plugin.git_manager.ci import CiHandler

# ############################################################################
# ########## Globals #############
# ################################

REMOTE_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "{}/{}".format(__about__.__title__, __about__.__version__),
}


# ############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger("mkdocs.mkdocs_rss_plugin")


# ############################################################################
# ########## Classes #############
# ################################


class Util:
    def __init__(self, path: str = "."):
        """Class hosting the plugin logic.

        :param str path: path tot the git repository to use. Defaults to: "." - optional
        """
        try:
            git_repo = Repo(path, search_parent_directories=True)
            self.repo = git_repo.git
            self.git_is_valid = 1
        except InvalidGitRepositoryError as err:
            logging.warning(
                "[rss-plugin] Path is not a valid git directory. " " Trace: %s" % err
            )
            self.git_is_valid = 0
        except Exception as err:
            logging.warning("[rss-plugin] Git issue: %s" % err)
            self.git_is_valid = 0

        # Checks if user is running builds on CI and raise appropriate warnings
        CiHandler(git_repo.git).raise_ci_warnings()

    def build_url(self, base_url: str, path: str, args_dict: dict = None) -> str:
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
        # Returns a list in the structure of urlparse.ParseResult
        url_parts = list(urlparse(base_url))
        url_parts[2] += path
        if args_dict:
            url_parts[4] = urlencode(args_dict)
        return urlunparse(url_parts)

    def get_file_dates(
        self,
        in_page: Page,
        source_date_creation: str = "git",
        source_date_update: str = "git",
        meta_datetime_format: str = "%Y-%m-%d %H:%M",
    ) -> Tuple[int, int]:
        """Extract creation and update dates from page metadata (yaml frontmatter) or \
            git log for given file.

        :param in_page: input page to work with
        :type in_page: Page
        :param source_date_creation: which source to use (git or meta tag) for creation \
            date, defaults to "git"
        :type source_date_creation: str, optional
        :param source_date_update: which source to use (git or meta tag) for update \
            date, defaults to "git"
        :type source_date_update: str, optional
        :param meta_datetime_format: datetime string format, defaults to "%Y-%m-%d %H:%M"
        :type meta_datetime_format: str, optional

        :return: tuple of timestamps (creation date, last commit date)
        :rtype: Tuple[int, int]
        """
        # empty vars
        dt_created = dt_updated = None

        # if enabled, try to retrieve dates from page metadata
        if source_date_creation != "git" and in_page.meta.get(source_date_creation):
            dt_created = self.get_date_from_meta(
                date_metatag_value=in_page.meta.get(source_date_creation),
                meta_datetime_format=meta_datetime_format,
            )
            if isinstance(dt_created, str):
                logger.error(dt_created)
                dt_created = None

        if source_date_update != "git" and in_page.meta.get(source_date_update):
            dt_updated = self.get_date_from_meta(
                date_metatag_value=in_page.meta.get(source_date_creation),
                meta_datetime_format=meta_datetime_format,
            )
            if isinstance(dt_updated, str):
                logger.error(dt_updated)
                dt_updated = None

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
                    "[rss-plugin] Unable to read git logs of '%s'. Is git log readable?"
                    " Falling back to build date. "
                    " Trace: %s" % (in_page.file.abs_src_path, err)
                )
            except GitCommandNotFound as err:
                logging.error(
                    "[rss-plugin] Unable to perform command 'git log'. Is git installed? "
                    " Falling back to build date. "
                    " Trace: %s" % err
                )
                self.git_is_valid = 0
        else:
            pass

        # return results
        if all([dt_created, dt_updated]):
            return (
                int(dt_created),
                int(dt_updated),
            )
        else:
            logging.warning(
                "[rss-plugin] Dates could not be retrieved for page: %s."
                % in_page.file.abs_src_path
            )
            return (
                get_build_timestamp(),
                get_build_timestamp(),
            )

    def get_authors_from_meta(self, in_page: Page) -> Tuple[str] or None:
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
                    "[rss-plugin] Type of author value in page.meta (%s) is not valid. "
                    "It should be str, list or tuple, not: %s."
                    % in_page.file.abs_src_path,
                    type(in_page.meta.get("author")),
                )
                return None
        elif "authors" in in_page.meta:
            if isinstance(in_page.meta.get("authors"), str):
                return (in_page.meta.get("authors"),)
            elif isinstance(in_page.meta.get("authors"), (list, tuple)):
                return tuple(in_page.meta.get("authors"))
            else:
                logging.warning(
                    "[rss-plugin] Type of authors value in page.meta (%s) is not valid. "
                    "It should be str, list or tuple, not: %s."
                    % in_page.file.abs_src_path,
                    type(in_page.meta.get("authors")),
                )
                return None

    def get_date_from_meta(
        self, date_metatag_value: str, meta_datetime_format: str
    ) -> float:
        """Get date from page.meta handling str with associated datetime format and \
            date already transformed by MkDocs.

        :param date_metatag_value: value of page.meta.{tag_for_date}
        :type date_metatag_value: str
        :param meta_datetime_format: expected format of datetime
        :type meta_datetime_format: str

        :return: datetime as timestamp
        :rtype: float
        """
        out_date = None
        try:
            if isinstance(date_metatag_value, str):
                out_date = datetime.strptime(date_metatag_value, meta_datetime_format)
            elif isinstance(date_metatag_value, (date, datetime)):
                out_date = datetime.combine(date_metatag_value, datetime.min.time())
            else:
                return "[rss-plugin] Incompatible date type."
        except ValueError as err:
            return "[rss-plugin] Incompatible date found. Trace: {}".format(err)
        except Exception as err:
            return "[rss-plugin] Unable to retrieve creation date. Trace: {}".format(
                err
            )

        return out_date.timestamp()

    def get_description_or_abstract(self, in_page: Page, chars_count: int = 150) -> str:
        """Returns description from page meta. If it doesn't exist, use the \
        {chars_count} first characters from page content (in markdown).

        :param Page in_page: page to look at
        :param int chars_count: if page.meta.description is not set, number of chars \
        of the content to use. Defaults to: 150 - optional

        :return: page description to use
        :rtype: str
        """
        if in_page.meta.get("description"):
            return in_page.meta.get("description")
        elif in_page.content:
            if len(in_page.content) < chars_count:
                return markdown.markdown(
                    in_page.content[:chars_count], output_format="html5"
                )
            else:
                return markdown.markdown(
                    "{}...".format(in_page.content[: chars_count - 3]),
                    output_format="html5",
                )
        elif in_page.markdown:
            if len(in_page.markdown) < chars_count:
                return markdown.markdown(
                    in_page.markdown[:chars_count], output_format="html5"
                )
            else:
                return markdown.markdown(
                    "{}...".format(in_page.markdown[: chars_count - 3]),
                    output_format="html5",
                )
        else:
            return ""

    def get_image(self, in_page: Page, base_url: str) -> tuple:
        """Get image from page meta and returns properties.

        :param in_page: page to parse
        :type in_page: Page
        :param base_url: website URL to resolve absolute URLs for images referenced with local path.
        :type base_url: str

        :return: (image url, mime type, image length)
        :rtype: tuple
        """
        if in_page.meta.get("image"):
            img_url = in_page.meta.get("image")
        elif in_page.meta.get("illustration"):
            img_url = in_page.meta.get("illustration")
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

    def get_local_image_length(self, page_path: str, path_to_append: str) -> int:
        """Build URL using base URL, cumulating existing and passed path, \
        then adding URL arguments.

        :param page_path: base URL with existing path to use
        :type base_url: str
        :param path: URL path to cumulate with existing
        :type path: str

        :return: complete and valid path
        :rtype: int
        """
        image_path = Path(page_path).parent / Path(path_to_append)
        if not image_path.is_file():
            return None

        return image_path.stat().st_size

    def get_remote_image_length(
        self,
        image_url: str,
        http_method: str = "HEAD",
        attempt: int = 0,
        ssl_context: ssl.SSLContext = None,
    ) -> int:
        """Retrieve length for remote images (starting with 'http' \
            in meta.image or meta.illustration). \
            It tries to perform a HEAD request and get the length from the headers. \
            If it fails, it tries again with a GET and disabling SSL verification.

        :param image_url: remote image URL
        :type image_url: str
        :param http_method: HTTP method used to perform request, defaults to "HEAD"
        :type http_method: str, optional
        :param attempt: request tries counter, defaults to 0
        :type attempt: int, optional
        :param ssl_context: SSL context, defaults to None
        :type ssl_context: ssl.SSLContext, optional

        :return: image length as str or None
        :rtype: int
        """
        # prepare request
        req = request.Request(
            image_url,
            method=http_method,
            headers=REMOTE_REQUEST_HEADERS,
        )
        # first, try HEAD request to avoid downloading the image
        try:
            attempt += 1
            remote_img = request.urlopen(url=req, context=ssl_context)
            img_length = remote_img.getheader("content-length")
        except (HTTPError, URLError) as err:
            logging.warning(
                "[rss-plugin] Remote image could not been reached: {}. "
                "Trying again with GET and disabling SSL verification. Attempt: {}. "
                "Trace: {}".format(image_url, attempt, err)
            )
            if attempt < 2:
                return self.get_remote_image_length(
                    image_url,
                    http_method="GET",
                    attempt=attempt,
                    ssl_context=ssl._create_unverified_context(),
                )
            else:
                logging.error(
                    "[rss-plugin] Remote image is not reachable: {} after {} attempts. "
                    " Trace: {}".format(
                        image_url,
                        attempt,
                        err,
                    )
                )
                return None

        return int(img_length)

    @staticmethod
    def get_site_url(mkdocs_config: Config) -> str or None:
        """Extract site URL from MkDocs configuration and enforce the behavior to ensure \
        returning a str with length > 0 or None. If exists, it adds an ending slash.

        :param mkdocs_config: configuration object
        :type mkdocs_config: Config

        :return: site url
        :rtype: str or None
        """
        # this method exists because the following line returns an empty string instead of \
        # None (because the key alwayus exists)
        defined_site_url = mkdocs_config.get("site_url", None)

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

    @staticmethod
    def guess_locale(mkdocs_config: Config) -> str or None:
        """Extract language code from MkDocs or Theme configuration.

        :param mkdocs_config: configuration object
        :type mkdocs_config: Config

        :return: language code
        :rtype: str or None
        """
        # MkDocs locale settings - might be added in future mkdocs versions
        # see: https://github.com/timvink/mkdocs-git-revision-date-localized-plugin/issues/24
        if mkdocs_config.get("locale"):
            return mkdocs_config.get("locale")

        # Some themes implement a locale or a language setting
        if "theme" in mkdocs_config and "locale" in mkdocs_config.get("theme"):
            return mkdocs_config.get("theme")._vars.get("locale")
        elif "theme" in mkdocs_config and "language" in mkdocs_config.get("theme"):
            return mkdocs_config.get("theme")._vars.get("language")
        else:
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
            filtered_pages.append(
                {
                    "authors": page.authors,
                    "comments_url": page.url_comments,
                    "description": page.description,
                    "guid": page.guid,
                    "image": page.image,
                    "link": page.url_full,
                    "pubDate": formatdate(getattr(page, attribute)),
                    "title": page.title,
                }
            )

        return filtered_pages
