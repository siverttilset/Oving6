

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
        if len(row) < 6:  # Check if the row has at least 6 columns
            continue  # Skip the row if it doesn't

        name_str = row[0]    #navn
        station = row[1]    #station
        date_str = row[2]  # Date and time
        temperature = float(row[3].replace(',', '.'))  # Temperature
        pressure = float(row[4].replace(',', '.'))  # Pressure

        # Further processing here

        
        # Parse the date and time
        date_time = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        sola_dates.append(date_time)
        sola_temperatures.append(temperature)
        sola_pressures.append(pressure)

# Print some values to verify
print(sola_dates[:4], sola_temperatures[:4], sola_pressures[:4])














