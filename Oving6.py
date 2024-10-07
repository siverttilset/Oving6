import csv
from datetime import datetime

# Define lists for storing data
sola1_dates = []
sola1_temperatures = []
sola1_pressures = []
sola2_dates = []
sola2_temperatures = []
sola2_pressures = []


def process_file(filename, date_format):
    def parse_date(date_str, current_format):
        """Parse the date string based on the provided format and convert to a unified format."""
        try:
            # Parse the date using the provided format
            date2_time = datetime.strptime(date_str, current_format)
            # Return a unified format: day, month, year
            return date2_time.strftime('%d.%m.%Y %H:%M')
        except ValueError:
            print(f"Date format issue with: {date_str}")
            return None
        


    # Read the Sola station data
    with open('temperatur_trykk_met_samme_rune_time_datasett.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            # Get the date string
            date1_str = row['Tid(norsk normaltid)'].strip()  # Strip to remove leading/trailing spaces

            # Check if date_str is empty and skip if it is
            if not date1_str:
                continue
            
            # Parse temperature and pressure
            temperature1 = row['Lufttemperatur'].replace(',', '.')
            pressure1 = row['Lufttrykk i havnivå'].replace(',', '.')
            


            # Try to parse the date and time
            try:
                date1_time = (date1_str)
                sola1_dates.append(date1_time)
                sola1_temperatures.append(float(temperature1))
                sola1_pressures.append(float(pressure1))
            except ValueError:
                # Skip the row if the date format doesn't match
                print(f"Skipping row with date format issue: {date1_str}")
                continue



    with open('trykk_og_temperaturlogg_rune_time.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            # Get the date string
            date2_str = row['Dato og tid'].strip()  # Strip to remove leading/trailing spaces

            # Check if date_str is empty and skip if it is
            if not date2_str:
                continue
            
            # Parse temperature and pressure
            temperature2 = row['Temperatur (gr Celsius)'].replace(',', '.')
            pressure2 = row['Trykk - absolutt trykk maaler (bar)'].replace(',', '.')
            


            # Parse the date using the given format
                unified_date_str = parse_date(date2_str, date_format)
                if unified_date_str is None:
                    continue
            # Try to parse the date and time
            try:
                date2_time = (date2_str)
                sola2_dates.append(date2_time)
                sola2_temperatures.append(float(temperature2))
                sola2_pressures.append(float(pressure2))
            except ValueError:
                # Skip the row if the date format doesn't match
                print(f"Skipping row with date format issue: {date2_str}")
                continue


# Print some values to verify
print(sola1_dates[:2], sola1_temperatures[:2], sola1_pressures[:2])
print(sola2_dates[:2], sola2_temperatures[:2], sola2_pressures[:2])
