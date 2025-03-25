import random
import csv
from datetime import datetime, timedelta

# Funkcja do losowania liczby z określonych przedziałów z wagami
def losuj_liczbe_z_przedzialu():
    przedzialy = [
        (2, 2),     # Przedział 2-2, czyli tylko 2
        (3, 9),     # Przedział od 3 do 9
        (10, 24),   # Przedział od 10 do 24
        (25, 50)    # Przedział od 25 do 50
    ]
    
    wagi = [0.3, 0.25, 0.35, 0.1]  # Wagi dla każdego przedziału

    # Losowanie przedziału z odpowiednią wagą
    wylosowany_przedzial = random.choices(przedzialy, weights=wagi, k=1)[0]

    # Losowanie liczby z wylosowanego przedziału
    wylosowana_liczba = random.randint(wylosowany_przedzial[0], wylosowany_przedzial[1])
    
    return wylosowana_liczba

# Funkcja do generowania dat wyjazdu i daty kupna dla każdego tygodnia
def generuj_wyjazdy_i_zakupy(start_date, end_date):
    current_date = start_date + timedelta(days=(7 - start_date.weekday()))  # Przesunięcie do najbliższego poniedziałku
    dane_wycieczki = []  # Lista na przechowywanie wyników

    while current_date <= end_date:
        # Losowanie liczby dni przed wyjazdem na zakup
        max_przedzial = min((current_date - start_date).days, 10)
        dni_przed_wyjazdem = random.randint(1, max_przedzial)
        data_kupna = current_date - timedelta(days=dni_przed_wyjazdem)
        
        # Losujemy liczbę rekordów dla tej daty wyjazdu/kupna
        liczba_rekordow = losuj_liczbe_z_przedzialu()
        
        # Losowanie wspólnych wartości dla całego zestawu
        id_wycieczki = random.randint(1, 13)  # Losujemy id_wycieczki (wspólne dla grupy)
        id_pracownika = random.randint(1, 6)  # Losujemy id_pracownika (wspólne dla grupy)

        for _ in range(liczba_rekordow):
            id_klienta = random.randint(1, 500)   # Losujemy id_klienta (indywidualne dla każdego rekordu)

            # Dodajemy rekord do listy wyników
            dane_wycieczki.append({
                "id_wycieczki": id_wycieczki,
                "id_klienta": id_klienta,
                "datakupna": data_kupna.strftime('%Y-%m-%d'),
                "datawyjazdu": current_date.strftime('%Y-%m-%d'),
                "id_pracownika": id_pracownika
            })

        # Przesunięcie do następnego poniedziałku (tydzień do przodu)
        current_date += timedelta(weeks=1)
    
    return dane_wycieczki

# Funkcja do zapisu danych do pliku CSV
def zapisz_do_csv(dane, nazwa_pliku):
    with open(nazwa_pliku, mode='w', newline='', encoding='utf-8') as plik_csv:
        fieldnames = ["id_wycieczki", "id_klienta", "datakupna", "datawyjazdu", "id_pracownika"]
        writer = csv.DictWriter(plik_csv, fieldnames=fieldnames)

        writer.writeheader()  # Zapis nagłówków
        for rekord in dane:
            writer.writerow(rekord)

# Zakres dat od 1-1-2024 do dzisiaj
start_date = datetime(2024, 1, 1)
end_date = datetime.now()

# Generowanie danych
dane = generuj_wyjazdy_i_zakupy(start_date, end_date)

# Zapis danych do pliku CSV
zapisz_do_csv(dane, "zrealizowane_wycieczki.csv")

print(f"Wygenerowano {len(dane)} rekordów i zapisano do pliku 'zrealizowane_wycieczki.csv'.")

