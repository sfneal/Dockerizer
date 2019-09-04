class DockerComposeCommands:
    def __init__(self, services=None):
        """
        A collection of properties and methods that return docker command strings.

        Provides access to underlying docker-compose commands that are executed.  Use cases
        include debugging, logging and copying and pasting commands to terminal
        in order to save time typing repeated commands.

       :param services: List of services to build
        """
        self.services = services

    @property
    def pull(self):
        """Returns a docker-compose 'pull' command string."""
        return 'docker-compose pull'

    @property
    def build(self):
        """Returns a docker-compose 'build' command string with specific services if set."""
        return 'docker-compose build {0}'.format(' '.join(self.services) if self.services else '').strip()

    @staticmethod
    def up(detached=False, build=False):
        """
        Returns a docker-compose 'up' command string.

        :param detached: Run services in 'detached' mode so that output is not streamed to console
        :param build: Build container services
        """
        return 'docker-compose up {} {}'.format('--build' if build else '', '-d' if detached else '').strip()

    @staticmethod
    def down(volumes=False):
        """
        Returns a docker-compose 'down' command string.

        :param volumes: Remove volumes
        :return:
        """
        return 'docker-compose down {}'.format('-v' if volumes else '')

    @property
    def bootstrap(self):
        """Return list of commands to execute for docker-compose bootstrapping."""
        return self.pull, self.up(detached=True), self.build, self.down(volumes=True), self.up(detached=True)

    @property
    def reboot(self):
        """Reboot docker-compose container services by rebuilding then restarting."""
        return self.build, self.down(volumes=True), self.up(detached=True)
