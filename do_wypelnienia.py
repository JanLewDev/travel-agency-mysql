"""Modul zawiernajacy stale do wypelnienia bazy danych"""

from datetime import datetime, timedelta
from random import randint

# firma dziala w 2024 roku

LICZBA_KLIENTOW = 200
LICZBA_WYCIECZEK = 20

# klucz to nazwa stanowiska, wartosc to pensja
STANOWISKA = {
    "Menager": 10000,
    "Kierowca": 5000,
    "Przewodnik": 6000,
    "Pracownik biurowy": 4666,
    "Marketingowiec": 5500,
    "Organizator": 7000,
}

# klucz to nazwa pracownika, wartosc to stanowisko
PRACOWNICY = {
    "Menager": "Menager",
    "Kierowca1": "Kierowca",
    "Kierowca2": "Kierowca",
    "Kierowca3": "Kierowca",
    "Przewodnik, język angielski": "Przewodnik",
    "Pracownik biurowy": "Pracownik biurowy",
    "Marketingowiec": "Marketingowiec",
    "Organizator1": "Organizator",
    "Organizator2": "Organizator",
    "Organizator3": "Organizator",
}

# tablice zeby potem sie odwolywac po indeksie

# autokar do 50 osob, bus do 20 osob
# nazwa, opis
TRANSPORT = [
    ("Autokar 1", "Autokar niebieski"),
    ("Autokar 2", "Autokar zielony"),
    ("Bus 1", "Bus czerwony"),
    ("Bus 2", "Bus zolty"),
]
# najpierw zatrudnilismy wszystkich pracownikow,
# a dopiero potem mielismy klientow (duzy kapital zakladowy)

MIASTA = ["Warszawa", "Międzyzdroje", "Karpacz", "Sosnowiec", "Hel"]

# transakcje najpierw posortowac
# wyplaty pensji w 2024 roku, 10 dnia kazdego miesiaca
TRANSAKCJE_PRACOWNICY = [
    (datetime(2024, i, 10, 12, 0, 0), pracownik, STANOWISKA[stanowisko])
    for i in range(1, 13)
    for pracownik, stanowisko in PRACOWNICY.items()
]

# propozycja - dwudniowe morsowanie w Międzyzdrojach w styczniu
# min osob 45, maks 50
# koszt transportu 150
# koszt miejsca 150
# koszt przewodnika 10 - nasze koszty + 30 jedzenie (prowiant)
# Kontrahent - Hotel Gromada, ul. Wyzwolenia 1, 72-500 Międzyzdroje
# email - gromada.top@gmail.com
# wyjazdy

PROPOZYCJE = [
    (
        "Morsowanie Międzyzdroje",  # nazwa
        "Dwudniowe morsowanie ze zwiedzaniem Międzyzdrojów",  # opis
        None,  # ograniczenia
        45,  # min osob
        50,  # max osob
        40,  # nasze koszty na osobe total
        80,  # cena dla kilienta za osobe za nasze koszty
    ),
    (
        "Wypoczynek na Helu",
        "Polskie morze w ostatnich latach cieszy się coraz większym zainteresowaniem ze strony turystów. Oferujemy dwutygodniowe wakacje na tym malowniczym półwyspie, opalanie się na plaży, pływanie w Bałtyku albo poznawanie historii w Muzeum Obrony Wybrzeża - każdy znajdzie coś dla siebie.",
        None,
        30,
        45,
        100,
        150,
    ),
]

# nazwa, id_adresu, ma byc w adres klucz taki jak tu, koszt, cena dla klienta, nazwa kontrahenta
MIEJSCA_WYCIECZKI = {
    "Morsowanie Międzyzdroje": (
        "Hotel Gromada Międzyzdroje",
        None,
        100,
        150,
        "Siec hoteli Gromada",
    ),
    "Wypoczynek na Helu": (
        "Hotel Gromada Hel",
        None,
        2000,
        3000,
        "Siec hoteli Gromada",
    ),
}

# nazwa, linijka 1, linijka 2, id_miasto(potem), kod pocztowy
ADRESY = {
    "Morsowanie Międzyzdroje": ("ul. Wyzwolenia 1", None, "Międzyzdroje", "72-500"),
    "Wypoczynek na Helu": ("ul. J. Piłsudzkiego 64", None, "Hel", "84-150"),
    "Siec hoteli Gromada biuro": ("ul. Marszałkowska 1", None, "Warszawa", "00-500"),
    "Wypożyczalnia desek surfingowych": (
        "ul. Nadmorska 1",
        None,
        "Międzyzdroje",
        "72-500",
    ),
    "Szkoła kitesurfingu ProKajciarz": ("ul. Pogodna 15", None, "Hel", "84-150"),
}

# koszt, cena dla klienta
KOSZTY_MIASTA = {"Międzyzdroje": (2 * 100, 2 * 150), "Hel": (2 * 150, 2 * 200)}

# nazwa, opis_uslugi, koszt, cena dla klienta, nazwa kontrahenta
# deska - mamy umowe ze dadza tyle desek ile beda potrzebowac klienci
# kurs kitesurfingu - umówiliśmy się z firmą odpowiedzialną za kurs, na to że każdy klient będzie mógł brać udział
RODZAJE_USLUG_DODATKOWYCH = {
    "Deski surfingowe": (
        "Deska surfingowa wypożyczana nad Bałtykiem",
        50,
        80,
        "Wypożyczalnia desek surfingowych",
    ),
    "Kurs kitesurfingu": (
        "Kurs szkoleniowy kitesurfingu po Bałtyku pod okiem doświadczonych instruktorów.",
        1000,
        1500,
        "Szkoła kitesurfingu ProKajciarz",
    ),
}

# klucz to id_wycieczki, wartosc to lista z nazwami uslug
USLUGI_DODATKOWE = {1: ["Deski surfingowe"], 2: ["Kurs kitesurfingu"]}

# nazwa, opis, email, nazwa_adresu
KONTRAHENCI = {
    "Siec hoteli Gromada": (
        "Siec hoteli Gromada",
        "Siec hoteli Gromada działająca w polsce",
        "gromada@office.pl",
        "Siec hoteli Gromada biuro",
    ),
    "Wypożyczalnia desek surfingowych": (
        "Wypożyczalnia desek surfingowych",
        "Wypożyczalnia desek surfingowych działająca nad Bałtykiem",
        "deski.baltyk@gmail.com",
        "Wypożyczalnia desek surfingowych",
    ),
    "Szkoła kitesurfingu ProKajciarz": (
        "Szkoła kitesurfingu Prokajciarz",
        "Kursu kitesurfingu po Bałtyku",
        "kontakt@prokajciarz.com",
        "Szkoła kitesurfingu Prokajciarz",
    ),
}

# nazwa, koszt, cena dla klienta, id_kontrahenta (potem)
KOSZTY_U_KONTRAHENTOW = {
    "Wieczorne ognisko": (50, 80, "Siec hoteli Gromada"),
}

# klucz to nazwa propozycji, wartosc to lista z nazwami z KOSZTY_U_KONTRAHENTOW
PROPOZYCJE_KOSZT_U_KONTRAHENTOW = {"Morsowanie Międzyzdroje": ["Wieczorne ognisko"]}

# klucz to nazwa propozycji, wartosci to (nazwa_transportu, koszty_miasta_klucz)
TRANSPORT_PROPOZYCJA_WYCIECZKI = {
    "Morsowanie Międzyzdroje": ("Autokar 1", "Międzyzdroje"),
    "Wypoczynek na Helu": ("Autokar 2", "Hel"),
}

# klucz to id_wycieczki, wartosc to lista nazw pracownikow
PRACOWNIK_WYCIECZKA = {
    1: ["Kierowca1", "Organizator1"],
    2: ["Kierowca1", "Organizator2"],
    3: ["Kierowca2", "Organizator3"],
}


# klucz to id wycieczki, wartosc to lista z id klientow (one sa od 1)
KLIENCI_WYCIECZKI = {i: [] for i in range(LICZBA_WYCIECZEK)}

for i in range(1, 51):
    KLIENCI_WYCIECZKI[0].append(i)

for i in range(1, 49, randint(1, 3)):
    KLIENCI_WYCIECZKI[1].append(i)

for i in range(51, 97):
    KLIENCI_WYCIECZKI[2].append(i)

# dalej w miary potrzeb dodawanie

# data wyjazdu, data powrotu, liczba osob, nazwa propozycji
WYCIECZKI = [
    (
        datetime(2024, 1, 3, 6, 0, 0),
        datetime(2024, 1, 4, 22, 0, 0),
        50,
        "Morsowanie Międzyzdroje",
    ),
    (
        datetime(2024, 1, 26, 6, 0, 0),
        datetime(2024, 1, 27, 22, 0, 0),
        48,
        "Morsowanie Międzyzdroje",
    ),
    (
        datetime(2024, 7, 14, 7, 0, 0),
        datetime(2024, 7, 28, 7, 0, 0),
        45,
        "Wypoczynek na Helu",
    ),
]

# w pierwszych wycieczkach przelew byl po 7 dniach od zakończenia wycieczki

# pls niech ktos obliczy :(
# kwota, data transakcji, nazwa kontrahenta, id_wycieczki od 1!
TRANSAKCJE_KONTRAHENCI = [
    (500, WYCIECZKI[0][1] + timedelta(days=7), "Siec hoteli Gromada", 1),
    (500, WYCIECZKI[1][1] + timedelta(days=7), "Siec hoteli Gromada", 2),
    (400, WYCIECZKI[1][1] + timedelta(days=7), "Wypożyczalnia desek surfingowych", 1),
]

# kwota, data transakcji, id_klienta, id_wycieczki
TRANSAKCJE_KLIENCI = {}

# klucz to id wycieczki
KOSZTY_KLIENTA_RAZEM = {0: 610, 1: 690, 2: 3550}

# klienci placa do dnia przed wycieczka
for i in range(LICZBA_WYCIECZEK):
    for j in KLIENCI_WYCIECZKI[i]:
        TRANSAKCJE_KLIENCI[(j, i + 1)] = (
            KOSZTY_KLIENTA_RAZEM[i],
            WYCIECZKI[i][0] - timedelta(days=randint(1, 3)),
        )
