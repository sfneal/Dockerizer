
from databasetools import JSON


def main():
    to_pull = JSON(MORNING_PULL_JSON).read()['images']


if __name__ == '__main__':
    main()
