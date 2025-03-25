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

mycursor.execute('''
    WITH Klienci_liczba AS (
        SELECT id_klienta, COUNT(id_wycieczki) AS liczba_wycieczek
        FROM zrealizowane_wycieczki
        GROUP BY id_klienta
    )
    SELECT 
        zw.id_wycieczki,
        tp.miejsce,
        COUNT(DISTINCT CASE WHEN k.liczba_wycieczek > 1 THEN zw.id_klienta ELSE NULL END) AS powracajacy_klienci,
        COUNT(DISTINCT zw.id_klienta) AS wszyscy_klienci,
        ROUND(
            (COUNT(DISTINCT CASE WHEN k.liczba_wycieczek > 1 THEN zw.id_klienta ELSE NULL END) * 100.0) 
            / NULLIF(COUNT(DISTINCT zw.id_klienta), 0), 
        2) AS procent_powracajacych
    FROM zrealizowane_wycieczki zw
    LEFT JOIN Klienci_liczba k ON zw.id_klienta = k.id_klienta
    JOIN travel_packages tp ON zw.id_wycieczki = tp.id  -- Dodajemy JOIN z tabelą travel_packages
    GROUP BY zw.id_wycieczki, tp.miejsce  -- Dodajemy miejsce do grupowania
    ORDER BY procent_powracajacych DESC
    LIMIT 3
''')


powracajacy_klienci_data = mycursor.fetchall()

mycursor.close()
con.close()


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj) 
        if obj is None:
            return 0.0 
        return super().default(obj)


data = {
    "powracajacy_klienci": [
        {
            "id_wycieczki": int(row[0]), 
            "miejsce": row[1],  
            "powracajacy_klienci": int(row[2]), 
            "wszyscy_klienci": int(row[3]), 
            "procent_powracajacych": row[4]  
        } 
        for row in powracajacy_klienci_data
    ]
}


with open("data_3.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4, cls=CustomJSONEncoder)

