import datetime
import os
import time

from tabulate import tabulate

from peek.log_statistics import LogStatistics


class PeekViewer:
    def __init__(self, log_file_path, db_path, refresh_rate=1):
        self._log_file_path = log_file_path
        self._db_path = db_path
        self._refresh_rate = refresh_rate
        self._log_statistics = LogStatistics(persist=True)

    def run(self):
        print('Viewing nginx log statistics')
        while True:
            self.clear_screen()
            self.report_statistics()
            time.sleep(self._refresh_rate)

    def report_statistics(self):
        current_time = int(time.time())
        one_minute_ago = int(time.time()) - 60
        rps = self._log_statistics.get_requests_per_second_in_timespan(
            timespan_start=one_minute_ago,
            timespan_end=current_time)
        get_count = self._log_statistics.get_verb_occurrences()['GET']
        average_bytes_sent = self._log_statistics.get_average_byte_count()
        distinct_ip_count = self._log_statistics.get_number_of_distinct_ip_addresses()
        distinct_ip_count_in_timespan = self._log_statistics.get_number_of_distinct_ip_addresses_in_timespan(
            timespan_start=one_minute_ago,
            timespan_end=current_time)
        stats = [
            ['Requests per Second', rps],
            ['GET count', get_count],
            self._get_formatted_byte_row(self._log_statistics.get_total_byte_count(), 'Total {} Sent', rounding=2),
            ['Average Bytes sent per request', round(average_bytes_sent, 2)],
            self._get_access_log_size_row(),
            self._get_db_size_row(),
            ['Total Unique IP Addresses', distinct_ip_count],
            ['Unique IP Addresses (last minute)', distinct_ip_count_in_timespan],
            self._get_last_checked_time_row()
        ]
        print('Nginx Statistics')
        print(tabulate(tabular_data=stats, tablefmt='grid', numalign='right'))

    @staticmethod
    def _get_formatted_byte_row(byte_count, byte_row_string, rounding=0):
        byte_string = byte_row_string.format('Bytes')
        if byte_count > 1000:
            byte_count /= 1000
            byte_string = byte_row_string.format('Kilobytes')
        if byte_count > 1000:
            byte_count /= 1000
            byte_string = byte_row_string.format('Megabytes')
        if byte_count > 1000:
            byte_count /= 1000
            byte_string = byte_row_string.format('Gigabytes')
        return [byte_string, round(byte_count, rounding)]

    @staticmethod
    def _get_last_checked_time_row():
        return ['Last check timestamp', datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')]

    def _get_access_log_size_row(self):
        access_log_size = os.path.getsize(self._log_file_path)
        return self._get_formatted_byte_row(access_log_size, 'Access Log size in {}', rounding=1)

    def _get_db_size_row(self):
        db_size = 0
        if not self._log_statistics.db_path == ':memory:':
            db_size = os.path.getsize(self._log_statistics.db_path)
        return self._get_formatted_byte_row(db_size, 'Database size in {}', rounding=1)

    @staticmethod
    def clear_screen():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
