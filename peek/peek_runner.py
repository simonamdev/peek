import time

from peek.log_file import LogFile


def watch_file(file_path, delay=0.1):
    with open(file_path, 'r') as log_file:
        # Go to the end of the file
        log_file.seek(0, 2)
        while True:
            line = log_file.readline()
            if line and not line == '\n':
                yield line
            time.sleep(delay)


class PeekRunner:
    def __init__(self, file_path):
        self._log_file = LogFile(file_path=file_path)
        self._original_line_count = self._log_file.length
        self._lines_parsed = 0

    def parse_logs(self):
        for incoming_connection in watch_file(file_path=self._log_file.file_path):
            self._lines_parsed += 1
            print('[{}] - {}'.format(self._lines_parsed, incoming_connection))
