"""
    Creation date: 2020-04-14 21:52
    Tampa, FL

    @author: Manuel Machado
    @version: 0.0.1

    Description: The purpose of this program is to test how we may ingest data from a MS SQL Server Database
    via stored procedure using an ODBC connection. This implementation uses a module do handle the connection
    logic.

"""

# I should rather do this an accessible module that handles the same data but it's not an API


import datetime
import decimal
import json
import pandas as pd

import DatabaseConnection as dbc

import configparser


# helper function. Handles date, and float data types.
def dateTimeHandler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def getInternetSalesPandas(connection, query):
    df = pd.read_sql(query, connection)
    return df.to_json(date_format='iso', indent=2, orient='records')


def getInternetSalesZipDict(connection, query):
    cursor = connection.cursor()
    dbData = cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    rowsFromCursor = []

    for row in dbData.fetchall():
        rowsFromCursor.append(dict(zip(columns, row)))

    dictTextEncoded = json.dumps(rowsFromCursor, default=dateTimeHandler, sort_keys=False, indent=2)
    cursor.close()
    return dictTextEncoded


# for testing on a non trusted connection, implement a config file where the program can read the credentials
if __name__ == '__main__':

    parser = configparser.ConfigParser()
    parser.read('flaskconfig.conf')
    serverName = parser.get('Database', 'server_name')
    databaseName = parser.get('Database', 'database_name')
    sqlQuery = parser.get('Database', 'sql_query')

    dbConnectionInstance = dbc.DataBaseConnection(server=serverName, database=databaseName)
    dbConnection = dbConnectionInstance.getTrustedConnection()

    jsonData = getInternetSalesPandas(dbConnection, sqlQuery)
    print(jsonData)
    dbConnection.close()

    #jsonData = getInternetSalesZipDict(dbConnection, sqlQuery)
    #print(jsonData)
    #dbConnection.close()
