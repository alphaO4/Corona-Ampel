from phue import Bridge
import json
import requests
from datetime import date, timedelta, datetime  # Time is important
import logging
# from apscheduler.schedulers.blocking import BlockingScheduler

b = Bridge('192.168.2.134') #IP der Bridge

b.connect() #Connect to the Bridge, in theory only needs to be done once, but for simplicity I left it to run every execution

b.get_light('Hue Play 3') #The one Hue Play

b.get_light('Hue Play 1') #The second Hue Play

b.get_light('Hue Play 2') #The third Hue Play

logging.basicConfig(filename='Requests.log',level=logging.INFO, format='%(message)s')  # logging conf

def Corona_ampel():
    
    # get the API data.
    # r = requests.get('https://www.berlin.de/lageso/gesundheit/infektionsepidemiologie-infektionsschutz/corona/tabelle-indikatoren-gesamtuebersicht/index.php/index/today.json')
    r = requests.get('https://www.berlin.de/lageso/gesundheit/infektionskrankheiten/corona/tabelle-indikatoren-gesamtuebersicht/index.php/index/all.json')

    abfrage = ("Daten abgefragt: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')) #Get the Current date, so its better to read. 
    logging.info(abfrage)
    print("Daten abgefragt: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "\n")

    print("Daten vom:", r.json()['index'][0]['datum'], "\n") # Get the date for the Data thats being used, so the printout is more organiesd even after a longer time of running.

    raw = ("Raw Data: ", r.json()['index'][0])  # print the latest info in the terminal.
    logging.info(raw)

    # 7 tage inzidenz abfragen
    tage = float(r.json()['index'][0]['7_tage_inzidenz'])
    if tage >= 30:  # wenn über 30
        data = ("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- ROT")
        logging.info(data) 
        print("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- ROT", "\n")
        b.set_light('Hue Play 3','on', True)
        b.set_light('Hue Play 3', {'xy': (0.675, 0.322)})
        
    elif 20 <= tage <= 30:  # wenn unter 30
        data = ("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GELB")
        logging.info(data)
        print("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GELB", "\n")
        b.set_light('Hue Play 3','on', True)
        b.set_light('Hue Play 3', {'xy': (0.4682, 0.476)})
        
    elif tage <= 19:  # wenn unter 20
        data = ("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GRUEN")
        logging.info(data)
        print("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GRÜN", "\n")
        b.set_light('Hue Play 3','on', True)
        b.set_light('Hue Play 3', {'xy': (0.2083, 0.6713)})
        

    #its_belegung
    its = float(r.json()['index'][0]['its_belegung'])
    if its >= 25:
        data = ("its_belegung -", float(r.json()['index'][0]['7_tage_inzidenz']), "- ROT")
        logging.info(data)
        print("its_belegung -", float(r.json()['index'][0]['7_tage_inzidenz']), "- ROT", "\n")
        b.set_light('Hue Play 1','on', True)
        b.set_light('Hue Play 1', {'xy': (0.675, 0.322)})
        
    elif 15 <= its <= 25:
        data = ("its_belegung -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GELB")
        logging.info(data)
        print("its_belegung -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GELB", "\n")
        b.set_light('Hue Play 1','on', True)
        b.set_light('Hue Play 1', {'xy': (0.4682, 0.476)})

    elif its <= 14:
        data = ("its_belegung -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GRUEN")
        logging.info(data)
        print("its_belegung -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GRÜN", "\n")
        b.set_light('Hue Play 1','on', True)
        b.set_light('Hue Play 1', {'xy': (0.2083, 0.6713)})

    #R-wert von letzter veränderung
    index = 1
    while float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']) == 0:
        index = index + 1
    if float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']) != 0:
        rWert = float(r.json()['index'][index]['4_tage_r_wert_berlin_rki'])
        if rWert >= 1.2:
            data = ("4_tage_r_wert_berlin_rki -", float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']), "- ROT")
            logging.info(data)
            print("4_tage_r_wert_berlin_rki -", float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']), "- ROT","\n")
            b.set_light('Hue Play 2','on', True)
            b.set_light('Hue Play 2', {'xy': (0.675, 0.322)})
            
        elif 1.1 <= rWert <= 1.2:
            data = ("4_tage_r_wert_berlin_rki -", float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']), "- GELB")
            logging.info(data)
            print("4_tage_r_wert_berlin_rki -", float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']), "- GELB","\n")
            b.set_light('Hue Play 2','on', True)
            b.set_light('Hue Play 2', {'xy': (0.4682, 0.476)})
            
        elif rWert <= 1.0:
            data = ("4_tage_r_wert_berlin_rki -", float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']), "- GRUEN")
            logging.info(data)
            print("4_tage_r_wert_berlin_rki -", float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']), "- GRÜN","\n")
            b.set_light('Hue Play 2','on', True)
            b.set_light('Hue Play 2', {'xy': (0.2083, 0.6713)})
            

    print("done")
    print("--------------------------------------------------------------------------------------------------------------------------------------------------")
    logging.info("--------------------------------------------------------------------------------------------------------------------------------------------------")

Corona_ampel()

# scheduler = BlockingScheduler()
# scheduler.add_job(Corona_ampel, 'cron', hour=19)
# '''scheduler.start()

#{"id":"877","datum":"2021-01-02","fallzahl":"98109","neue_faelle":"460","genesene":"79050","todesfaelle":"1285","7_tage_inzidenz":"130.7","rel_veraenderung_der_7_tage_inzidenz":"-21","its_belegung":"33.8","4_tage_r_wert_berlin_rki":"0"}],"item":[]}