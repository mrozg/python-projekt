import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

class Wykresy:
    def __init__(self):
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
        self.dane_wykresy = pd.merge(ceny_zarobki, inflacja_dlugie, on=["Wojewodztwo", "Rok"])
        self.dane_wykresy["Rok"] = self.dane_wykresy["Rok"].astype(int)
    def wyswietl_wykresy(self):
        st.header("Wykresy danych")
        wojewodztwa = self.dane_wykresy["Wojewodztwo"].unique()
        wybrane_woj = st.selectbox("Wybierz województwo:", wojewodztwa)
        dane_woj = self.dane_wykresy[self.dane_wykresy["Wojewodztwo"] == wybrane_woj]
        cena_2012 = dane_woj["Cena"].iloc[0]
        cena_2024 = dane_woj["Cena"].iloc[-1]
        wzrost_ceny_zloty = cena_2024 - cena_2012
        wzrost_ceny_procent = round((wzrost_ceny_zloty / cena_2012) * 100, 2)
        pensja_2012 = dane_woj["Pensja"].iloc[0]
        pensja_2024 = dane_woj["Pensja"].iloc[-1]
        wzrost_pensji_zloty = round(pensja_2024 - pensja_2012, 2)
        wzrost_pensji_procent = round((wzrost_pensji_zloty / pensja_2012) * 100, 2)
        x = dane_woj["Rok"]
        y = dane_woj["Cena"]
        wspolczynniki = np.polyfit(x, y, 1)
        funkcja_wykresu = np.poly1d(wspolczynniki)
        prognoza_2027 = funkcja_wykresu(2027)
        podloga_cena = (dane_woj["Cena"].min() // 1000) * 1000
        sufit_cena = prognoza_2027 + 1000
        kol1, kol2, kol3 = st.columns(3)
        with kol1:
            with st.container(border=True):
                st.metric(label="Wzrost cen za m² (2012-2024):", value=f"{wzrost_ceny_zloty} PLN", delta=f"{wzrost_ceny_procent} %")
        with kol2:
            with st.container(border=True):
                st.metric(label="Wzrost pensji (2012-2024):", value=f"{wzrost_pensji_zloty} PLN", delta=f"{wzrost_pensji_procent} %")
        with kol3:
            with st.container(border=True):
                st.metric(label="Prognoza na 2027:", value=f"{round(prognoza_2027, 2)} PLN/m²")
        st.divider()
        tryb_wykresu = st.radio("Wybierz wykres do wyświetlenia:", ["Cena za m² (z prognozą na 2027)", "Ile m² kupisz za jedną pensję", "Inflacja"], horizontal=True)
        if tryb_wykresu == "Cena za m² (z prognozą na 2027)":
            wykres_cen = px.line(dane_woj, x="Rok", y="Cena", markers=True, title=f"Cena za m² w {wybrane_woj} (z prognozą na 2027)")
            wykres_cen.add_scatter(x=[2027], y=[prognoza_2027], mode="markers", name="Prognoza 2027", marker=dict(size=10, color="red", symbol="x"))
            wykres_cen.add_shape(type="line", x0=2024, y0=cena_2024, x1=2027, y1=prognoza_2027, line=dict(dash="dash", color="red"))
            wykres_cen.update_xaxes(tickvals=[2012, 2015, 2018, 2021, 2024, 2027])
            wykres_cen.update_yaxes(range=[podloga_cena, sufit_cena], tickformat="d", title="Cena [PLN/m²]")
            st.plotly_chart(wykres_cen, use_container_width=True)
        elif tryb_wykresu == "Ile m² kupisz za jedną pensję":
            dane_woj["Metry"] = round(dane_woj["Pensja"] / dane_woj["Cena"], 2)
            wykres_pensja = px.line(dane_woj, x="Rok", y="Metry", markers=True, title=f"Ile m² kupisz za jedną pensję w {wybrane_woj}", hover_data={"Pensja": ":.2f"}, labels={"Metry": "Powierzchnia [m²]", "Pensja": "Średnia pensja [PLN]"})
            wykres_pensja.update_xaxes(tickvals=[2012, 2015, 2018, 2021, 2024])
            st.plotly_chart(wykres_pensja, use_container_width=True)
        else:
            wykres_inflacja = px.bar(dane_woj, x="Rok", y="Inflacja", title=f"Inflacja w {wybrane_woj} (2012-2024)", text_auto=".2f")
            wykres_inflacja.update_xaxes(tickvals=[2012, 2015, 2018, 2021, 2024])
            wykres_inflacja.update_yaxes(range=[0,125])
            wykres_inflacja.add_hline(y=102.5, line_dash="dot", line_color="green", annotation_text="Zdrowy cel NBP")
            st.plotly_chart(wykres_inflacja, use_container_width=True)
