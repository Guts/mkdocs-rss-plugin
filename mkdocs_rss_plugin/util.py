#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
from email.utils import formatdate
from mimetypes import guess_type
from typing import Tuple
from urllib.parse import urlencode, urlparse, urlunparse

# 3rd party
from git import GitCommandError, GitCommandNotFound, InvalidGitRepositoryError, Repo
from mkdocs.config.config_options import Config
from mkdocs.structure.pages import Page
from mkdocs.utils import get_build_timestamp

# package
from mkdocs_rss_plugin.git_manager.ci import CiHandler


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

    def get_file_dates(self, path: str) -> Tuple[int, int]:
        """Extract creation and update dates from git log for given file.

        :param str path: path to a tracked file

        :return: (creation date, last commit date)
        :rtype: tuple of timestamps
        """
        # empty vars
        dt_created = dt_updated = None

        # explore git log
        if self.git_is_valid:
            try:
                dt_created = self.repo.log(
                    path, n=1, date="short", format="%at", diff_filter="AR"
                )
                dt_updated = self.repo.log(
                    path,
                    n=1,
                    date="short",
                    format="%at",
                )
            except GitCommandError as err:
                logging.warning(
                    "[rss-plugin] Unable to read git logs of '%s'. Is git log readable?"
                    " Falling back to build date. "
                    " Trace: %s" % (path, err)
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
            logging.warning("Dates could not be retrieved for page: %s." % path)
            return (
                get_build_timestamp(),
                get_build_timestamp(),
            )

    def get_description_or_abstract(self, in_page: Page, chars_count: int = 150) -> str:
        """Returns description from page meta. If it doesn't exist, use the \
        {chars_count} first characters from page content (in markdown).

        :param Page in_page: [description]
        :param int chars_count: [description]. Defaults to: 150 - optional

        :return: page description to use
        :rtype: str
        """
        if in_page.meta.get("description"):
            return in_page.meta.get("description")
        elif in_page.content:
            return in_page.content[:chars_count]
        elif in_page.markdown:
            return in_page.markdown[:chars_count]
        else:
            return ""

    def get_image(self, in_page: Page, base_url: str) -> tuple:
        """Get image from page meta.

        :param in_page: page to parse
        :type in_page: Page
        :param base_url: website URL to resolve absolute URLs for images referenced with local path.
        :type base_url: str

        :return: (image url, mime type)
        :rtype: tuple
        """
        if in_page.meta.get("image"):
            img_url = in_page.meta.get("image")
        elif in_page.meta.get("illustration"):
            img_url = in_page.meta.get("illustration")
        else:
            return (None, None)

        # guess mimetype
        mime_type = guess_type(url=img_url, strict=False)[0]
        # if path, resolve absolute url
        if not img_url.startswith("http"):
            img_url = self.build_url(base_url=base_url, path=img_url)

        # return final tuple
        return (img_url, mime_type)

    @staticmethod
    def guess_locale(config: Config) -> str or None:
        """Extract language code from MkDocs or Theme configuration.

        :param config: configuration object
        :type config: Config

        :return: language code
        :rtype: str or None
        """
        # MkDocs locale settings - might be added in future mkdocs versions
        # see: https://github.com/timvink/mkdocs-git-revision-date-localized-plugin/issues/24
        if config.get("locale"):
            return config.get("locale")

        # Some themes implement a locale or a language setting
        if "theme" in config and "locale" in config.get("theme"):
            return config.get("theme")._vars.get("locale")
        elif "theme" in config and "language" in config.get("theme"):
            return config.get("theme")._vars.get("language")
        else:
            return None

    @staticmethod
    def filter_pages(pages: dict, attribute: str, length: int) -> list:
        """Filter and return pages into a friendly RSS structure.

        :param pages: pages to filter
        :type pages: dict
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
                    "description": page.description,
                    "link": page.url_full,
                    "pubDate": formatdate(page.created),
                    "title": page.title,
                    "image": page.image,
                }
            )

        return filtered_pages
