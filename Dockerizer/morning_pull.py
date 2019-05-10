from looptools import Timer
from databasetools import JSON
from Dockerizer.config import MORNING_PULL_JSON
from Dockerizer.docker import Docker, unpack_image_name


@Timer.decorator
def morning_pull():
    print('\nMorning pull image list path: {0}\n'.format(MORNING_PULL_JSON))
    to_pull = JSON(MORNING_PULL_JSON).read()['images']

    if len(to_pull) > 0:
        print('Pulling {0} images from DockerHub:\n'.format(len(to_pull)))
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
