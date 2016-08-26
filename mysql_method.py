import mysql.connector

class MysqlObject:

    _connector = None
    _cursor = None

    _username = ""
    _password = ""
    _database = ""

    def __init__(self, username, password, database):
        self._username = username
        self._password = password
        self._database = database

    def connect(self):
        self._connector = mysql.connector.connect(
                user=self._username,
                password=self._password,
                database=self._database)
        self._cursor = self._connector.cursor()

    def disconnect(self):
        self._cursor.close()
        self._connector.close()

    def insert_into(self, table_name, table, values):
        query = "INSERT INTO {}{} VALUES{}".format(table_name, table, values)

        self._cursor.execute(query)
        self._connector.commit()

    def select(self, column, table, where=None):
        if where == None:
            query = "SELECT {} FROM {}".format(column, table)
            count = self.table_row_count(table)
        else:
            query = "SELECT {} FROM {} WHERE {}".format(column, table, where)
            count = self.table_row_count(table, where)

        self._cursor.execute(query)

        return self._cursor, count

    def update(self, table, column, value, where=None):
        if where == None:
            query = "UPDATE {} SET {} = {}".format(table, column, value)
        else:
            query = "UPDATE {} SET {} = {} WHERE {}".format(table, column, value, where)
        self._cursor.execute(query)
        self._connector.commit()

    def table_row_count(self, table, where=None):
        if where == None:
            query = "SELECT COUNT(*) FROM {}".format(table)
        else:
            query = "SELECT COUNT(*) FROM {} WHERE {}".format(table, where)

        self._cursor.execute(query)

        return self._cursor.next()[0]

