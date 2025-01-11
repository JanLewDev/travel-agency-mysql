"""Modul zawiernajacy stale do wypelnienia bazy danych"""

from datetime import datetime, timedelta
from random import randint
from typing import List, Tuple, Optional, Dict

# firma dziala w 2024 roku

LICZBA_KLIENTOW = 200

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
}

# propozycja - dwudniowe morsowanie w Międzyzdrojach w styczniu
# min osob 45, maks 50
# koszt transportu 150
# koszt miejsca 150
# koszt przewodnika 10 - nasze koszty + 30 jedzenie (prowiant)
# Kontrahent - Hotel Gromada, ul. Wyzwolenia 1, 72-500 Międzyzdroje
# email - gromada.top@gmail.com
# wyjazdy


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
    )
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
    )
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
}


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
        [(500, "Sieć hoteli Gromada")],
        610,
        ["Kierowca1", "Organizator1"],
    ),
    Wycieczka(
        datetime(2024, 1, 26, 6, 0, 0),
        datetime(2024, 1, 27, 22, 0, 0),
        48,
        "Morsowanie Międzyzdroje",
        dokladnie_iles_co_random(1, 48, (2, 3)),
        [(500, "Sieć hoteli Gromada"), (400, "Wypożyczalnia desek surfingowych")],
        690,
        ["Kierowca1", "Organizator2"],
        ["Deski surfingowe"],
    ),
]

# klucz to id wycieczki, od 1
KLIENCI_WYCIECZKI = {
    i + 1: WYCIECZKI[i].klienci_wycieczki for i in range(len(WYCIECZKI))
}


# w pierwszych wycieczkach przelew byl po 7 dniach od zakończenia wycieczki

# pls niech ktos obliczy :(
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


# kwota, data transakcji, id_klienta, id_wycieczki
TRANSAKCJE_KLIENCI = []

# klienci placa do dnia przed wycieczka
for i, wycieczka in enumerate(WYCIECZKI, start=1):
    for j in KLIENCI_WYCIECZKI[i + 1]:
        TRANSAKCJE_KLIENCI.append(
            (
                wycieczka.koszty_klienta_razem,
                wycieczka.data_wyjazdu - timedelta(days=randint(1, 3)),
                j,
                i,
            )
        )
