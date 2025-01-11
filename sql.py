"""Modul zawierajacy uzywany kod SQL"""

DB_NAME = "team02"

TABLES = {}
TABLES[
    "stanowiska"
] = """-- sql
    CREATE TABLE stanowiska (
        id_stanowiska INT UNSIGNED NOT NULL AUTO_INCREMENT,
        nazwa_stanowiska VARCHAR(50) NOT NULL,
        wysokosc_pensji DECIMAL(10, 2) NOT NULL,
        PRIMARY KEY (id_stanowiska),
        KEY idx_nazwa_stanowiska (nazwa_stanowiska)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "telefony"
] = """-- sql
    CREATE TABLE telefony (
        id_telefonu INT UNSIGNED NOT NULL AUTO_INCREMENT,
        telefon VARCHAR(20) NOT NULL,
        numer_bliskiego VARCHAR(20) DEFAULT NULL,
        PRIMARY KEY (id_telefonu)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "klienci"
] = """-- sql
    CREATE TABLE klienci (
        id_klienta INT UNSIGNED NOT NULL AUTO_INCREMENT,
        imie VARCHAR(40) NOT NULL,
        nazwisko VARCHAR(40) NOT NULL,
        plec ENUM('K', 'M') NOT NULL,
        email VARCHAR(100) DEFAULT NULL,
        id_telefonu INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_klienta),
        CONSTRAINT fk_id_telefonu_klienci FOREIGN KEY (id_telefonu) REFERENCES telefony (id_telefonu) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "kraje"
] = """-- sql
    CREATE TABLE kraje (
        id_kraju INT UNSIGNED NOT NULL AUTO_INCREMENT,
        kraj VARCHAR(50) NOT NULL,
        PRIMARY KEY (id_kraju),
        KEY idx_kraj (kraj)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "miasta"
] = """-- sql
    CREATE TABLE miasta (
        id_miasta INT UNSIGNED NOT NULL AUTO_INCREMENT,
        miasto VARCHAR(50) NOT NULL,
        id_kraju INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_miasta),
        KEY idx_miasto (miasto),
        CONSTRAINT fk_id_kraju_miasta FOREIGN KEY (id_kraju) REFERENCES kraje (id_kraju) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "adresy"
] = """-- sql
    CREATE TABLE adresy (
        id_adresu INT UNSIGNED NOT NULL AUTO_INCREMENT,
        adres VARCHAR(50) NOT NULL,
        adres2 VARCHAR(50) DEFAULT NULL,
        id_miasta INT UNSIGNED NOT NULL,
        kod_pocztowy VARCHAR(6) DEFAULT NULL,
        PRIMARY KEY (id_adresu),
        CONSTRAINT fk_id_miasta_adresy FOREIGN KEY (id_miasta) REFERENCES miasta (id_miasta) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "kontrahenci"
] = """-- sql
    CREATE TABLE kontrahenci (
        id_kontrahenta INT UNSIGNED NOT NULL AUTO_INCREMENT,
        nazwa VARCHAR(40) NOT NULL,
        opis TEXT DEFAULT NULL,
        email VARCHAR(100) NOT NULL,
        id_adresu INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_kontrahenta),
        CONSTRAINT fk_id_adresu_kontrahenci FOREIGN KEY (id_adresu) REFERENCES adresy (id_adresu) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "pracownicy"
] = """-- sql
    CREATE TABLE pracownicy (
        id_pracownika INT UNSIGNED NOT NULL AUTO_INCREMENT,
        imie VARCHAR(40) NOT NULL,
        nazwisko VARCHAR(40) NOT NULL,
        id_stanowiska INT UNSIGNED NOT NULL,
        id_telefonu INT UNSIGNED NOT NULL,
        uwagi TEXT DEFAULT NULL,
        PRIMARY KEY (id_pracownika),
        CONSTRAINT fk_id_stanowiska_pracownicy FOREIGN KEY (id_stanowiska) REFERENCES stanowiska (id_stanowiska) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_telefonu_pracownicy FOREIGN KEY (id_telefonu) REFERENCES telefony (id_telefonu) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "rodzaje_uslug_dodatkowych"
] = """-- sql
    CREATE TABLE rodzaje_uslug_dodatkowych (
        id_uslugi_dodatkowej INT UNSIGNED NOT NULL AUTO_INCREMENT,
        nazwa VARCHAR(40) NOT NULL,
        opis_uslugi TEXT DEFAULT NULL,
        koszt DECIMAL(10, 2) NOT NULL,
        cena_dla_klienta DECIMAL(10, 2) NOT NULL,
        id_kontrahenta INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_uslugi_dodatkowej),
        CONSTRAINT fk_id_kontrahenta_uslugi_dodatkowej FOREIGN KEY (id_kontrahenta) REFERENCES kontrahenci (id_kontrahenta) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "rodzaje_transportu"
] = """-- sql
    CREATE TABLE rodzaje_transportu (
        id_rodzaju_transportu INT UNSIGNED NOT NULL AUTO_INCREMENT,
        nazwa VARCHAR(40) NOT NULL,
        opis TEXT DEFAULT NULL,
        PRIMARY KEY (id_rodzaju_transportu)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "miejsca_wycieczki"
] = """-- sql
    CREATE TABLE miejsca_wycieczki (
        id_miejsca INT UNSIGNED NOT NULL AUTO_INCREMENT,
        nazwa VARCHAR(50) NOT NULL,
        id_adresu INT UNSIGNED NOT NULL,
        koszt DECIMAL(10, 2) NOT NULL,
        cena_dla_klienta DECIMAL(10, 2) NOT NULL,
        id_kontrahenta INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_miejsca),
        CONSTRAINT fk_id_adresu_miejsca_wycieczki FOREIGN KEY (id_adresu) REFERENCES adresy (id_adresu) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_kontrahenta_miejsca_wycieczki FOREIGN KEY (id_kontrahenta) REFERENCES kontrahenci (id_kontrahenta) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "propozycje_wycieczki"
] = """-- sql
    CREATE TABLE propozycje_wycieczki (
        id_propozycji INT UNSIGNED NOT NULL AUTO_INCREMENT,
		nazwa VARCHAR(50) NOT NULL,
        opis TEXT DEFAULT NULL,
        ograniczenia VARCHAR(50) DEFAULT NULL,
        min_liczba_osob INT NOT NULL DEFAULT 0,
        maks_liczba_osob INT NOT NULL,
        nasze_koszty_razem DECIMAL(10, 2) NOT NULL,
        cena_dla_klienta DECIMAL(10, 2) NOT NULL,
        id_miejsca INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_propozycji),
        CONSTRAINT fk_id_miejsca_propozycje_wycieczki FOREIGN KEY (id_miejsca) REFERENCES miejsca_wycieczki (id_miejsca) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "wycieczki"
] = """-- sql
    CREATE TABLE wycieczki (
        id_wycieczki INT UNSIGNED NOT NULL AUTO_INCREMENT,
        czas_wyjazdu DATETIME NOT NULL,
        czas_powrotu DATETIME NOT NULL,
		liczba_osob INT UNSIGNED NOT NULL,
        id_propozycji INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_wycieczki),
        CONSTRAINT fk_id_propozycji_wycieczki FOREIGN KEY (id_propozycji) REFERENCES propozycje_wycieczki (id_propozycji) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "uslugi_dodatkowe"
] = """-- sql
    CREATE TABLE uslugi_dodatkowe (
        id_wycieczki INT UNSIGNED NOT NULL,
        id_uslugi INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_wycieczki, id_uslugi),
        CONSTRAINT fk_id_wycieczki_uslugi_dodatkowe FOREIGN KEY (id_wycieczki) REFERENCES wycieczki (id_wycieczki) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_uslugi_uslugi_dodatkowe FOREIGN KEY (id_uslugi) REFERENCES rodzaje_uslug_dodatkowych (id_uslugi_dodatkowej) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "klient_wycieczka"
] = """-- sql
    CREATE TABLE klient_wycieczka (
        id_klienta INT UNSIGNED NOT NULL,
        id_wycieczki INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_klienta, id_wycieczki),
        CONSTRAINT fk_id_klienta_klient_wycieczka FOREIGN KEY (id_klienta) REFERENCES klienci (id_klienta) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_wycieczki_klient_wycieczka FOREIGN KEY (id_wycieczki) REFERENCES wycieczki (id_wycieczki) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "pracownik_wycieczka"
] = """-- sql
    CREATE TABLE pracownik_wycieczka (
        id_wycieczki INT UNSIGNED NOT NULL,
        id_pracownika INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_wycieczki, id_pracownika),
        CONSTRAINT fk_id_wycieczki_pracownik_wycieczka FOREIGN KEY (id_wycieczki) REFERENCES wycieczki (id_wycieczki) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_pracownika_pracownik_wycieczka FOREIGN KEY (id_pracownika) REFERENCES pracownicy (id_pracownika) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "transport_propozycja_wycieczki"
] = """-- sql
    CREATE TABLE transport_propozycja_wycieczki (
        id_rodzaju_transportu INT UNSIGNED NOT NULL,
        id_propozycji INT UNSIGNED NOT NULL,
        id_kosztu_miasta INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_rodzaju_transportu, id_propozycji, id_kosztu_miasta),
        CONSTRAINT fk_id_rodzaju_transportu_transport_propozycja_wycieczki FOREIGN KEY (id_rodzaju_transportu) REFERENCES rodzaje_transportu (id_rodzaju_transportu) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_propozycji_transport_propozycja_wycieczki FOREIGN KEY (id_propozycji) REFERENCES propozycje_wycieczki (id_propozycji) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_kosztu_miasta_transport_propozycja_wycieczki FOREIGN KEY (id_kosztu_miasta) REFERENCES koszty_miasta (id_kosztu) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "koszty_u_kontrahentow"
] = """-- sql
    CREATE TABLE koszty_u_kontrahentow (
        id_kosztu_u_kontrahenta INT UNSIGNED NOT NULL AUTO_INCREMENT,
		nazwa VARCHAR(40) NOT NULL,
        koszt DECIMAL(10, 2) NOT NULL,
        cena_dla_klienta DECIMAL(10, 2) NOT NULL,
        id_kontrahenta INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_kosztu_u_kontrahenta),
        CONSTRAINT fk_id_kontrahenta_koszty_u_kontrahentow FOREIGN KEY (id_kontrahenta) REFERENCES kontrahenci (id_kontrahenta) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "propozycja_koszt_u_kontrahenta"
] = """-- sql
    CREATE TABLE propozycja_koszt_u_kontrahenta (
        id_propozycji INT UNSIGNED NOT NULL,
        id_kosztu_u_kontrahenta INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_propozycji, id_kosztu_u_kontrahenta),
        CONSTRAINT fk_id_propozycji_propozycja_koszt_u_kontrahenta FOREIGN KEY (id_propozycji) REFERENCES propozycje_wycieczki (id_propozycji) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_kosztu_u_kontrahenta_propozycja_koszt_u_kontrahenta FOREIGN KEY (id_kosztu_u_kontrahenta) REFERENCES koszty_u_kontrahentow (id_kosztu_u_kontrahenta) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "transakcje_klienci"
] = """-- sql
    CREATE TABLE transakcje_klienci (
        id_transakcji INT UNSIGNED NOT NULL AUTO_INCREMENT,
        kwota DECIMAL(10, 2) NOT NULL,
        data_transakcji DATETIME NOT NULL,
        id_klienta INT UNSIGNED NOT NULL,
        id_wycieczki INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_transakcji),
        CONSTRAINT fk_id_klienta_transakcje_klienci FOREIGN KEY (id_klienta) REFERENCES klienci (id_klienta) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_wycieczki_transakcje_klienci FOREIGN KEY (id_wycieczki) REFERENCES wycieczki (id_wycieczki) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "transakcje_kontrahenci"
] = """-- sql
    CREATE TABLE transakcje_kontrahenci (
        id_transakcji INT UNSIGNED NOT NULL AUTO_INCREMENT,
        kwota DECIMAL(10, 2) NOT NULL,
        data_transakcji DATETIME NOT NULL,
        id_kontrahenta INT UNSIGNED NOT NULL,
        id_wycieczki INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_transakcji),
        CONSTRAINT fk_id_kontrahenta_transakcje_kontrahenci FOREIGN KEY (id_kontrahenta) REFERENCES kontrahenci (id_kontrahenta) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_wycieczki_transakcje_kontrahenci FOREIGN KEY (id_wycieczki) REFERENCES wycieczki (id_wycieczki) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "transakcje_pracownicy"
] = """-- sql
    CREATE TABLE transakcje_pracownicy (
        id_transakcji INT UNSIGNED NOT NULL AUTO_INCREMENT,
        kwota DECIMAL(10, 2) NOT NULL,
        data_transakcji DATETIME NOT NULL,
        id_pracownika INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_transakcji),
        CONSTRAINT fk_id_pracownika_transakcje_pracownicy FOREIGN KEY (id_pracownika) REFERENCES pracownicy (id_pracownika) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "koszty_miasta"
] = """-- sql
    CREATE TABLE koszty_miasta (
        id_kosztu INT UNSIGNED NOT NULL AUTO_INCREMENT,
        koszt DECIMAL(10, 2) NOT NULL,
        cena_dla_klienta DECIMAL(10, 2) DEFAULT NULL,
        id_miasta INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_kosztu),
        CONSTRAINT fk_id_miasta_koszty_miasta FOREIGN KEY (id_miasta) REFERENCES miasta (id_miasta) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

ORDER_TO_CREATE = [
    "stanowiska",
    "telefony",
    "klienci",
    "kraje",
    "miasta",
    "adresy",
    "kontrahenci",
    "pracownicy",
    "rodzaje_uslug_dodatkowych",
    "koszty_miasta",
    "rodzaje_transportu",
    "miejsca_wycieczki",
    "propozycje_wycieczki",
    "wycieczki",
    "uslugi_dodatkowe",
    "klient_wycieczka",
    "pracownik_wycieczka",
    "transport_propozycja_wycieczki",
    "koszty_u_kontrahentow",
    "propozycja_koszt_u_kontrahenta",
    "transakcje_klienci",
    "transakcje_kontrahenci",
    "transakcje_pracownicy",
]

ORDER_TO_DROP = [
    "transport_propozycja_wycieczki",
    "koszty_miasta",
    "pracownik_wycieczka",
    "klient_wycieczka",
    "uslugi_dodatkowe",
    "transakcje_pracownicy",
    "transakcje_kontrahenci",
    "transakcje_klienci",
    "propozycja_koszt_u_kontrahenta",
    "wycieczki",
    "propozycje_wycieczki",
    "miejsca_wycieczki",
    "rodzaje_transportu",
    "rodzaje_uslug_dodatkowych",
    "pracownicy",
    "koszty_u_kontrahentow",
    "kontrahenci",
    "adresy",
    "miasta",
    "kraje",
    "klienci",
    "telefony",
    "stanowiska",
]
