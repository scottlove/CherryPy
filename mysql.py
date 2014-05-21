

import pyodbc

conn = pyodbc.connect('DRIVER={MySQL ODBC 5.1 Driver};SERVER=localhost;DATABASE=messagestore;UID=test;PWD=test')
cursor = conn.cursor()
cursor.execute("Select * from words")
row = cursor.fetchone()
if row:
    print (row)


