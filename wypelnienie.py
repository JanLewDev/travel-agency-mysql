"""Modul zawierajacy funkcje wypelniajace baze danych"""

import os
import sys
import argparse
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
from sql import DB_NAME, TABLES, ORDER_TO_DROP

load_dotenv()
parser = argparse.ArgumentParser(description="Wypelnienie bazy danych")
parser.add_argument(
    "--nodrop",
    action="store_true",
    help="Nie usuwaj wszystkich tabel",
    required=False,
)
args = parser.parse_args()


cnx = mysql.connector.connect(
    host="giniewicz.it",
    port=3306,
    user="team02",
    password=os.getenv("CONNECTION_PASSWORD"),
    database="team02",
)


def show_databases(connection) -> list[tuple[str]]:
    """Funkcja wyswietlajaca wszystkie bazy danych"""
    local_cursor = connection.cursor()
    local_cursor.execute("SHOW DATABASES")
    databases = local_cursor.fetchall()
    local_cursor.close()
    return databases


def show_tables(connection) -> list[tuple[str]]:
    """Funkcja wyswietlajaca wszystkie tabele w bazie danych"""
    local_cursor = connection.cursor()
    local_cursor.execute("SHOW TABLES")
    tables = local_cursor.fetchall()
    local_cursor.close()
    return tables


def create_tables(connection) -> None:
    """Funkcja tworzaca tabele w bazie danych"""
    local_cursor = connection.cursor()
    for table_name, table_description in TABLES.items():
        try:
            local_cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print(f"Tabela {table_name} juz istnieje.")
            else:
                print(err.msg)
                sys.exit()
        else:
            print(f"Tabela {table_name} utworzona poprawnie.")
    local_cursor.close()
    connection.commit()


def cleanup(connection) -> None:
    """Funkcja usuwajaca wszystkie tabele z bazy danych"""
    local_cursor = connection.cursor()
    local_cursor.execute("SHOW TABLES")
    local_tables = local_cursor.fetchall()
    local_tables = [table[0] for table in local_tables]
    for table in ORDER_TO_DROP:
        if table in local_tables:
            try:
                local_cursor.execute(f"DROP TABLE {table}")
            except mysql.connector.Error as err:
                print(table, err.msg)
                sys.exit()
    local_cursor.close()
    connection.commit()


assert cnx.is_connected()
assert cnx.charset == "utf8mb4"
assert (DB_NAME,) in show_databases(cnx)

if not args.nodrop:
    cleanup(cnx)
    assert len(show_tables(cnx)) == 0
    create_tables(cnx)
    assert len(show_tables(cnx)) == len(TABLES)

cnx.close()
