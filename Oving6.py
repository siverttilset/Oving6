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
    smoothed_dates, smoothed_temps = smooth_temperature(date_gokk, temp_gokk, n)

    plt.plot(date_gokk, temp_gokk, label='Original Temperatur (Gokk)')
    plt.plot(smoothed_dates, smoothed_temps, label=f'Smoothed Temperatur (n={n})', color='orange')

    # Convert temp_sola to float and plot it
    temp_sola_float = [float(temp) for temp in temp_sola]
    plt.plot(date_sola, temp_sola_float, label='Original Temperatur (Sola)', color='green')

    plt.xlabel('Tid')
    plt.ylabel('Temperatur (°C)')
    plt.title('Temperatur med Glattet Gjennomsnitt')
    plt.legend()

    plt.gcf().autofmt_xdate()  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()

    print('file1', date_sola[:2], temp_sola[:2], pressure_sola[:2])
    print('file2', date_gokk[:2], temp_gokk[:2], pressure_gokk[:2])
    print('sola,', len(date_sola))
    print('gokk', len(date_gokk))

def convert_date_format(date_str):
    try:
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
            temp1 = row[temp_index1].replace(',', '.')
            pressure1 = row[pressure_index1].replace(',', '.')
            date1 = convert_date_format(date1)
            if date1 is None:
                continue
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
            date2 = convert_date_format(date2)
            if date2 is None:
                continue
            date_gokk.append(date2)
            temp_gokk.append(float(temp2))
            pressure_gokk.append(float(pressure2))

def smooth_temperature(dates, temperatures, n):
    smoothed_dates = []
    smoothed_temps = []
    if len(dates) != len(temperatures):
        raise ValueError("Listene for tidspunkter og temperaturer må ha samme lengde.")
    for i in range(n, len(temperatures) - n):
        window = temperatures[i - n:i + n + 1]
        avg_temp = sum(window) / len(window)
        smoothed_dates.append(dates[i])
        smoothed_temps.append(avg_temp)
    return smoothed_dates, smoothed_temps

open_file1()
open_file2()
plot()
