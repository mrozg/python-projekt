import streamlit as st
import zakladka_mapa
import zakladka_wykresy
import zakladka_kalkulator
from dane import Dane

st.set_page_config(page_title="Projekt python", layout="wide")
st.title("Integracja i wizualizacja średnich cen mieszkań na mapie na podstawie danych z GUS")
st.divider()
st.sidebar.header("Menu", anchor="center", divider=True)
wybor = st.sidebar.radio("Wybierz zakładkę:", ["Mapa", "Wykresy", "Kalkulator", "Dane", "Inne"])

if wybor == "Mapa":
    modul_mapy = zakladka_mapa.Mapa()
    modul_mapy.wyswietl_mape()
elif wybor == "Wykresy":
    modul_wykresy = zakladka_wykresy.Wykresy()
    modul_wykresy.wyswietl_wykresy()
elif wybor == "Kalkulator":
    modul_kalkulator = zakladka_kalkulator.Kalkulator()
    modul_kalkulator.wyswietl_kalkulator()
elif wybor == "Dane":
    modul_dane = Dane()
    modul_dane.pobierz_dane()
else:
    st.info("chuj wie co tu bedzie, ale na pewno nie to :)")

st.sidebar.divider()
with st.sidebar:
    st.sidebar.markdown("""
    ### O projekcie
    **Autorzy (L5):** Małgorzata Mróz 184266, David Miśkowicz ,Julia Puchała \n
    **Kierunek studiów i rok wykonania:** Inżynieria i analiza danych, 2026 \n
    **Przedmiot:** Wstęp do programowania w języku Python \n
    Źródła danych: Główny Urząd Statystyczny (GUS)
    """)