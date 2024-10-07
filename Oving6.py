

import csv
from datetime import datetime

# Define lists for storing data
sola_dates = []
sola_temperatures = []
sola_pressures = []

# Read the Sola station data
with open('temperatur_trykk_met_samme_rune_time_datasett.txt', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Skip header
    for row in reader:
        date_str = row[2]  # Date and time
        temperature = float(row[4].replace(',', '.'))  # Temperature
        pressure = float(row[5].replace(',', '.'))  # Pressure
        
        # Parse the date and time
        date_time = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        sola_dates.append(date_time)
        sola_temperatures.append(temperature)
        sola_pressures.append(pressure)

# Print some values to verify
print(sola_dates[:5], sola_temperatures[:5], sola_pressures[:5])



























