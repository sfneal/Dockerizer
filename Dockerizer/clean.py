from looptools import Timer
from Dockerizer.docker import Docker


@Timer.decorator
def clean():
    d = Docker()
    d.clean()
    d.delete_volumes()


def main():
    clean()


if __name__ == '__main__':
    main()
