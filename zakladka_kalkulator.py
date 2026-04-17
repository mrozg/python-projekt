import streamlit as st
import pandas as pd
import numpy as np
from dane import pobierz_i_wyczysc_dane

class Kalkulator:
    def __init__(self):
        self.dane = pobierz_i_wyczysc_dane()
    def wyswietl_kalkulator(self):
        st.header("Kalkulator")
        st.caption("Oblicz, ile m² mieszkania możesz kupić za swoją pensję")
        wojewodztwa = self.dane["Wojewodztwo"].unique()
        wybrane_woj = st.selectbox("Wybierz województwo", wojewodztwa)
        dane_woj = self.dane[self.dane["Wojewodztwo"] == wybrane_woj]
        x = dane_woj["Rok"]
        y = dane_woj["Cena"]
        wspolczynniki = np.polyfit(x, y, 1)
        funkcja_wykresu = np.poly1d(wspolczynniki)
        cena_2026 = funkcja_wykresu(2026)
        a = dane_woj["Rok"]
        b = dane_woj["Pensja"]
        wspolczynniki = np.polyfit(a, b, 1)
        funkcja_wykresu2 = np.poly1d(wspolczynniki)
        pensja_2026 = int(funkcja_wykresu2(2026))
        col1, col2 = st.columns(2)
        with col1:
            metraz = st.number_input("Wybierz swój wymarzony metraż mieszkania [m²]", min_value=10, max_value=250, value=50, step=20)
            pensja_usera = st.number_input("Twoja aktualna pensja netto [PLN]", min_value=1000, value=pensja_2026, step=500)
            st.caption(f"Średnia pensja w {wybrane_woj} w 2026 roku (prognoza): " + str(pensja_2026) + " PLN")
            procent_pensji = st.slider("Ile % swojej pensji chcesz przeznaczyć na zakup mieszkania?", min_value=1, max_value=100, value=50)
            koszt_calkowity = metraz * cena_2026
            oszczednosci = pensja_usera * (procent_pensji/100)
            miesiace = koszt_calkowity / oszczednosci
            czas = miesiace / 12
        with col2:
            with st.container(border=True):
                st.metric(label="Koszt całkowity mieszkania (bez uwzględnienia inflacji i kredytu):", value=f"{round(koszt_calkowity, 2)} PLN", delta=f"Średnia cena za m² w {wybrane_woj} (2026): " + str(round(cena_2026, 2)) + " PLN/m²")
            with st.container(border=True):
                st.metric(label="Oszczędności miesięczne (bez uwzględnienia inflacji i kredytu):", value=f"{round(oszczednosci, 2)} PLN")
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.metric(label="Czas potrzebny na zakup:", value=f"{round(czas, 2)} lat", delta="bez uwzględnienia inflacji i kredytu")
        with col2:
            najnowsza_inflacja = dane_woj["Inflacja"].iloc[-1]
            stopa_inflacji = (najnowsza_inflacja - 100) / 100
            oszczednosci_temp = 0
            cena_temp = koszt_calkowity
            miesiace_temp = 0
            nieskonczonosc = False #flaga bezpieczenstwa
            while oszczednosci_temp < cena_temp:
                oszczednosci_temp += oszczednosci
                miesiace_temp += 1
                if miesiace_temp % 12 ==0:
                    cena_temp = cena_temp + (cena_temp * stopa_inflacji)
                if miesiace_temp > 600:
                    nieskonczonosc = True
                    break
            if nieskonczonosc:
                st.error("Niestety, przy obecnym poziomie oszczędności i inflacji, zakup mieszkania może być niemożliwy.")
            else:
                lata_inflacja = miesiace_temp / 12
                with st.container(border=True):
                    st.metric(label="Czas potrzebny na zakup:", value=f"{round(lata_inflacja, 2)} lat", delta="z uwzględnieniem inflacji i bez kredytu")
            