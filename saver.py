import json
import random
import time
from datetime import datetime
from namespaces import *


class DataSaver:
    def __init__(self, app):
        self.app = app
        self.__default_settings = {
            "x": 1024,
            "y": 640,
            # dialog table
            "x_dt": 640,
            "y_dt": 480,
            "last_img": -1,
            "full_screen": 0,
        }
        try:
            with open(PATH_TO_PRESETS + FILENAME_PRESETS, "r") as file:
                self.settings = json.load(file)
                for key, value in self.__default_settings.items():
                    if key not in self.settings:
                        self.settings[key] = value
        except (json.JSONDecodeError, FileNotFoundError):
            self.settings = self.__default_settings
        print(self.settings)

    def save_window_size(self, event):
        new_size = event.size()
        self.settings["x"] = new_size.width()
        self.settings["y"] = new_size.height()
        # print(self.actual_width, self.actual_height)

    def global_save(self):
        self.settings["last_time"] = int(time.time())
        with open(PATH_TO_PRESETS + FILENAME_PRESETS, "w") as file:
            json.dump(self.settings, file, indent=4)

    # no fucking need
    def data_access(self):
        return self.settings


# No use
import string


class SessionEngine:
    def __init__(self, app):
        self.app = app
        self.current_session_name = self.generate_random_string()
        while self.current_session_name in os.listdir(PATH_TO_SESSIONS):
            self.current_session_name = self.generate_random_string()
        self.current_session_file = open(
            PATH_TO_SESSIONS + self.current_session_name, "w"
        )

    def generate_random_string(self, length=10):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(length))
