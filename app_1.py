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

mycursor.execute('''
WITH Popularnosc AS (
    SELECT 
        id_wycieczki, 
        COUNT(*) AS liczba_realizacji
    FROM zrealizowane_wycieczki
    GROUP BY id_wycieczki
)
SELECT 
    w.miejsce AS miejsce,  
    p.liczba_realizacji,
    (w.koszt_para_mloda + w.koszt_mniej_10_osob) * p.liczba_realizacji AS koszt_calkowity,
    (w.cena_para_mloda + w.cena_mniej_10_osob) * p.liczba_realizacji AS przychod_calkowity,
    ((w.cena_para_mloda - w.koszt_para_mloda) + (w.cena_mniej_10_osob - w.koszt_mniej_10_osob)) * p.liczba_realizacji AS zysk_calkowity,

    CASE 
        WHEN ((w.cena_para_mloda + w.cena_mniej_10_osob) * p.liczba_realizacji) = 0 THEN 0
        ELSE 
            ROUND(
                (( (w.cena_para_mloda - w.koszt_para_mloda) + 
                   (w.cena_mniej_10_osob - w.koszt_mniej_10_osob) ) * p.liczba_realizacji ) / 
                ((w.cena_para_mloda + w.cena_mniej_10_osob) * p.liczba_realizacji) * 100, 2)
    END AS marza_procentowa
FROM Popularnosc p
JOIN travel_packages w ON p.id_wycieczki = w.id
ORDER BY p.liczba_realizacji DESC
LIMIT 4
''')

popularnosc_data = mycursor.fetchall()

popularnosc_df = pd.DataFrame(popularnosc_data, columns=[
    "Miejsce", "Liczba Realizacji", "Koszt Calkowity", "Przychod Calkowity", "Zysk Calkowity", "Marza Procentowa"])

for row in popularnosc_data:
    print(row)

mycursor.close()
con.close()

data = {
    "popularnosc": [{"miejsce": row[0], 
                     "liczba_realizacji": row[1], 
                     "koszt_calkowity": row[2], 
                     "przychod_calkowity": row[3], 
                     "zysk_calkowity": row[4], 
                     "marza_procentowa": row[5]} 
                    for row in popularnosc_data],
}

with open("data_1.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


