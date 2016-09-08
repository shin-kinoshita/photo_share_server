import mysql.connector

class MysqlObject:

    _connector = None
    _cursor = None

    _username = None
    _password = None
    _database = None

    def __init__(self, username='mysql_test', password='Mysql@2016', database=None):
        self._username = username
        self._password = password
        if database != None:
            self._database = database

    def connect(self):
        if self._database != None:
            self._connector = mysql.connector.connect(
                    user=self._username,
                    password=self._password,
                    database=self._database)
        else:
            self._connector = mysql.connector.connect(
                    user=self._username,
                    password=self._password)

        self._cursor = self._connector.cursor()

    def disconnect(self):
        self._cursor.close()
        self._connector.close()

    def create_user(self, username, password, grant_all=False):
        query = "CREATE USER '{}'@'localhost' IDENTIFIED BY '{}'".format(username, password)

        self._cursor.execute(query)
        if grant_all:
            query = "GRANT ALL PRIVILEGES ON *.* TO '{}'@'localhost' WITH GRANT OPTION".format(username)
            self._cursor.execute(query)

        
        self._connector.commit()

    def create_database(self, database_name):
        query = 'CREATE DATABASE {}'.format(database_name)

        self._cursor.execute(query)
        self._connector.commit()

    def create_table(self, database_name, table_name, elements, types):
        query = 'USE {}'.format(database_name)
        self._cursor.execute(query)
        
        query = 'CREATE TABLE {} ('.format(table_name)
        for i in range(len(elements)):
            query += elements[i] + ' ' + types[i] + ','
        query = query[:-1] + ')'

        self._cursor.execute(query)
        self._connector.commit()


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

