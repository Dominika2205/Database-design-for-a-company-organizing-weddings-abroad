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
mycursor.execute(
    '''SELECT 
        DATE_FORMAT(datakupna, '%Y-%m') AS miesiac, 
        COUNT(*) AS liczba_rezerwacji
    FROM zrealizowane_wycieczki
    GROUP BY miesiac
    ORDER BY liczba_rezerwacji DESC'''
)

rezerwacje_data = mycursor.fetchall()
rezerwacje_df = pd.DataFrame(rezerwacje_data, columns=["Miesiąc", "Liczba_Rezerwacji"])
for row in rezerwacje_data:
    print(row)
mycursor.close()
con.close()
data = {
    "rezerwacje_miesiac": [
        {"miesiac": row[0], "liczba_rezerwacji": row[1]} 
        for row in rezerwacje_data
    ]
}

with open("data_4.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
