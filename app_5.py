import mysql.connector
import pandas as pd
import json

con = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='malykot321$',
    database='projekt_bazy'
)

mycursor = con.cursor()
mycursor.execute('''SELECT 
    pracownicy.imie,
    pracownicy.nazwisko,
    COUNT(zrealizowane_wycieczki.id_wycieczki) AS liczba_wycieczek
FROM 
    zrealizowane_wycieczki
JOIN 
    pracownicy ON zrealizowane_wycieczki.id_pracownika = pracownicy.id
GROUP BY 
    pracownicy.id
ORDER BY 
    liczba_wycieczek DESC
LIMIT 3;''')

pracownicy_data = mycursor.fetchall()

pracownicy_df = pd.DataFrame(pracownicy_data, columns=["Imie", "Nazwisko", "Liczba_Wycieczek"])

for row in pracownicy_data:
    print(row)

mycursor.close()
con.close()

data = {
    "pracownicy_top_10": [
        {"imie": row[0], "nazwisko": row[1], "liczba_wycieczek": row[2]} 
        for row in pracownicy_data
    ]
}

with open("data_5.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


