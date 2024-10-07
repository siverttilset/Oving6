

import csv
from datetime import datetime
import matplotlib

# Define lists for storing data
sola_dates = []
sola_temperatures = []
sola_pressures = []

# Read the Sola station data
with open('temperatur_trykk_met_samme_rune_time_datasett.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Skip header
    for row in reader:
        name_str =str(row[0])   #navn
        #station = row[1]   #station
        date =float(row[2])  # Date and time
        temperature=float(row[3])
        pressure=float(row[4])
        #if len(row) < 6:  # Check if the row has at least 6 columns
        #    continue  # Skip the row if it doesn't
        # Further processing here

        
        # Parse the date and time
        date_time = datetime.strptime(date, '%d.%m.%Y %H:%M')
        sola_dates.append(date_time)
        sola_temperatures.append(temperature)
        sola_pressures.append(pressure)

# Print some values to verify
print(sola_dates[:2], sola_temperatures[:2], sola_pressures[:2])
print(sola_dates)
print(sola_pressures)
print(sola_temperatures)





main







