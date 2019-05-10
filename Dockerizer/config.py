import os

from databasetools import JSON

_HISTORY_JSON_ROOT = os.path.join(os.path.expanduser('~'), '.Dockerizer')
DOCKER_HISTORY_JSON = os.path.join(_HISTORY_JSON_ROOT, 'docker_history.json')
MORNING_PULL_JSON = os.path.join(_HISTORY_JSON_ROOT, 'morning_pull.json')

HOST_PORT, CONTAINER_PORT = 80, 80


def init_json_store(root=_HISTORY_JSON_ROOT, json=DOCKER_HISTORY_JSON, key='history'):
    # Make root if it doesn't exist
    if not os.path.exists(root):
        os.mkdir(root)

    # Make json file if it doesn't exist
    if not os.path.isfile(json):
        JSON(json).write({key: []})


# Initialize history
init_json_store()

# Initialize morning pull
init_json_store(json=MORNING_PULL_JSON, key='images')
