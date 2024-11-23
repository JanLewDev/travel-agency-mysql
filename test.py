"""Modol testowy do łączenia się z bazą danych."""

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

cnx = mysql.connector.connect(
    host="giniewicz.it",
    port=3306,
    user="student",
    password=os.getenv("CONNECTION_PASSWORD"),
    database="sakila",
)

cursor = cnx.cursor()
cursor.execute("SELECT * FROM actor")
for row in cursor:
    print(row)

cursor.close()
cnx.close()
