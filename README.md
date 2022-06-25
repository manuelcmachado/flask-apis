# flask-apis
API Development with Flask

The start_internet_sales.py file, is the Flask Application's starting point. By running it, a server instance is launched, and you can consume each endpoint's content. If you want to test the app before launching the server, run **run_internet_sales_inplace.py** file and you'll get what an endpoint would deliver. 

## Content of this Repository:
- CurrentInternetSales.sql: Stored Procedure used to pull out data from a SQL SERVER database, which in turn will be served by an endpoint.
- InternetSalesResponseViaPostman.json: The resulting json data consumed from one of the APIs.
- database_connection.py: Python class for connecting to a SQL Server database using ODBC connection.
- hello_world.py: Running this file, the classic "Hello World" message is rendered in a Web Browser. This a very basic Flask app.
- run_internet_sales_inplace.py: If you want to test the app before launching the server, run this.
- start_internet_sales.py: This is the app's starting point.  

## Running the Flask app

As mentioned above, run the script start_internet_sales.py and you have your Flask app up and running as depicted below:


