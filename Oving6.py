
import csv
from datetime import datetime

from numpy import column_stack

# Define lists for storing data
sola_dates = []
sola_temperatures = []
sola_pressures = []

# Read the Sola station data
with open('temperatur_trykk_met_samme_rune_time_datasett.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Skip header
    for row in reader:
<<<<<<< Updated upstream
        date_str = row[2]  # Date and time
        temperature = float(row[4].replace(',', '.'))  # Temperature
        pressure = float(row[5].replace(',', '.'))  # Pressure
=======
        date_str = column_stack[2]  # Date and time
        temperature = float(column_stack[4].replace(',', '.'))  # Temperature
        pressure = float(column_stack[5].replace(',', '.'))  # Pressure
>>>>>>> Stashed changes
        
        # Parse the date and time
        date_time = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        sola_dates.append(date_time)
        sola_temperatures.append(temperature)
        sola_pressures.append(pressure)

# Print some values to verify
<<<<<<< Updated upstream
print(sola_dates[:5], sola_temperatures[:5], sola_pressures[:5])
=======
print(sola_dates[:2], sola_temperatures[:2], sola_pressures[:2])
print(sola_dates)
print(sola_pressures)
print(sola_temperatures)


>>>>>>> Stashed changes






















<<<<<<< Updated upstream





=======
>>>>>>> Stashed changes
tester23213213213
sdf