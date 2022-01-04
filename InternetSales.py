"""
    Creation date: 2020-04-12 13:43:17
    Tampa, FL

    @author: Manuel Machado
    @version: 0.0.1

    Description: The purpose of this program is to create an API using python's web microservice Flask.
                 This particular API will provide a data set in form of a json and xml file. It ingests the data from
                 a SQL Server Database via stored procedure using an ODBC connection.
"""

import datetime
import decimal
import json
import xmltodict
import pandas as pd

from flask import Flask

import DatabaseConnection as dbc
import configparser


application = Flask(__name__)


# Helper function to handle time and float data types during the json serialization
def dateTimeHandler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return obj.__float__()


def database_connection():
    parser = configparser.ConfigParser()
    parser.read('flaskconfig.conf')
    serverName = parser.get('Database', 'server_name')
    databaseName = parser.get('Database', 'database_name')
    sqlQuery = parser.get('Database', 'sql_query')

    dbConnectionInstance = dbc.DataBaseConnection(server=serverName, database=databaseName)
    return dbConnectionInstance.getTrustedConnection(), sqlQuery


# list of sequence of dictionaries
@application.route('/api/internetsales/listofdicts/json', methods=['GET'])
def internetSalesJson():
    connection, query = database_connection()
    df = pd.read_sql(query, connection)
    connection.close()
    return df.to_json(date_format='iso', indent=2, orient='records')


# dictionary of sequence of dictionaries
@application.route('/api/internetsales/dictofdicts/json', methods=['GET'])
def internetSalesJsonDict():
    connection, query = database_connection()
    cursor = connection.cursor()
    dbData = cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    rowsFromCursor = []

    for row in dbData.fetchall():
        rowsFromCursor.append(dict(zip(columns, row)))

    dictTextEncoded = json.dumps(rowsFromCursor, default=dateTimeHandler, sort_keys=False, indent=2)
    cursor.close()
    connection.close()
    return dictTextEncoded

# to do: write a method to handle an xml endpoint


if __name__ == '__main__':
    application.run(port=8088, host='localhost', debug=True)