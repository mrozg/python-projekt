import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

class Mapa:
    def __init__(self):
        self.tabela_cen = pd.read_csv("dane_gus.csv")
        self.tabela_zarobki = pd.read_csv("zarobki_czyste.csv")
        self.tabela_inflacja = pd.read_csv("wskazniki_czyste.csv")
        self.tabela_inflacja = self.tabela_inflacja.rename(columns={rok: f"{rok}_inflacja" for rok in ["2012", "2015", "2018", "2021", "2024"]})
        temp_merge = pd.merge(self.tabela_cen, self.tabela_zarobki, on="Wojewodztwo", suffixes=("_cena", "_pensja"))
        self.tabele_polaczone = pd.merge(temp_merge, self.tabela_inflacja, on="Wojewodztwo")
    def wyswietl_mape(self):
        st.header("Mapa średnich cen za m² w Polsce oraz ich dynamiki wzrostu")
        rok = st.radio("Wybierz rok:", ["2012", "2015", "2018", "2021", "2024"], horizontal=True)
        tryb_mapy = st.radio("Wybierz tryb mapy:", ["Średnie ceny", "Dynamika wzrostu cen"], horizontal=True)
        srednia = self.tabela_cen[rok].mean()
        max_wiersz = self.tabela_cen.loc[self.tabela_cen[rok].idxmax()]
        min_wiersz = self.tabela_cen.loc[self.tabela_cen[rok].idxmin()]
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.metric(label="Średnia cena za m² w Polsce wynosi:", value=f"{round(srednia, 2)} PLN/m²", delta=None)
        with col2:
            with st.container(border=True):
                st.metric(label=f"Najwyższa cena za m² w Polsce wynosi ({max_wiersz['Wojewodztwo']}):", value=f"{round(max_wiersz[rok], 2)} PLN/m²", delta=None)
        with col3:
            with st.container(border=True):
                st.metric(label=f"Najniższa cena za m² w Polsce wynosi ({min_wiersz['Wojewodztwo']}):", value=f"{round(min_wiersz[rok], 2)} PLN/m²", delta=None)
        st.divider()
        st.info("Kolor pinezki na mapie cen średnich: zielony - cena poniżej 10 000 PLN/m²; czerwony - cena powyżej 10 000 PLN/m² \n\n" "Dla trybu dynamiki wzrostu cen: zielony - wzrost poniżej 100%; ciemnoczerwony - wzrost powyżej 100%")
        mapa = folium.Map(
            location=[52.06, 19.48],
            zoom_start=6.2,
            min_lat=48.50,
            max_lat=55.50, 
            min_lon=13.50, 
            max_lon=25.00, 
            max_bounds=True)
        # iterujemy przez wiersze tabeli, tworząc marker dla każdego województwa z odpowiednimi danymi
        for index, wiersz in self.tabele_polaczone.iterrows():
            nazwa = wiersz["Wojewodztwo"]
            czysta_cena = str(wiersz[f"{rok}_cena"]).replace("\xa0", "").replace(" ", "")
            cena = float(czysta_cena)
            pensja = wiersz[f"{rok}_pensja"]
            metry_za_pensje = round(pensja/cena, 2)
            wzrost_procentowy = round((wiersz[f"{rok}_cena"] - wiersz["2012_cena"])/wiersz["2012_cena"] * 100, 2)
            inflacja = wiersz[f"{rok}_inflacja"]
            szerokosc = wiersz["szerokosc"]
            dlugosc = wiersz["dlugosc"]

            if tryb_mapy == "Średnie ceny": 
                if cena > 10000:
                    kolor_pinezki = "red"
                else:
                    kolor_pinezki = "green"
                # upiększamy popup, dodając nagłówek, kolorową cenę oraz estetyczne formatowanie
                lepszy_popup = f"""
                <div style="font-family: 'Trebuchet MS', Arial, sans-serif; font-size: 13px; min-width: 150px;">
                    <h4 style="color: #2c3e50; font-size: 15px; margin-bottom: 5px; margin-top: 0;"><b>Województwo {nazwa}</b></h4>
                    <hr style="margin: 5px 0;">
                    <p style="margin: 0; font-size: 13px;">Średnia cena: <span style="color: #e74c3c;"><b>{cena} PLN/m²</b></span></p>
                    <p style="margin: 5px 0 0 0; font-size: 12px; color: #555;">Średnia pensja: <b>{wiersz[f"{rok}_pensja"]} PLN</b></p>
                    <p style="margin: 0; font-size: 12px; color: #555;">Za jedną pensję kupisz: <b>{metry_za_pensje} m²</b></p>
                </div>"""
                gotowy_popup = folium.Popup(lepszy_popup, max_width=300)
                # dodajemy marker do warstwy, a następnie warstwę do mapy
                folium.Marker(
                    location=[szerokosc, dlugosc],
                    popup=gotowy_popup,
                    icon=folium.Icon(color=kolor_pinezki, icon="home")
                ).add_to(mapa)
            else:
                if wzrost_procentowy > 100:
                    kolor_znacznika = "darkred"
                else:
                    kolor_znacznika = "green"
                popup_dynamiki = f"""
                <div style="font-family: 'Trebuchet MS', Arial, sans-serif; font-size: 13px; min-width: 150px;">
                    <h4 style="color: #2c3e50; font-size: 15px; margin-bottom: 5px; margin-top: 0;"><b>Województwo {nazwa}</b></h4>
                    <hr style="margin: 5px 0;">
                    <p style="margin: 0; font-size: 13px;">Wzrost procentowy od 2012 r.: <span style="color: #e74c3c;"><b>{wzrost_procentowy} %</b></span></p>
                    <p style="margin: 0; font-size: 13px;">Inflacja r/r: <span style="color: #e74c3c;"><b>{inflacja}</b></span></p>
                </div>"""
                gotowy_popup_dynamiki = folium.Popup(popup_dynamiki, max_width=300)
                folium.Marker(
                    location=[szerokosc, dlugosc],
                    popup=gotowy_popup_dynamiki,
                    icon=folium.Icon(color=kolor_znacznika, icon="info-sign")
                ).add_to(mapa)
        st_folium(mapa, height=675, use_container_width=True)
