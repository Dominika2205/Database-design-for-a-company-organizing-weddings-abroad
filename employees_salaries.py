import pandas as pd
from datetime import datetime

# Wczytanie plików
zrealizowane_df = pd.read_csv('zrealizowane_wycieczki.csv')
wycieczki_df = pd.read_csv('wycieczki.csv', sep=';')

# Grupowanie po kluczowych kolumnach (id_wycieczki, id_pracownika, datakupna) i zliczanie liczby unikalnych klientów
grouped_df = zrealizowane_df.groupby(['id_wycieczki', 'id_pracownika', 'datakupna'], as_index=False).agg({
    'id_klienta': 'nunique'
}).rename(columns={'id_klienta': 'count'})

# Debug: Sprawdzenie liczby uczestników po grupowaniu
print("Grupowane dane (po unikalnych klientach):")
print(grouped_df)

# Funkcja do przypisywania prowizji na podstawie liczby uczestników
def calculate_commission(row, wycieczki_df):
    wycieczka = wycieczki_df[wycieczki_df['id'] == row['id_wycieczki']]
    if wycieczka.empty:
        print(f"Brak danych o wycieczce dla ID {row['id_wycieczki']}. Prowizja = 0.")
        return 0  # Brak danych o wycieczce, prowizja = 0
    
    liczba_osob = row['count']  # Liczba uczestników w grupie
    wycieczka = wycieczka.iloc[0]
    
    # Warunki dla różnych progów liczby uczestników
    if 1 <= liczba_osob <= 2:
        prowizja = wycieczka['prowizja_para_mloda']
    elif 3 <= liczba_osob <= 9:
        prowizja = wycieczka['prowizja_mniej_10_osob']
    elif 10 <= liczba_osob <= 25:
        prowizja = wycieczka['prowizja_10_25_osob']
    elif 25 <= liczba_osob <= 50:
        prowizja = wycieczka['prowizja_25_50_osob']
    else:
        prowizja = 0

    # Debug: Wydruk przypisanej prowizji
    print(f"ID wycieczki: {row['id_wycieczki']}, liczba osób: {liczba_osob}, przypisana prowizja: {prowizja}")
    return prowizja

# Przypisanie prowizji dla każdej unikalnej grupy
grouped_df['prowizja'] = grouped_df.apply(calculate_commission, axis=1, wycieczki_df=wycieczki_df)

# Debug: Sprawdzenie wyników po przypisaniu prowizji
print("Grupowane dane z przypisaną prowizją:")
print(grouped_df)

# Scalanie wyników z oryginalną ramką danych
zrealizowane_df = zrealizowane_df.merge(grouped_df, on=['id_wycieczki', 'id_pracownika', 'datakupna'], how='left')

# Dodanie kolumny miesiąca
zrealizowane_df['datakupna'] = pd.to_datetime(zrealizowane_df['datakupna'])
zrealizowane_df['miesiac'] = zrealizowane_df['datakupna'].dt.to_period('M')

# Grupowanie po pracownikach i miesiącach, aby uzyskać sumy prowizji
monthly_commission = (
    zrealizowane_df.groupby(['id_pracownika', 'miesiac'])['prowizja']
    .sum()
    .reset_index()
    .rename(columns={'id_pracownika': 'EmployeeID', 'miesiac': 'Month', 'prowizja': 'Commission'})
)

# Debug: Sprawdzenie miesięcznych prowizji
print("Miesięczne prowizje:")
print(monthly_commission)

# Przygotowanie danych pracowników
employees = pd.DataFrame({
    'EmployeeID': range(1, 7),
    'HireDate': ['2024-01-01'] * 6,
    'TerminationDate': [None] * 6,
})

# Tworzenie tabeli płac dla wszystkich miesięcy
base_salary = 4666
date_range = pd.period_range(start='2024-01', end='2025-01', freq='M')

# Przygotowanie pełnej ramki wynikowej
salary_data = []
for employee in employees.itertuples(index=False):
    for month in date_range:
        # Sprawdzanie prowizji dla danego pracownika i miesiąca
        commission = monthly_commission.query("EmployeeID == @employee.EmployeeID and Month == @month")
        total_salary = base_salary + (commission['Commission'].sum() if not commission.empty else 0)
        
        # Debug: Sprawdzanie wynagrodzenia
        print(f"Pracownik: {employee.EmployeeID}, Miesiąc: {month}, Prowizja: {commission['Commission'].sum() if not commission.empty else 0}, Wynagrodzenie: {total_salary}")
        
        # Dodanie nowego wiersza do listy wyników
        salary_data.append({
            'EmployeeID': employee.EmployeeID,
            'HireDate': employee.HireDate,
            'TerminationDate': employee.TerminationDate,
            'SalaryDate': str(month),  # Zapis daty wypłaty w formacie yyyy-mm
            'SalaryAmount': total_salary
        })

# Tworzenie ramki danych z wynikami
final_df = pd.DataFrame(salary_data)

# Sortowanie według SalaryDate i EmployeeID
final_df['SalaryDate'] = pd.to_datetime(final_df['SalaryDate'], format='%Y-%m')
final_df = final_df.sort_values(by=['SalaryDate', 'EmployeeID'])

# Skalowanie pensji powyżej 20,000
def scale_salary(row, max_salary):
    if row['SalaryAmount'] > 20000:
        # Liniowe skalowanie w przedziale 20,000 - 25,000
        return int(20000 + round((row['SalaryAmount'] - 20000) / (max_salary - 20000) * (25000 - 20000),0))
    return row['SalaryAmount']

# Obliczanie maksymalnej pensji
max_salary = final_df['SalaryAmount'].max()

# Przeskalowanie pensji
final_df['SalaryAmount'] = final_df.apply(scale_salary, axis=1, max_salary=max_salary)

# Debug: Sprawdzenie pensji po skalowaniu
print("Pensje po skalowaniu:")
print(final_df.sort_values(by='SalaryAmount', ascending=False).head(10))

# Zapisanie wyniku do pliku CSV
output_file = 'employee_salaries.csv'
final_df.to_csv(output_file, index=False)

print(f"Wynagrodzenia zapisano w pliku: {output_file}")
