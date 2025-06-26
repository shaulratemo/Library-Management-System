import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='jeanette',
    port='3306'
)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE library")
