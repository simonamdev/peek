import os


class ConfigurationFile:
    def __init__(self, file_path):
        self._file_path = file_path
        self.__validate_file()

    def __validate_file(self):
        if not os.path.isfile(self._file_path):
            raise FileNotFoundError

    @property
    def length(self):
        length = 0
        with open(self._file_path) as config_file:
            length = sum(1 for line in config_file)
        return length
