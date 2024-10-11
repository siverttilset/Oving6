import matplotlib.pyplot as plt
import csv
import datetime

data_sola: dict[str, dict[datetime.datetime, float]] = {
    'temperatur':{},
    'trykk':{}
}
data_lang: dict[str, dict[datetime.datetime, float]] = {
    'temperatur':{},
    'baro_trykk':{},
    'abs_trykk':{}
}

def debug():
    print(f'Sola temp: {list(data_sola["temperatur"].items())[:2]}')
    print(f'Sola trykk: {list(data_sola["trykk"].items())[:2]}')
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
                starttid = ny_datetime + datetime.timedelta(seconds=8)
                return starttid
            except ValueError:
                pass
    if norsk_format:
        return datetime.datetime.strptime(dato_streng, '%d.%m.%Y %H:%M')
    else:
        ny_datetime = starttid + datetime.timedelta(seconds=sekunder)
        return ny_datetime

def les_sola():
    with open('temperatur_trykk_met_samme_rune_time_datasett.csv', 'r', encoding='UTF-8') as fil:
        csv_objekt = csv.reader(fil, delimiter=';')
        header = next(csv_objekt)
        dato_indeks = header.index('Tid(norsk normaltid)')
        temp_indeks = header.index('Lufttemperatur')
        trykk_indeks = header.index('Lufttrykk i havnivå')
        for row in csv_objekt:
            if len(row) != len(header):
                continue
            dato = row[dato_indeks].strip()
            temp = row[temp_indeks].strip().replace(',', '.')
            trykk = row[trykk_indeks].strip().replace(',', '.')
            if dato and temp:
                dato_datetime = dato_konverterer(dato, True)
                data_sola['temperatur'][dato_datetime] = float(temp)
                if trykk:
                    data_sola['trykk'][dato_datetime] = float(trykk)

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


def gjennomsnitts_utregning(temp_data:dict, gjennomsnittsverdi:int):
    gjennomsnitts_liste_temperatur = []
    gyldige_tidspunkter = []
    temperatur = list(temp_data.values())
    tider = list(temp_data.keys())
    lengde_templiste = len(temperatur)
    for x,i in enumerate(tider):
        if x >= gjennomsnittsverdi and x < lengde_templiste-gjennomsnittsverdi:
            sum_temp = 0
            for v in range(-gjennomsnittsverdi, gjennomsnittsverdi+1, 1):
                sum_temp += float(temperatur[x+v])
            gjennomsnitts_liste_temperatur.append(float(f'{sum_temp/((gjennomsnittsverdi*2)+1):.2f}'))
            gyldige_tidspunkter.append(i)


    return gyldige_tidspunkter, gjennomsnitts_liste_temperatur

def plot():
    temp_graf = plt.subplot(2, 1, 1)
    trykk_graf = plt.subplot(2, 1, 2)

    gjennomsnitts_tidspunkter, gjennomsnittstemperaturer = gjennomsnitts_utregning(data_lang['temperatur'], 30)

    tempfall_x1 = datetime.datetime(year=2021,month=6,day=11,hour=17,minute=31, second=8)
    tempfall_x2 = datetime.datetime(year=2021,month=6,day=12,hour=3,minute=5, second=8)
    tempfall_y1 = data_lang['temperatur'][tempfall_x1]
    tempfall_y2 = data_lang['temperatur'][tempfall_x2]
    tempfall_x = [tempfall_x1, tempfall_x2]
    tempfall_y = [tempfall_y1, tempfall_y2]

    temp_graf.plot(data_sola['temperatur'].keys(), data_sola['temperatur'].values(), label='Temperatur MET', color='green')
    temp_graf.plot(data_lang['temperatur'].keys(), data_lang['temperatur'].values(), label='Temperatur')
    temp_graf.plot(tempfall_x, tempfall_y, label='Temperaturfall maksimal til minimal', color='purple')
    temp_graf.plot(gjennomsnitts_tidspunkter, gjennomsnittstemperaturer, label='Gjenomsnittstemp.', color='orange')

    temp_graf.set_ylabel('Temperatur (°C)')
    temp_graf.set_title('Temperatur')
    temp_graf.legend()

    trykk_graf.plot(data_sola['trykk'].keys(), data_sola['trykk'].values(), label='Absolutt trykk MET', color='green')
    trykk_graf.plot(data_lang['abs_trykk'].keys(), data_lang['abs_trykk'].values(), label='Absolutt trykk')
    trykk_graf.plot(data_lang['baro_trykk'].keys(), data_lang['baro_trykk'].values(), label='Barometrisk trykk', color='orange')

    trykk_graf.legend()
    trykk_graf.set_ylabel('Trykk (millibar)')
    trykk_graf.set_title('Trykk')

    plt.show()
    
les_lang_fil()
les_sola()
#debug()
plot()
