import streamlit as st
import zakladka_mapa
import zakladka_wykresy

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
    st.info("cuming soon - dodaj kalkulator ")
elif wybor == "Dane":
    st.info("cuming soon - dodaj tabelki z mozliwoscia pobrania (wszystkie dane ktore uzywamy)")
else:
    st.info("chuj wie co tu bedzie, ale na pewno nie to :)")