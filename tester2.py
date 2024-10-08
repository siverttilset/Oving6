import csv
from datetime import datetime
import matplotlib.pyplot as plt

date_sola = []
temp_sola = []
pressure_sola = []

date_gokk = []
temp_gokk = []
pressure_gokk = []


def plot():
    n = 30
    smoothed_dates, smoothed_temps = gjennomsnitts_utregning(date_gokk, temp_gokk, n)

    plt.plot(date_gokk, temp_gokk, label='Original Temperatur')
    plt.plot(smoothed_dates, smoothed_temps, label=f'Gjennomsnittstemperatur', color='orange')
    plt.plot(date_sola, temp_sola, color='green', label=f'Temperatur MET')
    plt.xlabel('Tid')
    plt.ylabel('Temperatur (°C)')
    plt.title('Temperatur med Glattet Gjennomsnitt')
    plt.legend()

    #plt.gcf().autofmt_xdate()  # Roterer tidsstemplene på x-aksen for bedre lesbarhet
    plt.tight_layout()
    plt.show()

    print('file1', date_sola[:2], temp_sola[:2], pressure_sola[:2])
    print('file2', date_gokk[:2], temp_gokk[:2], pressure_gokk[:2])
    print('sola,', len(date_sola))
    print('gokk', len(date_gokk))

def convert_date_format(date_str, norsk_format:bool):
    try:
        if norsk_format == True:
            date_time = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        else:
            date_time = datetime.strptime(date_str, '%m.%d.%Y %H:%M')
        return date_time
    except ValueError:
        try:
            date_time = datetime.strptime(date_str, '%m/%d/%Y %I:%M:%S %p')
            return date_time
        except ValueError:
            return None

def open_file1():
    with open('temperatur_trykk_met_samme_rune_time_datasett.csv', mode='r', encoding='utf-8') as file1:
        reader = csv.reader(file1, delimiter=';')
        header = next(reader)
        date_index1 = header.index('Tid(norsk normaltid)')
        temp_index1 = header.index('Lufttemperatur')
        pressure_index1 = header.index('Lufttrykk i havnivå')
        for row in reader:
            date1 = row[date_index1].strip()
            date1 = convert_date_format(date1, True)
            temp1 = row[temp_index1].replace(',', '.')
            pressure1 = row[pressure_index1].replace(',', '.')
            if not temp1:
                continue
            date_sola.append(date1)
            temp_sola.append(float(temp1))
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
            date2 = convert_date_format(date2, False)
            if date2 is None:
                continue
            date_gokk.append(date2)
            temp_gokk.append(float(temp2))
            pressure_gokk.append(float(pressure2))


def gjennomsnitts_utregning(tider:list, temperatur:list, gjennomsnittsverdi:int):
    gjennomsnitts_liste_temperatur = []
    gyldige_tidspunkter = []
    lengde_templiste = len(temperatur)
    for x,i in enumerate(tider):
        if x >= gjennomsnittsverdi and x < lengde_templiste-gjennomsnittsverdi:
            sum_temp = 0
            for v in range(-gjennomsnittsverdi, gjennomsnittsverdi+1, 1):
                sum_temp += float(temperatur[x+v])
            gjennomsnitts_liste_temperatur.append(float(f'{sum_temp/((gjennomsnittsverdi*2)+1):.2f}'))
            gyldige_tidspunkter.append(i)
        else:                                                       ##### Disse 3 linjene kan fjernes hvis vi KUN skal ha med
            gjennomsnitts_liste_temperatur.append(temperatur[x])    ##### "gyldige" verdier med gjennomsnitt. Da vil de n første
            gyldige_tidspunkter.append(tider[x])                    ##### og n siste verdiene ikke returneres i det hele tatt


    return gyldige_tidspunkter, gjennomsnitts_liste_temperatur

open_file1()
open_file2()
plot()

print(type(date_sola[3]))