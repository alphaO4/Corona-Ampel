
from phue import Bridge
import json
import requests
from datetime import date, timedelta, datetime  # Time is important
import logging

# The IP of your Hue Bridge
HUE_BRIDGE_IP = "Philips-hue"
# Put your Philips Hue API Key for your Bridge into a text file and specify the location here

datei = open('Philips_Hue_API_Key.txt', 'r')
print(datei)

exit(0)


b = Bridge('192.168.2.134') # IP der Hue Bridge

b.connect() # Connect to the Bridge, in theory only needs to be done once, but for simplicity I left it to run every execution

b.get_light('Hue Play 1') #The first Hue Play
b.get_light('Hue Play 2') #The second Hue Play
b.get_light('Hue Play 3') # The third Hue Play

logging.basicConfig(filename='Requests.log',level=logging.INFO, format='%(message)s')  # logging conf

def Corona_ampel():
    
    # get the API data.
    r = requests.get('https://www.berlin.de/lageso/gesundheit/infektionskrankheiten/corona/tabelle-indikatoren-gesamtuebersicht/index.php/index/all.json')

    abfrage = ("Daten abgefragt: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')) #Get the Current date, so its better to read. 
    logging.info(abfrage)
    print("Daten abgefragt: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "\n")

    print("Daten vom:", r.json()['index'][0]['datum'], "\n") # Get the date for the Data thats being used, so the printout is more organised even after a longer time of running.

    raw = ("Raw Data: ", r.json()['index'][0])  # print the latest info in the terminal.
    logging.info(raw)

    '''
    7-Tage-Inzidenz
        Der Indikator steht auf Stufe 1 „grün“ solange die Anzahl der COVID-19-Neuinfektionen pro 100.000 Einwohner*innen in den letzten 7 Tagen unter 35 liegt
        Der Indikator steht auf Stufe 2 „gelb“, sobald die Anzahl der COVID-19-Neuinfektionen pro 100.000 Einwohner*innen in den letzten 7 Tagen bei mindestens 35 liegt
        Bei mindestens 100 Neuinfektionen pro 100.000 Einwohner*innen in den letzten 7 Tagen steht der Indikator auf Stufe 3 „rot“.
    '''
    sti = float(r.json()['index'][0]['7_tage_inzidenz'])
    # wenn über 100, dann ist dieser Wert ROT
    if sti >= 100:
        data = ("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- ROT")
        logging.info(data) 
        print("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- ROT", "\n")
        b.set_light('Hue Play 3','on', True)
        b.set_light('Hue Play 3', {'xy': (0.675, 0.322)})
    # wenn der Wert größer-gleich 35 und kleiner 100 ist, dann ist dieser Wert GELB        
    elif 35 <= sti <= 100:
        data = ("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GELB")
        logging.info(data)
        print("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GELB", "\n")
        b.set_light('Hue Play 3','on', True)
        b.set_light('Hue Play 3', {'xy': (0.4682, 0.476)})
    # wenn der Wert kleiner als 35 ist, dann ist dieses Licht GRÜN    
    elif sti <= 19:  # wenn unter 20
        data = ("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GRUEN")
        logging.info(data)
        print("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GRÜN", "\n")
        b.set_light('Hue Play 3','on', True)
        b.set_light('Hue Play 3', {'xy': (0.2083, 0.6713)})

    '''7-Tage-Hospitalisierungs-Inzidenz
    Die Zahl der Hospitalisierungen pro 100.000 Einwohner*innen in Zusammenhang mit einer SARS-CoV-2 Infektion in den letzten 7 Tagen ist ein Indikator für die Erkrankungsschwere.
    - Der Indikator steht auf Stufe 1 „grün“ solange die Anzahl der COVID-19-Hospitalisierungen pro 100.000 Einwohner*innen in den letzten 7 Tagen unter 4 liegt
    - Der Indikator steht auf Stufe 2 „gelb“, sobald die Anzahl der COVID-19-Hospitalisierungen pro 100.000 Einwohner*innen in den letzten 7 Tagen bei mindestens 4 liegt
    - Bei mindestens 8 COVID-19-Hospitalisierungen pro 100.000 Einwohner*innen in den letzten 7 Tagen steht der Indikator auf Stufe 3 „rot“.
    '''
    index = 1
    while float(r.json()['index'][index]['7_tage_hosp_inzidenz']) == None:
        index = index + 1
    if float(r.json()['index'][index]['7_tage_hosp_inzidenz']) != 0:
        sthi = float(r.json()['index'][index]['7_tage_hosp_inzidenz'])
        if sthi >= 8:
            data = ("7_tage_hosp_inzidenz -", float(r.json()['index'][index]['7_tage_hosp_inzidenz']), "- ROT")
            logging.info(data)
            print("7_tage_hosp_inzidenz -", float(r.json()['index'][index]['7_tage_hosp_inzidenz']), "- ROT","\n")
            b.set_light('Hue Play 2','on', True)
            b.set_light('Hue Play 2', {'xy': (0.675, 0.322)})
            
        elif 4 <= sthi < 8:
            data = ("7_tage_hosp_inzidenz -", float(r.json()['index'][index]['7_tage_hosp_inzidenz']), "- GELB")
            logging.info(data)
            print("7_tage_hosp_inzidenz -", float(r.json()['index'][index]['7_tage_hosp_inzidenz']), "- GELB","\n")
            b.set_light('Hue Play 2','on', True)
            b.set_light('Hue Play 2', {'xy': (0.4682, 0.476)})
            
        elif sthi < 4:
            data = ("7_tage_hosp_inzidenz -", float(r.json()['index'][index]['7_tage_hosp_inzidenz']), "- GRUEN")
            logging.info(data)
            print("7_tage_hosp_inzidenz -", float(r.json()['index'][index]['7_tage_hosp_inzidenz']), "- GRUEN","\n")
            b.set_light('Hue Play 2','on', True)
            b.set_light('Hue Play 2', {'xy': (0.2083, 0.6713)})

    '''
    COVID-19 ITS-Auslastung (Anteil der für COVID-19-Patient*innen benötigten Plätze auf Intensivstationen):
    Anteil der für COVID-19-Patient*innen benötigten Plätze auf Intensivstationen ist ein Indikator für die Krankheitslast durch COVID-19 und die Auslastung des Gesundheitssystems. Dieser Indikator steht für die Schwere der Infektionsfolgen.
    - Anteil < 5 %: Indikator auf Stufe 1 „grün“
    - Anteil = 5 %: Indikator auf Stufe 2 „gelb“
    - Anteil = 20 %: Indikator auf Stufe 3 „rot“
    '''
    indexx = 0
    # finde den letzen nicht-null (None) Wert
    while r.json()['index'][indexx]['its_belegung'] == None:
        indexx = indexx + 1
    its = float(r.json()['index'][indexx]['its_belegung'])
    if its >= 20:
        data = ("its_belegung -", float(r.json()['index'][indexx]['its_belegung']), "- ROT")
        logging.info(data)
        print("its_belegung -", float(r.json()['index'][indexx]['its_belegung']), "- ROT", "\n")
        b.set_light('Hue Play 1','on', True)
        b.set_light('Hue Play 1', {'xy': (0.675, 0.322)})
        
    elif 5 <= its < 20:
        data = ("its_belegung -", float(r.json()['index'][indexx]['its_belegung']), "- GELB")
        logging.info(data)
        print("its_belegung -", float(r.json()['index'][indexx]['its_belegung']), "- GELB", "\n")
        b.set_light('Hue Play 1','on', True)
        b.set_light('Hue Play 1', {'xy': (0.4682, 0.476)})

    elif its < 5:
        data = ("its_belegung -", float(r.json()['index'][indexx]['its_belegung']), "- GRUEN")
        logging.info(data)
        print("its_belegung -", float(r.json()['index'][indexx]['its_belegung']), "- GRÜN", "\n")
        b.set_light('Hue Play 1','on', True)
        b.set_light('Hue Play 1', {'xy': (0.2083, 0.6713)})
              

    print("done")
    print("--------------------------------------------------------------------------------------------------------------------------------------------------")
    logging.info("--------------------------------------------------------------------------------------------------------------------------------------------------")

Corona_ampel()