import pyodbc
import traceback


class MsSql:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        try:
            self.db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
                                     ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        except:
            traceback.print_exc()
            raise Exception("SQL Connection Error.")

    def cursor(self):
        return self.db.cursor()

    def close(self):
        try:
            self.db.close()
        except:
            pass
