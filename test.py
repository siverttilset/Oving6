import csv
from datetime import datetime

# Define lists for storing data
dates1 = []
temperatures1 = []
pressures1 = []
dates2 = []
temperatures2 = []
pressures2 = []


def parse_date(date2_str, current_format):
    """Parse the date string based on the provided format and convert to a unified format."""
    try:
        # Parse the date using the provided format
        date_time = datetime.strptime(date2_str, current_format)
        # Return a unified format: day, month, year
        return date_time.strftime('%d.%m.%Y %H:%M')
    except ValueError:
        print(f"Date format issue with: {date1_str}")
        return None

def process_file(file2, date_format):
    with open('temperatur_trykk_met_samme_rune_time_datasett.csv',mode='r',encoding='utf-8') as file1:
        reader1 = csv.reader(file1, delimiter=';')
        header1 = next(reader1)  # Read the header row
        date_index1 = header1.index('Tid(norsk normaltid)')
        temp_index1 = header1.index('Lufttemperatur')
        pressure_index1 = header1.index('Lufttrykk i havnivå')

        for row in reader1:
            date1_str=row[date_index1].strip()

            temperature1 = row[temp_index1].replace(',', '.')
            pressure1 = row[pressure_index1].replace(',', '.')

            unified_date_str = parse_date(date1_str, date_format)
            if unified_date_str is None:
                continue
            
            date_time = datetime.strptime(unified_date_str, '%d.%m.%Y %H:%M')
            dates1.append(date_time)
            temperatures1.append(float(temperature1))
            pressures1.append(float(pressure1))



    with open('trykk_og_temperaturlogg_rune_time.csv', mode='r',encoding='utf-8') as file2:
        reader2 = csv.reader(file2, delimiter=';')
        header2 = next(reader2)  # Read the header row
        date_index2 = header2.index('Dato og tid')
        temp_index2 = header2.index('Temperatur (gr Celsius)')
        pressure_index2 = header2.index('Trykk - absolutt trykk maaler (bar)')
        
        for row in reader2:
            date2_str = row[date_index2].strip()
    
            temperature2 = row[temp_index2].replace(',', '.')
            pressure2 = row[pressure_index2].replace(',', '.')
            

            # Parse the date using the given format
            unified_date_str = parse_date(date2_str, date_format)
            if unified_date_str is None:
                continue

            # Convert unified date string back to a datetime object for further processing
            date_time = datetime.strptime(unified_date_str, '%d.%m.%Y %H:%M')
            dates2.append(date_time)
            temperatures2.append(float(temperature2))
            pressures2.append(float(pressure2))

            
print(dates1[:2], temperatures1[:2], pressures1[:2])
print(dates2[:2], temperatures2[:2], pressures2[:2])





    #def parse_date(date1_str, current_format):
    # """Parse the date string based on the provided format and convert to a unified format."""
        #try:
            # Parse the date using the provided format
            #date_time = datetime.strptime(date1_str, current_format)
            # Return a unified format: day, month, year
            #return date_time.strftime('%d.%m.%Y %H:%M')
        #except ValueError:
            #print(f"Date format issue with: {date1_str}")
            #return None

    # Function to read and process the file
    #def process_file(filename, date_format):
        #with open('temperatur_trykk_met_samme_rune_time_datasett.csv', mode='r', encoding='utf-8') as file1:
         #   reader1 = csv.reader(file1, delimiter=';')
          #  header1 = next(reader1)  # Read the header row
            
            # Identify the indices for the relevant columns
           # date_index1 = header1.index('Tid(norsk normaltid)')
           # temp_index1 = header1.index('Lufttemperatur')
           # pressure_index1 = header1.index('Lufttrykk i havnivå')
            
          #  for row in reader1:
          #      date1_str = row[date_index1].strip()
          #      if not date1_str:
          #          continue
        
                # Parse temperature and pressure
           #     temperature1 = row[temp_index1].replace(',', '.')
           #     pressure1 = row[pressure_index1].replace(',', '.')
                
                # Parse the date using the given format
            #    unified_date_str = parse_date(date1_str, date_format)
            #    if unified_date_str is None:
            #        continue

                # Convert unified date string back to a datetime object for further processing
             #   date_time = datetime.strptime(unified_date_str, '%d.%m.%Y %H:%M')
             #   dates.append(date_time)
             #   temperatures.append(float(temperature1))
             #   pressures.append(float(pressure1))
        #with open('trykk_og_temperaturlogg_rune_time.csv', mode='r',encoding='utf-8') as file2:
        #    reader2 = csv.reader(file2, delimiter=';')
        #    header2 = next(reader2)  # Read the header row
            
            # Identify the indices for the relevant columns
         #   date_index2 = header2.index('Dato og tid')
         #   temp_index2 = header2.index('Temperatur (gr Celsius)')
         #   pressure_index2 = header2.index('Trykk - absolutt trykk maaler (bar)')
            
          #  for row in reader2:
          #      date2_str = row[date_index2].strip()
          #      if not date2_str:
          #          continue
        
                # Parse temperature and pressure
           #     temperature2 = row[temp_index2].replace(',', '.')
           #     pressure2 = row[pressure_index2].replace(',', '.')
                
                # Parse the date using the given format
            #    unified_date_str = parse_date(date2_str, date_format)
            #    if unified_date_str is None:
            #        continue

                # Convert unified date string back to a datetime object for further processing
              #  date_time = datetime.strptime(unified_date_str, '%d.%m.%Y %H:%M')
             #   dates.append(date_time)
              #  temperatures.append(float(temperature2))
              #  pressures.append(float(pressure2))


# Process the first file where the date format is '%d.%m.%Y %H:%M'
#process_file('temperatur_trykk_met_samme_rune_time_datasett.csv', '%d.%m.%Y %H:%M')

# Process the second file where the date format is '%m.%d.%Y %H:%M'
#process_file('trykk_og_temperaturlogg_rune_time.csv', '%m.%d.%Y %H:%M')

# Print some values to verify
#print(dates[:2], temperatures[:2], pressures[:2])


