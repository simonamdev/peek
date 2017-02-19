import os

import sqlite3

from peek.line import Line


class LogStatistics:
    def __init__(self, persist=False):
        self._persistence_mode = persist
        self._db_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'logs.db') if self.persistence_mode else ':memory:'
        self._connection = sqlite3.connect(database=self._db_path)
        self._cursor = self._connection.cursor()
        self.__initialise_database()

    def __initialise_database(self):
        create_table_query = 'CREATE TABLE IF NOT EXISTS `logs` (' \
                             'id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                             'ip        TEXT NOT NULL,' \
                             'timestamp INTEGER NOT NULL,' \
                             'verb      TEXT NOT NULL,' \
                             'path      TEXT NOT NULL,' \
                             'status    INTEGER NOT NULL,' \
                             'size      INTEGER NOT NULL,' \
                             'referrer  TEXT NOT NULL,' \
                             'useragent TEXT NOT NULL' \
                             ');'
        self._cursor.execute(create_table_query)
        self._connection.commit()

    @property
    def persistence_mode(self):
        return self._persistence_mode

    @property
    def lines_stored(self):
        count_query = 'SELECT COUNT(*) FROM `logs`;'
        line_amount = self._cursor.execute(count_query).fetchone()[0]
        return line_amount

    @staticmethod
    def convert_row_to_line(row):
        result = {
            'ip_address': row[1],
            'timestamp':  row[2],
            'verb':       row[3],
            'path':       row[4],
            'status':     row[5],
            'size':       row[6],
            'referrer':   row[7],
            'user_agent': row[8]
        }
        return Line(line_contents=result)

    def get_all_lines(self):
        retrieve_query = 'SELECT * FROM `logs`;'
        result = self._cursor.execute(retrieve_query).fetchall()
        return [self.convert_row_to_line(row=row) for row in result]

    def insert_line(self, line):
        if line is None:
            return
        insert_query = 'INSERT INTO `logs` (' \
                       'ip,' \
                       'timestamp,' \
                       'verb,' \
                       'path,' \
                       'status,' \
                       'size,' \
                       'referrer,' \
                       'useragent)' \
                       'VALUES (?, ?, ?, ?, ?, ?, ?, ?);'
        insert_data = (line.ip_address,
                       line.timestamp,
                       line.verb,
                       line.path,
                       line.status,
                       line.byte_count,
                       line.referrer,
                       line.user_agent)
        self._cursor.execute(insert_query, insert_data)
        self._connection.commit()

    def get_ip_address_occurrences(self):
        return self.__get_number_of_occurrences(field='ip')

    def get_number_of_distinct_ip_addresses(self):
        select_query = 'SELECT COUNT(DISTINCT ip)' \
                       'FROM `logs`;'
        return self._cursor.execute(select_query).fetchall()[0][0]

    def get_number_of_distinct_ip_addresses_in_timespan(self, timespan_start, timespan_end):
        ip_query = 'SELECT COUNT(DISTINCT ip)' \
                   'FROM `logs`' \
                   'WHERE timestamp >= ? AND timestamp <= ?'
        ip_data = (timespan_start, timespan_end)
        query_amount = self._cursor.execute(ip_query, ip_data).fetchone()[0]
        return round(query_amount / 60, 2)

    def get_verb_occurrences(self):
        return self.__get_number_of_occurrences(field='verb')

    def get_path_occurrences(self):
        return self.__get_number_of_occurrences(field='path')

    def get_status_occurrences(self):
        return self.__get_number_of_occurrences(field='status')

    def get_average_byte_count(self):
        average_query = 'SELECT AVG(size) FROM `logs`'
        return self._cursor.execute(average_query).fetchone()[0]

    def get_total_byte_count(self):
        total_query = 'SELECT SUM(size) FROM `logs`'
        return self._cursor.execute(total_query).fetchone()[0]

    def get_referrer_occurrences(self):
        return self.__get_number_of_occurrences(field='referrer')

    def get_user_agent_occurrences(self):
        return self.__get_number_of_occurrences(field='useragent')

    def get_requests_per_second_in_timespan(self, timespan_start, timespan_end):
        rps_query = 'SELECT COUNT(*)' \
                    'FROM `logs`' \
                    'WHERE timestamp >= ? AND timestamp <= ?'
        rps_data = (timespan_start, timespan_end)
        query_amount = self._cursor.execute(rps_query, rps_data).fetchone()[0]
        return round(query_amount / 60, 3)

    def __get_number_of_occurrences(self, field):
        select_query = 'SELECT {}, COUNT({})' \
                       'FROM `logs`' \
                       'GROUP BY {};'.format(field, field, field)
        occurrences = {}
        for row in self._cursor.execute(select_query).fetchmany(size=5):
            occurrences[row[0]] = row[1]
        return occurrences
