import matplotlib.pyplot as plt
import pandas
import datetime

dataframe_lang: pandas.DataFrame = None
dataframe_sola: pandas.DataFrame = None

def les_sola():
    global dataframe_sola
    dataframe_sola = pandas.read_csv('temperatur_trykk_met_samme_rune_time_datasett.csv', delimiter=';', decimal=',', parse_dates=[2], dayfirst=True)
    dataframe_sola.rename(columns={
        'Tid(norsk normaltid)': 'dato',
        'Lufttemperatur': 'temp',
        'Lufttrykk i havnivå': 'abs_trykk'
    }, inplace=True)
    dataframe_sola.drop(index=dataframe_sola.last_valid_index(), inplace=True)
    print(dataframe_sola.info())
    print(dataframe_sola)

def les_lang_fil():
    global dataframe_lang
    dataframe_lang = pandas.read_csv('trykk_og_temperaturlogg_rune_time.csv', delimiter=';', decimal=',')
    dataframe_lang.rename(columns={
        'Dato og tid': 'dato',
        'Trykk - barometer (bar)': 'baro_trykk',
        'Trykk - absolutt trykk maaler (bar)': 'abs_trykk',
        'Temperatur (gr Celsius)': 'temp'
    }, inplace=True)
    starttid = datetime.datetime.strptime(dataframe_lang['dato'][0], '%m.%d.%Y %H:%M') + datetime.timedelta(seconds=8)
    dataframe_lang['dato'] = [starttid + datetime.timedelta(seconds=sekunder) for sekunder in dataframe_lang['Tid siden start (sek)']]
    dataframe_lang['baro_trykk'] = [trykk * 10 for trykk in dataframe_lang['baro_trykk']]
    dataframe_lang['abs_trykk'] = [trykk * 10 for trykk in dataframe_lang['abs_trykk']]
    print(dataframe_lang.info())
    print(dataframe_lang)

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


    return gyldige_tidspunkter, gjennomsnitts_liste_temperatur

def plot():
    temp_graf = plt.subplot(2, 1, 1)
    trykk_graf = plt.subplot(2, 1, 2)

    gjennomsnitts_tidspunkter, gjennomsnittstemperaturer = gjennomsnitts_utregning(dataframe_lang['dato'], dataframe_lang['temp'], 30)

    tempfall_start = datetime.datetime(year=2021,month=6,day=11,hour=17,minute=31,second=28)
    tempfall_slutt = datetime.datetime(year=2021,month=6,day=12,hour=3,minute=5,second=8)
    tempfall_y1 = dataframe_lang.loc[dataframe_lang['dato'] == tempfall_start]['temp'].values[0]
    tempfall_y2 = dataframe_lang.loc[dataframe_lang['dato'] == tempfall_slutt]['temp'].values[0]

    tempfall_x = [tempfall_start, tempfall_slutt]
    tempfall_y = [tempfall_y1, tempfall_y2]

    temp_graf.plot(dataframe_sola['dato'], dataframe_sola['temp'], label='Temperatur MET', color='green')
    temp_graf.plot(dataframe_lang['dato'], dataframe_lang['temp'], label='Temperatur')
    temp_graf.plot(tempfall_x, tempfall_y, label='Temperaturfall maksimal til minimal', color='purple')
    temp_graf.plot(gjennomsnitts_tidspunkter, gjennomsnittstemperaturer, label='Gjenomsnittstemp.', color='orange')

    temp_graf.set_ylabel('Temperatur (°C)')
    temp_graf.set_title('Temperatur')
    temp_graf.legend()

    trykk_graf.plot(dataframe_sola['dato'], dataframe_sola['abs_trykk'], label='Absolutt trykk MET', color='green')
    trykk_graf.plot(dataframe_lang['dato'], dataframe_lang['abs_trykk'], label='Absolutt trykk')

    rader_med_barotrykk = dataframe_lang.query('baro_trykk > 0')
    trykk_graf.plot(rader_med_barotrykk['dato'], rader_med_barotrykk['baro_trykk'], label='Barometrisk trykk', color='orange')

    trykk_graf.legend()
    trykk_graf.set_ylabel('Trykk (millibar)')
    trykk_graf.set_title('Trykk')

    plt.show()
    
les_lang_fil()
les_sola()
plot()
