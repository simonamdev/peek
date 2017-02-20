import time

from peek.line_parser import LineParser
from peek.log_file import LogFile
from peek.log_statistics import LogStatistics


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
    version = '0.1'

    def __init__(self, file_path):
        self._log_file = LogFile(file_path=file_path)
        self._original_line_count = self._log_file.length
        self._lines_parsed = 0
        self._log_statistics = LogStatistics(persist=True)

    def parse_logs(self):
        print('Peeking into nginx logs')
        for incoming_connection_log in watch_file(file_path=self._log_file.file_path):
            self._lines_parsed += 1
            current_line = LineParser.parse_line(line=incoming_connection_log)
            self._log_statistics.insert_line(line=current_line)
