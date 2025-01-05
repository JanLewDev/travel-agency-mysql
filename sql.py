"""Modul zawierajacy uzywany kod SQL"""

DB_NAME = "team02"

TABLES = {}
TABLES[
    "stanowiska"
] = """-- sql
    CREATE TABLE stanowiska (
        id_stanowiska INT UNSIGNED NOT NULL AUTO_INCREMENT,
        nazwa_stanowiska VARCHAR(50) NOT NULL,
        wysokosc_pensji INT NOT NULL,
        PRIMARY KEY (id_stanowiska),
        KEY idx_nazwa_stanowiska (nazwa_stanowiska)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "telefony"
] = """-- sql
    CREATE TABLE telefony (
        id_telefonu INT UNSIGNED NOT NULL AUTO_INCREMENT,
        telefon VARCHAR(12) NOT NULL,
        numer_bliskiego VARCHAR(12) DEFAULT NULL,
        PRIMARY KEY (id_telefonu)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "klienci"
] = """-- sql
    CREATE TABLE klienci (
        id_klienta INT UNSIGNED NOT NULL AUTO_INCREMENT,
        imie VARCHAR(20) NOT NULL,
        nazwisko VARCHAR(20) NOT NULL,
        email VARCHAR(100) DEFAULT NULL,
        id_telefonu INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_klienta),
        CONSTRAINT fk_id_telefonu_klienci FOREIGN KEY (id_telefonu) REFERENCES telefony (id_telefonu) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "kontrahenci"
] = """-- sql
    CREATE TABLE kontrahenci (
        id_kontrahenta INT UNSIGNED NOT NULL AUTO_INCREMENT,
        nazwa VARCHAR(40) NOT NULL,
        opis TEXT DEFAULT NULL,
        PRIMARY KEY (id_kontrahenta),
        KEY idx_nazwa (nazwa)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "pracownicy"
] = """-- sql
    CREATE TABLE pracownicy (
        id_pracownika INT UNSIGNED NOT NULL AUTO_INCREMENT,
        imie VARCHAR(20) NOT NULL,
        nazwisko VARCHAR(20) NOT NULL,
        id_stanowiska INT UNSIGNED NOT NULL,
        id_telefonu INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_pracownika),
        CONSTRAINT fk_id_stanowiska_pracownicy FOREIGN KEY (id_stanowiska) REFERENCES stanowiska (id_stanowiska) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_telefonu_pracownicy FOREIGN KEY (id_telefonu) REFERENCES telefony (id_telefonu) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "typy_kosztow"
] = """-- sql
    CREATE TABLE typy_kosztow (
        id_typu_kosztu INT UNSIGNED NOT NULL AUTO_INCREMENT,
        nazwa VARCHAR(40) NOT NULL,
        PRIMARY KEY (id_typu_kosztu),
        KEY idx_nazwa (nazwa)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "koszty"
] = """-- sql
    CREATE TABLE koszty (
        id_kosztu INT UNSIGNED NOT NULL AUTO_INCREMENT,
        koszt DECIMAL(10, 2) NOT NULL,
        cena_dla_klienta DECIMAL(10, 2) NOT NULL,
        id_typu_kosztu INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_kosztu),
        CONSTRAINT fk_id_typu_kosztu_koszty FOREIGN KEY (id_typu_kosztu) REFERENCES typy_kosztow (id_typu_kosztu) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "rodzaje_uslug_dodatkowych"
] = """-- sql
    CREATE TABLE rodzaje_uslug_dodatkowych (
        id_uslugi_dodatkowej INT UNSIGNED NOT NULL AUTO_INCREMENT,
        nazwa VARCHAR(40) NOT NULL,
        opis_uslugi TEXT DEFAULT NULL,
        cena DECIMAL(10, 2) NOT NULL,
        koszt_organizacji DECIMAL(10, 2) NOT NULL,
        PRIMARY KEY (id_uslugi_dodatkowej)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "rodzaje_transportu"
] = """-- sql
    CREATE TABLE rodzaje_transportu (
        id_transportu INT UNSIGNED NOT NULL AUTO_INCREMENT,
        nazwa VARCHAR(20) NOT NULL,
        grupowy BOOLEAN NOT NULL DEFAULT FALSE,
        id_kosztu INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_transportu),
        CONSTRAINT fk_id_kosztu_rodzaje_transportu FOREIGN KEY (id_kosztu) REFERENCES koszty (id_kosztu) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "miejsca_wycieczki"
] = """-- sql
    CREATE TABLE miejsca_wycieczki (
        id_miejsca INT UNSIGNED NOT NULL AUTO_INCREMENT,
        miejsce VARCHAR(20) NOT NULL,
        id_kosztu INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_miejsca),
        CONSTRAINT fk_id_kosztu_miejsca_wycieczki FOREIGN KEY (id_kosztu) REFERENCES koszty (id_kosztu) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "rodzaje_wycieczki"
] = """-- sql
    CREATE TABLE rodzaje_wycieczki (
        id_rodzaju INT UNSIGNED NOT NULL AUTO_INCREMENT,
        opis TEXT NOT NULL,
        ograniczenia VARCHAR(50) DEFAULT NULL,
        min_liczba_osob INT UNSIGNED NOT NULL,
        maks_liczba_osob INT UNSIGNED NOT NULL,
        id_kosztu INT UNSIGNED NOT NULL,
        id_miejsca INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_rodzaju),
        CONSTRAINT fk_id_kosztu_rodzaje_wycieczki FOREIGN KEY (id_kosztu) REFERENCES koszty (id_kosztu) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_miejsca_rodzaje_wycieczki FOREIGN KEY (id_miejsca) REFERENCES miejsca_wycieczki (id_miejsca) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "wycieczki"
] = """-- sql
    CREATE TABLE wycieczki (
        id_wycieczki INT UNSIGNED NOT NULL AUTO_INCREMENT,
        czas_wyjazdu DATETIME NOT NULL,
        czas_powrotu DATETIME NOT NULL,
        id_rodzaju INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_wycieczki),
        CONSTRAINT fk_id_rodzaju_wycieczki FOREIGN KEY (id_rodzaju) REFERENCES rodzaje_wycieczki (id_rodzaju) ON DELETE RESTRICT ON UPDATE CASCADE
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
    "transport_rodzaj_wycieczki"
] = """-- sql
    CREATE TABLE transport_rodzaj_wycieczki (
        id_transportu INT UNSIGNED NOT NULL,
        id_rodzaju INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_transportu, id_rodzaju),
        CONSTRAINT fk_id_transportu_transport_rodzaj_wycieczki FOREIGN KEY (id_transportu) REFERENCES rodzaje_transportu (id_transportu) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_rodzaju_transport_rodzaj_wycieczki FOREIGN KEY (id_rodzaju) REFERENCES rodzaje_wycieczki (id_rodzaju) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "typy_transakcji"
] = """-- sql
    CREATE TABLE typy_transakcji (
        id_typu INT UNSIGNED NOT NULL AUTO_INCREMENT,
        nazwa VARCHAR(50) NOT NULL,
        opis TEXT DEFAULT NULL,
        PRIMARY KEY (id_typu)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "strony_transakcji"
] = """-- sql
    CREATE TABLE strony_transakcji (
        id_strony INT UNSIGNED NOT NULL AUTO_INCREMENT,
        typ_strony ENUM('klient', 'pracownik', 'kontrahent', 'firma') NOT NULL DEFAULT 'firma',
        id_klienta INT UNSIGNED NOT NULL,
        id_pracownika INT UNSIGNED NOT NULL,
        id_kontrahenta INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_strony),
        CONSTRAINT fk_id_klienta_strony FOREIGN KEY (id_klienta) REFERENCES klienci (id_klienta) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_pracownika_strony FOREIGN KEY (id_pracownika) REFERENCES pracownicy (id_pracownika) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_kontrahenta_strony FOREIGN KEY (id_kontrahenta) REFERENCES kontrahenci (id_kontrahenta) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

TABLES[
    "transakcje"
] = """-- sql
    CREATE TABLE transakcje (
        id_transakcji INT UNSIGNED NOT NULL AUTO_INCREMENT,
        id_wycieczki INT UNSIGNED NOT NULL,
        id_typu_transakcji INT UNSIGNED NOT NULL,
        kwota DECIMAL(10, 2) NOT NULL,
        data_transakcji TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        id_strony_od INT UNSIGNED NOT NULL,
        id_strony_do INT UNSIGNED NOT NULL,
        PRIMARY KEY (id_transakcji),
        CONSTRAINT fk_id_wycieczki_transakcje FOREIGN KEY (id_wycieczki) REFERENCES wycieczki (id_wycieczki) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_typu_transakcji_transakcje FOREIGN KEY (id_typu_transakcji) REFERENCES typy_transakcji (id_typu) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_strony_od_transakcje FOREIGN KEY (id_strony_od) REFERENCES strony_transakcji (id_strony) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_id_strony_do_transakcje FOREIGN KEY (id_strony_do) REFERENCES strony_transakcji (id_strony) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;
"""

ORDER_TO_DROP = [
    "transakcje",
    "strony_transakcji",
    "transport_rodzaj_wycieczki",
    "pracownik_wycieczka",
    "klient_wycieczka",
    "uslugi_dodatkowe",
    "wycieczki",
    "rodzaje_wycieczki",
    "miejsca_wycieczki",
    "rodzaje_transportu",
    "rodzaje_uslug_dodatkowych",
    "koszty",
    "typy_kosztow",
    "pracownicy",
    "kontrahenci",
    "klienci",
    "telefony",
    "stanowiska",
    "typy_transakcji",
]
