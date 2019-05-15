from looptools import Timer

from Dockerizer.docker import Docker, gui
from Dockerizer.config import DOCKER_HISTORY_JSON


@Timer.decorator
def dockerize(params):
    docker = Docker(source=params['source'],
                    repo=params['docker_repo'],
                    tag=params['docker_repo_tag'],
                    username=params['docker_user'],
                    host_port=params['host_port'],
                    container_port=params['container_port'],
                    dockerfile=params['dockerfile'],
                    build_cache=params['actions']['build-cache'])

    # Build docker image
    if params['actions']['build']:
        docker.build()

    # Push docker image to Docker Hub
    if params['actions']['push']:
        docker.push()
    if params['actions']['push-latest']:
        docker.cmd.tag = 'latest'
        docker.push()
        docker.cmd.tag = params['docker_repo_tag']

    # Run docker image locally
    if params['actions']['run']:
        docker.run()

    docker.show_tasks()
    docker.show_commands()
    docker.update_history(DOCKER_HISTORY_JSON, params)
    print(docker.available_commands)
    return docker


def main():
    parameters = []
    another = True
    while another:
        p = gui()
        parameters.append(p)
        if p['another_deploy'] is False:
            break

    # Executing Elastic Beanstalk deployments
    # Return Docker instances for post process parsing
    return [dockerize(params) for params in parameters]


if __name__ == '__main__':
    main()
