from tkinter import *
import tkintermapview

stations: list = []

class BikeStation:
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.name)

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup

        url = f'https://pl.wikipedia.org/wiki/{self.location}'
        response = requests.get(url).text
        response_html = BeautifulSoup(response, 'html.parser')
        longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        return [latitude, longitude]

def add_station():
    name = entry_name.get()
    location = entry_location.get()
    stations.append(BikeStation(name=name, location=location))
    show_stations()
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_name.focus()

def show_stations():
    listbox.delete(0, END)
    for idx, station in enumerate(stations):
        listbox.insert(idx, f'{idx + 1}. {station.name} | {station.location}')

def remove_station():
    i = listbox.index(ACTIVE)
    stations[i].marker.delete()
    stations.pop(i)
    show_stations()

def edit_station():
    i = listbox.index(ACTIVE)
    entry_name.insert(0, stations[i].name)
    entry_location.insert(0, stations[i].location)
    button_add.config(text="Zapisz", command=lambda: update_station(i))

def update_station(i):
    stations[i].marker.delete()
    stations[i].name = entry_name.get()
    stations[i].location = entry_location.get()
    stations[i].coordinates = stations[i].get_coordinates()
    stations[i].marker = map_widget.set_marker(stations[i].coordinates[0], stations[i].coordinates[1], text=stations[i].name)
    show_stations()
    button_add.config(text="Dodaj", command=add_station)
    entry_name.delete(0, END)
    entry_location.delete(0, END)

def show_station_details():
    i = listbox.index(ACTIVE)
    label_name_val.config(text=stations[i].name)
    label_location_val.config(text=stations[i].location)
    map_widget.set_zoom(12)
    map_widget.set_position(stations[i].coordinates[0], stations[i].coordinates[1])

root = Tk()
root.title('Mapa wypożyczalni rowerów')
root.geometry('1200x700')

frame_list = Frame(root)
frame_form = Frame(root)
frame_details = Frame(root)
frame_map = Frame(root)

frame_list.grid(row=0, column=0, padx=50)
frame_form.grid(row=0, column=1)
frame_details.grid(row=1, column=0, columnspan=2)
frame_map.grid(row=2, column=0, columnspan=2)

# Lista stacji
Label(frame_list, text='Lista wypożyczalni rowerowych').grid(row=0, column=0)
listbox = Listbox(frame_list, width=60)
listbox.grid(row=1, column=0, columnspan=3)
Button(frame_list, text='Szczegóły', command=show_station_details).grid(row=2, column=0)
Button(frame_list, text='Usuń', command=remove_station).grid(row=2, column=1)
Button(frame_list, text='Edytuj', command=edit_station).grid(row=2, column=2)

# Formularz
Label(frame_form, text='Nowa stacja').grid(row=0, column=0, columnspan=2)
Label(frame_form, text='Nazwa').grid(row=1, column=0, sticky=W)
Label(frame_form, text='Miejscowość').grid(row=2, column=0, sticky=W)

entry_name = Entry(frame_form)
entry_name.grid(row=1, column=1)
entry_location = Entry(frame_form)
entry_location.grid(row=2, column=1)

button_add = Button(frame_form, text='Dodaj', command=add_station)
button_add.grid(row=3, column=0, columnspan=2)

# Szczegóły stacji
Label(frame_details, text='Szczegóły stacji:').grid(row=0, column=0, columnspan=2)

Label(frame_details, text='Nazwa:').grid(row=1, column=0, sticky=E)
label_name_val = Label(frame_details, text='---')
label_name_val.grid(row=1, column=1, sticky=W)

Label(frame_details, text='Miejscowość:').grid(row=1, column=2, sticky=E)
label_location_val = Label(frame_details, text='---')
label_location_val.grid(row=1, column=3, sticky=W)

# Mapa
map_widget = tkintermapview.TkinterMapView(frame_map, width=1200, height=450)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23, 21.00)  # Warszawa
map_widget.set_zoom(6)

root.mainloop()
