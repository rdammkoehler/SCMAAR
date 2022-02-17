from argparse import ArgumentParser

parser = ArgumentParser(prog='scmaar', description='source control management analysis and reporting tool')
parser.add_argument('dir', help='the directory containing a repository needing examination')

args = parser.parse_args()

print(f'You said I should analyse {args.dir}')
