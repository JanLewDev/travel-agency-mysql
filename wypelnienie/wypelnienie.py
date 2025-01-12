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
from do_wypelnienia import (
    LICZBA_KLIENTOW,
    STANOWISKA,
    PRACOWNICY,
    RODZAJE_TRANSPORTU,
    MIASTA,
    TRANSAKCJE_PRACOWNICY,
    TRANSAKCJE_KONTRAHENCI,
    TRANSAKCJE_KLIENCI,
    KONTRAHENCI,
    ADRESY,
    KOSZTY_MIASTA,
    KOSZTY_U_KONTRAHENTOW,
    MIEJSCA_WYCIECZKI,
    PROPOZYCJE,
    WYCIECZKI,
    RODZAJE_USLUG_DODATKOWYCH,
    Adres,
)

from custom_util import progressbar

DIRNAME = os.path.dirname(os.path.abspath(__file__))

load_dotenv(dotenv_path=f"{DIRNAME}/../.env")
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
    "naz_zenskie": f"{DIRNAME}/../dane_statystyczne/nazwiska_zenskie.csv",
    "naz_meskie": f"{DIRNAME}/../dane_statystyczne/nazwiska_meskie.csv",
    "imiona": f"{DIRNAME}/../dane_statystyczne/Imiona_nadane_dzieciom_w_Polsce_w_I_polowie_2024.csv",
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
    assert len(show_tables(cnx)) == len(TABLES) == 23


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
    "rodzaje_uslug_dodatkowych": "id_uslugi_dodatkowej",
    "kraje": "id_kraju",
    "rodzaje_transportu": "id_rodzaju_transportu",
    "koszty_miasta": "id_kosztu_miasta",
    "koszty_u_kontrahentow": "id_kosztu_u_kontrahenta",
    "telefony": "id_telefonu",
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


def unpolish_string(string: str) -> str:
    """Funkcja zamieniajaca polskie znaki na ich odpowiedniki"""
    return (
        string.replace("ą", "a")
        .replace("ć", "c")
        .replace("ę", "e")
        .replace("ł", "l")
        .replace("ń", "n")
        .replace("ó", "o")
        .replace("ś", "s")
        .replace("ż", "z")
        .replace("ź", "z")
    )


def fill_klienci(connection):
    """Funkcja wypelniajaca tabele klienci"""
    for _ in progressbar(range(LICZBA_KLIENTOW)):
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
        # zastapic polskie znaki
        if email:
            email = unpolish_string(email)

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


def fill_rodzaje_transportu(connection):
    """Funkcja wypelniajaca tabele rodzaje transportu"""
    for nazwa, opis in RODZAJE_TRANSPORTU:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO rodzaje_transportu (nazwa, opis) VALUES (%s, %s)",
            (nazwa, opis),
        )
        cursor.close()
        connection.commit()


def dodaj_adres(connection, adres: Adres) -> int:
    """Funkcja dodajaca adres do bazy danych"""
    cursor = connection.cursor()
    id_miasta = get_id_from_table(connection, "miasta", "miasto", adres.miasto)
    if not id_miasta:
        id_kraju = get_id_from_table(connection, "kraje", "kraj", MIASTA[adres.miasto])
        if not id_kraju:
            cursor.execute(
                "INSERT INTO kraje (kraj) VALUES (%s)", (MIASTA[adres.miasto],)
            )
            id_kraju = cursor.lastrowid

        cursor.execute(
            "INSERT INTO miasta (miasto, id_kraju) VALUES (%s, %s)",
            (adres.miasto, id_kraju),
        )
        id_miasta = cursor.lastrowid

    assert isinstance(id_miasta, int)
    cursor.execute(
        "INSERT INTO adresy (adres, adres2, id_miasta, kod_pocztowy) VALUES (%s, %s, %s, %s)",
        (adres.adres, adres.adres2, id_miasta, adres.kod_pocztowy),
    )
    id_adresu = cursor.lastrowid
    cursor.close()
    connection.commit()
    return id_adresu


def fill_propozycje(connection):
    """Funkcja wypelniajaca tabele propozycje wycieczki i powiazane"""
    cursor = connection.cursor()
    for propozycja in PROPOZYCJE:
        # Pobieranie ID miejsca wycieczki
        nazwa_miejsca = propozycja.miejsce_wycieczki_nazwa
        adres = ADRESY[nazwa_miejsca]
        nazwa_kontrahenta = MIEJSCA_WYCIECZKI[nazwa_miejsca].nazwa_kontrahenta

        # Dodanie kontrahenta
        id_kontrahenta = get_id_from_table(
            connection, "kontrahenci", "nazwa", nazwa_kontrahenta
        )
        if not id_kontrahenta:
            id_adresu = dodaj_adres(connection, ADRESY[nazwa_kontrahenta])

            cursor.execute(
                "INSERT INTO kontrahenci (nazwa, opis, email, id_adresu) VALUES (%s, %s, %s, %s)",
                (
                    nazwa_kontrahenta,
                    KONTRAHENCI[nazwa_kontrahenta].opis,
                    KONTRAHENCI[nazwa_kontrahenta].email,
                    id_adresu,
                ),
            )
            id_kontrahenta = cursor.lastrowid

        # Dodanie miejsca wycieczki
        id_miejsca = get_id_from_table(
            connection, "miejsca_wycieczki", "nazwa", nazwa_miejsca
        )
        if not id_miejsca:
            id_adresu = dodaj_adres(connection, adres)
            cursor.execute(
                "INSERT INTO miejsca_wycieczki (nazwa, id_adresu, koszt, cena_dla_klienta, id_kontrahenta) VALUES (%s, %s, %s, %s, %s)",
                (
                    nazwa_miejsca,
                    id_adresu,
                    MIEJSCA_WYCIECZKI[nazwa_miejsca].koszt,
                    MIEJSCA_WYCIECZKI[nazwa_miejsca].cena_dla_kilienta,
                    id_kontrahenta,
                ),
            )
            id_miejsca = cursor.lastrowid

        # Dodanie propozycji wycieczki
        cursor.execute(
            """
            INSERT INTO propozycje_wycieczki (nazwa, opis, ograniczenia, min_liczba_osob, maks_liczba_osob, nasze_koszty_razem, cena_dla_klienta, id_miejsca)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                propozycja.nazwa,
                propozycja.opis,
                propozycja.ograniczenia,
                propozycja.min_osob,
                propozycja.max_osob,
                propozycja.nasze_koszty_na_osobe_total,
                propozycja.cena_dla_kilienta_za_osobe,
                id_miejsca,
            ),
        )
        id_propozycji = cursor.lastrowid
        connection.commit()

        print("Dodano propozycje wycieczki", propozycja.nazwa)

        for transport in propozycja.transport_propozycja_wycieczki:
            cursor.execute(
                "SELECT id_kosztu FROM koszty_miasta JOIN miasta ON koszty_miasta.id_miasta = miasta.id_miasta WHERE miasta.miasto = %s",
                (propozycja.miasto_z_koszty_miasta,),
            )
            id_kosztu_miasta = cursor.fetchone()
            if not id_kosztu_miasta:
                id_miasta = get_id_from_table(
                    connection, "miasta", "miasto", propozycja.miasto_z_koszty_miasta
                )
                if not id_miasta:
                    id_kraju = get_id_from_table(
                        connection,
                        "kraje",
                        "kraj",
                        MIASTA[propozycja.miasto_z_koszty_miasta],
                    )
                    print(id_kraju)
                    if not id_kraju:
                        cursor.execute(
                            "INSERT INTO kraje (kraj) VALUES (%s)",
                            (MIASTA[propozycja.miasto_z_koszty_miasta],),
                        )
                        id_kraju = cursor.lastrowid

                    cursor.execute(
                        "INSERT INTO miasta (miasto, id_kraju) VALUES (%s, %s)",
                        (propozycja.miasto_z_koszty_miasta, id_kraju),
                    )
                    id_miasta = cursor.lastrowid

                cursor.execute(
                    "INSERT INTO koszty_miasta (koszt, cena_dla_klienta, id_miasta) VALUES (%s, %s, %s)",
                    (
                        KOSZTY_MIASTA[propozycja.miasto_z_koszty_miasta][0],
                        KOSZTY_MIASTA[propozycja.miasto_z_koszty_miasta][1],
                        id_miasta,
                    ),
                )
                id_kosztu_miasta = cursor.lastrowid

            id_rodzaju_transportu = get_id_from_table(
                connection, "rodzaje_transportu", "nazwa", transport
            )
            assert id_rodzaju_transportu is not None
            cursor.execute(
                "INSERT INTO transport_propozycja_wycieczki (id_rodzaju_transportu, id_propozycji, id_kosztu_miasta) VALUES (%s, %s, %s)",
                (id_rodzaju_transportu, id_propozycji, id_kosztu_miasta),
            )

        if propozycja.propozycje_koszt_u_kontrahentow:
            for (
                nazwa_kosztu_u_kontrahenta
            ) in propozycja.propozycje_koszt_u_kontrahentow:
                id_kosztu = get_id_from_table(
                    connection,
                    "koszty_u_kontrahentow",
                    "nazwa",
                    nazwa_kosztu_u_kontrahenta,
                )
                koszt_u_kontrahenta = KOSZTY_U_KONTRAHENTOW[nazwa_kosztu_u_kontrahenta]
                id_kontrahenta = get_id_from_table(
                    connection,
                    "kontrahenci",
                    "nazwa",
                    koszt_u_kontrahenta.nazwa_kontrahenta,
                )
                if not id_kontrahenta:
                    nazwa_kontrahenta = koszt_u_kontrahenta.nazwa_kontrahenta
                    id_adresu = dodaj_adres(connection, ADRESY[nazwa_kontrahenta])

                    cursor.execute(
                        "INSERT INTO kontrahenci (nazwa, opis, email, id_adresu) VALUES (%s, %s, %s, %s)",
                        (
                            nazwa_kontrahenta,
                            KONTRAHENCI[nazwa_kontrahenta].opis,
                            KONTRAHENCI[nazwa_kontrahenta].email,
                            id_adresu,
                        ),
                    )
                    id_kontrahenta = cursor.lastrowid

                if not id_kosztu:
                    cursor.execute(
                        "INSERT INTO koszty_u_kontrahentow (nazwa, koszt, cena_dla_klienta, id_kontrahenta) VALUES (%s, %s, %s, %s)",
                        (
                            nazwa_kosztu_u_kontrahenta,
                            koszt_u_kontrahenta.koszt,
                            koszt_u_kontrahenta.cena_dla_kilienta,
                            id_kontrahenta,
                        ),
                    )
                    id_kosztu = cursor.lastrowid

                cursor.execute(
                    "INSERT INTO propozycja_koszt_u_kontrahenta (id_propozycji, id_kosztu_u_kontrahenta) VALUES (%s, %s)",
                    (id_propozycji, id_kosztu),
                )
        connection.commit()

    cursor.close()


def fill_wycieczki(connection):
    """Funkcja wypelniajaca tabele wycieczki i powiazane"""
    cursor = connection.cursor()
    for wycieczka in WYCIECZKI:
        id_propozycji = get_id_from_table(
            connection, "propozycje_wycieczki", "nazwa", wycieczka.nazwa_propozycji
        )
        cursor.execute(
            "INSERT INTO wycieczki (czas_wyjazdu, czas_powrotu, liczba_osob, id_propozycji) VALUES (%s, %s, %s, %s)",
            (
                wycieczka.data_wyjazdu,
                wycieczka.data_powrotu,
                wycieczka.liczba_osob,
                id_propozycji,
            ),
        )
        id_wycieczki = cursor.lastrowid

        if wycieczka.uslugi_dodatkowe:
            for nazwa_usluga in wycieczka.uslugi_dodatkowe:
                usluga = RODZAJE_USLUG_DODATKOWYCH[nazwa_usluga]
                id_uslugi = get_id_from_table(
                    connection, "rodzaje_uslug_dodatkowych", "nazwa", usluga.nazwa
                )
                if not id_uslugi:
                    id_kontrahenta = get_id_from_table(
                        connection, "kontrahenci", "nazwa", usluga.nazwa_kontrahenta
                    )
                    if not id_kontrahenta:
                        id_adresu = dodaj_adres(
                            connection, ADRESY[usluga.nazwa_kontrahenta]
                        )

                        cursor.execute(
                            "INSERT INTO kontrahenci (nazwa, opis, email, id_adresu) VALUES (%s, %s, %s, %s)",
                            (
                                usluga.nazwa_kontrahenta,
                                KONTRAHENCI[usluga.nazwa_kontrahenta].opis,
                                KONTRAHENCI[usluga.nazwa_kontrahenta].email,
                                id_adresu,
                            ),
                        )
                        id_kontrahenta = cursor.lastrowid

                    cursor.execute(
                        "INSERT INTO rodzaje_uslug_dodatkowych (nazwa, opis_uslugi, koszt, cena_dla_klienta, id_kontrahenta) VALUES (%s, %s, %s, %s, %s)",
                        (
                            usluga.nazwa,
                            usluga.opis,
                            usluga.koszt,
                            usluga.cena_dla_kilienta,
                            id_kontrahenta,
                        ),
                    )
                    id_uslugi = cursor.lastrowid

                cursor.execute(
                    "INSERT INTO uslugi_dodatkowe (id_wycieczki, id_uslugi) VALUES (%s, %s)",
                    (id_wycieczki, id_uslugi),
                )

        print("Dodano wycieczke", wycieczka.nazwa_propozycji)

        # Powiązanie z klientami
        for klient_id in wycieczka.klienci_wycieczki:
            cursor.execute(
                "INSERT INTO klient_wycieczka (id_klienta, id_wycieczki) VALUES (%s, %s)",
                (klient_id, id_wycieczki),
            )

        # Powiązanie z pracownikami
        for pracownik_nazwa in wycieczka.pracownicy_wycieczki:
            pracownik_id = get_id_from_table(
                connection, "pracownicy", "uwagi", pracownik_nazwa
            )
            cursor.execute(
                "INSERT INTO pracownik_wycieczka (id_wycieczki, id_pracownika) VALUES (%s, %s)",
                (id_wycieczki, pracownik_id),
            )
        connection.commit()

    cursor.close()


def fill_transakcje_pracownicy(connection):
    """Funkcja wypelniajaca tabele transakcje pracownicy"""
    cursor = connection.cursor()
    for data, pracownik, kwota in TRANSAKCJE_PRACOWNICY:
        id_pracownika = get_id_from_table(connection, "pracownicy", "uwagi", pracownik)
        cursor.execute(
            "INSERT INTO transakcje_pracownicy (kwota, data_transakcji, id_pracownika) VALUES (%s, %s, %s)",
            (kwota, data, id_pracownika),
        )
    cursor.close()
    connection.commit()


def fill_transakcje_kontrahenci(connection):
    """Funkcja wypelniajaca tabele transakcje kontrahenci"""
    cursor = connection.cursor()
    for kwota, data, kontrahent, id_wycieczki in TRANSAKCJE_KONTRAHENCI:
        id_kontrahenta = get_id_from_table(
            connection, "kontrahenci", "nazwa", kontrahent
        )
        assert id_kontrahenta is not None
        cursor.execute(
            "INSERT INTO transakcje_kontrahenci (kwota, data_transakcji, id_kontrahenta, id_wycieczki) VALUES (%s, %s, %s, %s)",
            (kwota, data, id_kontrahenta, id_wycieczki),
        )

    cursor.close()
    connection.commit()


def fill_transakcje_klienci(connection):
    """Funkcja wypelniajaca tabele transakcje klienci"""
    for i in progressbar(range(len(TRANSAKCJE_KLIENCI))):
        kwota, data, id_klienta, id_wycieczki = TRANSAKCJE_KLIENCI[i]
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO transakcje_klienci (kwota, data_transakcji, id_klienta, id_wycieczki) VALUES (%s, %s, %s, %s)",
            (kwota, data, id_klienta, id_wycieczki),
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

        print("Wypelnianie rodzajow transportu...")
        fill_rodzaje_transportu(connection)

        print("Wypelnianie propozycji wycieczek...")
        fill_propozycje(connection)

        print("Wypelnianie tabeli klienci...")
        fill_klienci(connection)

        print("Wypelnianie wycieczek...")
        fill_wycieczki(connection)

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
