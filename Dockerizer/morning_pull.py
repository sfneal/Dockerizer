from looptools import Timer
from databasetools import JSON
from Dockerizer.config import MORNING_PULL_JSON
from Dockerizer.docker import Docker, unpack_image_name


@Timer.decorator
def morning_pull():
    to_pull = JSON(MORNING_PULL_JSON).read()['images']
    print('Morning Pull - Docker image pull utility')
    print('\tlist path: {0}'.format(MORNING_PULL_JSON))
    print('\timages to pull:')
    for i, img in enumerate(to_pull):
        print('\t\t{0:2}: {1}'.format(i + 1, img))

    if len(to_pull) > 0:
        for pull in to_pull:
            Docker(**unpack_image_name(pull)).pull()
    else:
        print('No images to pull.  Add images to morning_pull.json.')

    print('\nAvailable Docker Images:')
    for i, image in enumerate(Docker().images):
        print('\t{0}: {1}'.format(i, image))
    print('\n')


def main():
    morning_pull()


if __name__ == '__main__':
    main()
