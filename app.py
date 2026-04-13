import streamlit as st
import zakladka_mapa

st.set_page_config(page_title="Projekt python", layout="wide")
st.title("Integracja i wizualizacja średnich cen mieszkań na mapie na podstawie danych z GUS")
st.divider()
st.sidebar.header("Menu", anchor="center", divider=True)
wybor = st.sidebar.radio("Wybierz zakładkę:", ["Mapa", "Inne zakładki"])

if wybor == "Mapa":
    modul_mapy = zakladka_mapa.Mapa()
    modul_mapy.wyswietl_mape()
else:
    st.info("coming soon")