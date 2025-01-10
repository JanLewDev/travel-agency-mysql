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

MIASTA = ["Warszawa", "Międzyzdroje", "Karpacz", "Sosnowiec","Legnica", "Szczecinek", "Polanica-Zdrój"]

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

# propozycja - trzydniowa wycieczka z instruktorem narciarstwa, Karpacz
# min osob 10, maks 20
# koszt transportu 100
# koszt miejsca 235
# koszt instruktora 40 za osobe - nasze koszty
# Kontrahent - Pensjonat Jar, ul. Narutowicza 1, 58-540 Karpacz
# email - bogumila.jarska@o2.pl

# propozycja - wakeboardowy, dwudniowy wypad do Szczecinka
# min 30, maks 50
# koszt transportu 130
# wynajem desek, pianki itp: 140 - nasze koszty
# Kontrahent - Hotel Zacisze (sieć Gromada), ul. Polna 25, 78-400 Szczecinek
# ramy czasowe: bardziej letnie

# propozycja - jednodniowa wycieczka, bez kontrahenta typu hotel, PN Góry Stołowe
# min 45, maks 50
# koszt transportu
# obiad w karczmie: koszt 30, cena 65
# kontrahent Karczma "U Krysi"
# ramy czasowe: poza zimą

PROPOZYCJE = [
    (
        "Morsowanie Międzyzdroje",  # nazwa
        "Dwudniowe morsowanie ze zwiedzaniem Międzyzdrojów",  # opis
        None,  # ograniczenia
        45,  # min osob
        50,  # max osob
        40,  # nasze koszty na osobe total
        80,  # cena dla klienta za osobe za nasze koszty
    ),
    (
        "Narty Karpacz",
        "Trzy dni na nartach w Karpaczu z instruktorem",
        None,
        10,
        20,
        40,
        90,
    ),
    (
        "Wakeboard Szczecinek",
        "Dwudniowy wypad na wakeboard na jeziorze Trzesiecko",
        "Umiejętność pływania na wakeboardzie",
        30,
        50,
        140,
        170,
    ),
    (
        "Góry Stołowe",
        "Jednodniowa wycieczka PN Gór Stołowych z obiadem w cenie",
        None,
        45,
        50,
        15,
        30,
    )
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
    "Narty Karpacz": (
        "Pensjonat Jar",
        None,
        235,
        300,
        "Jarska Apartments",
    ),
    "Wakeboard Szczecinek": (
        "Hotel Zacisze",
        None,
        70,
        105,
        "Siec hoteli Gromada",
    ),
    "Góry Stołowe": ( # tutaj wyjątkowo obiad a nie spanie
        "Karczma U Krysi",
        None,
        30,
        65,
        "Swojska Gastronomia",
    )
}

# nazwa, linijka 1, linijka 2, id_miasto(potem), kod pocztowy
ADRESY = {
    "Morsowanie Międzyzdroje": ("ul. Wyzwolenia 1", None, "Międzyzdroje", "72-500"),
    "Siec hoteli Gromada biuro": ("ul. Marszałkowska 1", None, "Warszawa", "00-500"),
    "Wypożyczalnia desek surfingowych": (
        "ul. Nadmorska 1",
        None,
        "Międzyzdroje",
        "72-500",
    ),
    "Narty Karpacz": ("ul. Narutowicza 1", None, "Karpacz", "58-540"),
    "Wypożyczalnia sprzętu narciarskiego": ("ul. Turystyczna 4", None, "Karpacz", "58-540"),
    "Jarska Apartments": ("ul. Hetmańska 2", None, "Legnica", "59-220"),
    "Wakeboard Szczecinek": ("ul. Polna 25", None, "Szczecinek", "78-400"),
    "Wypożyczalnia wakeboardowa": ("ul. Kościuszki 14", None, "Szczecinek", "78-400"),
    "Góry Stołowe": ("ul. Ogrodowa 11", None, "Polanica-Zdrój", "57-320"),
    "Swojska Gastronomia": ("ul. Francuska 18", None, "Warszawa", "03-906"),
    "Górpol": ("ul. Górska 1", None, "Polanica-Zdrój", "57-320"),
}

# koszt, cena dla klienta
KOSZTY_MIASTA = {
    "Międzyzdroje": (2 * 100, 2 * 150),
    "Karpacz": (2 * 65, 2 * 100),
    "Szczecinek": (2 * 90, 2 * 130),
    "Polanica-Zdrój": (2 * 50, 2 * 80),
}

# nazwa, opis_uslugi, koszt, cena dla klienta, nazwa kontrahenta
# deska - mamy umowe ze dadza tyle desek ile beda potrzebowac klienci
# sprzet narciarski - naturalnie tez
RODZAJE_USLUG_DODATKOWYCH = {
    "Deski surfingowe": (
        "Deska surfingowa wypożyczana nad Bałtykiem",
        50,
        80,
        "Wypożyczalnia desek surfingowych",
    ),
    "Sprzęt narciarski" : (
        "Narty i kijki wypożyczane w górach",
        100,
        125,
        "Wypożyczalnia sprzętu narciarskiego",
    ),
    "Wakeboard, pianka, kask": (
        "Sprzęt potrzebny do uprawiania wakeboardingu",
        140,
        175,
        "Wypożyczalnia wakeboardowa",
    ),
    "Kijki do chodzenia": (
        "Kijki ułatwiające poruszenia się po górach",
        15,
        25,
        "Górpol",
    )
}

# klucz to id_wycieczki, wartosc to lista z nazwami uslug
USLUGI_DODATKOWE = {1: ["Deski surfingowe"], 2: ["Sprzęt narciarski"], 3:["Wakeboard, pianka, kask"], 4:["Kijki do chodzenia"]}

# nazwa, opis, email, nazwa_adresu
KONTRAHENCI = {
    "Siec hoteli Gromada": (
        "Siec hoteli Gromada",
        "Siec hoteli Gromada działająca w Polsce",
        "gromada@office.pl",
        "Siec hoteli Gromada biuro",
    ),
    "Wypożyczalnia desek surfingowych": (
        "Wypożyczalnia desek surfingowych",
        "Wypożyczalnia desek surfingowych działająca nad Bałtykiem",
        "deski.baltyk@gmail.com",
        "Wypożyczalnia desek surfingowych",
    ),
    "Wypożyczalnia sprzętu narciarskiego": (
        "Wypożyczalnia sprzętu narciarskiego",
        "Wypożyczalnia sprzętu narciarskiego działająca w górach",
        "ski.rental@tlen.pl",
        "Wypożyczalnia sprzętu narciarskiego",
    ),
    "Jarska Apartments": (
        "Jarska Apartments",
        "Sieć pensjonatów Jarska działające w Polsce",
        "contact.jarska@hotmail.com",
        "Sieć pensjonatów Jarska biuro",
    ),
    "Wypożyczalnia wakeboardowa": (
        "Wypożyczalnia wakeboardowa",
        "Wypożyczalnia desek wakeboardowych, pianek i kasków",
        "wakeboard.szczecinek@wp.pl",
        "Wypożyczalnia wakeboardowa",
    ),
    "Swojska Gastronomia": (
        "Swojska Gastronomia",
        "Firma obsługujące restauracje w Polsce",
        "swojska.gastro@gmail.com",
        "Swojska Gastronomia",
    ),
    "Górpol": (
        "Górpol",
        "Firma zajmująca się górskim sprzętem",
        "gorpol@interia.pl",
        "Górpol",
    ),
}

# nazwa, koszt, cena dla klienta, id_kontrahenta (potem)
KOSZTY_U_KONTRAHENTOW = {
    "Wieczorne ognisko": (50, 80, "Siec hoteli Gromada"),
    "Karkonoskie fondue": (15, 40, "Jarska Apartments"),
    "Masaż misami tybetańskimi": (40, 70, "Siec hoteli Gromada")
}

# klucz to nazwa propozycji, wartosc to lista z nazwami z KOSZTY_U_KONTRAHENTOW
PROPOZYCJE_KOSZT_U_KONTRAHENTOW = {
    "Morsowanie Międzyzdroje": ["Wieczorne ognisko"],
    "Narty Karpacz": ["Karkonoskie fondue"],
    "Wakeboard Szczecinek": ["Masaż misami tybetańskimi"],
}

# klucz to nazwa propozycji, wartosci to (nazwa_transportu, koszty_miasta_klucz)
TRANSPORT_PROPOZYCJA_WYCIECZKI = {
    "Morsowanie Międzyzdroje": ("Autokar 1", "Międzyzdroje"),
    "Narty Karpacz": ("Bus 1", "Karpacz"),
    "Wakeboard Szczecinek": ("Autokar 2", "Szczecinek"),
    "Góry Stołowe": ("Autokar 1", "Polanica-Zdrój"),
}

# klucz to id_wycieczki, wartosc to lista nazw pracownikow
PRACOWNIK_WYCIECZKA = {
    1: ["Kierowca1", "Organizator1"],
    2: ["Kierowca1", "Organizator2"],
    3: ["Kierowca2", "Organizator1"],
    # do ustalenia gdy id wycieczki będą ustawione dopiero imo
}


# klucz to id wycieczki, wartosc to lista z id klientow (one sa od 1)
KLIENCI_WYCIECZKI = {i: [] for i in range(LICZBA_WYCIECZEK)}

for i in range(1, 51):
    KLIENCI_WYCIECZKI[0].append(i)

for i in range(1, 49, randint(1, 3)):
    KLIENCI_WYCIECZKI[1].append(i)

# dalej w miary potrzeb dodawanie

# data wyjazdu, data powrotu, liczba osob, nazwa propozycji
WYCIECZKI = [
    (   #id_wycieczki = 1
        datetime(2024, 1, 3, 6, 0, 0),
        datetime(2024, 1, 4, 22, 0, 0),
        50,
        "Morsowanie Międzyzdroje",
    ),
    (   #id_wycieczki = 2
        datetime(2024, 1, 26, 6, 0, 0),
        datetime(2024, 1, 27, 22, 0, 0),
        48,
        "Morsowanie Międzyzdroje",
    ),
    (   #id_wycieczki = 3
        datetime(2024, 2, 2, 7, 0, 0),
        datetime(2024, 2, 4, 17, 0, 0),
        14,
        "Narty Karpacz",
    ),
    (   #id_wycieczki = 4
        datetime(2024, 2, 9, 7, 0, 0),
        datetime(2024, 2, 11, 17, 0, 0),
        20,
        "Narty Karpacz",
    ),
    (   #id_wycieczki = 5
        datetime(2024, 3, 9, 8, 0, 0),
        datetime(2024, 3, 9, 18, 0, 0),
        49,
        "Góry Stołowe",
    ),
    (   #id_wycieczki = 6
        datetime(2024, 3, 23, 8, 0, 0),
        datetime(2024, 3, 23, 18, 0, 0),
        45,
        "Góry Stołowe",
    ),
]

# w pierwszych wycieczkach przelew byl po 7 dniach od zakończenia wycieczki

# kwota, data transakcji, nazwa kontrahenta, id_wycieczki od 1!
TRANSAKCJE_KONTRAHENCI = [
    (5000, WYCIECZKI[0][1] + timedelta(days=7), "Siec hoteli Gromada", 1),
    (4800, WYCIECZKI[1][1] + timedelta(days=7), "Siec hoteli Gromada", 2),
    (2400, WYCIECZKI[1][1] + timedelta(days=7), "Wypożyczalnia desek surfingowych", 1),
    (3290, WYCIECZKI[2][1] + timedelta(days=7), "Jarska Apartments", 3),
    (20*MIEJSCA_WYCIECZKI["Narty Karpacz"][2], WYCIECZKI[3][1] + timedelta(days=7), "Jarska Apartments", 4),
    (randint(10,14)*RODZAJE_USLUG_DODATKOWYCH["Sprzęt narciarski"][1], WYCIECZKI[2][1] + timedelta(days=7), "Wypożyczalnia sprzętu narciarskiego", 3), # losujemy ile osób nie miało nart i musiało wypożyczyć
    (randint(8,12)*RODZAJE_USLUG_DODATKOWYCH["Sprzęt narciarski"][1], WYCIECZKI[3][1] + timedelta(days=7), "Wypożyczalnia sprzętu narciarskiego", 4),
    (20*KOSZTY_U_KONTRAHENTOW["Karkonoskie fondue"][0], WYCIECZKI[3][1] + timedelta(days=7), "Jarska Apartments", 4),
    (49*MIEJSCA_WYCIECZKI["Góry Stołowe"][2], WYCIECZKI[4][1] + timedelta(days=7), "Swojska Gastronomia", 5),
    (randint(20,30)*RODZAJE_USLUG_DODATKOWYCH["Kijki do chodzenia"][1], WYCIECZKI[4][1] + timedelta(days=7), "Górpol", 5),
    (45*MIEJSCA_WYCIECZKI["Góry Stołowe"][2], WYCIECZKI[5][1] + timedelta(days=7), "Swojska Gastronomia", 6),
    (randint(20,30)*RODZAJE_USLUG_DODATKOWYCH["Kijki do chodzenia"][1], WYCIECZKI[5][1] + timedelta(days=7), "Górpol", 6),
]

# kwota, data transakcji, id_klienta, id_wycieczki
TRANSAKCJE_KLIENCI = {}

# klucz to id wycieczki
KOSZTY_KLIENTA_RAZEM = {
    0: 610,
    1: 690,
}

# klienci placa do dnia przed wycieczka
for i in range(LICZBA_WYCIECZEK):
    for j in KLIENCI_WYCIECZKI[i]:
        TRANSAKCJE_KLIENCI[(j, i + 1)] = (
            KOSZTY_KLIENTA_RAZEM[i],
            WYCIECZKI[i][0] - timedelta(days=randint(1, 3)),
        )
