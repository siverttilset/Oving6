import csv
from datetime import datetime

# Define lists for storing data
sola_dates = []
sola_temperatures = []
sola_pressures = []

# Read the Sola station data
with open('temperatur_trykk_met_samme_rune_time_datasett.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    #next(reader)  # Skip header
    for row in reader:
        #name = row['Navn']    #navn
        #print(name_str)
        #station = row['Stasjon']    #station
        date_str = row['Tid(norsk normaltid)']  # Date and time
        temperature=row['Lufttemperatur']
        pressure=row['Lufttrykk i havnivå']
        #temperature = float(row[3].replace(',', '\t'))  # Temperature
        #pressure = float(row[4].replace(',', '\t'))  # Pressure
        #if len(row) < 6:  # Check if the row has at least 6 columns
        #    continue  # Skip the row if it doesn't
        # Further processing here

        
        # Parse the date and time
        date_time = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        sola_dates.append(date_time)
        sola_temperatures.append(temperature)
        sola_pressures.append(pressure)

# Print some values to verify
print(sola_dates[:2], sola_temperatures[:2], sola_pressures[:2])
#print(sola_dates)
#print(sola_pressures)
#print(sola_temperatures)
#print(header)