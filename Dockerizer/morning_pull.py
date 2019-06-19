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
        print('\t{0:2}: {1}'.format(i + 1, item))


def mp_json(json_path=MORNING_PULL_JSON):
    """Return JSON object with morning_pull.json available."""
    return JSON(json_path)


def add_image(image, json_path=MORNING_PULL_JSON):
    """Add a Docker Image to the morning_pull.json list."""
    mp_json(json_path).append(key='images', data=image)


def remove_image(image, json_path=MORNING_PULL_JSON):
    """Remove a Docker Image from the morning_pull.json list."""
    images = get_mp_list()
    images.pop(images.index(image))
    mp_json(json_path).update(key='images', data=images)


def get_mp_list():
    return sorted(mp_json().read()['images'])


def print_morning_pull(msg='morning-pull Docker Image list:'):
    list_print(get_mp_list(), msg)


def enumerate_images(images=None):
    """Return a dictionary of enumerated Docker images with ID keys and Docker image values."""
    return {i + 1: item for i, item in enumerate(get_mp_list() if not images else images)}


@Timer.decorator
def morning_pull():
    to_pull = get_mp_list()
    print('Morning Pull - Docker image pull utility')
    print('\tlist path: {0}'.format(MORNING_PULL_JSON))
    list_print(to_pull, 'Docker Images to pull:')

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
        'add': "Name(s) of the Docker image to add to the morning pull list",
        'remove': "Name(s) of the Docker image to remove from the morning pull list",
        'list': "Display the morning pull Docker Image list",
        'edit': "Edit the morning-pull docker image list",
    }

    # construct the argument parse and parse the arguments
    ap = ArgumentParser(usage=usage, description=description)
    ap.add_argument('--add', help=helpers['add'], nargs='+')
    ap.add_argument('--remove', help=helpers['remove'], nargs='+')
    ap.add_argument('--list', help=helpers['list'], action='store_true')
    ap.add_argument('--edit', help=helpers['edit'], action='store_true')
    args = vars(ap.parse_args())

    # Run morning pull if no additional arguments were passed
    if all(k in (None, False) for k in args.values()):
        print('Morning pull')
        morning_pull()
    else:
        # Display the morning pull list
        if args['list']:
            print_morning_pull()

        # Add images to morning pull list
        if args['add']:
            print('Added the following Docker Image(s) to the morning pull list:')
            for image in args['add']:
                if image not in mp_json().read()['images']:
                    print('\t{0}'.format(image))
                    add_image(image.strip())

        # Remove images from the morning pull list
        if args['remove']:
            print('Removing the following Docker Image(s) from the morning pull list:')
            for image in args['remove']:
                print('\t{0}'.format(image))
                remove_image(image.strip())

        # Edit the morning-pull Docker image list
        if args['edit']:
            print_morning_pull()
            print('\nEnter the ID(s) of the image(s) you would like to remove separated by spaced')
            removals = input('Image(s) to remove: ')
            if len(removals) > 0:
                image_ids = list(map(int, removals.split(' ')))
                if len(image_ids) > 0:
                    for i_id, img in enumerate_images().items():
                        if i_id in image_ids:
                            print('\tRemoving', img.strip())
                            remove_image(img.strip())
                    print_morning_pull('\nNew morning-pull Docker image list:')
            else:
                print('No images to remove.')


if __name__ == '__main__':
    main()
