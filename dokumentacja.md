# Dokumentacja

## Struktura projektu

```
.
├── dane_statystyczne/
│ ├── imiona_nadane_dzieciom.csv
│ ├── nazwiska_meskie.csv
│ └── nazwiska_zenskie.csv
├── wypelnienie/
│ ├── custom_util.py
│ ├── do_wypelnienia.py
│ ├── sql.py
│ └── wypelnienie.py
├── .env.example
├── .gitignore
├── dokumentacja.md
├── LICENSE
├── README.md
├── requirements.txt
└── schemat_bazy_danych.vuerd
```

## Instrukcja do uruchomienia

Aby uruchomić projekt potrzebny jest Python w wersji 3.9 lub nowszej.

Po sklonowaniu repozytorium należy zainstalować wymagane moduły Pythona:

```bash
pip install -r requirements.txt
```

Następnie należy skopiować plik `.env.example` i zmienić jego nazwę na `.env`. W pliku tym należy podać dane do połączenia z bazą danych.

```bash
cp .env.example .env
vim .env
```

Po zainstalowaniu modułów i uzupełnieniu pliku `.env` można uruchomić skrypt `wypelnienie/wypelnienie.py`.

```bash
python wypelnienie/wypelnienie.py
```

## Spis technologii

Moduły Pythona:
pandas
matplotlib
mysql-connector-python
python-dotenv

Inne:
ERD editor dodatek do VSC
Inline SQL dodatek do VSC

Dane statystyczne imion i nazwisk:
<https://dane.gov.pl/en/dataset/1681,nazwiska-osob-zyjacych-wystepujace-w-rejestrze-pesel>
<https://dane.gov.pl/en/dataset/219,imiona-nadawane-dzieciom-w-polsce>
