"""Modol testowy do łączenia się z bazą danych."""

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

cnx = mysql.connector.connect(
    host="giniewicz.it",
    port=3306,
    user="team02",
    password=os.getenv("CONNECTION_PASSWORD"),
    database="team02",
)

cursor = cnx.cursor()
# show all tables
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print(tables)

cursor.close()
cnx.close()
