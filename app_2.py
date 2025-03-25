import mysql.connector
import pandas as pd
import json
import matplotlib.pyplot
con = mysql.connector.connect(
    host = '127.0.0.1',
    user =  'root',            
    password = 'malykot321$',       
    database = 'projekt_bazy' 
)
mycursor = con.cursor()

mycursor.execute(
'''select DATE_FORMAT(datakupna, '%m-%Y') AS data , count(id_klienta) as ilosc_klientow
from zrealizowane_wycieczki
group by data
order by MIN(datakupna) asc;
''')
klienci_data = mycursor.fetchall()
klienci_df = pd.DataFrame(klienci_data, columns=["data", "Ilość Klientów"])


for row in mycursor:
    print(row)

mycursor.close()
con.close()


data = {
    "klienci": [{"data": row[0], "ilosc_klientow": row[1]} for row in klienci_data]
}


with open("data_2.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

