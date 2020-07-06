#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
import os
from datetime import datetime
from typing import Tuple

# 3rd party
from git import Git
from mkdocs.structure.pages import Page


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

    def get_file_dates(
        self, path: str, fallback_to_build_date: bool = False
    ) -> Tuple[datetime, datetime]:
        """Extract creation and update dates from git log for given file.

        :param str path: path to a tracked file
        :param bool fallback_to_build_date: [description]. Defaults to: False - optional

        :return: (creation date, last commit date)
        :rtype: tuple
        """
        dt_created = int(
            self.repo.log(path, n=1, date="short", format="%at", diff_filter="A")
        )
        dt_updated = int(self.repo.log(path, n=1, date="short", format="%at",))

        return (
            datetime.utcfromtimestamp(dt_created),
            datetime.utcfromtimestamp(dt_updated),
        )
