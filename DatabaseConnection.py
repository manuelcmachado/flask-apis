"""
    Creation date: 2021-12-04
    Tampa, FL

    @author: Manuel Machado
    @version: 0.0.1

    Description: The purpose of this class is to connect to a Microsoft SQL Server Relational Database.
                 This particular class has two methods which may be used according to the platform being used: Windows
                 or UNIX/LINUX.
"""
import pyodbc


class DataBaseConnection:

    def __init__(self, server, database):
        self.server = server
        self.database = database

    def getTrustedConnection(self) -> pyodbc.Connection:
        """ This method implements a trusted connection to a MSSQL Server Database instance.
            :returns -- A Database connection object
        """

        with pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server={' + self.server + '};'
                            'Database={' + self.database + '};'
                            'Trusted_Connection=Yes;'
                            ) as connection:
            return connection

    def getConnection(self, user_id, user_pwd):
        """ This method implements a non-trusted connection to a MSSQL Server Database instance.
            :param user_id The user id for connecting to the RDBMS
            :param user_pwd he password to login into the RDBMS
            :returns A database connection object
        """

        with pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server={' + self.server + '};'
                            'Database={' + self.database + '};'
                            'UID={' + user_id + '};'
                            'PWD={' + user_pwd + '}'
                            ) as connection:
            return connection
