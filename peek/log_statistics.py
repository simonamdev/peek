import os

import sqlite3


class LogStatistics:
    def __init__(self, persist=False):
        self._persistence_mode = persist
        self._db_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'logs.db')
        self._connection = sqlite3.connect(database=self._db_path)
        self._cursor = self._connection.cursor()
        self.__initialise_database()

    def __initialise_database(self):
        create_table_query = 'CREATE TABLE IF NOT EXISTS `logs` (' \
                             'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                             'ip TEXT NOT NULL,' \
                             'timestamp INTEGER NOT NULL,' \
                             'verb TEXT NOT NULL,' \
                             'path TEXT NOT NULL,' \
                             'status INTEGER NOT NULL,' \
                             'size INTEGER NOT NULL,' \
                             'referrer TEXT NOT NULL,' \
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

    def get_lines(self):
        pass

    def insert_line(self, line):
        pass
