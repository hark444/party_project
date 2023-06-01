import sys

args = sys.argv

with open('./.github/workflows/foo.txt', 'w') as env_file:
    env_file.writelines(args[1])
