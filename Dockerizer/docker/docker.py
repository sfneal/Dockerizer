import os

from RuntimeWatch import TaskTracker
from dirutility import SystemCommand, Versions


def unpack_image_name(image_name):
    """Retrieve a dict with (user, repo, tag) keys by extracting values from a Docker image name string."""
    split = image_name.split('/', 1)
    return {'username': split[0],
            'repo': split[1].split(':', 1)[0] if ':' in image_name else split[1],
            'tag': split[1].split(':', 1)[1] if ':' in image_name else None}


class DockerCommands:
    def __init__(self, source=None, repo=None, tag=None, username=None, host_port=None, container_port=None,
                 dockerfile='Dockerfile', build_cache=True):
        """
        A collection of properties and methods that return docker command strings.

        Provides access to underlying Docker commands that are executed.  Use cases
        include debugging, logging and copying and pasting commands to terminal
        in order to save time typing repeated commands.

        :param source: Docker files source path
        :param repo: Docker repo name
        :param tag: Docker repo tag
        :param username: Docker username
        :param host_port: Host port to publish when running Docker image
        :param container_port: Container port to expose
        :param dockerfile: Path to Dockerfile (relative to source)
        :param build_cache: Bool, use cache's to decrease docker build times
        """
        self.source = source
        self.repo = repo
        self.tag = tag
        self.username = username
        self.host_port = host_port
        self.container_port = container_port
        self.dockerfile = dockerfile
        self.build_cache = build_cache

    @property
    def docker_image(self):
        """Concatenate DockerHub user name and environment name to create docker image tag."""
        i = '{user}/{repo}'.format(user=self.username, repo=self.repo)
        if self.tag:
            i += ':{tag}'.format(tag=self.tag)
        return i

    @property
    def dockerfile_path(self):
        """Join source path and Dockerfile path to create full path to Dockerfile."""
        return os.path.join(self.source, self.dockerfile)

    @property
    def build(self):
        """Returns a Docker 'build' command string."""
        cmd = 'docker build -t {tag} -f {dockerfile}'.format(tag=self.docker_image, dockerfile=self.dockerfile_path)
        if not self.build_cache:
            cmd += ' --no-cache'
        cmd += ' {source}'.format(source=self.source,)
        return cmd

    @property
    def run(self):
        """Returns a Docker 'run' command string."""
        # Docker run command with 'interactive' and 'tag' flags
        cmd = 'docker run -i -t'

        # Confirm both host_port and container_port are integers
        if all(port != '' and isinstance(int(port), int) for port in (self.host_port, self.container_port)):
            cmd += ' -p {host}:{container}'.format(host=self.host_port, container=self.container_port)
        return cmd + ' {image}'.format(image=self.docker_image)

    @property
    def push(self):
        """Returns a Docker 'push' command string."""
        return 'docker push {0}'.format(self.docker_image)

    @property
    def pull(self):
        """Returns a Docker 'pull' command string."""
        return 'docker pull {0}'.format(self.docker_image)

    @property
    def images(self):
        """Retrieve's a Docker 'images' command string."""
        return 'docker images'

    @property
    def containers(self):
        """Return a list of containers on the current machine."""
        return 'docker ps -a -q'

    @property
    def delete_containers(self):
        """Delete all containers on the current machine."""
        return 'docker rm $({0})'.format(self.containers)

    @property
    def delete_images(self):
        """Retrieve a list of all images on the current machine."""
        return 'docker rmi $(docker images -q)'

    @property
    def clean(self):
        """Remove stopped containers and intermediate images from the current machine."""
        return 'docker system prune -f'


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
        cmd = "wget -q https://registry.hub.docker.com/v1/repositories/{0}/{1}/tags ".format(self.cmd.username,
                                                                                             self.cmd.repo)
        cmd += "-O -  | sed -e 's/[][]//g' -e 's/"
        cmd += '"//g'
        cmd += "' -e 's/ //g' | tr '}' '\n'  | awk -F: '{print $3}'"

        return Versions(SystemCommand(cmd).output).sorted

    @property
    def containers(self):
        """Return a list of containers on the current machine."""
        return SystemCommand(self.cmd.containers).output

    def delete_containers(self):
        """Delete all containers on the current machine."""
        if len(self.containers) > 0:
            SystemCommand(self.cmd.delete_containers)

    def delete_images(self):
        """Retrieve a list of all images on the current machine."""
        if len(self.images) > 0:
            return SystemCommand(self.cmd.delete_images)

    def clean(self):
        """Remove stopped containers and intermediate images from the current machine."""
        return SystemCommand(self.cmd.clean)
