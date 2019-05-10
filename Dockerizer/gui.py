import PySimpleGUI as sg
from Deployer.utils import most_recent_history
from Deployer.aws.config import DOCKER_HISTORY_JSON, HOST_PORT, CONTAINER_PORT


LABEL_COL_WIDTH = 20
INPUT_COL_WIDTH = 50
HEADER_FONT_SIZE = 30
BODY_FONT_SIZE = 20
DEFAULT_FONT = 'Any {0}'.format(HEADER_FONT_SIZE)


def gui():
    """GUI form for choosing packages to upload to DeployPyPi."""
    # Get most recent deployment data
    most_recent = most_recent_history(DOCKER_HISTORY_JSON)
    sg.SetOptions(text_justification='left')

    # Set parameter values
    most_recent['source'] = most_recent.get('source', '')
    most_recent['docker_user'] = most_recent.get('docker_user', '')
    most_recent['docker_repo'] = most_recent.get('docker_repo', '')
    most_recent['docker_repo_tag'] = most_recent.get('docker_repo_tag', '')

    # Local directory settings
    directory_settings = [
        # Source
        [sg.FolderBrowse('Source', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent['source'], size=(INPUT_COL_WIDTH, 1), key='source',
               font='Any {0}'.format(16))]
    ]

    # DockerHub settings
    docker_hub_settings = [
        # Username
        [sg.Text('Username', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('docker_user', ''), size=(INPUT_COL_WIDTH, 1), key='docker_user')],

        # Repo
        [sg.Text('Repository', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('docker_repo', most_recent.get('aws_environment-name', '')),
               size=(INPUT_COL_WIDTH, 1), key='docker_repo')],

        # Tag
        [sg.Text('Tag', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('docker_repo_tag', ''), size=(INPUT_COL_WIDTH, 1),
               key='docker_repo_tag')],

        # Host Port
        [sg.Text('Host Port', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('host_port', HOST_PORT), size=(INPUT_COL_WIDTH, 1),
               key='host_port')],

        # Container Port
        [sg.Text('Container Port', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('container_port', CONTAINER_PORT), size=(INPUT_COL_WIDTH, 1),
               key='container_port')],

        # Dockerfile
        [sg.Text('Dockerfile path (relative to source)', size=(LABEL_COL_WIDTH, 1),
                 font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('dockerfile', 'Dockerfile'), size=(INPUT_COL_WIDTH, 1),
               key='dockerfile')],

        # Another deployment?
        [sg.Checkbox('Deploy another environment?', size=(LABEL_COL_WIDTH * 2, 2), default=False,
                     key='another_deploy')]
    ]

    # Deployable project options
    commands = [[sg.Checkbox(cmd.capitalize(), size=(LABEL_COL_WIDTH, 1),
                             default=False if not cmd.startswith('build') else True, key='action_' + cmd)
                 for cmd in ('build', 'push', 'run', 'push-latest')],
                [sg.Checkbox('build-cache'.capitalize(), size=(LABEL_COL_WIDTH, 1),
                             default=True, key='action_build-cache')]]

    # Create form layout
    layout = [
        [sg.Frame('Directory settings', directory_settings, title_color='green', font=DEFAULT_FONT)],
        [sg.Frame('DockerHub settings', docker_hub_settings, title_color='blue', font=DEFAULT_FONT)],
        [sg.Frame('Docker commands', commands, title_color='blue', font=DEFAULT_FONT)],
        [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('Docker Hub Deployment Control', font=("Helvetica", HEADER_FONT_SIZE))
    window.Layout(layout)

    while True:
        button, values = window.ReadNonBlocking()
        if button is 'Submit':
            # Pack keys with 'action' prefix into a new 'actions' key
            values['actions'] = {key.replace('action_', ''): values.pop(key) for key in list(values.keys())
                                 if key.startswith('action_')}

            return values
        elif button is 'Cancel':
            exit()
