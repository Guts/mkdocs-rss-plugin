from unittest.mock import Mock

from mkdocs_rss_plugin.git_manager.ci import CiHandler


def test_commit_count_returns_zero_when_repository_has_no_refs():
    repo = Mock()
    repo.for_each_ref.return_value = ""

    assert CiHandler(repo).commit_count() == 0
