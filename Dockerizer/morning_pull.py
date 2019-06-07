from argparse import ArgumentParser
from looptools import Timer
from databasetools import JSON
from Dockerizer.config import MORNING_PULL_JSON
from Dockerizer.docker import Docker, unpack_image_name


def list_print(items, head=None):
    """Print a list of items."""
    if head:
        print(head)
    for i, item in enumerate(items):
        print('\t\t{0:2}: {1}'.format(i + 1, item))


def mp_json(json_path=MORNING_PULL_JSON):
    """Return JSON object with morning_pull.json available."""
    return JSON(json_path)


def add_image(image, json_path=MORNING_PULL_JSON):
    """Add a Docker Image to the morning_pull.json list."""
    mp_json(json_path).append(key='images', data=image)


@Timer.decorator
def morning_pull():
    to_pull = mp_json().read()['images']
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
    # Declare argparse argument descriptions
    usage = 'Docker multi-image pull utility.'
    description = 'Pull multiple Docker images from the Docker Hub repository.'
    helpers = {
        'add': "Name of the Docker image to add to the morning pull list",
    }

    # construct the argument parse and parse the arguments
    ap = ArgumentParser(usage=usage, description=description)
    ap.add_argument('--add', help=helpers['add'], nargs='+')
    args = ap.parse_args()

    # Add images to morning pull list
    if args.add:
        print('Added the following Docker Image(s) to the morning pull list:')
        for image in args.add:
            print('\t{0}'.format(image))
            add_image(image.strip())
    else:
        morning_pull()


if __name__ == '__main__':
    main()
