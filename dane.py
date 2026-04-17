import streamlit as st
import pandas as pd

@st.cache_data
def pobierz_i_wyczysc_dane():
    temp_ceny = pd.read_csv("dane_gus.csv")
    temp_zarobki = pd.read_csv("zarobki_czyste.csv")
    temp_inflacja = pd.read_csv("wskazniki_czyste.csv")
    lata = ["2012", "2015", "2018", "2021", "2024"]
    for rok in lata:
        temp_ceny[rok] = temp_ceny[rok].astype(str).str.replace("\xa0", "").replace(" ", "").astype(float)
    ceny_dlugie = pd.melt(temp_ceny, id_vars=["Wojewodztwo"], value_vars=lata, var_name="Rok", value_name="Cena")
    zarobki_dlugie = pd.melt(temp_zarobki, id_vars=["Wojewodztwo"], value_vars=lata, var_name="Rok", value_name="Pensja")
    inflacja_dlugie = pd.melt(temp_inflacja, id_vars=["Wojewodztwo"], value_vars=lata, var_name="Rok", value_name="Inflacja")
    ceny_zarobki = pd.merge(ceny_dlugie, zarobki_dlugie, on=["Wojewodztwo", "Rok"])
    gotowa_tabela = pd.merge(ceny_zarobki, inflacja_dlugie, on=["Wojewodztwo", "Rok"])
    gotowa_tabela["Rok"] = gotowa_tabela["Rok"].astype(int)
    return gotowa_tabela

class Dane:
    def __init__(self):
        self.ceny = pd.read_csv("dane_gus.csv")
        self.zarobki = pd.read_csv("zarobki_czyste.csv")
        self.inflacja = pd.read_csv("wskazniki_czyste.csv")
    def pobierz_dane(self):
        st.title("Eksplorator danych źródłowych")
        st.write("Poniżej znajdują się tabele z danymi, które zostały użyte w projekcie. Możesz je przeglądać oraz pobrać w formacie CSV. Wszystkie dane pochodzą z Głównego Urzędu Statystycznego (GUS) i zostały odpowiednio przetworzone, aby były gotowe do analizy i wizualizacji w naszym projekcie. Dane obejmują średnie ceny za m² mieszkań, przeciętne miesięczne wynagrodzenia oraz wskaźnik inflacji dla poszczególnych województw w Polsce w latach 2012-2024.")
        tab_ceny, tab_zarobki, tab_inflacja = st.tabs(["Ceny mieszkań", "Zarobki", "Inflacja"])
        with tab_ceny:
            st.subheader("Średnia cena lokali mieszkalnych sprzedanych w ramach transakcji rynkowych")
            st.dataframe(self.ceny, use_container_width=True)
            csv_ceny = self.ceny.to_csv(index=False).encode('utf-8')
            st.download_button(label="Pobierz dane o cenach", data=csv_ceny, file_name='ceny_mieszkan.csv', mime='text/csv')
        with tab_zarobki:
            st.subheader("Przeciętne miesięczne wynagrodzenia brutto")
            st.dataframe(self.zarobki, use_container_width=True)
            csv_zarobki = self.zarobki.to_csv(index=False).encode('utf-8')
            st.download_button(label="Pobierz dane o zarobkach", data=csv_zarobki, file_name='zarobki.csv', mime='text/csv')
        with tab_inflacja:
            st.subheader("Wskaźnik cen towarów i usług konsumpcyjnych (pot. inflacja)")
            st.dataframe(self.inflacja, use_container_width=True)
            csv_inflacja = self.inflacja.to_csv(index=False).encode('utf-8')
            st.download_button(label="Pobierz dane o inflacji", data=csv_inflacja, file_name='inflacja.csv', mime='text/csv')