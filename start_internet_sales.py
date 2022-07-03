"""
    Creation date: 2022-06-11 13:43:17
    Tampa, FL

    @author: Manuel Machado
    @version: 0.0.2

    Description: The purpose of this program is to create an API using python's web microservice Flask.
                 The endpoints in this particular API serializes data to json file format. It ingests data from
                 a SQL Server Database via, stored procedure using an ODBC connection.
"""

from datetime import datetime, date
from decimal import Decimal
import json
import pandas as pd

from flask import Flask

import database_connection as dbc
import configparser

import platform


application = Flask(__name__)


# Helper function to handle time and float data types during the json serialization
def date_time_handler(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return obj.__float__()
    raise TypeError(f'Type {obj} no serializable')


def database_untrusted_connection():
    parser = configparser.ConfigParser()
    parser.read('flaskconfig.conf')
    serverName = parser.get('Database', 'server_name')
    databaseName = parser.get('Database', 'database_name')
    sqlQuery = parser.get('Database', 'sql_query')
    pwd = parser.get('Database', 'user_pwd')
    user = parser.get('Database', 'user_id')

    dbConnectionInstance = dbc.DataBaseConnection(server=serverName, database=databaseName)
    return dbConnectionInstance.get_connection(user_id=user, user_pwd=pwd), sqlQuery


def database_trusted_connection():
    parser = configparser.ConfigParser()
    parser.read('flaskconfig.conf')
    serverName = parser.get('Database', 'server_name')
    databaseName = parser.get('Database', 'database_name')
    sqlQuery = parser.get('Database', 'sql_query')

    dbConnectionInstance = dbc.DataBaseConnection(server=serverName, database=databaseName)
    return dbConnectionInstance.get_trusted_connection(), sqlQuery


@application.route('/api/internetsales/pandas/json', methods=['GET'])
def internet_sales_pandas():
    """ This method serializes an object to a JSON formatted string using the Pandas library.
        :returns -- A serialized object to a json formatted string
        """
    if platform.system() == 'Windows':
        connection, query = database_trusted_connection()
        df = pd.read_sql(query, connection)
        connection.close()
        return df.to_json(date_format='iso', indent=2, orient='records')
    elif platform.system() == 'Linux':
        connection, query = database_untrusted_connection()
        df = pd.read_sql(query, connection)
        connection.close()
        return df.to_json(date_format='iso', indent=2, orient='records')


@application.route('/api/internetsales/dumps/json', methods=['GET'])
def internet_sales_dumps():
    """ This method serializes an object to a JSON formatted string using the Python native json module.
        :returns -- A serialized object to a json formatted string
    """
    if platform.system() == 'Windows':
        connection, query = database_trusted_connection()
        cursor = connection.cursor()
        dbData = cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rowsFromCursor = []
    elif platform.system() == 'Linux':
        connection, query = database_untrusted_connection()
        cursor = connection.cursor()
        dbData = cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rowsFromCursor = []

    for row in dbData.fetchall():
        rowsFromCursor.append(dict(zip(columns, row)))

    dictTextEncoded = json.dumps(rowsFromCursor, default=date_time_handler, sort_keys=False, indent=2)
    cursor.close()
    connection.close()
    return dictTextEncoded


if __name__ == '__main__':
    application.run(port=8088, host='localhost', debug=True)