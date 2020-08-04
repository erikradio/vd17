import requests, csv, sys

#this script takes existing GNDs and runs them against the GND database to see if they have been updated with a new ID

with open(sys.argv[1],'r') as csvFile:
    for row in csv.DictReader(csvFile):
        bibData = {}

        gnd = row['GND-Nummer']
        if gnd != 'keine GND-Nummer vorhanden&nbsp':

            # print(gnd)
            url = 'https://hub.culturegraph.org/entityfacts/' + gnd
            r = requests.get(url)
            
            docs=r.json()
            newGND = ''
            try:
                r.raise_for_status()
                if docs['@id']:
                    newGND = docs['@id'].replace('https://d-nb.info/gnd/','')
                # do things if it doesn't
            except:
                newGND = 'NA'
                # do things if it does

            if gnd != newGND:
                print(gnd,newGND)
