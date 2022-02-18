from os import listdir
from os.path import isdir

from git import Repo


def scan(directory):
    if not directory:
        raise NotADirectoryError
    if not isdir(directory):
        raise NotADirectoryError
    listing = listdir(directory)
    if '.git' not in listing:
        raise FileNotFoundError(f'{directory} is not a git repo')
    repo = Repo(directory)
    try:
        head = repo.head
        head_commit = head.commit
        report = f'Last Updated: {head_commit.committed_datetime}\n'
        report += f'Last Authored: {head_commit.authored_datetime}\n'
        report += _create_commit_block(head_commit)
        for commit in head_commit.iter_parents():
            report += _create_commit_block(commit)
        return report
    except ValueError:
        return 'no commits found at head'


def _create_commit_block(commit):
    stats = commit.stats
    return f'Commit {commit.hexsha}\n' \
           f'\tCommitted {commit.committed_datetime}\n' \
           f'\tCommitter {commit.committer}\n' \
           f'\tAuthored  {commit.authored_datetime}\n' \
           f'\tAuthor    {commit.author}\n' \
           f'\tSummary   {commit.summary}\n' \
           f'\t{stats.total}\n' \
           f'\tsize {commit.size} bytes\n'
