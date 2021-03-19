from phue import Bridge
import json
import requests
from datetime import date, timedelta         #Time is important
import pp

b = Bridge('192.168.2.134')
b.connect()
b.get_light('Hue Play 3')

b.get_light('Hue Play 1')

b.get_light('Hue Play 2')

y1 = b.set_light('Hue Play 1', {'xy': (0.4325035269415173, 0.5007488105282536)})  # 7 Tage

y2 = b.set_light('Hue Play 2', {'xy': (0.4325035269415173, 0.5007488105282536)})  # its

y3 = b.set_light('Hue Play 3', {'xy': (0.4325035269415173, 0.5007488105282536)})  # r-wert

# Get the date from yesterday, so the printout is more organiesd even after a long time of running.
yesterday = date.today() - timedelta(days=1)
spl_word = yesterday                        #
print("Coronazahlen vom: " + str(spl_word), "\n")

# get the API data.
r = requests.get('Corona API')

print(r.json()['index'][0], "\n")  # print the latest info in the terminal.
#print("")

# 7 tage inzidenz abfragen
tage = float(r.json()['index'][0]['7_tage_inzidenz'])
if tage >= 30:  # wenn über 30
    print("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- ROT","\n")
    b.set_light('Hue Play 1','on', True)
    b.set_light('Hue Play 1', {'xy': (0.675, 0.322)})
elif 20 <= tage <= 30:  # wenn unter 30
    print("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GELB","\n")
    b.set_light('Hue Play 1','on', True)
    b.set_light('Hue Play 1', {'xy': (0.4325035269415173, 0.5007488105282536)})
elif tage <= 19:  # wenn unter 20
    print("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GRÜN","\n")
    b.set_light('Hue Play 1','on', True)
    b.set_light('Hue Play 1', {'xy': (0.4091, 0.518)})



#its_belegung
its = float(r.json()['index'][0]['its_belegung'])
if its >= 25:
    print("its_belegung -", float(r.json()['index'][0]['7_tage_inzidenz']), "- ROT","\n")
    b.set_light('Hue Play 2','on', True)
    b.set_light('Hue Play 2', {'xy': (0.675, 0.322)})
elif 15 <= its <= 25:
    print("its_belegung -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GELB","\n")
    b.set_light('Hue Play 2','on', True)
    b.set_light('Hue Play 2', {'xy': (0.4325035269415173, 0.5007488105282536)})
elif its <= 14:
    print("its_belegung -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GRÜN","\n")
    b.set_light('Hue Play 2','on', True)
    b.set_light('Hue Play 2', {'xy': (0.4091, 0.518)})



#R-wert von letzter veränderung
index = 1
while float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']) == 0:
    index = index + 1
if float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']) != 0:
    rWert = float(r.json()['index'][index]['4_tage_r_wert_berlin_rki'])
    if rWert >= 1.2:
        print("4_tage_r_wert_berlin_rki -", float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']), "- ROT","\n")
        b.set_light('Hue Play 3','on', True)
        b.set_light('Hue Play 3', {'xy': (0.675, 0.322)})
    elif 1.1 <= rWert <= 1.2:
        print("4_tage_r_wert_berlin_rki -", float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']), "- GELB","\n")
        b.set_light('Hue Play 3','on', True)
        b.set_light('Hue Play 3', {'xy': (0.4325035269415173, 0.5007488105282536)})
    elif rWert <= 1.0:
        print("4_tage_r_wert_berlin_rki -", float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']), "- GRÜN","\n")
        b.set_light('Hue Play 3','on', True)
        b.set_light('Hue Play 3', {'xy': (0.4091, 0.518)})
 
 

print("done")

#{"id":"877","datum":"2021-01-02","fallzahl":"98109","neue_faelle":"460","genesene":"79050","todesfaelle":"1285","7_tage_inzidenz":"130.7","rel_veraenderung_der_7_tage_inzidenz":"-21","its_belegung":"33.8","4_tage_r_wert_berlin_rki":"0"}],"item":[]}
