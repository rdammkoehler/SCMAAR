from datetime import datetime
from os import path
from tempfile import TemporaryFile, TemporaryDirectory

import pytest
from git import Repo

from scmaar.scanner import scan


def helper_add_readme(repo):
    readme_path = path.join(repo.working_tree_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as readme:
        readme.write('# SCMAAR Test Repo!')
    repo.index.add([readme_path])
    repo.index.commit('testing')


class RepositoryContext:
    """
    A Repository Context object for testing
    """
    def __init__(self):
        # pylint: disable=R1732
        self.temp_dir = TemporaryDirectory()
        self.repo = Repo.init(self.temp_dir.name)

    def __enter__(self):
        helper_add_readme(self.repo)
        return self

    def __exit__(self, type_, value, traceback):
        self.repo.close()
        self.temp_dir.cleanup()


def test_scan_requires_directory():
    with pytest.raises(NotADirectoryError):
        scan(None)


def test_scan_directory_must_be_directory_type():
    with TemporaryFile() as temp_file:
        with pytest.raises(NotADirectoryError):
            scan(temp_file.name)


def test_scan_directory_must_be_git_repo():
    with TemporaryDirectory() as temp_dir_name:
        with pytest.raises(FileNotFoundError) as exc_info:
            scan(temp_dir_name)

        assert exc_info.value.args[0] == f'{temp_dir_name} is not a git repo'


def test_scan_reports_error_on_empty_repo():
    with TemporaryDirectory() as temp_dir_name:
        with Repo.init(temp_dir_name):
            assert scan(temp_dir_name) == 'no commits found at head'


def test_scan_reports_on_repo():
    with TemporaryDirectory() as temp_dir_name:
        with Repo.init(temp_dir_name) as repo:
            helper_add_readme(repo)
            assert scan(temp_dir_name) is not None


def test_scan_report_contains_last_updated_datetime():
    now = datetime.now().replace(microsecond=0)
    with RepositoryContext() as test_repo:
        assert f'Last Updated: {now}' in scan(test_repo.temp_dir.name)


def test_scan_report_contains_last_authored_datetime():
    now = datetime.now().replace(microsecond=0)
    with RepositoryContext() as test_repo:
        assert f'Last Authored: {now}' in scan(test_repo.temp_dir.name)
