import csv
from datetime import datetime
date_sola=[]
temp_sola=[]
pressure_sola=[]

date_gokk=[]
temp_gokk=[]
pressure_gokk=[]

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
            
        print(date_sola[:2], temp_sola[:2], pressure_sola[:2])

def open_file2():
    with open('trykk_og_temperaturlogg_rune_time.csv',mode='r',encoding='utf-8') as file2:
        reader=csv.reader(file2, delimiter=';')
        header=next(reader)
        date_index2 = header.index('Dato og tid')
        temp_index2 = header.index('Temperatur (gr Celsius)')
        pressure_index2 = header.index('Trykk - absolutt trykk maaler (bar)')
        for row in reader:
            date2=row[date_index2].strip()
            temp2 = row[temp_index2].replace(',', '.')
            pressure2 = row[pressure_index2].replace(',', '.')

            #####if date1 is None:
            #####    continue
            date_gokk.append(date2)
            temp_gokk.append(temp2)
            pressure_gokk.append(pressure2)

        print(date_gokk[:2], temp_gokk[:2], pressure_gokk[:2])

open_file1()
open_file2()
