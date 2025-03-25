import sys
import mysql.connector
import csv
from generating_pesel import get_names_list3, get_names_list4


travels_file_path = "./wycieczki2.csv"
wycieczki_zrealizowane_file_path = "./zrealizowane_wycieczki.csv"
salaries_file_path = "./employee_salaries.csv"
host = "localhost"
user = "root"
password = "malykot321$"
database_name = "projekt_bazy"


def create_connection():
    return mysql.connector.connect(user=user, password=password, host=host, database=database_name)


def read_csv(filepath, delimiter=';', skip_header=False):
    data = []
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=delimiter)
        if skip_header:
            next(csvfile)
        for row in csv_reader:
            data.append(row)
    return data

def read_csv2(filepath, delimiter=',', skip_header=False):
    data = []
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=delimiter)
        if skip_header:
            next(csvfile)
        for row in csv_reader:
            data.append(row)
    return data


try:
  
    mydb = create_connection()
    cursor = mydb.cursor()

    
    full_names = get_names_list3()
    
    
    data = []
    for record in full_names:
        imie, nazwisko = record['name'].split(' ', 1)  
        pesel = record['pesel']
        telefon = record['telefon']
        telefon_kontaktowy = record['telefon_kontaktowy']
        email = record['email']
        data.append((imie, nazwisko, pesel, telefon, telefon_kontaktowy, email))

    insert_query_names = "INSERT INTO klienci (imie, nazwisko, pesel, telefon, telefon_kontaktowy, email) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(insert_query_names, data)

    # Wstaw dane do tabeli pracownicy
    full_names2 = get_names_list4()
    
    data2 = []
    for record in full_names2:
        imie, nazwisko = record['name'].split(' ', 1)
        pesel = record['pesel']
        telefon = record['telefon']
        telefon_kontaktowy = record['telefon_kontaktowy']
        email = record['email']
        data2.append((imie, nazwisko, pesel, telefon, telefon_kontaktowy, email))

    insert_query_names2 = "INSERT INTO pracownicy (imie, nazwisko, pesel, telefon, telefon_kontaktowy, email) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(insert_query_names2, data2)

   
    travels_csv = read_csv(travels_file_path, delimiter=';', skip_header=False)
    insert_query_travel = """
        INSERT INTO travel_packages (
            id, miejsce, cena_para_mloda, koszt_para_mloda, prowizja_para_mloda,
            cena_mniej_10_osob, koszt_mniej_10_osob, prowizja_mniej_10_osob,
            cena_10_25_osob, koszt_10_25_osob, prowizja_10_25_osob,
            cena_25_50_osob, koszt_25_50_osob, prowizja_25_50_osob
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    columns_order = [
        "id", "miejsce", "cena_para_mloda", "koszt_para_mloda", "prowizja_para_mloda",
        "cena_mniej_10_osob", "koszt_mniej_10_osob", "prowizja_mniej_10_osob",
        "cena_10_25_osob", "koszt_10_25_osob", "prowizja_10_25_osob",
        "cena_25_50_osob", "koszt_25_50_osob", "prowizja_25_50_osob"
    ]

    rows = []
    for row in travels_csv:
        try:
            row_data = tuple(row[column] for column in columns_order)
            rows.append(row_data)
        except KeyError as e:
            print(f"Missing column in CSV: {e}")

    cursor.executemany(insert_query_travel, rows)

    
    realized_travels_csv = read_csv(wycieczki_zrealizowane_file_path, delimiter=',', skip_header=False)
    insert_query_travel2 = """
        INSERT INTO zrealizowane_wycieczki (
            id_wycieczki, id_klienta, datakupna, datawyjazdu, id_pracownika
        ) VALUES (%s, %s, %s, %s, %s)
    """

    columns_order2 = ["id_wycieczki", "id_klienta", "datakupna", "datawyjazdu", "id_pracownika"]

    rows2 = []  
    for row in realized_travels_csv:
        try:
            row_data = tuple(row[column] for column in columns_order2)
            rows2.append(row_data) 
        except KeyError as e:
            print(f"Missing column in CSV: {e}")

    cursor.executemany(insert_query_travel2, rows2)

    salaries_csv = read_csv2(salaries_file_path, delimiter=',', skip_header=False )
    insert_query_salaries = """
    INSERT INTO zarobkipracowników (
        EmployeeID, HireDate, TerminationDate, SalaryDate, SalaryAmount
    ) VALUES (%s, %s, %s, %s, %s)
    """
    columns_order3 = [
    "EmployeeID", "HireDate", "TerminationDate", "SalaryDate", "SalaryAmount"]

    rows3 = []
    for row in salaries_csv:
        try:
            row_data = []
            for column in columns_order3:
                value = row[column]
                if column in ["HireDate", "TerminationDate"] and value.strip() == "":
                    value = None  # Replace empty string with NULL
                row_data.append(value)
            rows3.append(tuple(row_data))
        except KeyError as e:
            print(f"Missing column in CSV: {e}")


    cursor.executemany(insert_query_salaries, rows3)

    
    mydb.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")
except Exception as e:
    print(f"Unexpected Error: {e}")
finally:
    cursor.close()
    mydb.close()

