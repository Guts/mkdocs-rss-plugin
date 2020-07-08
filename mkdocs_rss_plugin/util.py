#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
from typing import Tuple

# 3rd party
from git import GitCommandError, GitCommandNotFound, InvalidGitRepositoryError, Repo
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
                dt_updated = self.repo.log(path, n=1, date="short", format="%at",)
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
