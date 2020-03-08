import os
import configparser


class Config:
    def __init__(self):
        self.filename = "config.ini"
        self.check_for_config()

    def create_config(self):
        lines_to_write = [
            "[MacroMaker]", "pause=home"
        ]

        with open("config.ini", "w") as f:
            f.write("\n".join(lines_to_write))
            f.close()

    def check_for_config(self):
        checker = os.path.isfile(self.filename)
        if not checker:
            self.create_config()

    def get(self):
        config = configparser.ConfigParser()
        config.read(self.filename)
        return config
