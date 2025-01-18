"""Modul zawiernajacy stale do wypelnienia bazy danych"""

from datetime import datetime, timedelta
from random import randint
from typing import List, Tuple, Optional, Dict
from collections import defaultdict

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
    "Organizator3": "Organizator",
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
    "Hel": "Polska",
    "Zator": "Polska",
    "Kraków": "Polska"
}

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
        ["Bus 1"],
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
    PropozycjaWycieczki(
        "Wypoczynek na Helu",
        "Polskie morze w ostatnich latach cieszy się coraz większym zainteresowaniem ze strony \
            turystów. Oferujemy dwutygodniowe wakacje na tym malowniczym półwyspie, opalanie się \
                na plaży, pływanie w Bałtyku albo poznawanie historii w Muzeum Obrony Wybrzeża - \
                    każdy znajdzie coś dla siebie.",
        None,
        30,
        45,
        100,
        150,
        "Hel",
        "Hotel Gromada Hel",
        ["Autokar 2"],
    ),
    PropozycjaWycieczki(
        "Emocje w Zatorze",
        "Wizyta w Energylandii, parku linowym oraz escape roomie",
        "Wszyscy uczestnicy powinni mieć wzrost co najmniej 150 cm oraz mieć 12 lat.",
        25,
        45,
        400,
        700,
        "Zator",
        "Hotel Tygrys",
        ["Autokar 1"],
        ["Grupowe pieczenie pianek przy ognisku", "Energylandia"],
    ),
    PropozycjaWycieczki(
        "Królewski Kraków – podróż w serce historii i magii",
        "Odkryj magię królewskiego Krakowa! Wybierz się na niezapomnianą podróż przez Stare Miasto, Wawel i klimatyczny Kazimierz. Zanurz się w historii, podziwiaj zabytki i delektuj się lokalnymi przysmakami. Spacer po królewskich uliczkach, wizyta w Smoczej Jamie i chwila relaksu nad Wisłą to tylko początek tej wyjątkowej przygody!",
        None,
        20,
        30,
        300,
        450,
        "Kraków",
        "Hotel Marriott Kraków",
        ["Autokar 2"],
        []
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
    ),
    "Hotel Marriott Kraków": MiejsceWycieczki(
        "Hotel Marriott Kraków",
        400,
        600,
        "Hotel Marriott Kraków"
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
    "Hotel Gromada Hel": MiejsceWycieczki(
        "Hotel Gromada Hel",
        2000,
        3000,
        "Sieć hoteli Gromada",
    ),
    "Hotel Tygrys": MiejsceWycieczki("Hotel Tygrys", 500, 700, "Hotel Tygrys"),
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
    "Hotel Marriott Kraków": Adres(
        "aleja 3 Maja 51", None, "Kraków", "30-062"
    ),
    "Hotel Marriot biuro": Adres (
        "ul. Dmowskiego 42", None, "Warszawa", "03-906"
    ),
    "Muzeum Schindlera": Adres(
        "ul. Lipowa 4", None, "Kraków","30-702"
    ),
    "Hotel Gromada Hel": Adres("ul. J. Piłsudzkiego 64", None, "Hel", "84-150"),
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
    "Szkoła kitesurfingu ProKajciarz": Adres("ul. Pogodna 15", None, "Hel", "84-150"),
    "Hotel Tygrys": Adres("ul. Wyspiańskiego 35", None, "Zator", "32-640"),
    "Energylandia sp. z o.o.": Adres("aleja 3 Maja 2", None, "Zator", "32-640"),
}

# koszt, cena dla klienta
KOSZTY_MIASTA = {
    "Międzyzdroje": (2 * 100, 2 * 150),
    "Karpacz": (2 * 65, 2 * 100),
    "Szczecinek": (2 * 90, 2 * 130),
    "Polanica-Zdrój": (2 * 50, 2 * 80),
    "Hel": (2 * 150, 2 * 200),
    "Zator": (2 * 200, 2 * 300),
    "Kraków": (2*150, 2*200)
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
    "Kurs kitesurfingu": RodzajUslugiDodatkowej(
        "Kurs kitesurfingu",
        "Kurs szkoleniowy kitesurfingu po Bałtyku pod okiem doświadczonych instruktorów.",
        1000,
        1500,
        "Szkoła kitesurfingu ProKajciarz",
    ),
    "Wizyta w Muzeum Schindlera": RodzajUslugiDodatkowej(
        "Wizyta w Muzeum Schindlera",
        "Wizyta w muzeum opowiadającym historię Krakowa podczas II wojny światowek",
        50,
        70,
        "Muzeum Schindlera"
    )
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
        "Sieć hoteli Gromada działająca w Polsce",
        "gromada@office.pl",
        "Sieć hoteli Gromada biuro",
    ),
    "Hotel Marriott": Kontrahent(
        "Hotel Marriott",
        "Sieć hoteli Marriott działająca w Polsce",
        "marriott@kontakt.com",
        "Sieć hoteli Marriott biuro"
    ),
    "Muzeum Schindlera": Kontrahent(
        "Muzeum Schindlera",
        "Muzeum II wojny światowej w Krakowie",
        "muzeum_schindlera@gmail.com",
        "Muzeum Schindlera"
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
    "Szkoła kitesurfingu ProKajciarz": Kontrahent(
        "Szkoła kitesurfingu ProKajciarz",
        "Szkoła kitesurfingu działająca na Helu",
        "kontakt@prokajciarz.com",
        "Szkoła kitesurfingu ProKajciarz",
    ),
    "Hotel Tygrys": Kontrahent(
        "Hotel Tygrys",
        "Hotel w Zatorze",
        "kontakt@hotel.tygrys.com",
        "ul. Wyspiańskiego 35",
    ),
    "Energylandia sp. z o.o.": Kontrahent(
        "Park rozrywki Energylandia",
        "Największy park rozrywki w Polsce",
        "energylandia@kontakt.com",
        "aleja 3 Maja 2",
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
    "Grupowe pieczenie pianek przy ognisku": KosztUKontrahenta(
        "Grupowe pieczenie pianek przy ognisku", 50, 80, "Hotel Tygrys"
    ),
    "Energylandia": KosztUKontrahenta(
        "Energylandia", 120, 150, "Energylandia sp. z o.o."
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
        transakcje_kontrahenci: List[Tuple[int, str]],  # samo sie oblicza
        koszty_klienta_razem: int,  # samo sie oblicza
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
    start: int, ile: int, jaki_random: Optional[Tuple[int, int]] = None
) -> List[int]:
    """Funkcja zwracajaca liste od min do ile co co_ile"""
    ret = []
    for _ in range(ile):
        ret.append(start)
        start += randint(*jaki_random) if jaki_random else 1
    return ret


WYCIECZKI: List[Wycieczka] = [
    Wycieczka(
        datetime(2024, 1, 3, 6, 0, 0),
        datetime(2024, 1, 4, 22, 0, 0),
        50,
        "Morsowanie Międzyzdroje",
        dokladnie_iles_co_random(1, 50),
        [],
        0,
        ["Kierowca1", "Organizator1"],
    ),
    Wycieczka(
        datetime(2024, 1, 26, 6, 0, 0),
        datetime(2024, 1, 27, 22, 0, 0),
        48,
        "Morsowanie Międzyzdroje",
        dokladnie_iles_co_random(1, 48, (1, 2)),
        [],
        0,
        ["Kierowca1", "Organizator2"],
        ["Deski surfingowe"],
    ),
    Wycieczka(
        datetime(2024, 2, 2, 7, 0, 0),
        datetime(2024, 2, 4, 17, 0, 0),
        14,
        "Narty Karpacz",
        dokladnie_iles_co_random(100, 14),
        [],
        0,
        ["Kierowca2", "Organizator1"],
        ["Sprzęt narciarski"],
    ),
    Wycieczka(
        datetime(2024, 2, 9, 7, 0, 0),
        datetime(2024, 2, 11, 17, 0, 0),
        20,
        "Narty Karpacz",
        dokladnie_iles_co_random(120, 20),  # zaadaptowac
        [],
        0,
        ["Kierowca2", "Organizator1"],
        ["Sprzęt narciarski"],
    ),
    Wycieczka(
        datetime(2024, 3, 9, 8, 0, 0),
        datetime(2024, 3, 9, 18, 0, 0),
        49,
        "Góry Stołowe",
        dokladnie_iles_co_random(140, 49),  # zaadaptowac
        [],
        0,
        ["Kierowca3", "Organizator2"],
        ["Kijki do chodzenia"],
    ),
    Wycieczka(
        datetime(2024, 3, 23, 8, 0, 0),
        datetime(2024, 3, 23, 18, 0, 0),
        45,
        "Góry Stołowe",
        dokladnie_iles_co_random(190, 45),  # zaaadaptowac
        [],
        0,
        ["Kierowca3", "Organizator2"],
        ["Kijki do chodzenia"],
    ),
    Wycieczka(
        datetime(2024,1, 8,7,0,0),
        datetime(2024,1,10,12,0,0),
        23,
        "Królewski Kraków – podróż w serce historii i magii",
        dokladnie_iles_co_random(120, 23),
        [],
        0,
        ["Kierowca2", "Organizator1"],
        ["Wizyta w Muzeum Schindlera"]
    ),
    Wycieczka(
        datetime(2024,12, 8,7,0,0),
        datetime(2024,12,10,12,0,0),
        20,
        "Królewski Kraków – podróż w serce historii i magii",
        dokladnie_iles_co_random(124, 20),
        [],
        0,
        ["Kierowca2", "Organizator1"],

    ),
    Wycieczka(
        datetime(2024,10, 8,7,0,0),
        datetime(2024,10,10,12,0,0),
        30,
        "Królewski Kraków – podróż w serce historii i magii",
        dokladnie_iles_co_random(120, 30),
        [],
        0,
        ["Kierowca2", "Organizator1"],
        ["Wizyta w Muzeum Schindlera"]
    ),
    Wycieczka(
        datetime(2024,4, 8,7,0,0),
        datetime(2024,4,10,12,0,0),
        25,
        "Królewski Kraków – podróż w serce historii i magii",
        dokladnie_iles_co_random(70, 25),
        [],
        0,
        ["Kierowca1", "Organizator1"],
        ["Wizyta w Muzeum Schindlera"]
    ),
    Wycieczka(
        datetime(2024,1, 8,7,0,0),
        datetime(2024,1,10,12,0,0),
        23,
        "Królewski Kraków – podróż w serce historii i magii",
        dokladnie_iles_co_random(70, 23),
        [],
        0,
        ["Kierowca1", "Organizator2"],
        ["Wizyta w Muzeum Schindlera"]
    ),

    Wycieczka(
        datetime(2024, 7, 14, 7, 0, 0),
        datetime(2024, 7, 28, 22, 0, 0),
        45,
        "Wypoczynek na Helu",
        dokladnie_iles_co_random(200, 45),  # zaadaptowac
        [],
        0,
        ["Kierowca2", "Organizator3"],
        ["Kurs kitesurfingu"],
    ),
    Wycieczka(
        datetime(2024, 4, 5, 6, 0, 0),
        datetime(2024, 4, 8, 19, 0, 0),
        38,
        "Emocje w Zatorze",
        dokladnie_iles_co_random(15, 38),  # zaadaptowac
        [],
        0,
        ["Kierowca2", "Organizator2"],
    ),
    Wycieczka(
        datetime(2024, 9, 21, 6, 0, 0),
        datetime(2024, 9, 24, 19, 0, 0),
        25,
        "Emocje w Zatorze",
        dokladnie_iles_co_random(15, 25),  # zaadaptowac
        [],
        0,
        ["Kierowca1", "Organizator1"],
    ),
    Wycieczka(
        datetime(2024, 10, 13, 6, 0, 0),
        datetime(2024, 10, 16, 19, 0, 0),
        30,
        "Emocje w Zatorze",
        dokladnie_iles_co_random(50, 30),  # zaadaptowac
        [],
        0,
        ["Kierowca2", "Organizator1"],
    ),
    Wycieczka(
        datetime(2024, 8, 14, 7, 0, 0),
        datetime(2024, 8, 28, 22, 0, 0),
        36,
        "Wypoczynek na Helu",
        dokladnie_iles_co_random(170, 36),  # zaadaptowac
        [],
        0,
        ["Kierowca1", "Organizator2"],
        [],
    ),
    Wycieczka(
        datetime(2024, 8, 1, 7, 0, 0),
        datetime(2024, 8, 15, 22, 0, 0),
        31,
        "Wypoczynek na Helu",
        dokladnie_iles_co_random(120, 31),  # zaadaptowac
        [],
        0,
        ["Kierowca2", "Organizator3"],
        ["Kurs kitesurfingu"],
    ),
]

# klucz to id wycieczki, od 1
KLIENCI_WYCIECZKI = {
    i: wycieczka.klienci_wycieczki for i, wycieczka in enumerate(WYCIECZKI, start=1)
}


def create_transakcje_kontrahenci():
    """Funkcja tworzaca transakcje kontrahentow"""
    for wycieczka in WYCIECZKI:
        wycieczka.transakcje_kontrahenci = []
        wysokosc_transakcji: Dict[str, int] = defaultdict(lambda: 0)
        ile_osob = wycieczka.liczba_osob
        propozycja = next(
            propozycja
            for propozycja in PROPOZYCJE
            if propozycja.nazwa == wycieczka.nazwa_propozycji
        )
        miejsce_wycieczki = MIEJSCA_WYCIECZKI[propozycja.miejsce_wycieczki_nazwa]
        wysokosc_transakcji[miejsce_wycieczki.nazwa_kontrahenta] += (
            ile_osob * miejsce_wycieczki.koszt
        )

        propozycja_koszty_u_kontrahentow = propozycja.propozycje_koszt_u_kontrahentow
        for koszt_u_kontrahenta in propozycja_koszty_u_kontrahentow or []:
            koszt_u_kontrahenta = KOSZTY_U_KONTRAHENTOW[koszt_u_kontrahenta]
            wysokosc_transakcji[koszt_u_kontrahenta.nazwa_kontrahenta] += (
                ile_osob * koszt_u_kontrahenta.koszt
            )

        for usluga_dodatkowa in wycieczka.uslugi_dodatkowe or []:
            usluga_dodatkowa = RODZAJE_USLUG_DODATKOWYCH[usluga_dodatkowa]
            wysokosc_transakcji[usluga_dodatkowa.nazwa_kontrahenta] += (
                ile_osob * usluga_dodatkowa.koszt
            )

        for nazwa_kontrahenta, kwota in wysokosc_transakcji.items():
            wycieczka.transakcje_kontrahenci.append((kwota, nazwa_kontrahenta))

        print(wycieczka.transakcje_kontrahenci)


def calculate_koszty_klienta_razem():
    """Funckja obliczajaca koszty klienta razem"""
    for wycieczka in WYCIECZKI:
        propozycja = next(
            propozycja
            for propozycja in PROPOZYCJE
            if propozycja.nazwa == wycieczka.nazwa_propozycji
        )
        miejsce_wycieczki = MIEJSCA_WYCIECZKI[propozycja.miejsce_wycieczki_nazwa]
        wycieczka.koszty_klienta_razem = (
            propozycja.cena_dla_kilienta_za_osobe
            + miejsce_wycieczki.cena_dla_kilienta
            + sum(
                (
                    KOSZTY_U_KONTRAHENTOW[koszt_u_kontrahenta].cena_dla_kilienta
                    for koszt_u_kontrahenta in propozycja.propozycje_koszt_u_kontrahentow
                    or []
                ),
                0,
            )
            + sum(
                (
                    RODZAJE_USLUG_DODATKOWYCH[usluga_dodatkowa].cena_dla_kilienta
                    for usluga_dodatkowa in wycieczka.uslugi_dodatkowe or []
                ),
                0,
            )
            + KOSZTY_MIASTA[propozycja.miasto_z_koszty_miasta][1]
        )

        print(wycieczka.nazwa_propozycji, wycieczka.koszty_klienta_razem)


TRANSAKCJE_KONTRAHENCI = []


def gen_transakcje_kontrahenci():
    """Funkcja generujaca transakcje kontrahentow"""
    # w pierwszych wycieczkach przelew byl po 7 dniach od zakończenia wycieczki

    # kwota, data transakcji, nazwa kontrahenta, id_wycieczki od 1!

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


TRANSAKCJE_KLIENCI = []


def gen_transakcje_klienci():
    """Funkcja generujaca transakcje klientow"""
    # kwota, data transakcji, id_klienta, id_wycieczki
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


# Sprawdzenia poprawnosci danych
def test():
    """Funkcja testujaca poprawnosc danych"""
    assert len(TRANSAKCJE_PRACOWNICY) == 12 * len(PRACOWNICY)

    czasy_wycieczek_klienta: Dict[int, List[tuple[datetime, datetime]]] = {}
    for wycieczka in WYCIECZKI:
        propozycja = next(
            propozycja
            for propozycja in PROPOZYCJE
            if propozycja.nazwa == wycieczka.nazwa_propozycji
        )
        assert (
            wycieczka.data_wyjazdu < wycieczka.data_powrotu
        ), f"{wycieczka.nazwa_propozycji} -> koniec przed startem"

        assert (
            propozycja.min_osob <= wycieczka.liczba_osob <= propozycja.max_osob
        ), f"{wycieczka.nazwa_propozycji} -> niepoprawna liczba osob"

        assert (
            len(wycieczka.klienci_wycieczki) == wycieczka.liczba_osob
        ), f"{wycieczka.nazwa_propozycji} -> niepoprawna liczba klientow"

        for klient in wycieczka.klienci_wycieczki:
            if klient not in czasy_wycieczek_klienta:
                czasy_wycieczek_klienta[klient] = []
            czasy_wycieczek_klienta[klient].append(
                (wycieczka.data_wyjazdu, wycieczka.data_powrotu)
            )

    # sprawdzanie czy wycieczki sie nie nakladaja (klienci)
    for klient, czasy in czasy_wycieczek_klienta.items():
        czasy.sort(key=lambda x: x[0])
        if len(czasy) > 1:
            for i in range(1, len(czasy)):
                assert (
                    czasy[i][0] >= czasy[i - 1][1]
                ), f"Klient {klient} ma nakładające się wycieczki"

    # sprawdzanie czy wycieczki sie nie nakladaja (pracownicy)
    czasy_wycieczek_pracownika: Dict[str, List[tuple[datetime, datetime]]] = {}
    for wycieczka in WYCIECZKI:
        for pracownik in wycieczka.pracownicy_wycieczki:
            if pracownik not in czasy_wycieczek_pracownika:
                czasy_wycieczek_pracownika[pracownik] = []
            czasy_wycieczek_pracownika[pracownik].append(
                (wycieczka.data_wyjazdu, wycieczka.data_powrotu)
            )

    for pracownik, czasy in czasy_wycieczek_pracownika.items():
        czasy.sort(key=lambda x: x[0])
        if len(czasy) > 1:
            for i in range(1, len(czasy)):
                assert (
                    czasy[i][0] >= czasy[i - 1][1]
                ), f"Pracownik {pracownik} ma nakładające się wycieczki"


create_transakcje_kontrahenci()
calculate_koszty_klienta_razem()
gen_transakcje_kontrahenci()
gen_transakcje_klienci()
test()

print("Wygenerowano dane wycieczek poprawnie\n\n")
