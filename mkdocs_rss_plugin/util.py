#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
import os
from typing import Tuple

# 3rd party
from git import Git, GitCommandError, GitCommandNotFound
from mkdocs.structure.pages import Page
from mkdocs.utils import get_build_timestamp


# ############################################################################
# ########## Functions #############
# ##################################
def is_shallow_clone(repo: Git) -> bool:
    """
    Helper function to determine if repository
    is a shallow clone.

    References:
    https://stackoverflow.com/a/37203240/5525118

    Args:
        repo (git.Repo): Repository

    Returns:
        bool: If a repo is shallow clone
    """
    return os.path.exists(".git/shallow")


def commit_count(repo: Git) -> bool:
    """
    Helper function to determine the number of commits in a repository

    Args:
        repo (git.Repo): Repository

    Returns:
        count (int): Number of commits
    """
    refs = repo.for_each_ref().split("\n")
    refs = [x.split()[0] for x in refs]

    counts = [int(repo.rev_list(x, count=True, first_parent=True)) for x in refs]
    return max(counts)


# ############################################################################
# ########## Classes #############
# ################################
class Util:
    def __init__(self, path: str = "."):
        self.repo = Git(path)

        # Checks when running builds on CI
        # See https://github.com/guts/mkdocs-rss-plugin/issues/10
        if is_shallow_clone(self.repo):
            n_commits = commit_count(self.repo)

            if os.environ.get("GITLAB_CI") and n_commits < 50:
                # Default is GIT_DEPTH of 50 for gitlab
                logging.warning(
                    """
                       Running on a gitlab runner might lead to wrong git revision dates
                       due to a shallow git fetch depth.
                       Make sure to set GIT_DEPTH to 1000 in your .gitlab-ci.yml file.
                       (see https://docs.gitlab.com/ee/user/project/pipelines/settings.html#git-shallow-clone).
                       """
                )
            if os.environ.get("GITHUB_ACTIONS") and n_commits == 1:
                # Default is fetch-depth of 1 for github actions
                logging.warning(
                    """
                       Running on github actions might lead to wrong git revision dates
                       due to a shallow git fetch depth.
                       Try setting fetch-depth to 0 in your github action
                       (see https://github.com/actions/checkout).
                       """
                )

    def get_file_dates(self, path: str) -> Tuple[int, int]:
        """Extract creation and update dates from git log for given file.

        :param str path: path to a tracked file

        :return: (creation date, last commit date)
        :rtype: tuple
        """
        # empty vars
        dt_created = dt_updated = None

        # explore git log
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
