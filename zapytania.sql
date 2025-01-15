-- Najpopularniejsze rodzaje wycieczek
SELECT
    pw.nazwa AS "Rodzaj wycieczki",
    SUM(w.liczba_osob) AS "Liczba uczestników",
    SUM(pw.maks_liczba_osob) AS "Maksymalna liczba uczestników",
    (SUM(w.liczba_osob) / SUM(pw.maks_liczba_osob)) * 100 AS "Procent popularności"
FROM
    wycieczki w
JOIN
    propozycje_wycieczki pw ON w.id_propozycji = pw.id_propozycji
GROUP BY
    pw.nazwa
ORDER BY
    (SUM(w.liczba_osob) / SUM(pw.maks_liczba_osob)) * 100 DESC;


-- Porównanie kosztów i zysków wycieczek
SELECT
    w.id_wycieczki,
    SUM(kuk.koszt) AS "Koszt całkowity",
    SUM(tk.kwota) AS "Zysk całkowity",
    (SUM(tk.kwota) - SUM(kuk.koszt) - (SUM(tk.kwota) * 0.187)) AS "Zysk netto"
FROM
    wycieczki w
JOIN
    propozycje_wycieczki pw ON w.id_propozycji = pw.id_propozycji
JOIN
    propozycja_koszt_u_kontrahenta pkuk ON pw.id_propozycji = pkuk.id_propozycji
JOIN
    koszty_u_kontrahentow kuk ON pkuk.id_kosztu_u_kontrahenta = kuk.id_kosztu_u_kontrahenta
JOIN
    transakcje_klienci tk ON w.id_wycieczki = tk.id_wycieczki
GROUP BY
    w.id_wycieczki
ORDER BY
    (SUM(tk.kwota) - SUM(kuk.koszt) - (SUM(tk.kwota) * 0.187)) DESC;


-- Wycieczki, po których klienci wracają na kolejne
SELECT
    w.id_wycieczki,
    w.czas_wyjazdu,
    w.czas_powrotu,
    COUNT(DISTINCT k.id_klienta) AS "Liczba klientów",
    COUNT(DISTINCT CASE WHEN k.id_klienta IN (
        SELECT
            kw2.id_klienta
        FROM
            klient_wycieczka kw2
        WHERE
            kw2.id_wycieczki != w.id_wycieczki
    ) THEN k.id_klienta END) AS Liczba_powracajacych_klientow,
    (COUNT(DISTINCT CASE WHEN k.id_klienta IN (
        SELECT
            kw2.id_klienta
        FROM
            klient_wycieczka kw2
        WHERE
            kw2.id_wycieczki != w.id_wycieczki
    ) THEN k.id_klienta END) / COUNT(DISTINCT k.id_klienta)) * 100 AS "Procent powracających klientów"
FROM
    wycieczki w
JOIN
    klient_wycieczka kw ON w.id_wycieczki = kw.id_wycieczki
JOIN
    klienci k ON kw.id_klienta = k.id_klienta
GROUP BY
    w.id_wycieczki
ORDER BY
    Liczba_powracajacych_klientow DESC;


-- Wycieczki, po których klienci nie wracają
SELECT
    w.id_wycieczki,
    w.czas_wyjazdu,
    w.czas_powrotu,
    COUNT(DISTINCT k.id_klienta) AS "Liczba klientów, którzy nie wracają",
    (COUNT(DISTINCT k.id_klienta) / (SELECT COUNT(DISTINCT k2.id_klienta)
                                     FROM klient_wycieczka kw2
                                     JOIN klienci k2 ON kw2.id_klienta = k2.id_klienta
                                     WHERE kw2.id_wycieczki = w.id_wycieczki)) * 100 AS Procent_klientów_którzy_nie_wracają
FROM
    wycieczki w
JOIN
    klient_wycieczka kw ON w.id_wycieczki = kw.id_wycieczki
JOIN
    klienci k ON kw.id_klienta = k.id_klienta
WHERE
    k.id_klienta NOT IN (
        SELECT
            kw2.id_klienta
        FROM
            klient_wycieczka kw2
        WHERE
            kw2.id_wycieczki != w.id_wycieczki
    )
GROUP BY
    w.id_wycieczki
ORDER BY
    Procent_klientów_którzy_nie_wracają DESC;


-- Liczba obsłużonych klientów w każdym miesiącu działalności firmy
SELECT
    DATE_FORMAT(tk.data_transakcji, '%Y-%m') AS Miesiąc,
    COUNT(DISTINCT tk.id_klienta) AS "Liczba obsłużonych klientów"
FROM
    transakcje_klienci tk
GROUP BY
    DATE_FORMAT(tk.data_transakcji, '%Y-%m')
ORDER BY
    Miesiąc;


-- Najbardziej dochodowi kontrahenci
SELECT k.nazwa, SUM(t.kwota) AS Dochód
FROM transakcje_kontrahenci t
JOIN kontrahenci k ON t.id_kontrahenta = k.id_kontrahenta
GROUP BY k.nazwa
ORDER BY Dochód DESC;


-- Najbardziej dochodowe usługi dodatkowe
SELECT
    rud.nazwa AS usluga_dodatkowa,
    SUM(rud.cena_dla_klienta - rud.koszt) AS zysk
FROM
    uslugi_dodatkowe ud
JOIN
    rodzaje_uslug_dodatkowych rud ON ud.id_uslugi = rud.id_uslugi_dodatkowej
GROUP BY
    rud.nazwa
ORDER BY
    zysk DESC;


-- Proporcja kobiet do mężczyzn w poszczególnych wycieczkach
SELECT
    w.id_wycieczki,
    SUM(CASE WHEN k.plec = 'K' THEN 1 ELSE 0 END) AS liczba_kobiet,
    SUM(CASE WHEN k.plec = 'M' THEN 1 ELSE 0 END) AS liczba_mezczyzn,
    (SUM(CASE WHEN k.plec = 'K' THEN 1 ELSE 0 END) / SUM(CASE WHEN k.plec = 'M' THEN 1 ELSE 0 END)) AS "Proporcja kobiet do mężczyzn"
FROM
    wycieczki w
JOIN
    klient_wycieczka kw ON w.id_wycieczki = kw.id_wycieczki
JOIN
    klienci k ON kw.id_klienta = k.id_klienta
GROUP BY
    w.id_wycieczki;


-- Ile dni w miesiącu było z wycieczkami, jaki to procent
SELECT
    MONTH(czas_wyjazdu) AS miesiac,
    SUM(DATEDIFF(LEAST(LAST_DAY(czas_wyjazdu), czas_powrotu), czas_wyjazdu) + 1) AS dni_w_miesiacu,
    (SUM(DATEDIFF(LEAST(LAST_DAY(czas_wyjazdu), czas_powrotu), czas_wyjazdu) + 1) / DAY(LAST_DAY(czas_wyjazdu))) * 100 AS "Procent dni z wycieczkami w miesiącu"
FROM
    wycieczki
GROUP BY
    MONTH(czas_wyjazdu);


-- Ranking klientów pod względem wydatków
SELECT
    k.id_klienta,
    k.imie,
    k.nazwisko,
    SUM(tk.kwota) AS "Łączne wydatki"
FROM
    klienci k
JOIN
    transakcje_klienci tk ON k.id_klienta = tk.id_klienta
GROUP BY
    k.id_klienta, k.imie, k.nazwisko
ORDER BY
    SUM(tk.kwota) DESC, k.id_klienta;


-- Średnia długość wycieczki
SELECT AVG(DATEDIFF(czas_powrotu, czas_wyjazdu) + 1) AS "Średnia długość wycieczki"
FROM wycieczki;


-- Zyski i koszty w zależności od długości wycieczki
SELECT
    CASE
        WHEN DATEDIFF(w.czas_powrotu, w.czas_wyjazdu) + 1 <= 3 THEN 'Do 3 dni'
        ELSE 'Dłuższa niż 3 dni'
    END AS czas_trwania,
    SUM(tk.kwota) AS zyski,
    SUM(pw.nasze_koszty_razem) AS koszty
FROM
    wycieczki w
JOIN
    transakcje_klienci tk ON w.id_wycieczki = tk.id_wycieczki
JOIN
    propozycje_wycieczki pw ON w.id_propozycji = pw.id_propozycji
GROUP BY
    czas_trwania;