"""Modul zawiernajacy stale do wypelnienia bazy danych"""

from datetime import datetime, timedelta
from random import randint
from typing import List, Tuple, Optional, Dict

# firma dziala w 2024 roku

LICZBA_KLIENTOW = 250

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
RODZAJE_TRANSPORTU = [
    ("Autokar 1", "Autokar niebieski"),
    ("Autokar 2", "Autokar zielony"),
    ("Bus 1", "Bus czerwony"),
    ("Bus 2", "Bus zolty"),
]
# najpierw zatrudnilismy wszystkich pracownikow,
# a dopiero potem mielismy klientow (duzy kapital zakladowy)

# klucz to miasto, wartosc to kraj
MIASTA = {
    "Warszawa": "Polska",
    "Międzyzdroje": "Polska",
    "Karpacz": "Polska",
    "Sosnowiec": "Polska",
    "Legnica": "Polska",
    "Szczecinek": "Polska",
    "Polanica-Zdrój": "Polska",
}

# transakcje najpierw posortowac
# wyplaty pensji w 2024 roku, 10 dnia kazdego miesiaca
TRANSAKCJE_PRACOWNICY = [
    (datetime(2024, i, 10, 12, 0, 0), pracownik, STANOWISKA[stanowisko])
    for i in range(1, 13)
    for pracownik, stanowisko in PRACOWNICY.items()
]

# koszt, cena dla klienta
KOSZTY_MIASTA = {
    "Międzyzdroje": (2 * 100, 2 * 150),
    "Karpacz": (2 * 65, 2 * 100),
    "Szczecinek": (2 * 90, 2 * 130),
    "Polanica-Zdrój": (2 * 50, 2 * 80),
}

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


class PropozycjaWycieczki:
    """Klasa reprezentujaca propozycje wycieczki"""

    def __init__(
        self,
        nazwa: str,
        opis: str,
        ograniczenia: Optional[str],
        min_osob: int,
        max_osob: int,
        nasze_koszty_na_osobe_total: int,
        cena_dla_kilienta_za_osobe: int,
        miasto_z_koszty_miasta: str,
        miejsce_wycieczki_nazwa: str,
        transport_propozycja_wycieczki: List[str],
        propozycje_koszt_u_kontrahentow: Optional[List[str]] = None,
    ):
        self.nazwa = nazwa
        self.opis = opis
        self.ograniczenia = ograniczenia
        self.min_osob = min_osob
        self.max_osob = max_osob
        self.nasze_koszty_na_osobe_total = nasze_koszty_na_osobe_total
        self.cena_dla_kilienta_za_osobe = cena_dla_kilienta_za_osobe
        self.miasto_z_koszty_miasta = miasto_z_koszty_miasta
        self.miejsce_wycieczki_nazwa = miejsce_wycieczki_nazwa
        self.transport_propozycja_wycieczki = transport_propozycja_wycieczki
        self.propozycje_koszt_u_kontrahentow = propozycje_koszt_u_kontrahentow


PROPOZYCJE: List[PropozycjaWycieczki] = [
    PropozycjaWycieczki(
        "Morsowanie Międzyzdroje",
        "Dwudniowe morsowanie ze zwiedzaniem Międzyzdrojów",
        None,
        45,
        50,
        40,
        80,
        "Międzyzdroje",
        "Hotel Gromada Międzyzdroje",
        ["Autokar 1"],
        ["Wieczorne ognisko"],
    ),
    PropozycjaWycieczki(
        "Narty Karpacz",
        "Trzydniowa wycieczka z instruktorem narciarstwa",
        None,
        10,
        20,
        140,
        235,
        "Karpacz",
        "Pensjonat Jar",
        ["Autokar 2"],
        ["Karkonoskie fondue"],
    ),
    PropozycjaWycieczki(
        "Wakeboard Szczecinek",
        "Dwudniowy wypad na wakeboard na jeziorze Trzesiecko",
        "Umiejętność pływania na wakeboardzie",
        30,
        50,
        140,
        175,
        "Szczecinek",
        "Hotel Zacisze",
        ["Autokar 1"],
        ["Masaż misami tybetańskimi"],
    ),
    PropozycjaWycieczki(
        "Góry Stołowe",
        "Jednodniowa wycieczka PN Góry Stołowe z obiadem w karczmie",
        None,
        45,
        50,
        15,
        30,
        "Polanica-Zdrój",
        "Karczma U Krysi",
        ["Autokar 2"],
    ),
]


class MiejsceWycieczki:
    """Klasa reprezentujaca miejsce wycieczki"""

    def __init__(
        self,
        nazwa: str,
        koszt: int,
        cena_dla_kilienta: int,
        nazwa_kontrahenta: str,
    ):
        self.nazwa = nazwa
        self.koszt = koszt
        self.cena_dla_kilienta = cena_dla_kilienta
        self.nazwa_kontrahenta = nazwa_kontrahenta


# klucz to nazwa miejsca wycieczki
MIEJSCA_WYCIECZKI: Dict[str, MiejsceWycieczki] = {
    "Hotel Gromada Międzyzdroje": MiejsceWycieczki(
        "Hotel Gromada Międzyzdroje",
        100,
        150,
        "Sieć hoteli Gromada",
    ),
    "Pensjonat Jar": MiejsceWycieczki(
        "Pensjonat Jar",
        235,
        300,
        "Jarska Apartments",
    ),
    "Hotel Zacisze": MiejsceWycieczki(
        "Hotel Zacisze",
        70,
        105,
        "Sieć hoteli Gromada",
    ),
    "Karczma U Krysi": MiejsceWycieczki(
        "Karczma U Krysi",
        30,
        65,
        "Swojska Gastronomia",
    ),
}


class Adres:
    """Klasa reprezentujaca adres"""

    def __init__(
        self,
        adres: str,
        adres2: Optional[str],
        miasto: str,
        kod_pocztowy: str,
    ):
        self.adres = adres
        self.adres2 = adres2
        self.miasto = miasto
        self.kod_pocztowy = kod_pocztowy


ADRESY: Dict[str, Adres] = {
    "Hotel Gromada Międzyzdroje": Adres(
        "ul. Wyzwolenia 1", None, "Międzyzdroje", "72-500"
    ),
    "Sieć hoteli Gromada": Adres("ul. Marszałkowska 1", None, "Warszawa", "00-500"),
    "Wypożyczalnia desek surfingowych": Adres(
        "ul. Nadmorska 1", None, "Międzyzdroje", "72-500"
    ),
    "Narty Karpacz": Adres("ul. Narutowicza 1", None, "Karpacz", "58-540"),
    "Wypożyczalnia sprzętu narciarskiego": Adres(
        "ul. Turystyczna 4",
        None,
        "Karpacz",
        "58-540",
    ),
    "Jarska Apartments": Adres("ul. Hetmańska 2", None, "Legnica", "59-220"),
    "Pensjonat Jar": Adres("ul. Narutowicza 1", None, "Karpacz", "58-540"),
    "Hotel Zacisze": Adres("ul. Polna 25", None, "Szczecinek", "78-400"),
    "Wakeboard Szczecinek": Adres("ul. Polna 25", None, "Szczecinek", "78-400"),
    "Wypożyczalnia wakeboardowa": Adres(
        "ul. Kościuszki 14", None, "Szczecinek", "78-400"
    ),
    "Góry Stołowe": Adres("ul. Ogrodowa 11", None, "Polanica-Zdrój", "57-320"),
    "Swojska Gastronomia": Adres("ul. Francuska 18", None, "Warszawa", "03-906"),
    "Karczma U Krysi": Adres("ul. Górska 10", None, "Polanica-Zdrój", "57-320"),
    "Górpol": Adres("ul. Górska 1", None, "Polanica-Zdrój", "57-320"),
}

# koszt, cena dla klienta
KOSZTY_MIASTA = {
    "Międzyzdroje": (2 * 100, 2 * 150),
    "Karpacz": (2 * 65, 2 * 100),
    "Szczecinek": (2 * 90, 2 * 130),
    "Polanica-Zdrój": (2 * 50, 2 * 80),
}

# deska - mamy umowe ze dadza tyle desek ile beda potrzebowac klienci
# sprzet narciarski - naturalnie tez


class RodzajUslugiDodatkowej:
    """Klasa reprezentujaca rodzaj uslugi dodatkowej"""

    def __init__(
        self,
        nazwa: str,
        opis: str,
        koszt: int,
        cena_dla_kilienta: int,
        nazwa_kontrahenta: str,
    ):
        self.nazwa = nazwa
        self.opis = opis
        self.koszt = koszt
        self.cena_dla_kilienta = cena_dla_kilienta
        self.nazwa_kontrahenta = nazwa_kontrahenta


RODZAJE_USLUG_DODATKOWYCH: Dict[str, RodzajUslugiDodatkowej] = {
    # deska - mamy umowe ze dadza tyle desek ile beda potrzebowac klienci
    "Deski surfingowe": RodzajUslugiDodatkowej(
        "Deski surfingowe",
        "Deska surfingowa wypożyczana nad Bałtykiem",
        50,
        80,
        "Wypożyczalnia desek surfingowych",
    ),
    "Sprzęt narciarski": RodzajUslugiDodatkowej(
        "Sprzęt narciarski",
        "Narty i kijki wypożyczane w górach",
        100,
        125,
        "Wypożyczalnia sprzętu narciarskiego",
    ),
    "Wakeboard, pianka, kask": RodzajUslugiDodatkowej(
        "Wakeboard, pianka, kask",
        "Sprzęt potrzebny do uprawiania wakeboardingu",
        140,
        175,
        "Wypożyczalnia wakeboardowa",
    ),
    "Kijki do chodzenia": RodzajUslugiDodatkowej(
        "Kijki do chodzenia",
        "Kijki ułatwiające poruszenia się po górach",
        15,
        25,
        "Górpol",
    ),
}


class Kontrahent:
    """Klasa reprezentujaca kontrahenta"""

    def __init__(self, nazwa: str, opis: Optional[str], email: str, adres: str):
        self.nazwa = nazwa
        self.opis = opis
        self.email = email
        self.adres = adres


KONTRAHENCI: Dict[str, Kontrahent] = {
    "Sieć hoteli Gromada": Kontrahent(
        "Sieć hoteli Gromada",
        "Sieć hoteli Gromada działająca w polsce",
        "gromada@office.pl",
        "Sieć hoteli Gromada biuro",
    ),
    "Wypożyczalnia desek surfingowych": Kontrahent(
        "Wypożyczalnia desek surfingowych",
        "Wypożyczalnia desek surfingowych działająca nad Bałtykiem",
        "deski.baltyk@gmail.com",
        "Wypożyczalnia desek surfingowych",
    ),
    "Wypożyczalnia sprzętu narciarskiego": Kontrahent(
        "Wypożyczalnia sprzętu narciarskiego",
        "Wypożyczalnia sprzętu narciarskiego działająca w górach",
        "ski.rental@tlen.pl",
        "Wypożyczalnia sprzętu narciarskiego",
    ),
    "Jarska Apartments": Kontrahent(
        "Jarska Apartments",
        "Sieć pensjonatów Jarska działające w Polsce",
        "contact.jarska@hotmail.com",
        "Sieć pensjonatów Jarska biuro",
    ),
    "Wypożyczalnia wakeboardowa": Kontrahent(
        "Wypożyczalnia wakeboardowa",
        "Wypożyczalnia desek wakeboardowych, pianek i kasków",
        "wakeboard.szczecinek@wp.pl",
        "Wypożyczalnia wakeboardowa",
    ),
    "Swojska Gastronomia": Kontrahent(
        "Swojska Gastronomia",
        "Firma obsługujące restauracje w Polsce",
        "swojska.gastro@gmail.com",
        "Swojska Gastronomia",
    ),
    "Górpol": Kontrahent(
        "Górpol",
        "Firma zajmująca się górskim sprzętem",
        "gorpol@interia.pl",
        "Górpol",
    ),
}


class KosztUKontrahenta:
    """Klasa reprezentujaca koszt u kontrahenta"""

    def __init__(
        self, nazwa: str, koszt: int, cena_dla_kilienta: int, nazwa_kontrahenta: str
    ):
        self.nazwa = nazwa
        self.koszt = koszt
        self.cena_dla_kilienta = cena_dla_kilienta
        self.nazwa_kontrahenta = nazwa_kontrahenta


KOSZTY_U_KONTRAHENTOW: Dict[str, KosztUKontrahenta] = {
    "Wieczorne ognisko": KosztUKontrahenta(
        "Wieczorne ognisko", 50, 80, "Sieć hoteli Gromada"
    ),
    "Karkonoskie fondue": KosztUKontrahenta(
        "Karkonoskie fondue", 15, 40, "Jarska Apartments"
    ),
    "Masaż misami tybetańskimi": KosztUKontrahenta(
        "Masaż misami tybetańskimi", 40, 70, "Sieć hoteli Gromada"
    ),
}


class Wycieczka:
    """Klasa reprezentujaca wycieczke"""

    def __init__(
        self,
        data_wyjazdu: datetime,
        data_powrotu: datetime,
        liczba_osob: int,
        nazwa_propozycji: str,
        klienci_wycieczki: List[int],  # id klientow od 1
        transakcje_kontrahenci: List[Tuple[int, str]],  # kwota, nazwa kontrahenta
        koszty_klienta_razem: int,
        pracownicy_wycieczki: List[str],
        uslugi_dodatkowe: Optional[List[str]] = None,
    ):
        self.data_wyjazdu = data_wyjazdu
        self.data_powrotu = data_powrotu
        self.liczba_osob = liczba_osob
        self.nazwa_propozycji = nazwa_propozycji
        self.klienci_wycieczki = klienci_wycieczki
        self.transakcje_kontrahenci = transakcje_kontrahenci
        self.koszty_klienta_razem = koszty_klienta_razem
        self.pracownicy_wycieczki = pracownicy_wycieczki
        self.uslugi_dodatkowe = uslugi_dodatkowe


def dokladnie_iles_co_random(
    start: int, ile: int, jaki_random: Tuple[int, int]
) -> List[int]:
    """Funkcja zwracajaca liste od min do ile co co_ile"""
    ret = []
    for _ in range(ile):
        ret.append(start)
        start += randint(*jaki_random)
    return ret


WYCIECZKI: List[Wycieczka] = [
    Wycieczka(
        datetime(2024, 1, 3, 6, 0, 0),
        datetime(2024, 1, 4, 22, 0, 0),
        50,
        "Morsowanie Międzyzdroje",
        range(1, 51),
        [(5000, "Sieć hoteli Gromada")],
        610,
        ["Kierowca1", "Organizator1"],
    ),
    Wycieczka(
        datetime(2024, 1, 26, 6, 0, 0),
        datetime(2024, 1, 27, 22, 0, 0),
        48,
        "Morsowanie Międzyzdroje",
        dokladnie_iles_co_random(1, 48, (1, 2)),
        [(4800, "Sieć hoteli Gromada"), (2400, "Wypożyczalnia desek surfingowych")],
        690,
        ["Kierowca1", "Organizator2"],
        ["Deski surfingowe"],
    ),
    Wycieczka(
        datetime(2024, 2, 2, 7, 0, 0),
        datetime(2024, 2, 4, 17, 0, 0),
        14,
        "Narty Karpacz",
        range(100, 114),  # zaadaptowac
        [
            (3290, "Jarska Apartments"),
            (
                randint(10, 14) * RODZAJE_USLUG_DODATKOWYCH["Sprzęt narciarski"].koszt,
                "Wypożyczalnia sprzętu narciarskiego",
            ),
        ],
        20,  # poprawic
        ["Kierowca2", "Organizator1"],
        ["Sprzęt narciarski"],
    ),
    Wycieczka(
        datetime(2024, 2, 9, 7, 0, 0),
        datetime(2024, 2, 11, 17, 0, 0),
        20,
        "Narty Karpacz",
        range(120, 140),  # zaadaptowac
        [
            (
                20 * 235 + 20 * KOSZTY_U_KONTRAHENTOW["Karkonoskie fondue"].koszt,
                "Jarska Apartments",
            ),
            (
                20 * RODZAJE_USLUG_DODATKOWYCH["Sprzęt narciarski"].koszt,
                "Wypożyczalnia sprzętu narciarskiego",
            ),
        ],
        20,  # poprawic
        ["Kierowca2", "Organizator1"],
        ["Sprzęt narciarski"],
    ),
    Wycieczka(
        datetime(2024, 3, 9, 8, 0, 0),
        datetime(2024, 3, 9, 18, 0, 0),
        49,
        "Góry Stołowe",
        range(140, 189),  # zaadaptowac
        [
            (49 * MIEJSCA_WYCIECZKI["Karczma U Krysi"].koszt, "Swojska Gastronomia"),
            (49 * RODZAJE_USLUG_DODATKOWYCH["Kijki do chodzenia"].koszt, "Górpol"),
        ],
        20,  # poprawic
        ["Kierowca3", "Organizator2"],
        ["Kijki do chodzenia"],
    ),
    Wycieczka(
        datetime(2024, 3, 23, 8, 0, 0),
        datetime(2024, 3, 23, 18, 0, 0),
        45,
        "Góry Stołowe",
        range(190, 235),  # zaaadaptowac
        [
            (45 * MIEJSCA_WYCIECZKI["Karczma U Krysi"].koszt, "Swojska Gastronomia"),
            (45 * RODZAJE_USLUG_DODATKOWYCH["Kijki do chodzenia"].koszt, "Górpol"),
        ],
        20,
        ["Kierowca3", "Organizator2"],
        ["Kijki do chodzenia"],
    ),
]

# klucz to id wycieczki, od 1
KLIENCI_WYCIECZKI = {
    i: wycieczka.klienci_wycieczki for i, wycieczka in enumerate(WYCIECZKI, start=1)
}


# w pierwszych wycieczkach przelew byl po 7 dniach od zakończenia wycieczki

# kwota, data transakcji, nazwa kontrahenta, id_wycieczki od 1!
TRANSAKCJE_KONTRAHENCI = []

for i, wycieczka in enumerate(WYCIECZKI, start=1):
    for j in wycieczka.transakcje_kontrahenci:
        TRANSAKCJE_KONTRAHENCI.append(
            (
                j[0],
                wycieczka.data_powrotu + timedelta(days=7),
                j[1],
                i,
            )
        )

TRANSAKCJE_KONTRAHENCI.sort(key=lambda x: x[1])


# kwota, data transakcji, id_klienta, id_wycieczki
TRANSAKCJE_KLIENCI = []

# klienci placa do dnia przed wycieczka
for i, wycieczka in enumerate(WYCIECZKI, start=1):
    for j in KLIENCI_WYCIECZKI[i]:
        TRANSAKCJE_KLIENCI.append(
            (
                wycieczka.koszty_klienta_razem,
                wycieczka.data_wyjazdu - timedelta(days=randint(1, 3)),
                j,
                i,
            )
        )

TRANSAKCJE_KLIENCI.sort(key=lambda x: x[1])
