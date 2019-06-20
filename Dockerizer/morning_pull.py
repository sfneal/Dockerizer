from argparse import ArgumentParser
from looptools import Timer
from databasetools import JSON
from Dockerizer.config import MORNING_PULL_JSON
from Dockerizer.docker import Docker, unpack_image_name


class MorningPull:
    def __init__(self, json_path=MORNING_PULL_JSON):
        self.json_path = json_path
        self._json = None
        self._existing_images = None

    @property
    def json(self):
        """Return JSON object with morning_pull.json available."""
        if not self._json:
            self._json = JSON(self.json_path)
        return self._json

    @property
    def existing_images(self):
        if not self._existing_images:
            self._existing_images = sorted(self.json.read()['images'])
        return self._existing_images

    @property
    def images_dict(self):
        """Return a dictionary of enumerated Docker images with ID keys and Docker image values."""
        return {i + 1: item for i, item in enumerate(self.existing_images)}

    def pull(self):
        to_pull = self.existing_images
        print('Morning Pull - Docker image pull utility')
        print('\tlist path: {0}'.format(MORNING_PULL_JSON))
        self.print('Docker Images to pull:')

        if len(to_pull) > 0:
            with Timer('morning-pull'):
                for pull in to_pull:
                    Docker(**unpack_image_name(pull)).pull()
        else:
            print('No images to pull.  Add images to morning_pull.json.')
        images = Docker().images
        self.print('\nAvailable Docker Images:')
        return images

    def print(self, msg='morning-pull Docker Image list:'):
        """Print a list of items."""
        if msg:
            print(msg)
        for i, item in enumerate(self.existing_images):
            print('\t{0:2}: {1}'.format(i + 1, item))

    def _add(self, image):
        """Add a Docker Image to the morning_pull.json list."""
        self.json.append(key='images', data=image)

    def add(self, images_to_add):
        print('Added the following Docker Image(s) to the morning pull list:')
        for image in images_to_add:
            if image not in self.json.read()['images']:
                print('\t{0}'.format(image))
                self._add(image.strip())

    def _remove(self, image):
        """Remove a Docker Image from the morning_pull.json list."""
        self.existing_images.pop(self.existing_images.index(image))
        self.json.update(key='images', data=self.existing_images)

    def remove(self, images_to_remove):
        print('Removing the following Docker Image(s) from the morning pull list:')
        for image in images_to_remove:
            print('\t{0}'.format(image))
            self._remove(image.strip())

    def edit(self):
        self.print()
        print('\nEnter the ID(s) of the image(s) you would like to remove separated by spaced')
        removals = input('Image(s) to remove: ')
        if len(removals) > 0:
            image_ids = list(map(int, removals.split(' ')))
            if len(image_ids) > 0:
                for i_id, img in self.images_dict.items():
                    if i_id in image_ids:
                        print('\tRemoving', img.strip())
                        self._remove(img.strip())
                self.print('\nNew morning-pull Docker image list:')
        else:
            print('No images to remove.')


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

    # Initialize MorningPull
    mp = MorningPull()

    # Run morning pull if no additional arguments were passed
    if all(k in (None, False) for k in args.values()):
        print('Morning pull')
        mp.pull()
    else:
        # Display the morning pull list
        if args['list']:
            mp.print()

        # Add images to morning pull list
        if args['add']:
            mp.add(args['add'])

        # Remove images from the morning pull list
        if args['remove']:
            mp.remove(args['remove'])

        # Edit the morning-pull Docker image list
        if args['edit']:
            mp.edit()


if __name__ == '__main__':
    main()
