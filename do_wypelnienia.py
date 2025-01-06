"""Modul zawiernajacy stale do wypelnienia bazy danych"""

# firma dziala w 2024 roku

LICZBA_KLIENTOW = 50

STANOWISKA = {
    "Kierownik": 10000,
    "Kierowca": 5000,
    "Przewodnik": 6000,
    "Pracownik biurowy": 4666,
    "Marketingowiec": 5500,
}

PRACOWNICY = {
    "Kierownik": (10000, "Kierownik"),
    "Kierowca1": (5000, "Kierowca"),
    "Kierowca2": (5000, "Kierowca"),
    "Przewodnik1": (6000, "Przewodnik, język angielski"),
    "Przewodnik2": (6000, "Przewodnik, język niemiecki"),
    "Przewodnik3": (6000, "Przewodnik, język francuski"),
    "Pracownik biurowy": (4666, "Pracownik biurowy"),
    "Marketingowiec": (5500, "Marketingowiec"),
}

# najpierw zatrudnilismy wszystkich pracownikow,
# a dopiero potem mielismy klientow (duzy kapital zakladowy)
LICZBA_NUMEROW_TELEFONOW = LICZBA_KLIENTOW + len(PRACOWNICY)


# wyplaty pensji w 2024 roku, 10 dnia kazdego miesiaca
