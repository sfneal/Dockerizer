import os

from databasetools import JSON

_HISTORY_JSON_ROOT = os.path.join(os.path.expanduser('~'), '.Dockerizer')
DOCKER_HISTORY_JSON = os.path.join(_HISTORY_JSON_ROOT, 'docker_history.json')

HOST_PORT, CONTAINER_PORT = 80, 80


def init_history(root=_HISTORY_JSON_ROOT, json=DOCKER_HISTORY_JSON):
    # Make root if it doesn't exist
    if not os.path.exists(root):
        os.mkdir(root)

    # Make json file if it doesn't exist
    if not os.path.isfile(json):
        JSON(json).write({'history': []})


# Initialize history
init_history()
