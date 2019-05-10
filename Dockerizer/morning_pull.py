from databasetools import JSON
from Dockerizer.config import MORNING_PULL_JSON
from Dockerizer.docker import Docker


def main():
    print('Morning pull image list path:\n{0}'.format(MORNING_PULL_JSON))
    to_pull = JSON(MORNING_PULL_JSON).read()['images']

    if to_pull > 0:
        for pull in to_pull


if __name__ == '__main__':
    main()
