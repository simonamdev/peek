import os


class LogFile:
    def __init__(self, file_path):
        self._file_path = file_path
        self.__validate_file()

    def __validate_file(self):
        if not isinstance(self._file_path, str):
            raise TypeError('Incorrect file path type')
        if not os.path.isfile(self._file_path):
            raise FileNotFoundError('File does not exist at path: {}'.format(self._file_path))

    @property
    def file_path(self):
        return self._file_path

    @property
    def length(self):
        length = 0
        with open(self._file_path) as config_file:
            length = sum(1 for line in config_file)
        return length
