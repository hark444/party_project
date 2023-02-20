import os
import re

# Picking tasks_checklist as default file
BASE_DIR = os.path.dirname(os.getcwd())
filename = BASE_DIR + '/tasks_checklist.txt'


def get_latest_tag():
    latest_tag = 000
    regex = r"\d{3}"

    with open(filename, "r") as file:
        for line in file.read().split('\n'):
            res = re.search(regex, line)
            if res and int(res.group()) > latest_tag:
                latest_tag = int(res.group())

    return latest_tag


if __name__ == '__main__':
    last_tag = get_latest_tag()
    print(last_tag)
