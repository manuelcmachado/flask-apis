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
import collections
import xmltodict

import DatabaseConnection as dbc

dbData = dbc.DataBaseConnection()


# helper function. Handles date, and float data types.
def dateTimeHandler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return obj.__float__()
    #raise TypeError("Unknown type")


# returns the cursor content as a list of dictionaries sequences.
def getInternetSalesArrays():
    cursor = dbData.getCursorFromDB()
    rowsFromCursor = []
    for row in cursor.fetchall():
        columns = (row.DateCreated, row.ProductLine, row.ModelName, row.EnglishProductName, row.Color,
                   row.OrderQuantity, row.TotalProductCost, row.ListPrice, row.UnitPrice, row.SalesAmount, row.TaxAmt,
                   row.OrderDate, row.ShipDate, row.SalesOrderNumber, row.CurrencyKey, row.CurrencyName,
                   row.SalesTerritoryKey, row.SalesTerritoryCountry, row.SalesTerritoryRegion, row.SalesTerritoryGroup
                   )
        rowsFromCursor.append(columns)
    dictTextEncoded = json.dumps(rowsFromCursor, default=dateTimeHandler, sort_keys=False, indent=2)
    dbData.closeConnection()
    return dictTextEncoded


def getInternetSalesTuple():
    cursor = dbData.getCursorFromDB()
    columns = [column[0] for column in cursor.description]
    rowsFromCursor = []
    for row in cursor.fetchall():
        rowsFromCursor.append(row)
    tupleTextEncoded = json.dumps(rowsFromCursor, default=dateTimeHandler, sort_keys=False, indent=2)
    return tupleTextEncoded


def getInternetSalesZipDict():
    resultset = dbData.getCursorFromDB()
    columns = [column[0] for column in resultset.description]
    rowsFromCursor = []
    internetSales = {}
    for row in resultset.fetchall():
        rowsFromCursor.append(dict(zip(columns, row)))

    for value in rowsFromCursor:
        internetSales.setdefault('InternetSales', []).append(value)

    dictTextEncoded = json.dumps(internetSales, default=dateTimeHandler, sort_keys=False, indent=2)
    resultset.close()
    return dictTextEncoded


def getInternetSalesDictionary():
    cursor = dbData.getCursorFromDB()
    rowsFromCursor = []
    for row in cursor.fetchall():
        rowsFromCursorDict = collections.OrderedDict()
        rowsFromCursorDict['DateCreated'] = row.DateCreated
        rowsFromCursorDict['ProductLine'] = row.ProductLine
        rowsFromCursorDict['ModelName'] = row.ModelName
        rowsFromCursorDict['EnglishProductName'] = row.EnglishProductName
        rowsFromCursorDict['Color'] = row.Color
        rowsFromCursorDict['OrderQuantity'] = row.OrderQuantity
        rowsFromCursorDict['TotalProductCost'] = row.TotalProductCost
        rowsFromCursorDict['ListPrice'] = row.ListPrice
        rowsFromCursorDict['UnitPrice'] = row.UnitPrice
        rowsFromCursorDict['SalesAmount'] = row.SalesAmount
        rowsFromCursorDict['TaxAmt'] = row.TaxAmt
        rowsFromCursorDict['OrderDate'] = row.OrderDate
        rowsFromCursorDict['ShipDate'] = row.ShipDate
        rowsFromCursorDict['SalesOrderNumber'] = row.SalesOrderNumber
        rowsFromCursorDict['CurrencyKey'] = row.CurrencyKey
        rowsFromCursorDict['CurrencyName'] = row.CurrencyName
        rowsFromCursorDict['SalesTerritoryKey'] = row.SalesTerritoryKey
        rowsFromCursorDict['SalesTerritoryCountry'] = row.SalesTerritoryCountry
        rowsFromCursorDict['SalesTerritoryRegion'] = row.SalesTerritoryRegion
        rowsFromCursorDict['SalesTerritoryGroup'] = row.SalesTerritoryGroup
        rowsFromCursor.append(rowsFromCursorDict)
    dictTextEncoded = json.dumps(rowsFromCursor, default=dateTimeHandler, sort_keys=False, indent=2)
    dbData.closeConnection()
    return dictTextEncoded

#TODO: This function is not working. I need to fix it
def getInternetSalesXml():
    cursor = dbData.getCursorFromDB()
    columns = [column[0] for column in cursor.description]
    xmlData = ['<InternetSale>']
    for row in cursor.fetchall():
        xmlData.append(list(zip(columns, row)))
    xmlData.append('</InternetSale>')
    return xmlData



#jsonData = getInternetSalesArrays()
#print(jsonData)

#This was the last tested function

jsonData = getInternetSalesZipDict()
print(jsonData)

param = {'root': jsonData}
xmlData = xmltodict.unparse(param, output=None, encoding='utf-8')
print(xmlData)

#jsonData = getInternetSalesDictionary()
#print(jsonData)


#getInternetSalesDictComprehension()


# tupleData = getInternetSalesTuple()
# print(tupleData)

xml = getInternetSalesXml()
print(xml)


# We need to define the root and elements to have the xml
# xmlData = xmltodict.unparse(jsonData, full_document=False)
# print(xmlData)

# print data in a XML format
# dictText = getInternetSalesDictionary()
# dictTextEncoded = xmltodict.unparse(dictText)
# print(dictTextEncoded)
