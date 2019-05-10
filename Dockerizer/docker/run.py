import os
import shutil

from RuntimeWatch import TaskTracker
from databasetools import JSON


class Dockerrun(TaskTracker):
    def __init__(self, source, docker_repo, docker_user, container_port=80, docker_repo_tag='latest',
                 remote_source_ext='-remote'):
        """

        :param docker_repo:
        :param docker_user:
        :param remote_source_ext: Extension given to the directory containing a Dockerrun file
        """
        self.source = source
        self.docker_user = docker_user
        self.docker_repo = docker_repo
        self.docker_repo_tag = docker_repo_tag
        self.container_port = container_port

        self._remote_source_ext = remote_source_ext

    @property
    def remote_source(self):
        """Path to source directory with '-remote' extension."""
        return self.source + self._remote_source_ext

    @property
    def path(self):
        """Path to Dockerrun file."""
        return os.path.join(self.remote_source, 'Dockerrun.aws.json')

    @property
    def data(self):
        """Default values for a Dockerrun.aws.json file."""
        return {"AWSEBDockerrunVersion": "1",
                "Image": {
                    "Name": "{user}/{app}:{tag}".format(user=self.docker_user, app=self.docker_repo,
                                                        tag=self.docker_repo_tag),
                    "Update": "true"},
                "Ports": [{"ContainerPort": self.container_port}]}

    def create(self):
        """Create a Dockerrun.aws.json file in the default directory with default data."""
        if not os.path.exists(os.path.dirname(os.path.join(self.path))):
            os.mkdir(os.path.dirname(os.path.join(self.path)))
        JSON(os.path.join(self.path)).write(self.data, sort_keys=False, indent=2)
        self.add_task('Make Dockerrun.aws.json file with default deployment config')

    def destroy(self):
        """Delete a Dockerrun.aws.json file and its directory as it is dynamically built on each deployment."""
        if os.path.exists(os.path.dirname(os.path.join(self.path))):
            shutil.rmtree(os.path.dirname(os.path.join(self.path)))
            return True
        else:
            return False
