import mysql.connector
import json
from decimal import Decimal

con = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='malykot321$',
    database='projekt_bazy'
)
mycursor = con.cursor()

mycursor.execute(
    '''SELECT 
        AVG(DATEDIFF(datawyjazdu, datakupna)) AS sredni_czas_oczekiwania
    FROM zrealizowane_wycieczki'''
)
sredni_czas_data = mycursor.fetchone()

sredni_czas_oczekiwania = float(sredni_czas_data[0]) if sredni_czas_data and sredni_czas_data[0] is not None else 0.0

mycursor.close()
con.close()

data = {
    "sredni_czas_oczekiwania": sredni_czas_oczekiwania
}
with open("data_6.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Średni czas oczekiwania na wycieczkę: {sredni_czas_oczekiwania} dni")
