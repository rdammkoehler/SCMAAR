from os import path
from random import randint
from re import search
from tempfile import TemporaryFile, TemporaryDirectory

import pytest
from git import Repo

from scmaar.scanner import scan


def helper_add_file(repo, filename=str(randint(0, 1000)), content='file'):
    filepath = path.join(repo.working_tree_dir, filename)
    with open(filepath, mode='w', encoding='utf-8') as file:
        file.write(content)
    repo.index.add([filepath])
    repo.index.commit(filename)


def helper_add_readme(repo):
    helper_add_file(repo, 'README.md', '# SCMAAR Test Repo!')


class RepositoryContext:
    """
    A Repository Context object for testing
    """

    def __init__(self, commit_count=1):
        # pylint: disable=R1732
        self.temp_dir = TemporaryDirectory()
        self.repo = Repo.init(self.temp_dir.name)
        helper_add_readme(self.repo)
        if commit_count:
            for _ in range(1, commit_count):
                helper_add_file(self.repo)

    def __enter__(self):
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
    with RepositoryContext() as test_repo:
        updated_pattern = r'Last Updated: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\+|-)\d{2}:\d{2}'
        assert search(updated_pattern, scan(test_repo.temp_dir.name)), 'Last Updated date not found'


def test_scan_report_contains_last_authored_datetime():
    with RepositoryContext() as test_repo:
        authored_pattern = r'Last Authored: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\+|-)\d{2}:\d{2}'
        assert search(authored_pattern, scan(test_repo.temp_dir.name)), 'Last Authored date not found'


def test_commit_is_reported():
    with RepositoryContext() as test_repo:
        report = scan(test_repo.temp_dir.name)

        assert search(r'Commit [0-9a-z]{40}', report)
        assert "\t{'insertions': 1, 'deletions': 0, 'lines': 1, 'files': 1}" in report
        assert search(r'size \d+ bytes', report), 'Size of commit not found in report'


def test_each_commit_is_reported():
    with RepositoryContext(commit_count=2) as test_repo:
        report = scan(test_repo.temp_dir.name)

        assert report.count('Commit ') == 2
