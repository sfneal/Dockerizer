from argparse import ArgumentParser

from Dockerizer.compose import DockerCompose


def main():
    # Declare argparse argument descriptions
    usage = 'docker-compose utility for rebooting (rebuilding/restarting) container services.'
    description = 'Pull, build and run docker-compose services.'
    helpers = {
        'services': "Name(s) of the services to build.",
    }

    # construct the argument parse and parse the arguments
    ap = ArgumentParser(usage=usage, description=description)
    ap.add_argument('--services', help=helpers['services'], nargs='+')
    args = vars(ap.parse_args())

    # Run bootstrap
    DockerCompose(services=args['services']).reboot()


if __name__ == '__main__':
    main()
