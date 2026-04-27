import streamlit as st
import zakladka_mapa
import zakladka_wykresy
import zakladka_kalkulator
import zakladka_porownywarka
from dane import Dane

st.set_page_config(page_title="Projekt python", layout="wide")
st.title("Integracja i wizualizacja średnich cen mieszkań na mapie na podstawie danych z GUS")
st.divider()
st.sidebar.header("Menu", anchor="center", divider=True)
wybor = st.sidebar.radio("Wybierz zakładkę:", ["Mapy", "Wykresy", "Kalkulator", "Porównywarka", "Dane"])

if wybor == "Mapy":
    modul_mapy = zakladka_mapa.Mapa()
    modul_mapy.wyswietl_mape()
elif wybor == "Wykresy":
    modul_wykresy = zakladka_wykresy.Wykresy()
    modul_wykresy.wyswietl_wykresy()
elif wybor == "Kalkulator":
    modul_kalkulator = zakladka_kalkulator.Kalkulator()
    modul_kalkulator.wyswietl_kalkulator()
elif wybor == "Porównywarka":
    modul_porownywarka = zakladka_porownywarka.Porownywarka()
    modul_porownywarka.wyswietl_porownywarke()
else:
    modul_dane = Dane()
    modul_dane.pobierz_dane()

st.sidebar.html("<div style='margin-top: 18vh;'></div>")
st.sidebar.divider()
with st.sidebar:
    st.sidebar.caption("### O projekcie \n **Autorzy (L5):** Małgorzata Mróz 184266, David Miśkowicz 184263, Julia Puchała 184186 \n\n **Kierunek studiów i rok wykonania:** Inżynieria i analiza danych, 2026 \n\n **Przedmiot:** Wprowadzenie do programowania w języku Python \n\n Źródła danych: Główny Urząd Statystyczny (GUS)")