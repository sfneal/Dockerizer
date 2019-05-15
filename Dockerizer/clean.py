from looptools import Timer
from Dockerizer.docker import Docker


@Timer.decorator
def clean():
    Docker().clean()


def main():
    clean()


if __name__ == '__main__':
    main()
