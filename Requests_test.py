from phue import Bridge
import json
import requests
from datetime import date, timedelta, datetime  # Time is important
import pp

b = Bridge('192.168.2.134') #IP der Bridge

b.connect() #Connect to the Bridge, in theory only needs to be done once. but for simplicity I left it to run every execution

b.get_light('Hue Play 3') #The one Hue Play

b.get_light('Hue Play 1') #The seconed Hue Play

b.get_light('Hue Play 2') #The third Hue Play



# get the API data.
r = requests.get('https://www.berlin.de/lageso/gesundheit/infektionsepidemiologie-infektionsschutz/corona/tabelle-indikatoren-gesamtuebersicht/index.php/index/today.json')

                    #
print("Daten abgefragt: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "\n")

print(r.json()['index'][0]['datum']) # Get the date for the Data thats being used, so the printout is more organiesd even after a longer time of running.

print(r.json()['index'][0], "\n")  # print the latest info in the terminal.

# 7 tage inzidenz abfragen
tage = float(r.json()['index'][0]['7_tage_inzidenz'])
if tage >= 30:  # wenn über 30
    print("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- ROT","\n")
    b.set_light('Hue Play 3','on', True)
    b.set_light('Hue Play 3', {'xy': (0.675, 0.322)})
elif 20 <= tage <= 30:  # wenn unter 30
    print("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GELB","\n")
    b.set_light('Hue Play 3','on', True)
    b.set_light('Hue Play 3', {'xy': (0.4682, 0.476)})
elif tage <= 19:  # wenn unter 20
    print("7_tage_inzidenz -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GRÜN","\n")
    b.set_light('Hue Play 3','on', True)
    b.set_light('Hue Play 3', {'xy': (0.2083, 0.6713)})

#its_belegung
its = float(r.json()['index'][0]['its_belegung'])
if its >= 25:
    print("its_belegung -", float(r.json()['index'][0]['7_tage_inzidenz']), "- ROT","\n")
    b.set_light('Hue Play 1','on', True)
    b.set_light('Hue Play 1', {'xy': (0.675, 0.322)})
elif 15 <= its <= 25:
    print("its_belegung -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GELB","\n")
    b.set_light('Hue Play 1','on', True)
    b.set_light('Hue Play 1', {'xy': (0.4682, 0.476)})
elif its <= 14:
    print("its_belegung -", float(r.json()['index'][0]['7_tage_inzidenz']), "- GRÜN","\n")
    b.set_light('Hue Play 1','on', True)
    b.set_light('Hue Play 1', {'xy': (0.2083, 0.6713)})



#R-wert von letzter veränderung
index = 1
while float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']) == 0:
    index = index + 1
if float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']) != 0:
    rWert = float(r.json()['index'][index]['4_tage_r_wert_berlin_rki'])
    if rWert >= 1.2:
        print("4_tage_r_wert_berlin_rki -", float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']), "- ROT","\n")
        b.set_light('Hue Play 2','on', True)
        b.set_light('Hue Play 2', {'xy': (0.675, 0.322)})
    elif 1.1 <= rWert <= 1.2:
        print("4_tage_r_wert_berlin_rki -", float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']), "- GELB","\n")
        b.set_light('Hue Play 2','on', True)
        b.set_light('Hue Play 2', {'xy': (0.4682, 0.476)})
    elif rWert <= 1.0:
        print("4_tage_r_wert_berlin_rki -", float(r.json()['index'][index]['4_tage_r_wert_berlin_rki']), "- GRÜN","\n")
        b.set_light('Hue Play 2','on', True)
        b.set_light('Hue Play 2', {'xy': (0.2083, 0.6713)})
 
 

print("done")
print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
print("")

exit
#{"id":"877","datum":"2021-01-02","fallzahl":"98109","neue_faelle":"460","genesene":"79050","todesfaelle":"1285","7_tage_inzidenz":"130.7","rel_veraenderung_der_7_tage_inzidenz":"-21","its_belegung":"33.8","4_tage_r_wert_berlin_rki":"0"}],"item":[]}
