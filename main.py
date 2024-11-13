import matplotlib.pyplot as plt
import csv
import datetime
import math

###   gruppe 104

data_sola: dict[str, dict[datetime.datetime, float]] = {
    'temperatur':{},
    'trykk':{}
}
data_lang: dict[str, dict[datetime.datetime, float]] = {
    'temperatur':{},
    'baro_trykk':{},
    'abs_trykk':{}
}
data_sauda: dict[str, dict[datetime.datetime, float]] = {
    'temperatur':{},
    'trykk':{}
}
data_sinnes: dict[str, dict[datetime.datetime, float]] = {
    'temperatur':{},
    'trykk':{}
}

def debug():
    print(f'Sola temp: {list(data_sola["temperatur"].items())[:2]}')
    print(f'Sola trykk: {list(data_sola["trykk"].items())[:2]}\n')
    print(f'Sauda temp: {list(data_sauda["temperatur"].items())[:2]}')
    print(f'Sauda trykk: {list(data_sauda["trykk"].items())[:2]}\n')
    print(f'Sinnes temp: {list(data_sinnes["temperatur"].items())[:2]}')
    print(f'Sinnes trykk: {list(data_sinnes["trykk"].items())[:2]}\n')
    print(f'Lang temp: {list(data_lang["temperatur"].items())[:2]}')
    print(f'Lang abs trykk: {list(data_lang["abs_trykk"].items())[:2]}')
    print(f'Lang baro trykk: {list(data_lang["baro_trykk"].items())[:2]}')

starttid = None

def dato_konverterer(dato_streng:str, norsk_format:bool=False, sekunder:int=-1) -> datetime.datetime:
    dato_formater = ['%m.%d.%Y %H:%M', '%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y 00:%M:%S %p']
    if sekunder == 0:
        for format in dato_formater:
            try:
                ny_datetime = datetime.datetime.strptime(dato_streng, format)
                global starttid
                starttid = ny_datetime #+ datetime.timedelta(seconds=8)
                return starttid
            except ValueError:
                pass
    if norsk_format:
        return datetime.datetime.strptime(dato_streng, '%d.%m.%Y %H:%M')
    else:
        ny_datetime = starttid + datetime.timedelta(seconds=sekunder)
        return ny_datetime

def les_fil(fil_sti: str):
    with open(fil_sti, 'r', encoding='UTF-8') as fil:
        csv_objekt = csv.reader(fil, delimiter=';')
        header = next(csv_objekt)
        dato_indeks = header.index('Tid(norsk normaltid)')
        temp_indeks = header.index('Lufttemperatur')
        trykk_indeks = header.index('Lufttrykk i havnivå')
        for row in csv_objekt:
            if len(row) != len(header):
                continue

            if row[0] == 'Sirdal - Sinnes':
                riktig_dict = data_sinnes
            elif row[0] == 'Sola':
                riktig_dict = data_sola
            elif row[0] == 'Sauda':
                riktig_dict = data_sauda
            dato = row[dato_indeks].strip()
            temp = row[temp_indeks].strip().replace(',', '.')
            trykk = row[trykk_indeks].strip().replace(',', '.')
            if dato and temp:
                dato_datetime = dato_konverterer(dato, True)
                riktig_dict['temperatur'][dato_datetime] = float(temp)
                if trykk:
                    riktig_dict['trykk'][dato_datetime] = float(trykk)

def les_lang_fil():
    with open('trykk_og_temperaturlogg_rune_time.csv', 'r', encoding='UTF-8') as fil:
        csv_objekt = csv.reader(fil, delimiter=';')
        header = next(csv_objekt)
        dato_indeks = header.index('Dato og tid')
        temp_indeks = header.index('Temperatur (gr Celsius)')
        baro_trykk_indeks = header.index('Trykk - barometer (bar)')
        sekunder_indeks = header.index('Tid siden start (sek)')
        abs_trykk_indeks = header.index('Trykk - absolutt trykk maaler (bar)')
        for row in csv_objekt:
            if len(row) != len(header):
                continue
            dato = row[dato_indeks].strip()
            temp = row[temp_indeks].strip().replace(',', '.')
            baro_trykk = row[baro_trykk_indeks].strip().replace(',', '.')
            sekunder = row[sekunder_indeks].strip()
            abs_trykk = row[abs_trykk_indeks].strip().replace(',','.')
            if dato and temp:
                dato_datetime = dato_konverterer(dato, sekunder=float(sekunder))
                data_lang['temperatur'][dato_datetime] = float(temp)
                if baro_trykk:
                    data_lang['baro_trykk'][dato_datetime] = float(baro_trykk)*10
                if abs_trykk:
                    data_lang['abs_trykk'][dato_datetime] = float(abs_trykk)*10

def gjennomsnitts_utregning(data:dict, gjennomsnittsverdi:int) -> tuple[list, list]:
    tider = list(data.keys())
    temperatur = list(data.values())
    gjennomsnitts_liste_temperatur = []
    gyldige_tidspunkter = []
    std_avvik = []
    for index,dato in enumerate(tider[gjennomsnittsverdi:len(tider)-gjennomsnittsverdi], gjennomsnittsverdi):
        sum_temp = 0
        temp_rundt = temperatur[index-gjennomsnittsverdi:index+gjennomsnittsverdi+1]
        for temp in temp_rundt:
            sum_temp += temp
        std_avvik.append(standard_avvik(temp_rundt))
        gjennomsnitts_liste_temperatur.append(sum_temp/((gjennomsnittsverdi*2)+1))
        gyldige_tidspunkter.append(dato)
    return gyldige_tidspunkter, gjennomsnitts_liste_temperatur, std_avvik

def gjennomsnittlig_forskjell(data1: dict, data2: dict):
    sum = 0
    antall = 0
    lavest = None
    høyest = None
    for key,value in data1.items():
        if not key in data2.keys():
            continue
        diff = abs(value - data2[key])
        sum += diff
        antall += 1
        if lavest == None or lavest[1] > diff:
            lavest = [key, diff]
        if høyest == None or høyest[1] < diff:
            høyest = [key, diff]
    return sum/antall, høyest, lavest

def standard_avvik(datasett: list):
    gjennomsnitt = sum(datasett) / len(datasett)
    summ = 0
    for i in datasett:
        summ += (i - gjennomsnitt) ** 2
    dev = math.sqrt(1/(len(datasett)-1) * summ)
    return dev

def plot():
    temp_graf = plt.subplot(3, 2, 1)
    trykk_graf = plt.subplot(3, 2, 2)
    diff_graf = plt.subplot(3, 2, 4)
    ny_graf = plt.subplot(3, 2, 3)
    histogram = plt.subplot(3, 2, 5)
    stand_div_graf = plt.subplot(3, 2, 6)

    gjennomsnitts_tidspunkter, gjennomsnittstemperaturer, stand_dev = gjennomsnitts_utregning(data_lang['temperatur'], 30)

    tempfall_x1 = datetime.datetime(year=2021,month=6,day=11,hour=17,minute=31)
    tempfall_x2 = datetime.datetime(year=2021,month=6,day=12,hour=3,minute=5)
    tempfall_y1 = data_lang['temperatur'][tempfall_x1]
    tempfall_y2 = data_lang['temperatur'][tempfall_x2]
    tempfall_x = [tempfall_x1, tempfall_x2]
    tempfall_y = [tempfall_y1, tempfall_y2]

    tempfallsola_x1 = datetime.datetime(year=2021,month=6,day=11,hour=17)
    tempfallsola_x2 = datetime.datetime(year=2021,month=6,day=12,hour=3)
    tempfallsola_y1 = data_sola['temperatur'][tempfallsola_x1]
    tempfallsola_y2 = data_sola['temperatur'][tempfallsola_x2]
    tempfallsola_x = [tempfallsola_x1, tempfallsola_x2]
    tempfallsola_y = [tempfallsola_y1, tempfallsola_y2]

    temp_graf.plot(data_sola['temperatur'].keys(), data_sola['temperatur'].values(), label='Temperatur Sola', color='green')
    temp_graf.plot(data_lang['temperatur'].keys(), data_lang['temperatur'].values(), label='Temperatur UiS')
    temp_graf.plot(tempfall_x, tempfall_y, label='Temperaturfall maksimal til minimal', color='purple')
    temp_graf.plot(tempfallsola_x, tempfallsola_y, label='Temp. fall Sola', color='yellow')
    temp_graf.plot(gjennomsnitts_tidspunkter, gjennomsnittstemperaturer, label='Gjenomsnittstemp.', color='orange')
    
    temp_graf.set_ylabel('Temperatur (°C)')
    temp_graf.set_title('Temperatur')
    temp_graf.legend(loc='upper right')

    trykk_graf.plot(data_sola['trykk'].keys(), data_sola['trykk'].values(), label='Absolutt trykk Sola')
    trykk_graf.plot(data_lang['abs_trykk'].keys(), data_lang['abs_trykk'].values(), label='Absolutt trykk UiS')
    trykk_graf.plot(data_lang['baro_trykk'].keys(), data_lang['baro_trykk'].values(), label='Barometrisk trykk UiS')
    trykk_graf.plot(data_sauda['trykk'].keys(), data_sauda['trykk'].values(), label='Trykk Sauda')
    trykk_graf.plot(data_sinnes['trykk'].keys(), data_sinnes['trykk'].values(), label='Trykk Sinnes')

    trykk_graf.legend()
    trykk_graf.set_ylabel('Trykk (millibar)')
    trykk_graf.set_title('Trykk')

    differanse = {}
    for k,v in data_lang['baro_trykk'].items():
        differanse[k] = abs(v - data_lang['abs_trykk'][k])
    diff_gjennomsnitts_tidspunkter, diff_gjennomsnitts_trykk, std = gjennomsnitts_utregning(differanse, 10)
    diff_graf.plot(diff_gjennomsnitts_tidspunkter, diff_gjennomsnitts_trykk, label='Differanse absolutt og barometrisk trykk UiS')

    diff_graf.set_xlim(datetime.datetime(year=2021, month=6, day=9, hour=20), datetime.datetime(year=2021, month=6, day=14, hour=5))
    diff_graf.legend()
    diff_graf.set_ylabel('Differanse trykk')
    diff_graf.set_title('Differanse i trykk')

    ny_graf.plot(data_sinnes['temperatur'].keys(), data_sinnes['temperatur'].values(), label='Temp Sinnes')
    ny_graf.plot(gjennomsnitts_tidspunkter, gjennomsnittstemperaturer, label='Gjenomsnittstemp. UiS')
    ny_graf.plot(data_sola['temperatur'].keys(), data_sola['temperatur'].values(), label='Temperatur Sola')
    ny_graf.plot(data_sauda['temperatur'].keys(), data_sauda['temperatur'].values(), label='Temp Sauda')

    ny_graf.legend()
    ny_graf.set_ylabel('Temperatur')
    ny_graf.set_title('Temperatur nye stasjoner')

    stand_div_graf.errorbar(gjennomsnitts_tidspunkter, gjennomsnittstemperaturer, yerr=stand_dev, errorevery=30, capsize=2, ecolor='lightcoral', label='Gjennomsnittstemp UiS')

    stand_div_graf.legend()
    stand_div_graf.set_title('Gjennomsnittstemp UiS m/ standard-avvik')
    stand_div_graf.set_ylabel('Temp °C')

    histogram_data = []
    for v in data_lang['temperatur'].values():
        rundet = round(v)
        histogram_data.append(rundet)
    for v in data_sola['temperatur'].values():
        rundet = round(v)
        histogram_data.append(rundet)

    histogram.hist(histogram_data, label='Antall målinger hver grad')

    histogram.legend()
    histogram.set_xlabel('Temperatur')
    histogram.set_ylabel('Antall målinger, Sola og UiS')

    plt.show()
    
les_lang_fil()
les_fil('temperatur_trykk_sauda_sinnes_samme_tidsperiode.csv')
les_fil('temperatur_trykk_met_samme_rune_time_datasett.csv')
#debug()
diff_temp, temp_høy, temp_lav = gjennomsnittlig_forskjell(data_sola['temperatur'], data_lang['temperatur'])
diff_trykk, trykk_høy, trykk_lav = gjennomsnittlig_forskjell(data_sola['trykk'], data_lang['baro_trykk'])
print(f'\nGjennomsnittlig forskjell i temperatur mellom Sola og UiS er {diff_temp:.2f} °C. Høyest differanse: {temp_høy[0]} med {temp_høy[1]:.2f} °C, lavest: {temp_lav[0]} med {temp_lav[1]:.2f} °C')
print(f'Gjennomsnittlig forskjell i trykk mellom Sola og UiS er {diff_trykk:.2f} millibar. Høyest differanse: {trykk_høy[0]} med {trykk_høy[1]:.2f} mbar, lavest: {trykk_lav[0]} med {trykk_lav[1]:.2f} mbar\n')
plot()