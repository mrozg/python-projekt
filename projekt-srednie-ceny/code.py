import pandas as pd 
import folium
import webbrowser
import plotly.express as px

# importujemy dane z pliku csv zawierające: średnie ceny za 1m² z GUS oraz współrzędne geograifczne województw
tabela = pd.read_csv("dane_gus.csv")
#print(tabela)

# ustawiamy mapę Polski z odpowiednimi ograniczeniami, aby nie pokazywała obszaru poza granicą kraju
mapa = folium.Map(
    location=[52.0693, 19.4803], 
    zoom_start=6,
    min_lat=48.50,
    max_lat=55.50, 
    min_lon=13.50, 
    max_lon=25.00, 
    max_bounds=True)

# dodajemy warstwy dla każdego roku, z których tylko 2024 jest domyślnie widoczna
lata = ["2012", "2015", "2018", "2021", "2024"]
for rok in lata:
    czy_pokazac = True if rok == "2024" else False
    warstwa = folium.FeatureGroup(name=f"Ceny w {rok}", show=czy_pokazac)

# iterujemy przez wiersze tabeli, tworząc marker dla każdego województwa z odpowiednimi danymi
    for index, wiersz in tabela.iterrows():
        nazwa = wiersz["Wojewodztwo"]
        czysta_cena = str(wiersz[rok]).replace("\xa0", "").replace(" ", "")
        cena = float(czysta_cena)
        szerokosc = wiersz["szerokosc"]
        dlugosc = wiersz["dlugosc"]

        if cena > 10000:
            kolor_pinezki = "red"
        else:
            kolor_pinezki = "green"
# upiększamy popup, dodając nagłówek, kolorową cenę oraz estetyczne formatowanie
        lepszy_popup = f"""
        <div style="font-family: 'Trebuchet MS', Arial, sans-serif; font-size: 13px; min-width: 150px;">
            <h4 style="color: #2c3e50; margin-bottom: 5px; margin-top: 0;"><b>Województwo {nazwa}</b></h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 0; font-size: 14px;">Średnia cena: <span style="color: #e74c3c;"><b>{cena} PLN/m²</b></span></p>
        </div>"""
        gotowy_popup = folium.Popup(lepszy_popup, max_width=300)
# dodajemy marker do warstwy, a następnie warstwę do mapy
        folium.Marker(
            location=[szerokosc, dlugosc],
            popup=gotowy_popup,
            icon=folium.Icon(color=kolor_pinezki, icon="home")
        ).add_to(warstwa)
    warstwa.add_to(mapa)

# dodajemy kontrolkę warstw, aby użytkownik mógł przełączać się między latami, oraz stylizujemy menu warstw
folium.LayerControl().add_to(mapa)
styl_menu = """<style>
    .leaflet-control-layers-list {
        font-family: 'Trebuchet MS', Arial, sans-serif;
        font-size: 12px;}
    </style>"""
# dodajemy stylizację do mapy, a następnie zapisujemy i otwieramy mapę w przeglądarce
mapa.get_root().html.add_child(folium.Element(styl_menu))
mapa.save("mapa_cen_srednich.html")
webbrowser.open("mapa_cen_srednich.html")

# przygotowujemy dane do wykresu, przekształcając tabelę z szerokiego formatu na długi format, co ułatwia tworzenie wykresów liniowych
tabela_wykres = tabela.melt(
    id_vars=["Wojewodztwo"], 
    value_vars=lata, 
    var_name="Rok", 
    value_name="Cena"
)
tabela_wykres["Cena"] = tabela_wykres["Cena"].astype(str).str.replace('\xa0', '').str.replace(' ', '')
tabela_wykres["Cena"] = tabela_wykres["Cena"].astype(float)

# tworzymy wykres liniowy za pomocą plotly express zawierajacy średnie ceny za 1m² dla każdego województwa, podpisujemy osie
fig = px.line(
    tabela_wykres, 
    x="Rok",
    y="Cena",
    color="Wojewodztwo", 
    markers=True,
    title="Średnie ceny za 1m² w Polsce (2012-2024) na podstawie danych GUS",
    labels={"Cena": "Średnia cena [PLN/m²]", "Rok": "Rok"},
)
# zapisujemy wykres do pliku HTML i otwieramy go w przeglądarce
fig.write_html("wykres_cen_srednich.html")
webbrowser.open("wykres_cen_srednich.html")