from looptools import Timer
from Dockerizer.docker import Docker


@Timer.decorator
def reset():
    docker = Docker()
    docker.delete_containers()
    docker.delete_images()


def main():
    reset()


if __name__ == '__main__':
    main()
