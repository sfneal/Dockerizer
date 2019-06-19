from RuntimeWatch import TaskTracker
from dirutility import SystemCommand, Versions

from Dockerizer.docker.commands import DockerCommands


def unpack_image_name(image_name):
    """Retrieve a dict with (user, repo, tag) keys by extracting values from a Docker image name string."""
    d = dict()
    if '/' in image_name:
        split = image_name.split('/', 1)
        d['username'] = split[0]
    else:
        split = [None, image_name]
    d['repo'] = split[1].split(':', 1)[0] if ':' in image_name else split[1]
    d['tag'] = split[1].split(':', 1)[1] if ':' in image_name else None
    return d


class Docker(TaskTracker):
    def __init__(self, source=None, repo=None, tag=None, username=None, host_port=None, container_port=None,
                 dockerfile='Dockerfile', build_cache=True):
        """
        Docker hub deployment helper.

        :param source: Docker files source path
        :param repo: Docker repo name
        :param tag: Docker repo tag
        :param username: Docker username
        :param host_port: Host port to publish when running Docker image
        :param container_port: Container port to expose
        :param dockerfile: Path to Dockerfile (relative to source)
        :param build_cache: Bool, use cache's to decrease docker build times
        """
        self.cmd = DockerCommands(source, repo, tag, username, host_port, container_port, dockerfile, build_cache)

    @property
    def source(self):
        return self.cmd.source

    @property
    def repo(self):
        return self.cmd.repo

    @property
    def tag(self):
        return self.cmd.tag

    @property
    def username(self):
        return self.cmd.username

    @property
    def host_port(self):
        return self.cmd.host_port

    @property
    def container_port(self):
        return self.cmd.container_port

    @property
    def dockerfile(self):
        return self.cmd.dockerfile

    @property
    def available_commands(self):
        """Return a string containing all available Docker commands"""
        return '\nAVAILABLE DOCKER COMMANDS:\n' + '\n'.join('{0}'.format(cmd) for cmd in
                                                            (self.cmd.build, self.cmd.run, self.cmd.push)) + '\n'

    def build(self):
        """Build a docker image for distribution to DockerHub."""
        print('Building Docker image ({0})'.format(self.cmd.docker_image))
        sc = SystemCommand(self.cmd.build, decode_output=False)
        self.add_command(sc.command)
        self.add_task('Built Docker image ({0})'.format(self.cmd.docker_image))

    def run(self):
        """Push a docker image to a DockerHub repo."""
        print('Locally running Docker image')
        sc = SystemCommand(self.cmd.run, decode_output=False)
        self.add_command(sc.command)
        if sc.success:
            self.add_task('Running Docker image ({0}) on local machine'.format(self.cmd.docker_image))
        else:
            self.add_task('ERROR: Unable to running Docker image ({0}) on local machine'.format(self.cmd.docker_image))

    def push(self):
        """Push a docker image to a DockerHub repo."""
        print('Pushing Docker image ({0})'.format(self.cmd.docker_image))
        sc = SystemCommand(self.cmd.push, decode_output=False)
        self.add_command(sc.command)
        self.add_task('Pushed Docker image {0} to DockerHub repo'.format(self.cmd.docker_image))

    def pull(self, resolve_tag=True):
        """Push a docker image to a DockerHub repo."""
        if resolve_tag and not self.cmd.tag:
            self.cmd.tag = self.image_tags[0]
        print('Pulling Docker image ({0})'.format(self.cmd.docker_image))
        sc = SystemCommand(self.cmd.pull, decode_output=False)
        self.add_command(sc.command)
        self.add_task('Pulled Docker image {0} from DockerHub repo'.format(self.cmd.docker_image))

    @property
    def images(self):
        """Return a list of Docker images on the current machine."""
        output = SystemCommand(self.cmd.images).output
        output.pop(0)
        return [row.split(' ', 1)[0] + ':' + row.split(' ', 1)[1].strip().split(' ', 1)[0] for row in output]

    @property
    def image_tags(self):
        """Return a list of available tags for a docker image sorted by version."""
        return Versions(SystemCommand(self.cmd.image_tags).output).sorted

    @property
    def containers(self):
        """Return a list of containers on the current machine."""
        return SystemCommand(self.cmd.containers).output

    def delete_containers(self):
        """Delete all containers on the current machine."""
        if len(self.containers) > 0:
            SystemCommand(self.cmd.delete_containers)

    def delete_images(self):
        """Delete all images on the current machine."""
        if len(self.images) > 0:
            return SystemCommand(self.cmd.delete_images)

    def delete_volumes(self):
        """Delete all volumes on the current machine."""
        return SystemCommand(self.cmd.delete_volumes)

    def clean(self):
        """Remove stopped containers and intermediate images from the current machine."""
        return SystemCommand(self.cmd.clean)
