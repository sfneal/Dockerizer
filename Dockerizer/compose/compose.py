import os

from looptools import Timer
from RuntimeWatch import TaskTracker
from dirutility import SystemCommand

from Dockerizer.compose.commands import DockerComposeCommands


class DockerCompose(TaskTracker):
    def __init__(self, directory=os.getcwd(), services=None):
        """
        Docker compose command wrapper.

        :param services: List of services to build
        """
        self._starting_directory = os.getcwd()
        self.directory = directory
        self.cmd = DockerComposeCommands(services)

        # Change to target directory
        os.chdir(self.directory)

    def __exit__(self):
        os.chdir(self._starting_directory)

    def pull(self):
        """Pull docker-compose images from Docker Hub."""
        sc = SystemCommand(self.cmd.pull, decode_output=False)
        self.add_command(sc.command)
        self.add_task('Pulled docker-compose service images')

    def build(self):
        """Build a docker image for distribution to DockerHub."""
        sc = SystemCommand(self.cmd.build, decode_output=False)
        self.add_command(sc.command)
        self.add_task('Built docker-compose services')

    def up(self):
        """Run docker-compose services locally."""
        sc = SystemCommand(self.cmd.up, decode_output=False)
        self.add_command(sc.command)

    def down(self):
        """Push a docker image to a DockerHub repo."""
        sc = SystemCommand(self.cmd.down, decode_output=False)
        self.add_command(sc.command)
        self.add_task('Stopped docker-compose services')

    @Timer.decorator
    def bootstrap(self):
        """Bootstrap docker-compose service development by pulling existing images then building services."""
        print('Bootstrapping docker-compose services')
        for index, cmd in enumerate(self.cmd.bootstrap):
            sc = SystemCommand(cmd, decode_output=False)
            self.add_command(sc.command)
            if sc.success:
                self.add_task('SUCCESS ({}/{}): {}'.format(index + 1, len(self.cmd.bootstrap) + 1, sc.command))
            else:
                self.add_task('ERROR   ({}/{}): {}'.format(index + 1, len(self.cmd.bootstrap) + 1, sc.command))

    @Timer.decorator
    def reboot(self):
        """Reboot docker-compose container services by rebuilding then restarting."""
        print('Bootstrapping docker-compose services')
        for index, cmd in enumerate(self.cmd.reboot):
            sc = SystemCommand(cmd, decode_output=False)
            self.add_command(sc.command)
            if sc.success:
                self.add_task('SUCCESS ({}/{}): {}'.format(index + 1, len(self.cmd.reboot) + 1, sc.command))
            else:
                self.add_task('ERROR   ({}/{}): {}'.format(index + 1, len(self.cmd.reboot) + 1, sc.command))