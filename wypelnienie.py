"""Modul zawierajacy funkcje wypelniajace baze danych"""

import os
import sys
import argparse
from random import randint, random
from datetime import datetime
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
from sql import DB_NAME, TABLES, ORDER_TO_CREATE, ORDER_TO_DROP
from do_wypelnienia import (
    LICZBA_KLIENTOW,
    PRACOWNICY,
    STANOWISKA,
)

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

data_paths = {
    "naz_zenskie": "dane_statystyczne/nazwiska_zenskie.csv",
    "naz_meskie": "dane_statystyczne/nazwiska_meskie.csv",
    "imiona": "dane_statystyczne/Imiona_nadane_dzieciom_w_Polsce_w_I_polowie_2024.csv",
}


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
    for table_name in ORDER_TO_CREATE:
        table_description = TABLES[table_name]
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


def dropall(connection) -> None:
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


def emptyall(connection) -> None:
    """Funkcja usuwajaca wszystkie rekordy z tabeli"""
    local_cursor = connection.cursor()
    for table in ORDER_TO_DROP:
        try:
            local_cursor.execute(f"DELETE FROM {table}")
        except mysql.connector.Error as err:
            print(table, err.msg)
            sys.exit()
    local_cursor.close()
    connection.commit()


assert cnx.is_connected()
assert cnx.charset == "utf8mb4"
assert (DB_NAME,) in show_databases(cnx)

if not args.nodrop:
    dropall(cnx)
    assert len(show_tables(cnx)) == 0
    create_tables(cnx)
    assert len(show_tables(cnx)) == len(TABLES) == 21


def save_top_1000_surnames():
    """Funkcja uzyta do odfiltrowania 1000 najpopularniejszych nazwisk"""
    for path in data_paths[:2]:
        df = pd.read_csv(path)
        df = df.sort_values(by="liczba", ascending=False).head(1000)
        df.to_csv(path, index=False, encoding="utf-8")


def get_weighted_random_entry(data):
    """Funkcja zwracajaca losowy wpis z danymi z wagami"""
    return data.sample(weights=data["LICZBA"].astype(int)).iloc[0]


def fill_stanowiska(connection):
    """Funkcja wypelniajaca tabele stanowiska"""
    local_cursor = connection.cursor()
    for stanowisko, pensja in STANOWISKA.items():
        local_cursor.execute(
            "INSERT INTO stanowiska (nazwa_stanowiska, wysokosc_pensji) VALUES (%s, %s)",
            (stanowisko, pensja),
        )

    local_cursor.close()
    connection.commit()


def fill_pracownicy(connection):
    """Funkcja wypelniajaca tabele pracownicy"""
    for uwaga, stanowisko in PRACOWNICY.items():
        imie_row = get_weighted_random_entry(pd.read_csv(data_paths["imiona"]))
        imie = imie_row["IMIĘ"]
        plec = imie_row["PŁEĆ"]
        nazwisko = get_weighted_random_entry(
            pd.read_csv(data_paths["naz_zenskie" if plec == "K" else "naz_meskie"])
        )["NAZWISKO"]
        local_cursor = connection.cursor()
        local_cursor.execute(
            "SELECT id_stanowiska FROM stanowiska WHERE nazwa_stanowiska = %s",
            (stanowisko,),
        )
        id_stanowiska = local_cursor.fetchone()[0]
        telefon = f"{randint(500, 999)}-{randint(100, 999)}-{randint(100, 999)}"
        numer_bliskiego = None
        local_cursor.execute(
            "INSERT INTO telefony (telefon, numer_bliskiego) VALUES (%s, %s)",
            (telefon, numer_bliskiego),
        )
        id_telefonu = local_cursor.lastrowid
        local_cursor.execute(
            "INSERT INTO pracownicy (imie, nazwisko, id_stanowiska, id_telefonu, uwagi) VALUES (%s, %s, %s, %s, %s)",
            (imie, nazwisko, id_stanowiska, id_telefonu, uwaga),
        )
        local_cursor.close()
        connection.commit()


def dry_fill(connection):
    """Funkcja wypelniajaca tabele w bazie danych suchymi danymi"""
    print("Czyszczenie wszystkich tabel...")
    emptyall(connection)
    try:
        # najpierw tabele bez kluczy obcych
        print("Wypelnianie tabeli stanowiska...")
        fill_stanowiska(connection)

        print("Wypelnianie tabeli pracownicy...")
        fill_pracownicy(connection)

    except mysql.connector.Error as err:
        print(err.msg)
        sys.exit()


dry_fill(cnx)

cnx.close()
