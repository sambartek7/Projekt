from tkinter import *
from tkinter import ttk
import tkintermapview
import requests
from bs4 import BeautifulSoup

# ===================== LISTY =====================
stacje_meteo = []
pracownicy = []
klienci = []

# ===================== KLASY =====================
class StacjaMeteo:
    def __init__(self, nazwa, lokalizacja):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.wspolrzedne = self.pobierz_wspolrzedne()
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"Wypożyczalnia: {self.nazwa}")

    def pobierz_wspolrzedne(self):
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
        longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]

class Pracownik:
    def __init__(self, imie, nazwisko, stacja):
        self.imie = imie
        self.nazwisko = nazwisko
        self.stacja = stacja
        self.wspolrzedne = stacja.wspolrzedne
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"Pracownik: {self.imie} {self.nazwisko}")

class Klient:
    def __init__(self, imie, stacja):
        self.imie = imie
        self.stacja = stacja
        self.wspolrzedne = stacja.wspolrzedne
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"Klient: {self.imie}")

# ===================== FUNKCJE MAP =====================
def wyczysc_markery():
    for obiekt in stacje_meteo + pracownicy + klienci:
        if hasattr(obiekt, 'marker') and obiekt.marker:
            obiekt.marker.delete()

def pokaz_mape_stacji():
    wyczysc_markery()
    for s in stacje_meteo:
        s.marker = map_widget.set_marker(s.wspolrzedne[0], s.wspolrzedne[1], text=f"Wypożyczalnia: {s.nazwa}")

def pokaz_mape_pracownikow():
    wyczysc_markery()
    for p in pracownicy:
        p.marker = map_widget.set_marker(p.wspolrzedne[0], p.wspolrzedne[1], text=f"Pracownik: {p.imie} {p.nazwisko}")

def pokaz_mape_klientow():
    wyczysc_markery()
    for k in klienci:
        k.marker = map_widget.set_marker(k.wspolrzedne[0], k.wspolrzedne[1], text=f"Klient: {k.imie}")

# ===================== FUNKCJE FORMULARZY =====================
def dodaj_stacje():
    nazwa = entry_nazwa_stacji.get()
    lokalizacja = entry_lokalizacja_stacji.get()
    if nazwa and lokalizacja:
        stacja = StacjaMeteo(nazwa, lokalizacja)
        stacje_meteo.append(stacja)
        entry_nazwa_stacji.delete(0, END)
        entry_lokalizacja_stacji.delete(0, END)
        update_comboboxes()
        pokaz_mape_stacji()

def dodaj_pracownika():
    imie = entry_imie_pracownika.get()
    nazwisko = entry_nazwisko_pracownika.get()
    indeks = combo_stacja_pracownika.current()
    if imie and nazwisko and indeks >= 0:
        p = Pracownik(imie, nazwisko, stacje_meteo[indeks])
        pracownicy.append(p)
        entry_imie_pracownika.delete(0, END)
        entry_nazwisko_pracownika.delete(0, END)
        combo_stacja_pracownika.set('')
        pokaz_mape_pracownikow()

def dodaj_klienta():
    imie = entry_imie_klienta.get()
    indeks = combo_stacja_klienta.current()
    if imie and indeks >= 0:
        k = Klient(imie, stacje_meteo[indeks])
        klienci.append(k)
        entry_imie_klienta.delete(0, END)
        combo_stacja_klienta.set('')
        pokaz_mape_klientow()

def update_comboboxes():
    nazwy = [s.nazwa for s in stacje_meteo]
    combo_stacja_pracownika['values'] = nazwy
    combo_stacja_klienta['values'] = nazwy

# ===================== GUI =====================
root = Tk()
root.geometry("1200x950")
root.title("System zarządzania wypożyczalniami rowerów")

# ----- PRZYCISKI MAPY -----
frame_kontrola_mapy = Frame(root)
frame_kontrola_mapy.pack(pady=10)

Button(frame_kontrola_mapy, text="Mapa wypożyczalni", command=pokaz_mape_stacji).grid(row=0, column=0, padx=5)
Button(frame_kontrola_mapy, text="Mapa pracowników", command=pokaz_mape_pracownikow).grid(row=0, column=1, padx=5)
Button(frame_kontrola_mapy, text="Mapa klientów", command=pokaz_mape_klientow).grid(row=0, column=2, padx=5)

# ----- MAPA -----
frame_mapa = Frame(root)
frame_mapa.pack()

map_widget = tkintermapview.TkinterMapView(frame_mapa, width=1150, height=600, corner_radius=5)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)
map_widget.pack()

# ----- FORMULARZE -----
frame_formularze = Frame(root)
frame_formularze.pack(pady=10)

# STACJA
Label(frame_formularze, text="Dodaj stację:").grid(row=0, column=0, sticky=W)
entry_nazwa_stacji = Entry(frame_formularze, width=20)
entry_nazwa_stacji.grid(row=0, column=1)
entry_lokalizacja_stacji = Entry(frame_formularze, width=20)
entry_lokalizacja_stacji.grid(row=0, column=2)
Button(frame_formularze, text="Dodaj stację", command=dodaj_stacje).grid(row=0, column=3)

# PRACOWNIK
Label(frame_formularze, text="Dodaj pracownika:").grid(row=1, column=0, sticky=W)
entry_imie_pracownika = Entry(frame_formularze, width=15)
entry_imie_pracownika.grid(row=1, column=1)
entry_nazwisko_pracownika = Entry(frame_formularze, width=15)
entry_nazwisko_pracownika.grid(row=1, column=2)
combo_stacja_pracownika = ttk.Combobox(frame_formularze, width=20, state="readonly")
combo_stacja_pracownika.grid(row=1, column=3)
Button(frame_formularze, text="Dodaj pracownika", command=dodaj_pracownika).grid(row=1, column=4)

# KLIENT
Label(frame_formularze, text="Dodaj klienta:").grid(row=2, column=0, sticky=W)
entry_imie_klienta = Entry(frame_formularze, width=15)
entry_imie_klienta.grid(row=2, column=1)
combo_stacja_klienta = ttk.Combobox(frame_formularze, width=20, state="readonly")
combo_stacja_klienta.grid(row=2, column=2)
Button(frame_formularze, text="Dodaj klienta", command=dodaj_klienta).grid(row=2, column=3)

root.mainloop()
