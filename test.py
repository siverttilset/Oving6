# Her fungerer koden, alle datoer er lagt til i hver sin liste. I tillegg er datoene nå skrevet på lik form





import csv
from datetime import datetime
date_sola=[]
temp_sola=[]
pressure_sola=[]

date_gokk=[]
temp_gokk=[]
pressure_gokk=[]


def convert_date_format(date_str):
    """Converts different date formats to DD.MM.YYYY HH:MM."""
    try:
        # First, try parsing with the DD.MM.YYYY HH:MM format
        date_time = datetime.strptime(date_str, '%m.%d.%Y %H:%M')
        # If it succeeds, the date is already in the correct format
        return date_time.strftime('%d. %H:%M')
    except ValueError:
        try:
            # Try parsing with the MM/DD/YYYY hh:mm:ss AM/PM format
            date_time = datetime.strptime(date_str, '%m/%d/%Y %I:%M:%S %p')
            # Convert it to DD.MM.YYYY HH:MM format (24-hour format)
            return date_time.strftime('%d. %H:%M')
        except ValueError:
            # If neither format works, print an error and return the original date string
            #print(f"Date format issue with: {date_str}")
            return date_str
    





def open_file1():
    with open('temperatur_trykk_met_samme_rune_time_datasett.csv',mode='r',encoding='utf-8') as file1:
        reader=csv.reader(file1, delimiter=';')
        header=next(reader)
        date_index1 = header.index('Tid(norsk normaltid)')
        temp_index1 = header.index('Lufttemperatur')
        pressure_index1 = header.index('Lufttrykk i havnivå')
        for row in reader:
            date1=row[date_index1].strip()
            temp1 = row[temp_index1].replace(',', '.')
            pressure1 = row[pressure_index1].replace(',', '.')

            

            #####if date1 is None:
            #####    continue
            date_sola.append(date1)
            temp_sola.append(temp1)
            pressure_sola.append(pressure1)
        
        

def open_file2():
    with open('trykk_og_temperaturlogg_rune_time.csv', mode='r', encoding='utf-8') as file2:
        reader2 = csv.reader(file2, delimiter=';')
        header2 = next(reader2)
        date_index2 = header2.index('Dato og tid')
        temp_index2 = header2.index('Temperatur (gr Celsius)')
        pressure_index2 = header2.index('Trykk - absolutt trykk maaler (bar)')
        for row in reader2:
            date2 = row[date_index2].strip()
            temp2 = row[temp_index2].replace(',', '.')
            pressure2 = row[pressure_index2].replace(',', '.')

            # Convert the date format using the function
            date2 = convert_date_format(date2)
            if date2 is None:
                continue

            date_gokk.append(date2)
            temp_gokk.append(float(temp2))
            pressure_gokk.append(float(pressure2))

        
        


open_file1()
open_file2()



print('file1',date_sola[:2], temp_sola[:2], pressure_sola[:2])
print('file2',date_gokk[:2], temp_gokk[:2], pressure_gokk[:2])
print('sola,',len(date_sola))
print('gokk', len(date_gokk))