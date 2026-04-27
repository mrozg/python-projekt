import streamlit as st
import pandas as pd
import plotly.express as px

class Porownywarka: 
    def __init__(self):
        #wczytujemy dane
        self.df_ceny = pd.read_csv('dane_gus.csv')
        self.df_zarobki = pd.read_csv('zarobki_czyste.csv')
        self.lata = ["2012", "2015", "2018", "2021", "2024"]

    def wyswietl_porownywarke(self):
        st.header("Porównywarka województw")
        st.write("Wybierz dwa województwa i dowiedz się o różnicach w cenach i zarobkach!")
        wojewodztwa = self.df_ceny['Wojewodztwo'].unique()

        #wybor regionow, podzial na dwie kolumny
        col1, col2 = st.columns(2)
        with col1:
            woj_1 = st.selectbox("Wybierz pierwsze województwo: ", wojewodztwa, index=0)
        with col2:
            woj_2 = st.selectbox("Wybierz druge województwo: ", wojewodztwa, index=1)

        if woj_1 == woj_2:
            st.warning("Wybierz dwa rózne województwa!")
            return
        
        #pobranie danych dla 2024
        rok_ostatni = "2024"
        c1 = self.df_ceny[self.df_ceny['Wojewodztwo'] == woj_1][rok_ostatni].values[0]
        c2 = self.df_ceny[self.df_ceny['Wojewodztwo'] == woj_2][rok_ostatni].values[0]

        z1 = self.df_zarobki[self.df_zarobki['Wojewodztwo'] == woj_1][rok_ostatni].values[0]
        z2 = self.df_zarobki[self.df_zarobki['Wojewodztwo'] == woj_2][rok_ostatni].values[0]
        m1 = z1 / c1
        m2 = z2 / c2

        #wyswietlanie metry obok siebie
        st.subheader(f"{woj_1} vs {woj_2} (Dane na {rok_ostatni})")

        m_col1, m_col2, m_col3 = st.columns(3)

        with m_col1:
            diff_c = c1 - c2
            st.metric("Cena m²", f"{c1:,.0f} zł", delta=f"{diff_c:,.0f} zł", delta_color="inverse")
            st.metric("Cena m²", f"{c2:,.0f} zł", delta=f"{-diff_c:,.0f} zł", delta_color="inverse")

        with m_col2:
            diff_z = z1 - z2
            st.metric("Średnie zarobki", f"{z1:,.0f} zł", delta=f"{diff_z:,.0f} zł")
            st.metric("Średnie zarobki", f"{z2:,.0f} zł", delta=f"{-diff_z:,.0f} zł")

        with m_col3:
            diff_m = m1 - m2
            st.metric("Dostępność (m²/pensję)", f"{m1:.2f}", delta=f"{diff_m:.2f}")
            st.metric("Dostępność (m²/pensję)", f"{m2:.2f}", delta=f"{-diff_m:.2f}")

        st.divider()

        #wykres trendu dla obu wojewodztw
        st.subheader("Trend cenowy na przestrzeni lat")
        #przygotowanie danych do wykresu
        d1 = self.df_ceny[self.df_ceny['Wojewodztwo'] == woj_1][self.lata].T
        d1.columns = [woj_1]
        d2 = self.df_ceny[self.df_ceny['Wojewodztwo'] == woj_2][self.lata].T
        d2.columns = [woj_2]

        df_plot = pd.concat([d1, d2], axis=1).reset_index()
        df_plot.columns = ['Rok', woj_1, woj_2]

        fig = px.line(df_plot, x='Rok', y=[woj_1, woj_2], 
                      markers=True, 
                      title="Porównanie wzrostu cen m²",
                      labels={"value": "Cena (PLN)", "variable": "Województwo"})
        
        st.plotly_chart(fig, use_container_width=True)

        # Ciekawostka na dole
        lepie_m = woj_1 if m1 > m2 else woj_2
        st.info(f"Mimo różnic w cenach, większą siłę nabywczą mają mieszkańcy województwa **{lepie_m}**.")
