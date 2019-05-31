from looptools import Timer
from databasetools import JSON
from Dockerizer.config import MORNING_PULL_JSON
from Dockerizer.docker import Docker, unpack_image_name


def list_print(items, head=None):
    if head:
        print(head)
    for i, item in enumerate(items):
        print('\t\t{0:2}: {1}'.format(i + 1, item))


@Timer.decorator
def morning_pull():
    to_pull = JSON(MORNING_PULL_JSON).read()['images']
    print('Morning Pull - Docker image pull utility')
    print('\tlist path: {0}'.format(MORNING_PULL_JSON))
    list_print(to_pull, '\timages to pull:')

    if len(to_pull) > 0:
        for pull in to_pull:
            Docker(**unpack_image_name(pull)).pull()
    else:
        print('No images to pull.  Add images to morning_pull.json.')
    images = Docker().images
    list_print(images, '\nAvailable Docker Images:')
    return images


def main():
    morning_pull()


if __name__ == '__main__':
    main()
