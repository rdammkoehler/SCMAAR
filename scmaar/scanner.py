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
        head = repo.head.commit
        return f'Last Updated: {head.committed_datetime}\n' \
               f'Last Authored: {head.authored_datetime}\n'
    except ValueError:
        return 'no commits found at head'
