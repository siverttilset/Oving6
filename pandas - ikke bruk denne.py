import matplotlib.pyplot as plt
import pandas
import datetime

def les_sola() -> None:
    dataframe_sola = pandas.read_csv('temperatur_trykk_met_samme_rune_time_datasett.csv', delimiter=';', decimal=',', parse_dates=[2], dayfirst=True)
    dataframe_sola.rename(columns={
        'Tid(norsk normaltid)': 'dato',
        'Lufttemperatur': 'temp',
        'Lufttrykk i havnivå': 'abs_trykk'
    }, inplace=True)
    dataframe_sola.drop(index=dataframe_sola.last_valid_index(), inplace=True)  # slette den siste raden som ikke inneholder noe data
    # print(dataframe_sola.info())
    # print(dataframe_sola)
    return dataframe_sola

def les_lang_fil() -> None:
    dataframe_lang = pandas.read_csv('trykk_og_temperaturlogg_rune_time.csv', delimiter=';', decimal=',')
    dataframe_lang.rename(columns={
        'Dato og tid': 'dato',
        'Trykk - barometer (bar)': 'baro_trykk',
        'Trykk - absolutt trykk maaler (bar)': 'abs_trykk',
        'Temperatur (gr Celsius)': 'temp'
    }, inplace=True)
    starttid = datetime.datetime.strptime(dataframe_lang['dato'][0], '%m.%d.%Y %H:%M') + datetime.timedelta(seconds=8)  # Lage datetime objekt for første raden, bruke denne til å få ut alle de andre ved hjelp av sekunder
    dataframe_lang['dato'] = [starttid + datetime.timedelta(seconds=sekunder) for sekunder in dataframe_lang['Tid siden start (sek)']]  # Sette hver dato til et datetime objekt som er sekunder_siden_start + starttiden
    dataframe_lang['baro_trykk'] = [trykk * 10 for trykk in dataframe_lang['baro_trykk']]
    dataframe_lang['abs_trykk'] = [trykk * 10 for trykk in dataframe_lang['abs_trykk']]
    # print(dataframe_lang.info())
    # print(dataframe_lang)
    return dataframe_lang

def gjennomsnitts_utregning(tider:list, temperatur:list, gjennomsnittsverdi:int) -> tuple[list, list]:
    gjennomsnitts_liste_temperatur = []
    gyldige_tidspunkter = []
    for index,dato in enumerate(tider[gjennomsnittsverdi:len(tider)-gjennomsnittsverdi], gjennomsnittsverdi):
        sum_temp = 0
        temp_rundt = temperatur[index-gjennomsnittsverdi:index+gjennomsnittsverdi+1]
        for temp in temp_rundt:
            sum_temp += temp
        gjennomsnitts_liste_temperatur.append(sum_temp/((gjennomsnittsverdi*2)+1))
        gyldige_tidspunkter.append(dato)
    return gyldige_tidspunkter, gjennomsnitts_liste_temperatur

def plot() -> None:
    temp_graf = plt.subplot(2, 1, 1)
    trykk_graf = plt.subplot(2, 1, 2)

    gjennomsnitts_tidspunkter, gjennomsnittstemperaturer = gjennomsnitts_utregning(dataframe_lang['dato'], dataframe_lang['temp'], 30)

    tempfall_tid = dataframe_lang.query('"2021-06-11 17:31:28" <= dato <= "2021-06-12 03:05:08"') # Hente ut alle punkter innenfor klokkeslett oppgitt i oppgaven til tempfall
    index_max_temp = tempfall_tid['temp'].idxmax()   # finne index til høyeste temp
    index_min_temp = tempfall_tid['temp'].idxmin()   # finne index til laveste temp
    rad_max_temp = tempfall_tid.loc[index_max_temp]  # hente ut raden med høyest temp
    rad_min_temp = tempfall_tid.loc[index_min_temp]  # hente ut raden med lavest temp

    temp_graf.plot(dataframe_sola['dato'], dataframe_sola['temp'], label='Temperatur MET', color='green')
    temp_graf.plot(dataframe_lang['dato'], dataframe_lang['temp'], label='Temperatur')
    temp_graf.plot([rad_min_temp['dato'], rad_max_temp['dato']], [rad_min_temp['temp'], rad_max_temp['temp']], label='Temperaturfall maksimal til minimal', color='purple')
    temp_graf.plot(gjennomsnitts_tidspunkter, gjennomsnittstemperaturer, label='Gjenomsnittstemp.', color='orange')

    temp_graf.set_ylabel('Temperatur (°C)')
    temp_graf.set_title('Temperatur')
    temp_graf.legend().set_loc('upper left')

    trykk_graf.plot(dataframe_sola['dato'], dataframe_sola['abs_trykk'], label='Absolutt trykk MET', color='green')
    trykk_graf.plot(dataframe_lang['dato'], dataframe_lang['abs_trykk'], label='Absolutt trykk')

    rader_med_barotrykk = dataframe_lang.query('baro_trykk > 0')
    trykk_graf.plot(rader_med_barotrykk['dato'], rader_med_barotrykk['baro_trykk'], label='Barometrisk trykk', color='orange')
    
    trykk_graf.legend().set_loc('upper left')
    trykk_graf.set_ylabel('Trykk (millibar)')
    trykk_graf.set_title('Trykk')

    plt.show()

dataframe_lang: pandas.DataFrame = les_lang_fil()
dataframe_sola: pandas.DataFrame = les_sola()
plot()