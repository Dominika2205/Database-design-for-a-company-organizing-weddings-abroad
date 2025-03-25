import json
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER

pdfmetrics.registerFont(TTFont("czcionka", "DejaVuSans.ttf")) 
styles = getSampleStyleSheet()

paragraph_style = ParagraphStyle(
    name="czcionka",
    fontName="czcionka",
    fontSize=12,
    textColor=colors.black
)
naglowki = ParagraphStyle(
    name="naglowki",
    fontName="czcionka",
    fontSize=12,
    textColor=colors.black,
    alignment=1,
    spaceAfter=6,
    topPadding=8
)

def zawijanie_tekstu(text, is_header=False):
    text_color = colors.white if is_header else colors.black
    return Paragraph(
        text, 
        ParagraphStyle(
            name="zawijanie",
            fontName="czcionka",
            fontSize=10,
            alignment=TA_CENTER,
            textColor=text_color,
            leading=12,
            spaceBefore=5,
            spaceAfter=5
        )
    )

def wczytaj_json(json_file):
    with open(json_file, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

def tytul():
    title_style = getSampleStyleSheet()['Title']
    title = Paragraph("Raport roczny firmy za rok 2024", title_style)
    return title

def naglowek_tabeli(header_text):
    header_style = getSampleStyleSheet()['Heading1']
    header = Paragraph(header_text, naglowki)
    return header

def sredni_czas(json_data):
    sredni_czas = json_data.get("sredni_czas_oczekiwania", "Brak danych")
    text = f"Średni czas oczekiwania na wycieczkę: <b>{sredni_czas}</b> dni."
    return Paragraph(text, paragraph_style)

def tabela_zainteresowanie(json_data):
    table_data = [[zawijanie_tekstu("Miejsce", is_header=True), zawijanie_tekstu("Liczba realizacji", is_header=True), zawijanie_tekstu("Koszt całkowity", is_header=True), zawijanie_tekstu("Przychód całkowity", is_header=True), zawijanie_tekstu("Zysk całkowity", is_header=True), zawijanie_tekstu("Marża procentowa", is_header=True)]]
    for entry in json_data["popularnosc"]:
        miejsce = entry["miejsce"]
        liczba_realizacji = entry["liczba_realizacji"]
        koszt_calkowity = entry["koszt_calkowity"]
        przychod_calkowity = entry["przychod_calkowity"]
        zysk_calkowity = entry["zysk_calkowity"]
        marza_procentowa = entry["marza_procentowa"]
        table_data.append([miejsce, liczba_realizacji, koszt_calkowity, przychod_calkowity, zysk_calkowity, marza_procentowa])

    table = Table(table_data, colWidths=[83.3,83.3 ,83.3,83.3,83.3,83.3])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, -1), "czcionka"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    return table

def wykres(json_data, output_image):
    dates = [entry["data"] for entry in json_data["klienci"]]
    customers = [entry["ilosc_klientow"] for entry in json_data["klienci"]]
    plt.figure(figsize=(10, 6))
    plt.bar(dates, customers, color='skyblue')
    plt.xlabel("Data (Miesiąc-Rok)")
    plt.ylabel("Liczba klientów")
    plt.title("Liczba klientów w poszczególnych miesiącach")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_image)
    plt.close()

def tabela_rezerwacji(json_data):
    table_data = [["Miesiąc", "Liczba rezerwacji"]]
    for entry in json_data["rezerwacje_miesiac"]:
        miesiac = entry["miesiac"]
        liczba_rezerwacji = entry["liczba_rezerwacji"]
        table_data.append([miesiac, liczba_rezerwacji])
    table = Table(table_data, colWidths=[250, 250])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, -1), "czcionka"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    return table

def tabela_pracownikow(json_data):
    table_data = [["Imię", "Nazwisko", "Liczba Wycieczek"]]
    for entry in json_data["pracownicy_top_10"]:
        imie = entry["imie"]
        nazwisko = entry["nazwisko"]
        liczba_wycieczek = entry["liczba_wycieczek"]
        table_data.append([imie, nazwisko, liczba_wycieczek])
    table = Table(table_data, colWidths=[166, 166, 166])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, -1), "czcionka"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    return table

def tabela_najslabszych_miesiecy(json_data):
    table_data = [["Miesiąc", "Liczba Rezerwacji"]]
    for entry in json_data["najsłabsze_miesiące"]:
        miesiac = entry["miesiac"]
        liczba_rezerwacji = entry["liczba_rezerwacji"]
        table_data.append([miesiac, liczba_rezerwacji])
    table = Table(table_data, colWidths=[250, 250])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, -1), "czcionka"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    return table

def tabela_powracajacych_klientow(json_data):
    table_data = [[
        zawijanie_tekstu("Miejsce", is_header=True), 
        zawijanie_tekstu("ID Wycieczki", is_header=True), 
        zawijanie_tekstu("Powracający Klienci", is_header=True), 
        zawijanie_tekstu("Wszyscy Klienci", is_header=True), 
        zawijanie_tekstu("Procent Powracających (%)", is_header=True)
    ]]
    
    for entry in json_data["powracajacy_klienci"]:
        table_data.append([
            zawijanie_tekstu(entry["miejsce"]),
            zawijanie_tekstu(str(entry["id_wycieczki"])),
            zawijanie_tekstu(str(entry["powracajacy_klienci"])),
            zawijanie_tekstu(str(entry["wszyscy_klienci"])),
            zawijanie_tekstu(str(entry["procent_powracajacych"]))
        ])

    table = Table(table_data, colWidths=[100, 100, 100, 100, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, -1), "czcionka"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    return table

def generuj_pdf(json_1_data, json_2_data, json_3_data, json_4_data, json_5_data, json_6_data, json_7_data, output_pdf, chart_image):
    pdf = SimpleDocTemplate(output_pdf, pagesize=letter)
    elements = []
    
    elements.append(tytul())
    elements.append(Spacer(1, 20))
    
    elements.append(sredni_czas(json_6_data))
    elements.append(Spacer(1, 20))
    
    elements.append(naglowek_tabeli("Najpopularniejsze wycieczki i czy są opłacalne"))
    elements.append(tabela_zainteresowanie(json_1_data))
    elements.append(Spacer(1, 20))
    
    wykres(json_2_data, chart_image)
    elements.append(Image(chart_image, width=500, height=300))
    elements.append(Spacer(1, 20))
    
    elements.append(naglowek_tabeli("Ranking miesięcy według liczby rezerwacji"))
    elements.append(tabela_rezerwacji(json_4_data))
    elements.append(Spacer(1, 20))
    
    elements.append(naglowek_tabeli("3 najlepszych pracowników"))
    elements.append(tabela_pracownikow(json_5_data))
    elements.append(Spacer(1, 20))
    
    elements.append(naglowek_tabeli("Najsłabsze miesiące według ilości rezerwacji"))
    elements.append(tabela_najslabszych_miesiecy(json_7_data))
    elements.append(Spacer(1, 20))
    
    elements.append(naglowek_tabeli("Na jakie wycieczki klienci najchętniej wracają?"))
    elements.append(tabela_powracajacych_klientow(json_3_data))
    
    pdf.build(elements)

json_1_file = "data_1.json"
json_2_file = "data_2.json"
json_3_file = "data_3.json"
json_4_file = "data_4.json"
json_5_file = "data_5.json"
json_6_file = "data_6.json"
json_7_file = "data_7.json"
stworzony_pdf = "raport.pdf"
wykres_obraz = "wykres.png"

data_1 = wczytaj_json(json_1_file)
data_2 = wczytaj_json(json_2_file)
data_3 = wczytaj_json(json_3_file)
data_4 = wczytaj_json(json_4_file)
data_5 = wczytaj_json(json_5_file)
data_6 = wczytaj_json(json_6_file)
data_7 = wczytaj_json(json_7_file)

generuj_pdf(data_1, data_2, data_3, data_4, data_5, data_6, data_7, stworzony_pdf, wykres_obraz)

