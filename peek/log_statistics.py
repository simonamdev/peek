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
        pass
