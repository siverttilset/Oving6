import csv
from datetime import datetime
import matplotlib.pyplot as plt

date_sola = []
temp_sola = []
trykk_sola = []

date_gokk = []
temp_gokk = []
trykk_gokk = []

trykk_absolutt = []
gyldige_tider_trykk = []


def plot():
    fig,ax = plt.subplots(2,1)
    temp = ax[0]
    trykk = ax[1]

    gjennomsnitts_dato, gjennomsnitts_temp = gjennomsnitts_utregning(date_gokk, temp_gokk, 30)
    temp.plot(date_gokk, temp_gokk, label='Temperatur')
    temp.plot([date_gokk[1128], date_gokk[4570]], [temp_gokk[1128], temp_gokk[4570]],label=f'Temperaturfall maksimal til minimal',color='purple')
    temp.plot(gjennomsnitts_dato, gjennomsnitts_temp, label=f'Gjennomsnittstemp.', color='orange')
    temp.plot(date_sola, temp_sola, label=f'Temperatur MET', color='green')
    temp.set_ylabel('Temperatur (°C)')
    temp.set_title('Temperatur')
    temp.legend()

    trykk.plot(date_sola, trykk_sola, label='Absolutt trykk MET',color='green')
    trykk.plot(gyldige_tider_trykk, trykk_gokk, label='Barometrisk lufttrykk', color='orange')
    trykk.plot(date_gokk, trykk_absolutt, label='Absolutt trykk')
    trykk.legend()
    trykk.set_ylabel('Trykk (millibar)')
    trykk.set_title('Trykk')
    plt.show()

def convert_date_format(date_str, norsk_format:bool):
    try:
        if norsk_format == True:
            date_time = datetime.strptime(date_str, '%d.%m.%Y %H:%M')  # 24T dag/måned/år
        else:
            date_time = datetime.strptime(date_str, '%m.%d.%Y %H:%M')  # 24T måned/dag/år
        return date_time
    except ValueError:
        try:
            date_time = datetime.strptime(date_str, '%m/%d/%Y %I:%M:%S %p')  # AM/PM format
            return date_time
        except ValueError:
            try:
                date_time = datetime.strptime(date_str, '%m/%d/%Y 00:%M:%S %p')  # hvis timen er 00 i AM/PM format
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
            trykk_sola.append(float(pressure1))

def open_file2():
    with open('trykk_og_temperaturlogg_rune_time.csv', mode='r', encoding='utf-8') as file2:
        reader2 = csv.reader(file2, delimiter=';')
        header2 = next(reader2)
        date_index2 = header2.index('Dato og tid')
        temp_index2 = header2.index('Temperatur (gr Celsius)')
        absolutt_trykk = header2.index('Trykk - absolutt trykk maaler (bar)')
        trykk_barometer = header2.index('Trykk - barometer (bar)')

        for row in reader2:
            date2 = row[date_index2].strip()
            temp2 = row[temp_index2].replace(',', '.')
            pressure2 = row[trykk_barometer].replace(',', '.')
            abstrykk2 = row[absolutt_trykk].replace(',', '.')
            date2 = convert_date_format(date2, False)
            date_gokk.append(date2)
            temp_gokk.append(float(temp2))
            if pressure2:
                pressure2 = float(pressure2) * 10
                trykk_gokk.append(float(f'{pressure2:.1f}'))
                gyldige_tider_trykk.append(date2)
            if abstrykk2:
                abstrykk2 = float(abstrykk2) * 10
                trykk_absolutt.append(float(f'{abstrykk2:.1f}'))



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

