# -*- coding: utf-8 -*-
import sqlite3


class InstancedDatabase(object):
    """ Instanced database handler class. """

    def __init__(self, database_file):
        self._connection = sqlite3.connect(database_file, check_same_thread=False)
        self._cursor = self._connection.cursor()

    def execute(self, sql_query, query_args=None):
        """ Execute a sql query on the instanced database. """
        if query_args:
            self._cursor.execute(sql_query, query_args)
        else:
            self._cursor.execute(sql_query)

        return self._cursor

    def commit(self):
        """ Commit any changes of the instanced database. """
        try:
            self._connection.commit()
            return True
        except sqlite3.Error:
            return False

    def close(self):
        """ Close the instanced database connection. """
        self._connection.close()
        return

    def __del__(self):
        """ Close the instanced database connection on destroy. """
        self._connection.close()