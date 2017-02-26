import os
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
        self._log_file_size = 0
        self._previous_log_file_size = 0
        self._log_statistics = LogStatistics(persist=True)

    def parse_logs(self):
        print('Peeking into nginx logs')
        while True:
            # Reset  the log file watcher when the new log size is smaller than the last size
            log_file_watcher = watch_file(file_path=self._log_file.file_path)
            self._previous_log_file_size = 0
            for incoming_connection_log in log_file_watcher:
                self._lines_parsed += 1
                log_file_size_mb = os.path.getsize(self._log_file.file_path) / (1024 * 1024)
                if log_file_size_mb < self._previous_log_file_size:
                    self._previous_log_file_size = 0
                    break
                current_line = LineParser.parse_line(line=incoming_connection_log)
                self._log_statistics.insert_line(line=current_line)
                print('Lines Parsed: {} Log Size: {} MB'.format(
                    self._lines_parsed,
                    round(log_file_size_mb, 2)), end='\r')
                self._previous_log_file_size = log_file_size_mb

