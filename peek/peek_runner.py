import os
import time

from tabulate import tabulate

from peek.line import Line
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

    def __init__(self, file_path, persist=False):
        self._log_file = LogFile(file_path=file_path)
        self._original_line_count = self._log_file.length
        self._lines_parsed = 0
        self._log_statistics = LogStatistics(persist=persist)

    def parse_logs(self):
        print('Peeking into nginx logs')
        for incoming_connection_log in watch_file(file_path=self._log_file.file_path):
            self._lines_parsed += 1
            current_line = LineParser.parse_line(line=incoming_connection_log)
            self._log_statistics.insert_line(line=current_line)
            self.report_statistics()

    def report_statistics(self):
        current_time = int(time.time())
        one_minute_ago = int(time.time()) - 60
        rps = self._log_statistics.get_requests_per_second_in_timespan(
            timespan_start=one_minute_ago,
            timespan_end=current_time)
        get_count = self._log_statistics.get_verb_occurrences()['GET']
        total_bytes_sent = self._log_statistics.get_total_byte_count()
        average_bytes_sent = self._log_statistics.get_average_byte_count()
        distinct_ip_count = self._log_statistics.get_number_of_distinct_ip_addresses()
        distinct_ip_count_in_timespan = self._log_statistics.get_number_of_distinct_ip_addresses_in_timespan(
            timespan_start=one_minute_ago,
            timespan_end=current_time)
        self.clear_screen()
        stats = [
            ['Requests per Second', rps],
            ['GET count', get_count],
            ['Total Bytes sent', total_bytes_sent],
            ['Average Bytes sent per request', average_bytes_sent],
            ['Unique IP Addresses', distinct_ip_count],
            ['Unique IP Addresses (last minute)', distinct_ip_count_in_timespan]
        ]
        print('Nginx Statistics')
        print(tabulate(tabular_data=stats, tablefmt='grid', numalign='right'))

    @staticmethod
    def clear_screen():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
