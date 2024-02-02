from flask import Flask
import os


class Application:
    current_folder_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, application_name=__name__) -> None:
        self.flask = Flask(application_name, template_folder='../src', static_folder='../src')
        self._config = None
        self.connection = None