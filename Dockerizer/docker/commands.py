import os


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
        i = ''
        i += '{user}/' if self.username else ''
        i += '{repo}'
        if self.tag:
            i += ':{tag}'
        return i.format(user=self.username, repo=self.repo, tag=self.tag)

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
    def image_tags(self):
        """Retrieve a list of available docker image tags."""
        cmd = "wget -q https://registry.hub.docker.com/v1/repositories/{0}/{1}/tags ".format(self.username, self.repo)
        cmd += "-O -  | sed -e 's/[][]//g' -e 's/"
        cmd += '"//g'
        cmd += "' -e 's/ //g' | tr '}' '\n'  | awk -F: '{print $3}'"
        return cmd

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
        """Delete all images on the current machine."""
        return 'docker rmi $(docker images -q)'

    @property
    def delete_volumes(self):
        """Delete all volumes on the current machine."""
        return 'docker system prune --volumes -f'

    @property
    def clean(self):
        """Remove stopped containers and intermediate images from the current machine."""
        return 'docker system prune -f'
