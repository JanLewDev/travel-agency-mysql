"""Modul zawierajacy funkcje wypelniajace baze danych"""

import os
import sys
import argparse
from random import randint, random, choice
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
from sql import DB_NAME, TABLES, ORDER_TO_CREATE, ORDER_TO_DROP
from do_wypelnienia import *

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
    print("Usuwanie wszystkich tabel...")
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
    assert len(show_tables(cnx)) == len(TABLES) == 22


def save_top_1000_surnames():
    """Funkcja uzyta do odfiltrowania 1000 najpopularniejszych nazwisk"""
    for path in data_paths[:2]:
        df = pd.read_csv(path)
        df = df.sort_values(by="liczba", ascending=False).head(1000)
        df.to_csv(path, index=False, encoding="utf-8")


def get_weighted_random_entry(data):
    """Funkcja zwracajaca losowy wpis z danymi z wagami"""
    return data.sample(weights=data["LICZBA"].astype(int)).iloc[0]


nazwy_id = {
    "miasta": "id_miasta",
    "adresy": "id_adresu",
    "kontrahenci": "id_kontrahenta",
    "miejsca_wycieczki": "id_miejsca",
    "propozycje_wycieczki": "id_propozycji",
    "wycieczki": "id_wycieczki",
    "pracownicy": "id_pracownika",
    "klienci": "id_klienta",
    "rodzaje_uslug_dodatkowych": "id_uslugi",
}


def get_id_from_table(connection, table, column, value):
    """Funkcja zwracajaca ID z tabeli"""
    cursor = connection.cursor()
    query = f"SELECT {nazwy_id[table]} FROM {table} WHERE {column} = %s"
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None


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


def get_random_name() -> tuple[str, str, str]:
    """Funkcja zwracajaca losowe imie i nazwisko"""
    imie_row = get_weighted_random_entry(pd.read_csv(data_paths["imiona"]))
    imie = imie_row["IMIĘ"]
    plec = imie_row["PŁEĆ"]
    nazwisko = get_weighted_random_entry(
        pd.read_csv(data_paths["naz_zenskie" if plec == "K" else "naz_meskie"])
    )["NAZWISKO"]
    return (imie, nazwisko, plec)


def fill_pracownicy(connection):
    """Funkcja wypelniajaca tabele pracownicy"""
    for uwaga, stanowisko in PRACOWNICY.items():
        imie, nazwisko, _ = get_random_name()
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


def fill_klienci(connection):
    """Funkcja wypelniajaca tabele klienci"""
    for _ in range(LICZBA_KLIENTOW):
        imie, nazwisko, plec = get_random_name()
        telefon = f"{randint(500, 999)}-{randint(100, 999)}-{randint(100, 999)}"
        numer_bliskiego = (
            f"{randint(500, 999)}-{randint(100, 999)}-{randint(100, 999)}"
            if random() < 0.4
            else None
        )
        email = (
            f"{imie.lower()}.{nazwisko.lower()}@{choice(['gmail.com', 'onet.pl', 'wp.pl', 'interia.pl'])}"
            if random() < 0.8
            else None
        )
        local_cursor = connection.cursor()
        local_cursor.execute(
            "INSERT INTO telefony (telefon, numer_bliskiego) VALUES (%s, %s)",
            (telefon, numer_bliskiego),
        )
        id_telefonu = local_cursor.lastrowid
        local_cursor.execute(
            "INSERT INTO klienci (imie, nazwisko, plec, email, id_telefonu) VALUES (%s, %s, %s, %s, %s)",
            (imie, nazwisko, plec, email, id_telefonu),
        )
        local_cursor.close()
        connection.commit()


def fill_propozycje(connection):
    """Funkcja wypelniajaca tabele propozycje wycieczki i powiazane"""
    for propozycja in PROPOZYCJE:
        nazwa, opis, ograniczenia, min_osob, max_osob, koszty, cena = propozycja

        # Pobieranie ID miejsca wycieczki
        miejsce = MIEJSCA_WYCIECZKI[nazwa]
        adres = ADRESY[nazwa]
        kontrahent = KONTRAHENCI[miejsce[4]]

        id_miasta = get_id_from_table(connection, "miasta", "miasto", adres[2])
        if not id_miasta:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO miasta (miasto) VALUES (%s)", (adres[2],))
            id_miasta = cursor.lastrowid
            cursor.close()
            connection.commit()

        # Dodanie adresu
        id_adresu = get_id_from_table(connection, "adresy", "adres", adres[0])
        if not id_adresu:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO adresy (adres, adres2, id_miasta, kod_pocztowy) VALUES (%s, %s, %s, %s)",
                (adres[0], adres[1], id_miasta, adres[3]),
            )
            id_adresu = cursor.lastrowid
            cursor.close()
            connection.commit()

        # Dodanie kontrahenta
        id_kontrahenta = get_id_from_table(
            connection, "kontrahenci", "nazwa", kontrahent[0]
        )
        if not id_kontrahenta:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO kontrahenci (nazwa, opis, email, id_adresu) VALUES (%s, %s, %s, %s)",
                (kontrahent[0], kontrahent[1], kontrahent[2], id_adresu),
            )
            id_kontrahenta = cursor.lastrowid
            cursor.close()
            connection.commit()

        # Dodanie miejsca wycieczki
        id_miejsca = get_id_from_table(connection, "miejsca_wycieczki", "nazwa", nazwa)
        if not id_miejsca:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO miejsca_wycieczki (nazwa, id_adresu, koszt, cena_dla_klienta, id_kontrahenta) VALUES (%s, %s, %s, %s, %s)",
                (nazwa, id_adresu, miejsce[2], miejsce[3], id_kontrahenta),
            )
            id_miejsca = cursor.lastrowid
            cursor.close()
            connection.commit()

        # Dodanie propozycji wycieczki
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO propozycje_wycieczki (nazwa, opis, ograniczenia, min_liczba_osob, maks_liczba_osob, nasze_koszty_razem, cena_dla_klienta, id_miejsca)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (nazwa, opis, ograniczenia, min_osob, max_osob, koszty, cena, id_miejsca),
        )
        cursor.close()
        connection.commit()


def fill_wycieczki(connection):
    """Funkcja wypelniajaca tabele wycieczki i powiazane"""
    for wycieczka in WYCIECZKI:
        czas_wyjazdu, czas_powrotu, liczba_osob, propozycja = wycieczka

        id_propozycji = get_id_from_table(
            connection, "propozycje_wycieczki", "nazwa", propozycja
        )
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO wycieczki (czas_wyjazdu, czas_powrotu, liczba_osob, id_propozycji) VALUES (%s, %s, %s, %s)",
            (czas_wyjazdu, czas_powrotu, liczba_osob, id_propozycji),
        )
        id_wycieczki = cursor.lastrowid

        # Powiązanie z klientami
        for klient_id in KLIENCI_WYCIECZKI.get(id_wycieczki, []):
            cursor.execute(
                "INSERT INTO klient_wycieczka (id_klienta, id_wycieczki) VALUES (%s, %s)",
                (klient_id, id_wycieczki),
            )

        # Powiązanie z pracownikami
        for pracownik_nazwa in PRACOWNIK_WYCIECZKA.get(id_wycieczki, []):
            pracownik_id = get_id_from_table(
                connection, "pracownicy", "uwagi", pracownik_nazwa
            )
            cursor.execute(
                "INSERT INTO pracownik_wycieczka (id_wycieczki, id_pracownika) VALUES (%s, %s)",
                (id_wycieczki, pracownik_id),
            )

        cursor.close()
        connection.commit()


def fill_uslugi_dodatkowe(connection):
    """Funkcja wypelniajaca tabele uslugi dodatkowe i powiazane"""
    for nazwa, (opis, koszt, cena, kontrahent) in RODZAJE_USLUG_DODATKOWYCH.items():
        # Pobieranie ID kontrahenta
        id_kontrahenta = get_id_from_table(
            connection, "kontrahenci", "nazwa", kontrahent
        )
        if not id_kontrahenta:
            cursor = connection.cursor()
            kontrahent_data = KONTRAHENCI[kontrahent]
            adres = ADRESY[kontrahent_data[0]]

            id_miasta = get_id_from_table(connection, "miasta", "miasto", adres[2])
            if not id_miasta:
                cursor.execute("INSERT INTO miasta (miasto) VALUES (%s)", (adres[2],))
                id_miasta = cursor.lastrowid

            cursor.execute(
                "INSERT INTO adresy (adres, adres2, id_miasta, kod_pocztowy) VALUES (%s, %s, %s, %s)",
                (adres[0], adres[1], id_miasta, adres[3]),
            )
            id_adresu = cursor.lastrowid

            cursor.execute(
                "INSERT INTO kontrahenci (nazwa, opis, email, id_adresu) VALUES (%s, %s, %s, %s)",
                (kontrahent_data[0], kontrahent_data[1], kontrahent_data[2], id_adresu),
            )
            id_kontrahenta = cursor.lastrowid
            connection.commit()

        # Dodanie usługi dodatkowej
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO rodzaje_uslug_dodatkowych (nazwa, opis_uslugi, koszt, cena_dla_klienta, id_kontrahenta) VALUES (%s, %s, %s, %s, %s)",
            (nazwa, opis, koszt, cena, id_kontrahenta),
        )
        id_uslugi = cursor.lastrowid
        cursor.close()
        connection.commit()

        # Powiązanie usługi z wycieczkami
        for id_wycieczki, uslugi in USLUGI_DODATKOWE.items():
            if nazwa in uslugi:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO uslugi_dodatkowe (id_wycieczki, id_uslugi) VALUES (%s, %s)",
                    (id_wycieczki, id_uslugi),
                )
                cursor.close()
                connection.commit()


def fill_transakcje_pracownicy(connection):
    """Funkcja wypelniajaca tabele transakcje pracownicy"""
    for data, pracownik, kwota in TRANSAKCJE_PRACOWNICY:
        id_pracownika = get_id_from_table(connection, "pracownicy", "uwagi", pracownik)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO transakcje_pracownicy (kwota, data_transakcji, id_pracownika) VALUES (%s, %s, %s)",
            (kwota, data, id_pracownika),
        )
        cursor.close()
        connection.commit()


def fill_transakcje_kontrahenci(connection):
    """Funkcja wypelniajaca tabele transakcje kontrahenci"""
    for kwota, data, kontrahent, id_wycieczki in TRANSAKCJE_KONTRAHENCI:
        id_kontrahenta = get_id_from_table(
            connection, "kontrahenci", "nazwa", kontrahent
        )
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO transakcje_kontrahenci (kwota, data_transakcji, id_kontrahenta, id_wycieczki) VALUES (%s, %s, %s, %s)",
            (kwota, data, id_kontrahenta, id_wycieczki),
        )
        cursor.close()
        connection.commit()


def fill_transakcje_klienci(connection):
    """Funkcja wypelniajaca tabele transakcje klienci"""
    for (id_klienta, id_wycieczki), (kwota, data) in TRANSAKCJE_KLIENCI.items():
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO transakcje_klienci (kwota, data_transakcji, id_klienta, id_wycieczki) VALUES (%s, %s, %s, %s)",
            (kwota, data, id_klienta, id_wycieczki),
        )
        cursor.close()
        connection.commit()


def fill_klienci_wycieczki(connection):
    """Funkcja wypelniajaca tabele klienci_wycieczki"""
    for id_klienta, id_wycieczki in KLIENCI_WYCIECZKI:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO klient_wycieczka (id_klienta, id_wycieczki) VALUES (%s, %s)",
            (id_klienta, id_wycieczki),
        )
        cursor.close()
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

        print("Wypelnianie tabeli klienci...")
        fill_klienci(connection)

        print("Wypelnianie propozycji wycieczek...")
        fill_propozycje(connection)

        print("Wypelnianie wycieczek...")
        fill_wycieczki(connection)

        print("Wypelnianie uslug dodatkowych...")
        fill_uslugi_dodatkowe(connection)

        print("Wypelnianie transakcji pracownikow...")
        fill_transakcje_pracownicy(connection)

        print("Wypelnianie transakcji kontrahentow...")
        fill_transakcje_kontrahenci(connection)

        print("Wypelnianie transakcji klientow...")
        fill_transakcje_klienci(connection)

    except mysql.connector.Error as err:
        print(err.msg)
        sys.exit()


dry_fill(cnx)

cnx.close()
